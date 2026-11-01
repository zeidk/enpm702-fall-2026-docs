.. _l9_index:

====================
L9: OOP Advanced
====================

Overview
--------

This lecture covers advanced object-oriented programming in C++, on the ride service program. A warm-up asks you to improve a ``Vehicle`` class with what you already know. The lecture then opens with the UML class diagram of the whole program and comes back to it, with the part being built in purple, before each new piece. A **design** comes first: requirements say what the program must do, their nouns and verbs give the classes and methods, and a **UML class diagram** draws them. Every class of the program is in the namespace ``fleet``. The lecture then names each line of the diagram: a ``Passenger`` rides a ``Vehicle`` (association, ``std::weak_ptr``), a ``Fleet`` holds vehicles it shares (aggregation, ``std::shared_ptr``), a ``Vehicle`` owns its ``Sensor``\ s and a ``Route`` its ``Position``\ s (composition), a ``Vehicle`` uses a ``Route`` for one call (dependency), and a ``RoboTaxi`` and a ``Taxi`` are vehicles (inheritance, with ``protected``, base class initializers and construction order). **Polymorphism** follows: compile-time (redefinition, static types) and runtime (``virtual``, ``override``), slicing, and ``virtual`` destructors, measured with AddressSanitizer. The lecture ends with **abstraction**, an abstract ``Vehicle`` with a pure ``virtual`` ``drive``, concrete classes that override it, and ``final``. In class, you write ``Passenger``, ``Fleet``, ``RoboTaxi`` and ``Taxi`` and change the ``Vehicle`` you already wrote in seven Live Coding steps: Step 1 with me, Steps 2 to 5 on your own; Steps 6 and 7 are homework, not collected. The other discussions, with their answers, and a summary of each part are in the Further Reading part of the lecture page.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Turn** requirements into classes, and **read** a UML class diagram.
   2. **Put** classes in a namespace.
   3. **Write** association, aggregation, composition and dependency.
   4. **Derive** a class from a base class, and **call** the base constructor.
   5. **Write** ``virtual`` methods with ``override``, and a ``virtual`` destructor.
   6. **Write** an abstract class, and **use** ``final``.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 9 Contents

   l9_lecture
   l9_requirements
   l9_design
   l9_operators
   l9_shell
   l9_quiz
   l9_references

Before Class
------------

Follow :doc:`Setup Before Class </lectures/lecture8/l8_setup>`, and run the script with the week number: ``bash ~/Downloads/enpm702_setup.sh 9``. In class you type Step 1 with me, in ``project/week9/live``, and write Steps 2 to 5 on your own; Steps 6 and 7 are homework, not collected. You upload every file of ``live/include`` and ``live/src`` to the L9 Live Coding assignment on Canvas before the end of class. The upload counts toward Participation, as complete or incomplete, and no AI is allowed. The rules are in :ref:`Upload Your Live Coding <l9-upload-live-coding>`.

Class starts with **Quiz 4**, which includes questions on the reading :doc:`Rule of Five and Rule of Zero </lectures/lecture8/l8_rule_of_five>`. Read it before you come.

Before the Next Lecture
-----------------------

**RWA3** is posted today and is due on **Nov 17**.

- **Before the end of class**: upload every file of ``live/include`` and ``live/src`` on Canvas. If you watch the recording, upload them before Nov 10. The Live Coding is this week's exercise: L9 has no C++ exercise on this site. Steps 6 and 7 are homework, not collected.
- The :doc:`shell exercises <l9_shell>` and the :doc:`quiz <l9_quiz>` are for your own practice. They are **not** collected.

**Required reading, after class:**

- :doc:`Operator Overloading <l9_operators>`: ``operator<<`` for ``Position``, and ``operator<`` and ``operator>`` for ``Route``, with the program ``week9_operators``.
- `C++ Core Guidelines: Class hierarchies (OOP) <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ss-hier>`_
- `cppreference: virtual function specifier <https://en.cppreference.com/w/cpp/language/virtual>`_

Next Steps
----------

In **Lecture 10: ROS 2 Foundations** (Nov 10), we cover nodes, publishers and subscribers. A ROS 2 node is a class derived from ``rclcpp::Node``: today's inheritance. **RWA3** is due on **Nov 17**.

Before that class, check that your ROS 2 installation works.

The :doc:`references <l9_references>` page lists the recommended reading for this lecture.
