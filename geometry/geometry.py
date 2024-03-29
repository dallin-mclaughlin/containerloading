from core.attribute import Attribute
import numpy

class Geometry(object):

    def __init__(self):

        # store attribute objects,
        #indexed by name of associated variable in shader.
        #Shader variable assocations set up later and stored in vertex array object in Mesh.
        self.attributes = {}

        #number of vertices
        self.vertexCount = None
    
    def addAttribute(self, dataType, variableName, data):
        self.attributes[variableName] = Attribute(dataType, data)

    def countVertices(self):
        #number of vertices may be calculated from the length of any Attribute object's array of data
        attrib = list(self.attributes.values())[0]
        self.vertexCount = len(attrib.data)

    #transform the data in an attribute using a matrix
    def applyMatrix(self, matrix, variableName="vertexPosition"):
        oldPositionData = self.attributes[variableName].data
        newPositionData = []

        for oldPos in oldPositionData:
            #avoid changing list references
            newPos = oldPos.copy()
            #add homogenous fourth coordinate
            newPos.append(1)
            #multiply by matrix
            newPos = matrix @ newPos
            #remove homogenous coordinate
            newPos = list(newPos[0:3])
            #add to new data list
            newPositionData.append(newPos)

        self.attributes[variableName].data = newPositionData

        #extract the rotation submatrix
        rotationMatrix = numpy.array([  matrix[0][0:3],
                                        matrix[1][0:3],
                                        matrix[2][0:3]])
        if "vertexNormal" in self.attributes.keys():
            oldVertexNormalData = self.attributes["vertexNormal"].data
            newVertexNormalData = []
            for oldNormal in oldVertexNormalData:
                newNormal = oldNormal.copy()
                newNormal = rotationMatrix @ newNormal
                newVertexNormalData.append(newNormal)
            self.attributes["vertexNormal"].data = newVertexNormalData

        if "faceNormal" in self.attributes.keys():
            oldFaceNormalData = self.attributes["faceNormal"].data
            newFaceNormalData = []
            for oldNormal in oldFaceNormalData:
                newNormal = oldNormal.copy()
                newNormal = rotationMatrix @ newNormal
                newFaceNormalData.append(newNormal)
            self.attributes["faceNormal"].data = newFaceNormalData
        #new data must be uploaded
        self.attributes[variableName].uploadData()

    #merge data from attributes of other geometry into this object
    #requires both geometries to have attributes with same names
    def merge(self, otherGeometry):

        for variableName, attributeObject in self.attributes.items():
            attributeObject.data += otherGeometry.attributes[variableName].data
            #new data must be uploaded
            attributeObject.uploadData()

        #update the number of vertices
        self.countVertices()