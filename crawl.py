from googlesearch import search
from bs4 import BeautifulSoup
import requests
import re

class Documents:
    def __init__(self, query):
        self.query = query
        
    def get(self):
        link_search = search(self.query)
        docs = []
        count = 0
        i = 0
        while count < 5 and i < 10:
            url = link_search[i]
            if url.split('/')[0] == '':
                i += 1
                continue
            html = requests.get(url, timeout = 4)
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
            if doc_str == '':
                i += 1
                continue
            docs.append(doc_str)
            i += 1
            count += 1
        return docs