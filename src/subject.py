from .utils import Utils

import re

import wikipedia


class Subject(Utils):
    def __init__(self, subject, bs_parser="lxml", latin_encoder="latin-1"):
        super().__init__(latin_encoder="latin-1")
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

    def get_meta(self):
        if not self.wikipedia_object:
            self._get_wiki_object()
        self.meta["url"] = self.wikipedia_object.url
        self.meta["title"] = self.wikipedia_object.title