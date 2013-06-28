import salome
import geompy
import GEOM

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
    Additionally stores coordinate of
    the Vertex

    """
    
    def __init__(self,x, y = 0.0, z = 0.0):

        if isinstance(x,GEOM._objref_GEOM_Object):
            if x.GetShapeType() == GEOM.VERTEX:
                self.coord = x.GetPosition[:3]
                self.geomObject = x
            else:
                raise ValueError("Error: This is no vertex!")

        else:
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



class MyLine(MyGeomObject):
    """
    Help class for storing edges
    Holds two instances of MyVertex
    """
    def __init__(self,p,q):

        if p == q: 
            raise ValueError("Error: Line is a single point!")
        
        self.geomObject = geompy.MakeLine(p.geomObject,q.geomObject)
        self.p = p
        self.q = q

    def __eq__(self,other):
        """
        Two Lines are considered to be the same iff they have the same endpoints
        (without order)
        """
        if (self.p == other.p and self.q == other.q) or (self.q == other.p and self.p == other.q):
            return True
        else:
            False
# Perhaps deprecate this and replace it by face construction and
# explosion

class MyVector(MyLine):
    """
    Help class for vectors
    """
    def __init__(self,vec_or_point,p = None):
        
        if isinstance(vec_or_point,MyVertex):
            if p is None:
                self.p = MyVertex(0.0,0.0,0.0)
            elif isinstance(p,MyVertex):
                self.p = p
            else:
                raise ValueError("This constructor does not support that option!")
            self.q = vec_or_point
            self.geomObject = \
                  geompy.MakeVector(self.p.geomObject,self.q.geomObject)
        
        elif isinstance(vec_or_point,GEOM._objref_GEOM_Object):
            type = geompy.ShapeIdToType(vec_or_point.GetType())
            if type == 'VECTOR':
                self.geomObject = vec_or_point
            elif type == 'POINT':
                pass
            
            

    def __eq__(self,other):
        """
        Two Vectors are considered to be the same iff they have the same startpoints and endpoints. Thats the only difference between a vector and a line.
        (without order)
        """
        if (self.p == other.p and self.q == other.q):
            return True
        else:
            False



class MyFace(MyGeomObject):
    """
    Help class for faces, and face related stuff
    """

    def __init__(self,face):

        if face.GetShapeType() == GEOM.FACE:
            self.face = face
        else:
            raise ValueError("Error: Shape is not a Face!")

    def ChangeOrientation(self):
        pass

        

class MyQuadrangleFromLines(MyGeomObject):
    """
    Help class for Quadrangles built from
    Lines.
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
