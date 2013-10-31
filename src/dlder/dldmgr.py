#!/usr/bin/env python3
import time
import threading 

import dlder
import fetcher
 
class download_mgr(threading.Thread):
    def __init__(self):
        #default file db path
        self._db_path = "../../db/filedb"
        #default downloader number
        self._dlder_num = 8
        #all working downloaders
        self._dlders = []
        
        #link number feed for downloader per time
        self._feed_per_time = 32
    
        #fetcher who get download url from remote
        self._fetcher = None
    
        #stop flash for fetcher thread
        self._stopflag = True
        #invoke parent's construct function
        threading.Thread.__init__(self)
        
    def start(self):
        #init&start all downloaders
        for i in range(0, self._dlder_num):
            worker = dlder.downloader(self._db_path+"/downloader_"+str(i))
            worker.start()
            self._dlders.append(worker)
        
        #init&start a fetcher
        self._fetcher = fetcher.fetcher()
        self._fetcher.start()
        
        #start downloader manager thread
        self._stopflag = False
        threading.Thread.start(self)        
    
    def stop(self):
        #stop download manager thread first
        self._stopflag = True
        threading.Thread.join(self)
        
        #then stop the fetcher thread
        self._fetcher.stop()
        self._fetcher = None
        
        #stop all the downloaders last
        while(len(self._dlders) != 0):
            worker = self._dlders.pop()
            worker.stop()
    
    def run(self):
        while(not self._stopflag):
            #check load of all downloaders
            for worker in self._dlders:
                if(worker.hungry()):
                    worker.puts(self._fetcher.gets(self._feed_per_time))
            
            #wait for while
            time.sleep(5)
            
if(__name__ == "__main__"):
    dldmgr = download_mgr()
    dldmgr.start()