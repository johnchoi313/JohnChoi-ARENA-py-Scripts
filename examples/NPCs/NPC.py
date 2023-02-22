# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from asyncio import create_subprocess_exec
from arena import *

from config import *
from YarnParser import *
from ColorPrinter import *
from ARENA_NPC_Helpers import *

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
    color=NPC_CUBE_COLOR,
    material = Material(opacity=NPC_CUBE_OPACITY, transparent=True),
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

#NPC Collider
npcCollider = Cylinder(
    object_id=NPC_NAME + "(Collider)",
    scale=COLLIDER_SCALE,
    color=COLLIDER_COLOR,
    material = Material(opacity=COLLIDER_OPACITY, transparent=True),
    parent=npc,
    #evt_handler=buttonHandler,
    persist=True
)
scene.add_object(npcCollider)

bubbles = ArenaDialogueBubbleGroup(scene , npc , npcGLTF, dialogue)

bubbles.setSpeechSettings(SPEECH_TEXT_COLOR, SPEECH_TEXT_POSITION, SPEECH_TEXT_SCALE)
bubbles.setButtonSettings(CHOICE_TEXT_COLOR, CHOICE_BUBBLE_COLOR, CHOICE_BUBBLE_POSITION, CHOICE_BUBBLE_OFFSET_Y)

@scene.run_once
def programStart():
    dialogue.printJson()
    dialogue.printInfo()
    bubbles.start()

scene.run_tasks()