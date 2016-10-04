# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 15:44:33 2016

@author: daukes
"""

from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer
import shapely.geometry as sg
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import PyQt4.QtGui as qg
import sys

box = sg.box(-2,-1,2,1)
box = Layer(box)

circle =sg.Point((0,0))
circle = Layer(circle)<<1.5
lam = Laminate(box,circle)
lam -= lam.scale(.5,.5)
lam |= lam.translate(0,-4)

t = [1]*len(lam)
mi = lam.mesh_items(thickness=t)

#zgrid = gl.GLGridItem()
#zgrid.scale(0.1, 0.1, 0.1)
#view_widget.addItem(zgrid)

app = qg.QApplication(sys.argv)
view_widget = gl.GLViewWidget()
view_widget.setBackgroundColor(pg.mkColor(1, 1, 1))
for item in mi:
    view_widget.addItem(item)    
view_widget.show()
sys.exit(app.exec())