import matplotlib.pyplot as plt
plt.ion()
from genericshapes import GenericPoly

#import popupcad.filetypes.genericshapes as pg
#from popupcad.geometry.vertex import ShapeVertex
#import popupcad.algorithms.csg_shapely

if __name__=='__main__':
    exterior = [[0,0],[0,1],[1,2],[2,1],[2,-1],[1,-2],[0,-1]]
    exterior = [tuple(item) for item in exterior]
    exterior2 = [(.5,0),(1,3**.5/2),(1.5,0)]
    a = GenericPoly(exterior,[])
    b = GenericPoly(exterior2,[])

#    aa = pg.GenericPoly([ShapeVertex(item) for item in exterior],[])
#    bb = pg.GenericPoly([ShapeVertex(item) for item in exterior2],[])

#    a.plot()
#    b.plot()
#    A=a.to_shapely()
#    B=b.to_shapely()
#    C = A.difference(B)
#    c=csg_shapely.to_generic(C)
    c = a-b
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
