#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 14:24:17 2021

@author: danaukes
"""

import matplotlib.pyplot as plt
import PIL
from PIL import Image
from PIL import Image, ImageFilter
import os
import numpy
import skimage
import skimage.measure
from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import shapely.geometry as sg

import sys
import numpy as np
import skimage.color
import skimage.filters
import skimage.io


import polyskel.polyskel as ps

filename = '~/sig.jpg'

# get filename and sigma value from command line
# filename = sys.argv[1]
sigma = 2

# read and display the original image
image = skimage.io.imread(fname=filename)
skimage.io.imshow(image)

blur = skimage.color.rgb2gray(image)
# blur = skimage.filters.gaussian(blur, sigma=sigma)

# perform adaptive thresholding
t = skimage.filters.threshold_otsu(blur)
mask = (blur > t)
# mask = numpy.array(mask*255,dtype = numpy.uint8)

skimage.io.imshow(mask*1)

# use the mask to select the "interesting" part of the image
# sel = np.zeros_like(image)
# sel[mask] = image[mask]

# display the result
# skimage.io.imshow(sel)

# # i = Image.open(os.path.expanduser(filename))
# # print(i)

# # i.thumbnail((400,400))
# # i2 = i.convert('L')
# # a = numpy.array(i2)
# # b = (a>120)*255
# # c = numpy.array(b,dtype=numpy.uint8)
# # i3 = Image.fromarray(c)
# # i3 = i3.filter(ImageFilter.GaussianBlur(radius=1))
# # i4 = i3.crop((0,100,400,200))
# # i4.show()

result = skimage.measure.find_contours(mask)

polys = [Layer(sg.Polygon(item)) for item in result]
l = Layer()
for item in polys:
    l^=item
l= l.rotate(-90)
m = 1
l = l.simplify(5)
# l = l<<m
l.plot(new=True)
plt.figure()

ls = [Layer(item) for item in l.geoms]
for item in ls:
    # xy2 = item.exteriors()[0],item.interiors())
    
    skeleton = ps.skeletonize(item.exteriors()[0], item.interiors())
    for arc in skeleton:
        for sink in arc.sinks:
            plt.plot((arc.source.x, sink.x),(arc.source.y, sink.y))
