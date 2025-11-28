---
sidebar_position: 1
---

# Bipedal Locomotion

One of the defining characteristics of a humanoid robot is its ability to walk on two legs: **bipedal locomotion**. Walking is one of the most challenging problems in robotics, as it involves controlling a complex, high-dimensional, and inherently unstable system.

While wheeled robots are more stable and energy-efficient on flat surfaces, legged robots have a significant advantage in navigating the complex, unstructured environments that are designed for humans, such as stairs, cluttered rooms, and uneven terrain.

## The Challenge of Balance

The central challenge of bipedal walking is maintaining balance. A walking robot is constantly on the verge of falling. To stay upright, the robot must actively control its motion to keep its center of mass within its **support polygon** (the area formed by its feet on the ground).

### The Zero Moment Point (ZMP)

A key concept for controlling balance is the **Zero Moment Point (ZMP)**. The ZMP is the point on the ground where the net moment of the inertial and gravitational forces is zero. In other words, it is the point where the total tipping moment acting on the robot is zero.

**To maintain balance, the ZMP must always remain within the support polygon.**

![ZMP Diagram](https://i.imgur.com/7gY3sQe.png)

If the ZMP moves outside the support polygon, the robot will begin to fall. Controllers for humanoid robots are designed to generate motions that keep the ZMP in a stable location.

## Generating a Walking Gait

A **gait** is a pattern of limb movements made during locomotion. For walking, the gait involves alternating between a **single support phase** (one foot on the ground) and a **double support phase** (both feet on the ground).

### Trajectory Generation

The process of generating a walking motion is often broken down into several steps:

1.  **Footstep Planning**: The robot first decides where to place its feet to navigate towards a goal.
2.  **Center of Mass (CoM) Trajectory Generation**: A trajectory for the robot's center of mass is planned. A common simplified model used for this is the **Linear Inverted Pendulum Model (LIPM)**, which models the robot as a single point mass on a massless leg.
3.  **ZMP Trajectory Generation**: Based on the CoM trajectory, a desired trajectory for the ZMP is calculated.
4.  **Inverse Kinematics**: An inverse kinematics solver is used to calculate the joint angle trajectories that will produce the desired CoM and foot motions.

## Whole-Body Control

The methods described above often rely on simplified models. Modern humanoid robots are increasingly using **whole-body control**.

A whole-body controller considers the full dynamics of the robot and formulates the control problem as a constrained optimization problem. The controller's goal is to find the joint torques that will best achieve a set of prioritized tasks, subject to the physical constraints of the robot and the environment.

A typical task hierarchy might be:
1.  **Highest Priority**: Maintain balance (keep ZMP in the support polygon).
2.  **Second Priority**: Follow the desired CoM and foot trajectories.
3.  **Third Priority**: Keep the torso upright.
4.  **Lowest Priority**: Move the arms in a natural-looking way.

This optimization-based approach allows for the control of very complex motions and interactions with the environment, and is a key technology enabling the dynamic and agile behaviors we see in modern humanoid robots.