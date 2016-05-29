import json, urllib.request
from exceptions.HieraException import HieraException

class JsonParser(object):
    def __init__(self, fileName):
        self.printStatus = True
        self.__jsonData__ = self.__getFile__(fileName)
    
    def __getFile__(self, fileName):
        if fileName.startswith('https://') or fileName.startswith('http://'):
            if self.printStatus:
                print('Download', fileName.rsplit('/', 1)[1] , 'from URL:', fileName)
            resource = urllib.request.urlopen(fileName)
        else:
            if self.printStatus:
                print('Open', fileName.rsplit('/', 1)[1] , 'from file:', fileName)
            resource = open(fileName)
        try:
            data = json.loads(resource.read().decode('utf-8'))
        except:
            raise HieraException('Error while parsing a json file (perhapes misformed file): ' + fileName)
        finally:
            resource.close()
    
        return data
