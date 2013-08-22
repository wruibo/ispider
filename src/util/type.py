#!/usr/bin/env python3

class url_t:
    def __init__(self, tag, url, ref, title):
        self._tag = ""
        self._url = ""
        self._ref = ""
        self._title = ""
        
    def tag(self):
        return self._tag

    def url(self):
        return self._url

    def ref(self):
        return self._ref

    def title(self):
        return self._title

    def dump(self):
        pass#return "tag: {}, title: {} url: {}, ref: {}".format((self._tag, self._title self._url, self._ref))

class header_t:
    
    def __init__(self):
        pass

if __name__ == '__main__':
    ui = urlinfo("http://www.baidu.com/", "http://www.youku.com/");
    print("url:", ui._url, "ref:", ui._ref);
