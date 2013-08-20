#!/usr/bin/env python3
import time
import threading
import scheduler

class worker(threading.Thread):
    _scheduler = None
    _downloader = None
    _parser = None
       
    def __init__(self, scdler, dlder, parser):
        threading.Thread.__init__(self)
        self._shceduler = scdler
        self._downloader = dlder
        self._parser = parser
    
    def run(self):
        
  
    

if __name__ == "__main__" :
    for i in range(0, 5):
        w = worker(None)
        w.start()
    
    time.sleep(10)
