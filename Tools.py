# MyGeom Module - API for easier Salome geompy usage
# Tools.py: Tool functions for MyGeom module
#
# Copyright (C) 2013  Stefan Reiterer - stefan.reiterer@magnasteyr.com or maldun.finsterschreck@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from __future__ import print_function

import salome
import geompy
import GEOM

from MyGeom.Types import *

from numpy import array, ndarray
from numpy import float64 as data_type

# For future Versions of salome!
# from salome.geom import geomBuilder
# geompy = geomBuilder.New(salome.myStudy)

def add_list2study(liste,string, startindex = 0):
    """
    Function to add list of geom objects to a study,
    with numbered name
    """
    i = startindex
    for object in liste:
        object.addToStudy(string + str(i))
        i+=1

def explode_sub_shape(my_geom_object,type,add_to_study = True):
    """
    Explode Sub Shapes of certain Type. If add_to_study is
    True add all objects to study

    Parameters
    ----------

    my_geom_object : Objcet of MyGeomObjectType
    type : String with type description
    add_to_study : If Objects should be added to study. True when yes, else False
    
    Examples
    --------
    faces = explode_sub_shape(shell,"FACE",add_to_study = False)
    """
    geom_object = my_geom_object.geomObject
    subshapes = geompy.SubShapeAll(geom_object,geompy.ShapeType[type])
    if add_to_study:
        for sub in subshapes:
            name = geompy.SubShapeName(sub,geom_object)
            geompy.addToStudyInFather(geom_object,sub,name)

    return subshapes

def create_local_coordinates(face, coord_u, coord_v,my_geom = True):
    """
    Creates MyVertex list of a local coordinate system for a given degree.
    
    Parameters
    ----------
    face : GEOM.FACE or MyFace
           Face from Salome or MyFace 
        
    coord_u : array, one dimensional
              local u coordinates
    
    coord_v : array, one dimensional

    Returns
    -------
    vertices : list of vertices, shape is the same as the input array

    Examples
    --------
    """

    if not isinstance(face,MyFace):
        face = MyFace(face)

    make_vertex = face.makeVertexOnSurface
    if my_geom:
        vertices = [[make_vertex(u,v) for v in coord_v] for u in coord_u]
    else:
        vertices = [[make_vertex(u,v).getGeomObject() for v in coord_v] for u in coord_u]

    return vertices

def create_face_by_points(points,isPlanarFace = True):
    """
    Takes a set of points and creates a face with it
    """
    # Create wires in u direction
    wires = [geompy.MakeInterpol(coords) for coords in points]

    # Transpose list 
    points2 = array(points).transpose()
    points2 = points2.tolist()

    # Create wires in v direction
    wires += [geompy.MakeInterpol(coords) for coords in points2]
    
    face = MyGeomObject(geompy.MakeFaceWires(wires,isPlanarFace))
    face = explode_sub_shape(face,"FACE")[0]
    return MyFace(face)

def inner_product(vector1, vector2):
    """
    Calculates the inner product of two vectors.
    """
    
    if isinstance(vector1,MyVertex) or isinstance(vector1,MyVector):
        vec1 = vector1.getCoord()
    else:
        raise ValueError("Error: Wrong data type!")

    if isinstance(vector2,MyVertex) or isinstance(vector1,MyVector):
        vec2 = vector2.getCoord()
    else:
        raise ValueError("Error: Wrong data type!")

    from numpy import dot
    return dot(vec1,vec2)

def find_object(descriptive_string):
    """
    Help function to find object in a study
    """
    return salome.myStudy.FindObject(descriptive_string).GetObject()

def get_min_distance(object1,object2):
    """
    Help function to get minimal distance between 2 objects
    """
    if isinstance(object1,MyGeomObject):
        object_1 = object1.getGeomObject()
    else:
        object_1 = object1

    if isinstance(object2,MyGeomObject):
        object_2 = object2.getGeomObject()
    else:
        object_2 = object2


    return geompy.MinDistance(object_1,object_2)

def get_list_by_name(name,alternative_name = None, info = False):
    """
    Help function that searches for all objects in a study with a certain name.
    If the object with this name is not found it tries to search for an alternative name.
    """
    liste = []
    counter = 0
    if alternative_name is None: # No alternative no info
        info = False

    if info: 
        info_liste = []

    while True:
        counter += 1
        try:
            dired_object = find_object(name + str(counter))
            liste.append(dired_object)
            if info:
                info_liste.append(0)

        except AttributeError:
            if alternative_name is None:
                break
            else:
                try:
                    dired_object = find_object(alternative_name + str(counter))
                    liste.append(dired_object)
                    if info:
                        info_liste.append(1)
                except AttributeError:
                    break

    if info:
        return liste, info_liste
    else:
        return liste
