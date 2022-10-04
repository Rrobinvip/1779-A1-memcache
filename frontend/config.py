import os
from tkinter import TOP

TEMPLATE_DIR = os.path.abspath("./frontend/templates")
STATIC_DIR = os.path.abspath("./frontend/static")

class Config(object):
    SECRET_KEY = 'teeesssttt'
    UPLOADED_PHOTOS_DEST = "./frontend/static/uploads"
