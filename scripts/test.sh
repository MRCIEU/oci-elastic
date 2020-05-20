url='localhost'
port='9300'
#url='192.168.0.20'
#url='140.238.83.192'

#curl -XGET $url':9200/_cat/indices/ukb-b*' | sort -k3

#random_snp=rs$((1 + RANDOM % 1000000))
#echo $random_snp

index_name='ukb-a,ukb-b,ukb-d,ieu-a,ebi-a,eqtl-a,met-a,met-b,met-c,prot-a,prot-b,ubm-a'

#get 1000 records for random snps
echo 'Getting random set of SNPs'
com="time curl -s -o 1000.out -XGET '$url:$port/$index_name/_search?pretty' -H 'Content-Type: application/json' -d '{\"size\":10000,\"query\":{\"bool\":{\"filter\":[{\"term\":{\"gwas_id\":\"5776\"}}]}}}';"
echo $com
eval $com
random_snps=`grep snp_id 1000.out | cut -d ' ' -f13 | sed 's/"//g' | sed 's/,//' | sort --random-sort | head -n10`
echo $random_snps

pval=1e-3

#do phewas tests
for i in $random_snps;
	do
	echo $i
	#time curl -o test.$i.out -XGET $url':9200/ukb-b-00/_search?pretty' -H 'Content-Type: application/json' -d '{"size":1000,"query":{"bool":{"filter":[{"term":{"snp_id":"'$i'"}}]}}}';
	com="time curl -s -o out/test1.$i.out -XGET $url':'$port'/'$index_name'/_search?pretty' -H 'Content-Type: application/json' -d '{\"size\":100000,\"query\":{\"bool\":{\"filter\":{\"term\":{\"snp_id\":\"'$i'\"}}}},\"post_filter\": {\"range\": {\"p\": {\"lt\": $pval}}}}';"
	echo $com
	eval $com
done
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

#do pval search
SECONDS=0
numSnps=10
for i in {1..10};
 	do
	snpList=\"`grep snp_id 1000.out | cut -d ' ' -f13 | sed 's/"//g' | sed 's/,//' | sort --random-sort | head -n 10 | paste -s -d, - | sed 's/,/","/g'`\"
	echo "snpList $snpList"
	echo 'pval search'
	#curl -s -o out/test2.$i.out -XGET $url':'$port'/'$index_name'/_search?pretty' -H 'Content-Type: application/json' -d '{"size":10000,"query":{"bool":{"filter":[{"terms":{"snp_id":['$snpList']}},{"range" : {"p": {"lt": 1e-5}}}]}}}';
	com="time curl -s -o out/test2.$i.out -XGET $url':'$port'/'$index_name'/_search?pretty' -H 'Content-Type: application/json' -d '{\"size\":10000,\"query\":{\"bool\":{\"filter\":{\"terms\":{\"snp_id\":[$snpList]}}}},\"post_filter\": {\"range\": {\"p\": {\"lt\": $pval}}}}';"
	echo $com
	eval $com
done
duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
