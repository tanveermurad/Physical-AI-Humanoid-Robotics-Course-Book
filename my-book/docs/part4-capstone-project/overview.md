# Capstone Project: The Autonomous Humanoid

Humanoid robots are poised to excel in our human-centered world because they share our physical form and can be trained with abundant data from interacting in human environments. This represents a significant transition from AI models confined to digital spaces.

This capstone quarter introduces Physical AI—AI systems that function in reality and comprehend physical laws. Students learn to design, simulate, and deploy humanoid robots.

## Project Overview

A final project where a simulated robot receives a voice command, plans a path, navigates obstacles, and identifies an object using computer vision.

### Focus Areas
*   Physics simulation and environment
*   NVIDIA Isaac Sim: Photorealistic simulation
*   Voice-to-Action: Using OpenAI Whisper for voice commands
*   ROS 2 package development: Nodes, topics, services

## Hardware Requirements

Because the capstone involves a "Simulated Humanoid," the primary investment must be in High-Performance Workstations.

If you do not have access to RTX-enabled workstations, we must restructure the course.

### Physical Robot Components

For the physical robot, we will use a shared "Edge Brain" model.

*   **Edge Brain:** Jetson Orin Nano. Runs the "Inference" stack. Students deploy their code here.
*   **Sensors:** RealSense Camera + Lidar. Connected to the Jetson to feed real-world data to the AI.
*   **Actuator:** Unitree Go2 or G1 (Shared). Receives motor commands from the Jetson.

**Warning:** The cheap kits (Hiwonder) usually run on Raspberry Pi, which cannot run NVIDIA Isaac ROS efficiently. You would use these only for kinematics (walking) and use the Jetson kits for AI.

### Voice Interface

*   **Microphone:** ReSpeaker USB Mic Array.
*   **Cost:** Approximately $700 (One-time purchase).

## Robot Options

### Option 1: Unitree Go2/G1
*   **Pros:** Highly durable, excellent ROS 2 support.
*   **Best for:** Rapid deployment, or students with less robotics experience.

### Option 2: Custom Build (e.g., Hiwonder)
*   **Pros:** Lower cost, more customization.
*   **Cons:** Requires more assembly and troubleshooting. Raspberry Pi based kits are not suitable for the full AI stack.

## Learning Trajectory

Solution: Students train their models on the high-performance workstations and then deploy them to the Jetson for real-world testing.
