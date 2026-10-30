====================================================
Value Categories
====================================================

Overview
--------

This reading material gives more examples and practice for the value
categories of Lecture 7: lvalue, xvalue and prvalue. It is a self-study
reading module, with no video. Read it after the Value Categories part of
:doc:`Lecture 7 </lectures/lecture7/l7_lecture>`.

The page gives a step-by-step way to find the category of any expression,
then applies it to 54 expressions, each with its reason. The exercises
add 33 more, with answers. Every category in this module was checked
with g++ 13.3 and ``-std=c++20``.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Say why "rvalue" is not a third answer next to "prvalue" and "xvalue".
   - Find the category of an expression in four steps: names, literals,
     function calls and casts, built-in operators.
   - Check any answer with ``decltype((e))`` and the ``CATEGORY`` helper.
   - Tell the type of a variable apart from the category of an expression
     that names it.
   - Predict which overload, ``const T&`` or ``T&&``, a call picks, and
     whether an object is copied or moved.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   vcat_lecture
   vcat_exercises
   vcat_quiz
   vcat_references
