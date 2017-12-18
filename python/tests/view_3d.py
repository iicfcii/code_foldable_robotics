# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer
import shapely.geometry as sg
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import PyQt5.QtGui as qg
import sys
from foldable_robotics.dynamics_info import MaterialProperty


box = sg.box(-2,-1,2,1)
box = Layer(box)

circle =sg.Point((0,0))
circle = Layer(circle)<<1.5
lam = Laminate(box,circle)
lam -= lam.scale(.5,.5)
lam |= lam.translate(0,-4)

m1 = MaterialProperty('red',(1,0,0,.5),.1,1,1,1,.3,False,True,False,False)
m2 = MaterialProperty('cyan',(0,1,1,.5),.1,1,1,1,.3,False,True,False,False)
mp = [m1,m2]
mi = lam.mesh_items(mp)

#zgrid = gl.GLGridItem()
#zgrid.scale(0.1, 0.1, 0.1)
#view_widget.addItem(zgrid)

app = qg.QApplication(sys.argv)
view_widget = gl.GLViewWidget()
view_widget.setBackgroundColor(pg.mkColor(1, 1, 1))
view_widget.addItem(mi)    
view_widget.show()
sys.exit(app.exec())