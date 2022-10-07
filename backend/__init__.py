from flask import Flask

global memcache,usage,itemNum,itemSize,requestNum,missRate,hitRate

app = Flask(__name__)
memcache = {}
usage = {}
itemNum = 0
itemSize = 0.0
requestNum = 0
missRate = 0.0
hitRate = 0.0


from backend import main




