
from asyncio import create_subprocess_exec
from arena import *

import colorama
from colorama import Fore
colorama.init(strip=False)

import json
import re

# ------------------------------------------ #
# -----------STARTING VARIABLES------------- #
# ------------------------------------------ #

HOST = "mqtt.arenaxr.org"
NAMESPACE = "johnchoi"
SCENE = "NPC"

DIALOGUE_FILENAME = "cartoon_dialogue.json"

# ------------------------------------------ #
# ----------YARN DIALOGUE CLASSES----------- #
# ------------------------------------------ #

#Define Yarn Dialogue Classes and Subcomponents of data structure.
class Dialogue:
    def __init__(self, filename):
        self.nodes = self.getNodesFromFile(filename)
        self.currentNode = self.nodes[0] 
    def getNodesFromFile(self, filename):
        # Open file
        f = open(filename)
        
        jsonString = f.read()

        print(Fore.YELLOW + jsonString + Fore.WHITE)

        jsonString = "{\"nodes\":" + jsonString + "}"

        yarnJson = json.loads(jsonString) #yarnJson is a list of nodeJsons.
        
        # Iterating through the json list
        nodes = []
        for nodeJson in yarnJson['nodes']:
            nodes.append(Node(nodeJson["title"], nodeJson["body"]))
        # Closing file
        f.close()
        return nodes

    def getNodeIndexFromString(self, nodeName):
        print("Boboby")
        print(nodeName)
        for i in range(len(self.nodes)):

            print("    " + self.nodes[i].title + " | " + nodeName)

            if self.nodes[i].title == nodeName:
                return i

        print(Fore.RED + "Node with name \"" + nodeName + "\" not found!")

        return 0

    def printInfo(self):
        for node in self.nodes:
            print("\n")
            print("NodeTitle: " + node.title)        
            
            for l in range(len(node.lines)):
                line = node.lines[l]
                #show full unprocessed lines
                print("  "+str(l)+". Text: " + line.text)        
                # extract commands (format << >>)
                for c in range(len(line.commands)):            
                    print("    <<"+str(c)+">> commandType: " + line.commands[c].type)
                    print(         "          commandText: " + line.commands[c].text)
                #extract choices (format [[|]])
                for c in range(len(line.choices)):
                    print("    [["+str(c)+"]] choiceText: " + line.choices[c].text)
                    print(         "          choiceNode: " + line.choices[c].node)
        print("\n")

class Node:
    def __init__(self, titleString, bodyString):
        self.title = titleString
        self.lines = self.getLinesFromBodyString(bodyString)
        self.currentLineIndex = 0
    def getLinesFromBodyString(self, bodyString):
        lineStrings = bodyString.split("\n")
        lines = []
        for c in range(len(lineStrings)):
            lines.append(Line(lineStrings[c]))
        return lines

class Line:
    def __init__(self, lineString):
        self.text = self.getTextFromLine(lineString)
        self.choices = self.getChoicesFromLine(lineString)
        self.commands = self.getCommandsFromLine(lineString)
        self.currentChoiceIndex = 0
    def getTextFromLine(self, lineString): #[Input: line is a single dialogue line] -> [Output: Dialogue Text only] 
        text = re.sub(r'\<\<.*?\>\>', "", lineString)
        text = re.sub(r'\[\[.*?\]\]', "", text)
        return text
    def getCommandsFromLine(self, lineString): #[Input: line is a single dialogue line] -> [Output: List of string commands in <<>>s, brackets removed.]
        commandStrings = re.findall(r'\<\<.*?\>\>', lineString)
        commands = []
        for c in range(len(commandStrings)):            
            commandStrings[c] = commandStrings[c].replace("<","").replace(">","")
            commands.append(Command(commandStrings[c]))
        return commands
    def getChoicesFromLine(self, lineString): #[Input: line is a single dialogue line] -> [Output: List of string choices in [[]]s, brackets removed.]
        choiceStrings = re.findall(r'\[\[.*?\]\]', lineString)
        choices = []
        for c in range(len(choiceStrings)):
            choiceStrings[c] = choiceStrings[c].replace("[","").replace("]","")
            choices.append(Choice(choiceStrings[c]))
        return choices

class Command:
    def __init__(self, commandString):
        self.type = self.getTypeFromCommand(commandString)
        self.text = self.getTextFromCommand(commandString)
    def getTypeFromCommand(self, commandString): #[Input: String command in <<>>] -> [Output: Command TYPE, split by ' '.]
        if(commandString.count(' ') != 1): return ""
        commandType = commandString.split(' ')[0]
        return commandType         
    def getTextFromCommand(self, commandString): #[Input: String command in <<>>] -> [Output: Command TEXT, split by ' '.]
        if(commandString.count(' ') != 1): return ""
        commandText = commandString.split(' ')[1]
        return commandText

class Choice:
    def __init__(self, choiceString):
        self.text = self.getTextFromChoice(choiceString)
        self.node = self.getNodeFromChoice(choiceString)
    def getTextFromChoice(self, choiceString): #[Input: String choice in [[]] ] -> [Output: Choice TEXT, split by '|'.]
        if(choiceString.count('|') != 1): return ""
        choiceText = choiceString.split('|')[0]
        return choiceText         
    def getNodeFromChoice(self, choiceString): #[Input: String choice in [[]] ] -> [Output: Choice NODE, split by '|'.]
        if(choiceString.count('|') != 1): return ""
        choiceNode = choiceString.split('|')[1]
        return choiceNode 

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
    
class ArenaDialogueBubbleGroup():
    def __init__(self, scene, npc, line):
        self.scene = scene
        self.npc = npc

        self.speechBubble = self.createSpeechBubble(line)
        self.buttons = self.createButtons(line)

    def runCommands(self, line):
        commands = line.commands
        return

    #functions to create chat bubble from current line (at parent position)
    def createSpeechBubble(self, line):
        speech = line.text
        
        speechBubble = Text(
            object_id=self.npc.object_id + "_speechBubble",
            text=speech,
            parent=self.npc,
            align="center",
            color=(200,200,200),
            position=(0,0.7,0),
            scale=(0.4,0.4,0.4),

            #clickable=True,
            #evt_handler=onClickNextButton
        )
        self.scene.add_object(speechBubble) # add the box
        return speechBubble

    def createButtons(self, line):
        choices = line.choices
        self.buttons = []
        if(len(choices) > 0): 
            for c in range(len(choices)):                
                choiceButton = Button(scene, self.npc, self.npc.object_id + "_choiceButton_"+str(c), choices[c].text, onClickChoiceButton, 
                                      position = (0.5, 0.2 + c * 0.15, 0.5), color = (100,100,200), textColor = (200,200,200))


                self.buttons.append(choiceButton)
        else: 
            nextButton = Button(scene, self.npc, self.npc.object_id + "_nextButton", "[Next]", onClickNextButton, 
                                position = (0,0.2,0.6), color = (100,100,200), textColor = (200,200,200))
                
            self.buttons.append(nextButton)
        return self.buttons

    def createNewButtons(self, line):


        self.createSpeechBubble(line)
        self.createButtons(line)
        self.runCommands(line)

    def clearButtons(self):
        print("deleting speechBubble...")
        self.scene.delete_object(self.speechBubble)
        print("speechBubble deleted.")

        for button in self.buttons:
            self.scene.delete_object(button.box)
            self.scene.delete_object(button.text)
            
        self.buttons = []

        return

# ------------------------------------------ #
# ------------HELPER VARIABLES-------------- #
# ------------------------------------------ #

#functions to control choice button click behaviour
def onClickChoiceButton(scene, evt, msg):
    if evt.type == "mousedown":
        print("Choice Button Pressed!")
    
        print(msg)

        print(msg["object_id"])

        choiceButtonID = msg["object_id"]

        print(choiceButtonID)

        filterLen = len(npc.object_id + "_choiceButton_")

        print(filterLen)

        choiceButtonNumber = int(choiceButtonID[filterLen:])

        print(choiceButtonNumber)

        choiceNodeName = dialogue.currentNode.lines[dialogue.currentNode.currentLineIndex].choices[choiceButtonNumber].node

        print(choiceNodeName)
        

        print("Clearing buttons.")
        bubbles.clearButtons()
        print("Buttons cleared.")

        #get the current line represented by the selections

        
        dialogue.currentNode = dialogue.nodes[dialogue.getNodeIndexFromString(choiceNodeName)]

        print("Bob.")

        dialogue.currentNode.currentLineIndex = 0

        bubbles.createNewButtons(dialogue.currentNode.lines[dialogue.currentNode.currentLineIndex])
            
        #bubbles.createNewButtons( dialogue.currentNode.currentLine )

    print("")

'''
#functions to control choice button click behaviour
def onClickSpeechBubble(scene, evt, msg):
    if evt.type == "mousedown":
        dialogue.
        dialogue.createNewButtons(dialogue.currentNode.currentLine)
'''

#functions to control choice button click behaviour
def onClickNextButton(scene, evt, msg):
    if evt.type == "mousedown":
        print("Next Button Pressed!")
        
        print("Clearing buttons.")
        bubbles.clearButtons()
        print("Buttons cleared.")
        dialogue.currentNode.currentLineIndex = dialogue.currentNode.currentLineIndex + 1

        if(dialogue.currentNode.currentLineIndex <= len(dialogue.currentNode.lines)):
            print("Creating new buttons.")
            bubbles.createNewButtons(dialogue.currentNode.lines[dialogue.currentNode.currentLineIndex])
            print("New buttons created.")
        else:
            print("No new buttons created.")
            
    print("")
    
# ------------------------------------------ #
# --------MAIN LOOP/INITIALIZATION---------- #
# ------------------------------------------ #

# setup ARENA scene
scene = Scene(host=HOST, namespace=NAMESPACE, scene=SCENE)

# create Dialogue, and show contents
dialogue = Dialogue(DIALOGUE_FILENAME)

# Iterating through the json list
dialogue.printInfo()

#Initialize text, buttons, and command from current line from current node:
dialogue.currentNode.currentLine = dialogue.currentNode.lines[0]
line = dialogue.currentNode.currentLine

npc = Box(
    object_id="NPC",
    position=(0,0,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    color=(255,100,16),
    material = Material(opacity=0.3, transparent=True),
    persist=True
)
scene.add_object(npc)

bubbles = ArenaDialogueBubbleGroup(scene , npc , line)

@scene.run_once
def programStart():
    print("Completed.")

scene.run_tasks()



