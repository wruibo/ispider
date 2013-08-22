#!/usr/bin/env python3
import os

'''
   persistent file database for all urls and url wait for crawling.
   
urls.db:
   save all the url parsed from page, it's format is:
          url, ref
          url, ref
          ........

fresh.db:
   save all the url waiting to crawl, it's format is:
          url, ref
          url, ref
          .......
'''
class urldb:
    def __init__(self, dbpath):
        self.open(dbpath)
    
    def open(self, dbpath):
        #make directory for url database if not exist
        if(not os.path.exists(dbpath)):
            os.makedirs(dbpath)

        #create history urls db file first
        self._urlsdbf = dbpath+"/urls.db"
        if(not os.path.isfile(self._urlsdbf)):
            f = open(self._urlsdbf, 'w')
            f.close()
        
        #create all fresh url db file not crawled    
        self._freshdbf = dbpath+"/fresh.db"
        if(not os.path.isfile(self._freshdbf)):
            f = open(self._freshdbf, 'w')
            f.close()
        
        #create url dict from url db file
        self._urlsdb = open(self._urlsdbf, 'r+')
        self._allurls = {}
        for line in self._urlsdb:
            line = line.strip()
            url, ref = line.split(',')
            self._allurls[url] = ref
        
        #create new url list from fresh url db file
        freshdb = open(self._freshdbf, 'r+')
        self._newurls = []
        for line in freshdb:
            line = line.strip()
            self._newurls.append(line.split(','))
        freshdb.close()
    
        
    def put(self, newurls):
        for url, ref in newurls:
            if(url not in self._allurls):
                self._allurls[url] = ref
                self._newurls.append([url, ref])
                self._urlsdb.write(url+","+ref+"\n")
                
    def get(self, number):
        urls = self._newurls[0:number]
        del self._newurls[0:number]
        return urls
    
    def sync(self):
        freshdb = open(self._freshdbf, 'w', encoding="utf-8")
        for url, ref in self._newurls:
            freshdb.write(url+","+ref+"\n")
        freshdb.flush()
        freshdb.close()
        
        self._urlsdb.flush()
        
    def close(self):
        self._urlsdb.close()

if(__name__ == "__main__"):
    db = urldb("../../db/urldb")
    newurls = []
    for i in range(100000, 100010):
        newurls.append(["http://wwww.baidu.com/"+str(i), "http://wwww.sohu.com/"+str(i)])
    db.put(newurls)
    print(db.get(10))
    db.sync()