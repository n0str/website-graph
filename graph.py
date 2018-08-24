import json

from db import Page
import networkx as nx


class Graph:

    def __init__(self):
        pass

    def generate_adjacency_matrix(self, drop_static=False):
        pages = [page for page in Page.select() if not drop_static or "html" in page.content_type]
        ids = {}
        matrix = {}

        for page in pages:
            if drop_static and "text/html" not in page.content_type:
                continue
            ids[page.url] = int(page.id)
            matrix[page.id] = set()

        for page in pages:
            if drop_static and "text/html" not in page.content_type:
                continue
            for link in json.loads(page.links):
                if drop_static and link not in ids:
                    continue
                if ids[link] not in matrix[page.id]:
                    matrix[page.id].add(ids[link])

        for el in matrix:
            matrix[el] = list(matrix[el])

        with open("data\\matrix.json", "w") as w:
            w.write(json.dumps(matrix))
