# You're a wizard, Quinn

<img src="https://pbs.twimg.com/media/Cen7qkHWIAAdKsB.jpg" height="400">

In this lab, we want you to practice wizarding an interactive device as discussed in class. We will focus on audio as the main modality for interaction but there is no reason these general techniques can't extend to video, haptics or other interactive mechanisms. In fact, you are welcome to add those to your project if they enhance your design.


## Text to Speech and Speech to Text

In the home directory of your Pi there is a folder called `text2speech` containing some shell scripts.

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav

```

you can run these examples by typing 
`./espeakdeom.sh`. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts

```

You can also play audio files directly with `aplay filename`.

After looking through this folder do the same for the `speech2text` folder. In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

## Serving Pages

In Lab 1 we served a webpage with flask. In this lab you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/$ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to [http://ixe00.local:5000]()


## Demo

In the [demo directory](./demo), you will find an example wizard of oz project you may use as a template. **You do not have to** feel free to get creative. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You can control what system says from the controller as well.

## Optional

There is an included [dspeech](./dspeech) demo that uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) for speech to text. If you're interested in trying it out we suggest you create a seperarate virutalenv. 


# Lab 3 Part 2

Create a system that runs on the Raspberry Pi that takes in one or more sensors and requires participants to speak to it. Document how the system works and include videos of both the system and the controller.

## Prep for Part 2

1. Sketch ideas for what you'll work on in lab on Wednesday.

![Sketch](https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%203/sketch.jpg?raw=true)


## Share your idea sketches with Zoom Room mates and get feedback

*what was the feedback? Who did it come from?*


Feedback from Andrew (jl3983): Andrew thought that I should add a "repeat" feature since the instructions are long and they are easy to forget. By adding the repeat feature, the user would be able to listen to a specific step instruction as many times as he/she wants.

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

Supplies used:
- raspberry Pi 
- Speaker: speech to text. The recipe assistant uses the speaker to read the step instructions.
- microphone: text to speech. Microphone was used to capture user inputs.
- adafruit mini pitft: Used to display the picture of the food.
- Sparkfun joystick: used to capture user inputs.

This recipe assistant will teach you how to cook based on the food you have in your home. We can say "next step", "go back", or "repeat" to have the assistant read the next step, the previous step or repeat the current step in the recipe book. In addtion, we can also use the joystick to control the assistant. By pushing left, it will read the previous step in the recipe book. By pushing right, it will read the next step in the recipe book. Finally, it will repeat the instruction of current step if we push down the joystick button.


*Include videos or screencaptures of both the system and the controller.*

video: https://drive.google.com/file/d/1Bzy_rMPjc-ap-GJk3evMtE0HLGaC5qmI/view?usp=sharing


## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?

*The system worked pretty well. It was able to nagivate smoothly between the step instructions and no mistakes were observed.*

### What worked well about the controller and what didn't?

*The speaker and microphone worked very well. In most cases, the joystick worked well, but sometimes a very small movement can cause the joystick to move to a direction and trigger an unexpected response from the recipe assistant.*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

*To design a more autonomous version of the system, we can take user's accents into account when working on speech to text. Since the person who tested my system and I are both non native speakers, the speech to text feature does not correctly recognize our word every time.*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

*From the currently system, I can record what types of food are recommendated the most/most favored by the family members. This dataset can help to develp a more autonomous version of the system in the future. I can use the accelerator to adjust the volume of the speaker, and use the twist as a timer to remind user when the food will be ready.*
