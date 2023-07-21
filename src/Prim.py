from Utils import isIncident


def searchPrim(graphTuple, n):
    graphTupleTemp = graphTuple.copy()
    graphTupleTemp.sort(key=lambda x: x[2]) 
    mst: list[tuple(str, str, int)] = [graphTupleTemp[0]]
    graphTupleTemp.remove(graphTupleTemp[0])
    
    for i in range (n-2):
        nextEdge = searchNextEdge(graphTupleTemp, mst)
        graphTupleTemp.remove(nextEdge)
        mst.append(nextEdge)

    return mst


def searchNextEdge(graphTuple, mst):
    for edge1 in graphTuple:
        for edge2 in mst:
            if (isIncident(edge1, edge2)) and (not isCircuit(edge1, mst)):
                return edge1


def isCircuit(edge, mst):
    node1Incident = False
    node2Incident = False
    i = 0

    while ((not node1Incident) or (not node2Incident)) and (i < len(mst)):
        if (edge[0] == mst[i][0] or edge[0] == mst[i][1]):
            node1Incident = True
        if (edge[1] == mst[i][0] or edge[1] == mst[i][1]):
            node2Incident = True
        i += 1
    
    return (node1Incident and node2Incident)