
from asyncio import create_subprocess_exec
from arena import *

from config import *
from mappings import *
from YarnParser import *
from ColorPrinter import *

class Button():
    def __init__(self, scene, npc, name, text, eventHandler, position, rotation, buttonScale, textScale, color, textColor):
        self.scene = scene
        self.npc = npc

        self.box = self.makeButtonBox(name, text, eventHandler, color, position, rotation, buttonTextColor=textColor, buttonScale = buttonScale)
        self.text = self.makeButtonText(self.box, name, text, buttonColor=textColor, buttonScale = textScale)

    def makeButtonText(self, button, buttonID, buttonText, buttonColor = (255,255,255), buttonPos = (0, 0, 0.5), buttonRot = (0,0,0), buttonScale = (0.5, 2, 1)):
        buttonText = Text(
            object_id=buttonID+"_text",
            text=buttonText,
            align="center",
                
            position=buttonPos,
            rotation=buttonRot,
            scale=buttonScale,
            
            material = Material(color = buttonColor, transparent = False, opacity=1),

            parent = button,

            persist=True
        )
        self.scene.add_object(buttonText)
        return buttonText

    def makeButtonBox(self, buttonID, buttonText, buttonHandler, buttonColor = (128,128,128), buttonPos = (0,0,0), buttonRot = (0,0,0), buttonScale = (0.4, 0.08, 0.04), buttonTextColor = (255,255,255)):
        
        
        button = Box(
            object_id=buttonID,

            position=buttonPos,
            rotation=buttonRot,
            scale=(0,0,0),

            parent = self.npc,
            clickable=True,
            

            material = Material(color = buttonColor, transparent = True, opacity=CHOICE_BUBBLE_OPACITY),

            evt_handler=buttonHandler,

            persist=True
        )
        self.scene.add_object(button)
    
    
        animation = Animation(property="scale", start=(0,0,0), end=buttonScale, easing="easeInOutQuad", dur=500)
        button.dispatch_animation(animation)
        self.scene.run_animations(button)

    
        return button