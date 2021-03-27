# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 13:06:11 2017

@author: danaukes
"""

import numpy
import shapely.geometry as sg

svg_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   width="{width:f}"
   height="{height:f}"
   viewBox="-0.04 -0.04 1.08 1.08"
   preserveAspectRatio="xMinYMin meet"
   version="1.1"
   id="svg1015">
  <metadata
     id="metadata1021">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs1019" />
  <g
     transform="matrix(1,0,0,-1,0,1.0)"
     id="g1013">
    {paths}
  </g>
</svg>'''

style_template ='''
opacity:1;
fill:{2};
fill-opacity:{1};
fill-rule:evenodd;
stroke:#808080;
stroke-width:{0}px;
stroke-linecap:round;
stroke-linejoin:round;
stroke-opacity:1
'''
style_template=style_template.replace('\n','')

path_template='    <path d="{paths}" style="{style}"/>'

def color_tuple_to_hex(tuple_in):
    string = '#'
    for item in tuple_in:
        val=int(item*255)
        string+='{:02x}'.format(val)
    return string

def loop_string(loop):
    loop = loop.tolist()
    c1 = loop.pop(0)
    loop_string = 'M '+'{0:f} {1:f}'.format(*c1)+ ' L ' +(' L '.join([('{0:f} {1:f}'.format(x,y)) for x,y in loop]))+' z'
    return loop_string 

def line_string(loop):
    loop = loop.tolist()
    c1 = loop.pop(0)
    loop_string = 'M '+'{0:f} {1:f}'.format(*c1)+ ' L ' +(' L '.join([('{0:f} {1:f}'.format(x,y)) for x,y in loop]))
    return loop_string 

def make_svg_path(geom,line_width,fill_opacity,fill_color):
    if isinstance(geom,sg.Polygon):

        exterior = list(geom.exterior.coords)
        interiors = [list(interior.coords) for interior in geom.interiors]

        loops = [exterior]+interiors
        loops = [numpy.array(loop) for loop in loops]

        paths = [loop_string(loop) for loop in loops]
        paths2 = ' '.join(paths)    

        path_string = path_template.format(paths = paths2, style=style_template.format(line_width,fill_opacity,fill_color))  

    elif isinstance(geom,sg.LineString):
        exterior = numpy.array(geom.coords)
        path = line_string(exterior)

        path_string = path_template.format(paths = path, style=style_template.format(line_width,0,fill_color))  

    else:
        path_string=''
        
    return path_string

def make_svg(paths,w,h):
    '''create a svg representation'''
    svg_string = svg_template.format(paths = paths, width=w, height = h, width_i=int(w), height_i = int(h))    
    return svg_string
    
if __name__=='__main__':    
    pass
#    shape = JupyterSupport([[(0.,0),(10,0),(10,10)],[(1.5,1),(9.5,1),(9.5,9)]])
#    shape._repr_svg_()
#    print(shape)    
    