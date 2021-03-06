# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

In Lab 5 part 1, we focus on detecting and sense-making.

In Lab 5 part 2, we'll incorporate interactive responses.


## Prep

1.  Pull the new Github Repo.
2.  Read about [OpenCV](https://opencv.org/about/).
3.  Read Belloti, et al's [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf)

### For the lab, you will need:

1. Raspberry Pi
1. Raspberry Pi Camera (2.1)
1. Microphone (if you want speech or sound input)
1. Webcam (if you want to be able to locate the camera more flexibly than the Pi Camera)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.


## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

Play with contour detection:

<img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/contour_out.jpg?raw=true"  width="400"/>

Play with object detection:

<img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/detected_out.jpg?raw=true"  width="400"/>

Play with flow detection:

<img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/flow.png?raw=true"  width="400"/>

Play with face detection:

<img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/faces_detected.jpg?raw=true"  width="400"/>

Play with Teachable Machines:

<img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/Squirtle.png?raw=true"  width="200"/><img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/Squishmallow.png?raw=true"  width="200"/>
<img src="https://github.com/quinn997/Interactive-Lab-Hub/blob/Spring2021/Lab%205/Unrelated.png?raw=true"  width="200"/>



Befor you get started connect the RaspberryPi Camera V2. [The Pi hut has a great explanation on how to do that](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera).  

#### OpenCV
A more traditional to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python.

Additionally, we also included 4 standard OpenCV examples. These examples include contour(blob) detection, face detection with the ``Haarcascade``, flow detection(a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (I.e. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example.

```shell
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
#### Filtering, FFTs, and Time Series data. (beta, optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the set up from the [Lab 3 demo](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Spring2021/Lab%203/demo) and the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

Include links to your code here, and put the code for these in your repo--they will come in handy later.

#### Teachable Machines (beta, optional)
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple.  However, its simplicity is very useful for experimenting with the capabilities of this technology.

You can train a Model on your browser, experiment with its performance, and then port it to the Raspberry Pi to do even its task on the device.

Here is Adafruit's directions on using Raspberry Pi and the Pi camera with Teachable Machines:

1. [Setup](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/raspberry-pi-setup)
2. Install Tensorflow: Like [this](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4/tensorflow-lite-2-setup), but use this [pre-built binary](https://github.com/bitsy-ai/tensorflow-arm-bin/) [the file](https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl) for Tensorflow, it will speed things up a lot.
3. [Collect data and train models using the PiCam](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/training)
4. [Export and run trained models on the Pi](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/transferring-to-the-pi)

Alternative less steps option is [here](https://github.com/FAR-Lab/TensorflowonThePi).

#### PyTorch  
As a note, the global Python install contains also a PyTorch installation. That can be experimented with as well if you are so inclined.

### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interactions outputs and inputs.
**Describe and detail the interaction, as well as your experimentation.**

**Squishmallows shark or Squirtle**

Model: Teachable Machines object detection

When an object is placed in front of the camera, the camera will be able to tell if an object is a squishmallows shark or a squirtle. If it's neither, it should also notify the user that it's an unrelated object.

Experimentation
- When I place the squishmallows shark in front of the camera, it correctly detects the object and outputs "I think it's a Squishmallows".
- When I place the squirtle in front of the camera, it also correclt detects the object and outputs "I think it's a squirtle".
- When neither of the obejcts is placed in front of the camera, it outputs "I think it's unrelated"

video: https://drive.google.com/file/d/1rXATOsQJszdxEBG5gSVA5W0NyImLmW4y/view?usp=sharing


### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note your observations**:
For example:
1. When does it what it is supposed to do?

For the most of the time, the face lock does what it supposed to do. In particular, I noticed that it works well when the person keeps an appropriate distance from the camera (not too close & Not too far)

2. When does it fail?

Sometimes the face lock fails to detect the right person when the lighting is dark or when the angle is different.

3. When it fails, why does it fail?

When the light is too dark in the room, it makes the face lock harder to classify objects. When the angle is different, the model fails because some of these angles weren't used to train the model.

4. Based on the behavior you have seen, what other scenarios could cause problems?

I think the background color could also cause problems. Since I'm wearing a white shirt and a photo of another person I used to test the model also has a white background, sometimes face lock fails to identity the owner correctly.

**Think about someone using the system. Describe how you think this will work.**
1. Are they aware of the uncertainties in the system?

During their first try, they will probably not be aware of the uncertainties in the system. After experimenting a few more times, they will be able to work it out.

2. How bad would they be impacted by a miss classification?

If the owner of the computer got identified as the stranger, it wouldn't be too bad since he/she could simply give face lock another chance to detect his/her face. On the other hand, It will have a bad consequence if a stranege was identified as the owner because the stranger will have the access to owner's personal files. 

3. How could change your interactive system to address this?

I added a second identification method - password - to make sure that strangers will not be able to unlock the owner's computer even if he used the owener's face to unlock the face lock.

4. Are there optimizations you can try to do on your sense-making algorithm.

Increase the size of the dataset will help face lock to generate more accurate results.


### Part D
### Characterize your own Observant system

**Include a short video demonstrating the finished result.**

Final Video: https://drive.google.com/file/d/1pwWuGaStvRvc9e22MTiKnsn4rQcXC8Ak/view?usp=sharing

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use Face Lock for?

Face lock can be used to protect people's computers and privacy. For example, when a stranger is sitting in front of my computer, the face lock will alarm the stranger and speaker will play "You are not Quinn, go away!"

* What is a good environment for Face Lock?

Good lighting, simple background, the person shows the whole face and doesn't move.

* What is a bad environment for Face Lock?

poor lighting, too many objects detected, the person only shows part of the face and is constantly moving.

* When will Face Lock break?

Sometimes the face lock fails to detect the right person when the lighting is dark or when the angle is different.

* When it breaks how will Face Lock break?

It will incorrectly classify the stranger as the owner of the computer. If the person is constantly moving in front of the camera, it will also incorrectly classify the stranger as the owner of the computer.

* What are other properties/behaviors of Face Lock?

I added a second identification method - password - to make sure that strangers will not be able to unlock the owner's computer even if he used the owener's face to unlock the face lock.

* How does Face Lock feel?

Face lock is connected to the labtop webcam. It can be easily removed so that the user could set is up at different places like doors.

