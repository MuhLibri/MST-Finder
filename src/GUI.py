from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import networkx as nx
from Prim import searchPrim
from Kruskal import searchKruskal
from Utils import matrixToEdges, calculateMSTWeight


class GUI(Tk):
    # Global Variables
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
        renameButton = Button(frameConfig, text="Rename Node", font=custom_font, command=self.renameWindow, width=15)
        addNodeButton = Button(frameConfig, text="Add Node/Edge", font=custom_font, command=self.addWindow, width=15)
        deleteNodeButton = Button(frameConfig, text="Delete Node/Edge", font=custom_font, command=self.deleteWindow, width=15)
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
        renameButton.pack(pady=7)
        addNodeButton.pack(pady=7)
        deleteNodeButton.pack(pady=7)
        frameConfig.pack(side=BOTTOM)
        frameRight.pack_propagate(False)
        frameRight.pack(side=RIGHT, fill=Y)

        # Frame Graph
        frameGraph = Frame(self, height=600, width=900, bg="#777778")
        # Canvas
        fig = plt.figure(figsize=(9, 5))
        self.canvas = FigureCanvasTkAgg(fig, master=frameGraph)
        toolbar = NavigationToolbar2Tk(self.canvas, frameGraph, pack_toolbar=False)
        toolbar.update()
        # Pack
        self.canvas.get_tk_widget().pack(expand=True, fill=BOTH)
        toolbar.pack(anchor="w", fill=X)
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
        frameOpenFile.pack(side=TOP, expand=TRUE, fill=X, anchor="n")
        frameBottom.pack(side=BOTTOM, expand=TRUE, fill=X, padx=mainPadding)


    # Functions
    def openFile(self):
        file = filedialog.askopenfile(title="Select a File", filetypes=[("txt", "*.txt")])
        adjacencyMatrix = [[int(num.strip()) for num in line.split(' ')] for line in file]
        file.close()

        self.fileText.config(state=NORMAL)
        self.fileText.delete(0.0, END)
        self.fileText.insert(END, file.name)
        self.fileText.config(state=DISABLED)

        self.nameList.clear()
        for i in range(len(adjacencyMatrix)):
            self.nameList.append(str(i+1))

        self.edgeList = matrixToEdges(adjacencyMatrix, self.nameList)

        self.visualizeGraph()


    def visualizeGraph(self):
        plt.clf()

        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.nameList)
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
            edgeMST = searchPrim(self.edgeList, len(self.nameList))
        else:
            edgeMST = searchKruskal(self.edgeList, len(self.nameList))

        nx.draw_networkx_edges(self.graph, self.pos, edgelist=edgeMST, edge_color="red", width=5)
        edge_labels = nx.get_edge_attributes(self.graph, "weight")
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels, font_size=10)

        self.canvas.draw()

        self.resultText.config(state=NORMAL)
        self.resultText.delete(0.0, END)
        self.resultText.insert(END, calculateMSTWeight(edgeMST))
        self.resultText.config(state=DISABLED)


    def renameWindow(self):
        renameWindow = Toplevel()
        renameWindow.title("Rename Node")
        renameWindow.resizable(False, False)
        # Frame
        frameMain = Frame(renameWindow, height=300, width=500, bg="#696969")
        frameRenameNode = Frame(frameMain, bg="#696969")
        # Label
        labelOldName = Label(frameRenameNode, text="Old Name", bg="#696969", fg="white", justify="left", font=3)
        labelNewName = Label(frameRenameNode, text="New Name", bg="#696969", fg="white", justify="left", font=3)
        # Entry
        self.oldName = Entry(frameRenameNode)
        self.newName = Entry(frameRenameNode)
        # Button
        addRenameButton = Button(frameRenameNode, text="Rename", command=self.renameNode, padx=5, pady=5)
        # Pack
        labelOldName.grid(row=0, column=0, padx=(0,15))
        self.oldName.grid(row=0, column=1)
        labelNewName.grid(row=1, column=0, padx=(0,15))
        self.newName.grid(row=1, column=1)
        addRenameButton.grid(row=2, column=0, columnspan=2, pady=15)
        frameRenameNode.pack(pady=(100,0))
        frameMain.pack_propagate(False)
        frameMain.pack()


    def renameNode(self):
        if ((len(self.oldName.get()) == 0) or (len(self.newName.get()) == 0)):
            messagebox.showerror(title="Error", message="All field must be filled!")
        elif (not self.oldName.get() in self.nameList):
            messagebox.showerror(title="Error", message="Node doesn't exist!")
        elif (self.newName.get() in self.nameList):
            messagebox.showerror(title="Error", message="New name already exist!")
        else:
            index = self.nameList.index(self.oldName.get())
            self.nameList[index] = self.newName.get()

            for i in range (len(self.edgeList)):
                edge = self.edgeList[i]
                if (edge[0] == self.oldName.get()):
                    newEdge = (self.newName.get(), edge[1], edge[2])
                    self.edgeList[i] = newEdge
                elif (edge[1] == self.oldName.get()):
                    newEdge = (edge[0], self.newName.get(), edge[2])
                    self.edgeList[i] = newEdge

            messagebox.showinfo(title="Success", message="Node " + '"' + self.oldName.get() + '"' + " has been renamed to " + '"' + self.newName.get() + '"')
            self.visualizeGraph()

        self.oldName.delete(0, END)
        self.newName.delete(0, END)


    def addWindow(self):
        addWindow = Toplevel()
        addWindow.title("Add Node/Edge")
        addWindow.resizable(False, False)
        # Frame
        frameMain = Frame(addWindow, height=300, width=500, bg="#696969")
        frameAddNode = Frame(frameMain, bg="#696969")
        frameAddEdge = Frame(frameMain, bg="#696969")
        # Label
        labelNewNode = Label(frameAddNode, text="Node", bg="#696969", fg="white", justify="left", font=3)
        labelNode1 = Label(frameAddEdge, text="Node 1", bg="#696969", fg="white", justify="left", font=3)
        labelNode2 = Label(frameAddEdge, text="Node 2", bg="#696969", fg="white", justify="left", font=3)
        labelWeight = Label(frameAddEdge, text="Weight", bg="#696969", fg="white", justify="left", font=3)
        # Entry
        self.newNode = Entry(frameAddNode)
        self.newNode1 = Entry(frameAddEdge)
        self.newNode2 = Entry(frameAddEdge)
        self.newWeight = Entry(frameAddEdge)
        # Button
        addNodeButton = Button(frameAddNode, text="Add Node", command=self.addNode, padx=5, pady=5)
        addEdgeButton = Button(frameAddEdge, text="Add Edge", command=self.addEdge, padx=5, pady=5)
        # Pack
        labelNewNode.grid(row=0, column=0, padx=(0,30))
        self.newNode.grid(row=0, column=1)
        labelNode1.grid(row=0, column=0, padx=(0,15))
        self.newNode1.grid(row=0, column=1)
        labelNode2.grid(row=1, column=0, padx=(0,15))
        self.newNode2.grid(row=1, column=1)
        labelWeight.grid(row=2, column=0, padx=(0,15))
        self.newWeight.grid(row=2, column=1)
        addNodeButton.grid(row=1, column=0, columnspan=2, pady=15)
        addEdgeButton.grid(row=3, column=0, columnspan=2, pady=15)
        frameAddNode.pack(side=TOP, pady=(20,20))
        frameAddEdge.pack(side=BOTTOM, pady=(0, 20))
        frameMain.pack_propagate(False)
        frameMain.pack()


    def addNode(self):
        if (len(self.newNode.get()) == 0):
            messagebox.showerror(title="Error", message="Field must be filled!")
        elif (self.newNode.get() in self.nameList):
            messagebox.showerror(title="Error", message="Node already exist!")
        else:
            self.nameList.append(self.newNode.get())
            messagebox.showinfo(title="Success", message="Node has been added")
            self.visualizeGraph()

        self.newNode.delete(0, END)


    def addEdge(self):
        if (len(self.newNode1.get()) == 0 or len(self.newNode2.get()) == 0 or len(self.newWeight.get()) == 0):
            messagebox.showerror(title="Error", message="All field must be filled!")
        elif (not (self.newWeight.get().isdigit())):
            messagebox.showerror(title="Error", message="Weight field must be an integer!")
        else:
            newEdge1 = (str(self.newNode1.get()), str(self.newNode2.get()), int(self.newWeight.get()))
            newEdge2 = (str(self.newNode2.get()), str(self.newNode1.get()), int(self.newWeight.get()))

            if (newEdge1 in self.edgeList or newEdge2 in self.edgeList):
                messagebox.showerror(title="Error", message="Edge already exist!")
            else:
                self.edgeList.append(newEdge1)
                messagebox.showinfo(title="Success", message="Edge has been added")
                self.visualizeGraph()

        self.newNode1.delete(0, END)
        self.newNode2.delete(0, END)
        self.newWeight.delete(0, END)


    def deleteWindow(self):
        deleteWindow = Toplevel()
        deleteWindow.title("Delete Node/Edge")
        deleteWindow.resizable(False, False)
        # Frame
        frameMain = Frame(deleteWindow, height=300, width=500, bg="#696969")
        frameDeleteNode = Frame(frameMain, bg="#696969")
        frameDeleteEdge = Frame(frameMain, bg="#696969")
        # Label
        labelDeleteNode = Label(frameDeleteNode, text="Node", bg="#696969", fg="white", justify="left", font=3)
        labelDelNode1 = Label(frameDeleteEdge, text="Node 1", bg="#696969", fg="white", justify="left", font=3)
        labelDelNode2 = Label(frameDeleteEdge, text="Node 2", bg="#696969", fg="white", justify="left", font=3)
        labelDelWeight = Label(frameDeleteEdge, text="Weight", bg="#696969", fg="white", justify="left", font=3)
        # Entry
        self.delNode = Entry(frameDeleteNode)
        self.delNode1 = Entry(frameDeleteEdge)
        self.delNode2 = Entry(frameDeleteEdge)
        self.delWeight = Entry(frameDeleteEdge)
        delNodeButton = Button(frameDeleteNode, text="Delete Node", command=self.deleteNode, padx=5, pady=5)
        delEdgeButton = Button(frameDeleteEdge, text="Delete Edge", command=self.deleteEdge, padx=5, pady=5)
        # Pack
        labelDeleteNode.grid(row=0, column=0, padx=(0,30))
        self.delNode.grid(row=0, column=1)
        labelDelNode1.grid(row=0, column=0, padx=(0,15))
        self.delNode1.grid(row=0, column=1)
        labelDelNode2.grid(row=1, column=0, padx=(0,15))
        self.delNode2.grid(row=1, column=1)
        labelDelWeight.grid(row=2, column=0, padx=(0,15))
        self.delWeight.grid(row=2, column=1)
        delNodeButton.grid(row=1, column=0, columnspan=2, pady=15)
        delEdgeButton.grid(row=3, column=0, columnspan=2, pady=15)
        frameDeleteNode.pack(side=TOP, pady=(20,20))
        frameDeleteEdge.pack(side=BOTTOM, pady=(0, 20))
        frameMain.pack_propagate(False)
        frameMain.pack()


    def deleteNode(self):
        if (len(self.delNode.get()) == 0):
            messagebox.showerror(title="Error", message="Field must be filled!")
        elif (not self.delNode.get() in self.nameList):
            messagebox.showerror(title="Error", message="Node doesn't exist!")
        else:
            self.nameList.remove(self.delNode.get())
            removeList = []

            for edge in self.edgeList:
                if ((edge[0] == self.delNode.get()) or (edge[1] == self.delNode.get())):
                    removeList.append(edge)

            for edge in removeList:
                self.edgeList.remove(edge)

            messagebox.showinfo(title="Success", message="Node has been deleted")
            self.visualizeGraph()

        self.delNode.delete(0, END)


    def deleteEdge(self):
        if (len(self.delNode1.get()) == 0 or len(self.delNode2.get()) == 0 or len(self.delWeight.get()) == 0):
            messagebox.showerror(title="Error", message="All field must be filled!")
        elif (not (self.delWeight.get().isdigit())):
            messagebox.showerror(title="Error", message="Weight field must be an integer!")
        else:
            delEdge1 = (str(self.delNode1.get()), str(self.delNode2.get()), int(self.delWeight.get()))
            delEdge2 = (str(self.delNode2.get()), str(self.delNode1.get()), int(self.delWeight.get()))
            if (delEdge1 in self.edgeList):
                self.edgeList.remove(delEdge1)
                messagebox.showinfo(title="Success", message="Edge has been deleted")
                self.visualizeGraph()
            elif (delEdge2 in self.edgeList):
                self.edgeList.remove(delEdge2)
                messagebox.showinfo(title="Success", message="Edge has been deleted")
                self.visualizeGraph()
            else:
                messagebox.showerror(title="Error", message="Edge doesn't exist!")

        self.delNode1.delete(0, END)
        self.delNode2.delete(0, END)
        self.delWeight.delete(0, END)