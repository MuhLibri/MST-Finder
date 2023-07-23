from tkinter import *
from tkinter import filedialog
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from Prim import searchPrim
from Kruskal import searchKruskal
from Utils import matrixToEdges


# Global Variables
adjacencyMatrix = []
nameList = []
edgeList = []


# Functions
def openFile():
    global adjacencyMatrix
    global nameList
    global edgeList

    file = filedialog.askopenfile(title="Select a File", filetypes=[("txt", "*.txt")])
    adjacencyMatrix = [[int(num.strip()) for num in line.split(' ')] for line in file]
    file.close()

    textFile.config(state=NORMAL)
    textFile.delete(0.0, END)
    textFile.insert(END, file.name)
    textFile.config(state=DISABLED)

    nameList.clear()
    for i in range(len(adjacencyMatrix)):
        nameList.append(str(i+1))

    edgeList = matrixToEdges(adjacencyMatrix, nameList)

    visualizeGraph()


def visualizeGraph():
    plt.clf()

    graph = nx.Graph()

    for name in nameList:
        graph.add_node(name)

    graph.add_weighted_edges_from(edgeList)

    pos = nx.spring_layout(graph, seed=5)
    nx.draw_networkx_nodes(graph, pos, node_size=[len(v) * 1000 for v in graph.nodes()])
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges, width=5)
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=10)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    canvas.draw()


def solve(algorithm):
    plt.clf()

    if (algorithm == "prim"):
        edgeMST = searchPrim(edgeList, len(adjacencyMatrix))
    else:
        edgeMST = searchKruskal(edgeList, len(adjacencyMatrix))

    graph = nx.Graph()

    for name in nameList:
        graph.add_node(name)

    graph.add_weighted_edges_from(edgeList)

    eNotPath = [(u, v) for (u, v, d) in graph.edges(data=True) if (u, v, d) not in edgeMST]

    pos = nx.spring_layout(graph, seed=5)
    nx.draw_networkx_nodes(graph, pos, node_size=[len(v) * 1000 for v in graph.nodes()])
    nx.draw_networkx_edges(graph, pos, edgelist=eNotPath, width=5)
    nx.draw_networkx_edges(graph, pos, edgelist=edgeMST, width=5, edge_color="red")
    nx.draw_networkx_labels(graph, pos, font_size=20, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=10)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()

    canvas.draw()


def addNode():
    print("Add Node")
    return


def deleteNode():
    print("Delete Node")
    return


# ====================================================================================================================================================================================================================================================================================


# GUI
root = Tk()
root.title("MST Finder")
root.config(bg="darkgray")


# GUI Variables
custom_font = font.Font(size=11)
mainPadding = 20


# Frame Right
frameRight = Frame(root, height=700, width=250, bg="#696969", padx=mainPadding, pady=mainPadding)
frameAlgorithm = Frame(frameRight, bg="darkgray")
frameSolve = Frame(frameAlgorithm, bg="#696969")
frameConfig = Frame(frameRight, bg="#696969")

# Algorithm Section
algorithmLabel = Label(frameAlgorithm, text="Algorithm:", font=(20), bg="darkgray")
algorithmChoice = StringVar()
algorithmChoice.set("prim")
primButton = Radiobutton(frameAlgorithm, text="Prim", font=(20), variable=algorithmChoice, value="prim", bg="darkgray", activebackground="darkgray", activeforeground="white")
kruskalButton = Radiobutton(frameAlgorithm, text="Kruskal", font=(20), variable=algorithmChoice, value="kruskal", bg="darkgray", activebackground="darkgray", activeforeground="white")
solveButton = Button(frameSolve, text="Solve", font=custom_font, command=lambda: solve(algorithmChoice.get()), width=7)
resetButton = Button(frameSolve, text="Reset", font=custom_font, command=visualizeGraph, width=7)

# Config Section
addNodeButton = Button(frameConfig, text="Add Node", font=custom_font, command=addNode, width=10)
deleteNodeButton = Button(frameConfig, text="Delete Node", font=custom_font, command=deleteNode(), width=10)

# Pack
addNodeButton.pack(pady=7)
deleteNodeButton.pack(pady=7)
frameConfig.pack(side=BOTTOM)
algorithmLabel.pack(padx=20, pady=(20, 0), anchor="w")
primButton.pack(padx=20, anchor="w")
kruskalButton.pack(padx=20, pady=(0, 20), anchor="w")
resetButton.pack(side=LEFT, padx=(0,15), pady=(15, 0))
solveButton.pack(side=RIGHT, pady=(15, 0))
frameSolve.pack(fill=X)
frameAlgorithm.pack(side=TOP, pady=100)
frameRight.pack_propagate(False)
frameRight.pack(side=RIGHT, fill=Y)


# Frame Graph
frameGraph = Frame(root, height=600, width=900, bg="#777778")

# Canvas
fig = plt.figure(figsize=(9, 6))
canvas = FigureCanvasTkAgg(fig, master=frameGraph)

# Pack
canvas.get_tk_widget().pack(expand=True, fill=BOTH)
frameGraph.pack(side=TOP, expand=TRUE, fill=BOTH, padx=mainPadding, pady=(mainPadding, 0))


# Frame Bottom
frameBottom = Frame(root, height=100, width=900, bg="darkgray")
frameOpenFile = Frame(frameBottom, bg="darkgray")

# Buttons
openFileButton = Button(frameOpenFile, text="Open File", font=custom_font, command=openFile, width=10)

# Text File
textFile = Text(frameOpenFile, height=1, width=75, font=custom_font, padx=6, pady=6, relief="sunken")
textFile.config(state=DISABLED)

# Pack
openFileButton.pack(side=LEFT)
textFile.pack(side=RIGHT, expand=TRUE, fill=X)
frameOpenFile.pack(side=LEFT, anchor="n", expand=TRUE, fill=X)
frameBottom.pack(side=BOTTOM, expand=TRUE, fill=X, padx=mainPadding)


root.mainloop()