# Display Bounding Box and Label

import cv2
import time

# MARCO DEFINE
# Color
RED = (0, 0, 255)
NEON = (10, 255, 0)
YELLOW = (0,255,255)

# Radius
radius = 4

# Thickness
CIRCLE_THICKNESS = -1
TEXT_THICKNESS = 2

# Font
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8 

# Item List
myItems = ['apple', 'banana', 'bottle', 'cup', 'orange']

def mousePosition(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        position = [x,y]
        print(position)


def drawBoxAndLabel(frame, labels, imW, imH, boxes, classes, scores, i):
    
    # Specific object
    anItem = ''
    # Draw Label
    objectName = labels[int(classes[i])] # Look up object name from "labels" array using class index
    
    ymin = 0
    xmin = 0 
    xmax = 0
    ymax = 0
    # make specification item here 
    if objectName in myItems:
        
#         print(objectName) 
        
    # Get bounding box coordinates and draw box
    # Interpreter can return coordinates that are outside of image dimensions, need to force them
    # to be within image using max() and min()
        ymin = int(max(1, (boxes[i][0] * imH))) # topLeft y-axis
        xmin = int(max(1, (boxes[i][1] * imW))) # topLeft x-axis
        ymax = int(min(imH, (boxes[i][2] * imH))) # bottomRight y-axis
        xmax = int(min(imW, (boxes[i][3] * imW))) # bottomRight x-axis
        
        label = '%s: %d%%' % (objectName, int(scores[i]*100)) # Example: 'person: 72%'
        labelSize, baseLine = cv2.getTextSize(label, FONT, 0.7, 2) # Get font size
        label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of the window
        
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), NEON, 2)
        
        # Create center point
        center_x, center_y = createCenterPoint(xmin,ymin, xmax,ymax)
        # Draw center point
        cv2.circle(frame, (center_x, center_y), radius, RED, CIRCLE_THICKNESS)
        
        # Draw white box to put label text in 
        cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10), (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (xmin, label_ymin - 7), FONT, 0.7, (0,0,0), 2) # Draw label text
         
        anItem = anItem + objectName

    return (xmin,ymin,xmax,ymax), anItem
    
def createCenterPoint(x1,y1,x2,y2):
    center_x = int(x1+x2) // 2 #center point of x-axis
    center_y = int(y1+y2) // 2 #center point of y-axis
    
    return center_x, center_y

def drawLine(frame, start_x, start_y, end_x, end_y, color, thickness):
    cv2.line(frame, (start_x, start_y), (end_x, end_y), color, thickness)
    
