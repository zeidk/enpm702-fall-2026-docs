====================================================
Lecture
====================================================




Course Introduction
====================================================


Course Overview
---------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Operating System**

    - Ubuntu Desktop 24.04 LTS: Noble Numbat (recommended)
    - Ubuntu Desktop 22.04 LTS: Jammy Jellyfish

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Software**

    - **Visual Studio Code**, Code editor with rich extension support.
    - **ROS 2:**

      - Jazzy Jalisco (for Ubuntu 24.04)
      - Iron Irwini (for Ubuntu 22.04)

    - **Doxygen**, Code documentation generator.
    - **Version Control:**

      - Git
      - GitHub (account required)

    - **Valgrind**, Memory debugging and leak detection.
    - **CMake**, Cross-platform build system.


Online Students
^^^^^^^^^^^^^^^

.. important::

   Online students participate asynchronously. They cannot be required to
   attend in-person for exams, presentations, or activities. Online
   students have at least 48 hours after the release of a recorded lecture
   to complete quizzes and assignments.


Exercises
---------

Besides the lecture material, every lecture page includes two kinds of
hands-on practice: **Shell exercises** and **C++ exercises**. These are
*not* graded like the RWAs, instead, submitting your weekly exercise
solutions on Canvas is one of the ways you earn **participation** credit
(see the :doc:`syllabus </syllabus/syllabus>`).

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Shell Exercises
        :class-card: sd-border-info sd-shadow-sm

        Hands-on Linux shell (Bash) exercises that **begin in Lecture 1**
        and build progressively across the semester. They develop the
        terminal fluency you need for the C++ build workflow and, later,
        for ROS 2 development (``colcon``, launch files, and CLI tools).

    .. grid-item-card:: C++ Exercises
        :class-card: sd-border-info sd-shadow-sm

        Short C++ programming exercises tied to each lecture's topic.
        They **begin in Lecture 2** (Lecture 1 has no C++ exercises) and
        let you practice each new language feature by writing and running
        real code before applying it in the RWAs.

.. note::

   Work through the exercises after each lecture on your own machine.
   Experimenting with code is the fastest way to internalize the
   concepts, and submitting your solutions on Canvas counts toward
   your **participation** grade.


Course Conventions
====================================================


``'\n'`` vs ``std::endl``
-------------------------

In this course, always use ``'\n'`` to insert a newline character. Do
**not** use ``std::endl`` unless you have a specific reason to flush the
output buffer.

.. code-block:: cpp

   std::cout << "Hello, World!" << '\n';    // correct
   std::cout << "Hello, World!" << std::endl; // avoid

.. warning::

   ``std::endl`` inserts a newline **and** flushes the output buffer.
   Flushing forces the program to write all buffered output to the
   console immediately, which is significantly slower than simply
   writing a newline character. In most situations, flushing is
   unnecessary, because the buffer is automatically flushed when it is
   full, when the program ends, or when ``std::cin`` is used.

   Using ``std::endl`` in loops or high-frequency output can cause
   noticeable performance degradation. Use ``'\n'`` by default.
