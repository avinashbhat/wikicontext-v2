from .utils import Utils

import re

import wikipedia



class Subject(Utils):
    def __init__(self, subject, bs_parser="lxml", latin_encoder="latin-1"):
        super().__init__(latin_encoder="latin-1")
        self.subject = subject
        self.bs_parser = bs_parser
        # This is None to simulate lazy loading
        self.wikipedia_object = None

    # def get_hyperlinks(self):
    #     # Append the url tag to wiki
    #     bs_obj = BeautifulSoup(self._get_html, self.bs_parser)
    #     new_links = list()
    #     # The url tags are always i) found in bodycontent tag
    #     for each in bs_obj.findAll("div", {"id": "bodyContent"}):
    #         for link in bs_obj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
    #             if 'href' in link.attrs:
    #                 stripped = re.sub('/wiki/', "", link.attrs['href'])
    #                 stripped = re.sub('_', " ", stripped)
    #                 stripped = self._cleanup_latin_encoding(stripped)
    #                 newLinks.append(stripped)
    #     return new_links

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