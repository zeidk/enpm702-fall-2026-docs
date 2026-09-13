.. _l3-index:

====================================================
L3: Pointers and Memory Management
====================================================

Overview
--------

This lecture is about the third storage duration. Lecture 2 covered the
two that the compiler manages, static and automatic, and showed that
every object has an address. This lecture takes that address and puts it
in a variable.

Every example on the lecture page comes from the same place, the flight
controller of a small quadrotor, so that the names in the code say what
the data is.

It covers what a pointer is and how to declare, initialize and
dereference one; null and wild pointers; what the *type* of a pointer is
for; const-correctness; dynamic allocation with ``new`` and ``delete``
and the four ways it goes wrong; finding those bugs with Valgrind and the
sanitizers; and references, the safer alternative you will reach for far
more often.

The C++20 facility that belongs to this material is allocation inside a
constant expression, where a leak becomes a compile error. It is covered
alongside the classical material, together with the reason this course
asks you to write almost none of it by hand. Arrays, and the pointer
arithmetic that goes with them, wait for Lecture 4.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Say which storage duration an object has, where it lives, and who
     ends its lifetime.
   - Declare and initialize pointers, read a pointer declaration
     inside-out, and explain why ``int* altitude_ptr, target_m;`` does
     not do what it looks like.
   - Use ``&`` and ``*`` correctly, and distinguish ``ptr = …`` (change
     the pointer) from ``*ptr = …`` (change the object).
   - Explain what a null pointer is, why ``nullptr`` is preferred to
     ``NULL`` or ``0``, and how a null pointer differs from an
     uninitialized (wild) one.
   - Explain why every pointer has the same size, and what the pointer's
     *type* actually determines.
   - Apply const-correctness: distinguish ``const int*``,
     ``int* const``, and ``const int* const``, and choose the right one
     for a function parameter.
   - Allocate and release heap memory with ``new`` and ``delete``, and
     state what ``delete`` does *not* do.
   - Recognize, and explain the cause of, the four classic failures:
     memory leak, dangling pointer, double delete, and null
     dereference.
   - Use ``valgrind --leak-check=full`` and ``-fsanitize=address``, read
     their output, and add a ``memcheck`` target to ``CMakeLists.txt``.
   - Use references: state the five properties, explain why they cannot
     be reseated, and choose between a reference and a pointer for a
     given interface.
   - Explain what RAII means and why the course prefers containers and
     smart pointers to explicit ``new``/``delete``.
   - Use the C++20 facility that applies here: allocation in a constant
     expression, where failing to free is a compile error.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l3_lecture
   l3_shell
   l3_exercises
   l3_quiz
   l3_references

Next Steps
----------

- In the next lecture, we will cover **L4: STL Containers**:

  - ``std::string``, ``std::array``, and ``std::vector``.
  - Iterators, and why they are a generalization of pointers.
  - Pointer and iterator invalidation, the constraint that Discussion 2
    of this lecture ran into.

- **Pre-work:**

  - Complete the Lecture 3 :doc:`shell exercises <l3_shell>`,
    :doc:`C++ exercises <l3_exercises>`, and
    :doc:`self-check quiz <l3_quiz>`.
  - Make sure ``valgrind --version`` works on your machine; the
    exercises need it.

- **Recommended reading:**

  - `cppreference: pointer declaration <https://en.cppreference.com/w/cpp/language/pointer>`_
  - `cppreference: new expression <https://en.cppreference.com/w/cpp/language/new>`_
  - `Valgrind Quick Start <https://valgrind.org/docs/manual/quick-start.html>`_
  - `C++ Core Guidelines, R: Resource management <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-resource>`_
