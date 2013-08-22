#!/usr/bin/env python3

class gerror(Exception):
    def __init__(self, *args):
        self.err = ""
        for arg in args:
            self.err += str(arg)
        
    def msg(self):
        return "[" + self.__class__.__name__ + "]: " + self.err

class dberror(gerror):
    def __init__(self, *args):
        gerror.__init__(self, *args)
    
class logerror(gerror):
    def __init__(self, *args):
        gerror.__init__(self, *args)

if( __name__ == "__main__"):
    try:
        raise dberror("test, ", "error")
    except gerror as err:
        print(err.msg())
    except:
        print("other")
        
    
    