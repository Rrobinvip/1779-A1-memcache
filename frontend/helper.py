import requests
from frontend.config import LOCAL_CACHE_DIR
import os
import base64

def api_call(url, params=None):
    '''
    This function is used to use the api. \n
    The flag will need to be updated in the future to accommodate different api's.
    '''
    return requests.get(url, params, timeout=0.5)

def write_img_local(filename, decode_value):
    '''
    This function is used to decode the image and save it to the local path.
     - filename: The name of the file used to store the image.
     - decode_value: Images encrypted with decode64.
    '''
    final_path = os.path.join(LOCAL_CACHE_DIR, filename)
    image_decode = base64.b64decode(decode_value)
    file = open(final_path, "w")
    file.write(image_decode)
    file.close