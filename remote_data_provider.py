"""
Data provider from a remote source.
"""

import re
import requests

from chan_thread import Thread

def find_threads(board, thread_regex, output_dir):
    """'
    Finds all threads in the given board whose title meets the given thread regex.
    """
    threads = []
    catalog = requests.get(f"http://a.4cdn.org/{board}/catalog.json").json()
    for page in catalog:
        page_num = page["page"]
        for thread in page["threads"]:
            match = re.search(thread_regex, thread["sub"], re.MULTILINE | re.IGNORECASE)
            if match is not None:
                threads.append(Thread(
                    board=board,
                    page=page_num,
                    thread_id=thread["no"],
                    output_dir=output_dir))
    return threads
