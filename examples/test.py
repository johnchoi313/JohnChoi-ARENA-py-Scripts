from arena import *
import random

scene = Scene(host="mqtt.arenaxr.org", namespace="johnchoi", scene="example")

def click(scene, evt, msg):
    if evt.type == "mouseup":
        print("mouseup!")
    elif evt.type == "mousedown":
        print("mousedown!")

@scene.run_once
def main():
    my_tet = scene.get_persisted_obj("my_tet")
    scene.update_object(my_tet, clickable=True, evt_handler=click)

scene.run_tasks()