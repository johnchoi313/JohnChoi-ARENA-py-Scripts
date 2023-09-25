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
    def __init__(self, scene, root, x, y): 
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
        PIECE_NAME = HEADER+"_Piece_"+str(team.name)+"_"+str(type.name)+"_["+str(self.X)+"]["+str(self.Y)+"]" 
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

            parent = self.tile,
            persist=True
        )
        self.scene.add_object(self.piece)

class ArenaChess:
    def __init__(self, scene):
        self.scene = scene
        self.initialized = False

        self.InitializeEverything()
        #self.DeleteEverything()

    def InitializeEverything(self):
        self.board = [[],[],[],[],[],[],[],[]]
        self.CreateRoot()
        self.CreateBoard()
        self.CreateLettersAndNumbers()
        self.CreateAllPieces()
        self.initialized = True
    def DeleteEverything(self):
        if(self.initialized):
            self.DeleteLettersAndNumbers()
            self.DeleteAllPieces()
            self.DeleteAllTiles()
            self.DeleteRoot()
            self.initialized = False
        else:
            printWarning("Can only delete everything after initialization! Not initialized yet...")

    def DeleteRoot(self):
        self.scene.delete_object(self.root)
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
                square = ChessSquare(scene, self.root, x, y)            
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

    
scene.run_tasks()