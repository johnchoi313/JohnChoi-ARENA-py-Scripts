# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from asyncio import create_subprocess_exec
from arena import *

from datetime import datetime
from datetime import timezone
from time import gmtime, strftime

from config import *
from mappings import *
from YarnParser import *
from ColorPrinter import *
from ArenaDialogueBubbleGroup import *

# ------------------------------------------ #
# -----------MAIN NPC MASTERCLASS----------- #
# ------------------------------------------ #

class NPC:
    def __init__(self, scene):
        self.scene = scene
        self.entered = False
        self.userCount = 0

        self.talking = False
        
        # create Dialogue, and show contents
        self.dialogue = Dialogue(DIALOGUE_FILENAME)

        #NPC ROOT OBJECT (with debug box)
        self.root = Box(
            object_id=NPC_NAME,
            #position=ROOT_POSITION,
            #rotation=ROOT_ROTATION,
            scale=ROOT_SCALE,
            color=ROOT_COLOR,
            material = Material(opacity=ROOT_OPACITY, transparent=True),
            sound = None,
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
        
        self.bubbles = ArenaDialogueBubbleGroup(self.scene, self.root , self.gltf, self.dialogue)

# ------------------------------------------ #
# --------MAIN LOOPS/INITIALIZATION--------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

# make NPC
npc = NPC(scene)

@scene.run_once
def ProgramStart():
    npc.dialogue.printJson()
    npc.dialogue.printInfo()
    npc.bubbles.start()

@scene.run_forever(interval_ms=ENTER_INTERVAL)
def EnterExit_Handler(): #checks whether or not a user is in range of NPC
    users = scene.get_user_list()
    sceneUserCount = len(scene.get_user_list())
    userCount = 0

    #strange bug - closing browser does not send exit message?
    if(scene.get_user_list() == None):
        users = []
        sceneUserCount = 0

    for user in scene.get_user_list():
        #if user.data.position.distance_to(npc.root.data.position) <= ENTER_DISTANCE:
        userCount+=1
    
    if(npc.userCount != userCount):
        printLightRedB(str(userCount) + " users in area of NPC with name \"" + NPC_NAME + "\".")
        if(userCount > 0 and npc.entered == False): # At least one user in range of NPC starts interaction.
            npc.entered = True
            npc.bubbles.gotoNodeWithName(ENTER_NODE)

            if(USE_DEFAULT_SOUNDS):
                npc.bubbles.PlaySound(SOUND_ENTER)

        if(userCount == 0 and npc.entered == True): # All users left, so end interaction.
            npc.entered = False
            npc.bubbles.gotoNodeWithName(EXIT_NODE)

            if(USE_DEFAULT_SOUNDS):
                npc.bubbles.PlaySound(SOUND_EXIT)
    
    npc.userCount = userCount





@scene.run_forever(interval_ms=SPEECH_INTERVAL)
def Speech_Handler(): #iteratively adds characters to speech bubble
    
    if(npc.bubbles.checkIfArenaObjectExists(npc.bubbles.speechBubble)):
    

        #if walking, let walk, hide buttons
        if(npc.bubbles.transformTimer > 0):
            npc.bubbles.transformTimer = npc.bubbles.transformTimer - SPEECH_INTERVAL


        else:

            if(0 <= npc.bubbles.speechIndex and npc.bubbles.speechIndex < len(npc.bubbles.speech)):
                npc.bubbles.speechIndex += 1
            
                #start talking animation if not started already
                if(USE_DEFAULT_ANIMATIONS and not npc.talking and not npc.bubbles.animationUsedThisLine):
                    npc.bubbles.PlayAnimation(ANIM_TALK)

                #move mouth up and down if blendshapes applicable
                if(USE_DEFAULT_MORPHS):
                    if(npc.bubbles.speechIndex % 2 == 0):
                        npc.bubbles.PlayMorph(MORPH_OPEN)
                    else:
                        npc.bubbles.PlayMorph(MORPH_CLOSE)
                    
                npc.talking = True

            else:
                npc.bubbles.speechIndex = len(npc.bubbles.speech)

                #play idle if not started already.
                if(USE_DEFAULT_ANIMATIONS and npc.talking and not npc.bubbles.animationUsedThisLine):
                    npc.bubbles.PlayAnimation(ANIM_IDLE)

                #close mouth if blendshapes applicable
                if(USE_DEFAULT_MORPHS and npc.talking):
                    npc.bubbles.PlayMorph(MORPH_CLOSE)

                npc.talking = False

            npc.isTalking = npc.talking

        npc.bubbles.speechBubble.data.text = npc.bubbles.speech[:npc.bubbles.speechIndex]
        scene.update_object(npc.bubbles.speechBubble)

scene.run_tasks()