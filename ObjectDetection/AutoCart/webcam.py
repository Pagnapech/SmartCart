###### Main File -- Webcam

##### Webcam Object Detection Using TensorFlow-trained Classifer #####
##### Reference Link: https://www.youtube.com/watch?v=aimSGOAUI8Y&pp=ygU_aG93IHRvIHJ1biB0ZW5zb3JmbG93IGxpdGUgb24gcmFzcGJlcnJ5IHBpIGZvciBvYmplY3QgZGV0ZWN0aW9u
##### Reference Github: https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/deploy_guides/Raspberry_Pi_Guide.md

# Senior Design EECS 159A/B Fall 2023 UC Irvine

# This program uses TensorFlow Lite model to perform object detection on a live webcam
# It draws boxes and scores around around the objects of interest in each frame from the webcam
# It counts an item putting in/ taking out when moving across the line threshold
# To improve the FPS, the webcam object runs in a separate thread from the main program
# This script will work with regular USB webcam (not sure about PiCamera)

# Method of draw boxes, labels, and lines implemented using OpenCV


# from backend.objectdetection import *
import sys
sys.path.append("../")
from django.db import connection
# from backend.admin import *
# sys.path.append("../")
# from backend.models import GUITable


# import requests 
# SERVER_URL = 'http://127.0.0.1:8000/objectdetection/'

# Import Packages
import cv2
import numpy as np
import json 
import time


# external written files
import videostream as vs
import interpreter 
import framerate
import utilities
from tracker import *
import audio

# backend file
# sys.path.append('~/Desktop/SmartCartApp/AutoCart/backend')





# Global Constant
inputMean = 127.5
inputStd = 127.5

# Font
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8

# LINE POSITION
# LINE1_xS = 25 # line 1 x start coordination
# LINE1_y = 350 # line 1 y coordination
# LINE1_xE = 1200 # line 1 x end coordination
# LINE2_y = 400 # line 2 y coordination
# OFFSET = 10 #base on Line offset calculation (Google Sheet) 

LINE1_xS = 1 # line 1 x start coordination
# LINE1_y = 350 # line 1 y coordination
LINE1_y = 190 # line 1 y coordination
LINE1_xE = 320 # line 1 x end coordination
# LINE2_y = 400 # line 2 y coordination
LINE2_y = 240 # line 2 y coordination
OFFSET = 10 #base on Line offset calculation (Google Sheet) 

# Resolution is imW x imH = 320 x 320 


# Color
YELLOW = (0,255,255)
RED = (0,0,255)
CYAN = (255,255,0)

# Thickness
LINE_THICKNESS = 2
CIRCLE_THICKNESS = -1
TEXT_THICKNESS = 2

# IN/OUT Text Position
IN_X = 1000
IN_Y = 100

# Dictionary ObjectInBasket is used to save the Object in the basket
ObjectIn = {}
counterIn = []

# Dictionary ObjectTakeOut is used to save the Object out of the basket
ObjectOut = {}
counterOut = []

# Cart Item
myCartItem = {}

# Item Name
myCurrentItem = ''


def webcam():

    # set object Tracker
    tracker = Tracker() 
    
    # Dictionary ObjectInBasket is used to save the Object in the basket
    ObjectIn = {}
    counterIn = []
    # Set up Interpreter 
    interpret = interpreter.setupInterpreter()
    
    interPreter = interpret[0] 
    imW = interpret[1]
    imH = interpret[2]
    min_conf_threshold = interpret[3]
    labels = interpret[4] 
    
    interPreter.allocate_tensors()
    
    # Create a window name (REQUIRED)
    cv2.namedWindow('WebCam')
    # Print mouse position 
    cv2.setMouseCallback('WebCam', utilities.mousePosition)
    
    # Get model details
    inputDetails = interPreter.get_input_details()
    outputDetails = interPreter.get_output_details()
    height = inputDetails[0]['shape'][1]
    width = inputDetails[0]['shape'][2]
     
    floatingModel = (inputDetails[0]['dtype'] == np.float32)
    
    # Check output layer name to determine if this model was created with TF2 or TF1
    # output order is different for TF1 and TF2
    outname = outputDetails[0]['name']
    
    if('StatefulPartitionedCall' in outname): # TF2 model
        boxes_idx, classes_idx, scores_idx = 1,3,0
    else: # TF1 model
        boxes_idx, classes_idx, scores_idx = 0,1,2
    

    # Initialize frame rate calculation
    frameRateCal = 1
    frequency = framerate.init_FrameRate()
    
    # Initialize video stream
    imW = 320
    imH = 320
    videoStream = vs.VideoStream(resolution=(imW, imH), framerate=30).start()
    time.sleep(1) # delay for 1 sec
    itemDetected = ''
    itemName = ''
    while (True):
        
        # clear the dictionary
        myCartItem = {}
        
        # Start timer (Calculate frame rate)
        t1 = cv2.getTickCount()
        
        # Grab frame from video stream
        frame1 = videoStream.read()
        
        # Acquire frame and resize to expected shape [1xHxWx3]
        frame = frame1.copy() # copy and put into the new frame
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameResized = cv2.resize(frameRGB, (width, height))
        inputData = np.expand_dims(frameResized, axis=0)
        
        # Normalize pixel values if using a floating model (ex: if model is non-quantized)
        if floatingModel :
            inputData = (np.float32(inputData) - inputMean) / inputStd
        
        # Perform the actual detection by running the model with the image as input
        interPreter.set_tensor(inputDetails[0]['index'],inputData)
        interPreter.invoke()
        
        # Retrieve detection result
        boxes = interPreter.get_tensor(outputDetails[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = interPreter.get_tensor(outputDetails[classes_idx]['index'])[0] # Class index of detected objects
        scores = interPreter.get_tensor(outputDetails[scores_idx]['index'])[0] # Confidence of detected objects
        
        # Keep track of items in LIST
        itemList = []
        
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw box
                coord, itemName  = utilities.drawBoxAndLabel(frame, labels, imW, imH, boxes, classes, scores, i)
                # Add Specific Class condition here: if 'orange', 'apple' then append the item coord in the list 
                itemList.append(coord)
#                 if (i == len(scores) -1):
                if itemName != '':
                    myCurrentItem = itemName
#                 print(f'Coordinate: ' + str(coord))
                

        #1. Keep track of the item in frame
        bbox_id = tracker.update(itemList)
            
#         if (len(itemDetected) != 0):
#             print(f'for debugging: ' + itemDetected[0])
        #2. Call Tracker class to assign the ID
        for bbox in bbox_id:
#             print(f'In BBOX: ' + itemDetected[0])
            #3. Add if-condition
#             print(f'itemName: ' + itemName)
            x3, y3, x4, y4, id = bbox
            cx, cy = utilities.createCenterPoint(x3,y3,x4,y4) #center of the box x and y coordinate

            # GO DOWN
            # Object pass the line and object is about to cross the line (LINE 1) 
            if (LINE1_y < (cy + OFFSET)) and (LINE1_y > (cy - OFFSET)):
                # Create a dictionary to save the ID and its downward position
                ObjectIn[id] = cy
                
            # Check only the existing id in the ObjectIn dictionary
            if id in ObjectIn:
                # object pass the line and object is about to cross the line (LINE 2)
                if (LINE2_y < (cy + OFFSET)) and (LINE2_y > (cy - OFFSET)):
                    # Once the item touches the line, it will print out the ID
                    cv2.circle(frame, (cx, cy), 4, RED, CIRCLE_THICKNESS)
                    cv2.putText(frame, str(id), (cx, cy), FONT, FONT_SCALE, YELLOW, TEXT_THICKNESS) # put ID text on the object
                    # this condition is to avoid repetitive counting
                    
                    if counterIn.count(id) == 0:
                        counterIn.append(id)
                        # Send to the BackEnd to Evaluate
#                         print(f'ItemName from OI: ' + itemDetected) 
                        time.sleep(0.1) 
                        myCartItem[myCurrentItem] = 1
                        print(f'myCurrentItem: ' + myCurrentItem)
                        print(myCartItem)
                        # setItemDetected(myCurrentItem)
                        sendData(myCurrentItem, 1)
                        myCurrentItem = ''
                        # audio.itemInCart()
                            
                       
            # GO UP
            # Object pass the line and object is about to cross the line (LINE 2)
            if (LINE2_y < (cy + OFFSET)) and (LINE2_y > (cy - OFFSET)):
                # Create a dictionary to save the ID and its upward position
                ObjectOut[id] = cy
            
            # check only the existing id in the ObjectOut dictionary
            if id in ObjectOut:
                # object pass the line and object is about to cross the line (LINE 1)
                if (LINE1_y < (cy  + OFFSET)) and (LINE1_y > (cy - OFFSET)):
                    cv2.circle(frame, (cx,cy), 4, RED, CIRCLE_THICKNESS)
                    cv2.putText(frame, str(id), (cx, cy), FONT, FONT_SCALE, YELLOW, TEXT_THICKNESS)
                    # this condition is to avoid repetitive counting
    #                     print(f'Inside if ObjectOut: ' + itemDetected[0])
                    if counterOut.count(id) == 0:
                        # append the id
                        counterOut.append(id)
                        # Send to the BackEnd to Evaluate
#                         print(f'ItemName from OO: ' + itemDetected)
                        time.sleep(0.1)
                        myCartItem[myCurrentItem] = -1
                        
                        print(f'myCurrentItem: ' + myCurrentItem)
                        print(myCartItem)
                        sendData(myCurrentItem, -1)
                        myCurrentItem = ''
                        # audio.itemOutCart()
                           
            
        # Write framerate in the corner of frame
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frameRateCal), (30, 50), FONT, 1, CYAN, 2, cv2.LINE_AA) 
        
        
        # Draw Line 1
        utilities.drawLine(frame, LINE1_xS, LINE1_y, LINE1_xE, LINE1_y, YELLOW, LINE_THICKNESS)
        # Draw Line 2 
        utilities.drawLine(frame, LINE1_xS, LINE2_y, LINE1_xE, LINE2_y, YELLOW, LINE_THICKNESS)
        
        # Number of Object in the Basket
        NumIn = len(counterIn)
        # Number of Object out the Basket
        NumOut = len(counterOut)
        
        # Write Number of items in and out
        cv2.putText(frame, "In: " + str(NumIn), (IN_X, IN_Y), FONT, FONT_SCALE, YELLOW, TEXT_THICKNESS)
        cv2.putText(frame, "Out: " + str(NumOut), (IN_X, IN_Y + 50), FONT, FONT_SCALE, YELLOW, TEXT_THICKNESS)
        
        
        # Show the webcam
        cv2.imshow('WebCam', frame) 
        
        # Calculate the framerate
        t2 = cv2.getTickCount()
        frameRateCal = framerate.calculateFrameRate(t1, t2, frequency)
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break 

    # Clean up
    cv2.destroyAllWindows()
    videoStream.stop()


def sendData(productName, indicates):

    # read and write     
    filename = "itemDetected.txt"

    # try open the existing file
    try: 
        # read if the file is empty, then proceed with write 
        file = open("../connectOD_Backend/{}".format(filename), "r+") # r+ is both for reading and writing 
        emptyString = file.read() 
        

        if(emptyString == ""):
            # dict = {productName: indicates} 
            # json_obj = json.dumps(dict, indent=1) 
            # file.write(json_obj) 
            list = "{}:{}".format(productName, indicates)
            file.write(list) 
            print("Successfully added to the file.\n") 
        else: 
            print("Try again. There is a string. \n") 
    
        file.close() 
        

    except:
        print("Cannot open {} file".format(filename)) 



# Call function for execution  
webcam()
        
    
    
    


