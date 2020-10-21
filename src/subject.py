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
        self.url = None
    
    def _linkify(self):
        # A function to create the link in parsable format
        # wikipedia url is in the form : https://en.wikipedia.org/wiki/Papa_CJ
        self.url = 'https://en.wikipedia.org/wiki/' + '_'.join(self.subject.split(" "))

    def get_hyperlinks(self):
        # Append the url tag to wiki
        self._linkify()
        bs_obj = BeautifulSoup(urlopen(self.url), self.bs_parser)
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

    def get_summary(self):
        return wikipedia.summary(self.subject)

    def get_page_content(self):
        return wikipedia.page(self.subject).content