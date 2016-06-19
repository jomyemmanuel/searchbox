from bs4 import BeautifulSoup
from stopwords import sw
import esIndex
import esRanks
import requests
import string

def get_all_links(page):
	links = []
	if page.find_all('a'):
		for link in page.find_all('a'):
			elm  = link.get('href')
			if elm and not str(elm).endswith('.pdf') and not str(elm).endswith('.jpg'):
				if 'http://mec.ac.in' in str(elm) or 'www.mec.ac.in' in str(elm) or 'excelmec.org' in str(elm):
					links.append(str(elm))
				else:
					if ('https://' not in str(elm)) and ('http://' not in str(elm)):
						links.append("http://mec.ac.in/mec/" + str(elm))
	return links

def crawl_web(seed):
	tocrawl = [seed]
	crawled = []
	index = {}
	graph = {}
	while tocrawl:
		page = tocrawl.pop(0)
		if not page.endswith('/') and not page.endswith('.php'):
			page += '/'
		if page.find("#") != -1 :
			end = page.find("#")
			page = page[:end]
		if page not in crawled:
			try:
				r = requests.get(page, timeout=3, allow_redirects=False)
			except:
				pass
			else:
				html_doc = r.text.encode('utf-8')
				content = BeautifulSoup(html_doc, 'html.parser')
				add_page_to_index(index,r.url,content)
				outlinks = get_all_links(content)
				if outlinks:
					graph[r.url] = outlinks
					tocrawl += outlinks
				crawled.append(r.url)
	return crawled, index, graph

def add_to_index(index,keyword,url):
	if keyword in index:
			if url not in index[keyword]:
				index[keyword].append(url)
			return
	index[keyword] = [url]

def add_page_to_index(index,url,content):
	words = content.get_text().encode('utf-8').split()
	for word in words:
		word = word.translate(string.maketrans("",""), string.punctuation).strip().decode('utf-8')
		if word not in sw:
			add_to_index(index,word,url)



crawled, index, graph = crawl_web("http://mec.ac.in/")

with open("crawled.txt", "w") as f:
	for url in crawled:
		f.write(str(url)+'\n')
for key,url in index.items():
	esIndex.add_to_index(key,url)
# ranks = esRanks.compute_ranks(graph)
# for url,score in ranks.items():
# 	esRanks.add_to_index(url,score)