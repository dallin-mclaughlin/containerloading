from core.mesh import Mesh
from geometry.geometry import Geometry
from material.lineMaterial import LineMaterial

class RaycastDebug(Mesh):

    def __init__(self, camera, length = 50, lineWidth = 4, color = [0,0,0]):
        geometry = Geometry()

        cameraPos = camera.getWorldPosition()
        positionData = [cameraPos, [cameraPos[0], cameraPos[1], cameraPos[2] - length]]

        colorData = [color, color]

        geometry.addAttribute("vec3", "vertexPosition", positionData)
        geometry.addAttribute("vec3", "vertexColor", colorData)
        geometry.countVertices()

        material = LineMaterial({
            "useVertexColors": True,
            "lineWidth": lineWidth,
            "lineType": "connected"
        })

        #initialize the mesh
        super().__init__(geometry,material)

    def update(self, input):
        mousePos = input.currentMousePos
        #self.setDirection([mousePos[0], mousePos[1], -1])
        self.setDirection([3,5,-2])


