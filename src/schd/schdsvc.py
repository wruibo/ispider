#!/usr/bin/env python3
import threading
import http.server

import schdbhd
import schdcore

'''
   scheduler service with a http server, which receive both links provided by spider
   and links wanted by the downloader.
'''
class schdsvc(threading.Thread):
    def __init__(self):
        #default local http server address
        self._addr = ''
        #default local http server port
        self._port = 80
        #stop flag for scheduler service
        self._stopflag = True
        #invoke parent's construct function
        threading.Thread.__init__(self)        
    
    def start(self):
        if(not self._stopflag): return
        self._stopflag = False
        threading.Thread.start(self)
    
    def stop(self):
        if(self._stopflag): return
        self._httpsvc.shutdown()
        self._stopflag = True
    
    def run(self):
        #http service object for scheduler
        self._httpsvc = http.server.HTTPServer((self._addr, self._port), schd_http_handler)
        #start http service
        self._httpsvc.serve_forever()
'''
   class for the http service handler, dispatch with the: GET/POST/HEAD method for 
   http request, use scheduler business handler @schd_business_handler to process 
   the actual request
'''
class schd_http_handler(http.server.BaseHTTPRequestHandler):
    #business handler object for request
    business_handler = schdbhd.schd_business_handler()
    
    
    #process the post request
    def do_POST(self):
        try:
            #try to get the post content size
            csz = self.get_post_size()
            #read the content
            content = self.rfile.read(csz)
            #parse the local path & parameters from absolute path
            lpath, lparams = self.parse_path_and_params(self.path)
            #process the request
            result, response = self.business_handler.do_request(lpath, lparams, content)
            '''valid request, response to client'''
            #set response header
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            if(response): self.send_header("Content-Length", len(response))
            self.end_headers()
            
            #write the response content
            if(response): self.wfile.write(response)
        except Exception as err:
            self.send_error(403, err)
            
    #process the get request    
    def do_GET(self):
        try:
            #parse the local path & parameters from absolute path
            lpath, lparams = self.parse_path_and_params(self.path)
            #process the request
            result, response = self.business_handler.do_request(lpath, lparams, None)
            
            '''valid request, response to client'''
            #set response header
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            if(response): self.send_header("Content-Length", len(response))
            self.end_headers()
            
            #write the response content
            if(response): self.wfile.write(response)
        except Exception as err:
            self.send_error(403, err)
            
    #process the head request
    def do_HEAD(self):
        self.send_error(403, 'unsupport request method')
    
    #get the post content size in bytes
    def get_post_size(self):
        #read the content if size more than 0
        sz = self.headers.get('content-length')
        if(not sz): return 0
        return int(sz)
    
    #parse path&parameters from request path
    def parse_path_and_params(self, path):
        pairs = path.split('?')
        n = len(pairs)
        if(n<0 or n>2): raise Exception('parse path and parameters failed.')
        if(n == 1): return pairs[0], None
        return pairs
    
if(__name__ == "__main__"):
    myschd = schdsvc()
    myschd.start()
    import time
    time.sleep(500)
    myschd.stop()
