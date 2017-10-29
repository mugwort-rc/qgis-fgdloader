from qgis.core import *


class Feature:
    def __init__(self):
        self.properties = {}
        self.coordinates = []

    def setAttribute(self, key, value):
        self.properties[key] = value

    def setGeometry(self, g):
        if self.coordinates:
            raise Exception("Geometry is already set")
        self.coordinates = g

    def toGeoJsonObject(self):
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometory": {
                "type": self.type,
                "coordinates": self.coordinates,
            }
        }

    def toQgsFeature(self, fields):
        raise NotImplementedError

    def _applyProperties(self, qf, fields):
        for field in fields:
            name = field.name()
            if name in self.properties:
                qf.setAttribute(name, self.properties[name])

    @property
    def type(self):
        raise NotImplementedError



class Point(Feature):
    def toQgsFeature(self, fields):
        f = QgsFeature(fields)
        self._applyProperties(f, fields)
        y, x = self.coordinates
        f.setGeometry(QgsGeometry.fromPoint(QgsPoint(x, y)))
        return f

    @property
    def type(self):
        return "Point"


class LineString(Feature):
    def toQgsFeature(self, fields):
        f = QgsFeature(fields)
        self._applyProperties(f, fields)
        points = []
        for coord in self.coordinates:
            y, x = coord
            points.append(QgsPoint(x, y))
        f.setGeometry(QgsGeometry.fromPolyline(points))
        return f

    @property
    def type(self):
        return "LineString"


class Polygon(Feature):
    def toQgsFeature(self, fields):
        f = QgsFeature(fields)
        self._applyProperties(f, fields)
        polygon = []
        for items in self.coordinates:
            points = []
            for coord in items:
                y, x = coord
                points.append(QgsPoint(x, y))
            polygon.append(points)
        f.setGeometry(QgsGeometry.fromPolygon(polygon))
        return f

    def setGeometry(self, g):
        self.coordinates.append(g)

    @property
    def type(self):
        return "Polygon"


TYPE = {
    "point": Point,
    "linestring": LineString,
    "polygon": Polygon,
}

WKB_TYPE = {
    "point": 0,  #QgsWkbTypes.PointGeometry,
    "linestring": 1,  #QgsWkbTypes.LineGeometry,
    "polygon": 2,  #QgsWkbTypes.PolygonGeometry,
}
