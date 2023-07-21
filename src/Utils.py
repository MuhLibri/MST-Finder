import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt
from queue import Queue


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


def isIncident(edge1: tuple((str, str, int)), edge2: tuple((str, str, int))) -> bool:
    return (edge1[0] == edge2[0]) or (edge1[0] == edge2[1]) or (edge1[1] == edge2[0]) or (edge1[1] == edge2[1])


def isCircuit(edge: tuple((str, str, int)), mst: list[tuple((str, str, int))]) -> bool:
    circuit: bool = False
    listVisitedNode: list[str] = []
    nodeQueue: Queue = Queue()
    nodeQueue.put(edge[0])

    while (not nodeQueue.empty()) and (not circuit):
        currentNode = nodeQueue.get()
        listVisitedNode.append(currentNode)
        for x in mst:
            if (x[0] == currentNode) and (not (x[1] in listVisitedNode)):
                nodeQueue.put(x[1])
            elif (x[1] == currentNode) and (not (x[0] in listVisitedNode)):
                nodeQueue.put(x[0])
        if (currentNode == edge[1]):
            circuit = True

    return circuit


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