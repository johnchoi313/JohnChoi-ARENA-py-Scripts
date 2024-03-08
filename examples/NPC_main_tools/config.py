from ColorPrinter import *
from arena import *
import json

#DEVELOPER DEBUG SETTINGS
USE_DEV_ARENAPY = False
ARENAPY_DEV_PATH = "D:/Github/arena-py/"  # Linux/Mac (Civilized)
ARENAPY_DEV_PATH = "D:\\Github\\arena-py" # Windows   (Uncivilized)

USE_DEV_SERVER = False
if(USE_DEV_SERVER):
    HOST = "arena-dev1.conix.io" #dev server
if(USE_DEV_SERVER):
    FILESTORE = "https://arena-dev1.conix.io/" #dev server

PRINT_VERBOSE = False

# CLI ARGUMENT: CONFIG (Contains path to dialogue file, mappings file, and various settings)
CONFIG_FILENAME = "config.json"

# Open config file
f = open(CONFIG_FILENAME)
jsonString = f.read()
configJson = json.loads(jsonString) 


def ToPosition(json):
    return Position(json["x"],json["y"],json["z"])
def ToRotation(json):
    return Rotation(json["x"],json["y"],json["z"])
def ToScale(json):
    return Scale(json["x"],json["y"],json["z"])
def ToColor(json):
    return Color(json["r"],json["g"],json["b"])



#GET DIALOGUE AND MAPPINGS FILENAMES
DIALOGUE_FILENAME = configJson["DIALOGUE_FILENAME"] #"robot_arena.json"
MAPPINGS_FILENAME = configJson["MAPPINGS_FILENAME"] #"mappings.json"

#ARENA CONNECTION
HOST = configJson["HOST"]           #"arenaxr.org"      
NAMESPACE = configJson["NAMESPACE"] #"johnchoi"
SCENE = configJson["SCENE"]         #"arena"

#NPC (name Alphanumeric only plus '_', no spaces!)
NPC_NAME = configJson["NPC_NAME"]         #"NPC_RobotBuddy"
NPC_GLTF_URL = configJson["NPC_GLTF_URL"] #"https://arenaxr.org/store/users/johnchoi/Characters/RobotBuddy/RobotBuddyBlue.glb"
NPC_ICON_URL = configJson["NPC_ICON_URL"] #"https://arenaxr.org/store/users/johnchoi/Characters/RobotBuddy/RobotBuddyBlue.png"

#ENTER/EXIT SPECIAL EVENT NODES 
ENTER_NODE = configJson["ENTER_NODE"] #"Enter"
EXIT_NODE = configJson["EXIT_NODE"]   #"Exit"

#NO ACTIVITY RESET
RESET_INTERVAL = configJson["RESET_INTERVAL"] #100
RESET_TIME = configJson["RESET_TIME"] #5*60000 #x min of no activity resets interaction.

#MISCELLANEOUS
TRANSFORM_INTERVAL = configJson["TRANSFORM_INTERVAL"] #500
TRANSFORM_TIMER = configJson["TRANSFORM_TIMER"]       #3000

#UI
USE_NAME_AS_TITLE = configJson["USE_NAME_AS_TITLE"]       #False
UI_THEME = configJson["UI_THEME"]                         #"light" or "dark"
UI_VERTICAL_BUTTONS = configJson["UI_VERTICAL_BUTTONS"]   #True
UI_SPEECH_FONT_SIZE = configJson["UI_SPEECH_FONT_SIZE"]   #0.05
UI_SPEECH_TEXT_WIDTH = configJson["UI_SPEECH_TEXT_WIDTH"] #0.5
UI_SPEECH_ICON_WIDTH = configJson["UI_SPEECH_ICON_WIDTH"] #0.5
UI_SPEECH_ICON_FILL = configJson["UI_SPEECH_ICON_FILL"]   #cover, contain, stretch

#USE DEFAULT ACTIONS
USE_DEFAULT_ANIMATIONS = configJson["USE_DEFAULT_ANIMATIONS"] #True
USE_DEFAULT_MORPHS = configJson["USE_DEFAULT_MORPHS"]         #True
USE_DEFAULT_SOUNDS = configJson["USE_DEFAULT_SOUNDS"]         #True

#NPC ROOT TRANSFORM
ROOT_PARENT = configJson["ROOT_PARENT"]     #"" or "marker1"
ROOT_SCALE = ToScale(configJson["ROOT_SCALE"])       #Scale(0.8,0.8,0.8)
ROOT_SIZE = configJson["ROOT_SIZE"]         #0.2
ROOT_POSITION = ToPosition(configJson["ROOT_POSITION"]) #Position(7.2, 0.0, -2.8) #This is the start position
ROOT_ROTATION = ToRotation(configJson["ROOT_ROTATION"]) #Rotation(0,0,0)
ROOT_COLOR = ToColor(configJson["ROOT_COLOR"])       #Color(255,100,16)
ROOT_OPACITY = configJson["ROOT_OPACITY"]   #0.5

#NPC GLTF TRANSFORM
GLTF_SCALE = ToScale(configJson["GLTF_SCALE"])       #Scale(1,1,1)
GLTF_POSITION = ToPosition(configJson["GLTF_POSITION"]) #Position(0,0,0)
GLTF_ROTATION = ToRotation(configJson["GLTF_ROTATION"]) #Rotation(0,180,0) 

#NPC PLANE SETTINGS (for both images and videos)
PLANE_SIZE = configJson["PLANE_SIZE"]                  #1.2
PLANE_SIZE_DURATION = configJson["PLANE_SIZE_DURATION"] #500
PLANE_POSITION = ToPosition(configJson["PLANE_POSITION"])             #Position(1.5,0.8,0)
PLANE_ROTATION = ToRotation(configJson["PLANE_ROTATION"])             #Rotation(0,-15,0) 
PLANE_OPACITY = configJson["PLANE_OPACITY"]               #0.9

#SPEECH SETTINGS
SPEECH_INTERVAL = configJson["SPEECH_INTERVAL"] #100
SPEECH_SPEED = configJson["SPEECH_SPEED"]       #3

SPEECH_TEXT_COLOR = configJson["SPEECH_TEXT_COLOR"]       #Color(250,100,250)
SPEECH_TEXT_POSITION = configJson["SPEECH_TEXT_POSITION"] #Position(0,1.6,0)
SPEECH_TEXT_SCALE = configJson["SPEECH_TEXT_SCALE"]       #Scale(0.6,0.7,0.7)

SPEECH_BUBBLE_POSITION = ToPosition(configJson["SPEECH_BUBBLE_POSITION"]) #Position(0,1.7,0)
SPEECH_BUBBLE_ROTATION = ToRotation(configJson["SPEECH_BUBBLE_ROTATION"]) #Rotation(0,5,0)
SPEECH_BUBBLE_SCALE = ToScale(configJson["SPEECH_BUBBLE_SCALE"])       #Scale(1,1,1)

#CHOICE SETTINGS
CHOICE_TEXT_COLOR = ToColor(configJson["CHOICE_TEXT_COLOR"])         #Color(255,255,255)
CHOICE_BUBBLE_COLOR = ToColor(configJson["CHOICE_BUBBLE_COLOR"])     #Color(0,0,200)
CHOICE_BUBBLE_OPACITY = configJson["CHOICE_BUBBLE_OPACITY"] #0.5

CHOICE_BUBBLE_POSITION = ToPosition(configJson["CHOICE_BUBBLE_POSITION"]) #Position(-0.95,0.6,0.4)
CHOICE_BUBBLE_ROTATION = ToRotation(configJson["CHOICE_BUBBLE_ROTATION"]) #Rotation(0,15,0)
CHOICE_BUBBLE_OFFSET_Y = configJson["CHOICE_BUBBLE_OFFSET_Y"] #0.25

CHOICE_BUBBLE_SCALE = ToScale(configJson["CHOICE_BUBBLE_SCALE"])     #Scale(0.8, 0.8, 0.8)
CHOICE_TEXT_SCALE = ToScale(configJson["CHOICE_TEXT_SCALE"])        #Scale(0.4, 2, .5)

#URL SETTINGS
LINK_TEXT_COLOR = ToColor(configJson["LINK_TEXT_COLOR"])         #Color(255,255,255)
LINK_BUBBLE_COLOR = ToColor(configJson["LINK_BUBBLE_COLOR"])     #Color(0,200,100)
LINK_BUBBLE_OPACITY = configJson["LINK_BUBBLE_OPACITY"] #0.8

LINK_BUBBLE_POSITION = ToPosition(configJson["LINK_BUBBLE_POSITION"]) #Position(0,0.8,0.7)
LINK_BUBBLE_ROTATION = ToRotation(configJson["LINK_BUBBLE_ROTATION"]) #Rotation(0,0,0)
LINK_BUBBLE_SCALE = ToScale(configJson["LINK_BUBBLE_SCALE"])       #Scale(1.5, 0.2, 0.08)
LINK_TEXT_SCALE = ToScale(configJson["LINK_TEXT_SCALE"])           #Scale(0.2, 2, .5)