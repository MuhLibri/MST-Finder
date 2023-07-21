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

print(searchKruskal(c, n))
print(searchPrim(c, n))