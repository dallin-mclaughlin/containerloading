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
from material.material import Material

screenWidth = 1600
screenHeight = 1000

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=screenWidth/screenHeight)
        self.camera.setPosition([0,0,1.5])

        vertexShaderCode = """
            uniform mat4 projectionMatrix;
            uniform mat4 viewMatrix;
            uniform mat4 modelMatrix;
            in vec3 vertexPosition;
            in vec2 vertexUV;
            out vec2 UV;

            void main()
            {
                gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1.0);
                UV = vertexUV;
            }
        """

        fragmentShaderCode = """
            uniform sampler2D noise;
            uniform sampler2D image;
            in vec2 UV;
            uniform float time;
            out vec4 fragColor;

            void main()
            {
                vec2 uvShift = UV + vec2(-0.033, 0.07) * time;
                vec4 noiseValues = texture2D(noise, uvShift);
                vec2 uvNoise = UV + 0.4 * noiseValues.rg;
                fragColor = texture2D(image, uvNoise);
            }
        """

        noiseTex = Texture("images/noise.png")
        gridTex = Texture("images/blue.png")
        self.distortMaterial = Material(vertexShaderCode, fragmentShaderCode)
        self.distortMaterial.addUniform("sampler2D", "nosie", [noiseTex.textureRef, 1])
        self.distortMaterial.addUniform("sampler2D", "image", [gridTex.textureRef, 2])
        self.distortMaterial.addUniform("float", "time", 0.0)
        self.distortMaterial.locateUniforms()

        geometry = RectangleGeometry()
        self.mesh = Mesh(geometry, self.distortMaterial)
        self.scene.add(self.mesh)


    def update(self):
        self.renderer.render(self.scene, self.camera)
        self.distortMaterial.uniforms["time"].data += self.deltaTime

#instantiate this class and run the program
Test(screenSize=[screenWidth,screenHeight]).run()