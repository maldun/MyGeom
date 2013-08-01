# MyGeom Module - API for easier Salome geompy usage
# Types.py: Extended Data Types for MyGeom
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

from numpy import array, ndarray, arange
from numpy import float64 as data_type

# For future Versions of salome!
# from salome.geom import geomBuilder
# geompy = geomBuilder.New(salome.myStudy)

# Define help classes for more structured programming
class MyGeomObject(object):
    """
    Base class for all custom geometrical objects
    """
    def __init__(self,geomObject):
        self.geomObject = geomObject

    def addToStudy(self,studyName, father = None):
        """
        Adds Vertex to study and adds
        the name in the study
        """
        
        if father is None:
            geompy.addToStudy(self.getGeomObject(),studyName)
        else:
            my_father = MyGeomObject(father)
            geompy.addToStudyInFahter(my_father.getGeomObject(),self.getGeomObject(),studyName)
        self.studyName = studyName

    def getStudyName(self):
        return self.studyName

    def getGeomObject(self):
        return self.geomObject

    def setGeomObject(self,geom_object):
        self.geomObject = geom_object
    



class MyVertex(MyGeomObject):
    """
    Help class for storing vertices.
    Additionally stores coordinate of
    the Vertex

    """
    
    def __init__(self,x, y = 0.0, z = 0.0):

        if isinstance(x,GEOM._objref_GEOM_Object):
            if x.GetShapeType() == GEOM.VERTEX:
                self.setCoord(geompy.GetPosition(x)[:3])
                self.setGeomObject(x)
            else:
                raise ValueError("Error: This is not a vertex!")
        elif isinstance(x,MyVertex):
            self.setCoord(x.getCoord())
            self.setGeomObject(x.getGeomObject())
        elif isinstance(x,ndarray) or isinstance(x,tuple) or isinstance(x,list):
            if len(x) is 3:
                self.setCoord(data_type(x))
                self.setGeomObject(geompy.MakeVertex(x[0],x[1],x[2]))
            else:
                raise ValueError("Error: Wrong Dimension!")
        else:
            try:
                self.setCoord((x,y,z))
                self.setGeomObject(geompy.MakeVertex(x,y,z))
            except Exception:
                raise ValueError("Error: Wrong data type!")

    def __eq__(self,q):
        """
        Two points are considered equal iff
        the coordinates are the same
        """
        if all(self.getCoord() == q.getCoord()):
            return True
        else:
            return False

    def setCoord(self,coord):
        self.coord = array(coord,dtype=data_type)
        
    def getCoord(self):
        return self.coord

    def __repr__(self):
        """
        Function to print the point as a tuple
        """
        return str(tuple(self.getCoord()))

    def __add__(self,other):
        """
        Arithmetic: Addition of 2 points
        """
        return MyVertex(self.getCoord() + other.getCoord())

    def __sub__(self,other):
        """
        Arithmetic: Subtraction of 2 points
        """
        return MyVertex(self.getCoord() - other.getCoord())

    def __mul__(self,scalar):
        """
        Arithmetic: Multiplication with a scalar
        """
        return MyVertex(self.getCoord()*scalar)

    def __div__(self,scalar):
        """
        Arithmetic: Division by a scalar
        """
        return MyVertex(self.getCoord()/scalar)

class MyLine(MyGeomObject):
    """
    Help class for storing lines
    Holds two instances of MyVertex
    """
    def __init__(self,line_or_point,q = None):
                       
        if isinstance(line_or_point,GEOM._objref_GEOM_Object):
            type = geompy.ShapeIdToType(line_or_point.GetType())
            if type == 'LINE' and q is None:
                subshapes = geompy.SubShapeAll(line_or_point,geompy.ShapeType['VERTEX'])
                line_or_point = subshapes[0]
                q = subshapes[-1]
            elif type == 'LINE' and q is not None:
                raise ValueError("Wrong Type!")

        self.setP(line_or_point)
        self.setQ(q)
        
        self.geomObject = geompy.MakeLineTwoPnt(self.getP().getGeomObject(),self.getQ().getGeomObject())

        
    def getP(self):
        return self.p

    def setP(self,p):
        self.p = MyVertex(p)
        
    def getQ(self):
        return self.q

    def setQ(self,q):
        self.q = MyVertex(q)

    def __eq__(self,other):
        """
        Two Lines are considered to be the same iff they have the same endpoints
        (without order)
        """
        if (self.getP() == other.getP() and self.getQ() == other.getQ()) or (self.getQ() == other.getP() and self.getP() == other.getQ()):
            return True
        else:
            False
# Perhaps deprecate this and replace it by face construction and
# explosion

class MyVector(MyGeomObject):
    """
    Help class for vectors
    """
    def __init__(self,vec_or_point,q = None):
        
        if isinstance(vec_or_point,MyVertex):
            p_type = 'MyVertex'
        elif isinstance(vec_or_point,GEOM._objref_GEOM_Object):
            p_type = geompy.ShapeIdToType(vec_or_point.GetType())
        else:
            raise ValueError("This constructor does not support that option!")

        if isinstance(q,MyVertex):
            q_type = 'MyVertex'
        elif isinstance(q,GEOM._objref_GEOM_Object):
            q_type = geompy.ShapeIdToType(vec_or_point.GetType())
        elif q is None:
            pass
        else:
            raise ValueError("This constructor does not support that option!")

        
        if q is None:
            if p_type == 'MyVertex':
                self.setQ(vec_or_point)
                self.setP(MyVertex(0.0))
            elif p_type == 'POINT':
                self.setQ(MyVertex(vec_or_point))
                self.setP(MyVertex(0.0))
            elif p_type == 'VECTOR':
                subshapes = geompy.SubShapeAll(vec_or_point,geompy.ShapeType['VERTEX'])
                self.setP(subshapes[0])
                self.setQ(subshapes[-1])
            else:
                raise ValueError('Error: Wrong Type!')
        elif q_type == 'POINT': 
            self.setQ(q)
            if p_type == 'MyVertex': 
                self.setP(vec_or_point)
            elif  p_type == 'POINT':
                self.setP(vec_or_point)
            else:
                raise ValueError('Error: Wrong Type!')
        elif q_type == 'MyVertex':
            self.setQ(q)
            if p_type == 'MyVertex': 
                self.setP(vec_or_point)
            elif  p_type == 'POINT':
                self.setP(vec_or_point)
            else:
                raise ValueError('Error: Wrong Type!')
        else:
            raise ValueError('Error: Wrong Type!')

        
        self.geomObject = geompy.MakeVector(self.getP().getGeomObject(),self.getQ().getGeomObject())

        
    def getP(self):
        return self.p

    def setP(self,p):
        self.p = MyVertex(p)
        
 
    def getQ(self):
        return self.q
           
    def setQ(self,q):
        self.q = MyVertex(q)

    def __eq__(self,other):
        """
        Two Vectors are considered to be the same iff they have the same startpoints and endpoints. Thats the only difference between a vector and a line.
        (without order)
        """
        if (self.getP() == other.getP()) and (self.getQ() == other.getQ()):
            return True
        else:
            return False

    def getCoord(self):
        """
        Get the coordinate represention of a vector by the formula
        x = p - q
        """
        return (self.getP()-self.getQ()).getCoord()


class MyWire(MyGeomObject):
    """
    Help class for wires
    """

    def __init__(self,wire_or_edges):
        """
        Init function for wire creation
        """
        if isinstance(wire_or_edges,MyWire):
            self.setGeomObject(wire_or_edges.getGeomObject())
        elif isinstance(wire_or_edges,list) or isinstance(wire_or_edges,tuple):
            self.setGeomObject(geompy.MakeWire(wire_or_edges))
        elif isinstance(wire_or_edges,GEOM._objref_GEOM_Object):
            type = geompy.ShapeIdToType(wire_or_edges.GetType())
            if type == 'WIRE':
                self.setGeomObject(wire_or_edges)
            else:
                raise ValueError("Error: Wrong data type!")
        else:
            raise ValueError("Error: Wrong data type!")
        
class MyFace(MyGeomObject):
    """
    Help class for faces, and face related stuff
    """

    def __init__(self,face,isPlanarFace = True, precision = 5):
        """
        This init is a stub! It will be extended Later!
        Precision : Nr of points to compare
        """

        self._precision = precision

        if isinstance(face,MyFace):
            self.setGeomObject(face.getGeomObject())
        elif isinstance(face,MyWire):
            compound = geompy.MakeFaceWires([face.getGeomObject()],isPlanarFace)
            new_face = geompy.SubShapeAll(compound,geompy.ShapeType["FACE"])[0]
            self.setGeomObject(new_face)
        elif isinstance(face,GEOM._objref_GEOM_Object):
            if face.GetShapeType() == GEOM.FACE:
                self.setGeomObject(face)
            elif face.GetShapeType() == GEOM.WIRE:
                new_face = MyFace(MyWire(face),isPlanarFace)
                self.setGeomObject(new_face.getGeomObject())
            else:
                raise ValueError("Error: Shape is not a Face or Wire!")
        else:
            ValueError("Error: Data type not valid!")

    def changeOrientation(self,make_copy = False):
        """        
        Changes the Orientation of the Face
        
        Parameters
        ----------
        make_copy : bool
                    Indicates if a copy should be made or not. Default is False
        Returns
        -------
        A MyFace or nothing 
        
        Examples
        --------
        
        """
        if make_copy:
            return MyFace(geompy.ChangeOrientation(self.geomObject))
        else:
            self.geomObject = geompy.ChangeOrientation(self.geomObject) 

    def makeVertexOnSurface(self,u,v = None):
        """
        Creates Vertex on given local coordinates
        
        Parameters
        ----------

        u : array, list, tuple or float
        v : None or float

        Returns
        -------

        MyVertex instance which holds the desired point
        """
        
        if v is None:

            if isinstance(u,ndarray) or isinstance(u,list) or isinstance(u,tuple):
                if len(u) is 2:
                    return MyVertex(geompy.MakeVertexOnSurface(self.geomObject,u[0],u[1]))
                else:
                    raise ValueError("Error: List has wrong dimension!")
            else:
                raise ValueError("Error: Wrong data type!")
        else:
            return MyVertex(geompy.MakeVertexOnSurface(self.geomObject,u,v))

    def getNormal(self, p = None):
        """
        Creates the normal vector of the Face and returns it.

        Parameters
        ----------

        p : Point where the normal should be. Given As Vertex or MyVertex

        Returns
        -------

        MyVector instance which holds the normal of the face.
        """
        if p is None:                    
            normal = geompy.GetNormal(self.getGeomObject())
        else:
            my_p = MyVertex(p)
            normal = geompy.GetNormal(self.getGeomObject(),my_p.getGeomObject())

        return MyVector(normal)

    def setPrecision(self,precision):
        self._precision = precision

    def getPrecision(self):
        return self._precision

    def _setParameterListToPrecision(self,precision):
        return arange(0.0,1.0+1.0/precision,1.0/precision).tolist() 
        

    def checkEquality(self,other,nr_points = 0):
        """
        Checks if 2 faces are equal in the sense of the following
        E = F <=> x = y and m(x) = n(y) for all x in E and all y in F,
        where m,n are the normal vector fields of E and F.
        This criterion may be an overestimation, but it makes more sense
        in a discrete setting, since the shape functions are also compared
        indirectly.

        In this implementation only a discrete set of points is compared
        and one normal is checked
        """

        if nr_points is 0:
            nr_points = self.getPrecision()

        # check for higher precision
        other_precision = other.getPrecision()
        if nr_points < other_precision:
            nr_points = other_precision
        

        parameters = self._setParameterListToPrecision(nr_points)
        
        points_self = array([self.makeVertexOnSurface(u,v) for u in parameters for v in parameters])
        points_other = array([other.makeVertexOnSurface(u,v) for u in parameters for v in parameters])
        
        if all(points_self == points_other):
            same = True
        else:
            same = False

        normals_self = self.getNormal()
        normals_other = other.getNormal()
        if normals_self == normals_other and same is True:
            return True
        else:
            return False

    def __eq__(self,other):
        return self.checkEquality(other)

    def __ne__(self,other):
        return not self.checkEquality(other)
        

class MyQuadrangleFromLines(MyFace):
    """
    Help class for Quadrangles built from
    Lines.
    """

    def __init__(self,edges):
        self.geomObject = geompy.MakeFaceWires(
            [edge.geomObject for edge in edges],1)
        self.edges = edges
 

class MyShell(MyGeomObject):
    """
    Help class for shell creation and handling
    """

    def __init__(self,face_list_or_shell):
        """
        creates from a list of faces a shell
        """
        if isinstance(face_list_or_shell,MyShell):
            self.setGeomObject(face_list_or_shell.getGeomObject())  
        elif isinstance(face_list_or_shell,GEOM._objref_GEOM_Object):
            if face_list_or_shell.GetShapeType() == GEOM.SHELL:
                self.setGeomObject(face_list_or_shell)
        elif isinstance(face_list_or_shell,list):
            #To guarantee that we have the correct data type
            my_face_list = [ MyFace(face) for face in face_list_or_shell]
        
            my_face_list = [face.getGeomObject() for face in my_face_list]
            self.geomObject = geompy.MakeShell(my_face_list)
        else:
            raise ValueError("Error: Wrong data type!")

