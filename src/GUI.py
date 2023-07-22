from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from Prim import searchPrim
from Kruskal import searchKruskal
from Utils import *
from tkinter import font


# Global Variables
adjacencyMatrix = []
nameList = []


# Functions
def openFile():
    global adjacencyMatrix
    file = filedialog.askopenfile(title="Select a File", filetypes=[("txt", "*.txt")])
    adjacencyMatrix = [[int(num.strip()) for num in line.split(' ')] for line in file]
    textFile.config(state=NORMAL)
    textFile.delete(0.0, END)
    textFile.insert(END, file.name)
    textFile.config(state=DISABLED)
    file.close()


def visualizeGraph():
    children = frameGraph.winfo_children()
    if (len(children) != 0):
        children[0].destroy()
    fig = plt.figure(figsize=(9, 6))


    for i in range(len(adjacencyMatrix)):
        nameList.append(str(i+1))


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

    # fg = plt.figure(figsize=(8, 6), dpi=100)

    canvas = FigureCanvasTkAgg(fig, master=frameGraph)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)


def solve(algorithm):
    children = frameGraph.winfo_children()
    if (len(children) != 0):
        children[0].destroy()
    fig = plt.figure(figsize=(9, 6))


    # for i in range(len(adjacencyMatrix)):
    #     nameList.append(str(i+1))


    if (algorithm == "prim"):
        edgeMST = searchPrim(matrixToEdges(adjacencyMatrix, nameList), len(adjacencyMatrix))
    else:
        edgeMST = searchKruskal(matrixToEdges(adjacencyMatrix, nameList), len(adjacencyMatrix))


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



    canvas = FigureCanvasTkAgg(fig, master=frameGraph)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=BOTH)

# ====================================================================================================================================================================================================================================================================================

# GUI
root = Tk()
root.title("MST Finder")
root.config(bg="darkgray")
# root.config(height=1000, width=1400, bg="black")


# GUI Varibles
custom_font = font.Font(size=11)


# Frame Right
frameRight = Frame(root, height=800, width=250, bg="#696969")
frameAlgorithm = Frame(frameRight, bg="darkgray")
frameSolve = Frame(frameAlgorithm, bg="#696969")


aLabel = Label(frameAlgorithm, text="Algorithm:", font=custom_font, bg="darkgray")
a = StringVar()
a.set("prim")
solveButton = Button(frameSolve, text="Solve", font=custom_font, command=lambda: solve(a.get()), height=1, width=10)


aLabel.pack(padx=20, pady=(20, 0))
buttonPrim = Radiobutton(frameAlgorithm, text="Prim", font=custom_font, variable=a, value="prim", bg="darkgray", activebackground="darkgray", activeforeground="white")
buttonKruskal = Radiobutton(frameAlgorithm, text="Kruskal", font=custom_font, variable=a, value="kruskal", bg="darkgray", activebackground="darkgray", activeforeground="white")


buttonPrim.pack(padx=10, anchor="w")
buttonKruskal.pack(padx=10, pady=(0, 20), anchor="w")
solveButton.pack(pady=(20, 0))
frameSolve.pack(fill=X)
frameAlgorithm.pack(pady=(200,0))
frameRight.pack_propagate(False)
frameRight.pack(side=RIGHT, fill=Y)


# Frame Graph
frameGraph = Frame(root, height=600, width=900, bg="#777778")
frameGraph.pack(side=TOP, expand=TRUE, fill=BOTH, padx=25, pady=25)



# Frame Bottom
frameBottom = Frame(root, height=200, width=900, bg="darkgray")
frameOpenFile = Frame(frameBottom, bg="darkgray")
frameConfig = Frame(frameBottom, bg="darkgray")

# Button
openFileButton = Button(frameOpenFile, text="Open File", font=custom_font, command=openFile, width=10)
visualizeButton = Button(frameConfig, text="Visualize", font=custom_font, command=visualizeGraph, width=10)
addNodeButton = Button(frameConfig, text="Add Node", font=custom_font, command=visualizeGraph, width=10)
deleteNodeButton = Button(frameConfig, text="Delete Node", font=custom_font, command=visualizeGraph, width=10)

# Text File
textFile = Text(frameOpenFile, height=1, width=75, font=custom_font, padx=6, pady=6, relief="sunken")
textFile.insert(0.0, "File location")
textFile.config(state=DISABLED)

openFileButton.pack(pady=7, side=LEFT)
visualizeButton.pack(pady=7)
addNodeButton.pack(pady=7)
deleteNodeButton.pack(pady=7)

textFile.pack(side=RIGHT)

frameOpenFile.pack(side=LEFT, anchor="n")
frameConfig.pack(side=RIGHT)
frameBottom.pack(side=BOTTOM, expand=TRUE, fill=X, padx=25)


root.mainloop()