---
sidebar_position: 3
---

# Control Systems

Having models for a robot's kinematics and dynamics is essential, but they are only useful if we can use them to make the robot move in a desired way. This is the role of the **control system**.

A control system is a device, or set of devices, that manages, commands, directs, or regulates the behavior of other devices or systems. In robotics, the control system is the brain that translates a desired task (e.g., "pick up the object") into the precise sequence of torques that the motors must apply to the joints.

## Open-Loop vs. Closed-Loop Control

Control systems can be broadly categorized into two types:

- **Open-Loop Control**: In an open-loop system, the control action is independent of the system's output. It's like a toaster: you set the timer, and it applies heat for that duration, regardless of how toasted the bread actually is. For a robot, this would be applying a pre-calculated set of torques without checking if the robot is actually following the desired trajectory. These systems are simple but cannot compensate for errors or disturbances.

- **Closed-Loop (Feedback) Control**: In a closed-loop system, the controller uses feedback from sensors to measure the system's output and compare it to the desired output. The difference, called the **error**, is then used to adjust the control action. This is like a thermostat: it measures the room temperature and turns the heater on or off to maintain the desired temperature. This is the dominant paradigm in robotics.

![A diagram showing a feedback control loop](https://i.imgur.com/kY7h7s7.png)

## PID Control

The Proportional-Integral-Derivative (PID) controller is the most common type of feedback controller used in industrial robotics. It calculates the control action based on three terms:

$$ 
\tau(t) = K_p e(t) + K_i \int_0^t e(t') dt' + K_d \frac{de(t)}{dt} 
$$

- **Proportional ($K_p$)**: This term produces a control action that is proportional to the current error, $e(t)$. A larger error results in a larger control action. It's the primary driver of the controller.
- **Integral ($K_i$)**: This term sums up the error over time. It is used to eliminate the **steady-state error**, which is the final error that remains after the system has settled.
- **Derivative ($K_d$)**: This term is proportional to the rate of change of the error. It is used to "damp" the system's response, reducing overshoot and oscillations.

PID controllers are popular because they are effective, intuitive to tune (though tuning can be an art), and don't require a detailed model of the system.

## Model-Based Control

While PID control is effective for many tasks, it can be limited when high performance is required. Model-based control techniques use the dynamic model of the robot to achieve more precise and efficient motion.

### Computed Torque Control

Computed Torque Control (also known as inverse dynamics control) is a powerful model-based technique. Recall the equation of motion:

$$ 
\tau = M(q)\ddot{q} + C(q, \dot{q})\dot{q} + G(q) 
$$

If we know the model ($M, C, G$), we can calculate the required torque to achieve a desired acceleration, $\ddot{q}_{des}$. The control law is:

$$ 
\tau = M(q)(\ddot{q}_{des}) + C(q, \dot{q})\dot{q} + G(q) 
$$

The desired acceleration, $\ddot{q}_{des}$, is often chosen using a PID-like structure to correct for any errors from the desired trajectory:

$$ 
\ddot{q}_{des} = \ddot{q}_d + K_d(\dot{q}_d - \dot{q}) + K_p(q_d - q) 
$$

By using the model to "cancel out" the complex, non-linear dynamics of the robot, we are left with a simple, linear system that is much easier to control.

## Force Control

The control schemes discussed so far are for **motion control**. However, many tasks require the robot to interact with its environment, such as pushing a button, turning a crank, or polishing a surface. In these cases, we also need to control the **forces** of interaction.

**Force control** (or impedance control) is a strategy that allows the robot to behave like a mass-spring-damper system. Instead of controlling the position of the end-effector directly, the controller regulates the relationship between the end-effector's position and the force it exerts on the environment. This makes the robot compliant and safe for interaction tasks.

This concludes our look at the fundamentals of robotics. With an understanding of kinematics, dynamics, and control, we are now ready to explore how artificial intelligence can be used to give robots the ability to perceive, plan, and learn.