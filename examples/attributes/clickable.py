from arena import *
import random

scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="NPC")

def click_tet(scene, evt, msg):
    if evt.type == "mouseup":
        print("mouseup tet!")
    elif evt.type == "mousedown":
        print("mousedown tet!")

def click_box(scene, evt, msg):
    if evt.type == "mouseup":
        print("mouseup box!")
    elif evt.type == "mousedown":
        print("mousedown box!")


@scene.run_once
def main():
    my_tet = Tetrahedron(
        object_id="my_tet",
        position=(-1,2,-5),
        clickable=True,
        evt_handler=click_tet
    )
    scene.add_object(my_tet)

    my_box = Box(
        object_id="my_box",
        position=(1,2,-2),
        clickable=True,
        evt_handler=click_box
    )
    scene.add_object(my_box)


scene.run_tasks()
