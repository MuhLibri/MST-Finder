def searchCluster(edgeMST, n):
    clusterEdges = sorted(edgeMST, key=lambda x: x[2], reverse=True)

    for i in range(n-1):
        clusterEdges = clusterEdges[1:]

    return clusterEdges