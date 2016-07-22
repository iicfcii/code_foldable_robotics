# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:06:48 2016

@author: daukes
"""
#[numpy for matlab](https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html)
import numpy
import numpy.random

a = numpy.array([[1,2,3],[4,5,6]])
a[:,0]
a.T
b = numpy.array([4,5,6,7,8,9])
c = numpy.eye(3)
d = numpy.zeros((4,5))
f = numpy.zeros((5,4))
g = d.dot(f)
g.shape
d.shape

e=d[:,None,:]

a = numpy.random.random((4,5))
b = numpy.random.random((5,4))

#[broadcasting](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
c = a.dot(b)
d = (a[:,:,None]*b).sum(1)
print(c-d)

e = c[:,None,:]
f = e.squeeze() - c

import scipy
import scipy.linalg

d = scipy.linalg.det(c)
e = scipy.linalg.inv(c)