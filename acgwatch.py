import requests
import re
import time
import os.path
import datetime

THREAD_REGEX = r"(\/acg\/)|(animal\scrossing)"
BOARD = "vg"

def get_filename(threadId):
    filename = "%s.csv" % threadId
    return os.path.join(os.path.dirname(__file__), filename)

def find_threads():
    threads = []
    catalog = requests.get("http://a.4cdn.org/%s/catalog.json" % BOARD).json()
    for page in catalog:
        for thread in page["threads"]:
            match = re.search(THREAD_REGEX, thread["sub"], re.MULTILINE | re.IGNORECASE)
            if match is not None:
                threads.append((thread["no"], page["page"]))
    return threads

def get_prior_data(threadId):
    filename = get_filename(threadId)
    if not os.path.isfile(filename):
        return None
    with open(filename) as f:
        lines = f.read().splitlines()
        if len(lines) <= 1:
            return None
        return lines[-1]

def get_prior_time():
    currtime = time.time()
    lastupdatefile = os.path.join(os.path.dirname(__file__), "lastupdate")
    if os.path.isfile(lastupdatefile):
        with open(lastupdatefile, "r") as f:
            priortime = float(f.read())
        with open(lastupdatefile, "w") as f:
            f.write(str(currtime))
        return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(priortime))
    with open(lastupdatefile, "w") as f:
        f.write(str(currtime))
    return None

def make_headers(threadId, timestamp):
    if not os.path.isfile(get_filename(threadId)) or timestamp is None:
        return { }

    return { "If-Modified-Since": timestamp }

def write(f, now, replies, images, posters, page):
    f.write("%s,%s,%s,%s,%s\n" % (now, replies, images, posters, page))

if __name__ == '__main__':
    threads = find_threads()
    timestamp = get_prior_time()
    now = datetime.datetime.now().isoformat()

    for threadId,page in threads:
        headers = make_headers(threadId, timestamp)
        filename = get_filename(threadId)
        r = requests.get("http://a.4cdn.org/%s/thread/%s.json" % (BOARD, threadId), headers=headers)
        if r.status_code == 304:
            print("Copying prior data")
            priordata = get_prior_data(threadId)
            if priordata is None:
                print("Nothing to copy!")
            else:
                datapoints = priordata.split(",")
                with open(filename, "a") as f:
                    write(f, now, datapoints[1], datapoints[2], datapoints[3], page)
        elif r.status_code == 200:
            print("Writing new data")
            firstwrite = not os.path.exists(filename)
            thread = r.json()
            op = thread["posts"][0]
            replies = op["replies"]
            images = op["images"]
            posters = op["unique_ips"]
            with open(filename, "a") as f:
                if firstwrite:
                    f.write("time,replies,images,posters,page\n")
                write(f, now, replies, images, posters, page)
        else:
            print("ERR %s" % r.status_code)