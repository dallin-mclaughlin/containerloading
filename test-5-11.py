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
from extras.movementRig import MovementRig
from core.renderTarget import RenderTarget
from extras.raycastDebug import RaycastDebug

screenWidth = 800
screenHeight = 600

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/600)

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0,0,0])
        skyGeometry = SphereGeometry(radius=50)
        skyMaterial = TextureMaterial(Texture("images/blue.png"))
        sky = Mesh(skyGeometry, skyMaterial)
        self.scene.add(sky)
        grassGeometry = RectangleGeometry(width=100, height=100)
        grassMaterial = TextureMaterial(Texture("images/grass.jpg"), {"repeatUV": [50,50]})
        grass = Mesh(grassGeometry, grassMaterial)
        grass.rotateX(-3.14/2)
        self.scene.add(grass)

        sphereGeometry = SphereGeometry()
        sphereMaterial = TextureMaterial(Texture("images/grid.png"))
        self.sphere = Mesh(sphereGeometry, sphereMaterial)
        self.sphere.setPosition([-1.2, 1, 0])
        self.scene.add(self.sphere)

        boxGeometry = BoxGeometry(width=2, height=2, depth=0.2)
        boxMaterial = SurfaceMaterial({"baseColor": [0,0,0]})
        box = Mesh(boxGeometry, boxMaterial)
        box.setPosition([1.2, 1, 0])
        self.scene.add(box)

        self.renderTarget = RenderTarget(resolution=[512,512], texture=None)
        screenGeometry = RectangleGeometry(width=1.8, height=1.8)
        screenMaterial = TextureMaterial(self.renderTarget.texture)
        screen = Mesh(screenGeometry, screenMaterial)
        screen.setPosition([1.2, 1, 0.11])
        self.scene.add(screen)

        self.skyCamera = Camera(aspectRatio=512/512)
        self.skyCamera.setPosition([self.rig.getWorldPosition()[0], self.rig.getWorldPosition()[1] + 10, self.rig.getWorldPosition()[2]] )
        #self.skyCamera.lookAt([0,0,0])
        self.skyCamera.rotateX(-3.14/2)
        self.rig.add(self.skyCamera)

        self.raycast = RaycastDebug(self.camera)
        self.camera.add(self.raycast)

    def update(self):
        self.sphere.rotateY(0.01337)
        #self.skyCamera.lookAt(self.rig.getWorldPosition())
        self.rig.update(self.input, self.deltaTime)
        self.renderer.render(self.scene, self.skyCamera, renderTarget=self.renderTarget)
        self.renderer.render(self.scene, self.camera)
        #self.raycast.update(self.input)

#instantiate this class and run the program
Test(screenSize=[800,600]).run()