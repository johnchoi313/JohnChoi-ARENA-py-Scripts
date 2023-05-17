# ------------------------------------------ #
# ----------IMPORTING EVERYTHING------------ #
# ------------------------------------------ #

from ColorPrinter import *

from arena import *

from asyncio import create_subprocess_exec
from time import gmtime, strftime

# ------------------------------------------ #
# -----------MAIN NPC MASTERCLASS----------- #
# ------------------------------------------ #

BUTTON_BASE_COLOR = (0, 65, 168)
BUTTON_TEXT_COLOR = (255, 255, 255)

BUTTON_BASE_OPACITY = 0.9
BUTTON_TEXT_OPACITY = 0.5

OPTITRACK_TEXT_COLOR = (20, 48, 255)

ANIMATION_DURATION = 5

START_SOUND_URL = "store/users/johnchoi/Sounds/NPC/Next.wav"

#ARENA SETTINGS
FILESTORE = "https://arenaxr.org/" #main server

HOST = "mqtt.arenaxr.org"          #main server
NAMESPACE = "etc" #"johnchoi"
SCENE = "RemakeLearning2023" #"NPC"

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

ARENA_DEBUG_TEXT = Text(
    object_id="DEBUG_TEXT",
    text="Welcome to Remake Learning 2023!",
    align="center",
    position=(0,0.05,3.2), rotation=(-90,0,0), scale=(1, 1, 1),            
    material = Material(color = BUTTON_TEXT_COLOR, transparent = False, opacity=BUTTON_TEXT_OPACITY),
    shadow = {"cast":True, "receive":True},
    persist=True
)
scene.add_object(ARENA_DEBUG_TEXT)

def printArenaDebugText(text):
    ARENA_DEBUG_TEXT.data.text = text
    scene.update_object(ARENA_DEBUG_TEXT)
    printGreen(text)

# ------------------------------------------ #
# -----------MAIN NPC MASTERCLASS----------- #
# ------------------------------------------ #

class Part:
    def __init__(self, scene, partNum, name, partNames, soundURL, buttonText, buttonPos, buttonRot, zoneStart, zoneEnd):
        self.scene = scene
        self.num = partNum
        self.name = name
        self.soundURL = soundURL

        self.zoneStart = zoneStart
        self.zoneEnd = zoneEnd
        
        self.createButton(buttonText, buttonPos, buttonRot)

        self.OptitrackBoxCreated = False
        self.OptitrackTrigger = False
        self.createOptitrackBox()

        self.clicked = False

        self.gltfs = []
        for partName in partNames:
            self.gltfs.append(self.createPart(partNum, partName))    
    

    
    def createOptitrackBox(self):
        #Create Button Object
        self.OptitrackBox = Box(
            object_id="Box" + str(self.num) + "_" + self.name,

            position = ((self.zoneStart[0]+self.zoneEnd[0]) * 0.5,2,(self.zoneStart[2]+self.zoneEnd[2]) * 0.5),
            rotation = (0,0,0),

            depth = 0.2, height = 0.2, width = 0.2,
            material = Material(color = BUTTON_BASE_COLOR, transparent = True, opacity=BUTTON_BASE_OPACITY),
            shadow = {"cast":True, "receive":False},

            persist=True
        )
        self.scene.add_object(self.OptitrackBox)

        #Create Button Text Object
        text = Text(
            object_id="Box" + str(self.num) + "_" + self.name + "(Text)",
            text=self.name,
            align="center",
            position=(0,0.15,0), rotation=(0,0,0), scale=(0.5, 0.5, 0.5),      
            material = Material(color = OPTITRACK_TEXT_COLOR, transparent = False, opacity=BUTTON_TEXT_OPACITY),
            parent = self.OptitrackBox,
            persist=True
        )
        self.scene.add_object(text)


    def CheckOptitrackInZone(self):
        if(self.zoneStart[0] < self.OptitrackBox.data.position.x < self.zoneEnd[0] and 
           self.zoneStart[1] < self.OptitrackBox.data.position.y < self.zoneEnd[1] and 
           self.zoneStart[2] > self.OptitrackBox.data.position.z > self.zoneEnd[2]):
            return True
        else:            
            return False


    def createPart(self, partNum, partName):
        gltf = GLTF(
            object_id="part" + str(partNum) + "_" + partName,
            url="/store/users/etc/RemakeLearning2023/Part"+str(partNum)+"/part"+str(partNum)+"_"+partName+".glb",

            position=(0,0.1,0),
            rotation=(0,0,0),
            scale=(1,1,1),

            shadow = {"cast":True, "receive":True},
            persist=True
        )
        scene.add_object(gltf)
        return gltf

    def createButton(self, buttonText, pos, rot):        
        #Create Button Object
        self.buttonBase = Box(
            object_id="part" + str(self.num) + "_button_" + self.name + "(base)",
            position=pos, rotation=rot,
            depth = 0.2, height = 0.05, width = 1,
            material = Material(color = BUTTON_BASE_COLOR, transparent = True, opacity=BUTTON_BASE_OPACITY),
            shadow = {"cast":True, "receive":False},
            evt_handler=self.onClicked,
            clickable=True,
            persist=True
        )
        self.scene.add_object(self.buttonBase)
        #Create Button Text Object
        self.buttonText = Text(
            object_id="part" + str(self.num) + "_button_" + self.name + "(text)",
            text=buttonText,
            align="center",
            position=(0,0.05,0), rotation=(-90,0,0), scale=(0.5, 0.5, 0.5),            
            material = Material(color = BUTTON_TEXT_COLOR, transparent = False, opacity=BUTTON_TEXT_OPACITY),
            parent = self.buttonBase,
            persist=True
        )
        self.scene.add_object(self.buttonText)
   
    def onClicked(self, scene, evt, msg):
        if evt.type == "mousedown":
            self.clicked = True
            self.runPart("Manually Started Part " + str(self.num) + " " + self.name + "!")

    def isClicked(self):
        if(self.clicked):
            self.clicked = False
            return True
        return False


    def runPart(self, text):
        printArenaDebugText(text)
        self.PlaySoundFromUrl(START_SOUND_URL)
        self.PlaySoundFromUrl(self.soundURL)
        self.PlayAnimations()

    def PlayAnimations(self):
        for gltf in self.gltfs:
            animation = AnimationMixer(clip="*", loop="pingpong", repetitions = 2, duration = ANIMATION_DURATION, crossFadeDuration=0.0, timeScale = 1, clampWhenFinished = False)
            gltf.dispatch_animation(animation)
            self.scene.run_animations(gltf)
    def PlaySoundFromUrl(self, url):
        sound = Sound(volume=1, autoplay=True, src=url)
        self.PlaySound(sound)
    def PlaySound(self, sound):
        self.buttonBase.data.sound=None #resets so can play same sound again
        self.scene.update_object(self.buttonBase)
        self.buttonBase.data.sound=sound
        self.scene.update_object(self.buttonBase)

# ------------------------------------------ #
# --------MAIN LOOPS/INITIALIZATION--------- #
# ------------------------------------------ #

PART1_NAMES = ["flashy" , "set", "snail", "turtle"]
PART2_NAMES = ["cloud" , "conveyors", "flashy", "rocket", "set", "turtle"]
PART3_NAMES = ["flag" , "flashy", "set", "snail", "symbols", "turtle"]
PART4_NAMES = ["flashy" , "set", "snail", "traffic", "turtle"]
PART5_NAMES = ["flashy" , "podium", "set", "snail", "straw", "trophy", "turtle"]

part1 = Part(scene, 1, "BV", PART1_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "Manual Start BV", 
            (3, 0.1, 1.8288), (0,90,0), 
            (-0.9144, 0, 2.7432), (0.9144, 1, 0.9144))

part2 = Part(scene, 2, "SV", PART2_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "Manual Start SV", 
            (3, 0.1, -1.8288), (0,90,0), 
            (0.9144, 0, 0.9144), (2.7432, 1, -0.9144) )

part3 = Part(scene, 3, "WL", PART3_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "Manual Start WL", 
            (-3, 0.1, -1.8288), (0,-90,0), 
            (-0.9144, 0, -0.9144), (0.9144, 1, -2.7432))

part4 = Part(scene, 4, "RV", PART4_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "Manual Start RV", 
            (-3, 0.1, 1.8288), (0,-90,0), 
            (-2.7432, 0, 0.9144), (-0.9144, 1, -0.9144))


part5 = Part(scene, 5, "SxL",PART5_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "Manual Start SxL", 
            (0, 0.1, -3), (0,180,0), (-0.9144, 0, 0.9144), (0.9144, 1, -0.9144))

parts = [part1, part2, part3, part4, part5]


# ------------------------------------------ #
# --------MAIN LOOPS/INITIALIZATION--------- #
# ------------------------------------------ #


def CheckZoneAndRunNextPart(partA, partB):

    if(partA.CheckOptitrackInZone()):
        if(partA.OptitrackTrigger == False):
            partA.OptitrackTrigger = True
            partB.runPart("Trigger Started Part " + str(partB.num) + " " + partB.name + "!")
            return True
    else:
        if(partA.OptitrackTrigger == True):
            partA.OptitrackTrigger = False
    return False


@scene.run_forever(interval_ms=100)
def Collision_Handler(): #checks whether or not a user is in range of NPC

    CheckZoneAndRunNextPart(part1, part4)
    CheckZoneAndRunNextPart(part4, part3)
    CheckZoneAndRunNextPart(part3, part2)
    
    ranPart5A = CheckZoneAndRunNextPart(part2, part5)
    ranPart5B = CheckZoneAndRunNextPart(part5, part5)
    
    if(ranPart5A or ranPart5B):
        printCyan("Running Last Part!")
    
    if(part5.isClicked()):
        printCyan("Running Last Part!")
    
scene.run_tasks()