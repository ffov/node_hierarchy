class Filter(object):
    def __init__(self, args):
        self.__args__ = args
        self.__filters__ = self.__getFilters()
        
    def filterLocalGraphs(self, localGraphs):
        filteredGraphs = []
        for localGraph in localGraphs:
            if localGraph.isAutoupdaterEnabledOnAllNodes() == False:
                continue
            if  self.__allowCloudsWithLanLinks__() == False and len(localGraph.getLanLinksInCloud()) > 0:
                continue
            filteredGraphs.append(localGraph)
        return filteredGraphs
    
    def __allowCloudsWithLanLinks__(self):
        if 'exclude_clouds_with_lan_links' in self.__filters__ or 'no_lan' in self.__filters__:
            return False
        return True
    
    def __getFilters(self):
        return [] if self.__args__.filters == None else self.__args__.filters
    
    def filterNodes(self, nodes):
        filteredNodes = []
        for node in nodes:
            filteredNodes.append(node)
        return filteredNodes
