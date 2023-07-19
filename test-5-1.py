from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.rectangleGeometry import RectangleGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)
        self.camera.setPosition([0,0,2])

        geometry = RectangleGeometry()
        grid = Texture("images/blue.png")
        material = TextureMaterial(grid)
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

        #initial rotation
        #self.mesh.rotateY(0.514)
        #self.mesh.rotateX(0.37)

    def update(self):
        #self.mesh.rotateY(0.00514)
        #self.mesh.rotateX(0.00337)
        self.renderer.render(self.scene, self.camera)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()