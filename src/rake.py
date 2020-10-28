from rake_nltk import Rake as RAKE


class Rake():
    def __init__(self):
        self.rake = RAKE()

    def get_keyphrases_with_score(self, rake_input):
        if isinstance(rake_input, list):
            self.rake.extract_keywords_from_sentences(rake_input)
        elif isinstance(rake_input, str):
            self.rake.extract_keywords_from_text(rake_input)
        return self.rake.get_ranked_phrases_with_scores()

    def get_keyphrases(self, rake_input):
        if isinstance(rake_input, list):
            self.rake.extract_keywords_from_sentences(rake_input)
        elif isinstance(rake_input, str):
            self.rake.extract_keywords_from_text(rake_input)
        return self.rake.get_ranked_phrases()
