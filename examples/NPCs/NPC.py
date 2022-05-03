from arena import *

import json
import re

# ------------------------ #

#functions to process and extract data from node
def getLinesFromNode(node): #[Input: Node is a JSON string] -> [Output: List of dialogue lines.] 
    lines = node["body"].split("\n")
    return lines

def getTextFromLine(line): #[Input: line is a single dialogue line] -> [Output: Dialogue Text only] 
    text = re.sub(r'\<\<.*?\>\>', "", line)
    text = re.sub(r'\[\[.*?\]\]', "", text)
    return text

def getCommandsFromLine(line): #[Input: line is a single dialogue line] -> [Output: List of string commands in <<>>s, brackets removed.]
    commands = re.findall(r'\<\<.*?\>\>', line)
    for c in range(len(commands)):            
        commands[c] = commands[c].replace("<","").replace(">","")
    return commands
def getTypeFromCommand(command): #[Input: String command in <<>>] -> [Output: Command TYPE, split by ' '.]
    if(command.count(' ') != 1): return ""
    commandType = command.split(' ')[0]
    return commandType         
def getTextFromCommand(command): #[Input: String command in <<>>] -> [Output: Command TEXT, split by ' '.]
    if(command.count(' ') != 1): return ""
    commandText = command.split(' ')[1]
    return commandText         

def getChoicesFromLine(line): #[Input: line is a single dialogue line] -> [Output: List of string choices in [[]]s, brackets removed.]
    choices = re.findall(r'\[\[.*?\]\]', line)
    for c in range(len(choices)):
        choices[c] = choices[c].replace("[","").replace("]","")
    return choices
def getTextFromChoice(choice): #[Input: String choice in [[]] ] -> [Output: Choice TEXT, split by '|'.]
    if(choice.count('|') != 1): return ""
    choiceText = choice.split('|')[0]
    return choiceText         
def getNodeFromChoice(choice): #[Input: String choice in [[]] ] -> [Output: Choice NODE, split by '|'.]
    if(choice.count('|') != 1): return ""
    choiceNode = choice.split('|')[1]
    return choiceNode         

# ------------------------ #

# get file and extract as JSON
f = open("cartoon_dialogue.json")
dialogueNodes = json.load(f)

# Iterating through the json list
for node in dialogueNodes['nodes']:
    print("\n")
 
    #parse body, splitting by newline
    lines = getLinesFromNode(node)
    print(lines)
    for line in lines:
        #show full unprocessed lines
        print(line)        
        # extract text
        print("  Text: " + getTextFromLine(line))
        # extract commands (format << >>)
        commands = getCommandsFromLine(line)
        print("  Commands: " + str(commands))
        for c in range(len(commands)):            
            print("    (" + str(c) + "): " + commands[c])
            print("      commandType: " + getTypeFromCommand(commands[c]))
            print("      commandText: " + getTextFromCommand(commands[c]))
        #extract choices (format [[|]])
        choices = getChoicesFromLine(line)
        print("  Choices: " + str(choices))
        for c in range(len(choices)):
            print("    (" + str(c) + "): " + choices[c])
            print("      choiceText: " + getTextFromChoice(choices[c]))
            print("      choiceNode: " + getNodeFromChoice(choices[c]))
            
# Closing file
f.close()

# ------------------------ #

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

# ------------------------ #


# setup ARENA scene
scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="NPC")

# Load first node (node 0) as current node. #
currentNode = dialogueNodes['nodes'][0]
currentLine = getLinesFromNode(currentNode)[0]

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




