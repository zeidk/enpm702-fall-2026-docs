====================================================
Exception Handling
====================================================

Overview
--------

This reading material covers C++ exception handling using ``try``,
``catch``, and ``throw``. It is a self-study reading module. Read it
before Lecture 7. It explains the two Lecture 6 programs that stopped
with ``terminate called after throwing an instance of ...``, and how to
catch those errors.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Explain the purpose of exception handling in C++.
   - Use ``try``, ``catch``, and ``throw`` to handle runtime errors.
   - Catch exceptions by type and by reference.
   - Use standard exception classes (``std::exception``, ``std::runtime_error``, ``std::out_of_range``, etc.).
   - Create custom exception types that build on ``std::runtime_error``.
   - Apply the RAII principle to ensure exception-safe resource management.
   - Decide when to use exceptions and when to use ``std::optional`` or return codes.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   eh_lecture
   eh_exercises
   eh_quiz
   eh_references
