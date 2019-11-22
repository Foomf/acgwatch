"""
prior_time module.
"""

import time
import os

LAST_UPDATE_FILE_PATH = os.path.join(os.path.dirname(__file__), "lastupdate")

def get_prior_time():
    """
    Gets the last time this function was called, and writes the current time to
    the last update file. If the last update file does not exist, the file will
    be created and this function will return None.
    """
    if not os.path.isfile(LAST_UPDATE_FILE_PATH):
        __write_last_update()
        return None

    prior_time = __read_last_update()
    __write_last_update()
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(prior_time))

def __read_last_update():
    with open(LAST_UPDATE_FILE_PATH, "r") as last_update_file:
        return float(last_update_file.read())

def __write_last_update():
    current_time = time.time()
    with open(LAST_UPDATE_FILE_PATH, "w") as last_update_file:
        last_update_file.write(str(current_time))
