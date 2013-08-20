#!/usr/bin/env python3

import configparser

class cfg_base:
    def __init__(self):
        pass
    
    def __getattribute__(self, name):
        name = name.lstrip('_')
        return object.__getattribute__(self, name)
    
    def __setattr__(self, name, val):
        name = name.lstrip('_')
        object.__setattr__(self, name, val)
        
    def parse(self, cfg):
        pass

'''configure for logger moudle'''
class cfg_logger(cfg_base):
    def __init__(self):
        self._dir = "./log"
        self._name = "spider"
        self._level = "debug"
        self._format = "[%(asctime)s][%(module)s][%(levelname)s]: %(message)s"
        self._handler = "RotatingFileHandler('spider.rfh.log', 'a', 0, 0, None, 0)"
        
    def parse(self, cfg):
        self._dir = cfg.get("log", "dir")
        self._name = cfg.get("log", "name")
        self._level = cfg.get("log", "level")
        self._format = cfg.get("log", "format")
        self._handler = cfg.get("log", "handler")

'''configure for page&file downloader'''
class cfg_httpreq(cfg_base):
    def __init__(self):
        self._header = {}
        self._filedir = "./files/"
        
        
class config(cfg_base):
    def __init__(self, path):
        self._config = configparser.RawConfigParser()
        self._config.read(path)
        
        self._logger = cfg_logger()
        self._logger.parse(self._config)

    
    #just for debug
    def dump(self):
        for section in self._config.sections():
            print("[", section, "]")
            for item in self._config.items(section):
                print(item[0], "=", item[1])

if(__name__ == "__main__"):
    mycfg = config("../etc/spider.cfg")
    print(mycfg.logger.format)
    print(mycfg.logger.handler)
    
        
        
    
    
