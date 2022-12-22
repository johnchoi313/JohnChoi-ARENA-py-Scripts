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

HOST = "mqtt.arenaxr.org"
NAMESPACE = "johnchoi"
SCENE = "NPC"

DIALOGUE_FILENAME = "cartoon_dialogue.json"

NPC_OBJECT = ""

NPC_SCALE = (1,1,1)
NPC_START_POSITION = (0,0,0)
NPC_START_ROTATION = (0,0,0)


#SPEECH_ICON#
SPEECH_BUBBLE_COLOR = (0,0,0)
SPEECH_TEXT_COLOR = (0,0,0)
CHOICE_BUBBLE_COLOR = (0,0,0)
CHOICE_TEXT_COLOR = (0,0,0)

#SPEECH_ICON#
SPEECH_BUBBLE_POSITION = (0,0,0)
CHOICE_BUBBLE_POSITION = (0,0,0)
CHOICE_BUBBLE_OFFSET_Y = 2
        
# ------------------------------------------ #
# --------MAIN LOOP/INITIALIZATION---------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

# create Dialogue, and show contents
dialogue = Dialogue(DIALOGUE_FILENAME)

# Iterating through the json list
dialogue.printInfo()

#Initialize text, buttons, and command from current line from current node:
dialogue.currentNode.currentLine = dialogue.currentNode.lines[0]
line = dialogue.currentNode.currentLine

npc = Box(
    object_id="NPC",
    position=NPC_START_POSITION,
    rotation=NPC_START_ROTATION,
    scale=NPC_SCALE,
    color=(255,100,16),
    material = Material(opacity=0.3, transparent=True),
    persist=True
)
scene.add_object(npc)


bubbles = ArenaDialogueBubbleGroup(scene , npc , dialogue, line)

@scene.run_once
def programStart():
    print("Completed.")

scene.run_tasks()