====================================================
Namespaces and Remapping
====================================================

Overview
--------

A node writes the names of its topics in its code. This reading shows how to
change the names a node uses without editing that code. A **namespace** is a
prefix in front of a node's name and of its relative names, so the same code
runs once per robot. A **remapping rule**, ``match:=replacement``, changes a
name the node uses when it starts. The reading runs two copies of the heading
controller in two namespaces, reads the wheel odometry with a rule, combines a
namespace with two rules, and writes the same settings in a launch file. It is
a self-study reading module, with no video.

Read it after :doc:`Lecture 12 </lectures/lecture12/l12_index>`. It uses the
heading controller node and the parameters of that lecture, and the ROSbot
simulation of the :doc:`ROSbot Simulation </setup/rosbot_simulation>` page.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Put a node in a **namespace**, and tell how it changes a **relative**, an
     **absolute** and a **private** name.
   - Write a **remapping rule**, ``match:=replacement``, with
     ``--ros-args -r`` or in a launch file, to rename a topic, a node or a
     namespace, and combine rules with a namespace.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   remap_lecture
   remap_quiz
   remap_references
