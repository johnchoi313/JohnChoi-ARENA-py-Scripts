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

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

UPDATE_INTERVAL = 100
TELEPORT_THRES = 5


class NPC:
    def __init__(self, scene):
        self.scene = scene

        self.entered = False
        self.exited = False
        
        # create Dialogue, and show contents
        self.dialogue = Dialogue(DIALOGUE_FILENAME)

        #NPC ROOT OBJECT (with debug box)
        self.npc = Box(
            object_id=NPC_NAME,
            position=NPC_START_POSITION,
            rotation=NPC_START_ROTATION,
            scale=NPC_SCALE,
            color=NPC_CUBE_COLOR,
            material = Material(opacity=NPC_CUBE_OPACITY, transparent=True),
            persist=True
        )
        scene.add_object(self.npc)
        #NPC GLTF
        npcGLTF = GLTF(
            object_id=NPC_NAME + "(GLTF)",
            url=NPC_GLTF_URL,
            position=NPC_GLTF_POSITION,
            rotation=NPC_GLTF_ROTATION,
            scale=NPC_GLTF_SCALE,
            parent=self.npc,
            persist=True
        )
        scene.add_object(npcGLTF)

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
        
        self.bubbles = ArenaDialogueBubbleGroup(scene , self.npc , npcGLTF, self.dialogue)
        self.bubbles.setSpeechSettings(SPEECH_TEXT_COLOR, SPEECH_TEXT_POSITION, SPEECH_TEXT_SCALE)
        self.bubbles.setButtonSettings(CHOICE_TEXT_COLOR, CHOICE_BUBBLE_COLOR, CHOICE_BUBBLE_POSITION, CHOICE_BUBBLE_OFFSET_Y)



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
        
        if user.data.position.distance_to(npc.npc.data.position) <= TELEPORT_THRES:
            
    
            npc.exited = False
            if(npc.entered == False):
                print("entered!")
                npc.entered = True
    
        
        else:
    
            npc.entered = False
            if(npc.exited == False):
                print("exited!")
                npc.exited = True
            


scene.run_tasks()
