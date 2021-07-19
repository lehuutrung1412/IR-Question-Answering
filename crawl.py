from googlesearch import search
from bs4 import BeautifulSoup
import requests
import re
import concurrent.futures
import cchardet
import lxml

MAX_THREADS = 30

class Documents:
    def __init__(self, query):
        self.query = query
        self.link_search = search(self.query)
        self.requests_session = requests.Session()

    def gett(self, link_search):
        url = link_search
        if url.split('/')[0] == '':
            return ''
        html = self.requests_session.get(url, timeout = 4)
        tree = BeautifulSoup(html.text,'lxml')
        para = tree.findAll(['p', 'span', 'h1', 'h2', 'h3', 'li'])
        doc = []
        for p in para:
            p_text = p.getText()
            if p_text == '\n':
                continue
            doc.append(p_text)
        doc_str = ' '.join(doc)
        doc_str = re.sub(r'\[.*?\]', '', doc_str)
        # doc_str = re.sub('\n\n', '\n', doc_str)
        doc_str = re.sub('\xa0', ' ', doc_str)
        return doc_str


    def get(self):
        threads = min(MAX_THREADS, len(self.link_search))
        docs = []
        count = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            for link_search in self.link_search:
                if count > 4:
                    break
                doc = executor.submit(self.gett, link_search).result()
                if doc != '':
                    docs.append(doc)
                    count += 1
        return docs