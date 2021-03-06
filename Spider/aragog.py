import threading
import argparse
from queue import Queue
from spider import Spider
from xdomain import *
from general import *


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Python Based Web Crawler")
    parser.add_argument("-p",
                        "--project",
                        dest="project",
                        help="Project/Directory",
                        default='aragog_project')
    parser.add_argument("-u",
                        "--url",
                        dest="url",
                        help="Project/Homepage")
    parser.add_argument("-t",
                        "--threads",
                        dest="threads",
                        help="Project/Threads",
                        default="8")

    return parser


PROJECT_NAME = ''
HOMEPAGE = ''
NUMBER_OF_THREADS = 8


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    PROJECT_NAME = args.project
    HOMEPAGE = args.url
    NUMBER_OF_THREADS = int(args.threads)


DOMAIN_NAME = get_domain(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
queue = Queue()

# Aragog
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create Workers
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        web = threading.Thread(target=work)
        web.daemon = True
        web.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for url in file_to_set(QUEUE_FILE):
        queue.put(url)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_urls = file_to_set(QUEUE_FILE)
    if len(queued_urls) > 0:
        print(str(len(queued_urls)) + ' urls in the queue')
        create_jobs()
    else:
        print('\nCrawling Complete\n')

create_workers()
crawl()