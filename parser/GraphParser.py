from parser.JsonParser import JsonParser

class GraphParser(JsonParser):
    def __init__(self, filePath):
        super().__init__(filePath.rstrip('/')+'/graph.json')
        self.links = self.__prettyFormGraph__()
    
    def __prettyFormGraph__(self):
        links = []
        for link in self.__jsonData__['batadv']['links']:
            prettyLink = link
            prettyLink['target'] = self.__getEndpointData__(self.__jsonData__['batadv']['nodes'][link['target']])
            prettyLink['source'] = self.__getEndpointData__(self.__jsonData__['batadv']['nodes'][link['source']])
            links.append(prettyLink)
        return links
    
    def __getEndpointData__(self, endpoint):
        data = {}
        if endpoint:
            if 'id' in endpoint:
                data['interface_mac'] = endpoint['id']
            if 'node_id' in endpoint:
                data['node_id'] = endpoint['node_id']
            return data
        else:
            return None
    
    
    def getLinksForNodeID(self, nodeID):
        links = []
        for link in self.links:
            if link['target']['node_id'] == nodeID or link['source']['node_id'] == nodeID:
                links.append(link)
        return links
