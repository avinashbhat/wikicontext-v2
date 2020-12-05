from .utils import Utils
from.rake import Rake

import re

import wikipedia


class Subject(Utils, Rake):
    def __init__(self, subject, bs_parser="lxml", latin_encoder="latin-1"):
        Utils.__init__(self, latin_encoder="latin-1")
        Rake.__init__(self)
        self.subject = subject
        self.bs_parser = bs_parser
        # lazy loaded
        self.wikipedia_object = None

    def _get_wiki_object(self):
        if not self.wikipedia_object:
            self.wikipedia_object = wikipedia.page(self.subject)

    def _get_links(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        return self.wikipedia_object.links

    def _get_url(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        return self.wikipedia_object.url

    def _get_summary(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        return self.wikipedia_object.summary

    def _get_content(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        return self.wikipedia_object.content

    def _get_html(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        return self.wikipedia_object.html

    def _get_search(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        return self.wikipedia_object.search

    def get_meta(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        self.meta["url"] = self.wikipedia_object.url
        self.meta["title"] = self.wikipedia_object.title

    def get_top_keywords_with_score_from_rake(self):
        return self.get_keyphrases_with_score(self._get_content()) 

    def get_top_keywords_from_rake(self):
        return self.get_keyphrases(self._get_content())