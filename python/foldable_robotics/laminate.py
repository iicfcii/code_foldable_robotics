# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from .class_algebra import ClassAlgebra

class IterableLaminate(object):

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.list[index]

        elif isinstance(index, slice):
            return self.list[index]

    def __setitem__(self, index, v):
        if isinstance(index, int):
            self.list[index] = v
            
        elif isinstance(index, slice):
            self.list[index] = v

    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

class Laminate(IterableLaminate,ClassAlgebra):
    def __init__(self, *layers):
        self.layers = layers
        self.id = id(self)

    def copy(self,identical = True):
        new = type(self)(*[layer.copy(identical) for layer in self.layers])
        if identical:        
            new.id = self.id
        return new

    def plot(self):
        for geom in self.layers:
            geom.plot()
    
    @property
    def list(self):
        return self.layers
    
#    @list.setter
#    def list(self,v):
#        self.layers = v