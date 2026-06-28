====================================================
L13: ROS 2 Coordinate Frames and Transforms
====================================================

Overview
--------

This lecture covers **coordinate frame management with TF2**, the ROS 2
framework for tracking and transforming between the many reference frames
on a robot (its base, each sensor, and the world). TF2 is essential
whenever your robot has multiple sensors and links, and it underpins the
spatial reasoning used throughout the autonomy stack. The companion topic,
**lifecycle nodes**, is covered in the next lecture
(:doc:`Lecture 14 <../lecture14/l14_index>`).


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Understand what coordinate frames are and why they are essential in robotics.
   - Describe the TF2 frame tree and standard frame conventions.
   - Use the ``TransformStamped`` message to represent a transform.
   - Broadcast static and dynamic transforms with TF2.
   - Listen for transforms and look them up with ``lookupTransform()``.
   - Handle transform exceptions and debug frames with ``view_frames``, ``tf2_echo``, and RViz2.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l13_lecture
   l13_exercises
   l13_quiz
   l13_references

Next Steps
----------

- TF2 is used extensively in **GP3**. Complete the exercises and quiz
  before starting the project.

- :doc:`Lecture 14 <../lecture14/l14_index>` (Lifecycle Nodes) is the
  companion to this lecture, and :doc:`Lecture 15 <../lecture15/l15_index>`
  (Robot Autonomy Architecture) shows how coordinate frames fit into a
  complete autonomy stack.
