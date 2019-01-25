import requests
import random
import time
import json
import os
import config
import gzip
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from collections import deque
from collections import defaultdict
from datetime import datetime


#tests mrbase elasticsearch index with 7 queries, each run 10 times and average calcualted
#to run - python test.py
#to run in parallel - for i in {1..10}; do python test.py &  done

#to compare runs
#for i in run_logs/*; do tail $i | grep 'q5'; done

#jojo
#es = Elasticsearch(
#	[{'host': 'jojo.epi.bris.ac.uk','port': 9200}]
#)

timeout=120

es = Elasticsearch(
	[{'host': config.elastic_host,'port': config.elastic_port}],
	#http_auth=(config.elastic_user, config.elastic_password),
)

def es_study_search(study_id, index_name):
	res=es.search(
		request_timeout=timeout,
		index=index_name,
		body={
			"size":1,
			"query": {
				"bool" : {
					"filter" : [
						{"term":{"study_id":study_id}},
					]
				}
			}
		})
	total=res['hits']['total']
	#print(res)
	return(total)

def create_random_list(min,max,num):
	r = random.sample(range(min,max),num)
	return r

def create_query(num_studies,num_snps,pval):
	maxStudy=500
	maxSnp=10000000
	filterSelect = {}
	study_list=snp_list=[]
	if num_studies != 'NA':
		study_list=create_random_list(1,maxStudy,num_studies)
		#filterSelect['study'] = study_list
		filterSelect['study_id'] = study_list
	if num_snps != 'NA':
		snp_list=create_random_list(1,maxSnp,num_snps)
		snp_list = ['rs'+str(s) for s in snp_list]
		filterSelect['snp_id'] = snp_list
	if pval != 'NA':
		filterSelect['p'] = pval
	print len(study_list),'studies',len(snp_list),'snps'

	filterData=[]
	for f in filterSelect:
		if f in ['study_id','snp_id']:
			filterData.append({"terms" : {f:filterSelect[f]}})
		else:
			filterData.append({"range" : {"p": {"lt": filterSelect[f]}}})
	return filterData

def run_query(filterData,index,size=1000):
	#print(index)
	start=time.time()
	res=es.search(
		request_timeout=timeout,
		index=index,
		#index="ukb-b",
		#index="pqtl-a",
		#index="mrb-original",
		#index="mrbase-opt-disk",
		#doc_type="assoc",
		body={
			"size":size,
			#{}"profile": True,
			"query": {
				"bool" : {
					"filter" : filterData
				}
			}

		})
	end = time.time()
	t=round((end - start), 4)
	print "Time taken:",t, "seconds"
	print res['hits']['total']
	return t,res['hits']['total']

def run_tests(index='',size=10):
	repeat=10
	queryData = {
		'q1':[1,1,'NA'],
		'q2':[100,1,'NA'],
		'q3':[1,100,'NA'],
		'q4':[1,'NA','NA'],
		'q5':[100,100,'NA'],
		'q6':[1,'NA',1e-8],
		'q7':[100,'NA',1e-8]
	}
	aTime = {'q1':0,'q2':0,'q3':0,'q4':0,'q5':0,'q6':0,'q7':0}
	for i in range(1,repeat):
		print '\n-----',i,'-----'
		for q in sorted(queryData):
			print '########### '+str(q)+' ###########'
			filterData = create_query(num_studies=queryData[q][0],num_snps=queryData[q][1],pval=queryData[q][2])
			#print(filterData)
			t,time = run_query(filterData=filterData,index=index,size=size)
			aTime[q]+=t

	print "\nResults"
	timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
	o=open('./run_logs/run_times_'+str(timestr)+'.txt','w')
	for a in sorted(aTime):
		avA = aTime[a]/repeat
		o.write(str(a)+' '+str(avA)+'\n')
		print a,avA

def test_query():
	res=es.search(
		request_timeout=timeout,
		index="MRB",
		doc_type="assoc",
		body={
			"size":5,
			"query": {
				"bool" : {
					"filter" : [
						{"terms":{"study_id":['965']}},
						{"terms":{"snp_id":['rs12740374','rs4751870','rs964184','rs7412']}},
						#{"range":{"p": {"lt":1e-8}}}
					]
				}
			}
		})
	print json.dumps(res,indent=4)

def db_test():
	snp_list=[]
	#with open('monocyte.clumped.instruments.finalrevised.csv') as f:
	#	next(f)
	#	for line in f:
	#		rs = line.split(',')[0]
	#		snp_list.append(rs)
	print len(snp_list)
	res=es.search(
		request_timeout=timeout,
		index="mrb-test",
		doc_type="assoc",
		body={
			"size":5,
			"query": {
				"bool" : {
					"filter" : [
						{"terms":{"study_id":['MRB:1']}},
						#{"terms":{"snp_id":snp_list}},
						#{"range":{"p": {"lt":1e-8}}}
					]
				}
			}
		})
	print json.dumps(res,indent=4)

#all bn data = 10879181
def check_bn_totals():
	#bn test
	for i in range(1,597):
		print i
		res=es.search(
			request_timeout=timeout,
			index="ukb-a-test",
			doc_type="assoc",
			body={
				"size":2,
				"query": {
					"bool" : {
						"filter" : [
							{"terms":{"study_id":[i]}},
							#{"terms":{"snp_id":['rs7949566']}},
							#{"range":{"p": {"lt":1e-2}}}
						]
					}
				}
			})
		#print json.dumps(res,indent=4)
		print res['hits']['total']

def check_mrb_totals():
	#mrb test
	#for i in range(1,1120):
	for i in range(1120,1126):
		print '### '+str(i)
		res=es.search(
			request_timeout=timeout,
			index="mrbase-original",
			doc_type="assoc",
			body={
				"size":2,
				"query": {
					"bool" : {
						"filter" : [
							{"terms":{"study_id":[i]}},
							#{"terms":{"snp_id":['rs7949566']}},
							#{"range":{"p": {"lt":1e-2}}}
						]
					}
				}
			})
		print json.dumps(res,indent=4)
		#print res['hits']['total']

def get_snps():
	res=es.search(
		request_timeout=timeout,
		index="ukb-a",
		doc_type="assoc",
		body={
			"size":0,
			"aggs" : {
			    "uniq_snps" : {
					"terms" : { "field" : "snp_id" }
				}
			}
		})
	o = gzip.open('ukb-a-snpcounts.txt','w')
	o.write(json.dumps(res))

def proxies_test():
	snps = ['rs115740542', 'rs1913707', 'rs2622873', 'rs2785988', 'rs75621460', 'rs34811474', 'rs330050', 'rs317630', 'rs6966540', 'rs62182810', 'rs1560707', 'rs13107325', 'rs10502437', 'rs2856821', 'rs11031191', 'rs2171126', 'rs55698100', 'rs3771501', 'rs1149620', 'rs35206230', 'rs1126464', 'rs798726', 'rs919642', 'rs10218792', 'rs12154055']
	snps = ['rs115740542', 'rs1913707', 'rs2622873', 'rs2785988', 'rs75621460', 'rs34811474']
	filterData = [{'terms': {'target': snps}}, {'range': {'rsq': {'gte': 0.8}}}, {'term': {'palindromic': 0}}]
	ESRes=es.search(
        request_timeout=timeout,
        index='mrb-proxies',
        doc_type="proxies",
        body={
                "size":100000,
                "query": {
                        "bool" : {
                                "filter" : filterData
                        }
                }
        })
	#print ESRes
	hits = ESRes['hits']['hits']
	for hit in hits:
		print hit['_source']['target'],hit['_source']['proxy']
	print len(hits)

def count_test():
	print 'count_test'
	c=es.count(index='ukb-b',request_timeout=timeout)
	print c

def create_test(assoc_data, study_id, index_name):
	bulk_data = []
	counter=0
	start = time.time()
	chunkSize = 100000
	with gzip.open(assoc_data) as f:
		#next(f)
		for line in f:
			counter+=1
			if counter % 100000 == 0:
				end = time.time()
				t=round((end - start), 4)
				print(assoc_data,t,counter)
			if counter % chunkSize == 0:
				deque(helpers.streaming_bulk(client=es,actions=bulk_data,chunk_size=chunkSize,request_timeout=timeout),maxlen=0)
				bulk_data = []
			#print(line.decode('utf-8'))
			l = line.decode('utf-8').split('\t')
			if l[0].startswith('rs'):
				effect_allele_freq = beta = se = p = n = ''
				try:
					effect_allele_freq = float(l[3])
				except ValueError:
					logger.info(l[0],study_id,assoc_data,counter,'effect_allel_freq error')
				try:
					beta = float(l[4])
				except ValueError:
					logger.info(l[0],study_id,assoc_data,counter,'beta error')
				try:
					se = float(l[5])
				except ValueError:
					logger.info(l[0],study_id,assoc_data,counter,'se error')
				try:
					p = float(l[6])
				except ValueError:
					logger.info(l[0],study_id,assoc_data,counter,'p error')
				try:
					n = float(l[7].rstrip())
				except ValueError:
					logger.info(l[0],study_id)
				data_dict = {
				        'study_id':study_id,
				        'snp_id':l[0],
				        'effect_allele':l[1],
				        'other_allele':l[2],
				        'effect_allele_freq':effect_allele_freq,
				        'beta':beta,
				        'se':se,
				        'p':p,
				        'n':n
				}
				op_dict = {
					"_op_type":'create',
					"_id" : study_id+':'+l[0],
					"_index": index_name,
					"_type": 'assoc',
					"_routing":study_id,
					"_source":data_dict
				}
				bulk_data.append(op_dict)
				#bulk_data.append(data_dict)
	#print bulk_data[0]
	#print len(bulk_data)
	deque(helpers.streaming_bulk(client=es,actions=bulk_data,chunk_size=chunkSize,request_timeout=timeout),maxlen=0)
	#refresh the index
	es.indices.refresh(index=index_name)
	total = es_study_search(study_id,index_name)
	print('Records indexed: '+str(total))

def compare_indexes(index_list):
	repeat=2
	queryData = {
		'q1':[1,1,'NA'],
		'q2':[100,1,'NA'],
		'q3':[1,100,'NA'],
		'q4':[1,'NA','NA'],
		'q5':[10,100,'NA'],
		'q6':[1,'NA',1e-8],
		'q7':[100,'NA',1e-8]
	}
	#aTime = {'q1':0,'q2':0,'q3':0,'q4':0,'q5':0,'q6':0,'q7':0}
	aTime = defaultdict(dict)
	for i in range(1,repeat):
		print '\n-----',i,'-----'
		for q in sorted(queryData):
			print i,'########### '+str(q)+' ###########'
			filterData = create_query(num_studies=queryData[q][0],num_snps=queryData[q][1],pval=queryData[q][2])
			for index in index_list:
				print '---',index,'---'
				time,total = run_query(filterData=filterData,index=index)
				#t = run_query(filterData=filterData,index=index)
				if q in aTime:
					aTime[q][index]=+time
				else:
					aTime[q][index]=time

	print "\nResults"
	timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
	o=open('./run_logs/run_times_'+str(timestr)+'.txt','w')
	print('test',index_list[0],index_list[1],'1/2')
	finalCom=0
	for a in sorted(aTime):
		avA1 = aTime[a][index_list[0]]/repeat
		avA2 = aTime[a][index_list[1]]/repeat
		o.write(index_list[0]+' '+index_list[1]+' '+str(a)+' '+str(round(avA1/avA2,3))+'\n')
		print a,avA1,avA2,round(avA1/avA2,3)
		finalCom+=avA1/avA2
	print('overall',index_list[1],'is',round(finalCom/len(queryData),3)),'times as fast as',index_list[0]

def compare_ukb_b_indexes(index_list):
	aTime = defaultdict(dict)
	aTotal = defaultdict(dict)
	repeat=2
	queryData = {
		'q1':[1,1,'NA'],
		'q2':[10,1,'NA'],
		'q3':[1,10,'NA'],
		'q4':[1,'NA','NA'],
		'q5':[10,10,'NA'],
		'q6':[1,'NA',1e-8],
		'q7':[10,'NA',1e-8]
	}
	for i in range(1,repeat):
		print '\n-----',i,'-----'
		for q in sorted(queryData):
			print i,'########### '+str(q)+' ###########'
			filterData = create_query(num_studies=queryData[q][0],num_snps=queryData[q][1],pval=queryData[q][2])
			print(filterData)
			for index in index_list:
				print '---',index,'---'
				time,total = run_query(filterData=filterData,index=index)
				#t = run_query(filterData=filterData,index=index)
				if q in aTime:
					aTime[q][index]=+time
				else:
					aTime[q][index]=time
				aTotal[q][index]=total

	for q in aTotal:
		if aTotal[q][index_list[0]]==aTotal[q][index_list[01]]:
			print(q,'Totals match')
		else:
			print(q,'Error with totals')

	print "\nResults"
	#timestr = time.strftime("%Y%m%d-%H%M%S")
	timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
	o=open('./run_logs/run_times_'+str(timestr)+'.txt','w')
	print('test',index_list[0],index_list[1],'1/2')
	finalCom=0
	for a in sorted(aTime):
		avA1 = aTime[a][index_list[0]]/repeat
		avA2 = aTime[a][index_list[1]]/repeat
		o.write(index_list[0]+' '+index_list[1]+' '+str(a)+' '+str(round(avA1/avA2,3))+'\n')
		print a,avA1,avA2,round(avA1/avA2,3)
		finalCom+=avA1/avA2
	print('overall',index_list[1],'is',round(finalCom/len(queryData),3)),'times as fast as',index_list[0]

	#print(aTotal)

if __name__ == '__main__':
	#if not os.path.exists('run_logs'):
	#	os.makedirs('run_logs')
	#compare_indexes(['ukb-b','UKB-b2'])
	#compare_ukb_b_indexes(['ukb-b','UKB-b2'])
	#compare_indexes(['ukb-b:00','ukb-c'])
	run_tests(index='UKB-b2')
	#run_tests(index='ukb-b-alias')
	#test_query()
	#db_test()
	#check_mrb_totals()
	#get_snps()
	#proxies_test()
	#count_test()
	#create_test(assoc_data='data/adipogen_test.txt.gz',study_id='1',index_name='create-test')
