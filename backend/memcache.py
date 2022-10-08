from distutils.command.upload import upload
from operator import truediv
import random
from backend.helper import byteSize, mbytesize
from backend.data import Data
sql_connection = Data()

class Memcache:
    memcacheKeyValue = None
    memcacheKeyUploadTime = None
    memcacheKeyUsage = None            # Record memcacheKeyUsage of each key
    itemNum = None
    itemSize = None
    requestNum = None
    hit = None
    missRate = None
    hitRate = None
    configSize = None
    replacementPolicy = None
    
    def __init__(self):
        self.memcacheKeyValue = {}
        self.memcacheKeyUploadTime = {}
        self.memcacheKeyUsage = {}
        self.itemNum = 0
        self.itemSize = 0.0
        self.requestNum = 0
        self.hit = 0
        self.missRate = 0.0
        self.hitRate = 0.0
        
        specs = sql_connection.get_config_data()
        try:
            self.configSize = specs[0][1]
            self.replacementPolicy = specs[0][2]
        except IndexError:
            self.configSize = 100.0      # Give 100MB initial size as default
            self.replacementPolicy = 1

        print(" - Backend.memcache.__init__ : Init complete, status =>")
        print(" \t configsize: ", self.configSize)
        print(" \t policy: ", self.replacementPolicy)

        pass

    def put(self, key, value, upload_time):
        '''
        This funciton will put a pair into memcache. 
        First, it will inspect if memcache is full (when self.itemSize is greater than self.configSize)
        Otherwise, it will start to remove pairs based on user selected replacement policy. 
        '''
        print(" - Backend.memcache: f:put, v:configSize:", self.configSize)
        if key in self.memcacheKeyValue:
            self.pairDelete(key)
            self.pairAdd(key, value, upload_time)
            return True
        else:
            _exceed, size = self.checkSize()
            print(" - Backend.memcache.put v:_exceed: ", _exceed)
            if _exceed == False:
                self.pairAdd(key, value, upload_time)
                return True
            else:
                if self.itemNum != 0:
                    notEmpty = True
                else:
                    notEmpty = False

                while _exceed and notEmpty:
                    if self.replacementPolicy == 1:
                        result =  self.removeLeastRecentUse()
                        if result == None:
                            notEmpty = False
                    else:
                        result = self.randomRemove()
                        if result == None:
                            notEmpty = False                        
                    _exceed, size = self.checkSize()
                if not notEmpty and _exceed:
                    print("Very rare situation happened. It's empty but size is already too large to put any pairs.")
                    print("Consider add more default size. ")
                    return False
                self.pairAdd(key, value, upload_time)
                return True
    
    def get(self, key):
        '''
        This function will search a given key within the memcache. If hit, self.hit and self.requestNum will increase and 
        value & upload_time associate with that key will be returned. If miss, nothing will be returned. 
        '''
        value = None
        upload_time = None
        if key in self.memcacheKeyValue:

            value = self.memcacheKeyValue[key]
            upload_time = self.memcacheKeyUploadTime[key]
            self.memcacheKeyUsage[key]+=1

            # Update status with hit/requestNum/hitRate/missRate
            self.hit += 1
            self.requestNum += 1

            self.hitRate = self.hit/self.requestNum
            self.missRate = 1-self.hitRate
            return value, upload_time
        else:
            # Update status with hit/requestNum/hitRate/missRate
            self.requestNum += 1

            self.hitRate = self.hit/self.requestNum
            self.missRate = 1-self.hitRate
            return None, None

            

    def invalidateKey(self, key):
        '''
        To drop a specific key. 
        '''
        if key in self.memcacheKeyValue:
            self.pairDelete(key)
        
    def refreshConfiguration(self, size, replacement_policy):
        '''
        This function will reset memcache config. After reset config, if current item size is larger than config size, memcache
        will keep removing items based on replacement policy until some conditions are meet. 
        '''
        self.configSize = float(size)
        self.replacementPolicy = replacement_policy

        _exceed, size = self.checkSize()
        print(" - Backend.memcache.put v:_exceed: ", _exceed)
        if _exceed == False:
            return True
        else:
            if self.itemNum != 0:
                notEmpty = True
            else:
                notEmpty = False
                
            while _exceed and notEmpty:
                if self.replacementPolicy == 1:
                    result =  self.removeLeastRecentUse()
                    if result == None:
                        notEmpty = False
                else:
                    result = self.randomRemove()
                    if result == None:
                        notEmpty = False                        
                _exceed, size = self.checkSize()
            if not notEmpty and _exceed:
                print("Very rare situation happened. It's empty but size is already too large to put any pairs.")
                print("Consider add more default size. ")
                return False
            return True
        
    def checkSize(self):
        '''
        This function checks whether the size of memcache.
        If the size is greater than configSize, then return true,
        else return false. Also, it returns current total size usage. 
        '''
        size = mbytesize(self.memcacheKeyValue)
        size += mbytesize(self.memcacheKeyUploadTime)
        size += mbytesize(self.memcacheKeyUsage)
        print(" - Backend.memcache.checkSize v:size: ", size)
        return size > self.configSize, size

    def randomRemove(self):
        '''
        This function helps reandom remove an item from memcache.
        it will return the removed key, if the value is none, then the remove
        action fails
        '''
        key = None
        if self.itemNum != 0:
            key = random.choice(list(self.memcacheKeyValue.keys()))
            self.pairDelete(key)
        return key


    def removeLeastRecentUse(self):
        '''
        This function helps remove the least recent use key.
        It will return the removed key, if key is none, then the remove
        action fails.
        '''
        key = None
        if self.itemNum != 0:
            key = min(self.memcacheKeyUsage)
            self.pairDelete(key)
        return key
    
    def resetMemcache(self):
        '''
        This function will remove all keys and pairs from memcache.
        '''
        self.memcacheKeyValue.clear()
        self.memcacheKeyUploadTime.clear()
        self.memcacheKeyUsage.clear()
        self.itemNum = 0
        self.itemSize = 0.0

    def getStatus(self):
        '''
        This function will return multiple items in a list required by `backend.stats.stats_update()`.
        '''
        return [self.itemNum, self.itemSize, self.requestNum, self.missRate, self.hitRate]

    def pairDelete(self, key):
        '''
        This function helps on deleting pairs. With given key, all pairs will be removed from all dict, and status will update. 
        '''
        self.memcacheKeyValue.pop(key)
        self.memcacheKeyUploadTime.pop(key)
        self.memcacheKeyUsage.pop(key) 
        self.itemNum -= 1 
        _exceed, self.itemSize = self.checkSize()

    def pairAdd(self, key, value, upload_time):
        '''
        This function helps on adding pairs. With given key, all pairs will be removed from all dict, and status will update. 
        '''
        self.memcacheKeyValue.update({key:value})
        self.memcacheKeyUploadTime.update({key:upload_time})
        self.memcacheKeyUsage.update({key:0})
        self.itemNum+=1
        _exceed, self.itemSize = self.checkSize()