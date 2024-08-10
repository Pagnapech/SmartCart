# Basic ROS 2 program to publish real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
   
# Import the necessary libraries
from __future__ import print_function # Python 2/3 compatibility
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import smartcart_controller.videostream as vs
import cv2 # OpenCV library
import numpy as np # Import Numpy library
# Import Packages
import cv2

# external written files
# import videostream as vs
import smartcart_controller.interpreter as interpreter
# import interpreter 
import smartcart_controller.framerate as framerate
# import framerate
import smartcart_controller.utilities as utilities 
# import utilities
from smartcart_controller.tracker import *

# Global Constant
inputMean = 127.5
inputStd = 127.5

# Font
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.8

# Resolution is imW x imH = 320 x 320 

# Draw line
imW = 320
imH = 320
LINE1_xS = (imW // 2) - (imW // 10) # line 1 x start coordination
# LINE1_y = 350 # line 1 y coordination
LINE1_y = 1 # line 1 y coordination
LINE1_xE = (imW // 2) + (imW // 10) # line 1 x end coordination
# LINE2_y = 400 # line 2 y coordination
LINE2_y = imH # line 2 y coordination
OFFSET = 10 #base on Line offset calculation (Google Sheet) 


# Color
YELLOW = (0,255,255)
RED = (0,0,255)
GREEN = (0,255, 0)
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

# Initialize distance 
msg = Int32MultiArray()
msgtest = Int32MultiArray()
cxtemp = int()
msg.data = [0, 0, 0, 0, 0]
msgtest.data = [0, 0, 0, 0, 0]
class ImagePublisher(Node):
  """
  Create an ImagePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('tensor_image_publisher')
    
    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
    self.publisher_coordinates = self.create_publisher(Int32MultiArray, 'position', 10)
    
    # We will publish a message every 0.1 seconds
    timer_period = 0.1  # seconds
       
    # Create the timer
    self.timer = self.create_timer(timer_period, self.timer_callback)
    '''
    self.subscription = self.create_subscription(
      Int32MultiArray, 
      'distance', 
      self.timer_callback, 
      10)
    self.subscription # prevent unused variable warning    
    '''
    # Create a VideoCapture object
    # The argument '0' gets the default webcam.
    # self.cap = cv2.VideoCapture(0)
    
    # Used to convert between ROS and OpenCV images
    self.br = CvBridge()
    
    self.cli = self.create_client(Int32MultiArray, 'distance')
    while not self.cli.wait_for_service(timeout_sec=1.0):
        self.get_logger().info('service not available, waiting again...')
    self.req = Int32MultiArray.Request()
  def send_request(self):
    self.future = self.cli.call_async(self.req)
    rclpy.spin_until_future_complete(self, self.future)
    return self.future.result()
    
    ''' 
  def listener_callback(self, distance):
    self.msg = distance
    self.get_logger().info('Publishing msg.data: ' "%s" % msg.data)
    '''
    
  def timer_callback(self):
    """
    Callback function.
    This function gets called every 0.1 seconds.
    """
    ### tensor
    
    # set object Tracker
    tracker = Tracker() 
    
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
    # time.sleep(1) # delay for 1 sec
    itemName = ''
    
    
    ###
    
    
    while (True):
        # Capture frame-by-frame
        # This method returns True/False as well
        # as the video frame.
        
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
#            centriod text
#            cv2.putText(frame, str(id), (cx, cy), FONT, FONT_SCALE, RED, TEXT_THICKNESS)
#            bounding box thresholds text
#            cv2.putText(frame, str((x3, x4)), (cx, cy), FONT, FONT_SCALE, RED, TEXT_THICKNESS)

            # self.get_logger().info("id_count is {}".format(tracker.dist))
            # self.get_logger().info("id_count is {}".format(tracker.id_count))
            # self.get_logger().info("Object list is {}".format(itemList))

            # detects if object is outside thershold
            #if (LINE1_xS > cx) or (LINE1_xE < cx):
                # id number
                # cv2.putText(frame, str(id), (cx, cy), FONT, FONT_SCALE, RED, TEXT_THICKNESS)
                
                # cv2.putText(frame, "outside", (cx, cy), FONT, FONT_SCALE, RED, TEXT_THICKNESS)

            # Appends id to objectList
                    
            #msg.data for pixal position
            position = (imW - 160)
            # cx is center of Object, x3 bbox left, x4 bbox right
            msg.data[0] = cx
            msg.data[1] = x3
            msg.data[2] = x4
            msgtest.data[0] = cx
            msgtest.data[1] = x3
            msgtest.data[2] = x4
            
            # Finds if Object is first in objectList
            # If Object goes out of view saves previous pixal for Left or Right 
            #if str(id) in objectList[0]:
            if msgtest.data[0] != 0:
                msg.data[0]= cx - position
                cxtemp = cx - position
            else:
                msg.data[0] = cxtemp
                
            # Detects if Object position in the center
            if (LINE1_xS < cx) and (LINE1_xE > cx):
                # Create a dictionary to save the ID and its downward position
                # id number
                # cv2.putText(frame, str(id), (cx, cy), FONT, FONT_SCALE, GREEN, TEXT_THICKNESS)
                # inside
                # cv2.putText(frame, "inside", (cx, cy), FONT, FONT_SCALE, GREEN, TEXT_THICKNESS)
                
                #if str(id) == objectList[0]:
                msg.data[0] = 0
                cxtemp = 0
                # bbox inside cyan lines
                if (x3 > 85 - 5) and (x4 < 235 + 5):
                    print("INSIDE FOCUS THRESHOLD TURN ON ULTRASONIC")
                    msg.data[1] = int(x3)
                    msg.data[2] = int(x4)
                else: 
                    # too close to camera
                    msg.data[1] = -1
                    msg.data[2] = -1
            
            # Object posititon not in center    
            else:
                # if str(id) == objectList[0]:
                msg.data[0] = cxtemp
                msg.data[1] = 0
                msg.data[2] = 0
                #negative left and positive right
            # bbox inside yellow lines
            '''
            if (LINE1_xS < x3) and (LINE1_xE > x4):
                print("IN THRESHOLD MOVING FORWARD")
                msg.data[1] = int(x3)
                msg.data[2] = int(x4)
            '''
            
                
        # Write framerate in the corner of frame
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frameRateCal), (30, 50), FONT, 1, CYAN, 2, cv2.LINE_AA) 
        
        # Draw Cyan Line 1
        utilities.drawLine(frame, 85, LINE1_y, 85, LINE2_y, CYAN, LINE_THICKNESS)
        # Draw Cyan Line 2
        utilities.drawLine(frame, 235, LINE1_y, 235, LINE2_y, CYAN, LINE_THICKNESS)

        # Draw Yellow Line 1
        utilities.drawLine(frame, LINE1_xS, LINE1_y, LINE1_xS, LINE2_y, YELLOW, LINE_THICKNESS)
        # Draw Yellow Line 2 
        utilities.drawLine(frame, LINE1_xE, LINE1_y, LINE1_xE, LINE2_y, YELLOW, LINE_THICKNESS)
        
        # Show the webcam
        cv2.imshow('WebCam', frame)
        self.publisher_.publish(self.br.cv2_to_imgmsg(frame))
        self.publisher_coordinates.publish(msg)
        # Display the message on the console
        # meow
        self.get_logger().info('Publishing video frame')
        self.get_logger().info('Publishing msg.data: ' "%s" % msg.data)
        
        # Calculate the framerate
        t2 = cv2.getTickCount()
        frameRateCal = framerate.calculateFrameRate(t1, t2, frequency)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rclpy.shutdown()
            break
        

    # Clean up
    cv2.destroyAllWindows()
    videoStream.stop()

   
def main(args=None):
   
  # Initialize the rclpy library
  rclpy.init(args=args)
   
  # Create the node
  image_publisher = ImagePublisher()

  # Spin the node so the callback function is called.
  rclpy.spin(image_publisher)
   
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_publisher.destroy_node()
   
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()
