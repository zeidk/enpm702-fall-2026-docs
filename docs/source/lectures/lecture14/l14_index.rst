====================================================
L14: ROS 2 Lifecycle Nodes
====================================================

Overview
--------

This lecture covers **managed (lifecycle) nodes**, ROS 2 nodes whose
execution is governed by a state machine, giving you deterministic
startup, shutdown, and error recovery. Lifecycle nodes let you bring up a
complex system in a controlled order and are widely used in
production-grade ROS 2 software. The lecture builds on the coordinate
frame material from :doc:`Lecture 13 <../lecture13/l13_index>`.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Explain why managed nodes exist and when to use them.
   - Describe the lifecycle state machine and its primary states (Unconfigured, Inactive, Active, Finalized).
   - Implement a lifecycle node by inheriting from ``rclcpp_lifecycle::LifecycleNode``.
   - Use the transition callbacks (``on_configure``, ``on_activate``, ``on_deactivate``, ``on_cleanup``, ``on_shutdown``).
   - Understand ``LifecyclePublisher`` behavior across states.
   - Manage lifecycle nodes using ``ros2 lifecycle`` CLI commands and programmatic transitions.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l14_lecture
   l14_exercises
   l14_quiz
   l14_references

Next Steps
----------

- Lifecycle nodes (together with TF2 from :doc:`Lecture 13
  <../lecture13/l13_index>`) are used extensively in **GP3**. Complete the
  exercises and quiz before starting the project.

- :doc:`Lecture 15 <../lecture15/l15_index>` (Robot Autonomy Architecture)
  shows how lifecycle nodes fit into a complete robot autonomy stack.
