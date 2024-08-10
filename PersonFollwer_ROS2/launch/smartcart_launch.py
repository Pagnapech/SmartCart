from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
   return LaunchDescription([
        Node(
            package='smartcart_controller',
            #namespace='tensor_image_publisher',
            executable='tensor_img_publisher',
            #name='publisher',
            arguments=["--modeldir=Sample_TFLite_model"]
        ),
        Node(
            package='smartcart_controller',
            #namespace='motor_subscriber',
            executable='motor_subscriber',
            #name='subscriber'
           
        ),
   ])