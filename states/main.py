from states.state import State
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
import pygame
from core.values import SCREEN_HEIGHT, SCREEN_WIDTH

class MainState(State):

     def __init__(self, renderer):
          super().__init__(renderer)
          self.scene = Scene()
          self.camera = Camera(aspectRatio=800/500)

          crateGeometry = BoxGeometry()
          crateMaterial = SurfaceMaterial({"useVertexColors": True,
                                        "doubleSide": True,
                                        "wireframe": False,
                                        "lineWidth": 1})
          self.crate = Mesh(crateGeometry, crateMaterial)
          self.scene.add(self.crate)
          self.crate.setPosition([-1.8,0,-4])

          self.hudScene = Scene()
          self.hudCamera = Camera()
          self.hudCamera.setOrthographic(0,SCREEN_WIDTH, 0, SCREEN_HEIGHT, 1, -1)

          self.labelRect1 = self.createButton(width=0.25*SCREEN_WIDTH ,height=0.075*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,0.125*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Exit")
          self.labelRect2 = self.createButton(width=0.25*SCREEN_WIDTH ,height=0.075*SCREEN_HEIGHT, position=[0.8125*SCREEN_WIDTH,0.6*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Create New Layout")
          self.labelRect3 = self.createButton(width=0.25*SCREEN_WIDTH ,height=0.075*SCREEN_HEIGHT, position=[0.25*SCREEN_WIDTH,0.125*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Database")
    
     def update(self, inputObject, deltaTime):
          self.crate.rotateZ(0.003)
          self.crate.rotateY(0.002)
          self.renderer.render(self.scene, self.camera)
          self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)
          if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT) and self.labelRect1.collidepoint(inputObject.getRectMousePos()):
               inputObject.quit = True
          if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT) and self.labelRect2.collidepoint(inputObject.getRectMousePos()):
               pygame.event.post(pygame.event.Event(inputObject.MAIN_TO_CREATE))
          if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT) and self.labelRect3.collidepoint(inputObject.getRectMousePos()):
               pygame.event.post(pygame.event.Event(inputObject.MAIN_TO_DATABASE))

     def resetScene(self):
          self.scene = Scene()
          self.camera = Camera(aspectRatio=800/500)

          crateGeometry = BoxGeometry()
          crateMaterial = SurfaceMaterial({"useVertexColors": True,
                                        "doubleSide": True,
                                        "wireframe": False,
                                        "lineWidth": 1})
          self.crate = Mesh(crateGeometry, crateMaterial)
          self.scene.add(self.crate)
          self.crate.setPosition([-1.8,0,-4])


