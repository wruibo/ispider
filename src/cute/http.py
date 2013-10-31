#!/usr/bin/env python3
import urllib.request
import http.server

class client:
    def __init__(self):
        pass
    
    def request(self, url):
        resp = urllib.request.urlopen(url)
        content = resp.read()
        return content.decode('utf-8')

class server:
    def __init__(self):
        pass

    
if(__name__ == "__main__"):
    ch = cutehttp()
    content = ch.request("http://www.funshion.com")
    print(content)
    
    