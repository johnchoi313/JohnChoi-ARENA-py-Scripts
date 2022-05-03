from arena import *

import json
import re

# get file and extract as JSON
f = open("cartoon_dialogue.json")
dialogue = json.load(f)

# Iterating through the json list
for i in dialogue['nodes']:

    print("\n")
 
    #parse body, splitting by newline
    lines = i["body"].split("\n")

    print(lines)
    #print("\n")

    for line in lines:
        print(line)
        
        # extract text
        text = re.sub(r'\<\<.*?\>\>', "", line)
        text = re.sub(r'\[\[.*?\]\]', "", text)
        print("  Text: " + str(text))

        # extract commands (format << >>)
        commands = re.findall(r'\<\<.*?\>\>', line)
        print("  Commands: " + str(commands))
        for c in range(len(commands)):            
            command = commands[c].replace("<","").replace(">","")
            commandType = command.split(' ')[0]
            commandText = command.split(' ')[1]            
            print("    (" + str(c) + "): " + command)
            print("      commandType: " + commandType)
            print("      commandText: " + commandText)
            
        #extract choices (format [[|]])
        choices = re.findall(r'\[\[.*?\]\]', line)
        print("  Choices: " + str(choices))
        for c in range(len(choices)):
            choice = choices[c].replace("[","").replace("]","")
            choiceText = choice.split('|')[0]
            choiceNode = choice.split('|')[1]            
            print("    (" + str(c) + "): " + choice)
            print("      choiceText: " + choiceText)
            print("      choiceNode: " + choiceNode)
            
# Closing file
f.close()

# --- Now, we can play with Dialogue nodes. --- #




'''

# setup library
scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="NPC")


def main():
    # make a box
    box = Box(object_id="my_box", position=Position(0,4,-2), scale=Scale(2,2,2))
    print(box.json())
    # add the box
    scene.add_object(box)

# add and start tasks
scene.run_once(main)
scene.run_tasks()

'''