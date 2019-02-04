# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 20:59:36 2018

@author: danaukes
"""

import foldable_robotics_tests.manufacturing_example1
import foldable_robotics.pdf
d = foldable_robotics_tests.manufacturing_example1.worst_case_supported_design.translate(10,10)[-1]
d=d.scale(foldable_robotics.pdf.ppi,foldable_robotics.pdf.ppi)
p=foldable_robotics.pdf.Page('test.pdf')
for item in d.get_paths():
    p.draw_poly(item)
p.close()
