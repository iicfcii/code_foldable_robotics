#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 14:24:17 2021

@author: danaukes
"""

import skimage
import skimage.color
import skimage.filters
import skimage.io
import skimage.measure

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import shapely.geometry as sg

import foldable_robotics
from foldable_robotics.layer import Layer
foldable_robotics.resolution = 4

import ladybug_geometry_polyskel.polyskel as ps


def plot_subtree(*subtrees):
    for subtree in subtrees:
        for sink in subtree.sinks:
            plt.plot((subtree.source.x, sink.x),(subtree.source.y, sink.y))
    
def same_point(a,b,tolerance=1e-7):
    return a.distance(b)<tolerance
    

filename = 'hi2.jpg'

sigma = 1

image = skimage.io.imread(fname=filename)
plt.figure()
plt.imshow(image)

gray = skimage.color.rgb2gray(image)

plt.figure()
plt.imshow(gray,cmap=cm.gray)
blur = skimage.filters.gaussian(gray, sigma=sigma)

t = skimage.filters.threshold_otsu(blur)
mask = (blur > t)
plt.figure()
plt.imshow(mask,cmap=cm.gray)

result = skimage.measure.find_contours(mask)

polys = [Layer(sg.Polygon(item)) for item in result]
l = Layer()
for item in polys:
    l^=item

l= l.rotate(-90)
l.plot(new=True)
l<<=2
l.plot(new=True)
l = l.simplify(2)
l.plot(new=True)

ls = [Layer(item) for item in l.geoms]

for item in ls:
    # skeleton = ps.skeletonize(item.exteriors()[0], item.interiors())
    skeleton = ps.skeleton_as_subtree_list(item.exteriors()[0][::-1], item.interiors())
    all_sources = [item.source for item in skeleton]
    all_sinks = [item2 for item in skeleton for item2 in item.sinks]
    non_terminal_sinks = [item for item in all_sinks if item in all_sources]
    
    for arc in skeleton:
        for sink in arc.sinks:
            if sink in non_terminal_sinks:
                plt.plot((arc.source.x, sink.x),(arc.source.y, sink.y))
