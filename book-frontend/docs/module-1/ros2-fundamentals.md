# ROS 2 Fundamentals

This module introduces the core concepts of ROS 2 (Robot Operating System 2), a flexible framework for writing robot software. You will learn about nodes, topics, URDF, and the `rclpy` bridge for Python.

## 1. ROS 2 Nodes

ROS 2 applications are composed of independent functional units called **nodes**. Each node is responsible for a single, modular purpose (e.g., a camera driver, a motor controller, a laser scan matcher).

### 1.1 Creating a Simple ROS 2 Node

To create a basic ROS 2 node, you typically use a client library like `rclpy` (for Python) or `rclcpp` (for C++). Here's a simple Python example that creates a node and prints a message.

```python
# File: my_package/my_package/minimal_publisher.py

import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

This node, named `minimal_publisher`, publishes a "Hello World" message to a topic every 0.5 seconds.


## 2. ROS 2 Topics

**Topics** are the main communication mechanism in ROS 2. Nodes publish messages to topics, and other nodes subscribe to those topics to receive the messages. This allows for a decoupled architecture where nodes don't need to know about each other's existence, only about the topics they communicate through.

### 2.1 Understanding Publish-Subscribe

Consider a robot with a camera. The camera driver node might publish image messages to an `/camera/image` topic. A separate image processing node can then subscribe to this topic to receive and process the images, without directly interacting with the camera driver itself.

### 2.2 Simple ROS 2 Subscriber Example

Here's a Python example for a subscriber node that receives messages from the `topic` that our `minimal_publisher` node publishes to.

```python
# File: my_package/my_package/minimal_subscriber.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

To run these examples, you would typically compile your ROS 2 package and then run the nodes using `ros2 run <package_name> <node_executable>`.

## 3. Unified Robot Description Format (URDF)

**URDF** (Unified Robot Description Format) is an XML format for describing robots. It defines the robot's kinematic and dynamic properties, visual appearance, and collision models. URDF files are essential for simulating robots in environments like Gazebo and for visualizing them in tools like RViz.

### 3.1 Basic URDF Structure

A URDF file consists of `<link>` and `<joint>` elements. A `<link>` represents a rigid body part of the robot (e.g., a wheel, a torso), and a `<joint>` describes the kinematic and dynamic properties of the connection between two links.

```xml
<?xml version="1.0"?>
<robot name="my_simple_robot">

  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.6 0.4 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
  </link>

  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="base_to_left_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0.2 0.2 0" rpy="1.57079632679 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

</robot>
```

This simple URDF defines a `base_link` and a `left_wheel` connected by a continuous joint. The visual elements provide a basic appearance.

## 4. `rclpy` Bridge for Python

`rclpy` is the Python client library for ROS 2. It provides a Pythonic interface to all the core ROS 2 functionalities, allowing developers to write nodes, publishers, subscribers, services, and actions using Python.

### 4.1 Key `rclpy` Features

-   **Node creation**: `rclpy.create_node()`
-   **Publishers and Subscribers**: `create_publisher()`, `create_subscription()`
-   **Timers**: `create_timer()` for periodic callbacks
-   **Parameters**: Accessing node parameters
-   **Executors**: Running multiple nodes in a single process

### 4.2 Using `rclpy` in a Package

To make your Python ROS 2 nodes executable, you need to set up your `setup.py` and `package.xml` files correctly within your ROS 2 package. The `entry_points` in `setup.py` are crucial for making your scripts runnable via `ros2 run`.

```python
# File: my_package/setup.py

from setuptools import find_packages, setup

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/my_launch_file.launch.py']), # Example launch file
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='A minimal ROS 2 Python package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'minimal_publisher = my_package.minimal_publisher:main',
            'minimal_subscriber = my_package.minimal_subscriber:main',
        ],
    },
)
```

This `setup.py` defines two console scripts, `minimal_publisher` and `minimal_subscriber`, which can be run using `ros2 run my_package minimal_publisher` and `ros2 run my_package minimal_subscriber` respectively.

