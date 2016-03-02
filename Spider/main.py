import threading
from queue import Queue
from spider import Spider
from xdomain import *
from general import *

PROJECT_NAME = 'Example'
HOMEPAGE = 'https://www.example.com/'
DOMAIN_NAME = get_domain(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

# Aragog
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create Workers
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        web = threading.Thread(target=work)
        web.daemon = True
        web.start()

# Crawl Next
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def create_jobs():
    for url in file_to_set(QUEUE_FILE):
        queue.put(url)
    queue.join()
    crawl()

# Crawl Through To Crawl Queue
def crawl():
    queued_urls = file_to_set(QUEUE_FILE)
    if len(queued_urls) > 0:
        print(str(len(queued_urls)) + ' urls in the queue.')
        create_jobs()

create_workers()
crawl()