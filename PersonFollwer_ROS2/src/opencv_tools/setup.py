from setuptools import find_packages, setup

package_name = 'opencv_tools'

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
            'img_publisher = opencv_tools.basic_image_publisher:main',
            'tensor_img_publisher = opencv_tools.tensor_image_publisher:main',
            'img_subscriber = opencv_tools.basic_image_subscriber:main',
        ],
    },
)
