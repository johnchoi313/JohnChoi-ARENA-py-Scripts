
from asyncio import create_subprocess_exec
from arena import *

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
        #SPEECH SETTINGS
        self.SPEECH_TEXT_COLOR = (0,0,0)
        self.SPEECH_TEXT_POSITION = (0,0,0)
        self.SPEECH_TEXT_SCALE = (0.4,0.4,0.4)
        #CHOICE SETTINGS
        self.CHOICE_TEXT_COLOR = (0,0,0)
        self.CHOICE_BUBBLE_COLOR = (0,0,0)
        self.CHOICE_BUBBLE_POSITION = (0,0,0)
        self.CHOICE_BUBBLE_OFFSET_Y = 2
        #create bubbles to init types
        self.createBubbles()

    #reinitializes and restarts the interaction
    def start(self):
        print("\n(---Starting NPC interaction:---)")
        self.clearButtons()
        self.createBubbles()

    #creates new bubbles
    def createBubbles(self, line = None):
        if(line == None):
            self.dialogue.currentNode.currentLine = self.dialogue.currentNode.lines[0]
            line = self.dialogue.currentNode.currentLine
        self.speechBubble = self.createSpeechBubble(line)
        self.buttons = self.createButtons(line)

    #customization functions   
    def setColors(self, speechTextColor, choiceBubbleColor, choiceTextColor):
        self.SPEECH_TEXT_COLOR = speechTextColor
        self.CHOICE_BUBBLE_COLOR = choiceBubbleColor
        self.CHOICE_TEXT_COLOR = choiceTextColor
    
    def setPositionOffsets(self, speechTextPosition, choiceBubblePosition, choiceBubbleOffsetY):
        self.SPEECH_TEXT_POSITION = speechTextPosition
        self.CHOICE_BUBBLE_POSITION = choiceBubblePosition
        self.CHOICE_BUBBLE_OFFSET_Y = choiceBubbleOffsetY

    def setSpeechSettings(self, speechTextColor, speechTextPosition, speechTextScale):
        self.SPEECH_TEXT_COLOR = speechTextColor
        self.SPEECH_TEXT_POSITION = speechTextPosition
        self.SPEECH_TEXT_SCALE = speechTextScale

    def setButtonSettings(self, choiceTextColor, choiceBubbleColor, choiceBubblePosition, choiceBubbleOffsetY):
        self.CHOICE_TEXT_COLOR = choiceTextColor
        self.CHOICE_BUBBLE_COLOR = choiceBubbleColor
        self.CHOICE_BUBBLE_POSITION = choiceBubblePosition
        self.CHOICE_BUBBLE_OFFSET_Y = choiceBubbleOffsetY

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
        
            #<<print "text">>
            if(command.type.lower() == "print".lower()):
                printYellow("    " + command.text)

            #<<hide objectName>>

            #<<show objectName>>


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

            #collide restart
            #-collision enter/exit
            #-collision triggers boundary event

            #<<rotate (x,y,z)>>
            elif(command.type.lower() == "rotate".lower()):
                print("    " + command.text)
            #<<lookAt (x,y,z)>>
            elif(command.type.lower() == "lookAt".lower()):
                print("    " + command.text)

            #<<playSound >>
            elif(command.type.lower() == "playSound".lower()):                
                self.npc = Box(sound = Sound(positional=True, poolSize=1, loop=False, autoplay=True, src=command.text))
                self.scene.add_object(self.npc);

            #<<loopSound >>
            elif(command.type.lower() == "loopSound".lower()):
                self.npc = Box(sound = Sound(positional=True, poolSize=1, loop=True, autoplay=True, src=command.text))
                self.scene.add_object(self.npc);

            #<<playAnimation >>
            elif(command.type.lower() == "playAnimation".lower()):
                self.gltf.dispatch_animation(
                    AnimationMixer(clip=command.text, loop="once")
                )
            #<<loopAnimation >>
            elif(command.type.lower() == "loopAnimation".lower()):
                self.gltf.dispatch_animation(
                    AnimationMixer(clip=command.text, loop="repeat")
                )
            #<<loopAnimation >>
            elif(command.type.lower() == "stopAnimation".lower()):
                self.gltf.dispatch_animation(
                    AnimationMixer(clip=command.text, loop="repeat")
                )


        return

    #functions to create chat bubble from current line (at parent position)
    def createSpeechBubble(self, line):
        speech = line.text
        
        speechBubble = Text(
            object_id=self.npc.object_id + "_speechBubble",
            text=speech,
            parent=self.npc,
            align="center",
            
            color = self.SPEECH_TEXT_COLOR,
            
            position=self.SPEECH_TEXT_POSITION,

            scale=self.SPEECH_TEXT_SCALE,
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
                                      position = (self.CHOICE_BUBBLE_POSITION[0], self.CHOICE_BUBBLE_POSITION[1] + c * self.CHOICE_BUBBLE_OFFSET_Y, self.CHOICE_BUBBLE_POSITION[2]), 
                                      color = self.CHOICE_BUBBLE_COLOR, textColor = self.CHOICE_TEXT_COLOR)

                self.buttons.append(choiceButton)
        else: 
            nextButton = Button(self.scene, self.npc, self.npc.object_id + "_nextButton", "[Next]", self.onClickNextButton, 
                                position = self.CHOICE_BUBBLE_POSITION, color = self.CHOICE_BUBBLE_COLOR, textColor = self.CHOICE_TEXT_COLOR)
                
            self.buttons.append(nextButton)
        return self.buttons

    def createNewButtons(self, line):
        self.createSpeechBubble(line)
        self.createButtons(line)
        self.runCommands(line)

    def clearButtons(self):
        self.scene.delete_object(self.speechBubble)
      
        for button in self.buttons:
            self.scene.delete_object(button.box)
            self.scene.delete_object(button.text)
            
        self.buttons = []

        return

    # ------------------------------------------ #
    # ------------HELPER VARIABLES-------------- #
    # ------------------------------------------ #

    #functions to control choice button click behaviour
    def onClickChoiceButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            #print("Choice Button Pressed!")

            choiceButtonID = msg["object_id"]
            filterLen = len(self.npc.object_id + "_choiceButton_")

            choiceButtonNumber = int(choiceButtonID[filterLen:])
            choiceText = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].text
            choiceNodeName = self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].node
            
            printYellow("  Choice Button with text \"" + choiceText + "\" pressed! Going to Node [" + choiceNodeName + "]:")
            
            self.clearButtons()
            #get the current line represented by the selections
        
            self.dialogue.currentNode = self.dialogue.nodes[self.dialogue.getNodeIndexFromString(choiceNodeName)]
            self.dialogue.currentNode.currentLineIndex = 0
            self.createNewButtons(self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex])
                
            #bubbles.createNewButtons( dialogue.currentNode.currentLine )

    #functions to control choice button click behaviour
    def onClickNextButton(self, scene, evt, msg):
        if evt.type == "mousedown":
            printCyan("  Next Button Pressed!")
            
            self.clearButtons()
            self.dialogue.currentNode.currentLineIndex = self.dialogue.currentNode.currentLineIndex + 1

            if(self.dialogue.currentNode.currentLineIndex <= len(self.dialogue.currentNode.lines)):
                self.createNewButtons(self.dialogue.currentNode.lines[self.dialogue.currentNode.currentLineIndex])


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
    
