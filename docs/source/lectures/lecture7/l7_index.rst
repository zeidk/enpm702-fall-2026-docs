.. _l7_index:

==========================================
L7: Smart Pointers and Move Semantics
==========================================

Overview
--------

This lecture is about who owns an object on the heap. An **owner** keeps the object alive, and an object can have one owner or several: the last owner to let go deletes it. A raw pointer such as ``Obstacle*`` cannot say that it owns, and three bugs come from that: a leak, a double ``delete``, and a dangling read. LeakSanitizer, part of ``-fsanitize=address``, finds the leak and names the line that allocated it. The lecture then covers move semantics. A move hands what one object owns to another, so a ``std::vector`` moves 24 bytes instead of copying its elements. The value category of an expression (lvalue, xvalue or prvalue) decides whether a move may happen, ``T&&`` binds only to rvalues, and ``std::move`` is a cast that marks an object as one you may take from. With moves in place, the lecture owns heap objects with smart pointers: ``std::unique_ptr`` for one owner, ``std::shared_ptr`` for several owners that share a count, and ``std::weak_ptr`` for an observer that owns nothing and breaks a reference cycle. It ends with one table for choosing a pointer. The running example is the software of an autonomous car, the ego vehicle, on a two-lane road: its tracker owns one ``Obstacle`` for each obstacle it sees, the planner shares the obstacles near its path (the hazards), and a dashboard watches one obstacle without keeping it alive.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Say** who owns an object on the heap, and find a leak with the sanitizers.
   2. **Move** a ``std::vector`` instead of copying it, and say what is left in the source.
   3. **Name** the value category of an expression (lvalue, prvalue, xvalue) and test it with ``decltype``.
   4. **Use** rvalue references and ``std::move``, and write a function that takes a parameter it moves from.
   5. **Own** a heap object with ``std::unique_ptr``, and pass it to and return it from functions.
   6. **Share** an object with ``std::shared_ptr``, and break a reference cycle with ``std::weak_ptr``.
   7. **Choose** between ``std::unique_ptr``, ``std::shared_ptr``, ``std::weak_ptr``, and a plain pointer or reference.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 7 Contents

   l7_lecture
   l7_shell
   l7_exercises
   l7_quiz
   l7_references

Before the Next Lecture
-----------------------

The next lecture is on **Oct 27**.

- The :doc:`C++ exercise <l7_exercises>` is **graded**. Hand it in on Canvas before the next lecture.
- The :doc:`shell exercises <l7_shell>` and the :doc:`quiz <l7_quiz>` are for your own practice. They are **not** collected.
- **RWA2** is due **Fri, Oct 23**, on Canvas.

Next Steps
----------

In **Lecture 8: OOP Basics**, we cover classes, objects, encapsulation and constructors. A class can own a resource and give it back in its destructor, as ``std::unique_ptr`` does.

The :doc:`references <l7_references>` page lists the recommended reading for this lecture.
