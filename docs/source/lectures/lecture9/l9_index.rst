.. _l9_index:

====================
L9: OOP Advanced
====================

Overview
--------

This lecture covers advanced object-oriented programming in C++, on the same robotaxi program as L8. It opens with the UML class diagram of the whole program and comes back to it, with the part being built in purple, before each new piece. A **design** comes first: requirements say what the program must do, their nouns and verbs give the classes and methods, and a **UML class diagram** draws them. The lecture then names each line of the diagram: a ``Passenger`` rides a ``Vehicle`` (association, ``std::weak_ptr``), a ``Fleet`` holds vehicles it shares (aggregation, ``std::shared_ptr``), a ``Vehicle`` owns its ``Sensor``\ s and a ``Route`` its ``Position``\ s (composition), a ``Vehicle`` uses a ``Route`` for one call (dependency), and a ``RoboTaxi`` and a ``Taxi`` are vehicles (inheritance, with ``protected``, base class initializers and construction order). **Polymorphism** follows: compile-time (redefinition, static types) and runtime (``virtual``, ``override``), slicing, ``auto`` against a pointer to the base class, and ``virtual`` destructors, measured with AddressSanitizer. The lecture ends with **abstraction**, an abstract ``Vehicle`` with a pure ``virtual`` ``drive``, concrete classes that override it, and ``final``. In class, we write ``Passenger``, ``Fleet``, ``RoboTaxi`` and ``Taxi`` together in seven Live Coding steps, and change L8's ``Vehicle``; discussions take the place of the in-class exercises of earlier lectures. The graded C++ exercise is done after class.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Turn** requirements into classes, and **read** a UML class diagram.
   2. **Tell** association, aggregation, composition and dependency apart, and **write** each one with the right member or parameter.
   3. **Derive** a class from a base class, **call** the base constructor, and **use** ``protected``.
   4. **Explain** compile-time and runtime polymorphism, and **write** ``virtual`` methods with ``override``.
   5. **Choose** between ``auto`` and a pointer to the base class.
   6. **Give** a base class a ``virtual`` destructor, and **say** what goes wrong without one.
   7. **Write** an abstract class with a pure ``virtual`` method, and concrete classes that override it.
   8. **Use** ``final`` on a class and on a method.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 9 Contents

   l9_lecture
   l9_shell
   l9_exercises
   l9_quiz
   l9_references

Before Class
------------

Follow :doc:`Setup Before Class </lectures/lecture8/l8_setup>` from Lecture 8, and run the script with the week number: ``bash ~/Downloads/enpm702_setup.sh 9``. In class you type each Live Coding step with me, in ``project/week9/live``, and you upload ``fleet.hpp``, ``fleet.cpp`` and ``main.cpp`` to the L9 Live Coding assignment on Canvas before the end of class. The upload counts toward Participation, as complete or incomplete, and no AI is allowed. The rules are in :ref:`Upload Your Live Coding <l9-upload-live-coding>`.

Class starts with **Quiz 4**, which includes questions on the Lecture 8 reading, :doc:`Rule of Five and Rule of Zero </lectures/lecture8/l8_rule_of_five>`. Read it before you come.

Before the Next Lecture
-----------------------

**RWA3** is posted today and is due on **Nov 17**.

- **Before the end of class**: upload your three Live Coding files on Canvas. If you watch the recording, upload them before Nov 10.
- The :doc:`C++ exercise <l9_exercises>` is **graded**. Hand it in on Canvas before the next lecture.
- The :doc:`shell exercises <l9_shell>` and the :doc:`quiz <l9_quiz>` are for your own practice. They are **not** collected.

**Required reading, after class:**

- `C++ Core Guidelines: Class hierarchies (OOP) <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ss-hier>`_
- `cppreference: virtual function specifier <https://en.cppreference.com/w/cpp/language/virtual>`_

Next Steps
----------

In **Lecture 10: ROS 2 Foundations** (Nov 10), we cover nodes, publishers and subscribers. A ROS 2 node is a class derived from ``rclcpp::Node``: today's inheritance. **RWA3** is due on **Nov 17**.

Before that class, check that your ROS 2 installation works.

The :doc:`references <l9_references>` page lists the recommended reading for this lecture.
