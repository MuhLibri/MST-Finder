from Utils import *
from Prim import searchPrim
from Kruskal import searchKruskal

adjacencyMatrix = readFile()

nameList = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
# nameList = []
# for i in range(len(adjacencyMatrix)):
#     nameList.append(str(i+1))

n = len(adjacencyMatrix)
edgeList = (matrixToEdges(adjacencyMatrix, nameList))
print(edgeList)

drawGraph(adjacencyMatrix, nameList)

p = (searchPrim(edgeList, n))
k = (searchKruskal(edgeList, n))

print(p)
print(k)

showMST(adjacencyMatrix, nameList, p)
showMST(adjacencyMatrix, nameList, k)