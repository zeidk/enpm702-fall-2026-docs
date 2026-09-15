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

Pointer arithmetic is introduced here in the only form a single variable
can show, the rule that ``p + 1`` steps by ``sizeof(*p)``; arrays, and
the arithmetic that finally makes it useful, wait for Lecture 4. Smart
pointers, the tool that makes almost all of the manual work unnecessary,
are :doc:`Lecture 7 </lectures/lecture7/l7_index>`.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Read a memory address: why it is printed in hexadecimal, why two
     hex digits are one byte, and why ``0x…a28 + 8`` is ``0x…a30``.
   - Choose a **build type** and say what it changes: ``Debug`` against
     ``Release``, and why Valgrind loses its line numbers without
     ``-g``.
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
   - Apply pointer arithmetic: explain why ``p + 1`` advances by
     ``sizeof(*p)`` rather than one byte, say which positions are legal
     around a single object, and name what makes dereferencing a
     one-past-the-end pointer undefined.
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
  - Pointer and iterator invalidation: why a pointer into a container
    can go stale when the container changes.

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
  - `C++ Core Guidelines, R: Resource management <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r-resource-management>`_
