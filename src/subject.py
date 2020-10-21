from utils import Utils

import re

from urllib.request import urlopen
from bs4 import BeautifulSoup
import wikipedia



class Subject(Utils):
    def __init__(self, subject, bs_parser="lxml", latin_encoder="latin-1"):
        super().__init__(latin_encoder="latin-1")
        self.subject = subject
        self.bs_parser = bs_parser
        self.meta = {}

    def get_hyperlinks(self):
        # Append the url tag to wiki
        bs_obj = BeautifulSoup(self._get_html, self.bs_parser)
        new_links = list()
        # The url tags are always i) found in bodycontent tag
        for each in bs_obj.findAll("div", {"id": "bodyContent"}):
            for link in bs_obj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
                if 'href' in link.attrs:
                    stripped = re.sub('/wiki/', "", link.attrs['href'])
                    stripped = re.sub('_', " ", stripped)
                    stripped = self._cleanup_latin_encoding(stripped)
                    newLinks.append(stripped)
        return new_links

    def _get_url(self):
        return wikipedia.page(self.subject).url

    def _get_summary(self):
        return wikipedia.summary(self.subject)

    def _get_content(self):
        return wikipedia.page(self.subject).content

    def _get_html(self):
        return wikipedia.page(self.subject).html