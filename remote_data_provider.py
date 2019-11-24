"""
Data provider from a remote source.
"""

import re
import requests

from chan_thread import Thread

class RemoteDataProvider:
    """
    4chan data provider
    """
    def __init__(self, board, thread_regex, output_dir):
        self.__board = board
        self.__thread_regex = thread_regex
        self.__output_dir = output_dir

    def find_threads(self):
        """'
        Finds all threads in the given board whose title meets the given thread regex.
        """
        threads = []
        catalog = requests.get(f"http://a.4cdn.org/{self.__board}/catalog.json").json()
        for page in catalog:
            page_num = page["page"]
            for thread in page["threads"]:
                match = re.search(self.__thread_regex, thread["sub"], re.MULTILINE | re.IGNORECASE)
                if match is not None:
                    threads.append(Thread(
                        board=self.__board,
                        page=page_num,
                        thread_id=thread["no"],
                        output_dir=self.__output_dir))
        return threads
