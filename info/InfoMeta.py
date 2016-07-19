import json
class InfoMeta(object):
    def __init__(self):
        self.resultNodes = None
        self.resultGraph = None
        
        
    def __generateNodesJson__(self):
        if self.resultNodes == None:
            return []
        result = []
        for node in self.resultNodes:
            result.append(node.__jsonObject__)
        return result
    
    def __generateNodesCSV__(self):
        if self.resultNodes == None:
            return ''
        
        result = '"hostname","site","nodeid","ipv6addresses","status","lastseen","firstseen","autoupdater","branch","firmware","hardware"\n'
        for node in self.resultNodes:
            nodeData = node.__jsonObject__
            nodeinfo = nodeData['nodeinfo']
            result += '"'+nodeinfo['hostname']+'",'
            
            try:
                result +='"'+nodeinfo['system']['site_code']+'",'
            except:
                result += '"none",'
            result += '"'+nodeinfo['node_id']+'","'
            
            #add array of public IPv6 Addresses
            addresses = node.__getPublicAddresses__()
            for i, address in enumerate(addresses):
                if i == len(addresses)-1:
                    result += address
                else:
                    result += address + ','
            result += '",'
            
            if nodeData['flags']['online'] == True:
                result += '"online",'
            else:
                result += '"offline",'
            
            result += '"'+nodeData['lastseen']+'","'+nodeData['firstseen']+'",'
            try:
                if nodeinfo['software']['autoupdater']['enabled'] == True:
                    result += '"enabled",'
                else:
                    result += '"disabled",'
            except:
                    result += '"none",'
                    
            try:
                result += '"'+nodeinfo['software']['autoupdater']['branch']+'",'
            except:
                result += '"none",'
            result += '"'+nodeinfo['software']['firmware']['release']+'",'
            
            try:
                result += '"'+nodeinfo['hardware']['model']+'"'
            except:
                result += '"none"'
                
            result += '\n'
        return result
    
    def writeCSVtoFile(self, filename):
        with open(filename, 'w') as out:
            out.write(self.__generateNodesCSV__())
            
    def writeJsonToFile(self, filename):
        with open(filename, 'w') as out:
            out.write(json.dumps(self.__generateNodesJson__(), sort_keys=True, indent=4, ensure_ascii=False))