# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
#import shapely.geometry as sg
#from .shape import Base
#from . import shape
import shapely.geometry
import shapely.geometry as sg
import shapely.affinity as sa
from .class_algebra import ClassAlgebra
import shapely.ops as so

def is_collection(item):
    collections = [
        shapely.geometry.MultiPolygon,
        shapely.geometry.GeometryCollection,
        shapely.geometry.MultiLineString,
        shapely.geometry.multilinestring.MultiLineString,
        shapely.geometry.MultiPoint]
    iscollection = [isinstance(item, cls) for cls in collections]
    return any(iscollection)

def extract_r(item,list_in = None):
    list_in = list_in or []
    if is_collection(item):
        list_in.extend([item3 for item2 in item.geoms for item3 in extract_r(item2,list_in)])
    else:
        list_in.append(item)
    return list_in
    
def condition_shapely_entities(*entities):
    entities = [item for item2 in entities for item in extract_r(item2)]
    entities = [item for item in entities if any([isinstance(item,classitem) for classitem in [shapely.geometry.Polygon,shapely.geometry.LineString,shapely.geometry.Point]])]
    entities = [item for item in entities if not item.is_empty]
#    entities = [item for item in entities if not item.is_valid]
    return entities

class Layer(ClassAlgebra):

    def __init__(self, *geoms):
        geoms = self.flatten(geoms)
        self.geoms = geoms
        self.id = id(self)

    @classmethod
    def new(cls,*geoms):
        geoms = cls.flatten(geoms)
        new = cls(*geoms)
        return new

    def copy(self,identical = True):
        new = type(self)(*[geom.copy(identical) for geom in self.geoms])        
        if identical:        
            new.id = self.id
        return new

    def plot(self,*args,**kwargs):
        for geom in self.geoms:
            self.plot_poly(geom,*args,**kwargs)

    def plot_poly(self,poly,color = (1,0,0,1)):
        from matplotlib.patches import PathPatch
        from matplotlib.path import Path
        import matplotlib.pyplot as plt
        axes = plt.gca()
        vertices = []
        codes = []
        if isinstance(poly,sg.Polygon):
            exterior = list(poly.exterior.coords)
            interiors = [list(interior.coords) for interior in poly.interiors]
        elif isinstance(poly,sg.LineString):
            exterior = list(poly.coords)
            interiors = []
        for item in [exterior]+interiors:
            vertices.extend(item+[(0,0)])
            codes.extend([Path.MOVETO]+([Path.LINETO]*(len(item)-1))+[Path.CLOSEPOLY])
        path = Path(vertices,codes)
        color = list(color)
        patch = PathPatch(path,facecolor=color[:3]+[.25],edgecolor=color[:3]+[.5])        
        axes.add_patch(patch)
        plt.axis('equal')
        
    def binary_operation(self,other,function_name):
        a = so.unary_union(self.geoms)
        b = so.unary_union(other.geoms)
        function = getattr(a,function_name)
        c = function(b)
        e = self.flatten(c)
        return type(self)(*e)

    @staticmethod
    def flatten(geoms):
        geoms = so.unary_union(geoms)
        geoms2 = condition_shapely_entities(geoms)
        return geoms2

    def union(self,other):
        return self.binary_operation(other,'union')

    def difference(self,other):
        return self.binary_operation(other,'difference')

    def symmetric_difference(self,other):
        return self.binary_operation(other,'symmetric_difference')

    def intersection(self,other):
        return self.binary_operation(other,'intersection')
    
    def buffer(self,value,resolution = 0):
        return self.dilate(value,resolution)

    def dilate(self,value,resolution = 0):
        geoms = so.unary_union(self.geoms)
        new_geoms = (geoms.buffer(value,resolution))
        new_geoms = self.flatten(new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def erode(self,value,resolution = None):
        return self.dilate(-value,resolution)
        
    def translate(self,*args,**kwargs):
        geoms = so.unary_union(self.geoms)
        new_geoms = sa.translate(geoms,*args,**kwargs)
        new_geoms = self.flatten(new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def rotate(self,*args,**kwargs):
        geoms = so.unary_union(self.geoms)
        new_geoms = sa.rotate(geoms,*args,**kwargs)
        new_geoms = self.flatten(new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def affine_transform(self,*args,**kwargs):
        geoms = so.unary_union(self.geoms)
        new_geoms = sa.affine_transform(geoms,*args,**kwargs)
        new_geoms = self.flatten(new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def export_dxf(self,name):
        import ezdxf
        dwg = ezdxf.new('R2010')
        msp = dwg.modelspace()
        for geom in self.geoms:
            segments = self.get_segments(geom)
            for segment in segments:
                for c0,c1 in zip(segment[:-1],segment[1:]):
                    print(c0,c1)
                    msp.add_line(c0,c1)
        dwg.saveas(name)
        
    def get_segments(self,poly):
        if isinstance(poly,sg.Polygon):
            exterior = list(poly.exterior.coords)
            interiors = [list(interior.coords) for interior in poly.interiors]
            segments = [exterior]+interiors
            segments = [loop+loop[0:1] for loop in segments]
            
        elif isinstance(poly,sg.LineString):
            segments = list(poly.coords)
            
        return segments