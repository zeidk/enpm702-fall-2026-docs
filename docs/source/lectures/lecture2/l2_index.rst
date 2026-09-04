====================================================
L2: Introduction to C++
====================================================

Overview
--------

This lecture covers the core building blocks of the C++ language:
terminal input and output, how memory is organized into bits, bytes and
segments, variables and the five properties every variable has, the
fundamental types (integral, floating-point, boolean), the rules the
compiler uses to convert between those types, constants, scope, and
namespaces. It emphasizes the modern practices this course requires
throughout the semester: uniform initialization, ``constexpr``, and
explicit namespace qualification.

The build pipeline itself was covered in
:doc:`Lecture 1 </lectures/lecture1/l1_lecture>`; this lecture recaps it
in one table and then moves on.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Perform terminal input and output with ``std::cin`` and
     ``std::cout``, and explain what the ``<<`` and ``>>`` operators do.
   - Describe how a process is laid out in memory (text, data, BSS,
     heap, stack) and say which segment a given variable lands in.
   - Declare, initialize, and use variables following the course
     naming convention (``snake_case``) and uniform initialization.
   - Explain what happens in memory when a variable is created and read,
     and use the ``sizeof`` and ``&`` operators.
   - Recognize undefined behavior, name its common sources, and enable
     the compiler warnings that catch some of it.
   - Choose appropriately among the integral, floating-point, and
     boolean types, including signedness and size modifiers.
   - Predict the result of implicit conversions: numeric promotions,
     numeric conversions, and the usual arithmetic conversions.
   - Identify a narrowing conversion, explain why uniform initialization
     rejects it, and make it explicit with ``static_cast``.
   - Use ``const``, ``constexpr``, and literals correctly, and explain
     why macros are not an acceptable substitute.
   - Use type deduction with ``auto``, including what it does to
     ``const``.
   - Reason about local and global scope, and avoid naming collisions
     with namespaces.
   - Create type aliases and scoped enumerations (``enum class``).
   - Use the C++20 facilities that apply to this material:
     ``std::numbers`` for mathematical constants, ``std::cmp_*`` for
     safe signed/unsigned comparison, ``std::format`` for output, and
     ``using enum``.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l2_lecture
   l2_shell
   l2_exercises
   l2_quiz
   l2_references

Next Steps
----------

- In the next lecture (**Sep 15**), we will cover **L3: Pointers and
  Memory Management**:

  - Stack versus heap memory.
  - Pointers and references.
  - Dynamic allocation with ``new`` and ``delete``.
  - Memory debugging with Valgrind.

- **Pre-work:**

  - Complete the Lecture 2 :doc:`shell exercises <l2_shell>`,
    :doc:`C++ exercises <l2_exercises>`, and
    :doc:`self-check quiz <l2_quiz>`.
  - Self-study reading: **Flow Control and Operations**, due before
    Sep 15.
  - **RWA1** is posted in Week 3 and builds directly on this material.

- **Recommended reading:**

  - `cppreference: initialization <https://en.cppreference.com/w/cpp/language/initialization>`_
  - `cppreference: implicit conversions <https://en.cppreference.com/w/cpp/language/implicit_conversion>`_
  - `C++ Core Guidelines, ES: Expressions and statements <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es-expressions-and-statements>`_
