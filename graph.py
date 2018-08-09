import json

from db import Page
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot

class Graph:

    def __init__(self):
        self.G = nx.DiGraph()

    def generate_adjacency_matrix(self):
        pages = [page for page in Page.select()]
        ids = {}
        matrix = {}

        for page in pages:
            ids[page.url] = int(page.id)
            matrix[page.id] = set()
            self.G.add_node(page.id)

        for page in pages:
            for link in json.loads(page.links):
                if ids[link] not in matrix[page.id]:
                    matrix[page.id].add(ids[link])
                    self.G.add_edge(page.id, ids[link])

        for el in matrix:
            matrix[el] = list(matrix[el])

        with open("matrix.json", "w") as w:
            w.write(json.dumps(matrix))

        nx.draw(self.G, with_labels=True, font_weight='bold')
        plt.savefig("path.png")
        pos = nx.nx_agraph.graphviz_layout(self.G)
        nx.draw(self.G, pos=pos)
        write_dot(self.G, 'file.dot')