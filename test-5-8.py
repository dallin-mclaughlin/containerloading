from email.mime import image
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.matrix import Matrix
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.textTexture import TextTexture
from extras.movementRig import MovementRig
from geometry.rectangleGeometry import RectangleGeometry

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
        self.rig.setPosition([0,0,0])
        self.scene.add(self.rig)

        labelTexture = TextTexture(text=" This is a Crate. ", systemFontName="Arial Bold",
                                    fontSize=40, fontColor=[0,0,200], imageWidth=256,
                                    imageHeight=128, alignHorizontal=0.5, alignVertical=0.5,
                                    imageBorderWidth=4, imageBorderColor=[255,0,0])
        labelMaterial = TextureMaterial(labelTexture)
        labelGeometry = RectangleGeometry(width=1, height=0.5)
        labelGeometry.applyMatrix(Matrix.makeRotationY(3.14))
        self.label = Mesh(labelGeometry, labelMaterial)
        self.label.setPosition([0,1,0])

        crateGeometry = BoxGeometry()
        crateTexture = Texture("images/crate.jpg")
        crateMaterial = TextureMaterial(crateTexture)
        self.crate = Mesh(crateGeometry, crateMaterial)
        self.crate1 = Mesh(crateGeometry, crateMaterial)
        self.scene.add(self.crate)
        self.crate1.setPosition([0,0,4])

        self.crate.add(self.crate1)

    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.rig.update(self.input, self.deltaTime)
        self.crate.rotateX(0.005)
        self.crate1.rotateZ(0.02)
        self.label.lookAt(self.camera.getWorldPosition())
        


#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()