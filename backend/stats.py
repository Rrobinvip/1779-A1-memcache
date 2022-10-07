from backend.data import Data
import time

class Stats:
    
    mysql_connection = Data()

    def __init__(self):
        pass

    #This function update the statistics every 5 second
    def stats_update(self,itemNum,itemSize,requestNum,missRate,hitRate):
        while True:
            self.mysql_connection.insert_stat_data(itemNum,itemSize,requestNum,missRate,hitRate)
            time.sleep(5)

