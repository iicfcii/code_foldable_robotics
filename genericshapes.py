# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

import shapely.geometry as sg
import genericshapebase
import matplotlib.pyplot as plt
import numpy
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import csg_shapely
import shapely_algebra 

class GenericPoly(genericshapebase.GenericShapeBase,shapely_algebra.ClassAlgebra):

    def to_shapely(self):
        obj = sg.Polygon(self.exterior, self.interiors)
        return obj

    def segments(self):
        return self.segments_closed()
        
    def plot(self):
        ext = numpy.array(self.exterior)
        ints =[numpy.array(interior) for interior in self.interiors]
        a=plt.plot(*self.closepath(ext).T)
        [plt.plot(*self.closepath(interior).T) for interior in ints]
        plt.axis('equal')
        
    def closepath(self,array):
        out = numpy.r_[array,array[0:1]]
        return out

        
if __name__=='__main__':
  pass