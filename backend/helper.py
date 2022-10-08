import sys
import random
from datetime import datetime
from flask import jsonify


    
#This function return the size of the memcache
def byteSize(memcache):
    size = sys.getsizeof(memcache)
    return size

def mbytesize(memcache):
    return byteSize(memcache)/1024

#This function checks whether the size of memcache 
#If the size is greater than config_size, then return true
#else return false
def checkSize(memcache,config_size):
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
def randomRemove(memcache):
    key = random.choice(memcache.keys())
    removed_value = memcache.pop(key,None)
    return removed_value

#This function helps remove the least recent use key
#It will return the removed value, the the value is none, then the remove
#action fails
def removeLeastRecentUse(memcache,usage):
    minValue = min(usage.values())
    key = usage.get(minValue)
    removed_value = None
    if key is not None:
        memcache.pop(key,None)
    return removed_value

#This function helps remove key and value from the memcache
def removeKey(memcache,key):
    removed_value = memcache.pop(key,None)
    return removed_value




    
    