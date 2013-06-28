import salome
import geompy

# Define help classes for more structured programming
class MyGeomObject(object):
    """
    Base class for all custom geometrical objects
    """
    def __init__(self,geomObject):
        self.geomObject = geomObject

    def addToStudy(self,studyName):
        """
        Adds Vertex to study and adds
        the name in the study
        """
        geompy.addToStudy(self.geomObject,studyName)
        self.studyName = studyName

    def getStudyName(self):
        return self.studyName
    



class MyVertex(MyGeomObject):
    """
    Help class for storing vertices.
    Additionally stores coordinat of
    the Vertex

    """
    
    def __init__(self,x,y,z):
        self.coord = (x,y,z)
        self.geomObject = geompy.MakeVertex(x,y,z)

    def __eq__(self,q):
        """
        Two points are considered equal iff
        the coordinates are the same
        """
        if self.coord == q.coord:
            return True
        else:
            return False



class MyEdge(MyGeomObject):
    """
    Help class for storing edges
    Holds two instances of MyVertex
    """
    def __init__(self,p,q):

        if p == q: 
            raise ValueError("Error: Edge is a single point!")
        
        self.geomObject = geompy.MakeEdge(p.geomObject,q.geomObject)
        self.p = p
        self.q = q

    def __eq__(self,other):
        """
        Two Edges are considered to be the same iff they have the same endpoints
        (without order)
        """
        if (self.p == other.p and self.q == other.q) or (self.q == other.p and self.p == other.q):
            return True
        else:
            False
# Perhaps deprecate this and replace it by face construction and
# explosion
 
class MyQuadrangleFromEdges(MyGeomObject):
    """
    Help class for Quadrangles built from
    Edges.
    """

    def __init__(self,edges):
        self.geomObject = geompy.MakeFaceWires(
            [edge.geomObject for edge in edges],1)
        self.edges = edges
 
def addListToStudy(liste,string):
    """
    Function to add list of geom objects to a study,
    with numbered name
    """
    i = 0
    for object in liste:
        object.addToStudy(string + str(i))
        i+=1

def ExplodeSubShape(my_geom_object,type):
    """
    Explode Sub Shapes of certain Type
    """
    geom_object = my_geom_object.geomObject
    subshapes = geompy.SubShapeAll(geom_object,geompy.ShapeType[type])
    for sub in subshapes:
        name = geompy.SubShapeName(sub,geom_object)
        geompy.addToStudyInFather(geom_object,sub,name)
