# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from asyncio import create_subprocess_exec
from arena import *

from YarnParser import *
from ColorPrinter import *
from ARENA_NPC_Helpers import *

# ------------------------------------------ #
# -----------STARTING VARIABLES------------- #
# ------------------------------------------ #

#ARENA SETTINGS
HOST = "mqtt.arenaxr.org"
NAMESPACE = "johnchoi"
SCENE = "NPC"

#DIALOGUE TREE FILE
DIALOGUE_FILENAME = "cartoon_dialogue.json"

###---------###

#NPC (name Alphanumeric only plus _)
NPC_NAME = "NPC_cactus"
NPC_GLTF_URL = "/store/users/johnchoi/Characters/Cactus/Cactus.gltf"

#NPC ROOT TRANSFORM
NPC_SCALE = (2,2,2)
NPC_START_POSITION = (0,0,0)
NPC_START_ROTATION = (0,0,0)
#NPC DEBUG CUBE
NPC_DEBUG_COLOR = (255,100,16)
NPC_DEBUG_OPACITY = 0.3

#NPC GLTF TRANSFORM
NPC_GLTF_SCALE = (1,1,1)
NPC_GLTF_POSITION = (0,0,0)
NPC_GLTF_ROTATION = (0,180,0)

#SPEECH SETTINGS
SPEECH_TEXT_COLOR = (100,100,100)
SPEECH_TEXT_POSITION = (0,1,0)
SPEECH_TEXT_SCALE = (0.4,0.4,0.4)

#CHOICE SETTINGS
CHOICE_TEXT_COLOR = (0,0,0)
CHOICE_BUBBLE_COLOR = (200,200,200)
CHOICE_BUBBLE_POSITION = (0,0.2,0.6)
CHOICE_BUBBLE_OFFSET_Y = 0.15

# ------------------------------------------ #
# --------MAIN LOOP/INITIALIZATION---------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

# create Dialogue, and show contents
dialogue = Dialogue(DIALOGUE_FILENAME)

#NPC ROOT OBJECT (with debug box)
npc = Box(
    object_id=NPC_NAME,
    position=NPC_START_POSITION,
    rotation=NPC_START_ROTATION,
    scale=NPC_SCALE,
    color=NPC_DEBUG_COLOR,
    material = Material(opacity=NPC_DEBUG_OPACITY, transparent=True),
    persist=True
)
scene.add_object(npc)

#NPC GLTF
npcGLTF = GLTF(
    object_id=NPC_NAME + "(GLTF)",
    url=NPC_GLTF_URL,
    position=NPC_GLTF_POSITION,
    rotation=NPC_GLTF_ROTATION,
    scale=NPC_GLTF_SCALE,
    parent=npc,
    persist=True
)
scene.add_object(npcGLTF)

bubbles = ArenaDialogueBubbleGroup(scene , npc , dialogue)

bubbles.setSpeechSettings(SPEECH_TEXT_COLOR, SPEECH_TEXT_POSITION, SPEECH_TEXT_SCALE)
bubbles.setButtonSettings(CHOICE_TEXT_COLOR, CHOICE_BUBBLE_COLOR, CHOICE_BUBBLE_POSITION, CHOICE_BUBBLE_OFFSET_Y)

@scene.run_once
def programStart():
    
    dialogue.printJson()
    
    dialogue.printInfo()
    
    bubbles.start()

    

scene.run_tasks()