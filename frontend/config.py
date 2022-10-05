import os
from tkinter import TOP

TEMPLATE_DIR = os.path.abspath("./frontend/templates")
STATIC_DIR = os.path.abspath("./frontend/static")

class Config(object):
    SECRET_KEY = "teeesssttt"
    UPLOADED_PHOTOS_DEST = "./frontend/static/uploads"
    DB_CONFIG = {
        "user":"test_1",
        "password":"19970808",
        "host":"localhost",
        "database":"memcache_test_1"
    }