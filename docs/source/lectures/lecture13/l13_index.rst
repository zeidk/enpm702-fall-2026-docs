====================================================
L13: Frames and Transforms
====================================================

Overview
--------

This lecture covers **coordinate frames and transforms**, from the pose
of a robot to the frame tree of TF2. A **pose**, a position and an
orientation, has a meaning only inside a frame. Every part of a robot
has a frame: the base, each sensor, and the world. **TF2**, the ROS 2
library for frames, keeps the tree of these frames, lets nodes broadcast
the transform between two of them, and lets other nodes listen for it
and use it. TF2 is essential whenever your robot has several sensors
and links, and it underpins the spatial reasoning of the autonomy stack.

The frames of the ROSbot (``odom``, ``base_link`` and the sensor frames)
are the ones of :doc:`ROSbot Simulation </setup/rosbot_simulation>`.
:doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>`
explains the quaternion and the yaw of a robot on a floor.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Explain what **coordinate frames** are and why a robot needs several.
   - Describe the **TF2 frame tree** and the standard frame names.
   - Use the ``TransformStamped`` message to represent a transform.
   - Broadcast **static** and **dynamic** transforms with TF2.
   - **Listen** for a transform, look it up with ``lookupTransform()``, and
     use it to express a point in another frame.
   - **Debug** frames: handle transform exceptions, and use
     ``view_frames``, ``tf2_echo`` and RViz2.


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

- TF2 is used extensively in **GP2**. Complete the exercise and quiz
  before you start its TF2 requirements.

- :doc:`Lecture 14 <../lecture14/l14_index>` (Robot Autonomy
  Architecture) shows how coordinate frames fit into a complete autonomy
  stack.
