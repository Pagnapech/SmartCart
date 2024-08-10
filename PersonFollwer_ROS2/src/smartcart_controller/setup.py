from setuptools import find_packages, setup

package_name = 'smartcart_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Randy Chhan',
    maintainer_email='Randychhan@gmail.com',
    description='Tensor_flow_image_publisher and subscriber',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "test_node = smartcart_controller.my_first_node:main",
            'tensor_img_publisher = smartcart_controller.tensor_image_publisher:main',
            'ultrasonic_publisher = smartcart_controller.ultrasonic_publisher:main',
            'img_subscriber = smartcart_controller.basic_image_subscriber:main',
            'motor_subscriber = smartcart_controller.motor_subscriber:main',
            'service = smartcart_controller.ultrasonic_service:main',
        ],
    },
)
