"""
/acg/ thread watcher.
"""

import os.path

import toml

from prior_time import get_prior_time
from remote_data_provider import find_threads

TOML_CONFIG_FILE = "config.toml"

THREAD_REGEX = r"(\/acg\/)|(animal\scrossing)"
BOARD = "vg"

def __main():
    config = toml.load("config.toml")
    out_dir = config["output_dir"]

    timestamp = get_prior_time()
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    for thread in find_threads(BOARD, THREAD_REGEX, out_dir):
        data = thread.get_data(timestamp)
        if data is None:
            print("No data!")
            continue
        firstwrite = not os.path.exists(thread.get_filename())
        with open(thread.get_filename(), "a") as thread_file:
            if firstwrite:
                thread_file.write("time,replies,images,posters,page\n")
            thread_file.write(data.to_csv_entry())

if __name__ == '__main__':
    __main()
