from parser.JsonParser import JsonParser
from shapely.geometry import shape
class ShapesParser(JsonParser):
    def __init__(self, filePath, targetName):
        super().__init__(filePath.rstrip('/') + '/' + targetName + '.geojson')
        self.shapes = self.__createShapes__()
  
    def __createShapes__(self):
        shapes = []
        for feature in self.__jsonData__['features']:
            shapes.append(shape(feature['geometry']))
        return shapes
