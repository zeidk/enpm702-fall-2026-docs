====================================================
Lecture
====================================================


Compiler Warning Flags
====================================================

Three warning options appear in the build command used throughout this
course:

.. code-block:: bash

   g++ -std=c++20 -Wall -Wextra -Wpedantic -g main.cpp -o main

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    ``-Wall``, ``-Wextra``, and ``-Wpedantic`` are *groups* of compiler
    warnings understood by both ``g++`` and ``clang++``. None of them
    change the code that is generated. They only change what the
    compiler tells you about the code you wrote.

.. tip::

   That command is long enough to be worth an alias. Using what you
   practiced in the :doc:`Lecture 1 shell exercises
   </lectures/lecture1/l1_shell>`:

   .. code-block:: bash

      alias 702g++='g++ -std=c++20 -Wall -Wextra -Wpedantic -g'

   Add it to your ``~/.bashrc`` (or ``~/.zshrc``) and you can then
   build with ``702g++ main.cpp -o main``.


``-Wall``
----------------------------------------------------

The name is misleading. It does **not** enable all warnings, only the
set the GCC maintainers consider uncontroversial: problems that almost
always indicate a real mistake, with few false positives.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Warning**
     - **What it catches**
   * - ``-Wunused-variable``
     - A variable is declared and never used
   * - ``-Wreturn-type``
     - A non-void function can reach its end without returning
   * - ``-Wsign-compare``
     - A signed value is compared to an unsigned one
   * - ``-Wuninitialized``
     - A variable is read before being assigned
   * - ``-Wswitch``
     - A ``switch`` over an enum is missing some enumerators

The signed/unsigned case is the one students hit most often:

.. code-block:: cpp

   std::vector<int> v{1, 2, 3};
   for (int i{0}; i < v.size(); ++i) {  // warning: i is int, size() is size_t
       // ...
   }

The fix is ``std::size_t i{0}``, or a range-based ``for`` loop.


``-Wextra``
----------------------------------------------------

A second tier of warnings. Still useful, but they fire more often on
code that was written deliberately.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Warning**
     - **What it catches**
   * - ``-Wunused-parameter``
     - A function parameter is never used in the body
   * - ``-Wempty-body``
     - A stray semicolon, as in ``if (x);``
   * - ``-Wmissing-field-initializers``
     - Aggregate initialization leaves some members defaulted
   * - Type-based comparisons
     - A comparison that is always true or always false

The stray semicolon is worth seeing once:

.. code-block:: cpp

   if (count > 0);                 // warning: this if does nothing
       std::cout << "positive\n";  // this line always runs

.. warning::

   The indentation says one thing and the semicolon says another. The
   compiler follows the semicolon. Without ``-Wextra``, it says nothing
   at all.


``-Wpedantic``
----------------------------------------------------

This one sits on a different axis.

- ``-Wall`` and ``-Wextra`` ask: *is this likely a bug?*
- ``-Wpedantic`` asks: *is this strictly conforming ISO C++?*

It warns about GNU extensions that ``g++`` accepts happily but that are
not in the standard, so the same code would fail to compile with MSVC or
another compiler. The classic case is a variable-length array, which
exists in C99 but not in C++:

.. code-block:: cpp

   int n{};
   std::cin >> n;
   int arr[n];  // warning: ISO C++ forbids variable length array

The portable version is ``std::vector<int> arr(n);``.

.. note::

   This is the same concern as ``set(CMAKE_CXX_EXTENSIONS OFF)`` in
   :doc:`Lecture 1 </lectures/lecture1/l1_lecture>`, approached from
   the other side. ``CMAKE_CXX_EXTENSIONS OFF`` asks for
   ``-std=c++20`` instead of ``-std=gnu++20``; ``-Wpedantic`` reports
   the places where your code relied on the difference.


Why All Three in This Course
----------------------------------------------------

Beginner code produces exactly what these flags catch:

- unused variables left behind by half-finished edits,
- signed/unsigned comparisons in loops,
- and variable-length arrays carried over from a C course.

Without the flags the compiler stays silent, and the bug surfaces later
as strange runtime behavior that is much harder to diagnose.


Two Things Worth Knowing
----------------------------------------------------

They Are Not Cumulative in a Tidy Way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In practice ``-Wextra`` pulls in most of ``-Wall``, but ``-Wpedantic``
is independent of both, and even all three together leave plenty of
warnings disabled. Two useful additions:

- ``-Wshadow``: an inner declaration hides an outer one of the same
  name.
- ``-Wconversion``: an implicit narrowing conversion silently loses
  data.

.. note::

   ``-Wconversion`` is noisy enough that it tends to frustrate students
   if it is turned on too early in the semester.


``-Werror`` Turns Every Warning Into a Hard Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

That is the right setting for a professional codebase, but a debatable
one for a first course: a student blocked by an unused parameter cannot
run their program at all.

If you want some of that discipline without the wall,
``-Werror=return-type`` alone catches the single most dangerous case,
since falling off the end of a non-void function is **undefined
behavior**.


Quick Reference
----------------------------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Flag**
     - **Question it answers**
   * - ``-Wall``
     - Is this probably a bug?
   * - ``-Wextra``
     - Is this suspicious, even if it might be intentional?
   * - ``-Wpedantic``
     - Is this standard C++, or a GNU extension?
   * - ``-Werror``
     - Should warnings stop the build?
   * - ``-g``
     - Should debug symbols be emitted, for ``gdb`` and Valgrind?
