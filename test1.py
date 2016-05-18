import matplotlib.pyplot as plt
from genericshapes import GenericPoly

if __name__=='__main__':
    exterior = [[0,0],[0,1],[1,2],[2,1],[2,-1],[1,-2],[0,-1]]
    exterior = [tuple(item) for item in exterior]
    exterior2 = [(.5,0),(1,3**.5/2),(1.5,0)]
    a = GenericPoly(exterior,[])
    b = GenericPoly(exterior2,[])
#    a.plot()
#    b.plot()
#    A=a.to_shapely()
#    B=b.to_shapely()
#    C = A.difference(B)
#    c=csg_shapely.to_generic(C)
    c = a-b
    
#    plt.figure()
#    c.plot()
    raise AttributeError