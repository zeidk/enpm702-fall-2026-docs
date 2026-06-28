====================================================
L15: Robot Autonomy Architecture
====================================================

Overview
--------

This is the final lecture in the course. It is a **capstone** that ties
together everything you learned in the ROS 2 lectures. Rather than
introducing a new ROS 2 feature, it shows how nodes, topics, services,
actions, parameters, launch files, TF2, and lifecycle nodes **compose
into an autonomy architecture**, a standard way of organizing
perception, decision-making, and control. This lecture also shows
**where Artificial Intelligence and Machine Learning fit** into a robotic
system: in the decision and perception layers, behind the same ROS 2
interfaces you already use.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Describe the **Sense-Plan-Act** paradigm and the autonomy cycle.
   - Map an autonomy architecture onto ROS 2 nodes and communication patterns.
   - Identify the perception, decision, and control layers in a robotic system.
   - Explain **where AI and ML fit** in the architecture and why the decision layer's implementation is interchangeable.
   - Recognize how trained models are integrated for inference in C++ (OpenCV DNN, ONNX Runtime, LibTorch), at a conceptual level.
   - Distinguish reactive, deliberative, and hybrid architectures, and name common ROS 2 frameworks (Nav2, BehaviorTree.CPP).

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l15_lecture
   l15_exercises
   l15_quiz
   l15_references

Next Steps
----------

- This is the **final lecture** in the course. You now have all the tools
  and knowledge needed for the remaining assignments.

- The autonomy architecture in this lecture is the conceptual frame for
  the **Group Projects**: the TurtleBot3 system you build *is* a
  Sense-Plan-Act stack.

- The advanced ROS 2 capabilities that support this architecture,
  **TF2 (coordinate frames)** and **lifecycle nodes**, are covered in
  :doc:`Lecture 13 <../lecture13/l13_index>` and
  :doc:`Lecture 14 <../lecture14/l14_index>`. Review them alongside this
  lecture, especially before **GP3**.

- Work through the exercises and take the quiz to solidify your
  understanding of how the pieces fit together.
