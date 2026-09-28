.. _l5_index:

==========================
L5: Functions
==========================

Overview
--------

This lecture introduces functions: how to declare, define and call them, and how to split a program into header and source files that CMake builds together. It covers how arguments are passed (by value, by reference, by ``const`` reference, by pointer, with ``std::string_view`` and ``std::span``), how results come back (by value with copy elision, by reference, by pointer), overloading and default arguments, static local variables, the call stack, the ``main`` function with its command-line arguments, and documenting functions with Doxygen. The running example is a program for a planar arm with three joints: read the joint angles, clamp each one to its limit, convert it to radians, and report where the tool ends up.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   1. **Write**, declare and call functions, and split them into header and source files.
   2. **Choose** how to pass arguments and how to return results.
   3. **Overload** a function and give it default arguments.
   4. **Explain** static locals, stack frames, and the arguments of ``main``.
   5. **Document** functions with Doxygen.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Lecture 5 Contents

   l5_lecture
   l5_shell
   l5_exercises
   l5_quiz
   l5_references

Before the Next Lecture
-----------------------

The next lecture is on **Oct 6**.

- The :doc:`C++ exercises <l5_exercises>` are **graded**. Hand them in on Canvas before the next lecture.
- The :doc:`shell exercises <l5_shell>` and the :doc:`quiz <l5_quiz>` are for your own practice. They are **not** collected.
- **RWA1** is due **Oct 1**.

Next Steps
----------

In **Lecture 6: Functions, Advanced Topics**, we return several values with types you write and structured bindings, write function templates and use the class templates Lecture 4 relied on, and write lambdas, the inline functions Lecture 4 showed with the algorithms.
