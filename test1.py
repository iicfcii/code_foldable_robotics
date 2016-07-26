#import matplotlib.pyplot as plt
#plt.ion()
from foldable_robotics.shape import Polygon,Polyline,Point
from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate

#import popupcad.filetypes.genericshapes as pg
#from popupcad.geometry.vertex import ShapeVertex
#import popupcad.algorithms.csg_shapely

if __name__=='__main__':
    exterior = [[0,0],[0,1],[1,2],[2,1],[2,-1],[1,-2],[0,-1]]
#    exterior = [tuple(item) for item in exterior]
    exterior2 = [(.5,0),(1,3**.5/2),(1.5,0)]
    a = Polygon(exterior,[])
    b = Polygon(exterior2,[])
    e = Polyline(exterior2,[])
    g = e.translate(-3,0)
    f = b.translate(1,1)
    h = e.translate(-1,0)
    c = (a-b)[0]
    d = a.translate(0.1,-2)
    p = Point([(-1,-1)],[])

#    aa = pg.GenericPoly([ShapeVertex(item) for item in exterior],[])
#    bb = pg.GenericPoly([ShapeVertex(item) for item in exterior2],[])

#    a.plot()
#    b.plot()
#    A=a.to_shapely()
#    B=b.to_shapely()
#    C = A.difference(B)
#    c=csg_shapely.to_generic(C)
#    l = Layer.new(c,f,d,e,g,h)
    l = Layer.new(a,g,p)
#    m = Layer.new(c)
#    m = l.dilate(.5)
    
#    l.plot()
#    plt.figure()
#    m.plot()
    n = (l.dilate(.5,4))-(l.dilate(.1,4))
    m = n.translate(1,0)|l
#    m.plot()
    
    lam = Laminate(l,n,m)
#    lam.plot()
#    plt.figure()
    #m.rotate(15,about=(1,-2)).plot()
#    plt.figure()
    #a.rotate(15,about=(1,-2)).plot()
    
#    plt.figure()
    a = Polygon.make_rect_bl((0,0),1,.5)
    b = a.erode(.1)[0]
    d = Polygon.make_circle_r((0,0),.3,3)
    c = ((a-b)[0]|d)[0]
#    c.plot()
#    plt.axis('equal')
#    cc = popupcad.algorithms.csg_shapely.to_generic(aa.to_shapely().difference(bb.to_shapely()).buffer(-1000))
#    c = c.erode(.3,8)
#    
#    if isinstance(c,list):
#        d = c
#    else:        
#        d=[c]
#      
#    plt.figure()
#    for item in d:
#        item.plot()

