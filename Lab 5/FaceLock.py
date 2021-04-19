
#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
from gtts import gTTS
import os


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

def say(message):
    audio_filename = "temp.mp3"
    google_tts = gTTS(message, lang = 'en')
    google_tts.save(audio_filename)
    os.system("/usr/bin/mplayer " + audio_filename)

img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      img = cv2.imread("../data/test.jpg")
      print("Using default image.")


# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')
# Load Labels:
labels=[]
f = open("labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())


while(True):
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open('/home/pi/openCV-examples/data/test.jpg')
    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    label = labels[np.argmax(prediction)]
    if label == "NotQuinn":
        print("You are not Quinn! Go away!")
        say("You are not Quinn! Go away!")
    elif label == "Quinn":
        print("Welcome Back!", label)
        say("Welcome back, Quinn")
        break
    else:
        print("Locked")


    if webCam:
        if sys.argv[-1] == "noWindow":
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

while 1:
    say("Please enter your password")
    password = input("Please enter your password: ")
    if password == '971218':
        print("Correct! Welcome!")
        say("Correct! Welcome!")
        break
    else:
        print("Wrong password! Please try again!")
        say("Wrong password! Please try again!")

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
