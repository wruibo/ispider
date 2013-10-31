#!/usr/bin/env python3
import re
import time
import hashlib
import threading
import urllib.request

import filedb
import cute.linkq

class downloader(threading.Thread): 
    def __init__(self, dbpath):
        #minimal links of queue, below the value means 'hungry'
        self._links_min = 32
        #url queue wait for downloading
        self._linkq = cute.linkq.linkq()

        #file db for downloaded files
        self._filedb = filedb.filedb(dbpath)
        
        #stop flag for downloader
        self._stopflag = False
        #invoke parent's construct function
        threading.Thread.__init__(self)
    
    def start(self):
        self._stopflag = False
        threading.Thread.start(self)
            
    #put a link [url, ref] to the url download queue
    def put(self, link):
        self._linkq.put(link)
        
    #put some links[[url, ref], ...] to the url download queue
    def puts(self, links):
        self._linkq.puts(links)

    #get the next file url to download
    def next(self):
        return self._linkq.get()

    def hungry(self):
        return self._linkq.size() < self._links_min
    
    #get the downloader load, waiting queue size
    def load(self):
        return self._linkq.size()
    
    #download a file specified by @url and save data to file db
    def dld(self, url, ref):
        #build an url request object to url
        conn = urllib.request.urlopen(url)  
        
        #get file name from response header
        fname = respmsg.get_filename()
        if(not fname): 
            items = re.search("([^\/]+)\.([^\.\/\\\]+)\Z", url)
            if(not items): #use url sha1 as file name
                m = hashlib.sha1()
                m.update(url.encode())
                fname = m.hexdigest()
            else:
                fname = items.group(0)
                
        #create db file
        self._filedb.fopen(url, ref, fname)
        
        #download the file & save to db file
        RDSZ = 256*1024
        data = conn.read(RDSZ)
        while(data):
            self._filedb.fwrite(data)
            data = conn.read(RDSZ)
            
        #close the db file    
        self._filedb.fclose()
            
    def stop(self):
        self._stopflag = True
        threading.Thread.join(self)
    
    def info(self):
        strmsg = "url queue length: " + str(self._linkq.size())+"\n"        
        return strmsg
        
    #thread function for running
    def run(self):
        while(not self._stopflag):
            #get the next url wait for downloading
            link = self.next() 
            if(not link):
                time.sleep(1)
                continue
            #download the page content of the url
            url, ref = link
            try:
                page = self.dld(url, ref)
            except Exception as err:
                print(err)
            finally:
                pass
            
if __name__ == "__main__":
    urls = []
    for i in range(263, 1000):
        for j in range(560, 1000):
            url = "http://img0.fspcdn.com/pictures/"+str(i)+"/"+str(j)+"/"+str(i*1000+j)+".jpg"
            urls.append([url, "http://www.funshion.com/"])
    
    mydld = downloader("../../db/filedb")
    mydld.puts(urls)
    mydld.start()
    
    while(True):
        print(mydld.info())
        print("\r\n")
        time.sleep(1)
    
    