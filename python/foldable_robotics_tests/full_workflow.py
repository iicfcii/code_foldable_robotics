# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import foldable_robotics
import foldable_robotics.dxf 
import numpy
import matplotlib.pyplot as plt
import shapely.geometry as sg
from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import foldable_robotics.manufacturing
import foldable_robotics.parts.castellated_hinge1

filename = 'flipper.dxf'

body = foldable_robotics.dxf.read_lwpolylines(filename,layer='body')

bodies = [Layer(sg.Polygon(item)) for item in body]
body = bodies.pop(0)
for item in bodies:
    body ^= item
body = body.to_laminate(5)
body.plot()
plt.savefig('f0.png')

hinges_up = foldable_robotics.dxf.read_lines(filename,layer='hinge_mountain')
hinges_down = foldable_robotics.dxf.read_lines(filename,layer='hinge_valley')
hinges = hinges_down+hinges_up

fig = plt.figure()
for hinge in numpy.array(hinges):
    plt.plot(hinge[:,0],hinge[:,1])
plt.axis('equal')
plt.savefig('f1.png')

simple_hinges = Layer()
for item in hinges:
    simple_hinges |= Layer(sg.LineString(item))
simple_hinges<<=.1
simple_hinges = Laminate(simple_hinges,simple_hinges,Layer(),simple_hinges,simple_hinges)
simple_hinges.plot(new=True)
plt.savefig('f2.png')

design = body-simple_hinges
design.plot(new=True)
plt.savefig('f3.png')

castellated_hinge = foldable_robotics.parts.castellated_hinge1.generate()
castellated_hinge = castellated_hinge.scale(1,.1)

castellated_hinges = Layer().to_laminate(5)
for p3,p4 in hinges:
    castellated_hinges|=castellated_hinge.map_line_stretch((0,0),(1,0),p3,p4)

castellated_hinges.plot(new=True)
plt.savefig('f4.png')

cut_lines = foldable_robotics.dxf.read_lines(filename,layer='cuts')
cut_lines += foldable_robotics.dxf.read_lwpolylines(filename,layer='cuts')

cuts = Layer()
for item in cut_lines:
    cuts |= Layer(sg.LineString(item))
cuts<<=.01
cuts = cuts.to_laminate(5)
cuts.plot(new=True)
plt.savefig('f5.png')

holes = foldable_robotics.dxf.read_lwpolylines(filename,layer='holes')
points = []
for item in holes:
    for vertex in item:
        points.append(sg.Point(*vertex))
holes_layer = Layer(*points)
holes_layer<<=.1
holes_lam = holes_layer.to_laminate(5)
holes_lam.plot(new=True)
plt.savefig('f6.png')

hole,dummy = foldable_robotics.manufacturing.calc_hole(hinges,.1)
hole = hole.to_laminate(5)
hole = foldable_robotics.manufacturing.cleanup(hole,.025,resolution = 4)
hole.plot(new=True)
plt.savefig('f7.png')

design1 = body- hole -simple_hinges - cuts - holes_lam
design1.plot(new=True)
plt.savefig('f8.png')

design2 = body- hole -castellated_hinges - cuts-holes_lam
design2.plot(new=True)
plt.savefig('f9.png')

both = (design1 | design2.translate(10))

design2.export_dxf('design2.dxf')

both2=foldable_robotics.manufacturing.cleanup(both2,.01)
from foldable_robotics.dynamics_info import MaterialProperty
m = MaterialProperty.make_n_blank(5,thickness = .1)
import idealab_tools.plot_tris
mi=both.mesh_items(m)
idealab_tools.plot_tris.plot_mi(mi)

design_outer = foldable_robotics.manufacturing.unary_union(design2)
sheet = (design_outer<<.5).bounding_box()
sheet=sheet.to_laminate(5)

support_width = .1

keepout =  foldable_robotics.manufacturing.keepout_laser(design2)
second_pass_scrap = sheet-keepout
second_pass_scrap.plot(new=True)
plt.savefig('f10.png')

#Why is the center cut out of every hinge?

first_pass_scrap = sheet - design2-second_pass_scrap
first_pass_scrap.plot(new=True)
plt.savefig('f11.png')
first_pass_scrap = foldable_robotics.manufacturing.cleanup(first_pass_scrap,.00001)
first_pass_scrap.plot(new=True)
plt.savefig('f12.png')

support = foldable_robotics.manufacturing.support(design2,foldable_robotics.manufacturing.keepout_laser,support_width,support_width/2)
support.plot(new=True)
plt.savefig('f13.png')

#Calculate the web by using only the material which can be cut, minus a gap determined by the support width.  Is that the only material you can use?

web = sheet-(keepout<<support_width)

supported_design = web|design2|support
supported_design.plot(new=True)
plt.savefig('f14.png')

cut_line = keepout<<.05

cut_line.plot(new=True)
plt.savefig('f15.png')

cut_material = (keepout<<.1)-keepout
cut_material.plot(new=True)
plt.savefig('f16.png')

remaining_material = supported_design-cut_material
remaining_material.plot(new=True)
plt.savefig('f17.png')

results = foldable_robotics.manufacturing.find_connected(remaining_material,[False,True,False,True,False])
for ii,item in enumerate(results):
    item.plot(new=True)
    plt.savefig('f18-'+str(ii)+'.png')

zero = results[0]^design2
zero = foldable_robotics.manufacturing.cleanup(zero,.00001)
zero.plot(new=True)
plt.savefig('f19.png')

zero[0].geoms


first_pass_cut = sheet-supported_design
first_pass_cut.plot(new=True)
plt.savefig('f20.png')

first_pass_scrap_new = sheet-first_pass_cut
first_pass_scrap_new.plot(new=True)
plt.savefig('f21.png')

