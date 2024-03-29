import os

TEMPLATE_DIR = os.path.abspath("./frontend/templates")
STATIC_DIR = os.path.abspath("./frontend/static")
LOCAL_CACHE_DIR = os.path.abspath("./frontend/static/local_cache")
LOCAL_UPLOADS_DIR = os.path.abspath("./frontend/static/uploads")
ALLOWED_EXTENSIONS = {'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'webp'}

class Config(object):
    SECRET_KEY = "teeesssttt"
    UPLOADED_PHOTOS_DEST = "./frontend/static/uploads"
    DB_CONFIG = {
        "user":"root",
        "password":"ece1779pass",
        "host":"localhost",
        "database":"cloudcomputing"
    }