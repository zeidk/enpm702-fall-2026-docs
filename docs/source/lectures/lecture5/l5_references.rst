.. _l5_references:

====================
Lecture 5 References
====================

.. dropdown:: Lecture 5 Summary
   :class-container: sd-border-success

   This lecture covered functions in C++, built around one program: a planar arm
   with three joints that reads its joint angles from the command line, clamps
   each one to its limit, converts it to radians, and reports where the tool
   ends up.

   - **Functions**: the parts of a function (return type, name, parameter
     list, body), parameters and arguments, declarations and definitions, and
     the compile error or link error each one produces when it is missing.
     Header files (``.hpp``) hold declarations and source files (``.cpp``)
     hold definitions. Each ``.cpp`` is compiled on its own and the linker
     joins the results; CMake lists every ``.cpp`` and finds the headers with
     ``target_include_directories``. Include guards and ``#pragma once`` stop a
     header from being pasted twice into one source file, and a body in a
     header breaks the one-definition rule. The ``return`` statement, the
     undefined behavior of a missing return, conversion on return, and
     ``[[nodiscard]]``.

   - **Passing Arguments**: by value, by reference, by reference to ``const``,
     and by pointer, with ``std::string_view`` for text and ``std::span`` for
     a read-only sequence.

   - **Returning Values**: return by value and copy elision (RVO, and NRVO
     measured with ``std::vector``), return by reference, and return by
     pointer, with ``nullptr`` for "not found". Returning a reference or a
     pointer to a local, or to a temporary argument, leaves it dangling.

   - **Overloading and Default Arguments**: overloads that differ in count,
     type or order of parameters, overload resolution and ambiguous calls, and
     default arguments, which belong in the declaration only.

   - **Static Local Variables**: a local that lives for the whole program. It
     sits in ``.bss`` when its initializer is 0 or missing (so it starts at
     zero) and in ``.data`` otherwise, and its initializer runs once.

   - **The Call Stack**: every active call has one stack frame, pushed by a
     call and popped by a return. The in-class exercise A Stack Trace
     draws the stack of a short program at one line.

   - **The main Function**: the two standard forms of ``main`` and the
     command-line arguments ``argc`` and ``argv``.

   - **Documenting Functions**: Doxygen comments (``@brief``, ``@param``,
     ``@return``, ``@file``) on declarations, the ``Doxyfile``, and running
     Doxygen from the ``docs`` folder.

   The appendix of the slides, which is not presented, covers ``constexpr``
   and ``consteval`` functions, cases where elision is not done, the call stack
   step by step, five common uses of ``static``, and recursion.

.. dropdown:: C++ Reference Links
   :class-container: sd-border-success

   - `Functions (cppreference.com) <https://en.cppreference.com/w/cpp/language/functions>`_
   - `The return statement (cppreference.com) <https://en.cppreference.com/w/cpp/language/return>`_
   - `nodiscard (cppreference.com) <https://en.cppreference.com/w/cpp/language/attributes/nodiscard>`_
   - `std::span (cppreference.com) <https://en.cppreference.com/w/cpp/container/span>`_
   - `Copy elision (cppreference.com) <https://en.cppreference.com/w/cpp/language/copy_elision>`_
   - `Overload resolution (cppreference.com) <https://en.cppreference.com/w/cpp/language/overload_resolution>`_
   - `Default arguments (cppreference.com) <https://en.cppreference.com/w/cpp/language/default_arguments>`_
   - `Storage duration (cppreference.com) <https://en.cppreference.com/w/cpp/language/storage_duration>`_
   - `static (cppreference.com) <https://en.cppreference.com/w/cpp/language/static>`_
   - `The main function (cppreference.com) <https://en.cppreference.com/w/cpp/language/main_function>`_
   - `constexpr (cppreference.com) <https://en.cppreference.com/w/cpp/language/constexpr>`_ and
     `consteval (cppreference.com) <https://en.cppreference.com/w/cpp/language/consteval>`_ (appendix)

.. dropdown:: C++ Core Guidelines
   :class-container: sd-border-success

   - `F: Functions <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#s-functions>`_
   - `F.1: "Package" meaningful operations as carefully named functions <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-package>`_
   - `F.2: A function should perform a single logical operation <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-logical>`_
   - `SF.2: A header file must not contain object definitions or non-inline function definitions <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-inline>`_
   - `F.15: Prefer simple and conventional ways of passing information <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-conventional>`_
   - `F.16: For "in" parameters, pass cheaply-copied types by value and others by reference to const <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-in>`_
   - `F.17: For "in-out" parameters, pass by reference to non-const <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-inout>`_
   - `F.20: For "out" output values, prefer return values to output parameters <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out>`_
   - `I.13: Do not pass an array as a single pointer <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-array>`_
   - `SL.str.2: Use std::string_view to refer to character sequences <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-view>`_
   - `F.60: Prefer T* over T& when "no argument" is a valid option <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-ptr-ref>`_
   - `F.43: Never (directly or indirectly) return a pointer or a reference to a local object <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-dangle>`_
   - `F.51: Where there is a choice, prefer default arguments over overloading <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-default-args>`_
   - `F.46: int is the return type for main() <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-main>`_
   - `F.4: If a function might have to be evaluated at compile time, declare it constexpr <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-constexpr>`_ (appendix)

.. dropdown:: Doxygen Documentation
   :class-container: sd-border-success

   - `Doxygen manual <https://www.doxygen.nl/manual/index.html>`_
   - `Doxygen: installation <https://www.doxygen.nl/manual/install.html>`_
   - `Doxygen: documenting the code <https://www.doxygen.nl/manual/docblocks.html>`_
   - `Doxygen: special commands <https://www.doxygen.nl/manual/commands.html>`_, including
     `@file <https://www.doxygen.nl/manual/commands.html#cmdfile>`_
   - `Doxygen: configuration reference <https://www.doxygen.nl/manual/config.html>`_
   - `Doxygen: doxywizard <https://www.doxygen.nl/manual/doxywizard_usage.html>`_
   - Reading material: :doc:`Documentation with Sphinx and Breathe </reading_material/sphinx_breathe/sb_index>`,
     which builds these pages with Sphinx from Doxygen's XML.
   - Other tools: `Sphinx with Breathe <https://breathe.readthedocs.io/>`_, which builds on
     Doxygen's output, and `MrDocs <https://www.mrdocs.com/>`_ and
     `clang-doc <https://clang.llvm.org/extra/clang-doc.html>`_, which read the code with
     the Clang compiler.

.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   - *A Tour of C++* by Bjarne Stroustrup, Chapter 1 (The Basics: functions and scope)
   - *C++ Primer* by Lippman, Lajoie, and Moo, Chapter 6 (Functions)
   - *The Pragmatic Programmer* by Hunt and Thomas, on DRY, Don't Repeat Yourself
   - `LearnCpp.com: Introduction to functions <https://www.learncpp.com/cpp-tutorial/introduction-to-functions/>`_
   - `LearnCpp.com: Function parameters and arguments <https://www.learncpp.com/cpp-tutorial/introduction-to-function-parameters-and-arguments/>`_
   - `LearnCpp.com: Header files <https://www.learncpp.com/cpp-tutorial/header-files/>`_
   - `#pragma once: the tradeoffs, both ways (Wikipedia) <https://en.wikipedia.org/wiki/Pragma_once>`_
