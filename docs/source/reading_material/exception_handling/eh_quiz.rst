====================================================
Exception Handling: Quiz
====================================================


.. admonition:: Question 1
   :class: hint

   What keyword is used to raise an exception in C++?

   a) ``raise``
   b) ``throw``
   c) ``catch``
   d) ``error``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) throw**

      The ``throw`` keyword is used to raise (throw) an exception.
      ``catch`` is used to handle it, and ``raise`` is a Python keyword,
      not C++.


.. admonition:: Question 2
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      try {
          std::cout << "A\n";
          throw std::runtime_error{"error"};
          std::cout << "B\n";
      } catch (const std::runtime_error& e) {
          std::cout << "C\n";
      }
      std::cout << "D\n";

   a) ``A B C D``
   b) ``A C D``
   c) ``A C``
   d) ``A B D``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) A C D**

      ``A`` is printed before the throw. The throw skips ``B`` and
      transfers control to the catch block, which prints ``C``.
      Execution continues after the catch block, printing ``D``.


.. admonition:: Question 3
   :class: hint

   Which standard exception class is thrown by ``std::vector::at()``
   when the index is out of bounds?

   a) ``std::runtime_error``
   b) ``std::logic_error``
   c) ``std::out_of_range``
   d) ``std::invalid_argument``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) std::out_of_range**

      The ``.at()`` method performs bounds checking and throws
      ``std::out_of_range`` if the index is invalid.


.. admonition:: Question 4
   :class: hint

   Why should exceptions be caught by ``const`` reference?

   a) It is required by the C++ standard.
   b) It prevents slicing and avoids unnecessary copies.
   c) It makes the exception immutable at the language level.
   d) It improves performance by enabling move semantics.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) It prevents slicing and avoids unnecessary copies.**

      Catching by value copies the exception, and a handler for a base
      class keeps only the base part of a derived exception (slicing).
      The reference avoids both. The ``const`` stops the handler from
      changing the exception object.


.. admonition:: Question 5
   :class: hint

   What happens if a ``noexcept`` function throws an exception?

   a) The exception is silently ignored.
   b) The exception is caught by the nearest handler.
   c) ``std::terminate`` is called.
   d) The compiler prevents this with a compilation error.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) std::terminate is called.**

      If an exception leaves a function marked ``noexcept``, the
      program calls ``std::terminate``, which by default aborts it. The
      compiler does not reject the code; for a ``throw`` written directly
      in a ``noexcept`` function, g++ only warns: ``'throw' will always
      call 'terminate'``. An exception that is thrown and caught inside
      the function is fine.


.. admonition:: Question 6
   :class: hint

   Which header must be included to use ``std::runtime_error``?

   a) ``<exception>``
   b) ``<stdexcept>``
   c) ``<errors>``
   d) ``<iostream>``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) <stdexcept>**

      The ``<stdexcept>`` header declares ``std::runtime_error``,
      ``std::logic_error``, ``std::out_of_range`` and
      ``std::invalid_argument``, among others. ``std::exception`` itself
      is declared in ``<exception>``.


.. admonition:: Question 7
   :class: hint

   What is the correct order for these catch blocks?

   .. code-block:: cpp

      // Option A
      catch (const std::exception& e) { ... }
      catch (const std::out_of_range& e) { ... }

      // Option B
      catch (const std::out_of_range& e) { ... }
      catch (const std::exception& e) { ... }

   a) Option A is correct.
   b) Option B is correct.
   c) Both are equivalent.
   d) Neither is correct.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Option B is correct.**

      Catch blocks are matched in order. Since ``std::out_of_range``
      derives from ``std::exception``, Option A catches every exception
      derived from ``std::exception``, including ``std::out_of_range``,
      in the first block, so the second block never runs. g++ warns
      about Option A with ``-Wexceptions``. Derived types must come
      before base types.


.. admonition:: Question 8
   :class: hint

   What does the ``what()`` method return?

   a) The exception type name.
   b) A ``const char*`` describing the error.
   c) An integer error code.
   d) A ``std::string`` containing the stack trace.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) A const char* describing the error.**

      ``what()``, a member function of ``std::exception``, returns a
      ``const char*`` that describes the error. Each standard exception
      returns its own message.


.. admonition:: Question 9
   :class: hint

   When creating a custom exception class, what should it inherit from?

   a) ``std::string``
   b) ``std::exception`` or one of its derived classes
   c) ``std::error_code``
   d) No inheritance is needed

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) std::exception or one of its derived classes**

      Custom exception classes should inherit from ``std::exception``
      or a derived class such as ``std::runtime_error``. This ensures
      compatibility with standard catch handlers and provides the
      ``what()`` method.


.. admonition:: Question 10
   :class: hint

   What does ``catch (...)`` do?

   a) Catches only ``std::exception`` objects.
   b) Catches any exception of any type.
   c) Catches no exceptions (it is a no-op).
   d) Causes a compilation error.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Catches any exception of any type.**

      The catch-all handler ``catch (...)`` matches any thrown
      exception, regardless of type. It must be the last handler of its
      ``try`` block; anywhere else, the compiler rejects it.


.. admonition:: Question 11
   :class: hint

   True or False: Exceptions should be used for normal control flow
   (e.g., breaking out of a loop).

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Exceptions are for errors that a function cannot handle itself.
      Using them for normal control flow is bad practice because
      throwing and catching exceptions is expensive and makes code
      harder to understand.


.. admonition:: Question 12
   :class: hint

   True or False: It is safe to throw exceptions from destructors.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Destructors are ``noexcept`` by default, so an exception that
      leaves a destructor calls ``std::terminate``, even when no other
      exception is in flight.


.. admonition:: Question 13
   :class: hint

   True or False: RAII ensures that resources are properly released
   even when an exception is thrown.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      RAII ties resource lifetime to object lifetime. When an exception
      causes stack unwinding, local objects are destroyed and their
      destructors run, releasing any managed resources (file handles,
      memory, locks, etc.). Unwinding needs a handler: if nothing catches
      the exception, g++ calls ``std::terminate`` without running the
      destructors.


.. admonition:: Question 14
   :class: hint

   True or False: ``std::bad_alloc`` is thrown when ``new`` fails to
   allocate memory.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      When the ``new`` operator cannot allocate the requested memory,
      it throws ``std::bad_alloc`` (declared in ``<new>``).


.. admonition:: Question 15
   :class: hint

   True or False: Modern C++ exception handling has zero runtime cost
   even when exceptions are thrown.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      With g++ on x86-64, a ``try`` block adds no instructions to the
      path where nothing is thrown. When an exception is thrown, the
      runtime must unwind the stack: find the matching handler, destroy
      local objects, and transfer control. That process is slow.
