from cloud.LocalGraph import LocalGraph
class Domaene(object):
    def __init__(self, name, shapes, globalGraph):
        self.name = name
        self.__shapes__ = shapes
        self.__globalGraph__ = globalGraph
        self.localGraphs = self.__getLocalGraphsInDomaene__()
        
    def __getLocalGraphsInDomaene__(self):
        graphs = []
        for localGraph in self.__globalGraph__.localGraphs:
            if self.isLocalGraphInDomaene(localGraph) == True:
                graphs.append(localGraph)
        return graphs
        
    def isLocalGraphInDomaene(self, localGraph):
        return self.isPointInDomaene(localGraph.getGeoCenterOfNodeCloud())
    
    def isPointInDomaene(self, point):
        for shape in self.__shapes__.shapes:
            if point.within(shape):
                return True
        return False
