---
sidebar_position: 2
---

# Dynamics

While kinematics describes the motion of a robot, **dynamics** addresses the forces and torques required to create that motion. Understanding dynamics is critical for designing controllers, simulating robot behavior, and ensuring the robot's structure can withstand the stresses of operation.

Dynamics is the study of motion in relation to the forces that cause it. For a robot, this means modeling the relationship between the joint torques applied by the motors and the resulting motion of the links.

## The Equation of Motion

The dynamics of a robot manipulator can be described by the following general equation of motion:

$$ 
\tau = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + G(q)
$$ 

Let's break down each component of this equation:

- $\tau$: A vector of the forces or torques applied by the joint actuators.
- $q$, $\dot{q}$, $\ddot{q}$: The position, velocity, and acceleration vectors of the robot's joints.
- $M(q)$: The **mass matrix** or **inertia matrix**. This is a symmetric positive-definite matrix that represents the inertia of the robot. It depends on the robot's configuration, $q$.
- $C(q, \dot{q})\dot{q}$: A vector of **Coriolis and centrifugal torques**. These terms arise from the interaction between the moving links. The $C$ matrix is often called the Coriolis matrix.
- $G(q)$: A vector of **gravitational torques**. These are the torques required at each joint to hold the robot's position against gravity.

This equation forms the basis of many advanced control techniques, as it provides a model of the robot's behavior that the controller can use.

---

## Formulations for Deriving the Equations of Motion

There are two primary methods for deriving the equations of motion for a robot: the Lagrangian and the Newton-Euler formulations.

### Lagrangian Dynamics

The Lagrangian approach is an energy-based method that is elegant and systematic. It considers the robot as a whole system and derives the equations of motion from its kinetic and potential energy.

The **Lagrangian** ($\mathcal{L}$) of the system is defined as the difference between the total kinetic energy ($K$) and the total potential energy ($P$) of the manipulator.

$$ 
\mathcal{L}(q, \dot{q}) = K(q, \dot{q}) - P(q)
$$ 

The equations of motion are then derived using the **Euler-Lagrange equation**:

$$ 
\frac{d}{dt} \left( \frac{\partial \mathcal{L}}{\partial \dot{q}_i} \right) - \frac{\partial \mathcal{L}}{\partial q_i} = \tau_i
$$ 

For each joint $i$.

- **Advantages**: Systematic, avoids dealing with internal forces between links.
- **Disadvantages**: Can be computationally intensive for complex robots, as it involves differentiating the energy terms.

### Newton-Euler Formulation

The Newton-Euler method is an algorithm that directly applies Newton's and Euler's equations of motion to each link in the manipulator. It is a recursive algorithm that is often more computationally efficient.

The algorithm consists of two passes:

1.  **Forward (Outward) Recursion**: Starting from the base and moving to the end-effector, the velocities and accelerations (linear and angular) of each link are calculated.
2.  **Backward (Inward) Recursion**: Starting from the end-effector and moving to the base, the forces and torques exerted on each link are calculated, ultimately yielding the required joint torques.

- **Advantages**: Computationally efficient, provides the forces and torques at each joint (useful for mechanical design).
- **Disadvantages**: Can be more complex to implement by hand compared to the Lagrangian method.

---

## Applications of Dynamic Modeling

A good dynamic model is essential for:

- **Model-Based Control**: Controllers like "computed torque control" use the dynamic model to calculate the exact torques needed to achieve a desired motion, compensating for inertia, gravity, and other effects.
- **Simulation**: Simulators use the equations of motion to accurately predict how a robot will move under the influence of certain forces, which is crucial for testing and development without using a physical robot.
- **Mechanical Design**: By calculating the forces and torques that each link and joint will experience, engineers can design robots that are strong enough for their intended tasks.
- **Force Control**: For tasks that involve interaction with the environment (e.g., polishing a surface), the dynamic model helps in controlling the forces exerted by the end-effector.