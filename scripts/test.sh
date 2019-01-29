url='localhost'
#url='192.168.0.20'

#curl -XGET $url':9200/_cat/indices/ukb-b*' | sort -k3

#random_snp=rs$((1 + RANDOM % 1000000))
#echo $random_snp

#get 1000 records for random snps
time curl -o 1000.out -XGET $url':9200/ukb-b-00/_search?pretty' -H 'Content-Type: application/json' -d '{"size":1000,"query":{"bool":{"filter":[{"term":{"study_id":"1"}}]}}}';
random_snps=`grep snp_id 1000.out | cut -d ' ' -f13 | sed 's/"//g' | sed 's/,//' | sort --random-sort | head -n10`
#echo $random_snps
for i in $random_snps:
	do echo $i;
	time curl -o test.$i.out -XGET $url':9200/ukb-b-00/_search?pretty' -H 'Content-Type: application/json' -d '{"size":1000,"query":{"bool":{"filter":[{"term":{"snp_id":"'$i'"}}]}}}';
done
