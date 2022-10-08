import sys
import random
from datetime import datetime
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
    
    #This function helps reandom remove an item from memcache
    #it will return the removed value, if the value is none, then the remove
    #action fails
    def randomRemove(self,memcache):
        key = random.choice(memcache.keys())
        removed_value = memcache.pop(key,None)
        return removed_value
    
    #This function helps remove the least recent use key
    #It will return the removed value, the the value is none, then the remove
    #action fails
    def removeLeastRecentUse(self,memcache,usage):
        #find least recent use datetime
        minValue = min(usage.values())
        #find key value with minValue
        key_list = list(usage.keys())
        value_list = list(usage.values())
        position = value_list.index(minValue)
        key = key_list(position)
        removed_value = memcache.pop(key,None)
        return removed_value
    
    #This function helps remove key and value from the memcache
    def removeKey(self,memcache,key):
        removed_value = memcache.pop(key,None)
        return removed_value




    
    