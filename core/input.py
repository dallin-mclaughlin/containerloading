import pygame
from math import tan, pi
from numpy.linalg import norm
#from states.view import ViewState

class Input(object):

    def __init__(self):
        #has the user quit the application?
        self.quit = False

        self.hoverPanel = False

        self.resetViewState = False
        self.resetCreateState = False
        self.transferCreateData = False

        self.cartonData = None
        self.containerData = None
        self.orderData = None

        self.nextState = None

        #has the user lifted up the mouse button
        self.mouseButtonDown = False

        self.previousMousePos = (0,0)
        self.currentMousePos = (0,0)

        self.worldSpaceDirection = None

        self.screenCoordinates = pygame.display.get_surface().get_size()

        self.currentCamera = None

        # list to store key states
        #   down, up:   discrete event; lasts for one iteration
        #   pressed:    continuous event, between down and up events
        self.keyDownList = []
        self.keyPressedList = []
        self.keyUpList = []

        self.numList = ['0','1','2','3','4','5','6','7','8','9']
        # The list of codes for the numbers on the numpad
        # '[0]','[1]','[2]','[3]','[4]','[5]','[6]','[7]','[8]','[9]']

        self.MAIN_TO_CREATE = pygame.USEREVENT + 1
        self.MAIN_TO_DATABASE = pygame.USEREVENT + 2
        self.MAIN_TO_VIEW = pygame.USEREVENT + 3
        self.CREATE_TO_MAIN = pygame.USEREVENT + 4
        self.CREATE_TO_VIEW = pygame.USEREVENT + 5
        self.VIEW_TO_MAIN = pygame.USEREVENT + 6
        self.DATABASE_TO_MAIN = pygame.USEREVENT + 7

    def setCamera(self, camera):
        self.currentCamera = camera

    def update(self):
        # reset the next State to None every iteration
        self.nextState = None

        self.resetViewState = False
        self.resetCreateState = False

        #reset discrete key states
        self.keyDownList = []
        self.keyUpList = []

        #iterate over all user input events, e.g. keyboard or mouse, that occurred since the
        #last time events were checked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                keyName = pygame.key.name(event.key)
                self.keyDownList.append(keyName)
                self.keyPressedList.append(keyName)
            if event.type == pygame.KEYUP:
                keyName = pygame.key.name(event.key)
                self.keyPressedList.remove(keyName)
                self.keyUpList.append(keyName)
            if event.type == pygame.MOUSEBUTTONDOWN:
                button = event.button
                self.keyDownList.append(button)
                self.keyPressedList.append(button)
            if event.type == pygame.MOUSEBUTTONUP:
                button = event.button
                self.keyPressedList.remove(button)
                self.keyUpList.append(button)
            if event.type == self.MAIN_TO_CREATE:
                self.nextState = "CREATE" 
            if event.type == self.MAIN_TO_VIEW:
                self.nextState = "VIEW"
            if event.type == self.MAIN_TO_DATABASE:
                self.nextState = "DATABASE"
                self.updateDatabase = True
            if event.type == self.CREATE_TO_MAIN:
                self.nextState = "MAIN"
                self.resetCreateState = True
            if event.type == self.CREATE_TO_VIEW:
                self.nextState = "VIEW"
                self.resetCreateState = True
                self.transferCreateData = True
            if event.type == self.VIEW_TO_MAIN:
                self.nextState = "MAIN"
                self.resetViewState = True
            if event.type == self.DATABASE_TO_MAIN:
                self.nextState = "MAIN"

        self.currentMousePos = pygame.mouse.get_pos()

    def isKeyDown(self, keyCode):
        return keyCode in self.keyDownList
    
    def isKeyPressed(self, keyCode):
        return keyCode in self.keyPressedList

    def isKeyUp(self, keyCode):
        return keyCode in self.keyUpList

    def isBackspace(self):
        return 'backspace' in self.keyDownList

    def isTextEntered(self):
        for keyCode in self.numList:
            if keyCode in self.keyDownList:
                return keyCode
        return False

    def updatePreviousMousePos(self):
        self.previousMousePos = self.currentMousePos

    def getMousePos(self):
        return self.currentMousePos

    #Since the y-axis of the mouse position and pygame screen is inverted
    def getRectMousePos(self):
        return (self.currentMousePos[0], self.screenCoordinates[1] - self.currentMousePos[1])