from tkinter import Y
import pygame
from numpy.linalg import norm
from numpy import dot
import numpy
from math import pi
from core.mesh import Mesh
from extras.axesHelper import AxesHelper

class MouseSelector(object):

    def __init__(self, camera):
        self.camera = camera

        self.resetStackPositions = False
        self.previouslySelectedStack = None

        self.worldSpaceDirection = None

        self.hoveredObject = None

        #the stack
        self.selectedStack= None
        #the carton
        self.selectedCarton = None

        self.BUTTON_MOUSE_LEFT = 1
        self.BUTTON_MOUSE_RIGHT = 3

    def update(self, container, inputObject):
        if self.selectedStack is None:
            self.hoverNearestStack(container, inputObject)
            self.selectHoveringStack(inputObject)
        else :
            self.hoverNearestCarton(self.selectedStack, inputObject)
            self.selectHoveringCarton(inputObject)

    def getWorldSpaceDirection(self, inputObject):
        mousePos = inputObject.getMousePos()
        screenCoordinates = pygame.display.get_surface().get_size()
        camera = self.camera
        clipSpaceCoords = [mousePos[0]*2/screenCoordinates[0]-1, 
                -mousePos[1]*2/screenCoordinates[1]+1, -1, 1]
        viewSpaceCoords = camera.getInverseProjectionMatrix() @ clipSpaceCoords
        viewSpaceCoords = [viewSpaceCoords[0], viewSpaceCoords[1], -1, 0]
        worldSpaceCoords = camera.getInverseViewMatrix() @ viewSpaceCoords
        worldSpaceCoords = [worldSpaceCoords[0], worldSpaceCoords[1], worldSpaceCoords[2]]
        worldSpaceNorm = norm(worldSpaceCoords)
        self.worldSpaceDirection = worldSpaceCoords/worldSpaceNorm
        
        return self.worldSpaceDirection

    def hoverNearestStack(self, parentObject, inputObject):
        camera = self.camera
        directionVector = self.getWorldSpaceDirection(inputObject)
        descendentList = parentObject.children
        meshFilter = lambda x : isinstance(x, Mesh)
        meshList = list(filter(meshFilter, descendentList))

        intersectList = []

        smallestDistance = 1000

        hoveredMesh = None

        for mesh in meshList:

            #will only need two intersections
            intersectionCount = 0

            if "faceNormal" not in mesh.geometry.attributes.keys():
                continue

            worldPosition = mesh.getWorldPosition()

            faceNormalData = mesh.geometry.attributes["faceNormal"].data
            positionData = mesh.geometry.attributes["vertexPosition"].data

            P0,P1,P2,P3 = positionData[6],positionData[1],positionData[11],positionData[2]
            P4,P5,P6,P7 = positionData[7],positionData[0],positionData[8],positionData[5]

            #+x
            positiveXNormal = faceNormalData[0]
            positiveXVertices = [P7] + [P3] + [P5] + [P1]
            #-x
            negativeXNormal = faceNormalData[6]
            negativeXVertices = [P6] + [P4] + [P2] + [P0]
            #+y
            positiveYNormal = faceNormalData[12]
            positiveYVertices = [P6] + [P7] + [P2] + [P3]
            #-y
            negativeYNormal = faceNormalData[18]
            negativeYVertices = [P4] + [P5] + [P1] + [P0]
            #+z
            positiveZNormal = faceNormalData[24]
            positiveZVertices = [P6] + [P7] + [P4] + [P5]
            #-z
            negativeZNormal = faceNormalData[30]
            negativeZVertices = [P2] + [P3] + [P0] + [P1]

            normals = [positiveXNormal, negativeXNormal, positiveYNormal, 
                        negativeYNormal, positiveZNormal, negativeZNormal]
            vertices = [positiveXVertices, negativeXVertices, positiveYVertices, 
                        negativeYVertices, positiveZVertices, negativeZVertices]
            
            for i in range(len(normals)):
                if self.intersectPlane(directionVector, camera, worldPosition, normals[i], 
                                        vertices[i]):
                    intersectionCount += 1
                if intersectionCount >= 2:
                    intersectList.append(mesh)
                    break

        for mesh in intersectList:
            differenceVector = numpy.add(mesh.getWorldPosition(),
                                        numpy.negative(camera.getWorldPosition()))
            distanceFromCameraToMesh = norm(differenceVector)
            
            if distanceFromCameraToMesh < smallestDistance:
                smallestDistance = distanceFromCameraToMesh
                hoveredMesh = mesh

        #do something to the previously selected object (e.g. no highlighting)
        if hoveredMesh != self.hoveredObject:
            self.makeInvisible(self.hoveredObject)

        self.hoveredObject = hoveredMesh

        #Only show hovered when not dragging mouse after click
        if(self.hoveredObject != None and not inputObject.isKeyPressed(self.BUTTON_MOUSE_LEFT)):
            self.makeVisible(self.hoveredObject)

    #works for box objects
    #need to make sure that the individual objects within the scene have different geometry
    #classes so that when one geometry is selected or hovered all of the geometries get 
    #hovered or selected simultaneously
    def hoverNearestCarton(self, parentObject, inputObject):
        camera = self.camera
        directionVector = self.getWorldSpaceDirection(inputObject)
        descendentList = parentObject.children
        meshFilter = lambda x : isinstance(x, Mesh)
        meshList = list(filter(meshFilter, descendentList))

        intersectList = []

        smallestDistance = 1000

        hoveredMesh = None

        for mesh in meshList:

            if not mesh.visible:
                continue
            #will only need two intersections
            intersectionCount = 0

            if "faceNormal" not in mesh.geometry.attributes.keys():
                continue

            worldPosition = mesh.getWorldPosition()

            faceNormalData = mesh.geometry.attributes["faceNormal"].data
            positionData = mesh.geometry.attributes["vertexPosition"].data

            P0,P1,P2,P3 = positionData[6],positionData[1],positionData[11],positionData[2]
            P4,P5,P6,P7 = positionData[7],positionData[0],positionData[8],positionData[5]

            #+x
            positiveXNormal = faceNormalData[0]
            positiveXVertices = [P7] + [P3] + [P5] + [P1]
            #-x
            negativeXNormal = faceNormalData[6]
            negativeXVertices = [P6] + [P4] + [P2] + [P0]
            #+y
            positiveYNormal = faceNormalData[12]
            positiveYVertices = [P6] + [P7] + [P2] + [P3]
            #-y
            negativeYNormal = faceNormalData[18]
            negativeYVertices = [P4] + [P5] + [P1] + [P0]
            #+z
            positiveZNormal = faceNormalData[24]
            positiveZVertices = [P6] + [P7] + [P4] + [P5]
            #-z
            negativeZNormal = faceNormalData[30]
            negativeZVertices = [P2] + [P3] + [P0] + [P1]

            normals = [positiveXNormal, negativeXNormal, positiveYNormal, 
                        negativeYNormal, positiveZNormal, negativeZNormal]
            vertices = [positiveXVertices, negativeXVertices, positiveYVertices, 
                        negativeYVertices, positiveZVertices, negativeZVertices]
            
            for i in range(len(normals)):
                if self.intersectPlane(directionVector, camera, worldPosition, normals[i], 
                                        vertices[i]):
                    intersectionCount += 1
                if intersectionCount >= 2:
                    intersectList.append(mesh)
                    break

        for mesh in intersectList:
            differenceVector = numpy.add(mesh.getWorldPosition(),
                                        numpy.negative(camera.getWorldPosition()))
            distanceFromCameraToMesh = norm(differenceVector)
            
            if distanceFromCameraToMesh < smallestDistance:
                smallestDistance = distanceFromCameraToMesh
                hoveredMesh = mesh

        #do something to the previously selected object (e.g. no highlighting)
        if (hoveredMesh != self.hoveredObject and self.hoveredObject != None and 
                self.selectedCarton != self.hoveredObject):
            self.removeHoverEffect(self.hoveredObject)

        self.hoveredObject = hoveredMesh

        if(self.hoveredObject != None and not inputObject.isKeyPressed(self.BUTTON_MOUSE_LEFT)):
            self.addHoverEffect(self.hoveredObject)

    def intersectPlane(self, directionVector, camera, worldPosition, faceNormal, vertexPoints):
        cameraPos = camera.getWorldPosition()
        denominator = dot(directionVector, faceNormal)
        if denominator == 0:
            return False
        #Ax + By + Cz = d
        d = dot(faceNormal, numpy.add(worldPosition, vertexPoints[0]))
        numerator = d - dot(faceNormal, cameraPos)
        t = numerator / denominator
        if t < 0:
            return False
        intersectionPoint = numpy.add(t * directionVector, cameraPos)

        minX = min(vertexPoints[0][0]+worldPosition[0], vertexPoints[1][0]+worldPosition[0], 
                    vertexPoints[2][0]+worldPosition[0], vertexPoints[3][0]+worldPosition[0])
        maxX = max(vertexPoints[0][0]+worldPosition[0], vertexPoints[1][0]+worldPosition[0], 
                    vertexPoints[2][0]+worldPosition[0], vertexPoints[3][0]+worldPosition[0])
        minY = min(vertexPoints[0][1]+worldPosition[1], vertexPoints[1][1]+worldPosition[1], 
                    vertexPoints[2][1]+worldPosition[1], vertexPoints[3][1]+worldPosition[1])
        maxY = max(vertexPoints[0][1]+worldPosition[1], vertexPoints[1][1]+worldPosition[1], 
                    vertexPoints[2][1]+worldPosition[1], vertexPoints[3][1]+worldPosition[1])
        minZ = min(vertexPoints[0][2]+worldPosition[2], vertexPoints[1][2]+worldPosition[2], 
                    vertexPoints[2][2]+worldPosition[2], vertexPoints[3][2]+worldPosition[2])
        maxZ = max(vertexPoints[0][2]+worldPosition[2], vertexPoints[1][2]+worldPosition[2], 
                    vertexPoints[2][2]+worldPosition[2], vertexPoints[3][2]+worldPosition[2])

        offset = 0.001

        intersect = (self.betweenMinMax(intersectionPoint[0], minX-offset, maxX+offset) and
                    self.betweenMinMax(intersectionPoint[1], minY-offset, maxY+offset) and 
                    self.betweenMinMax(intersectionPoint[2], minZ-offset, maxZ+offset))
        return intersect

    def betweenMinMax(self, intersectionPoint, min, max):
        if intersectionPoint < min or intersectionPoint > max:
            return False
        else :
            return True

    def selectHoveringStack(self, inputObject):
        if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT):
            if self.hoveredObject != None:
                self.selectedStack = self.hoveredObject
                self.makeInvisible(self.selectedStack)
            else :
                self.makeInvisible(self.selectedStack)
                self.selectedStack = None

    def selectHoveringCarton(self, inputObject):
        if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT) or inputObject.isKeyDown(self.BUTTON_MOUSE_RIGHT):
            if self.hoveredObject != None:
                self.removeHoverEffect(self.selectedCarton)
                self.selectedCarton = self.hoveredObject
                #Make the Stack Invisible 
                self.makeInvisible(self.selectedStack)
                self.addHoverEffect(self.selectedCarton)
            else :
                #self.removeSelectionBox(self.selectedCarton)
                self.removeHoverEffect(self.selectedCarton)
                self.previouslySelectedStack = self.selectedStack
                self.selectedCarton = None
                self.selectedStack = None
                self.resetStackPositions = True

    def addHoverEffect(self, hoveredObject):
        if hoveredObject:
            hoveredObject.material.settings["wireframe"] = True
            hoveredObject.material.settings["doubleSide"] = True
            hoveredObject.material.settings["lineWidth"] = 3

    def removeHoverEffect(self, object):
        if object:
            object.material.settings["wireframe"] = False
            object.material.settings["doubleSide"] = False
            object.material.settings["lineWidth"] = 1

    def makeInvisible(self, mesh):
        if mesh:
            mesh.visible = False
            mesh.material.settings["wireframe"] = True
            mesh.material.settings["doubleSide"] = True
            mesh.material.settings["lineWidth"] = 5

    def makeVisible(self, mesh):
        if mesh:
            mesh.visible = True
            mesh.material.settings["wireframe"] = True
            mesh.material.settings["doubleSide"] = True
            mesh.material.settings["lineWidth"] = 5
