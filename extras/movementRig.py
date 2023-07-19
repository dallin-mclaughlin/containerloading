from core.object3D import Object3D

class MovementRig(Object3D):

    def __init__(self, unitsPerSecond=1, degreesPerSecond=60):

        #initialize base Object3D; controls movement and turn/left/right
        super().__init__()

        #initialize attached Object3D; controls look up/down
        self.lookAttachment = Object3D()
        self.children = [self.lookAttachment]
        self.lookAttachment.parent = self

        #control rate of movement
        self.unitsPerSecond = unitsPerSecond
        self.degreesPerSecond = degreesPerSecond

        #customizable key mappings
        # defaults: WASDRF (move), QE (turn), TG (look)
        self.KEY_MOVE_FORWARDS = "w"
        self.KEY_MOVE_BACKWARDS = "s"
        self.KEY_MOVE_LEFT = "a"
        self.KEY_MOVE_RIGHT = "d"
        self.KEY_MOVE_UP = "r"
        self.KEY_MOVE_DOWN = "f"
        self.KEY_TURN_LEFT = "q"
        self.KEY_TURN_RIGHT = "e"
        self.KEY_LOOK_UP = "t"
        self.KEY_LOOK_DOWN = "g"
        self.KEY_SHIFT = "shift"
        self.BUTTON_MOUSE_LEFT = 1

    #adding and removing objects applies to looks attachment; override functions from Object3D class
    def add(self, child):
        self.lookAttachment.add(child)

    def remove(self, child):
        self.lookAttachment.remove(child)

    def update(self, inputObject, deltaTime):
        moveAmount = self.unitsPerSecond * deltaTime
        rotateAmount = self.degreesPerSecond * (3.1415926 / 180) * deltaTime
        mouseClickMovementFactor = 0.05

        if inputObject.isKeyPressed(self.KEY_MOVE_FORWARDS):
            self.translate(0,0,-moveAmount)
        if inputObject.isKeyPressed(self.KEY_MOVE_BACKWARDS):
            self.translate(0,0,moveAmount)
        if inputObject.isKeyPressed(self.KEY_MOVE_LEFT):
            self.translate(-moveAmount, 0, 0)
        if inputObject.isKeyPressed(self.KEY_MOVE_RIGHT):
            self.translate(moveAmount, 0, 0)
        if inputObject.isKeyPressed(self.KEY_MOVE_UP):
            self.translate(0, moveAmount, 0)
        if inputObject.isKeyPressed(self.KEY_MOVE_DOWN):
            self.translate(0, -moveAmount, 0)
        
        if inputObject.isKeyPressed(self.KEY_TURN_RIGHT):
            self.rotateY(-rotateAmount)
        if inputObject.isKeyPressed(self.KEY_TURN_LEFT):
            self.rotateY(rotateAmount)

        if inputObject.isKeyPressed(self.KEY_LOOK_UP):
            self.lookAttachment.rotateX(rotateAmount)
        if inputObject.isKeyPressed(self.KEY_LOOK_DOWN):
            self.lookAttachment.rotateX(-rotateAmount)

        if inputObject.isKeyPressed(self.BUTTON_MOUSE_LEFT) and not inputObject.hoverPanel:
            mousePosDifference = tuple(map(lambda x, y: x - y, 
                                    inputObject.previousMousePos, inputObject.currentMousePos))
            self.rotateY(-mousePosDifference[0] * rotateAmount * mouseClickMovementFactor)
            self.lookAttachment.rotateX(-mousePosDifference[1] * rotateAmount * mouseClickMovementFactor)