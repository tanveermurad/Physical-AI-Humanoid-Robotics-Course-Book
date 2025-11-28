---
sidebar_position: 2
---

# Manipulation

Beyond walking, the primary way a humanoid robot interacts with the world is through **manipulation**: using its hands and arms to grasp, move, and use objects. The goal of humanoid robotics is to create robots that can operate in human environments, and a key part of this is the ability to use the same tools and objects that humans do.

Manipulation is a rich and complex field that brings together challenges in perception, planning, and control.

## Grasping

Grasping is the foundational act of manipulation. To pick up an object, a robot must be able to:

1.  **Perceive the Object**: Identify the object and estimate its pose (position and orientation).
2.  **Select a Grasp**: Choose a stable way to hold the object. A stable grasp is one that can resist external forces and torques.
3.  **Plan a Motion**: Plan a collision-free path for the arm and hand to reach the object and execute the grasp.
4.  **Control the Grasp**: Apply the correct amount of force to hold the object securely without crushing it.

### Grasp Analysis

A common way to analyze the stability of a grasp is through the concept of **force closure**. A grasp has force closure if the robot's fingers can apply forces to counteract any arbitrary external force or torque, preventing the object from slipping.

![Force Closure Diagram](https://i.imgur.com/gOQ5OqL.png)

## Mobile Manipulation

For a humanoid robot, manipulation is inherently **mobile manipulation**. The robot can use its whole body to assist in a manipulation task. This is a significant advantage over a fixed-base robotic arm.

- **Increasing Reach**: A humanoid can walk to an object that is out of its arm's reach.
- **Providing Support**: The robot can use one arm to brace itself against a surface while the other arm performs a task.
- **Whole-Body Coordination**: For heavy or awkward objects, the robot can use its legs and torso, in addition to its arms, to lift and move the object.

This coordination between locomotion and manipulation is a key area of research in humanoid robotics. A whole-body controller, as discussed in the bipedal locomotion chapter, is essential for managing the complex interactions between the robot's upper body and lower body.

## Dual-Arm Manipulation

Having two arms unlocks a vast range of new capabilities that are impossible with a single arm. **Dual-arm manipulation** allows a robot to perform tasks such as:

- **Lifting heavy objects** that one arm could not lift alone.
- **Holding an object with one hand while the other hand works on it** (e.g., holding a jar while twisting off the lid).
- **Assembling complex parts**.
- **Handing objects from one hand to the other (regrasping)** to get a better grip or to place the object in a new location.

Coordinating the motion of two arms is a challenging planning and control problem, as the motion of one arm can affect the other, and they must work together to achieve a common goal.

## In-Hand Manipulation

While much of robotics focuses on picking up and placing objects, humans are also skilled at **in-hand manipulation**: adjusting the pose of an object within the hand without letting go of it. Examples include re-orienting a pen to start writing, or spinning a key to fit it into a lock.

This is a highly advanced skill that requires dexterous, multi-fingered hands and sophisticated control strategies. It is an active area of research, and success in this area will be a major step towards creating robots with human-level dexterity.