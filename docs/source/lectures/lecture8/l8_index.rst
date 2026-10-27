.. _l8_index:

====================
L8: OOP Basics
====================

Overview
--------

This lecture covers the basics of object-oriented programming (OOP) in C++, around the software of a robotaxi. It opens with the program in words and as a UML class diagram of everything L8 and L9 build, and comes back to the diagram, with the part being built in purple, before each new piece. It compares the procedural and the object-oriented way to write the same program, and says when a class is not worth it. A **class** is a type you define: its data members hold an object's values, and its methods work on them. A type becomes a ``class`` when its data members must keep a rule, its **invariant**, and stays a ``struct`` when they vary independently: a ``Sensor``'s range must be at least 0, while any ``x`` and ``y`` make a ``Position``. The lecture builds ``Vehicle``, whose speed must stay from 0 to its maximum speed: ``private`` data members and ``public`` methods, a header and a source file, accessors and mutators with ``[[nodiscard]]`` and ``noexcept``, constructors and ``explicit``, and the ``this`` pointer. It ends with destructors: when one runs, and how a ``Vehicle`` that owns its sensors through ``std::unique_ptr`` needs no destructor of its own. You write ``Vehicle`` with me in five Live Coding steps, plus one block on your own, and upload it on Canvas at the end of class. The Further Reading part of the lecture page, not presented in class, holds the code each Live Coding step replaces, ``inline`` functions, ``const`` objects and ``static`` members. The :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>` page is required reading after class. Discussions in class replace the exercises of earlier lectures.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Say** when a type should be a ``class`` and when a ``struct``, from its invariant.
   2. **Write** a class with ``private`` data members and ``public`` methods, in a header and a source file.
   3. **Write** accessors and mutators that keep the invariant, with ``const``, ``[[nodiscard]]`` and ``noexcept`` where each one is true.
   4. **Construct** objects with constructors and member initializer lists, and mark a constructor ``explicit``.
   5. **Say** when an object's destructor runs.
   6. **Use** members that give back their own memory, such as ``std::unique_ptr``, so a class needs no destructor of its own.
   7. **Use** the ``this`` pointer.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 8 Contents

   l8_setup
   l8_lecture
   l8_rule_of_five
   l8_shell
   l8_quiz
   l8_references

Before Class
------------

Follow :doc:`Setup Before Class <l8_setup>`. In class you write code with me and upload it on Canvas before the end of class. That upload counts toward Participation, as complete or incomplete, and no AI is allowed. The lecture page's Upload Your Live Coding section has the rules.

Before the Next Lecture
-----------------------

There is no quiz in this lecture. The next lecture, on **Nov 3**, starts with the 5-minute quiz on the reading and **Quiz 4**, which has questions on the rule of five and the rule of zero.

- The :doc:`shell exercises <l8_shell>` and the :doc:`quiz <l8_quiz>` are for your own practice. They are **not** collected.

**Required reading, after class:**

- :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`, on this site. It is not presented in class. L8 has no C++ exercise: this reading replaces it, and Lecture 9, on Nov 3, starts with a 5-minute quiz on it.
- `C++ Core Guidelines: Classes and class hierarchies <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#s-class>`_
- `cppreference: Constructors <https://en.cppreference.com/w/cpp/language/constructor>`_

Next Steps
----------

In **Lecture 9: OOP Advanced**, we cover inheritance, polymorphism and abstract classes, and how to design classes with UML class diagrams. **RWA3** is posted.

The :doc:`references <l8_references>` page lists the recommended reading for this lecture.
