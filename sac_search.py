import graph
from graph import Graph, Circle
import numpy as np

"""
Effective Community Search over Large Spatial Graphs
"""

def exact(G, q, k):
    kCore_G = graph.kCore(G, k)
    if q not in kCore_G.adjList:
        raise RuntimeError('{} not in the kCore'.format(q))
    q_adjList =[q]
    q_adjList.extend(kCore_G.sortAdjList(q))

    if len(q_adjList) < 3:
        return q_adjList

    radius = np.infty

    mcc = None
    for i in range(2, len(q_adjList)):
        node_i = q_adjList[i]
        for j in range(0, i - 1):

            for h in range(j + 1, i):
                node_j = q_adjList[j]
                node_h = q_adjList[h]
                nodes = [node_i, node_j, node_h]
                circle = Circle(kCore_G, nodes)
                circle_radius = circle.radius
                if circle_radius < radius and q in nodes:
                    mcc = circle
                    radius = mcc.radius
    return mcc

def appInc(G, q, k):
    kCore_G = graph.kCore(G, k)
    if q not in kCore_G.adjList:
        raise RuntimeError('{} not in the kCore'.format(q))
    q_adjList = kCore_G.sortAdjList(q)

    subGraphNodes = [q]
    for adjNode in q_adjList:
        subGraphNodes.extend(adjNode)
        subGraph = graph.getSubGraph(G, subGraphNodes)
        if subGraph.minDegree >= k:
            return Circle(G, subGraphNodes)

def appFast(G, q, k, param_F):
    """
    To do
    Binary search
    :param G:
    :param q:
    :param k:
    :return:
    """
    pass

def appAcc(G, q, k, param_Acc):
    """
    To do
    quadtree search
    prune
    :param G:
    :param q:
    :param k:
    :param param_Acc:
    :return:
    """
    pass

def exactPlus(G, q, k, param_Acc):
    """
    To do
    prune fixed verticies
    enumeration of three vertex combinations
    :param G:
    :param q:
    :param k:
    :param param_Acc:
    :return:
    """
    pass



if __name__ == '__main__':
    G = Graph()
    G.load(edgeFileName='./data/test/edges', nodeFileName='./data/test/checkin')
    q = 'Q'
    k = 2
    # mcc1 = exact(G, q, k)
    # print(mcc1)
    mcc2 = appInc(G, q, k)
    print(mcc2)
