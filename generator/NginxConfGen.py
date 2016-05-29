from exceptions.HieraException import HieraException
from generator.Filter import Filter
class NginxConfGen(object):
    def __init__(self, domains, args):
        self.__domains__ = domains
        self.__args__ = args
        self.__filter__ = Filter(self.__args__)
        self.__generatedDomains__ = self.__genDomains__()
        
    def __genDomains__(self):
        domains = {}
        for k,v in self.__domains__.items():
            domains[k] = self.__genDomain__(v)
        return domains
        
    def __genDomain__(self, domain):
        nodes = {}
        for localGraph in self.__filter__.filterLocalGraphs(domain.localGraphs):
            try:
                for node in self.__filter__.filterNodes(localGraph.getNodesWithNoDependencies()):
                    nodes[node.nodeID] = {
                        'hostname' : node.hostname,
                        'ipv6_addresses' : node.publicIPv6Addresses                  
                        }
            except HieraException:
                print('Was not able to add local cloud, because no VPN link was found.')

        return nodes
    
    def writeNginxConfigFile(self):
        f = open(self.__args__.out_file,'w')
        f.write(self.__genNginxConfigFileContent__())
        f.close()
        
    def __genNginxConfigFileContent__(self):
        content = ''
        for k, v in self.__generatedDomains__.items():
            content += 'geo $' + k + ' {\n  default 0;'
            for ksub, vsub in v.items():
                for address in vsub['ipv6_addresses']:
                    content += '\n  ' + address + ' 1; #' + vsub['hostname'] 
            content += '\n}\n'
        return content
    