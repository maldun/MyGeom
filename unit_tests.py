# MyGeom Module - API for easier Salome geompy usage
# unit_tests.py: unit_tests for MyGeom module
#
# Copyright (C) 2013 Stefan Reiterer - stefan.reiterer@magnasteyr.com or maldun.finsterschreck@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA


#!!!! For this test a running Salome Session with test.hdf is needed!!!!

from __future__ import print_function

import salome 
import GEOM
import geompy

from numpy import array, arange
from MyGeom.Types import *
from MyGeom.Tools import *

class MyGeomUnitTester(object):
    """
    Class to test MyGeom classes and methods 
    """

    ###############################
    # Vertex
    ###############################
    def testVertexCreation(self):

        # create by coordinate
        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)

        # Create with Vertex
        vertex2 = MyVertex(vertex1.getGeomObject())

        # Create with Lists
        coords = (0.0,1.0,2.0)
        vertex3 = MyVertex(coords)
        vertex4 = MyVertex(list(coords))
        vertex5 = MyVertex(array(coords))

        print("Test Vertex creation: ")
        print("Vertex0: ", vertex0) # Test correct string representation
        print("Vertex1: ", vertex1.getCoord()) # test get method
        print("Vertex2: ", vertex2)
        print("Vertex3: ", vertex3.getCoord())
        print("Vertex4: ", vertex4.getCoord())
        print("Vertex5: ", vertex5.getCoord())

        try:
            coords = list(coords) + [3.0]
            MyVertex(coords)
        except ValueError:
            print("Correct Error Handling with wrong dimensions.")

    def testVertexComparison(self):

        # create by coordinate
        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)

        # Create with Vertex
        vertex2 = MyVertex(vertex1.getGeomObject())

        print("Test Vertex Comparison: ")
        print("are not the same: ", not vertex0 == vertex1)
        print("are the same: ", vertex2 == vertex1)

    def testVertexArithmetic(self):

        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)
        vertex2 = MyVertex(2.0)

        print("Test addition: ", (vertex0 + vertex1) == vertex1)
        print("Test subtraction: ", (vertex1 - vertex1) == vertex0)
        print("Test multiplication by scalar: ", (vertex1*2) == vertex2)
        print("Test division by scalar: ", (vertex2/2.) == vertex1)

    def testVertexClass(self):
        """
        Tests for Vertex Class
        """

        self.testVertexCreation()
        self.testVertexComparison()
        self.testVertexArithmetic()


    #################################
    # Lines
    #################################

    def testLineConstruction(self):

        # create vertex by coordinate
        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)

        line = MyLine(vertex0,vertex1)

        print("Check Line Construction, First Variant:", vertex0 == line.getP(),vertex1==line.getQ())

        line2 = MyLine(line.getGeomObject())

        print("Check Line Construction, Second Variant:", vertex0 == line2.getP(),vertex1==line2.getQ())
        line3 = MyLine(vertex0.getGeomObject(),vertex1)

        print("Check Line Construction, Third Variant:", vertex0 == line3.getP(),vertex1==line3.getQ())
        
        try:
            MyLine(vertex0)
            MyLine(vertex0.getGeomObject())
        except ValueError:
            print("correct error handling")


    def testLineCompare(self):

        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)
        vertex2 = MyVertex(0.0,1.0,0.0)
        line0 = MyLine(vertex0,vertex1)
        line1 = MyLine(vertex0.getGeomObject(),vertex1.getGeomObject())
        line2 = MyLine(vertex1,vertex2)

        print("Are not the same: ", not line1==line2)
        print("Are the same: ", line0 == line1)

            
    def testLineClass(self):
        """
        tests for Line Class
        """

        self.testLineConstruction()
        self.testLineCompare()

    def testVectorConstruction(self):

        # create vertex by coordinate
        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)

        vec = MyVector(vertex0,vertex1)

        print("Check Vector Construction, First Variant:", vertex0 == vec.getP(),vertex1==vec.getQ())

        vec2 = MyVector(vec.getGeomObject())

        print("Check Vector Construction, Second Variant:", vertex0 == vec2.getP(),vertex1==vec2.getQ())
        vec3 = MyVector(vertex0.getGeomObject(),vertex1)

        print("Check Vector Construction, Third Variant:", vertex0 == vec3.getP(),vertex1==vec3.getQ())
        
        try:
            line = MyLine(vertex0,vertex1)
            MyVector(line)
            MyVector(vertex0.getGeomObject(),line)
        except ValueError:
            print("correct error handling")

    def testVectorCompare(self):

        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)
        vertex2 = MyVertex(0.0,1.0,0.0)
        vec0 = MyVector(vertex0,vertex1)
        vec1 = MyVector(vertex0.getGeomObject(),vertex1.getGeomObject())
        vec2 = MyVector(vertex1,vertex2)
        vec3 = MyVector(vertex1,vertex0)

        print("Are not the same: ", vec1!=vec2,not vec0 == vec3)
        print("Are the same: ", vec0 == vec1)
        

    def testVectorClass(self):
        """
        tests for Vector  Class
        """

        self.testVectorConstruction()
        self.testVectorCompare()




    #################################
    # Faces
    #################################

    def testFaceCreation(self):
        
        salome_face1 = salome.myStudy.FindObject("test_face").GetObject()
        face1 = MyFace(salome_face1)

        #print("Test Face creation: ", face1.getGeomObject() == salome_face1) 


    def testMakeVertexOnSurface(self):

        salome_face1 = salome.myStudy.FindObject("test_face").GetObject()
        face1 = MyFace(salome_face1)

        vertex1 = face1.makeVertexOnSurface([0.,0.])
        vertex2 = face1.makeVertexOnSurface((0.5,0.5))
        vertex3 = face1.makeVertexOnSurface(1.,1.)
        
        vertex1_check = MyVertex(-1.,-1.)
        vertex2_check = MyVertex(0.)
        vertex3_check = MyVertex(1.0,1.0)


        print("Test makeVertexOnSurface creation: ",vertex1 == vertex1_check,\
                  vertex2 == vertex2_check,vertex3 == vertex3_check) 


    def testFaceClass(self):
        """
        tests for faces
        """
        self.testFaceCreation()
        self.testMakeVertexOnSurface()


    def testCreateLocalCoordinates(self):
        
        salome_face1 = salome.myStudy.FindObject("test_face").GetObject()
        face1 = MyFace(salome_face1)
        
        coord_u = arange(0,1.25,0.25)
        coord_v = coord_u

        vertices = create_local_coordinates(face1,coord_u,coord_v)
        
        string = ""
        for i in range(5):
            for j in range(5):
                string += str(vertices[i][j])

            string += "\n"

        print(string)
        

    def testTools(self):
        """
        Test given tools
        """
        self.testCreateLocalCoordinates()
        

    ######################################################
    #
    # Execution
    # 
    #####################################################
    def __init__(self):

        self.testVertexClass()
        self.testLineClass()
        self.testVectorClass()
        self.testFaceClass()
        self.testTools()


tester = MyGeomUnitTester()
