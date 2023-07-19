from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from material.flatMaterial import FlatMaterial
from material.lambertMaterial import LambertMaterial
from material.phongMaterial import PhongMaterial
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from light.pointLight import PointLight
from extras.movementRig import MovementRig
from math import sin, cos
from extras.pointLightHelper import PointLightHelper

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
        self.rig.setPosition([0,0,6])

        ambientLight = AmbientLight(color=[0.3, 0.3, 0.3])
        self.scene.add(ambientLight)
        self.pointLight = PointLight(color=[1,1,1], position=[1.2, 1.2, 1])
        self.scene.add(self.pointLight)
        pointHelper = PointLightHelper(self.pointLight)
        self.pointLight.add(pointHelper)

        colorTex = Texture("images/brick-color.png")
        bumpTex = Texture("images/brick-bump.png")

        geometry = RectangleGeometry(width=2, height=2)
        bumpMaterial = LambertMaterial(texture=colorTex, bumpTexture=bumpTex,
                                        properties={"bumpStrength":1})
        material = LambertMaterial(texture=colorTex, bumpTexture=None) 
        mesh = Mesh(geometry, bumpMaterial)
        mesh1 = Mesh(geometry, material)
        self.scene.add(mesh)
        self.scene.add(mesh1)
        mesh1.setPosition([4,0,0])

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.deltaTime)
        self.pointLight.setPosition([cos(self.time)+1.5, sin(self.time), 1])

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()