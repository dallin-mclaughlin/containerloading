from geometry.geometry import Geometry

class RectangleGeometry(Geometry):

    def __init__(self, width=1, height=1, position=[0,0], alignment=[0.5,0.5]):
        super().__init__()

        x, y = position
        a, b = alignment
        self.P0 = [x + (-a)*width, y + (-b)*height, 0]
        self.P1 = [x + (1-a)*width, y + (-b)*height, 0]
        self.P2 = [x + (-a)*width, y + (1-b)*height, 0]
        self.P3 = [x + (1-a)*width, y + (1-b)*height, 0]
        C0, C1, C2, C3 = [1,1,1], [1,0,0], [0,1,0], [0,0,1]
        T0, T1, T2, T3 = [0,0], [1,0], [0,1], [1,1]
        normalVector = [0,0,1]

        positionData = [self.P0, self.P1, self.P3, self.P0, self.P3, self.P2]
        colorData = [C0, C1, C3, C0, C3, C2]
        uvData = [T0, T1, T3, T0, T3, T2]
        normalData = [normalVector] * 6

        self.addAttribute("vec3", "vertexPosition", positionData)
        self.addAttribute("vec3", "vertexColor", colorData)
        self.addAttribute("vec2", "vertexUV", uvData)
        self.addAttribute("vec3", "vertexNormal", normalData)
        self.addAttribute("vec3", "faceNormal", normalData)
        self.countVertices()

    #For getting a pygame Rect object simulated for the geometry
    def getRectObject(self):
        rectData = (self.P0[0], self.P0[1], self.P3[0]-self.P0[0], self.P3[1]-self.P0[1])
        return rectData

