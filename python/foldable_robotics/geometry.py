# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
import numpy
import math

def length(v1):
    '''
    finds the length of a vector
    
    :param v1: the vector
    :type v1: tuple or list of floats
    :rtype: float
    '''
    v1 = numpy.array(v1)
    l = (v1.dot(v1))**.5
    return l
    
def angle(v1,v2):
    '''
    finds the angle between two vectors
    
    :param v1: the first vector
    :type v1: tuple or list of floats
    :param v2: the second vector
    :type v2: tuple or list of floats
    :rtype: float
    '''
    v1 = numpy.array(v1).flatten()
    v2 = numpy.array(v2).flatten()
    sint = numpy.cross(v1,v2).flatten()
    if len(sint)>1:
        sint = length(sint)
    cost = numpy.dot(v1,v2)
    t = math.atan2(sint,cost)
    return t

