from oauthlib.oauth1.rfc5849 import endpoints
class Graph(object):
    def __init__(self, nodes, links):
        self.__nodes__ = nodes
        self.__links__ = links
        
    def getListOfNodeIDs(self, getGateways = False):
        nodeIDs = []
        for k, v in self.__nodes__.items():
            if getGateways == True or v.isGateway == False:
                nodeIDs.append(k)
        return nodeIDs

    def getListOfNodeIDsOnline(self, getGateways = False):
        onlineNodeIDs = []
        nodeIDs = self.getListOfNodeIDs(getGateways)
        for nodeID in nodeIDs:
            if self.__nodes__[nodeID].isOnline == True:
                onlineNodeIDs.append(nodeID)
        return onlineNodeIDs
        
    def getNeighbourNodeIDsForNodeID(self, nodeID):
        neighNodeIDs = [nodeID]
        endpoints = []
        for link in self.__links__:
            if link.isVpn == False:
                endpoints = link.getEndpointNodeIDs(getGateways = False)
                if nodeID in endpoints:
                    neighNodeIDs = list(set(neighNodeIDs + endpoints))
        return neighNodeIDs
    
    def getLinksByNodeID(self, nodeID):
        links = []
        for link in self.__links__:
            endpoints = link.getEndpointNodeIDs()
            if nodeID in endpoints:
                if link not in links:
                    links.append(link)
        return links
    
    def getLinkCount(self):
        return len(self.__links__)
    
    def getNodesCount(self):
        return len(self.__nodes__)
