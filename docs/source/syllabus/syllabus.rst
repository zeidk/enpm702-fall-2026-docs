Syllabus
========

.. role:: reading
.. role:: quiz
.. role:: assignment

Grade Breakdown
---------------

.. list-table::
   :header-rows: 1
   :widths: 48 16 16
   :class: compact-table

   * - Component
     - Percentage
     - Points
   * - RWAs (3) + GPs (3)
     - 70%
     - 280
   * - Quizzes (5)
     - 25%
     - 100
   * - Participation/Engagement
     - 5%
     - 20
   * - **Total**
     - **100%**
     - **400**

.. note::

   The course is graded out of **400 points** (each component is scored
   on this scale to simplify grading); final letter grades are computed
   from the percentages above. **Participation** is earned by actively
   engaging in class discussions or by submitting weekly exercise
   solutions on Canvas.


.. _course-schedule:

Course Schedule
---------------

Lectures meet on **Tuesdays**. The first lecture is **September 1, 2026**
and the last day of class is **Friday, December 11, 2026**. The
Thanksgiving recess (**Nov 25-29**) does not fall on a Tuesday, so all
Tuesday lectures meet as scheduled.

**Color key:** :reading:`reading material`; :quiz:`quizzes`;
:assignment:`assignments (RWAs and GPs) posted/due`.

.. list-table::
   :header-rows: 1
   :widths: 6 8 20 38 28
   :class: compact-table schedule-table

   * - Week
     - Date
     - Before Class
     - During Class
     - After Class
   * - Week 1
     - Sep 1
     - :reading:`Read: Linux Shell, VSCode & CMake, Version Control`
     - Course Introduction and Conventions
     - Submit Lecture 1 exercises
   * - Week 2
     - Sep 8
     -
     - Introduction to C++ (Variables, Types, Constants, Namespaces)
     - Submit Lecture 2 exercises
   * - Week 3
     - Sep 15
     - :reading:`Read: Flow Control & Operations`
     - Pointers and Memory Management (Stack, Heap, References)
     - | Submit Lecture 3 exercises
       | :assignment:`RWA1 posted`
   * - Week 4
     - Sep 22
     -
     - | STL Containers (Strings, Arrays, Vectors, Iterators)
       | :quiz:`Quiz 1`
     - Submit Lecture 4 exercises
   * - Week 5
     - Sep 29
     -
     - Functions, Basics (Declarations, Parameters, Overloading, Recursion)
     - | Submit Lecture 5 exercises
       | :assignment:`RWA1 due, RWA2 posted`
   * - Week 6
     - Oct 6
     -
     - | Functions, Advanced (Templates, Lambdas, Functors, ``std::function``)
       | :quiz:`Quiz 2`
     - Submit Lecture 6 exercises
   * - Week 7
     - Oct 13
     - :reading:`Read: Exception Handling`
     - Smart Pointers and Move Semantics (``unique_ptr``, ``shared_ptr``, ``weak_ptr``)
     - | Submit Lecture 7 exercises
       | :assignment:`RWA2 due`
   * - Week 8
     - Oct 20
     -
     - | OOP Basics (Classes, Objects, Encapsulation, Constructors)
       | :quiz:`Quiz 3`
     - Submit Lecture 8 exercises
   * - Week 9
     - Oct 27
     -
     - OOP Advanced (Inheritance, Polymorphism, Abstraction)
     - | Submit Lecture 9 exercises
       | :assignment:`RWA3 posted`
   * - Week 10
     - Nov 3
     -
     - | ROS 2, Foundations (Publisher, Subscriber, Custom Interfaces)
       | :quiz:`Quiz 4`
     - Submit Lecture 10 exercises
   * - Week 11
     - Nov 10
     -
     - ROS 2, Configuration and Orchestration (Parameters, Launch Files, Executors)
     - | Submit Lecture 11 exercises
       | :assignment:`RWA3 due, GP1 posted`
   * - Week 12
     - Nov 17
     -
     - | ROS 2, Communication Patterns (Services, Actions)
       | :quiz:`Quiz 5`
     - | Submit Lecture 12 exercises
       | :assignment:`GP1 due, GP2 posted`
   * - Week 13
     - Nov 24
     -
     - ROS 2, Coordinate Frames and Transforms
     - Submit Lecture 13 exercises
   * - Week 14
     - Dec 1
     -
     - ROS 2, Lifecycle Nodes
     - | Submit Lecture 14 exercises
       | :assignment:`GP2 due, GP3 posted`
   * - Week 15
     - Dec 8
     -
     - ROS 2, Robot Autonomy Architecture (Sense-Plan-Act, where AI/ML fits)
     - | Submit Lecture 15 exercises
       | :assignment:`GP3 due (Dec 11)`

.. note::

   This is a tentative schedule, and subject to change as necessary.
   Monitor ELMS-Canvas for current deadlines.


Real-World Applications (RWAs)
------------------------------

The three RWAs are **cumulative** individual assignments that progressively
build a C++ application using robotics-themed use cases. Each RWA refactors
and extends the previous one, demonstrating why each new C++ feature
improves the codebase:

.. list-table::
   :header-rows: 1
   :widths: 36 12 12 12 10
   :class: compact-table

   * - Assignment
     - Posted
     - Due
     - Duration
     - Points
   * - RWA1: C++ Fundamentals (Variables, Types, Pointers)
     - Sep 15
     - Sep 29
     - 2 weeks
     - 44
   * - RWA2: STL Containers and Functions
     - Sep 29
     - Oct 13
     - 2 weeks
     - 48
   * - RWA3: Smart Pointers and OOP
     - Oct 27
     - Nov 10
     - 2 weeks
     - 48


Group Projects (GPs)
--------------------

The three GPs are **cumulative** team-based projects that progressively
build a ROS 2 application with a mobile robot in Gazebo. Each GP extends
the previous deliverable:

.. list-table::
   :header-rows: 1
   :widths: 36 12 12 12 10
   :class: compact-table

   * - Project
     - Posted
     - Due
     - Duration
     - Points
   * - GP1: ROS 2 Pub/Sub with Gazebo
     - Nov 10
     - Nov 17
     - 1 week
     - 44
   * - GP2: Services, Actions, and Robot Inheritance
     - Nov 17
     - Dec 1
     - 2 weeks (incl. Thanksgiving recess)
     - 48
   * - GP3: Autonomy, Frames, Lifecycle, and a Decision Layer
     - Dec 1
     - Dec 11
     - ~1.5 weeks
     - 48

.. tip::

   Start assignments early. RWAs and GPs are cumulative, so a strong
   foundation in each deliverable makes the next one easier.


Quizzes
-------

There are five short quizzes, each worth **20 points**. They are
comprehension checks given in class on the dates below:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 12
   :class: compact-table

   * - Quiz
     - Week
     - Date
     - Points
   * - Quiz 1
     - Week 4
     - Sep 22
     - 20
   * - Quiz 2
     - Week 6
     - Oct 6
     - 20
   * - Quiz 3
     - Week 8
     - Oct 20
     - 20
   * - Quiz 4
     - Week 10
     - Nov 3
     - 20
   * - Quiz 5
     - Week 12
     - Nov 17
     - 20


Reading Material
----------------

The following topics are provided as self-study reading modules.
Students are expected to work through these outside of class by the recommended
deadline:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30
   :class: compact-table

   * - Topic
     - Description
     - When to Complete
   * - Linux Shell
     - The Linux command-line shell: shell types, configuration files, aliases, and functions.
     - **Before the semester starts**
   * - VSCode and CMake
     - VSCode installation and interface, the ``.vscode`` folder, recommended extensions, the Command Palette, and the ``CMakeLists.txt`` build configuration.
     - **Before the semester starts**
   * - Version Control (Git and GitHub)
     - Distributed version control, branching, merging, pull requests, and the fork workflow.
     - **Before the semester starts**
   * - Flow Control and Operations
     - Conditionals, loops, and operators.
     - **Before Sep 15** (before RWA1 is posted)
   * - Exception Handling
     - Exception handling with ``try``, ``catch``, ``throw``, standard and custom exception classes, and RAII.
     - **Before Oct 13** (before Smart Pointers)
