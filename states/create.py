from core.values import SCREEN_HEIGHT, SCREEN_WIDTH
from states.state import State
from core.scene import Scene
from core.camera import Camera
import pygame

class CreateState(State):

    def __init__(self, renderer):
        super().__init__(renderer)

        self.resetScene()

    def update(self, inputObject, deltaTime):
        self.renderer.render(self.hudScene, self.hudCamera)
        if inputObject.transferCreateData:
            inputObject.cartonData = self.getCartonData()
            inputObject.containerData = self.getContainerData()
            inputObject.orderData = self.getOrderData()
        
        if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT):
            if self.containerPreviousButton.collidepoint(inputObject.getRectMousePos()) or self.containerNextButton.collidepoint(inputObject.getRectMousePos()):
                 newContainerSize = self.cycleList(self.containerSize, self.containerSizes,1)
                 self.hudScene.remove(self.containerSize[0])
                 self.containerSize = newContainerSize
            if self.orderPreviousButton.collidepoint(inputObject.getRectMousePos()):
                newOrder = self.cycleList(self.orderCode, self.customerOrderCodes,-1)
                self.hudScene.remove(self.orderCode[0])
                self.orderCode = newOrder
            if self.orderNextButton.collidepoint(inputObject.getRectMousePos()):
                newOrder = self.cycleList(self.orderCode, self.customerOrderCodes,1)
                self.hudScene.remove(self.orderCode[0])
                self.orderCode = newOrder
            if self.labelRect1.collidepoint(inputObject.getRectMousePos()):
                pygame.event.post(pygame.event.Event(inputObject.CREATE_TO_VIEW))
            if self.labelRect3.collidepoint(inputObject.getRectMousePos()):
                pygame.event.post(pygame.event.Event(inputObject.CREATE_TO_MAIN))
            if self.addLineButton.collidepoint(inputObject.getRectMousePos()):
                self.addLine()
            if self.removeLineButton.collidepoint(inputObject.getRectMousePos()):
                self.removeLastLine()
            for inputField in self.inputFields:
                if pygame.Rect(inputField[0].geometry.getRectObject()).collidepoint(inputObject.getRectMousePos()):
                    self.selectedField = inputField
                    break
                else:
                    self.selectedField = None

        if self.selectedField is not None:
            key = inputObject.isTextEntered()
            if key:
                for i in range(len(self.inputFields)):
                    if self.inputFields[i][0] == self.selectedField[0]:
                        newInputField = self.addToSelectedField(key)
                        self.inputFields.append(newInputField)
                        self.hudScene.remove(self.inputFields[i][0])
                        self.inputFields.remove(self.inputFields[i])
                        self.selectedField = newInputField
                        break
            elif inputObject.isBackspace():
               for i in range(len(self.inputFields)):
                   if self.inputFields[i][0] == self.selectedField[0]:
                       newInputField = self.backSpaceSelectedField()
                       self.inputFields.append(newInputField)
                       self.hudScene.remove(self.inputFields[i][0])
                       self.inputFields.remove(self.inputFields[i])
                       self.selectedField = newInputField
                       break
        if inputObject.resetCreateState:
            self.resetScene()

    def addLine(self):
        if len(self.inputFields) < 22:
            self.inputFields.append(self.createInputField(id=self.fieldID, type='itemcode', 
                                    width=0.125*SCREEN_WIDTH,height=0.04*SCREEN_HEIGHT, position=[0.75*SCREEN_WIDTH,0.8*SCREEN_HEIGHT - self.fieldID*0.045*SCREEN_HEIGHT], 
                                    alignment=[1,1],  text=""))
            self.inputFields.append(self.createInputField(id=self.fieldID, type='quantity', 
                                    width=0.0625*SCREEN_WIDTH,height=0.04*SCREEN_HEIGHT, position=[0.9375*SCREEN_WIDTH,0.8*SCREEN_HEIGHT - self.fieldID*0.045*SCREEN_HEIGHT], 
                                    alignment=[1,1], text=""))
            self.fieldID += 1  

    def removeLastLine(self):
        if len(self.inputFields) != 0: 
            lastItemCodeField = self.inputFields.pop()
            lastQuantityField = self.inputFields.pop()
            self.hudScene.remove(lastItemCodeField[0])
            self.hudScene.remove(lastQuantityField[0])

            self.fieldID -= 1    

    def resetScene(self):
        self.containerSizes = ['20','40']
        self.customerOrderCodes = ['JS','AEG','CWC','CEC','USA','BIM']

        self.hudScene = Scene()
        self.hudCamera = Camera()
        self.hudCamera.setOrthographic(0,SCREEN_WIDTH, 0, SCREEN_HEIGHT, 1, -1)

        self.fieldID = 1

        self.labelRect1 = self.createButton(width=0.25*SCREEN_WIDTH, height=0.075*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,0.125*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Solve")
        self.labelRect3 = self.createButton(width=0.25*SCREEN_WIDTH,height=0.075*SCREEN_HEIGHT, position=[0.25*SCREEN_WIDTH, 0.125*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Back")

        self.addLineButton = self.createButton(width=0.125*SCREEN_WIDTH, height=0.075*SCREEN_HEIGHT, position=[0.75*SCREEN_WIDTH,0.9*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Add Line")
        self.removeLineButton = self.createButton(width=0.15625*SCREEN_WIDTH,height=0.075*SCREEN_HEIGHT, position=[0.9375*SCREEN_WIDTH,0.9*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Remove Last Line")

        self.containerPreviousButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.25*SCREEN_WIDTH,0.9*SCREEN_HEIGHT],
                                             alignment=[1,1], text="<")
        
        self.containerNextButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.375*SCREEN_WIDTH,0.9*SCREEN_HEIGHT],
                                             alignment=[1,1], text=">")
        
        self.containerSize = self.createInputField(id=0, type='',width=0.04375*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.3125*SCREEN_WIDTH,0.9*SCREEN_HEIGHT], alignment=[1,1], 
                        text=self.containerSizes[0])

        self.orderPreviousButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.25*SCREEN_WIDTH,0.7*SCREEN_HEIGHT],
                                             alignment=[1,1], text="<")
        
        self.orderNextButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.375*SCREEN_WIDTH,0.7*SCREEN_HEIGHT],
                                             alignment=[1,1], text=">")

        self.orderCode = self.createInputField(id=0, type='',width=0.04375*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.3125*SCREEN_WIDTH,0.7*SCREEN_HEIGHT], alignment=[1,1], 
                        text=self.customerOrderCodes[0])

                                             
        self.createButton(width=0.09375*SCREEN_WIDTH,height=0.04*SCREEN_HEIGHT, position=[0.75*SCREEN_WIDTH,0.8*SCREEN_HEIGHT], alignment=[1,1], 
                        text="ItemCode:")
        self.createButton(width=0.09375*SCREEN_WIDTH,height=0.04*SCREEN_HEIGHT, position=[0.9375*SCREEN_WIDTH,0.8*SCREEN_HEIGHT], alignment=[1,1], 
                        text="Quantity:")
        

        self.inputFields = []

        self.selectedField = None

    def getCartonData(self):
        cartonData = []
        finalCartonData = []
        n = 2
        for x in self.inputFields:
            cartonData.append(x[1][6])
        for i in range(int(len(cartonData)/2)):
            data = []
            data.append(cartonData[2*i])
            data.append(cartonData[2*i+1])
            finalCartonData.append(data)
        return finalCartonData

    def getContainerData(self):
        return self.containerSize[1][6]

    def getOrderData(self):
        return self.orderCode[1][6]



                         
