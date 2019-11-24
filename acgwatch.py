"""
/acg/ thread watcher.
"""

from prior_time import get_prior_time
from remote_data_provider import RemoteDataProvider

TOML_CONFIG_FILE = "config.toml"

THREAD_REGEX = r"(\/acg\/)|(animal\scrossing)"
BOARD = "vg"

def __main():
    timestamp = get_prior_time()
    provider = RemoteDataProvider(BOARD, THREAD_REGEX, ".")
    for thread in provider.find_threads():
        data = thread.get_data(timestamp)
        if data is None:
            print("No data!")
            continue
        with open(thread.get_filename(), "a") as thread_file:
            thread_file.write(data.to_csv_entry())

if __name__ == '__main__':
    __main()
