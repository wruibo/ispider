#!/usr/bin/env python3
import os
import io
import uuid
import gzip

'''
   page database has manage relate page index file and page content db files.
    
page index file:
   it records the url, ref and page content index&size in the relage page content
db file, it's format is:
           url,ref,offset,size
           url,ref,offset,size
           ......
           ......
   page index file has ".idx" as an postfix which file name is the same as page
content db file

page content db file:
   it records the gziped page content, it's format is:
           gzip page content|gzip page content|.....
   notes that there is not delimiter bettwen conent, it just continous
'''
 
class pagedb:
    def __init__(self, dbpath):
        self._dbpath = dbpath
        self._maxdbsz = 2*1024*1024*1024
        
        self.open(dbpath)
    
    def open(self, dbpath):
        #create db dirs if not exist
        if(not os.path.exists(dbpath)):
            os.makedirs(dbpath)
        
        #load all the db informations
        self._idxdb, self._contentdb, self._currfname = self.load(dbpath)
        
    def load(self, dbpath):
        #scan all files in dbpath
        files = os.listdir(dbpath)
        
        #page index information, key:url, value:[ref, pos, size, file name]
        self._pageidx = {}
        
        #page index & content files
        self._idxfiles = []
        self._contentfiles = []
        
        #scan all file in the dbpath dir
        for file in files:
            if(file.endswith(".idx")):
                self._idxfiles.append(file)
                idxfname = file[0:-4]
                #load information in the idx file
                for record in open(dbpath+"/"+file):
                    record = record.strip()
                    if(len(record) == 0): continue
                    url,ref,pos,size = record.split(",")
                    self._pageidx[url] = [ref,int(pos),int(size), idxfname]
            elif(file.endswith(".db")):
                self._contentfiles.append(file[0:-3])
            else:
                continue
        
        #create current index&db file for writing
        currfname = None
        maxfsz = self._maxdbsz
        for file in self._contentfiles:
            fpath = dbpath+"/"+file+".db"
            fsz = os.path.getsize(fpath)
            if(fsz < maxfsz):
                maxfsz = fsz
                currfname = file
                
        if(not currfname): #create new index&db file
            return self.newdb(dbpath)
        else: #use old less size index&db file
            idxdb = open(dbpath+"/"+currfname+".idx", "a+")
            contentdb = open(dbpath+"/"+currfname+".db", "a+b")
            return idxdb, contentdb, currfname
            
        
    def newdb(self, dbpath):
        #use an uuid as primary part of file name
        fname = str(uuid.uuid4())
        
        #open the db relate files
        idxdb = open(dbpath+"/"+fname+".idx", "w")
        contentdb = open(dbpath+"/"+fname+".db", "wb")
        
        #save the file name
        self._idxfiles.append(fname)
        self._contentfiles.append(fname)
        
        return idxdb, contentdb, fname
        
    def put(self, url, ref, page):
        #zip the page first
        zipdata = gzip.compress(page)
        size = len(zipdata)
        
        #get the current write pos of content file
        pos = self._contentdb.tell()
        if(pos+size > self._maxdbsz): #create new db file is size reached
            self._idxdb.close()
            self._contentdb.close()
            self._idxdb, self._contentdb, self._currfname = self.newdb(self._dbpath)
        
        #write content to db file first
        self._contentdb.write(zipdata)
        
        #write index information
        self._idxdb.write(url+","+ref+","+str(pos)+","+str(size)+"\r\n")
        
        #add new url information to page index
        self._pageidx[url] = [ref, pos, size, self._currfname]
    
    def get(self, url):
        #check if the url has exist
        if(url not in self._pageidx):
            return None
        
        data = None
        ref, pos, size, fname = self._pageidx[url]
        #if the url content in the current db read directly
        if(fname == self._currfname):
            #move file pointer to relate position
            self._contentdb.seek(pos)
            data = gzip.decompress(self._contentdb.read(size))
            
            #recover the file pointer to end
            self._contentdb.seek(0, io.SEEK_END)
        else:
            dbfpath = self._dbpath+"/"+fname+".db"
            if(os.path.isfile(dbfpath)):
                dbf = open(dbfpath, 'rb')
                dbf.seek(pos)
                data = gzip.decompress(dbf.read(size))
                dbf.close()
            
        return data
    
    def sync(self):
        self._idxdb.flush()
        self._contentdb.flush()
    
    def close(self):
        self._idxdb.close()
        self._contentdb.close()
    
    
if __name__ == "__main__":
    import urllib.request
    pdb = pagedb("../../db/page")
    
    testflag = "put"
    if(testflag == "put"):
        for i in range(0, 100000):
            strurl = "http://www.funshion.com/subject/"+str(i)+"/"
            try:
                furl = urllib.request.urlopen(strurl)
                paged = furl.read()
            
                pdb.put(strurl, '', paged)
                
                pdb.sync()
            except:
                continue
    else:
        data = pdb.get("http://www.funshion.com/subject/27/")
        fout = open("../../tmp.html", 'wb')
        fout.write(data)
        fout.close()
    
    
    