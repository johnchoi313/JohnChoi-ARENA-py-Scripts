# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from config import *
from ColorPrinter import *
from enum import Enum

from arena import *


HEADER = "Chess"

# ------------------------------------------ #
# ----------MAIN CHESS MASTERCLASS---------- #
# ------------------------------------------ #

class ChessPieceTeam(Enum):
    WHITE = 1
    BLACK = 2

class ChessPieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class ChessSquare:
    def __init__(self, scene, root, x, y):
 
        self.scene = scene
        self.root = root

        self.X = x
        self.Y = y

    def CreateTile(self, x, y):
        SQUARE_COLOR = Color(50,50,50)
        if(x % 2 != y % 2): # Alternating black/white square 
            SQUARE_COLOR = Color(255,255,255)
        if(x == 0 and y == 0): # Mark A1(0,0) green
            SQUARE_COLOR = Color(0,255,0)
        if(x == 7 and y == 7): # Mark H8(7,7) blue
            SQUARE_COLOR = Color(0,0,255)

        square = Box(
            object_id=HEADER+"_Board_["+chr(x+65)+"]["+str(y+1)+"]",
            color=SQUARE_COLOR,
            
            depth=.8,
            width=.8,
            height=.2,

            scale=Scale(1,1,1),
            position=Position(x-3.5,0,3.5-y),
            rotation=Rotation(0,0,0),

            parent = self.root,
            persist=True
        )
        self.scene.add_object(square)

    def CreatePiece(self, tile, team, type, x, y):

        FILEPATH = "store/users/johnchoi/Chess/" #Path
        FILESTORE = "https://arenaxr.org/" #main server

        #team = black, white
        #type = pawn, rook, knight, bishop, queen, king 

        PIECE_URL = ""

        if(team == ChessPieceTeam.WHITE):

            if(type == ChessPieceType.PAWN):
                PIECE_URL = FILEPATH+FILESTORE+"white_pawn.glb"

            if(type == ChessPieceType.KNIGHT):
                PIECE_URL = FILEPATH+FILESTORE+"white_knight.glb"

            if(type == ChessPieceType.BISHOP):
                PIECE_URL = FILEPATH+FILESTORE+"white_bishop.glb"

            if(type == ChessPieceType.ROOK):
                PIECE_URL = FILEPATH+FILESTORE+"white_rook.glb"

            if(type == ChessPieceType.QUEEN):
                PIECE_URL = FILEPATH+FILESTORE+"white_queen.glb"

            if(type == ChessPieceType.KING):
                PIECE_URL = FILEPATH+FILESTORE+"white_king.glb"

        elif(team == ChessPieceTeam.BLACK):
            if(type == ChessPieceType.PAWN):
                PIECE_URL = FILEPATH+FILESTORE+"black_pawn.glb"

            if(type == ChessPieceType.KNIGHT):
                PIECE_URL = FILEPATH+FILESTORE+"black_knight.glb"

            if(type == ChessPieceType.BISHOP):
                PIECE_URL = FILEPATH+FILESTORE+"black_bishop.glb"

            if(type == ChessPieceType.ROOK):
                PIECE_URL = FILEPATH+FILESTORE+"black_rook.glb"

            if(type == ChessPieceType.QUEEN):
                PIECE_URL = FILEPATH+FILESTORE+"black_queen.glb"

            if(type == ChessPieceType.KING):
                PIECE_URL = FILEPATH+FILESTORE+"black_king.glb"


        ID = ""
        URL = ""

        piece = GLTF(
            object_id=HEADER+"_Board_["+str(x)+"]["+str(y)+"]",
            url=NPC_GLTF_URL,
            scale=Scale(1,1,1),
            
            color=SQUARE_COLOR,
            
            depth=.8,
            width=.8,
            height=.2,

            position=Position(x-3,0,y-3),
            rotation=Rotation(0,0,0),

            parent = self.tile,
            persist=True
        )

        self.scene.add_object(piece)




class ArenaChess:
    def __init__(self, scene):
        self.scene = scene
        self.board = [[],[],[],[],[],[],[],[]]

        self.CreateRoot()
        
        self.CreateBoard()

        self.CreateLettersAndNumbers()


    def CreateRoot(self):
        self.root = Box(
            object_id=HEADER+"_Root",

            material = Material( color=Color(255,0,0), opacity=0.1, transparent=True, visible=True),

            scale=Scale(1,1,1),
            position=Position(0,0,0),
            rotation=Rotation(0,0,0),

            persist=True
        )
        self.scene.add_object(self.root)

    def CreateLettersAndNumbers(self):
        #Create letters
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
        #Create numbers
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

    def CreateBoard(self):
        for x in range(8):
            for y in range(8):
                SQUARE_COLOR = Color(50,50,50)
                if(x % 2 != y % 2): # Alternating black/white square 
                    SQUARE_COLOR = Color(255,255,255)
                if(x == 0 and y == 0): # Mark A1(0,0) green
                    SQUARE_COLOR = Color(0,255,0)
                if(x == 7 and y == 7): # Mark H8(7,7) blue
                    SQUARE_COLOR = Color(0,0,255)

                square = Box(
                    object_id=HEADER+"_Board_["+chr(x+65)+"]["+str(y+1)+"]",
                    color=SQUARE_COLOR,
                    
                    depth=.8,
                    width=.8,
                    height=.2,

                    scale=Scale(1,1,1),
                    position=Position(x-3.5,0,3.5-y),
                    rotation=Rotation(0,0,0),

                    parent = self.root,
                    persist=True
                )
                self.scene.add_object(square)
                
                self.board[x].append(square)
                
                


# ------------------------------------------ #
# --------MAIN LOOPS/INITIALIZATION--------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

arenaChess = ArenaChess(scene)

#@scene.run_once
#def ProgramStart():

    
scene.run_tasks()