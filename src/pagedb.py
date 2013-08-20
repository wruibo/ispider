#!/usr/bin/env python3
import os
import uuid

from gerror import dberror
from logger import logger

'''
    page database is a file, the file has size limit, every file struct like this:
    |db index()|db content|
    |url(string)|sha1(20B)|file offset(in byte)|
'''
 
class pagedb:    
    DB_SIZE_LIMIT = 2*1024*1024*1024 # db file limit by max 2GB bytes
    
    def __init__(self, prefix = "pagedb"):
        self._prefix = prefix
        self._db_pos = 0
        
    
    def openw(self, db=None):        
        if(not db): # create new page database
            self._db = self._prefix + "." + uuid.uuid1().hex            
        else:
            self._db = db

        self._db_file = self._db + ".db"
        self._idx_file = self._db + ".idx"

        try:
            self.fidx = open(self._idx_file, 'a+b')
            self.fdb = open(self._db_file, 'a+b')
        except IOError as err:
            logger.error(err.strerror)

    def openr(self, db):
        self._db_file = db + ".db"
        self._idx_file = db + ".idx"
        
        if(not os.path.isfile(self._db_file) or not os.path.isfile(self._idx_file)):
            raise dberror("db file "+self._db_file + " or index file " + self._idx_file + " is not exist")
        
            
    def write(self, url, ref, pagedata):
        self.fdb.write(pagedata["header"])
        self.fdb.write(pagedata["content"])
        
    
    def read(self):
        pass
    
    def close(self):
        pass
    
    
if __name__ == "__main__":
    pass
    