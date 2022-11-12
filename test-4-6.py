from extras.axesHelper import AxesHelper
from extras.gridHelper import GridHelper
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from extras.mouseSelector import MouseSelector
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from math import pi
from extras.movementRig import MovementRig
from extras.mouseSelector import MouseSelector
import pygame
import numpy

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)
        self.mouseSelector = MouseSelector(self.camera)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([-3,6,20])
        self.scene.add(self.rig)

        #axes = AxesHelper(axisLength=2)
        #self.scene.add(axes)

        #grid = GridHelper(size=2, gridColor=[1,1,1], centerColor=[1,1,0])
        #grid.rotateX(-pi/2)
        #self.scene.add(grid)

        #cartonGeometry = BoxGeometry(width=1, height=1, depth=1)
        #cartonMaterial1 = SurfaceMaterial({"useVertexColors": True})
        #cartonMaterial2 = SurfaceMaterial({"useVertexColors": True})
        #self.carton1 = Mesh(cartonGeometry, cartonMaterial1)
        #self.carton2 = Mesh(cartonGeometry, cartonMaterial2)
        #self.carton.setPosition([0.3,1,2.1])
        #self.scene.add(self.carton1)
        #self.scene.add(self.carton2)
        #self.carton2.setPosition([2,0,3])
        #print(self.carton.geometry.attributes["faceNormal"].data)
        #print(self.carton.geometry.attributes["vertexPosition"].data)

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    cartonGeometry = BoxGeometry(width=1, height=0.5, depth=2)
                    cartonMaterial = SurfaceMaterial({"useVertexColors": True})
                    box = Mesh(cartonGeometry, cartonMaterial)
                    self.scene.add(box)
                    box.setPosition([k*1.1, j*0.6, i*2.1])



    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.deltaTime)
        self.mouseSelector.update(self.scene, self.input)
        
        print(self.mouseSelector.selectedObject)
        

        

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()