from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.movementRig import MovementRig
from extras.raycastDebug import RaycastDebug
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
        self.camera.setPosition([0,0,0])

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0,0,0])

        self.raycast = RaycastDebug(self.camera)
        self.scene.add(self.raycast)

        geometry = BoxGeometry()
        material = SurfaceMaterial({"useVertexColors": True,
                                    "wireframe": False,
                                    "lineWidth": 1})
        box = Mesh(geometry, material)
        self.scene.add(box)
        box.setPosition([0, 0, 0])


        

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.deltaTime)
        self.raycast.update(self.camera)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()