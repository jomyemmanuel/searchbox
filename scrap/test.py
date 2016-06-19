from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from stopwords import sw
import esIndex
import esRanks
import requests
import string


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# with open("graphFile.py", "w") as f:
# 	f.write(graph)

#es.search(index='keywords', q='keyword:\"{}\"'.format(keyword))

# r = requests.get('http://www.mec.ac.in/', timeout=5, allow_redirects=True)
# html_doc = r.text.encode('utf-8')
# page = BeautifulSoup(html_doc, 'html.parser')
# print page
# links = []
# for link in page.find_all('a'):
# 	elm  = link.get('href')
# 	if elm and not str(elm).endswith('.pdf') and not str(elm).endswith('.jpg'):
# 		if 'http://mec.ac.in' in str(elm) or 'www.mec.ac.in' in str(elm) or 'excelmec.org' in str(elm):
# 			links.append(str(elm))
# 		else:
# 			if ('https://' not in str(elm)) and ('http://' not in str(elm)):
# 				links.append("http://mec.ac.in/mec/" + str(elm))

# for x in links:
# 	print x


# r = requests.get('http://www.mec.ac.in/', timeout=5, allow_redirects=True)
# html_doc = r.text.encode('utf-8')
# page = BeautifulSoup(html_doc, 'html.parser')
# print page
# links = []
# for link in page.find_all('a'):
# 	elm  = link.get('href')
# 	if elm and not str(elm).endswith('.pdf') and not str(elm).endswith('.jpg'):
# 		if 'http://mec.ac.in' in str(elm) or 'www.mec.ac.in' in str(elm) or 'excelmec.org' in str(elm):
# 			links.append(str(elm))
# 		else:
# 			if ('https://' not in str(elm)) and ('http://' not in str(elm)):
# 				links.append("http://mec.ac.in/mec/" + str(elm))

# es.index(index='keywords', doc_type='url', id=1, body={
# 	'keyword' : 'yahoo',
#     'url': "['https://rocketmail.com/', 'https://www.yahoo.com/']"
# })
# print es.search(index='keywords', q='keyword:yahoo')['hits']['hits']
# es.delete(index='keywords', doc_type='url', id=1)
es.indices.delete(index="keywords")

# x = es.search(index="keywords", body={"query": {"match": {'keyword':keyword}}})['hits']['hits']
# print x
# if es.search(index='keywords', q='keyword:"fff"')['hits']['hits']:
# 	print es.search(index='keywords', q='mec')
# 	print es.search(index='keywords', q='keyword:"fff"')

# def add_to_index(keyword,url):
# 	if es.search(index='keywords', q='keyword:keyword')['hits']['hits']:
# 		id = es.search(index='keywords', q='keyword:keyword')['hits']['_id']
# 		if url not in es.get(index='keywords', doc_type='url', id=id)['_source']['url']:
# 			url_list = es.get(index='keywords', doc_type='url', id=id)['_source']['url']
# 			url_list.append(url)
# 			es.index(index='keywords', doc_type='url', id=id, body={
# 				'keyword' : keyword,
# 				'url': url_list
# 			})
# 		return
# 	es.index(index='keywords', doc_type='url', body={
# 		'keyword' : keyword,
# 		'url': [url]
# 	})

# def add_to_index(url,score):
# 	es.index(index='ranks', doc_type='scores', body={
# 		'url' : url,
# 		'score': score
# 	})