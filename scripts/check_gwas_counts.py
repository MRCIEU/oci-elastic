from elasticsearch import Elasticsearch
import config

#elasticsearch connection
try:
    es = Elasticsearch(
        [{'host': config.elastic_host,'port': config.elastic_port}],
    )
    if not es.ping():
        raise ValueError("Connection failed")
    else:
        print('Connected')
except Exception as e: 
    print('Elasticsearch error:',e)
    exit()

def gwas_count(gwas_id,index_name):
    filterData=[
			{"term":{"gwas_id":gwas_id}},
			]
    bodyText={
        "size":1,
        "query": {
            "bool" : {
                "filter" : filterData
            }
        }
    }
    res=es.search(
        request_timeout=60,
        index=index_name,
        body=bodyText
        )
    return res

def read_logs(log_file):
    with open(log_file,'r') as f:
        for line in f:
            l = line.split(' ')
            gwas_id = l[0]
            index_count=l[-1].rstrip()
            #print(gwas_id,index_count)
            index_name = "-".join(gwas_id.split('-')[0:2])
            gwas_name = gwas_id.split('-')[3].replace('.log','')
            res = gwas_count(gwas_id=gwas_name,index_name=index_name)
            try:
                if int(index_count) != int(res['hits']['total']):
                    print('Error',index_name,gwas_name,index_count,res['hits']['total'])      
                else:
                    print('Good',index_name,gwas_name,index_count,res['hits']['total'])    
            except:
                  print('Error',index_name,gwas_name,index_count,res['hits']['total'])   

if __name__ == '__main__':
    read_logs(config.log_file)
#res = gwas_count(es,gwas_id='ENSG00000100985',index_name='eqtl-a')
#print(res)
