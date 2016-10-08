from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def lookup(keyword):
	try:
		terms = es.search(index='keywords', q='keyword:%s%s'%(keyword,"~"),
						  _source_include=['url'], filter_path=['hits.hits._source.*'])
	except:
		print "Sorry! No results found"
	else:
		url_list = []
		if terms:
			for urls in terms['hits']['hits']:
				url_list += urls['_source']['url']
		return url_list

	

def good_lookup(keyword):
	collection = lookup(keyword)
	if not collection:
		return
	else:
		ranks = {}
		best_page = collection[0]
		try:
			score = es.search(index="ranks", q='url:"%s"'%(best_page),
							 _source_include=['score'], filter_path=['hits.hits._source.*']
							 )['hits']['hits'][0]['_source']['score']
		except:
			print "No ranks found!"
		else:
			ranks[best_page] = score
			for candidate in collection:
				try:
					score = es.search(index="ranks", q='url:"%s"'%(candidate),
									 _source_include=['score'], filter_path=['hits.hits._source.*']
									 )['hits']['hits'][0]['_source']['score']
				except:
					print "No ranks found"
				else:
					ranks[candidate] = score
					if ranks[candidate] > ranks[best_page]:
						best_page = candidate
			return best_page

q = raw_input("Enter Query: ")
if q:
	res = good_lookup(q)
	if res:
		print res
else:
	print "Enter valid keyword"