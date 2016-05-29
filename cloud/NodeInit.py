class NodeInit(object):
    def __init__(self, NodeJsonObject):
        self.__jsonObject__ = NodeJsonObject
        self.nodeID = self.__jsonObject__['nodeinfo']['node_id']
        self.interfaces = self.__getInterfaces__()
        self.hostname = self.__jsonObject__['nodeinfo']['hostname']
        self.isGateway = self.__jsonObject__['flags']['gateway']
        self.geo = self.__getGeo__()
        self.isAutoupdaterEnabled = self.__getAutoupdaterStatus__()
        self.autoupdaterBranch = self.__getBranch__()
        self.isOnline = self.__jsonObject__['flags']['online']
        self.publicIPv6Addresses = self.__getPublicAddresses__()
        self.domID = self.__getSiteCode__()
        
    def __getInterfaces__(self):
        try:
            return self.__jsonObject__['nodeinfo']['network']['mesh']['bat0']['interfaces']
        except:
            return {}

    def __getAutoupdaterStatus__(self):
        if 'autoupdater' in self.__jsonObject__['nodeinfo']['software']:
            return self.__jsonObject__['nodeinfo']['software']['autoupdater']['enabled']
        else:
            return False

    def __getBranch__(self):
        if 'autoupdater' in self.__jsonObject__['nodeinfo']['software']:
            return self.__jsonObject__['nodeinfo']['software']['autoupdater']['branch']
        else:
            return None

    def __getGeo__(self):
        geo = {}
        if 'location' in self.__jsonObject__['nodeinfo'] and 'latitude' in self.__jsonObject__['nodeinfo']['location'] and 'longitude' in self.__jsonObject__['nodeinfo']['location']:
            geo['lat'] = self.__jsonObject__['nodeinfo']['location']['latitude']
            geo['lon'] = self.__jsonObject__['nodeinfo']['location']['longitude']
            return geo
        return None

    def __getPublicAddresses__(self):
        addresses = []
        if 'addresses' in self.__jsonObject__['nodeinfo']['network']:
            for address in self.__jsonObject__['nodeinfo']['network']['addresses']:
                if not address.startswith('fe80'):
                    addresses.append(address)
        return addresses
    
    def __getSiteCode__(self):
        try:
            return self.__jsonObject__['nodeinfo']['system']['site_code']
        except:
            return None
