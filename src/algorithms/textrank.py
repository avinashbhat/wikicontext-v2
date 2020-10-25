from ..subject import Subject

from gensim.summarization import summarizer


class TextRank():
    def __init__(self, text):
        self.text = text

    def get_summary(self):
        return summarizer.summarize(self.text)
