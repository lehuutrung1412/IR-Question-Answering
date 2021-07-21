from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline
import operator


class Reader:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
        self.pipe = QuestionAnsweringPipeline(model=self.model, tokenizer=self.tokenizer, device=0)
    
    def extract(self, question, passages):
        answers = []
        for passage in passages:
            try:
                answer = self.pipe(question=question, context=passage)
                answer['text'] = passage
                answers.append(answer)
            except KeyError:
                pass
        answers.sort(key=operator.itemgetter('score'), reverse=True)
        return answers