import numpy as np
import itertools

class Node():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y


class Graph():
    def __init__(self):
        self.nodeId_loc = {} # {nodeId:Node,...}
        self.adjList = {} #{src:{dist1:weight1, dist2:weight2},...}

    @property
    def nodeIds(self):
        return self.nodeId_loc.keys()

    @property
    def minDegree(self):
        min_degree = np.infty
        for node in self.nodeIds:
            if self.degree(node) < min_degree:
                min_degree = self.degree(node)
        return min_degree

    @property
    def minDegreeNodes(self):
        minDegreeNodes = []
        for nodeId in self.nodeIds:
            if self.degree(nodeId) == self.minDegree:
                minDegreeNodes.append(nodeId)
        return minDegreeNodes

    def adjListOfSrcNode(self, src_nodeId):
        return self.adjList[src_nodeId].keys()

    def degree(self, node_id):
        if node_id in self.adjList:
            return len(self.adjList[node_id])


    def deleteNode(self, src):
        adjList = self.adjListOfSrcNode(src)
        #delete adjacent edges
        for dest in adjList:
            self.adjList[dest].pop(src)

        #delete node itself
        self.adjList.pop(src)
        self.nodeId_loc.pop(src)

    def sortAdjList(self, src):
        # sort the adjcent list in ascending order
        sorted_tuple = sorted(self.adjList[src].items(), key=lambda d: d[1])
        return [node_id for node_id, value in sorted_tuple]

    def getEdgeLength(self, node1_id, node2_id):
        if node1_id in self.adjList:
            if node2_id in self.adjList[node1_id]:
                return self.adjList[node1_id][node2_id]
        if node2_id in self.adjList:
            if node1_id in self.adjList[node2_id]:
                return self.adjList[node2_id][node1_id]
        return None

    def load(self, edgeFileName, nodeFileName):
        with open(nodeFileName) as nodeFile:
            nodeLines = nodeFile.readlines()
        for nodeLine in nodeLines:
            id, x, y = nodeLine.strip().split(' ')
            self.addNode(id, x, y)

        with open(edgeFileName) as edgeFile:
            edgeLines = edgeFile.readlines()
        for edgeLine in edgeLines:
            src_nodeId, dest_nodeId = edgeLine.strip().split(' ')
            src_node = self.nodeId_loc[src_nodeId]
            dest_node = self.nodeId_loc[dest_nodeId]
            self.addEdge(src_nodeId, dest_nodeId, getDistance(src_node, dest_node))

    def addNode(self, id, x, y):
        self.nodeId_loc[id] = Node(id, float(x), float(y))
        self.adjList[id] = {}

    def getNode(self, id):
        return self.nodeId_loc[id]

    def addEdge(self, src_nodeId, dest_nodeId, distance):
        self.adjList[src_nodeId][dest_nodeId] = distance
        self.adjList[dest_nodeId][src_nodeId] = distance


    def __str__(self):
        ret_str = 'node_loc\n:{}\n\n adjList\n:{}'.format(self.nodeId_loc, self.adjList)
        return ret_str

class Circle():
    """
    Minimum circle that covers a set of nodes
    """
    def __init__(self, G, nodeIds):
        self.G = G
        self.nodeIds = nodeIds

        edgeList = list(itertools.combinations(self.nodeIds, 2))
        maxDistance = 0
        maxEdge = None
        for edge in edgeList:
            node1_id = edge[0]
            node2_id = edge[1]
            node1 = self.G.getNode(node1_id)
            node2 = self.G.getNode(node2_id)
            distance = getDistance(node1, node2)
            if distance > maxDistance:
                maxDistance = distance
                maxEdge = (node1, node2)

        self.radius = maxDistance / 2

        self.centerX = (maxEdge[0].x + maxEdge[1].x) / 2
        self.centerY = (maxEdge[0].y + maxEdge[1].y) / 2
    def __str__(self):
        retStr = "circle:\n"+ \
        "center: ("+ str(self.centerX)+", "+str(self.centerY)+")\n"+ \
        "radius: " + str(self.radius) +"\n"+\
        "covered nodes: " + str(self.nodeIds)
        return retStr


def kCore(G, k):
    """
    M. Sozio and A. Gionis. The community-search problem and how to
    plan a successful cocktail party
    :param G:
    :param k:
    :return:
    """
    G_copy = G
    while G_copy.minDegree < k:
        minDegreeNode = G_copy.minDegreeNodes.pop(0)
        G_copy.deleteNode(minDegreeNode)
    return G_copy

def getSubGraph(G, nodeIds):
    """
    Given original graph, and a subset of nodes,
    construct a subgraph from the subset of nodes
    :param G:
    :param nodeIds:
    :return:
    """
    subGraph = Graph()

    for nodeId in nodeIds:
        node = G.getNode(nodeId)
        subGraph.addNode(nodeId, node.x, node.y)

    for nodeId in nodeIds:
        adjNodeIds = G.adjListOfSrcNode(nodeId)
        for adjNodeId in adjNodeIds:
            if adjNodeId in nodeIds:
                subGraph.addEdge(nodeId, adjNodeId, G.getEdgeLength(nodeId, adjNodeId))
    return subGraph

def getDistance(node1, node2):
    x_dist = node1.x - node2.x
    y_dist = node1.y - node2.y
    distance = np.sqrt(x_dist * x_dist + y_dist * y_dist)
    return distance

if __name__ == '__main__':
    graph = Graph()
    graph.load('./data/test/edges', './data/test/checkin')
    subGraph = getSubGraph(graph, ['E', 'H', 'G', 'I'])

    kCoreGraph = kCore(graph, 2)
    MCC = Circle(kCoreGraph, ['A', 'B', 'C'])
    print(MCC.radius)




