import itertools
from rank_bm25 import BM25Okapi
import spacy
import concurrent.futures

class PassageRetrieval:
    def __init__(self, nlp):
        self.tokenize = lambda text: [token.lemma_ for token in nlp(text)]
        self.bm25 = None
        self.passages = None

    def preprocess(self, doc):
        passages = [p for p in doc.split('\n') if p and not p.startswith('=')]
        return passages

    def fit(self, docs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            passages = list(itertools.chain(*executor.map(self.preprocess, docs)))
        # passages = list(itertools.chain(*map(self.preprocess, docs)))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            corpus = [executor.submit(self.tokenize, p).result() for p in passages]
        # corpus = [self.tokenize(p) for p in passages]
        print('oke')
        self.bm25 = BM25Okapi(corpus)
        self.passages = passages

    def most_similar(self, question, topn=10):
        tokens = self.tokenize(question)
        scores = self.bm25.get_scores(tokens)
        pairs = [(s, i) for i, s in enumerate(scores)]
        pairs.sort(reverse=True)
        passages = [self.passages[i] for _, i in pairs[:topn]]
        return passages
        # return self.passages