from arena import *

import numpy as np

import time
from pendulum_physical import PendulumPhysical

from utils import *

import BoschPendulum

scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="pendulum")

grabbing = False

grabber = None
child_pose_relative_to_parent = None

orig_position = (0,1.5,-1)
orig_scale = (0.1,0.1,0.1)
grabbed_scale = (0.11,0.11,0.11)

pendulum = PendulumPhysical()

BPsimulation = BoschPendulum(scene, Position(0,0,0), Rotation(0,0,0), Scale(1,1,1))

def box_click(scene, evt, msg):
    global chasis
    global grabbing
    global grabber
    global orig_scale
    global child_pose_relative_to_parent

    if evt.type == "mousedown":
        clicker = scene.users[evt.data.source]
        handRight = clicker.hands.get("handRight", None)
        # handLeft = clicker.hands.get("handLeft", None)

        if not grabbing:
            print("grabbed")

            if handRight is not None:
                grabber = handRight
                #print("Grabber: ",grabber)

                grabbing = True
                hand_pose = pose_matrix(grabber.data.position, grabber.data.rotation)
                print("hand pose ",chasis.data.position, chasis.data.rotation)
                child_pose = pose_matrix(chasis.data.position, chasis.data.rotation)
                print("child pose")
                child_pose_relative_to_parent = get_relative_pose_to_parent(hand_pose, child_pose)
                print("End grabbing")

    elif evt.type == "mouseup":
        if grabbing:
            print("released")
            grabbing = False
            chasis.update_attributes(scale=orig_scale)
            scene.update_object(chasis)

chasis = Box(
    object_id="chasis",
    position=orig_position,
    scale=orig_scale,
    rotation=(1,0,0,0),
    color=(50,60,200),
    parent=None,
    clickable=True,
    evt_handler=box_click
)

arm = Box(
    object_id="arm",
    position=(0,0,0),
    scale=(0.5,7,0.5),
    rotation=(1,0,0,0),
    color=(50,100,100),
    patent=None,
    clickable=True,
    parent=chasis,
    evt_handler=box_click
)

@scene.run_forever(interval_ms=10)
def move_box():
    global pendulum
    global chasis
    global grabber
    global grabbed_scale
    global child_pose_relative_to_parent

    if grabber is not None and child_pose_relative_to_parent is not None and grabbing:
        hand_pose = pose_matrix(grabber.data.position, grabber.data.rotation)
        new_pose = get_world_pose_when_parented(hand_pose, child_pose_relative_to_parent)

        new_position = (new_pose[0,3], new_pose[1,3], new_pose[2,3])
        new_rotation = Utils.matrix3_to_quat(new_pose[:3,:3])
        new_rotation = (new_rotation[3], new_rotation[0], new_rotation[1], new_rotation[2])
        print("New pos ",new_position[0]) # Virtual position
        pendulum.set_position(new_position[0])

        chasis.update_attributes(position=new_position, scale=grabbed_scale)#, rotation=new_rotation)
        scene.update_object(chasis)
        print("Finished move box update")

@scene.run_forever(interval_ms=100)
def update_pendulum():
    global pendulum
    global arm

    theta_rad = pendulum.get_rotation()
    if theta_rad is not None:
        theta_deg = np.degrees(theta_rad)
        arm.update_attributes(rotation=(0,0,theta_deg))
        scene.update_object(chasis)

@scene.run_once
def make_objects():
    global pendulum 
    pendulum.set_position(0)
    scene.add_object(chasis)
    scene.add_object(arm)

# @scene.run_async
# async def update_pendulum():
#     while True:
#         pendulum.set_position(.07)
#         await scene.sleep(1000)
#         pendulum.set_position(-.07)
#         await scene.sleep(1000)

if __name__ == "__main__":
    scene.run_tasks()
