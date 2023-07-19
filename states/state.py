import pygame
from core.mesh import Mesh
from core.values import SCREEN_HEIGHT, SCREEN_WIDTH
from extras.textTexture import TextTexture
from geometry.rectangleGeometry import RectangleGeometry
from material.textureMaterial import TextureMaterial

class State(object):
    
    def __init__(self, renderer):
        self.renderer = renderer
        self.BUTTON_MOUSE_LEFT = 1
        self.BUTTON_MOUSE_RIGHT = 3

    def update(self, inputObject, deltaTime):
        pass

    def createButton(self, width, height, position, alignment, text, fontColor=[0,0,200], backgroundColor = [255,255,255,135]):
        buttonGeo = RectangleGeometry(width=width, height=height, position=position,
                                    alignment=alignment)
        buttonRect = pygame.Rect(buttonGeo.getRectObject())
        buttonMat = TextureMaterial(TextTexture(text=text, systemFontName="Impact",
                    fontSize=32, fontColor=fontColor, imageWidth=width, imageHeight=height,
                    alignHorizontal=0.5, alignVertical=0.5, imageBorderWidth=0, backgroundColor = backgroundColor,
                    imageRoundedCorners=0, imageBorderColor=[255,0,0]))
        button = Mesh(buttonGeo, buttonMat)
        self.hudScene.add(button)
        return buttonRect

    def createInputField(self, id, type, width, height, position, alignment, text, fontColor = [0,0,200], backgroundColor = [255,255,255,135]):
        fieldGeo = RectangleGeometry(width=width, height=height, position=position,
                                    alignment=alignment)
        fieldMat = TextureMaterial(TextTexture(text=text, systemFontName="Impact",
                    fontSize=32, fontColor=fontColor, imageWidth=width, imageHeight=height,
                    alignHorizontal=0.5, alignVertical=0.5, imageBorderWidth=0, backgroundColor = backgroundColor,
                    imageRoundedCorners=0, imageBorderColor=[255,0,0]))
        field = Mesh(fieldGeo, fieldMat)
        self.hudScene.add(field)
        return field, (id, type, width, height, position, alignment, text, fontColor, backgroundColor)

    def addToSelectedField(self, key):
        selectedField = self.selectedField
        previousText = selectedField[1][6]
        text = previousText + key
        field = self.createInputField(selectedField[1][0], selectedField[1][1], selectedField[1][2],
                                selectedField[1][3], selectedField[1][4], selectedField[1][5], text, 
                                selectedField[1][7], selectedField[1][8])
        return field

    def backSpaceSelectedField(self):
        selectedField = self.selectedField
        previousText = selectedField[1][6]
        text = previousText[:-1]
        field = self.createInputField(selectedField[1][0], selectedField[1][1], selectedField[1][2],
                                selectedField[1][3], selectedField[1][4], selectedField[1][5], text, 
                                selectedField[1][7], selectedField[1][8])
        return field

    def cycleList(self, display, options, direction):
        previousText = display[1][6]
        text = options[(options.index(previousText)+direction)%len(options)]
        field = self.createInputField(display[1][0], display[1][1], display[1][2],
                                display[1][3], display[1][4], display[1][5], text, 
                                display[1][7], display[1][8])
        return field