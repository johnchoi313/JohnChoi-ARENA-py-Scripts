from arena import *

scene = Scene(host="arenaxr.org", namespace = "johnchoi", scene="NPC")

@scene.run_once
def make_box():
    scene.add_object(Box())

scene.run_tasks()
