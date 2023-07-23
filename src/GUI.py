from tkinter import *
from tkinter import filedialog
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from Prim import searchPrim
from Kruskal import searchKruskal
from Utils import matrixToEdges, calculateMSTWeight


class GUI(Tk):
    # Global Variables
    adjacencyMatrix = []
    nameList = []
    edgeList = []

    def __init__(self):
        super().__init__()
        self.title("MST Finder")
        self.config(bg="darkgray")

        # GUI Variables
        custom_font = font.Font(size=11)
        mainPadding = 20
        self.graph = nx.Graph()
        self.pos = nx.spring_layout(self.graph, seed=5)

        # Frame Right
        frameRight = Frame(self, height=700, width=250, bg="#696969", padx=mainPadding, pady=mainPadding)
        frameAlgorithm = Frame(frameRight, bg="darkgray")
        frameSolve = Frame(frameAlgorithm, bg="#696969")
        frameResult = Frame(frameRight, bg="darkgray")
        frameConfig = Frame(frameRight, bg="#696969")
        # Algorithm Section
        algorithmLabel = Label(frameAlgorithm, text="Algorithm:", font=(20), bg="darkgray")
        algorithmChoice = StringVar()
        algorithmChoice.set("prim")
        primButton = Radiobutton(frameAlgorithm, text="Prim", font=(20), variable=algorithmChoice, value="prim", bg="darkgray", activebackground="darkgray", activeforeground="white")
        kruskalButton = Radiobutton(frameAlgorithm, text="Kruskal", font=(20), variable=algorithmChoice, value="kruskal", bg="darkgray", activebackground="darkgray", activeforeground="white")
        solveButton = Button(frameSolve, text="Solve", font=custom_font, command=lambda: self.solve(algorithmChoice.get()), width=7)
        resetButton = Button(frameSolve, text="Reset", font=custom_font, command=self.visualizeGraph, width=7)
        # Result Section
        resultLabel = Label(frameResult, text="MST Weight ", font=custom_font, padx=6, pady=6, bg="darkgray")
        self.resultText = Text(frameResult, height=1, width=10, font=custom_font, padx=6, pady=6, relief="sunken")
        self.resultText.config(state=DISABLED)
        # Config Section
        addNodeButton = Button(frameConfig, text="Add Node", font=custom_font, command=self.addNode, width=10)
        deleteNodeButton = Button(frameConfig, text="Delete Node", font=custom_font, command=self.deleteNode, width=10)
        # Pack
        algorithmLabel.pack(padx=20, pady=(20, 0), anchor="w")
        primButton.pack(padx=20, anchor="w")
        kruskalButton.pack(padx=20, pady=(0, 20), anchor="w")
        resetButton.pack(side=LEFT, padx=(0,15), pady=(15, 0))
        solveButton.pack(side=RIGHT, pady=(15, 0))
        frameSolve.pack(fill=X)
        frameAlgorithm.pack(side=TOP, pady=100)
        resultLabel.pack(side=LEFT)
        self.resultText.pack(side=RIGHT)
        frameResult.pack(side=TOP)
        addNodeButton.pack(pady=7)
        deleteNodeButton.pack(pady=7)
        frameConfig.pack(side=BOTTOM)
        frameRight.pack_propagate(False)
        frameRight.pack(side=RIGHT, fill=Y)

        # Frame Graph
        frameGraph = Frame(self, height=600, width=900, bg="#777778")
        # Canvas
        fig = plt.figure(figsize=(9, 6))
        self.canvas = FigureCanvasTkAgg(fig, master=frameGraph)
        # Pack
        self.canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        frameGraph.pack(side=TOP, expand=TRUE, fill=BOTH, padx=mainPadding, pady=(mainPadding, 0))

        # Frame Bottom
        frameBottom = Frame(self, height=100, width=900, bg="darkgray")
        frameOpenFile = Frame(frameBottom, bg="darkgray")
        # Buttons
        openFileButton = Button(frameOpenFile, text="Open File", font=custom_font, command=self.openFile, width=10)
        # Text File
        self.fileText = Text(frameOpenFile, height=1, width=75, font=custom_font, padx=6, pady=6, relief="sunken")
        self.fileText.config(state=DISABLED)
        # Pack
        openFileButton.pack(side=LEFT)
        self.fileText.pack(side=RIGHT, expand=TRUE, fill=X)
        frameOpenFile.pack(side=LEFT, anchor="n", expand=TRUE, fill=X)
        frameBottom.pack(side=BOTTOM, expand=TRUE, fill=X, padx=mainPadding)


    # Functions
    def openFile(self):
        file = filedialog.askopenfile(title="Select a File", filetypes=[("txt", "*.txt")])
        self.adjacencyMatrix = [[int(num.strip()) for num in line.split(' ')] for line in file]
        file.close()

        self.fileText.config(state=NORMAL)
        self.fileText.delete(0.0, END)
        self.fileText.insert(END, file.name)
        self.fileText.config(state=DISABLED)

        self.nameList.clear()
        for i in range(len(self.adjacencyMatrix)):
            self.nameList.append(str(i+1))

        self.edgeList = matrixToEdges(self.adjacencyMatrix, self.nameList)

        self.visualizeGraph()


    def visualizeGraph(self):
        plt.clf()

        self.graph = nx.Graph()

        for name in self.nameList:
            self.graph.add_node(name)

        self.graph.add_weighted_edges_from(self.edgeList)

        self.pos = nx.spring_layout(self.graph, seed=5)
        nx.draw_networkx_nodes(self.graph, self.pos, node_size=[len(v) * 1000 for v in self.graph.nodes()])
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=self.graph.edges, width=5)
        nx.draw_networkx_labels(self.graph, self.pos, font_size=20, font_family="sans-serif")
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels, font_size=10)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()

        self.canvas.draw()

        self.resultText.config(state=NORMAL)
        self.resultText.delete(0.0, END)
        self.resultText.config(state=DISABLED)


    def solve(self, algorithm):
        if (algorithm == "prim"):
            edgeMST = searchPrim(self.edgeList, len(self.adjacencyMatrix))
        else:
            edgeMST = searchKruskal(self.edgeList, len(self.adjacencyMatrix))

        nx.draw_networkx_edges(self.graph, self.pos, edgelist=edgeMST, edge_color="red", width=5)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels, font_size=10)

        self.canvas.draw()

        self.resultText.config(state=NORMAL)
        self.resultText.delete(0.0, END)
        self.resultText.insert(END, calculateMSTWeight(edgeMST))
        self.resultText.config(state=DISABLED)


    def addNode(self):
        print("Add Node")


    def deleteNode(self):
        print("Delete Node")