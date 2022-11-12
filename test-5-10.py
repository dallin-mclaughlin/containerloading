from tkinter import Grid
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from extras.textTexture import TextTexture
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
from pygame import Rect
from core.values import SCREEN_HEIGHT, SCREEN_WIDTH

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.BUTTON_MOUSE_LEFT = 1
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/500)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0, 0.5, 3])
        self.scene.add(self.rig)

        crateGeometry = BoxGeometry()
        crateMaterial = TextureMaterial(Texture("images/crate.jpg"))
        crate = Mesh(crateGeometry, crateMaterial)
        self.scene.add(crate)

        grid = GridHelper(size=5, gridColor=[1,1,1], centerColor=[1,0,0])
        grid.rotateX(-3.14/2)
        self.scene.add(grid)

        self.hudScene = Scene()
        self.hudCamera = Camera()
        self.hudCamera.setOrthographic(0,SCREEN_WIDTH, 0, SCREEN_HEIGHT, 1, -1)
        labelGeo1 = RectangleGeometry(width=300, height=300, position=[800,400], 
                                        alignment=[1,1])
        self.labelRect = Rect(labelGeo1.getRectObject())
        print(self.labelRect)
        labelMat1 = TextureMaterial(TextTexture(text="Exit", systemFontName="Impact", fontSize=64,
                                fontColor=[0,0,200], imageWidth=512, imageHeight=512,
                                alignHorizontal=0.5, alignVertical=0.5, imageBorderWidth=0,
                                imageRoundedCorners=1, imageBorderColor=[255,0,0]))
        label1 = Mesh(labelGeo1, labelMat1)
        self.hudScene.add(label1)

        labelGeo2 = RectangleGeometry(width=400, height=80, position=[0,0], 
                                        alignment=[0,0])
        labelMat2 = TextureMaterial(Texture("images/version-1.png"))
        label2 = Mesh(labelGeo2, labelMat2)
        self.hudScene.add(label2)


    def update(self):
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.camera)
        self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)
        print(self.input.getRectMousePos())
        #print(self.labelRect)
        if(self.labelRect.collidepoint(self.input.getRectMousePos())):
            print('here')
        if(self.input.isKeyDown(self.BUTTON_MOUSE_LEFT) and self.labelRect.collidepoint(self.input.getRectMousePos())):
            self.input.quit = True

#instantiate this class and run the program
Test(screenSize=[SCREEN_WIDTH, SCREEN_HEIGHT]).run()