====================================================
RWA1: Search-and-Rescue Drone
====================================================

.. figure:: /_static/images/rwa1/rwa1.jpeg
   :align: center
   :alt: A pencil sketch of a quadrotor drone flying over a mountain valley. A gimbal-mounted camera under the drone casts a grid of scan lines across the rocky ground, where a person is lying among the scrub.

   A search-and-rescue drone sweeping a valley for a casualty. This is
   the machine your program reports on. Image generated with Google
   Gemini.

Overview
--------

You are writing the on-board status program for a **search-and-rescue
drone**. The drone holds an altitude, watches its battery, moves through
mission phases, and records one victim it has located.

Everything in this assignment comes from Lectures 1 to 3: variables and
types, constants, scoped enumerations, pointers, references,
const-correctness, and dynamic memory with ``new`` and ``delete``. There
are no arrays, no containers, no functions of your own, and no classes.
Those arrive in later lectures and later assignments.

.. important::

   **Posted Sep 15, due Sep 29.** Everything it asks for is covered by
   Lecture 3, so you can start the day it is posted. It is deliberately
   small: the whole program is a single ``main()``, about 100 lines once
   your comments are in. If yours is growing well past that, you are
   probably solving a problem that was not asked for.


.. admonition:: Using AI on this assignment
   :class: important

   The course AI policy from
   :doc:`Lecture 1 </lectures/lecture1/l1_lecture>` applies here in full.
   In short:

   * You **may** use a tool such as TerpAI, ChatGPT, Claude, Gemini or
     Copilot to explain a concept, read a compiler error, suggest a way
     to debug something, or review code **you have already written**.
   * You **must** say so at the top of your ``README.md``: name the tool
     and describe in two or three sentences what you used it for.
     Disclosure carries no penalty. Undisclosed use is a violation of
     the Code of Academic Integrity.
   * You **may not** submit generated code that you cannot read,
     explain, and change. You are responsible for every line you hand
     in, and you may be asked to walk through any part of it and say why
     it works and what would break it.

   Two warnings specific to RWA1. These tools skew old, and memory
   management is where that shows most: expect suggestions written for
   C++98, along with raw arrays and habits this assignment does not
   want. And the whole point of R2 to R4 is to find out whether *you*
   can reason about pointers and references. Code you did not think
   through will not survive the walkthrough.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Declare and initialize variables, constants, and a scoped enumeration
   for a small robotics program.
2. Use pointers to read and change an object you do not name directly.
3. Apply const-correctness: choose between ``const T*`` and
   ``T* const`` and say why.
4. Use a reference as a second name for an object, and explain what
   assigning to it does.
5. Allocate an object on the heap, release it exactly once, and prove
   with Valgrind that nothing leaked.
6. Follow the course conventions: ``snake_case``, uniform
   initialization, and ``'\n'`` rather than ``std::endl``.


Requirements
------------

.. dropdown:: R1: Mission Setup

   Declare the state of the drone and its mission.

   1. Two limits whose values are known before the program starts and
      never change while it runs: a maximum altitude of **120** meters
      and a minimum safe battery percentage of **20.0**. Use these two
      values exactly, so that every submission reports the same limits.
      Lecture 2 gave you two ways to write a constant; pick the one that
      fits a value the compiler already knows, and be ready to say why.
   2. A **scoped enumeration** for the mission phase, with at least the
      values ``idle``, ``searching``, and ``returning``. Declare a
      variable of that type and set it to ``searching``.
   3. The drone's telemetry, each with uniform initialization: an ``int``
      altitude in meters, a ``double`` battery percentage, a ``double``
      rotor speed in RPM, and a ``bool`` saying whether the drone is
      airborne.
   4. Use ``auto`` for **exactly one** of these declarations, choosing a
      line where the type is already obvious from the initializer, and
      add a comment saying why ``auto`` is reasonable there and not
      everywhere.

   Acceptance criteria:

   * The two limits are compile-time constants, not ordinary variables
     that merely happen never to be reassigned.
   * The phase type is a scoped enumeration, and the phase variable is
     set using an enumerator's qualified name.
   * Every variable uses braces and a ``snake_case`` name that says what
     the value is.

   R1 prints nothing on its own. Its values show up in the report in R5.

.. dropdown:: R2: Reading and Changing Telemetry Through a Pointer

   A pointer lets one piece of code work on a value that is named
   somewhere else. Use one here.

   1. Declare a pointer to your altitude variable. Print the value of
      the pointer (the address it holds), the address of the variable,
      and the object it points at. The first two must match.
   2. The drone climbs. Add 15 meters to the altitude **through the
      pointer**, not by naming the variable, then print the variable
      itself to show that it changed.
   3. Declare a second ``int`` for a target altitude, with a value
      clearly different from the current altitude, and point the same
      pointer at it instead. Print what it reads now. This is the
      difference between ``ptr = ...`` and ``*ptr = ...``, so add a
      comment saying which line does which.
   4. Declare a **pointer to const** that reads the battery percentage.
      Read through it and print the value. Then write the line that
      would change the battery through that pointer, confirm that it
      does not compile, comment it out, and explain in a comment which
      ``const`` rejected it.

   Acceptance criteria:

   * The address printed through the pointer equals ``&altitude_m``.
   * The altitude is changed once through the pointer and once by
     repointing, and the comments say which is which.
   * A ``const double*`` is used for read-only access, with the rejected
     line left in place as a comment.

   Expected output (illustrative: your addresses will differ on every
   run, and your values are your own):

   .. code-block:: text

      -- R2: telemetry through a pointer --
      pointer holds  : 0x7ffd9f0c08f8
      address of var : 0x7ffd9f0c08f8
      points at      : 95 m
      after climbing : 110 m
      now points at  : 60 m
      battery (read-only): 78.5 %

   The first two lines must be the same address. The last line is read
   through the pointer to ``const``.

.. dropdown:: R3: A Victim Record on the Heap

   The drone locates one victim. You do not know at compile time whether
   it will find anybody, so the record goes on the heap.

   .. admonition:: Why you use ``new`` and ``delete`` here
      :class: important

      Lecture 3 says not to manage heap memory by hand, and later in the
      course you will use tools that do it for you. In this one
      requirement you write ``new`` and ``delete`` yourself, once, so
      that you have done it by hand before those tools arrive.

   1. Declare an ``int*`` named for the victim record and initialize it
      to ``nullptr``. This is the state "nothing found yet".
   2. Print whether a victim has been located, using a test on the
      pointer itself (``if (victim_ptr)``), before anything is
      allocated. It must report that nothing has been found, and it must
      not dereference the pointer.
   3. Allocate the record with ``new``, giving it a victim ID, and print
      the ID through the pointer.
   4. Release it with ``delete`` and set the pointer to ``nullptr`` on
      the next line.
   5. Run the same "has a victim been located" test again. It must now
      report that nothing is there, without crashing. Add a comment
      explaining what that test would have done if you had skipped
      step 4.

   Acceptance criteria:

   * The pointer starts as ``nullptr`` and ends as ``nullptr``.
   * Exactly one ``new`` and exactly one ``delete`` appear in the
     program.
   * The pointer is never dereferenced while it is null.
   * A comment explains why ``delete`` and ``nullptr`` belong on
     consecutive lines.

   Expected output (illustrative):

   .. code-block:: text

      -- R3: victim record --
      before search  : no victim located
      located victim : id 5017
      after release  : no victim on record

   The first and third lines come from the *same* test on the pointer,
   run before the allocation and after the release.

.. dropdown:: R4: A Reference as a Second Name

   1. Bind a reference to your battery percentage variable, with a name a
      reader would understand.
   2. Drain the battery by 12.5 through the reference, then print the
      original variable to show that there is only one object.
   3. Print ``&battery_pct`` and the address of the reference. Explain in
      a comment why they are the same and what that tells you about what
      a reference is.
   4. Declare a second ``double`` holding a reserve battery level, then
      assign it to the reference. Print all three values and explain in a
      comment why the reference did **not** start naming the reserve
      variable.

   Acceptance criteria:

   * The reference is bound when it is declared.
   * The battery is changed through the reference, and the original
     variable shows the change.
   * The comment on step 4 says clearly that assignment copies a value
     and never rebinds a reference.

   Expected output (illustrative):

   .. code-block:: text

      -- R4: the battery, by another name --
      battery after draining 12.5: 66 %
      address of battery_pct : 0x7ffd9f0c0908
      address of the reference: 0x7ffd9f0c0908
      after assigning the reserve level: battery_pct 40, reference 40, reserve 40

   Both addresses are the same address. On the last line all three
   numbers are equal, which is the whole point: the assignment copied the
   reserve value into the battery, and the reference still names the
   battery.

.. dropdown:: R5: Situation Report and a Clean Valgrind Run

   1. Print one report with three labeled sections: **mission** (phase
      and the two limits), **telemetry** (altitude, battery, rotor speed,
      airborne or grounded), and **victim** (located or not).
   2. Print the mission phase as readable text, not a number. A
      ``switch`` over the enumeration is the natural way; C++20's
      ``using enum`` inside the ``switch`` keeps it readable.
   3. Print the airborne flag as "airborne" or "grounded", not ``1`` or
      ``0``.
   4. Compare the battery against ``min_battery_pct`` and print a warning
      line when it is below the limit.
   5. Build the project, then run the program under Valgrind and copy the
      last lines of its output into your ``README.md``.

   Acceptance criteria:

   * All three sections appear, separated by a header line.
   * No raw ``true``/``false`` or enumerator numbers appear in the
     output.
   * Valgrind reports ``All heap blocks were freed -- no leaks are
     possible`` and ``ERROR SUMMARY: 0 errors``.
   * Every newline is ``'\n'``. ``std::endl`` appears nowhere.

   Expected report (illustrative: your values are your own):

   .. code-block:: text

      ===== MISSION =====
      phase        : searching
      max altitude : 120 m
      min battery  : 20 %

      ===== TELEMETRY =====
      altitude : 110 m
      battery  : 40 %
      rotors   : 5400 rpm
      state    : airborne
      WARNING: battery below the safe minimum

      ===== VICTIM =====
      none on record

   In that run the battery ended at 40 %, which is above the 20 % limit,
   so the warning line would **not** appear. It is shown here only so you
   can see its wording. Drain the battery further, or raise the limit,
   to see it fire in your own program.

   Run it under Valgrind once the report is right:

   .. code-block:: bash

      valgrind --leak-check=full <path to your built program>

   The last lines you paste into ``README.md`` should look like this:

   .. code-block:: text

      ==12345== All heap blocks were freed -- no leaks are possible
      ==12345== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)


Deliverables
------------

Submit **one zip file** on Canvas, named after the folder it contains:
``rwa1_firstname_lastname.zip``, for example
``rwa1_bjarne_stroustrup.zip``.

The zip must contain exactly one folder, with exactly these three files
in it and nothing else:

.. code-block:: text

   rwa1_firstname_lastname/
   ├── CMakeLists.txt          # builds src/main.cpp into an executable
   ├── README.md               # how to build and run, plus Valgrind output
   └── src/
       └── main.cpp            # all of your code

.. list-table::
   :header-rows: 1
   :widths: 25 75
   :class: compact-table

   * - File
     - Description
   * - ``CMakeLists.txt``
     - Builds ``src/main.cpp`` into an executable named ``rwa1``, with
       ``CMAKE_CXX_STANDARD`` set to 20. Five lines is enough. Note the
       path: the source sits in ``src/``, so the target line reads
       ``add_executable(rwa1 src/main.cpp)``.
   * - ``src/main.cpp``
     - One source file, with all of your code inside ``main()``.
   * - ``README.md``
     - How to build and run it, the last lines of your Valgrind output
       pasted in showing no leaks and no errors, and your AI disclosure
       if you used a tool.

``src/main.cpp`` starts with a Doxygen file header and is laid out like
this. The markers are how your work gets found when it is graded, so keep
them and keep the requirements in this order. Everything inside the
blocks is yours to write.

.. code-block:: cpp

   /**
    * @file main.cpp
    * @author Firstname Lastname (your_email@umd.edu)
    * @brief RWA1: pointers, references, and dynamic memory on a
    *        search-and-rescue drone.
    * @version 0.1
    * @date 2026-09-29
    *
    * @copyright Copyright (c) 2026
    */

   #include <iostream>
   // TODO: add any other headers you need as you go

   int main() {
       // ===== R1: mission setup =====

       // ===== R2: telemetry through a pointer =====

       // ===== R3: victim record on the heap =====

       // ===== R4: a reference =====

       // ===== R5: situation report =====
   }

Fill in ``@author`` and ``@date`` with your own name and your submission
date. Doxygen comments are covered properly in Lecture 5; for now, copy
the header and fill in the fields.

.. warning::

   Do **not** include the ``build/`` directory, editor folders such as
   ``.vscode/``, or the compiled executable. The project will be graded
   by configuring and building it from your ``CMakeLists.txt``, so a
   submission that does not configure and build cannot be graded.


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 32 12 56
   :class: compact-table

   * - Category
     - Weight
     - Criteria
   * - Correctness
     - 30 %
     - The program builds with no warnings under ``-Wall -Wextra`` and
       prints the report described in R5.
   * - Pointers and const
     - 25 %
     - R2 is correct: the pointer reads and writes the right object, the
       difference between ``ptr =`` and ``*ptr =`` is demonstrated, and
       the pointer to ``const`` is used and explained.
   * - Dynamic memory
     - 20 %
     - R3 is correct: one ``new``, one ``delete``, no dereference of a
       null pointer, and a clean Valgrind run.
   * - References
     - 15 %
     - R4 is correct, including the explanation that assignment does not
       rebind a reference.
   * - Code quality
     - 10 %
     - The Doxygen file header is filled in, and the code uses uniform
       initialization, ``snake_case``, names that say what the value is,
       ``'\n'``, and comments that explain the pointer and reference
       lines.


Tips
----

.. admonition:: Write it in the order of the requirements
   :class: tip

   R1 to R5 are in dependency order. Get R1 printing, then add R2, and so
   on. Build and run after each requirement rather than at the end.

.. admonition:: The pointer questions are the assignment
   :class: tip

   For every pointer line, be able to say out loud what the pointer holds
   and which object you are changing. If you cannot, that line is where
   your bug is.

.. admonition:: Run Valgrind before you submit
   :class: tip

   There is one heap allocation in this whole program, so there is no
   excuse for a leak. ``valgrind --leak-check=full`` on your built
   program should end with ``0 errors``.

.. admonition:: Follow the conventions
   :class: tip

   * Uniform initialization: ``int count{0};``, not ``int count = 0;``
   * ``snake_case``: ``sensor_reading``, not ``sensorReading``
   * ``'\n'``, never ``std::endl``
   * Pointer declarations as ``int* ptr``, one per line

References
----------

The **C++ Core Guidelines** are the rules this course grades against.
These are the ones that apply to RWA1. Read the short entry behind each
link before you decide how to write the matching requirement.

.. list-table::
   :header-rows: 1
   :widths: 16 84
   :class: compact-table

   * - Rule
     - Says
   * - `ES.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es20-always-initialize-an-object>`_
     - Always initialize an object.
   * - `ES.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es10-declare-one-name-only-per-declaration>`_
     - Declare one name (only) per declaration.
   * - `Con.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con5-use-constexpr-for-values-that-can-be-computed-at-compile-time>`_
     - Use ``constexpr`` for values that can be computed at compile
       time.
   * - `ES.45 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es45-avoid-magic-constants-use-symbolic-constants>`_
     - Avoid "magic constants"; use symbolic constants.
   * - `Enum.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#enum3-prefer-class-enums-over-plain-enums>`_
     - Prefer ``enum class`` over plain ``enum``.
   * - `Enum.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#enum2-use-enumerations-to-represent-sets-of-related-named-constants>`_
     - Use enumerations to represent sets of related named constants.
   * - `ES.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es11-use-auto-to-avoid-redundant-repetition-of-type-names>`_
     - Use ``auto`` to avoid redundant repetition of type names.
   * - `ES.65 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es65-dont-dereference-an-invalid-pointer>`_
     - Do not dereference an invalid pointer.
   * - `R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r3-a-raw-pointer-a-t-is-non-owning>`_
     - A raw pointer (a ``T*``) is non-owning.
   * - `R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r11-avoid-calling-new-and-delete-explicitly>`_
     - Avoid calling ``new`` and ``delete`` explicitly.
   * - `NL.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl10-prefer-underscore_style-names>`_
     - Prefer ``underscore_style`` names.
   * - `NL.19 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl19-avoid-names-that-are-easily-misread>`_
     - Avoid names that are easily misread.
