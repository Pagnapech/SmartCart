# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - Addison Sears-Collins
# - https://automaticaddison.com
   
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from std_msgs.msg import Int32MultiArray # Image is the message type
  
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
       
    
  def listener_callback(self, msg):
    """
    Callback function.
    """
    # Display the message on the console
    self.get_logger().info('Receiving position: "%s"' % msg.data)
  
    ### 
    # do stuff
    ###
    
def main(args=None):
   
  # Initialize the rclpy library
  rclpy.init(args=args)
   
  # Create the node
  motor_subscriber = MotorSubscriber()
   
  # Spin the node so the callback function is called.
  rclpy.spin(motor_subscriber)
   
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  motor_subscriber.destroy_node()
   
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
   
if __name__ == '__main__':
  main()