from elasticsearch import Elasticsearch
import config

#elasticsearch connection
def es_connection():
    try:
        es = Elasticsearch(
            [{'host': config.elastic_host,'port': config.elastic_port}],
        )
        if not es.ping():
            raise ValueError("Connection failed")
        else:
            print('Connected')
            return es
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
    es = es_connection()
    res=es.search(
        request_timeout=60,
        index=index_name,
        body=bodyText
        )
    return res

es_connection()
res = gwas_count(gwas_id='ENSG00000100985',index_name='eqtl-a')
print(res)
