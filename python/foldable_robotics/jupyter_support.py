# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 13:06:11 2017

@author: danaukes
"""

import numpy
import shapely.geometry as sg

path_template = '''M {path} Z'''

svg_template = '''
<svg width="{width:f}" height="{height:f}">
{paths}</svg>
'''    

path_template_outer='    <path d="{paths}" style="{style}"/>'


def svg_style(linewidth,fill_rule=1,fill_color='#00FF00'):
    '''create the style string for svg'''
    
    #fill = 'fill:none'
    fill = 'fill:{}'.format(fill_color)
    fill_opacity = 'fill-opacity:{}'.format(fill_rule)
    fill_rule = 'fill-rule:evenodd'
    stroke = 'stroke:#808080'
    stroke_width = 'stroke-width:{0}px'.format(linewidth)
    stroke_linecap = 'stroke-linecap:round'
    stroke_linejoin = 'stroke-linejoin:round'
    stroke_opacity = 'stroke-opacity:1'
    style_list = [fill,fill_opacity,fill_rule,stroke,stroke_width,stroke_linecap,stroke_linejoin,stroke_opacity]
    style = ';'.join(style_list)
    return style

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

def make_svg_path(geom,linewidth,fill_color):
    if isinstance(geom,sg.Polygon):
        exterior = list(geom.exterior.coords)
        interiors = [list(interior.coords) for interior in geom.interiors]
        loops = [exterior]+interiors
        loops = [numpy.array(loop) for loop in loops]

        paths = [loop_string(loop) for loop in loops]
        paths2 = ' '.join(paths)    

        path_string = path_template_outer.format(paths = paths2, style=svg_style(linewidth=linewidth,fill_rule=1,fill_color=fill_color))  

    elif isinstance(geom,sg.LineString):
        exterior = numpy.array(geom.coords)
        path = line_string(exterior)

        path_string = path_template_outer.format(paths = path, style=svg_style(linewidth=linewidth,fill_rule=0,fill_color=fill_color))  
    else:
        path_string=''
        
    return path_string

def make_svg(paths,w,h):
    '''create a svg representation'''
    svg_string = svg_template.format(paths = paths, width=w, height = h, width_i=int(w), height_i = int(h))    
    return svg_string

def make_svg_old(loops,linewidth):
    '''create a svg representation'''
    loops = [numpy.array(loop) for loop in loops]
    
    all_points = numpy.vstack(loops)
    
    #mirror along y
    loops = [item *numpy.array([1,-1]) for item in loops]
    all_points *= numpy.array([1,-1])

    #shift minimum point to 0,0
    shift = all_points.min(0)
    loops = [loop-shift for loop in loops]
    all_points -= shift
    #find the dimensions of the shape
    dim = all_points.max(0)-all_points.min(0)
    
    #calculate the scaling according to drawing 100 pixels tall
    scaling = 100/dim[1]
    
    #scale the dimensions and exterior by the scaling factor
    dim*=scaling
    loops= [loop*scaling for loop in loops]
    
    #shift the exterior and dimensions by the width of the line
    loops = [loop + linewidth/2 for loop in loops]
    dim+=linewidth
    
    #create the path string
    
    paths = [loop_string(loop) for loop in loops]
    w = dim[0]
    h = dim[1]

    paths2 = ' '.join(paths)    
    #create the svg string
    path_string = path_template_outer.format(paths = paths2, style=svg_style(linewidth=linewidth))  
    svg_string = svg_template.format(paths = path_string, width=w, height = h, width_i=int(w), height_i = int(h))
    return svg_string
        

    
    
    
    
if __name__=='__main__':    
    shape = JupyterSupport([[(0.,0),(10,0),(10,10)],[(1.5,1),(9.5,1),(9.5,9)]])
    shape._repr_svg_()
    print(shape)    