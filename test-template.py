from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from material.flatMaterial import FlatMaterial
from material.lambertMaterial import LambertMaterial
from material.phongMaterial import PhongMaterial
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from light.pointLight import PointLight

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
                                    "wireframe": False,
                                    "lineWidth": 4})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self):
        self.renderer.render(self.scene, self.camera)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()