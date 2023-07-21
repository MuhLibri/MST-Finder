import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt


def readFile() -> list[list[int]]:
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfile()
    adjacencyMatrix = [[int(num.strip()) for num in line.split(' ')] for line in file]
    file.close()

    return adjacencyMatrix


def matrixToEdges(adjacencyMatrix: list[list[float]], nameList: list[str]) -> list[tuple((str, str, int))]:
    edgeList: list[tuple((str, str, int))] = []

    for i in range(len(adjacencyMatrix)):
        for j in range(i+1, len(adjacencyMatrix)):
            if (adjacencyMatrix[i][j] != 0):
                edgeList.append((nameList[i], nameList[j], adjacencyMatrix[i][j]))

    return edgeList


def drawGraph(adjacencyMatrix: list[list[float]], nameList: list[str]):
    G = nx.Graph()
    i = 0

    for name in nameList:
        G.add_node(name)
        i += 1

    for i in range (len(nameList)):
        for j in range (len(adjacencyMatrix[i])):
            if (adjacencyMatrix[i][j] != 0):
                G.add_edge(nameList[i], nameList[j], weight = adjacencyMatrix[i][j])

    pos = nx.spring_layout(G, seed=3)
    nx.draw_networkx_nodes(G, pos, node_size=[len(v) * 1000 for v in G.nodes()])
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=5)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=20)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def showMST(adjacencyMatrix: list[list[float]], nameList : list[str], edgeMST: list[str]):
    G = nx.Graph()
    i = 0

    for name in nameList:
        G.add_node(name)
        i += 1

    for i in range (len(nameList)):
        for j in range (len(adjacencyMatrix[i])):
            if (adjacencyMatrix[i][j] != 0):
                G.add_edge(nameList[i], nameList[j], weight = adjacencyMatrix[i][j])

    eNotPath = [(u, v) for (u, v, d) in G.edges(data=True) if (u, v, d) not in edgeMST]

    pos = nx.spring_layout(G, seed=3)
    nx.draw_networkx_nodes(G, pos, node_size=[len(v) * 1000 for v in G.nodes()])

    nx.draw_networkx_edges(G, pos, edgelist=eNotPath, width=5)
    nx.draw_networkx_edges(G, pos, edgelist=edgeMST, width=5, edge_color="violet")

    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=20)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()