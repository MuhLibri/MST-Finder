from Utils import *
from Prim import *
from Kruskal import *

a = readFile()

b = []
for i in range(len(a)):
    b.append(str(i+1))

n = len(a)
c = (matrixToEdges(a, b))
print(c)

drawGraph(a, b)

p = (searchPrim(c, n))
k = (searchKruskal(c, n))
print(p)
print(k)
showMST(a, b, p)
showMST(a, b, k)