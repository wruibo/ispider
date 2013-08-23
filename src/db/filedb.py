#!/usr/bin/env python3
import os
import re
import uuid
import hashlib
import urllib.request

'''
   save the resource file(not html) like picture/video/document to database.
there are 2 file type for the file database, resource index file & real resource
data file.

resource index file:
   store the resource file information, only one file. include:
        url, ref, file name(sha1 of url), size
        ......

resource file:
   store the resource file data, use sha1 of uri as file name, switch file directory
when file number limit in one dir reached
'''
class filedb:
    def __init__(self, dbpath):
        if(not os.path.exists(dbpath)):
            os.makedirs(dbpath)
        
        self._dbpath = dbpath
        self._maxdirfn = 2000
        
        self.open(dbpath)
    
    def open(self, dbpath):
        #load the file database index & file        
        self._fileidx, self._idxfile = self.loadidx(dbpath)
        
        #load the file database directories
        self._currdir, self._currfnum = self.loaddir(dbpath)
    
    def loadidx(self, dbpath):
        fileidx = {}
        idxfile = None
        
        #check if the index file is exists
        idxpath = dbpath+"/filedb.idx"
        if(not os.path.exists(idxpath)): #create index file
            idxfile = open(idxpath, 'w+')
        else: #load index information in file
            idxfile = open(idxpath, 'r+')
            for record in idxfile:
                record = record.strip()
                if(len(record)==0): continue
                uri, ref, fpath, retsize, size = record.split(",")
                fileidx[uri] = [ref, fpath, int(retsize), int(size)]
                
        return fileidx, idxfile
        
    def loaddir(self, dbpath):
        #selected directory for return
        currdir = None
        currfnum = self._maxdirfn
        
        #check if the exist directory has left space
        dirs = os.listdir(dbpath)
        for dir in dirs:
            if(not dir.endswith(".db")): continue
            dirpath = dbpath+"/"+dir
            fnum = len(os.listdir(dirpath))
            if(fnum < currfnum):
                currfnum = fnum
                currdir = dir
        
        #create new directory
        if(not currdir):
            return self.newdir(dbpath)
    
        return currdir, currfnum
    
    def newdir(self, dbpath):
        dirname = str(uuid.uuid4())+".db"
        dirpath = dbpath+"/"+dirname
        if(not os.path.exists(dirpath)): os.makedirs(dirpath)
        return dirname, 0
    
    def put(self, uri, ref):
        #check if uri has downloaded
        if(uri in self._fileidx):
            return
        
        #check file numbers in current dir
        if(not self._currfnum < self._maxdirfn):
            self._currdir, self._currfnum = self.newdir(self._dbpath)
        try:    
            #build an url request object to uri
            conn = urllib.request.urlopen(uri)
            #retrival the response message
            respmsg = conn.info()
            retfsz = respmsg.get('Content-Length')
            if(not retfsz): 
                retfsz = -1
            else:
                retfsz = int(retfsz)
            
            #get file name from response header
            fname = respmsg.get_filename()
            if(not fname): 
                items = re.search("([^\/]+)\.([^\.]+)\Z", uri)
                if(not items): #use uri sha1 as file name
                    m = hashlib.sha1()
                    m.update(uri.encode())
                    fname = m.hexdigest()
                else:
                    fname = items.group(0)
                    
            #create local file
            relatepath = self._currdir+"/"+fname
            fpath = self._dbpath+"/"+relatepath
            locfile = open(fpath, "wb")
            #read the file and write to local file
            fsz = 0
            data = conn.read(16*1024)
            while(data):
                locfile.write(data)
                fsz += len(data)
                data = conn.read(16*1024)
            locfile.close()
            
            #write index file
            self._idxfile.write(uri+","+ref+","+relatepath+","+str(retfsz)+","+str(fsz)+"\r\n")
            self._fileidx[uri] = [ref, relatepath, retfsz, fsz]
            
            #update current directory information
            self._currfnum += 1
        except:
            print("404:", uri)
        
    def get(self, uri):
        return self._fileidx.get(uri)        
    
    def close(self):
        self.idxfile.close()
    

if(__name__ == "__main__"):
    fdb = filedb("../../db/files")
    for i in range(256, 1000):
        for j in range(560, 1000):
            uri = "http://img0.fspcdn.com/pictures/"+str(i)+"/"+str(j)+"/"+str(i*1000+j)+".jpg"
            fdb.put(uri, "http://www.funshion.com/")
    fdb.close()