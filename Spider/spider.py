from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

class Spider:

    # Class Variables (Shared)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file =  ''
    crawled_file = ''
    queue_set = set()
    crawled_set = set()


    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('Spider One', Spider.base_url)
    
    
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue_set = file_to_set(Spider.queue_file)
        Spider.crawled_set = file_to_set(Spider.crawled_file)


    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + ' now crawling ' + page_url)
            print('In Queue : ' + str(len(Spider.queue_set)) + ' | Crawled : ' + str(len(Spider.crawled_set)))
            Spider.add_links_to_queue(Spider.gather_links())
            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            Spider.update_files()


    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode(encoding='utf-8')
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error : Cannot Crawl Page!')
            return set()
        return finder.page_links()


    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue_set:
                continue
            if url in Spider.crawled_set:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue_set.add(url)

    @staticmethod
    def update_files():
        set_to_file(queue_set, Spider.queue_file)
        set_to_file(crawled_set, Spider.crawled_file)