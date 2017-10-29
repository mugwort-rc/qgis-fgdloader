# -*- conding: utf-8 -*-

from collections import defaultdict
import xml.sax.handler

from . import feature


GML_Namespace = "http://www.opengis.net/gml/3.2"

FGD_Namespace = "http://fgd.gsi.go.jp/spec/2008/FGD_GMLSchema"


def _gml(name):
    return (GML_Namespace, name)

def _fgd(name):
    return (FGD_Namespace, name)


class GML:
    Namespace = GML_Namespace

    id = _gml("id")

    pos = _gml("pos")
    posList = _gml("posList")

    # gml:AbstractFeature

    AbstractFeature_attrib_properties = [
        ("id", "string"),
    ]


class FGD:
    """XML Schema for Down Loaded Fundamental Geospatial Data"""

    Namespace = FGD_Namespace

    # fgd:FGDFeatureType

    FGDFeature_properties = [
        ("fid", "string"),
        ("lfSpanFr", "string"),
        ("lfSpanTo", "string"),
        ("devDate", "string"),
        ("orgGILvl", "string"),
        ("orgMDId", "string"),
        ("vis", "string"),
    ]

    fid = _fgd("fid")
    lfSpanFr = _fgd("lfSpanFr")
    lfSpanTo = _fgd("lfSpanTo")
    devDate = _fgd("devDate")
    orgGILvl = _fgd("orgGILvl")
    orgMDId = _fgd("orgMDId")
    vis = _fgd("vis")

    GCP = _fgd("GCP")
    DEM = _fgd("DEM")
    DGHM = _fgd("DGHM")
    ElevPt = _fgd("ElevPt")
    Cntr = _fgd("Cntr")
    AdmArea = _fgd("AdmArea")
    AdmBdry = _fgd("AdmBdry")
    CommBdry = _fgd("CommBdry")
    AdmPt = _fgd("AdmPt")
    CommPt = _fgd("CommPt")
    SBArea = _fgd("SBArea")
    SBBdry = _fgd("SBBdry")
    SBAPt = _fgd("SBAPt")
    WA = _fgd("WA")
    WL = _fgd("WL")
    CStline = _fgd("CStline")
    WStrL = _fgd("WStrL")
    WStrA = _fgd("WStrA")
    LeveeEdge = _fgd("LeveeEdge")
    RvrMgtBdry = _fgd("RvrMgtBdry")
    BldA = _fgd("BldA")
    BldL = _fgd("BldL")
    RdEdg = _fgd("RdEdg")
    RdCompt = _fgd("RdCompt")
    RdASL = _fgd("RdASL")
    RdArea = _fgd("RdArea")
    RdSgmtA = _fgd("RdSgmtA")
    RdMgtBdry = _fgd("RdMgtBdry")
    RailCL = _fgd("RailCL")

    Features = [
        GCP,
        DEM,
        DGHM,
        ElevPt,
        Cntr,
        AdmArea,
        AdmBdry,
        CommBdry,
        AdmPt,
        CommPt,
        SBArea,
        SBBdry,
        SBAPt,
        WA,
        WL,
        CStline,
        WStrL,
        WStrA,
        LeveeEdge,
        RvrMgtBdry,
        BldA,
        BldL,
        RdEdg,
        RdCompt,
        RdASL,
        RdArea,
        RdSgmtA,
        RdMgtBdry,
        RailCL,
    ]

    # fgd:GCPType [Point]

    GCP_geometry = ("pos", "point")
    GCP_properties = [
        ("advNo", "string"),
        ("orgName", "string"),
        ("type", "string"),
        ("gcpClass", "string"),
        ("gcpCode", "string"),
        ("name", "string"),
        ("B", "double"),
        ("L", "double"),
        ("alti", "double"),
        ("altiAcc", "integer"),
    ]

    pos = _fgd("pos")
    advNo = _fgd("advNo")
    orgName = _fgd("orgName")
    type = _fgd("type")
    gcpClass = _fgd("gcpClass")
    gcpCode = _fgd("gcpCode")
    name = _fgd("name")
    B = _fgd("B")
    L = _fgd("L")
    alti = _fgd("alti")
    altiAcc = _fgd("altiAcc")

    # fgd:DEMType [Polygon]

    DEM_geometry = DGHM_geometry = ("coverage", "polygon")
    DEM_properties = DGHM_properties = [
        ("type", "string"),
        ("mesh", "string"),
    ]

    #type = _fgd("type")
    mesh = _fgd("mesh")
    coverage = _fgd("coverage")

    # fgd:DGHMType [Polygon]

    #type = _fgd("type")
    #mesh = _fgd("mesh")
    #coverage = _fgd("coverage")

    # fgd:ElevPtType [Point]

    ElevPt_geometry = ("pos", "point")
    ElevPt_properties = [
        ("type", "string"),
        ("alti", "double"),
    ]

    #pos = _fgd("pos")
    #type = _fgd("type")
    #alti = _fgd("alti")

    # fgd:CntrType [LineString]

    Cntr_geometry = ("loc", "linestring")
    Cntr_properties = [
        ("type", "string"),
        ("alti", "double"),
    ]

    loc = _fgd("loc")
    #type = _fgd("type")
    #alti = _fgd("alti")

    # fgd:AdmAreaType [Polygon]

    AdmArea_geometry = ("area", "polygon")
    AdmArea_properties = [
        ("type", "string"),
        ("name", "string"),
        ("admCode", "string"),
        ("repPt", "object"),
    ]

    area = _fgd("area")
    #type = _fgd("type")
    #name = _fgd("name")
    admCode = _fgd("admCode")
    repPt = _fgd("repPt")

    # fgd:AdmBdryType [LineString]
    # fgd:CommBdryType [LineString]

    AdmBdry_geometry = CommBdry_geometry = ("loc", "linestring")
    AdmBdry_properties = CommBdry_properties = [
        ("type", "string"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")

    # fgd:AdmPtType [Point]
    # fgd:CommPtType [Point]

    AdmPt_geometry = CommPt_geometry = ("pos", "point")
    AdmPt_properties = CommPt_properties = [
        ("type", "string"),
        ("name", "string"),
        ("admCode", "string"),
        ("admArea", "object"),
    ]

    #type = _fgd("type")
    #name = _fgd("name")
    #admCode = _fgd("admCode")
    admArea = _fgd("admArea")

    # fgd:SBAreaType [Polygon]

    SBArea_geometry = ("area", "polygon")
    SBArea_properties = [
        ("type", "string"),
        ("sbaNo", "string"),
    ]

    #area = _fgd("area")
    #type = _fgd("type")
    sbaNo = _fgd("sbaNo")

    # fgd:SBBdryType [LineString]

    SBBdry_geometry = ("loc", "linestring")
    SBBdry_properties = []

    #loc = _fgd("loc")

    # fgd:SBAPtType [Point]

    SBAPt_geometry = ("pos", "point")
    SBAPt_properties = [
        ("sbaNo", "string"),
    ]

    #pos = _fgd("pos")
    #sbaNo = _fgd("sbaNo")

    # fgd:WAType [Polygon]

    WA_geometry = ("area", "polygon")
    WA_properties = [
        ("type", "string"),
        ("name", "string"),
    ]

    #area = _fgd("area")
    #type = _fgd("type")
    #name = _fgd("name")

    # fgd:WLType [LineString]

    WL_geometry = ("loc", "linestring")
    WL_properties = [
        ("type", "string"),
        ("name", "string"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")

    # fgd:CstlineType [LineString]

    CStline_geometry = ("loc", "linestring")
    CStline_properties = [
        ("type", "string"),
        ("name", "string"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")

    # fgd:WStrLType

    WStrL_geometry = ("loc", "linestring")
    WStrL_properties = [
        ("type", "string"),
        ("name", "string"),
        ("surfA", "object"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")
    surfA = _fgd("surfA")

    # fgd:WStrAType

    WStrA_geometry = ("area", "polygon")
    WStrA_properties = [
        ("type", "string"),
        ("name", "string"),
        ("compL", "object"),
    ]

    #area = _fgd("area")
    #type = _fgd("type")
    #name = _fgd("name")
    compL = _fgd("compL")

    # fgd:LeveeEdgeType

    LeveeEdge_geometry = ("loc", "linestring")
    LeveeEdge_properties = [
        ("name", "string"),
    ]

    #loc = _fgd("loc")
    #name = _fgd("name")

    # fgd:RvrMgtBdryType

    RvrMgtBdry_geometry = ("loc", "linestring")
    RvrMgtBdry_properties = [
        ("name", "string"),
    ]

    #loc = _fgd("loc")
    #name = _fgd("name")

    # fgd:BldAType

    BldA_geometry = ("area", "polygon")
    BldA_properties = [
        ("type", "string"),
        ("name", "string"),
        ("compL", "object"),
    ]

    #area = _fgd("area")
    #type = _fgd("type")
    #name = _fgd("name")
    #compL = _fgd("compL")

    # fgd:BldLType

    BldL_geometry = ("loc", "linestring")
    BldL_properties = [
        ("type", "string"),
        ("name", "string"),
        ("surfA", "object"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")
    #surfA = _fgd("surfA")

    # fgd:RdEdgType

    RdEdg_geometry = ("loc", "linestring")
    RdEdg_properties = [
        ("type", "string"),
        ("name", "string"),
        ("admOffice", "string"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")
    admOffice = _fgd("admOffice")

    # fgd:RdComptType

    RdCompt_geometry = ("loc", "linestring")
    RdCompt_properties = [
        ("type", "string"),
        ("name", "string"),
        ("admOffice", "string"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")
    #admOffice = _fgd("admOffice")

    # fgd:RdASLType

    RdASL_geometry = ("loc", "linestring")
    RdASL_properties = []

    #loc = _fgd("loc")

    # fgd:RdAreaType

    RdArea_geometry = ("area", "polygon")
    RdArea_properties = [
        ("name", "string"),
        ("admOffice", "string"),
    ]

    #area = _fgd("area")
    #name = _fgd("name")
    #admOffice = _fgd("admOffice")

    # fgd:RdSgmtAType

    RdSgmtA_geometry = ("area", "polygon")
    RdSgmtA_properties = [
        ("type", "string"),
        ("name", "string"),
        ("admOffice", "string"),
    ]

    #area = _fgd("area")
    #type = _fgd("type")
    #name = _fgd("name")
    #admOffice = _fgd("admOffice")

    # fgd:RdMgtBdryType

    RdMgtBdry_geometry = ("loc", "linestring")
    RdMgtBdry_properties = [
        ("name", "string"),
    ]

    #loc = _fgd("loc")
    #name = _fgd("name")

    # fgd:RailCLType

    RailCL_geometry = ("loc", "linestring")
    RailCL_properties = [
        ("type", "string"),
        ("name", "string"),
    ]

    #loc = _fgd("loc")
    #type = _fgd("type")
    #name = _fgd("name")


    FeatureTypes = [
        GCP_geometry,
        DEM_geometry,
        DGHM_geometry,
        ElevPt_geometry,
        Cntr_geometry,
        AdmArea_geometry,
        AdmBdry_geometry,
        CommBdry_geometry,
        AdmPt_geometry,
        CommPt_geometry,
        SBArea_geometry,
        SBBdry_geometry,
        SBAPt_geometry,
        WA_geometry,
        WL_geometry,
        CStline_geometry,
        WStrL_geometry,
        WStrA_geometry,
        LeveeEdge_geometry,
        RvrMgtBdry_geometry,
        BldA_geometry,
        BldL_geometry,
        RdEdg_geometry,
        RdCompt_geometry,
        RdASL_geometry,
        RdArea_geometry,
        RdSgmtA_geometry,
        RdMgtBdry_geometry,
        RailCL_geometry,
    ]



class JPGISHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.path = []

        self.features = defaultdict(list)
        self._fstack = []
        self._tstack = []
        self.tmp = None
        self.tmp_content = ""

    @property
    def current_feature(self):
        if not self._fstack:
            return None
        return self._fstack[-1]

    @property
    def current_text(self):
        if not self._tstack:
            return None
        return self._tstack[-1]

    def startDocument(self):
        pass
        
    def endDocument(self):
        pass
    
    def startElementNS(self, name, qname, attrs):
        self.path.append(name)
        self._tstack.append("")
        if name[0] == FGD.Namespace:
            for feat, (elem, type) in zip(FGD.Features, FGD.FeatureTypes):
                if name == feat:
                    f = feature.TYPE[type]()
                    if GML.id in attrs:
                        f.setAttribute("id", attrs[GML.id])
                    self._fstack.append(f)
                    break
            else:
                if hasattr(self, "start_FGD_" + name[1]):
                    getattr(self, "start_FGD_" + name[1])()
        elif name[0] == GML.Namespace:
            if hasattr(self, "start_GML_" + name[1]):
                getattr(self, "start_GML_" + name[1])()

    def endElementNS(self, name, qname):
        t = self._tstack.pop()
        if name[0] == FGD.Namespace:
            for feat in FGD.Features:
                if name == feat:
                    f = self._fstack.pop()
                    self.features[name[1]].append(f)
                    break
            else:
                if len(self.path) > 2 and hasattr(FGD, self.path[-2][1] + "_properties"):
                    for elem, type in (FGD.FGDFeature_properties + 
                                       getattr(FGD, self.path[-2][1] + "_properties")):
                        if name == _fgd(elem):
                            if type in ["string", "double", "integer"]:
                                self.current_feature.setAttribute(elem, t.strip())
                            break
                elif hasattr(self, "end_FGD_" + name[1]):
                    getattr(self, "end_FGD_" + name[1])(t)
        elif name[0] == GML.Namespace:
            if hasattr(self, "end_GML_" + name[1]):
                getattr(self, "end_GML_" + name[1])(t)
        popped = self.path.pop()
        assert popped == name

    def end_GML_pos(self, text):
        y, x = self.line2coordinate(text)
        self.current_feature.setGeometry([y, x])

    def end_GML_posList(self, text):
        points = []
        for line in text.strip().split("\n"):
            if not line.strip():
                continue
            y, x = self.line2coordinate(line)
            points.append([y, x])
        self.current_feature.setGeometry(points)

    def line2coordinate(self, text):
        return map(float, text.strip().split())

    def characters(self, content):
        if self._tstack:
            self._tstack[-1] += content
