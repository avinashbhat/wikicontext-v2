from ..subject import Subject

from gensim.summarization import summarizer


class TextRank():
    def __init__(self, text, ratio=0.2, word_count=None, split=True):
        self.text = text
        self.ratio = ratio
        self.word_count = word_count
        self.split = split

    def get_summary(self, algorithm):
        summary = summarizer.summarize(self.text, self.ratio, self.word_count, self.split)
        if summary and len(summary) > 5:
            return " ".join(summary[:5])
        elif not summary:
            return self.text
        else:
            return " ".join(summary)
