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

ANIMATION_DURATION = 5

START_SOUND_URL = "store/users/johnchoi/Sounds/NPC/Next.wav"

# ------------------------------------------ #
# -----------MAIN NPC MASTERCLASS----------- #
# ------------------------------------------ #

class Part:
    def __init__(self, scene, partNum, partNames, soundURL, buttonName, buttonText, buttonPos, buttonRot):
        self.scene = scene
        self.num = partNum
        self.soundURL = soundURL

        self.createButton(buttonName, buttonText, buttonPos, buttonRot)

        self.gltfs = []
        for partName in partNames:
            self.gltfs.append(self.createPart(partNum, partName))    
    
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

    def createButton(self, buttonName, buttonText, pos, rot):        
        self.buttonBase = self.makeButtonBase(buttonName, pos, rot)
        self.buttonText = self.makeButtonText(self.buttonBase, buttonName, buttonText)

    def makeButtonBase(self, buttonName, pos, rot):        
        #Create Button Object
        button = Box(
            object_id="part" + str(self.num) + "_button_" + buttonName + "(base)",
            position=pos, rotation=rot,
            depth = 0.2, height = 0.05, width = 1,
            material = Material(color = BUTTON_BASE_COLOR, transparent = True, opacity=BUTTON_BASE_OPACITY),
            evt_handler=self.onClicked,
            clickable=True,
            persist=True
        )
        self.scene.add_object(button)
        return button
    def makeButtonText(self, button, buttonName, buttonText):
        #Create Button Text Object
        buttonText = Text(
            object_id="part" + str(self.num) + "_button_" + buttonName + "(text)",
            text=buttonText,
            align="center",
            position=(0,0.05,0), rotation=(-90,0,0), scale=(0.5, 0.5, 0.5),            
            material = Material(color = BUTTON_TEXT_COLOR, transparent = False, opacity=BUTTON_TEXT_OPACITY),
            parent = button,
            persist=True
        )
        self.scene.add_object(buttonText)
        return buttonText
    def onClicked(self, scene, evt, msg):
        if evt.type == "mousedown":
            self.PlayAnimations()
            self.PlaySoundFromUrl(START_SOUND_URL)
            self.PlaySoundFromUrl(self.soundURL)
            
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


# ------------------------------------------ #
# --------MAIN LOOPS/INITIALIZATION--------- #
# ------------------------------------------ #

#ARENA SETTINGS
FILESTORE = "https://arenaxr.org/" #main server

HOST = "mqtt.arenaxr.org"          #main server
NAMESPACE = "etc" #"johnchoi"
SCENE = "RemakeLearning2023" #"NPC"

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)


part1 = Part(scene, 1, PART1_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "BV", "Manual Start BV", (3, 0.1, 1.8288), (0,90,0))

part2 = Part(scene, 2, PART2_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "SV", "Manual Start SV", (3, 0.1, -1.8288), (0,90,0))

part3 = Part(scene, 3, PART3_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "WL", "Manual Start WL", (-3, 0.1, -1.8288), (0,-90,0))

part4 = Part(scene, 4, PART4_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "RV", "Manual Start RV", (-3, 0.1, 1.8288), (0,-90,0))

part5 = Part(scene, 5, PART5_NAMES, "store/users/johnchoi/Sounds/NPC/Enter.wav", "SxL", "Manual Start SxL", (0, 0.1, -3), (0,180,0))



scene.run_tasks()