from src.subject import Subject
from src.algorithms.textrank import TextRank
from src.algorithms.transformer import Transformer

class WikiContext(Subject):
    def __init__(self, subject, algorithm, max_prereq=5):
        Subject.__init__(self, subject=subject)
        self.algorithm = algorithm
        self.max_prereq = max_prereq

    def get_main_summary(self):
        return self._get_summary()
        # return self._get_content()

    def get_prereq_summary(self):
        keyphrases = self.get_top_keywords_from_rake()
        hyperlinks = self._get_links()
        match = []
        for phrase in keyphrases:
            match.extend([hyperlink for hyperlink in hyperlinks if hyperlink.lower() in phrase.lower()])
            # Make it unique
            match = list(set(match))
            if len(match) >= self.max_prereq:
                break
        
        pre_requisites = {}
        for prereq in match:
            s = Subject(prereq)
            pre_requisites[prereq] = s._get_summary()
        
        return pre_requisites