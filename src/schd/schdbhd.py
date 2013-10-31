#!/usr/bin/env python3
import schdcore

'''
   handler to process business logic, with @schdcore as an core schedule data object,
   with store the link data and realize the schedule strategy
'''
class schd_business_handler:
    
    def __init__(self):
        #scheduler core object for core business
        self._schdcore = schdcore.schdcore()
        #business handler methods for http request
        self._handle_methods = {}
        
        #register all used business handler methods
        self.register_method('/api/json/fetchflinks', 'handle_fetch_flinks')
        self.register_method('/api/json/fetchplinks', 'handle_fetch_plinks')
        self.register_method('/api/json/postlinks', 'handle_post_links')        
    
    def register_method(self, path, method):
        self._handle_methods[path] = method
    
    def find_method(self, path):
        method = self._handle_methods.get(path)
        if(not method) return None
        return getattr(self, method)
    
    def do_request(self, path, params, content=None):
        handle_method = self.find_method(path)
        if(not handle_method): raise Exception('not method to handle the request')
        return handle_method(params, content)
    
    def handle_fetch_flinks(self, params, content=None):
        return self._schdcore.getf()
    
    def handle_fetch_plinks(self, params, content=None):
        return self._schdcore.getp()
    
    def handle_post_links(self, params, content=None):
        pass

