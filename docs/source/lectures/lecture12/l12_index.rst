====================================================
L12: Robots in Gazebo and Parameters
====================================================

Overview
--------

This lecture puts the Husarion ROSbot in a Gazebo world and writes the first controllers for it. The ROSbot is the robot of Lecture 12 to Lecture 14 and of Group Project 2. You start it with one launch file, read its pose from ``/odometry/filtered``, and drive it with ``TwistStamped`` messages on ``/cmd_vel``.

A **proportional controller** sets a speed in proportion to an error. The lecture writes two of them as nodes: one turns the ROSbot on the spot to a heading, and one drives it straight for a distance. Each has a gain, a speed limit and a tolerance.

Those numbers are then moved out of the code into **parameters**: named values of a node that you set at start or change while the node runs, without a rebuild. The lecture declares and reads them, sets them with ``-p``, a YAML file and a launch file, and uses a parameter callback to accept or reject a new value while the ROSbot turns.

Before the lecture, read :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` and set up the :doc:`ROSbot Simulation </setup/rosbot_simulation>`. Then do the two steps of the Before Class part of the :doc:`l12_lecture`: update your copy of the course repository, and build the package ``l12_rosbot``.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Start the **ROSbot** in **Gazebo**, list its topics, and drive it with a ``TwistStamped`` command on ``/cmd_vel``.
   - Read the robot's position and its **yaw** from ``/odometry/filtered``.
   - Compute the **error** of a turn, the angle left to turn the short way, and the error of a drive, the distance left.
   - Write a **proportional controller** node: a command that is a **gain** times the error, limited to a maximum speed, that stops within a **tolerance**.
   - **Declare** a **parameter** with a type and a default value, and read it in a node.
   - Set parameters at start with ``-p``, with a **parameter file**, and with a **launch file**, and set ``use_sim_time`` for a node that runs with Gazebo.
   - List, get, set and dump the parameters of a running node, and explain why a value the node already read does not change its behavior.
   - Check and store a new value while the node runs, with a **parameter callback**.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l12_lecture
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
