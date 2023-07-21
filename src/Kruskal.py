from Helper import isCircuit


def searchKruskal(edgeList: list[tuple((str, str, int))], n: int) -> list[tuple((str, str, int))]:
    mst: list[tuple((str, str, int))] = []
    i: int = 0
    edgeList.sort(key=lambda x: x[2])

    while (len(mst) < n-1):
        if (not isCircuit(edgeList[i], mst)):
            mst.append(edgeList[i])
        i += 1

    return mst