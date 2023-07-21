from Helper import isIncident, isCircuit


def searchPrim(edgeList: list[tuple((str, str, int))], n: int) -> list[tuple((str, str, int))]:
    edgeListTemp = edgeList.copy()
    edgeListTemp.sort(key=lambda x: x[2]) 
    mst: list[tuple((str, str, int))] = [edgeListTemp[0]]
    edgeListTemp.remove(edgeListTemp[0])
    
    for i in range (n-2):
        nextEdge = searchNextEdge(edgeListTemp, mst)
        edgeListTemp.remove(nextEdge)
        mst.append(nextEdge)

    return mst


def searchNextEdge(edgeList: list[tuple((str, str, int))], mst: list[tuple((str, str, int))]) -> tuple((str, str, int)):
    for edge1 in edgeList:
        for edge2 in mst:
            if (isIncident(edge1, edge2)) and (not isCircuit(edge1, mst)):
                return edge1