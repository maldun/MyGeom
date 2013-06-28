
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
    def testLineClass(self):
        """
        tests for Line Class
        """

        self.testLineConstruction()
        
    def __init__(self):

        self.testVertexClass()
        self.testLineClass()

tester = MyGeomUnitTester()
