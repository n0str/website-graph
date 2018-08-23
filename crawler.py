import json
import logging
from urllib.parse import urlsplit, urljoin
import requests
from bs4 import BeautifulSoup
from db import Page
from selenium_test import get_page_source


class Crawler:

    def __init__(self, website, initial_page):
        self.website = website
        self.netloc = urlsplit(website).netloc
        self.pages = {}
        self.queue = set()
        self.initial_page = initial_page
        Page.create_table()
        self.id = -1

    def run(self):
        self.id = self.load() + 1
        if not self.queue:
            self.queue.add(self.initial_page)
        while len(self.queue):
            nxt = self.queue.pop()
            logging.debug(f"Get {nxt} from task queue")
            self.get_page(nxt)

    def get_page(self, url):
        normalized_url = self.normalize(url)
        if normalized_url not in self.pages:
            headers = requests.head(url)
            content_type = headers.headers.get('content-type', '')

            if "text/html" in content_type:
                try:
                    page = requests.get(url)
                except Exception as e:
                    logging.error(f"Requests get exception: {e}")
                    Page.create(id=self.id, url=normalized_url, status=headers.status_code, content_type=content_type,
                                links=json.dumps([]))
                    self.id += 1
                    return

                logging.debug(f"Got {url} [{page.status_code}]")

                try:
                    page_content = get_page_source(url)
                except Exception as e:
                    logging.error(f"Got selenium error: [{e}]")
                    page_content = page.content

                links = [self.normalize(link) for link in self.parse_page(page_content)]
                Page.create(id=self.id,
                            url=normalized_url,
                            status=page.status_code,
                            content_type=content_type,
                            links=json.dumps(links))
                self.pages[normalized_url] = None
                for link in links:
                    if link not in self.pages:
                        self.queue.add(link)
            else:
                logging.debug(f"Add {url} with content_type: {content_type}")
                Page.create(id=self.id,
                            url=normalized_url,
                            status=headers.status_code,
                            content_type=content_type,
                            links=json.dumps({}))
            self.id += 1

    def parse_page(self, html_page):
        soup = BeautifulSoup(html_page, "lxml")
        # hack for ifmo.su to remove random articles
        # res = soup.find('ul', {'class': 'random_articles'})
        # if res:
        #     res.extract()
        links = set()
        raw_links = set([l.get('href') for l in soup.findAll('a')]) | set([l.get('href') for l in soup.findAll('link')]) \
                    | set([l.get('href') for l in soup.findAll('script')])

        for link in raw_links:
            if not link:
                continue
            params = urlsplit(link.strip())
            netloc = params.netloc
            if params.scheme == "mailto":
                continue
            if netloc == "" or netloc == self.netloc:
                links.add(self.normalize(link))
        return links

    def normalize(self, url):
        return urljoin(self.website, url).rstrip('/').rsplit("#")[0]

    def load(self):
        max_id = 1
        visited_links = set()
        all_links = set()

        for page in Page.select():
            if page.id > max_id:
                max_id = page.id
            visited_links.add(page.url)
            for link in json.loads(page.links):
                all_links.add(link)

        self.pages = {l: None for l in visited_links}
        self.queue = all_links - visited_links
        return max_id
