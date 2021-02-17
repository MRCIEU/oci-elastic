import config
import os
import timeit
import datetime
import time
import random
import logging
import matplotlib.pyplot as plt
import numpy as np
import requests
import re
from elasticsearch import Elasticsearch
from multiprocessing import Process

#set up two loggers
today = datetime.date.today()
formatter = logging.Formatter('%(asctime)s %(name)s %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logging.getLogger("elasticsearch").disabled = True

    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

main_log = f'logs/run_{today}.log'
logger1 = setup_logger(name='s', log_file=main_log)
logger2 = setup_logger(name='m', log_file=main_log)
#logger3 = setup_logger(name='SQL', log_file=f'logs/run_sql_{today}.log')


#globals
repeat=1
run_num=10
gwas_list_length=2
snp_list_length=2
pval_filter=1e-2
#range_size=1000000
range_size=1000
return_limit=100000
random_snps=[]
multi_range = [1,2,5,50]

gwas_ids = []
q1_gwasList = []
q1_snpList = []

#q2
q2_snpList = []

#q3
q3_chr=0
q3_start=0
q3_end=0

#three queries
#q1 - list of random GWAS (length gwas_list_length) and list of random SNPs (length snp_list_length)
#q2 - PheWAS of 1 random SNP with pvalue filter (pval_filter)
#q3 - Range query (random 1000 bp range within pos 10000000 and 20000000 on random chromosome)

#each query is performed sequentially and concurrently according to [1,2,5,10,15,20]

#elasticsearch connection
def es_connection():
    #print('Testing Elasticsearch connection...')
    try:
        es = Elasticsearch(
            [{'host': config.elastic_host,'port': config.elastic_port}],
        )
        if not es.ping():
            raise ValueError("Connection failed")
        else:
            return es
    except Exception as e: 
        print('Elasticsearch error:',e)
        exit()

def create_random_snp_data():
    #create list of random SNPs
    print('Getting random SNPs')
    random_gwas=random.randrange(0, 1000)
    gwasList=[str(random_gwas)]
    filterData=[
            {"terms":{"gwas_id":gwasList}},
            ]
    bodyText={
        "size":10000,
        "query": {
            "bool" : {
                "filter" : filterData
            }
        }
    }
    print(filterData)
    res = es_query(bodyText)
    snpList=[]
    print(res['hits']['total'],'SNPs')
    for res in res['hits']['hits']:
        snpList.append(res['_source']['snp_id'])
    global random_snps
    random_snps = snpList
    return random_snps

def create_random_gwas_data():
    print('Getting random GWAS IDs...')
    og='open_gwas.txt'
    global gwas_ids
    if os.path.exists(og):
        print('OpenGWAS data already downloaded')
        with open(og) as f:
            for line in f:
                gwas_ids.append(line.strip())
    else:
        gwas_api_url='http://gwasapi.mrcieu.ac.uk/gwasinfo'
        gwas_res = requests.get(gwas_api_url).json()
        o = open(og,'w')
        for i in gwas_res.keys():
            o.write(i+'\n')
        o.close()
        gwas_ids = list(gwas_res.keys())
    #remove eqtls
    gwas_ids = [x for x in gwas_ids if not x.startswith('eqtl')]
    print(len(gwas_ids),'OpenGWAS IDs')
    return gwas_ids

index_name='ukb-a,ukb-b,ukb-d,ieu-a,ebi-a,eqtl-a,met-a,met-b,met-c,prot-a,prot-b,ubm-a'

def es_query(bodyText,index=index_name):
    print('index = ',index)
    #need to create separate connection each time to avoid issues with mulitprocessing
    t = time.process_time()
    es = es_connection()
    #print('es connection',time.process_time() - t)
    res=es.search(
        request_timeout=60,
        index=index,
        body=bodyText
        )
    #print(res)
    return res

def et1():
    #replicate API and run each batch separately - seems to be slower than running against all indexes at once!!!
    total = 0
    request = []
    batches = {}
    for i in q1_gwasList:
        reg = r'^([\w]+-[\w]+)-([\w]+)'
        study_prefix, study_id = re.match(reg, i).groups()
        print(study_prefix,study_id) 
        if study_prefix in batches:
            batches[study_prefix].append(study_id)
        else:
            batches[study_prefix] = [study_id]
    #batches = list(set(batches))
    for b in batches:
        req_head = {'index': b}
        print('Running batch',b,batches[b])
        filterData=[
                {"terms":{"gwas_id":batches[b]}},
                {"terms":{"snp_id":q1_snpList}}
                ]
        bodyText={
            "size":return_limit,
            "query": {
                "bool" : {
                    "filter" : filterData
                }
            }
        }
        request.extend([req_head, bodyText])
    es = es_connection()
    print(request)
    res = es.msearch(body = request)
    #print(res)
    for r in res['responses']:
        #print(res['responses'])
        total += int(r['hits']['total'])
    #todo filter out results and match to index batches...
    print('e1m total',total)
    return res


def run_tests(logger,name=0,db_type=''):
    if db_type == 'es':
        q1_time = timeit.timeit(et1,number=repeat)
        logger.info('e1.'+str(name)+':'+str(q1_time))
    elif db_type == 'oa':
        q1_time = timeit.timeit(ot1,number=repeat)
        logger.info('o1.'+str(name)+':'+str(q1_time))
        logger3.info('o1.'+str(name)+' '+str(q1_time))
    else:
        exit()

def single():
    print('Doing single proc tests...')
    for i in range(0,run_num):
        print('Single',i)
        global q1_gwasList, q1_snpList, q2_snpList, q3_chr, q3_start, q3_end
        q1_gwasList = random.sample(gwas_ids, gwas_list_length)
        q1_snpList=random.sample(random_snps, snp_list_length)

        #run_tests(logger=logger1,db_type='oa')
        run_tests(logger=logger1,name=0,db_type='es')

def multi(proc_num):
    print('Doing multiproc tests...')
    for i in range(0,run_num):
        proc=[]
        for i in range(0,proc_num):
            #create shared data sets and male global
            #q1
            global q1_gwasList, q1_snpList, q2_snpList, q3_chr, q3_start, q3_end
            q1_gwasList = random.sample(gwas_ids, gwas_list_length)
            q1_snpList=random.sample(random_snps, snp_list_length)


            p1 = Process(target=run_tests,args=(logger2,proc_num,'es'))
            p1.start()
            proc.append(p1)
        for p in proc:
            p.join()

def basic_test():
    #run single tests
    single()

    #run mutliprocessing tests
    multi(run_num)
    
    #plot things
    #plot_basic_times(main_log)

def multi_test():
    for i in multi_range:
        multi(i)

    #plot things
    #plot_multi_times(main_log)

if __name__ == "__main__":

    ##check connections

    print('Testing Elastic connection...')
    es_connection()

    create_random_snp_data()
    create_random_gwas_data()

    #basic_test()
    multi_test()


