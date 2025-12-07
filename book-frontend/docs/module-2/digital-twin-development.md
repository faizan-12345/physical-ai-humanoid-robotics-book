# Digital Twin Development

This module focuses on creating a simulated environment, or "digital twin," for your robot. You'll learn how to integrate physical properties using Gazebo, enhance visualization with Unity, and simulate various sensors.

## 1. Gazebo Physics Simulation

**Gazebo** is a powerful 3D robot simulator that accurately and efficiently simulates robots in complex indoor and outdoor environments. It provides robust physics engines, high-quality graphics, and convenient programmatic interfaces.

### 1.1 Setting up a Basic Gazebo World

To simulate a robot, you first need a "world" file that defines the environment, including lighting, ground plane, and any static objects. Gazebo uses SDF (Simulation Description Format) for world and model descriptions.

```xml
<!-- File: my_robot_world/worlds/empty.world -->
<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>
  </world>
</sdf>
```

To launch this world, you would typically use `gazebo --verbose my_robot_world/worlds/empty.world`.

### 1.2 Integrating Robot Models with Physics

When you import a URDF robot model into Gazebo, it automatically interprets the `<link>` and `<joint>` elements to apply physics. You can add Gazebo-specific extensions to your URDF to define custom physics properties, sensors, and actuators.

```xml
<!-- Example: Adding Gazebo physics to a URDF link -->
<link name="base_link">
  <collision>
    <geometry>
      <box size="0.6 0.4 0.2"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="10"/>
    <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
  </inertial>
  <visual>
    <geometry>
      <box size="0.6 0.4 0.2"/>
    </geometry>
  </visual>
</link>
```

This example shows a `base_link` with a collision shape, inertial properties (mass, inertia), and a visual representation, all used by Gazebo for physics calculations.

## 2. Unity Visualization Integration

While Gazebo provides good visualization, **Unity** can offer more advanced rendering, custom UI, and complex scene management for a richer digital twin experience. Integrating ROS 2 with Unity typically involves using the `ROS-TCP-Connector` and `ROS-TCP-Endpoint` packages.

### 2.1 Setting up Unity for ROS 2 Communication

1.  **Install Unity Hub and Unity Editor**: Download from the official Unity website.
2.  **Create a new 3D Unity Project**: Give it a suitable name.
3.  **Import ROS-TCP-Connector**: Add the `com.unity.ros-tcp-connector` package to your project via the Package Manager (from Git URL).
4.  **Configure ROS-TCP-Endpoint**: In your ROS 2 workspace, build the `ros_tcp_endpoint` package.

This setup allows Unity to act as a ROS 2 node, communicating with other ROS 2 nodes over TCP.

### 2.2 Visualizing ROS 2 Data in Unity

You can subscribe to ROS 2 topics in Unity and use the received data to update game objects, animations, or UI elements. For example, subscribing to a robot's joint states to animate a 3D model.

```csharp
// Example: Unity C# script to subscribe to a ROS 2 String topic
using RosMessageTypes.Std; // Assuming you have std_msgs generated
using Unity.Robotics.ROSTCPConnector;
using UnityEngine;

public class RosSubscriberExample : MonoBehaviour
{
    public string rosTopicName = "/my_string_topic";

    void Start()
    {
        ROSConnection.Get	Instance().Subscribe<StringMsg>(rosTopicName, ReceiveMessage);
    }

    void ReceiveMessage(StringMsg stringMessage)
    {
        Debug.Log($"Received from ROS: {stringMessage.data}");
        // Update UI or other game objects here
    }
}
```

This Unity C# script subscribes to a `/my_string_topic` and logs received string messages to the Unity console.

## 3. Sensor Simulation

Accurate sensor simulation is crucial for developing and testing robot perception algorithms without real hardware. Both Gazebo and Unity provide extensive capabilities for simulating various sensor types.

### 3.1 Gazebo Sensor Plugins

Gazebo supports a wide range of sensor plugins, including cameras, depth cameras, LiDARs, IMUs (Inertial Measurement Units), and contact sensors. These plugins can be added directly to your robot's SDF/URDF description.

```xml
<!-- Example: Adding a camera sensor to a Gazebo URDF extension -->
<gazebo reference="camera_link">
  <sensor name="camera" type="camera">
    <always_on>1</always_on>
    <visualize>true</visualize>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <ros> # ROS 2 specific configuration
        <namespace>camera</namespace>
        <argument>--ros-args -r __ns:=/my_robot</argument>
        <remap>image_raw:=image_raw</remap>
        <remap>camer-info:=camer-info</remap>
      </ros>
      <alwaysOn>true</alwaysOn>
      <updateRate>30.0</updateRate>
      <cameraName>camera</cameraName>
      <imageTopicName>image_raw</imageTopicName>
      <cameraInfoTopicName>camer-info</cameraInfoTopicName>
      <frameName>camera_link_optical</frameName>
    </plugin>
  </sensor>
</gazebo>
```

This Gazebo extension adds a camera sensor to a `camera_link` in the robot model, publishing image and camera info messages to ROS 2 topics.

### 3.2 Unity Sensor Simulation Tools

Unity provides tools like the **Unity Perception Package** to generate synthetic data for computer vision tasks. You can define ground truth labels, bounding boxes, and segmentation masks within your Unity scene to create annotated datasets for training AI models. Unity also supports physics-based raycasting and collision detection that can simulate range sensors.
