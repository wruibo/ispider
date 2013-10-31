#!/usr/bin/env python3
import threading

class linkq:
    def __init__(self):
        #array of [url, ref] pairs
        self._links = []
        #thread self lock for access links
        self._lock = threading.Lock()
    
    def put(self, link):
        if(not link): return
        self._lock.acquire()
        self._links.append(link)
        self._lock.release()        
            
    def puts(self, links):
        if(not links): return
        self._lock.acquire()
        for link in links: self._links.append(link)
        self._lock.release()

    def get(self):
        link = None
        self._lock.acquire()
        if(len(self._links) != 0):
            link = self._links.pop()
        self._lock.release()
        return link
    
    def gets(self, num):
        links = None
        self._lock.acquire()
        if(len(self._links)>0):
            links = self._links[0:num]
            for i in range(0, len(links)):
                self._links.pop()
        self._lock.release()    
        return links
    
    def size(self):
        self._lock.acquire()
        sz = len(self._links)
        self._lock.release()
        return sz
    