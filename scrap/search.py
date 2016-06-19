from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def lookup(keyword):
	# if es.search(index='keywords', body={"query": {"match": {'keyword':keyword}}},
	# 			 filter_path=['hits.hits._source.keyword']):
	terms = es.search(index='keywords', q='keyword:\"{}\"'.format(keyword),
						 analyzer="english", analyze_wildcard=True,
						_source_include=['url'],
						filter_path=['hits.hits._source.*'])
	# terms  = es.search(index='keywords', q='keyword:\"{}\"'.format(keyword))
	print terms
		# url_list  = []
		# for url in urls['hits']['hits'][0]:
		# 	url_list += url[0]['_source']
		# for id in ids['hits']['hits']:
		# 	print es.get(index='keywords', doc_type='url', id=id)
	# else:
	# 	return None

	

def good_lookup(keyword):
	collection = lookup(keyword)
	if not collection:
		return None
	# best_page = collection[0]
	# id = es.search(index="ranks", body={"query": {"match": {'best_page':best_page}}})['hits']['_id']
	# ranks[best_page] = es.get(index='ranks', doc_type='scores', id=id)['_source']['score']
	# for candidate in collection:
	# 	id = es.search(index="ranks", body={"query": {"match": {'candidate':candidate}}})['hits']['_id']
	# 	ranks[candidate] = es.get(index='ranks', doc_type='scores', id=id)['_source']['score']
	# 	if ranks[candidate] > ranks[best_page]:
	# 		best_page = candidate
	# return best_page

q = raw_input("Enter Query: ")
print good_lookup(q)