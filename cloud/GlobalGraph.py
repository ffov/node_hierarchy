from cloud.LocalGraph import LocalGraph
from cloud.Graph import Graph
from exceptions.HieraException import HieraException
class GlobalGraph(Graph):
    def __init__(self, nodes, links, debugPrint = False):
        super().__init__(nodes, links)
        self.__enableDebugPrinting__ = debugPrint
        self.localGraphs = self.__buildLocalGraphs__()
        
        if self.__enableDebugPrinting__:
            self.__debugPrint__()

    def __buildLocalGraphs__(self):
        nodeIDs = self.getListOfNodeIDsOnline()
        localGraphs = []
        while len(nodeIDs) > 0:
            connectedNodes = self.__getConnectedNodes__(nodeIDs[0])
            try:
                localGraphs.append(self.__createLocalCloudByNodesList__(connectedNodes))
                print('Create LocalGraph object #',len(localGraphs), '\r',end = '')
            except HieraException:
                print('Was not able to add local cloud, because no VPN link was found.')
            nodeIDs = [x for x in nodeIDs if x not in connectedNodes]
        print('')
        return localGraphs

    def __getConnectedNodes__(self, nodeID, trace = []):
        neighNodeIDs = self.getNeighbourNodeIDsForNodeID(nodeID)
        trace_new = list(set(trace + neighNodeIDs))
        for neighNodeID in neighNodeIDs:
            if neighNodeID not in trace:
                trace_new = list(set(trace_new + self.__getConnectedNodes__(neighNodeID, trace_new)))
        return trace_new

    def __createLocalCloudByNodesList__(self, nodesIDList):
        nodes = {}
        links = []
        for nodeID in nodesIDList:
            if nodeID:
                nodes[nodeID] = self.__nodes__[nodeID]
                links = list(set(links + self.getLinksByNodeID(nodeID)))
        return LocalGraph(nodes, links, self.__enableDebugPrinting__)

    def __debugPrint__(self):
        for localGraph in self.localGraphs:
            for node in localGraph.getNodesWithNoDependencies():
                print(node.hostname, node.publicIPv6Addresses)
