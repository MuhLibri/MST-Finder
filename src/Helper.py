from queue import Queue


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