from transformers import pipeline


class Transformer:
    def __init__(self, text):
        self.text = text

    def get_bart_summary(self, min_length=40, max_length=150):
        summarization = pipeline("summarization")
        summary = summarization(self.text, min_length=min_length, max_length=max_length)[0]['summary_text']
        return summary

    def get_t5_summary(self, model='t5-base', tokenizer='t5-base', framework='tf', min_length=40, max_length=150):
        summarization = pipeline("summarization", model=model, tokenizer=tokenizer, framework=framework)
        summary = summarization(self.text, min_length=min_length, max_length=max_length)[0]['summary_text']
        return summary




