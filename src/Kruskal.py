from queue import Queue
from Utils import *


def searchKruskal(graphTuple, n):
    graphTuple.sort(key=lambda x: x[2])
    mst: list[tuple(str, str, int)] = []
    i = 0

    while (len(mst) < n-1):
        if (not isCircuit(graphTuple[i], mst)):
            mst.append(graphTuple[i])
        i += 1

    return mst


def isCircuit(edge, mst):
    circuit = False
    nodeQueue = Queue()
    nodeQueue.put(edge[0])
    listVisitedNode = []

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