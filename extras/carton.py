from core.mesh import Mesh
from geometry.geometry import Geometry
from material.surfaceMaterial import SurfaceMaterial
from material.basicMaterial import BasicMaterial
from geometry.boxGeometry import BoxGeometry
from math import pi
import sqlite3

class Carton(Mesh):

    def __init__(self, itemCode='73450', orientation='LW', scaleFactor = 1):

        self.itemCode = itemCode
        self.orientation = orientation
        self.scaleFactor = scaleFactor

        self.carton = self.getDatabaseCartonCode(itemCode)
        self.color = self.getColor(self.carton)
        self.dimensions = self.getDatabaseDimensions(self.carton)

        mat = SurfaceMaterial({"useVertexColors": True,
                                    "doubleSide": False,
                                    "wireframe": False,
                                    "lineWidth" : 3})
        geo = BoxGeometry(self.dimensions[0],self.dimensions[1],self.dimensions[2], self.color)

        #initialize the mesh
        super().__init__(geo,mat)

    def changeOrientation(self):
        if self.orientation == 'LW':
            self.orientation = 'SW'
            self.rotateY(pi/2)
        elif self.orientation == 'SW':
            self.orientation = 'LW'
            self.rotateY(pi/2)

    def getDimensions(self):
        #for positioning purposes using the positioning algorithm
        if self.orientation == 'LW':
            return self.dimensions
        elif self.orientation == 'SW':
            return [self.dimensions[2], self.dimensions[1], self.dimensions[0]]

    def getCarton(self):
        return self.carton

    def getDatabaseDimensions(self, carton):
        con = sqlite3.connect('database/database.db')
        con.execute("PRAGMA foreign_keys = 1")

        cur = con.cursor()
        cur.execute('SELECT * FROM cartons WHERE carton = (?)',[carton])
        dimensions = cur.fetchone()[1:]

        con.commit()
        con.close()

        dimensions = [element * self.scaleFactor for element in dimensions]
        return dimensions

    def getDatabaseCartonCode(self, itemCode):
        if itemCode == 'A454':
            return 'A454'
        elif itemCode == 'A475':
            return 'A475'
        elif itemCode == 'A477':
            return 'A477'
        elif itemCode == 'A478':
            return 'A478'
        elif itemCode == 'A497':
            return 'A497'
        elif itemCode == 'A500':
            return 'A500'
        elif itemCode == 'C115':
            return 'C115'
        elif itemCode == 'C149':
            return 'C149'
        elif itemCode == 'C174':
            return 'C174'
        elif itemCode == 'C205':
            return 'C205'

        con = sqlite3.connect('database/database.db')
        con.execute("PRAGMA foreign_keys = 1")

        cur = con.cursor()
        cur.execute('SELECT carton FROM itemcodes WHERE itemcode = (?)',[itemCode])
        carton = cur.fetchone()[0]

        con.commit()
        con.close()

        return carton

    def getColor(self, carton):
        #red
        if carton == 'A454':
            return [[0.3,0,0],[0.3,0,0],[0.8,0,0],
                    [0.8,0,0],[0.5,0,0],[0.5,0,0]]
        #yellow
        elif carton == 'A475':
            return [[1,1,0],[1,1,0],[1,0.8,0],
                    [1,0.8,0],[1,0.8,0.3],[1,0.8,0.3]]
        #light green
        elif carton == 'A477':
            return [[0,1,0],[0,1,0],[0,0.75,0],
                    [0,0.75,0],[0.63,0.75,0],[0.63,0.75,0]]
        #blue
        elif carton == 'A478':
            return [[0,0,1],[0,0,1],[0,0.3,1],
                    [0,0.3,1],[0,0.6,1],[0,0.6,1]]
        #purple
        elif carton == 'A497':
            return [[0.43,0.2,1],[0.43,0.2,1],[0.53,0.2,1],
                    [0.53,0.2,1],[0.75,0.2,1],[0.75,0.2,1]]
        #grey
        elif carton == 'A500':
            return [[0.9,0.9,0.9],[0.9,0.9,0.9],[0.7,0.7,0.7],
                    [0.7,0.7,0.7],[0.5,0.5,0.5],[0.5,0.5,0.5]]
        #orange
        elif carton == 'C115':
            return [[0.75,0.27,0],[0.75,0.27,0],[0.62,0.27,0],
                    [0.62,0.27,0],[0.65,0.43,0],[0.65,0.43,0]]
        #pink
        elif carton == 'C149':
            return [[1,0,0.35],[1,0,0.35],[1,0,0.6],
                    [1,0,0.6],[1,0.45,0.6],[1,0.45,0.6]]
        #darkgreen
        elif carton == 'C174':
            return [[0,0.53,0],[0,0.53,0],[0,0.31,0],
                    [0,0.31,0],[0,0.31,0.21],[0,0.31,0.21]]
        #brown
        elif carton == 'C205':
            return [[0.4,0.24,0],[0.4,0.24,0],[0.57,0.24,0],
                    [0.57,0.24,0],[0.57,0.39,0.13],[0.57,0.39,0.13]]