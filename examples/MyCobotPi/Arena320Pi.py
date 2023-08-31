import time
import math
import sys
import os
import random

from arena import *

import serial
import serial.tools.list_ports

from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

#pygame for controller
#import pygame
#from pygame.locals import *
#pygame.init()

#pygame.joystick.init()
#joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

#------MAKE ROBOT ARM------#
myCobot = MyCobot(port = "/dev/ttyAMA0", baudrate = 115200, debug=True)
myCobot.send_angles([0,0,0,0,0,0], 50) #reset pose
myCobot.set_color(247, 0, 255)
myCobot.set_gripper_value(99, 80)

# initiate pose sequencer array

poses = []

#------MAKE CONNECT TO ARENA------#
#scene = Scene(host="arenaxr.org", namespace = "zhilu", scene="arena")
scene = Scene(host="arenaxr.org", namespace = "public", scene="arena")

#------MAKE ROBOT ARM------#
MyCobotPi_Base = Box(
    object_id = "MyCobotPi_Base",
    position = (-2, 0.8, -3),
    rotation = (0,0,0),
    material = Material(opacity = 0.1, transparent = True),
    persist = True
)

MyCobotPi_J0 = GLTF(
    object_id="MyCobotPi_J0",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J0/MyCobotPi_J0.gltf",
    position=(0,0,0),
    rotation=(0,90,0),
    scale=(1,1,1),
    parent = MyCobotPi_Base,
    persist=True
)
MyCobotPi_J1 = GLTF(
    object_id="MyCobotPi_J1",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J1/MyCobotPi_J1.gltf",
    position=(0,0,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=MyCobotPi_J0,
    persist=True
)
MyCobotPi_J2 = GLTF(
    object_id="MyCobotPi_J2",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J2/MyCobotPi_J2.gltf",
    position=(0,0.1433,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=MyCobotPi_J1,
    persist=True
)
MyCobotPi_J3 = GLTF(
    object_id="MyCobotPi_J3",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J3/MyCobotPi_J3.gltf",
    position=(0,0.1075,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=MyCobotPi_J2,
    persist=True
)
MyCobotPi_J4 = GLTF(
    object_id="MyCobotPi_J4",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J4/MyCobotPi_J4.gltf",
    position=(0,0.09710006,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=MyCobotPi_J3,
    persist=True
)
MyCobotPi_J5 = GLTF(
    object_id="MyCobotPi_J5",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J5/MyCobotPi_J5.gltf",
    position=(0.06340005,0,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=MyCobotPi_J4,
    persist=True
)
MyCobotPi_J6 = GLTF(
    object_id="MyCobotPi_J6",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J6/MyCobotPi_J6.gltf",
    position=(0,0.07610026,0),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=MyCobotPi_J5,
    persist=True
)

#------MAKE BUTTON FUNCTIONS ------#
def rotateMyCobot(angles):
    if(len(angles) != 6):
        print("Error: angles must have exactly 6 values. Ignoring!")
        return    
    #update arena virtual robot
    MyCobotPi_J1.update_attributes(rotation=Rotation(0,angles[0],0))
    MyCobotPi_J2.update_attributes(rotation=Rotation(angles[1],0,0))
    MyCobotPi_J3.update_attributes(rotation=Rotation(angles[2],0,0))
    MyCobotPi_J4.update_attributes(rotation=Rotation(angles[3],0,0))
    MyCobotPi_J5.update_attributes(rotation=Rotation(0,angles[4],0))
    MyCobotPi_J6.update_attributes(rotation=Rotation(0,0,angles[5]))
    scene.update_object(MyCobotPi_J1)
    scene.update_object(MyCobotPi_J2)
    scene.update_object(MyCobotPi_J3)
    scene.update_object(MyCobotPi_J4)
    scene.update_object(MyCobotPi_J5)
    scene.update_object(MyCobotPi_J6)
    #update real robot
    myCobot.send_angles(angles, 80)
    print("::send_angles() ==> angles {}, speed 100\n".format(angles))

randomColorButton = Box(object_id="randomColorButton")
def setMyCobotColor(r,g,b):
    #update arena virtual robot
    randomColorButton.update_attributes(color=(r,g,b,))
    scene.update_object(randomColorButton)
    #update real robot
    myCobot.set_color(r,g,b)
    print("::set_color() ==> color {}\n".format("255 255 0"))
    
def randomColorButton_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Random Color Button pressed!")
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        setMyCobotColor(r,g,b)

def randomAngleButton_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Random Angle Button pressed!")
        maxAngle = 80
        j1 = random.uniform(-maxAngle,maxAngle)
        j2 = random.uniform(-maxAngle,maxAngle)
        j3 = random.uniform(-maxAngle,maxAngle)
        j4 = random.uniform(-maxAngle,maxAngle)
        j5 = random.uniform(-maxAngle,maxAngle)
        j6 = random.uniform(-maxAngle,maxAngle)
        rotateMyCobot([j1,j2,j3,j4,j5,j6])

def resetAngleButton_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Reset Button pressed!")
        rotateMyCobot([0,0,0,0,0,0])

### PRECISE CONTROLS --> POSITIVE ANGLES

def j1AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 1 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()


        currAngles[0] = currAngles[0]+10

        rotateMyCobot(currAngles)

def j2AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 2 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()
        
        currAngles[1] = currAngles[1]+10

        rotateMyCobot(currAngles)
        
def j3AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 3 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()
        
        currAngles[2] = currAngles[2]+10

        rotateMyCobot(currAngles)

def j4AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 4 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()
        
        currAngles[3] = currAngles[3]+10

        rotateMyCobot(currAngles)

def j5AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 5 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[4] = currAngles[4]+10

        rotateMyCobot(currAngles)

def j6AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 6 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[5] = currAngles[5]+10

        rotateMyCobot(currAngles)

### PRECISE CONTROLS --> NEGATIVE ANGLES

def j1AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 1 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[0] = currAngles[0]-10

        rotateMyCobot(currAngles)

def j2AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 2 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[1] = currAngles[1]-10

        rotateMyCobot(currAngles)
        
def j3AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 3 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[2] = currAngles[2]-10

        rotateMyCobot(currAngles)

def j4AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 4 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[3] = currAngles[3]-10

        rotateMyCobot(currAngles)

def j5AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 5 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[4] = currAngles[4]-10

        rotateMyCobot(currAngles)

def j6AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 6 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        
        currAngles[5] = currAngles[5]-10

        rotateMyCobot(currAngles)



# gripper button handlers

def randomGripperButton_handler(scene, evt, msg):
    if evt.type =="mousedown":
        print ("Random Gripper button pressed!")

        myCobot.set_gripper_value(random.randrange(0,100), 100)
        
def gripperOpenButton_handler(scene, evt, msg):
    if evt.type =="mousedown":
        print ("Gripper open button pressed!")

        myCobot.set_gripper_value(99, 100)
        
def gripperCloseButton_handler(scene, evt, msg):
    if evt.type =="mousedown":
        print ("Gripper close button pressed!")

        myCobot.set_gripper_value(1, 100)


#pose buttons

def setPoseButton_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print ("Pose set!")

        currAngles = myCobot.get_angles()

        poses.append(currAngles)

def playPosesButton_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print ("Playing poses!")

        for angles in poses:
            rotateMyCobot(angles)



#------MAKE BUTTONS ------#
def makeButtonText(button, buttonID, buttonText, buttonColor = (255,255,255), buttonPos = (0, 0, 0.5), buttonRot = (0,0,0), buttonScale = (0.5, 2, 1)):
    return Text(
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

def makeButton(buttonID, buttonText, buttonHandler, buttonColor = (128,128,128), buttonPos = (0,0,0), buttonRot = (0,0,0), buttonScale = (0.4, 0.08, 0.04), buttonTextColor = (255,255,255)):
    button = Box(
        object_id=buttonID,
        parent = MyCobotPi_Base,
        position=buttonPos,
        rotation=buttonRot,
        scale=buttonScale,

        color=buttonColor,

        clickable=True,
        persist=True,
        evt_handler=buttonHandler,
    )
    buttonText = makeButtonText(button, buttonID, buttonText, buttonColor=buttonTextColor)
    scene.add_object(button)
    scene.add_object(buttonText)
    return button

def makeSmallButton(buttonID, buttonText, buttonHandler, buttonColor = (128,128,128), buttonPos = (0,0,0), buttonRot = (0,0,0), buttonScale = (0.1, 0.08, 0.04), buttonTextColor = (255,255,255)):
    button = Box(
        object_id=buttonID,
        parent = MyCobotPi_Base,
        position=buttonPos,
        rotation=buttonRot,
        scale=buttonScale,

        color=buttonColor,

        clickable=True,
        persist=True,
        evt_handler=buttonHandler,
    )
    buttonText = makeButtonText(button, buttonID, buttonText, buttonColor=buttonTextColor)
    scene.add_object(button)
    scene.add_object(buttonText)
    return button

def makeText(textID, text, textColor=(0,0,0), textPos = (0,0,0), textRot = (0,0,0), textScale = (0.5, 2, 1)):
    return Text(
        object_id=textID+"_text",       
        text=text,
        align="center",
            
        position=textPos,
        rotation=textRot,
        scale=textScale,

        color=textColor,    

        parent = MyCobotPi_Base,    
        persist=True,
    )


#------ PROGRAM INIT/UPDATE ------#

#global text variables so we can update it below
data_text = Text(
    object_id="data_text",
    text="hello",
    font="mozillavr", 
    position=(0, 1, 0),
    scale=(0.2,0.2,0.2),
    color=(100,255,255),
    parent = MyCobotPi_Base
    )

scene.add_object(data_text)

#gripper_text = Text(
        #object_id="gripper_text",
        #text= "hello",
        #align="center",
        #font="mozillavr", 
        #position=(0, 0.9, 0),
        #scale=(0.2,0.2,0.2),
        #color=(100,255,255),
        #parent = MyCobotPi_J0
    #)

#scene.add_object(gripper_text)

@scene.run_once
def programStart():
    # Add myCobotPi 
    scene.add_object(MyCobotPi_Base)
    scene.add_object(MyCobotPi_J0)
    scene.add_object(MyCobotPi_J1)
    scene.add_object(MyCobotPi_J2)
    scene.add_object(MyCobotPi_J3)
    scene.add_object(MyCobotPi_J4)
    scene.add_object(MyCobotPi_J5)
    scene.add_object(MyCobotPi_J6)
    # Add buttons
    makeButton("randomAngleButton", "Go to random angle!", randomAngleButton_handler, buttonColor=(11, 55, 255), buttonPos=(0, 0.55, 0))
    makeButton("resetAngleButton", "Reset angle!", resetAngleButton_handler, buttonColor=(255, 55, 11), buttonPos=(0, 0.65, 0))
    makeButton("randomColorButton", "Set random color!", randomColorButton_handler, buttonColor=(247, 0, 255), buttonPos=(0, 0.75, 0),buttonTextColor=(0,0,0))
    
    #makeButton("randomGripperButton", "Random Gripper Pos", randomGripperButton_handler, buttonColor=(254, 208, 0), buttonPos=(0.7, 0.45, 0),buttonTextColor=(0,0,0))

   

    # adding controller buttons
    makeSmallButton("j1AnglePosButton", "Joint 1", j1AnglePos_handler, buttonColor=(0, 255, 0), buttonPos=(0.5, 0.65, 0))
    makeSmallButton("j1AngleNegButton", "Joint 1", j1AngleNeg_handler, buttonColor=(255, 0, 0), buttonPos=(0.5, 0.55, 0))
    
    makeSmallButton("j2AnglePosButton", "Joint 2", j2AnglePos_handler, buttonColor=(0, 255, 0), buttonPos=(0.6, 0.65, 0))
    makeSmallButton("j2AngleNegButton", "Joint 2", j2AngleNeg_handler, buttonColor=(255, 0, 0), buttonPos=(0.6, 0.55, 0))

    makeSmallButton("j3AnglePosButton", "Joint 3", j3AnglePos_handler, buttonColor=(0, 255, 0), buttonPos=(0.7, 0.65, 0))
    makeSmallButton("j3AngleNegButton", "Joint 3", j3AngleNeg_handler, buttonColor=(255, 0, 0), buttonPos=(0.7, 0.55, 0))

    makeSmallButton("j4AnglePosButton", "Joint 4", j4AnglePos_handler, buttonColor=(0, 255, 0), buttonPos=(0.8, 0.65, 0))
    makeSmallButton("j4AngleNegButton", "Joint 4", j4AngleNeg_handler, buttonColor=(255, 0, 0), buttonPos=(0.8, 0.55, 0))

    makeSmallButton("j5AnglePosButton", "Joint 5", j5AnglePos_handler, buttonColor=(0, 255, 0), buttonPos=(0.9, 0.65, 0))
    makeSmallButton("j5AngleNegButton", "Joint 5", j5AngleNeg_handler, buttonColor=(255, 0, 0), buttonPos=(0.9, 0.55, 0))

    makeSmallButton("j6AnglePosButton", "Joint 6", j6AnglePos_handler, buttonColor=(0, 255, 0), buttonPos=(1, 0.65, 0))
    makeSmallButton("j6AngleNegButton", "Joint 6", j6AngleNeg_handler, buttonColor=(255, 0, 0), buttonPos=(1, 0.55, 0))

    #adding gripper control buttons

    #makeSmallButton("gripperOpenButton", "Open Gripper", gripperOpenButton_handler, buttonColor=(0, 255, 0), buttonPos=(1.3, 0.65, 0))
    #makeSmallButton("gripperCloseButton", "Close Gripper", gripperCloseButton_handler, buttonColor=(255, 0, 0), buttonPos=(1.3, 0.55, 0))


    #adding pose buttons

    #makeButton("playPosesButton", "Play poses", playPosesButton_handler, buttonColor=(11, 55, 255), buttonPos=(0, 0.85, 0))
    #makeButton("setPoseButton", "Set current pose", setPoseButton_handler, buttonColor=(11, 55, 255), buttonPos=(0, 0.95, 0))
    

#init the 2 text displays 

def makeText():
    angles = myCobot.get_angles()
    data_text = Text(
        object_id="data_text",
        text=f"Joint 1: {angles[0]}, Joint 2: {angles[1]}, Joint 3: {angles[2]}, Joint 4: {angles[3]}, Joint 5: {angles[4]}, Joint 6: {angles[5]}",
        align="center",
        font="mozillavr", 
        position=(0, 1, 0),
        scale=(0.2,0.2,0.2),
        color=(100,255,255),
        parent = MyCobotPi_Base
    )

    scene.add_object(data_text)

#def makeGripperText():


    #gripper_text = Text(
        #object_id="gripper_text",
        #text= "Gripper: ",
        #align="center",
        #font="mozillavr", 
        #position=(0, 0.9, 0),
        #scale=(0.2,0.2,0.2),
        #color=(100,255,255),
        #parent = MyCobotPi_J0
    #)

    #scene.add_object(gripper_text)
    

 
@scene.run_forever(interval_ms=500)
# updating data text display and gripper text display ever second

def updateData():

    angles = myCobot.get_angles()

    data_text.data.text = f"Joint 1: {angles[0]}, Joint 2: {angles[1]}, Joint 3: {angles[2]}, Joint 4: {angles[3]}, Joint 5: {angles[4]}, Joint 6: {angles[5]}"


    ######
    #gripper stuff
    #gripperValue = myCobot.get_gripper_value()

    #grippertext = ""

    #if gripperValue <50:
    #    grippertext = "Closed"
    #if gripperValue >= 50:
    #    grippertext = "Open"

    #gripper_text.data.text = "Gripper: " + grippertext


    scene.update_object(data_text)
    #scene.update_object(gripper_text)

#game controller
#for event in pygame.event.get():

    #currAngles = myCobot.get_angles()

    #if event.type == JOYBUTTONDOWN:
        #print(event)
        #if event.button == 6:
            #myCobot.set_gripper_value(99, 100)
        #if event.button == 7:
            #myCobot.set_gripper_value(1, 100)          
        
    #if event.type == JOYAXISMOTION:
        #print(event)

        #left joystick left/right
        #if event.axis == 0:
            #if event.value > 0: #right
                #currAngles[0] = currAngles[0]+10
            #else: #left
                #currAngles[0] = currAngles[0]-10

        #right joystick up/down
        #if event.axis == 3:
            #if event.value > 0: #down
                #currAngles[1] = currAngles[1]-10
            #else: #up
                #currAngles[1] = currAngles[1]+10
       
    #rotateMyCobot(currAngles)

    #if event.type == QUIT:
        #pygame.quit()


    
scene.run_tasks()