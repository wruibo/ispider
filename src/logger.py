#!/usr/bin/env python3

import os
import logging
import logging.handlers

class logger(logging.Logger):
    def __init__(self, cfg):
        self._logger = logging.getLogger(cfg.name)
        self._logger.setLevel(self.get_level_by_cfg(cfg))

        if(not os.path.exists(cfg.dir)):
            os.mkdir(cfg.dir)
            
        formatter = logging.Formatter(cfg.format)
        handler = eval("logging.handlers."+cfg.handler)
        handler.setFormatter(formatter)
        
        self._logger.addHandler(handler)
        
        self.log = self._logger.log
        self.debug = self._logger.debug
        self.info = self._logger.info
        self.warn = self._logger.warn
        self.warning = self._logger.warning
        self.critical = self._logger.critical
        self.error = self._logger.error
        self.fatal = self._logger.fatal
        
    def get_level_by_cfg(self, cfg):
        level_map = {"debug":logging.DEBUG, "info":logging.INFO, "warning":logging.WARNING, "error":logging.ERROR, "critical":logging.CRITICAL}
        return level_map.get(cfg.level, logging.DEBUG)

if __name__ == '__main__':
    from config import cfg_logger
    from config import config
    
    mycfg = config()
    mycfg.load("../etc/spider.cfg")
    
    mylog = logger(mycfg.logger)
    
    for i in range(1,10000):
        mylog.info("hello %s, age %d", 'polly', 12)
        mylog.debug("hello %s, age %d", 'polly', 12)
        mylog.warn("hello %s, age %d", 'polly', 12)
        mylog.error("hello %s, age %d", 'polly', 12)
        mylog.fatal("hello %s, age %d", 'polly', 12)
    
    
        
    
    