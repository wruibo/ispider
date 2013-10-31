#!/usr/bin/env python3
import time
import threading
import urllib.request

class filed(threading.Thread): 
    def __init__(self, dbmgr):
        #dbmgr instance for store page content
        self._dbmgr = dbmgr
        #url queue wait for downloading
        self._urlq = []
        #page content queue has downloaded
        self._pageq = []
        #lock for url queue
        self._lockurl = threading.Lock()
        #lock for page content queue
        self._lockpage = threading.Lock()
        
        #stop flag for downloader
        self._stop = False
        #invoke parent's construct function
        threading.Thread.__init__(self)
    
    def start(self):
        self._stop = False
        threading.Thread.start(self)
            
    #put a link [url, ref] to the url download queue
    def put(self, link):
        self._lockurl.acquire()
        self._urlq.append(link)
        self._lockurl.release()
        
    #put some links[[url, ref], ...] to the url download queue
    def puts(self, links):
        self._lockurl.acquire()
        for link in links: self._urlq.append(link)
        self._lockurl.release()
    
    #get next [url, ref] pair wait for downloading
    def next(self):
        link = None
        self._lockurl.acquire()
        if(len(self._urlq)>0): link = self._urlq.pop()
        self._lockurl.release()
        return link
    
    #download the page conent of url
    def dld(self, url):
        page = None
        try:
            conn = urllib.request.urlopen(url)
            page = conn.read()
        except:
            pass
        finally:
            pass
        return page
    
    #save page content[url, ref, page content] to the page queue
    def save(self, page):
        self._lockpage.acquire()
        #add content to queue for parsing
        self._pageq.append(page)
        #store content to db for persistent
        self._dbmgr.putpage(page)
        self._lockpage.release()        
    
    #pop a page content from queue
    def pop(self):
        page = None
        self._lockpage.acquire()
        if(len(self._pageq)>0): page = self._pageq.pop()
        self._lockpage.release()
        return page
    
    #pop all page conent from queue
    def pops(self):
        pages = None
        self._lockpage.acquire()
        if(len(self._pageq)>0):
            pages = self._pageq
            self._pageq = []
        self._lockpage.release()
        return pages
    
    def stop(self):
        self._stop = True
        threading.Thread.join(self)
    
    def info(self):
        self._lockurl.acquire()
        strmsg = "url queue length: " + str(len(self._urlq))+"\n"
        self._lockurl.release()
        
        self._lockpage.acquire()
        strmsg += "page queue length: " + str(len(self._pageq)) + "\n"
        self._lockpage.release()
        
        return strmsg
        
    #thread function for running
    def run(self):
        while(not self._stop):
            #get the next url wait for downloading
            link = self.next() 
            if(not link):
                time.sleep(1)
                continue
            #download the page content of the url
            url, ref = link
            page = self.dld(url)
            #pass the download result to the next responser
            if(page): self.save([url, ref, page])
            link = self.next()
        
if __name__ == "__main__":
    urls = []
    for i in range(0, 10000):
        urls.append(["http://www.funshion.com/subject/"+str(i)+"/", "http://www.funshion.com/"])
    
    mydld = filed()
    mydld.puts(urls)
    mydld.start()
    
    while(True):
        print(mydld.info())
        print("\r\n")
        time.sleep(1)
    
    