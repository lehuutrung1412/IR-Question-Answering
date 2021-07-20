from crawl import GoogleSearchAPI
# from retrieval import PassageRetrieval
from extract import Reader

model_name = 'bert-large-uncased-whole-word-masking-finetuned-squad'
# passage_retriever = PassageRetrieval()
reader = Reader(model_name)

def main(question):
    passages = GoogleSearchAPI().get_passages(question)
    answers = reader.extract(question, passages)
    return answers[0]
    
    