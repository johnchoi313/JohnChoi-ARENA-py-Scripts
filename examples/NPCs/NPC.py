# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from asyncio import create_subprocess_exec
from arena import *

from datetime import datetime
from datetime import timezone
from time import gmtime, strftime

from config import *
from YarnParser import *
from ColorPrinter import *
from ARENA_NPC_Helpers import *

# ------------------------------------------ #
# --------MAIN LOOP/INITIALIZATION---------- #
# ------------------------------------------ #

class NPC:
    def __init__(self, scene):
        self.scene = scene

        self.entered = False
        self.exited = False
        
        # create Dialogue, and show contents
        self.dialogue = Dialogue(DIALOGUE_FILENAME)

        #NPC ROOT OBJECT (with debug box)
        self.root = Box(
            object_id=NPC_NAME,
            position=ROOT_POSITION,
            rotation=ROOT_ROTATION,
            scale=ROOT_SCALE,
            color=ROOT_COLOR,
            material = Material(opacity=ROOT_OPACITY, transparent=True),
            persist=True
        )
        scene.add_object(self.root)
        #NPC GLTF
        self.gltf = GLTF(
            object_id=NPC_NAME + "(GLTF)",
            url=NPC_GLTF_URL,
            position=GLTF_POSITION,
            rotation=GLTF_ROTATION,
            scale=GLTF_SCALE,
            parent=self.root,
            persist=True
        )
        scene.add_object(self.gltf)

        '''
        #NPC Collider
        npcCollider = Sphere(
            object_id=NPC_NAME + "(Collider)",
            scale=COLLIDER_SCALE,
            color=COLLIDER_COLOR,
            material = Material(opacity=COLLIDER_OPACITY, transparent=True),
            parent=npc,
            #evt_handler=buttonHandler,
            persist=True
        )
        scene.add_object(npcCollider)
        '''
        
        self.bubbles = ArenaDialogueBubbleGroup(self.scene, self.root , self.gltf, self.dialogue)
        #self.bubbles.setSpeechSettings(SPEECH_TEXT_COLOR, SPEECH_TEXT_POSITION, SPEECH_TEXT_SCALE)
        #self.bubbles.setButtonSettings(CHOICE_TEXT_COLOR, CHOICE_BUBBLE_COLOR, CHOICE_BUBBLE_POSITION, CHOICE_BUBBLE_OFFSET_Y)


# ------------------------------------------ #
# --------MAIN LOOP/INITIALIZATION---------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

# make NPC
npc = NPC(scene)

@scene.run_once
def programStart():
    npc.dialogue.printJson()
    npc.dialogue.printInfo()
    npc.bubbles.start()

@scene.run_forever(interval_ms=UPDATE_INTERVAL)
def teleporter_handler():

    for user in scene.get_user_list():
        #print("distance: " + str(user.data.position.distance_to(npc.npc.data.position)))
        if user.data.position.distance_to(npc.root.data.position) <= ENTER_DISTANCE:
            npc.exited = False
            if(npc.entered == False):
                print("User entered area of NPC with name \"" + NPC_NAME + "\"!")
                npc.entered = True
                npc.bubbles.gotoNodeWithName(ENTER_NODE)

        else:
            npc.entered = False
            if(npc.exited == False):
                print("User exited area of NPC with name \"" + NPC_NAME + "\"!")
                npc.exited = True
                npc.bubbles.gotoNodeWithName(EXIT_NODE)


scene.run_tasks()
