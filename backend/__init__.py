from flask import Flask

global memcache

app = Flask(__name__)
memcache = {}

from backend import main




