from arena import *

import json
import re

# ------------------------ #

#Define Yarn Dialogue Classes and Subcomponents of data structure.
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

class Line:
    def __init__(self, lineString):
        self.text = self.getTextFromLine(lineString)
        self.choices = self.getChoicesFromLine(lineString)
        self.commands = self.getCommandsFromLine(lineString)
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

class Node:
    def __init__(self, titleString, bodyString):
        self.title = titleString
        self.lines = self.getLinesFromBodyString(bodyString)
    def getLinesFromBodyString(self, bodyString):
        lineStrings = bodyString.split("\n")
        lines = []
        for c in range(len(lineStrings)):
            lines.append(Line(lineStrings[c]))
        return lines

class Dialogue:
    def __init__(self, filename):
        self.nodes = self.getNodesFromFile(filename)
        self.currentNode = self.nodes[0] 
    def getNodesFromFile(self, filename):
        # Open file
        f = open(filename)
        yarnJson = json.load(f) #yarnJson is a list of nodeJsons.
        # Iterating through the json list
        nodes = []
        for nodeJson in yarnJson['nodes']:
            nodes.append(Node(nodeJson["title"], nodeJson["body"]))
        # Closing file
        f.close()
        return nodes
                    
# ------------------------ #

'''
#functions to control choice button click behaviour
def onClickLineChoiceButton(nextNode):
    return

#functions to create chat bubble from current line (at parent position)
def createSpeechBubbleFromLine(line, npc):
    speech = getTextFromLine(line)
    
    speechBubble = Text(
        object_id=npc.object_id + "_speechBubble",
        text=speech,
        parent=npc,
        align="center",
        color=(200,200,200),
        position=(0,0.3,0),
        scale=(0.4,0.4,0.4),
    )

    # add the box
    scene.add_object(speechBubble)

    return

def createChoiceButtonsFromLine(line, npc):
    choices = getChoicesFromLine(line)

    for c in range(len(choices)):
        choiceButton = Text(
            object_id=npc.object_id + "_choiceButton_"+str(c),
            text=choices[c],
            parent=npc,
            align="center",
            color=(200,200,200),
            position=(0,-0.1 + c * 0.05,-0.3),
            scale=(0.4,0.4,0.4),
        )
    
    return
'''

# ------------------------ #

# setup ARENA scene
scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="NPC")

# create Dialogue, and show contents
dialogue = Dialogue("cartoon_dialogue.json")

# Iterating through the json list
for node in dialogue.nodes:
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
    
'''
@scene.run_once
def main():
    
    my_box = Box(
        object_id="my_box",
        position=(1,2,-2),
        clickable=True,
        evt_handler=click_box
    )
    
    # make a box
    box = Box(object_id="my_box", position=Position(0,4,-2), scale=Scale(2,2,2))
    print(box.json())
    
    # add the box
    scene.add_object(box)


# add and start tasks
# scene.run_once(main)
scene.run_tasks()
'''



