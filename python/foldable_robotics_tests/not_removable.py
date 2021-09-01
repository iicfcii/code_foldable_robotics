from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import foldable_robotics.manufacturing as mfg
import shapely.geometry as sg
import matplotlib.pyplot as plt

# Generate a sample device
w = 40 # square device width
lw = 2 # cut width
is_adhesive = [False,True,False]

device = Layer(sg.Polygon([(w/2,w/2),(w/2,-w/2),(-w/2,-w/2),(-w/2,w/2)]))
device = device.to_laminate(3)

slot_r = sg.LineString([(w/4,w),(w/4,-w)])
slot_r = Layer(slot_r.buffer(lw, cap_style=sg.CAP_STYLE.square))

slot_l = sg.LineString([(-w/4,w),(-w/4,-w)])
slot_l = Layer(slot_l.buffer(lw, cap_style=sg.CAP_STYLE.square))

device[2] = device[2] - slot_r - slot_l
device[1] = device[1] - slot_l

# For this device, the removable material upward can only be the left slot on the top layer.
# The right slot can not be removed because it is adhered to the second adhesive layer.
# The left slot on the middle layer can not be removed because it is adhered to the first layer.
# The left slot on the top layer is removable because the second layer will be cut out during individual layer cut.
device.plot_layers()
nru = mfg.not_removable_up(device,is_adhesive)
nru.plot_layers()
plt.show(block=True)

# Similar for removable downward
device_d = Layer(sg.Polygon([(w/2,w/2),(w/2,-w/2),(-w/2,-w/2),(-w/2,w/2)]))
device_d = device_d.to_laminate(3)
device_d[0] = device_d[0] - slot_r - slot_l
device_d[1] = device_d[1] - slot_l

device_d.plot_layers()
nrd = mfg.not_removable_down(device_d,is_adhesive)
nrd.plot_layers()
plt.show(block=True)
