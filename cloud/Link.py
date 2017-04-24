class Link(object):
    def __init__(self, LinkJsonObject, nodes):
        self.__jsonObject = LinkJsonObject
        self.linkType, self.isVpn = self.__getLinkType__()
        self.__nodes = nodes

    def __getLinkType__(self):
        types = [x['type'] for x in self.__jsonObject]
        ltype = types[0]
        lvpn = False
        for x in types:
            if x != 'unknown' and x != 'other':
                if x == 'l2tp' or x == 'tunnel':
                    lvpn = True
                val = x
        return ltype, lvpn

    def getEndpointNodes(self, getGateways = False):
        return self.__nodes

    def getEndpointNodeIDs(self, getGateways = True):
        return [x.nodeID for x in self.__nodes]

    def isNodeIDinLink(self, nodeID):
        for x in self.__nodes:
            if nodeID == x.nodeID:
                return True
        return False

    def isNodeInLink(self, node):
        return self.isNodeIDinLink(node.nodeID)
