====================================================
C++ Exercises
====================================================

These exercises reinforce the autonomy-architecture concepts from
Lecture 15. They combine **design exercises** (decomposing a system into
Sense-Plan-Act and mapping it onto ROS 2) with **coding exercises**
(implementing the layers as ROS 2 nodes). Work through them in order.

.. note::

   The coding exercises require a ROS 2 Jazzy workspace and assume a
   TurtleBot3-style robot (or Gazebo simulation) exposing ``/scan`` and
   ``/cmd_vel``. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1: Decompose a Task (Design)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice decomposing a robotics task into the Sense-Plan-Act
    layers and mapping each data flow onto a ROS 2 communication pattern.

    **Specification**

    A warehouse robot must patrol between two shelves and stop if a
    person steps in front of it. For this task:

    1. Identify what belongs in the **perception**, **decision**, and
       **control** layers.
    2. For each arrow between layers, state which ROS 2 primitive
       (topic, service, or action) you would use and why.
    3. Identify one place where a **parameter** would be useful.

.. dropdown:: Exercise 2: Reactive Controller (Front Sector)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a reactive decision/control node that only reacts to
    obstacles **directly ahead**, instead of anywhere in the scan.

    **Specification**

    1. Create a node ``front_reactive_controller``.
    2. Subscribe to ``/scan`` (``sensor_msgs::msg::LaserScan``) and
       publish to ``/cmd_vel`` (``geometry_msgs::msg::Twist``).
    3. Examine only the readings in a **front sector**, the first and
       last 15 readings of ``ranges`` (which straddle straight ahead).
    4. If the nearest reading in the front sector is closer than a
       ``safe_distance`` parameter (default 0.5 m), turn in place;
       otherwise drive forward.

.. dropdown:: Exercise 3: Separate Perception from Decision
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Split the monolithic reactive controller into a **perception node**
    and a **decision node** connected by a topic, a true two-layer
    architecture.

    **Specification**

    1. **Perception node** ``obstacle_perception``: subscribe to
       ``/scan``, compute whether an obstacle is within 0.5 m anywhere in
       the scan, and publish a ``std_msgs::msg::Bool`` on
       ``/obstacle_ahead``.
    2. **Decision node** ``obstacle_decision``: subscribe to
       ``/obstacle_ahead`` and publish ``/cmd_vel``, turn if ``true``,
       drive forward if ``false``.
    3. Run both nodes together and confirm the robot behaves as before.

.. dropdown:: Exercise 4: Where Does the Model Go? (Design)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Reason about integrating a trained ML model into the architecture.

    **Specification**

    Suppose you train a neural network that takes a camera image and
    outputs whether the path ahead is "blocked" or "clear".

    1. Which layer and which node hosts the model?
    2. What is the node's input topic and output topic?
    3. If you later retrain the model to be more accurate, which other
       nodes in the system must change?
    4. Name one C++ library you could use to run the model for inference.

.. dropdown:: Exercise 5: Choose an Architecture Style (Design)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Match architecture styles (reactive, deliberative, hybrid) to
    scenarios.

    **Specification**

    For each scenario, choose the most appropriate style and justify it:

    1. An emergency bumper that stops the robot the instant it touches
       something.
    2. A delivery robot that must find the shortest route across a known
       building map.
    3. A warehouse robot that plans efficient routes but must also avoid
       people who suddenly appear.
