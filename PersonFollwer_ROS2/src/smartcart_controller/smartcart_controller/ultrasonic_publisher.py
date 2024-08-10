from __future__ import print_function # Python 2/3 compatibility
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from std_msgs.msg import Int32MultiArray
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIGF = 5
ECHOF = 6

TRIGB = 16
ECHOB = 26

class UltrasonicPublisher(Node):
    def __init__(self):
        # Initiate the Node class's constructor and give it a name
        super().__init__('ultrasonic_publisher')
            
        # Create the publisher. This publisher will publish an Image
        # to the video_frames topic. The queue size is 10 messages.
        self.publisher_ = self.create_publisher(Int32MultiArray, 'distance', 10)
            
        # We will publish a message every 0.1 seconds
        timer_period = 0.1  # seconds
            
        # Create the timer
        self.timer = self.create_timer(timer_period, self.timer_callback)  
    
    def timer_callback(self):
        
        distance = Int32MultiArray()
        distance.data = [0, 0, 0, 0, 0]
        print("Distance Measurement in Progress")

        GPIO.setup(TRIGF,GPIO.OUT)
        GPIO.setup(ECHOF,GPIO.IN)
        GPIO.setup(TRIGB,GPIO.OUT)
        GPIO.setup(ECHOB,GPIO.IN)
        
        # print("Wating for sensor")
        time.sleep(2) # change to interal of time

        GPIO.output(TRIGF, True)
        GPIO.output(TRIGB, True)
        time.sleep(0.00001)
        GPIO.output(TRIGF, False)
        GPIO.output(TRIGB, False)
        '''
        # Front sensor
        while GPIO.input(ECHOF) ==0:
            pulse_startF = time.time()

        while GPIO.input(ECHOF) ==1:
            pulse_endF = time.time()
        # Back sensor
        while GPIO.input(ECHOB) ==0:
            pulse_startB = time.time()

        while GPIO.input(ECHOB) ==1:
            pulse_endB = time.time()
        
        pulse_durationF = pulse_endF - pulse_startF
        pulse_durationB = pulse_endB - pulse_startB
        
        #distanceF  in cm
        distanceF = pulse_durationF * 17150
        distanceF = round(distanceF, 2)
        #distanceB in cm
        distanceB = pulse_durationB * 17150
        distanceB = round(distanceB, 2)
        '''
        # print("Distance Front:",distanceF,"cm")
        # print(type(distanceF))
        # print("Distance Back:",distanceB,"cm")
        
        # real
        #distance.data[0] = distanceF
        #distance.data[1] = distanceB
#       test
        distance.data[3] = 1234
        distance.data[4] = 8
        
        self.publisher_.publish(distance)
    
        # Display the message on the console
        self.get_logger().info("%s" % distance.data)

def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the node
    ultrasonic_publisher = UltrasonicPublisher()

    # Spin the node so the callback function is called.
    rclpy.spin(ultrasonic_publisher)
    
    GPIO.cleanup()

    ultrasonic_publisher.destroy_node()
    
    # Shutdown the ROS client library for Python
    rclpy.shutdown()
   
if __name__ == '__main__':
  main()