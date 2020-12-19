from ..subject import Subject

from gensim.summarization import summarizer


class TextRank():
    def __init__(self, text, ratio=0.2, word_count=None, split=False):
        self.text = text
        self.ratio = ratio
        self.word_count = word_count
        self.split = split

    def get_summary(self, algorithm):
        return summarizer.summarize(self.text, self.ratio, self.word_count, self.split)
