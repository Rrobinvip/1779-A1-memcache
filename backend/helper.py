import sys
from flask import jsonify

class helper:
    def __init__(self):
        None
    
    #This function return the size of the memcache
    def byteSize(self,memcache):
        size = sys.getsizeof(memcache)
        return size
    
    #This function checks whether the size of memcache 
    #If the size is greater than config_size, then return true
    #else return false
    def checkSize(self,memcache,config_size):
        result = False
        size = sys.getsizeof(memcache)
        if size > config_size:
            return result
        else:
            result = True
            return result
    