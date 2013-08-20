#!/usr/bin/env python3

import os
import logging
import logging.handlers

from gerror import logerror
from config import conf_logger

class logger:
    def __init__(self):
        self._logger = None
        self._file_handlers = ["RotatingFileHandler", "TimedRotatingFileHandler"]
        self._valid_handlers = ["RotatingFileHandler", "TimedRotatingFileHandler", "DatagramHandler"]        
      
    def init(self, conf = None):
        if(conf == None):
            self.__use_default_logger()
            return
        
        if(not self.__valid_handlers(conf._handlers.keys())):
            raise logerror("invalid handlers for logger.")
        
        if(self.__has_file_handler(conf._handlers.keys())):
            if(not os.path.exists(conf._dir)):
                os.mkdir(conf._dir)
        
        self._logger = logging.getLogger(conf._name)
        self._logger.setLevel(self.__get_level_by_conf(conf))
            
        formatter = logging.Formatter(conf._formatter)
        
        handlers = self.__get_handlers_by_conf(conf)
        for handler in handlers:    
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)        

    def __use_default_logger(self):
        default_log_dir = "../log"
        if(not os.path.exists(default_log_dir)):
            os.mkdir(default_log_dir)
            
        self._logger = logging.getLogger("spider")
        self._logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(asctime)s][%(module)s][%(levelname)s]: %(message)s")
        handler = logging.handlers.RotatingFileHandler(default_log_dir+"/spider.log", 'a', 1024*1024*1024, 16, None, 0)
        handler.setFormatter(formatter)
        
        self._logger.addHandler(handler)
    
    def __valid_handlers(self, handlers):
        if(handlers <= self._valid_handlers):
            return True
        else:
            return False
        
    def __has_file_handler(self, handlers):
        if(set(handlers).isdisjoint(_file_handlers)):
            return False
        else:
            return True    

    def __get_level_by_conf(self, conf):
        level_map = {"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
        return level_map.get(conf._level, logging.DEBUG)
        
    def __get_handlers_by_conf(self, conf):
        handlers = []
        if("RotatingFileHandler" in conf._handlers):
            filename = conf._handlers["RotatingFileHandler"].get("filename", "spider.rfh.log")
            mode = conf._handlers["RotatingFileHandler"].get("mode", 'a')
            maxBytes = conf._handlers["RotatingFileHandler"].get("maxBytes", 0)
            backupCount = conf._handlers["RotatingFileHandler"].get("backupCount", 0)
            encoding = conf._handlers["RotatingFileHandler"].get("encoding", None)
            delay = conf._handlers["RotatingFileHandler"].get("delay", 0)
            rfh = logging.handlers.RotatingFileHandler(conf._dir+"/"+filename, mode, maxBytes, backupCount, encoding, delay)
            handlers.append(rfh)
            
        if("TimedRotatingFileHandler" in conf._handlers):
            filename = conf._handlers["TimedRotatingFileHandler"].get("filename", "spider.rfh.log")
            when = conf._handlers["TimedRotatingFileHandler"].get("when", 'H')
            interval = conf._handlers["TimedRotatingFileHandler"].get("interval", 0)
            backupCount = conf._handlers["TimedRotatingFileHandler"].get("backupCount", 0)
            encoding = conf._handlers["TimedRotatingFileHandler"].get("encoding", None)
            delay = conf._handlers["TimedRotatingFileHandler"].get("delay", 0)
            utc = conf._handlers["TimedRotatingFileHandler"].get("utc", False)
            trfh = logging.handlers.TimedRotatingFileHandler(conf._dir+"/"+filename, when, interval, backupCount, encoding, delay, utc)
            handlers.append(trfh)
        
        if("DatagramHandler" in conf._handlers):
            host = conf._handlers["DatagramHandler"].get("host", "0.0.0.0")
            port = conf._handlers["DatagramHandler"].get("port", 0)
            dh = logging.handlers.DatagramHandler(host, port)
            handlers.append(dh)
        
        return handlers
        
    def info(self, msg, *args, **kargs):
        self._logger.info(msg, *args, **kargs)

    def debug(self, msg, *args, **kargs):
        self._logger.debug(msg, *args, **kargs)

    def warn(self, msg, *args, **kargs):
        self._logger.warn(msg, *args, **kargs)

    def error(self, msg, *args, **kargs):
        self._logger.error(msg, *args, **kargs)
        
    def fatal(self, msg, *args, **kargs):
        self._logger.fatal(msg, *args, **kargs)

if __name__ == '__main__':
    mylog = logger()
    mylog.init()
    
    for i in range(1,10000):
        mylog.info("hello %s, age %d", 'polly', 12)
        mylog.debug("hello %s, age %d", 'polly', 12)
        mylog.warn("hello %s, age %d", 'polly', 12)
        mylog.error("hello %s, age %d", 'polly', 12)
        mylog.fatal("hello %s, age %d", 'polly', 12)
    
    
        
    
    