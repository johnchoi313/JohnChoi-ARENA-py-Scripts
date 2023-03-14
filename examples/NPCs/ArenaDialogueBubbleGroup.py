
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
    def __init__(self, scene, npc, gltf, dialogue):
        self.scene = scene
        self.npc = npc
        self.gltf = gltf
        self.dialogue = dialogue
        self.speech = ""
        self.speechIndex = 0
        self.initializeBubbles()
    #reinitializes and restarts the interaction
    def start(self):
        printGreenB("\n(---Starting NPC interaction:---)")
        self.clearButtons()
        self.initializeBubbles()
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
            printWarning("    " + "Attempting to play sound from URL \"" + key + "\" because no such mapping exists in mappings.py.")
            self.PlaySoundFromUrl(key)
    def PlaySoundFromUrl(self, url):
        sound = Sound(volume=1, autoplay=True, src=url)
        self.PlaySound(sound)
    def PlaySound(self, SOUND):
        printWhiteB("Playing sound")
        self.npc.data.sound=None #resets so can play same sound again
        self.scene.update_object(self.npc)
        self.npc.data.sound=SOUND
        self.scene.update_object(self.npc)

    #Animations
    def PlayAnimationFromMapping(self, key):
        if(key in animationMappings):
            self.npc.PlayAnimation(animationMappings[key])
        else: 
            printWarning("    " + "Attempting to play animation from name \"" + key + "\" because no such mapping exists in mappings.py.")
            self.npc.PlayAnimationFromName(key)
    def PlayAnimationFromName(self, name):
        animation = AnimationMixer(clip=name, loop="once")
        self.npc.PlayAnimation(animation)
    def PlayAnimation(self, animation):
        self.npc.dispatch_animation(animation)
        self.scene.run_animations(self.npc)

    #Transforms
    def PlayTransformFromMapping(self, key):
        if(key in transformMappings):
            self.PlayTransform(transformMappings[key])
        else:
            printWarning("    " + "Cannot play transform \"" + key + "\" because no such mapping exists in mappings.py.")
    def PlayTransform(self, transform):
        self.npc.dispatch_animation(transform)
        self.scene.run_animations(self.npc)
        return

    #Morphs
    def PlayMorphFromMapping(self, key):
        if(key in morphMappings):
            self.PlayMorph(morphMappings[key])
        else:
            printWarning("    " + "Cannot play morph \"" + key + "\" because no such mapping exists in mappings.py.")
    def PlayMorph(self, morphs):
        self.npc.xr_logo.update_morph(morphs)

    #GotoUrl
    def PlayUrlFromMapping(self, key):
        if(key in urlMappings):
            self.PlayGotoUrl(urlMappings[key])
        else:
            printWarning("    " + "Attempting to directly play URL \"" + key + "\" because no such mapping exists in mappings.py.")
            self.PlayUrl(key)
    def PlayUrl(self, link):
        gotoUrl = GotoUrl(dest="popup", on="mousedown", url=link)
        self.PlayGotoUrl(gotoUrl)
    def PlayGotoUrl(self, gotoUrl):
        self.npc.data.goto_url=gotoUrl
        self.scene.update_object(self.npc)
        
    #Visibility
    def SetVisible(self, key, visible):            
        if (self.scene.all_objects.get(key) is not None):
            self.scene.all_objects.get[key].data.visible = visible
            self.scene.update_object(self.scene.all_objects.get[key])
        else:
            printWarning("    " + "Cannot set visibility of object with name \"" + key + "\" because no such object exists in scene.")

    #Clear extra properties
    def ClearCommandProperties(self):
        self.npc.data.goto_url = None
        return

    #runs commands
    def runCommands(self, line):
        commands = line.commands

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
                self.PlaySoundFromMapping(command.args[0])

            #<<animation ("animationMappingName")>>
            elif(command.type.lower() == "animation".lower()):
                printYellow("    " + command.text)
                self.PlayAnimationFromMapping(command.args[0])

            #<<transform ("transformMappingName")>>
            elif(command.type.lower() == "transform".lower()):
                printYellow("    " + command.text)
                self.PlayTransformFromMapping(command.args[0])

            #<<morph ("morphMappingName")>>
            elif(command.type.lower() == "morph".lower()):
                printYellow("    " + command.text)
                self.PlayMorphFromMapping(command.args[0])

            #<<url ("urlMappingName")>>
            elif(command.type.lower() == "url".lower()):
                printYellow("    " + command.text)
                self.PlayUrlFromMapping(command.args[0])


        return

    # ------------------------------------------ #
    # -------------BUTTON CREATION-------------- #
    # ------------------------------------------ #

    def createNewButtons(self, line):
        self.createSpeechBubble(line)
        self.createButtons(line)
        self.runCommands(line)
        
    def clearButtons(self):
        if(self.speechBubble != None):
            if(self.speechBubble.object_id != None):
                if(self.scene.all_objects.get(self.speechBubble.object_id) != None):
                    self.scene.delete_object(self.speechBubble)

        for button in self.buttons:
            self.scene.delete_object(button.box)
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
            for c in range(len(choices)):                
                printMagenta("    [["+str(c)+"]] choiceText: " + choices[c].text)
                printMagenta(         "          choiceNode: " + choices[c].node)
        
                choiceButton = Button(self.scene, self.npc, self.npc.object_id + "_choiceButton_" + self.randomUUID(UUID_LEN)+"_"+str(c), choices[c].text, self.onClickChoiceButton, 
                                      position = (CHOICE_BUBBLE_POSITION[0], CHOICE_BUBBLE_POSITION[1] + (len(choices) - c - 1) * CHOICE_BUBBLE_OFFSET_Y, CHOICE_BUBBLE_POSITION[2]), 
                                      color = CHOICE_BUBBLE_COLOR, textColor = CHOICE_TEXT_COLOR)

                self.buttons.append(choiceButton)
        else: 
            nextButton = Button(self.scene, self.npc, self.npc.object_id + "_nextButton_" + self.randomUUID(UUID_LEN), "[Next]", self.onClickNextButton, 
                                position = CHOICE_BUBBLE_POSITION, color = CHOICE_BUBBLE_COLOR, textColor = CHOICE_TEXT_COLOR)
                
            self.buttons.append(nextButton)

        return self.buttons

    def randomUUID(self, n = 6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

    # ------------------------------------------ #
    # ------------EVENT PROCESSING-------------- #
    # ------------------------------------------ #

    #functions to control choice button click behaviour
    def onClickChoiceButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            choiceButtonID = msg["object_id"]
            filterLen = len(self.npc.object_id + "_choiceButton_") + UUID_LEN + 1

            choiceButtonNumber = int(choiceButtonID[filterLen:])
            choiceText = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].text
            choiceNodeName = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].node
            
            printCyan("  Choice Button with text \"" + choiceText + "\" pressed!")
                        
            self.gotoNodeWithName(choiceNodeName)

            self.ClearCommandProperties()

            self.PlaySound(SOUND_CHOICE)

    #functions to control choice button click behaviour
    def onClickNextButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            printCyan("  Next Button Pressed!")
            self.advanceToNextLine()

            self.ClearCommandProperties()

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