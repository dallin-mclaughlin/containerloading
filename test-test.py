from tkinter import Grid
from core.base import Base
from core.renderer import Renderer
from states.create import CreateState
from states.main import MainState
from states.view import ViewState
from states.database import DatabaseState
from core.values import SCREEN_HEIGHT, SCREEN_WIDTH
import sqlite3

#render a basic scene
class Test(Base):

    def initialize(self):

        #self.initializeDatabase()
        print("Initializing program...")
        self.renderer = Renderer()

        #contains the list of states for the application
        self.stateDict = {  "MAIN" : MainState(self.renderer), "CREATE" : CreateState(self.renderer),
                            "VIEW" : ViewState(self.renderer), "DATABASE" : DatabaseState(self.renderer) }

        self.currentState = self.stateDict["MAIN"]

        

    def initializeDatabase(self):
        con = sqlite3.connect('database/database.db')
        con.execute("PRAGMA foreign_keys = 1")

        cur = con.cursor()

        cur.execute('''CREATE TABLE cartons (carton TEXT PRIMARY KEY, width INTEGER, height INTEGER, length INTEGER)''')
        cur.execute('''INSERT INTO cartons VALUES ('A454', 430, 170, 680)''')
        cur.execute('''INSERT INTO cartons VALUES ('A475', 210, 150, 560)''')
        cur.execute('''INSERT INTO cartons VALUES ('A477', 405, 205, 540)''')
        cur.execute('''INSERT INTO cartons VALUES ('A478', 200, 210, 540)''')
        cur.execute('''INSERT INTO cartons VALUES ('A497', 310, 105, 360)''')
        cur.execute('''INSERT INTO cartons VALUES ('A500', 250, 115, 360)''')
        cur.execute('''INSERT INTO cartons VALUES ('C115', 355, 115, 525)''')
        cur.execute('''INSERT INTO cartons VALUES ('C149', 355, 150, 525)''')
        cur.execute('''INSERT INTO cartons VALUES ('C174', 355, 175, 525)''')
        cur.execute('''INSERT INTO cartons VALUES ('C205', 355, 205, 525)''')

        cur.execute('''CREATE TABLE containers (container TEXT PRIMARY KEY, width INTEGER, height INTEGER, length INTEGER)''')
        cur.execute('''INSERT INTO containers VALUES ('TWENTY', 2300, 2100, 5300)''')
        cur.execute('''INSERT INTO containers VALUES ('FORTY', 2300, 2100, 11300)''')

        cur.execute('''CREATE TABLE itemcodes (itemcode TEXT PRIMARY KEY, carton TEXT, FOREIGN KEY (carton) REFERENCES cartons (carton))''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14009', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14016', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14031', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14113', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14243', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14244', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14245', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14246', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14247', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14285', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14286', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('14287', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24450', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24454', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24457', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24458', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24459', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24460', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24462', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24500', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24502', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24503', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24504', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24505', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('24506', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35530', 'A454')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35531', 'A454')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35535', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35538', 'A475')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35540', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35541', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35550', 'A454')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35560', 'A475')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35562', 'A475')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35568', 'A475')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35571', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35580', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('35590', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('37571', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('37590', 'A497')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44602', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44608', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44612', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44618', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44670', 'A500')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44671', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44672', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44673', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44730', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44731', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44732', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44733', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44756', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44760', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44783', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44784', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44810', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44812', 'A500')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44911', 'A477')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('44912', 'A477')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('45252', 'A454')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('46632', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('46644', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('48658', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('48660', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('48668', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('59758', 'A478')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('62521', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('70950', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('71350', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('71850', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('72250', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('72350', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('73250', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('73350', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('73450', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('74250', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('82350', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('91364', 'C174')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98516', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98518', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98530', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98531', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98533', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98536', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98546', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('98612', 'C149')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('99090', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('99092', 'C115')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('99137', 'C205')''')
        cur.execute('''INSERT INTO itemcodes VALUES ('99173', 'C174')''')

        con.commit()

        con.close()



    def update(self):
        self.currentState.update(self.input, self.deltaTime)

#instantiate this class and run the program
Test(screenSize=[SCREEN_WIDTH, SCREEN_HEIGHT]).run()