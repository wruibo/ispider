#!/usr/bin/env python3
import time
import threading

import linkdb

'''
   scheduler core class with the links recevied from spider, links with dispatch to
   the downloader when asked for.
'''
class schdcore(threading.Thread):
    #file links db path
    _file_linkdb_path = "../../db/filelinkdb"
    #page links db path
    _page_linkdb_path = "../../db/pagelinkdb"
    
    #time for link db sync to file in minites
    _db_sync_interval = 16
    
    #number of page links return when the @getp method invoked
    _pfeed_per_time = 5   
    #number of file links return when the @getf method invoked
    _ffeed_per_time = 5

    #initialize the file link db & page link db
    def __init__(self):
        #file links received from spider
        self._fdb = linkdb.linkdb(self._file_linkdb_path)
        #page links received from spider
        self._pdb = linkdb.linkdb(self._page_linkdb_path)
        
        #stop flag for thread
        self._stopflag = True
        
        #initialize parent
        threading.Thread.__init__(self)
    
    def init(self):
        if(not self._stopflag): return
        self._stopflag = False
        threading.Thread.start(self)        
    
    #put file links to db, @links is list of [url, ref]
    def putf(self, links):
        self._fdb.put(links)
        
    
    #put page links to db, @links if list of [url, ref]
    def putp(self, links):
        self._pdb.put(links)
    
    #get list of links from file link db
    def getf(self):
        return self._fdb.get(self._ffeed_per_time)
    
    #get list of links from page link db
    def getp(self):
        return self._pdb.get(self._pfeed_per_time)   
    
    #flush data to db file periodly
    def run(self):
        while not self._stopflag:
            time.sleep(self._db_sync_interval)
            self._fdb.sync()
            self._pdb.sync()
    
    #destory schedule core object
    def destroy(self):
        self._stopflag = True
        threading.Thread.join(self)

if(__name__ == "__main__"):
    sc = schdcore()
    sc.init()
    
    newurls = []
    for i in range(0, 10):
        newurls.append(["http://wwww.baidu.com/"+str(i), "http://wwww.sohu.com/"+str(i)])
    sc.putp(newurls)
    sc.putf(newurls)
    
    sc.getp()
    sc.getf()
    
    time.sleep(20)
    
    sc.destroy()
              