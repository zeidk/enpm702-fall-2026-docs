.. _l6_index:

==============================
L6: Functions Advanced
==============================

Overview
--------

This lecture groups values and uses them as parameters and results. It covers ``struct`` (declaring one, initializing it, member access, and how its members sit in memory with padding), ``std::pair`` and ``std::tuple``, returning several values and unpacking them with structured bindings, and returning a value that may be missing with ``std::optional``. It then writes function templates and constrains them with concepts, and moves on to callables: lambdas with their captures, passed to the standard algorithms, then ``std::function`` to store a callable and ``std::bind`` to adapt one. The running example is a fleet manager for four warehouse robots: it tracks each robot's battery, position and state, picks a robot for each new task, and sends commands through a dispatcher.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Group** values with a ``struct``, a ``std::pair``, or a ``std::tuple``, and predict a ``struct``'s size.
   2. **Return** several values, or a value that may be missing, and unpack them with structured bindings.
   3. **Write** a function template, and constrain it with a concept.
   4. **Write** lambdas with captures, and pass them to the standard algorithms.
   5. **Write** higher-order functions: pass, store, and adapt callables with ``std::function`` and ``std::bind``.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 6 Contents

   l6_lecture
   l6_shell
   l6_exercises
   l6_quiz
   l6_references

Before the Next Lecture
-----------------------

The next lecture is on **Oct 13**.

- The :doc:`C++ exercise <l6_exercises>` is **graded**: one exercise this week. Hand it in on Canvas before the next lecture.
- The :doc:`shell exercises <l6_shell>` and the :doc:`quiz <l6_quiz>` are for your own practice. They are **not** collected.
- Read the :doc:`exception handling </reading_material/exception_handling/eh_index>` reading. Exceptions are not presented in class. Two parts of this lecture show a standard type that **throws**; the reading explains what that means and how to catch one.

Next Steps
----------

In **Lecture 7: Smart Pointers**, we use ``std::unique_ptr`` and ``std::shared_ptr``: heap memory that frees itself, without Lecture 3's ``delete``.
