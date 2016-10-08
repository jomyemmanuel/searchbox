from elasticsearch import Elasticsearch


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

try:
	es.indices.delete(index="ranks")
except:
	es.indices.create(index='ranks', ignore=400)

# try:
# 	es.indices.delete(index="keywords")
# except:
# 	es.indices.create(index='keywords', ignore=400)

def add_to_keywords_index(keyword,urls):
	id_info = es.search(index="keywords", body={"query": {"match": {'keyword':keyword}}},
					filter_path=['hits.hits._id'])
	if id_info:
		id = id_info['hits']['hits'][0]['_id']
		url_list = es.get(index='keywords', doc_type='url', id=id)['_source']['url']
		if urls not in es.get(index='keywords', doc_type='url', id=id)['_source']['url']:
			for url in urls:
				url_list.append(url)
		es.index(index='keywords', doc_type='url', id=id, body={
			'keyword' : keyword,
			'url': url_list
		})
	else:
		es.index(index='keywords', doc_type='url', body={
			'keyword' : keyword,
			'url': urls
		})

def add_to_ranks_index(url,score):
	es.index(index='ranks', doc_type='scores', body={
		'url' : url,
		'score': score
	})