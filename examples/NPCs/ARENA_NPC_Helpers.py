
from asyncio import create_subprocess_exec
from arena import *

from config import *
from YarnParser import *
from ColorPrinter import *

# ------------------------------------------ #
# ------------HELPER VARIABLES-------------- #
# ------------------------------------------ #

class ArenaDialogueBubbleGroup():
    def __init__(self, scene, npc, gltf, dialogue):
        self.scene = scene
        self.npc = npc
        self.gltf = gltf
        self.dialogue = dialogue
        self.speech = ""
        self.speechIndex = 0

        #create bubbles to init types
        self.createBubbles()

    #reinitializes and restarts the interaction
    def start(self):
        printGreenB("\n(---Starting NPC interaction:---)")
        self.clearButtons()
        self.createBubbles()

    #creates new bubbles
    def createBubbles(self, line = None):
        if(line == None):
            self.dialogue.currentNode.currentLine = self.dialogue.currentNode.lines[0]
            line = self.dialogue.currentNode.currentLine
        self.speechBubble = self.createSpeechBubble(line)
        self.buttons = self.createButtons(line)

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
        for command in commands:
        
            #<<print ("text")>>
            if(command.type.lower() == "print".lower()):
                printYellow("    " + command.text)

            #<<hide (objectName)>> (this shows an object with the name if it exists)
            elif(command.type.lower() == "hide".lower()):
                printYellow("    " + command.text)
            #<<show (objectName)>> (this shows an object with the name if it exists)
            elif(command.type.lower() == "show".lower()):
                printYellow("    " + command.text)
                
            #<<setMorph (morphTarget, value)>> (sets a morph target to value)
            elif(command.type.lower() == "setMorph".lower()):
                printYellow("    " + command.text)

            #<<move (x,y,z)>>
            elif(command.type.lower() == "move".lower()):
                printYellow("    " + command.text)

                '''
                self.npc.dispatch_animation(
                    Animation(
                        property="rotation",
                        start=(0,0,0),
                        end=(0,180,0),
                        easing="linear",
                        dur=1000
                    )
                )
                '''

            #<<rotate (x,y,z)>>
            elif(command.type.lower() == "rotate".lower()):
                print("    " + command.text)
            #<<lookAt (x,y,z)>>
            elif(command.type.lower() == "lookAt".lower()):
                print("    " + command.text)

            #<<playSound ()>>
            elif(command.type.lower() == "playSound".lower()):                
                #self.npc = Box(sound = Sound(positional=True, poolSize=1, loop=False, autoplay=True, src=command.text))
                #self.scene.add_object(self.npc);
                print("    " + command.text)

            #<<loopSound ()>>
            elif(command.type.lower() == "loopSound".lower()):
                #self.npc = Box(sound = Sound(positional=True, poolSize=1, loop=True, autoplay=True, src=command.text))
                # self.scene.add_object(self.npc);
                print("    " + command.text)

            #<<playAnimation ()>>
            elif(command.type.lower() == "playAnimation".lower()):
                self.gltf.dispatch_animation(
                    AnimationMixer(clip=command.text, loop="once")
                )
            #<<loopAnimation ()>>
            elif(command.type.lower() == "loopAnimation".lower()):
                self.gltf.dispatch_animation(
                    AnimationMixer(clip=command.text, loop="repeat")
                )
            #<<loopAnimation ()>>
            elif(command.type.lower() == "stopAnimation".lower()):
                self.gltf.dispatch_animation(
                    AnimationMixer(clip=command.text, loop="repeat")
                )

        return

    #functions to create chat bubble from current line (at parent position)
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
        
                choiceButton = Button(self.scene, self.npc, self.npc.object_id + "_choiceButton_"+str(c), choices[c].text, self.onClickChoiceButton, 
                                      position = (CHOICE_BUBBLE_POSITION[0], CHOICE_BUBBLE_POSITION[1] + (len(choices) - c - 1) * CHOICE_BUBBLE_OFFSET_Y, CHOICE_BUBBLE_POSITION[2]), 
                                      color = CHOICE_BUBBLE_COLOR, textColor = CHOICE_TEXT_COLOR)

                self.buttons.append(choiceButton)
        else: 
            nextButton = Button(self.scene, self.npc, self.npc.object_id + "_nextButton", "[Next]", self.onClickNextButton, 
                                position = CHOICE_BUBBLE_POSITION, color = CHOICE_BUBBLE_COLOR, textColor = CHOICE_TEXT_COLOR)
                
            self.buttons.append(nextButton)

        return self.buttons

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
            
        self.buttons = []

        return

    # ------------------------------------------ #
    # ------------HELPER VARIABLES-------------- #
    # ------------------------------------------ #

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
        
    #functions to control choice button click behaviour
    def onClickChoiceButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            choiceButtonID = msg["object_id"]
            filterLen = len(self.npc.object_id + "_choiceButton_")

            choiceButtonNumber = int(choiceButtonID[filterLen:])
            choiceText = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].text
            choiceNodeName = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].node
            
            printCyan("  Choice Button with text \"" + choiceText + "\" pressed!")
                        
            self.gotoNodeWithName(choiceNodeName)

    #functions to control choice button click behaviour
    def onClickNextButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            printCyan("  Next Button Pressed!")
            self.advanceToNextLine()

# ------------------------------------------ #
# --------------ARENA CLASSES--------------- #
# ------------------------------------------ #

class Button():
    def __init__(self, scene, npc, name, text, eventHandler, position, color, textColor):
        self.scene = scene
        self.npc = npc

        self.box = self.makeButtonBox(name, text, eventHandler, color, position, buttonTextColor=textColor)
        self.text = self.makeButtonText(self.box, name, text, buttonColor=textColor)

    def makeButtonText(self, button, buttonID, buttonText, buttonColor = (255,255,255), buttonPos = (0, 0, 0.5), buttonRot = (0,0,0), buttonScale = (0.5, 2, 1)):
        buttonText = Text(
            object_id=buttonID+"_text",
            text=buttonText,
            align="center",
                
            position=buttonPos,
            rotation=buttonRot,
            scale=buttonScale,

            color=buttonColor,

            parent = button,
            persist=True,
        )
        self.scene.add_object(buttonText)
        return buttonText

    def makeButtonBox(self, buttonID, buttonText, buttonHandler, buttonColor = (128,128,128), buttonPos = (0,0,0), buttonRot = (0,0,0), buttonScale = (0.4, 0.08, 0.04), buttonTextColor = (255,255,255)):
        button = Box(
            object_id=buttonID,

            position=buttonPos,
            rotation=buttonRot,
            scale=buttonScale,

            color=buttonColor,

            parent = self.npc,
            clickable=True,
            persist=True,
            evt_handler=buttonHandler,
        
        )
        self.scene.add_object(button)
        return button
    
