import logging
from crawler import Crawler
from graph import Graph
from local import DEFAULT_HOST

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    crawler = Crawler(DEFAULT_HOST, DEFAULT_HOST)

    # Run crawling process
    # crawler.run()

    # Save statistics for ML
    # g = Graph()
    # g.generate_adjacency_matrix()
