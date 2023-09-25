# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from config import *
from ColorPrinter import *
from enum import Enum

from arena import *

HEADER = "Chess"

class ChessPieceTeam(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

class ChessPieceType(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

# ------------------------------------------ #
# ----------MAIN CHESS MASTERCLASS---------- #
# ------------------------------------------ #

class ChessSquare:
    def __init__(self, scene, root, x, y, clickHandler): 
        self.clickHandler = clickHandler
        self.team = ChessPieceTeam.NONE
        self.type = ChessPieceType.NONE
        self.scene = scene
        self.root = root
        self.X = x
        self.Y = y
        self.CreateTile()

    def DeleteTile(self):
        if(self.tile is not None):
            self.scene.delete_object(self.tile)

    def CreateTile(self):
        x = self.X
        y = self.Y

        SQUARE_COLOR = Color(50,50,50)
        if(x % 2 != y % 2): # Alternating black/white square 
            SQUARE_COLOR = Color(255,255,255)
        if(x == 0 and y == 0): # Mark A1(0,0) green
            SQUARE_COLOR = Color(0,255,0)
        if(x == 7 and y == 7): # Mark H8(7,7) blue
            SQUARE_COLOR = Color(0,0,255)

        self.tile = Box(
            object_id=HEADER+"_Board_["+chr(x+65)+"]["+str(y+1)+"]",
            color=SQUARE_COLOR,
            
            depth=.9,
            width=.9,
            height=.2,

            scale=Scale(1,1,1),
            position=Position(x-3.5,0,3.5-y),
            rotation=Rotation(0,0,0),

            evt_handler=self.clickHandler,
            clickable = True,

            parent = self.root,
            persist=True
        )
        self.scene.add_object(self.tile)




    def DeletePiece(self):
        if(self.team == ChessPieceTeam.NONE or self.type == ChessPieceType.NONE):
            return

        self.scene.delete_object(self.piece)

        self.team = ChessPieceTeam.NONE
        self.type = ChessPieceType.NONE

    def CreatePiece(self, team, type):
        FILESTORE = "https://arenaxr.org/" #main server
        FILEPATH = "store/users/johnchoi/Chess/" #Path
        
        if(team == ChessPieceTeam.NONE or type == ChessPieceType.NONE):
            printError("Error: Cannot create piece with team NONE or type NONE!")
            return

        self.team = team
        self.type = type

        #team = black, white
        #type = pawn, rook, knight, bishop, queen, king 
        PIECE_NAME = HEADER+"_Piece_"+str(team.name)+"_"+str(type.name)+"_["+chr(self.X+65)+"]["+str(self.Y+1)+"]" 
        PIECE_URL = ""
        if(team == ChessPieceTeam.WHITE):
            if(type == ChessPieceType.PAWN):
                PIECE_URL = FILESTORE+FILEPATH+"white_pawn.glb"
            if(type == ChessPieceType.KNIGHT):
                PIECE_URL = FILESTORE+FILEPATH+"white_knight.glb"
            if(type == ChessPieceType.BISHOP):
                PIECE_URL = FILESTORE+FILEPATH+"white_bishop.glb"
            if(type == ChessPieceType.ROOK):
                PIECE_URL = FILESTORE+FILEPATH+"white_rook.glb"
            if(type == ChessPieceType.QUEEN):
                PIECE_URL = FILESTORE+FILEPATH+"white_queen.glb"
            if(type == ChessPieceType.KING):
                PIECE_URL = FILESTORE+FILEPATH+"white_king.glb"
        elif(team == ChessPieceTeam.BLACK):
            if(type == ChessPieceType.PAWN):
                PIECE_URL = FILESTORE+FILEPATH+"black_pawn.glb"
            if(type == ChessPieceType.KNIGHT):
                PIECE_URL = FILESTORE+FILEPATH+"black_knight.glb"
            if(type == ChessPieceType.BISHOP):
                PIECE_URL = FILESTORE+FILEPATH+"black_bishop.glb"
            if(type == ChessPieceType.ROOK):
                PIECE_URL = FILESTORE+FILEPATH+"black_rook.glb"
            if(type == ChessPieceType.QUEEN):
                PIECE_URL = FILESTORE+FILEPATH+"black_queen.glb"
            if(type == ChessPieceType.KING):
                PIECE_URL = FILESTORE+FILEPATH+"black_king.glb"

        self.piece = GLTF(
            object_id=PIECE_NAME,
            url=PIECE_URL,
            
            position=Position(0,0.1,0),
            rotation=Rotation(0,-90,0),
            scale=Scale(.2,.2,.2),

            evt_handler=self.clickHandler,
            clickable = True,


            parent = self.tile,
            persist=True
        )
        self.scene.add_object(self.piece)




class ArenaChess:
    def __init__(self, scene):
        self.scene = scene
        self.initialized = False


        self.moveStep = 0
        self.pointer = None
        self.selection = None
        self.destination = None
        self.selectionCylinder = None
        self.destinationCylinder = None

        self.actionReady = False
        self.actionX = 0
        self.actionY = 0

        self.InitializeEverything()
        #self.DeleteEverything()

    def InitializeEverything(self):
        self.board = [[],[],[],[],[],[],[],[]]
    
        self.CreateRoot()
        self.CreateBoard()
        self.CreateLettersAndNumbers()
        self.CreateAllPieces()
        self.CreateUI()
        self.initialized = True
        
    def DeleteEverything(self):
        if(self.initialized):
            self.DeleteLettersAndNumbers()
            
            self.DeletePointerCylinders()

            self.DeleteAllPieces()

            self.DeleteAllTiles()

            self.DeleteUI()
            
            self.DeleteRoot()
            
            self.initialized = False
        else:
            printWarning("Can only delete everything after initialization! Not initialized yet...")




    def DeletePointerCylinders(self):
        if(self.pointer is not None):
            self.scene.delete_object(self.pointer)
        if(self.selectionCylinder is not None):
            self.scene.delete_object(self.selectionCylinder)
        if(self.destinationCylinder is not None):
            self.scene.delete_object(self.destinationCylinder)
        self.selection = None
        self.destination = None


    
    def CreatePointer(self, x, y):
        tile = self.board[x][y].tile

        self.pointer = Cone(
            object_id=HEADER+"_Pointer",
            material = Material(color=Color(255,0,255), opacity=0.7, transparent=True, visible=True),

            scale=Scale(.1,.15,.1),
            position=Position(0,1.3,0),
            rotation=Rotation(180,0,0),
            
            parent = tile,
            persist=True        
        )
        self.scene.add_object(self.pointer)



    def CreateSelection(self, x, y):
        tile = self.board[x][y].tile

        self.selection = self.board[x][y]


        self.selectionCylinder = Cylinder(
            object_id=HEADER+"_Selection",
            material = Material(color=Color(0,0,255), opacity=0.2, transparent=True, visible=True),

            scale=Scale(.3,1.1,.3),
            position=Position(0,.55,0),
            rotation=Rotation(0,0,0),
            
            parent = tile,
            persist=True        
        )
        self.scene.add_object(self.selectionCylinder)


    def CreateDestination(self, x, y):
        tile = self.board[x][y].tile

        self.destination = self.board[x][y]

        self.destinationCylinder = Cylinder(
            object_id=HEADER+"_Destination",
            material = Material(color=Color(0,255,255), opacity=0.2, transparent=True, visible=True),

            scale=Scale(.3,1.1,.3),
            position=Position(0,.55,0),
            rotation=Rotation(0,0,0),
            
            parent = tile,
            persist=True        
        )
        self.scene.add_object(self.destinationCylinder)





    def getX(self,text):
        printLightYellow(text[-5])
        return ord(text[-5])-65
    def getY(self,text):
        printLightYellow(text[-2])
        return int(text[-2])-1

    def ClickHandler(self, scene, evt, msg):
        if evt.type == "mousedown":

            printLightGreen(str(msg))
            printLightCyan(str(evt.data))
            printLightYellow(msg["object_id"])


            self.actionReady = True
    
            self.actionX = self.getX(msg["object_id"])
            self.actionY = self.getY(msg["object_id"])

            self.RunClickAction()


    def RunClickAction(self):

        self.actionReady = False

        x = self.actionX
        y = self.actionY

        print("X = " + str(x))      
        print("Y = " + str(y))      

        printCyanB("MoveStep = " + str(self.moveStep))

        self.CreatePointer(x,y)

        if(self.moveStep % 3 == 0):

            if(self.board[x][y].team is not ChessPieceTeam.NONE and 
               self.board[x][y].type is not ChessPieceType.NONE):
                self.CreateSelection(x,y)            
                self.moveStep = 1
    
        elif(self.moveStep % 3 == 1):
            if(self.selection.X != x or self.selection.Y != y):
                self.CreateDestination(x,y)            
                self.moveStep = 2
                self.CreateActionConfirmationPrompt()


    def CreateActionConfirmationPrompt(self, buttons):
        self.prompt = Prompt(
            object_id=HEADER + "_ConfirmationPrompt",
            look_at="#my-camera",
            
            title="Confirmation",
            description="Are you sure you want to do this?",
            
            buttons=["Yes","No"],
            
            fontSize = 0.05,
       
            evt_handler=self.prompt_handler,
                
            position=Position(0,2,0),
            rotation=Rotation(0,90,0),
            scale=Scale(1,1,1),
            
            parent=self.root,
            persist = True
        )
        self.scene.add_object(self.prompt)

      
    def prompt_handler(self, scene, evt, msg):
        if evt.type == "buttonClick":
            if(evt.data.buttonName == "Yes"):
                print("Pressed confirmation button: " + evt.data.buttonName)
                scene.delete_object(self.prompt)

                self.moveStep = 0

                self.destination.DeletePiece()
                self.destination.CreatePiece(self.selection.team, self.selection.type)
                self.selection.DeletePiece()

                self.DeletePointerCylinders()

            if(evt.data.buttonName == "No"):
                print("Pressed confirmation button: " + evt.data.buttonName)
                scene.delete_object(self.prompt)
                
                self.moveStep = 0

                self.DeletePointerCylinders()


    def CreateActionConfirmationPrompt(self):
        self.prompt = Prompt(
            object_id=HEADER + "_ConfirmationPrompt",
            look_at="#my-camera",
            
            title="Confirmation",
            description="Are you sure you want to make this move?",
            
            buttons=["Yes","No"],
            
            fontSize = 0.05,
       
            evt_handler=self.prompt_handler,
                
            position=Position(0,2,0),
            rotation=Rotation(0,90,0),
            scale=Scale(1,1,1),
            
            parent=self.root,
            persist = True
        )
        self.scene.add_object(self.prompt)


    def UI_handler(self, scene, evt, msg):
        if evt.type == "buttonClick":
            if(evt.data.buttonName == "Reset Game"):
                print("Pressed confirmation button: " + evt.data.buttonName)
                self.DeleteEverything()
                self.InitializeEverything()


            if(evt.data.buttonName == "Clear Chess"):
                print("Pressed confirmation button: " + evt.data.buttonName)
                self.DeleteEverything()



    def DeleteUI(self):
        printBlue("UI Deleted!")
        if(self.Card is not None):
            self.scene.delete_object(self.Card)
        if(self.ButtonPanel is not None):
            self.scene.delete_object(self.ButtonPanel)


    def CreateUI(self):
        printBlue("UI Created!")

        self.Card = Card(
            object_id=HEADER + "_Card",
            #look_at="#my-camera",
            
            title="ARENA Chess!",
            

            body="Play Chess in ARENA!",
            bodyAlign="center",
            
            font="Roboto-Mono",
            fontSize = 0.15,
       
            #widthScale=1.25,
            
            position=Position(4.5,2.8,0),
            rotation=Rotation(0,-90,0),
            scale=Scale(1,1,1),
            
            parent=self.root,
            persist = True
        )
        self.scene.add_object(self.Card)

        self.UndoRedoPanel = ButtonPanel(
            object_id=HEADER + "_UndoRedoPanel",
            
            title="Undo or Redo",
            
            font="Roboto-Mono",
            fontSize = 0.5,
       
            buttons=["Undo","Redo"],
        
            widthScale=1,
            
            #evt_handler=self.UI_handler,
                
            position=Position(4.5,1.7,0),
            rotation=Rotation(0,-90,0),
            scale=Scale(1.2,1.2,1.2),
            
            parent=self.root,
            persist = True
        )
        self.scene.add_object(self.UndoRedoPanel)

        self.ButtonPanel = ButtonPanel(
            object_id=HEADER + "_ButtonPanel",
            #look_at="#my-camera",
            
            title="00:00",
            
            description="Chess UI",

            body="Please applaud",
            bodyAlign="center",
            
            font="Roboto-Mono",
            fontSize = 0.5,
       
            buttons=["Reset Game","Clear Chess"],
        
            widthScale=1,
            
            evt_handler=self.UI_handler,
                
            position=Position(4.5,1,0),
            rotation=Rotation(0,-90,0),
            scale=Scale(1.2,1.2,1.2),
            
            parent=self.root,
            persist = True
        )
        self.scene.add_object(self.ButtonPanel)


    def DeleteRoot(self):
        self.scene.delete_object(self.root)
    def CreateRoot(self):
        self.root = Box(
            object_id=HEADER+"_Root",
            material = Material( color=Color(255,0,0), opacity=0.1, transparent=True, visible=False),

            scale=Scale(1,1,1),
            position=Position(0,0,0),
            rotation=Rotation(0,0,0),

            persist=True
        )
        self.scene.add_object(self.root)





    def DeleteLettersAndNumbers(self):
        if(self.letters is not None):
            for letter in self.letters:
                self.scene.delete_object(letter)
        if(self.numbers is not None):
            for number in self.numbers:
                self.scene.delete_object(number)
    def CreateLettersAndNumbers(self):
        #Create letters
        self.letters = []
        for x in range(8): 
            letter = Text(
                object_id=HEADER+"_LabelLetter_["+chr(x+65)+"]",
                text=chr(x+65),
                align="center",
                font="exo2bold",

                position=Position(x-3.5,.1,4.2),
                rotation=Rotation(-90,0,0),
                scale=Scale(1.5,1.5,1.5),
                color=Color(0,250,0),
        
                parent = self.root,
                persist=True
            )
            self.scene.add_object(letter)
            self.letters.append(letter)
        #Create numbers
        self.numbers = []        
        for y in range(8):
            number = Text(
                object_id=HEADER+"_LabelNumber_["+str(y+1)+"]",
                text=str(y+1),
                align="center",

                position=Position(-4.2,.1,3.5-y),
                rotation=Rotation(-90,0,0),
                scale=Scale(1.5,1.5,1.5),                
                color=Color(0,250,0),

                parent = self.root,
                persist=True
            )
            self.scene.add_object(number)
            self.numbers.append(number)


    def DeleteAllTiles(self):
        for x in range(8):
            for y in range(8):
                self.board[x][y].DeleteTile()
    def CreateBoard(self):
        for x in range(8):
            for y in range(8):
                square = ChessSquare(scene, self.root, x, y, self.ClickHandler)            
                self.board[x].append(square)


    def DeleteAllPieces(self):
        for x in range(8):
            for y in range(8):
                self.board[x][y].DeletePiece()
    def CreateAllPieces(self):
        #White pieces
        self.board[0][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.ROOK)
        self.board[1][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.KNIGHT)
        self.board[2][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.BISHOP)
        self.board[3][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.QUEEN)
        self.board[4][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.KING)
        self.board[5][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.BISHOP)
        self.board[6][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.KNIGHT)
        self.board[7][0].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.ROOK)
        for x in range(8):
            self.board[x][1].CreatePiece(ChessPieceTeam.WHITE, ChessPieceType.PAWN)
        #Black pieces
        self.board[0][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.ROOK)
        self.board[1][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.KNIGHT)
        self.board[2][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.BISHOP)
        self.board[3][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.QUEEN)
        self.board[4][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.KING)
        self.board[5][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.BISHOP)
        self.board[6][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.KNIGHT)
        self.board[7][7].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.ROOK)

        for x in range(8):
            self.board[x][6].CreatePiece(ChessPieceTeam.BLACK, ChessPieceType.PAWN)
                
# ------------------------------------------ #
# --------MAIN LOOPS/INITIALIZATION--------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

arenaChess = ArenaChess(scene)

#@scene.run_once
#def ProgramStart():

#@scene.run_forever(interval_ms=100)
#def RunActionLoop(): #checks whether or not a user is in range of NPC
#    if(arenaChess.actionReady):
#        arenaChess.RunClickAction()

scene.run_tasks()