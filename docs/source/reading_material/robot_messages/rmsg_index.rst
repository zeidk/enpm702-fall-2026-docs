====================================================
Mobile Robot Messages
====================================================

Overview
--------

GP1 and GP2 use the topic names and message types of a real mobile
robot, the Husarion ROSbot: ``cmd_vel``, ``odometry/filtered`` and
``scan``. The lectures did not cover these messages. This reading
material explains each one: what its fields hold, which fields a robot
on a floor uses, in which direction and unit each one counts, and how
to read and write them in C++. It is a self-study reading module, with
no video. Read it before you start GP1.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Give the directions and units of ROS (REP 103): x forward, y left,
     z up, and a positive yaw to the left.
   - Command a ground robot with the ``linear.x`` and ``angular.z`` of a
     ``Twist``, and say which path a command drives.
   - Find the position and the heading in a ``nav_msgs/msg/Odometry``,
     and say which frame they are measured in.
   - Convert between a yaw and the quaternion of a robot on a floor, with
     the helpers of ``geometry.hpp``.
   - Compute the angle of each beam of a ``LaserScan``, and discard the
     ranges a scanner could not measure.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   rmsg_lecture
   rmsg_references
