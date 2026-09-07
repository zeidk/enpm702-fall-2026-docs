====================================================
Validating Terminal Input
====================================================

Overview
--------

This reading material covers what happens when ``std::cin >> value``
does not get the input it expects, and the two standard ways to handle
it. It is a self-study reading module. Work through it alongside
:doc:`Lecture 2 </lectures/lecture2/l2_lecture>`, where ``std::cin``
first appears.

The short version: extraction can fail, it can also *partially* succeed,
and the partial success is the one that will surprise you. Checking
whether the read "worked" does not catch it.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Describe the three outcomes of ``std::cin >> value``: clean success,
     failure, and partial read.
   - Explain why a failed extraction leaves the offending characters in
     the buffer, and why the next read then fails immediately.
   - Recover a stream with ``clear()`` and ``ignore()``, and say why
     ``clear()`` alone is not enough.
   - Reject input that is not *entirely* a number, using ``std::getline``
     with ``std::from_chars``.
   - Choose between the two approaches for a given situation.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   iv_lecture
   iv_references

.. note::

   Since C++11 a failed extraction **zeroes** the variable. A value you
   set earlier is destroyed, not preserved. That alone is worth knowing
   before you write a program that reads from a user.
