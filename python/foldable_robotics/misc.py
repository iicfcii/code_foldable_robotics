# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:29:55 2016

@author: daukes
"""
import shapely.geometry as sg

def plot_poly(poly,color = (1,0,0,1)):
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

