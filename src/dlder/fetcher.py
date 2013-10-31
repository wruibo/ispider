#!/usr/bin/env python3
import sys
sys.path.append("..")

import time
import threading
import cute.http
import cute.linkq

'''
   fetch resource url waiting for download from remote manager, put the resource url
   into local url link queue.
'''
class fetcher(threading.Thread):
    def __init__(self):
        #queue for links fetched from remaote manager
        self._linkq = cute.linkq.linkq()
        #minimal number of links limit in link queue
        self._link_minimal = 1024
        #request url for manager
        self._request_url = "http://localhost/api/fetchlinks"
        #stop flash for fetcher thread
        self._stopflag = True
        #invoke parent's construct function
        threading.Thread.__init__(self)
    
    def start(self):
        self._stopflag = False
        threading.Thread.start(self)
    
    def stop(self):
        self._stopflag = True
        threading.Thread.join(self)

    def hungry(self):
        #if links number is less than limit, then need fetch more links
        return self._linkq.size() < self._link_minimal
    
    def feed(self):
        #use cute http to fetch links from remote manager
        chttp = cute.http.client()
        #content format: "url,ref\nurl,ref\nurl,ref\n..."
        content = chttp.request(self._request_url)
        if(content):
            links = content.split('\n')
            for linkstr in links:
                link = linkstr.split(',')
                if(len(link) != 2):
                    pass
                
                url = link[0].strip()
                ref = link[1].strip()
                if(not url or not ref):
                    pass
                
                self._linkq.put([url, ref])                
    
    def gets(self, num):
        return self._linkq.gets(num)
    
    def run(self):
        while(not self._stopflag):
            #fetch new links waiting for download from manager if need
            if(self.hungry()):
                self.feed()
            
            #wait for a while
            time.sleep(5)

