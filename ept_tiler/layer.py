
import fiona
from shapely.geometry import mapping, Polygon
from collections import OrderedDict


schema = {
   'geometry': 'Polygon',
   'properties': OrderedDict([
     ('name', 'str'),
     ('id', 'int')
   ])
 }


# Will be written when self.layer.__del__ is called
class Layer(object):
    def __init__(self, args):
        self.args = args
        self.count = 0

        self.initialize()

    def initialize(self):

        output_driver = "GeoJSON"
        self.layer = fiona.open(
                 self.args.features,
                 'w',
                 driver=output_driver,
                 schema=schema)

    def add(self, tile):
        minx = tile.minx; maxx = tile.maxx
        miny = tile.miny; maxy = tile.maxy

        poly = Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)])
        feature =  {
            'geometry': mapping(poly),
            'properties': OrderedDict([
             ('name', 'something'),
             ('id', self.count)
            ])
         }

        self.layer.write(feature)

        self.count += 1




