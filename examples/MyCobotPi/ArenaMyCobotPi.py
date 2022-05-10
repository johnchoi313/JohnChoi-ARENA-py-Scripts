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
myCobot = MyCobot(port = "COM3", baudrate = 115200, debug=True)
myCobot.send_angles([0,0,0,0,0,0], 50) #reset pose

#------MAKE CONNECT TO ARENA------#
scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="MyCobotPi")

#------MAKE ROBOT ARM------#
MyCobotPi_J0 = GLTF(
    object_id="MyCobotPi_J0",
    url="/store/users/johnchoi/MyCobotPi/MyCobotPi_J0/MyCobotPi_J0.gltf",
    position=(0,0,0),
    rotation=(0,0,0),
    scale=(1,1,1),
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
    
def button1_handler(scene, evt, msg):
    if evt.type == "mousedown":
        print("Button pressed!")
        maxAngle = 80
        j1 = random.uniform(-maxAngle,maxAngle)
        j2 = random.uniform(-maxAngle,maxAngle)
        j3 = random.uniform(-maxAngle,maxAngle)
        j4 = random.uniform(-maxAngle,maxAngle)
        j5 = random.uniform(-maxAngle,maxAngle)
        j6 = random.uniform(-maxAngle,maxAngle)
        rotateMyCobot([j1,j2,j3,j4,j5,j6])

#------MAKE BUTTONS ------#
button1 = Box(
    object_id="button1",

    position=(0.5, 0, 2),
    rotation=(0, 0, 0),
    scale=(0.5, 0.1, 0.5),

    color=(0, 255, 0),

    clickable=True,
    persist=True,
    evt_handler=button1_handler,
)
button1_text = Box(
    object_id="button1",

    position=(0.5, 0, 2),
    rotation=(0, 0, 0),
    scale=(0.5, 0.1, 0.5),

    color=(0, 255, 0),

    clickable=True,
    persist=True,
    evt_handler=button1_handler,
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
    scene.add_object(button1)

'''
@scene.run_async
async def programUpdate():
    # add click_listener
    scene.update_object(button1, 
                        click_listener=True, 
                        evt_handler=button1_handler)
'''

scene.run_tasks()
