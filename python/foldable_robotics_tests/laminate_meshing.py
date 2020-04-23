# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:07:00 2020

@author: danaukes
"""

from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
from foldable_robotics.dynamics_info import MaterialProperty

import shapely.geometry as sg
import numpy

g = sg.box(0,0,.1,.01)
l = Layer(g)
L = Laminate(l)
m = MaterialProperty('carbon fiber',(1,0,0),.0005,1e7,1e7,1000,.3,False,True,False,False)
M = [m]
T = [item.thickness for item in M]

mo = L.to_mesh(T,characteristic_len_min = .0005,characteristic_len_max = .001)
#mesh_data = L.to_mesh(T)

triangles_outer = mo.cells['triangle']


import idealab_tools.plot_tris as pt

#pt.plot_mesh_object(mo,face_colors = (1,0,0,.5),draw_edges = True)

import pyfea.fea as fea

material = fea.Material(1e7,.3)
factor = 1

coordinates = mo.points[:]
elements = mo.cells['tetra']

used_elements = fea.find_used_elements(elements,triangles_outer)
coordinates,mapping = fea.coord_reduce(coordinates,used_elements)
triangles_outer = fea.element_reduce(triangles_outer,mapping)
elements= fea.element_reduce(elements,mapping)

a=fea.analyze(coordinates,elements)
print(a)
elements[a] = elements[a][:,(0,2,1,3)]
a=fea.analyze(coordinates,elements)
print(a)

T = coordinates[elements[:,1:]]-coordinates[elements[:,0:1]]
dt = numpy.array([numpy.linalg.det(item) for item in T])
elements = elements[dt!=0]


xx = coordinates[:,0]
yy = coordinates[:,1]
zz = coordinates[:,2]

x_min = coordinates.min(0)[0]
x_max = coordinates.max(0)[0]
y_min = coordinates.min(0)[1]
y_max = coordinates.max(0)[1]
z_min = coordinates.min(0)[2]
z_max = coordinates.max(0)[2]

ii_tri_x_minus = ((coordinates[triangles_outer,0]==x_min).sum(1)==3)
ii_tri_x_plus = ((coordinates[triangles_outer,0]==x_max).sum(1)==3)
ii_tri_y_minus = ((coordinates[triangles_outer,1]==y_min).sum(1)==3)
ii_tri_y_plus = ((coordinates[triangles_outer,1]==y_max).sum(1)==3)
ii_tri_z_minus = ((coordinates[triangles_outer,2]==z_min).sum(1)==3)
ii_tri_z_plus = ((coordinates[triangles_outer,2]==z_max).sum(1)==3)
#ii_neumann = (ii_bottom+ii_top)==0

constrained_tris = triangles_outer[ii_tri_x_minus]
constrained_nodes = numpy.unique(constrained_tris)

surface_forces= numpy.zeros((0,3),dtype = int)
surface_forces = triangles_outer[ii_tri_x_plus]
neumann_nodes = numpy.unique(surface_forces)

#heat_source_nodes = 
#fea.plot_triangles(coordinates,triangles_outer)


def volume_force(x):
    density = 1000
    volforce = numpy.zeros((x.shape[0],3))
#    volforce[:,2] = -9.81*density
#    volforce[:,2] = -9.81
    return volforce    

f = .01
a = .01*.01
p = f/a

def area_force(x,n):
    f = numpy.array([[0,0,-p]])
    return f

point_forces = []
#point_force_tris = triangles_outer[ii_tri_x_plus]
#point_force_nodes = numpy.unique(point_force_tris)
#ll = len(point_force_nodes)
#point_forces = [(ii,[0,0,-.1/ll]) for ii in point_force_nodes]

#def point_force(x):
#    volforce = numpy.zeros((x.shape[0],3))
#    volforce[:,2] = -9.81*density
#    return volforce    

def u_d(x):
    mm = x.shape[0]
    M = numpy.zeros((3*mm,3))
    W = numpy.zeros((3*mm,1))
    
#    aa = (x[:,0]==1).nonzero()[0]
    bb = (x[:,0]==x_min).nonzero()[0]

    M[3*bb,0] = 1
    M[3*bb+1,1] = 1
    M[3*bb+2,2] = 1

#    M[3*aa+2,2] = 1
#    W[3*aa+2] = 1e-1
    return W,M

elements4 = []

x,u = fea.compute(material,coordinates,elements,elements4,surface_forces,constrained_nodes,volume_force,area_force,u_d,point_forces=point_forces)
u3 = u.reshape((int(len(u)/3),3))
d = ((u3**2).sum(1))**.5
d_max = d.max()
print(d_max)
ax = fea.show3(elements,elements4,triangles_outer,coordinates,u,material,factor=factor,draw_edges = True,edge_color = (0,0,0,.5)) 
