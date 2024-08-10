# Import Packages
import cv2
from threading import Thread

# VideoStream class handles the streaming of video from webcam in separate processing thread
class VideoStream:
    # Initialize the camera image stream
    def __init__(self, resolution=(640,480), framerate=30):
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])
        
        # Read first frame from the stream
        (self.get, self.frame) = self.stream.read()
        
        # Variable to control when the camera is stopped
        self.stopped = False
    
    # Start the thread that reads frames from the video stream
    def start(self):
        Thread(target=self.update,args=()).start()
        return self
    
    # Keep looping indefinitely until the thread is stopped
    def update(self):
        while (True):
            # if the camera stopped, then stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return
            
            # Otherwise, grab the next frame from the stream
            (self.get, self.frame) = self.stream.read()
    
    # Return the most recent frame
    def read(self):
        return self.frame
    
    # Indicate that the camera and thread should be stopped
    def stop(self):
        self.stopped = True 
        