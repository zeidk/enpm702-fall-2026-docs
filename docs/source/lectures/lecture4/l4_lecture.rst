.. _l4-lecture:

====================================================
Lecture
====================================================

:doc:`Lecture 3 </lectures/lecture3/l3_lecture>` ended with ``new`` and
``delete`` and the four ways they go wrong. This lecture is about never
writing them again. The standard library ships containers that own their
storage, grow on demand and free everything on the closing brace. You
choose one, and the language does the bookkeeping.

The page follows the slides section by section. Each top-level heading is
a section of the deck, each second-level heading is a subsection, and
each third-level heading is one slide. Every number on this page was
measured on the course machine, GCC 13 with libstdc++ on x86-64 Linux,
unless the text says otherwise.

The examples come from a small robot: joint angles of an arm, a lidar
scan, an occupancy grid, sensor names and their sampling periods. Names
carry their unit as a suffix, as in Lecture 3: ``ranges_m`` is metres,
``joint_deg`` is degrees.

.. seealso::

   Assumed from earlier lectures and not repeated here: the segments of
   a process (``.rodata``, stack, heap) and undefined behaviour from
   :doc:`Lecture 2 </lectures/lecture2/l2_lecture>`; pointers, ``p + 1``
   stepping by ``sizeof(*p)``, dangling pointers, references and
   const-correctness from :doc:`Lecture 3 </lectures/lecture3/l3_lecture>`.


The Type of Every Size
======================

.. admonition:: Definition: ``std::size_t``
   :class: tip

   The one type every size in the standard library uses, from
   ``<cstddef>``. ``sizeof`` returns one, and so does ``size()`` on every
   container in this lecture. It is **unsigned**, so it has no negative
   values at all.

.. code-block:: cpp

   std::size_t n{3};
   n - 5;  // not -2, but 18446744073709551614

   for (std::size_t i{n - 1}; i >= 0; --i) { }   // never ends

- Subtracting past zero does not go negative. It **wraps** to the top of
  the range.
- ``i >= 0`` is always true for an unsigned ``i``, so that loop never
  stops. Count upwards, or take a signed count with ``std::ssize``
  (C++20).
- Mixing it with ``int`` in a comparison is the other trap. ``-Wall``
  reports it as ``comparison of integer expressions of different
  signedness``.

.. note::

   C++20, [support.types.layout], section 17.2.4, paragraph 3: *the type*
   ``size_t`` *is an implementation-defined unsigned integer type that is
   large enough to contain the size in bytes of any object*. Its width is
   not fixed by the standard: 8 bytes here, 4 on a 32-bit target.


Time Complexity
===============

Every container in this lecture offers the same operations, at different
costs: adding to the end of a vector is cheap, adding to its middle is
not.

.. admonition:: Definition: Time complexity
   :class: tip

   How the number of steps an operation takes **grows** with the size of
   its input, *n*. It is written in **Big-O notation**: O(1), O(log n),
   O(n), O(n log n), O(n²).

- Not seconds: it drops the machine, the compiler and constant factors
  and keeps the **shape of the growth**.
- Why know it: a loop that is fine on 10 readings can be unusable on a
  4000 by 4000 map. Complexity says so before you run it.

**How to read it**

- Call the input size *n*: readings in a scan, robots in a fleet.
- Count the steps for the **worst case**, unless the cost says "average"
  or "amortized".
- Keep the fastest-growing part and drop the rest: 3n + 5 is O(n), and
  ½n² − ½n is O(n²).

.. note::

   For the record: f(n) = O(g(n)) means a constant *c* and a size *n₀*
   exist with f(n) ≤ c · g(n) for all n ≥ n₀. The *O* is for *order*. The
   notation comes from number theory (Bachmann 1894, Landau 1909) and
   entered the analysis of algorithms through Knuth (1976).

The Costs, One at a Time
------------------------

Five costs cover every operation in this lecture, each guaranteed by the
standard.

.. list-table::
   :header-rows: 1
   :widths: 14 40 16 30

   * - Cost
     - How to read the curve
     - At n = 1000
     - Today
   * - O(1)
     - a flat line: more elements, the same cost
     - 1
     - ``v[i]``, ``push_back``
   * - O(log n)
     - rises at first, then almost flat: doubling *n* adds one step
     - about 10
     - ``map`` lookup
   * - O(n)
     - a straight diagonal: double *n*, double the work
     - 1000
     - ``find``, a middle ``insert``
   * - O(n log n)
     - a little steeper than the diagonal: double *n*, a bit more than double the work
     - about 10,000
     - ``std::sort``
   * - O(n²)
     - bends upward: double *n*, four times the work
     - 1,000,000
     - a loop calling ``strlen``
   * - O(2ⁿ)
     - shoots straight up: one more element doubles the work
     - a 302-digit number
     - nothing today

Example 1: One Loop
-------------------

Count how many times ``stmt`` runs, as a function of ``n``:

.. code-block:: cpp

   int n{1000};
   for (int i{0}; i < n; ++i)
     stmt;

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - pass
     - ``i``
     - times ``stmt`` has run
   * - 1
     - 0
     - 1
   * - 2
     - 1
     - 2
   * - 3
     - 2
     - 3
   * - ...
     - ...
     - ...
   * - n
     - n − 1
     - n

- The body runs once per pass, and there are *n* passes: ``i`` takes
  every value from 0 to n − 1.
- The count is exactly *n*. Nothing to add up, nothing to drop: O(n).
- Checked: n = 1000 runs ``stmt`` 1,000 times, and doubling *n* to 2000
  gives 2,000, twice as many. A ratio of 2 is the O(n) signature.

Example 2: Two Nested Loops
---------------------------

The same count with a second loop inside the first:

.. code-block:: cpp

   int n{1000};
   for (int i{0}; i < n; ++i)
     for (int j{0}; j < i; ++j)
       stmt;

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - ``i``
     - values of ``j``
     - times ``stmt`` runs
   * - 0
     - nothing
     - 0
   * - 1
     - 0
     - 1
   * - 2
     - 0, 1
     - 2
   * - 3
     - 0, 1, 2
     - 3
   * - ...
     - ...
     - ...
   * - n − 1
     - 0 ... n − 2
     - n − 1

- The outer loop runs *n* times. On pass *i* the inner loop runs *i*
  times, so the counts are 0, 1, 2, ..., n − 1.
- Add them up: 0 + 1 + ... + (n − 1) = n(n − 1)/2 = ½n² − ½n.
- Keep the fastest-growing term and drop the constant: O(n²). Checked:
  n = 1000 runs ``stmt`` 499,500 times, about ½n².

The Growth, Not the Count
-------------------------

n² is a million at n = 1000, and the two nested loops of Example 2 ran ``stmt`` 499,500 times. Both are
right, because O(n²) does not name a count. Every row here is O(n²):

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Count
     - at n = 1000
     - at n = 2000
     - ratio
   * - n²
     - 1,000,000
     - 4,000,000
     - 4.0
   * - ½n²
     - 500,000
     - 2,000,000
     - 4.0
   * - ½n² − ½n
     - 499,500
     - 1,999,000
     - 4.0
   * - 3n² + 7
     - 3,000,007
     - 12,000,007
     - 4.0

- The rows differ by constant factors and lower terms. Big-O drops
  exactly those.
- What they share is the **shape**: double *n* and each one grows four
  times. That shape is what O(n²) names.

.. note::

   A single count next to O(n²) invites the wrong reading. The check
   that shows growth is to **double n** and look at the ratio:
   (2n)² = 4n², so 4 for O(n²); 2 for O(n); and log 2n = log n + 1, so
   about 1 for O(log n).

The Standard Library and the STL
================================

.. admonition:: Definition: C++ Standard Library
   :class: tip

   The library the ISO C++ standard requires every compiler to ship:
   strings, streams, containers, algorithms, threads and more. It is
   part of the standard document itself.

.. admonition:: Definition: STL
   :class: tip

   The **Standard Template Library**, older and smaller. Alexander
   Stepanov and Meng Lee wrote it at HP in the early 1990s, and the
   committee adopted it into the draft standard in 1994. Three pieces of
   today's library came from it: containers, iterators and algorithms.

People still say "the STL" for that part of the standard library, though
the standard never uses the name. The figure shows where it sits.

.. figure:: /_static/images/l4/stl_in_stdlib.png
   :width: 90%
   :align: center
   :alt: One large box labelled C++ Standard Library. Inside it, a dashed region labelled from the STL holds Containers, Algorithms, Iterators, Function objects and Allocators, with arrows noting that algorithms see only iterators, never a container. To the right, still inside the library box but outside the STL region, a column lists the rest of the library: strings, streams, smart pointers, numerics, threads, filesystem and ranges.

   The STL inside the Standard Library. Containers, iterators and
   algorithms came from the STL; ``std::string`` took the container
   interface later but was never part of it.

Containers
----------

.. admonition:: Definition: STL container
   :class: tip

   A class template that owns a collection of objects of one type and
   manages their storage.

The Four Categories
^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Category
     - Finds an element by
     - Examples
   * - Sequence
     - **position**
     - ``array``, ``vector``, ``string``, ``list``
   * - Associative
     - **key**, kept sorted
     - ``map``, ``set``
   * - Unordered associative
     - **key**, via a hash
     - ``unordered_map``, ``unordered_set``
   * - Adapters
     - a limited view of another container
     - ``stack``, ``queue``, ``priority_queue``

- Today we cover **1)** ``std::array``, **2)** ``std::vector`` and
  **3)** ``std::string`` from the first row, **4)** ``std::map`` from the
  second, and **5)** ``std::unordered_map`` from the third.
- **Adapters (not covered).** A ``std::stack`` is a ``std::deque`` with
  most of its interface hidden.

One Interface, Every Container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Same meaning on all five: ``array``, ``vector``, ``string``, ``map``,
``unordered_map``.

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Call
     - What it gives you
     - Containers
   * - ``c.size()``
     - how many elements
     - all five
   * - ``c.empty()``
     - ``true`` when there are none
     - all five
   * - ``c[i]``
     - element ``i``, no check
     - all five (maps: by key)
   * - ``c.at(i)``
     - element ``i``, range-checked
     - all five (maps: by key)
   * - ``c.front()``, ``c.back()``
     - the first and the last element
     - array, vector, string
   * - ``c.data()``
     - a pointer to the first element
     - array, vector, string
   * - ``c.begin()``, ``c.end()``
     - both ends, for loops and algorithms
     - all five


Arrays
======

An **array** is a fixed number of objects of one type, stored
contiguously and addressed by index. See
`cppreference: std::array <https://en.cppreference.com/w/cpp/container/array>`_.

Two Kinds of Array
------------------

C++ gives you two ways to write an array.

.. grid:: 2

   .. grid-item-card:: Inherited from C

      .. code-block:: cpp

         int joint_deg[6];

   .. grid-item-card:: ``std::array``, since C++11

      .. code-block:: cpp

         #include <array>
         std::array<int, 6> joint_deg;

- **The bytes are identical.** Both take 24 bytes: six ``int`` values,
  four bytes each, side by side. ``std::array`` adds **no** header, no
  pointer and no size field.
- **The operations are not.** ``.size()``, ``.at(0)``, ``.begin()``,
  ``.fill(0)``: every one compiles for ``std::array``, none for the C
  array, which cannot even be assigned.
- A C array is a **built-in type**, not a class, so there is nowhere to
  hang a member function. ``std::array`` is a class template wrapping
  that same ``int[6]``, which is where those members live.
- It also does not know its own length, which is why text kept in one
  marks its end with a ``'\0'`` byte. The Strings section returns to
  that.

C-style Arrays
--------------

.. admonition:: Definition: C-style array
   :class: tip

   A fixed number of elements of one type, side by side in memory, built
   into the language. It has no member functions, does not carry its own
   length, and turns into a pointer when passed to a function.

Initialization
^^^^^^^^^^^^^^

.. code-block:: cpp

   int a[6];            // 1. garbage: six uninitialized values
   int b[6]{};          // 2. all six are 0
   int c[6]{10, 20, 30};// 3. 10 20 30 0 0 0  -- the rest are zeroed
   int d[]{10, 20, 30}; // 4. size deduced: d has 3 elements

- Case 1 is the **undefined behaviour** from Lecture 2, six times over.
  Reading ``a[0]`` before you write it is a bug, and the compiler does
  not have to warn you.
- Case 3 is a **partial** initializer: it zeroes the rest, so ``c[3]``
  prints ``0``, not garbage.
- Case 4 leaves the size out. The compiler counts the initializers and
  deduces it, so ``d`` has 3 elements.

Contiguity
^^^^^^^^^^

.. admonition:: Definition: Contiguous
   :class: tip

   Stored in one block with no gaps. Element *i* sits exactly
   i × ``sizeof(int)`` bytes after element 0, so its address is
   arithmetic, not a lookup.

.. code-block:: cpp

   int joint_deg[6]{10, 20, 30};

   std::cout << &joint_deg[0] << '\n';// 0x7ffd...a10
   std::cout << &joint_deg[1] << '\n';// 0x7ffd...a14 <- 4 bytes on
   std::cout << &joint_deg[2] << '\n';// 0x7ffd...a18 <- 8 bytes on

- The addresses go up by **4**, which is ``sizeof(int)``. The elements
  really are next to each other, with nothing in between.
- Element *i* is 4i bytes from the start, which is why the first index
  is **0**: the first element is zero bytes in.
- Nothing so far has used a pointer. The next two slides show what
  happens when the array's name becomes one.

Array Decay
^^^^^^^^^^^

.. admonition:: Definition: Array decay
   :class: tip

   In almost every expression, an array name turns into **a pointer to
   its first element**. It happens automatically, with no warning, and
   the length goes with it.

.. code-block:: cpp

   int joint_deg[6]{};
   std::cout << joint_deg << '\n'; // decays:  0x7ffd...a10
   int* p{joint_deg};  // decays: p holds &joint_deg[0]

**Where it does not happen**

- ``sizeof(joint_deg)`` asks about the array and gets 24.
- ``&joint_deg`` gives the address of the whole array, with type
  ``int(*)[6]``.
- Binding to a reference keeps the length in the type:
  ``int (&r)[6]{joint_deg};``, or as a parameter,
  ``void f(int (&a)[6])``.
- ``std::array`` never decays at all. Its length is part of its type, so
  it survives even a by-value pass, with no reference needed.

.. note::

   Decay costs you **the length**. The element count lives in the array's
   *type*; a pointer is only an address.

Pointer Arithmetic on an Array
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lecture 3 showed that ``p + 1`` moves forward by ``sizeof(*p)`` bytes,
but there was nowhere useful to move to. A decayed array is that place:

.. code-block:: cpp

   int joint_deg[6]{10, 20, 30};
   int* p{joint_deg};   // decay: p is &joint_deg[0], 0x7ffd...a10

   p + 1;               // 0x7ffd...a14: one element on, 4 bytes
   *(p + 2);            // 30: step two elements, then read
   joint_deg[2];        // 30: the same two steps, with brackets

- ``p + 1`` adds ``sizeof(*p)``, 4 bytes, so it lands exactly on the
  next element. That only works because the elements are contiguous.
- ``joint_deg[2]`` is **defined** to mean ``*(joint_deg + 2)``: the name
  decays to a pointer, the pointer steps two elements, the star reads
  what is there.
- So the subscript is not a separate feature, and ``joint_deg[0]`` is
  the first element because it is zero steps from the start.

One Block, Read Two Ways
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int joint_deg[6]{10, 20, 30};
   std::cout << &joint_deg[2] << '\n';// 0x7ffd...a18
   std::cout << joint_deg[2] << '\n';// 30

.. figure:: /_static/images/l4/array_memory.png
   :width: 90%
   :align: center
   :alt: Six adjoining cells holding 10, 20, 30, 0, 0, 0, each divided into four byte cells, labelled with index 0 to 5 above and byte offset plus 0 to plus 20 below. The base address 0x7ffd…a10 marks the left edge, the third cell is annotated joint_deg[2] equals star of joint_deg plus 2, and a brace under the run reads 24 bytes: six ints, four bytes each, no gaps.

   The array as bytes. The address of element 2 is the base plus
   2 × 4 bytes, and the value there is 30.

sizeof After Decay
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void report(int joint_deg[6]) {  // the 6 is ignored: this is int*
     std::cout << sizeof(joint_deg); // 8: pointer
     std::cout << sizeof(joint_deg) / sizeof(joint_deg[0]);  // 2
   }

   int main() {
     int joint_deg[6]{};
     std::cout << sizeof(joint_deg); // 24: array
     std::cout << sizeof(joint_deg) / sizeof(joint_deg[0]);  // 6
     report(joint_deg);
   }

- Same name, same array, **two different answers**: 6 in ``main`` and 2
  inside the function. The parameter was never an array to begin with.
- The ``[6]`` in the parameter list is just **decoration**. The compiler
  reads it as ``int*`` and never checks it against anything.

.. warning::

   GCC does warn here, under ``-Wall``. But it only **matches this one
   pattern**. Write the parameter as ``int* joint_deg`` and the warning
   goes away while the bug stays. Rule:
   `Core Guidelines I.13 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ri-array>`_.

Array Length
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 35 20 45

   * - How you ask
     - Works on
     - After decay
   * - ``sizeof(a)/sizeof(a[0])``
     - C array only
     - Compiles, **wrong answer**
   * - ``std::size(a)`` (C++17)
     - both
     - **Does not compile**
   * - ``a.size()``
     - ``std::array``
     - Cannot decay in the first place
   * - ``std::ssize(a)`` (C++20)
     - both
     - As ``std::size``, but signed

- ``std::size`` lives in ``<iterator>`` and refuses a pointer outright:
  ``no matching function for call to 'size(int*&)'``. A compile error
  is much better than a wrong number.
- ``std::ssize`` returns a **signed** type. This matters if you write
  ``i < std::size(a) - 1`` on an empty container, where the unsigned
  subtraction wraps around to a huge number.

.. note::

   ``std::array`` **cannot** decay, so the length never goes missing and
   this question never has a wrong answer. See
   `cppreference: std::size <https://en.cppreference.com/w/cpp/iterator/size>`_.
   Rule:
   `Core Guidelines SL.con.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-arrays>`_.

Arrays Sized at Run Time
^^^^^^^^^^^^^^^^^^^^^^^^

Can the length of an array be a variable?

.. code-block:: cpp

   int n{};
   std::cin >> n;
   int scan[n];      // compiles on GCC. Not C++.

.. admonition:: Definition: Variable length array
   :class: tip

   A C array whose length is a run-time value. It is a C99 feature that
   GCC offers as an extension. Standard C++ has never had it.

- Our build catches it, because ``CMakeLists.txt`` passes
  ``-pedantic-errors``, giving
  ``error: ISO C++ forbids variable length array 'scan'``.
- Drop that flag and the C array compiles again. ``std::array<int, n>``
  still will not: its length is a **template argument**, part of the
  type, and no extension relaxes that.

std::array
----------

.. admonition:: Definition: ``std::array``
   :class: tip

   A class template from ``<array>`` that wraps a C array of the same
   size: the same 24 bytes for six ``int``, no header, plus the members a
   C array lacks. Its length is part of its type, so it never decays.

.. code-block:: cpp

   #include <array>
   std::array<int, 6> joint_deg{10, 20, 30};

   joint_deg.size();   // 6
   joint_deg.at(1);    // 20, range-checked
   joint_deg.fill(0);  // every element becomes 0

- Everything the C array cannot do is a **member**: ``size()``,
  ``at()``, ``begin()``, ``fill()``, ``data()``.
- Pass it by value or by reference and the length travels with it.
  There is no decay to lose it.
- The same brace initialization, the same subscript, the same row-major
  layout as the C array underneath.

Reading the Angle Brackets
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Class template
   :class: tip

   A recipe for a type, not a type. The angle brackets fill in what is
   missing, and each different filling makes a different type.

.. code-block:: cpp

   std::array<int, 6> joint_deg;// 6 ints
   std::array<double, 6> torque_nm;// 6 doubles: a different type

- The angle brackets fill in what is missing. ``std::array<int, 6>`` and
  ``std::array<double, 6>`` are **different types**.
- One template, written once, serves every element type.

.. note::

   The mechanism is a **class template**, and
   :doc:`Lecture 6 </lectures/lecture6/l6_index>` covers it. For today,
   just read the notation: whatever sits in the brackets is what the
   container holds.

Initialization
^^^^^^^^^^^^^^

.. code-block:: cpp

   std::array<int, 6> a; // 1. garbage: no constructor runs
   std::array<int, 6> b{}; // 2. all six are 0: the braces do it
   std::array<int, 6> c{10, 20, 30}; // 3. 10 20 30 0 0 0
   std::array d{10, 20, 30}; // 4. deduces std::array<int, 3>

.. admonition:: Definition: Aggregate
   :class: tip

   A class with no constructor of its own, such as ``std::array`` or a
   plain ``struct``. Nothing runs when one is declared, so its members
   hold garbage until braces zero or fill them.

- These four cases match the C-style cases one for one.
- Case 4 is **class template argument deduction**. Give it the values
  and it figures out both the element type and the count. Lecture 6
  explains how.

.. note::

   You will see ``std::array<int, 3> e{{10, 20, 30}}`` in older code.
   The inner braces have been optional for a long time. Do not copy that
   style.

Visiting Every Element
^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Range-based ``for``
   :class: tip

   A loop that visits every element in order without an index. You never
   write the bounds, so it cannot run off either end. It works on any
   container in this lecture.

.. code-block:: cpp

   std::array<double, 3> ranges_m{3.0, 1.0, 4.0};

   for (const auto& r : ranges_m) {
       std::cout << r; // read each one
   }

**Three ways to write the loop variable**

- ``auto r`` gives you a **copy**. Writing to ``r`` changes nothing.
- ``auto& r`` gives you the element **itself**. Use it to change the
  element.
- ``const auto& r`` gives the element, read-only, no copy. **Use this by
  default.**

.. note::

   This is the reference rule from Lecture 3: ``auto&`` is a second
   *name* for the element, not a copy. See
   `cppreference: range-based for <https://en.cppreference.com/w/cpp/language/range-for>`_.
   Rule:
   `Core Guidelines ES.71 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-for-range>`_.

Access and Modification
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::array<int, 6> joint_deg{};

   joint_deg[9] = 1; // UB: no check, no complaint
   joint_deg.at(9) = 1;  // throws std::out_of_range
   int* p{joint_deg.data()}; // address of element 0: p[2] is joint_deg[2]

.. admonition:: Definition: ``data()``
   :class: tip

   A pointer to the first element of the block. It is **borrowed**, in
   Lecture 3's sense: you may look through it, you must not ``delete``
   it.

- ``operator[]`` is **unchecked**. Going out of range is undefined
  behaviour. It might overwrite a nearby variable, crash, or look like it
  worked.
- ``at()`` is **checked**. It throws, and the message gives you the
  numbers: ``array::at: __n (which is 9) >= _Nm (which is 6)``.
- Pointer arithmetic starts from ``data()``: ``joint_deg.data() + 2`` is
  ``&joint_deg[2]``. Never ``joint_deg + 2``: a ``std::array`` does not
  decay.

.. note::

   Which version to use for ``std::array``?
   `Core Guidelines SL.con.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-bounds>`_.

Multidimensional Arrays
-----------------------

.. admonition:: Definition: Occupancy grid
   :class: tip

   A map cut into cells, each one recording whether that patch of floor
   is free, blocked, or never scanned. Store one number per cell and the
   map becomes an array.

.. figure:: /_static/images/l4/occupancy_grid.png
   :width: 80%
   :align: center
   :alt: Two panels joined by an arrow. On the left, a patch of floor as a map of three rows by four cells, with three black obstacle cells, two grey unseen cells and seven white free cells. On the right, the same arrangement as numbers: 0 0 1 -1, then 0 0 1 -1, then 1 0 0 0, with a key reading free 0, blocked 1, unknown -1.

   From a patch of floor to what you store: one number per cell.

Declaration
^^^^^^^^^^^

Three rows of four cells, written both ways:

.. grid:: 2

   .. grid-item-card:: C array

      .. code-block:: cpp

         int grid[3][4]{};

         grid[1][2] = 1;

   .. grid-item-card:: ``std::array``

      .. code-block:: cpp

         std::array<std::array<int, 4>, 3> grid{};

         grid[1][2] = 1;

- Read the ``std::array`` version **inside out**: an array of 3, each
  holding an array of 4. The dimensions look backwards.
- ``sizeof(grid)`` is **48** either way, which is 3 × 4 × 4 bytes. Again,
  no overhead.
- ``grid.size()`` and ``std::size(grid)`` both answer **3**, the number
  of *rows*, not the number of cells. All twelve is rows × columns:
  ``grid.size() * grid[0].size()``, or
  ``sizeof(grid) / sizeof(grid[0][0])`` for the C array.
- As a parameter the C version is worse: ``void f(int grid[][4])``. Only
  the *first* dimension may be left out.

Row-major Order
^^^^^^^^^^^^^^^

.. admonition:: Definition: Row-major order
   :class: tip

   Rows stored one after another in one flat block. There is no second
   dimension in memory, so ``grid[i][j]`` sits at element i × cols + j.

.. code-block:: cpp

   int grid[3][4]{{0, 0, 1, -1}, {0, 0, 1, -1}, {1, 0, 0, 0}};

- ``grid[i][j]`` sits at element i × 4 + j, the row width times the row,
  plus the column. This is why the compiler has to know the **row
  width**, but not the number of rows.
- That **4 is the column count**, not ``sizeof(int)``, which is also 4
  here. Make the grid ``[3][5]`` and the offset becomes i × 5 + j.

.. figure:: /_static/images/l4/row_major.png
   :width: 90%
   :align: center
   :alt: Two panels for int grid[3][4]. On the left, the grid as a table of three rows by four columns with the 1 at row 1 column 2 highlighted. On the right, the same twelve values as one flat strip with the flat index 0 to 11 below each cell and the rows braced as row 0, row 1 and row 2, with the highlighted cell at flat index 6. A curved arrow joins the two highlighted cells over the caption grid[1][2] maps to flat index 1 times 4 plus 2 equals 6.

   The grid as it is written, and the grid as it is stored.

With the Layout
^^^^^^^^^^^^^^^

Put the **last index in the inner loop** and the order you visit matches
the order in memory.

.. code-block:: cpp

   for (int i{0}; i < 3; ++i)    // rows
     for (int j{0}; j < 4; ++j)  // columns
       grid[i][j] = 0;

.. figure:: /_static/images/l4/loop_with_layout.png
   :width: 90%
   :align: center
   :alt: On the left, the three by four grid as a table with a numbered badge in each cell giving the visit order, 1 to 12 straight across each row. On the right, the same values as one flat strip in memory order with short arcs joining each cell to its neighbour. A caption reads: every step lands on the next value in memory.

   Row by row: every step lands on the next value in memory.

Against the Layout
^^^^^^^^^^^^^^^^^^

Swap the two loops and the same twelve cells are visited in a different
order.

.. code-block:: cpp

   for (int j{0}; j < 4; ++j)    // columns
     for (int i{0}; i < 3; ++i)  // rows
       grid[i][j] = 0;

.. figure:: /_static/images/l4/loop_against_layout.png
   :width: 90%
   :align: center
   :alt: On the left, the three by four grid as a table with numbered badges giving the visit order down each column, reading 1, 4, 7, 10 then 2, 5, 8, 11 then 3, 6, 9, 12. On the right, the same values as one flat strip with long crossing arcs joining the cells in that visit order. A caption reads: every step jumps a whole row, then comes back for the rest.

   Column by column: every step jumps a whole row, then comes back for
   the rest.

.. note::

   On a 4000 × 4000 grid: **1.8 ms** with the layout, **19 ms** against
   it. The rule is that **the last index belongs in the inner loop**, and
   it follows from row-major order, nothing else.


Iterators
=========

An **iterator** is an object that identifies a position in a sequence
and can advance to the next one. See
`cppreference: Iterator library <https://en.cppreference.com/w/cpp/iterator>`_.

A Pointer Is Already an Iterator
--------------------------------

Walk an array with an iterator:

.. code-block:: cpp

   int joint_deg[6]{10, 20, 30, 40, 50, 60};

   int* it{&joint_deg[0]};   // start at the first element
   ++it;                     // step forward by sizeof(int)
   std::cout << *it;         // 20

.. figure:: /_static/images/l4/pointer_iterator.png
   :width: 85%
   :align: center
   :alt: A row of six cells holding 10 to 60, labelled with index and byte offset. A grey marker labelled it points at the first cell; a curved arrow labelled plus plus it, one element forward, four bytes, runs to a bold marker over the second cell holding 20. A caption reads: star it gives 20; the pointer names a position, dereferencing it reads the element there.

   The pointer names a position; dereferencing it reads the element
   there.

Begin and End
-------------

.. admonition:: Definition: Half-open range
   :class: tip

   The pair [begin, end): closed on the left, open on the right. The
   first position is in the range, the last one is not. Every container
   gives you both ends, apart from the adapters, which hide them on
   purpose.

.. code-block:: cpp

   std::array<int, 6> joint_deg{10, 20, 30, 40, 50, 60};

   // the first element, and one past the last element
   std::array<int, 6>::iterator first{joint_deg.begin()};
   std::array<int, 6>::iterator last{joint_deg.end()};

   std::cout << last - first;       // 6, the same as size()

- ``begin()`` is the position of the **first** element. ``*begin()``
  reads it, and writes it.
- ``end()`` is the position **one past** the last. A position, not an
  element.
- ``end() - begin()`` is the length: the same number ``size()`` gives.
- ``cbegin()`` and ``cend()`` are those same two positions, read-only.
- ``std::begin(x)`` and ``std::end(x)`` also accept a **C array**.

One Past the End
^^^^^^^^^^^^^^^^

``end()`` is a **position**, not an element. Dereferencing it is
undefined behaviour, just like dereferencing a one-past-the-end pointer.

.. code-block:: cpp

   std::array<int, 6> joint_deg{10, 20, 30, 40, 50, 60};

.. figure:: /_static/images/l4/half_open_range.png
   :width: 90%
   :align: center
   :alt: Six solid cells holding 10 through 60, indexed 0 to 5, followed by a seventh dashed grey cell left empty. A blue arrow labelled begin() points at the first cell; a grey arrow labelled end() points at the dashed cell, annotated not an element, never dereference. A brace under the six real cells reads end() minus begin() equals 6.

   Half-open: the length needs no plus or minus one, and an empty
   container is exactly ``begin() == end()``.

Writing the Loop
^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::array<double, 3> ranges_m{3.55, 1.28, 4.12};

   // 1. by index
   for (std::size_t i{0}; i < ranges_m.size(); ++i)
     std::cout << ranges_m[i];

   // 2. by iterator
   for (auto it{ranges_m.begin()}; it != ranges_m.end(); ++it)
     std::cout << *it;

   // 3. range-based
   for (const auto& r : ranges_m)
     std::cout << r;

- All three print the same thing. Prefer **3**, because you never write
  the bounds yourself, so it cannot run off either end.
- Use **2** when you need the position itself, for example to ``erase``
  at it or to stop partway through.
- Use **1** when the index is part of the problem, such as "cell *i* of
  the grid", or when you are walking two containers at once.

Exercise 1: Writing the Loop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trace the behaviour of the iterator ``iter`` in this loop.

.. code-block:: cpp

   std::array<double, 3> ranges_m{3.55, 1.28, 4.12};

   // 2. by iterator
   for (auto iter{ranges_m.begin()}; iter != ranges_m.end(); ++iter)
     std::cout << *iter;

Const Iterators
---------------

.. code-block:: cpp

   std::array<int, 6> joint_deg{};

   auto it{joint_deg.begin()}; // int* -- may write through it
   auto ct{joint_deg.cbegin()};  // int const* -- may not

   *it = 90; // fine
   *ct = 90; // error: assignment of read-only location

- Lecture 3 described ``const int*`` as locking the object, not the
  arrow. A ``const_iterator`` is **that same type** with a longer name,
  as the output above shows: ``int const*``.
- If the container is already ``const``, then plain ``begin()`` hands
  back a ``const_iterator`` anyway. There is nothing extra to ask for.
- ``cbegin()`` and ``cend()`` are for when the container is *not*
  ``const`` but you still want to promise that this particular walk will
  not write anything.

.. note::

   Same advice as Lecture 3. Write ``const`` wherever it is true and let
   the compiler check it every time, instead of relying on a promise.


Vectors
=======

A ``std::vector`` is a sequence container that holds its elements
contiguously on the heap and resizes itself as elements are added or
removed. See
`cppreference: std::vector <https://en.cppreference.com/w/cpp/container/vector>`_.

Vector in Memory
----------------

.. code-block:: cpp

   std::vector<int> ranges_m{10, 20, 30};
   ranges_m.reserve(6);
   std::cout << ranges_m.capacity(); // 6
   std::cout << sizeof(ranges_m);  // 24

.. figure:: /_static/images/l4/vector_memory.png
   :width: 80%
   :align: center
   :alt: At the top, a stack box named ranges_m with three fields labelled begin, end and capacity, each holding an address. Below, a heap row of six cells; the first three hold 10, 20 and 30 and the other three are empty. Three arrows drop from the fields onto the first cell, the cell just past the last element, and the point just past the last slot. Braces read size() equals 3, spare room, and capacity() equals 6.

Who Gives the Memory Back
-------------------------

.. admonition:: Definition: RAII
   :class: tip

   *Resource acquisition is initialization*: the constructor takes the
   resource, the destructor gives it back, and the compiler makes the
   destructor run on every way out.

- **Why the heap?** The element count is settled at run time, and
  ``push_back`` changes it again. A stack frame is laid out when the
  function is *compiled*, so it cannot hold something that grows.
- **Not always the heap.** An empty vector owns nothing: ``capacity()``
  is 0, ``data()`` is ``nullptr``.

.. note::

   No ``delete`` to forget, to run twice, or to skip on an early return.
   C++20, [stmt.jump], 8.7 paragraph 2: *on exit from a scope (however
   accomplished), objects with automatic storage duration ... are
   destroyed*. See
   `N4861: [stmt.jump] <https://timsong-cpp.github.io/cppwp/n4861/stmt.jump>`_.
   Rule:
   `Core Guidelines R.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-raii>`_.

The Pointer to the Block
------------------------

``data()`` hands out the **begin** pointer from the figure, as a plain
``int*``:

.. code-block:: cpp

   std::vector<int> ranges_m{10, 20, 30};
   int* p{ranges_m.data()};  // 0x6311...2b0 == &ranges_m[0]
   *(p + 1); // 20: pointer arithmetic

.. note::

   The one job for ``data()`` is a C API that wants a buffer and a count,
   such as a sensor driver. Pass it and ``size()`` together, and take the
   pointer fresh each call. See
   `cppreference: vector::data <https://en.cppreference.com/w/cpp/container/vector/data>`_.

Initialization
--------------

.. code-block:: cpp

   std::vector<int> a;       // empty
   std::vector<int> a2{};    // the same: empty, capacity 0
   std::vector<int> b(3, 7); // 7 7 7  -- three copies of 7
   std::vector<int> c{3, 7}; // 3 7  -- two elements
   std::vector<int> d(3);    // 0 0 0  -- three value-initialized
   std::vector<int> e{c};    // a copy of c

- ``b`` and ``c`` differ by **one character**, yet ``b.size()`` is 3 and
  ``c.size()`` is 2.
- The rule is simple. If the braces can be read as **a list of
  elements**, they will be. Parentheses are the only way to say count
  first, then value.
- ``d`` holds three zeros. A count on its own **value-initializes**
  every element: 0 for ``int``, 0.0 for ``double``, an empty string for
  ``std::string``.
- ``a`` and ``a2`` are identical. A vector has a **constructor**, so it
  is never garbage. On ``std::array`` the braces were the only thing
  zeroing it.

.. note::

   Lecture 2 said braces everywhere. This is the documented exception:
   parentheses for a **count**, braces for **contents**.

A Grid of Vectors
^^^^^^^^^^^^^^^^^

An occupancy grid sized at run time, ``rows`` by ``cols``, all zeros.
The nested form:

.. code-block:: cpp

   std::size_t rows{3};   // from the map header, at run time
   std::size_t cols{4};
   std::vector<std::vector<int>> nested(rows, std::vector<int>(cols, 0));
   nested[1][2] = 7;      // reads like the 2D array

.. figure:: /_static/images/l4/nested_grid.png
   :width: 90%
   :align: center
   :alt: A stack object named nested with begin, end and capacity fields points at an outer heap block of three vector objects labelled nested[0], nested[1] and nested[2], each showing its own begin, end and cap fields and annotated 3 objects, 72 bytes. From each object's begin field a black arrow runs down to a separate heap block of four int cells; the middle block reads 0 0 7 0 and the others 0 0 0 0, braced as row 0 block, row 1 block and row 2 block.

   Four allocations: the outer block, then one block per row.

Size and Capacity
-----------------

.. admonition:: Definition: ``size()``
   :class: tip

   How many elements the vector **holds**. This is the one your loops
   use.

.. admonition:: Definition: ``capacity()``
   :class: tip

   How many elements it could hold **before the block has to be
   replaced**. It is never smaller than ``size()``: ``capacity >= size``.

.. code-block:: cpp

   std::vector<int> v;
   v.push_back(1);
   v.push_back(2);
   v.push_back(3);

   v.size();       // 3  -- three elements
   v.capacity();   // 4  -- room for one more before it moves

The gap is **spare room**, not elements. Reading ``v[3]`` here is
undefined behaviour, even though the storage is sitting right there.

Growth and Reallocation
-----------------------

Your **bookshelf** is full and one more book arrives. You cannot make the
shelf longer, the wall is in the way, so you buy a bigger one, carry
every book across, and get rid of the old shelf. The question is *how
much* bigger.

.. figure:: /_static/images/l4/bookshelf.png
   :width: 85%
   :align: center
   :alt: Two rows of bookshelves. The top row, headed grow by one, shows a full shelf of capacity four, then a move to a full shelf of five, then another move to a full shelf of six: two more books, two whole moves. The bottom row, headed grow by a factor, shows the same shelf of four and a single move to a shelf of eight with four empty slots: the next four books just go on the shelf.

   Grow by one and every new book means a move. Grow by a factor and one
   move buys room for many.

.. note::

   A vector buys room **to spare**: capacity grows by a **factor**, not
   by a fixed amount, so the bigger it gets the rarer a move becomes.
   Here the capacities run 1, 2, 4, 8, 16, 32, and one million
   ``push_back`` calls cost **21** reallocations rather than a million.
   Spreading that rare cost over all the cheap calls is what
   **amortized** O(1) means.

The Four Steps
^^^^^^^^^^^^^^

.. admonition:: Definition: Reallocation
   :class: tip

   What a vector does when ``size() == capacity()`` and another element
   arrives. It cannot extend the block, because the memory right after it
   belongs to someone else, so it replaces the block in four steps. One
   reallocation is O(n): every element already stored is moved. It is
   rare enough that ``push_back`` stays amortized O(1).

1. **Allocate** a new, larger block on the heap. On libstdc++ it is
   twice the old capacity.
2. **Move** every existing element across, one by one. This is where
   the O(n) goes.
3. **Free** the old block. Anything still holding an address into it now
   points at freed memory.
4. **Update** the three pointers, begin, end and capacity, to the new
   block. Only then is the new element written.

.. warning::

   Step 3 is why every iterator, pointer and reference into the old block
   is now **dangling**. Steps 1 to 4 are the ``new``, copy and ``delete``
   you wrote by hand in Lecture 3, done correctly for you every time.

Exercise 2: Trace Size and Capacity
-----------------------------------

Fill in the two columns on paper, then work out how many times the
elements were moved.

.. code-block:: cpp

   std::vector<int> readings;

   for (int i{0}; i < 6; ++i) {
       readings.push_back(i);
       std::cout << readings.size() << "/" << readings.capacity() << '\n';
   }

.. note::

   A new vector has capacity **0**, not 1.

Answer
^^^^^^

.. list-table::
   :header-rows: 1

   * - push
     - start
     - 0
     - 1
     - 2
     - 3
     - 4
     - 5
   * - size
     - 0
     - 1
     - 2
     - 3
     - 4
     - 5
     - 6
   * - capacity
     - 0
     - 1
     - 2
     - 4
     - 4
     - 8
     - 8
   * - reallocated
     -
     - yes
     - yes
     - yes
     -
     - yes
     -

- **Four** reallocations for six elements, at pushes 0, 1, 2 and 4.
  Verified on GCC 13 / libstdc++.
- Pushes 3 and 5 were free: the capacity was already 4 and 8, so the
  element just went into spare room.
- Extending the loop to ten pushes gives capacities 1 2 4 4 8 8 8 8 16 16
  and **five** reallocations, the fifth at push 8, when 8 elements became
  9.
- Total element moves for six pushes: 1 + 2 + 4 = 7, since each
  reallocation moves everything already there. Growing by one instead
  would have moved 0 + 1 + 2 + 3 + 4 + 5 = 15.

.. note::

   The capacity column is **this implementation's**. The examinable
   facts are that it grows geometrically and that each growth moves
   every element.

Reserve and Shrink to Fit
-------------------------

.. admonition:: Definition: ``reserve(n)``
   :class: tip

   Allocates a block that can hold at least ``n`` elements, now. Capacity
   becomes at least ``n``; size does not change. If capacity is already
   ``n`` or more, nothing happens. It never shrinks.

.. code-block:: cpp

   std::vector<int> scan;
   scan.reserve(1080); // one allocation, now: 0/1080
   for (int i{0}; i < 1080; ++i)
       scan.push_back(read()); // zero reallocations

- Without it: **12** reallocations, **2047** moves, final capacity 2048.
- With it: **0** and **0**, final capacity 1080. Use it whenever the
  count is known up front.

.. note::

   Reserving also stops **invalidation**: if nothing can move the block,
   nothing pointing into it can dangle. See Iterator Invalidation below,
   and
   `cppreference: vector::reserve <https://en.cppreference.com/w/cpp/container/vector/reserve>`_.

Capacity Given Back
^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: ``shrink_to_fit()``
   :class: tip

   Asks the vector to release its spare capacity, so that capacity drops
   to size. The standard calls it a **non-binding request**: an
   implementation may ignore it. Size does not change.

.. code-block:: cpp

   std::vector<int> v;
   for (int i{0}; i < 1000; ++i)
       v.push_back(i);         // 1000/1024 after the loop
   v.shrink_to_fit();          // 1000/1000: 24 slots returned

- If it shrinks, it **reallocates**: new block, every element moved,
  every iterator invalidated.
- Do not call it before more pushes. The spare room is what makes the
  next push cheap.

.. note::

   libstdc++ (GCC 13) honours the request. Another library may not.
   Write code that is correct either way. See
   `cppreference: vector::shrink_to_fit <https://en.cppreference.com/w/cpp/container/vector/shrink_to_fit>`_.

Insertion
---------

Both add one element to the end. They differ in *where the element gets
built*.

.. code-block:: cpp

   std::vector<Waypoint> path;

   path.push_back(Waypoint{1, 2}); // build a Waypoint, then move it in
   path.emplace_back(3, 4);  // build it directly in the vector

- ``emplace_back`` takes the **constructor arguments** and forwards
  them, so the temporary never exists.
- For an ``int`` or a ``double`` the difference is nothing at all. It
  matters when the element is expensive to move.

insert and emplace
^^^^^^^^^^^^^^^^^^

To put an element anywhere other than the end, you have to say *where*.
The way you say it is with an **iterator**.

.. code-block:: cpp

   std::vector<int> v{10, 20, 30};

   v.insert(v.begin() + 1, 15);  // 10 15 20 30
   v.emplace(v.begin(), 5);  // 5 10 15 20 30

- The position is an **iterator**, the same value your loops use, so
  ``v.begin() + 1`` means "before the second element".
- Everything after the insertion point has to **shift up one place** to
  make room. That is O(n), and it is unavoidable in a contiguous block.
- ``insert(v.end(), x)`` is just ``push_back(x)``: nothing after it to
  shift.

.. note::

   If your code inserts into the middle inside a loop, then a vector is
   the wrong container, and no amount of ``reserve`` will help. The cost
   is the shifting, not the allocation. Choosing a Container says what to
   use instead.

Deletion
--------

.. code-block:: cpp

   std::vector<int> v{10, 20, 30, 40, 50};

   v.pop_back(); // 10 20 30 40  -- O(1), returns nothing
   auto it{v.erase(v.begin() + 1)};  // 10 30 40 -- it now points at 30
   v.erase(v.begin(), v.begin() + 2);  // 40 -- erase a range
   v.clear();  // empty

- ``pop_back()`` returns ``void``. If you want the value, read ``back()``
  *first*, then pop.
- ``erase`` shifts everything after the hole down, so O(n). It
  **returns an iterator to the next element**.
- That return value is what lets you erase while looping. Write
  ``it = v.erase(it)`` instead of ``++it``.

.. note::

   ``clear()`` sets ``size()`` to 0 and **leaves capacity alone**.
   Verified: a vector at 10/16 becomes 0/16. It destroys the elements,
   not the block. To give the memory back, follow it with
   ``shrink_to_fit()``.

Erasing by Value
^^^^^^^^^^^^^^^^

.. admonition:: Definition: Erase-remove idiom
   :class: tip

   ``erase`` takes a *position*. Removing every element equal to some
   *value* used to need this:

.. code-block:: cpp

   // the erase-remove idiom -- you will meet it in older code
   v.erase(std::remove(v.begin(), v.end(), 2), v.end());

Since C++20 it takes one call, and this course uses C++20:

.. code-block:: cpp

   std::erase(v, 2);         // returns how many were removed
   std::erase_if(v, is_stale);

- Checked on ``1 2 3 2 5 2``: ``std::erase(v, 2)`` returns ``3`` and
  leaves ``1 3 5``.
- The old version takes two steps because ``std::remove`` cannot change
  the size. It only holds iterators.

.. warning::

   Write ``std::erase`` yourself, but learn to read the old version,
   because the code you inherit is full of it. A ``std::remove`` on its
   own, with no ``erase`` after it, is a real bug that leaves the vector
   the same length. See
   `cppreference: std::erase, std::erase_if <https://en.cppreference.com/w/cpp/container/vector/erase2>`_.

Iterator Invalidation
---------------------

.. admonition:: Definition: Iterator invalidation
   :class: tip

   An iterator, pointer or reference into a container, including the
   pointer from ``data()``, stops being usable once a later operation
   moves or destroys what it points at. It is only good for as long as
   the block stays where it is.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Operation
     - What it invalidates
   * - ``push_back``, ``insert``, ``resize``
     - **Everything**, if it reallocates. Otherwise from the insertion
       point on
   * - ``reserve``
     - Everything, if it actually grows the block
   * - ``erase``
     - From the erased position on. Before it, still valid
   * - ``pop_back``
     - ``end()`` and the erased element only
   * - ``clear``
     - Everything
   * - ``operator[]``, ``at``, ``size``
     - Nothing. Reading never invalidates

Every "if it reallocates" is the same rule: a reallocation invalidates
everything. Reserve enough up front and the first two rows no longer
apply.

Lecture 3's Dangling Pointer, Renamed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> ranges_m{10, 20, 30};
   int* first{&ranges_m[0]};
   ranges_m.push_back(40); // reallocates: the old block is freed
   std::cout << *first;  // reads freed memory

.. warning::

   A container saves you from **calling** ``delete``. It does not save
   you from knowing **when the storage moves**. The full table:
   `cppreference: iterator invalidation <https://en.cppreference.com/w/cpp/container#Iterator_invalidation>`_.


Strings
=======

A **string** is a sequence of characters stored one after another. C++
has two: the **C-string**, a ``char`` array ended by a ``'\0'`` byte,
and ``std::string``, a container that stores its length, owns its buffer
and grows as text is added. See
`cppreference: null-terminated byte strings <https://en.cppreference.com/w/cpp/string/byte>`_
and
`cppreference: std::string <https://en.cppreference.com/w/cpp/string/basic_string>`_.

C-Strings
---------

.. code-block:: cpp

   auto name{"John Doe"};
   std::cout << typeid(name).name() << '\n';  // PKc: char const*

.. admonition:: Definition: C-string
   :class: tip

   Not a type. ``"John Doe"`` is a ``const char[9]``, eight characters
   and a ``'\0'``, that everyone agrees ends at that byte. Handed to
   ``auto`` it decays, so ``name`` is a pointer to the first character
   and nothing more.

- The length is stored nowhere. ``strlen`` walks from the pointer to the
  ``'\0'``, O(n) on every call.
- The ``s`` suffix from ``<string>`` makes the literal a ``std::string``
  instead: it stores its length and owns its buffer.

.. code-block:: cpp

   using namespace std::literals;
   auto name2{"John Doe"s};  // std::string
   std::cout << name2.size() << '\n';  // 8, stored: O(1)

Where the Characters Live
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto name{"John Doe"};  // name: on the stack, 0x7ffe...9b0
                           // the chars: .rodata, 0x61f6...004
   name = "Jane Doe";      // repoints name. "John Doe" is untouched
   name[0] = 'j';          // error: read-only location

- The literal has **static storage**. It sits in the ``.rodata`` segment
  from Lecture 2, next to the code, for the whole run. Only the pointer
  is a local.
- Assigning to ``name`` changes which literal it points at. Nothing
  rewrites ``"John Doe"``, and nothing is copied or freed.
- The characters are ``const``, so a write through the pointer does not
  compile. Cast the ``const`` away and the OS refuses instead:
  ``.rodata`` is mapped read-only, and the write segfaults.

.. note::

   A C-string from a literal is **not mutable**. To edit text, copy it
   into storage you own: ``char name[]{"John Doe"}`` puts a copy on the
   stack, and ``"John Doe"s`` puts one in a ``std::string``. See
   `cppreference: string literal <https://en.cppreference.com/w/cpp/language/string_literal>`_.

The Terminator
^^^^^^^^^^^^^^

The other way to write a C-string copies the literal into an array you
own, terminator included:

.. code-block:: cpp

   char name[]{"lidar"};   // a copy on the stack, 6 bytes
   sizeof(name);           // 6: array, terminator included
   std::strlen(name);      // 5: walks to '\0' on each call

- This copy is yours, so ``name[0] = 'L'`` is allowed. ``sizeof`` works
  only because ``name`` is an array; on the pointer form it would be 8.
- The length is still **not stored anywhere**: ``strlen`` is O(n) per
  call, and a loop with it in the condition is O(n²).

.. figure:: /_static/images/l4/c_string.png
   :width: 70%
   :align: center
   :alt: Six cells holding l, i, d, a, r and a null byte drawn in pale red, indexed 0 to 5. The last cell is annotated the terminator, one byte, not a character. A brace over all six reads sizeof(name) equals 6; a brace under the first five reads std::strlen(name) equals 5.

   The length is stored nowhere: ``strlen`` walks from the front until
   it meets the ``'\0'``, every time.

std::string
-----------

.. admonition:: Definition: ``std::string``
   :class: tip

   A class from ``<string>`` that owns its characters and stores its
   length. It took ``std::vector``'s interface, and C++20 calls it a
   contiguous container, though it never came from the STL. After the
   last character it keeps a ``'\0'`` for C APIs.

.. code-block:: cpp

   std::string topic{"/robot/scan"};

   topic.size();    topic.empty();    topic.capacity();
   topic[0];        topic.at(0);      topic.front();   topic.back();
   topic.push_back('!');              topic.reserve(64);
   for (char c : topic) { /* ... */ }

- Same names, same meanings, same costs as ``std::vector``. It grows the
  same way and it invalidates the same way.
- Measured: appending one character at a time takes the capacity through
  **15, 30, 60, 120**. That is geometric growth, exactly as in Growth and
  Reallocation.

.. note::

   Short text never touches the heap: the **small string optimization**,
   next. Rule:
   `Core Guidelines SL.str.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-string>`_.

Small String Optimization
^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Small string optimization
   :class: tip

   A small buffer kept *inside* the string object and used whenever the
   text fits. Most strings in real programs are short, like a topic name,
   and a heap block for ``"imu"`` would cost more than the string is
   worth.

.. code-block:: cpp

   sizeof(std::string) // 32 bytes, whatever the text is

- Those 32 bytes are a pointer, a length, and a ``union`` of *either*
  the heap capacity *or* the small buffer.

Inside the Object
^^^^^^^^^^^^^^^^^

Three characters fit in the 16-byte buffer, so the pointer points back
into the object itself:

.. figure:: /_static/images/l4/sso_short.png
   :width: 90%
   :align: center
   :alt: One 32-byte string object with three fields: pointer, size 3, and a 16-byte buffer split into byte cells holding i, m, u and a null byte. An arrow from the pointer loops back into the first buffer cell, and a note reads the characters are inside the object, nothing is allocated, capacity() equals 15.

   ``std::string s{"imu"}``: the third field is the buffer, and nothing
   is allocated.

On the Heap
^^^^^^^^^^^

Twenty-three characters do not fit. The same bytes now hold the
capacity, and the pointer goes to a heap block:

.. figure:: /_static/images/l4/sso_long.png
   :width: 90%
   :align: center
   :alt: One 32-byte string object with three fields: pointer, size 23, and a third field holding the capacity 23 with its second half greyed out as unused. An arrow from the pointer runs down to a heap block of character cells braced as 23 chars and a terminator, and a note reads the object holds only the address, the characters are on the heap.

   ``std::string l{"a-very-long-sensor-name"}``: the third field is the
   capacity, and the characters live on the heap.

Common Operations
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::string topic{"/robot"};

   topic += "/scan";              // append in place
   topic.append("/filtered");     // the same thing, spelled out
   topic.insert(0, "/tf");        // insert at a position
   topic.erase(0, 3);             // erase 3 characters from index 0
   topic.replace(0, 6, "/base");  // replace a range with new text

- ``a + b + c`` builds a **temporary at every** ``+``, and each one may
  allocate. ``+=`` appends into the buffer you already have and reuses
  the spare capacity.
- In a loop, build with ``+=``, or ``reserve`` first and then append.
- ``insert`` and ``erase`` shift the characters after them, so both cost
  O(n), for the same reason as a vector.

Searching
^^^^^^^^^

.. code-block:: cpp

   std::string topic{"/robot/scan"};

   topic.find("scan");     // 7      -- index where it starts
   topic.find("imu");      // npos   -- not found
   topic.substr(7);        // "scan"

   if (topic.find("imu") != std::string::npos) { /* found */ }

.. admonition:: Definition: ``npos``
   :class: tip

   What ``find`` returns when nothing is found. Not a special marker: it
   is the **largest possible** ``std::size_t``, 18446744073709551615, or
   2⁶⁴ − 1.

- So using a "not found" result as an index is a disaster, and it will
  not show up as −1 in a debugger.
- **Always compare against** ``npos``. A result of 0 means "found at the
  start", but as a bool it reads ``false``.

.. note::

   ``rfind`` searches from the end, and ``substr(pos, count)`` takes a
   length rather than a second index. Both are easy to get one-off wrong;
   check them against the documentation rather than guessing. See
   `cppreference: string::find <https://en.cppreference.com/w/cpp/string/basic_string/find>`_.

Input
^^^^^

``>>`` stops at the first whitespace. ``std::getline`` takes everything
up to the newline.

.. code-block:: cpp

   int id{};
   std::string topic;

   std::cin >> id;                 // reads 7, leaves the newline in the buffer
   std::getline(std::cin, topic);  // reads that leftover newline: EMPTY

- The fix is to eat the whitespace first. Put ``std::cin >> std::ws``
  before the ``getline`` and the topic reads ``/robot/scan`` as intended.

.. note::

   ``>>`` leaves the newline in the buffer and ``getline`` stops at it.
   The two functions disagree about whose job the newline is. See
   `cppreference: std::getline <https://en.cppreference.com/w/cpp/string/basic_string/getline>`_.

String Views
^^^^^^^^^^^^

.. admonition:: Definition: ``std::string_view``
   :class: tip

   **A pointer and a length** over someone else's characters. It owns
   nothing, allocates nothing and copies nothing.

.. code-block:: cpp

   void log(std::string_view msg);   // takes std::string, const char*,
                                     // or a literal -- with no copy

   std::string_view bad() {
       std::string local{"a-long-name-on-the-heap"};
       return local;   // the string dies here; the view outlives it
   }

- As a **read-only parameter** it is strictly better than
  ``const std::string&``, because a ``const char*`` argument no longer
  has to build a temporary string.
- ``bad()`` returns a **dangling view**. That is the dangling pointer
  from Lecture 3 with a length attached, and ASan reports it the same
  way.

.. warning::

   Store the ``std::string``. Pass the ``std::string_view``. Never store
   or return a view. See
   `cppreference: string_view <https://en.cppreference.com/w/cpp/string/basic_string_view>`_.
   Rule:
   `Core Guidelines SL.str.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rstr-view>`_.


Maps
====

An **associative container** stores key and value pairs and finds a
value from its key rather than from a position. See
`cppreference: std::map <https://en.cppreference.com/w/cpp/container/map>`_
and
`cppreference: std::unordered_map <https://en.cppreference.com/w/cpp/container/unordered_map>`_.

Keyed Lookup
------------

Say you have sensor names and their sampling periods. In a vector the
name is not a position, so you have to search for it:

.. code-block:: cpp

   std::vector<std::pair<std::string, double>> sensors;

   for (const auto& s : sensors) // O(n), every lookup
     if (s.first == "lidar") { /* ... */ }

With a map, the name itself is the handle:

.. code-block:: cpp

   std::map<std::string, double> sensors{{"lidar", 0.25}, {"imu", 0.01}};
   sensors.at("lidar");  // 0.25 -- O(log n)

- An **associative container** stores **key and value** pairs and finds
  the value from the key. Position is not part of the interface at all.
- The gain is as much about readability as speed. ``at("lidar")``
  cannot compare the wrong field; the vector loop can.

Ordered Maps
------------

.. admonition:: Definition: ``std::map``
   :class: tip

   An associative container that keeps its keys **in sorted order**, in
   a balanced binary tree rather than a block. Lookup, insert and erase
   cost O(log n), and the elements are **not contiguous**.

- Iterating over one visits the keys in order, with no sorting step
  needed.
- The order is ``std::less<Key>`` unless you supply your own comparison.

.. code-block:: cpp

   std::map<std::string, double> sensors{{"lidar", 0.25}, {"imu", 0.01}};

   for (const auto& [name, period] : sensors)
     std::cout << name << ' '; // imu lidar   -- sorted, not inserted

Insertion
^^^^^^^^^

.. code-block:: cpp

   std::map<std::string, double> sensors{{"imu", 0.01}};

   auto r{sensors.insert({"imu", 99.0})};  // key exists: nothing changes
   r.second;                               // false: not inserted
   sensors.at("imu");                      // still 0.01

   auto s{sensors.insert_or_assign("imu", 99.0)};  // overwrites
   s.second;                               // false: not inserted, but
   sensors.at("imu");                      // now 99

- ``insert`` and ``emplace`` **never overwrite**. Given a key that
  already exists, they return without changing anything, and the value
  you passed is thrown away.
- Both calls return a **pair**: ``.first`` is an iterator to the entry,
  ``.second`` is a ``bool`` that answers one question, "did I add a
  **new** entry?"

.. note::

   The ``bool`` does not report whether the value changed.
   ``insert_or_assign`` on an existing key overwrites the value and still
   returns ``false``, because no new entry was added. To see the value,
   read the map. See
   `cppreference: map::insert_or_assign <https://en.cppreference.com/w/cpp/container/map/insert_or_assign>`_.

Subscript Inserts
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::map<std::string, double> sensors{{"lidar", 0.25}, {"imu", 0.01}};

   double period{sensors["camera"]}; // "camera" is not in the map
                                     // {"camera", 0} is inserted

- Given a missing key, ``operator[]`` **builds a default value and
  inserts it**, then hands you a reference to it.
- This is also why ``operator[]`` does not exist on a ``const`` map. It
  might modify the map.

.. warning::

   Use ``[]`` only when you actually mean "insert if missing". Counting
   occurrences is the honest use for it. To **read** a value use
   ``at()``. To **ask** whether a key is there, use ``contains()`` or
   ``find()``.

The Four Right Tools
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Call
     - On a missing key
     - Use it when
   * - ``m.at(k)``
     - throws ``std::out_of_range``
     - the key must be there
   * - ``m.find(k)``
     - returns ``m.end()``
     - you want the value *if* present
   * - ``m.contains(k)`` (C++20)
     - returns ``false``
     - you only need yes or no
   * - ``m.count(k)``
     - returns ``0``
     - the old spelling of ``contains``

- **None of these four insert anything.**
- Use ``find`` when you want the value: it locates the entry once, and
  you read through the iterator.

Iterating a Map
^^^^^^^^^^^^^^^

Dereferencing a map iterator does not give you a value. It gives you
**both halves** of the pair:

.. code-block:: cpp

   std::map<std::string, double> sensors{{"lidar", 0.25}, {"imu", 0.01}};
   *sensors.begin()   // std::pair<const std::string, double>

   for (const auto& entry : sensors) // the long way
     std::cout << entry.first << ' ' << entry.second;

   for (const auto& [name, period] : sensors)  // C++17, readable
     std::cout << name << ' ' << period;

- The key half is ``const``. Changing it in place would break the
  ordering, so erase and re-insert instead.
- The second form uses **structured bindings** to name the two halves.
  **Lecture 6 explains how they work.** For today, read them as a way to
  avoid writing ``.first`` and ``.second``.

.. note::

   Prefer ``const auto&`` here for the same reason as everywhere else:
   the element is a pair containing a ``std::string``, and ``auto`` by
   value would copy it on every iteration. See
   `cppreference: structured bindings <https://en.cppreference.com/w/cpp/language/structured_binding>`_.

Unordered Maps
--------------

.. admonition:: Definition: ``std::unordered_map``
   :class: tip

   An associative container that stores each pair in a **bucket** chosen
   by a **hash function**, a function that turns the key into a number.
   Lookup is O(1) **on average**, O(n) at worst.

- The price: **there is no order at all**. Iterating walks the buckets,
  not the keys.
- ``bucket_count()`` and ``load_factor()`` show the machinery: 13
  buckets, load factor 0.23, for the map below.
- Built-in types and ``std::string`` hash for free. A key type you wrote
  needs a ``std::hash``, beyond this course, so keep keys to strings and
  numbers.

.. code-block:: cpp

   std::unordered_map<std::string, double> sensors{
       {"camera", 0.05}, {"imu", 0.01}, {"lidar", 0.25}};

   for (const auto& [name, period] : sensors)
     std::cout << name << ' '; // lidar imu camera   -- no order promised

Worked Example
^^^^^^^^^^^^^^

.. code-block:: cpp

   std::unordered_map<std::string, std::vector<double>> readings;

   readings["lidar"].push_back(2.31);  // insert if absent
   readings["lidar"].push_back(2.28);
   readings["imu"].push_back(0.04);

   if (auto it{readings.find("gps")}; it != readings.end())
     report(it->first, it->second.back());
   else
     std::cout << "no gps readings yet\n";

   for (const auto& [name, values] : readings)
     std::cout << name << ": " << values.size() << " samples\n";

.. note::

   Three containers in nine lines. Note the two deliberate choices:
   ``[]`` where inserting is wanted, ``find`` where it is not.


Choosing a Container
====================

The choice follows from two questions: is the size fixed when the
program is compiled, and is an element found by **position** or by
**key**?

Side by Side
------------

.. list-table::
   :header-rows: 1
   :widths: 24 16 18 20 22

   * - Container
     - Size
     - Elements
     - Find one
     - Invalidates on
   * - ``std::array``
     - compile time
     - in place
     - by index, O(1)
     - never
   * - ``std::vector``
     - grows
     - heap block
     - by index, O(1)
     - any reallocation
   * - ``std::string``
     - grows
     - SSO, then heap
     - by index, O(1)
     - any reallocation
   * - ``std::map``
     - grows
     - tree nodes
     - by key, O(log n)
     - only what you erase
   * - ``std::unordered_map``
     - grows
     - hash buckets
     - by key, O(1) avg.
     - rehash; erase

- None of this is specific to ``int`` or ``double``. A
  ``std::vector<Pose>`` or a ``std::map<std::string, JointState>``
  behaves exactly the same way, using types **you** write. **Lecture 6**
  covers how to declare them.
- Two questions decide it. Is the **size** fixed when you compile, and
  is the **handle** a position or a key?

.. note::

   The C-style array is left out of this table on purpose. It does
   everything ``std::array`` does, loses its length at the first function
   call, and gives you nothing back in return.

Default to Vector
-----------------

**Use** ``std::vector`` **unless you have a reason not to.**

The reasons not to:

- Fixed size: Use ``std::array``.
- The size is a **compile-time constant**. Use ``std::array``.
- The handle is a **key**. Use ``std::unordered_map``, or ``std::map``
  for order.
- It is **text**. Use ``std::string``.
- You insert **in the middle** constantly, and you have measured it.

.. note::

   Contiguous memory is fast: walking a vector uses every byte the
   hardware loads. Reach for something cleverer only when you can point
   to the measurement that made you. Rule:
   `Core Guidelines SL.con.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-vector>`_.

Exercise 3: Pick the Container
------------------------------

For each one, name the container and give **one sentence** explaining
why. Some of these have more than one good answer.

1. The six joint angles of a manipulator arm, read every control cycle.
2. A log of waypoints the robot has visited, appended to as it drives,
   length unknown in advance.
3. Calibration offsets, looked up by sensor name, printed in a report
   sorted by name at shutdown.
4. One lidar scan: 1080 range values, count known before the first
   sample arrives.
5. The last 100 commands, appended at one end and discarded from the
   other.

Answer the two questions from the table first. **Is the size fixed at
compile time**, and **is the handle a position or a key**? Number 5 is
not covered by today's five containers on purpose. Say what you would
need, rather than forcing one of ours to fit.


STL Algorithms
==============

An **STL algorithm** is a function template that operates on a range
given by two iterators, independently of the container that supplied
them.

Algorithms Take Iterators
-------------------------

Every algorithm in ``<algorithm>`` takes a **pair of iterators** marking
a half-open range. None of them take a container.

.. code-block:: cpp

   std::find(first, last, value);  // the shape

   std::find(topic.begin(), topic.end(), 's'); // a std::string -> 7
   std::max_element(std::begin(arr), std::end(arr)); // a C array -> 9
   std::max_element(v.begin(), v.end()); // a std::vector

- **One implementation works for every container.** There is no
  vector-sort and string-sort, just one sort.
- Because you pass *two* iterators, you get to run an algorithm over
  **part** of a container for free. ``std::sort(v.begin(), v.begin() +
  10)`` sorts only the first ten elements.
- An algorithm can never change a container's **size**. It holds
  iterators, not the container.

The Ones You Will Use
---------------------

.. code-block:: cpp

   std::vector<double> ranges_m{2.31, 0.42, 5.00, 0.18, 1.75};

   std::sort(ranges_m.begin(), ranges_m.end());  // 0.18 0.42 1.75 ...
   std::find(ranges_m.begin(), ranges_m.end(), 5.00); // iterator, or end()
   std::count(ranges_m.begin(), ranges_m.end(), 5.00); // 1
   *std::min_element(ranges_m.begin(), ranges_m.end());  // 0.18
   std::accumulate(ranges_m.begin(), ranges_m.end(), 0.0); // 9.66
   std::ranges::sort(ranges_m);  // C++20: one argument instead of two

- ``std::accumulate`` lives in ``<numeric>``, not ``<algorithm>``. That
  costs everyone one compile error.
- ``std::sort`` costs O(n log n) and needs a **random-access** iterator,
  so it works here but refuses a ``std::map``.

.. warning::

   **Watch the seed.** ``accumulate(..., 0.0)`` gives ``9.66``;
   ``accumulate(..., 0)`` gives ``8``. The seed's *type* becomes the
   accumulator's type, so an ``int`` seed truncates every addition. Both
   compile without a warning.

Predicates
^^^^^^^^^^

.. admonition:: Definition: Predicate
   :class: tip

   A function that answers yes or no about one element. Write it as an
   ordinary named function and pass its name to the algorithm.

.. code-block:: cpp

   bool is_far(const Waypoint& w) { return w.x * w.x + w.y * w.y > 25.0; }

   std::vector<Waypoint> path{{1, 2}, {3, 4}, {6, 0}, {0, 1}, {5, 5}};

   std::count_if(path.begin(), path.end(), is_far);  // 2
   std::find_if(path.begin(), path.end(), is_far);   // -> (6, 0), index 2

- You pass the function's **name**, with no parentheses. The algorithm
  calls it once per element.
- ``Waypoint`` is **a type you wrote**. Everything today works on it
  unchanged.

.. note::

   **Lecture 6 teaches lambdas properly.** You will meet this same test
   written inline as
   ``[](const Waypoint& w){ return w.x * w.x + w.y * w.y > 25.0; }``,
   which is an unnamed function written right where it is used. Read it
   that way today. You are not expected to write one.


Summary
=======

.. grid:: 1 1 2 2
    :gutter: 3

    .. grid-item-card:: Containers and iterators
        :class-card: sd-border-secondary

        - Every container uses the same names: ``size``, ``at``,
          ``front``, ``back``, ``begin``, ``end``. Learn the interface
          once.
        - An **iterator** is a position that supports ``*``, ``++``,
          ``==`` and ``!=``. For an array it really is a pointer. The
          range is [begin, end), so the length is ``end - begin``.

    .. grid-item-card:: array and vector
        :class-card: sd-border-secondary

        - A C array **decays** to a pointer and loses its length. A
          ``std::array`` cannot.
        - ``size()`` is the contents and ``capacity()`` is the block.
          Growth is geometric, so ``push_back`` is **amortized** O(1),
          and ``reserve`` removes the reallocations you can predict.
        - Reallocating **invalidates** every iterator, pointer and
          reference. It is the dangling pointer from Lecture 3, in code
          with no ``new``.

    .. grid-item-card:: string and map
        :class-card: sd-border-secondary

        - A ``std::string`` is a vector of ``char``, plus a ``'\0'`` for
          C APIs and **SSO**, so short strings never allocate.
        - A map is found by **key**. ``std::map`` is sorted at
          O(log n), ``std::unordered_map`` is hashed at O(1) average.
          Remember that ``operator[]`` **inserts**: read with ``at``,
          ask with ``contains``.

    .. grid-item-card:: What to actually write
        :class-card: sd-border-warning

        - ``std::vector``, unless the size is a compile-time constant
          (``std::array``), the handle is a key (a map), or it is text
          (``std::string``). Never a raw array, never ``new[]``.
