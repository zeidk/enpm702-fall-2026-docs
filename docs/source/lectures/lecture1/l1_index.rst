====================================================
L1: Course Introduction
====================================================

Overview
--------

This lecture introduces the ENPM702 course: its structure, grading
policies, assignment progression, and coding conventions. It then
covers C++ as a language, the sequence of language standards and why
this course targets **C++20**, and the full path a program takes from
source text to a running process: preprocessor, compiler, linker,
loader, CPU. The same program is then built with CMake and inside
VSCode, and the lecture closes with an in-class verification of your
development environment.

The development environment (Ubuntu, Visual Studio Code, CMake, and
Git) and the Linux shell are covered in dedicated reading modules that
you should work through before the semester begins.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Understand the course structure, objectives, and grading policies.
   - Identify the software tools used in this course (Ubuntu, VSCode,
     ROS 2, Git, Valgrind, Doxygen) and the required toolchain versions.
   - Explain how shell and C++ exercises contribute to your
     participation grade, and apply the course AI-disclosure policy.
   - Place the major C++ standards on a timeline and explain why this
     course targets C++20.
   - Trace a program from source through the preprocessor, compiler,
     and linker to an executable, and identify which stage produced a
     given error message.
   - Build and run the same program two ways: directly with ``g++`` and
     through CMake, both from the terminal and inside VSCode.
   - Verify that your development environment is working and diagnose
     the most common toolchain failures.
   - Apply the course coding conventions, such as using ``'\n'``
     instead of ``std::endl``.
   - Know where to find the setup, Linux Shell, and VSCode and CMake
     reading modules.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l1_lecture
   l1_shell
   l1_quiz
   l1_references

Next Steps
----------

- In the next lecture (**Sep 8**), we will cover **L2: Introduction to
  C++**:

  - Variables: declaration, initialization, memory allocation.
  - Integral, floating-point, and Boolean types.
  - Type conversion and type deduction.
  - Constants, scope, and namespaces.

- **Pre-work:**

  - Finish your environment setup if it is not working yet. Email the
    instructor this week rather than next week.
  - Complete the Lecture 1 :doc:`shell exercises <l1_shell>` and
    :doc:`self-check quiz <l1_quiz>`. Lecture 1 has no C++ exercises,
    so there is nothing to submit for participation credit this week.
  - Self-study reading, if not already done: **Linux Shell**, **VSCode
    and CMake**, **Version Control**.
  - **Flow Control and Operations** is due before Sep 15.

- **Recommended reading:**

  - `cppreference: declarations <https://en.cppreference.com/w/cpp/language/declarations>`_
  - `C++ Core Guidelines, ES: Expressions and statements <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es-expressions-and-statements>`_
