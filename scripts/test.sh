local_url='localhost'
orcale_url='192.168.0.20'

#curl -XGET $local_url':9200/_cat/indices/ukb-b*' | sort -k3

random_snp=rs$((1 + RANDOM % 1000000))
echo $random_snp

time curl -XGET $local_url':9200/ukb-b-01/_search?pretty' -H 'Content-Type: application/json' -d '{"size":1000,"query":{"bool":{"filter":[{"term":{"snp_id":"'$random_snp'"}}]}}}';
