from parser.JsonParser import JsonParser

class NodesParser(JsonParser):
    def __init__(self, filePath):
        super().__init__(filePath.rstrip('/')+'/nodes.json')
        self.nodes = self.__jsonData__['nodes']
        #print(self.nodes)
        pass
    
    def getNodeByID(self, nodeID):
        if nodeID in self.nodes:
            return self.nodes[nodeID]
        else:
            return None
        
    def getListOfNodeIDs(self):
        IDlist = []
        for k, v in self.nodes.items():
            IDlist.append(k)
        return IDlist
