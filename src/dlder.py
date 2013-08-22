 #!/usr/bin/env python3
import os
import sys
import time
import http.client
import urllib.parse

import type

class dlder:    
    def __init__(self):
        pass
    
    @staticmethod
    def download_file(url, file):
        pres = urllib.parse.urlparse(url)
        host, port, path = pres.hostname, pres.port, pres.path
    
        conn = http.client.HTTPConnection(host, port)
        conn.connect()
        conn.request("GET", path)
        response = conn.getresponse()
        
        fobj = open(file, 'wb')
        
        rd_sz = 512*1024
        data = response.read(rd_sz)
        while(len(data) != 0):
            fobj.write(data)
            data = response.read(rd_sz)
        
        conn.close()

    def download_page(url):
        pres = urllib.parse.urlparse(url)
        host, port, path = pres.hostname, pres.port, pres.path
    
        conn = http.client.HTTPConnection(host, port)
        conn.connect()
        conn.request("GET", path, None, {"Accept-Encoding":"gzip"})

        response = conn.getresponse()
        print(response.getheaders())
        page = response.read()

        return page

if __name__ == "__main__":
    page = dlder.download_page("http://www.qq.com/")
    import gzip
    data = gzip.decompress(page)
    
    print(len(page))
    print(len(data))
        
    strpage = data.decode('gb2312', 'ignore')
    print(strpage[0:1000])
    #print(page.decode('utf_8' ,'ignore'))