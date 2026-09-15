====================================================
Lecture
====================================================

:doc:`Lecture 2 </lectures/lecture2/l2_lecture>` established that every
object lives at an address, that ``&`` hands you that address, and that a
variable's **storage duration** (static, automatic, or dynamic) is
fixed by the way it is declared. Two of those three you have already
used. This lecture is about the third.

A **pointer** is a variable whose value is an address. That one sentence
is the whole idea; everything else on this page follows from it. Pointers
are what let a function reach an object it does not own, what lets a
program ask for memory while it is running, and what every smart pointer,
every ``std::vector``, and every ROS 2 node handle is built out of.

The examples on this page all come from one place: the flight controller
of a small quadrotor. It holds an altitude, reads a battery percentage,
drives four rotors, and logs what its sensors report. The names are
longer than ``a`` and ``p``, and that is on purpose. In code that flies
something, a pointer called ``p`` is a pointer whose purpose no reviewer
can check.

Variables also carry their **unit** as a suffix: ``altitude_m`` is metres,
``voltage_v`` is volts, ``battery_pct`` is percent. The unit belongs in the
name so a reviewer can catch a wrong assignment by reading the two names
alone, without hunting for where either value came from. NASA lost the Mars
Climate Orbiter in 1999 to exactly that mistake: one team worked in
pound-seconds, another in newton-seconds.

.. seealso::

   Assumed from :doc:`Lecture 2 </lectures/lecture2/l2_lecture>` and not
   repeated here: the segments of a process (``.text``, ``.rodata``,
   ``.data``, ``.bss``, heap, stack); storage duration and lifetime;
   uniform initialization; ``const`` and ``constexpr``; and ``typeid``
   for inspecting a type. Go back to that page if any of those are hazy.


Memory Addresses and Hexadecimal
================================

An **address** is just a number: *which byte*, counting from zero. On the
64-bit machines this course targets it is a 64-bit number, which is why
every pointer is **8 bytes**. Addresses print in **hexadecimal**, base 16,
marked by the ``0x`` prefix.

**Why hexadecimal.** The digits run ``0`` to ``9``, then ``a b c d e f``,
so ``0xf`` is 15. One hex digit is exactly **4 bits**, so two hex digits
are exactly **one byte**: ``0x41`` is ``0100 0001``. That is why debuggers
print bytes in pairs; binary would be four times longer and unreadable.

.. warning::

   **Hex arithmetic catches people out.**

   .. code-block:: text

      0x...a28 + 8  ==  0x...a30      not a36

   ``0x28`` is :math:`2 \times 16 + 8 = 40`. Add 8 to get 48, and 48 is
   ``0x30``. So ``a28`` to ``a30`` really *is* eight bytes, even though it
   looks like two.

.. note::

   **Reading the addresses on this page.** A real address is long, such as
   ``0x7ffd2e233a10``, and it changes on every run because of address
   space layout randomization. These notes elide the middle and write
   ``0x7ffd…a10``, so only the digits that matter are shown. Expect the
   last digit to be ``0``, ``4``, ``8`` or ``c``: an ``int`` sits at a
   multiple of 4 and a ``double`` at a multiple of 8, which is
   **alignment**.


Debug and Release Builds
========================

The same source compiles several very different ways. VS Code's
*CMake: Select Variant* offers five, and CMake turns the choice into
compiler flags:

.. list-table:: The five variants, with the flags CMake adds for each.
   :widths: 20 26 54
   :header-rows: 1
   :class: compact-table

   * - Variant
     - Flags CMake adds
     - What VS Code says it does
   * - ``Debug``
     - ``-g``
     - Disable optimizations, include debug information
   * - ``Release``
     - ``-O3 -DNDEBUG``
     - Optimize for speed, exclude debug information
   * - ``MinSizeRel``
     - ``-Os -DNDEBUG``
     - Optimize for smallest binary size
   * - ``RelWithDebInfo``
     - ``-O2 -g -DNDEBUG``
     - Optimize for speed, include debug information
   * - ``Unspecified``
     - *nothing at all*
     - "Let CMake pick the default build type"

**In VS Code.** Press :kbd:`Ctrl+Shift+P`, run *CMake: Select Variant*,
pick one, then *CMake: Build*. The current variant is shown in the Status
Bar. CMake Tools passes your choice as ``-DCMAKE_BUILD_TYPE=...`` when it
configures.

**In CMakeLists.txt.** Nothing in the course project sets a build type, so
choose one when nobody passes it:

.. code-block:: cmake

   if(NOT CMAKE_BUILD_TYPE)
       set(CMAKE_BUILD_TYPE Debug CACHE STRING "" FORCE)
   endif()

From a terminal you pass it yourself:

.. code-block:: bash

   cmake -S . -B build -DCMAKE_BUILD_TYPE=Release

.. important::

   **This course builds Debug.** Valgrind can only name the *line* that
   leaked when ``-g`` is there.

   Beware ``Unspecified``. It sounds like a sensible default, and it
   leaves you with no optimization **and** no debug information, which is
   the one combination nobody wants.


Three Storage Durations
=======================

Lecture 2 gave you the three storage durations, and the map they live
on:

.. figure:: /_static/images/l3/png/memory_layout_lifetime.png
   :align: center
   :alt: A horizontal band showing one process's virtual address space from
      low to high addresses: reserved, .text, .rodata, .data, .bss, heap,
      free space, stack and argv/env, each with a one-line note on its
      contents. The heap is red and labelled grows up, the stack is blue
      and labelled grows down, and their arrows point at each other into
      the grey free space between them, annotated: both grow into it, but
      never meet. A legend below colours the segments by storage duration:
      yellow for static, the whole program; blue for automatic, the
      enclosing block; red for dynamic, the heap.

   The address space of Lecture 2, colored by **storage duration**.
   This lecture lives in the two bands facing each other across the free
   space: the blue **stack**, where every variable you have written so
   far goes, and the red **heap**, which is the one region nothing will
   tidy up for you.

Here are the three again in one table, with the column that matters this
week on the right.

.. list-table:: The three storage durations, and who ends the lifetime.
   :widths: 18 30 26 26
   :header-rows: 1
   :class: compact-table

   * - Duration
     - Declared as
     - Lives in
     - Ends when
   * - **Static**
     - Global, or local with ``static``
     - ``.data`` / ``.bss``
     - The program exits
   * - **Automatic**
     - A local variable
     - The stack
     - Its scope ends
   * - **Dynamic**
     - ``new`` (or a container, internally)
     - The heap
     - **You** say ``delete``

The first two are managed for you: the compiler knows exactly where the
lifetime begins and ends, and emits the code to match. The third is the
one that has a human in the loop, and that is the entire reason this
lecture has a section called *What Goes Wrong*.

Stack and Heap
--------------

.. list-table:: The two regions a pointer normally points into.
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - 
     - Stack
     - Heap
   * - **Size fixed**
     - At compile time
     - At run time
   * - **Allocation cost**
     - One register adjustment
     - A call into the allocator
   * - **Freed**
     - Automatically, at the end of scope
     - Only by ``delete``
   * - **Total size**
     - Small and fixed (``ulimit -s``, typically 8 MiB)
     - Large; effectively the free memory of the machine
   * - **Outlives its scope?**
     - No
     - Yes, that is the point of it

.. tip::

   ``ulimit -s`` prints your stack limit in kilobytes. A recursive
   function with no base case runs into that limit and the program dies
   with a **stack overflow**.
   The heap has no such small ceiling, which is one reason large data
   goes there.

.. important::

   **You will rarely call the heap yourself.** ``std::vector``,
   ``std::string``, and the smart pointers all allocate on the heap for
   you and free it for you. When this course says "do not use ``new``",
   it does not mean "do not use the heap". It means "do not manage the
   heap by hand".


Pointers
========

What a Pointer Is
-----------------

A pointer is a variable whose **value** is the address **of another
object**. Its type says which kind: an ``int*`` holds the address of an
``int``, a ``double*`` the address of a ``double``.

It is a variable itself, so it also has a type, a size, and an address of
its own: where the *pointer* lives, not where it points. Those are two
different addresses, and keeping them apart is most of what the next
figure is for.

.. figure:: /_static/images/l3/png/pointer_anatomy.png
   :align: center
   :alt: Two variable boxes on the stack. The left box, named altitude_ptr,
      holds the address 0x7ffd...a04 and itself sits at 0x7ffd...9f8,
      noted: a pointer is a variable, it has its own address, and its value
      is another address. The right box, named altitude_m, holds 120 and
      sits at 0x7ffd...a04, noted: the object being pointed at, it does not
      know about the pointer. A blue arrow runs from altitude_ptr to
      altitude_m, labelled points to.

   ``int altitude_m{120}; int* altitude_ptr{&altitude_m};``. Here
   ``altitude_ptr`` is drawn the same way every other variable was drawn
   in Lecture 2, because it *is* one. What makes it a pointer is only
   what its value means.

Three things in that picture are worth saying out loud, because most
early pointer confusion is one of them:

.. grid:: 1 1 3 3
    :gutter: 3

    .. grid-item-card:: The pointer has its own address
        :class-card: sd-border-secondary

        ``altitude_ptr`` lives at ``0x7ffd…9f8``. That has nothing to do
        with the address it *stores*. A pointer to a pointer, later on,
        is exactly this observation used twice.

    .. grid-item-card:: The object does not know
        :class-card: sd-border-secondary

        Nothing about ``altitude_m`` changes when a pointer to it is
        created.
        An object has no idea how many pointers point at it, and that is
        precisely why dangling pointers are possible.

    .. grid-item-card:: The arrow is not stored
        :class-card: sd-border-secondary

        The arrow in the diagram is the *interpretation* of a number.
        Memory holds ``0x7ffd…a04``; the type ``int*`` is what says to
        read that number as "the address of an ``int``".

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Why the course needs them**

    - **Reaching an object you do not own.** A function that takes
      ``int*`` (or ``int&``) can modify the caller's variable, and does
      not copy it. Lecture 5 builds on this.
    - **Objects whose size or count is known only at run time.** Reading
      sensor data of unknown length needs the heap, and the heap is
      reached through a pointer.
    - **Polymorphism.** Calling a derived class's method through a base
      class pointer is how Lecture 9 makes different robots share one
      interface.
    - **ROS 2 and third-party libraries.** ``rclcpp`` hands you
      ``std::shared_ptr<Node>``; OpenCV, PCL, and the C libraries under
      them all speak raw pointers at their boundaries.

Declaring a Pointer
-------------------

.. code-block:: cpp

   type* identifier;

The ``*`` is part of the declaration, not an operation. Read the
declaration **inside-out**, starting at the identifier and working
outward:

.. code-block:: cpp

   int* altitude_ptr;        // altitude_ptr is a pointer to an int
   double* voltage_ptr;      // voltage_ptr is a pointer to a double
   int** altitude_handle;    // a pointer to a pointer to an int

.. warning::

   The ``*`` binds to the **declarator**, not to the type. This bites
   everyone exactly once:

   .. code-block:: cpp

      int* altitude_ptr, target_m;   // only altitude_ptr is a pointer
      int *left_ptr, *right_ptr;     // both of these are pointers

   The course style is ``int* altitude_ptr``, with the ``*`` next to the
   type, because
   that is where the reader looks for it. The cost of that style is the
   trap above, and the fix is simple: **one declaration per line**, which
   is also `ES.10: Declare one name (only) per declaration
   <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es10-declare-one-name-only-per-declaration>`_.

.. note::

   ``int* ptr``, ``int *ptr``, and ``int * ptr`` are the same
   declaration to the compiler. Pick one and be consistent; the course
   uses the first.

   You do not have to do it by hand. The course project has a
   ``.clang-format`` file at its root setting ``PointerAlignment: Left``,
   so **Format Document** rewrites all three spellings to ``int* ptr``.
   VS Code's C/C++ extension finds that file on its own.

   Ignore the ``Vc Format`` entries in the VS Code settings UI. They
   belong to a different formatting engine and are read only when
   ``C_Cpp.formatting`` is set to ``vcFormat``, which is not the default.
   Changing them while clang-format is in charge does nothing.

Initializing a Pointer
----------------------

.. code-block:: cpp

   type* identifier{value};

There are exactly three sensible values to start a pointer with:

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Initializer
     - Meaning
   * - ``nullptr``
     - "Points at nothing, and says so." The safe default.
   * - ``&variable``
     - The address of an object that already exists.
   * - ``new T{...}``
     - The address of a fresh object on the heap, which you now own.

.. danger::

   The fourth possibility is **no initializer at all**, and it is the one
   to avoid:

   .. code-block:: cpp

      int* imu_ptr;      // holds whatever was already in those 8 bytes
      *imu_ptr = 100;    // undefined behavior: writing to a random address

   An uninitialized pointer is called a **wild pointer**. It is worse
   than a null pointer: null fails immediately and visibly, whereas a
   wild pointer may quietly corrupt something far away and crash the
   program ten minutes later in a function that is perfectly correct.

The Address-of and Dereference Operators
-----------------------------------------

Two operators move between an object and its address, in opposite
directions.

.. figure:: /_static/images/l3/png/address_of_deref.png
   :align: center
   :alt: The boxes altitude_ptr and altitude_m, the first holding 0x7ffd...a04
      and the second holding 120 at that address. A teal arrow curves
      through the gap from altitude_m to altitude_ptr, labelled
      &altitude_m, the address of altitude_m, which is what altitude_ptr
      stores. A red arrow curves the other way, labelled *altitude_ptr, the
      object at that address, which is altitude_m.

   ``&`` goes from an object to its address; ``*`` goes from an address
   back to the object. They undo each other: ``*(&altitude_m)`` **is**
   ``altitude_m``.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int altitude_m{120};
       int* altitude_ptr{&altitude_m};

       std::cout << &altitude_m << '\n';      // 0x7ffd…a04, its address
       std::cout << altitude_ptr << '\n';     // 0x7ffd…a04, the same address
       std::cout << *altitude_ptr << '\n';    // 120, the object there
       std::cout << *(&altitude_m) << '\n';   // 120, the same object
   }

Same address, and the same type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``&altitude_m`` does not produce merely *an* address. It produces an
``int*``, which is exactly the type of ``altitude_ptr``, and that is why
the initialization compiles at all. Ask the compiler rather than take it
on trust:

.. code-block:: cpp

   #include <iostream>
   #include <typeinfo>

   int main() {
       int altitude_m{120};
       int* altitude_ptr{&altitude_m};

       std::cout << typeid(&altitude_m).name() << '\n';    // the type of &altitude_m
       std::cout << typeid(altitude_ptr).name() << '\n';   // the same type
   }

Run it and you get the *mangled* name, which is compiler-specific:

.. code-block:: text

   Pi
   Pi

``Pi`` is GCC for "**P**\ ointer to **i**\ nt". Pipe the program through
``c++filt -t`` to read it:

.. code-block:: bash

   ./week3 | c++filt -t

.. code-block:: text

   int*
   int*

Dereferencing is not read-only. ``*altitude_ptr`` names the object, so it
can appear on the left of an assignment, and writing through it changes
the original variable:

.. code-block:: cpp

   int altitude_m{120};
   int* altitude_ptr{&altitude_m};

   *altitude_ptr = 90;                  // writes through the pointer
   std::cout << altitude_m << '\n';     // 90
   *altitude_ptr *= 2;                  // works like any other name for it
   std::cout << altitude_m << '\n';     // 180

.. warning::

   ``*`` does three unrelated jobs, and you will see all three in one
   program:

   .. list-table::
      :widths: 30 35 35
      :header-rows: 1
      :class: compact-table

      * - Job
        - Example
        - Where it appears
      * - Multiplication
        - ``int area{w * h};``
        - Between two expressions
      * - Declare a pointer
        - ``int* p{&a};``
        - In a declaration, after a type
      * - Dereference
        - ``*altitude_ptr = 90;``
        - Before an expression that is a pointer

   Position tells them apart. The compiler is never confused; readers
   sometimes are.

.. admonition:: Exercise 1 (in class): Trace it on paper
   :class: hint

   Do not run this. Write down, line by line, the value of
   ``altitude_m``, the value of ``climb_m``, and what ``target_ptr``
   points to. Then say what the four outputs are.

   .. code-block:: cpp

      int altitude_m{4};
      int climb_m{7};
      int* target_ptr{&altitude_m};

      *target_ptr = *target_ptr + climb_m;   // (1)
      std::cout << altitude_m << '\n';
      std::cout << climb_m << '\n';

      target_ptr = &climb_m;                 // (2)
      *target_ptr = altitude_m;
      std::cout << altitude_m << '\n';
      std::cout << climb_m << '\n';

   .. dropdown:: Answer
      :class-container: sd-border-success

      **11, 7, 11, 11.**

      Line ``(1)``: ``*target_ptr`` is another name for ``altitude_m``,
      so this is ``altitude_m = altitude_m + climb_m``, that is
      ``4 + 7 = 11``. ``climb_m`` is only read, so it is still ``7``.

      Line ``(2)``: this assigns to ``target_ptr`` **itself**, not
      through it. The pointer stops pointing at ``altitude_m`` and starts
      pointing at ``climb_m``. The next line, ``*target_ptr =
      altitude_m``, therefore writes ``11`` into ``climb_m``.

      The whole exercise is the difference between ``target_ptr = …``
      (change the arrow) and ``*target_ptr = …`` (change what is at the
      end of the arrow).
      Getting that distinction automatic is most of what this lecture is
      for.

Null Pointers
-------------

A **null pointer** is a pointer that holds a reserved value meaning "this
points at no object". It is a real value with a definite meaning, unlike the
garbage in a wild pointer.

.. code-block:: cpp

   int* imu_ptr{nullptr};   // C++11 and later: the one to use
   int* gps_ptr{NULL};      // a C macro, usually 0; avoid in C++
   int* mag_ptr{0};         // legal, but 0 reads like a number, not an address
   int* baro_ptr{};         // value initialization: also null

.. important::

   Use ``nullptr``. It has its own type (``std::nullptr_t``), so it can
   never be mistaken for the integer ``0`` when the compiler chooses
   between overloads, and it says "pointer" to anyone reading the line.

Testing a pointer is normal C++: a pointer turns into a ``bool`` when
you test it, and it is ``false`` exactly when the pointer is null.

.. code-block:: cpp

   int* sensor_ptr{nullptr};

   if (sensor_ptr == nullptr) { /* explicit, and fine */ }
   if (!sensor_ptr)           { /* shorter, and means the same */ }

   if (sensor_ptr) {
       std::cout << *sensor_ptr << '\n';   // only reachable when it is not null
   } else {
       std::cout << "no sensor attached\n";
   }

.. note::

   **Why null is detectable at all.** Lecture 2's memory map starts with
   a *reserved* region around address ``0x0`` that is never mapped into
   the process. Dereferencing ``nullptr`` is undefined behavior by the
   standard, but on a normal system it lands in that unmapped region and
   the hardware stops the program with a segmentation fault. That is the
   best kind of bug: loud, immediate, and pointing at the right line.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Comparing pointers** (a C++20 detail worth knowing)

    - ``p1 == p2`` and ``p1 != p2`` are always well defined. Two pointers
      are equal when they hold the same address.
    - ``p1 < p2`` is only meaningful for pointers **into the same
      object**. Comparing pointers to two unrelated variables is
      unspecified. It will compile, but the answer means nothing.
    - If you genuinely need a total order over unrelated pointers (to use
      them as map keys, say), use ``std::less<int*>``, which is required
      to provide one. It is a comparison *object*: you construct one, then
      call it. It compares the two **addresses**, never the objects they
      point at.

    .. code-block:: cpp

       #include <functional>   // std::less

       int altitude_m{120};
       int battery_pct{88};        // an unrelated object

       int* altitude_ptr{&altitude_m};
       int* battery_ptr{&battery_pct};

       // unspecified: it compiles and produces an answer that means nothing
       bool guess{altitude_ptr < battery_ptr};

       // well defined: a real order, and the same one every time you ask
       std::less<int*> address_order{};
       bool ordered{address_order(altitude_ptr, battery_ptr)};

    Both lines produce a ``bool``, and on a given run they may well agree.
    The difference is that only the second one is *promised* to: ``<`` on
    pointers into unrelated objects has no meaning the standard will stand
    behind, so nothing stops it from answering differently after a
    recompile. ``std::less<int*>`` is specialized to give a strict total
    order over **all** ``int*`` values, whatever they point at.

    This is also why the ordered containers work on pointer keys: a
    ``std::map<int*, T>`` compares its keys with ``std::less<int*>`` by
    default, not with ``<``, so the container is on firm ground even
    though writing ``<`` yourself would not be. Lecture 4 covers the
    containers themselves.

Size of a Pointer
-----------------

Every pointer holds the same kind of thing, an address, so every
pointer has the same size, whatever it points to. On the 64-bit machines
this course targets, that is **8 bytes**.

.. code-block:: cpp

   #include <iostream>

   int main() {
       int altitude_m{120};
       double voltage_v{11.1};
       char status{'A'};

       int* altitude_ptr{&altitude_m};
       double* voltage_ptr{&voltage_v};
       char* status_ptr{&status};

       std::cout << sizeof(altitude_ptr) << ' ' << sizeof(voltage_ptr) << ' '
                 << sizeof(status_ptr) << '\n';
       std::cout << sizeof(altitude_m) << ' ' << sizeof(voltage_v) << ' '
                 << sizeof(status) << '\n';
   }

.. code-block:: text

   8 8 8
   4 8 1

The first line is the size of the three **pointers**; the second is the
size of the three **objects** they point to. ``sizeof(p)`` never tells
you anything about the object at the other end.

.. _l3-typed-pointers:

Typed Pointers
--------------

If all pointers are the same size and all hold the same kind of value,
why does a pointer have a type at all?

.. figure:: /_static/images/l3/png/typed_pointer.png
   :align: center
   :alt: Three rows, each a pointer and the object it points at. In every row
      a blue stack box holds an address and is marked sizeof of the pointer
      equals 8, with an arrow to the bytes of its object, tinted teal. Row
      one: char* status_ptr holds 0x7ffd...a00 and points at status, one
      byte, 0100 0001, marked sizeof(*status_ptr) == 1, read as the
      character 'A'. Row two: int* altitude_ptr holds 0x7ffd...a04 and
      points at altitude_m, four bytes, marked sizeof(*altitude_ptr) == 4
      and little-endian, read as 120. Row three: double* voltage_ptr holds
      0x7ffd...a08 and points at voltage_v, eight bytes, marked
      sizeof(*voltage_ptr) == 8 and little-endian, read as 11.1.

   These are the three variables from the ``sizeof`` example above, each
   at its own address. All three pointers are **8 bytes**, because all
   three hold an address. The type is there for the **dereference**:
   ``sizeof(p)`` is the size of the pointer, ``sizeof(*p)`` is the size of
   the object it points at.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Byte order: little-endian and big-endian**

    A one-byte object has nothing to arrange. An object of two bytes or
    more does: its bytes sit at consecutive addresses, and **byte order**,
    or **endianness**, is the question of which end goes first.

    Take ``int mission_id{16909060};``, whose four bytes are all
    different:

    .. list-table:: One ``int``, two possible arrangements.
       :widths: 34 16 16 16 16
       :header-rows: 1
       :class: compact-table

       * - stored at
         - ``…a04``
         - ``…a05``
         - ``…a06``
         - ``…a07``
       * - **little-endian**
         - ``0000 0100``
         - ``0000 0011``
         - ``0000 0010``
         - ``0000 0001``
       * - **big-endian**
         - ``0000 0001``
         - ``0000 0010``
         - ``0000 0011``
         - ``0000 0100``

    - **Little-endian** puts the **least** significant byte at the
      **lowest** address. Every machine in this course is little-endian,
      which is why ``altitude_m`` in the figure above begins with
      ``0111 1000`` (that is 120) and is followed by three zero bytes,
      rather than the other way round.
    - **Big-endian** puts the **most** significant byte first, which is
      the order you would write the number on paper. The internet
      protocols specify it, so it is also called **network byte order**.

    The names come from *Gulliver's Travels*, where a war is fought over
    which end of a boiled egg to crack. That is the point: neither order
    is better, and each machine has simply picked one.

The type also lets the compiler stop you from mixing things up.The type also lets the compiler stop you from mixing things up. There is
no implicit conversion between unrelated pointer types:

.. code-block:: cpp

   int altitude_m{120};
   double voltage_v{11.1};

   int* altitude_ptr{nullptr};
   altitude_ptr = &altitude_m;   // OK
   altitude_ptr = &voltage_v;    // error: cannot convert 'double*' to 'int*'

.. warning::

   ``auto`` deduces pointer types correctly but hides them from the
   reader:

   .. code-block:: cpp

      auto altitude_m{120};
      auto ptr{&altitude_m};     // ptr is int*, but the line does not say so

   Write the type out for pointers: ``int* altitude_ptr{&altitude_m};``.
   "It is a pointer" is exactly the fact a reader must not have to work
   out.

.. seealso::

   You can always ask the compiler what a type is, with the ``typeid``
   technique from
   :doc:`Lecture 2 </lectures/lecture2/l2_lecture>`:

   .. code-block:: bash

      ./week3 | c++filt -t

Pointer Arithmetic
------------------

The type decides how much ``*ptr`` reads. It decides one more thing: how
far ``ptr + 1`` moves. These are the operations, and one rule sits behind
all of them:

.. code-block:: cpp

   ptr + n     ptr - n     ++ptr     --ptr     ptr2 - ptr1

Every one of them counts in **objects**, never in bytes. ``sizeof(*ptr)``
scales the step going out and scales it back on the way in, which is why
subtracting two pointers gives a count of objects rather than a distance
in bytes.

Adding ``1`` therefore does **not** mean "one byte later". It means
**one object later**:

.. code-block:: cpp

   int altitude_m{120};
   double voltage_v{11.1};

   int* altitude_ptr{&altitude_m};
   double* voltage_ptr{&voltage_v};

   std::cout << altitude_ptr << '\n';       // 0x7ffd…a10
   std::cout << altitude_ptr + 1 << '\n';   // 0x7ffd…a14, four bytes on
   std::cout << voltage_ptr << '\n';        // 0x7ffd…a20
   std::cout << voltage_ptr + 1 << '\n';    // 0x7ffd…a28, eight bytes on

Addresses print in **hexadecimal**. The ones above are picked so the
arithmetic reads the same either way; real ones often will not, and
``a28 + 8`` is ``a30``, not ``a36``.

.. list-table:: ``+ 1`` moves by one object, and objects are not the same size.
   :widths: 26 20 54
   :header-rows: 1
   :class: compact-table

   * - Pointer
     - ``sizeof(*p)``
     - ``p + 1`` lands
   * - ``char*``
     - 1
     - 1 byte on
   * - ``int*``
     - 4
     - 4 bytes on
   * - ``double*``
     - 8
     - 8 bytes on

This is the figure from :ref:`Typed Pointers <l3-typed-pointers>` read
from the other side. There, the type said how many bytes a dereference
*reads*; here, the same number says how far a step *moves*. Both come
from ``sizeof(*p)``, which is why a pointer that has lost its type has
lost both.

The rest of the arithmetic follows from that one rule. ``++p`` and
``p += 1`` advance one object, ``--p`` and ``p -= 1`` go back one, and
subtracting two pointers gives a count of **objects, not bytes**:

.. code-block:: cpp

   std::cout << (altitude_ptr + 1) - altitude_ptr << '\n';   // 1, not 4

.. note::

   ``std::cout << p`` prints an address for every pointer type except
   ``char*``, which the stream treats as the start of a C-string and
   tries to print as text. That is a Lecture 4 topic; for now, just know
   that ``char*`` is the one type where printing a pointer does not show
   you a pointer.

What is legal on a single object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the purposes of arithmetic, a lone variable counts as an array of
one element. That gives exactly two positions you are allowed to name:

- ``altitude_ptr``, the object itself.
- ``altitude_ptr + 1``, the **one-past-the-end** position. You may form it and
  compare with it. You may **not** dereference it.

.. danger::

   Everything beyond those two is undefined behaviour, and **none of it
   is a compile error**:

   .. code-block:: cpp

      int altitude_m{120};
      int* altitude_ptr{&altitude_m};

      std::cout << *(altitude_ptr + 1) << '\n';   // UB: reading past the object
      int* far{altitude_ptr + 2};                 // UB: even forming this
      int battery_pct{88};
      &battery_pct - altitude_ptr;                // UB: unrelated objects

   ``*(altitude_ptr + 1)`` is the dangerous one, because it *works*. Compiled
   normally it prints whatever happens to sit next on the stack:

   .. code-block:: text

      433613372

   No warning, no crash, a plausible-looking number, and a different
   answer tomorrow. Built with ``-fsanitize=address`` that same
   ``*(altitude_ptr + 1)`` says what is really going on:

   .. code-block:: text

      ERROR: AddressSanitizer: stack-buffer-overflow
      READ of size 4 at 0x711a76d00024

   This is exactly the case the sanitizers section below exists for.

   ``&battery_pct - altitude_ptr`` is the same rule you met in **Comparing
   pointers** above: arithmetic between pointers into *unrelated* objects
   has no meaning, whether you subtract them or compare them with ``<``.

.. note::

   **Why this section is short.** On a single variable, pointer
   arithmetic is all rules and no use: there is nowhere to go and nothing
   to find. It earns its keep when the objects it steps through are
   genuinely laid out one after another in memory, which is what an
   **array** is. :doc:`Lecture 4 </lectures/lecture4/l4_index>` introduces
   arrays and ``std::vector``, and there ``p + 1``, ``++p`` and
   ``p2 - p1`` stop being trivia and become how you walk a container.
   What you need from this section is the *scaling* rule, because that is
   the part students get wrong later: ``p + 1`` moves by
   ``sizeof(*p)`` bytes, never by one.


Const-Correctness
-----------------

``const`` and a pointer can each be constant, independently. That gives
three useful combinations, and the syntax for them is the single most
misread piece of declaration syntax in C++.

Each ``const`` locks one thing: the object at the end of the arrow, or
the arrow itself.

.. list-table:: What each ``const`` forbids. ``altitude_m`` and
                ``target_alt_m`` are ``int``.
   :widths: 34 14 16 36
   :header-rows: 1
   :class: compact-table

   * - Declaration
     - ``*altitude_ptr = 90;``
     - ``altitude_ptr = &target_alt_m;``
     - Read right to left as
   * - ``int* altitude_ptr{&altitude_m};``
     - yes
     - yes
     - a pointer to an ``int``
   * - ``const int* altitude_ptr{&altitude_m};``
     - **no**
     - yes
     - a pointer to a ``const int``
   * - ``int* const altitude_ptr{&altitude_m};``
     - yes
     - **no**
     - a ``const`` pointer to an ``int``
   * - ``const int* const altitude_ptr{&altitude_m};``
     - **no**
     - **no**
     - a ``const`` pointer to a ``const int``

The middle two columns are the only two things a pointer can do: write
through it, and repoint it. Each ``const`` takes one of them away.

.. code-block:: cpp

   int altitude_m{120};
   int target_alt_m{80};

   // 1. pointer to const: the object is read-only *through this pointer*
   const int* altitude_ptr1{&altitude_m};
   // *altitude_ptr1 = 90;               // error
   altitude_ptr1 = &target_alt_m;        // OK

   // 2. const pointer: the arrow is frozen, the object is not
   int* const altitude_ptr2{&altitude_m};   // must be initialized here
   *altitude_ptr2 = 90;                     // OK
   // altitude_ptr2 = &target_alt_m;        // error

   // 3. const pointer to const: both frozen
   const int* const altitude_ptr3{&altitude_m};
   // *altitude_ptr3 = 90;                  // error
   // altitude_ptr3 = &target_alt_m;        // error

.. tip::

   **The reading rule.** Go right to left from the identifier, and read
   ``*`` as "pointer to":

   - ``const int* altitude_ptr`` → *pointer to* a *const int*.
   - ``int* const altitude_ptr`` → *const pointer* to an *int*.
   - ``const int* const altitude_ptr`` → *const pointer* to a *const int*.

   ``const int*`` and ``int const*`` mean the same thing. The right-to-
   left rule works on the second spelling with no exceptions, which is
   why some codebases prefer it.

.. note::

   A ``const int*`` does **not** promise the object never changes. It
   promises *you* will not change it *through that pointer*:

   .. code-block:: cpp

      int altitude_m{120};
      const int* altitude_view{&altitude_m};
      altitude_m = 118;                       // fine: altitude_m is not const
      std::cout << *altitude_view << '\n';    // 118

   Pointer-to-const is about **permission at this access path**, not
   about immutability of the object.

.. admonition:: Discussion 1 (in class): Who is ``const`` for?
   :class: important

   A flight controller has one altitude reading, and several parts of the
   code need to get at it. Here are four ways to hand it out:

   .. code-block:: cpp

      int altitude_m{120};
      int target_alt_m{80};

      int altitude_copy{altitude_m};            // 1. a copy
      int* altitude_ctrl{&altitude_m};          // 2. a pointer
      const int* altitude_view{&altitude_m};    // 3. a pointer to const
      int* const altitude_fixed{&altitude_m};   // 4. a const pointer

   All four compile. Discuss with the person next to you:

   1. Which of the four can set ``altitude_m`` to 90? Which of them can
      be made to refer to ``target_alt_m`` instead? Answer both from the
      declarations alone, without reading the code that follows them.
   2. What does ``sizeof`` report for each? Which cost 8 bytes and which
      costs 4?
   3. Suppose the very next line is ``altitude_m = 118;``. Which of the
      four report 118 afterwards, and which does not?
   4. Which of the four can be given "no altitude at all", and which
      cannot? When is that worth having, and when is it a nuisance?
   5. Someone argues that ``const`` is pointless because they simply will
      not write to the object. What does the compiler give you that a
      promise does not?

   .. dropdown:: Talking points
      :class-container: sd-border-success

      - Writing: only ``altitude_ctrl`` and ``altitude_fixed`` can do
        ``*p = 90``. Repointing: only ``altitude_ctrl`` and
        ``altitude_view`` can be aimed at ``target_alt_m``. Each
        ``const`` takes away exactly one of the two, and the declaration
        is where it says so. ``altitude_copy = target_alt_m;`` compiles,
        but it changes only the copy: it was never a way to reach
        anything.
      - ``altitude_copy`` is an ``int``, so 4 bytes. All three pointers
        are 8 bytes, whatever they point at and whatever ``const`` is
        attached to them.
      - All three pointers report 118. ``altitude_copy`` still reports
        120: it was a snapshot, and it went stale the moment
        ``altitude_m`` changed. In particular ``altitude_view`` reports
        118, which is the point of the note above: pointer-to-const
        restricts *this access path*, it does not promise the object
        never changes.
      - Only the pointers can hold ``nullptr``, so only they can
        represent "no reading available" as a value. That is a feature
        when absence is a real state to model, and a liability when it is
        not, because then every single use has to be guarded first.
      - ``const`` is checked by the compiler on **every** use, including
        the ones written next semester by someone who never heard your
        promise. It also records the intent in the one place a reader
        reliably looks: the declaration. Writing ``const`` wherever it is
        true is what **const-correctness** means, and it is much easier
        to start that way than to add it afterwards, because ``const``
        spreads: once an access path is ``const``, everything you reach
        through it has to be ``const`` too.

Where the Pointee Lives
-----------------------

Nothing so far required the heap. A pointer can just as happily point at
an ordinary local variable, and most of the pointers you will write in
this course do.

.. figure:: /_static/images/l3/png/pointee_location.png
   :align: center
   :alt: Two rows. In the top row, int altitude_m{120}; int*
      altitude_ptr{&altitude_m}; draws a stack pointer box with a blue
      arrow to a named stack box holding 120, noted: the object has a name
      and a scope, it dies at the end of it. In the bottom row, int*
      battery_pct{new int{88}}; draws the same pointer with a red arrow to
      a heap box holding 88 headed no name, noted: the object has no name
      and no scope, it lives until delete.

   The pointer is the same variable in both rows. What differs is the
   object at the other end: one has a name and a scope, the other has
   neither.

That difference is the whole of the next section:

- A pointer into the **stack** points at an object somebody else's scope
  is responsible for. When that scope ends, the object is gone and your
  pointer is stale, but you were never responsible for freeing it.
- A pointer into the **heap** points at an object with no name and no
  scope. Nothing will ever free it for you. That job is now yours, and
  freeing it is the only thing ``delete`` is for.


Dynamic Memory
==============

.. warning::

   **A note on how this material is used.** Almost everything in this
   section (``new``, ``delete``, and the four ways they go wrong) is
   material you need to **read** and **debug**, not material you should
   **write**. Modern C++ manages heap memory with
   :doc:`smart pointers </lectures/lecture7/l7_index>` and containers.
   You are learning the manual version first because it is the only way
   to understand what the automatic version is doing for you, and
   because you will meet it in other people's code.

**Dynamic memory allocation** is asking for storage while the program is
running, and being handed the address of it. You need it whenever the
amount of data is not known when the program is compiled.

The ``new`` Operator
--------------------

.. code-block:: cpp

   int* battery_pct{new int{88}};

``new int{88}`` does three things, in order:

1. asks the allocator for enough bytes to hold an ``int``;
2. creates an ``int`` there, initialized to ``88``;
3. yields the **address** of that object, which is what ``battery_pct``
   stores.

.. figure:: /_static/images/l3/png/new.png
   :align: center
   :alt: A stack box named battery_pct holding the address 0x5591...2b0, with
      a red arrow to a heap box holding 88 whose own address is
      0x5591...2b0.

   ``battery_pct`` is an ordinary stack variable. What it holds is an
   address, and what lives at that address is on the heap, with no name
   of its own.

.. note::

   If the allocator cannot find the memory, ``new`` does **not** hand
   back ``nullptr``. It throws ``std::bad_alloc``, so a pointer that
   comes back from ``new`` is never null and never needs checking for
   that. Exceptions are covered in the reading material on exception
   handling.

.. important::

   **The object created by ``new`` has no name.** It is not a variable.
   It cannot go out of scope, because it is not in any scope. The only
   way to reach it, ever, is through the address you were handed at
   allocation.

So losing the address is not an inconvenience. It is final:

.. code-block:: cpp

   {
       int* battery_pct{new int{88}};   // the only address of that object
   }   // battery_pct dies here. The int does not: it is still
       // allocated, and nothing knows where it is any more.

.. figure:: /_static/images/l3/png/new2.png
   :align: center
   :alt: The same two boxes, but the stack box named battery_pct is now greyed
      out, dashed and labelled freed, while the heap box still holds 88 at
      address 0x5591...2b0 with no arrow reaching it.

   The pointer went out of scope; **the object could not**, because it
   was never in one. Lose that address and the object is unreachable but
   still allocated, which is precisely the definition of a memory leak.

The ``delete`` Operator
-----------------------

``new`` made you the owner. ``delete`` is the only way to hand the storage
back. Write the two lines as a pair, and in this order:

.. code-block:: cpp

   int* battery_pct{new int{88}};
   // ... use *battery_pct ...
   delete battery_pct;       // the storage goes back
   battery_pct = nullptr;    // and now the pointer says so

.. figure:: /_static/images/l3/png/new_delete.png
   :align: center
   :alt: Three numbered stages. One, int* battery_pct{new int{88}};: a stack
      box named battery_pct holds a heap address and a red arrow points to
      a live heap box holding 88. Two, delete battery_pct;: the heap box is
      greyed, dashed and labelled freed, the arrow is dashed and labelled
      dangling, and the pointer still holds the old address. Three,
      battery_pct = nullptr;: the pointer holds nullptr and no arrow leaves
      it, noted: no arrow, it points nowhere.

   The three states of a raw owning pointer. Stage 2 is the dangerous
   one, and it is the state your program is in between every ``delete``
   and the line after it.

``delete`` acts on the **storage**, not on the pointer. Everything below
follows from that one sentence.

.. warning::

   **``delete`` does not delete anything you can see.**

   - It does not erase the bytes. The value is usually still sitting
     there, which is why buggy programs so often appear to work.
   - It does not destroy ``battery_pct``. That is an ordinary automatic
     variable, and it still holds the same address it held a line
     earlier.
   - It does not change the arrow in the diagram. The pointer still
     points at that address. The address is simply no longer yours.

   What it does do is hand the storage back, after which every use of
   that address is undefined behavior.

Three rules about ``delete`` follow, and all three come up in the
exercises:

.. grid:: 1 1 3 3
    :gutter: 3

    .. grid-item-card:: Only ``delete`` what you ``new``
        :class-card: sd-border-warning

        .. code-block:: cpp

           int altitude_m{120};
           int* altitude_ptr{&altitude_m};
           delete altitude_ptr;   // UB

        ``altitude_m`` is on the stack. The allocator never handed it
        out and cannot take it back.

    .. grid-item-card:: ``delete nullptr`` is safe
        :class-card: sd-border-secondary

        .. code-block:: cpp

           int* battery_pct{nullptr};
           delete battery_pct;   // does nothing

        Guaranteed by the standard, so ``if (ptr) { delete ptr; }`` is
        redundant. Just write ``delete ptr;``.

    .. grid-item-card:: ``delete`` exactly once
        :class-card: sd-border-warning

        .. code-block:: cpp

           delete battery_pct;
           delete battery_pct;   // UB

        Setting the pointer to ``nullptr`` after the first one turns the
        second into a harmless no-op.

.. admonition:: Exercise 2 (in class): Where does it go wrong?
   :class: hint

   This compiles cleanly with ``-Wall -Wextra -Wpedantic``. It has
   **three** distinct memory bugs. Find them, name them, and say what the
   minimal fix for each one is.

   .. code-block:: cpp
      :linenos:

      #include <iostream>

      int main() {
          int* imu_reading{new int{118}};
          int* gps_reading{new int{121}};

          imu_reading = gps_reading;             // line 7

          std::cout << *imu_reading << '\n';
          delete imu_reading;                    // line 10
          delete gps_reading;                    // line 11

          std::cout << *gps_reading << '\n';     // line 13
      }

   .. dropdown:: Answer
      :class-container: sd-border-success

      **1. A memory leak, at line 7.** ``imu_reading`` was the only
      pointer to the first ``int``. Overwriting it loses the only address
      of an object that is still allocated; nothing can ever free it now.
      The fix is to ``delete imu_reading;`` *before* the assignment, or
      better still, to not have two raw owning pointers in the first
      place.

      **2. A double delete, at line 11.** After line 7, ``imu_reading``
      and ``gps_reading`` hold the *same* address. Line 10 frees that
      block and line 11 frees it again. The fix is that exactly one
      pointer owns a block: delete it once, and set the pointer to
      ``nullptr``.

      **3. A dangling read, at line 13.** By line 13 the block has been
      freed, so ``*gps_reading`` reads storage that is no longer ours. This is the
      bug that will *appear* to work: the old value is usually still in
      those bytes.

      Notice what the three have in common: none of them is a mistake
      about pointer *syntax*. They are all mistakes about **ownership**:
      who is responsible for freeing this block, and is that still
      true two lines later? That question is what
      :doc:`smart pointers </lectures/lecture7/l7_index>` answer by
      construction.

What Goes Wrong
---------------

Four failure modes account for nearly every bug in hand-managed memory:
a **dangling pointer**, a **memory leak**, a **double delete**, and a
**null dereference**. Each one gets its own picture below. The first of
them you have already seen. It is stage 2 of the previous figure.

Dangling pointers
^^^^^^^^^^^^^^^^^

A **dangling pointer** holds the address of storage whose lifetime has
ended. Dereferencing it is undefined behavior.

.. code-block:: cpp

   int* battery_pct{new int{88}};
   delete battery_pct;
   std::cout << *battery_pct << '\n';   // UB, and it will probably print 88

There are two common ways to create one, and only the first involves the
heap:

.. code-block:: cpp

   // 1. deleting, and then forgetting
   int* battery_pct{new int{88}};
   delete battery_pct;
   // battery_pct dangles from here until it is reassigned or nulled

   // 2. keeping a pointer to something whose scope ended
   int* reading_ptr{nullptr};
   {
       int reading{5};
       reading_ptr = &reading;
       std::cout << *reading_ptr << '\n';   // fine: reading is alive
   }                                        // reading dies here
   std::cout << *reading_ptr << '\n';       // UB: reading_ptr dangles

.. tip::

   **The habit that costs nothing:** write ``delete p;`` and then
   ``p = nullptr;``, always, in that order, on the same pair of lines. It
   turns a silent problem that shows up much later into an immediate,
   obvious crash, and it
   makes a second ``delete`` harmless.

Memory leaks
^^^^^^^^^^^^

A **memory leak** is allocated storage that nothing points at any more.
It is not freed, and it cannot be freed.

.. code-block:: cpp

   for (int i{0}; i < 100000; ++i) {
       int* reading{new int{i}};   // allocated on every iteration
   }                               // the pointer dies at the end of each
                                   // iteration; the int it pointed at does not

A short-lived program "gets away with" leaks, because the operating
system reclaims every page when the process exits. That is not a reason
to allow them:

.. important::

   A robot's control node is not a short-lived program. It runs for
   hours, and a leak of a few hundred bytes per sensor callback at 30 Hz
   is a process that grows by a gigabyte a day and then gets killed in
   the middle of an experiment. Fix leaks even when the program appears
   fine, and especially when the code is going to be reused.

Double delete
^^^^^^^^^^^^^

Freeing the same block twice is undefined behavior. It takes two
pointers and one honest mistake:

.. code-block:: cpp

   int* primary{new int{88}};
   int* backup{primary};   // backup owns nothing, but it looks like it does

   delete primary;
   primary = nullptr;
   delete backup;          // UB: this block was freed a moment ago

.. figure:: /_static/images/l3/png/double_delete.png
   :align: center
   :alt: Two stack boxes, primary and backup, both holding the same heap
      address 0x5591...2b0, with dashed arrows converging on one heap box
      holding 88 that is greyed, dashed and labelled freed. The left arrow
      is labelled delete primary; and marked OK in green; the right is
      labelled delete backup; and marked UB in red. The same block is freed
      twice.

   Two pointers, one block. Nulling ``primary`` does nothing to
   ``backup``.

This one is worth staring at, because the copy on the second line is
completely innocent-looking. **Copying a raw pointer copies the address,
not the ownership**, and nothing in the type system records which of
the two is supposed to call ``delete``.

Null dereference
^^^^^^^^^^^^^^^^

Dereferencing a pointer that holds ``nullptr`` is undefined behavior.
On a normal system it is an immediate segmentation fault:

.. code-block:: cpp

   int* sensor{nullptr};
   std::cout << *sensor << '\n';   // UB

Of the four failures this is the friendly one: it stops the program at
the line that is wrong, rather than corrupting something and failing
later.


Finding These Bugs: Valgrind
============================

You cannot test your way to "there are no dangling pointers": the whole
problem with undefined behavior is that it often produces the output you
expected. You need a tool that watches every allocation.

`Valgrind <https://valgrind.org/>`_ runs your program on a synthetic CPU
and tracks every byte it allocates, frees, and reads. It is already
installed if you followed :doc:`/setup/cpp_setup`; if not:

.. code-block:: bash

   sudo apt install valgrind

Running it
----------

Build the course project in VS Code as usual, then point Valgrind at the
executable CMake produced:

.. code-block:: bash

   valgrind --leak-check=full ./build/project/week3/week3

.. important::

   Build in **Debug**, which is what the course project configures by
   default. A Debug build compiles with ``-g``, and those debug symbols
   are what let Valgrind name a line: without them it can still tell you
   that memory leaked, but not *which line* allocated it.

.. dropdown:: A leak, as Valgrind reports it
    :class-container: sd-border-secondary
    :open:

    .. code-block:: cpp
       :linenos:

       #include <iostream>

       int main() {
           int* battery_pct{new int{88}};
           std::cout << *battery_pct << '\n';
           // forgot: delete battery_pct;
       }

    .. code-block:: text

       ==335924== HEAP SUMMARY:
       ==335924==     in use at exit: 4 bytes in 1 blocks
       ==335924==   total heap usage: 3 allocs, 2 frees, 77,828 bytes allocated
       ==335924==
       ==335924== 4 bytes in 1 blocks are definitely lost in loss record 1 of 1
       ==335924==    at 0x4846FA3: operator new(unsigned long) (...)
       ==335924==    by 0x10919E: main (battery_leak.cpp:4)
       ==335924==
       ==335924== LEAK SUMMARY:
       ==335924==    definitely lost: 4 bytes in 1 blocks
       ==335924==    indirectly lost: 0 bytes in 0 blocks
       ==335924==      possibly lost: 0 bytes in 0 blocks
       ==335924==    still reachable: 0 bytes in 0 blocks
       ==335924== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)

    Read it from the bottom up: one error; 4 bytes **definitely lost**
    (one ``int``); allocated by ``operator new`` at
    ``battery_leak.cpp:4``. That line number is what the debug build
    bought you.

.. dropdown:: A use-after-free, as Valgrind reports it
    :class-container: sd-border-secondary

    .. code-block:: cpp
       :linenos:

       #include <iostream>

       int main() {
           int* battery_pct{new int{88}};
           delete battery_pct;
           std::cout << *battery_pct << '\n';   // UB
       }

    .. code-block:: text

       ==329918== Invalid read of size 4
       ==329918==    at 0x1091E3: main (battery.cpp:6)
       ==329918==  Address 0x4e44080 is 0 bytes inside a block of size 4 free'd
       ==329918==    at 0x484A61D: operator delete(void*, unsigned long) (...)
       ==329918==    by 0x1091DE: main (battery.cpp:5)
       ==329918==  Block was alloc'd at
       ==329918==    at 0x4846FA3: operator new(unsigned long) (...)
       ==329918==    by 0x1091BE: main (battery.cpp:4)
       ==329918== 88

    Valgrind gives you the three lines that matter: where the bad read
    happened (6), where the block was freed (5), and where it was
    allocated (4).

    And note the last line of output: **the program printed 88**. That is the
    value still sitting in those bytes on this run. Without the tool the
    bug is invisible. Run the same binary outside Valgrind and it may
    print 88, print garbage, or crash, depending on what the allocator
    did with the block in the meantime; that is what "undefined" means.

.. list-table:: What the leak categories mean.
   :widths: 28 72
   :header-rows: 1
   :class: compact-table

   * - Category
     - Meaning
   * - **definitely lost**
     - No pointer to the block exists any more. A real leak; fix it.
   * - **indirectly lost**
     - The block was only reachable through a block that is itself lost
       (a leaked node whose children leak with it).
   * - **possibly lost**
     - A pointer to the *interior* of the block still exists. Usually a
       real leak.
   * - **still reachable**
     - Never freed, but a pointer to it still existed at exit. Often a
       long-lived global; not urgent, but not tidy either.

A ``memcheck`` target in CMake
------------------------------

Instead of typing the Valgrind command every time, add a target that runs
it for you. It belongs in the week's own file,
``project/week3/CMakeLists.txt``, directly under the ``add_executable``
line, because everything in it names the ``week3`` target:

.. code-block:: cmake
   :caption: project/week3/CMakeLists.txt
   :emphasize-lines: 1

   add_executable(week3 src/main.cpp)

   find_program(VALGRIND_EXECUTABLE valgrind)

   if(VALGRIND_EXECUTABLE)
       add_custom_target(memcheck
           COMMAND ${VALGRIND_EXECUTABLE}
                   --leak-check=full
                   --show-leak-kinds=all
                   --track-origins=yes
                   --error-exitcode=1
                   $<TARGET_FILE:week3>
           DEPENDS week3
           COMMENT "Running Valgrind on week3"
           VERBATIM)
   endif()

Then, in the **top-level** ``CMakeLists.txt``, uncomment the line that
brings that directory into the build:

.. code-block:: cmake
   :caption: CMakeLists.txt

   add_subdirectory(project/week3)

``memcheck`` then shows up next to ``week3`` in the target list, and you
run it the way you build everything else in this course:

1. Open the Command Palette (``Ctrl + Shift + P``) and run
   *CMake: Set Build Target*, then pick ``memcheck``.
2. Run *CMake: Build*. Valgrind's report appears in the output panel,
   and the build fails if it finds anything, because of
   ``--error-exitcode=1``.
3. Run *CMake: Set Build Target* once more and pick ``week3`` again.
   Until you do, the play button (▶) and the Status Bar are still
   pointed at ``memcheck`` rather than at your program.

.. warning::

   Put the ``memcheck`` block in the **week's** file, not the top-level
   one. ``$<TARGET_FILE:week3>`` and ``DEPENDS week3`` both name a target
   that only exists once ``project/week3`` has been added, so a copy in
   the top-level file fails at configure time whenever
   ``add_subdirectory(project/week3)`` is still commented out:

   .. code-block:: text

      CMake Error at CMakeLists.txt (add_custom_target):
        Error evaluating generator expression:
          $<TARGET_FILE:week3>

   Keeping it in ``project/week3/CMakeLists.txt`` also means the target
   appears exactly when that week is enabled, and each later week can
   have its own without anyone editing the root file.

``--track-origins=yes`` is worth the slowdown: it reports where an
uninitialized value came from, not merely that one was used.
``--error-exitcode=1`` makes the target *fail* when Valgrind finds
something, which is what turns it into a check rather than a suggestion.

.. tip::

   **The faster alternative: sanitizers.** GCC and Clang can instrument
   the program itself, which runs perhaps 2x slower instead of Valgrind's
   20x. Turn them on for one target in ``CMakeLists.txt``. They have to
   be passed to the linker as well as the compiler:

   .. code-block:: cmake

      target_compile_options(week3 PRIVATE -fsanitize=address,undefined)
      target_link_options(week3 PRIVATE -fsanitize=address,undefined)

   Then build and run the target as usual; a sanitized binary reports the
   error itself, with a stack trace, the moment it happens.

   AddressSanitizer catches use-after-free, buffer overruns, and leaks;
   UndefinedBehaviorSanitizer catches signed overflow, bad shifts, and
   null dereference. Use them while developing and keep Valgrind for the
   deeper checks: the two find overlapping, not identical, sets of bugs.
   Do not run a sanitized binary *under* Valgrind, because they instrument the
   same things and will fight.


References
==========

A **reference** is an alias: a second name for an object that already
exists. It is not a pointer, it is not a copy, and it is not an object of
its own.

.. code-block:: cpp

   type& identifier{existing_object};

.. code-block:: cpp

   int altitude_m{120};
   int& alt{altitude_m};          // alt is another name for altitude_m

   alt = 90;
   std::cout << altitude_m << '\n';   // 90, there is only one object here
   altitude_m = 118;
   std::cout << alt << '\n';          // 118

Five properties
---------------

.. card:: 1. A reference must be initialized
    :class-card: sd-border-secondary

    .. code-block:: cpp

       int& alt1;      // error: a reference must bind to something
       int& alt2{};    // error: nothing to bind to

    There is no such thing as an "empty" reference waiting to be
    assigned later. This is the property that makes references safe by
    construction.

.. card:: 2. A reference is an alias, not a copy
    :class-card: sd-border-secondary

    Writing through the reference writes to the object. There is one
    object and two names for it, and neither name is privileged.

.. card:: 3. A reference has no identity of its own
    :class-card: sd-border-secondary

    .. code-block:: cpp

       int altitude_m{120};
       int& alt{altitude_m};
       std::cout << &altitude_m << '\n';   // 0x7ffd…a04
       std::cout << &alt << '\n';          // 0x7ffd…a04, the same address

    ``&alt`` gives the address of ``altitude_m``, because ``alt`` *is*
    ``altitude_m``. There is no way to ask for "the address of the
    reference itself".

.. card:: 4. A reference cannot be reseated
    :class-card: sd-border-secondary

    .. code-block:: cpp

       int altitude_m{120};
       int target_alt_m{80};
       int& alt{altitude_m};

       alt = target_alt_m;                  // assigns the VALUE into altitude_m
       std::cout << altitude_m << '\n';     // 80
       std::cout << target_alt_m << '\n';   // 80, unchanged: alt is still altitude_m

    This is the one that surprises people. ``r = b`` looks like
    rebinding and is not: every operation on ``alt`` is an operation on
    ``altitude_m``, for as long as ``altitude_m`` exists. A reference is
    bound once, at initialization, for life.

.. card:: 5. A reference cannot be null
    :class-card: sd-border-secondary

    There is no ``nullptr`` for references, so a function taking
    ``int&`` need not check for one. "The object might not exist" is not
    a state a reference can represent, which is a reason to choose it
    when that state is not real, and a reason to choose a pointer when
    it is.

.. note::

   "Cannot be null" is not "cannot dangle": a reference bound to an
   object that then dies is just as broken as a dangling pointer, and
   harder to spot, because nothing at the use site looks like a pointer.
   That happens mostly when a reference outlives the scope it was bound
   in, which is :doc:`Lecture 5 </lectures/lecture5/l5_index>`.

What a reference is in memory
-----------------------------

The natural next question is where ``alt`` lives. On the stack, like
``altitude_m``? In a register? The honest answer has two halves, and the
first one is the one to remember.

**The language's answer: a reference is not an object.** The standard
does not say whether a reference takes up any memory. That is left to
the compiler. A reference is a name the compiler puts in place while it
builds your program, and three things follow from that. You can check
all three yourself:

.. table::
   :class: compact-table

   +------------------------------+------------------------+------------------------------------------------------+
   | Given ``int altitude_m{120}; int& alt{altitude_m};``                                                         |
   +------------------------------+------------------------+------------------------------------------------------+
   | Expression                   | Result                 | Because                                              |
   +==============================+========================+======================================================+
   | ``sizeof(alt)``              | ``4``                  | ``sizeof`` on a reference gives the size of the      |
   |                              |                        | **referred-to type**. It never tells you the size of |
   |                              |                        | "the reference".                                     |
   +------------------------------+------------------------+------------------------------------------------------+
   | ``&alt == &altitude_m``      | ``true``               | There is one object, and ``&`` on either name yields |
   |                              |                        | its address.                                         |
   +------------------------------+------------------------+------------------------------------------------------+
   | ``alt = 90;``                | ``altitude_m`` is      | Every operation on the name is an operation on the   |
   |                              | ``90``                 | object.                                              |
   +------------------------------+------------------------+------------------------------------------------------+

Where references are actually used
----------------------------------Where references are actually used
----------------------------------

You will write far more references than pointers, and mostly in two
places:

.. code-block:: cpp

   // 1. function parameters: no copy, and modification is visible to the caller
   void charge(Battery& pack);           // may modify the caller's battery
   void report(const Battery& pack);     // reads it, copies nothing

   // 2. range-based for loops over containers
   for (const auto& reading : altitudes) { /* no copy per element */ }
   for (auto& reading : altitudes) { reading += 1; }   // modifies in place

Both are the subject of later lectures:
:doc:`Lecture 4 </lectures/lecture4/l4_index>` for containers and
:doc:`Lecture 5 </lectures/lecture5/l5_index>` for parameter passing.
The reason is already visible here: ``const Battery&`` passes an
**address**, the same 8 bytes any pointer is, instead of copying the whole
object. Across a function boundary the compiler has to pass *something*,
and what it passes is the address, exactly as the previous section
described. Measured with GCC on a 56-byte ``Battery``: the by-reference
call copies nothing and hands over one register, while the by-value call
emits four instructions to copy all 56 bytes onto the stack. And the
signature says the object will not be modified.


Pointers vs. References
=======================

.. figure:: /_static/images/l3/png/pointer_vs_reference.png
   :align: center
   :alt: Two panels. On the left, int* altitude_ptr{&altitude_m}; draws two
      stack boxes joined by an arrow: altitude_ptr holds 0x7ffd...a04 and
      altitude_m holds 120, noted: two objects, altitude_ptr holds the
      address of altitude_m, and *altitude_ptr reaches it. On the right,
      int& alt{altitude_m}; draws a single stack box holding 120 with two
      names above it, altitude_m and alt, joined to the box by a brace,
      noted: one object with two names, alt is altitude_m, and nothing
      else, for ever.

   A pointer is a second **object**. A reference is a second **name**.
   Every difference in the table below follows from that one.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - 
     - Pointer
     - Reference
   * - **What it is**
     - An object holding an address
     - Another name for an existing object
   * - **Initialization**
     - Optional (and dangerous to skip)
     - Mandatory
   * - **Can be null**
     - Yes, ``nullptr`` is a valid state
     - No
   * - **Can be reseated**
     - Yes, assign a new address
     - No, bound for life
   * - **Syntax at use**
     - ``*ptr`` to read, ``ptr->`` for members
     - Used exactly like the object
   * - **Own address**
     - Yes, ``&p`` is its own address
     - No, ``&r`` is the object's address
   * - **Can own heap memory**
     - Yes (but should not; use a smart pointer)
     - No: it can *refer* to a heap object, but never owns it
   * - **Arithmetic**
     - Yes, once there is a sequence to walk (Lecture 4)
     - No

.. note::

   **Owning** means being responsible for the ``delete``. A reference can
   perfectly well be *bound* to a heap object, and Exercise 3 does exactly
   that with ``int& fused{*imu_reading};``. The pointer is still the owner;
   the reference only gives that object a second name.

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **How to choose**

    1. **Prefer a reference.** It cannot be null, cannot be reseated, and
       needs no ``*``. Fewer states means fewer bugs.
    2. **Use a raw pointer when "nothing" is a real answer**: an
       optional argument, a search that found no match, the end of a
       list.
    3. **Use a raw pointer when an API demands one**: C libraries,
       and some C++ ones, take ``T*``.
    4. **Use a smart pointer to own heap memory.** Never a raw one.

.. admonition:: Exercise 3 (in class): Audit this code.. admonition:: Exercise 3 (in class): Audit this code
   :class: hint

   Eleven lines, several bugs. For each line, say whether it is fine or
   broken, and if broken, name the bug using the vocabulary of this
   lecture.

   .. code-block:: cpp
      :linenos:

      int* imu_reading{new int{10}};
      int* gps_reading{new int{20}};
      int& fused{*imu_reading};

      fused = *gps_reading;
      *gps_reading = 30;
      imu_reading = new int{40};
      delete gps_reading;
      *imu_reading = *gps_reading;
      int* spare{gps_reading};
      fused = 50;
      delete spare;

   .. dropdown:: Answer
      :class-container: sd-border-success

      - **1 and 2**: fine. Two heap ``int``\ s, each with one owner.
      - **3**: legal, and a warning sign. ``fused`` is now an alias for
        the object ``imu_reading`` owns. That object has two names with
        different lifetimes: ``fused`` will still be there after
        ``imu_reading`` stops pointing at it.
      - **5**: fine. ``fused = *gps_reading`` writes ``20`` into the
        first block.
      - **6**: fine. The second block becomes ``30``.
      - **7**: **memory leak**. ``imu_reading`` was the only pointer to
        the first block, and it has just been overwritten. The block is
        unreachable, and ``fused`` is now an alias for an object nobody
        can free.
      - **8**: fine. The second block is freed. Note what this does to
        ``gps_reading``: it dangles from here on.
      - **9**: **dangling read**, and a write to a new block.
        ``*gps_reading`` reads freed storage.
      - **10**: legal, and dangerous. ``spare`` copies an address that
        is already dead. Copying a raw pointer copies the address only,
        not whether it is still good and not who has to free it.
      - **11**: writes ``50`` through ``fused``, into the leaked block
        from line 7. Nothing crashes; the program is simply keeping a
        block alive that it can never release.
      - **12**: **double delete**. ``spare`` holds the address freed at
        line 8.

      Also, at the end of it all, the block allocated on line 7 is
      **leaked**: ``imu_reading`` still points at it, but no
      ``delete imu_reading`` appears.

      The point of the exercise is not the count of bugs. It is that
      every single one is an ownership question that the code does not
      record anywhere: ``int*`` looks identical whether it owns a block,
      observes one, or points at freed storage.


Summary
=======

.. grid:: 1 1 2 2
    :gutter: 3

    .. grid-item-card:: Pointers
        :class-card: sd-border-secondary

        - A pointer is a variable whose value is an address.
        - ``&`` takes an address; ``*`` goes back to the object.
        - Always initialize: ``nullptr``, ``&x``, or ``new``.
        - The type decides how the bytes are read, not how big the
          pointer is. Every pointer is 8 bytes here.
        - ``const int*`` locks the object; ``int* const`` locks the
          arrow. Read right to left.

    .. grid-item-card:: Dynamic memory
        :class-card: sd-border-secondary

        - ``new`` yields the address of an unnamed heap object that you
          now own; ``delete`` returns the storage and nothing else.
        - ``delete`` what you ``new``, exactly once, and ``delete
          nullptr`` is safe.
        - Four failures: leak, dangling, double delete, null
          dereference. All four are ownership mistakes.
        - Check with ``valgrind --leak-check=full``, or with
          ``-fsanitize=address,undefined``.

    .. grid-item-card:: References
        :class-card: sd-border-secondary

        - A reference is a second name for an existing object.
        - It must be initialized, cannot be null, and cannot be
          reseated.
        - ``r = b`` assigns a value; it never rebinds.
        - It can still dangle if the object it names dies first.

    .. grid-item-card:: What to actually write
        :class-card: sd-border-warning

        - Prefer a local variable; then a reference; then ``std::vector``
          or ``std::string``; then a smart pointer.
        - Use a raw pointer to **observe**, or when "nothing" is a valid
          answer. Never to own.
        - If you wrote ``new``, ask what would free it if the next line
          threw.
