from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from geometry.sphereGeometry import SphereGeometry
from geometry.polygonGeometry import PolygonGeometry
from geometry.pyramidGeometry import PyramidGeometry
from geometry.coneGeometry import ConeGeometry
from geometry.cylinderGeometry import CylinderGeometry
from geometry.cylindricalGeometry import CylindricalGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from material.flatMaterial import FlatMaterial
from material.lambertMaterial import LambertMaterial
from material.phongMaterial import PhongMaterial
from light.ambientLight import AmbientLight
from light.directionalLight import DirectionalLight
from light.pointLight import PointLight
from extras.movementRig import MovementRig
from extras.directionalLightHelper import DirectionalLightHelper
from extras.pointLightHelper import PointLightHelper
from math import sin

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

        ambient = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(ambient)
        self.directional = DirectionalLight(color=[0.3, 0.8, 0.2], direction=[-5,5,8])
        self.directional.rotateX(-3.14/2)
        self.scene.add(self.directional)
        #self.point = PointLight(color=[0.9, 0, 0], position=[1,1,0.8])
        #self.scene.add(self.point)

        directHelper = DirectionalLightHelper(self.directional)
        self.directional.setPosition([3,2,0])
        self.directional.add(directHelper)
        #pointHelper = PointLightHelper(self.point)
        #self.point.add(pointHelper)

        sphereGeometry = SphereGeometry()
        flatMaterial = FlatMaterial(properties={"baseColor": [0.6, 0.2, 0.2]})
        grid = Texture("images/grid.PNG")
        lambertMaterial = LambertMaterial(texture = grid)
        phongMaterial = PhongMaterial(properties={"baseColor": [0.5, 0.5, 1]})
        sphere1 = Mesh(sphereGeometry, flatMaterial)
        sphere1.setPosition([-2.2, 0, 0])
        self.scene.add(sphere1)
        sphere2 = Mesh(sphereGeometry, lambertMaterial)
        sphere2.setPosition([0,0,0])
        self.scene.add(sphere2)
        sphere3 = Mesh(sphereGeometry, phongMaterial)
        sphere3.setPosition([2.2, 0, 0])
        self.scene.add(sphere3)

    def update(self):
        self.rig.update(self.input, self.deltaTime)
        self.directional.setDirection([-5, sin(0.7*self.time), -2])
        #self.point.setPosition([1, sin(self.time), 0.8])
        self.renderer.render(self.scene, self.camera)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()