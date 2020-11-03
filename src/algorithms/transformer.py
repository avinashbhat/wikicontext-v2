from transformers import pipeline


class Transformer:
    def __init__(self, text, model='t5-base', tokenizer='t5-base', 
            min_length=40, max_length=150, framework='tf'):
        self.text = text
        self.model = model
        self.tokenizer = tokenizer
        self.min_length = min_length
        self.max_length = max_length
        self.framework = framework

    def _get_bart_summary(self):
        summarization = pipeline("summarization")
        summary = summarization(self.text, min_length=self.min_length, 
                max_length=self.max_length)[0]['summary_text']
        return summary

    def _get_t5_summary(self):
        summarization = pipeline("summarization", model=self.model, 
                tokenizer=self.tokenizer, framework=self.framework)
        summary = summarization(self.text, min_length=self.min_length, 
                max_length=self.max_length)[0]['summary_text']
        return summary

    def get_summary(self, algorithm):
        if algorithm == 'BART':
            return self._get_bart_summary()
        elif algorithm == 'T5':
            return self._get_t5_summary()
