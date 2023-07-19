from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial

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

        geometry = BoxGeometry()
        material = SurfaceMaterial({"useVertexColors": True,
                                    "doubleSide": True,
                                    "wireframe": True,
                                    "lineWidth": 1})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.mesh.rotateY(0.00914)
        self.mesh.rotateX(0.00937)
        self.renderer.render(self.scene, self.camera)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()