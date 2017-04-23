import json, urllib.request
from exceptions.HieraException import HieraException

class JsonParser(object):
    def __init__(self, fileName):
        self.printStatus = True
        self.__jsonData__ = self.__getFile__(fileName)
    
    def __getFile__(self, fileName):
        if fileName.startswith('https://') or fileName.startswith('http://'):
            if self.printStatus:
                print('Download', fileName, 'from URL:', fileName)
            resource = urllib.request.urlopen(fileName)
            try:
                data = json.loads(resource.read().decode('utf-8'))
            except:
                raise HieraException('Error while parsing a json file (perhapes misformed file): ' + fileName)
            finally:
                resource.close()
        else:
            if self.printStatus:
                print('Open', fileName, 'from file:', fileName)
            with open(fileName) as data_file:  
                try:  
                    data = json.load(data_file)
                except:
                    raise HieraException('Error while parsing a json file (perhapes misformed file): ' + fileName)

    
        return data
