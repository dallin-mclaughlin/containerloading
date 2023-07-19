from core.base import Base
from core.renderer import Renderer
from states.create import CreateState
from states.main import MainState
from states.view import ViewState
from states.database import DatabaseState
from database.database import Database
from core.values import SCREEN_HEIGHT, SCREEN_WIDTH

#render a basic scene
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()

        #contains the list of states for the application
        self.stateDict = {  "MAIN" : MainState(self.renderer), "CREATE" : CreateState(self.renderer),
                            "VIEW" : ViewState(self.renderer), "DATABASE" : DatabaseState(self.renderer) }

        self.currentState = self.stateDict["MAIN"]

        Database().initialize()



    def update(self):
        self.currentState.update(self.input, self.deltaTime)

#instantiate this class and run the program
Test(screenSize=[SCREEN_WIDTH, SCREEN_HEIGHT]).run()