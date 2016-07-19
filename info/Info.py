from info.OfflineInfo import OfflineInfo
class Info(object):
    def __init__(self, infoTypes, infoOutFolder, infoOutType, infoFilters, nodes, globalGraph, domains):
        self.__infoTypes__ = infoTypes
        self.__infoOutFolder__ = infoOutFolder
        self.__infoOutType__ = infoOutType
        self.__infoFilters__ = infoFilters
        self.__nodes__ = nodes
        self.__globalGraph__ = globalGraph
        self.__domains__ = domains
        if self.__infoTypes__ != None:
            if 'get_offline_nodes' in self.__infoTypes__:
                self.__offlineNodes__ = OfflineInfo(self.__infoFilters__, self.__nodes__, self.__domains__)
                print(self.__infoOutType__)
                if 'csv' in self.__infoOutType__:
                    self.__offlineNodes__.writeCSVtoFile(self.__infoOutFolder__+'/offline_nodes.csv')
                if 'json' in self.__infoOutType__:
                    self.__offlineNodes__.writeJsonToFile(self.__infoOutFolder__+'/offline_nodes.json')