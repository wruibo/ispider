#!/usr/bin/env python3
import os
import uuid
import urllib.request

'''
   save the resource file(not html) like picture/video/document to database.
there are 2 file type for the file database, resource index file & real resource
data file.

resource index file:
   store the resource file information, only one file. include:
        url, ref, file name(sha1 of url), file size
        ......

resource file:
   store the resource file data, use sha1 of url as file name, switch file directory
when file number limit in one dir reached
'''
class filedb:
    def __init__(self, dbpath):
        if(not os.path.exists(dbpath)):
            os.makedirs(dbpath)
        
        self._dbpath = dbpath
        self._maxdirfn = 2000
        
        self.open(dbpath)
        
    #open the file database by specified @dbpath
    def open(self, dbpath):
        #load the file database index & file        
        self._fileidx, self._idxfile = self.loadidx(dbpath)
        
        #load the file database directories
        self._curr_dir, self._curr_fnum = self.loaddir(dbpath)
    
    #load the index information of file database @dbpath
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
                url, ref, fpath, size = record.split(",")
                fileidx[url] = [ref, fpath, int(size)]
                
        return fileidx, idxfile
    
    #load the current directory of database @dbpath    
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
    
    #switch current file directory of database
    def newdir(self, dbpath):
        dirname = str(uuid.uuid4())+".db"
        dirpath = dbpath+"/"+dirname
        if(not os.path.exists(dirpath)): os.makedirs(dirpath)
        return dirname, 0

    #open a new file in db for saving data
    def fopen(self, url, ref, fname):
        #record the current file information
        self._curr_url, self._curr_ref, self._curr_fname = url, ref, fname
    
        #check if url has downloaded
        if(self._curr_url in self._fileidx):
            return False
        
        #check file numbers in current dir
        if(not self._curr_fnum < self._maxdirfn):
            self._curr_dir, self._curr_fnum = self.newdir(self._dbpath)
        
        #create current local file
        self._curr_fpath = self._dbpath+"/"+self._curr_dir+"/"+fname
        self._curr_file = open(self._curr_fpath, "wb")
        
        #set current new file size
        self._curr_fsize = 0
        
        #update current directory information
        self._curr_fnum += 1
            
    #write data to current file
    def fwrite(self, data):
        self._curr_file.write(data)
        self._curr_fsize += len(data)
    
    #close the current file
    def fclose(self):
        self._curr_file.close()
                
        self._idxfile.write(self._curr_url+","+self._curr_ref+","+self._curr_fpath+","+str(self._curr_fsize)+"\r\n")
        self._fileidx[self._curr_url] = [self._curr_ref, self._curr_fpath, self._curr_fsize]
        
        self._curr_url, self._curr_ref, self._curr_fname, self._curr_fpath, self._curr_file, self._curr_fsize = None, None, None, None, None, None
        

    def get(self, url):
        return self._fileidx.get(url)        
    
    def close(self):
        self._idxfile.close()
    

if(__name__ == "__main__"):
    fdb = filedb("../../db/files")
    for i in range(1, 3000):
        fdb.fopen(str(i), str(i), str(i))
        fdb.fwrite(b"test")
        fdb.fclose()
        
    fdb.close()