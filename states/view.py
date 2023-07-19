from core.object3D import Object3D
from core.values import SCREEN_HEIGHT, SCREEN_WIDTH
from extras.mouseSelector import MouseSelector
from extras.textTexture import TextTexture
from geometry.planeGeometry import PlaneGeometry
from material.basicMaterial import BasicMaterial
from states.state import State
from tkinter import Grid
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
from extras.carton import Carton
from extras.stack import Stack
from collections import OrderedDict
import pygame
import sqlite3
import numpy
import numpy.linalg



class ViewState(State):
    
    def __init__(self, renderer):
        super().__init__(renderer)

        self.scaleFactor = 0.002

    def update(self, inputObject, deltaTime):
        
        #Checks to see if there is input data from create state to pass to view state
        if inputObject.cartonData is not None:
            self.resetScene()
            self.cartonData = inputObject.cartonData
            self.containerData = inputObject.containerData
            self.orderData = inputObject.orderData
            self.calculateInitialMaxHeight()
            self.createCartonTallyPanel()
            self.createContainerFloorGrid()
            self.createContainerBackPanel()
            self.setMovementRigPosition()
            print("initial max height", self.initialMaxHeight)
            self.displayCartonData()
            inputObject.cartonData = None
            inputObject.containerData = None
            inputObject.orderData = None
            print(self.totalCartonTally)

        self.rig.update(inputObject, deltaTime)
        
        if not pygame.Rect(self.panel[0].geometry.getRectObject()).collidepoint(inputObject.getRectMousePos()):
            inputObject.hoverPanel = False
            self.mouseSelector.update(self.container, inputObject)
        else:
            inputObject.hoverPanel = True
        # For the below two conditions include the condition that not colliding with menu panel
    

        if inputObject.resetViewState:
            self.resetScene()

        if inputObject.isKeyDown(self.BUTTON_MOUSE_RIGHT):
            self.deleteCarton()

        if inputObject.isKeyDown(self.BUTTON_MOUSE_LEFT):
            if pygame.Rect(self.panel[0].geometry.getRectObject()).collidepoint(inputObject.getRectMousePos()):
                if self.positionNextButton.collidepoint(inputObject.getRectMousePos()) or self.positionPreviousButton.collidepoint(inputObject.getRectMousePos()):
                    newPos = self.cycleList(self.position, self.addingPosition, 1)
                    self.hudScene.remove(self.position[0])
                    self.hudScene.remove(self.panel[0])
                    self.position = newPos
                    self.panel = self.createInputField(id=0,type='',width=0.225*SCREEN_WIDTH,height=1*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,1*SCREEN_HEIGHT], alignment=[1,1], text="")
                if self.orientationNextButton.collidepoint(inputObject.getRectMousePos()) or self.orientationPreviousButton.collidepoint(inputObject.getRectMousePos()):
                    newOrientation = self.cycleList(self.orientation, self.addingOrientation, 1)
                    self.hudScene.remove(self.orientation[0])
                    self.hudScene.remove(self.panel[0])
                    self.orientation = newOrientation
                    self.panel = self.createInputField(id=0,type='',width=0.225*SCREEN_WIDTH,height=1*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,1*SCREEN_HEIGHT], alignment=[1,1], text="")
                if self.labelRect1.collidepoint(inputObject.getRectMousePos()):
                    pygame.event.post(pygame.event.Event(inputObject.VIEW_TO_MAIN))
                if self.labelRect2.collidepoint(inputObject.getRectMousePos()):
                    self.deleteCarton()
                if (self.mouseSelector.selectedStack != None and self.mouseSelector.selectedCarton == None):
                    if self.labelRect3.collidepoint(inputObject.getRectMousePos()):
                        self.deleteStack()
                    if self.labelRect4.collidepoint(inputObject.getRectMousePos()):
                        self.rotateStack()
                    #print(self.cartonTallyLabels)
                    for k,v in self.cartonTallyLabels.items():
                        #check if collision occurs first lol
                        if pygame.Rect(v[0].geometry.getRectObject()).collidepoint(inputObject.getRectMousePos()):
                            if self.position[1][6] == 'TOP' and self.orientation[1][6] == 'LW':
                                print('1')
                                self.addCartonToTop(self.mouseSelector.selectedStack, v[1][0], False)
                            elif self.position[1][6] == 'TOP' and self.orientation[1][6] == 'SW':
                                print('2')
                                self.addCartonToTop(self.mouseSelector.selectedStack, v[1][0], True)
                            elif self.position[1][6] == 'BOT' and self.orientation[1][6] == 'LW':
                                print('3')
                                self.addCartonToBottom(self.mouseSelector.selectedStack, v[1][0], False)
                            elif self.position[1][6] == 'BOT' and self.orientation[1][6] == 'SW':
                                print('4')
                                self.addCartonToBottom(self.mouseSelector.selectedStack, v[1][0], True)
                            break
            else:
                # If a stack is selected then move the other stacks away from it
                if(self.mouseSelector.selectedStack != None and self.mouseSelector.selectedCarton == None):
                    self.viewStack()
                # Deselect the current stack and put all the stacks back into their original position
                if(self.mouseSelector.previouslySelectedStack != None and self.mouseSelector.hoveredObject == None):
                    self.unViewStack()

        self.renderer.render(self.scene, self.camera)
        self.renderer.render(self.hudScene, self.hudCamera, clearColor=False)

    def addCartonToTop(self, stack, cartonCode, sideways=False):
        carton = Carton(cartonCode, scaleFactor=self.scaleFactor)
        if sideways:
            carton.changeOrientation()
        cartonPosition = self.findPosition(carton, stack, heightConscious=False)
        stack.add(carton)
        carton.setPosition(cartonPosition)
        self.alterCartonTally(carton.getCarton(), -1)

    def addCartonToBottom(self, stack, cartonCode, sideways=False):
        #get index of previous stack
        index = self.stacks.index(stack)
        #create new stack
        newStack = Stack(stack.getDimensions())
        self.container.add(newStack)
        self.stacks.insert(index, newStack)
        newStack.setPosition(stack.getPosition())
        #add new carton
        carton = Carton(cartonCode, scaleFactor=self.scaleFactor)
        if sideways:
            carton.changeOrientation()
        cartonPosition = self.findPosition(carton, newStack, heightConscious=False)
        newStack.add(carton)
        carton.setPosition(cartonPosition)
        #restack previous cartons
        self.restack(stack, newStack, 0, heightConscious=False)
        #update carton tally
        self.alterCartonTally(carton.getCarton(), -1)
        self.mouseSelector.selectedStack = newStack
        self.mouseSelector.previouslySelectedStack = newStack

    def getDatabaseCartonDimensions(self, cartonCode):
        con = sqlite3.connect('database/database.db')
        con.execute("PRAGMA foreign_keys = 1")

        cur = con.cursor()
        cur.execute('SELECT * FROM cartons WHERE carton = (?)',[cartonCode])
        dimensions = cur.fetchone()[1:]
        con.commit()

        con.close()

        return dimensions

    def createContainerFloorGrid(self):
        geometry = PlaneGeometry(width=self.containerDimensions[0]*self.scaleFactor,
                                    height=self.containerDimensions[2]*self.scaleFactor)
        material = SurfaceMaterial({"useVertexColors": False,
                                    "doubleSide": True,
                                    "wireframe": False,
                                    "lineWidth" : 3})
        containerFloor = Mesh(geometry, material)
        containerFloor.rotateX(3.14/2)
        containerFloor.translate(x=0,y=self.containerDimensions[2]*self.scaleFactor/2,z=0.05)
        self.scene.add(containerFloor)

    def createContainerBackPanel(self):
        geometry = PlaneGeometry(width=self.containerDimensions[0]*self.scaleFactor,
                                    height=self.containerDimensions[1]*self.scaleFactor)
        material = SurfaceMaterial({"useVertexColors": False,
                                    "doubleSide": True,
                                    "wireframe": False,
                                    "lineWidth" : 3})
        self.containerBackPanel = Mesh(geometry, material)
        #change this back to translate if it doesn't work
        self.containerBackPanel.setPosition([0,self.containerDimensions[1]*self.scaleFactor/2,-0.05])
        self.scene.add(self.containerBackPanel)
    
    def resetScene(self):
        
        self.containerDimensions = None

        self.scene = Scene()
        self.camera = Camera(aspectRatio=800/500)
        self.rig = MovementRig()

        self.totalCartonTally = {}

        self.cartonTallyLabels = {}

        self.addingPosition = ['TOP','BOT']
        self.addingOrientation = ['LW','SW']

        self.rig.add(self.camera)
        self.rig.setPosition([0, 0.5, 3])
        self.scene.add(self.rig)
        self.mouseSelector = MouseSelector(self.camera)

        self.container = Object3D()
        self.scene.add(self.container)
        self.stacks = []

        self.hudScene = Scene()
        self.hudCamera = Camera()
        self.hudCamera.setOrthographic(0,SCREEN_WIDTH, 0, SCREEN_HEIGHT, 1, -1)

        self.orientationPreviousButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.85*SCREEN_WIDTH,0.99*SCREEN_HEIGHT],
                                             alignment=[1,1], text="<", fontColor=[255,255,255], backgroundColor = [0,0,0,255])
        
        self.orientationNextButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.95*SCREEN_WIDTH,0.99*SCREEN_HEIGHT],
                                             alignment=[1,1], text=">", fontColor=[255,255,255], backgroundColor = [0,0,0,255])
        
        self.orientation = self.createInputField(id=0, type='',width=0.04375*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.905*SCREEN_WIDTH,0.99*SCREEN_HEIGHT], alignment=[1,1], 
                        text=self.addingOrientation[0], fontColor=[255,255,255], backgroundColor = [0,0,0,255])

        self.positionPreviousButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.85*SCREEN_WIDTH,0.93*SCREEN_HEIGHT],
                                             alignment=[1,1], text="<", fontColor=[255,255,255], backgroundColor = [0,0,0,255])
        
        self.positionNextButton = self.createButton(width=0.03125*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.95*SCREEN_WIDTH,0.93*SCREEN_HEIGHT],
                                             alignment=[1,1], text=">", fontColor=[255,255,255], backgroundColor = [0,0,0,255])
        
        self.position = self.createInputField(id=0, type='',width=0.04375*SCREEN_WIDTH,height=0.05*SCREEN_HEIGHT, position=[0.905*SCREEN_WIDTH,0.93*SCREEN_HEIGHT], alignment=[1,1], 
                        text=self.addingPosition[0], fontColor=[255,255,255], backgroundColor = [0,0,0,255])

        self.labelRect1 = self.createButton(width=0.2*SCREEN_WIDTH,height=0.075*SCREEN_HEIGHT, position=[0.9875*SCREEN_WIDTH,0.1*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Exit", 
                                             fontColor=[0,0,0], backgroundColor = [255,255,255,255])
        self.addNewStackButton = self.createButton(width=0.2*SCREEN_WIDTH,height=0.055*SCREEN_HEIGHT, position=[0.9875*SCREEN_WIDTH,0.18*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Add New Stack", 
                                             fontColor = [0,0,0], backgroundColor = [255,255,255,255])
        self.labelRect2 = self.createButton(width=0.2*SCREEN_WIDTH,height=0.055*SCREEN_HEIGHT, position=[0.9875*SCREEN_WIDTH,0.24*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Delete Carton", 
                                             fontColor = [0,0,0], backgroundColor = [255,255,255,255])
        self.labelRect3 = self.createButton(width=0.2*SCREEN_WIDTH,height=0.055*SCREEN_HEIGHT, position=[0.9875*SCREEN_WIDTH,0.3*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Delete Stack", 
                                             fontColor = [0,0,0], backgroundColor = [255,255,255,255])
        self.labelRect4 = self.createButton(width=0.2*SCREEN_WIDTH,height=0.055*SCREEN_HEIGHT, position=[0.9875*SCREEN_WIDTH,0.36*SCREEN_HEIGHT],
                                             alignment=[1,1], text="Rotate Stack", 
                                             fontColor = [0,0,0], backgroundColor = [255,255,255,255])

        self.containerData = None
        self.orderData = None
        self.cartonData = None


    def createCartonTallyPanel(self):
        for index, (carton, quantity) in enumerate(self.totalCartonTally.items()):
            text = "0/"+str(quantity)
            self.cartonTallyLabels['ADD_'+str(carton)] = self.createInputField(id=str(carton), type='add', 
                                    width=0.05*SCREEN_WIDTH,height=0.04*SCREEN_HEIGHT, position=[0.8375*SCREEN_WIDTH,0.85*SCREEN_HEIGHT - index * 0.06*SCREEN_HEIGHT], 
                                    alignment=[1,1],  text='ADD', fontColor=[255,255,255], 
                                    backgroundColor = self.getBackGroundColor(str(carton)))
            self.cartonTallyLabels[str(carton)] = self.createInputField(id=str(carton), type='carton', 
                                    width=0.125*SCREEN_WIDTH,height=0.04*SCREEN_HEIGHT, position=[0.9725*SCREEN_WIDTH,0.85*SCREEN_HEIGHT - index * 0.06*SCREEN_HEIGHT], 
                                    alignment=[1,1],  text=text, fontColor=[255,255,255], 
                                    backgroundColor = self.getBackGroundColor(str(carton)))
        self.panel = self.createInputField(id=0,type='',width=0.225*SCREEN_WIDTH,height=1*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,1*SCREEN_HEIGHT], alignment=[1,1], text="")
    
    def getBackGroundColor(self, carton):
        #red
        if carton == 'A454':
            return [77,0,0,255]
        #yellow
        elif carton == 'A475':
            return [255,255,0,255]
        #green
        elif carton == 'A477':
            return [0,255,0,255]
        #blue
        elif carton == 'A478':
            return [0,77,255,255]
        #purple
        elif carton == 'A497':
            return [110,51,255,255]
        #grey
        elif carton == 'A500':
            return [230,230,230,255]
        #orange
        elif carton == 'C115':
            return [191,69,0,255]
        #pink
        elif carton == 'C149':
            return [255,0,89,255]
        #dark green
        elif carton == 'C174':
            return [0,79,54,255]
        #brown
        elif carton == 'C205':
            return [102,61,0,255]

    def calculateInitialMaxHeight(self):
        volume = 0
        con = sqlite3.connect('database/database.db')
        con.execute("PRAGMA foreign_keys = 1")

        cur = con.cursor()
        print(self.containerData)
        container = None
        if self.containerData == '20':
            container = 'TWENTY'
        elif self.containerData == '40':
            container = 'FORTY'
        cur.execute('SELECT * FROM containers WHERE container = (?)',[container])
        self.containerDimensions = cur.fetchone()[1:]

        for itemTuple in self.cartonData:
            itemCode = itemTuple[0]
            quantity = int(itemTuple[1])
            cur.execute('SELECT * FROM itemcodes WHERE itemcode = (?)',[itemCode])
            carton = cur.fetchone()[1]
            # length, width, height
            cur.execute('SELECT * FROM cartons WHERE carton = (?)', [carton])
            dimensions = cur.fetchone()[1:]
            #populate the container space with cartons
            self.sumCartonTally(carton, quantity)
            volume = volume + self.calculateVolume(dimensions, quantity)
        self.orderCartonTally()

        self.initialMaxHeight = self.scaleFactor * volume / self.containerDimensions[0] / self.containerDimensions[2]

        con.commit()

        con.close()

    def setMovementRigPosition(self):
        self.rig.setPosition([- self.scaleFactor * (self.containerDimensions[0] + 1000), 
                            self.scaleFactor * self.containerDimensions[1],
                            self.scaleFactor * (self.containerDimensions[2]+800)])
        self.rig.lookAttachment.rotateX(-0.4)
        self.rig.rotateY(-1.0)

    def calculateVolume(self, dimensions, quantity):
        volume = quantity * dimensions[0] * dimensions[1] * dimensions[2]
        return volume
    
    def sumCartonTally(self, carton, quantity):
        if carton not in list(self.totalCartonTally):
            self.totalCartonTally[carton] = 0
        self.totalCartonTally[carton] += quantity

    def orderCartonTally(self):
        orderedDict = {}
        unorderedDict = self.totalCartonTally
        orderedDict = dict(sorted(unorderedDict.items()))
        self.totalCartonTally = orderedDict

    def displayCartonData(self):
        for carton, quantity in self.cartonData:
            self.generateLine(carton, quantity)

    def printContainer(self):
        container = self.container
        for stack in container.children:
            for carton in stack.children:
                print(carton.geometry.attributes["vertexPosition"].data)

    def viewStack(self):
        stackNum = -1
        for i in range(len(self.stacks)):
            if self.stacks[i] == self.mouseSelector.selectedStack:
                stackNum = i
                break
        if stackNum != -1:
            for i in range(len(self.stacks)):
                if i < stackNum:
                    self.moveStackBack(self.stacks[i])
                if i > stackNum:
                    self.moveStackForward(self.stacks[i])
            self.containerBackPanel.translate(x=0,y=0,z=-3)

    def unViewStack(self):
        stackNum = -1
        for i in range(len(self.stacks)):
            if self.stacks[i] == self.mouseSelector.previouslySelectedStack:
                stackNum = i
                break
        if stackNum != -1:
            for i in range(len(self.stacks)):
                if i < stackNum:
                    self.moveStackForward(self.stacks[i])
                if i > stackNum:
                    self.moveStackBack(self.stacks[i])
            self.containerBackPanel.translate(x=0,y=0,z=3)
        
        self.mouseSelector.previouslySelectedStack = None

    #just do an instantaneous position change
    def moveStackBack(self, stack, z=-3):
        stack.translate(x=0,y=0,z=z)

    def moveStackForward(self, stack, z=3):
        stack.translate(x=-0,y=0,z=z)

    def deleteCarton(self):
        if self.mouseSelector.selectedCarton != None:
            deletedCarton = self.mouseSelector.selectedCarton
            selectedStack = self.mouseSelector.selectedStack
            carton = deletedCarton.carton
            self.alterCartonTally(carton, 1)
            self.mouseSelector.selectedCarton = None

            #Determine if carton was the last added then restack
            indexDeletedCarton = selectedStack.children.index(deletedCarton)
            selectedStack.remove(deletedCarton)
            del deletedCarton
            if indexDeletedCarton < len(selectedStack.children):
                self.restack(selectedStack, selectedStack, indexDeletedCarton, heightConscious=False)

            #if there are no more cartons delete the stack
            if len(selectedStack.children) == 0:
                #reposition back all the stacks
                self.resetStackPositions(selectedStack)
                self.container.remove(selectedStack)
                self.stacks.remove(selectedStack)
                del selectedStack
                self.mouseSelector.selectedStack = None

    def deleteStack(self):
        if self.mouseSelector.selectedStack != None and self.mouseSelector.selectedCarton == None:
            alteredCartons = {}
            selectedStack = self.mouseSelector.selectedStack
            for carton in selectedStack.children:
                cartonCode = carton.getCarton()
                if cartonCode not in alteredCartons:
                    alteredCartons[cartonCode] = 0
                alteredCartons[cartonCode] += 1
            for carton in selectedStack.children:
                selectedStack.remove(carton)
            self.container.remove(selectedStack)
            self.stacks.remove(selectedStack)
            del selectedStack

            #apply alterCartonTally Function
            for k,v in alteredCartons.items():
                self.alterCartonTally(k,v)

            #reposition all the stacks
            self.repositionStacks()

            #reset mouseSelector object
            self.mouseSelector.selectedStack = None

    def repositionStacks(self):
        #set the back panel of the container
        self.containerBackPanel.setPosition([0,self.containerDimensions[1]*self.scaleFactor/2,-0.05])

        newPos = numpy.array([0, self.containerDimensions[1]*self.scaleFactor/2, 0])
        for i in range(len(self.stacks)):
            stackDims = self.stacks[i].getDimensions()
            newPos = numpy.add(newPos, numpy.array([0,0,stackDims[2]/2]))
            self.stacks[i].setPosition(newPos)
            newPos = numpy.add(newPos, numpy.array([0,0,stackDims[2]/2]))

    def rotateStack(self):
        selectedStack = self.mouseSelector.selectedStack
        index = self.stacks.index(selectedStack)
        firstCarton = selectedStack.children[0]
        firstCartonDimensions = firstCarton.getDimensions()
        newStack = Stack([self.containerDimensions[0]*self.scaleFactor,
                            self.containerDimensions[1]*self.scaleFactor,
                            firstCartonDimensions[0]])
        self.restack(selectedStack, newStack, 0, changeOrientation=True)
        self.stacks.insert(index, newStack)
        self.container.add(newStack)
        self.repositionStacks()
        self.mouseSelector.selectedStack = newStack
        self.viewStack()

            
    def restack(self, fromStack, toStack, index, changeOrientation=False, heightConscious=True):
        aboveHeight = False
        discardedCartons = {}
        #restack the stacks with index numbers equal to or greater than index in method
        toBeReStacked = []
        for i in range(index,len(fromStack.children)):
            cartonObject = fromStack.children[i]
            if changeOrientation:
                cartonObject.changeOrientation()
            toBeReStacked.append(cartonObject)
        for carton in toBeReStacked:
            fromStack.remove(carton)
        for carton in toBeReStacked:
            position = None
            if aboveHeight:
                cartonCode = carton.getCarton()
                if cartonCode not in discardedCartons:
                    discardedCartons[cartonCode] = 0
                discardedCartons[cartonCode] += 1
            else:
                position = self.findPosition(carton, toStack, heightConscious)
            #continue here
            if isinstance(position, int):
                aboveHeight = True
                discardedCartons[carton.getCarton()] = 1
            elif not aboveHeight:
                carton.setPosition(position)
                toStack.add(carton)
        if fromStack != toStack:
            self.container.remove(fromStack)
            self.stacks.remove(fromStack)
            del fromStack
        #apply alterCartonTally Function
        for k,v in discardedCartons.items():
            self.alterCartonTally(k,v)

    def resetStackPositions(self, deletedStack):
        stackNum = -1
        for i in range(len(self.stacks)):
            if self.stacks[i] == deletedStack:
                stackNum = i
                break
        if stackNum != -1:
            for i in range(len(self.stacks)):
                if i < stackNum:
                    self.moveStackForward(self.stacks[i])
                if i > stackNum:
                    self.moveStackBack(self.stacks[i], z=-(3+deletedStack.getDimensions()[2]))
            self.containerBackPanel.translate(x=0,y=0,z=3)
        
        self.mouseSelector.previouslySelectedStack = None
        
    def alterCartonTally(self, carton, quantity):
        cartonTallyLabel = self.cartonTallyLabels[carton][0]
        self.hudScene.remove(cartonTallyLabel)
        self.hudScene.remove(self.panel[0])
        cLabelInfo = self.cartonTallyLabels[carton][1]
        oldText = cLabelInfo[6]
        index = oldText.index('/')
        newQuantity = int(oldText[:index]) + quantity
        newText = str(newQuantity) + oldText[index:]
        self.cartonTallyLabels[carton] = self.createInputField(id=cLabelInfo[0], type=cLabelInfo[1], 
                                    width=cLabelInfo[2],height=cLabelInfo[3], position=cLabelInfo[4], 
                                    alignment=cLabelInfo[5], text=newText, fontColor = cLabelInfo[7],
                                    backgroundColor = cLabelInfo[8])
        self.panel = self.createInputField(id=0,type='',width=0.225*SCREEN_WIDTH,height=1*SCREEN_HEIGHT, position=[1*SCREEN_WIDTH,1*SCREEN_HEIGHT], alignment=[1,1], text="")

    def generateLine(self, itemCode, quantity):
        for i in range(int(quantity)):
            self.addCarton(itemCode)
            #print(i)

    def addCarton(self, itemCode, heightConscious=True):
        carton = Carton(itemCode, orientation='LW', scaleFactor=self.scaleFactor)
        cartonDimensions = carton.getDimensions()
        #make sure there is at least one stack to which the carton will be added 
        if len(self.container.children) == 0:
            self.addStack(cartonDimensions)
        #return the position of the carton
        cartonPosition = self.positionCartonInitial(carton, cartonDimensions, heightConscious)
        stack = self.getLastStack()
        stack.add(carton)
        carton.setPosition(cartonPosition)

    def addStack(self, dimensions):
        #the first stack
        if len(self.container.children) == 0:
            self.stacks.append(Stack([self.containerDimensions[0] * self.scaleFactor,
                                        self.containerDimensions[1] * self.scaleFactor, 
                                        dimensions[2]]))
            self.container.add(self.stacks[0])
            self.stacks[0].setPosition([0,
                                        self.containerDimensions[1] * self.scaleFactor/2,
                                        dimensions[2]/2])
            print(self.stacks[0].getPosition())
        #other stacks after the first stack
        else :
            self.stacks.append(Stack([self.containerDimensions[0] * self.scaleFactor,
                                        self.containerDimensions[1] * self.scaleFactor, 
                                        dimensions[2]]))
            self.container.add(self.stacks[len(self.stacks)-1])
            self.stacks[len(self.stacks)-1].setPosition([0,
                                        self.containerDimensions[1] * self.scaleFactor/2,
                                        self.stacks[len(self.stacks)-2].getPosition()[2] +
                                        dimensions[2]])

    def positionCartonInitial(self, carton, cartonDimensions, heightConscious):
        lastStack = self.getLastStack()
        position = self.findPosition(carton, lastStack, heightConscious)
        #if added carton position is above the inital max height then add another stack
        if isinstance(position, int):
            self.addStack(cartonDimensions)
            lastStack = self.getLastStack()
            position = self.findPosition(carton, lastStack, heightConscious)
        return position

    def findPosition(self, carton, stack, heightConscious):
        #needed to add this error height because the 7th carton always collided with the first layer of cartons
        #affects the gap between 
        errorHeight = 0.001
        cartonDimensions = carton.getDimensions()
        stackDimensions = stack.getDimensions()
        #check vertical axis on the right hand side first
        lowerRight = numpy.array([stackDimensions[0]-cartonDimensions[0],
                                -stackDimensions[1]+cartonDimensions[1],
                                -stackDimensions[2]+cartonDimensions[2]])
        higherRight = numpy.array([stackDimensions[0]-cartonDimensions[0],
                                stackDimensions[1]-cartonDimensions[1],
                                -stackDimensions[2]+cartonDimensions[2]])
        lowerLeft = numpy.array([-stackDimensions[0]+cartonDimensions[0],
                                -stackDimensions[1]+cartonDimensions[1],
                                -stackDimensions[2]+cartonDimensions[2]])
        lowerRight = numpy.dot(0.5, lowerRight)
        higherRight = numpy.dot(0.5, higherRight)
        lowerLeft = numpy.dot(0.5, lowerLeft)

        #the height at which a carton can be added
        firstPos = self.findNoCollision(lowerRight, higherRight, cartonDimensions, stack, heightConscious)
        #the width pos value at which a carton can be added
        if isinstance(firstPos, int):
            return False
        secondPos = self.findNoCollision(numpy.add(lowerLeft,[0,
                                            errorHeight + firstPos[1]-lowerLeft[1],0]),
                                         numpy.add(lowerRight,[0,
                                            errorHeight + firstPos[1]-lowerRight[1],0]), 
                                         cartonDimensions, stack, heightConscious)
        #then now just need to check if there is any space below to add a carton
        return secondPos

    #algorithm that iteratively moves pointers within a space range to check where a carton can be placed in the stack
    def findNoCollision(self, start, end, cartonDimensions, stack, heightConscious):
        initialStart = start
        # the required difference between the start and end positions before position is chosen
        threshold = 0.0001
        pointer = start
        distance = numpy.linalg.norm(numpy.add(end, numpy.negative(start)))
        while(distance > threshold):
            if(self.collisionOccurs(pointer, cartonDimensions, stack)):
                start = pointer
                pointer = numpy.dot(0.5, numpy.add(end, pointer))
            else:
                end = pointer
                pointer = numpy.dot(0.5, numpy.add(start, pointer))
            distance = numpy.linalg.norm(numpy.add(end, numpy.negative(start)))
        # if the new height is more than the initial max height create a new stack
        # i think i'll have to add in the dunnage factor as well to lower the height
        if heightConscious:
            if pointer[1] > self.initialMaxHeight + initialStart[1]:
                return False
        return pointer
        
    #checks to see if there is a collision between cartons in a stack
    def collisionOccurs(self, pointer, cartonDimensions, stack):
        lastStack = stack
        collision = False

        descendentList = lastStack.children
        meshFilter = lambda x : isinstance(x, Mesh)
        meshList = list(filter(meshFilter, descendentList))
        #the collision algorithm will only work for spherical objects because I want to 
        #compare the norms of vectors
        for mesh in meshList:
            meshPos = mesh.getPosition()
            meshDimensions = mesh.getDimensions()
            #x, y, then z
            if (self.cartonsOverlap(0.5* (meshDimensions[0]+cartonDimensions[0]), 
                                    abs(pointer[0]-meshPos[0])) and 
                self.cartonsOverlap(0.5*(meshDimensions[1]+cartonDimensions[1]), 
                                    abs(pointer[1]-meshPos[1])) and 
                self.cartonsOverlap(0.5*(meshDimensions[2]+cartonDimensions[2]), 
                                    abs(pointer[2]-meshPos[2]))):
                collision = True
                break

        return collision
            

    def getLastStack(self):
        return self.container.children[len(self.container.children)-1]

    #checks to see if the distance between the centres of cartons are below the minimum distance threshold
    def cartonsOverlap(self, distanceMin, distance):
        #affects the gap between cartons along the x-axis
        errorMargin = 0.001
        if distanceMin + errorMargin < distance:
            return False
        else:
            return True