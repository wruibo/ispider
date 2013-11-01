#!/usr/bin/env python3
import sys
sys.path.append("..")

import os
import cute.digest

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
class linkdb:
    def __init__(self, dbpath):
        #local db path
        self._dbpath = dbpath
        #total url db file path
        self._urlsdbf = dbpath+"/urls.db"
        #fresh url db file path
        self._freshdbf = dbpath+"/fresh.db"
        
        #all the url md5 information, used for new url judgement
        self._urlmd5 = set()
        #all the url in db, key->url, value->ref
        self._allurls = dict()
        #all the url not crawled, item->url, ref
        self._newurls = list()        
        
        #db file for all url
        self._urlsdb = None
        
        #initialize the link database
        self.__init()
        
    def __init(self):
        #create database if not exist
        self.__create()
        
        #load data from database
        self.__load()

    #create relate db file if not exist    
    def __create(self):
        #make directory for url database if not exist
        if(not os.path.exists(self._dbpath)):
            os.makedirs(self._dbpath)

        #create all urls db file first
        if(not os.path.isfile(self._urlsdbf)):
            f = open(self._urlsdbf, 'w')
            f.close()
        
        #create fresh url db file not crawled    
        if(not os.path.isfile(self._freshdbf)):
            f = open(self._freshdbf, 'w')
            f.close()
    #load new url & all url from db files    
    def __load(self):
        #create url dict from url db file
        self._urlsdb = open(self._urlsdbf, 'r+')
        for line in self._urlsdb:
            line = line.strip()
            url, ref = line.split(',')
            self._allurls[url] = ref
            self._urlmd5.add(cute.digest.md5(url))
        
        #create new url list from fresh url db file
        freshdb = open(self._freshdbf, 'r+')
        for line in freshdb:
            line = line.strip()
            self._newurls.append(line.split(','))
        freshdb.close()
    
    #put urls to db, where @newurls is list of [url, ref]    
    def put(self, newurls):
        for url, ref in newurls:
            urlmd5 = cute.digest.md5(url)
            if(urlmd5 not in self._urlmd5):
                self._urlmd5.add(urlmd5)
                self._allurls[url] = ref
                self._newurls.append([url, ref])
                self._urlsdb.write(url+","+ref+"\n")
                
    #get @number [url, ref] pairs from the new urls db
    def get(self, number):
        urls = self._newurls[0:number]
        del self._newurls[0:number]
        return urls
    
    #flush newurls & all urls data to db files
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
    db = linkdb("../../db/urldb")
    newurls = []
    for i in range(100000, 100010):
        newurls.append(["http://wwww.baidu.com/"+str(i), "http://wwww.sohu.com/"+str(i)])
    db.put(newurls)
    print(db.get(10))
    db.sync()