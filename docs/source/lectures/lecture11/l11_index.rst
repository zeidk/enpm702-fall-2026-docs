====================================================
L11: ROS 2 Configuration and Orchestration
====================================================

Overview
--------

This lecture is about starting and running the nodes of a ROS 2 system, and about the messages they send. Launch files start several nodes with one command: the lecture writes them in Python, then adds an included launch file, launch arguments and conditions, groups with namespaces, and event handlers. Executors run the callbacks of the nodes: the lecture compares a single-threaded executor with a multi-threaded one, and shows with a four-timer test node and timelines what mutually exclusive and reentrant callback groups change. Custom interfaces replace a standard message type with one you write yourself, in a ``.msg`` file. A robotaxi and a fleet depot run through the lecture.

Before class, do the two steps of the Before Class part of the :doc:`l11_lecture`: update your copy of the course repository, and build the two packages of this lecture.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Write a Python **launch file** that starts several nodes, and install it from ``CMakeLists.txt``.
   - Include another launch file, and use **launch arguments** and **conditions** to start a node only when an argument says so.
   - Use **groups** and namespaces to run two copies of the same nodes, with or without a condition.
   - Use **event handlers** to run actions when a process starts or the launch shuts down.
   - Explain what **rclcpp::spin(node)** does, and run two nodes in one **single-threaded executor**.
   - Explain what a slow callback does to the other callbacks of a single-threaded executor.
   - Explain how a **multi-threaded executor** runs callbacks in **parallel** on several threads, and why parallel callbacks can cause a data race.
   - Choose between **mutually exclusive** and **reentrant callback groups**, and predict which callbacks wait.
   - Write a **custom message** in a ``.msg`` file inside an interface package, and build it.
   - Use a custom message in C++ nodes: depend on its package, include the generated header, and read the constants and fields.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l11_lecture
   l11_exercises
   l11_quiz
   l11_references

Next Steps
----------

- In the next lecture (**L12: ROS 2 Communication Patterns**), we will cover parameters, services and actions.
- Before next class: complete the L11 exercises and quiz, and build and run ``l11_robotaxi`` in your own workspace.
- Required reading: `ROS 2 Jazzy: Creating a launch file <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`_, `ROS 2 Jazzy: Executors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`_ and `ROS 2 Jazzy: Creating custom msg and srv files <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html>`_.
