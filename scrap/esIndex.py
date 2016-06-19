from elasticsearch import Elasticsearch


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='keywords', ignore=400)

def add_to_index(keyword,url):
	if es.search(index='keywords', body={"query": {"match": {'keyword':keyword}}},
				 filter_path=['hits.hits._source.keyword']):
		id = es.search(index="keywords", body={"query": {"match": {'keyword':keyword}}},
						filter_path=['hits.hits._id'])
		if url not in es.get(index='keywords', doc_type='url', id=id)['_source']['url']:
			url_list = es.get(index='keywords', doc_type='url', id=id)['_source']['url']
			url_list.append(url)
			es.index(index='keywords', doc_type='url', id=id, body={
				'keyword' : keyword,
				'url': url_list
			})
		return
	es.index(index='keywords', doc_type='url', body={
		'keyword' : keyword,
		'url': [url]
	})