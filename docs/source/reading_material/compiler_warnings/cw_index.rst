====================================================
Compiler Warning Flags
====================================================

Overview
--------

This reading material explains the compiler warning flags used
throughout this course: ``-Wall``, ``-Wextra``, and ``-Wpedantic``. It
is a self-study reading module. Work through it alongside
:doc:`Lecture 1 </lectures/lecture1/l1_lecture>`, where these flags
first appear in the build command. None of these flags change the code
the compiler generates; they only change what the compiler tells you
about the code you wrote.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Explain what ``-Wall``, ``-Wextra``, and ``-Wpedantic`` each
     enable, and why ``-Wall`` does not mean "all warnings".
   - Recognize the warnings these flags produce most often in beginner
     code, such as signed/unsigned comparisons and unused variables.
   - Distinguish a likely-bug warning from a portability warning.
   - Decide when additional flags such as ``-Wshadow``,
     ``-Wconversion``, and ``-Werror`` are appropriate.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   cw_lecture
   cw_references

.. note::

   Warnings are not optional noise in this course. A program that
   compiles with warnings is a program with a defect you have not
   triggered yet. Treat every warning as something to fix before you
   submit.
