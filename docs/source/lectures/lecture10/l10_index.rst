====================================================
L10: ROS 2 Foundations
====================================================

Overview
--------

This is the first ROS 2 lecture in ENPM702. It is about topics, the way ROS 2 nodes send each other a stream of data. A fleet of robotaxis runs through the whole lecture: a robotaxi node publishes its position, and a dispatcher node subscribes to it and computes the distance to a pickup point. On the way, the lecture reads the build files of a package, writes a first node as a class derived from ``rclcpp::Node``, and shows what spinning does and what happens to messages when a subscriber is slow.

Before class, read the Pre-Reading part of the :doc:`l10_lecture` and do the two steps of its Before Class part. The lecture starts from it.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Tell topics, services and actions apart, and read a computation graph.
   - State the four rules of a topic, and recognize its four patterns.
   - Start nodes with ``ros2 run`` and ``ros2 launch``, and inspect them with ``ros2 node``, ``ros2 topic`` and ``ros2 interface``.
   - Read a package's ``package.xml`` and ``CMakeLists.txt``, and say where ``ros2 run`` finds an executable.
   - Write a node as a class derived from ``rclcpp::Node``, and keep it alive with ``rclcpp::spin``.
   - Use a standard message type in C++, and declare its package in both build files.
   - Write a publisher with a timer, and a subscriber with a callback.
   - Explain what happens to messages with no subscriber, a fast subscriber and a slow one.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_lecture
   l10_exercises
   l10_quiz
   l10_references

Next Steps
----------

- In the next lecture (**L11: ROS 2 Configuration and Orchestration**), we will cover message types of your own, parameters, launch files and executors.
- Before next class: complete the L10 exercise and quiz, and build and run ``robotaxi_demo`` in your own workspace.
- Required reading: `Writing a simple publisher and subscriber (C++) <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>`_ and `Topics <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Topics.html>`_.
