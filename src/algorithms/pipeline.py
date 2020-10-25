from transformers import pipeline


class Pipeline():
    def __init__(self, text):
        self.text = text
        self.summarization = pipeline("summarization")

    def get_summary(self):
        return self.summarization(self.text)[0]['summary_text']


