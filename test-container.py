from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from extras.mouseSelector import MouseSelector
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from material.lineMaterial import LineMaterial
from material.phongMaterial import PhongMaterial
from material.basicMaterial import BasicMaterial
from extras.movementRig import MovementRig
import math

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0,0,0])

        self.mouseSelector = MouseSelector(self.camera)

        # box1 = Mesh(geometry, material)
        # box2 = Mesh(geometry, material)
        # self.scene.add(box1)
        # self.scene.add(box2)
        # box2.setPosition([3,0,0])
        # box2.rotateY(90*math.pi/180)
        for i in range(5):
           for j in range(5):
               for k in range(5):
                    geometry = BoxGeometry(1,0.5,2)
                    material = SurfaceMaterial({"useVertexColors": True,
                                    "doubleSide": True,
                                    "wireframe": False,
                                    "lineWidth": 1})
                    box = Mesh(geometry, material)
                    self.scene.add(box)
                    box.setPosition([k*1.2, j*1.2, i*2.4])

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.deltaTime)
        self.mouseSelector.update(self.scene, self.input)
        

#instantiate this class and run the program
Test(screenSize=[screenWidth, screenHeight]).run()