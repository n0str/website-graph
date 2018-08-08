import logging
from crawler import Crawler
from local import DEFAULT_HOST

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)

    crawler = Crawler(DEFAULT_HOST, DEFAULT_HOST)
    crawler.run()
