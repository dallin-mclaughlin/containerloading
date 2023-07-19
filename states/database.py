from core.values import SCREEN_HEIGHT, SCREEN_WIDTH
from extras.textTexture import TextTexture
from states.state import State
from tkinter import Grid
from core.base import Base
from core.renderer import Renderer
from core.scene import Scene
from core.camera import Camera
from core.mesh import Mesh
from core.texture import Texture
from geometry.boxGeometry import BoxGeometry
from geometry.rectangleGeometry import RectangleGeometry
from material.surfaceMaterial import SurfaceMaterial
from material.textureMaterial import TextureMaterial
from extras.gridHelper import GridHelper
from extras.movementRig import MovementRig
import pygame
import sqlite3

class DatabaseState(State):

    def __init__(self, renderer):
        super().__init__(renderer)

        self.hudScene = Scene()
        self.hudCamera = Camera()
        self.hudCamera.setOrthographic(0,SCREEN_WIDTH, 0, SCREEN_HEIGHT, 1, -1)

        self.labelRect1 = self.createButton(width=0.25*SCREEN_WIDTH, height=0.075*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,0.125*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Back")

    
    def update(self, inputObject, deltaTime):
        self.renderer.render(self.hudScene, self.hudCamera)
        if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT) and self.labelRect1.collidepoint(inputObject.getRectMousePos()):
            pygame.event.post(pygame.event.Event(inputObject.DATABASE_TO_MAIN))

    # def getContainerData(self):
    #     data = []
    #     con = sqlite3.connect('database/database.db')
    #     con.execute("PRAGMA foreign_keys = 1")

    #     cur = con.cursor()
    #     for row in cur.execute('SELECT * FROM containers'):
    #         data.append(row)
    #     self.containerDatabase = data

    #     con.commit()

    #     con.close()

    # def getCartonData(self):
    #     data = []
    #     con = sqlite3.connect('database/database.db')
    #     con.execute("PRAGMA foreign_keys = 1")

    #     cur = con.cursor()
    #     for row in cur.execute('SELECT * FROM cartons'):
    #         data.append(row)
    #     self.cartonDatabase = data

    #     con.commit()

    #     con.close()

    # def getItemcodeData(self):
    #     data = []
    #     con = sqlite3.connect('database/database.db')
    #     con.execute("PRAGMA foreign_keys = 1")

    #     cur = con.cursor()
    #     for row in cur.execute('SELECT * FROM itemcodes'):
    #         data.append(row)
    #     self.itemcodeDatabase = data

    #     con.commit()

    #     con.close()