from arena import *

#---PRE-DEFINED QUICK ACTION MAPPINGS---#

# Shorthand sound names mapped to (Sound URL, volume, loop)
soundMappings = {
    "next" : Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "choice" : Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "enter" :  Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "exit" :  Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3"),
    "talking" : Sound(positional=True, poolSize=1, autoplay=True, src="store/users/wiselab/audio/september.mp3")
}

# Shorthand animation names mapped to (animationName, crossFade, timeScale, loopMode['once', 'repeat', 'pingpong'])
animationMappings = {
    "idle" : AnimationMixer(clip="*", loop="repeat"),
    "walk" : AnimationMixer(clip="*", loop="repeat"),
    "talk" : AnimationMixer(clip="*", loop="repeat")
}

# Shorthand transform names mapped to transform action over time
transformMapping = {
    "point1" : [              
        Animation(property="rotation", end=(0,180,0), easing="linear", dur=1000),
        Animation(property="position", end=(0,0,-10), easing="linear", dur=1000)   
    ]
}

# Shorthand morph names mapped to list of morph target names with weights
morphMappings = {
    "smile" : [Morph(morphtarget="eyeTop",value=0.0), Morph(morphtarget="eyeBottom",value=0.0)],
    "frown" : [Morph(morphtarget="eyeTop",value=0.0), Morph(morphtarget="eyeBottom",value=0.0)]
}

'''
# Shorthand emoji names mapped to (PNG URL)
emojiMappings = {
    "exclamation" : "",
    "question" : "",
    
    "smile" : "",
    "cry" : "",
    
    "heart" : "",
    "fire" : ""
}
'''
