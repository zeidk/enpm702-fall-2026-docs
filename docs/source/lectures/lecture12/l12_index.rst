====================================================
L12: Robots in Gazebo and Parameters
====================================================

Overview
--------

This lecture puts the Husarion ROSbot in a Gazebo world and writes the
first controller for it. A **proportional controller** sets the velocity
of the robot in proportion to an error, such as the angle to the
direction it should face. The gain of such a controller, and the speeds
of the robot, are **parameters**: values of a node that you set at start
or change while the node runs, without a rebuild. This lecture shows how
to declare a parameter, read it, load it from a YAML file with a launch
file, and change it with ``ros2 param``.

The ROSbot is the robot of Lecture 12 to Lecture 14 and of Group Project
2. Read :doc:`Mobile Robot Messages
</reading_material/robot_messages/rmsg_index>` before the lecture: it
explains the ``cmd_vel``, ``odometry/filtered`` and ``scan`` topics of
the ROSbot.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Start the **ROSbot** in **Gazebo**, and list its topics.
   - Command the ROSbot with a velocity message on ``cmd_vel``, and read
     its pose from ``odometry/filtered``.
   - Write a **proportional controller**: a velocity that is a **gain**
     times an error.
   - **Declare** a **parameter** with a type and a default, and read its
     value in a node.
   - Set parameters at start with ``-p``, with a **YAML file**, and with a
     **launch file**.
   - Change a parameter of a running node with ``ros2 param set``, and
     check the new value in a **parameter callback**.

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

- In the next lecture (:doc:`L13: Frames and Transforms
  <../lecture13/l13_index>`), we will cover:

  - Poses, the quaternion and the yaw.
  - Coordinate frames and the frame tree.
  - Static and dynamic transform broadcasters, listeners, and how to
    debug a transform.

- Before next class: read :doc:`Mobile Robot Messages
  </reading_material/robot_messages/rmsg_index>` and set up :doc:`ROSbot
  Simulation </setup/rosbot_simulation>`.
- Extra reading, not needed for the course projects: :doc:`Services and
  Actions </reading_material/services_actions/sa_index>`.
