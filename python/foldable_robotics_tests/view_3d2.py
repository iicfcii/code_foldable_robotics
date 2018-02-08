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

app = qg.QApplication(sys.argv)

view_widget = gl.GLViewWidget()
view_widget.setBackgroundColor(pg.mkColor(1, 1, 1))
view_widget.addItem(mi)    

def clear_view():
    [view_widget.removeItem(item) for item in view_widget.items]
    view_widget.update()
    
def output_dxf():
    pass



w = qg.QMainWindow()
#l = qg.QVBoxLayout()
m = qg.QMenu('asdf')
clear_act = qg.QAction("&Clear", None,shortcut=qg.QKeySequence.New,statusTip="Clear View", triggered=clear_view)
output_act= qg.QAction("&Output dxf", None,shortcut='ctrl+o',statusTip="Output Dxf", triggered=output_dxf)

fileMenu = w.menuBar().addMenu("&File")
fileMenu.addAction(clear_act)
fileMenu.addAction(output_act)
w.setCentralWidget(view_widget)

w.show()
sys.exit(app.exec())