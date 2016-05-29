class Link(object):
    def __init__(self, LinkJsonObject, srcNode, dstNode):
        self.__jsonObject__ = LinkJsonObject
        self.__srcNode__ = srcNode
        self.__dstNode__ = dstNode
        self.linkType = self.__getLinkType__()
        self.isVpn = self.__getLinkVpnState__()
        
        
    def __getLinkType__(self):
        if self.__srcNode__ != None:
            for k, v in self.__srcNode__.interfaces.items():
                if self.__jsonObject__['source']['interface_mac'] in v:
                    return k
        if self.__dstNode__ != None:
            for k, v in self.__dstNode__.interfaces.items():
                if self.__jsonObject__['target']['interface_mac'] in v:
                    return k
        return 'unknown'
        
    def __getLinkVpnState__(self):
        if self.__jsonObject__['vpn'] == True:
            return True
        for node in self.getEndpointNodes(getGateways = True):
            if node.isGateway == True:
                return True
        return False
        
    def getEndpointNodes(self, getGateways = False):
        nodes = []
        if self.__srcNode__ != None:
            if getGateways == True or self.__srcNode__.isGateway == False:
                nodes.append(self.__srcNode__)
        if self.__dstNode__ != None:
            if getGateways == True or self.__dstNode__.isGateway == False:
                nodes.append(self.__dstNode__)
        return nodes
    
    def getEndpointNodeIDs(self, getGateways = True):
        nodeIDs = []
        for node in self.getEndpointNodes(getGateways):
            nodeIDs.append(node.nodeID)
        return nodeIDs
    
    def isNodeIDinLink(self, nodeID):
        for endpoint in self.getEndpointNodes():
            if endpoint.nodeID == nodeID:
                return True
        return False
    
    def isNodeInLink(self, node):
        return self.isNodeIDinLink(node.nodeID)
