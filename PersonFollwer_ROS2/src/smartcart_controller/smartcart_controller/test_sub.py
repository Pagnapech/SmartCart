# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
   
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from std_msgs.msg import Int32MultiArray # Inte32MultiArray is the message type
from std_msgs.msg import Float32MultiArray # Int32 is the message type
import RPi.GPIO as GPIO

# Constants
MAXPWM = 25 

# Define the motor control pins
# A-right B-left
pinPWMR = 12
pinRF = 22
pinRB = 23

pinPWML = 13
pinLF = 24
pinLB = 25

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinPWMR, GPIO.OUT)
GPIO.setup(pinRF, GPIO.OUT)
GPIO.setup(pinRB, GPIO.OUT)

GPIO.setup(pinPWML, GPIO.OUT)
GPIO.setup(pinLF, GPIO.OUT)
GPIO.setup(pinLB, GPIO.OUT)

pwmR = GPIO.PWM(pinPWMR, 10000)
pwmL = GPIO.PWM(pinPWML, 10000)

# Function to drive right motors 
def drive_motorR(direction):
    GPIO.output(pinRF, direction)
    GPIO.output(pinRB, not direction)
    pwmR.ChangeDutyCycle(25)
    print("")

# Function to drive Left motors
def drive_motorL(direction):
    GPIO.output(pinLF, direction)
    GPIO.output(pinLB, not direction)
    
class MotorSubscriber(Node):
  """
  Create an MotorSubscriber class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('motor_subscriber')
       
    # Create the subscriber. This subscriber will receive an Int32MultiArray
    # from the position topic. The queue size is 10 messages.
    self.subscription = self.create_subscription(
      Int32MultiArray, 
      'position', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
    
    self.subscription = self.create_subscription(
      Float32MultiArray, 
      'distance', 
      self.listener_callback, 
      10)
    self.subscription # prevent unused variable warning
    
    
    pwmR.start(0)
    pwmL.start(0)
    print("PWM initialized")
  # def listener_callback(self, msg, distance):
  def listener_callback(self, msg):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving position: "%s"' % msg.data)
    
    ### 
    # if msg data recieved 
    # A left B right
    # A
    if msg.data[0] > 0:
      drive_motorR(0)
      # drive_motorL(1)
      self.get_logger().info('Turning Right')
    # B
    elif msg.data[0] < 0:
      # drive_motorL(0)
      # drive_motorR(1)
      self.get_logger().info('Turning Left')
    # stop motor
    else:
      if msg.data[1] and msg.data[2] != -1:
        # drive_motorL(1)
        # drive_motorR(1)
        self.get_logger().info('Move Forward')
      else:
        GPIO.output(pinRF, 0)
        GPIO.output(pinRB, 0)
        GPIO.output(pinLF, 0)
        GPIO.output(pinLB, 0)
        pwmR.ChangeDutyCycle(0)
        pwmL.ChangeDutyCycle(0)
        self.get_logger().info('Motor Stopped')
    
    ###
    
def main(args=None):
   
  # Initialize the rclpy library
  rclpy.init(args=args)
   
  # Create the node
  motor_subscriber = MotorSubscriber()
   
  # Spin the node so the callback function is called.
  rclpy.spin(motor_subscriber)
  
  
   # Stop both motors
  GPIO.output(pinPWMR, GPIO.LOW)
  GPIO.output(pinPWML, GPIO.LOW)

  # Clean up GPIO
  GPIO.cleanup()
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  motor_subscriber.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
   
if __name__ == '__main__':
  main()