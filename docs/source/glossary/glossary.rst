====================================================
Glossary
====================================================

This glossary covers the key terms of ENPM702, grouped by the lecture that
introduces them and sorted A to Z within each lecture. Click a lecture in the
right panel to jump to its terms. A term that a later lecture uses again is
listed at the end of that lecture's section.

.. only:: html

   .. raw:: html

      <div id="glossary-search-wrap" style="margin: 1.2em 0 0.6em 0;">
        <input
          id="glossary-search"
          type="search"
          placeholder="Filter terms..."
          autocomplete="off"
          spellcheck="false"
          style="
            width: 100%;
            max-width: 480px;
            padding: 0.45em 0.75em;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
          "
        />
        <span
          id="glossary-search-count"
          style="margin-left: 0.8em; font-size: 0.88em; color: #666;"
        ></span>
      </div>
      <div id="glossary-letters" aria-label="Show the terms that start with a letter"
           style="display: flex; flex-wrap: wrap; gap: 0.3em; margin: 0 0 1.4em 0;"></div>

      <style>
        #glossary-letters button {
          min-width: 2em;
          padding: 0.15em 0.45em;
          font: inherit;
          font-size: 0.95em;
          color: var(--pst-color-primary, #2f6fb5);
          background: transparent;
          border: 1px solid var(--pst-color-border, #ccc);
          border-radius: 4px;
          cursor: pointer;
        }
        #glossary-letters button.active {
          color: var(--pst-color-background, #fff);
          background: var(--pst-color-primary, #2f6fb5);
          border-color: var(--pst-color-primary, #2f6fb5);
        }
      </style>

      <script>
      (function () {
        /* The search box filters by text; a letter button shows the terms
           that start with that letter, across all lectures. Both apply
           together. A lecture section with no matching term is hidden. */
        function initGlossarySearch() {
          var input   = document.getElementById('glossary-search');
          var count   = document.getElementById('glossary-search-count');
          var letters = document.getElementById('glossary-letters');
          if (!input) return;
          var letter = '';

          function firstLetter(dt) {
            var m = dt.textContent.trim().match(/[a-z]/i);
            return m ? m[0].toUpperCase() : '';
          }

          /* One button per letter that starts a term, plus "All". */
          var present = {};
          document.querySelectorAll('dl.glossary dt').forEach(function (dt) {
            var c = firstLetter(dt);
            if (c) present[c] = true;
          });
          function addButton(label, value) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.textContent = label;
            btn.dataset.letter = value;
            if (value === '') btn.classList.add('active');
            btn.addEventListener('click', function () {
              letter = value;
              letters.querySelectorAll('button').forEach(function (b) {
                b.classList.toggle('active', b.dataset.letter === letter);
              });
              run();
            });
            letters.appendChild(btn);
          }
          addButton('All', '');
          Object.keys(present).sort().forEach(function (c) { addButton(c, c); });

          function run() {
            var query = input.value.trim().toLowerCase();
            var filtering = query !== '' || letter !== '';
            var visible = 0;

            document.querySelectorAll('dl.glossary dt').forEach(function (dt) {
              var match = (!query || dt.textContent.toLowerCase().indexOf(query) !== -1)
                       && (!letter || firstLetter(dt) === letter);
              dt.style.display = match ? '' : 'none';
              var node = dt.nextElementSibling;
              while (node && node.tagName === 'DD') {
                node.style.display = match ? '' : 'none';
                node = node.nextElementSibling;
              }
              if (match) visible++;
            });

            /* Each lecture section: hide it when nothing in it matches, and
               hide its "Also used here" line while a filter is on. */
            document.querySelectorAll('section > h2').forEach(function (h2) {
              var section = h2.parentElement;
              var dts = section.querySelectorAll('dl.glossary dt');
              var any = Array.prototype.some.call(dts, function (dt) {
                return dt.style.display !== 'none';
              });
              section.style.display = (!filtering || any) ? '' : 'none';
              section.querySelectorAll('dl.glossary').forEach(function (dl) {
                dl.style.display = (!filtering || any) ? '' : 'none';
              });
              section.querySelectorAll('p.glossary-also').forEach(function (p) {
                p.style.display = filtering ? 'none' : '';
              });
            });

            count.textContent = filtering
              ? (visible === 1 ? '1 term found' : visible + ' terms found')
              : '';
          }

          input.addEventListener('input', run);
          input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
          });
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initGlossarySearch);
        } else {
          initGlossarySearch();
        }
      })();
      </script>

----


.. _g-l1:

L1: Course Introduction
=======================

.. glossary::

   Alias
      A shell shortcut that maps a short identifier to a longer command.
      Defined with ``alias name='command'`` in a shell configuration file.
      Aliases are lost when the terminal session ends unless saved in the
      configuration file.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Bash
      Bourne Again Shell. The default shell for most Linux distributions,
      widely used for scripting and interactive command-line use.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   CMake
      An open-source, cross-platform build system used to build, test,
      and package C++ software. Uses ``CMakeLists.txt`` files to define
      build configurations.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   CMakeLists.txt
      The configuration file used by CMake to define how a project should
      be built, including source files to compile and libraries to link.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Command Line Interface (CLI)
      A text-based interface for interacting with the operating system by
      typing commands. Linux shells provide a CLI.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Command Palette
      A searchable list of all available commands in Visual Studio Code,
      accessed via ``Ctrl + Shift + P``. Includes built-in commands and
      those from installed extensions.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Configuration File (Shell)
      A script that runs automatically each time a new shell session
      starts. Used to define aliases, functions, and environment
      variables. Examples: ``.bashrc`` (Bash), ``.zshrc`` (Zsh),
      ``config.fish`` (Fish).
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Function (Shell)
      A reusable block of shell code that groups commands and can be
      executed by calling the function's name. Can accept arguments
      via positional parameters (``$1``, ``$2``, etc.).
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Ksh
      Korn Shell. A Unix shell with advanced scripting features,
      sometimes used in enterprise environments. Uses ``.kshrc`` as its
      configuration file.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Shell
      A program that provides a command-line interface for users to
      interact with the operating system, allowing them to execute
      commands, run scripts, manage files, and control processes.
      Common shells include Bash, Zsh, Fish, Csh, and Ksh.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Visual Studio Code
      A free, cross-platform code editor by Microsoft. Supports virtually
      every programming language through extensions. Used in this course
      for C++ and ROS 2 development.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Workspace
      In VSCode, a container that holds a set of related projects or code
      files. Workspace-specific settings are stored in the ``.vscode``
      folder and take precedence over user settings.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Zsh
      Z Shell. A shell similar to Bash with additional features like
      improved autocompletion and customization. Uses ``.zshrc`` as its
      configuration file.
      :doc:`L1 </lectures/lecture1/l1_lecture>`


.. _g-l2:

L2: Variables, Types and Memory
===============================

.. glossary::

   Address-of Operator
      The unary ``&`` operator, which yields the memory address of a
      variable. ``std::cout << &number;`` prints where ``number`` lives.
      Not to be confused with a reference declaration, which also uses
      ``&``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Alias (C++ Type)
      A type alias created with the ``using`` keyword that gives an
      alternative name to an existing type. Example:
      ``using Integer = int;``
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Arithmetic Conversion
      Implicit type conversion rules applied when binary operators have
      operands of different types. The operand with lower priority is
      converted to the higher-priority type.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Assignment
      Storing a value in a variable that has already been declared,
      using the copy assignment operator ``=``. The previous value is
      overwritten. Distinct from initialization, which gives a variable
      its value at the point of declaration.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   auto
      A keyword that enables type deduction, allowing the compiler to
      deduce the type of a variable from its initializer. Requires an
      initializer; drops ``const`` by default.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Bit
      Binary digit. The smallest unit of data, holding either ``0`` or
      ``1``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   bool
      The Boolean type. Occupies 1 byte and holds ``true`` or ``false``.
      Any non-zero value converts to ``true``; converting back yields
      ``1`` or ``0``. Print the words instead of the digits with
      ``std::boolalpha``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   BSS Segment
      The region of a process image holding **uninitialized** global and
      static variables. The loader zeroes it before ``main()`` runs,
      which is why an uninitialized global is 0 while an uninitialized
      local is garbage. Short for Block Started by Symbol.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Byte
      A group of 8 bits, and the smallest individually addressable unit
      of memory on typical architectures.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   char
      The character type, 1 byte, and an integral type. Plain ``char``,
      ``signed char``, and ``unsigned char`` are three **distinct**
      types, and whether plain ``char`` is signed is
      implementation-defined.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Compile-time Constant
      A constant whose value is known while the program is being
      compiled, so the compiler can substitute it directly. A ``const``
      variable is one only if its initializer is itself a constant
      expression; ``constexpr`` requires it.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Compiler
      A program that translates preprocessed C++ source code into
      machine code (object files). Part of the build process between
      preprocessing and linking.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Compound Statement
      A group of zero or more statements enclosed in braces ``{}``.
      Also called a block. No semicolon needed after the closing brace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   const
      A qualifier that makes a variable read-only after initialization.
      May be evaluated at compile-time or runtime depending on the
      initializer.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Constant Expression
      An expression the compiler can evaluate at compile time, because
      every value in it is known then. The compiler replaces it with its
      result, so ``1 + 2`` never costs anything at runtime.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   constexpr
      A specifier that guarantees a variable or expression is evaluated
      at compile-time. Provides better optimization than ``const`` alone.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Copy Initialization
      Initialization with ``=``, as in ``int a = 1;``. Inherited from C
      and little used in modern C++, because unlike uniform
      initialization it permits narrowing conversions.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Data Segment
      The region of a process image holding **initialized** global and
      static variables. Compare with the BSS segment, which holds the
      uninitialized ones.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Declaration
      A statement that introduces a variable's type and name to the
      compiler, reserving storage and enabling type checking of every
      later use. ``int number;`` is a declaration.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Demangling
      Turning a compiler-generated (mangled) symbol or type name back
      into readable C++. Do it with ``c++filt``; ``./program | c++filt -t``
      makes the output of ``typeid(...).name()`` legible.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Direct Initialization
      Initialization with parentheses, as in ``int a(1);``. Introduced
      for efficient initialization of class types; like copy
      initialization, it permits narrowing conversions and is little
      used in modern C++.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   enum class
      See :term:`Scoped Enumeration`.

   Escape Sequence
      A two-character sequence beginning with a backslash that stands for
      one character inside a character or string literal: ``\n`` newline,
      ``\t`` tab, ``\'`` single quote, ``\\`` backslash, ``\0`` null. It is
      **one** ``char``, not two.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Extraction Operator
      The ``>>`` operator, which reads a value out of an input stream
      and into a variable: ``std::cin >> age;``. The arrows point in the
      direction the data travels.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Fixed-width Integer Type
      An integer type of guaranteed exact width, declared in ``<cstdint>``:
      ``int8_t``, ``int32_t``, ``uint64_t`` and so on. Use these when the
      width actually matters, because the width of ``int``, ``long`` and
      friends is only implementation-defined.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Floating-point Type
      A type representing real numbers with a fractional part:
      ``float``, ``double``, and ``long double``. Always signed. Its
      *precision* is the number of significant decimal digits it can
      carry, not the number of digits after the decimal point.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Global Scope
      File scope: the region from a declaration made outside every
      function to the end of that file. Globals live in the data or BSS
      segment, not on the stack. Non-const globals are strongly
      discouraged (Core Guideline ``R.6``) because any function can
      modify them.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Identifier
      The name of a variable, function, type, or other entity. May
      contain letters, digits and underscores, must not begin with a
      digit, is case sensitive, and cannot be a reserved keyword. This
      course names variables in ``snake_case``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Implementation-defined Behavior
      Behavior an implementation must choose and document, but which the
      standard does not fix. Every fundamental type's exact size is
      implementation-defined (``[expr.sizeof]/1``); the standard
      guarantees only minimum widths and their ordering. Unlike undefined
      behavior, the program is still well formed.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Implicit Type Conversion
      A type conversion performed automatically by the compiler when
      one data type is required but a different type is supplied.
      Does not change the original value or type.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Initialization
      Declaring a variable and giving it a value in a single step. C++
      offers three forms: copy (``int a = 1;``), direct (``int a(1);``),
      and uniform (``int a{1};``). This course uses uniform
      initialization.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Initializer
      The value used to initialize a variable. In ``int a{1};`` the
      initializer is ``1``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Insertion Operator
      The ``<<`` operator, which sends a value into an output stream:
      ``std::cout << value;``. Each insertion returns the stream, which
      is why insertions can be chained.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Integer Overflow
      What happens when an arithmetic result falls outside the range its
      type can represent. For **signed** types this is undefined
      behavior; for **unsigned** types it is defined to wrap around
      modulo the type's range, which is why unsigned ``0 - 1`` yields a
      very large number rather than ``-1``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Integral Type
      A C++ data type that represents whole numbers. Includes ``int``,
      ``char``, ``short``, ``long``, ``long long``, ``bool``, and
      their unsigned counterparts.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Lifetime
      The span of program execution during which a variable exists in
      memory. A local variable's lifetime ends at the closing brace of
      its block; a global's lasts for the whole program.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Linker
      A program that combines object files and libraries into a single
      executable program. Resolves dependencies and calculates memory
      addresses.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Literal
      A fixed value written directly into the source code: ``42``,
      ``3.14``, ``'a'``, ``"Hello"``, ``true``. Numeric literals may
      carry a suffix (``12L``, ``1.05f``) that sets their type.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Literal Suffix
      A suffix that pins a literal's type: ``u`` unsigned, ``L`` long,
      ``LL`` long long, ``f`` float. They combine, so ``12uLL`` is an
      ``unsigned long long``. Without one, an integer literal is ``int``
      and a floating-point literal is ``double``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Local Scope
      The region within a pair of braces ``{}`` where a variable is
      accessible. Variables are destroyed when execution leaves the
      block.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Macro
      A preprocessor definition (``#define``) that is substituted
      textually before compilation. Macros have no type checking and no
      scope, and do not survive into the debugger. Use ``const`` or
      ``constexpr`` instead.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Magic Number
      A bare literal written into the logic, such as the ``1`` in
      ``if (state == 1)``. It needs a comment to be readable and a search
      to be safe to change. Replace it with a named constant or, for a
      fixed set of alternatives, a :term:`Scoped Enumeration`.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Mangling
      The compiler's encoding of C++ names and types into the unique
      symbol names the linker works with. Reverse it with ``c++filt``.
      See :term:`Demangling`.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Memory Segment
      One region of a running process's memory image. From the lowest
      address up: reserved, text (code), data, BSS, heap, stack, and
      arguments. Which segment a variable occupies is determined by how
      it is declared.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Namespace
      A declarative region that provides a scope to identifiers inside
      it. Used to organize code and avoid naming collisions. The C++
      Standard Library uses the ``std`` namespace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Naming Collision
      Two entities with the same name visible in the same scope, which the
      compiler cannot disambiguate. Namespaces exist to prevent this.
      Compare shadowing, where an inner declaration hides an outer one
      instead of colliding with it.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Narrowing Conversion
      A type conversion where data loss may occur (e.g., ``double`` to
      ``int``). Disallowed by uniform initialization. Use
      ``static_cast`` for explicit narrowing.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Numeric Conversion
      Any conversion between arithmetic types that is not a promotion,
      such as ``double`` to ``int`` or ``int`` to ``short``. May lose
      data or precision. ``int`` to ``double`` is a conversion too, even
      though nothing is lost.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Numeric Promotion
      The conversion of a smaller numeric type to a larger type within
      the same family. Always safe (no data loss). Examples:
      ``float`` to ``double``, ``char`` to ``int``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Page
      The fixed-size block a memory segment is divided into, typically
      4 KiB. Each page of a process's virtual address space is mapped to
      a **frame**, a physical slot of the same size in RAM. Pages that sit
      side by side in the virtual address space need not be adjacent, or
      in order, in physical memory.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Preprocessor
      The first stage of the C++ build process. Modifies source code
      before compilation by processing directives (``#include``,
      ``#define``, etc.), removing comments, and adjusting whitespace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Rodata Segment
      The region of a process image holding **read-only** data: string
      literals and ``const`` globals. Writing to it traps at runtime.
      Short for read-only data (``.rodata``).
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Scope
      The region of code where a variable can be accessed. Variables
      are *in scope* when accessible and *out of scope* when not.
      Scope is a compile-time property.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Scope Resolution Operator
      The ``::`` operator, which selects a name from a namespace, class,
      or enumeration: ``std::cout``, ``Color::red``. Written with
      nothing on its left (``::value``) it names the global namespace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Scoped Enumeration
      An ``enum class``. A type-safe enumeration whose enumerators are
      scoped to the enum name (``Color::red``) and do **not** implicitly
      convert to ``int``. The underlying integral type can be specified
      after a colon. Preferred over unscoped ``enum``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Shadowing
      Declaring a name in an inner scope that hides the same name from an
      outer scope. The inner declaration wins for the rest of that block;
      the outer object still exists and, if it is global, can still be
      reached through ``::name``. Compile with ``-Wshadow`` to be warned.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Signedness
      Whether an integral type can represent negative values.
      ``signed`` types hold negative, zero and positive values;
      ``unsigned`` types hold only non-negative values, with twice the
      positive range and well-defined wraparound on overflow. Comparing
      the two converts the signed operand first, which is why
      ``-1 < 1u`` is ``false``; C++20's ``std::cmp_less`` and its
      siblings in ``<utility>`` compare by mathematical value instead.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Significant Decimal Digits
      The measure of a floating-point type's precision. Count from the
      **first non-zero digit**, left to right, ignoring where the decimal
      point falls, so ``31415.9``, ``3.14159`` and ``0.0000314159`` each
      carry six. ``float`` carries about 7, ``double`` about 16.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   sizeof
      A C++ operator that returns the size (in bytes) of a type or
      variable. The result is platform-dependent.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Stack Frame
      The block of stack memory one function call occupies: its
      parameters, its local variables, and the bookkeeping needed to
      return. Created on entry and released at the closing brace, which
      is what gives automatic variables their lifetime.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Statement
      A complete instruction that tells the computer to perform a
      specific action. Terminated by a semicolon (``;``) in C++.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   static_cast
      A C++ cast operator used for explicit type conversions. Preferred
      over C-style casts for safe, intentional narrowing conversions.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::boolalpha
      Stream manipulator that prints ``bool`` as the words ``true`` and
      ``false`` instead of ``1`` and ``0``. Sticky; undo it with
      ``std::noboolalpha``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::cin
      The standard input stream. Data is read from it with the extraction
      operator ``>>``, which converts the typed characters into the
      variable's type and stops at whitespace.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::cout
      The standard output stream. Data is sent to it with the insertion
      operator ``<<``, which chains left to right.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::endl
      Stream manipulator that writes a newline **and** flushes the stream.
      Prefer a plain ``'\n'``: the flush is rarely needed and is costly
      inside a loop.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::fixed
      Stream manipulator selecting fixed-point notation for floating-point
      output. It also changes what ``std::setprecision`` counts: digits
      **after the decimal point** rather than significant digits. Undo
      with ``std::defaultfloat``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::format
      The C++20 formatting library, from ``<format>``. Formats one value
      at a time (``std::format("{:.2f}", x)``) with no sticky state,
      replacing ``std::fixed`` and ``std::setprecision``. Requires
      GCC 13.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::numbers
      A C++20 header providing mathematical constants to the full
      precision of the type: ``std::numbers::pi``, ``e``, ``sqrt2``,
      ``ln2``, ``phi``. Use these rather than typing digits.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::scientific
      Stream manipulator selecting scientific notation, as in
      ``3.142e+00``. Like ``std::fixed`` it makes ``std::setprecision``
      count digits after the decimal point. Undo with
      ``std::defaultfloat``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   std::setprecision
      Stream manipulator setting how many digits are shown for
      floating-point output. On its own it counts **significant digits**,
      so ``setprecision(3)`` prints ``3.14``; combined with ``std::fixed``
      it counts digits after the decimal point, so the same call prints
      ``3.142``. Declared in ``<iomanip>``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Storage Duration
      How long a variable's memory exists, fixed by **how it is declared**
      rather than by where it is used. *Static* lasts from before
      ``main()`` until after it returns, *automatic* until the enclosing
      block ends, and *dynamic* until the memory is released. Compare
      lifetime and scope.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Stream
      An object representing a sequence of characters flowing to or from a
      device. ``<iostream>`` declares ``std::cout`` for output and
      ``std::cin`` for input; data moves with ``<<`` and ``>>``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Stream Manipulator
      A value inserted into a stream with ``<<`` that changes **how the
      stream formats**, instead of printing anything itself.
      ``std::cout << std::boolalpha`` outputs zero characters; it sets a
      flag that changes how every later ``bool`` is rendered. Most
      manipulators are *sticky* -- they persist until changed back.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Symbolic Constant
      A constant created with a preprocessor macro, e.g.
      ``#define PI 3.14159``. Avoid in modern C++; use ``constexpr``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Text Segment
      The region of a process image holding the program's **machine
      code**. Read-only, and shared between processes running the same
      executable. Also written ``.text``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Type Conversion
      Producing a value of one type from a value of another. Implicit
      when the compiler does it unprompted, explicit when requested with
      a cast such as ``static_cast``. A conversion never modifies the
      original object.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Type Deduction
      A C++ feature that allows the compiler to deduce the type of a
      variable from its initializer using the ``auto`` keyword.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   typeid
      An operator from ``<typeinfo>`` that reports the type of an
      expression. ``typeid(x).name()`` returns a mangled name; pipe the
      program's output through ``c++filt -t`` to read it.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Undefined Behavior
      The result of executing code that violates the C++ language rules.
      The program may produce correct results, incorrect results, crash,
      or behave erratically. Common examples: reading uninitialized
      variables, array out-of-bounds access, null pointer dereference.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Uniform Initialization
      The modern C++ initialization syntax using braces: ``int a{1};``.
      Prevents narrowing conversions and provides consistent syntax
      across all types. Preferred in this course.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Uninitialized Variable
      A variable declared without an initializer. It holds whatever bits
      were already at its memory location, and reading it is undefined
      behavior. Globals are the exception: they are zeroed in the BSS
      segment.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   using Declaration
      Imports a **single** name from a namespace into the current scope:
      ``using std::cout;``. Preferred over a ``using namespace``
      directive because it brings in only what you asked for.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   using Directive
      ``using namespace X;``. Makes **every** name in namespace ``X``
      available unqualified. Avoid it, and never write one in a header:
      it can create ambiguities and it hides where each name came from.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   using enum
      A C++20 declaration that makes a scoped enumeration's enumerators
      usable unqualified inside one scope: ``using enum RobotState;``.
      Keep it in the narrowest scope that needs it, or it reintroduces
      the name leakage ``enum class`` prevents.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Variable
      A symbolic name for a storage location that holds data. Has five
      characteristics: type, name (identifier), scope, lifetime, and
      value.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Virtual Address Space
      The contiguous range of addresses a process believes it has. The
      operating system maps it onto physical RAM one page at a time, so
      each process gets its own private view and addresses that look
      adjacent to the program may be scattered in hardware.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Word
      A fixed-size unit of data that the processor handles as a single
      entity. Architecture-dependent: commonly 16, 32, or 64 bits.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Zero Initialization
      Initialization with empty braces, ``int a{};``, which sets a
      variable to zero, or to whatever counts as empty for its type.
      Use ``{0}`` when the zero is a value you intend to use, and ``{}``
      when it is a placeholder to be overwritten.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-l3:

L3: Pointers and Memory Management
==================================

.. glossary::

   Alignment
      The requirement that an object's address be a multiple of a certain
      number of bytes, usually its own size. An ``int`` sits at a multiple
      of 4 and a ``double`` at a multiple of 8, which is why addresses in
      these notes end in ``0``, ``4``, ``8`` or ``c``. A ``struct`` takes
      the largest alignment of its members.
      :doc:`L3 </lectures/lecture3/l3_lecture>`,
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Build Type
      The CMake setting (``CMAKE_BUILD_TYPE``) that decides which compiler
      flags are added. ``Debug`` adds ``-g``, ``Release`` adds
      ``-O3 -DNDEBUG``, ``RelWithDebInfo`` adds ``-O2 -g -DNDEBUG``, and
      ``MinSizeRel`` adds ``-Os -DNDEBUG``. Leaving it unset adds nothing
      at all: no optimization and no debug information. This course builds
      ``Debug``, because Valgrind needs ``-g`` to name a line.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Dangling Pointer
      A pointer that points to a memory location that has been
      deallocated. Dereferencing a dangling pointer is undefined
      behavior. Avoid by setting pointers to ``nullptr`` after
      ``delete`` or by using smart pointers.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   delete
      An operator that deallocates memory previously allocated with
      ``new``. Does not destroy the pointer variable itself. Calling
      ``delete`` on a ``nullptr`` is safe. Only ``delete`` what you
      ``new``.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Dereference Operator
      The unary ``*`` operator used to access the value stored at the
      memory address held by a pointer. Also called the indirection
      operator.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Dynamic Memory Allocation
      Reserving memory on the heap at runtime using ``new``. The
      programmer is responsible for freeing this memory with ``delete``
      (or using smart pointers). Allocated objects have no identifier
      and never go out of scope on their own.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Endianness
      The order in which the bytes of a multi-byte object are stored.
      **Little-endian** puts the least significant byte at the lowest
      address and is what every machine in this course uses;
      **big-endian** puts the most significant byte first and is the order
      the internet protocols specify. It changes nothing inside one
      program, and becomes visible in a debugger, in a hex dump, or when
      raw bytes cross machines.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Heap
      A region of memory used for dynamic memory allocation at runtime.
      Memory on the heap persists until explicitly deallocated. Flexible
      in size but requires manual management (or smart pointers).
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Hexadecimal
      Base 16, written with the ``0x`` prefix and the digits ``0``--``9``
      then ``a``--``f``. One hex digit is exactly 4 bits, so two hex
      digits are exactly one byte, which is why addresses and memory dumps
      are printed this way. Beware the arithmetic: ``0x28 + 8`` is
      ``0x30``, not ``0x36``.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Memory Leak
      Occurs when dynamically allocated memory is not freed. Reduces
      available memory and can cause performance degradation or crashes.
      Detected with tools like Valgrind.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   new
      An operator that dynamically allocates memory on the heap at
      runtime and returns a pointer to the allocated memory. Must be
      paired with ``delete`` to avoid memory leaks.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   nullptr
      A keyword representing a null pointer literal. Preferred over
      ``NULL`` or ``0`` for initializing pointers that do not yet point
      to a valid object. Deleting a ``nullptr`` is safe.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Ownership
      The responsibility for releasing a resource. A raw pointer records
      no ownership: ``T*`` looks identical whether it owns a heap block,
      merely observes one, or points at storage that has already been
      freed. Leaks, double deletes and dangling pointers are all
      ownership mistakes, which is why C++ expresses ownership in the
      type instead: ``std::unique_ptr``, ``std::shared_ptr``, or a
      container. An **owner** of a heap object keeps it alive; with several
      owners, the last one to let go deletes it.
      :doc:`L3 </lectures/lecture3/l3_lecture>`,
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Pointer
      A variable that holds a memory address as its value. The address
      belongs to a variable, literal, or function. Declared with
      ``type* identifier;``. Must be initialized to avoid undefined
      behavior.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Reference
      An alias for an existing variable. Must be initialized at
      declaration, cannot be null, and cannot be reseated. Shares the
      same memory address as the original variable. Syntax:
      ``type& identifier{existing_variable};``
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Sanitizer
      Compiler instrumentation that checks a program as it runs.
      ``-fsanitize=address`` catches use-after-free, buffer overruns and
      leaks; ``-fsanitize=undefined`` catches undefined behavior such as
      signed overflow and null dereference. Roughly 2x slower than an
      uninstrumented build, against Valgrind's 20x, and the two find
      overlapping but not identical sets of bugs.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Stack
      A region of memory used for automatic memory allocation. Local
      variables and function parameters are stored here. Memory is
      automatically deallocated when variables go out of scope. Fast
      but limited in size.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Valgrind
      A programming tool for memory management, memory error detection,
      and profiling. Detects memory leaks, use-after-free, and other
      memory errors. Essential for C++ development with raw pointers.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Wild Pointer
      A pointer that has not been initialized to a known memory
      address. Holds a garbage value pointing to an unknown location.
      Dereferencing a wild pointer is undefined behavior.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-l4:

L4: The Standard Library and Its Containers
===========================================

.. glossary::

   Aggregate
      A class with no constructor of its own, such as ``std::array`` or
      a plain ``struct``. Nothing runs when one is declared, so its
      members hold garbage until braces zero or fill them.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Amortized O(1)
      Constant cost per operation on average over a long run, even
      though one operation now and then is expensive. ``push_back`` is
      amortized O(1): a reallocation moves every element, but geometric
      growth makes reallocations rare.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Array decay
      The rule that an array name turns into a pointer to its first
      element in almost every expression. It happens automatically and
      the length goes with it, so ``sizeof`` on the pointer gives 8, not
      the array size. ``std::array`` never decays.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Associative container
      A container that stores key and value pairs and finds a value from
      its key rather than from a position: ``std::map`` (sorted) and
      ``std::unordered_map`` (hashed).
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Big-O notation
      The notation that states time complexity: O(1), O(log n), O(n),
      O(n log n), O(n²). It keeps the fastest-growing term and drops
      constant factors, so it names the shape of the growth, not a
      count.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   C-string
      Not a type: a ``char`` array that everyone agrees ends with a
      ``'\0'`` byte. The length is stored nowhere; ``strlen`` walks to
      the terminator, O(n), on every call. A string literal is a
      C-string in the read-only ``.rodata`` segment.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Cache line
      The unit the hardware fetches from memory, 64 bytes on a typical
      CPU, which is 16 ``int`` values. Walking contiguous memory in
      order lets one fetch serve the next 16 reads.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Capacity
      How many elements a ``std::vector`` or ``std::string`` could hold
      before the block has to be replaced. Never smaller than
      ``size()``. Read it with ``capacity()``, raise it with
      ``reserve()``, release it with ``shrink_to_fit()``.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Class template
      A recipe for a type, not a type. ``std::array`` on its own is not
      a type; ``std::array<int, 6>`` and ``std::array<double, 6>`` are
      two different types made from the same template.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Contiguous
      Stored in one block with no gaps, so element *i* sits exactly i ×
      sizeof(element) bytes after element 0 and its address is
      arithmetic, not a lookup. Arrays, ``std::vector`` and
      ``std::string`` are contiguous; the maps are not.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   emplace_back
      A ``std::vector`` member that builds the new element directly in
      the vector from constructor arguments, so no temporary is created.
      ``push_back`` builds the object first and then moves it in. For
      ``int`` or ``double`` the difference is nothing.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Erase-remove idiom
      The pre-C++20 way to remove every element equal to a value:
      ``v.erase(std::remove(v.begin(), v.end(), x), v.end())``. Since
      C++20 it is one call, ``std::erase(v, x)`` or ``std::erase_if(v,
      predicate)``.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Half-open range
      The pair [begin, end): closed on the left, open on the right. The
      first position is in the range, the last one is not, so ``end() -
      begin()`` is the length with no plus or minus one, and an empty
      container is ``begin() == end()``.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Iterator
      An object that identifies a position in a sequence and can advance
      to the next one, supporting ``*``, ``++``, ``==`` and ``!=``. For
      an array it really is a pointer. ``begin()`` names the first
      element and ``end()`` the position one past the last.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Iterator invalidation
      An iterator, pointer or reference into a container stops being
      usable once a later operation moves or destroys what it points at.
      A ``std::vector`` reallocation invalidates everything; ``erase``
      invalidates from the erased position on; reading never
      invalidates.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   npos
      What ``std::string::find`` returns when nothing is found. Not a
      special marker: the largest possible ``std::size_t``,
      18446744073709551615. Always compare a ``find`` result against
      ``npos``.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Occupancy grid
      A map cut into cells, each recording whether that patch of floor
      is free, blocked, or never scanned. Store one number per cell and
      the map becomes a two-dimensional array in row-major order.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Predicate
      A function or lambda that answers yes or no: it returns a ``bool``.
      ``count_if``, ``find_if`` and ``std::erase_if`` call one with one
      element at a time; ``std::sort`` takes one with two parameters that
      says which element comes first. You pass a function's name without
      parentheses.
      :doc:`L4 </lectures/lecture4/l4_lecture>`,
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   RAII
      Resource acquisition is initialization: the constructor takes the
      resource, the destructor gives it back, and the compiler runs the
      destructor on every way out of the scope. It is why a
      ``std::vector`` needs no ``delete``. Smart pointers apply the same idea to single objects.
      :doc:`L4 </lectures/lecture4/l4_lecture>`,
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Range-based for
      A loop that visits every element in order without an index: ``for
      (const auto& r : container)``. You never write the bounds, so it
      cannot run off either end. Use ``const auto&`` by default,
      ``auto&`` to modify, ``auto`` for a copy.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Reallocation
      What a ``std::vector`` does when ``size() == capacity()`` and
      another element arrives: allocate a larger block, move every
      element across, free the old block, update its three pointers.
      O(n) once, and the reason every iterator into the old block
      dangles.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   reserve
      ``vector::reserve(n)`` allocates a block for at least ``n``
      elements now. Capacity becomes at least ``n``, size does not
      change, and it never shrinks. Use it whenever the count is known
      up front; it also prevents invalidation during the fill.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Row-major order
      Rows stored one after another in one flat block. ``grid[i][j]``
      sits at element i × cols + j, so the compiler must know the row
      width but not the number of rows, and the last index belongs in
      the inner loop.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   shrink_to_fit
      ``vector::shrink_to_fit()`` asks the vector to release spare
      capacity so that capacity drops to size. The standard calls it a
      non-binding request; when it shrinks, it reallocates and moves
      every element.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Small String Optimization (SSO)
      A small buffer kept inside the ``std::string`` object and used
      whenever the text fits, so short strings never touch the heap. The
      object is 32 bytes on libstdc++ and holds up to 15 characters in
      place; the number belongs to the implementation.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::array
      A class template from ``<array>`` that wraps a C array of the same
      size: the same bytes, no header, plus the members a C array lacks
      (``size()``, ``at()``, ``begin()``, ``fill()``, ``data()``). Its
      length is part of its type, so it never decays.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::map
      An associative container that keeps its keys in sorted order in a
      balanced binary tree. Lookup, insert and erase cost O(log n), the
      elements are not contiguous, and iterating visits the keys in
      order.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::size_t
      The one unsigned type every size in the standard library uses,
      from ``<cstddef>``: what ``sizeof`` and every ``size()`` return.
      Subtracting past zero wraps to the top of the range, and ``i >=
      0`` is always true.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::string
      A class from ``<string>`` that owns its characters and stores its
      length. It took ``std::vector``'s interface and C++20 calls it a
      contiguous container, though it never came from the STL. It keeps
      a ``'\0'`` after the last character for C APIs.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::string_view
      A pointer and a length over someone else's characters. It owns,
      allocates and copies nothing, which makes it the right read-only
      parameter type and a dangling view if it outlives the string it
      refers to.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::unordered_map
      An associative container that stores each pair in a bucket chosen
      by a hash function. Lookup is O(1) on average and O(n) at worst,
      and there is no order at all.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   std::vector
      A sequence container that holds its elements contiguously on the
      heap and resizes itself as elements are added or removed. The
      object is three pointers (begin, end, capacity), 24 bytes; the
      elements live in a separate heap block.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   STL
      The Standard Template Library, written by Stepanov and Lee at HP
      in the early 1990s and adopted into the draft standard in 1994.
      Containers, iterators and algorithms came from it; the standard
      itself never uses the name.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   STL algorithm
      A function template that operates on a range given by two
      iterators, independently of the container that supplied them:
      ``sort``, ``find``, ``count_if``, ``min_element``, ``accumulate``.
      Since C++20, ``std::ranges::`` versions take the container
      directly.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   STL Container
      A class template from the Standard Template Library that owns a
      collection of objects of one type and manages their storage. Four
      categories: sequence, associative, unordered associative, and
      container adapters.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Subscript inserts
      On a map, ``operator[]`` with a missing key builds a default
      value, inserts it and hands you a reference to it, so a read makes
      the map bigger. Read with ``at()``, ask with ``contains()`` or
      ``find()``, and use ``[]`` only when inserting is wanted.
      :doc:`L4 </lectures/lecture4/l4_lecture>`

   Time complexity
      How the number of steps an operation takes grows with the size of
      its input, n. Written in Big-O notation. Not seconds: it drops the
      machine, the compiler and constant factors and keeps the shape of
      the growth.
      :doc:`L4 </lectures/lecture4/l4_lecture>`


.. _g-l5:

L5: Functions
=============

.. glossary::

   Copy Elision
      A compiler optimization that eliminates unnecessary copy/move operations when returning objects from functions. Guaranteed in C++17 for certain cases (RVO).
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   Default Parameter
      A value provided in a function declaration that is used when no argument is supplied for that parameter. Must be specified from right to left.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   Function Overloading
      Defining multiple functions with the same name but different parameter lists. The compiler selects the correct overload based on the arguments.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   inline
      A specifier that lets a function be defined in a header that several
      ``.cpp`` files include. Without it, each file gets its own copy of
      the body and the linker reports ``multiple definition``.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   Recursion
      A programming technique where a function calls itself to solve a problem by breaking it into smaller subproblems. Requires a base case to terminate.
      :doc:`L5 </lectures/lecture5/l5_lecture>`

   Static Variable
      A local variable that retains its value between function calls. Initialized once and persists for the program's lifetime.
      :doc:`L5 </lectures/lecture5/l5_lecture>`


.. _g-l6:

L6: Functions Advanced
======================

.. glossary::

   Abbreviated Function Template
      A function with ``auto`` as a parameter type, such as
      ``void print_all(const auto& values)``. It is a template written
      without the ``template`` line, and each ``auto`` is its own template
      parameter. C++20.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Aggregate Initialization
      Giving the members of an aggregate their values from a braced list,
      in the order they are declared:
      ``RobotStatus robot_3{3, 64.0, {2.0, 3.0}, false};``. A member the
      list does not reach takes its default member initializer, or zero.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   alignof
      An operator that gives a type's alignment in bytes. With g++ 13 on
      x86-64, ``alignof(int)`` is 4 and ``alignof(double)`` is 8. C++11.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Callable
      Anything you can call with parentheses: a function, a lambda, a
      pointer to a function, or an object that holds one of them.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Callback
      A callable you hand over now, for other code to call later. ROS 2
      calls a subscription's callback each time a message arrives.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Capture Clause
      The ``[ ]`` at the start of a lambda, which lists the local variables
      the lambda keeps. ``[limit_pct]`` copies the variable when the lambda
      is created; ``[&limit_pct]`` stores a reference and reads the variable
      at each call. ``[=]`` and ``[&]`` capture every local the body uses.
      A lambda that is returned or stored should capture by value, or its
      references can dangle.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Concept
      A named test on a template parameter. The compiler runs it at each
      call, before it writes the function, and rejects the call if the test
      fails. Examples: ``std::integral``, ``std::floating_point``. You write
      it in place of ``typename`` (``template <std::integral T>``), in a
      ``requires`` clause, or before ``auto`` (``std::integral auto id``).
      C++20, header ``<concepts>``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   decltype
      An operator that gives the type of a name or an expression, without
      evaluating it. ``decltype(battery_pct[0])`` is ``double&``, because
      ``operator[]`` returns a reference.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Deduced Return Type
      A return type written as ``auto``: the compiler works it out from the
      ``return`` statements, which must all give the same type. The body
      must be visible before any call, so the function goes in the header.
      C++14.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Default Member Initializer
      A value written next to a member in a ``struct``, such as
      ``double battery_pct{100.0};``. It is used whenever the braced list
      does not reach that member, so the member never holds garbage.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Dependent Name
      A name inside a template whose meaning depends on a template
      parameter, such as ``Container::value_type``. The compiler assumes
      it names a value; write ``typename`` in front when it names a type.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Designated Initializer
      Aggregate initialization that names each member it sets:
      ``RobotStatus robot_1{.id = 1, .battery_pct = 82.5};``. The names must
      follow declaration order, and you may skip members. C++20.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Function Pointer
      A pointer that holds the address of a function:
      ``double (*convert)(double){to_fraction};``. Calling through it calls
      that function. A lambda with no capture converts to one; a lambda
      that captures does not.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Function Template
      A pattern for a family of functions, introduced by
      ``template <typename T>``. The compiler writes one function from it
      for each set of types you call it with. The whole template, body
      included, goes in a header.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Functor
      Also called a function object. An object that can be called like a
      function, because its type defines ``operator()``. A lambda
      expression creates one: an object of an unnamed ``struct`` whose
      members are the captures.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Generic Lambda
      A lambda with ``auto`` as a parameter type:
      ``[](const auto& left, const auto& right) { ... }``. Like an
      abbreviated function template, it works for any types the body
      accepts, and each ``auto`` is a separate type.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Higher-Order Function
      A function that takes a callable as a parameter, or returns one. The
      standard algorithms ``std::count_if``, ``std::find_if`` and
      ``std::sort`` are higher-order functions.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Init-capture
      A capture that makes a new variable only the lambda has, with its own
      initializer: ``[id = 100]() mutable { return ++id; }``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Instantiation
      The compiler writing a real function from a template, for the types of
      one call. ``clamp_value(130, 0, 100)`` instantiates
      ``clamp_value<int>``; later calls with ``int`` arguments reuse it.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Lambda
      An expression that creates a callable right where it is used:
      ``[captures](parameters) { body }``. It makes an object of an unnamed
      ``struct`` whose members are the captures. Its main use is as the
      argument of a higher-order function such as ``std::count_if``. Its
      type has no name, so you store one with ``auto``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   mutable (Lambda)
      A keyword after a lambda's parameter list that lets the body change
      its by-value captures, which are read-only without it. The changed
      value lives inside the lambda object, so a copy of the lambda counts
      on its own.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   offsetof
      A macro from ``<cstddef>``. ``offsetof(Type, member)`` is the number
      of bytes from the start of an object to that member, so it shows
      where the compiler put padding.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Padding
      Unused bytes the compiler adds inside a ``struct`` so that each
      member's address is a multiple of its alignment, and at the end so
      that the elements of an array stay aligned. With g++ 13 on x86-64,
      ``RobotStatus`` holds 29 bytes of data and its ``sizeof`` is 40.
      Putting the largest members first leaves fewer gaps; the compiler
      never reorders members.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Projection
      A function that a ``std::ranges`` algorithm calls on each element
      before it compares, turning the element into the value to compare.
      ``std::ranges::sort(fleet, {}, [](const RobotStatus& robot) { return
      robot.battery_pct; })`` sorts the robots by battery. C++20.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   requires Clause
      A condition on template parameters, written after the ``template``
      line, that the compiler checks at each call:
      ``requires std::integral<T> && (!std::same_as<T, bool>)``. Of the
      three ways to apply a concept, it is the only one that joins tests
      with ``&&``, ``||`` and ``!``. C++20.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   std::bind
      A standard function from ``<functional>`` that makes a new callable
      from an existing one, with some arguments fixed:
      ``std::bind(charge_time_h, _1, 40.0)``. The placeholders ``_1``,
      ``_2`` stand for the arguments of the new call. ``std::bind_front``
      (C++20) fixes arguments from the left, with no placeholders. Prefer a
      lambda; learn ``std::bind`` to read older code and ROS 2 examples.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   std::function
      A standard type from ``<functional>`` that holds any callable with a
      given signature, captures included: ``std::function<double(double)>``.
      Use it to store a callable and call it later. Calling an empty one
      throws ``std::bad_function_call``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   std::optional
      A standard type, ``std::optional<T>``, that holds one value of type
      ``T`` or nothing. ``return std::nullopt;`` returns it empty. Read it
      with ``*`` after checking ``if (opt)``, with ``value()``, which throws
      ``std::bad_optional_access`` when it is empty, or with
      ``value_or(fallback)``. ``*`` on an empty optional is undefined
      behavior. In ``<optional>``, C++17.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   std::pair
      A standard ``struct`` with two members, ``first`` and ``second``, of
      any two types: ``std::pair<int, double> reading{3, 64.0};``. Each
      element of a ``std::map`` is a ``std::pair``. In ``<utility>``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   std::tuple
      A standard type that holds any number of values, of any types, read by
      position with ``std::get<0>``, ``std::get<1>`` and so on. The values
      have no names. In ``<tuple>``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   struct
      A type you define that gives one name to a group of variables, its
      members. The definition goes in a header and ends with a semicolon.
      A ``struct`` and a ``class`` differ only in default access.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Structured Binding
      A declaration that gives a new name to each member of a ``struct``, a
      pair or a tuple, in declaration order:
      ``auto [boxes, left_over] = pack(17, 5);``. It needs one name per
      member. ``auto`` binds to a copy; ``auto&`` binds to the original.
      C++17.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Template
      A mechanism for writing generic code that works with any data type. The compiler generates specific versions (instantiations) for each type used.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Template Argument Deduction
      The compiler working out a template parameter from the types of the
      arguments in a call. It takes the types as written, with no
      conversions, so ``clamp_value(104, 0.0, 100.0)`` fails: ``T`` cannot
      be both ``int`` and ``double``. Write ``clamp_value<double>`` to set
      ``T`` yourself. The type of the variable that receives the result is
      not used.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Template Parameter
      A name, such as ``T`` in ``template <typename T>``, that stands for a
      type in a template. ``typename`` and ``class`` mean the same thing in
      that line; the course uses ``typename``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Template Specialization
      A version of a template written for one specific type:
      ``template <> const char* larger_of<const char*>(...)``. For a
      function template, prefer an overload: specializations do not take
      part in overloading.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Trailing Return Type
      A return type written after the parameters with ``->``:
      ``auto add_offset(T value, U offset) -> decltype(value + offset)``.
      It can name the parameters, which the front of the line cannot. A
      lambda uses it too: ``[](double pct) -> double { ... }``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Alignment" target="_blank" rel="noopener">Alignment</a> (L3), <a href="#term-Predicate" target="_blank" rel="noopener">Predicate</a> (L4).</p>


.. _g-l7:

L7: Smart Pointers and Move Semantics
=====================================

.. glossary::

   Control Block
      The part of a ``std::shared_ptr``'s heap memory that holds the count
      of owners and the count of ``std::weak_ptr``\ s. A ``std::shared_ptr`` is
      two pointers, 16 bytes: one to the object and one to the control block.
      ``std::make_shared`` puts the object and the control block in one
      allocation (56 bytes for a ``RobotStatus``); with ``new`` there are two
      (40 and 24 bytes). Measured with g++ 13.3 and libstdc++.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Deleted Function
      A function that is declared so that calling it is a compile error, and
      is never defined. The copy constructor of ``std::unique_ptr`` is deleted,
      so ``std::unique_ptr<RobotStatus> copy{robot};`` does not compile: g++
      reports "use of deleted function".
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Deleter
      What a smart pointer calls to give the memory back. For
      ``std::unique_ptr<T>`` the default is ``std::default_delete<T>``, which
      calls ``delete``. A ``std::unique_ptr`` takes another deleter as its
      second template argument, for example a lambda.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   glvalue
      An expression whose evaluation determines the identity of an object,
      bit-field or function. In plain words, it names something with an
      address. A glvalue is an lvalue or an xvalue. C++20 [basic.lval].
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Indirect Leak
      A leaked heap block that LeakSanitizer finds reachable only from another
      leaked block. Two robots that own each other through
      ``std::shared_ptr``\ s are reported as two indirect leaks.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   LeakSanitizer
      The leak checker that comes with ``-fsanitize=address``. When the
      program ends, it reports each heap block that was never freed, with its
      size and the line that allocated it. AddressSanitizer "integrates
      LeakSanitizer and enables it by default on supported platforms".
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   lvalue
      An expression that refers to an object that already exists, and does
      not let another object take its contents: an object made from it is a
      copy. C++20 calls it a glvalue
      that is not an xvalue. A named variable, ``*ptr``, ``fleet[0]``, a call
      that returns ``T&``, and a string literal are lvalues. You can take an
      lvalue's address.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Move
      Handing what one object owns to another. A move of a ``std::vector``
      gives its three pointers (24 bytes) to the new vector and copies no
      element. A **copy** makes a second object with its own memory: a new
      block, every element copied. The source of a move still exists, as a
      moved-from object.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Moved-from Object
      The source of a move. It still exists, and it is destroyed at the end
      of its scope as usual. The standard leaves moved-from library objects "in
      a valid but unspecified state" unless it says otherwise, so destroy it or
      assign it a new value before you use it again. A moved-from
      ``std::unique_ptr`` is guaranteed to be empty.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   noexcept
      A specifier that promises no exception leaves the function. The
      compiler does not check the promise. If an exception does leave, the
      program calls ``std::terminate`` and stops.
      :doc:`EH </reading_material/exception_handling/eh_lecture>`,
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   prvalue
      An expression that does not refer to an object that already exists. It
      computes a value, and that value can initialize a new object. A literal
      such as ``42``, ``a + b``, and a call that returns by value are
      prvalues. You cannot take a prvalue's address.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Reference Cycle
      Objects that own each other through ``std::shared_ptr``\ s. When the
      outside owners are gone, each count stays at 1, never 0, so no object is
      deleted and the memory leaks. Make one link a ``std::weak_ptr`` to break
      the cycle.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Reseat
      To make a pointer own a different object. A function that takes a
      ``std::unique_ptr<T>&`` may reseat the caller's pointer: the caller keeps
      ownership, and only what it owns changes.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   rvalue
      A prvalue or an xvalue: something you may move from. An rvalue
      reference binds only to rvalues.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   rvalue Reference
      A reference declared with ``&&``, such as ``std::vector<Position>&&``.
      It binds only to rvalues, and says that whatever it refers to may be
      taken. A named rvalue reference is an lvalue, so a function must write
      ``std::move`` again to move from its ``T&&`` parameter.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Smart Pointer
      An object that points at one heap object and says, in its type, how
      that object is owned. The owning ones delete the object when its last
      owner lets go. Lecture 7 covers ``std::unique_ptr`` (the only owner),
      ``std::shared_ptr`` (one of several owners) and ``std::weak_ptr``, an
      observer that owns nothing. A raw pointer cannot say any of this.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   std::make_shared
      A function from ``<memory>`` that creates an object on the heap and
      returns the ``std::shared_ptr`` that owns it. Its arguments go to the
      object. It puts the object and the control block in one allocation.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   std::make_unique
      A function from ``<memory>`` that creates an object on the heap and
      returns the ``std::unique_ptr`` that owns it:
      ``std::make_unique<RobotStatus>(3, 64.0, Position{2.0, 3.0}, false)``.
      Its arguments go to the object. With it, you write no ``new`` and no
      ``delete``.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   std::move
      A cast to an rvalue reference, from ``<utility>``. ``std::move(route)``
      is an xvalue that marks ``route`` as an object you may take from. It
      moves nothing by itself: the move happens if a move constructor or a
      ``&&`` overload takes the result. On a ``const`` object the compiler
      copies instead, and on a returned local it blocks copy elision.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   std::shared_ptr
      A smart pointer that is one of several owners of an object on the
      heap. The owners share a count in a control block. A copy adds an owner,
      a move hands one owner's place to another, and the last owner to let go
      deletes the object. It is two pointers, 16 bytes. Make one with
      ``std::make_shared``.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   std::unique_ptr
      A smart pointer that is the only owner of one object on the heap. It
      cannot be copied, only moved, and when it is destroyed it deletes the
      object. It is 8 bytes with g++ 13.3 and libstdc++, the same as a raw
      pointer. Make one with ``std::make_unique``.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   std::weak_ptr
      A smart pointer that watches an object that ``std::shared_ptr``\ s own.
      It does not add to the count, so it never keeps the object alive. It has
      no ``->`` and no ``*``: ``lock()`` returns a ``std::shared_ptr`` to the
      object, or an empty one if the object is gone, and ``expired()`` is
      ``true`` when the count is 0. It breaks reference cycles.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Temporary Materialization
      Creating a temporary object from a prvalue when the code needs an
      object, for example to read a member. In ``make_robot(3).id``, the
      compiler creates a temporary robot, and the expression becomes an xvalue
      that names it. The temporary is destroyed at the end of the full
      expression. C++20 [conv.rval].
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   use_count
      A member of ``std::shared_ptr`` and ``std::weak_ptr`` that returns how
      many ``std::shared_ptr``\ s own the object. A copy adds 1, a move leaves
      it unchanged, and ``reset()`` or destroying an owner subtracts 1. The
      object is deleted when the count reaches 0.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   Value Category
      The property of an expression that says whether it names an object,
      and whether that object's resources may be taken. Every expression is
      exactly one of lvalue, xvalue or prvalue, and ``decltype((e))`` tells
      which: ``T&``, ``T&&`` or ``T``. The **type** of an expression is a
      separate property.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

   xvalue
      An expression that refers to an object that already exists, and lets
      another object take its contents: the object may be moved from. C++20
      calls it a glvalue whose
      object's resources can be reused.
      ``std::move(route)``, a cast to ``T&&``, and a member of an xvalue are
      xvalues. Naming an xvalue moves nothing.
      :doc:`L7 </lectures/lecture7/l7_lecture>`

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-Ownership" target="_blank" rel="noopener">Ownership</a> (L3), <a href="#term-RAII" target="_blank" rel="noopener">RAII</a> (L4).</p>


.. _g-l8:

L8: OOP Basics
==============

.. glossary::

   Access Specifier
      Keywords (``public``, ``private``, ``protected``) that control the visibility and accessibility of class members.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Class
      A user-defined type that encapsulates data (attributes) and behavior (methods). A blueprint for creating objects.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Constructor
      A special member function automatically called when an object is created. Initializes the object's data members.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Encapsulation
      An OOP principle that bundles data and methods that operate on that data within a single class, restricting direct access to internal state.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Member Initialization List
      A constructor syntax that initializes data members before the constructor body executes. More efficient than assignment in the body. Required for ``const`` and reference members.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   Object
      An instance of a class. Contains its own copy of the class's data members and can call the class's methods.
      :doc:`L8 </lectures/lecture8/l8_lecture>`

   this Pointer
      An implicit pointer available inside non-static member functions that points to the object on which the method was called.
      :doc:`L8 </lectures/lecture8/l8_lecture>`


.. _g-l9:

L9: OOP Advanced
================

.. glossary::

   Abstract Class
      A class with at least one pure virtual function. Cannot be instantiated directly; serves as an interface for derived classes.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Aggregation
      A "has-a" relationship where the part can exist independently of the whole. Represented by an empty diamond in UML.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Association
      A general relationship between classes where objects of one class use or interact with objects of another.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Composition
      A strong "has-a" relationship where the part cannot exist without the whole. The whole manages the lifetime of its parts.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Inheritance
      An OOP mechanism where a derived class acquires the properties and behaviors of a base class. Supports code reuse and hierarchical relationships.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Polymorphism
      The ability to process objects differently based on their type. Compile-time (overloading) and runtime (virtual functions) forms exist in C++.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Pure Virtual Function
      A virtual function declared with ``= 0`` that has no implementation in the base class. Forces derived classes to provide their own implementation.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Virtual Destructor
      A destructor declared ``virtual`` to ensure proper cleanup when deleting a derived object through a base class pointer.
      :doc:`L9 </lectures/lecture9/l9_lecture>`

   Virtual Function
      A member function declared with the ``virtual`` keyword that enables runtime polymorphism. The correct function is called based on the actual object type, not the pointer/reference type.
      :doc:`L9 </lectures/lecture9/l9_lecture>`


.. _g-vc:

Reading: Version Control
========================

.. glossary::

   Bare repository
      A repository holding history but no checked-out files. This is what a
      server holds. ``git init --bare`` creates one, which is all a remote
      needs to be.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Branch
      A file under ``.git/refs/heads/`` holding one commit hash. Creating a
      branch copies no files, which is why it is instant. The file is
      rewritten forward with each new commit on that branch.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Clone
      A complete copy of a repository, including its full history and every
      branch. A clone is a repository in its own right, not a view of one
      elsewhere.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Commit
      One saved snapshot of the project, with a message saying what changed
      and why. A commit never changes once made; its hash is fixed and it
      records its parent, so commits form a chain backwards through history.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Detached HEAD
      The state where ``.git/HEAD`` holds a commit hash instead of a branch
      name. You are on a commit rather than a branch, so new commits have no
      branch to move forward and become unreachable when you switch away.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Diverged
      The state where two branches each hold commits the other lacks, so
      neither can fast-forward to the other. Distinct from one branch simply
      being **ahead** of another.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Fast-forward
      A merge that needs no new commit because the target branch is an
      ancestor of the source. Git just moves the branch pointer forward.
      ``--no-ff`` forces a merge commit instead, preserving the record that a
      branch existed.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Fetch
      Downloading commits from a remote and updating the remote-tracking
      branches. It does not touch your branch or your files, which is what
      makes it safe to run at any time.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Fork
      A server-side copy of a repository under your own account. A GitHub
      feature, not a Git one. It lets you contribute without write access to
      the original.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   HEAD
      The file ``.git/HEAD``, holding the name of the branch you are
      currently on. It normally points at a branch, and through that branch
      at a commit.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Hunk
      One contiguous block of changed lines in a diff, with a few unchanged
      lines of context either side. ``git add -p`` stages a hunk at a time.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Merge
      Combining another branch's commits into the current branch. Produces a
      merge commit with two parents, unless it can fast-forward.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Merge conflict
      What happens when two branches change the same lines and Git cannot
      choose between them. Git pauses, writes ``<<<<<<<``, ``=======`` and
      ``>>>>>>>`` markers into the file, and waits for you to decide.
      ``git merge --abort`` backs out.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Origin
      The conventional name for the remote a repository was cloned from.
      Nothing about the name is special; it is set by ``git clone`` or by
      ``git remote add origin``.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Pull
      ``fetch`` followed by ``merge``, in one command. Downloads commits from
      a remote and integrates them into the current branch.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Pull request
      A request to merge one branch into another, with review and discussion
      attached. A GitHub feature, not a Git one. A pull request tracks a
      **branch**, so pushing again updates the same request.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Push
      Uploading commits from a local branch to a remote. Rejected if the
      remote holds commits you do not have, which protects a teammate's work
      from being overwritten.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Rebase
      Replaying your commits on top of another branch, producing new commits
      with new hashes and a linear history. Never rebase commits others
      already have.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Reflog
      A local record of every position ``HEAD`` has held, including commits
      no branch points at any more. The way to recover work after a deleted
      branch or a bad reset. Local to one clone, and it expires.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Remote
      A repository your repository can reach. It need not be a service: a
      folder, a USB stick, or any machine you can reach over SSH all work.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Remote-tracking branch
      A local, read-only pointer such as ``origin/main``, recording where a
      branch on the remote was **the last time you fetched**. Not the remote
      itself, and it does not update on its own.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Repository
      A project plus its complete history, stored in the hidden ``.git``
      directory at the project root.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Revert
      Adding a new commit that undoes an earlier one. The safe way to undo
      anything already pushed, because it adds to history rather than
      rewriting it.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Sparse checkout
      Checking out only part of a repository's tree. Combined with a partial
      clone (``--filter=blob:none``) it cuts both disk and download
      substantially. A convenience, not access control: the history is still
      complete.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Staging area
      The area holding the changes that will go into the next commit. Filled
      by ``git add``, emptied by ``git commit``. Also called the index.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Stash
      A scratch area for uncommitted changes, letting you switch branches
      with a clean working tree. Local, never pushed, and not a backup.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Tag
      A name permanently attached to one commit. Unlike a branch it does not
      move, which is what makes it usable for marking a submission or a
      release.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Tracked file
      A file Git already knows about, because an earlier ``git add``
      introduced it. Git watches tracked files for changes and reports them;
      untracked files it ignores until added.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Upstream
      The remote pointing at the original repository you forked from, by
      convention named ``upstream``. Fetching from it is how a fork is kept
      in sync.
      :doc:`VC </reading_material/version_control/vc_lecture>`

   Working directory
      The actual project files on disk, the ones you edit. One of Git's three
      areas, alongside the staging area and the repository.
      :doc:`VC </reading_material/version_control/vc_lecture>`


.. _g-eh:

Reading: Exception Handling
===========================

.. raw:: html

   <p class="glossary-also">Also used here: <a href="#term-noexcept" target="_blank" rel="noopener">noexcept</a> (L7).</p>
