#!/usr/bin/env python3
import json

'''
   scheduler core class with the links recevied from spider, links with dispatch to
   the downloader when asked for.
'''
class schdcore:
    #number of page links return when the @getp method invoked
    _pfeed_per_time = 1024    
    #number of file links return when the @getf method invoked
    _ffeed_per_time = 256
    
    def __init__(self):
        #file links received from spider
        self._flinkq = cute.linkq.linkq()
        #page links received from spider
        self._plinkq = cute.linkq.linkq()
    
    def putf(self, linkstr):
        self.put(linkstr, self._flinkq)
    
    def putp(self, linkstr):
        self.put(linkstr, self._plinkq)
    
    def getf(self):
        linkstr = ''
        links = self._flinkq.gets(self._ffeed_per_time);
        for link in links:
            linkstr += link[0]+','+link[1]+'\n'
        return linkstr
    
    def getp(self):
        linkstr = ''
        links = self._flinkq.gets(self._pfeed_per_time);
        for link in links:
            linkstr += link[0]+','+link[1]+'\n'
        return linkstr        
    
    #parse links from spider and put to relate queue, @linksstr format: 'url,ref\nurl,ref\n....'
    def put(self, linkstr, lnkq):
        if(not linkstr): return
        links = linkstr.split('\n')
        for record in links:
            link = record.split(',')
            if(len(link) != 2):
                pass
            
            url = link[0].strip()
            ref = link[1].strip()
            if(not url or not ref):
                pass
            
            lnkq.put([url, ref])           