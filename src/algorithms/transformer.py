from transformers import pipeline
from transformers import AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM


class Transformer:
    def __init__(self, text, model='t5-small', tokenizer='t5-small', min_length=20, 
            max_length=80, framework='pt'):
        self.text = text
        self.model = model
        self.device = -1 # no cuda support
        self.tokenizer = tokenizer
        self.min_length = min_length
        self.max_length = max_length
        self.framework = framework

    def _get_pipeline(self, model, tokenizer):
        return pipeline("summarization", model=self.model, tokenizer=self.tokenizer, 
                    device=self.device, framework=self.framework)

    def _get_bart_summary(self):
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer)
        model = AutoModel.from_pretrained(self.model)
        pipeline = self._get_pipeline(model, tokenizer)
        summary = pipeline(self.text, min_length=self.min_length, 
                max_length=self.max_length)
        return summary[0]['summary_text']

    def _get_t5_summary(self):
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model)
        pipeline = self._get_pipeline(model, tokenizer)
        summary = pipeline(self.text, min_length=self.min_length, 
                max_length=self.max_length)
        return summary[0]['summary_text']

    def _get_pegasus_summary(self):
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model)
        pipeline = self._get_pipeline(model, tokenizer)
        summary = pipeline(self.text, min_length=self.min_length, 
                max_length=self.max_length)
        return summary[0]['summary_text']

    def get_summary(self, algorithm):
        if algorithm == 'BART':
            return self._get_bart_summary()
        elif algorithm == 'T5':
            return self._get_t5_summary()
        elif algorithm == "Pegasus":
            return self._get_pegasus_summary()
