from elasticsearch import Elasticsearch 

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='ranks', ignore=400)

def add_to_index(url,score):
	if es.search(index="ranks", body={"query": {"match": {'url':url}}})['hits']['hits']:
		id = es.search(index="ranks", body={"query": {"match": {'url':url}}})['hits']['_id']
		es.index(index='ranks', doc_type='scores', id=id, body={
			'url' : url,
			'score': score
			})
		return
	es.index(index='ranks', doc_type='scores', body={
		'url' : url,
		'score': score
	})

def compute_ranks(graph):
	d = 0.8 # damping factor
	numloops = 10

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0/npages

	for i in range(0, numloops):
		newranks = {}
		for page in graph:
			new_rank = (1-d) / npages
			inlinks = 0
			for otherpages in graph:
				if page in graph[otherpages]:
					new_rank = new_rank + d * (ranks[otherpages] / len(graph[otherpages]))
			newranks[page] = new_rank
		ranks = newranks
	return ranks