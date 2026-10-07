.. _l5_quiz:

================
Lecture 5 Quiz
================

Multiple Choice
----------------

.. admonition:: Question 1
   :class: hint

   Which of these is **not** one of the four parts of a function?

   A. The return type
   B. The name
   C. The parameter list
   D. The ``#include`` line above it

   .. dropdown:: Answer
      :class-container: sd-border-success

      **D. The #include line above it**

      A function has four parts: a return type, a name, a parameter list in parentheses, and a body in braces. An ``#include`` belongs to the file, not to any function.

.. admonition:: Question 2
   :class: hint

   Which of these is part of a function's **signature**?

   A. The return type
   B. The parameter types
   C. The parameter names
   D. The body

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. The parameter types**

      The signature is the name, the enclosing namespace, and the parameter types. The return type and the parameter names are not part of it. The signature is what the linker uses, and what appears in a message such as ``undefined reference to `convert_deg_to_rad(double)'``.

.. admonition:: Question 3
   :class: hint

   ``main.cpp`` declares ``double clamp_joint(double deg);`` and calls it, but no file defines it. What happens?

   A. The compiler rejects ``main.cpp``
   B. ``main.cpp`` compiles, and the **link** step fails with ``undefined reference``
   C. The program runs and ``clamp_joint`` returns 0
   D. The compiler writes an empty body for it

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. main.cpp compiles, and the link step fails with undefined reference**

      A declaration is a promise. It is enough for the compiler to check the call. The linker then looks for the body in every object file, finds none, and stops.

.. admonition:: Question 4
   :class: hint

   ``kinematics.hpp`` has ``#pragma once`` and contains the **body** of ``convert_deg_to_rad``. Both ``main.cpp`` and ``planner.cpp`` include it. What happens when you build?

   A. It builds: ``#pragma once`` keeps only one copy of the body
   B. The compiler rejects the header
   C. The linker reports ``multiple definition of `convert_deg_to_rad(double)'``
   D. It builds, but calls go to whichever copy the linker sees first

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The linker reports multiple definition**

      ``#pragma once`` only works within one source file. Each ``.cpp`` is compiled on its own, so each object file gets its own copy of the body, and the linker finds two definitions. That breaks the one-definition rule. Keep bodies in the ``.cpp``.

.. admonition:: Question 5
   :class: hint

   In ``CMakeLists.txt``, what does ``target_include_directories(week5_arm_demo PRIVATE arm_demo/include)`` do?

   A. It compiles every ``.hpp`` in ``include``
   B. It tells the compiler where to look for the headers named in ``#include "..."``
   C. It copies the headers into the build folder
   D. It adds the headers to ``add_executable``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It tells the compiler where to look for the headers**

      A header is included, never compiled on its own, so it is never listed in ``add_executable``. Without this line, ``#include "kinematics.hpp"`` fails with ``No such file or directory``.

.. admonition:: Question 6
   :class: hint

   What does this function do when it is called with ``0``?

   .. code-block:: cpp

      int get_sign(int number) {
        if (number > 0) {
          return 1;
        } else if (number < 0) {
          return -1;
        }
      }

   A. It returns 0
   B. It returns -1
   C. The behavior is undefined
   D. It does not compile

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The behavior is undefined**

      For ``0`` the function falls off the end without a ``return``. That is undefined behavior for any non-void function other than ``main``. GCC warns: ``control reaches end of non-void function [-Wreturn-type]``.

.. admonition:: Question 7
   :class: hint

   ``int truncate_value() { double value{99.99}; return value; }`` is compiled with the course flags, ``-Wall -Wextra -pedantic-errors -Wshadow``. What happens?

   A. It does not compile
   B. It compiles with no warning and returns 99
   C. It compiles with no warning and returns 100
   D. It warns and returns 99.99

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It compiles with no warning and returns 99**

      The ``double`` is converted to the ``int`` return type, and the fraction is lost. None of the four flags reports it. ``-Wconversion`` does: ``conversion from 'double' to 'int' may change value``. If you mean to drop the fraction, write ``return static_cast<int>(value);``.

.. admonition:: Question 8
   :class: hint

   What does ``[[nodiscard]]`` on a function do?

   A. It stops the function from being called twice
   B. It asks the compiler to warn when a caller ignores the result
   C. It makes the result read-only
   D. It prevents the compiler from removing the function

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It asks the compiler to warn when a caller ignores the result**

      Use it when ignoring the result is always a bug. ``clamp_joint(200.0);`` on its own line then warns ``ignoring return value``. The standard library uses it too: ``v.empty();`` on its own line warns, because it only asks, it does not empty anything.

.. admonition:: Question 9
   :class: hint

   What does this print?

   .. code-block:: cpp

      void nudge_joint(double deg) {
        deg += 10.0;
      }

      double q2{5.0};
      nudge_joint(q2);
      std::cout << q2;

   A. 5
   B. 15
   C. 10
   D. It does not compile

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A. 5**

      The parameter is passed by value. ``deg`` is a new object, initialized from ``q2`` as if you wrote ``double deg{q2};``, so the function changes its own copy. Change the parameter to ``double& deg`` and the program prints 15.

.. admonition:: Question 10
   :class: hint

   A function only reads a ``std::vector<double>`` of a million elements. How should it take it?

   A. ``std::vector<double> angles``
   B. ``std::vector<double>& angles``
   C. ``const std::vector<double>& angles``
   D. ``std::vector<double>* angles``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. const std::vector<double>& angles**

      By value would allocate and copy 8 MB on every call. A reference to ``const`` makes no copy, and the compiler stops the function from changing the vector. ``std::span<const double>`` is also a good choice, and accepts a C array or a ``std::array`` as well.

.. admonition:: Question 11
   :class: hint

   What does a ``std::span<const double>`` hold?

   A. A copy of every element
   B. A pointer to the first element and a count
   C. A reference to a ``std::vector``
   D. The elements, on the heap

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. A pointer to the first element and a count**

      A span owns nothing. It is 16 bytes whether the sequence holds 2 elements or 2 million, so pass it by value. It must not outlive the sequence it looks at.

.. admonition:: Question 12
   :class: hint

   In C++17 and later, which return is **guaranteed** to be elided?

   A. ``return std::vector<double>(n);``, a temporary
   B. ``return v;``, a named local
   C. ``return first ? x : y;``
   D. None: elision is always optional

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A. return std::vector<double>(n);**

      Returning a temporary (RVO) is always elided since C++17: the object is built directly in the caller's destination. Returning a named local (NRVO) is usually elided but not required, and when it is not done the local is moved. ``first ? x : y`` is not a plain name, so it is copied.

.. admonition:: Question 13
   :class: hint

   What is wrong with this function?

   .. code-block:: cpp

      double& tool_x() {
        double local_x{0.42};
        return local_x;
      }

   A. Nothing
   B. It returns a reference to a local that is destroyed when the function returns
   C. A function cannot return a reference
   D. ``local_x`` must be ``const``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It returns a reference to a local that is destroyed when the function returns**

      The caller gets a dangling reference, and using it is undefined behavior. GCC warns: ``reference to local variable 'local_x' returned [-Wreturn-local-addr]``. Return by value instead: copy elision makes that free.

.. admonition:: Question 14
   :class: hint

   When should a function return a pointer rather than a reference?

   A. Always: pointers are faster
   B. When the result may be "nothing", written as ``nullptr``
   C. When the object is a local of the function
   D. Never: pointers are deprecated

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. When the result may be "nothing", written as nullptr**

      A search, such as ``find_value``, can return ``nullptr`` for "not found". A reference cannot say that. The caller must check the pointer before dereferencing it. Returning the address of a local dangles exactly like returning a reference to one.

.. admonition:: Question 15
   :class: hint

   Given the three overloads below, what happens with ``long n{3}; add(2, n);``?

   .. code-block:: cpp

      int add(int a, int b);
      int add(int a, float b);
      int add(int a, double b);

   A. ``add(int, int)`` is called
   B. ``add(int, double)`` is called
   C. ``add(int, float)`` is called
   D. It does not compile: the call is ambiguous

   .. dropdown:: Answer
      :class-container: sd-border-success

      **D. It does not compile: the call is ambiguous**

      ``long`` to ``int``, to ``float`` and to ``double`` are all conversions, the same rank, so no overload is better than the others. GCC reports ``call of overloaded 'add(int, long int&)' is ambiguous``.

.. admonition:: Question 16
   :class: hint

   ``print_pose`` is declared in ``kinematics.hpp`` as ``void print_pose(double x, double y, int precision = 3);``. How should its definition in ``kinematics.cpp`` start?

   A. ``void print_pose(double x, double y, int precision = 3) {``
   B. ``void print_pose(double x, double y, int precision) {``
   C. ``void print_pose(double x, double y) {``
   D. Either A or B

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. void print_pose(double x, double y, int precision) {**

      The default belongs in the declaration, where callers see it. Repeating it in the definition is an error even with the same value: ``default argument given for parameter 3``. Keep the value as a comment if you want it visible: ``int precision /* = 3 */``.

.. admonition:: Question 17
   :class: hint

   In which segment does ``static int id{0};``, declared inside a function, live?

   A. The stack
   B. The heap
   C. ``.bss``
   D. ``.data``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. .bss**

      A static local is not on the stack: it lives for the whole program. An initializer of 0, or no initializer at all, puts it in ``.bss``. A non-zero initializer, such as ``static int calls{7};``, puts it in ``.data``, because the value must be stored in the file.

.. admonition:: Question 18
   :class: hint

   The program is run as ``./week5_arguments 30 -45 60``. What is ``argc``?

   A. 3
   B. 4
   C. 1
   D. It depends on the compiler

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 4**

      ``argc`` counts the program name too, so ``argv[0]`` is ``./week5_arguments`` and ``argv[1]`` to ``argv[3]`` are the three angles, as text. ``argv[argc]`` is always a null pointer.

.. admonition:: Question 19
   :class: hint

   Where should the Doxygen comment for a function go?

   A. Above the definition, in the ``.cpp``
   B. Above the declaration, in the header
   C. In both places, so they stay together
   D. In the ``Doxyfile``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Above the declaration, in the header**

      Write it on the declaration, and only there: two copies drift apart. It starts with ``/**`` and uses ``@brief`` for one line on what the function does, ``@param`` once per parameter, and ``@return`` for what comes back.


True or False
--------------

.. admonition:: Question 20
   :class: hint

   True or False: A function can be called before its definition in the file, as long as a declaration appears above the call.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      The compiler reads the file top to bottom and needs to have seen a declaration before the call. Without one, it reports ``'print_limits' was not declared in this scope``. Declaring every function at the top lets the definitions go in any order.

.. admonition:: Question 21
   :class: hint

   True or False: Two functions may be overloaded if they differ only in their return type.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      A call does not say which return type it wants, so ``int joint_count()`` and ``double joint_count()`` cannot both exist. GCC reports ``ambiguating new declaration of 'double joint_count()'``. Overloads must differ in the number, type or order of their parameters.

.. admonition:: Question 22
   :class: hint

   True or False: A ``static`` local variable with no initializer holds garbage, like an ordinary local.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      A static with no initializer, such as ``static int count;``, is zero-initialized and sits in ``.bss``. An ordinary local with no initializer holds garbage.

.. admonition:: Question 23
   :class: hint

   True or False: In ``int count_calls() { static int calls{0}; ++calls; return calls; }``, ``calls`` is set back to 0 on every call.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      The initializer of a static local runs once, the first time control passes through it. The calls return 1, 2, 3. Writing ``static int calls; calls = 0;`` instead would reset it on every call, because an assignment is an ordinary statement.

.. admonition:: Question 24
   :class: hint

   True or False: A stack frame holds the function's parameters, its local variables and the return address.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      A call pushes a frame on top of the stack, and a return pops it, so frames leave last in, first out. The return address is where execution goes on when the call ends.

.. admonition:: Question 25
   :class: hint

   True or False: Without a ``@file`` comment, Doxygen leaves the free functions of that header out of the pages, and prints no warning.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      A function outside a class belongs to its file, and Doxygen only lists the members of a file that is itself documented. Start every header with a ``@file`` comment. Also run Doxygen from the ``docs`` folder: the paths in a ``Doxyfile`` are relative to the folder Doxygen runs in.
