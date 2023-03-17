from asyncio import create_subprocess_exec
from arena import *

import string
import random

from Button import *
from config import *
from mappings import *
from YarnParser import *
from ColorPrinter import *

# ------------------------------------------ #
# -----------ARENA BUBBLE GROUP------------- #
# ------------------------------------------ #

class ArenaDialogueBubbleGroup():
    def __init__(self, scene, npc, gltf, image, video, dialogue):
        self.scene = scene
        self.npc = npc
        self.gltf = gltf

        self.image = image
        self.video = video

        self.dialogue = dialogue
        self.speech = ""
        self.speechIndex = 0
        self.initializeBubbles()

        self.animationUsedThisLine = False
        self.transformUsedThisLine = False

        self.imageUsedThisLine = False
        self.videoUsedThisLine = False
        self.soundUsedThisLine = False

        
        self.lastImageSize = (0,0,0)
        self.lastVideoSize = (0,0,0)

        self.lastTransform = TRANSFORM_RESET

        self.transformTimer = 0
        self.resetTimer = 0

    #reinitializes and restarts the interaction
    def start(self):
        printGreenB("\n(---Starting NPC interaction:---)")
        self.clearButtons()
        self.initializeBubbles()

        self.PlayTransform(self.lastTransform)

    #creates new bubbles
    def initializeBubbles(self, line = None):
        if(line == None):
            self.dialogue.currentNode.currentLine = self.dialogue.currentNode.lines[0]
            line = self.dialogue.currentNode.currentLine
        self.speechBubble = self.createSpeechBubble(line)
        self.buttons = self.createButtons(line)

    # ------------------------------------------ #
    # ------------RUNNING COMMANDS-------------- #
    # ------------------------------------------ #

    #Sounds
    def PlaySoundFromMapping(self, key):
        if(key in soundMappings):
            self.PlaySound(soundMappings[key])
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Attempting to play sound from URL \"" + key + "\" because no such mapping exists in mappings.py.")
            
            self.PlaySoundFromUrl(key)
    def PlaySoundFromUrl(self, url):
        if(PRINT_VERBOSE):
            printWhiteB("Play sound from url \'" + url + "\"")
        sound = Sound(volume=1, autoplay=True, src=url)
        self.PlaySound(sound)
    def PlaySound(self, sound):
        if(PRINT_VERBOSE):
            printWhiteB("Playing sound...")
        self.npc.data.sound=None #resets so can play same sound again
        self.scene.update_object(self.npc)
        self.npc.data.sound=sound
        self.scene.update_object(self.npc)

    #Animations
    def PlayAnimationFromMapping(self, key):
        if(key in animationMappings):
            self.PlayAnimation(animationMappings[key])
        else:     
            if(PRINT_VERBOSE):
                printWarning("    " + "Attempting to play animation from name \"" + key + "\" because no such mapping exists in mappings.py.")
            self.PlayAnimationFromName(key)

    def PlayAnimationFromName(self, name):
        if(PRINT_VERBOSE):
            printWhiteB("Play animation from name \'" + name + "\"")
        animation = AnimationMixer(clip=name, loop="once", crossFadeDuration=0.5, timeScale = 1)
        self.PlayAnimation(animation)

    def PlayAnimation(self, animation):
        if(PRINT_VERBOSE):
            printWhiteB("Playing animation...")
        self.gltf.dispatch_animation(animation)
        self.scene.run_animations(self.gltf)
        
    #Transforms
    def PlayTransformFromMapping(self, key):
        if(key in transformMappings):
            self.PlayTransform(transformMappings[key])
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Cannot play transform \"" + key + "\" because no such mapping exists in mappings.py.")
    def PlayTransform(self, transform):
        if(PRINT_VERBOSE):
            printWhiteB("Playing transform...")
        self.npc.dispatch_animation(transform)
        self.scene.run_animations(self.npc)
        #self.scene.update_object(self.npc)

        if(self.lastTransform == transform):
            self.transformUsedThisLine = False
        else:
            self.lastTransform = transform


    #Morphs
    def PlayMorphFromMapping(self, key):
        if(key in morphMappings):
            self.PlayMorph(morphMappings[key])
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Cannot play morph \"" + key + "\" because no such mapping exists in mappings.py.")
    def PlayMorph(self, morphs):
        if(PRINT_VERBOSE):
            printWhiteB("Playing morph...")
        self.gltf.update_morph(morphs)
        self.scene.update_object(self.gltf)

    #GotoUrl
    def PlayUrlFromMapping(self, key):
        if(key in urlMappings):
            self.PlayGotoUrl(urlMappings[key])
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Attempting to directly play URL \"" + key + "\" because no such mapping exists in mappings.py.")
            self.PlayUrl(key)
    def PlayUrl(self, link):
        if(PRINT_VERBOSE):
            printWhiteB("Play url with link \'" + link + "\"")
        
        gotoUrl = GotoUrl(dest="popup", on="mousedown", url=link)
        self.PlayGotoUrl(gotoUrl)

    def PlayGotoUrl(self, gotoUrl):

        if(PRINT_VERBOSE):
            printWhiteB("Playing gotoUrl...")
        self.npc.data.goto_url=None
        self.scene.update_object(self.npc)

        self.npc.data.goto_url=gotoUrl
        self.scene.update_object(self.npc)
        #urls are persistent? I don't know why
        self.npc.data.goto_url=None
        self.scene.update_object(self.npc)

    #Videos
    def PlayVideoFromMapping(self, key):
        if(key in videoMappings):
            if(videoMappings[key] is not None):
                self.PlayVideo(videoMappings[key])
            else:
                self.HideVideo()
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Hiding video \"" + key + "\" because no such mapping exists in mappings.py.")
            self.HideVideo()

    def PlayVideoFromUrl(self, url):
        if(PRINT_VERBOSE):
            printWhiteB("Play video from url \'" + url + "\":")        
        material = Material(src = url, transparent = True, opacity = 0.9, color = "#ffffff", w = 1920, h = 1080, size = 1)
        self.PlayVideo(material)
    
    def PlayVideo(self, material):
        if(PRINT_VERBOSE):
            printWhiteB("Playing video...")
        #Clear Material
        self.video.data.material=None 
        self.scene.update_object(self.video)
        self.ShowVideo(self.getNewScale(material.w, material.h, material.size))
        self.video.data.material=material
        self.scene.update_object(self.video)

    def HideVideo(self):
        animation = Animation(property="scale", start=self.lastVideoSize, end=(0,0,random.uniform(0, 0.01)), easing="easeInOutQuad", dur=500)
        self.video.dispatch_animation(animation)
        self.scene.run_animations(self.video)
        self.lastVideoSize = (0,0,0)
    
    def ShowVideo(self, scale):
        animation = Animation(property="scale", start=(0,0,random.uniform(0, 0.01)), end=scale, easing="easeInOutQuad", dur=500)
        self.video.dispatch_animation(animation)
        self.scene.run_animations(self.video)
        self.lastVideoSize = scale



    #Images
    def PlayImageFromMapping(self, key):
        if(key in imageMappings):
            if(imageMappings[key] is not None):
                self.PlayImage(imageMappings[key])
            else:
                self.HideImage()
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Hiding image with \"" + key + "\" because no such mapping exists in mappings.py.")
            self.HideImage()
    def PlayImageFromUrl(self, src):
        if(PRINT_VERBOSE):
            printWhiteB("Play image from url \'" + src + "\":")        
        img = IMG(url = src, w = 1000, h = 1000, size = 1)
        self.PlayImage(img)
    def PlayImage(self, img):
        if(PRINT_VERBOSE):
            printWhiteB("Playing image...")

        self.ShowImage(self.getNewScale(img.w, img.h, img.size))
        self.scene.update_object(self.image, url = img.url)
    def HideImage(self):
        animation = Animation(property="scale", start=self.lastImageSize, end=(0,0,random.uniform(0, 0.01)), easing="easeInOutQuad", dur=500)
        self.image.dispatch_animation(animation)
        self.scene.run_animations(self.image)
        self.lastImageSize = (0,0,0)
    def ShowImage(self, scale):
        animation = Animation(property="scale", start=(0,0,random.uniform(0, 0.01)), end=scale, easing="easeInOutQuad", dur=500)
        self.image.dispatch_animation(animation)
        self.scene.run_animations(self.image)
        self.lastImageSize = scale
        if(USE_DEFAULT_SOUNDS and not self.soundUsedThisLine):
            self.PlaySound(SOUND_IMAGE)




    def HidePlane(self):
        animation = Animation(property="scale", start=self.lastImageSize, end=(0,0,random.uniform(0, 0.01)), easing="easeInOutQuad", dur=500)
        self.image.dispatch_animation(animation)
        self.scene.run_animations(self.image)
        self.lastImageSize = (0,0,0)
    def ShowPlane(self, scale):
        animation = Animation(property="scale", start=(0,0,random.uniform(0, 0.01)), end=scale, easing="easeInOutQuad", dur=500)
        self.image.dispatch_animation(animation)
        self.scene.run_animations(self.image)
        self.lastImageSize = scale
        if(USE_DEFAULT_SOUNDS and not self.soundUsedThisLine):
            self.PlaySound(SOUND_IMAGE)
    def getNewScale(self, w, h, size):
        aspect = ( w * 1.0 ) / ( h * 1.0 )
        scale = 1
        
        if( w > h):
            scale = (w + h) * 0.5 / (w * 1.0)
        else:
            scale = (w + h) * 0.5 / (h * 1.0)
            
        nw = aspect * scale * size * PLANE_SCALE
        nh = 1.0 * scale * size * PLANE_SCALE

        return (nw, nh, 1)
    
    #Visibility
    def SetVisible(self, key, visible):            
        if (self.scene.all_objects.get(key) is not None):
            self.scene.all_objects.get[key].data.visible = visible
            self.scene.update_object(self.scene.all_objects.get[key])
        else:
            if(PRINT_VERBOSE):
                printWarning("    " + "Cannot set visibility of object with name \"" + key + "\" because no such object exists in scene.")

    #Clear extra properties
    def ClearCommandProperties(self):
        self.npc.data.goto_url = None
        return

    #runs commands
    def runCommands(self, line):
        commands = line.commands
        self.animationUsedThisLine = False
        self.transformUsedThisLine = False

        self.imageUsedThisLine = False
        self.videoUsedThisLine = False
        self.soundUsedThisLine = False

        #print details
        for c in range(len(commands)):            
            printGreen("    <<"+str(c)+">> commandType: " + commands[c].type)
            printGreen(         "          commandText: " + commands[c].text)
            if(len(commands[c].args) > 0):
                for a in range(len(commands[c].args)):
                    printGreen(     "          --commandArgs["+str(a)+"]: " + commands[c].args[a])
                 
        #run through each command: 
        #--parentheses () optional for one argument, required for multiple, separated by commas.
        for command in commands:
        
            ###------MISCELLANEOUS------###

            #<<print ("text")>>
            if(command.type.lower() == "print".lower()):
                printYellow("    " + command.text)

            ###------VISIBILITY------###

            #<<show ("objectName")>> (this shows an object with the name if it exists)
            elif(command.type.lower() == "show".lower()):
                printYellow("    " + command.text)
                self.SetVisible(command.args[0], True)
            #<<hide ("objectName")>> (this shows an object with the name if it exists)
            elif(command.type.lower() == "hide".lower()):
                printYellow("    " + command.text)
                self.SetVisible(command.args[0], False)

            ###------QUICK ACTION MAPPINGS------###

            #<<sound ("soundMappingName")>>
            elif(command.type.lower() == "sound".lower()):
                printYellow("    " + command.text)
                self.soundUsedThisLine = True
                self.PlaySoundFromMapping(command.args[0])

            #<<animation ("animationMappingName")>>
            elif(command.type.lower() == "animation".lower()):
                printYellow("    " + command.text)
                self.animationUsedThisLine = True
                self.PlayAnimationFromMapping(command.args[0])
                
            #<<transform ("transformMappingName")>>
            elif(command.type.lower() == "transform".lower()):
                printYellow("    " + command.text)
                self.transformUsedThisLine = True
                self.PlayTransformFromMapping(command.args[0])
                
            #<<morph ("morphMappingName")>>
            elif(command.type.lower() == "morph".lower()):
                printYellow("    " + command.text)
                self.PlayMorphFromMapping(command.args[0])

            #<<url ("urlMappingName")>>
            elif(command.type.lower() == "url".lower()):
                printYellow("    " + command.text)
                self.PlayUrlFromMapping(command.args[0])

            #<<image ("imageMappingName")>>
            elif(command.type.lower() == "image".lower()):
                printYellow("    " + command.text)
                self.imageUsedThisLine = True
                self.PlayImageFromMapping(command.args[0])

            #<<video ("imageMappingName")>>
            elif(command.type.lower() == "video".lower()):
                printYellow("    " + command.text)
                self.videoUsedThisLine = True
                self.PlayVideoFromMapping(command.args[0])

        #If moving, then play walk animation if enabled. 
        if(self.transformUsedThisLine):
            if(USE_DEFAULT_ANIMATIONS):
                self.PlayAnimation(ANIM_WALK)
            self.transformTimer = TRANSFORM_TIMER
        else: #If not moving, reset transform:
            self.PlayTransform(self.lastTransform)

    # ------------------------------------------ #
    # -------------BUTTON CREATION-------------- #
    # ------------------------------------------ #

    def createNewButtons(self, line):
        self.createSpeechBubble(line)
        self.createButtons(line)
        self.runCommands(line)
        
    def clearButtons(self):
        if(self.checkIfArenaObjectExists(self.speechBubble)):
            self.scene.delete_object(self.speechBubble)

        for button in self.buttons:
            if(self.checkIfArenaObjectExists(button.box)):
                self.scene.delete_object(button.box)
            if(self.checkIfArenaObjectExists(button.text)):
                self.scene.delete_object(button.text)
            
        self.commands = []

    def createSpeechBubble(self, line):
        self.speech = line.text
        self.speechIndex = 0

        speechBubble = Text(
            object_id=self.npc.object_id + "_speechBubble",
            text="",
            parent=self.npc,
            align="center",
            color = SPEECH_TEXT_COLOR,            
            position=SPEECH_TEXT_POSITION,
            scale=SPEECH_TEXT_SCALE,
        )
        self.scene.add_object(speechBubble) # add the box
        return speechBubble

    def createButtons(self, line):
        choices = line.choices
        self.buttons = []
        if(len(choices) > 0): 
            for c in reversed(range(len(choices))):                
                printMagenta("    [["+str(c)+"]] choiceText: " + choices[c].text)
                printMagenta(         "          choiceNode: " + choices[c].node)
        
                choiceButton = Button(self.scene, self.npc, self.npc.object_id + "_choiceButton_" + self.randomUUID(UUID_LEN)+"_"+str(c), choices[c].text, self.onClickChoiceButton, 
                                      position = (CHOICE_BUBBLE_POSITION[0], CHOICE_BUBBLE_POSITION[1] + (len(choices) - c - 1) * CHOICE_BUBBLE_OFFSET_Y, CHOICE_BUBBLE_POSITION[2]), 
                                      rotation = CHOICE_BUBBLE_ROTATION, buttonScale = CHOICE_BUBBLE_SCALE, textScale = CHOICE_TEXT_SCALE, color = CHOICE_BUBBLE_COLOR, textColor = CHOICE_TEXT_COLOR)

                self.buttons.append(choiceButton)
        else: 
            nextButton = Button(self.scene, self.npc, self.npc.object_id + "_nextButton_" + self.randomUUID(UUID_LEN), "[Next]", self.onClickNextButton, 
                                position = CHOICE_BUBBLE_POSITION, rotation = CHOICE_BUBBLE_ROTATION, buttonScale = CHOICE_BUBBLE_SCALE, 
                                textScale = CHOICE_TEXT_SCALE, color = CHOICE_BUBBLE_COLOR, textColor = CHOICE_TEXT_COLOR)
                
            self.buttons.append(nextButton)

        return self.buttons

    def randomUUID(self, n = 6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

    def checkIfArenaObjectExists(self, obj):
        if(obj != None):
            if(obj.object_id != None):
                if(self.scene.all_objects.get(obj.object_id) != None):
                    return True

        return False

    # ------------------------------------------ #
    # ------------EVENT PROCESSING-------------- #
    # ------------------------------------------ #

    #functions to control choice button click behaviour
    def onClickChoiceButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            
            self.resetTimer = RESET_TIME

            choiceButtonID = msg["object_id"]
            filterLen = len(self.npc.object_id + "_choiceButton_") + UUID_LEN + 1

            choiceButtonNumber = int(choiceButtonID[filterLen:])
            choiceText = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].text
            choiceNodeName = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].node
            
            printCyan("  Choice Button with text \"" + choiceText + "\" pressed!")
                        
            self.gotoNodeWithName(choiceNodeName)
            
            self.ClearCommandProperties()

            if(USE_DEFAULT_SOUNDS):
                self.PlaySound(SOUND_CHOICE)



    #functions to control choice button click behaviour
    def onClickNextButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            self.resetTimer = RESET_TIME

            printCyan("  Next Button Pressed!")
            
            self.advanceToNextLine()

            self.ClearCommandProperties()

            if(USE_DEFAULT_SOUNDS):
                self.PlaySound(SOUND_NEXT)

    '''
    def nodeWithNameExists(self, nodeName):
        return True    
    def nodeWithIndexExists(self, nodeIndex):
        return (0 <= nodeIndex and nodeIndex < len(self.dialogue.nodes))
    '''

    def gotoNodeWithName(self, nodeName):
        nodeIndex = self.dialogue.getNodeIndexFromString(nodeName)
        if(nodeIndex >= 0):
            self.gotoNodeWithIndex(nodeIndex)
            printBlueB("Going to node with name \"" + nodeName + "\"...")
        else:
            printWarning("No node with name \"" + nodeName + "\" exists! Ignoring gotoNodeWithName() request.")

    def gotoNodeWithIndex(self, nodeIndex):
        if(0 <= nodeIndex and nodeIndex < len(self.dialogue.nodes)):          
            self.clearButtons()    
            self.dialogue.currentNode = self.dialogue.nodes[nodeIndex]
            self.dialogue.currentNode.currentLineIndex = 0
            self.createNewButtons(self.dialogue.currentNode.lines[0])
        else:
            printWarning("No node with index [" + str(nodeIndex) + "] exists! Ignoring gotoNodeWithIndex() request.")
        
    def advanceToNextLine(self):
        self.clearButtons()
        self.dialogue.currentNode.currentLineIndex = self.dialogue.currentNode.currentLineIndex + 1

        if(self.dialogue.currentNode.currentLineIndex < len(self.dialogue.currentNode.lines)):
            self.createNewButtons(self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex])
        elif(self.dialogue.currentNode.currentLineIndex == len(self.dialogue.currentNode.lines)):
            printRedB("\n(---Finished NPC interaction.---)")