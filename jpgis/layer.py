from builtins import object
from qgis.PyQt.QtCore import QVariant
from qgis.core import *

from . import jpgis
from .feature import WKB_TYPE


class JPGISLayers(object):
    def __init__(self, tr={}):
        self.tr = tr
        self.layers = {}

    def values(self):
        return list(self.layers.values())

    def addFeatures(self, handler, **kwargs):
        into = kwargs.get("into")
        changed = []
        for key, value in list(handler.features.items()):
            if key not in self.layers:
                if into is not None and self.check_same(key, into):
                    self.layers[key] = into
                else:
                    self.layers[key] = self.createLayer(key)
            layer = self.layers[key]
            provider = layer.dataProvider()
            provider.addFeatures([x.toQgsFeature(provider.fields()) for x in value])
            layer.updateExtents()

    def createLayer(self, elem):
        fields = ([x[0] for x in jpgis.GML.AbstractFeature_attrib_properties] +
                  [x[0] for x in jpgis.FGD.FGDFeature_properties] +
                  [x[0] for x in getattr(jpgis.FGD, elem + "_properties")])
        _, type = getattr(jpgis.FGD, elem + "_geometry")
        layer = QgsVectorLayer(type + "?crs=EPSG:4612", self.tr.get(elem, elem), "memory")
        provider = layer.dataProvider()
        provider.addAttributes([QgsField(x, QVariant.String) for x in fields])
        layer.updateFields()
        return layer

    def check_same(self, elem, layer):
        layer_fields = [x.name() for x in layer.fields()]
        elem_fields = [x[0] for x in getattr(jpgis.FGD, elem + "_properties")]
        _, type = getattr(jpgis.FGD, elem + "_geometry")
        return layer_fields == elem_fields and WKB_TYPE[type] == layer.geometryType()

