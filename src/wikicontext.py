from src.subject import Subject
from src.algorithms.textrank import TextRank


class WikiContext(Subject):
    def __init__(self, subject, algorithm, params, max_prereqs=5):
        Subject.__init__(self, subject=subject)
        self.algorithm = algorithm
        self.params = params
        self.max_prereq = max_prereqs
        self.content = None
        self.prereq = {}

    def get_main_content(self):
        self.content = self._get_summary()

    def get_prereqs_content(self):
        keyphrases = self.get_top_keywords_from_rake()
        hyperlinks = self._get_links()
        match = []
        count = 0
        for phrase in keyphrases:
            match.extend([hyperlink for hyperlink in hyperlinks if hyperlink.lower() in phrase.lower()])
            # Make it unique
            match = list(set(match))
        
        for prereq in match:
            s = Subject(prereq)
            if s._check_page_exists:
                summary = s._get_content()
                if summary:
                    self.prereq[prereq] = summary
                    count += 1
        
            if count >= self.max_prereq:
                break
    
    def mapper(self):
        if self.algorithm == 'TextRank':
            return TextRank

    def get_main_summary(self):
        model_class = self.mapper()
        model = model_class(text=self.content, **self.params)
        summary = model.get_summary(self.algorithm)
        if summary:
            return summary
        else:
            return self.content

    def get_prereqs_summary(self):
        model_class = self.mapper()
        prereq_summary = {}
        for each in self.prereq:
            model = model_class(self.prereq[each], **self.params)
            prereq_summary[each] = model.get_summary(self.algorithm)
        return prereq_summary
