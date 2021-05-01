# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 21:44:56 2021

@author: danaukes
"""

# https://github.com/idealabasu/polyskel/blob/master/LICENSE
# https://github.com/migurski/Skeletron

# import sys
# sys.path.append(r'C:\Users\danaukes\code_external')

import shapely.geometry as sg
import numpy
from foldable_robotics.layer import Layer
import matplotlib.pyplot as plt
# import scipy.spatial as ss


import polyskel.polyskel as ps
from PIL import Image, ImageDraw


# foldable_robotics.
x = numpy.r_[0:10]
y = numpy.sin(x)

xy = numpy.array([x,y])

# plt.plot(x,y)

ls = sg.LineString(xy.T)

l = Layer(ls)

l<<=.1
# l.plot()

xy2 = numpy.array(l.geoms[0].exterior.coords)

l2=l<<1e-1
p = l2.geoms[0]

# d = ss.Delaunay(xy2)

# v = ss.Voronoi(xy2)

# ss.voronoi_plot_2d(v)

# # for a,b in v.ridge_points:
#     # ab = numpy.array()
#     # plt.plot()

# plt.figure()
    

# for item in v.ridge_vertices:
#     if not(-1 in item):
   
#         plt.plot(v.vertices[item][:,0],v.vertices[item][:,1])
    
# # interior_ridges
# items = []
# for item in v.ridge_vertices:
#     if not(-1 in item):
#         # item2 = item
#         a,b = v.vertices[item]
#         a = sg.Point(a)
#         b = sg.Point(b)
#         if p.intersects(a) and p.intersects(b):
#             items.append(item)
            
# f  = plt.figure()            
# ax=f.add_subplot()
# for item in items:
    
#     plt.plot(v.vertices[item][:,0],v.vertices[item][:,1])

# l.plot()
# l2.plot()

verbose = False

im = Image.new("RGB", tuple(([int(item) for item in xy2.max(0)])), "white")
draw = ImageDraw.Draw(im)
if verbose:
    ps.set_debug((im, draw))

skeleton = ps.skeletonize(xy2, [])
for arc in skeleton:
    for sink in arc.sinks:
        plt.plot((arc.source.x, sink.x),(arc.source.y, sink.y))

# im.show()
