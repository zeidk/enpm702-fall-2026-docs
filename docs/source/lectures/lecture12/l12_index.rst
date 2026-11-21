====================================================
L12: Robots in Gazebo and Parameters
====================================================

Overview
--------

This lecture puts the Husarion ROSbot in a Gazebo world and writes the first controllers for it. The ROSbot is the robot of Lecture 12 to Lecture 14 and of Group Project 2. You start it with one launch file, see what the launch file starts, view the robot in **RViz**, read its pose from ``/odometry/filtered``, and drive it with ``TwistStamped`` messages on ``/cmd_vel``. Gazebo has its own topics, and a bridge copies the ones you need to ROS. Gazebo also has its own clock, **simulation time**: the lecture shows what ``use_sim_time`` changes for ``now()``, and which kind of timer stops when Gazebo is paused.

A **proportional controller** sets a speed in proportion to an error. The lecture writes one as a node that turns the ROSbot on the spot to a heading. It has a gain, a speed limit and a tolerance. A second node, which drives the ROSbot straight for a distance, is in a More detail box of the lecture page.

Those numbers are then moved out of the code into **parameters**: named values of a node that you set at start or change while the node runs, without a rebuild. The lecture declares and reads them, sets them with ``-p``, a YAML file and a launch file, and uses a parameter callback to accept or reject a new value while the ROSbot turns.

The last section is **namespaces** and **remapping**. A namespace is a prefix in front of a node's name and of its relative names, so the same code runs once per robot. A remapping rule, ``match:=replacement``, changes a name the node uses without editing its code. The lecture runs two copies of the heading controller in two namespaces, reads the wheel odometry with a rule, combines a namespace with two rules, and writes the same settings in a launch file.

Before the lecture, read :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` and set up the :doc:`ROSbot Simulation </setup/rosbot_simulation>`. Then do the two steps of the Before Class part of the :doc:`l12_lecture`: update your copy of the course repository, and build the package ``l12_rosbot``.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Start the **ROSbot** in **Gazebo**, and explain why Gazebo's own topics reach ROS only through a **bridge**.
   - View the robot in **RViz**, list its ROS topics, and drive it with a ``TwistStamped`` command on ``/cmd_vel``.
   - Read the robot's pose from ``/odometry/filtered``, and compute its **yaw** from the orientation.
   - Explain the difference between the computer's clock and **simulation time**, what ``use_sim_time`` changes for ``now()``, and which kind of **timer** stops when Gazebo is paused.
   - Compute the **error** of a turn, the angle left to turn the short way.
   - Write a **proportional controller** node: a command that is a **gain** times the error, limited to a maximum speed, that stops within a **tolerance**.
   - **Declare** a **parameter** with a type and a default value, and read it in a node.
   - Set parameters at start with ``-p``, with a **parameter file**, and with a **launch file**, and set ``use_sim_time`` for a node that runs with Gazebo.
   - List, get and set the parameters of a running node, and explain why a value the node already read does not change its behavior.
   - Check and store a new value while the node runs, with a **parameter callback**.
   - Put a node in a **namespace**, and tell how it changes a **relative**, an **absolute** and a **private** name.
   - Write a **remapping rule**, ``match:=replacement``, with ``--ros-args -r`` or in a launch file, to rename a topic, a node or a namespace, and combine rules with a namespace.

Interactive Slides
------------------

The slides from class as a web page you can try: build a velocity command and see the path it gives, turn the heading-error dial, replay the measured runs, test a value against the parameter callback, and resolve names in a namespace. It runs in your browser, with nothing to install. The :doc:`l12_interactive` page says how to use it.

.. button-link:: interactive/L12_interactive.html
   :color: primary
   :shadow:

   Open the interactive slides

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l12_lecture
   l12_interactive
   l12_exercises
   l12_quiz
   l12_references

Next Steps
----------

- In the next lecture (:doc:`L13: Frames and Transforms <../lecture13/l13_index>`), we will cover poses, frames, and broadcasting, listening to and debugging transforms. The ``/tf`` and ``/tf_static`` topics of the ROSbot are in the topic table of this lecture.
- Before next class: complete the L12 exercises and quiz, and build and run ``l12_rosbot`` in your own workspace.
- GP2 is posted today. This lecture covers the simulation it runs in, proportional control and parameters.
- Required reading: `ROS 2 Jazzy: Parameters <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`_, the :doc:`ROSbot Simulation </setup/rosbot_simulation>` page and the :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` reading.
- Optional, beyond the course: the :doc:`Services and Actions </reading_material/services_actions/sa_index>` reading.
