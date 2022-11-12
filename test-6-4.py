from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from core.renderTarget import RenderTarget
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from geometry.sphereGeometry import SphereGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.movementRig import MovementRig
from extras.postprocessor import Postprocessor
from effects.tintEffect import TintEffect
from effects.invertEffect import InvertEffect
from effects.pixelateEffect import PixelateEffect
from effects.vignetteEffect import VignetteEffect
from effects.colorReduceEffect import ColorReduceEffect
from effects.brightFilterEffect import BrightFilterEffect
from effects.horizontalBlurEffect import HorizontalBlurEffect
from effects.verticalBlurEffect import VerticalBlurEffect
from effects.additiveBlendEffect import AdditiveBlendEffect

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer(clearColor=[0,0,0])
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)

        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.setPosition([0,1,4])
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
        self.sphere.setPosition([0,1,0])
        self.scene.add(self.sphere)

        # glow scene
        self.glowScene = Scene();
        redMaterial = SurfaceMaterial({"baseColor": [1,0,0]})
        glowSphere = Mesh(sphereGeometry, redMaterial)
        glowSphere.transform = self.sphere.transform
        self.glowScene.add(glowSphere)

        #glow postprocessing
        glowTarget = RenderTarget(resolution=[800,600])
        self.glowPass = Postprocessor(self.renderer, self.glowScene, self.camera, glowTarget)
        self.glowPass.addEffect(HorizontalBlurEffect(textureSize=[800,600], blurRadius=50))
        self.glowPass.addEffect(VerticalBlurEffect(textureSize=[800,600], blurRadius=50))

        #combining results of glow effect with main scene
        self.comboPass = Postprocessor(self.renderer, self.scene, self.camera)
        self.comboPass.addEffect(AdditiveBlendEffect(glowTarget.texture, originalStrength=1,
                                                    blendStrength=3))

    def update(self):
        self.glowPass.render()
        self.comboPass.render()
        self.rig.update(self.input, self.deltaTime)

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()