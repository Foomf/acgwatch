"""
Thread class.
"""

import os.path
import datetime
import requests

class ThreadData:
    """
    4chan thread data.
    """
    def __init__(self, timestamp, reply_count, image_count, unique_ip_count, page):
        self.timestamp = timestamp
        self.reply_count = reply_count
        self.image_count = image_count
        self.unique_ip_count = unique_ip_count
        self.page = page

    def to_csv_entry(self):
        """
        Converts thread data to a csv entry
        """
        return (
            f"{self.timestamp},"
            f"{self.reply_count},"
            f"{self.image_count},"
            f"{self.unique_ip_count},"
            f"{self.page}")

class Thread:
    """
    Represents a 4chan thread.
    """
    def __init__(self, board, page, thread_id, output_dir):
        self.__board = board
        self.__page = page
        self.__thread_id = thread_id
        self.__output_dir = output_dir

    def get_data(self, timestamp):
        """
        Retrieves thread data, or returns None if thread data hasn't changed.
        """
        headers = self.__make_headers(timestamp)
        req = requests.get(
            url=f"http://a.4cdn.org/{self.__board}/thread/{self.__thread_id}.json",
            headers=headers)
        if req.status_code == 304:
            return self.__get_prior_data()
        if req.status_code == 200:
            thread = req.json()
            thread_op = thread["posts"][0]
            return ThreadData(
                timestamp=datetime.datetime.now().isoformat(),
                reply_count=thread_op["replies"],
                image_count=thread_op["images"],
                unique_ip_count=thread_op["unique_ips"],
                page=self.__page)
        print(f"ERR {req.status_code}")
        return None

    def get_filename(self):
        """
        Gets the file that this thread data is stored at.
        """
        filename = f"{self.__thread_id}.csv"
        return os.path.join(self.__output_dir, filename)

    def __get_prior_data(self):
        """
        Gets the most recent recorded csv entry, with the time updated to be "now".
        """
        filename = self.get_filename()
        if not os.path.isfile(filename):
            return None
        with open(filename) as thread_file:
            lines = thread_file.read().splitlines()
            if len(lines) <= 1:
                return None
            last_line = lines[-1]
        return Thread.__read_line(last_line)

    @staticmethod
    def __read_line(text, timestamp=None):
        parts = text.split(",")
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()
        return ThreadData(
            timestamp=timestamp,
            reply_count=parts[0],
            image_count=parts[1],
            unique_ip_count=parts[2],
            page=parts[3])

    def __make_headers(self, timestamp):
        if not os.path.isfile(self.get_filename()) or timestamp is None:
            return {}
        return {"If-Modified-Since": timestamp}
