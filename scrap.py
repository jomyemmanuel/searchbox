from bs4 import BeautifulSoup
import esIndex
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
		word = word.translate(string.maketrans("",""), string.punctuation).decode('utf-8').lower().strip()
		if word != "":
			add_to_index(index,word,url)

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


if __name__ == "__main__":
	crawled, index, graph = crawl_web("http://mec.ac.in/")
	with open("crawled.txt", "w") as f:
		for url in crawled:
			f.write(str(url)+'\n')
	for keyword, url in index.items():
		esIndex.add_to_keywords_index(keyword,url)
	ranks = compute_ranks(graph)
	for url,score in ranks.items():
			esIndex.add_to_ranks_index(url,score)