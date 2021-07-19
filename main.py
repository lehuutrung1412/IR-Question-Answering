from crawl import Documents
from retrieval import PassageRetrieval
from extract import Reader

model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
passage_retriever = PassageRetrieval()
reader = Reader(model_name)

def main(question):
    docs = Documents(question).get()
    passage_retriever.fit(docs)
    passages = passage_retriever.most_similar(question)
    answers = reader.extract(question, passages)
    return answers[0]
    
    