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

#------MAKE ROBOT ARM------#
myCobot = MyCobot(port = "/dev/ttyAMA0", baudrate = 1000000, debug=True)
myCobot.send_angles([0,0,0,0,0,0], 50) #reset pose
myCobot.set_color(247, 0, 255)

#------MAKE CONNECT TO ARENA------#
scene = Scene(host="mqtt.arenaxr.org", namespace = "zhilu", scene="arena")

#------MAKE ROBOT ARM------#
AprilTag = Box(
    object_id="[SpotAR] Cobot 100",
    position=(-2.79,1.688,-0.176),
    rotation=(0,90,0),
    scale=(0.15,0.15,0.06),
    persist=True
)
MyCobotPi_J0 = GLTF(
    object_id="MyCobotPi_J0",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J0/MyCobotPi_J0.gltf",
    position=(-0.4,-0.75,0.8),
    rotation=(0,0,0),
    scale=(1,1,1),
    parent=AprilTag,
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
    myCobot.send_angles(angles, 50)
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

        if currAngles[0]+10<80:
            currAngles[0] = currAngles[0]+10

        rotateMyCobot(currAngles)

def j2AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 2 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()
        if currAngles[1]+10<80:
            currAngles[1] = currAngles[1]+10

        rotateMyCobot(currAngles)
        
def j3AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 3 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()
        if currAngles[2]+10<80:
            currAngles[2] = currAngles[2]+10

        rotateMyCobot(currAngles)

def j4AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 4 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()
        if currAngles[3]+10<80:
            currAngles[3] = currAngles[3]+10

        rotateMyCobot(currAngles)

def j5AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 5 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[4]+10<80:
            currAngles[4] = currAngles[4]+10

        rotateMyCobot(currAngles)

def j6AnglePos_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 6 Positive Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[5]+10<80:
            currAngles[5] = currAngles[5]+10

        rotateMyCobot(currAngles)

### PRECISE CONTROLS --> NEGATIVE ANGLES

def j1AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 1 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[0]-10>-80:
            currAngles[0] = currAngles[0]-10

        rotateMyCobot(currAngles)

def j2AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 2 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[1]-10>-80:
            currAngles[1] = currAngles[1]-10

        rotateMyCobot(currAngles)
        
def j3AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 3 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[2]-10>-80:
            currAngles[2] = currAngles[2]-10

        rotateMyCobot(currAngles)

def j4AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 4 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[3]-10>-80:
            currAngles[3] = currAngles[3]-10

        rotateMyCobot(currAngles)

def j5AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 5 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[4]-10>-80:
            currAngles[4] = currAngles[4]-10

        rotateMyCobot(currAngles)

def j6AngleNeg_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Joint 6 Negative Button pressed!")
        
        currAngles = myCobot.get_angles()

        if currAngles[5]-10>-80:
            currAngles[5] = currAngles[5]-10

        rotateMyCobot(currAngles)





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
        parent = MyCobotPi_J0,
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
        parent = MyCobotPi_J0,
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

        parent = MyCobotPi_J0,    
        persist=True,
    )


#------ PROGRAM INIT/UPDATE ------#

@scene.run_once
def programStart():
    # Add myCobotPi 
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

    

 
@scene.run_forever(interval_ms=100)
# data text display


def makeText():
    angles = myCobot.get_angles()
    my_text = Text(
        object_id="data_text",
        text=f"Joint 1: {angles[0]}, Joint 2: {angles[1]}, Joint 3: {angles[2]}, Joint 4: {angles[3]}, Joint 5: {angles[4]}, Joint 6: {angles[5]}",
        align="center",
        font="mozillavr", 
        position=(0, 1, 0),
        scale=(0.3,0.3,0.3),
        color=(100,255,255),
        parent = MyCobotPi_J0
    )
    scene.add_object(my_text)


    
scene.run_tasks()