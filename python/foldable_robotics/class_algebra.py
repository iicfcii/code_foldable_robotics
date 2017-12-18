# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
class ClassAlgebra(object):
    def __or__(self,other):
        return self.union(other)
        
    def __sub__(self,other):
        return self.difference(other)
        
    def __and__(self,other):
        return self.intersection(other)        

    def __xor__(self,other):
        return self.symmetric_difference(other)

    def __lshift__(self,value):
        return self.dilate(value)

    def __rshift__(self,value):
        return self.erode(value)
        
