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
DIALOGUE_FILENAME = configJson["FILENAME"]["DIALOGUE"] #"robot_arena.json"
MAPPINGS_FILENAME = configJson["FILENAME"]["MAPPINGS"] #"mappings.json"

#ARENA CONNECTION
HOST = configJson["ARENA"]["HOST"]           #"arenaxr.org"      
NAMESPACE = configJson["ARENA"]["NAMESPACE"] #"johnchoi"
SCENE = configJson["ARENA"]["SCENE"]         #"arena"

#ENTER/EXIT SPECIAL EVENT NODES 
ENTER_NODE = configJson["NODE"]["ENTER"] #"Enter"
EXIT_NODE = configJson["NODE"]["EXIT"]   #"Exit"

#NPC (name Alphanumeric only plus '_', no spaces!)
NPC_NAME = configJson["NPC"]["NAME"]         #"NPC_RobotBuddy"
NPC_GLTF_URL = configJson["NPC"]["GLTF_URL"] #"https://arenaxr.org/store/users/johnchoi/Characters/RobotBuddy/RobotBuddyBlue.glb"
NPC_ICON_URL = configJson["NPC"]["ICON_URL"] #"https://arenaxr.org/store/users/johnchoi/Characters/RobotBuddy/RobotBuddyBlue.png"

#USE DEFAULT ACTIONS
USE_DEFAULT_ANIMATIONS = configJson["USE_DEFAULTS"]["ANIMATIONS"] #True
USE_DEFAULT_MORPHS = configJson["USE_DEFAULTS"]["MORPHS"]         #True
USE_DEFAULT_SOUNDS = configJson["USE_DEFAULTS"]["SOUNDS"]         #True


#NO ACTIVITY RESET TIMER
RESET_INTERVAL = configJson["TIMERS"]["RESET"]["INTERVAL"] #100
RESET_TIME = configJson["TIMERS"]["RESET"]["TIME"] #5*60000 #x min of no activity resets interaction.
#TRANSFORM MOVE TIMER
TRANSFORM_INTERVAL = configJson["TIMERS"]["TRANSFORM"]["INTERVAL"] #500
TRANSFORM_TIMER = configJson["TIMERS"]["TRANSFORM"]["TIMER"]       #3000
#SPEECH TIMER
SPEECH_INTERVAL = configJson["TIMERS"]["SPEECH"]["INTERVAL"] #100
SPEECH_SPEED = configJson["TIMERS"]["SPEECH"]["SPEED"]       #3

#UI
USE_NAME_AS_TITLE = configJson["UI"]["USE_NAME_AS_TITLE"]       #False
UI_THEME = configJson["UI"]["THEME"]                         #"light" or "dark"
UI_VERTICAL_BUTTONS = configJson["UI"]["VERTICAL_BUTTONS"]   #True
UI_SPEECH_FONT_SIZE = configJson["UI"]["FONT_SIZE"]   #0.05
UI_SPEECH_TEXT_WIDTH = configJson["UI"]["TEXT_WIDTH"] #0.5
UI_SPEECH_ICON_WIDTH = configJson["UI"]["ICON_WIDTH"] #0.5
UI_SPEECH_ICON_FILL = configJson["UI"]["ICON_FILL"]   #cover, contain, stretch

#NPC ROOT TRANSFORM
ROOT_PARENT = configJson["ROOT"]["PARENT"]     #"" or "marker1"
ROOT_SCALE = ToScale(configJson["ROOT"]["SCALE"])       #Scale(0.8,0.8,0.8)
ROOT_SIZE = configJson["ROOT"]["SIZE"]         #0.2
ROOT_POSITION = ToPosition(configJson["ROOT"]["POSITION"]) #Position(7.2, 0.0, -2.8) #This is the start position
ROOT_ROTATION = ToRotation(configJson["ROOT"]["ROTATION"]) #Rotation(0,0,0)
ROOT_COLOR = ToColor(configJson["ROOT"]["COLOR"])       #Color(255,100,16)
ROOT_OPACITY = configJson["ROOT"]["OPACITY"]   #0.5

#NPC GLTF TRANSFORM
GLTF_SCALE = ToScale(configJson["GLTF"]["SCALE"])       #Scale(1,1,1)
GLTF_POSITION = ToPosition(configJson["GLTF"]["POSITION"]) #Position(0,0,0)
GLTF_ROTATION = ToRotation(configJson["GLTF"]["ROTATION"]) #Rotation(0,180,0) 

#NPC PLANE SETTINGS (for both images and videos)
PLANE_SIZE = configJson["PLANE"]["SIZE"]                  #1.2
PLANE_SIZE_DURATION = configJson["PLANE"]["SIZE_DURATION"] #500
PLANE_POSITION = ToPosition(configJson["PLANE"]["POSITION"])             #Position(1.5,0.8,0)
PLANE_ROTATION = ToRotation(configJson["PLANE"]["ROTATION"])             #Rotation(0,-15,0) 
PLANE_OPACITY = configJson["PLANE"]["OPACITY"]               #0.9

#SPEECH TEXT SETTINGS
SPEECH_TEXT_COLOR = configJson["SPEECH"]["TEXT"]["COLOR"]       #Color(250,100,250)
SPEECH_TEXT_POSITION = configJson["SPEECH"]["TEXT"]["POSITION"] #Position(0,1.6,0)
SPEECH_TEXT_SCALE = configJson["SPEECH"]["TEXT"]["SCALE"]       #Scale(0.6,0.7,0.7)
#SPEECH BUBBLE SETTINGS
SPEECH_BUBBLE_POSITION = ToPosition(configJson["SPEECH"]["BUBBLE"]["POSITION"]) #Position(0,1.7,0)
SPEECH_BUBBLE_ROTATION = ToRotation(configJson["SPEECH"]["BUBBLE"]["ROTATION"]) #Rotation(0,5,0)
SPEECH_BUBBLE_SCALE = ToScale(configJson["SPEECH"]["BUBBLE"]["SCALE"])       #Scale(1,1,1)

#CHOICE TEXT SETTINGS
CHOICE_TEXT_COLOR = ToColor(configJson["CHOICE"]["TEXT"]["COLOR"])         #Color(255,255,255)
CHOICE_TEXT_SCALE = ToScale(configJson["CHOICE"]["TEXT"]["SCALE"])        #Scale(0.4, 2, .5)
#CHOICE BUBBLE SETTINGS
CHOICE_BUBBLE_COLOR = ToColor(configJson["CHOICE"]["BUBBLE"]["COLOR"])     #Color(0,0,200)
CHOICE_BUBBLE_OPACITY = configJson["CHOICE"]["BUBBLE"]["OPACITY"] #0.5
CHOICE_BUBBLE_POSITION = ToPosition(configJson["CHOICE"]["BUBBLE"]["POSITION"]) #Position(-0.95,0.6,0.4)
CHOICE_BUBBLE_ROTATION = ToRotation(configJson["CHOICE"]["BUBBLE"]["ROTATION"]) #Rotation(0,15,0)
CHOICE_BUBBLE_OFFSET_Y = configJson["CHOICE"]["BUBBLE"]["OFFSET_Y"] #0.25
CHOICE_BUBBLE_SCALE = ToScale(configJson["CHOICE"]["BUBBLE"]["SCALE"])     #Scale(0.8, 0.8, 0.8)

#LINK TEXT SETTINGS
LINK_TEXT_COLOR = ToColor(configJson["LINK"]["TEXT"]["COLOR"])         #Color(255,255,255)
LINK_TEXT_SCALE = ToScale(configJson["LINK"]["TEXT"]["SCALE"])           #Scale(0.2, 2, .5)
#LINK BUBBLE SETTINGS
LINK_BUBBLE_COLOR = ToColor(configJson["LINK"]["BUBBLE"]["COLOR"])     #Color(0,200,100)
LINK_BUBBLE_OPACITY = configJson["LINK"]["BUBBLE"]["OPACITY"] #0.8
LINK_BUBBLE_POSITION = ToPosition(configJson["LINK"]["BUBBLE"]["POSITION"]) #Position(0,0.8,0.7)
LINK_BUBBLE_ROTATION = ToRotation(configJson["LINK"]["BUBBLE"]["ROTATION"]) #Rotation(0,0,0)
LINK_BUBBLE_SCALE = ToScale(configJson["LINK"]["BUBBLE"]["SCALE"])       #Scale(1.5, 0.2, 0.08)