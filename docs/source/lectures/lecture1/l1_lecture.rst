====================================================
Lecture
====================================================

.. admonition:: Disclaimer
   :class: caution

   I teach this course solely in my capacity as a lecturer at the
   University of Maryland.

   - I do **not** represent NIST in this course.
   - Opinions, findings, and recommendations expressed here are my own
     and do not necessarily reflect the views of NIST or the U.S.
     Department of Commerce.
   - Nothing stated in this course should be interpreted as an official
     NIST position, policy, or endorsement.
   - Course content, assignments, and grading are governed by UMD
     policy only.


Syllabus
====================================================

The full syllabus is posted on ELMS-Canvas. This page covers the parts
that change how you work week to week. See also the course
:doc:`syllabus </syllabus/syllabus>` page.


Course Overview
----------------------------------------------------

Modern C++ for robotics, from language fundamentals to complete systems
with ROS 2 and Gazebo.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Part 1: C++ Foundations (Weeks 1 to 9)
        :class-card: sd-border-info sd-shadow-sm

        - Types, pointers, memory management, STL containers
        - Functions, templates, lambdas, smart pointers
        - Object-oriented programming: classes, inheritance,
          polymorphism
        - Practiced through cumulative **Real-World Application (RWA)**
          assignments

    .. grid-item-card:: Part 2: ROS 2 and Gazebo (Weeks 10 to 15)
        :class-card: sd-border-info sd-shadow-sm

        - Publishers, subscribers, custom interfaces, parameters,
          launch files
        - Services, actions, coordinate frames (TF2), lifecycle nodes
        - Cumulative **Group Projects (GPs)**: a multi-node system
          driving a mobile robot in simulation


Learning Outcomes
----------------------------------------------------

After successfully completing this course, students will be able to:

#. Write correct and efficient C++ programs using variables, types,
   constants, namespaces, and modern initialization (C++17 and beyond).
#. Manage memory safely with pointers, references, smart pointers
   (``unique_ptr``, ``shared_ptr``, ``weak_ptr``), and RAII.
#. Use the STL (strings, arrays, vectors, iterators) and write reusable
   code with function templates, lambdas, and ``std::function``.
#. Design object-oriented systems using classes, encapsulation,
   inheritance, polymorphism, and abstract interfaces.
#. Develop ROS 2 applications using publishers, subscribers, services,
   actions, custom interfaces, parameters, launch files, and executors.
#. Build and simulate robotic systems in Gazebo, including coordinate
   frame management (TF2) and lifecycle node orchestration.


Operating System and Software
----------------------------------------------------

Operating System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Ubuntu Desktop 24.04 LTS: Noble Numbat (recommended).
- Or Ubuntu Desktop 22.04 LTS: Jammy Jellyfish.

Software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Visual Studio Code, plus the recommended extensions.
- ROS 2:

  - Jazzy Jalisco (for Ubuntu 24.04).
  - Iron Irwini (for Ubuntu 22.04).

- Code documentation: Doxygen.
- Version control: Git, and a GitHub account.
- Valgrind.


Logistics
----------------------------------------------------

.. list-table:: Course meeting details and instructor contact.
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Item
     - Detail
   * - Credits
     - 3
   * - Dates
     - Sep 1 to Dec 8, 2026
   * - Time
     - Tuesdays, 7:00 to 9:40 pm
   * - Room
     - JMP 2217
   * - Instructor
     - Zeid Kootbally
   * - Email
     - ``zeidk@umd.edu``
   * - Office hours
     - Fridays, 6 to 7 pm, and by appointment

Where Things Live
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **ELMS-Canvas**: announcements, grades, submissions, team
  assignments, quiz delivery.
- `ReadTheDocs <https://enpm702-fall-2026-docs.readthedocs.io/en/latest/>`_:
  lecture notes, weekly exercises, setup guides, self-study reading,
  glossary.

Email Expectations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Replies within 24 hours where possible, most reliably Monday,
  Wednesday, and Friday, 8 to 10 am EST.
- Use it for academic and personal concerns, not for due dates and
  point values already in the syllabus.

.. important::

   **Enable your ELMS notifications.** Changes to assignments and due
   dates are announced there, and checking is your responsibility.


Course Structure
----------------------------------------------------

The Weekly Cycle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every lecture has a companion page in this documentation.

- **Lecture notes and references**: what was covered, in written form.
- **C++ exercises**: **graded**. Submitting them is one of the two
  routes to participation credit.
- **Shell exercises**: **not graded**, but recommended. The terminal is
  where you will spend the second half of this course.
- **Self-check quiz**: a way to find the gaps before a graded quiz
  does.

How to Use the Exercises
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Attempt them in the days right after class, while the material is
  fresh.
- Bring anything that does not work to the following week.
- Only the C++ exercises need to be submitted, and only before the
  start of the following lecture.

Expected Workload
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Roughly 2 to 4 hours per week outside class, more in weeks an
  assignment is due.
- That estimate includes environment problems. Toolchain trouble is
  normal in systems programming and always takes longer than expected.


Self-Study Material
----------------------------------------------------

Some material is assigned rather than lectured, because it is better
learned by doing than by watching. All of it is in the
:doc:`Reading Material </reading_material/index>` section.

.. list-table:: Self-study topics and the deadline by which each must be completed.
   :widths: 65 35
   :header-rows: 1
   :class: compact-table

   * - Topic
     - Complete by
   * - Linux shell; VSCode and CMake; version control
     - Before Sep 1
   * - Flow control and operations
     - Before Sep 15
   * - Exception handling
     - Before Oct 13

.. warning::

   **Environment setup is not optional preparation**: it is the first
   thing the course depends on. Follow the :doc:`Setup </setup/setup>`
   section before the first class and contact me if anything does not
   work.


Required Resources
----------------------------------------------------

.. list-table:: Required software and the standard targeted by all course code.
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Item
     - Requirement
   * - OS
     - Ubuntu 24.04 LTS
   * - Compiler
     - GCC 13 or newer
   * - Standard
     - C++20
   * - Build
     - CMake
   * - Debugging
     - ``gdb``, Valgrind
   * - Docs
     - Doxygen
   * - Version control
     - Git, GitHub account
   * - Editor
     - VSCode plus recommended extensions
   * - Robotics
     - ROS 2 Jazzy, Gazebo Harmonic

Hardware
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- 8 GB RAM minimum.
- Two or more CPU cores.
- 50 GB free disk space.

Install Advice
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Native or dual-boot is strongly recommended.
- A VM works for the first half, but Gazebo in the second half is
  graphics-intensive and will suffer.
- ROS 2 and Gazebo are required from Week 10, but install them now so
  problems surface early.

Free References
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `cppreference.com <https://en.cppreference.com/w/>`_
- `C++ Core Guidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_
- `docs.ros.org/en/jazzy <https://docs.ros.org/en/jazzy/>`_

.. note::

   **Total cost of required materials: $0.00.** There is no textbook
   and nothing to buy. Every tool is free and installed from the Ubuntu
   archive.


Assessments
----------------------------------------------------

.. list-table:: Course components and their weight in the final grade.
   :widths: 50 25 25
   :header-rows: 1
   :class: compact-table

   * - Component
     - Pts
     - Weight
   * - RWA1 to RWA3
     - 140
     - 35%
   * - GP1 to GP3
     - 140
     - 35%
   * - Quizzes (5)
     - 100
     - 25%
   * - Participation
     - 20
     - 5%
   * - **Total**
     - **400**
     - **100%**

Two Phases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Weeks 1 to 9**: individual work in C++, assessed through three RWAs
  and five quizzes.
- **Weeks 10 to 15**: teamwork in ROS 2, assessed through three Group
  Projects.

Both sequences are **cumulative**. Each assignment extends the code
written for the previous one, so a weak RWA1 is not a closed chapter,
it is the starting point for RWA2.

.. note::

   **No final exam.** GP3 is the capstone assessment.


Assignment Milestones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Two cumulative chains: one individual in C++, one in teams in ROS 2.

.. list-table:: Real-World Applications and Group Projects with content, dates, and points.
   :widths: 10 40 16 16 8
   :header-rows: 1
   :class: compact-table

   * - Item
     - Content
     - Posted
     - Due
     - Pts
   * - RWA1
     - C++ fundamentals
     - Sep 15
     - Sep 29
     - 44
   * - RWA2
     - STL containers and functions
     - Sep 29
     - Oct 13
     - 48
   * - RWA3
     - Smart pointers and object-oriented design
     - Oct 27
     - Nov 10
     - 48
   * - GP1
     - Publishers, subscribers, simulation
     - Nov 10
     - Nov 17
     - 44
   * - GP2
     - Services, actions, robot class hierarchies
     - Nov 17
     - Dec 1
     - 48
   * - GP3
     - Coordinate frames, lifecycle nodes, autonomy layer
     - Dec 1
     - Dec 11
     - 48

- **RWAs are individual.** Discussing concepts with classmates is fine;
  submitted code must be your own.
- **Group Projects are collaborative.** Teams are assigned on
  ELMS-Canvas, and each member is responsible for understanding the
  whole submission, not only the part they wrote.


Quizzes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Quiz dates. Each quiz is worth 20 points.
   :widths: 34 33 33
   :header-rows: 1
   :class: compact-table

   * - Quiz
     - Week
     - Date
   * - Quiz 1
     - 4
     - Sep 22
   * - Quiz 2
     - 6
     - Oct 6
   * - Quiz 3
     - 8
     - Oct 20
   * - Quiz 4
     - 10
     - Nov 3
   * - Quiz 5
     - 12
     - Nov 17

- They check that concepts are absorbed before the next assignment
  depends on them.
- Short, and not designed to be tricky.
- No AI assistance, and no makeups.


Participation and Engagement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

20 points, earned week by week rather than as a single total.

- **Two equivalent routes**, credited each week: engage in class
  discussion, **or** submit that week's exercise solutions on
  ELMS-Canvas.
- The exercise route exists deliberately, so that students for whom
  speaking up in a large lecture is not the best way to learn are not
  disadvantaged.
- **Score**: :math:`20 \times (\text{weeks credited} / 15)`, about 1.33
  points per week.
- Solutions count only when submitted **before the start of the
  following lecture**. Week 15 solutions are due December 11.

.. warning::

   **A bulk upload scores zero**, regardless of how many weeks it
   covers or how good the work is. The point of this component is
   continuous practice, and a late batch does not serve that purpose.


Grading and Policies
----------------------------------------------------

.. list-table:: Letter grades assigned from the percentage of total points earned.
   :widths: 12 13 12 13 12 13 12 13
   :header-rows: 1
   :class: compact-table

   * - Grade
     - Cutoff
     - Grade
     - Cutoff
     - Grade
     - Cutoff
     - Grade
     - Cutoff
   * - A+
     - 97.00%
     - B+
     - 87.00%
     - C+
     - 77.00%
     - D+
     - 67.00%
   * - A
     - 94.00%
     - B
     - 84.00%
     - C
     - 74.00%
     - D
     - 64.00%
   * - A-
     - 90.00%
     - B-
     - 80.00%
     - C-
     - 70.00%
     - D-
     - 60.00%

F is anything below 60.00%.

Late Work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- RWAs and Group Projects: accepted up to **48 hours** late with a
  **20% penalty**, not accepted after that.
- Quizzes and participation cannot be made up.
- Extensions for documented excused absences under University policy.
- Contact me **before** a deadline, not after.

Regrades
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Submit in writing within **one week** of receiving the grade.
- Errors are corrected immediately.
- Questions about how something was scored go to me by email.

.. warning::

   **Cutoffs are applied consistently to every student**: 89.99 is not
   90.00. Exceptions are not made for some and not others.


Academic Integrity and AI
----------------------------------------------------

.. list-table:: Resources permitted for each assessment type.
   :widths: 28 12 12 12 12 12 12
   :header-rows: 1
   :class: compact-table

   * - Assessment
     - Open notes
     - Use book
     - Learn online
     - Gather with AI
     - Ask friends
     - Work in groups
   * - Real-World Applications
     - Yes
     - Yes
     - Yes
     - Yes
     - No
     - No
   * - Quizzes
     - Yes
     - Yes
     - Yes
     - No
     - No
     - No
   * - Group Projects
     - Yes
     - Yes
     - Yes
     - Yes
     - Yes
     - Yes

- Some assignments are collected through **Turnitin** on ELMS.
- Course assistance sites such as CourseHero are **not** permitted
  sources.
- Every assignment carries the signed honor pledge.
- If you are ever unclear about the acceptable level of collaboration,
  ask before submitting.


AI Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generative AI tools (TerpAI, ChatGPT, Claude, Gemini, GitHub Copilot,
and similar) are part of professional robotics practice, and this
course treats them that way.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Permitted, With Disclosure
        :class-card: sd-border-success sd-shadow-sm

        On RWAs, Group Projects, and weekly exercises:

        - Explaining concepts
        - Interpreting compiler and linker errors
        - Reviewing code you have **already written**
        - Suggesting debugging strategies
        - Generating small illustrative examples

        +++

        Disclose at the top of the submission: name the tool, describe
        how it was used. Two or three sentences are enough.

    .. grid-item-card:: Not Permitted
        :class-card: sd-border-danger sd-shadow-sm

        - AI tools during quizzes
        - Submitting AI-generated code you cannot read, explain, and
          modify

The standard applied:

- You are responsible for every line submitted.
- I may ask, in class or office hours, for a walkthrough of any part:
  why it works, what would break it, what would be changed.
- Work that cannot be explained does not count, regardless of whether
  it compiles.
- This is the same standard a future employer will apply.

.. important::

   **Disclosure carries no penalty. Undisclosed use is a violation of
   the Code of Academic Integrity.**

.. warning::

   **These tools skew old.** They are strongest on the patterns most
   common on the public internet, so expect ROS 1 idioms, deprecated
   ``rclcpp`` APIs, and pre-C++11 memory management. Verify against the
   course documentation and the ROS 2 Jazzy documentation before
   relying on anything. Catching a plausible wrong answer is itself a
   skill this course is trying to build.


Schedule
----------------------------------------------------

Each assignment builds on the previous one, ending in a working
autonomous robot in simulation.

- **RWA1** (Weeks 3 to 5): C++ fundamentals. Variables, types,
  pointers, memory.
- **RWA2** (Weeks 5 to 7): STL containers and functions added to the
  RWA1 code.
- **RWA3** (Weeks 9 to 11): smart pointers and object-oriented design
  added to the RWA2 code.
- **GP1** (Weeks 11 to 12): the design moves into ROS 2 with
  publishers, subscribers, and Gazebo.
- **GP2** (Weeks 12 to 14): services, actions, and robot class
  hierarchies added to GP1.
- **GP3** (Weeks 14 to 15): coordinate frames, lifecycle nodes, and an
  autonomy decision layer added to GP2.

.. note::

   **The second half depends on the first throughout.** No topic is
   taught for its own sake.

.. list-table:: Weekly topics, quizzes, and assignment deadlines for the semester.
   :widths: 12 48 10 30
   :header-rows: 1
   :class: compact-table

   * - Wk
     - Topic
     - Quiz
     - Deliverable
   * - 1 (Sep 1)
     - L1: Course introduction and conventions
     -
     -
   * - 2 (Sep 8)
     - L2: Introduction to C++ (variables, types, namespaces)
     -
     -
   * - 3 (Sep 15)
     - L3: Pointers and memory (stack, heap, references)
     -
     - RWA1 posted
   * - 4 (Sep 22)
     - L4: STL containers (strings, arrays, vectors, iterators)
     - Quiz 1
     -
   * - 5 (Sep 29)
     - L5: Functions, basics (overloading, recursion)
     -
     - RWA1 due, RWA2 posted
   * - 6 (Oct 6)
     - L6: Functions, advanced (templates, lambdas, functors)
     - Quiz 2
     -
   * - 7 (Oct 13)
     - L7: Smart pointers and move semantics
     -
     - RWA2 due
   * - 8 (Oct 20)
     - L8: OOP basics (classes, encapsulation, constructors)
     - Quiz 3
     -
   * - 9 (Oct 27)
     - L9: OOP advanced (inheritance, polymorphism, abstraction)
     -
     - RWA3 posted
   * - 10 (Nov 3)
     - L10: ROS 2 foundations (nodes, publishers, subscribers)
     - Quiz 4
     -
   * - 11 (Nov 10)
     - L11: ROS 2 configuration (parameters, launch, executors)
     -
     - RWA3 due, GP1 posted
   * - 12 (Nov 17)
     - L12: ROS 2 communication (services, actions)
     - Quiz 5
     - GP1 due, GP2 posted
   * - 13 (Nov 24)
     - L13: ROS 2 coordinate frames and transforms
     -
     -
   * - 14 (Dec 1)
     - L14: ROS 2 lifecycle nodes
     -
     - GP2 due, GP3 posted
   * - 15 (Dec 8)
     - L15: Robot autonomy architecture (sense-plan-act)
     -
     - GP3 due Fri, Dec 11

Lecture exercises are due every week. Self-study reading is completed
before Sep 1, Sep 15, and Oct 13.


Succeeding in This Course
----------------------------------------------------

Tips for Success
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Participate.** Articulating an idea is how you find out whether you
  actually have it.
- **Manage your time.** Block your schedule, including extra time for
  technology problems.
- **Log in regularly.** Several times a week, and more often when group
  submissions are due.
- **Do not fall behind.** Each week builds on the previous one.
- **Use ELMS notifications.** Set announcements to instant or daily.
- **Ask for help.** IT Support for technology, me and your classmates
  for concepts.

Support and Accommodations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **ADS**: 301-314-7682, adsfrontdesk@umd.edu. ADS cannot assist
  retroactively, so request accommodations early.
- **Names and pronouns**: tell me how you want to be referred to.
  Identity is self-identified, never presumed.
- **Other resources**: Counseling Center, Writing Center, Student
  Academic Support Services, Division of Student Affairs, Veteran
  Student Life.
- **Mandatory reporting**: as a Responsible University Employee I must
  report disclosures of sexual assault, harassment, interpersonal
  violence, and stalking to the Title IX Coordinator. Confidential
  resources: CARE to Stop Violence (301-741-3442), Counseling Center
  (301-314-7651).

.. note::

   **Recording** of class sessions requires advance permission.
   Maryland is an all-party consent state.


Online Students
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. important::

   Online students participate asynchronously. They cannot be required to
   attend in-person for exams, presentations, or activities. Online
   students have at least 48 hours after the release of a recorded lecture
   to complete quizzes and assignments.


Exercises
----------------------------------------------------

Besides the lecture material, every lecture page includes two kinds of
hands-on practice: **Shell exercises** and **C++ exercises**. The C++
exercises are **graded**, and submitting them on Canvas before the start
of the following lecture is one of the two routes to **participation**
credit (see the :doc:`syllabus </syllabus/syllabus>`). The shell
exercises are **not graded**, but they are strongly recommended.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Shell Exercises
        :class-card: sd-border-info sd-shadow-sm

        Hands-on Linux shell (Bash) exercises that **begin in Lecture 1**
        and build progressively across the semester. They develop the
        terminal fluency you need for the C++ build workflow and, later,
        for ROS 2 development (``colcon``, launch files, and CLI tools).
        They are **not graded**, but they are strongly recommended.

    .. grid-item-card:: C++ Exercises
        :class-card: sd-border-info sd-shadow-sm

        Short C++ programming exercises tied to each lecture's topic.
        They **begin in Lecture 2** (Lecture 1 has no C++ exercises) and
        let you practice each new language feature by writing and running
        real code before applying it in the RWAs. They are **graded**,
        and submitting them is one of the two routes to participation
        credit.

.. note::

   Work through the exercises after each lecture on your own machine.
   Experimenting with code is the fastest way to internalize the
   concepts, and submitting your C++ solutions on Canvas counts toward
   your **participation** grade.


C++ Overview
====================================================

C++ is a **statically typed**, **compiled**, and **multi-paradigm**
programming language. Developed by Bjarne Stroustrup at Bell Labs
starting in 1979 as an enhancement to the C programming language, C++
provides low-level control over system resources while offering
high-level programming abstractions through features such as classes,
templates, and the Standard Template Library.

Authoritative and Secondary Sources
----------------------------------------------------

- The C++ standard is the sole authoritative source for C++
  specifications. Everything else, including the reputable sites below,
  is secondary. Secondary sources are generally accurate and highly
  useful, but they lack the definitive authority of the standard
  itself.
- `N4868 <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4868.pdf>`_:
  the final working draft of C++20, free from the ISO C++ committee.
  The published ISO document is paid, but the draft is what people cite
  in practice and is what this course refers to.
- `cppreference.com <https://en.cppreference.com/w/>`_: an extensive
  reference for C++ and its standard library, covering syntax,
  functions, and the standards themselves.
- `cplusplus.com <https://cplusplus.com/>`_: tutorials, references, and
  examples, aimed at beginners and intermediate learners.

.. note::

   **Course code targets C++20** and is compiled with GCC 13 or newer.


Standards
----------------------------------------------------

C++ is revised on a three-year cycle. Every release is a distinct
language version, and code written for one is not automatically valid
or idiomatic in another.

.. figure:: /_static/images/l1/cpp_timeline.png
   :align: center
   :alt: Timeline of C++ language standards from the language's origins through the most recent release.

   Timeline of C++ language standards. C++20 is the course target.


What Each Standard Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The releases below are the ones that matter for the code you will write
in this course.

.. list-table:: Language standards and the features from each that this course relies on.
   :widths: 15 55 30
   :header-rows: 1
   :class: compact-table

   * - Standard
     - Additions relevant to this course
     - Where you meet it
   * - C++11
     - Uniform initialization, ``auto``, range-based ``for``, lambdas,
       ``nullptr``, move semantics, smart pointers
     - Lectures 2, 6, 7
   * - C++14
     - Generic lambdas, ``std::make_unique``
     - Lectures 6, 7
   * - C++17
     - Structured bindings, ``std::optional``, initializers in ``if``
     - Lectures 4, 5
   * - C++20
     - Concepts, ranges, three-way comparison, designated initializers
     - Lectures 6, 9
   * - C++23
     - ``std::expected``, ``std::print``, deducing ``this``
     - Not used in this course

.. note::

   Most of what people call **modern C++** arrived in C++11. The later
   standards refine it rather than replace it. If you find a tutorial
   written before 2011, close it.


Why C++20 in This Course
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C++17, C++20, and C++23 were all plausible choices. C++20 wins on three
counts.

- **It is the newest standard the required toolchain fully supports.**
  GCC 13 implements C++20. Its C++23 support is partial, so choosing
  C++23 would mean checking feature by feature whether your compiler
  has it.
- **It costs nothing in the second half.** ROS 2 Jazzy requires C++17
  as a floor, and C++20 is compatible with that floor. Nothing you
  learn in Weeks 1 to 9 has to be unlearned in Weeks 10 to 15.
- **It is where professional code is.** Teaching C++17 would teach a
  version the field has already moved past. The habits you build here
  should be the ones you carry to work.

How You Set It
""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: bash

   g++ -std=c++20 -Wall -Wextra main.cpp -o main

- The standard is a **compiler flag, not a property of the file**.
  Omitting it means silently compiling against whatever your compiler
  defaults to.
- ``-Wall -Wextra`` turn on the warnings that catch the mistakes
  beginners actually make. Treat a warning as an error you have not hit
  yet.

.. seealso::

   :doc:`Compiler Warning Flags
   </reading_material/compiler_warnings/cw_index>` covers what
   ``-Wall``, ``-Wextra``, and ``-Wpedantic`` each enable, the warnings
   they catch most often in beginner code, and when to add ``-Wshadow``
   or ``-Werror``.

.. warning::

   **ROS 2 Jazzy packages do not default to C++20.** Starting in Week
   10 you will set the standard in ``CMakeLists.txt`` for every package
   rather than relying on the default.


Why C++ for Robotics
----------------------------------------------------

Hardware Interfacing Capabilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a compiled language, C++ offers robust mechanisms for low-level
hardware interaction.

- **Direct memory access**: through pointers, allowing precise
  manipulation of memory addresses.
- **Memory-mapped I/O**: reading from and writing to hardware registers
  mapped into memory space.
- **Inline assembly**: embedding assembly snippets for highly optimized
  or specific CPU operations.
- **System calls and APIs**: interfacing with operating system kernels
  and hardware-specific APIs for device driver communication.
- **Specialized libraries**: low-level and platform-specific libraries
  for peripherals and hardware components.

.. note::

   There is a second reason, specific to this program: the ROS 2 client
   library ``rclcpp``, the perception and planning stacks you will read
   later, and most production robotics code are written in C++. Fluency
   here is what makes that code something you can change rather than
   something you work around.


A Note for Students Arriving from Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is no prerequisite for this course and no prior C++ is assumed.
If your background is Python, the first few weeks are more likely to
feel **unfamiliar** than **difficult**.

.. list-table:: Where C++ asks for something Python handles on your behalf.
   :widths: 28 34 38
   :header-rows: 1
   :class: compact-table

   * - What
     - Python
     - C++
   * - Type of a variable
     - Decided at run time
     - Declared by you, checked at compile time
   * - Memory
     - Managed for you
     - Yours to reason about
   * - Errors
     - Usually surface when the line runs
     - Many surface before the program runs
   * - Running code
     - Interpreted directly
     - Preprocessed, compiled, linked, then run

.. note::

   C++ requires explicitness about matters that Python handles
   silently, and **that explicitness is the point**. It is also why the
   compiler can catch mistakes for you.


From Source to Executable
====================================================

Running a C++ program is not one step. Source text is transformed by
the **preprocessor**, translated by the **compiler**, assembled into
object code, joined to libraries by the **linker**, and only then
loaded and executed.

.. figure:: /_static/images/l1/development.png
   :align: center
   :alt: Diagram of the development process from writing source code through building to running the executable.

   The C++ development process: Write, Build, Run.

.. important::

   Each stage has its own errors and its own error messages. **Knowing
   which stage produced a message is most of the work of fixing it.**


Getting the Code
----------------------------------------------------

Every lecture has a matching folder in one repository. Clone it once
now, then pull before each lecture.

Clone It Once
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   mkdir -p ~/enpm702_cpp && cd ~/enpm702_cpp
   git clone https://github.com/zeidk/enpm702-fall-2026-cpp.git
   ls

Pull Before Every Lecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   cd ~/enpm702_cpp/enpm702-fall-2026-cpp
   git pull

- Each week's folder contains ``src/main.cpp``, a ``CMakeLists.txt``,
  and the code shown in that lecture.
- Work in your own copy. If you edit the cloned files directly,
  ``git pull`` will conflict with your changes.

.. note::

   **No GitHub account is needed to clone**, but you need one for the
   course. If ``git`` is not installed: ``sudo apt install git``.


Write
----------------------------------------------------

Open ``week1/src/main.cpp`` in Visual Studio Code:

.. code-block:: cpp

   #include <iostream>

   int main() {
       std::cout << "Week 1\n";
       return 0;
   }

- ``main()`` is the required entry point of every C++ program. It must
  return ``int``, not ``void``.

  - ``return 0`` can be omitted; reaching the closing brace returns 0
    automatically.

- ``std::cout << "Week 1\n";``

  - ``std::cout <<`` prints to the terminal. Requires
    ``#include <iostream>``.
  - ``'\n'`` adds a newline after the message.
  - The semicolon (``;``) terminates the statement. A statement is a
    complete instruction that tells the computer to perform a specific
    action.

.. note::

   The semicolon acts like a period in English: it marks the end of one
   complete instruction. Without it, the compiler would not know where
   one statement ends and the next begins.


Comments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Comments document code for the people who read, understand, and
maintain it. They explain complex logic, record design decisions, and
supply context that is not obvious from the code itself. Unlike other
code elements, comments are ignored during compilation and do not
affect program execution.

.. code-block:: cpp

   // Single-line comment: explains the next line of code
   /*
      Multi-line comment: useful for longer explanations,
      function descriptions, or temporarily disabling code blocks
   */

.. tip::

   Use ``Ctrl`` + ``/`` to comment and uncomment selected lines in
   VSCode.


Build
----------------------------------------------------

The build turns a text file into something the operating system can
load and run. It happens in three stages, and each can fail on its own
terms.

.. figure:: /_static/images/l1/build.png
   :align: center
   :alt: Diagram of the build pipeline: source file through preprocessor, compiler, and linker to an executable.

   The build process: preprocessor, compiler, linker.


Preprocessor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The preprocessor modifies source code before compilation:

  - Removes comments and adjusts whitespace.
  - Processes directives starting with ``#``:

    - ``#include`` performs a copy-paste of files.
    - Other directives: ``#define``, ``#ifdef``, ``#endif``, etc.

- ``g++ -std=c++20 -E main.cpp`` shows preprocessor output before
  compilation.
- ``g++ -std=c++20 -E main.cpp -o main.i`` stores that output in
  ``main.i``.

.. important::

   The preprocessor operates on **text**. It has no understanding of
   C++ syntax, semantics, or language rules.


Linemarkers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open ``main.i`` and you will find it is enormous, and that most of the
lines are not yours. Scattered through it are lines beginning with
``#``:

.. code-block:: text

   # 3 "main.cpp" 2

- This says: what follows came from **line 3** of ``main.cpp``.
- The trailing digit is a flag:

  - **1**: entering a file.
  - **2**: returning from one.
  - **3**: a system header.
  - **4**: treat as ``extern "C"`` (C linkage).

- Flag **3** is how the compiler knows not to warn you about code in
  ``<iostream>``. Without it, enabling warnings would bury you in
  complaints about libstdc++ rather than about your own code.


Compiler
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The compiler takes the preprocessed code and generates machine code
(object code). Machine code is the lowest-level language the CPU
understands directly: binary instructions, not text.

- ``g++ -std=c++20 -c main.cpp`` does the following:

  - **Preprocessing**: handles ``#include``, ``#define``, ``#ifdef``,
    etc.
  - **Compilation**: converts the preprocessed C++ code to assembly.
  - **Assembly**: converts assembly to a machine code object file
    (``.o``).

- ``g++ -std=c++20 -c main.i -o main.o`` skips the preprocessing step,
  since the input is already preprocessed, and performs the other two.
- ``hexdump -C main.o`` displays raw machine code.
- ``objdump -D main.o`` disassembles the object file.

.. tip::

   Read the **first** compiler error, not the last. One mistake early
   in a file usually produces a cascade, and the later messages are
   consequences rather than causes.


Linker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The linker combines object files and libraries into an executable
program. It resolves dependencies, calculates memory addresses, and
links external libraries.

- ``g++ main.o -o main`` does the following:

  - Takes the object file ``main.o``.
  - Links it, resolving any external references.
  - Creates an executable named ``main``.
  - Inspect the result with ``objdump -d --demangle main``.

.. important::

   Linker errors read differently from compiler errors. **undefined
   reference to** means the compiler accepted your code but the linker
   could not find the definition of something you used. That is a
   missing source file or a missing library, not a syntax problem.


Run
----------------------------------------------------

``./main`` runs the executable.

What Happens When You Run the Program
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The OS loads the executable file from storage into RAM.
- RAM stores the program's machine code instructions and data in memory
  locations.
- The CPU fetches instructions from RAM one by one.
- The CPU decodes each instruction to determine what operation to
  perform.
- The CPU executes the instruction (arithmetic, memory access, function
  calls, and so on).
- This fetch-decode-execute cycle continues until the program
  terminates.

Two Roles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **CPU**: the part that actually performs computations and controls
  program flow.
- **RAM**: fast temporary storage holding both program instructions and
  data during execution.


The Whole Path
----------------------------------------------------

.. figure:: /_static/images/l1/whole_path.png
   :align: center
   :alt: Summary diagram of the full path from source code to a running process.

   The full path from source files to a running process.


Building with CMake
====================================================

CMake is a **build system generator**. You describe your project once,
and CMake produces the actual build files for your platform.

Why Not Just ``g++``
----------------------------------------------------

- Typing ``g++`` by hand works for one file. It does not work for
  twenty files, three libraries, and a dependency graph.
- CMake tracks which files changed and rebuilds only those.
- Every ROS 2 package you write from Week 10 onward is a CMake project.
  You are learning the tool now so that it is familiar later.

.. note::

   **This is a demonstration, not the lesson.** CMake and VSCode are
   covered in the :doc:`VSCode and CMake
   </reading_material/vscode_cmake/vcm_index>` reading material,
   assigned before the first class. The sections below are a working
   demonstration to anchor that reading, not a substitute for it.


A Minimal Project
----------------------------------------------------

.. code-block:: text

   week1/
   ├── CMakeLists.txt
   ├── build/                  # generated, never commit it
   └── src/
       └── main.cpp

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.22)
   project(week1 LANGUAGES CXX)

   set(CMAKE_CXX_STANDARD 20)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   set(CMAKE_CXX_EXTENSIONS OFF)

   add_compile_options(-Wall -Wextra)

   add_executable(week1 src/main.cpp)

.. important::

   - ``CMAKE_CXX_STANDARD_REQUIRED ON`` makes the build **fail** if the
     compiler cannot provide C++20, instead of quietly falling back to
     an older standard.
   - ``CMAKE_CXX_EXTENSIONS OFF`` asks for ``-std=c++20`` rather than
     ``-std=gnu++20``, so you compile against the standard itself and
     not GCC's extensions to it. Code that relies on an extension
     compiles for you and fails for someone on a different compiler.

     - A compiler extension is a language feature the compiler accepts
       that the standard does not define.


Configure, Build, Run
----------------------------------------------------

CMake works in two steps. **Configure** reads ``CMakeLists.txt`` and
generates a build tree. **Build** runs the compiler and linker.

.. code-block:: bash

   cd week1
   cmake -S . -B build      # configure: generate the build tree
   cmake --build build      # build: compile and link
   ./build/week1            # run

- ``-S`` is the source directory, ``-B`` is the build directory.
- Everything generated goes in ``build/``. Deleting that directory is
  always safe, and is the correct first response to a build that has
  gone strange.
- Configure only needs rerunning when ``CMakeLists.txt`` changes.
  Adding a new source file counts as a change.

.. warning::

   Add ``build/`` to your ``.gitignore``. Committing a build tree is a
   common way to lose points and a common way to make a repository
   unusable for your teammates.


VSCode Workflow
----------------------------------------------------

With the **CMake Tools** and **C/C++** extensions installed, the
commands above have equivalents in the editor.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Build
        :class-card: sd-border-info sd-shadow-sm

        - Open the project folder: **File** → **Open Folder**
        - ``Ctrl + Shift + P``, then **CMake: Configure**. Select the
          GCC 13 kit when prompted.
        - **CMake: Build**, or the Build button in the status bar.
        - Pick what runs with the launch target in the status bar.

    .. grid-item-card:: Debug
        :class-card: sd-border-info sd-shadow-sm

        - **CMake: Debug** starts the executable under ``gdb``.
        - Click in the gutter to set a breakpoint, then step with the
          debug toolbar.
        - Inspect values in the Variables pane rather than adding print
          statements.
        - You will use ``gdb`` directly from Lecture 3, when a wrong
          pointer stops producing a readable error message.

.. tip::

   **Learn the debugger in week one**, while the programs are four
   lines long. It is much harder to learn it for the first time on a
   program that is already broken.


Environment Verification
====================================================

Everything in the rest of this course assumes the toolchain works. We
check that now, in the room, rather than discovering it the night RWA1
is due.

What We Are Checking
----------------------------------------------------

- That each required tool is installed and new enough.
- That you can compile and run a program by hand.
- That you can compile and run the same program through CMake.

.. note::

   **A failure here is expected** and is the reason we are doing it
   together. Toolchain trouble is normal in systems programming and
   always takes longer than expected.


Toolchain Check
----------------------------------------------------

Step 1: Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run each command and record what you get. Bring any line that fails to
the wrap-up.

.. code-block:: bash

   lsb_release -d          # expect: Ubuntu 24.04 LTS
   g++ --version           # expect: 13 or newer
   cmake --version         # expect: 3.22 or newer
   gdb --version
   valgrind --version
   doxygen --version
   git --version

Step 2: Build the Week 1 Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both routes build the same source. The first produces ``main``, the
second produces ``build/week1``.

.. code-block:: bash

   cd ~/enpm702_cpp/enpm702-fall-2026-cpp/week1
   g++ -std=c++20 -Wall -Wextra src/main.cpp -o main && ./main
   cmake -S . -B build && cmake --build build && ./build/week1


Common Failures
----------------------------------------------------

.. list-table:: Symptoms you are likely to hit today and what causes them.
   :widths: 45 55
   :header-rows: 1
   :class: compact-table

   * - Symptom
     - Usual cause
   * - ``g++: command not found``
     - ``sudo apt install build-essential``
   * - ``cmake: command not found``
     - ``sudo apt install cmake``
   * - Errors about unavailable language features
     - The standard flag is missing, or the build tree is stale
   * - ``undefined reference to main``
     - The source file was never added to ``add_executable``
   * - Changes to the code have no effect
     - You ran the old binary, or configure was not rerun after editing
       ``CMakeLists.txt``
   * - CMake reports a cached path that no longer exists
     - Delete ``build/`` and configure again

.. warning::

   If your environment is not working by the end of class, **email me
   this week**, not next week. Lecture 2 assumes you can compile.


Course Conventions
====================================================

A small number of conventions apply to every piece of code you submit
in this course. They are not stylistic preferences: each one exists
because the alternative causes a problem you would otherwise meet
later, in code that is harder to read.

.. important::

   These conventions are applied in the RWAs and Group Projects, and
   code that ignores them is marked down even when it compiles and runs
   correctly.


Newlines
----------------------------------------------------

The Rule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Always use ``'\n'`` to insert a newline. Do **not** use ``std::endl``
unless you have a specific reason to flush the output buffer.

.. code-block:: cpp

   std::cout << "Hello, World!" << '\n';       // correct
   std::cout << "Hello, World!" << std::endl;  // avoid

- Both lines produce the **same visible output**. They differ in what
  happens to the output buffer, not in what you see.
- ``'\n'`` is a character literal, written with single quotes.
  ``"\n"`` is a string literal containing that character; either
  works, but the character literal is the one to reach for.

.. note::

   This is the convention you will break most often out of habit,
   because ``std::endl`` appears in most older tutorials.


What ``std::endl`` Actually Does
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- It performs **two** operations: it writes a newline character,
  **and** it flushes the output buffer.
- Flushing forces the program to write all buffered output to the
  terminal immediately, rather than letting it accumulate and be
  written in one go.

Why the Flush Is Usually Unnecessary
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The buffer is flushed on your behalf in every case that matters:

- when it is full,
- when the program ends,
- and when ``std::cin`` is used to read input.

Why It Costs You
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

- A flush is a comparatively expensive operation. Paying for one on
  **every line** is wasted work.
- In loops or high-frequency output, which is exactly what robotics
  code produces, this causes noticeable performance degradation.

.. warning::

   Use ``'\n'`` by default. Use ``std::endl`` only when you genuinely
   need the output to appear **before** the program continues, for
   example a progress message printed immediately before a long
   computation or a suspected crash.
