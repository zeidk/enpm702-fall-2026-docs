.. _l4_index:

====================================================
L4: The Standard Library and Its Containers
====================================================

Overview
--------

This lecture is about never writing ``new`` and ``delete`` again.
:doc:`Lecture 3 </lectures/lecture3/l3_index>` ended with the four ways
manual memory management goes wrong. The standard library ships
containers that own their storage, grow on demand and free everything at
the closing brace, and this lecture covers the five you will use in
every robot program: ``std::array``, ``std::vector``, ``std::string``,
``std::map`` and ``std::unordered_map``.

It opens with two tools for reading the rest: ``std::size_t``, the type
of every size, and time complexity, the notation the standard uses to
state what each operation costs. It then covers arrays, both the C-style
kind and ``std::array``, and what array decay costs you; iterators and
the half-open range; ``std::vector`` in memory, its growth, reallocation
and iterator invalidation; C-strings against ``std::string``; the two
maps and the subscript trap; how to choose a container; and the
algorithms that take iterators.

The examples come from a small robot: joint angles, a lidar scan, an
occupancy grid, a registry of sensors. Every number on the slides was
measured on the course machine.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this lecture, you will be able to:

   - Use ``std::size_t`` for every size and name the two traps of
     unsigned arithmetic.
   - Read a Big-O cost and work one out for a loop: name the input
     size, count how often the body runs, keep the shape of the growth.
   - Say what the STL is, which part of the standard library came from
     it, and name the four categories of container.
   - Explain array decay, why ``sizeof`` lies after it, and why
     ``std::array`` cannot decay.
   - Index a multidimensional array by hand in row-major order and put
     the last index in the inner loop.
   - Use ``begin()`` and ``end()`` as a half-open range, choose between
     the three ways of writing a loop, and use a const iterator.
   - Describe a ``std::vector`` as three pointers and a heap block,
     trace its size and capacity through a sequence of pushes, and
     explain why ``push_back`` is amortized O(1).
   - Use ``reserve`` and ``shrink_to_fit`` correctly, and state which
     operations invalidate iterators.
   - Tell a C-string from a ``std::string`` by what each stores, say
     where a string literal lives, and use ``find``, ``npos`` and
     ``getline`` without the classic mistakes.
   - Use ``[]``, ``at``, ``find`` and ``contains`` on a map each for
     what it is for, and choose between ``std::map`` and
     ``std::unordered_map``.
   - Pick a container from two questions: is the size fixed at compile
     time, and is the handle a position or a key.
   - Call ``sort``, ``find``, ``count_if``, ``min_element`` and
     ``accumulate`` with a pair of iterators or, in C++20, a range.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Lecture 4 Contents

   l4_lecture
   l4_shell
   l4_exercises
   l4_quiz
   l4_references

Next Steps
----------

In **Lecture 5: Functions Basics**, you will write the functions this
lecture only used: declarations and definitions, header files, passing
by value, by reference and by pointer, which is the choice Lecture 3 set
up and left open, overloading, default arguments and the call stack. The
predicates you passed to ``count_if`` and ``erase_if`` here become
functions you design there.
