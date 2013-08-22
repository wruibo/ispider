#!/usr/bin/env python3
from html.parser import HTMLParser

from type import url_t

'''
    parser specified
'''
class parser(HTMLParser):
    
    def __init__(self, strict=True):
        HTMLParser.__init__(self, strict)

        self._curr_tag = ""
        self._url = ""
        self._urllst = []

    def reset(self):
        HTMLParser.reset(self)
    
    def parse(self, url, html):
        self._url = url
        self.feed(html)

    def geturls():
        return self._urllst

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == "href":
                    print(attr[0], ':', attr[1])

    def handle_data(self, data):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_comment(self, data):
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

if __name__ == "__main__":
    from dlder import dlder
    dlder
    page = dlder.download_page("http://www.sohu.com")
    print(page)
    
    #parser = parser(True)
    #parser.parse("", page.decode('GBK'))
    
