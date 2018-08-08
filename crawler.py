import json
import logging
import requests
from queue import Queue
from urllib.parse import urlsplit, urljoin, urlparse
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self, website, initial_page):
        self.website = website
        self.netloc = urlsplit(website).netloc
        self.pages = {}
        self.queue = set()
        self.queue.add(initial_page)

    def run(self):
        while len(self.queue):
            nxt = self.queue.pop()
            logging.debug(f"Get {nxt} from task queue")
            self.get_page(nxt)

        with open("results.json", "w") as w:
            w.write(json.dumps(self.pages))

    def get_page(self, url):
        normalized_url = self.normalize(url)
        if normalized_url not in self.pages:
            headers = requests.head(url)
            if "text/html" not in headers.headers['content-type']:
                return

            page = requests.get(url)
            logging.debug(f"Got {url} [{page.status_code}]")

            links = [self.normalize(link) for link in self.parse_page(page.content)]

            self.pages[normalized_url] = {
                'url': normalized_url,
                'status': page.status_code,
                'links': links
            }

            for link in links:
                if link not in self.pages:
                    self.queue.add(link)

    def parse_page(self, html_page):
        soup = BeautifulSoup(html_page, "lxml")
        links = set()
        for raw_link in soup.findAll('a'):
            link = raw_link.get('href')
            params = urlsplit(link)
            netloc = params.netloc
            if params.scheme == "mailto":
                continue
            if netloc == "" or netloc == self.netloc:
                links.add(self.normalize(link))
        return links

    def normalize(self, url):
        return urljoin(self.website, url).rstrip('/').rsplit("#")[0]
