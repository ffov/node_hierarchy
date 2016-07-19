class Link(object):
    def __init__(self, LinkJsonObject, srcNode, dstNode):
        self.__jsonObject__ = LinkJsonObject
        self.__srcNode__ = srcNode
        self.__dstNode__ = dstNode
        self.linkType = self.__getLinkType__()
        self.isVpn = self.__getLinkVpnState__()
        
        
    def __getLinkType__(self):
        type_src = None
        type_dst = None
        if self.__srcNode__ != None:
            for k, v in self.__srcNode__.interfaces.items():
                if self.__jsonObject__['source']['interface_mac'] in v:
                    type_src = k
        if self.__dstNode__ != None:
            for k, v in self.__dstNode__.interfaces.items():
                if self.__jsonObject__['target']['interface_mac'] in v:
                    type_dst = k
                    
        if type_src == type_dst:
            if type_src == None:
                return 'unknown'
            return type_src
        else:
            if type_src == None:
                return type_dst
            elif type_dst == None:
                return type_src
            else:
                #print(self.__srcNode__.hostname, type_src, '<-->', self.__dstNode__.hostname, type_dst)
                if type_src == 'wireless':
                    return type_dst
                else:
                    return type_src
        
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
