====================================================
Lecture
====================================================

Learning Objectives
-------------------

1. Write, declare and call functions, and split them into header and source files.
2. Choose how to pass arguments and how to return results.
3. Overload a function and give it default arguments.
4. Explain static locals, stack frames, and the arguments of ``main``.
5. Document functions with Doxygen.

Code for This Lecture
^^^^^^^^^^^^^^^^^^^^^

- ``project/week5/playground``: every snippet in ``src/snippets.cpp``, target ``week5_snippets``.
- ``project/week5/arm_demo``: the finished program in several files, target ``week5_arm_demo``.

These parts use ``arm_demo`` (the slides mark them with a file icon):

- Header Files: The Program So Far, Separate Compilation, Building with CMake, Include Guards, Nested Includes, A Definition in a Header, and Exercise 1.
- Default Arguments: The Program So Far and Defaults in the Declaration.
- Documenting Functions: Project Layout, The File Comment, Running Doxygen and The Working Directory.

.. note::

   The `Further Reading`_ part, after the summary, is the appendix of the slides. It is not presented. Read it on your own.

Functions
---------

A **function** is a named block of statements that runs when it is called. It can take inputs and can give back one value. See `cppreference: functions <https://en.cppreference.com/w/cpp/language/functions>`__.

The Program We Will Build
^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l5/narrative.jpeg
   :alt: Pencil sketch of the program in three steps. On the left, a robot arm with three joints is drawn twice, (a) before clamping and (b) after clamping, with its joint angles marked. Step 1, Input: a terminal where the user enters the angles 180, 95 and minus 10 degrees. Step 2, Clamp and Convert: each angle is checked against its joint limit and converted to radians. A table shows 180 clamped to 135 (2.356 rad), 95 clamped to 90 (1.571 rad), and minus 10 kept as minus 10 (minus 0.175 rad). Step 3, Compute and Report: a forward kinematics gear produces a report with the tool position (minus 4.5, 3.2) in the base frame, which is also marked at the tip of the arm below.
   :align: center
   :width: 90%

   A planar arm with three joints. Read the joint angles in degrees, typed in or from the command line, clamp each one to its joint's limit, convert it to radians, and report where the tool ends up.

To **clamp** an angle is to replace it with the limit when it goes past it. An angle inside the limits is kept as it is.

.. note::

   The program uses the same limits as the sketch: 135 degrees for the shoulder, 90 for the elbow and 45 for the wrist. For the input ``180 95 -10`` it prints the clamped angles 135, 90 and -10, as in the sketch, and the tool position x = -0.882 m, y = -0.101 m. The tool position in the sketch is only illustrative.

The program is split into five files:

.. figure:: /_static/images/l5/narrative_files.png
   :alt: Five file cards joined by #include arrows. Source files have a blue name strip and header files a grey one. At the top, kinematics.cpp includes kinematics.hpp and joint_limits.hpp and holds the definitions of convert_deg_to_rad, forward_kinematics and print_pose, each with its body written as {...}. At the top right, joint_limits.cpp includes joint_limits.hpp and holds the definition of clamp_joint(double deg, double limit). Below the middle, kinematics.hpp has #pragma once, includes joint_limits.hpp, and declares convert_deg_to_rad, forward_kinematics with double limit = max_deg, and print_pose with int precision = 3 and std::string_view label = "tool". At the bottom left, main.cpp includes kinematics.hpp and holds int main(int argc, char* argv[]) {...}, with an arrow across to kinematics.hpp. An arrow runs from kinematics.hpp across to joint_limits.hpp, which has #pragma once, constexpr double max_deg{170.0}, one limit per joint (shoulder_max_deg 135.0, elbow_max_deg 90.0, wrist_max_deg 45.0), and declares clamp_joint(double deg, double limit = max_deg).
   :align: center
   :width: 90%

   The five files of the arm program and what each one holds.

- An arrow means ``#include``. Blue files are **compiled** (never included). Grey files are **included** (never compiled).
- The finished program is in ``project/week5/arm_demo``: headers in ``include``, source files in ``src``.

Project Layout
^^^^^^^^^^^^^^

.. code-block:: text

   project/week5/
   ├── CMakeLists.txt
   ├── playground/
   │   └── src/snippets.cpp
   └── arm_demo/
       ├── include/
       │   ├── joint_limits.hpp
       │   └── kinematics.hpp
       ├── src/
       │   ├── joint_limits.cpp
       │   ├── kinematics.cpp
       │   └── main.cpp
       └── docs/
           ├── Doxyfile
           └── html/   (generated)

- ``playground``: every snippet from the slides, in one file. Target ``week5_snippets``.
- ``arm_demo``: the program in several files. Target ``week5_arm_demo``, from the Header Files section on.
- ``include``: headers. ``src``: source files.
- ``docs``: Doxygen, at the end of the lecture.

In ``snippets.cpp`` each block sits between ``#if 0`` and ``#endif``. Change it to ``#if 1`` to try it.

Why Functions
^^^^^^^^^^^^^

Two ways to clamp two joints to the arm's limit:

.. code-block:: cpp

   // Without a function
   constexpr double max_deg{170.0};

   double q2{-200.0};  // elbow
   if (q2 > max_deg) { q2 = max_deg; }
   if (q2 < -max_deg) { q2 = -max_deg; }

   double q3{-250.0};  // wrist, copied
   if (q3 > max_deg) { q3 = max_deg; }
   if (q3 < -max_deg) { q2 = -max_deg; }

.. code-block:: cpp

   // With a function
   constexpr double max_deg{170.0};

   double clamp_joint(double deg) {
     if (deg > max_deg) { return max_deg; }
     if (deg < -max_deg) { return -max_deg; }
     return deg;
   }

   double q2{clamp_joint(-200.0)};  // elbow
   double q3{clamp_joint(-250.0)};  // wrist

- **Without a function**, the logic is repeated: two tests per joint, twelve for a six-joint arm. **Copies drift.** The wrist block was copied and one ``q2`` was never renamed. It compiles with no warning, and the wrist stays at -250.
- **With a function**, there is one place to change the rule, one body to edit and one function to test.

The standard library already has ``std::clamp`` in ``<algorithm>``. ``clamp_joint`` is written out here to show the parts of a function.

.. admonition:: Best Practice
   :class: tip

   Write each piece of logic **once**, in a function, and call it. This is **DRY**, Don't Repeat Yourself (Hunt and Thomas, *The Pragmatic Programmer*). Rule: `Core Guidelines F.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-package>`__.

Anatomy of a Function
^^^^^^^^^^^^^^^^^^^^^

A function has four parts: a **return type**, a **name**, a **parameter list** in parentheses, and a **body** in braces.

.. code-block:: text

   return_type name(parameter_list) {
     body
   }

.. code-block:: cpp

   double convert_deg_to_rad(double deg) {
     return deg * std::numbers::pi / 180.0;  // C++20, <numbers>
   }

- A function that gives nothing back has return type ``void``.
- No parameters means empty parentheses: ``void stop_motors()``, not ``void stop_motors(void)``.
- Names are ``snake_case``, the same as variables, and start with a **verb**: a function does something.

Function Header
~~~~~~~~~~~~~~~

The **function header** is everything before the body: the return type, the name and the parameter list.

.. code-block:: cpp

   double convert_deg_to_rad(double deg)  // the header
   {
     return deg * std::numbers::pi / 180.0;  // the body
   }

- A header followed by ``;`` is a **declaration**. Followed by a body, it is a **definition**.
- A function header is **not** a header file: same word, two things.

.. note::

   "Function header" is the textbook name. The C++ standard has no single name for this line.

Function Signature
~~~~~~~~~~~~~~~~~~

The **signature** is the name, the namespace it is in, and the **types** of the parameters, in order. The return type and the parameter names are not part of it.

.. code-block:: cpp

   namespace robot {
     constexpr double convert_deg_to_rad(double deg);
   }
   // signature: robot::convert_deg_to_rad(double)

The linker names functions by signature: ``undefined reference to `robot::convert_deg_to_rad(double)'``.

.. note::

   C++20, **[defns.signature]**, section 3.20: for a function, the signature is its *name, parameter-type-list, and enclosing namespace (if any)*. Friends, templates and member functions add more (3.21 to 3.27).

Parameters and Arguments
~~~~~~~~~~~~~~~~~~~~~~~~

A **parameter** is a variable declared in the function's parameter list. It exists only while the function runs.

.. code-block:: cpp

   void print_velocities(double linear, double angular) {  // parameters
     std::cout << linear << ' ' << angular << '\n';
   }

An **argument** is the value the caller supplies for a parameter, written in the call.

.. code-block:: cpp

   print_velocities(0.5, 0.1);  // arguments

Each parameter is **initialized from** its argument, in order, when the call starts, by the rules you already know for ``int x{a};``.

.. admonition:: Best Practice
   :class: tip

   Keep a function to **one job**. Start its name with a **verb**, because it does an action: ``print_velocities``. Rule: `Core Guidelines F.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-logical>`__.

Declaration and Definition
^^^^^^^^^^^^^^^^^^^^^^^^^^

A **declaration** gives the return type, name and parameter types, and ends in a semicolon. A **definition** is a declaration with a body.

.. code-block:: cpp

   double clamp_joint(double deg); // declaration (a prototype)

   double clamp_joint(double deg) {  // definition
     return std::clamp(deg, -max_deg, max_deg);
   }

- A declaration is a promise to the compiler: this function exists (**it is defined somewhere**), and here is how to call it.
- A program may **declare** a function many times but must **define** it exactly once. This is the **one-definition rule**.

Declaration Order
~~~~~~~~~~~~~~~~~

The compiler reads a file from top to bottom. A name must be declared **above** the line that uses it.

.. code-block:: cpp

   void report_arm() {
     std::cout << "arm: ";
     print_limits();  // not seen yet
   }

   void print_limits() {
     std::cout << "170 deg\n";
   }

.. code-block:: text

   order.cpp:4:3: error: 'print_limits' was not declared in this scope

.. code-block:: cpp

   void print_limits();  // the promise

   void report_arm() {
     std::cout << "arm: ";
     print_limits();  // OK
   }

   void print_limits() {
     std::cout << "170 deg\n";
   }

- Moving ``print_limits`` above ``report_arm`` also works, until two functions call each other. Then no order works.
- A declaration fixes both cases, because a declaration can come before either definition.

Two Functions That Call Each Other
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A joint past its limit is clamped and driven again. Each function calls the other, so no order of the two definitions works:

.. code-block:: cpp

   void move_joint(double deg) {
     if (deg > max_deg) {
       retry_move(deg);// not seen yet
       return;
     }
     // drive the motor to deg
   }

   void retry_move(double deg) {
     move_joint(clamp_joint(deg));
   }

.. code-block:: text

   retry.cpp:3:5: error: 'retry_move' was not declared in this scope

One declaration fixes it:

.. code-block:: cpp

   void retry_move(double deg);

   void move_joint(double deg) {
     if (deg > max_deg) {
       retry_move(deg);  // OK
       return;
     }
     // drive the motor to deg
   }

   void retry_move(double deg) {
     move_joint(clamp_joint(deg));
   }

- Swapping the two definitions moves the error. It does not remove it.
- The declaration breaks the cycle because it can sit above **both** definitions.

.. admonition:: Best Practice
   :class: tip

   Declare **every** function, not only the one that causes an error. Then the definitions can go in any order.

   .. code-block:: cpp

      double clamp_joint(double deg);
      void move_joint(double deg);
      void retry_move(double deg);

      void retry_move(double deg) {
        move_joint(clamp_joint(deg));
      }

      void move_joint(double deg) {
        if (deg > max_deg) {
          retry_move(deg);
          return;
        }
      }

      double clamp_joint(double deg) {
        return std::clamp(deg, -max_deg, max_deg);
      }

A Missing Definition
~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   double clamp_joint(double deg);  // promised, never delivered

   int main() {
     std::cout << clamp_joint(200.0) << '\n';
   }

.. code-block:: bash

   g++ -std=c++20 -c main.cpp -o main.o   # compiles: the promise is enough
   g++ main.o -o main                     # links: fails

- The **compiler** only checks the call against the declaration. The **linker** looks for the body.
- An error that mentions ``ld`` or ``undefined reference`` is a link error, not a mistake in the line it names.

Header Files
^^^^^^^^^^^^

A **header file** (``.hpp``) holds declarations that other files ``#include``. The matching **source file** (``.cpp``) holds the definitions.

- The header is the **interface**: what you can call. The source file is the **implementation**: how it works.
- A ``.cpp`` file is **compiled**. A ``.hpp`` file is **included**, never compiled on its own.

.. admonition:: Code for this part
   :class: note

   The code for this part is ``project/week5/arm_demo``. Uncomment the last four lines of ``project/week5/CMakeLists.txt``, then configure and build ``week5_arm_demo`` with CMake in VS Code.

Why Split a Program
~~~~~~~~~~~~~~~~~~~

- **Faster builds.** Change a body in ``kinematics.cpp`` and only that file is compiled again.
- **A clear interface.** The header says what you can call. The source file keeps how it works out of sight.
- **One definition.** Declare a function in as many files as you like, but define it exactly once.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Header (``.hpp``): What
     - Source (``.cpp``): How
   * - **Declarations:** function signatures
     - **Definitions:** the function bodies
   * - **Constants:** ``constexpr`` values such as ``max_deg``
     - **Helpers:** functions only this file uses
   * - **Types and templates:** Lecture 6
     - **Local data:** values only this file uses, such as ``link1_m``

The Program So Far: One Header, Two Source Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l5/files_three.png
   :alt: Three file cards from project/week5/arm_demo. main.cpp and kinematics.cpp, with blue name strips, sit on top, each with an arrow down to kinematics.hpp, with a grey name strip. main.cpp holds #include "kinematics.hpp" and int main(int argc, char* argv[]) {...}. kinematics.hpp holds #pragma once and the declaration double convert_deg_to_rad(double deg);. kinematics.cpp holds #include "kinematics.hpp" and the definition double convert_deg_to_rad(double deg) {...}. In the two kinematics cards a grey ... stands for the lines shown on later slides.
   :align: center
   :width: 70%

   One header, two source files. Red marks what each stage adds from here on.

**include/kinematics.hpp**

.. code-block:: cpp

   #pragma once
   double convert_deg_to_rad(double deg);

**src/kinematics.cpp**

.. code-block:: cpp

   #include "kinematics.hpp"
   #include <numbers>
   double convert_deg_to_rad(double deg) {
     return deg * std::numbers::pi / 180.0;
   }

**src/main.cpp**

.. code-block:: cpp

   #include "kinematics.hpp"
   #include <iostream>
   int main() {
     std::cout << convert_deg_to_rad(90.0);
   }

- The header **declares**. The source file **defines**. ``main.cpp`` only **calls**.
- ``kinematics.cpp`` includes its own header, so a definition whose return type disagrees with the declaration does not compile.
- Quotes ``"..."`` search your project first. Angle brackets ``<...>`` search the system and the standard library.

Separate Compilation
~~~~~~~~~~~~~~~~~~~~

``main.cpp`` never sees ``kinematics.cpp``. Each ``.cpp`` is compiled on its own, and the **linker** joins the results.

.. code-block:: bash

   g++ -std=c++20 -Iinclude -c src/main.cpp         -o main.o
   g++ -std=c++20 -Iinclude -c src/kinematics.cpp   -o kinematics.o
   g++ -std=c++20 -Iinclude -c src/joint_limits.cpp -o joint_limits.o
   g++ main.o kinematics.o joint_limits.o -o arm_demo

- The header gives ``main.cpp`` the **signature**. That is enough to check the call, but the function's address is left blank in ``main.o``.
- The linker finds the body in ``kinematics.o`` and writes its address into the call. Leave ``kinematics.o`` off the last line and you get ``undefined reference``.

The Program So Far: What Is Compiled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l5/files_cmake.png
   :alt: Five file cards from project/week5/arm_demo. The three source files are outlined in red and show their contents: main.cpp with int main(int argc, char* argv[]) {...}; kinematics.cpp with its two #include lines and the definition of convert_deg_to_rad, then a grey ...; and joint_limits.cpp with the definition double clamp_joint(double deg, double limit) {...}. The two header files, kinematics.hpp and joint_limits.hpp, are greyed out as names only. Faint arrows run from main.cpp and kinematics.cpp to kinematics.hpp, from kinematics.cpp and kinematics.hpp to joint_limits.hpp, and from joint_limits.cpp up to joint_limits.hpp.
   :align: center
   :width: 90%

   Only the ``.cpp`` files, outlined in red, are compiled. The headers are included.

Building with CMake
~~~~~~~~~~~~~~~~~~~

.. code-block:: cmake

   add_executable(week5_arm_demo
     arm_demo/src/main.cpp
     arm_demo/src/kinematics.cpp
     arm_demo/src/joint_limits.cpp)

   target_include_directories(week5_arm_demo
     PRIVATE arm_demo/include)

- List **every** ``.cpp`` in ``add_executable``. Leave one out and you get ``undefined reference``.
- Never list a ``.hpp`` as a source to compile. ``target_include_directories`` tells the compiler where to look for them.
- ``PRIVATE`` means the directory is only for this target. It matters once one target uses another, in a later lecture.

.. note::

   Without ``target_include_directories``, ``#include "kinematics.hpp"`` fails in ``main.cpp`` with ``No such file or directory``, because the header is not in the same folder as the file that includes it.

These are the last four lines of ``project/week5/CMakeLists.txt``, which build the program in ``project/week5/arm_demo``: ``include/kinematics.hpp``, ``include/joint_limits.hpp``, ``src/main.cpp``, ``src/kinematics.cpp`` and ``src/joint_limits.cpp``. The slide snippets are in ``project/week5/playground/src/snippets.cpp``, built by the target ``week5_snippets``.

Include Guards
~~~~~~~~~~~~~~

An **include guard** is a pair of preprocessor lines that make the second and later copies of a header empty. Without one, a header included twice, directly or through another header, is pasted twice.

Portable:

.. code-block:: cpp

   #ifndef JOINT_LIMITS_HPP
   #define JOINT_LIMITS_HPP

   constexpr double max_deg{170.0};
   double clamp_joint(double deg);
   #endif  // JOINT_LIMITS_HPP

Shorter:

.. code-block:: cpp

   #pragma once

   constexpr double max_deg{170.0};
   double clamp_joint(double deg);

``#pragma once`` is not in the standard, but GCC, Clang and MSVC all support it. This course uses it.

.. warning::

   Every guard macro must be unique across the project and every third-party header. Two headers that both pick ``JOINT_LIMITS_HPP`` silently lose the second one. See `the tradeoffs, both ways <https://en.wikipedia.org/wiki/Pragma_once>`__.

The Program So Far: Nested Includes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/images/l5/files_nested.png
   :alt: Five file cards from project/week5/arm_demo, with main.cpp and joint_limits.cpp greyed out as names only. kinematics.cpp, at the top, has #include "joint_limits.hpp" and the definition of forward_kinematics in red. kinematics.hpp, below left, has #include "joint_limits.hpp" and the declaration of forward_kinematics ending in double limit = max_deg, both in red. joint_limits.hpp, below right, holds #pragma once, constexpr double max_deg{170.0}, one limit per joint (shoulder_max_deg 135.0, elbow_max_deg 90.0, wrist_max_deg 45.0) and the declaration double clamp_joint(double deg, double limit = max_deg);. Red arrows run from kinematics.cpp to kinematics.hpp, from kinematics.cpp to joint_limits.hpp, and from kinematics.hpp to joint_limits.hpp: two routes from kinematics.cpp to joint_limits.hpp.
   :align: center
   :width: 90%

   ``joint_limits.hpp`` reaches ``kinematics.cpp`` by two routes.

.. code-block:: cpp

   // kinematics.hpp
   #pragma once
   #include "joint_limits.hpp"  // for max_deg

   void forward_kinematics(double q1, double q2,
     double q3, double& x, double& y, double limit = max_deg);

- ``kinematics.hpp`` needs ``max_deg`` for a default argument, so it includes the header that defines it.
- ``kinematics.cpp`` includes both headers, so ``joint_limits.hpp`` arrives twice. The guard makes the second copy empty.

.. note::

   A repeated declaration is harmless, but a repeated **definition** is not.

A Definition in a Header
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // kinematics.hpp, included by main.cpp and by planner.cpp
   #pragma once
   #include <numbers>
   double convert_deg_to_rad(double deg) {
     return deg * std::numbers::pi / 180.0;
   }

.. code-block:: text

   /usr/bin/ld: planner.o: in function `convert_deg_to_rad(double)':
   planner.cpp:(.text+0x0): multiple definition of `convert_deg_to_rad(double)';
   main.o:main.cpp:(.text+0x0): first defined here
   collect2: error: ld returned 1 exit status

- ``#pragma once`` does not help. It works **within** one source file, and each ``.cpp`` is compiled on its own.
- Each file gets its own copy of the body, and the linker finds two definitions. That breaks the one-definition rule.

.. admonition:: Best Practice
   :class: tip

   Keep function bodies in the ``.cpp``. A header holds declarations. (Marking the function ``inline`` also works.) Rule: `Core Guidelines SF.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-inline>`__.

Exercise 1: Reading a Split Program
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open ``project/week5/arm_demo``. The target ``week5_arm_demo`` builds it. Undo each change before the next step.

1. Read ``include/kinematics.hpp`` and ``src/kinematics.cpp``. For each function, where is it declared and where is it defined?
2. ``src/kinematics.cpp`` includes ``joint_limits.hpp`` by two routes. Find both. Why is ``max_deg`` defined only once?
3. Remove ``src/kinematics.cpp`` from ``week5_arm_demo`` in ``CMakeLists.txt``. Does compiling or linking fail? Why?
4. Put it back and remove ``src/joint_limits.cpp`` instead. What is missing now?
5. Move the body of ``convert_deg_to_rad`` into the header. What fails, and why does ``#pragma once`` not help?

Calling and Returning
^^^^^^^^^^^^^^^^^^^^^

A **call** jumps to the start of the function's body. A ``return`` statement, or the closing brace of a ``void`` function, jumps back to just after the call.

.. code-block:: cpp
   :linenos:

   void print_limits() {
     std::cout << "170 deg\n";
   }

   void report_arm() {
     std::cout << "arm: ";
     print_limits();
   }

   int main() {
     report_arm();
     std::cout << "exit main\n";
   }

.. figure:: /_static/images/l5/call_sequence.png
   :alt: Sequence diagram with three lifelines, main, report_arm and print_limits, each named at the top and the bottom. A red arrow labelled call runs from main to report_arm. A short arrow looping back onto report_arm is labelled "arm:". A red arrow labelled call runs from report_arm to print_limits. A loop on print_limits is labelled "170 deg". A blue arrow labelled return runs back from print_limits to report_arm, then another from report_arm to main. A final loop on main is labelled "exit main".
   :align: center
   :width: 60%

   The order of calls and returns, and what each function prints.

The return Statement
~~~~~~~~~~~~~~~~~~~~

A ``return`` statement ends the function and sends control back to the caller. With an operand, the operand's value **initializes** the result of the call.

.. code-block:: cpp

   // In a void function
   void print_range(double m) {
     if (m < 0.0) {
       std::cout << "invalid\n";
       return;  // leave early
     }
     std::cout << m << " m\n";
   }  // returns here otherwise

.. code-block:: cpp

   // With a value
   int calculate_sum(int a, int b) {
     int result{a + b};
     return result;
   }

   int sum{calculate_sum(5, 3)};  // 8

- In a ``void`` function, ``return`` leaves early. At the end it is optional.
- The value is converted to the declared return type if it has to be.

.. admonition:: Best Practice
   :class: tip

   To get a value out, **return it**. Do not fill in a reference parameter instead. Rule: `Core Guidelines F.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out>`__.

Missing Returns
~~~~~~~~~~~~~~~

.. code-block:: cpp

   int get_sign(int number) {
     if (number > 0) {
       return 1;
     } else if (number < 0) {
       return -1;
     }
   }  // number == 0 falls off the end

.. code-block:: text

   noret.cpp:7:1: warning: control reaches end of non-void function [-Wreturn-type]

- It is a **warning**, not an error. The program builds, and ``get_sign(0)`` returns whatever happens to be left over.
- Treat it as an error with ``-Werror=return-type``. GCC prints it even without ``-Wall``.

.. warning::

   C++20, **[stmt.return]**, section 8.7.3, paragraph 2: *flowing off the end of a function other than* ``main`` *or a coroutine results in undefined behavior*. ``main`` is the one exception, covered in the section on ``main``.

Conversion on Return
~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   int truncate_value() {
     double value{99.99};
     return value;  // converted to int: 99
   }

- The ``double`` is **silently** converted to the return type, and the fraction is lost.
- The course flags, ``-Wall -Wextra -pedantic-errors -Wshadow``, say **nothing**. You need ``-Wconversion``:

.. code-block:: text

   trunc.cpp:3:10: warning: conversion from 'double' to 'int' may change value [-Wfloat-conversion]

.. note::

   If you mean to drop the fraction, say so: ``return static_cast<int>(value);``. The cast is the same one Lecture 2 used, and it tells the reader the loss is on purpose.

[[nodiscard]]
~~~~~~~~~~~~~

``[[nodiscard]]`` is an attribute (C++17) that asks the compiler to warn when a caller ignores the function's result.

.. code-block:: cpp

   [[nodiscard]] double clamp_joint(double deg) {
     return std::clamp(deg, -max_deg, max_deg);
   }

   clamp_joint(200.0);  // result thrown away

.. code-block:: text

   warning: ignoring return value of 'double clamp_joint(double)', declared with attribute 'nodiscard'

- Use it when ignoring the result is always a bug.
- The standard library uses it too. ``v.empty();`` on its own line warns, because it only **asks**. It does not empty anything.

.. note::

   ``[[nodiscard]]`` is an **attribute**, not a specifier: a note to the compiler in ``[[ ]]`` that does not change what the code does. See `cppreference: attributes <https://en.cppreference.com/w/cpp/language/attributes>`__.

For ``constexpr`` and ``consteval`` functions, see `constexpr and consteval Functions`_ under Further Reading.

Passing Arguments
-----------------

How a parameter is declared decides whether the function gets a **copy** of the argument or reaches the caller's **object**. Rule: `Core Guidelines F.15 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-conventional>`__.

Four Kinds of Parameter
^^^^^^^^^^^^^^^^^^^^^^^

A call initializes each parameter from its argument. Each of the four ways is a declaration you have already written:

.. list-table::
   :header-rows: 1
   :widths: 25 30 30 15

   * - Parameter
     - Works like
     - The function gets
     - Taught in
   * - ``int x``
     - ``int x{a};``
     - a copy
     - Lecture 2
   * - ``int& x``
     - ``int& x{a};``
     - the caller's object
     - Lecture 3
   * - ``const int& x``
     - ``const int& x{a};``
     - the object, read-only
     - Lecture 3
   * - ``int* p``
     - ``int* p{&a};``
     - a copy of an address
     - Lecture 3

- Nothing new happens at a call. Read the parameter as a variable declared with the argument as its initializer.
- So every rule from Lecture 3 carries over: a reference cannot be null, and a pointer can.

Pass by Value
^^^^^^^^^^^^^

With **pass by value**, the parameter is a **new object**, copied from the argument. Changes to it stay inside the function.

.. code-block:: cpp

   void nudge_joint(double deg) {  // double deg{q2};
     deg += 10.0;                  // changes the copy
   }

   int main() {
     double q2{5.0};
     nudge_joint(q2);
     std::cout << q2;                // 5
   }

- This is the default. Without ``&`` or ``*``, every parameter is a copy.
- Use it for small types: ``int``, ``double``, ``bool``, ``char``, and a pointer itself.
- "Small" means about two or three machine words: 16 to 24 bytes on x86-64. Copying that costs no more than passing an address.

The Cost of a Copy
~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   double average_angle(std::vector<double> angles) {  // a copy
     double sum{0.0};
     for (double a : angles) { sum += a; }
     return sum / angles.size();
   }

   std::vector<double> path(1'000'000);
   average_angle(path);  // 8 MB allocated and copied

- A copy of a ``std::vector`` needs **new memory** for the elements and a copy of every one: 8 MB on every call.
- Nothing warns you. The code is correct, just slow.
- The function only **reads** ``angles``, so it has no use for its own copy.

Pass by Reference
^^^^^^^^^^^^^^^^^

With **pass by reference**, the parameter is a **reference**: another name for the caller's object. No copy is made, and changes are visible to the caller.

.. code-block:: cpp

   void nudge_joint(double& deg) {  // double& deg{q2};
     deg += 10.0;                   // changes q2
   }

   double q2{5.0};
   nudge_joint(q2);
   std::cout << q2;                 // 15

- Use it when the function must **change** the caller's object: an **in-out** parameter.
- The call site looks exactly like pass by value. Only the declaration tells you ``q2`` can change.
- The argument must be a variable. ``nudge_joint(5.0)`` does not compile: there is no object to refer to.

A Swap Function
~~~~~~~~~~~~~~~

.. code-block:: cpp

   // By value
   void swap_deg(double a, double b) {
     double tmp{a};
     a = b;
     b = tmp;
   }  // swapped two copies

   double q2{1.0};
   double q3{2.0};
   swap_deg(q2, q3);  // q2 1, q3 2

.. code-block:: cpp

   // By reference
   void swap_deg(double& a, double& b) {
     double tmp{a};
     a = b;
     b = tmp;
   }  // swapped q2 and q3

   double q2{1.0};
   double q3{2.0};
   swap_deg(q2, q3);  // q2 2, q3 1

- Same body, same call. One character in each parameter decides whether the caller sees anything.
- The first version compiles without a warning. It simply does nothing useful.

.. admonition:: Best Practice
   :class: tip

   Pass a parameter the function must change by reference. ``std::swap`` in ``<utility>`` is written this way. Rule: `Core Guidelines F.17 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-inout>`__.

Pass by const Reference
^^^^^^^^^^^^^^^^^^^^^^^

With **pass by const reference**, the parameter is a **reference to const**: no copy is made, and the function may only read the object.

.. code-block:: cpp

   double average_angle(const std::vector<double>& angles) {
     double sum{0.0};
     for (double a : angles) { sum += a; }
     return sum / angles.size();
   }

.. code-block:: text

   error: passing 'const std::vector<double>' as 'this' argument discards qualifiers

- That is what ``angles.push_back(0.0)`` would print inside this function. The ``const`` is checked.
- This is the **default** for anything bigger than a few words that the function only reads.
- Unlike a plain ``std::vector<double>&``, it also accepts a temporary: ``average_angle({1.0, 2.0})`` compiles.

String Parameters
~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   void log_joint(std::string_view name);  // C++17, <string_view>

   std::string joint{"elbow"};
   log_joint(joint);    // views the string: no copy
   log_joint("elbow");  // views the literal: no std::string is built

- A ``std::string_view`` is the Lecture 4 view: a pointer and a length, copied by value.
- It accepts a ``std::string`` or a string literal, and copies neither.
- A ``const std::string&`` parameter would build a temporary copy of ``"elbow"``.
- It owns nothing, so it must not outlive the text it looks at.

std::span (C++20)
~~~~~~~~~~~~~~~~~

A ``std::span`` is a view of a contiguous sequence: a pointer to the first element and a count. It owns nothing.

.. code-block:: cpp

   #include <span>

   double average_angle(std::span<const double> angles) {
     double sum{0.0};
     for (double a : angles) { sum += a; }
     return sum / angles.size();
   }

- ``angles.size()`` gives the count. A range-based ``for`` walks the elements.
- ``const double`` makes it read-only. Drop the ``const`` to allow writes.
- Pass it by value. It is only a pointer and a count, so copying it is cheap.
- It owns nothing, so it must not outlive the sequence it looks at.

.. admonition:: Best Practice
   :class: tip

   A span replaces the old pointer and length pair. See `cppreference: std::span <https://en.cppreference.com/w/cpp/container/span>`__. Rule: `Core Guidelines I.13 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-array>`__.

One Parameter, Three Sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   double c_array[]{1.0, 2.0, 3.0};
   std::array<double, 2> arr{4.0, 6.0};
   std::vector<double> vec{1.5, 2.5, 3.5, 4.5};

   average_angle(c_array);  // 2
   average_angle(arr);      // 5
   average_angle(vec);      // 3

- One parameter accepts a C array, a ``std::array`` or a ``std::vector``.
- The C array keeps its length: ``angles.size()`` is 3 inside the first call.
- Each call builds a span that points at the caller's elements. Nothing is copied.

A Span in Memory
~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::array<double, 2> arr{4.0, 6.0};
   average_angle(arr);  // angles is built from arr

.. figure:: /_static/images/l5/span_memory.png
   :alt: One row of memory with a blue stack tab on the left. First, arr: two adjoining cells holding 4.0 and 6.0, labelled [0] +0 and [1] +8, with the base address 0x7ffd…a10 marked in red under the first cell. After a gap, angles: two cells, data holding the same address 0x7ffd…a10 in red, and size holding 2. A curved black arrow runs from the data field back to the first cell of arr.
   :align: center
   :width: 90%

   The span holds the address of the first element and a count. The elements stay in ``arr``.

``angles`` is 16 bytes whether ``arr`` holds 2 elements or 2 million.

Pass by Pointer
^^^^^^^^^^^^^^^

With **pass by pointer**, the parameter is a pointer, **copied** from the argument. The function reaches the caller's object through it, and the caller may pass ``nullptr`` to mean "no object".

.. code-block:: cpp

   void nudge_joint(double* p) {  // double* p{&q2};
     if (p != nullptr) {
       *p += 10.0;                // changes q2
     }
   }

   double q2{5.0};
   nudge_joint(&q2);              // 15
   nudge_joint(nullptr);          // does nothing

The call site shows ``&q2``, so the reader sees that ``q2`` may change.

.. admonition:: Best Practice
   :class: tip

   Take a pointer only when ``nullptr``, "no object", is a valid argument. Otherwise take a reference. Rule: `Core Guidelines F.60 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-ptr-ref>`__.

Choosing a Method
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 50 25 25

   * - The function...
     - Parameter
     - Core Guideline
   * - only reads a value that is cheap to copy (``int``, ``double``)
     - ``double x``
     - `F.16 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-in>`__
   * - only reads text
     - ``std::string_view s``
     - `SL.str.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-view>`__
   * - only reads the elements of an array or a vector
     - ``std::span<const T> s``
     - `I.13 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-array>`__
   * - only reads anything else, such as a ``std::map``
     - ``const T& x``
     - `F.16 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-in>`__
   * - changes the caller's variable
     - ``T& x``
     - `F.17 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-inout>`__
   * - changes the caller's variable, but may be given none (``nullptr``)
     - ``T* p``
     - `F.60 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-ptr-ref>`__
   * - gives back a result
     - the return value
     - `F.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out>`__

- Read the table top to bottom and take the first row that fits.
- The last row is not a parameter. A function gives back a result through its return value.

Exercise 2: Four Calls
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   void f1(int x) { x = 99; }
   void f2(int& x) { x = 99; }
   void f3(int* p) { p = nullptr; }
   void f4(int* p) { *p = 99; }

   int a{1};
   int b{1};
   int c{1};
   int d{1};
   f1(a);  f2(b);  f3(&c);  f4(&d);
   std::cout << a << ' ' << b << ' ' << c << ' ' << d << '\n';

Write your answer before you run it. Then explain ``f3`` in one sentence, using the table from the start of this section.

Returning Values
----------------

The return type decides whether the caller receives a **new object** or a way to reach an **existing** one. See `cppreference: return statement <https://en.cppreference.com/w/cpp/language/return>`__.

Return by Value
^^^^^^^^^^^^^^^

With **return by value**, the function's result is a **new object**, initialized from the ``return`` operand. The caller owns it.

.. code-block:: cpp

   double clamp_joint(double deg) {
     return std::clamp(deg, -max_deg, max_deg);
   }

   double q2{clamp_joint(200.0)};  // 170

- On x86-64, a small result such as a ``double`` comes back in a CPU **register**, ``xmm0``. The caller reads it from there.
- The function's own locals are destroyed when it returns. The result survives because it is not one of them.
- This is the default. Return by value unless you have a reason not to.

A Large Result
~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<double> plan_path() {
     std::vector<double> angles(1'000'000);
     // ... fill it, one step per millisecond ...
     return angles;  // copy a million doubles?
   }

   std::vector<double> path{plan_path()};

- A vector does not fit in a register. Taken literally, returning it means building it in the function and copying it to ``path``.
- It does not. The compiler usually builds ``angles`` **directly in** ``path``'s memory. At worst it is moved, never copied.

Copy Elision
~~~~~~~~~~~~

**Copy elision**: the compiler builds the returned object **directly in the caller's destination**, so the copy or move from the function's object is never made.

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Name
     - The function returns
     - Elided?
   * - RVO
     - a temporary: ``return std::vector<double>(n);``
     - **always**, since C++17
   * - NRVO
     - a named local: ``return v;``
     - usually, but not required
   * - Implicit move
     - a named local, when NRVO is not done
     - no, the local is **moved**: its elements are handed over
   * - Copy
     - anything that is not the plain name of a local: ``return first ? x : y;``
     - no, every element is **copied**

- **RVO** is Return Value Optimization. The N is for **named**.
- A **move** hands the vector's elements to the new object without copying them. Only three pointers change.
- The order is elide, then move, then copy.

Measured Elision
~~~~~~~~~~~~~~~~

``&v`` is the vector object. ``v.data()`` is where its elements are.

.. code-block:: cpp

   std::vector<double> make_path() {
     std::vector<double> v(1000);
     std::cout << &v << ' ' << v.data() << '\n';
     return v;  // a named local
   }
   std::vector<double> path{make_path()};
   std::cout << &path << ' ' << path.data() << '\n';

.. list-table::
   :header-rows: 1
   :widths: 40 20 20 20

   * - g++ -std=c++20
     - Object
     - Elements
     - Result
   * - default (``-O0`` or ``-O2``)
     - same
     - same
     - elided
   * - ``-fno-elide-constructors``
     - **new**
     - same
     - **moved**

- Same object: elided. New object, same elements: moved. New elements too: copied.
- GCC elides by default, even at ``-O0``. Turn elision off and NRVO falls back to a move.

Elision is not always done. See `cppreference: copy elision <https://en.cppreference.com/w/cpp/language/copy_elision>`__, and `Cases without Elision`_ under Further Reading.

.. note::

   C++20, **[dcl.init]**, section 9.4, paragraph 17.6.1: a prvalue of the same class *is used to initialize the destination object*. NRVO is only *permitted*, by **[class.copy.elision]**, 11.10.5, paragraph 1.1.

Return by Reference
^^^^^^^^^^^^^^^^^^^

With **return by reference**, the function returns a reference to an object that **already exists** and that **outlives the call**.

.. code-block:: cpp

   double& get_joint(std::vector<double>& q, std::size_t i) {
     return q.at(i);
   }

   std::vector<double> q{0.0, 0.5, 1.0};
   get_joint(q, 1) = 0.7;  // q is now 0 0.7 1

- The call names ``q[1]`` itself, not a copy of it, so you can assign to it.
- It returns into the caller's vector, which lives on after ``get_joint`` returns. That is what makes it safe.
- ``std::vector::at`` and ``operator[]`` from Lecture 4 are functions that return a reference in exactly this way.

Returning a Local
~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   double& tool_x() {
     double local_x{0.42};
     return local_x;
   }  // local_x is destroyed here

   double& r{tool_x()};
   std::cout << r;  // undefined behavior

.. code-block:: text

   warning: reference to local variable 'local_x' returned [-Wreturn-local-addr]

The reference outlives the object it names. This is the case Lecture 3 said would come back: a dangling reference.

.. admonition:: Best Practice
   :class: tip

   Never return a reference or pointer to a local. Return it **by value**: copy elision makes that free. Rule: `Core Guidelines F.43 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-dangle>`__.

Returning a Parameter
~~~~~~~~~~~~~~~~~~~~~

No local in sight, and it still dangles:

.. code-block:: cpp

   const std::string& pick_longer(const std::string& a,
                                  const std::string& b) {
     return a.size() >= b.size() ? a : b;
   }

   const std::string& r{pick_longer("lidar", "camera")};
   std::cout << r;  // undefined behavior

- ``"camera"`` is not a ``std::string``. The call builds a **temporary** one, and that temporary dies at the end of the line.
- ``r`` is left naming it. GCC 13 warns: ``possibly dangling reference to a temporary``.
- ``-fsanitize=address`` (Lecture 3) confirms it: ``stack-use-after-scope``.

.. warning::

   Returning a reference parameter is only safe if the caller keeps the argument alive. A temporary argument does not live past the line.

Return by Pointer
^^^^^^^^^^^^^^^^^

With **return by pointer**, the function returns the address of an object that **already exists** and that **outlives the call**, or ``nullptr`` for "not found".

.. code-block:: cpp

   double* find_value(std::vector<double>& v, double target) {
     for (double& x : v) {
       if (x == target) { return &x; }
     }
     return nullptr;  // not found
   }

   std::vector<double> q{0.0, 0.5, 1.0};
   double* p{find_value(q, 0.5)};
   if (p != nullptr) { *p = 0.7; }  // q is now 0 0.7 1

- A pointer can say "nothing" with ``nullptr``. A reference cannot, which is why this one returns a pointer.
- Check a returned pointer before you dereference it, every time.
- Lecture 4's invalidation still applies: a ``push_back`` on ``q`` can leave ``p`` dangling.

Returning the Address of a Local
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   double* tool_x() {
     double local_x{0.42};
     return &local_x;
   }  // local_x is destroyed here

   double* p{tool_x()};
   std::cout << *p;  // undefined behavior

.. code-block:: text

   warning: address of local variable 'local_x' returned [-Wreturn-local-addr]

- The same mistake as returning a reference to a local, and the same rule: never do it.
- With GCC, this program **crashed** with ``SIGSEGV``. GCC returns a null pointer in place of the dead address.

Function Overloading
--------------------

With **function overloading**, several functions share one name but have different parameter lists. The compiler picks one **at compile time** from the arguments of each call.

One Name, Three Functions
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_pose(double x, double y);              // position
   void print_pose(double x, double y, double deg);  // with heading
   void print_pose(std::string_view name,
                   double x, double y);              // labelled

   print_pose(0.42, 1.17);           // the two-value version
   print_pose(0.42, 1.17, 30.0);     // the three-value version
   print_pose("wrist", 0.42, 1.17);  // the labelled version

Without overloading you would write ``print_pose_xy``, ``print_pose_labelled`` and so on. The standard library overloads everywhere: ``std::abs``, and every ``<<`` on ``std::cout``.

Valid Overloads
^^^^^^^^^^^^^^^

Overloads must have different **signatures**: the name plus the parameter types.

.. code-block:: cpp

   void move_joint(int id);
   void move_joint(int id, int deg);
   void move_joint(double deg);
   void move_joint(int id, double deg);
   void move_joint(double deg, int id);

Return Type Only
^^^^^^^^^^^^^^^^

A difference in the return type only does not compile:

.. code-block:: cpp

   int joint_count() { return 3; }
   double joint_count() { return 3.0; }

.. code-block:: text

   error: ambiguating new declaration of
          'double joint_count()'

- The five ``move_joint`` overloads differ by parameter **count**, **type** or **order**. Any one of the three is enough.
- The compiler chooses from the **arguments**, and a call does not say which return type it wants.
- ``void f(int x)`` and ``void f(int y)`` are the same function declared twice.

Overload Resolution
^^^^^^^^^^^^^^^^^^^

For each argument, the compiler ranks how well it matches each candidate. Best first:

.. list-table::
   :header-rows: 1
   :widths: 25 55 20

   * - Rank
     - Examples
     - From
   * - 1. Exact match
     - ``int`` to ``int``; adding ``const``
     - Lecture 2
   * - 2. Promotion
     - ``char``, ``bool`` to ``int``; ``float`` to ``double``
     - Lecture 2
   * - 3. Standard conversion
     - ``int`` to ``double``; ``double`` to ``int``; ``long`` to ``int``
     - Lecture 2

- The winner must be **at least as good on every argument** and better on one.
- No candidate fits: an error. Two candidates tie: an error, ``call of overloaded ... is ambiguous``.
- A narrowing conversion, such as ``double`` to ``int``, still counts as a match. Overloading does not protect you from it.

.. note::

   The full rules run to many pages. These three ranks explain every call in this course. See `cppreference: overload resolution <https://en.cppreference.com/w/cpp/language/overload_resolution>`__.

Exercise 3: Overload Resolution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int add(int a, int b) { return a + b; }
   int add(int a, float b) { return a + b; }
   int add(int a, double b) { return a + b; }

   float f{3.5};
   long n{3};
   unsigned int u{3};

   std::cout << add(2, 3) << '\n';        // 1
   std::cout << add(2, f) << '\n';        // 2
   std::cout << add(2.5, 3) << '\n';      // 3
   std::cout << add('h', false) << '\n';  // 4
   std::cout << add(2, n) << '\n';        // 5
   std::cout << add(2, u) << '\n';        // 6

For each line, name the version that is called and what it prints, or say why it does not compile. Rank each argument with the table above. ``'h'`` is 104.

Default Arguments
-----------------

A **default argument** is a value written in the declaration that the compiler uses when the caller leaves out a **trailing** argument.

Filling from the Right
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_pose(double x, double y, int precision = 3,
                   std::string_view label = "tool");

   print_pose(0.42, 1.17, 2, "wrist");  // 2 dp, wrist
   print_pose(0.42, 1.17, 2);           // 2 dp, tool
   print_pose(0.42, 1.17);              // 3 dp, tool
   print_pose(0.42);                    // error: too few arguments

- Defaults fill from the **right**. Once a parameter has one, every parameter after it needs one too.
- You cannot skip a middle one: there is no way to give ``label`` and leave out ``precision``.

The Program So Far: Defaults
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l5/files_defaults.png
   :alt: Five file cards, with main.cpp, joint_limits.hpp and joint_limits.cpp greyed out as names only. kinematics.hpp adds, in red, the declaration void print_pose(double x, double y, int precision = 3, std::string_view label = "tool");. kinematics.cpp, above it, adds, in red, the definition void print_pose(double x, double y, int precision, std::string_view label) {...}, with no defaults. In both cards a grey ... above it stands for the functions shown on earlier slides.
   :align: center
   :width: 80%

   The defaults are written in the header, and only there.

Defaults in the Declaration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Correct:

.. code-block:: cpp

   // kinematics.hpp
   void print_pose(double x, double y,
                   int precision = 3);

   // kinematics.cpp
   void print_pose(double x, double y,
                   int precision) {
     // ...
   }

Repeated:

.. code-block:: cpp

   // kinematics.cpp
   #include "kinematics.hpp"
   void print_pose(double x, double y,
                   int precision = 3) {
     // ...
   }

.. code-block:: text

   error: default argument given for
          parameter 3 of 'void print_pose(
          double, double, int)'

- The default is part of the **interface**, so it goes in the header, where callers see it.
- The definition must not repeat it. Keep the value as a comment there if you want it visible: ``int precision /* = 3 */``.

.. note::

   C++20, **[dcl.fct.default]**, section 9.3.3.6, paragraph 4: *a default argument cannot be redefined by a later declaration (not even to the same value)*.

Defaults versus Overloads
^^^^^^^^^^^^^^^^^^^^^^^^^

Two functions (overloads):

.. code-block:: cpp

   void print_pose(double x, double y);
   void print_pose(double x, double y,
                   int precision);

One function (default argument):

.. code-block:: cpp

   void print_pose(double x, double y,
                   int precision = 3);

- When the versions only differ by a missing value, use one function with a default. There is one body to maintain.
- Overload when the versions do **different work**, such as ``print_pose(x, y)`` against ``print_pose(name, x, y)``, which also prints a label.

.. admonition:: Best Practice
   :class: tip

   Prefer a default argument to an overload when both would do the same work. Rule: `Core Guidelines F.51 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-default-args>`__. See `cppreference: default arguments <https://en.cppreference.com/w/cpp/language/default_arguments>`__.

Static Local Variables
----------------------

A **static local variable** is a local variable declared ``static``. Its name is visible only inside the function, but it lives for the **whole program** and keeps its value between calls. See `cppreference: storage duration <https://en.cppreference.com/w/cpp/language/storage_duration>`__.

Lifetime and Scope
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int next_move_id() {
     static int id{0};
     return ++id;
   }

   next_move_id();  // 1
   next_move_id();  // 2
   next_move_id();  // 3

- ``id`` is not on the stack. It sits in ``.bss``, because its initializer is 0.
- So returning does not destroy it: its lifetime is the program's. Lecture 2 said it: **lifetime is not scope**.
- A ``static`` with no initializer, such as ``static int count;``, is **zero-initialized** and also sits in ``.bss``.

.. figure:: /_static/images/l5/static_segments.png
   :alt: A horizontal band of memory segments, low addresses on the left: reserved, .text, .rodata, .data, .bss, heap, free space, stack, argv/env. Three white cells sit inside three of them: scale in .rodata, calls in .data and width in .bss. The heap grows right and the stack grows left, toward the free space between them. A legend underneath gives one row per cell. .rodata, static constexpr int scale{2}: read-only, fixed before the program starts. .data, static int calls{7}: a non-zero initializer, the value is in the file. .bss, static double width: no initializer, so all zeros, 0.0. A final note reads: a global lands in .rodata, .data or .bss by the same test; a local without static is on the stack.
   :align: center
   :width: 100%

   Where a static local lives, by how it is initialized.

One-time Initialization
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int count_calls() {
     static int calls{0};  // once
     ++calls;
     return calls;  // 1, 2, 3
   }

   int count_calls_wrong() {
     static int calls;
     calls = 0;  // every call
     ++calls;
     return calls;  // always 1
   }

The **initializer** runs once. An **assignment** is an ordinary statement and runs on every call. See `cppreference: static locals <https://en.cppreference.com/w/cpp/language/storage_duration#Static_local_variables>`__.

For more uses, see `Five Common Uses of static`_ under Further Reading.

The Call Stack
--------------

The **call stack** is the stack segment from Lecture 2, seen one call at a time: every active call has one **stack frame** on it.

Stack Frames
^^^^^^^^^^^^

A **stack frame** is the memory for one call: its parameters, its local variables, and the **return address**, where execution goes on when the call ends.

.. code-block:: cpp

   void C() { }
   void B() { C(); }
   void A() { B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_frames.png
   :alt: Six stacks of boxes side by side, labelled underneath start, A(), B(), C(), C returns and B returns. Each stack is built upward from a box reading main(). The stacks read, bottom to top: main(); main(), A(); main(), A(), B(); main(), A(), B(), C(); main(), A(), B(); and main(), A(). In every stack the top box is outlined in red to mark the running function, and the boxes below it are grey.
   :align: center
   :width: 90%

   The stack at each call and return.

- A call **pushes** a frame on top. A return **pops** it.
- Red marks the running frame. Frames leave last in, first out.

For the registers and the addresses of each frame, see `The Call Stack, Step by Step`_ under Further Reading.

Exercise 4: A Stack Trace
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:

   constexpr int scale{2}; // global

   void f(int& x, int y, int* z) {
     static int calls{0};
     ++calls;
     x += y + *z;
   }

   int g(int a, int b) {
     int result{};
     result = a + b;
     f(result, a, &b);
     return result * scale;
   }

   int main() {
     int x{10};
     int y{20};
     int z{};
     z = g(x, y);
     std::cout << z << '\n';
   }

Draw the stack at line 6. For each frame, write its parameters and locals with their values. Which variable does ``x`` name there? Which variable does ``z`` point at? Where are ``calls`` and ``scale``?

The main Function
-----------------

``main`` is the function the operating system starts the program with. It returns an ``int``, and it can receive the command-line arguments. See `cppreference: main function <https://en.cppreference.com/w/cpp/language/main_function>`__.

Two Forms of main
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int main() { }
   int main(int argc, char* argv[]) { }
   // the second form, with argc and argv unused:
   int main([[maybe_unused]] int argc,
            [[maybe_unused]] char* argv[]) { }

- The return type is always ``int``. ``0`` means success. Anything else is an error code the shell can read with ``echo $?``.
- ``main`` is the one function that may fall off its end. That counts as ``return 0;``.
- You may not call ``main`` yourself, overload it, or make it ``static``.
- The attribute ``[[maybe_unused]]`` (C++17) silences the ``unused parameter`` warning that ``-Wextra`` gives when ``argc`` and ``argv`` are not used.

.. note::

   C++20, **[basic.start.main]**, section 6.9.3.1: paragraph 2 requires every compiler to accept these two forms, and paragraph 5 says flowing off the end of ``main`` *is equivalent to a return with operand 0*. Rule: `Core Guidelines F.46 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-main>`__.

Command-line Arguments
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int main(int argc, char* argv[]) {
     std::cout << "Number of arguments: " << argc << '\n';
     for (int i{0}; i < argc; ++i) {
       std::cout << "argv[" << i << "]: " << argv[i] << '\n';
     }
   }

.. code-block:: bash

   ./week5_snippets 30 -45 60

.. code-block:: text

   Number of arguments: 4
   argv[0]: ./week5_snippets
   argv[1]: 30
   argv[2]: -45
   argv[3]: 60

- ``argc`` counts the arguments, including the program's own name, so it is normally at least 1.
- ``argv`` is an array of C-strings from Lecture 4. As a parameter it has decayed: its real type is ``char**``.
- ``argv[argc]`` is always a null pointer.

.. note::

   Copy them into something safer first. Two pointers are an iterator range, as Lecture 4 showed: ``std::vector<std::string_view> args(argv, argv + argc);``

Documenting Functions
---------------------

**Doxygen** builds reference pages from specially marked comments above each declaration. This course uses it for every function you write. See the `Doxygen manual <https://www.doxygen.nl/manual/index.html>`__.

Other tools: `Sphinx with Breathe <https://breathe.readthedocs.io/>`__, which builds on Doxygen's output, and `MrDocs <https://www.mrdocs.com/>`__ and `clang-doc <https://clang.llvm.org/extra/clang-doc.html>`__, which read the code with the Clang compiler.

.. seealso::

   The reading material :doc:`Documentation with Sphinx and Breathe </reading_material/sphinx_breathe/sb_index>` builds the pages for ``arm_demo`` with Sphinx, from the XML that Doxygen writes.

Setting Up Doxygen
^^^^^^^^^^^^^^^^^^

Installation
~~~~~~~~~~~~

.. code-block:: bash

   sudo apt install doxygen doxygen-gui graphviz
   doxygen --version        # 1.9.8 on Ubuntu 24.04
   code --install-extension cschlosser.doxdocgen

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Package
     - Gives you
     - Used for
   * - ``doxygen``
     - ``doxygen``
     - generating the pages, from the command line
   * - ``doxygen-gui``
     - ``doxywizard``
     - writing a ``Doxyfile`` and running Doxygen from a window
   * - ``graphviz``
     - ``dot``
     - optional: the call and include graphs in the pages
   * - VS Code extension
     - ``cschlosser.doxdocgen``
     - optional: types the comment skeleton for you

.. note::

   There is no package called ``doxywizard``. The program of that name comes in ``doxygen-gui``. See `Doxygen: installation <https://www.doxygen.nl/manual/install.html>`__.

Project Layout
~~~~~~~~~~~~~~

.. code-block:: text

   project/week5/
   ├── CMakeLists.txt
   ├── playground/
   │   └── src/snippets.cpp
   └── arm_demo/
       ├── include/
       │   ├── joint_limits.hpp
       │   └── kinematics.hpp
       ├── src/
       │   ├── joint_limits.cpp
       │   ├── kinematics.cpp
       │   └── main.cpp
       └── docs/
           ├── Doxyfile
           └── html/   (generated)

- ``include``: headers, the declarations and their comments.
- ``src``: source files, the definitions.
- ``docs``: the ``Doxyfile``, and the pages it generates in ``docs/html``.
- Commit the ``Doxyfile``, never the pages it generates.

**The one edit.** Done in the Header Files section. If not: uncomment the last four lines of ``project/week5/CMakeLists.txt``, then in VS Code run **CMake: Configure** and build ``week5_arm_demo``.

Doxygen Comments
^^^^^^^^^^^^^^^^

A **Doxygen comment** is a comment that starts with ``/**``. Doxygen reads it and turns it into the page for the declaration below it.

.. code-block:: cpp

   /**
    * @brief Convert an angle from degrees to radians.
    * @param deg The angle in degrees. Any finite value.
    * @return The same angle in radians.
    */
   double convert_deg_to_rad(double deg);

- ``@brief``: one line on what it does. ``@param``: one per parameter, by name. ``@return``: what comes back.
- Write it on the **declaration**, in the header, and only there. Two copies drift apart.
- Say what the signature cannot: units, the valid range, what happens on bad input. See `Doxygen: documenting the code <https://www.doxygen.nl/manual/docblocks.html>`__.

The File Comment
~~~~~~~~~~~~~~~~

.. code-block:: cpp

   #pragma once

   /**
    * @file kinematics.hpp
    * @brief Angle conversions for the robot arm.
    */

   /**
    * @brief Convert an angle from degrees to radians.
    * ...

- Every header starts with a ``@file`` comment: the file's name and one line on what it holds.
- Without it, the header gets **no page**, and a function documented only there disappears. Doxygen prints no warning.

.. warning::

   This is the most common reason for "I wrote the comments and nothing shows up". A function outside a class belongs to its file, and Doxygen only lists the members of a file that is itself documented. See `Doxygen: @file <https://www.doxygen.nl/manual/commands.html#cmdfile>`__.

The VS Code Extension
~~~~~~~~~~~~~~~~~~~~~

**Doxygen Documentation Generator**, ID ``cschlosser.doxdocgen``, writes the skeleton for you:

.. code-block:: bash

   code --install-extension cschlosser.doxdocgen

Type ``/**`` on the line above a declaration and press **Enter**:

.. code-block:: cpp

   /**
    * @brief
    *
    * @param deg
    * @return double
    */
   double convert_deg_to_rad(double deg);

- It copies what the signature already says: the parameter names, and the return **type**. You write the meaning.
- Replace ``@return double`` with what the value is: ``@return The same angle in radians.``

The Doxyfile
^^^^^^^^^^^^

The **Doxyfile** is the configuration file Doxygen reads: plain text, one ``KEY = value`` per line, such as ``INPUT = ../include ../src``.

.. code-block:: bash

   cd project/week5/arm_demo/docs
   doxygen -g Doxyfile     # create a new one, every setting at its default
   doxywizard Doxyfile     # edit an existing one, in the GUI
   doxygen Doxyfile        # generate the HTML pages, in docs/html

doxywizard, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~~

Follow along in ``doxywizard``, the Doxygen GUI:

1. ``cd project/week5/arm_demo/docs`` and run ``doxywizard &``.
2. **Step 1** at the top, the working directory: the ``docs`` folder. Reopening ``docs/Doxyfile`` later sets it for you.
3. **Wizard, Project**: a project name. Leave the destination directory empty.
4. **Wizard, Mode**: *Documented entities only*, and *Optimize for C++ output*.
5. **Wizard, Output**: *HTML* with a navigation panel. Untick *LaTeX*.
6. **Expert, Input**: set ``INPUT`` to ``../include`` and ``../src``, and tick ``RECURSIVE``.
7. **File, Save as**: ``docs/Doxyfile``.

.. warning::

   Check what was saved: ``grep '^INPUT ' Doxyfile``. The paths must be **relative**. A path the file browser filled in, such as ``/home/you/week5/src``, breaks on every other machine. See `Doxygen: doxywizard <https://www.doxygen.nl/manual/doxywizard_usage.html>`__.

Running Doxygen
^^^^^^^^^^^^^^^

Doxygen reads the ``Doxyfile``, collects the comments from ``INPUT``, and writes the pages to ``docs/html``.

From the command line:

.. code-block:: bash

   cd project/week5/arm_demo
   cd docs
   doxygen Doxyfile
   xdg-open html/index.html

From ``doxywizard``:

- Open the tab **Run**.
- Press **Run Doxygen**. It asks you to save first.
- Press **Show HTML output**.

Run Doxygen again after every change to a comment. The pages do not update themselves.

The Working Directory
~~~~~~~~~~~~~~~~~~~~~

The paths in a ``Doxyfile`` are relative to the folder Doxygen **runs in**, not the folder the file is in. From ``project/week5/arm_demo``:

.. code-block:: bash

   doxygen docs/Doxyfile

.. code-block:: text

   warning: tag INPUT: input source '../include' does not exist
   warning: tag INPUT: input source '../src' does not exist

- Doxygen finds no source, and writes an empty ``html`` folder into the project root.
- Always run it from ``docs``: ``cd docs && doxygen Doxyfile``.
- ``doxywizard`` gets this right when you open ``docs/Doxyfile``: it sets the working directory to the file's folder.

Summary
-------

**Declaring and Building**

- Declare in a header with ``#pragma once``. Define once, in a ``.cpp``. A compiler error means the declaration is missing. ``undefined reference`` means the definition is.
- Every path of a non-``void`` function returns a value. Falling off the end is undefined behavior everywhere except ``main``.

**Passing and Returning**

- A parameter is initialized from its argument. Small and read: by value. Large and read: ``const T&``, ``std::string_view`` or ``std::span``. Changed: ``T&``. Changed or absent: ``T*``.
- Return results by value. Copy elision makes it free for a temporary, and nearly free for a named local.
- Never return a reference or pointer to anything that dies when the call ends, including a temporary argument.

**Overloading and Defaults**

- Overloads differ in their parameter types, never only in the return type. The compiler ranks exact, promotion, conversion. A tie does not compile.
- A default argument goes in the declaration, fills from the right, and is often better than a second overload.

**Under the Hood**

- Every call pushes a frame with its parameters, locals and return address. Every return pops it. A ``static`` local is in no frame.
- ``main`` receives the command line: ``argc`` counts the program name too, and ``argv[argc]`` is a null pointer.

**Documenting**

- A ``@file`` comment on every header, and ``@brief``, ``@param``, ``@return`` on every declaration. Keep the ``Doxyfile`` in ``docs`` and run Doxygen from there.

Further Reading
---------------

The sections below come from the appendix of the slides. They are **not presented** in the lecture. Read them on your own.

constexpr and consteval Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``constexpr`` function is a function the compiler **can** run while compiling, when its arguments are constants. Given run-time values, it runs like any other function.

.. code-block:: cpp

   constexpr double convert_deg_to_rad(double deg) {
     return deg * std::numbers::pi / 180.0;
   }

   constexpr double limit{convert_deg_to_rad(170.0)};  // at compile time

- ``170.0`` is a literal, so the compiler knows the argument.
- ``limit`` is ``constexpr``, so the compiler **must** run the call while compiling.
- The program stores the result, 2.967. Nothing is computed at run time.
- Without ``constexpr`` on the function, this line does not compile.

The same function at run time:

.. code-block:: cpp

   double input{};
   std::cin >> input;
   double r{convert_deg_to_rad(input)};  // at run time

   double x{convert_deg_to_rad(170.0)};  // may run early, not required to

- ``input`` is known only when the program runs, so ``r`` gets an ordinary function call.
- ``constexpr`` on a function **allows** compile time. It does not **require** it.
- ``x`` is not ``constexpr``, so the compiler may compute it early, but it does not have to.
- One function, two uses. Without ``constexpr``, ``limit`` needs a hand-typed ``2.967``.
- A ``constexpr`` function cannot read input, print, or change globals.

Rule: `Core Guidelines F.4 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-constexpr>`__. See `cppreference: constexpr <https://en.cppreference.com/w/cpp/language/constexpr>`__.

A ``consteval`` function (C++20) is a function the compiler **must** run while compiling. Every call needs constant arguments.

.. code-block:: cpp

   consteval int steps_for(int deg) { return deg * 10; }

   std::array<int, steps_for(3)> plan{};  // 30 elements

   int n{3};
   int bad{steps_for(n)};  // error: n is not a constant

- ``constexpr`` **allows** compile time. ``consteval`` **requires** it.
- ``n`` holds 3, but it is not ``constexpr``, so the compiler cannot use its value.
- Use ``consteval`` when a run-time call would be a bug. See `cppreference: consteval <https://en.cppreference.com/w/cpp/language/consteval>`__.

Cases without Elision
^^^^^^^^^^^^^^^^^^^^^

Two candidates:

.. code-block:: cpp

   std::vector<double> pick(bool first) {
     std::vector<double> x(1000);
     std::vector<double> y(1000);
     return first ? x : y;  // copy
   }

.. code-block:: cpp

   std::vector<double> pick(bool first) {
     std::vector<double> x(1000);
     std::vector<double> y(1000);
     if (first) { return x; }  // move
     return y;
   }

Assignment:

.. code-block:: cpp

   // e exists: move-assign
   std::vector<double> e;
   e = make_path();

   // f is new: elided
   std::vector<double> f{make_path()};

- With two candidates, NRVO is not done. The implicit move then needs a plain name: ``first ? x : y`` is not one, so it is **copied**.
- An object that already exists cannot be built again. Assigning to it moves.

.. note::

   Return a plain name, and initialize from the call. C++20, **[class.copy.elision]**, 11.10.5, paragraph 3.1, gives the plain-name rule.

Five Common Uses of static
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Use
     - What you write
     - Why it is static
   * - A running count, or the next id
     - ``static int id{0};``
     - the number must survive the return
   * - A table too slow to rebuild
     - ``static const auto t{load()};``
     - built on the first call, then reused
   * - Warn once
     - ``static bool warned{false};``
     - later calls stay quiet
   * - Remember the last answer
     - ``static double last{};``
     - the next call can skip the work
   * - One-time setup
     - ``static bool ready{setup()};``
     - the initializer runs exactly once

- All five keep one value between calls. That is the only thing ``static`` buys you.
- Not for a value the caller should pass in, and not for anything two callers could disagree about.

.. note::

   A **static data member** of a class is the same lifetime rule with a different scope: one object shared by every instance, such as a count of how many exist. Lecture 6. See `cppreference: static <https://en.cppreference.com/w/cpp/language/static>`__.

The Call Stack, Step by Step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Stack Pointer and the Frame Pointer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **stack pointer** (``rsp``) is a CPU register that holds the address of the top of the stack. A push moves it down 8 bytes. A pop moves it back up. The **frame pointer** (``rbp``) is a CPU register that holds a fixed address inside the running frame. Each local is at a fixed distance from it.

.. code-block:: text

   B():
     push rbp       ; save A's rbp
     mov  rbp,rsp   ; B's fixed point
     sub  rsp,0x10  ; 16 bytes for b
     mov  DWORD PTR [rbp-0x4],0x2  ; b{2}
     call C()
     leave          ; rsp = rbp, pop rbp
     ret            ; pop return address

- ``rsp`` moves on every push, pop, call and return. ``rbp`` stays put while the function runs.
- That is why locals are found from ``rbp``: ``b`` is always at ``rbp - 4``.
- ``rbp`` points at the saved ``rbp``, the caller's own. Each frame links to the one that called it.
- At ``-O2``, GCC does not set ``rbp`` up at all. It finds ``b`` from ``rsp``.

Step 0: Inside main()
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 4

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_0.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(); main() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. rbp and rsp both point at the edge marked …c710.
   :align: center
   :width: 50%

- ``main`` has no locals. Its frame is the return address and the saved ``rbp``, so ``rsp`` and ``rbp`` both hold ``…c710``.
- Each address sits on the **top edge** of its 8-byte slot: the slot's first byte.
- The stack grows toward **lower** addresses: up, in these drawings.

.. note::

   Measured with ``gdb``: g++ 13, ``-O0``, x86-64 Linux. Each address shows only its last four hex digits.

Step 1: The Call to A()
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 3

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_1.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(), A(); A() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. A(), 32 bytes: padding, a 1, saved rbp …c710, return to main …5177. rbp points at the edge marked …c700, the saved rbp, and rsp at the edge marked …c6f0, the top of the stack.
   :align: center
   :width: 50%

- ``call`` pushes the **return address**: the next instruction in ``main``.
- ``A`` pushes the old ``rbp``, then sets ``rbp`` to ``rsp``.
- It subtracts 16 from ``rsp`` for ``a``. The 12 unused bytes keep ``rsp`` a multiple of 16.

Step 2: The Call to B()
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 2

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_2.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(), A(), B(); B() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. A(), 32 bytes: padding, a 1, saved rbp …c710, return to main …5177. B(), 32 bytes: padding, b 2, saved rbp …c700, return to A …5167. rbp points at the edge marked …c6e0, the saved rbp, and rsp at the edge marked …c6d0, the top of the stack.
   :align: center
   :width: 50%

- The same three steps: return address, saved ``rbp``, 16 bytes for ``b``.
- Each saved ``rbp`` holds the address of the one before. A debugger follows that chain to list the frames.

Step 3: The Call to C()
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 1

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_3.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(), A(), B(), C(); C() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. A(), 32 bytes: padding, a 1, saved rbp …c710, return to main …5177. B(), 32 bytes: padding, b 2, saved rbp …c700, return to A …5167. C(), 16 bytes: saved rbp …c6e0, return to B …514c. rbp and rsp both point at the edge marked …c6c0.
   :align: center
   :width: 50%

- ``C`` has no locals, so ``rsp`` stays equal to ``rbp``.
- Four frames, 96 bytes in all. Each frame's size is fixed when its function is compiled.

Step 4: The Return from C()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 2

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_4.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(), A(), B(); B() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. A(), 32 bytes: padding, a 1, saved rbp …c710, return to main …5177. B(), 32 bytes: padding, b 2, saved rbp …c700, return to A …5167. Greyed and dashed above them, marked popped but still holding their old values: C(). rbp points at the edge marked …c6e0, the saved rbp, and rsp at the edge marked …c6d0, the top of the stack.
   :align: center
   :width: 50%

- ``C`` pops its saved ``rbp``, so ``rbp`` marks ``B``'s frame again.
- ``ret`` pops the return address and jumps to it: back in ``B``, just after ``C();``.
- The old slots are **not erased**. The next call writes over them.

Step 5: The Return from B()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 3

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_5.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(), A(); A() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. A(), 32 bytes: padding, a 1, saved rbp …c710, return to main …5177. Greyed and dashed above them, marked popped but still holding their old values: B(), C(). rbp points at the edge marked …c700, the saved rbp, and rsp at the edge marked …c6f0, the top of the stack.
   :align: center
   :width: 50%

- ``leave`` sets ``rsp`` to ``rbp`` and pops the saved ``rbp``. That frees ``b`` in one step.
- ``ret`` jumps back into ``A``.
- A pointer to ``b`` would still find 2, until a call reuses the slot. A dangling pointer can seem to work.

Step 6: The Return from A()
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 4

   void C() { }
   void B() { int b{2}; C(); }
   void A() { int a{1}; B(); }
   int main() { A(); }

.. figure:: /_static/images/l5/stack_call_6.png
   :alt: Twelve 8-byte stack slots, the lowest address …c6c0 at the top and the highest …c718 at the bottom, so each call stacks a new frame on top of the last. Each address is written on the top edge of its slot, the slot's first byte. Live frames, bottom to top: main(); main() is outlined in red as the running frame. main(), 16 bytes: saved rbp …c7b0, return to startup …a1ca. Greyed and dashed above them, marked popped but still holding their old values: A(), B(), C(). rbp and rsp both point at the edge marked …c710.
   :align: center
   :width: 50%

- ``rsp`` and ``rbp`` are back where Step 0 left them.
- A call and a return only move two registers. Nothing is searched for, and nothing is freed.

The Cost of a Call
~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   void g(int a) {
     int b{a + 1};  // b lives in g's frame
   }                // b destroyed here

   void f() {
     int x{10};     // x lives in f's frame
     g(x);          // g's frame stacks on top of f's
   }                // x destroyed here

- Entering a function **subtracts** a size fixed at compile time from the stack pointer. Returning **adds** it back. One instruction each way.
- Nothing is searched for. The next frame always starts where the last one ended.
- Because frames leave in order, the stack **cannot fragment**, unlike the heap.

.. note::

   A local costs almost nothing to create, which is why you should reach for one first. The ``new`` from Lecture 3 has to find free space on the heap, which costs far more than moving one register.

Frame Addresses
~~~~~~~~~~~~~~~

Print the address of one local per call, and you can watch each new frame land at a **lower** address:

.. code-block:: cpp

   void descend(int depth) {
     int local{depth};
     std::cout << "depth " << depth << "  &local = " << &local << '\n';
     if (depth < 3) { descend(depth + 1); }
   }

.. code-block:: text

   depth 1  &local = 0x7ffc5ff841a4
   depth 2  &local = 0x7ffc5ff84174
   depth 3  &local = 0x7ffc5ff84144

- Each address is ``0x30``, 48 bytes, below the last: the frame the compiler reserved for ``descend``.
- Every call gets a new ``local`` in a new frame, though they share one name.
- Printing a pointer with ``<<`` shows the address in hexadecimal, as in Lecture 3.

Recursion
^^^^^^^^^

A **recursive** function calls itself. Every call gets its own frame, and a **base case** ends the chain of calls.

.. code-block:: cpp

   long long compute_factorial(int n) {
     if (n <= 1) {        // base case
       return 1;
     }
     return n * compute_factorial(n - 1);
   }

   long long r{compute_factorial(4)};

Write ``f`` for ``compute_factorial``:

.. code-block:: text

   f(4) calls f(3)
     f(3) calls f(2)
       f(2) calls f(1)
         f(1) returns 1
       f(2) returns 2 x 1 = 2
     f(3) returns 3 x 2 = 6
   f(4) returns 4 x 6 = 24

- Four frames of ``compute_factorial`` are on the stack at once, each with its own ``n``.
- Every call must move **toward** the base case. Here, ``n`` shrinks by one each time.

Frames of a Recursive Call
~~~~~~~~~~~~~~~~~~~~~~~~~~

``compute_factorial(4)``, with ``f`` standing for ``compute_factorial``. Each row is the stack after one step, bottom first:

.. code-block:: text

   call f(4)            main(), f(4)
   call f(3)            main(), f(4), f(3)
   call f(2)            main(), f(4), f(3), f(2)
   call f(1), base case main(), f(4), f(3), f(2), f(1)
   f(1) returns 1       main(), f(4), f(3), f(2)
   f(2) returns 2       main(), f(4), f(3)
   f(3) returns 6       main(), f(4)

Stack Overflow
~~~~~~~~~~~~~~

.. code-block:: cpp

   int depth{0};

   void dig() {
     ++depth;
     dig();  // no base case
   }

- Built at ``-O0`` with the Linux default 8 MiB stack, this crashed with ``Segmentation fault`` after about **520,000** calls.
- That is the arithmetic: 8 MiB is 8,388,608 bytes, and each frame of ``dig`` is 16 bytes, so 524,288 frames fit.
- A correct base case is not enough if it is too far away. A bigger frame, or a deeper input, reaches the limit sooner.

.. note::

   A second limit hides in ``compute_factorial``: ``compute_factorial(21)`` does not fit in a ``long long``. It printed ``-4249290049419214848``, which is signed overflow, undefined behavior from Lecture 2.

Recursion versus a Loop
~~~~~~~~~~~~~~~~~~~~~~~

Good fits for recursion:

- The data is recursive: a tree, a folder of folders, a map split into quadrants.
- Divide and conquer: merge sort, quicksort.
- The recursive version is much clearer, and the depth is small and known.

Good fits for a loop:

- A walk along a sequence: a sum, or a search in a vector. The depth is its length.
- The depth depends on the input, which a user or a sensor controls.
- Every call costs a frame. A loop reuses one.

.. code-block:: cpp

   double sum_readings(std::span<const double> readings) {
     double total{0.0};
     for (double r : readings) {
       total += r;
     }
     return total;
   }

.. note::

   Ask first: can a loop do this just as clearly? If so, use the loop.

The Costs of Recursion
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   long long compute_fibonacci(int n) {
     if (n < 2) { return n; }
     return compute_fibonacci(n - 1) + compute_fibonacci(n - 2);
   }

- **Memory.** Every call is a frame: 48 bytes for ``compute_factorial`` at ``-O0``. The stack caps the depth, and running out is a crash, not an error you can handle.
- **Repeated work.** ``compute_fibonacci(40)`` makes **331,160,281** calls and took 0.13 s at ``-O2``. A loop does 40 additions in under a microsecond.
- **Harder to follow.** The state is spread across many frames. A loop keeps it in a few variables you can watch.
- **Banned where failure is costly.** Rule 1 of NASA JPL's `Power of Ten <https://spinroot.com/gerard/pdf/P10.pdf>`__ forbids *direct or indirect recursion*.

.. note::

   Use recursion only where the data is recursive, such as a tree or a folder of folders, or for divide and conquer, and only when the depth is small and known. Factorial and Fibonacci are teaching examples. In real code, write them as loops.

A Folder Tree
~~~~~~~~~~~~~

.. code-block:: cpp

   namespace fs = std::filesystem;

   void print_tree(const fs::path& dir, int depth) {
     for (const auto& entry : fs::directory_iterator(dir)) {
       std::cout << std::string(2 * depth, ' ')
         << entry.path().filename().string() << '\n';
       if (entry.is_directory()) {
         print_tree(entry.path(), depth + 1);
       }
     }
   }

.. code-block:: text

   $ ./tree arm_demo
   include
     joint_limits.hpp
     kinematics.hpp
   docs
     Doxyfile
   src
     joint_limits.cpp
     kinematics.cpp
     main.cpp

- A folder holds files and folders, and each of those folders is the same problem again. The recursion follows the data.
- Nobody knows the depth in advance. A loop would have to keep its own list of folders still to visit.
- ``std::filesystem`` (C++17) lists folders. The order is whatever the file system returns, not sorted.
