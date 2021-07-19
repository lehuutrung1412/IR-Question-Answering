import itertools
from rank_bm25 import BM25Okapi
import spacy

class PassageRetrieval:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenize = lambda text: [token.lemma_ for token in self.nlp(text)]
        self.bm25 = None
        self.passages = None

    def preprocess(self, doc):
        passages = [p for p in doc.split('\n') if p and not p.startswith('=')]
        return passages

    def fit(self, docs):
        passages = list(itertools.chain(*map(self.preprocess, docs)))
        corpus = [self.tokenize(p) for p in passages]
        self.bm25 = BM25Okapi(corpus)
        # self.average_idf = sum(float(val) for val in self.bm25.idf.values()) / len(self.bm25.idf)
        self.passages = passages

    def most_similar(self, question, topn=10):
        tokens = self.tokenize(question)
        scores = self.bm25.get_scores(tokens)
        pairs = [(s, i) for i, s in enumerate(scores)]
        pairs.sort(reverse=True)
        passages = [self.passages[i] for _, i in pairs[:topn]]
        return passages