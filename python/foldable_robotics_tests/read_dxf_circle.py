import foldable_robotics.dxf as dxf
import shapely.geometry as sg

circles = dxf.read_circles('./python/foldable_robotics_tests/circle.dxf')
circles2 = dxf.read_circles('./python/foldable_robotics_tests/circle2.dxf')

diff = sg.Polygon()
for c in circles:
    diff |= sg.Point(list(c[0])[0:2]).buffer(c[1],5)
for c in circles2:
    diff ^= sg.Point(list(c[0])[0:2]).buffer(c[1],5)
assert diff.area == 0, 'Should be the same but area difference is {}'.format(diff.area)
