from transformers import T5ForConditionalGeneration, T5Tokenizer

# initialize the model architecture and weights
model = T5ForConditionalGeneration.from_pretrained("t5-base")
# initialize the model tokenizer
tokenizer = T5Tokenizer.from_pretrained("t5-base")


class T5():
    def __init__(self, text, tokenizer_max_length=512, tokenizer_truncation=True, model_max_length=150,
                 model_min_length=40, model_length_penalty=2.0, model_num_beams=4, model_early_stopping=True):
        self.text = text
        # encode the text into tensor of integers using the appropriate tokenizer
        self.inputs = tokenizer.encode("summarize: " + self.text, return_tensors="pt", max_length=tokenizer_max_length,
                                       truncation=tokenizer_truncation)
        self.outputs = model.generate(self.inputs, max_length=model_max_length, min_length=model_min_length,
                                      length_penalty=model_length_penalty, num_beams=model_num_beams,
                                      early_stopping=model_early_stopping)

    def get_summary(self):
        # just for debugging
        print(self.outputs)
        return tokenizer.decode(self.outputs[0])

