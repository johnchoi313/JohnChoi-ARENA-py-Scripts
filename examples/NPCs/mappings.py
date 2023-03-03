from arena import *

#---PRE-DEFINED DEFAULT ACTIONS (triggered when talking/moving/clicking/etc)---#

#DEFAULT SOUNDS (set these to None if you don't want default sound effects, or set USE_DEFAULT_SOUNDS = False)
SOUND_NEXT = Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
SOUND_CHOICE = Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
SOUND_ENTER = Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
SOUND_EXIT = Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
SOUND_TALKING = Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3")

#DEFAULT ANIMATIONS (set these to None if you don't want default animations, or set USE_DEFAULT_ANIMATIONS = False)
ANIM_IDLE = AnimationMixer(clip="idle", loop="repeat"),
ANIM_WALK = AnimationMixer(clip="walk", loop="repeat"),
ANIM_TALK = AnimationMixer(clip="talk", loop="repeat")

#DEFAULT MORPHS (set these to None if you don't want default morphs, or set USE_DEFAULT_MORPHS = False)
MORPH_OPEN  = [Morph(morphtarget="eyeTop",value=0.0), Morph(morphtarget="eyeBottom",value=0.0)],
MORPH_CLOSE = [Morph(morphtarget="eyeTop",value=0.0), Morph(morphtarget="eyeBottom",value=0.0)]

#---PRE-DEFINED QUICK ACTION MAPPINGS (for use in Yarn, because who wants to type all this out every time?)---#

# Shorthand sound names mapped to (Sound URL, volume, loop)
# --Sound Schema: https://docs.arenaxr.org/content/schemas/message/sound.html
# --Sound Example: https://github.com/arenaxr/arena-py/blob/master/examples/attributes/sound.py 
soundMappings = {
    "next" : Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "choice" : Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "enter" :  Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "exit" :  Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "talking" : Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3")
}

# Shorthand animation names mapped to (animationName, crossFade, timeScale, loopMode['once', 'repeat', 'pingpong'])
# --AnimationMixer Schema: https://docs.arenaxr.org/content/schemas/message/animation-mixer.html 
# --AnimationMixer Example: https://github.com/arenaxr/arena-py/blob/master/examples/attributes/animation_mixer.py 
animationMappings = {
    "idle" : AnimationMixer(clip="*", loop="repeat"),
    "walk" : AnimationMixer(clip="*", loop="repeat"),
    "talk" : AnimationMixer(clip="*", loop="repeat")
}

# Shorthand transform names mapped to transform action over time
# --Animation Schema: https://docs.arenaxr.org/content/schemas/message/animation.html 
# --Animation Example: https://github.com/arenaxr/arena-py/blob/master/examples/attributes/animation.py 
transformMappings = {
    "point1" : [              
        Animation(property="rotation", end=(0,180,0), easing="linear", dur=1000),
        Animation(property="position", end=(0,0,-10), easing="linear", dur=1000)   
    ]
}

# Shorthand morph names mapped to list of morph target names with weights
# --Morph Schema: https://docs.arenaxr.org/content/python/animations.html#gltf-morphs
# --Morph Example: https://github.com/arenaxr/arena-py/blob/master/examples/attributes/morph.py
morphMappings = {
    "smile" : [Morph(morphtarget="eyeTop",value=0.0), Morph(morphtarget="eyeBottom",value=0.0)],
    "frown" : [Morph(morphtarget="eyeTop",value=0.0), Morph(morphtarget="eyeBottom",value=0.0)]
}

# Shorthand url names mapped to (Website URL, volume, loop)
# --Url Schema: https://docs.arenaxr.org/content/schemas/message-examples.html#goto-url 
# --Url Example: https://github.com/arenaxr/arena-py/blob/master/examples/attributes/goto_url.py 
urlMappings = {
    "next" : GotoUrl(dest="popup", on="mousedown", url="https://www.conix.io/")
}
