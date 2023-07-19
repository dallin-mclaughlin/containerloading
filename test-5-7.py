from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.textTexture import TextTexture
from states.create import CreateState
from states.main import MainState
from states.view import ViewState
from states.database import DatabaseState
from pygame import Rect

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):

        #contains the list of states for the application
        self.stateDict = {  "MAIN" : MainState(), "CREATE" : CreateState(),
                            "VIEW" : ViewState(), "DATABASE" : DatabaseState() }

        self.currentState = self.stateDict["MAIN"]
        print("Initializing program...")
        self.BUTTON_MOUSE_LEFT = 1
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)
        self.camera.setPosition([0,0,1.5])

        self.geometry = RectangleGeometry()
        
        #self.rect = Rect(self.geometry.attributes["vertexPosition"].data)
        self.message = TextTexture(text="Python Graphics", systemFontName="Impact", fontSize=32,
                                fontColor=[0,0,200], imageWidth=256, imageHeight=256,
                                alignHorizontal=0.5, alignVertical=0.5, imageBorderWidth=0,
                                imageRoundedCorners=100, imageBorderColor=[255,0,0])
        self.material = TextureMaterial(self.message)
        self.mesh = Mesh(self.geometry, self.material)
        self.scene.add(self.mesh)

        #initial rotation
        #self.mesh.rotateY(0.514)
        #self.mesh.rotateX(0.37)

    def update(self, inputObject):
        #self.mesh.rotateY(0.00514)
        #self.mesh.rotateX(0.00337)
        self.renderer.render(self.scene, self.camera)
        print(inputObject.getMousePos())
        print('hi')
        print(self.mesh.geometry.attributes["vertexPosition"].data)
        #print(self.rect)
        if(inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT) and self.material.collidepoint(inputObject.getMousePos())):
            inputObject.quit = True

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()