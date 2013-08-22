#!/usr/bin/env python3

import configparser

'''configure for logger moudle'''
class conf_logger:
    def __init__(self):
        #base configure for logger
        self._dir = "./log"
        self._name = "spider"
        self._level = "debug"
        self._formatter = "[%(asctime)s][%(module)s][%(levelname)s]: %(message)s"
        
        #default handler using rotating file handler
        self._handlers = {"RotatingFileHandler":{"filename":"spider.rfh.log", "mode":'a', "maxBytes":0, "backupCount":0, "encoding":None, "delay":0},
                          "TimedRotatingFileHandler":{"filename":"spider.trfh.log", "when":'H', "interval":1, "backupCount":0, "encoding":None, "delay":0, "utc":False},
                          "DatagramHandler":{"host":"0.0.0.0", "port":0}}
        

'''configure for page&file downloader'''
class conf_http_request:
    def __init__(self):
        self._header = {}
        
        self._filedir = "./files/"
        
        
class config:
    def __init__(self):
        self._config = None
    
    def load(self, path):
        self._config = configparser.ConfigParser()
        self._config.read(path)
        

        
        
    
    
