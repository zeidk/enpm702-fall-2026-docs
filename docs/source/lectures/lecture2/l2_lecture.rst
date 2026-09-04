====================================================
Lecture
====================================================

Lecture 1 covered what C++ is, why this course targets **C++20**, and the
path a program takes from source text to a running process. This lecture
starts writing that source text. It covers the pieces every C++ program is
built from: input and output, variables, types, conversions between types,
constants, scope, and namespaces.

.. note::

   Everything on this page is compiled with the course toolchain:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -Wpedantic -g main.cpp -o main

   If that command is not working yet, fix your environment before going
   further. See :doc:`/lectures/lecture1/l1_lecture`.

.. seealso::

   Assumed from :doc:`Lecture 1 </lectures/lecture1/l1_lecture>` and not
   repeated here: ``main()`` and the structure of a minimal program;
   the preprocessor, compiler and linker stages and their ``g++``
   flags; statements and comments; the ``'\n'`` convention; and
   ``-Wall -Wextra``. Go back to that page if any of those are hazy,
   because everything below builds on them.


Basic Input and Output
====================================================

C++ programs talk to the terminal through **streams** declared in the
``<iostream>`` header. Two of them matter for now:

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ``std::cout``
        :class-card: sd-border-secondary

        The standard **output** stream. Data is sent to it with the
        **insertion operator** ``<<``.

    .. grid-item-card:: ``std::cin``
        :class-card: sd-border-secondary

        The standard **input** stream. Data is read from it with the
        **extraction operator** ``>>``.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Reading** ``std::cout``

    - ``std`` is a **namespace**, the one the entire standard library
      lives in.
    - ``::`` is the **scope resolution operator**. ``std::cout`` means
      "the name ``cout`` found in the namespace ``std``".
    - The arrows point in the direction the data travels:
      ``std::cout << value`` sends ``value`` **into** the stream;
      ``std::cin >> value`` pulls data **out of** the stream and into
      ``value``.

.. dropdown:: Output with ``std::cout``
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           std::cout << "Hello, World!";           // text, no newline
           std::cout << '\n';                      // newline
           std::cout << "Number: " << 42 << '\n';  // chained insertions
           std::cout << "Pi: " << 3.14159 << '\n';
       }

    Insertions chain because each ``<<`` returns the stream itself, so
    the next ``<<`` operates on the same stream.

.. dropdown:: Input with ``std::cin``
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           int age{};
           double height{};

           std::cout << "Enter your age: ";
           std::cin >> age;                        // reads an int

           std::cout << "Enter your height: ";
           std::cin >> height;                     // reads a double

           std::cout << "Age: " << age
                     << ", Height: " << height << '\n';
       }

    A variable must be **declared before** you can read into it, and
    ``std::cin`` converts the typed characters into the variable's type
    for you.

.. important::

   Every ``std::cout`` on this page ends with ``'\n'``, never
   ``std::endl``. That is the course convention, and
   :doc:`Lecture 1 </lectures/lecture1/l1_lecture>` explains why.


Bits, Bytes, and Words
====================================================

Every type in this lecture is ultimately a number of bytes in memory, so
the vocabulary is worth pinning down.

.. grid:: 1 3 3 3
    :gutter: 3

    .. grid-item-card:: Bit
        :class-card: sd-border-secondary

        A **binary digit**: ``0`` or ``1``. The smallest unit of data.

    .. grid-item-card:: Byte
        :class-card: sd-border-secondary

        A group of **8 bits**, and the smallest individually
        **addressable** unit of memory on typical architectures.

    .. grid-item-card:: Word
        :class-card: sd-border-secondary

        The amount of data the processor handles **as a single entity**.
        Architecture-dependent: commonly 16, 32, or 64 bits.

.. figure:: /_static/images/l2/memory.png
   :align: center
   :alt: A row of eight bit cells labeled as one byte, with a wider bracket labeled one word.

   Bits, bytes, and words.


Memory Segments
---------------

When the OS loader brings an executable into RAM, the process image is
divided into segments. Which segment a variable lands in is decided by
**how** you declare it, and it is the reason global and local variables
behave differently later in this lecture.

.. list-table:: Segments of a running process, from the lowest address up.
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - Segment
     - Contents
   * - **Reserved**
     - Address ``0x0`` and the region around it. Never a valid object;
       this is what makes dereferencing a null pointer detectable.
   * - **Text (code)**
     - The program's machine instructions. Read-only.
   * - **Data**
     - **Initialized** global and static variables.
   * - **BSS**
     - **Uninitialized** global and static variables. Zeroed by the
       loader.
   * - **Heap**
     - Dynamically allocated memory. Grows upward. Covered in Lecture 3.
   * - **Stack**
     - Local variables and function-call bookkeeping. Grows downward.
   * - **Arguments**
     - Command-line arguments and the environment passed to ``main()``.

.. figure:: /_static/images/l2/representation.png
   :align: center
   :alt: A memory bank divided into reserved, text, data, BSS, heap, stack and argument segments, expanded below into a grid of addressable bytes.

   The segments of a process, and the same memory seen as a sequence of
   addressable bytes.

.. note::

   Nothing in this lecture allocates memory you have to manage
   yourself: every variable here is placed automatically, in the
   segment its declaration implies. Lecture 3 introduces the heap,
   where the amount of memory in use becomes your problem, and with it
   the ways that can go wrong.


Variables
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A **variable** is a **symbolic name** for a storage location that
    holds data. The name lets you read and modify that storage without
    ever writing down an address.


Characteristics
---------------

Every variable has five properties. The rest of this lecture works
through each of them.

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Type
        :class-card: sd-border-secondary

        What kind of value the variable can hold, and therefore how much
        memory it occupies.

    .. grid-item-card:: Name (identifier)
        :class-card: sd-border-secondary

        The symbolic name. Unique within its scope.

    .. grid-item-card:: Scope
        :class-card: sd-border-secondary

        The region of code where the name can be used.

    .. grid-item-card:: Lifetime
        :class-card: sd-border-secondary

        How long the variable exists in memory while the program runs.

    .. grid-item-card:: Value
        :class-card: sd-border-secondary

        The data currently stored at the variable's location.

.. dropdown:: All five, on one line of code
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           int number{20};
       }

    - **Type:** ``int``
    - **Name:** ``number``
    - **Value:** ``20``
    - **Scope:** the body of ``main()``
    - **Lifetime:** from the declaration until ``main()`` returns


Naming (Identifiers)
---------------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Rules the compiler enforces**

    - Identifiers may contain **letters**, **digits**, and
      **underscores** only.
    - They must **begin** with a letter or an underscore, never a digit.
    - They are **case sensitive**: ``count``, ``Count`` and ``COUNT`` are
      three different names.
    - They cannot be a
      `reserved keyword <https://en.cppreference.com/w/cpp/keyword>`_.

.. dropdown:: Legal and illegal identifiers
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       int break1;     // OK
       int break_1;    // OK
       int Break1;     // OK
       int BREAK;      // OK
       int _break1;    // legal, but see the warning below
       int 1Break;     // Error: an identifier cannot start with a digit
       int my-name;    // Error: '-' is not part of an identifier
       int class;      // Error: 'class' is a reserved keyword

.. warning::

   **Do not start an identifier with an underscore.** ``_break1`` above
   compiles, but the rule is subtler than it looks: a name beginning
   with an underscore followed by a **capital** letter, and any name
   containing a **double underscore**, is reserved for the
   implementation *everywhere*, and a name with a single leading
   underscore is reserved at **namespace scope**. Using one is not a
   compile error; it is a collision waiting to happen with something
   inside your standard library. Avoid the whole category.

.. warning::

   **This course uses** ``snake_case``: lowercase words separated by
   underscores.

   **Use:**

   - ``my_variable``
   - ``student_count``
   - ``max_temperature``
   - ``is_valid``

   **Avoid:**

   - ``camelCase``, e.g. ``myVariable``
   - ``PascalCase``, e.g. ``MyVariable``
   - ``ALL_CAPS``, e.g. ``MY_VARIABLE``, which by convention signals a
     macro

.. seealso::

   C++ Core Guidelines:
   `NL.8: Use a consistent naming style <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl8-use-a-consistent-naming-style>`_,
   `NL.10: Prefer underscore_style names <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl10-prefer-underscore_style-names>`_,
   `NL.19: Avoid names that are easily misread <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl19-avoid-names-that-are-easily-misread>`_.


Variable Types
--------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Primitive types
        :class-card: sd-border-secondary

        Built into the language and usable with no header:
        ``int``, ``double``, ``char``, ``bool``, ``float``, and their
        modified forms.

    .. grid-item-card:: Standard Library types
        :class-card: sd-border-secondary

        Provided by the standard library and available once the right
        header is included: ``std::string``, ``std::vector``,
        ``std::array``.

    .. grid-item-card:: User-defined types
        :class-card: sd-border-secondary

        Types you write yourself with ``class``, ``struct``, or
        ``enum class``.

.. note::

   The compiler uses a variable's type for two things:

   1. To know **how much memory** to reserve for it.
   2. To know **what kind of value** it may hold, so it can reject
      operations that make no sense.


sizeof Operator
^^^^^^^^^^^^^^^

``sizeof`` reports the size in **bytes** of a type or of the type an
expression would produce. It is evaluated by the compiler, not at
runtime.

.. code-block:: cpp

   int number{20};
   std::cout << sizeof(number) << '\n';  // 4 on a typical x86-64 machine
   std::cout << sizeof(int) << '\n';     // 4 on a typical x86-64 machine

.. note::

   **Sizes are platform-dependent.** The standard specifies minimums, not
   exact sizes. ``sizeof(int)`` is 4 on the machines used in this course,
   but the language does not promise that. Run the code above on your own
   machine and compare.


Memory Allocation
-----------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What** ``int number{20};`` **actually does**

    1. **Reserves** 4 bytes of memory (the size of an ``int`` here).
    2. **Associates** the address of the first of those bytes with the
       name ``number``.
    3. **Writes** ``20``, in binary, across those 4 bytes.
    4. **Restricts** those bytes to holding an ``int``, so the compiler
       can reject misuse.

.. tip::

   The **address-of operator** ``&`` gives you the address of a variable:

   .. code-block:: cpp

      int number{20};
      std::cout << &number << '\n';  // e.g. 0x7fff214aba04

   The value changes from run to run. A variable declared inside a
   function lives in the **stack** segment; Lecture 3 covers this in
   depth.

.. figure:: /_static/images/l2/demo.png
   :align: center
   :alt: The four bytes of the variable number, at consecutive addresses, located inside the stack segment of a memory bank.

   ``int number{20};`` occupies four consecutive bytes in the stack
   segment.

Reading the variable back reverses the process. For
``std::cout << number;`` the CPU goes to ``number``'s address, reads the
4 bytes stored there, interprets that bit pattern as an ``int``, and
prints the decimal value.

.. figure:: /_static/images/l2/visualization.png
   :align: center
   :alt: The raw four-byte binary layout on the left, and the simplified single labeled box holding the value 20 on the right.

   From here on, memory is drawn in this simplified form: a named box,
   its value, and its address.


Declarations
^^^^^^^^^^^^

A **declaration** states a variable's type and name, which is what lets
the compiler type-check every later use of it.

.. code-block:: cpp

   int number;  // number is declared and defined

.. note::

   Strictly, the line above is both a **declaration** (it introduces the
   name and its type) and a **definition** (it is what causes storage to
   be reserved). Every declaration of a variable in this lecture is also
   a definition, so the distinction does not bite yet. It starts to
   matter in Lecture 5, where a function can be declared in one place
   and defined in another.

More than one variable of the same type can be declared in one
statement, but do not.

.. code-block:: cpp

   int number1, number2, number3;  // legal, but avoid

.. seealso::

   C++ Core Guidelines:
   `ES.10: Declare one name (only) per declaration <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es10-declare-one-name-only-per-declaration>`_.


Assignments
^^^^^^^^^^^

Once declared, a variable is given a value with the **assignment
operator** ``=``. This is called *copy assignment*.

.. code-block:: cpp

   int number;                    // declaration
   number = 1;                    // assignment
   std::cout << number << '\n';   // 1
   number = 2;                    // assignment
   std::cout << number << '\n';   // 2

.. note::

   Assigning ``2`` **overwrites** the ``1`` that was there. A variable
   holds exactly one value at a time. If you are coming from Python,
   note that the name is not rebound to a new object here: the same 4
   bytes are rewritten in place.


Initializations
^^^^^^^^^^^^^^^

Declaration and assignment can be collapsed into one step, called
**initialization**. The value used is the **initializer**.

.. list-table:: The three forms of initialization.
   :widths: 26 30 44
   :header-rows: 1
   :class: compact-table

   * - Form
     - Syntax
     - Notes
   * - Copy initialization
     - ``int a = 1;``
     - Inherited from C. Little used in modern C++.
   * - Direct initialization
     - ``int a(1);``
     - Introduced for efficient initialization of class types. Also
       little used now.
   * - **Uniform initialization**
     - ``int a{1};``
     - Braces. The modern form, and **the one this course uses**.

.. tip::

   **Use uniform initialization.** Before it existed, some situations
   required copy initialization and others required direct
   initialization. Braces work consistently for every kind of object,
   built-in types, arrays, vectors, and class members alike, which is
   where the name comes from. They also reject narrowing conversions,
   as shown under :ref:`l2-numeric-conversion`.

.. seealso::

   C++ Core Guidelines:
   `ES.20: Always initialize an object <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es20-always-initialize-an-object>`_.


Zero Initialization
^^^^^^^^^^^^^^^^^^^

Empty braces initialize a variable to zero, or to whatever counts as
empty for its type. The standard calls this **value-initialization**,
which for the built-in types here means zeroing them; "zero
initialization" is the name you will see in most tutorials.

.. code-block:: cpp

   #include <iomanip>
   #include <iostream>

   int main() {
       int a{};                 // 0
       double b{};              // 0.0
       bool c{};                // false

       std::cout << a << '\n';  // 0
       std::cout << b << '\n';  // 0  <- cout drops the trailing .0
       std::cout << std::fixed << std::setprecision(1)
                 << b << '\n';  // 0.0
   }

.. note::

   ``std::cout`` omits digits after the decimal point when they add
   nothing. ``std::fixed`` forces fixed-point notation, and
   ``std::setprecision`` (from ``<iomanip>``) sets how many digits follow
   the decimal point.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **When to write** ``{0}`` **and when to write** ``{}``

    - Use ``{0}`` when the zero is a value you actually intend to use.
    - Use ``{}`` when the value is a placeholder that will be replaced
      before it is read.

    .. code-block:: cpp

       int a{};    // placeholder: a is assigned before it is read
       int b{0};   // the value 0 is meaningful here
       a = b + 3;


Uninitialized Variables
^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   A variable that is declared but not initialized holds whatever bits
   were already at that memory location. Reading it is **undefined
   behavior**.

   .. code-block:: cpp

      int number;                   // uninitialized
      std::cout << number << '\n';  // undefined behavior: garbage

   This is why ``ES.20`` says *always* initialize. ``int number{};``
   costs nothing and removes the problem.


Undefined Behavior
====================================================

.. card::
    :class-card: sd-border-danger sd-shadow-sm

    **Definition**

    **Undefined behavior** (UB) is what you get when a program breaks the
    rules of the language. The standard then imposes **no requirements at
    all**: the program may produce the right answer, produce a wrong
    answer, crash, or behave differently on the next run or under a
    different optimization level.

.. dropdown:: Common sources of undefined behavior
    :class-container: sd-border-secondary
    :open:

    - **Reading an uninitialized variable.** Covered above.
    - **Array out-of-bounds access.** Reading or writing past the end of
      an array. Lecture 4.
    - **Null pointer dereference.** Lecture 3.
    - **Signed integer overflow.** Exceeding the range of a signed
      integer. Note that *unsigned* overflow is well defined and wraps.

.. important::

   **UB that appears to work is the dangerous case.** A program that
   crashes tells you something is wrong. A program that reads garbage and
   happens to print a plausible number tells you nothing, and will fail
   later on a different machine.

.. tip::

   The warning flags from :doc:`Lecture 1 </lectures/lecture1/l1_lecture>`
   catch **some** of this, and reading an uninitialized variable is one
   of the cases they usually catch. Do not mistake that for a
   guarantee: most undefined behavior is invisible at compile time,
   because proving it would require the compiler to know what the
   program will do at runtime. A clean build is not evidence that a
   program is free of UB.

   See the
   :doc:`compiler warnings reading module </reading_material/compiler_warnings/cw_lecture>`
   for what each flag actually detects.


Integral Types
====================================================

**Integral types** represent whole numbers, with no fractional part.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **The integral types**

    ``bool``, ``char``, ``short``, ``int``, ``long``, ``long long``, and
    the ``unsigned`` counterparts of the integer types. Each has its own
    size and range, which depend on the architecture and the compiler.

    (The language also has the wide character types ``wchar_t``,
    ``char8_t``, ``char16_t`` and ``char32_t``. This course does not use
    them.)


Signedness Modifiers
--------------------

A **signedness modifier** controls whether a type can represent negative
values.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ``signed``
        :class-card: sd-border-secondary

        Holds **negative, zero, and positive** values. The default for
        the integer types.

        - Matches the mathematical integers, so arithmetic and
          comparisons behave the way you expect.
        - The right default for general calculation, and for anything
          involving subtraction.

    .. grid-item-card:: ``unsigned``
        :class-card: sd-border-secondary

        Holds **zero and positive** values only.

        - Doubles the positive range: every bit encodes magnitude.
        - Overflow is **well defined** and wraps modulo :math:`2^n`.
        - Natural for sizes, counts, indices, and bit manipulation.

.. note::

   **The trade-off.** Reach for ``signed`` for ordinary arithmetic. Reach
   for ``unsigned`` when negative values are meaningless *and* you need
   the extra positive range or the defined wraparound. Mixing the two in
   one expression is where the bugs are, as the next section shows.


Size Modifiers
--------------

**Size modifiers** change how many bits an integer type uses, and
therefore its range.

.. list-table:: Guaranteed minimum widths.
   :widths: 25 25 50
   :header-rows: 1
   :class: compact-table

   * - Type
     - Minimum width
     - Notes
   * - ``short``
     - 16 bits
     - Smaller range, smaller footprint.
   * - ``int``
     - 16 bits
     - In practice matches the processor's natural word size, which is
       why it is 32 bits on x86-64.
   * - ``long``
     - 32 bits
     - 64 bits on 64-bit Linux, 32 bits on Windows.
   * - ``long long``
     - 64 bits
     - Always at least 64 bits.

.. note::

   The standard guarantees only these minimums and the ordering:

   ``sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)``

   When you need an **exact** width, use the fixed-width types from
   ``<cstdint>``: ``int8_t``, ``int32_t``, ``uint64_t``, and so on. These
   matter as soon as you touch hardware registers or serialized message
   formats.


Type, Size, and Range
---------------------

.. list-table:: Typical sizes and ranges on a 64-bit Linux machine.
   :widths: 18 10 36 36
   :header-rows: 1
   :class: compact-table

   * - Type
     - Size (bytes)
     - Signed range
     - Unsigned range
   * - ``char``
     - 1
     - -128 to 127
     - 0 to 255
   * - ``short``
     - 2
     - -32,768 to 32,767
     - 0 to 65,535
   * - ``int``
     - 4
     - -2,147,483,648 to 2,147,483,647
     - 0 to 4,294,967,295
   * - ``long``
     - 8
     - -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
     - 0 to 18,446,744,073,709,551,615
   * - ``long long``
     - 8
     - -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
     - 0 to 18,446,744,073,709,551,615

.. note::

   **Modifiers you can leave out.** ``signed`` is the default for the
   integer types, and ``int`` is implied after a size modifier. So all of
   these name the same type:

   - ``signed long int``, ``signed long``, ``long int``, ``long``
   - ``signed int`` and ``int``
   - ``unsigned int`` and ``unsigned``

   ``char`` is the exception: plain ``char``, ``signed char`` and
   ``unsigned char`` are **three distinct types**, and whether plain
   ``char`` is signed is implementation-defined.


Compiler Behavior Differences
------------------------------

.. card::
    :class-card: sd-border-warning sd-shadow-sm

    **Signed and unsigned are not interchangeable**

    - **Comparisons can invert.** ``-1 < 1u`` evaluates to ``false``: the
      ``-1`` is converted to unsigned first and becomes 4,294,967,295.

      .. code-block:: cpp

         std::cout << std::boolalpha << (-1 < 1u) << '\n';  // false

    - **Overflow differs.** Signed overflow is **undefined behavior**;
      unsigned overflow wraps and is fully defined.
    - **Optimization differs.** Because signed overflow is UB, the
      compiler may optimize on the assumption that it never happens.
    - **Mixed arithmetic follows conversion rules** that are easy to get
      wrong. See :ref:`l2-arithmetic-conversion`.

.. tip::

   ``-Wsign-compare``, included in ``-Wall``, warns about comparisons
   between signed and unsigned operands. Do not ignore it.

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **C++20: comparisons that do the right thing**

    C++20 added a family of integer comparison functions in
    ``<utility>`` that compare the **mathematical values**, ignoring the
    conversion rules entirely:

    .. code-block:: cpp

       #include <iostream>
       #include <utility>

       int main() {
           std::cout << std::boolalpha;
           std::cout << (-1 < 1u) << '\n';                    // false: the trap
           std::cout << std::cmp_less(-1, 1u) << '\n';        // true:  correct
       }

    The full set is ``std::cmp_equal``, ``cmp_not_equal``, ``cmp_less``,
    ``cmp_greater``, ``cmp_less_equal`` and ``cmp_greater_equal``. Reach
    for them whenever you have to compare a signed value against an
    unsigned one and cannot fix the types instead.

    Fixing the types is still the better answer when you control them.
    These functions are for the cases where you do not, which in
    practice means comparing your ``int`` against something's
    ``.size()``.


Floating-point Number Types
====================================================

**Floating-point types** represent real numbers, with a fractional part.
The **precision** of such a type is the number of significant decimal
digits it can carry, not the number of digits after the decimal point.
All floating-point types are **signed**.


Precision and Range
-------------------

.. list-table:: Typical sizes, ranges, and precision on x86-64 Linux.
   :widths: 22 14 34 30
   :header-rows: 1
   :class: compact-table

   * - Type
     - Size (bytes)
     - Magnitude range
     - Significant digits
   * - ``float``
     - 4
     - ~1.18e-38 to ~3.40e+38
     - 6 to 9, typically 7
   * - ``double``
     - 8
     - ~2.23e-308 to ~1.80e+308
     - 15 to 17, typically 16
   * - ``long double``
     - 16
     - ~3.36e-4932 to ~1.19e+4932
     - about 18

.. note::

   ``long double`` varies more across platforms than any other
   arithmetic type: it is the 80-bit extended format on x86-64 Linux,
   but identical to ``double`` on ARM and on MSVC. Do not write code
   that depends on its size.

.. important::

   **Use** ``double`` **by default.** ``float`` buys you memory, not
   accuracy, and 7 significant digits is not much for sensor math.
   Reserve ``float`` for large arrays and for interfaces that require it.


Float Suffix
^^^^^^^^^^^^

A floating-point literal with no suffix is a ``double``. The ``f`` (or
``F``) suffix makes it a ``float``.

.. code-block:: cpp

   std::cout << 1.05 << '\n';   // double literal
   std::cout << 1.05f << '\n';  // float literal
   std::cout << 1.0f << '\n';   // OK
   std::cout << 1f << '\n';     // Error: invalid suffix "f" on integer constant

.. note::

   The last line fails because ``1`` is an *integer* literal, and ``f``
   is not a valid integer suffix. Write ``1.0f``.


std::setprecision
^^^^^^^^^^^^^^^^^

``std::cout`` shows 6 significant digits by default.
``std::setprecision()``, from ``<iomanip>``, changes that.

.. code-block:: cpp

   #include <iomanip>   // std::setprecision
   #include <iostream>

   int main() {
       std::cout << std::setprecision(9);
       std::cout << 0.33333333333f << '\n';           // 0.333333343

       std::cout << std::setprecision(15);
       std::cout << 8.3642343534322323232322 << '\n'; // 8.36423435343223
   }

.. note::

   ``0.33333333333f`` prints as ``0.333333343``. That is not a display
   bug: a ``float`` holds roughly 7 significant digits, so asking for 9
   exposes the representation error. Asking for more digits than the type
   carries never adds information.

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **C++20:** ``std::format``

    The manipulators above are **sticky**: ``std::setprecision(9)``
    changes the stream until something changes it back, so a formatting
    choice made in one function silently affects output written by
    another. C++20's ``<format>`` header formats a single value instead,
    with no side effects on the stream:

    .. code-block:: cpp

       #include <format>
       #include <iostream>

       int main() {
           const double reading{3.14159265};

           std::cout << std::format("{:.2f}\n", reading);   // 3.14
           std::cout << std::format("{:.5f}\n", reading);   // 3.14159
           std::cout << std::format("distance: {:.2f} m\n", reading);
       }

    ``{:.2f}`` means "this argument, fixed notation, two digits after
    the point". It replaces ``std::fixed << std::setprecision(2)`` and
    reads far better inside a sentence.

    .. note::

       ``<format>`` requires **GCC 13**, which is the course minimum, so
       it works for you. It arrived in libstdc++ later than the rest of
       C++20, so older compilers that otherwise accept ``-std=c++20``
       will reject it. Lecture examples continue to use ``<<`` because
       later lectures do, but use ``std::format`` in your own code where
       it is clearer.


Boolean Type
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **The** ``bool`` **type**

    - Size: **1 byte** on every platform this course uses, though the
      standard does not require it.
    - Values: ``true`` or ``false``.
    - Any **non-zero** value converts to ``true``; ``0`` converts to
      ``false``. Converting back gives ``1`` and ``0``.

.. dropdown:: Printing booleans
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           bool is_today_sunny{true};
           bool is_today_cloudy{false};

           std::cout << is_today_sunny << '\n';   // 1
           std::cout << is_today_cloudy << '\n';  // 0

           // std::boolalpha prints the words instead of the digits
           std::cout << std::boolalpha;
           std::cout << is_today_sunny << '\n';   // true
           std::cout << is_today_cloudy << '\n';  // false

           // std::noboolalpha switches back
           std::cout << std::noboolalpha;
           std::cout << is_today_sunny << '\n';   // 1
       }

    ``std::boolalpha`` is *sticky*: it changes the stream until you
    change it back with ``std::noboolalpha``.


Type Conversion
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    **Type conversion** produces a value of one type from a value of
    another. It is **implicit** when the compiler does it on its own, and
    **explicit** when you ask for it with a cast.

    .. code-block:: cpp

       float f{1};  // the int 1 is converted to float

    The compiler looks for a valid conversion from the type it has to the
    type it needs. If it finds one it produces a **new value** of the
    target type; if it does not, compilation fails.

.. note::

   A conversion **does not modify** the original object.
   ``int i{2}; double d{i};`` leaves ``i`` an ``int`` holding ``2``.


Implicit Type Conversion
-------------------------

The compiler converts automatically in five common situations.

.. list-table::
   :widths: 42 58
   :header-rows: 1
   :class: compact-table

   * - Situation
     - Example
   * - Initializing or assigning across types
     - ``double d{1};`` and ``d = 3;``
   * - Returning a value of a different type
     - ``double f() { return 1; }``
   * - Operands of a binary operator differ
     - ``double d{1 / 3.0};``
   * - A non-boolean value used as a condition
     - ``if (3) { }``
   * - An argument's type differs from the parameter's
     - ``void f(double x); f(2);``


typeid and c++filt
^^^^^^^^^^^^^^^^^^

``typeid`` from ``<typeinfo>`` lets you ask what type an expression has,
which is the quickest way to check whether a conversion happened.

.. code-block:: cpp

   #include <iostream>
   #include <typeinfo>

   int main() {
       double num1{1.5};
       int num2 = num1;  // 1.5 converted to 1

       std::cout << "Value of num1: " << num1 << '\n';                 // 1.5
       std::cout << "Type of num1:  " << typeid(num1).name() << '\n';  // d
       std::cout << "Value of num2: " << num2 << '\n';                 // 1
   }

.. warning::

   ``typeid(...).name()`` does **not** return ``"double"``. It returns
   the compiler's internal **mangled** name, which with GCC is a short
   code. For the fundamental types the codes are worth learning, because
   they are all you will see in this lecture:

   .. list-table::
      :widths: 20 20 20 20 20
      :header-rows: 1
      :class: compact-table

      * - Code
        - Type
        - Code
        - Type
        -
      * - ``b``
        - ``bool``
        - ``j``
        - ``unsigned int``
        -
      * - ``c``
        - ``char``
        - ``l``
        - ``long``
        -
      * - ``s``
        - ``short``
        - ``m``
        - ``unsigned long``
        -
      * - ``i``
        - ``int``
        - ``f``
        - ``float``
        -
      * - ``x``
        - ``long long``
        - ``d``
        - ``double``
        -

   These codes are **not** portable: they are GCC and Clang's shared
   ABI, and MSVC prints something else entirely.

.. tip::

   Mangling is how the compiler encodes names and types into the unique
   symbols the linker works with, and it is why linker errors are so
   hard to read. The ``c++filt`` tool reverses it:

   .. code-block:: bash

      echo '_ZSt4cout' | c++filt          # std::cout
      ./main | c++filt -t                 # demangle a program's output

   You will want it from Lecture 6 onward, when template types make
   these names genuinely unreadable. For the single-letter codes above,
   just use the table.


Standard Conversions
---------------------

The standard defines how fundamental types convert into one another.
These rules are the **standard conversions**, in four categories.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: Numeric promotions
        :class-card: sd-border-secondary

        A smaller type widened to a larger one in the same family.
        Always value-preserving.

    .. grid-item-card:: Numeric conversions
        :class-card: sd-border-secondary

        Everything else between arithmetic types. May lose data.

    .. grid-item-card:: Arithmetic conversions
        :class-card: sd-border-secondary

        Applied when a binary operator gets operands of different types.

    .. grid-item-card:: Other conversions
        :class-card: sd-border-secondary

        Pointer and reference conversions, covered in later lectures.


Numeric Promotion
^^^^^^^^^^^^^^^^^

A **numeric promotion** widens a smaller type to a larger type **within
the same family**: integral to integral, floating-point to
floating-point. It never loses information.

.. list-table::
   :widths: 34 34 32
   :header-rows: 1
   :class: compact-table

   * - Kind
     - From
     - To
   * - Floating-point promotion
     - ``float``
     - ``double``
   * - Integral promotion
     - ``char``
     - ``int``
   * - Integral promotion
     - ``short``
     - ``int``
   * - Integral promotion
     - ``bool``
     - ``int`` (``false`` to 0, ``true`` to 1)

.. code-block:: cpp

   double num1{5.0};                // no promotion needed
   double num2{4.0f};               // float -> double

   short s{1};
   int a = s;                       // short -> int
   int b = 'a';                     // char  -> int
   int c = true;                    // bool  -> int

   std::cout << a << '\n';          // 1
   std::cout << b << '\n';          // 97
   std::cout << c << '\n';          // 1
   std::cout << sizeof(s) << '\n';  // 2


.. _l2-numeric-conversion:

Numeric Conversion
^^^^^^^^^^^^^^^^^^

A **numeric conversion** is any other conversion between arithmetic
types. Unlike a promotion, it **may** lose data or precision.

.. code-block:: cpp

   // Integral conversions
   short s = 1;            // int    -> short
   long l = 1;             // int    -> long
   char c = s;             // short  -> char
   bool b = 3;             // int    -> bool

   // Floating-point conversions
   float f = 3.0;          // double -> float
   long double ld = 3.0;   // double -> long double  (not a promotion)

   // Floating-integral conversions
   int i = 5.8;            // double -> int, the .8 is discarded
   int j = 3.453f;         // float  -> int

   // Integral-floating conversions
   double d = 5;           // int    -> double       (not a promotion)

.. note::

   ``double`` to ``long double`` and ``int`` to ``double`` are
   **conversions, not promotions**, even though nothing is lost. The
   promotion categories are fixed lists; anything outside them is a
   conversion.

.. card::
    :class-card: sd-border-warning sd-shadow-sm

    **Narrowing conversions, and why braces reject them**

    A **narrowing conversion** is one where precision may be lost.
    Consider:

    .. code-block:: cpp
       :linenos:

       int a;       // uninitialized: garbage
       int b = 3.2; // b == 3, implicit double -> int
       int c(1.3);  // c == 1, implicit double -> int
       int d{3.5};  // Error: narrowing conversion of '3.5e+0'
                    //        from 'double' to 'int'

    Lines 2, 3 and 4 all request the same conversion, but **only the
    braced form is rejected**. That is deliberate: when uniform
    initialization was introduced in C++11, implicit narrowing was
    considered a defect worth catching, and braces were the place to
    catch it. If the compiler rejects a line like this, the first
    question to ask is whether you meant to narrow at all.

    If you did mean it, say so with ``static_cast``:

    .. code-block:: cpp

       int b = static_cast<int>(3.2);
       int c(static_cast<int>(1.3));
       int d{static_cast<int>(3.5)};   // OK: explicit

    ``static_cast`` **truncates**, it does not round:
    ``static_cast<int>(3.7)`` is ``3``.

.. note::

   A numeric conversion does not always lose data; it is the
   *possibility* that makes it narrowing.

   .. code-block:: cpp

      int x = 3.5;             // 0.5 dropped: data lost
      std::cout << x << '\n';  // 3
      int y = 3.0;             // nothing lost
      std::cout << y << '\n';  // 3


.. _l2-arithmetic-conversion:

Arithmetic Conversions
^^^^^^^^^^^^^^^^^^^^^^

Some operators require both operands to have the **same type**:

- binary arithmetic: ``+``, ``-``, ``*``, ``/``, ``%``
- relational: ``<``, ``>``, ``<=``, ``>=``, ``==``, ``!=``
- binary bitwise: ``&``, ``^``, ``|``
- the conditional operator ``?:`` (its second and third operands)

When the operands differ, the compiler applies the **usual arithmetic
conversions** to bring them to a common type. Work through it in three
steps.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **The procedure**

    1. **Floating point wins.** If either operand is a floating-point
       type, both become the largest floating-point type present, and
       you are done.
    2. **Otherwise, promote.** Apply integral promotion to both
       operands. This turns ``bool``, ``char`` and ``short`` into
       ``int``, so after this step every operand is at least ``int``.
    3. **Then rank.** If the two still differ, the lower-ranked operand
       is converted to the higher-ranked type.

The ranking used in step 3:

.. list-table::
   :widths: 15 85
   :header-rows: 1
   :class: compact-table

   * - Rank
     - Type
   * - 1 (highest)
     - ``long double``
   * - 2
     - ``double``
   * - 3
     - ``float``
   * - 4
     - ``unsigned long long``
   * - 5
     - ``long long``
   * - 6
     - ``unsigned long``
   * - 7
     - ``long``
   * - 8
     - ``unsigned int``
   * - 9 (lowest)
     - ``int``

.. warning::

   **That ranking is a simplification.** It gives the right answer for
   every case in this lecture and for essentially all code you will
   write, but it is not the rule in the standard. The real rule for two
   integer types of the same rank, one signed and one unsigned, depends
   on whether the signed type can represent every value of the unsigned
   one, which in turn depends on how wide those types are **on your
   platform**. So ``long long + unsigned long`` gives ``unsigned long
   long`` on 64-bit Linux, which the flat list above does not predict.

   Do not memorize the corner cases. Take the lesson instead: **do not
   mix signed and unsigned in one expression.** When you must, use the
   ``std::cmp_*`` functions or fix the types. The exact wording is in
   `cppreference: usual arithmetic conversions <https://en.cppreference.com/w/cpp/language/usual_arithmetic_conversions>`_.

.. dropdown:: Steps 1 and 3 in action
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       int i{42};
       double d{3.14};
       std::cout << typeid(i + d).name() << '\n';   // d  -> double
       std::cout << i + d << '\n';                  // 45.14

       unsigned int ui{100};
       long l{5000};
       std::cout << typeid(ui + l).name() << '\n';  // l  -> long
       std::cout << ui + l << '\n';                 // 5100

       unsigned short us{10};
       unsigned long ul{700000};
       std::cout << typeid(us + ul).name() << '\n'; // m  -> unsigned long
       std::cout << us + ul << '\n';                // 700010

    Remember that ``.name()`` prints the **mangled** name, so you get
    ``d``, ``l`` and ``m``, not the words after the arrows.

.. dropdown:: Step 2 in action
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       short s1{100};
       char c{50};
       std::cout << typeid(s1 + c).name() << '\n';  // i  -> int
       std::cout << s1 + c << '\n';                 // 150

       unsigned char uc{200};
       bool b1{true};
       std::cout << typeid(uc + b1).name() << '\n'; // i  -> int
       std::cout << uc + b1 << '\n';                // 201

    Neither ``short`` nor ``char`` survives step 2: both are promoted to
    ``int``, they now match, and the result is an ``int``. Note that
    this happens even though *both* operands were small types, which is
    why ``short + short`` also yields an ``int``.

.. warning::

   **Integer division is the classic trap.** With ``int a{3}; int b{2};``
   the expression ``a / b`` is ``int / int``, so no conversion happens
   and the result is ``1``, not ``1.5``. To get ``1.5``, force one
   operand to a floating-point type:

   .. code-block:: cpp

      std::cout << static_cast<double>(a) / b << '\n';  // 1.5


Constants
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A **constant** is an expression with a fixed value. Programs are full
    of quantities that must never change: 7 days in a week,
    :math:`\pi`, the speed of light, the number of joints on a robot arm.

    In C++ a constant is **initialized when it is created**, and cannot
    be assigned to afterwards.

C++ has three kinds:

.. grid:: 1 3 3 3
    :gutter: 3

    .. grid-item-card:: Literal constants
        :class-card: sd-border-secondary

        Fixed values written directly in the source.

    .. grid-item-card:: Constant variables
        :class-card: sd-border-secondary

        Named variables declared ``const``.

    .. grid-item-card:: Symbolic constants
        :class-card: sd-border-secondary

        Preprocessor macros. **Avoid these.**


Literal Constants
-----------------

A **literal** is a notation for a fixed value written into the source
code. Numeric literals can carry an
`integer suffix <https://en.cppreference.com/w/cpp/language/integer_literal>`_
or a
`floating-point suffix <https://en.cppreference.com/w/cpp/language/floating_literal>`_.

.. code-block:: cpp

   // Integral literals
   int dec{12};          // decimal
   int hex{0xFF};        // hexadecimal
   int bin{0b1010};      // binary
   long big{12L};        // long suffix

   // Floating-point literals
   double e{2.71};
   float pi{3.14159f};
   double exp{1.23e4};   // 12300.0

   // Character and string literals
   char a{'a'};
   char newline{'\n'};
   std::string hello{"Hello"};

   // Boolean literals
   bool yes{true};
   bool no{false};


Constant Variables
------------------

A variable whose value cannot change is a **constant variable**, declared
with ``const``.

.. code-block:: cpp

   const double radius{3.5};   // "west const": preferred in this course
   double const radius2{3.5};  // "east const": legal, not our style

.. warning::

   Two rules the compiler enforces:

   .. code-block:: cpp

      const double pi;            // Error: uninitialized const 'pi'

      const double e{2.71828};
      e = 2.7;                    // Error: assignment of read-only variable 'e'

   A ``const`` variable **must** be initialized where it is declared, and
   can **never** be assigned to afterwards.

.. tip::

   **Do not type out mathematical constants.** C++20 provides them, to
   the full precision of the type, in the ``<numbers>`` header:

   .. code-block:: cpp

      #include <numbers>

      constexpr double r{3.5};
      constexpr double area{std::numbers::pi * r * r};

   ``std::numbers`` also has ``e``, ``sqrt2``, ``ln2``, ``phi`` and
   others. A hand-typed ``3.141598`` is a digit wrong in the sixth
   decimal place, and that is exactly the kind of error nobody finds by
   reading. Let the library supply the digits.

   Note that ``r`` here is ``constexpr``, not ``const``. A ``const
   double`` cannot be used in a constant expression, so
   ``const double r{3.5};`` above a ``constexpr`` calculation is an
   error. See :ref:`l2-const-in-constant-expressions`.

.. seealso::

   C++ Core Guidelines:
   `NL.26: Use conventional const notation <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl26-use-conventional-const-notation>`_.


Symbolic Constants
------------------

**Symbolic constants** are made with preprocessor **macros**. The
preprocessor performs a blind text substitution before the compiler ever
sees the code.

.. code-block:: cpp

   #include <iostream>
   #define PI 3.14159  // symbolic constant

   int main() {
       std::cout << "pi: " << PI << '\n';  // PI is textually replaced
   }

.. warning::

   **In modern C++, use** ``const`` **or** ``constexpr`` **instead of
   macros.**

   - **No types on the macro itself.** A macro has no parameter types
     and no return type, so nothing checks what you pass it, and the
     text it expands to may not do what the call site looks like it
     does. The classic case is an argument evaluated **twice**:

     .. code-block:: cpp

        #define SQUARE(x) ((x) * (x))

        int i{5};
        int bad{SQUARE(i++)};  // expands to ((i++) * (i++))
                               // i is incremented twice; the result is
                               // not 25, and the expression is UB

     A ``constexpr`` function takes a typed parameter, evaluates its
     argument exactly once, and cannot do this.

   - **No scope.** A macro is live from its ``#define`` to the end of the
     translation unit, ignoring namespaces, functions and blocks.
   - **Hard to debug.** The macro name does not survive into the compiled
     program, so the debugger shows you ``3.14159 * 10 * 10``, never
     ``PI * 10 * 10``.


Constant Expressions
--------------------

A **constant expression** is one the compiler can evaluate **at compile
time**, because every value in it is known then. The compiler replaces
the expression with its result.

.. code-block:: cpp

   int main() {
       std::cout << 1 + 2 << '\n';
   }

The output is always ``3``, and ``1 + 2`` is never computed at runtime.
The compiler emits the equivalent of:

.. code-block:: cpp

   int main() {
       std::cout << 3 << '\n';
   }

.. tip::

   Paste both versions into `Compiler Explorer <https://godbolt.org/>`_
   and compare the generated assembly. This is the fastest way to see
   what the compiler actually does with your code.

.. note::

   Compile-time evaluation makes **compilation** slower, because the
   compiler is doing the work. It happens once, instead of on every run,
   so the resulting executable is faster and often smaller.


.. _l2-const-in-constant-expressions:

Compile-time and Runtime Constants
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **compile-time constant** is a constant whose value is known while
compiling. A ``const`` variable **may or may not** be one; it depends
entirely on its initializer.

.. code-block:: cpp

   const int a{1};              // compile-time constant
   const int b{2};              // compile-time constant
   std::cout << a + b << '\n';  // compile-time expression

.. code-block:: cpp

   std::cout << "Enter an integer: ";
   int input{};
   std::cin >> input;

   const int a{1};              // compile-time constant
   const int b{input};          // runtime constant: legal, but not compile-time
   std::cout << a + b << '\n';  // runtime expression

Both are valid ``const``. Only the first can be folded away by the
compiler, and nothing in the code says which one you got.

.. warning::

   **A** ``const`` **is not always usable in a constant expression, and
   the type decides.** A ``const`` variable of **integral** type
   initialized with a constant expression may be used in one. A
   ``const`` variable of any other type, ``double`` included, may not:

   .. code-block:: cpp

      const int n{10};
      constexpr int twice_n{2 * n};      // OK: n is const and integral

      const double r{3.5};
      constexpr double area{r * r};      // Error: the value of 'r' is not
                                         //        usable in a constant expression

      constexpr double r2{3.5};
      constexpr double area2{r2 * r2};   // OK

   This asymmetry surprises everyone the first time. It is one more
   reason to write ``constexpr`` rather than ``const`` whenever the
   value really is known at compile time: ``constexpr`` works for every
   type, and it fails loudly instead of silently not qualifying.


constexpr
^^^^^^^^^^

``constexpr`` removes that ambiguity: it states that the value **must**
be computable at compile time, and the compiler enforces it.

.. code-block:: cpp

   constexpr int a{1};      // OK: compile-time constant
   constexpr int b{2};      // OK: compile-time constant

   std::cout << "Enter an integer: ";
   int input{};
   std::cin >> input;
   constexpr int c{input};  // Error: the value of 'input' is not usable
                            //        in a constant expression

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Why prefer** ``constexpr``

    - **No runtime cost.** The value is computed during compilation, so
      the program never spends a cycle on it. A ``const`` initialized at
      runtime still carries that cost.
    - **Smaller footprint.** The compiler can substitute the value
      directly rather than storing a variable.
    - **Better inlining.** ``constexpr`` functions inline more
      aggressively, removing call overhead.
    - **It documents intent.** ``constexpr`` says "this is knowable now",
      and the compiler checks the claim. ``const`` only says "do not
      reassign this".

.. seealso::

   C++ Core Guidelines:
   `Con.5: Use constexpr for values that can be computed at compile time <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con5-use-constexpr-for-values-that-can-be-computed-at-compile-time>`_.
   Full reference:
   `cppreference: constexpr <https://en.cppreference.com/w/cpp/language/constexpr>`_.


Type Deduction
====================================================

**Type deduction** lets the compiler work out a variable's type from its
initializer. You write ``auto`` where the type would go.

.. code-block:: cpp

   auto a{3.0};    // 3.0 is a double literal    -> a is double
   auto b{1 + 2};  // 1 + 2 evaluates to an int  -> b is int
   auto c{b};      // b is an int                -> c is int

.. warning::

   ``auto`` needs something to deduce **from**. Both of these fail:

   .. code-block:: cpp

      auto a;    // Error: declaration of 'auto a' has no initializer
      auto b{};  // Error: unable to deduce 'auto' from '{}'

.. card::
    :class-card: sd-border-warning sd-shadow-sm

    ``auto`` **drops** ``const``

    Type deduction discards the ``const`` qualifier by default:

    .. code-block:: cpp

       const int a{5};  // a is const
       auto b{a};       // b is int, const has been dropped
       b = 1;           // OK

    To keep it, say so explicitly:

    .. code-block:: cpp

       constexpr int a{5};   // a is a compile-time constant int
       const auto b{a};      // b is const int
       constexpr auto c{a};  // c is a compile-time constant int
       c = 1;                // Error: assignment of read-only variable 'c'


Compound Statements
====================================================

A **compound statement**, also called a **block**, is a group of zero or
more statements between braces.

.. code-block:: cpp

   int main() {        // start outer block
       int a{};
       {               // start nested block 1
           int b{};
           {           // start nested block 2
               int c{};
           }           // end nested block 2
       }               // end nested block 1
   }                   // end outer block

.. note::

   - A block can appear anywhere a single statement can.
   - There is **no semicolon** after the closing brace of a block.
   - Keep nesting to **three levels or fewer**. If a function needs more,
     that is a signal to split it into smaller functions.


Scopes
====================================================

A variable's **scope** is the region of source code in which its name can
be used. An identifier that can be used is **in scope**; one that cannot
is **out of scope**.

.. important::

   Scope is a **compile-time** property. Using a name that is out of
   scope is a compile error, not a runtime failure. This is a case where
   the compiler catches the mistake for you, which is not true of the
   lifetime errors covered in Lecture 3.


Local Scope
-----------

Function parameters and variables defined inside a function body are
**local variables**, and their scope is delimited by the enclosing
braces. They are created where they are defined and destroyed in reverse
order at the closing brace.

.. dropdown:: Local scope example
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int main() {
           int a{1};
           {
               int b{2};
               std::cout << a << '\n';  // 1: a is still in scope
               std::cout << b << '\n';  // 2
           }  // b goes out of scope here

           std::cout << b << '\n';      // Error: 'b' was not declared in this scope
           int c{3};
       }  // a and c go out of scope here


Out of Scope
^^^^^^^^^^^^

When a variable goes out of scope its **lifetime ends**: the name can no
longer be used, and the storage is released for reuse. What the storage
still *contains* is a different question, and it is the reason
uninitialized variables hold garbage.

.. figure:: /_static/images/l2/outofscope.png
   :align: center
   :alt: Three stack diagrams: unknown values before the declaration, x holding 1 after it, and the same bits still present after the closing brace.

   The bit pattern left by ``x`` survives the closing brace; only the
   name is gone.


Global Scope
------------

Variables declared outside every function have **file scope**, informally
called **global scope**. They are visible from their point of declaration
to the end of the file. By convention they go at the top, below the
``#include`` directives and above any code.

.. dropdown:: Global scope example
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       int global_var{1};

       void my_function() {
           global_var++;
       }

       int main() {
           std::cout << global_var << '\n';  // 1
           global_var++;                     // now 2
           my_function();                    // now 3
           std::cout << global_var << '\n';  // 3
       }

.. warning::

   **Avoid non-const global variables.** Any function can read and modify
   them, so a wrong value gives you no clue about which line caused it,
   and the whole program has to be understood before any part of it can
   be trusted. If you genuinely need a global, make it read-only with
   ``const`` or ``constexpr``.

.. seealso::

   C++ Core Guidelines:
   `R.6: Avoid non-const global variables <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r6-avoid-non-const-global-variables>`_.


Where Globals Live
^^^^^^^^^^^^^^^^^^

Global variables do not live on the stack. **Initialized** globals go in
the **data** segment; **uninitialized** globals go in the **BSS**
segment, where the loader zeroes them.

.. code-block:: cpp

   #include <iostream>

   int global_x;      // uninitialized -> BSS
   int global_y{1};   // initialized   -> data

   int main() {
       std::cout << &global_x << '\n';
       std::cout << &global_y << '\n';
   }

.. figure:: /_static/images/l2/globalvars.png
   :align: center
   :alt: A memory bank with global_y labeled in the data segment and global_x labeled in the BSS segment.

   ``global_y`` in the data segment, ``global_x`` in BSS.

.. note::

   This is the one case where an uninitialized variable is **not**
   garbage: globals in BSS are zero-initialized by the loader. The rule
   still holds for local variables, which are not.


Naming Collisions and Namespaces
====================================================

Naming Collisions
-----------------

C++ requires every identifier to be unambiguous. A **naming collision**
occurs when two identifiers with the same name are declared in the same
scope.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int x{1};
       int x{2};  // Error: redeclaration of 'int x'
       std::cout << x << '\n';
   }

In a single function this is easy to see. Across a large project, or when
your code meets a third-party library, it is not, which is what
namespaces are for.


Namespaces
----------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A **namespace** is a declarative region that gives a scope, called
    **namespace scope**, to the names declared inside it. A name declared
    in a namespace will never be confused with an identical name declared
    elsewhere. The entire C++ standard library lives in the namespace
    ``std``, which is why you have been writing ``std::cout``.

.. code-block:: cpp

   namespace MyNamespace {
       // everything declared here belongs to MyNamespace
   }

There are three ways to reach a name inside a namespace.


Explicit Qualification
^^^^^^^^^^^^^^^^^^^^^^

Name the namespace with the **scope resolution operator** ``::``. This is
the form this course uses.

.. code-block:: cpp

   #include <iostream>

   namespace MyNamespace {
   int x{3};
   int y{4};
   }  // namespace MyNamespace

   int main() {
       std::cout << MyNamespace::x << '\n';  // 3
       std::cout << MyNamespace::y << '\n';  // 4
   }


The ``using namespace`` Directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A ``using namespace`` directive makes **every** name in a namespace
available unqualified.

.. code-block:: cpp

   #include <iostream>

   namespace MyNamespace {
   int x{3};
   int y{4};
   }  // namespace MyNamespace

   using namespace MyNamespace;

   int main() {
       std::cout << x << '\n';  // no MyNamespace:: needed
       std::cout << y << '\n';
   }


The ``using`` Declaration
^^^^^^^^^^^^^^^^^^^^^^^^^

A ``using`` **declaration** imports a **single** name, which is far more
targeted.

.. code-block:: cpp

   #include <iostream>

   namespace MyNamespace {
   int x{3};
   int y{4};
   }  // namespace MyNamespace

   using MyNamespace::x;

   int main() {
       std::cout << x << '\n';  // OK: x was imported
       std::cout << y << '\n';  // Error: 'y' was not declared in this scope
   }


Why to Avoid ``using namespace``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   ``using namespace`` pulls in names you never asked for, and two
   directives can pull in the same name.

   .. code-block:: cpp

      #include <iostream>

      namespace MyNamespace {
      int cout{1};
      }  // namespace MyNamespace

      using namespace std;
      using namespace MyNamespace;

      int main() {
          cout << cout << '\n';  // Error: reference to 'cout' is ambiguous
      }

   Never put a ``using namespace`` directive in a **header**: every file
   that includes it inherits the problem.

Readability suffers too. In the code below, nothing tells you which
namespace each name came from:

.. code-block:: cpp

   #include <array>
   #include <iostream>
   #include <vector>
   #include "outside_file.h"  // defines MyFirstNamespace, MySecondNamespace

   using namespace std;
   using namespace MyFirstNamespace;
   using namespace MySecondNamespace;

   int main() {
       array<array<int, 2>, 4> arr{{{1, 2}, {1, 2}}};
       vector<int> vect{1, 2, 3, 4};
       cout << x << '\n';   // from where?
       cout << y << '\n';   // from where?
       cout << z << '\n';   // from where?
   }

.. tip::

   **Best practice for this course:** qualify explicitly
   (``std::cout``), or import individual names with a ``using``
   declaration inside the narrowest scope that needs them. Write
   ``std::`` in full; it is five characters and it tells the reader
   exactly where the name comes from.


Aliases
====================================================

A **type alias** gives an existing type a second name. The ``using``
keyword creates one.

.. code-block:: cpp

   using Integer = int;
   using Float = float;
   using uint = unsigned int;

.. dropdown:: Aliases in use
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <iostream>

       using Integer = int;
       using Float = float;
       using uint = unsigned int;

       int main() {
           Integer a{10};
           Float b{20.5f};
           uint age{30};

           std::cout << "Integer: " << a << '\n';
           std::cout << "Float: " << b << '\n';
           std::cout << "Age: " << age << '\n';
       }

.. note::

   An alias creates **no new type**: ``Integer`` and ``int`` are the same
   type, and the compiler treats them interchangeably. What you gain is
   readability and a single place to change. Aliases pay for themselves
   once the underlying types get long, which happens quickly with the
   standard library:

   .. code-block:: cpp

      using JointAngles = std::vector<std::array<double, 6>>;


Scoped Enumerations
====================================================

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **What is** ``enum class`` **?**

    An ``enum class``, or **scoped enumeration**, is a type-safe
    enumeration introduced in C++11. Unlike a plain ``enum``, its
    enumerators are **scoped to the enum name** and do **not** implicitly
    convert to integers.


Syntax
------

.. code-block:: cpp

   enum class Color {
       red,
       green,
       blue
   };

   Color my_color{Color::red};

Enumerators are reached through the scope resolution operator, exactly
like namespace members: ``Color::red``.


Why ``enum class`` over ``enum``
---------------------------------

.. grid:: 1 3 3 3
    :gutter: 3

    .. grid-item-card:: Type safety
        :class-card: sd-border-secondary

        Enumerators do **not** implicitly convert to ``int``. If you want
        the integer, ask for it with ``static_cast``.

    .. grid-item-card:: Scoped names
        :class-card: sd-border-secondary

        Enumerator names live inside the enum, so ``Color::red`` and
        ``TrafficLight::red`` coexist happily.

    .. grid-item-card:: Chosen underlying type
        :class-card: sd-border-secondary

        The underlying integer type can be specified. The default is
        ``int``.

.. warning::

   **Avoid unscoped** ``enum`` **in modern C++.** Its enumerators leak
   into the enclosing scope and convert silently to ``int``:

   .. code-block:: cpp

      // Problem 1: name collisions
      enum Color { red, green, blue };
      enum TrafficLight { red, yellow, green };  // Error: 'red' and 'green' redeclared

      // Problem 2: silent conversion to int
      enum Direction { up, down };
      int value{up + 42};  // compiles without a warning, almost certainly a bug

   ``enum class`` prevents both.


Underlying Type
----------------

The default underlying type is ``int``. Name a different integral type
after a colon:

.. code-block:: cpp

   #include <cstdint>

   enum class Status : std::uint8_t {
       active,
       inactive
   };

This matters when memory is tight, as on an embedded target, or when the
value has to match a hardware register or a message field of a specific
width.


C++20: ``using enum``
----------------------

Qualifying every enumerator is what makes ``enum class`` safe, but it
gets repetitive in a ``switch`` where every label names the same type.
C++20 lets you drop the qualification **inside a limited scope**:

.. code-block:: cpp

   switch (state) {
       using enum RobotState;      // C++20: only inside this block
       case idle:     std::cout << "Robot is idle\n";     break;
       case moving:   std::cout << "Robot is moving\n";   break;
       case charging: std::cout << "Robot is charging\n"; break;
       case error:    std::cout << "Robot error!\n";      break;
   }

.. warning::

   Put ``using enum`` in the **narrowest** scope that needs it, exactly
   as with a ``using`` declaration for a namespace. At file scope it
   reintroduces the leaked names that ``enum class`` existed to prevent.


Use Cases in Robotics
----------------------

Scoped enumerations fit any fixed set of named alternatives:

.. grid:: 1 3 3 3
    :gutter: 3

    .. grid-item-card:: Robot states
        :class-card: sd-border-secondary

        ``idle``, ``moving``, ``charging``, ``error``

    .. grid-item-card:: Sensor types
        :class-card: sd-border-secondary

        ``lidar``, ``camera``, ``imu``

    .. grid-item-card:: Command types
        :class-card: sd-border-secondary

        ``forward``, ``backward``, ``left``, ``right``, ``stop``

.. dropdown:: A robot state machine
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp

       #include <cstdint>
       #include <iostream>

       enum class RobotState : std::uint8_t {
           idle,
           moving,
           charging,
           error
       };

       int main() {
           RobotState state{RobotState::idle};

           switch (state) {
               case RobotState::idle:
                   std::cout << "Robot is idle" << '\n';
                   break;
               case RobotState::moving:
                   std::cout << "Robot is moving" << '\n';
                   break;
               case RobotState::charging:
                   std::cout << "Robot is charging" << '\n';
                   break;
               case RobotState::error:
                   std::cout << "Robot error!" << '\n';
                   break;
           }
       }

    Leaving out the ``default`` label is deliberate: add a new enumerator
    later and ``-Wswitch``, part of ``-Wall``, warns you about every
    ``switch`` that has not been updated.

.. dropdown:: Getting the integer value out
    :class-container: sd-border-secondary

    .. code-block:: cpp

       #include <iostream>

       enum class SensorType {
           lidar,
           camera,
           imu
       };

       int main() {
           SensorType sensor{SensorType::camera};

           // static_cast is required: there is no implicit conversion
           int sensor_id{static_cast<int>(sensor)};
           std::cout << "Sensor ID: " << sensor_id << '\n';  // 1
       }

    Enumerators are numbered from 0 in declaration order unless you give
    them explicit values, so ``SensorType::camera`` is ``1``.
