
from __future__ import print_function
    
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

        # Create with Vertxe
        vertex2 = MyVertex(vertex1.getGeomObject())

        print("Test Vertex creation: ")
        print("Vertex0: ", vertex0.getCoord())
        print("Vertex1: ", vertex1.getCoord())
        print("Vertex2: ", vertex2.getCoord())

    def testVertexComparison(self):

        # create by coordinate
        vertex0 = MyVertex(0.0)
        vertex1 = MyVertex(1.0)

        # Create with Vertex
        vertex2 = MyVertex(vertex1.getGeomObject())

        print("Test Vertex Comparison: ")
        print("are not the same: ", not vertex0 == vertex1)
        print("are the same: ", vertex2 == vertex1)

    def testVertexClass(self):
        """
        Tests for Vertex Class
        """

        self.testVertexCreation()
        self.testVertexComparison()


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
 
    def __init__(self):

        self.testVertexClass()
        self.testLineClass()
        self.testVectorClass()

tester = MyGeomUnitTester()
