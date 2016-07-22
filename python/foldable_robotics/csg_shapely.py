# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

import shapely.geometry as sg

def is_collection(item):
    collections = [
        sg.MultiPolygon,
        sg.GeometryCollection,
        sg.MultiLineString,
        sg.multilinestring.MultiLineString,
        sg.MultiPoint]
    iscollection = [isinstance(item, cls) for cls in collections]
    return any(iscollection)
    
def extract_r(item,list_in = None):
    list_in = list_in or []
    if is_collection(item):
        list_in.extend([item3 for item2 in item.geoms for item3 in extract_r(item2,list_in)])
    else:
        list_in.append(item)
    return list_in
    
def condition_shapely_entities(*entities):
    entities = [item for item2 in entities for item in extract_r(item2)]
    entities = [item for item in entities if any([isinstance(item,classitem) for classitem in [sg.Polygon,sg.LineString,sg.Point]])]
    entities = [item for item in entities if not item.is_empty]
#    entities = [item for item in entities if not item.is_valid]
    return entities

def unary_union_safe(*listin):
    '''try to perform a unary union.  if that fails, fall back to iterative union'''
    import shapely
    import shapely.ops as so

    try:
        return so.unary_union(listin)
    except (shapely.geos.TopologicalError, ValueError):
        print('Unary Union Failed.  Falling Back...')
        workinglist = listin[:]
        try:
            result = workinglist.pop(0)
            for item in workinglist:
                try:
                    newresult = result.union(item)
                    result = newresult
                except (shapely.geos.TopologicalError, ValueError):
                    raise
            return result
        except IndexError:
            #            return sg.GeometryCollection()
            raise
