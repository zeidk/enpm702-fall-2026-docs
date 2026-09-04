====================================================
Quiz
====================================================

This self-check quiz covers :doc:`Lecture 2 <l2_lecture>`.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True/False questions ask whether the statement is correct as
     written.
   - Answer first, then open the dropdown. Reading the answer before
     committing to one teaches you nothing.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   After ``double b{};``, what does ``b`` hold?

   A. Garbage, because there is no initializer between the braces.
   B. ``0.0``.
   C. Nothing; the line does not compile.
   D. The same value as an uninitialized ``double``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``0.0``.

   *Explanation:* Empty braces perform **zero initialization**: the variable is set to zero, or to whatever counts as empty for its type (``false`` for ``bool``). Empty braces are not the same as no initializer at all. ``double b;`` leaves garbage and reading it is undefined behavior. Note that ``std::cout`` prints ``0`` rather than ``0.0``, because it drops digits after the decimal point that add nothing.


----

.. admonition:: Question 2
   :class: hint

   In ``std::cin >> age;``, what is ``>>`` called and what does it do?

   A. The insertion operator; it writes ``age`` to the terminal.
   B. The right-shift operator; it divides ``age`` by two.
   C. The extraction operator; it reads a value from the stream into ``age``.
   D. The scope resolution operator; it selects ``age`` from ``std``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, the extraction operator.

   *Explanation:* ``>>`` pulls data out of the input stream and stores it in the variable on its right. ``<<`` is the insertion operator and goes the other way. ``::`` is the scope resolution operator, which is what makes ``std::cin`` name ``cin`` inside the namespace ``std``. The arrows point in the direction the data travels.


----

.. admonition:: Question 3
   :class: hint

   Which of the following is the correct way to use uniform (brace) initialization in C++?

   A. ``int speed = 10;``
   B. ``int speed(10);``
   C. ``int speed{10};``
   D. ``int speed[10];``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``int speed{10};``

   *Explanation:* Uniform initialization uses curly braces ``{}``. This is the preferred initialization style in modern C++ because it prevents narrowing conversions. Option A is copy initialization, B is direct initialization, and D declares an array.


----

.. admonition:: Question 4
   :class: hint

   What is the output of the following code?

   .. code-block:: cpp

      int value{5};
      {
          int value{10};
          std::cout << value;
      }
      std::cout << value;

   A. ``55``
   B. ``1010``
   C. ``105``
   D. ``510``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``105``

   *Explanation:* The inner block declares a new variable ``value`` that shadows the outer one. Inside the block, ``value`` is 10. Once the block ends, the inner ``value`` goes out of scope, and the outer ``value`` (which is 5) is printed. The inner declaration never modified the outer variable.


----

.. admonition:: Question 5
   :class: hint

   What does the ``sizeof`` operator return?

   A. The value stored in a variable.
   B. The number of bits used by a type.
   C. The number of bytes used by a type or variable.
   D. The memory address of a variable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, The number of bytes used by a type or variable.

   *Explanation:* ``sizeof`` returns a size in **bytes**, and it is evaluated by the compiler rather than at runtime. ``sizeof(int)`` is 4 on the machines used in this course, but the standard specifies only minimum widths, so the value is platform-dependent. The **address** of a variable comes from the ``&`` operator instead.


----

.. admonition:: Question 6
   :class: hint

   A global variable is declared as ``int counter;`` with no initializer. Which memory segment does it occupy, and what is its initial value?

   A. Stack; undefined garbage.
   B. BSS; zero.
   C. Data; undefined garbage.
   D. Heap; zero.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, BSS, and it is zero.

   *Explanation:* **Uninitialized** globals and statics go in the BSS segment, which the loader zeroes before ``main()`` runs. **Initialized** globals go in the data segment. This is the one case where an uninitialized variable is not garbage; a *local* ``int counter;`` sits on the stack and reading it is undefined behavior.


----

.. admonition:: Question 7
   :class: hint

   Which of the following demonstrates a narrowing conversion that uniform initialization would catch?

   A. ``int x{5};``
   B. ``double d{3.14};``
   C. ``int x{3.14};``
   D. ``float f{3.14f};``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``int x{3.14};``

   *Explanation:* Assigning a ``double`` literal (3.14) to an ``int`` using brace initialization is a narrowing conversion, and the compiler rejects it because the fractional part would be lost. ``int x = 3.14;`` and ``int x(3.14);`` request the same conversion and compile silently. That difference is one of the main reasons this course uses braces.


----

.. admonition:: Question 8
   :class: hint

   Which of these is a numeric **promotion** rather than a numeric conversion?

   A. ``double`` to ``float``
   B. ``short`` to ``int``
   C. ``int`` to ``double``
   D. ``double`` to ``long double``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``short`` to ``int``.

   *Explanation:* Promotions are a fixed, short list: ``char``, ``short`` and ``bool`` to ``int``, and ``float`` to ``double``. Everything else between arithmetic types is a **conversion**, even when nothing is lost. ``int`` to ``double`` and ``double`` to ``long double`` are widening but are still classified as conversions; ``double`` to ``float`` loses precision outright.


----

.. admonition:: Question 9
   :class: hint

   What is the difference between ``const`` and ``constexpr``?

   A. ``const`` is evaluated at compile time; ``constexpr`` is evaluated at runtime.
   B. ``constexpr`` guarantees compile-time evaluation; ``const`` only means the value cannot be modified after initialization.
   C. They are identical in behavior.
   D. ``constexpr`` can only be used with integers.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``constexpr`` guarantees compile-time evaluation; ``const`` only means the value cannot be modified after initialization.

   *Explanation:* A ``const`` variable can be initialized with a runtime value, for example from ``std::cin``, in which case it is a *runtime* constant. ``constexpr`` requires an initializer the compiler can evaluate, and rejects anything else. Nothing in the source tells you which kind of ``const`` you have, which is exactly what ``constexpr`` fixes.


----

.. admonition:: Question 10
   :class: hint

   Why does this course prefer ``constexpr double pi{3.14159};`` over ``#define PI 3.14159``?

   A. Macros are slower at runtime.
   B. Macros cannot represent floating-point values.
   C. Macros have no type checking, no scope, and do not survive into the debugger.
   D. Macros were removed from the language in C++20.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, no type checking, no scope, and invisible to the debugger.

   *Explanation:* A macro is a blind text substitution performed by the preprocessor, so the compiler never sees a type to check and the name is gone by the time code is generated. Macros also ignore namespaces and blocks, living from their ``#define`` to the end of the translation unit. They are not slower, since the substitution happens before compilation, and they still exist in C++20. For pi specifically, the best answer is neither: use ``std::numbers::pi`` from ``<numbers>``.


----

.. admonition:: Question 11
   :class: hint

   What naming convention does this course use for variables?

   A. camelCase (e.g., ``myVariable``)
   B. PascalCase (e.g., ``MyVariable``)
   C. snake_case (e.g., ``my_variable``)
   D. Hungarian notation (e.g., ``iMyVariable``)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, snake_case (e.g., ``my_variable``)

   *Explanation:* The C++ Core Guidelines recommend underscore-style names (``NL.10``), and this course follows that. ALL_CAPS is conventionally reserved for macros, which is one more reason not to use macros for constants.


----

.. admonition:: Question 12
   :class: hint

   Given the following code, what is the type of ``result``?

   .. code-block:: cpp

      int a{5};
      double b{2.5};
      auto result = a + b;

   A. ``int``
   B. ``float``
   C. ``double``
   D. ``long``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``double``

   *Explanation:* ``double`` outranks ``int`` in the usual arithmetic conversions, so ``a`` is converted to ``double`` before the addition and the expression has type ``double``. ``auto`` then deduces that. The deduced type follows the **expression**, not the first operand.


----

.. admonition:: Question 13
   :class: hint

   With ``int a{7};`` and ``int b{2};``, what does ``std::cout << a / b;`` print?

   A. ``3.5``
   B. ``4``
   C. ``3``
   D. It fails to compile.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``3``.

   *Explanation:* Both operands are ``int``, so no conversion happens and integer division is performed: the fractional part is discarded, not rounded. To get ``3.5``, convert one operand at the point of use: ``static_cast<double>(a) / b``. Casting the whole expression, ``static_cast<double>(a / b)``, is too late, since ``7 / 2`` has already collapsed to ``3``.


----

.. admonition:: Question 14
   :class: hint

   What happens when you read an uninitialized local variable in C++?

   A. It is automatically initialized to zero.
   B. The compiler always generates an error.
   C. It results in undefined behavior.
   D. It is initialized to ``nullptr``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, It results in undefined behavior.

   *Explanation:* The variable holds whatever bits were already at that memory location. The compiler may warn with ``-Wall``, but it is not required to, and the program may well print a plausible-looking number. That is the dangerous case: it works on your machine and fails on the grader's.


----

.. admonition:: Question 15
   :class: hint

   After ``const int a{5}; auto b{a};``, what is the type of ``b``?

   A. ``const int``
   B. ``int``
   C. ``auto``
   D. It fails to compile.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``int``.

   *Explanation:* Type deduction drops the top-level ``const`` qualifier, so ``b`` is a plain ``int`` and can be reassigned. To keep the qualifier, write ``const auto b{a};`` or ``constexpr auto b{a};``.


----

.. admonition:: Question 16
   :class: hint

   Which statement about namespaces is correct?

   A. ``using namespace std;`` is recommended in header files.
   B. Namespaces prevent naming collisions by grouping identifiers under a unique name.
   C. You cannot nest namespaces inside other namespaces.
   D. The ``::`` operator is called the dot operator.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, Namespaces prevent naming collisions by grouping identifiers under a unique name.

   *Explanation:* ``using namespace std;`` in a header is the worst place for it, because every file that includes the header inherits the problem. Namespaces can be nested, and ``::`` is the scope resolution operator.


----

.. admonition:: Question 17
   :class: hint

   Why does ``enum class Color { red };`` not collide with ``enum class TrafficLight { red };``?

   A. Because the two enums have different underlying types.
   B. Because the enumerators are scoped to the enum name, so they are ``Color::red`` and ``TrafficLight::red``.
   C. Because enumerators are always converted to ``int`` first.
   D. It does collide; the code does not compile.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, the enumerators are scoped to the enum name.

   *Explanation:* This is the "scoped" in *scoped enumeration*. The same two declarations written with unscoped ``enum`` **would** collide, because unscoped enumerators leak into the enclosing scope. Scoped enumerators also do not convert implicitly to ``int``; you need ``static_cast``.


----

.. admonition:: Question 18
   :class: hint

   What is ``c++filt -t`` used for?

   A. Reformatting source code to the course style.
   B. Filtering compiler warnings out of the build log.
   C. Demangling the compiler-generated type and symbol names in a program's output.
   D. Checking a program for undefined behavior.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, demangling.

   *Explanation:* The compiler encodes names and types into the unique symbols the linker works with, a process called mangling. ``c++filt`` reverses it, which is what makes an ``undefined reference to _ZN5Robot4moveEv`` readable as ``Robot::move()``. Note that for the fundamental types ``typeid(x).name()`` already prints a short code (``i``, ``d``, ``m``) that you can simply look up.


----

True/False
==========

.. admonition:: Question 19
   :class: hint

   **True or False:** ``char``, ``signed char``, and ``unsigned char`` are three names for the same type.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* They are three **distinct** types, and whether plain ``char`` is signed is implementation-defined. This is the exception to the rule that ``signed`` is the default: for the integer types, ``signed int`` really is the same type as ``int``.


----

.. admonition:: Question 20
   :class: hint

   **True or False:** A ``constexpr`` variable can be initialized with a value obtained from ``std::cin``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* ``constexpr`` requires a value the compiler can compute while compiling, and ``std::cin`` does not read anything until the program runs. Use ``const`` for a value that is fixed but not known until runtime.


----

.. admonition:: Question 21
   :class: hint

   **True or False:** In C++, ``bool`` values ``true`` and ``false`` convert to the integers ``1`` and ``0`` respectively.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* ``bool`` to ``int`` is an integral promotion, with ``true`` becoming 1 and ``false`` becoming 0. Going the other way, **any** non-zero value converts to ``true``. Use ``std::boolalpha`` if you want ``true`` and ``false`` printed as words.


----

.. admonition:: Question 22
   :class: hint

   **True or False:** A variable declared inside a block can be accessed after the block ends.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Its scope ends at the closing brace, and using the name afterwards is a **compile error**, not a runtime one. Scope is a compile-time property, which is why the compiler catches this class of mistake for you.


----

.. admonition:: Question 23
   :class: hint

   **True or False:** ``static_cast<int>(3.7)`` evaluates to ``4``, because the conversion rounds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* The result is ``3``. Floating-to-integral conversion **truncates** toward zero; it discards the fractional part rather than rounding. ``static_cast`` is preferred over a C-style cast because it is explicit and greppable.


----

.. admonition:: Question 24
   :class: hint

   **True or False:** ``-1 < 1u`` evaluates to ``true``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* ``unsigned int`` outranks ``int``, so ``-1`` is converted to ``unsigned`` first and becomes 4,294,967,295, which is not less than 1. This is why mixing signed and unsigned values in a comparison is a bug waiting to happen, and why ``-Wsign-compare`` (part of ``-Wall``) warns about it.


----

.. admonition:: Question 25
   :class: hint

   **True or False:** Signed integer overflow and unsigned integer overflow both have well-defined behavior in C++.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* **Unsigned** overflow is well defined and wraps modulo :math:`2^n`. **Signed** overflow is undefined behavior, and the compiler is allowed to optimize on the assumption that it never happens, which is how code that "obviously" works can be transformed into something that does not.


----

.. admonition:: Question 26
   :class: hint

   **True or False:** ``using Integer = int;`` creates a new type that is distinct from ``int``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* A type alias creates a second **name** for an existing type, not a new type. ``Integer`` and ``int`` are interchangeable everywhere, and the compiler will not stop you from mixing them. What an alias buys you is readability and one place to change.


----

.. admonition:: Question 27
   :class: hint

   **True or False:** The literal ``1.05`` has type ``float``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* An unsuffixed floating-point literal is a ``double``. Add the ``f`` (or ``F``) suffix to make it a ``float``: ``1.05f``. Note that the suffix requires a floating-point literal, so ``1f`` is an error while ``1.0f`` is fine.
