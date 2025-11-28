---
sidebar_position: 2
---

# Dynamics

While kinematics describes the motion of a robot without considering the forces that cause it, **dynamics** is the study of motion in relation to the forces and torques that produce it. Understanding dynamics is crucial for simulating robot behavior, designing controllers, and ensuring the robot can perform its tasks without damaging itself or its environment.

## Key Concepts in Robot Dynamics

- **Mass**: A measure of an object's inertia, or its resistance to acceleration when a force is applied. In a robot, each link has its own mass.
- **Inertia Tensor**: This is the rotational equivalent of mass. It's a 3x3 matrix that describes how the mass of a link is distributed and how it resists angular acceleration.
- **Force**: A push or a pull on an object. In robotics, forces are applied by actuators, gravity, and contact with the environment.
- **Torque**: The rotational equivalent of force. It's a twisting force that causes an object to rotate. Actuators in revolute joints produce torques.

## Equations of Motion

The core of robot dynamics is the **equations of motion**, which describe the relationship between the forces and torques applied to the robot and the resulting acceleration of its joints. The general form of the equations of motion for a robotic manipulator is:

$$ 	au = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + G(q) $$ 

Where:
- $\tau$ is the vector of joint torques (and/or forces for prismatic joints).
- $q$, $\dot{q}$, and $\ddot{q}$ are the joint positions, velocities, and accelerations.
- $M(q)$ is the **mass matrix**, which represents the inertia of the robot. It depends on the current configuration of the robot ($q$).
- $C(q, \dot{q})\dot{q}$ represents the **Coriolis and centrifugal forces**. These are velocity-dependent forces that arise in a rotating coordinate frame.
- $G(q)$ is the **gravity vector**, which represents the forces on the joints due to gravity.

## Forward and Inverse Dynamics

Similar to kinematics, there are two main problems in dynamics:

- **Forward Dynamics**: Given the joint torques ($\tau$) and the current state of the robot ($q$, $\dot{q}$), what is the resulting joint acceleration ($\ddot{q}$)? This is used for simulation – predicting how the robot will move.

$$ \ddot{q} = M(q)^{-1}(\tau - C(q, \dot{q})\dot{q} - G(q)) $$ 

- **Inverse Dynamics**: Given the desired joint accelerations ($\\ddot{q}$) and the current state ($q$, $\dot{q}$), what are the required joint torques ($\\tau$)? This is used for control – calculating the motor commands needed to achieve a desired motion.

$$ \tau = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + G(q) $$ 

The **Recursive Newton-Euler Algorithm (RNEA)** and the **Euler-Lagrange formulation** are two common methods for deriving the equations of motion for a robot.

## Application in Humanoid Robots

Dynamics is critical for humanoid robotics:

- **Simulation**: Accurate dynamic simulation is essential for developing and testing walking gaits, control strategies, and planning algorithms before deploying them on a physical robot.
- **Feedforward Control**: Inverse dynamics can be used to calculate the torques required for a desired motion. This "feedforward" torque can be sent to the motors, which a feedback controller (like a PID) then refines. This makes the controller more efficient and accurate.
- **Force Control**: For tasks that involve contact with the environment, such as pushing a door or walking on uneven terrain, the robot needs to be able to control the forces it exerts. This requires a dynamic model of the robot and the environment.

By understanding the dynamics of a humanoid robot, we can create controllers that are more robust, efficient, and capable of performing a wider range of tasks.
