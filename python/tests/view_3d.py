# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:44:33 2016

@author: daukes
"""

from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer
import shapely.geometry as sg
import numpy
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import PyQt4.QtGui as qg
import PyQt4.QtCore as qc
import sys
import pypoly2tri
import matplotlib.cm as cm
c = pg.mkColor(1, 1, 1)


box = sg.box(-2,-1,2,1)
box = Layer(box)

circle =sg.Point((0,0))
circle = Layer(circle)<<1.5
lam = Laminate(box,circle)
lam -= lam.scale(.5,.5)

#box.plot(True)

from pypoly2tri.cdt import CDT

def check_loop(loop):
    if loop[-1]==loop[0]:
        return loop[:-1]

colors = [[1,0,0,1]]*3
edge_color = (1,1,1,1)

mi = []
lines = []
for ii,layer in enumerate(lam):
    color1 = list(cm.plasma(ii/(len(lam))))
#    color1[3] = .1
    for geom in layer.geoms:
        if isinstance(geom,sg.Polygon):
            exterior = list(geom.exterior.coords)
            exterior = check_loop(exterior)
            exterior2 = [pypoly2tri.shapes.Point(*item) for item in exterior]
            cdt = CDT(exterior2)
            interiors = []
            for interior in geom.interiors:
                interior= list(interior.coords)
                interior = check_loop(interior)
                interiors.append(interior)
            for interior in interiors:
                interior2 = [pypoly2tri.shapes.Point(*item) for item in interior]
                cdt.AddHole(interior2)
            cdt.Triangulate()
            tris =cdt.GetTriangles()
            points = cdt.GetPoints()
            points2 = numpy.array([item.toTuple() for item in points])
            tris2 = numpy.array([[points.index(point) for point in tri.points_] for tri in tris],dtype = int)
            print(tris2)
            z = points2[:,0:1]*0+ii
            points3 = numpy.c_[points2,z]
            verts =points3[tris2]
#            verts2 =points3[tris2[:,::-1]]
            
#            vc =numpy.array([[1,0,0,1]]*len(points3))
#            fc = [[1,0,0,1]]*len(tris2)
            
            verts_colors = [[color1]*3]*len(tris2)
#            meshdata = gl.MeshData(points3,tris,vertexColors = vc,faceColors=fc)
            mi.append(gl.GLMeshItem(vertexes=verts,vertexColors=verts_colors,smooth=False,shader='balloon',drawEdges=False,edgeColor = edge_color))
#            mi.append(gl.GLMeshItem(vertexes=verts2,vertexColors=verts_colors,smooth=False,shader='balloon',drawEdges=False,edgeColor = edge_color))
            
#            for loop in [exterior]+interiors:
#                loop = loop+loop[0:1]
#                loop = numpy.array(loop)
#                loop = numpy.c_[loop,loop[:,0]*0+ii]
#                color = [1,1,1,1]
#                pi =gl.GLLinePlotItem(pos = loop,color =color, width=10)
#                lines.append(pi)
app = qg.QApplication(sys.argv)

view_widget = gl.GLViewWidget()
#view_widget.setBackgroundColor(c)
#    c = pg.mkColor(1, 1, 1)
#    view.setBackgroundColor(c)

view_widget.show()

## create three grids, add each to the view
zgrid = gl.GLGridItem()
#view_widget.addItem(zgrid)
zgrid.scale(0.1, 0.1, 0.1)
for item in lines+mi:
    view_widget.addItem(item)    
#sys.exit(app.exec())