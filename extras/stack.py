from core.mesh import Mesh
from geometry.geometry import Geometry
from material.surfaceMaterial import SurfaceMaterial
from geometry.boxGeometry import BoxGeometry

class Stack(Mesh):

    def __init__(self, dimensions=[5,5,2]):

        self.dimensions = dimensions

        mat = SurfaceMaterial({"useVertexColors": True,
                                    "doubleSide": True,
                                    "wireframe": True,
                                    "lineWidth" : 3})
        geo = BoxGeometry(dimensions[0],dimensions[1],dimensions[2])

        #initialize the mesh
        super().__init__(geo,mat)

        self.visible = False

    def getDimensions(self):
        return self.dimensions