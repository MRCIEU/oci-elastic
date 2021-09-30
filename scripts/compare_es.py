import config
import os
import timeit
import datetime
import time
import random
import logging
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import re
import hashlib

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
return_limit=100000

# gwas/snp/range limits
gwas_list_length=2
snp_list_length=1
pval_filter=1e-2
range_size=100

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

# for testing multiple ES clusters
es_hosts = [
    {'host':config.elastic_host1,'port':config.elastic_port1,'name':config.elastic_name1},
    {'host':config.elastic_host2,'port':config.elastic_port2,'name':config.elastic_name2},
    ]

#elasticsearch connection
def es_connection(host=config.elastic_host1,port=config.elastic_port1,name=config.elastic_name1):
    print('Connecting to',host,port,name)
    try:
        es = Elasticsearch(
            [{'host': host, 'port': port}],
        )
        if not es.ping():
            raise ValueError("Connection failed")
        else:
            #print('Connection OK')
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
    t,count,res,md5 = es_query(bodyText,host=es_hosts[0])
    snpList=[]
    #print(res['hits']['total']['value'],'SNPs')
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

index_name='ukb-a,ukb-b,ukb-d,ieu-a,ebi-a,eqtl-a,met-a,met-b,met-c,prot-a,prot-b,ubm-a,finn-a'

def es_query(bodyText,host,index=index_name):
    es = es_connection(host['host'],host['port'],host['name'])

    print('index = ',index)
    #need to create separate connection each time to avoid issues with mulitprocessing
    t1 = time.time()
    #print('es connection',time.process_time() - t)
    res=es.search(
        request_timeout=60,
        index=index,
        body=bodyText
        )
    t2 = time.time()
    t = t2-t1
    # get total
    total = 0
    #print(res['responses'])
    # v6 and v7 ES return total in different format
    # actually, total is not always reliable, best to actually count
    # https://www.elastic.co/guide/en/elasticsearch/reference/master/search-your-data.html#track-total-hits
    total = len(res['hits']['hits'])
    #try:
    #    total += int(res['hits']['total']['value'])
    #except:
    #    total += int(res['hits']['total'])
    md5 = hashlib.md5(str(res['hits']['hits']).encode('utf-8')).hexdigest()
    return t, total, res, md5

def es_mquery(host,body):
    es = es_connection(host['host'],host['port'],host['name'])
    t1 = time.time()
    res = es.msearch(body = body)
    t2 = time.time()
    t = t2-t1

    # get total
    total = 0
    hits = []
    for r in res['responses']:
        #print(res['responses'])
        # v6 and v7 ES return total in different format
        # actually, total is not always reliable, best to actually count
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/search-your-data.html#track-total-hits
        total += len(r['hits']['hits'])
        hits.append(r['hits']['hits'])
        #try:
        #    total += int(r['hits']['total']['value'])
        #except:
        #   total += int(r['hits']['total'])
    print(hits)
    md5 = hashlib.md5(str(hits).encode('utf-8')).hexdigest()
    return t, total, res, md5

def et1(host):
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
        #print('Running batch',b,batches[b])
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
    es = es_connection(host['host'],host['port'],host['name'])
    #print(request)
    t, total, res, md5 = es_mquery(host,request)
    return t,total, md5

def et2(host):
    filterData=[
			{"terms":{"snp_id":q2_snpList}}
			]
    #print(filterData)
    bodyText={
        "size":return_limit,
        "query": {
            "bool" : {
                "filter" : filterData
            }
        },
        "post_filter": {
            "range": {"p": {"lt": pval_filter}}
        }
    }
    es = es_connection(host['host'],host['port'],host['name'])
    t, total, res, md5 = es_query(host=host,bodyText=bodyText)
    return t,total, md5

def et3(host):
    filterData=[
			{"terms":{"chr":[q3_chr]}},
			{"range": {'position': {'gte': q3_start, 'lte': q3_end}}}
			]
    bodyText={
        #"track_total_hits": True,
        "size":return_limit,
        "query": {
            "bool" : {
                "filter" : filterData
            }
        }
    }
    print(filterData)
    es = es_connection(host['host'],host['port'],host['name'])
    t, total, res, md5 = es_query(host=host,bodyText=bodyText)
    # check if res actually contains all hits
    print('et3',total,len(res['hits']['hits']))
    return t,total,md5

def run_tests(logger,name=0,db_type='',host=''):
    if db_type == 'es':
        t,c,md5 = et1(host)
        logger.info(f"{host['name']} et1 {name} {t} {c} {md5}")
        t,c,md5 = et2(host)
        logger.info(f"{host['name']} et2 {name} {t} {c} {md5}")
        t,c,md5 = et3(host)
        logger.info(f"{host['name']} et3 {name} {t} {c} {md5}")
    else:
        exit()

def single():
    print('Doing single proc tests...')
    for i in range(0,run_num):
        print('Single',i)

        # q1
        global q1_gwasList, q1_snpList, q2_snpList, q3_chr, q3_start, q3_end
        q1_gwasList = random.sample(gwas_ids, gwas_list_length)
        q1_snpList=random.sample(random_snps, snp_list_length)

        # q2
        q2_snpList=random.sample(random_snps, 1)

        # q3 
        q3_chr=str(random.randrange(1, 22))
        q3_start=random.randrange(10000000, 20000000)
        q3_end=q3_start+range_size

        for h in es_hosts:
            #run_tests(logger=logger1,db_type='oa')
            run_tests(logger=logger1,name=f's{i}:{run_num}',db_type='es',host=h)




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

            for h in es_hosts:
                p1 = Process(target=run_tests,args=(logger2,f'm{i}:{proc_num}','es',h))
                p1.start()
                proc.append(p1)
        for p in proc:
            p.join()

def read_log(log_file):
    df = pd.read_csv(log_file,sep=' ',names=['data','time','sm','version','test','run_num','run_time','count','md5'])
    df = df.sort_values(by=['test','run_num','version'])
    print(df)
    g = df.groupby(['test','version']).mean()
    print(g)

def basic_test():
    #run single tests
    single()

    #run mutliprocessing tests
    #multi(run_num)
    

def multi_test():
    for i in multi_range:
        multi(i)

if __name__ == "__main__":

    ##check connections

    print('Testing Elastic connection...')
    for h in es_hosts:
        es_connection(host=h['host'],port=h['port'],name=h['name'])

    create_random_snp_data()
    create_random_gwas_data()

    basic_test()
    #multi_test()

    read_log(main_log)

