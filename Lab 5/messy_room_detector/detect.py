# How to load a Tensorflow model using OpenCV
# Jean Vitor de Paulo Blog - https://jeanvitor.com/tensorflow-object-detecion-opencv/
# David edited some stuff

import numpy as np
import cv2
import subprocess
import sys
import qwiic_button 

### Initialize Buttons

red_button = qwiic_button.QwiicButton()
green_button = qwiic_button.QwiicButton(0x6E)

if red_button.begin() == False:
    print("The Red Qwiic Button isn't connected to the system. Please check your connection")

if green_button.begin() == False:
    print("The Green Qwiic Button isn't connected to the system. Please check your connection")

red_button.LED_config(250, 1000, 200)
green_button.LED_on(100)

### Initialize camera & tensorflow

# Load a model imported from Tensorflow
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

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




def speak(instruction):
    command = """
        say() { 
            local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; 
        } ; 
    """ + f"say '{instruction}'"
    subprocess.call(command, shell=True)

previous_count = 0
alarm_triggered = False

MESSY_THRESHOLD = 8
CLEAN_THRESHOLD = 4

while(True):
   if webCam:
      ret, img = cap.read()

   rows, cols, channels = img.shape

   # Use the given image as input, which needs to be blob(s).
   tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

   # Runs a forward pass to compute the net output
   networkOutput = tensorflowNet.forward()

   object_count = 0

   # Loop on the outputs
   for detection in networkOutput[0,0]:
      score = float(detection[2])
      if score > 0.18:
         object_count += 1
         left = detection[3] * cols
         top = detection[4] * rows
         right = detection[5] * cols
         bottom = detection[6] * rows

         #draw a red rectangle around detected objects
         cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), thickness=2)
   
   if object_count != previous_count:
      previous_count = object_count
      print("Object count: " + str(object_count))

   if object_count > MESSY_THRESHOLD and not alarm_triggered:
      speak("Clean the table please! It’s too messy!")
      alarm_triggered = True
      print("WARNING: You should clean your table!")
   if object_count <= CLEAN_THRESHOLD and alarm_triggered:
      speak("Good job! Your table is clean again.")
      alarm_triggered = False

   if webCam:
      if sys.argv[-1] == "noWindow":
         print("Finished a frame")
         cv2.imwrite('detected_out.jpg',img)
         continue
      cv2.imshow('detected (press q to quit)',img)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         cap.release()
         break
   else:
      break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()


