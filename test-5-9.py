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
from material.spriteMaterial import SpriteMaterial
from extras.movementRig import MovementRig
from extras.gridHelper import GridHelper
from math import floor

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)
        self.camera.setPosition([0,0,4])

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.setPosition([0,0.5,3])
        self.scene.add(self.rig)
        geometry = RectangleGeometry()
        tileSet = Texture("images/rolling-ball.png")
        spriteMaterial = SpriteMaterial(tileSet, {
                                                "billboard" : 1,
                                                "tileCount" : [4,4],
                                                "tileNumber": 0
        })
        self.tilesPerSecond = 8

        self.sprite = Mesh(geometry, spriteMaterial)
        self.scene.add(self.sprite)

        grid = GridHelper()
        grid.rotateX(-3.14/2)
        self.scene.add(grid)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        tileNumber = floor(self.time * self.tilesPerSecond)
        self.sprite.material.uniforms["tileNumber"].data = tileNumber
        self.rig.update(self.input, self.deltaTime)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()