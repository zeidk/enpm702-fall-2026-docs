====================================================
Services and Actions
====================================================

Overview
--------

Topics, which Lecture 10 teaches, carry a stream of messages. Two jobs
fit a topic badly: asking one question and getting one answer, and
running a task that takes seconds. ROS 2 has a **service** for the first
and an **action** for the second. This reading material builds one
example of each with the robotaxi: a fare service and a drive action, a
server and a client for each, in C++. It is extra material, beyond what
the lectures and the course projects need. It is a self-study reading
module, with no video.

Read it after :doc:`Lecture 11 </lectures/lecture11/l11_index>`. It uses
the topics of Lecture 10, the interface packages of Lecture 11, and the
way a node is written in both.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Choose between a **topic**, a **service** and an **action** for a
     job, and say why.
   - Define a service in a ``.srv`` file and an action in an ``.action``
     file, and build them in an interface package.
   - Write a **service server** with ``create_service`` and a **service
     client** with ``create_client`` and ``async_send_request``.
   - Write an **action server** with its three callbacks and an
     ``execute`` method that sends feedback, and an **action client** with
     its three callbacks.
   - **Cancel** a goal from the client when it takes longer than a
     **timeout** counted on the node clock.
   - Call and inspect a service and an action from the terminal with
     ``ros2 service`` and ``ros2 action``.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   sa_lecture
   sa_exercises
   sa_quiz
   sa_references
