"""
prior_time module.
"""

import time
import os

def get_prior_time(timestamp_persist_file):
    """
    Gets the last time this function was called, and writes the current time to
    the last update file. If the last update file does not exist, the file will
    be created and this function will return None.
    """
    if not os.path.isfile(timestamp_persist_file):
        __write_last_update(timestamp_persist_file)
        return None

    prior_time = __read_last_update(timestamp_persist_file)
    __write_last_update(timestamp_persist_file)
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(prior_time))

def __read_last_update(timestamp_persist_file):
    with open(timestamp_persist_file, "r") as last_update_file:
        return float(last_update_file.read())

def __write_last_update(timestamp_persist_file):
    current_time = time.time()
    with open(timestamp_persist_file, "w") as last_update_file:
        last_update_file.write(str(current_time))
