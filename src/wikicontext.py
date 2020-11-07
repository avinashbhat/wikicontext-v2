from src.subject import Subject
from src.algorithms.textrank import TextRank
from src.algorithms.transformer import Transformer


class WikiContext(Subject):
    def __init__(self, subject, algorithm, params, max_prereq=5):
        Subject.__init__(self, subject=subject)
        self.algorithm = algorithm
        self.params = params
        self.max_prereq = max_prereq
        self.content = None
        self.prereq = {}

    def get_main_content(self):
        self.content = self._get_summary()

    def get_prereqs_content(self):
        keyphrases = self.get_top_keywords_from_rake()
        hyperlinks = self._get_links()
        match = []
        for phrase in keyphrases:
            match.extend([hyperlink for hyperlink in hyperlinks if 
                hyperlink.lower() in phrase.lower()])
            # Make it unique
            match = list(set(match))
            if len(match) >= self.max_prereq:
                break
        
        for prereq in match:
            s = Subject(prereq)
            self.prereq[prereq] = s._get_summary()
    
    def mapper(self):
        if self.algorithm == 'TextRank':
            return TextRank
        elif self.algorithm == 'BART':
            return Transformer
        elif self.algorithm == 'T5':
            return Transformer

    def get_main_summary(self):
        model_class = self.mapper()
        model = model_class(text=self.content, **self.params)
        return model.get_summary(self.algorithm)

    def get_prereqs_summary(self):
        model_class = self.mapper()
        prereq_summary = {}
        for each in self.prereq:
            model = model_class(self.prereq[each], **self.params)
            prereq_summary[each] = model.get_summary(self.algorithm)
        return prereq_summary
