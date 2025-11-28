---
sidebar_position: 1
---

# Perception

A robot cannot act intelligently without the ability to **perceive** its environment. Perception is the process of taking sensory information and using it to build an internal model of the world. For a robot, this means turning raw sensor data—pixels, point clouds, forces—into meaningful information, such as "there is a door in front of me," or "I am holding a cup."

Perception is arguably the most challenging aspect of building autonomous robots, as the real world is messy, dynamic, and unpredictable.

## Sensors for Robotics

Robots use a wide variety of sensors to perceive the world. These can be categorized into two main types:

- **Proprioceptive Sensors**: These sensors measure the internal state of the robot.
  - **Encoders**: Measure the position of the robot's joints.
  - **Inertial Measurement Units (IMUs)**: Measure the robot's orientation and angular velocity (using accelerometers and gyroscopes).

- **Exteroceptive Sensors**: These sensors measure the external environment.
  - **Cameras (Monocular, Stereo, RGB-D)**: Provide rich visual information about the environment. RGB-D (depth) cameras are particularly powerful as they provide a 3D point cloud of the scene.
  - **LiDAR (Light Detection and Ranging)**: Uses lasers to create a precise 2D or 3D map of the environment as a point cloud.
  - **Force/Torque Sensors**: Measure the forces and torques exerted on the robot's wrist or feet, essential for interaction tasks.
  - **Tactile Sensors**: Provide a sense of "touch," allowing a robot to detect contact and pressure distribution.

---

## Computer Vision

Computer vision is the field of AI that enables computers to "see" and interpret the visual world. With the rise of deep learning, computer vision has become incredibly powerful and is a cornerstone of modern robotics.

Key computer vision tasks in robotics include:

- **Object Detection**: Identifying and drawing a bounding box around objects in an image (e.g., "this is a cat," "this is a person").
- **Semantic Segmentation**: Classifying each pixel in an image with a category label (e.g., "this pixel is part of the road," "this pixel is part of a building").
- **Object Pose Estimation**: Determining the 3D position and orientation of an object, which is critical for manipulation.

![Semantic Segmentation Example](https://i.imgur.com/2Y5F2QJ.png)

## State Estimation and Sensor Fusion

Sensor data is inherently noisy and incomplete. A robot rarely has a direct measurement of the information it truly needs. For example, a robot needs to know its own position and orientation in the world (its **state**), but it can only measure its wheel rotations or the features it sees in an image.

**State estimation** is the process of estimating the true state of the robot (or another object) from noisy sensor measurements.

### Sensor Fusion

To get a more accurate and reliable estimate, we often combine data from multiple sensors. This is called **sensor fusion**. A classic example is fusing data from an IMU (which is good at measuring short-term changes in orientation but drifts over time) with data from a camera (which can recognize landmarks but is slower).

### Kalman Filters and SLAM

- **Kalman Filter**: A powerful algorithm for state estimation and sensor fusion. It maintains a belief about the state of the system (represented as a probability distribution) and updates this belief over time using a predict-correct cycle. It is widely used for tracking and localization.

- **Simultaneous Localization and Mapping (SLAM)**: This is a fundamental problem in mobile robotics. A robot is placed in an unknown environment and must build a map of it while simultaneously keeping track of its own location within that map. SLAM algorithms (like EKF-SLAM or ORB-SLAM) often use techniques like the Kalman filter or particle filters at their core.

Perception is the bridge between the robot and the real world. Without a robust perception system, even the most sophisticated planning and control algorithms would be useless.