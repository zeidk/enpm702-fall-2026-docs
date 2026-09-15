.. _l3-quiz:

====================================================
Quiz
====================================================

This self-check quiz covers :doc:`Lecture 3 <l3_lecture>`.

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

   Which storage duration is the only one whose lifetime *you* are
   responsible for ending?

   A. Static.
   B. Automatic.
   C. Dynamic.
   D. All three; C++ never frees anything on its own.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, dynamic.

   *Explanation:* Static objects live until the program exits and
   automatic objects die at the end of their scope; in both cases the
   compiler emits the code that ends the lifetime. An object created with
   ``new`` has no scope and no name, so nothing will ever free it except
   an explicit ``delete``. That asymmetry is why this lecture has a
   section on what goes wrong.


----


.. admonition:: Question 2
   :class: hint

   What does this declaration create?

   .. code-block:: cpp

      int* c, d;

   A. Two pointers to ``int``.
   B. A pointer to ``int`` (``c``) and a plain ``int`` (``d``).
   C. Two plain ``int`` variables.
   D. A compilation error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, a pointer and a plain ``int``.

   *Explanation:* The ``*`` belongs to the declarator, not to the type,
   so it applies only to ``c``. Writing ``int *c, *d;`` makes both
   pointers. The course style is ``int* c;``, one declaration per line,
   which sidesteps the question entirely.


----


.. admonition:: Question 3
   :class: hint

   Which line produces a pointer that is **not** null?

   A. ``int* p{nullptr};``
   B. ``int* p{};``
   C. ``int* p;``
   D. ``int* p{0};``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``int* p;``.

   *Explanation:* A local pointer with no initializer is a **wild**
   pointer: it holds whatever bit pattern was already in those eight
   bytes. The other three are all null, because empty braces
   zero-initialize and ``0`` converts to a null pointer. Still,
   ``nullptr`` is the one to
   write, because it has its own type and cannot be confused with the
   integer ``0``.


----


.. admonition:: Question 4
   :class: hint

   ``p`` is an ``int*`` that points at ``a``. What is the difference
   between ``p = &b;`` and ``*p = b;``?

   A. Nothing; both make ``p`` point at ``b``.
   B. The first repoints ``p`` at ``b``; the second writes ``b``'s value
      into ``a``.
   C. The first writes ``b``'s value into ``a``; the second repoints
      ``p``.
   D. The second one does not compile.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* ``p = …`` changes the pointer, so the arrow moves.
   ``*p = …`` changes the object at the end of the arrow: the arrow stays
   where it is and ``a`` changes. Nearly every early pointer bug is
   one of these two written where the other was meant.


----


.. admonition:: Question 5
   :class: hint

   After ``const int* p{&x};``, which operation is rejected by the
   compiler?

   A. ``p = &y;``
   B. ``*p = 5;``
   C. ``std::cout << *p;``
   D. ``x = 5;``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``*p = 5;``.

   *Explanation:* ``const int*`` is a *pointer to const*: the object is
   read-only **through this pointer**. The pointer itself is free to move
   (A is fine), reading is fine (C), and ``x`` is not itself ``const``,
   so assigning to it directly is also fine (D). Pointer-to-const
   restricts an access path, not an object.


----


.. admonition:: Question 6
   :class: hint

   Which declaration says "this pointer will always point at the same
   object, but I may change that object"?

   A. ``const int* p{&x};``
   B. ``int* const p{&x};``
   C. ``const int* const p{&x};``
   D. ``int const* p{&x};``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``int* const p{&x};``.

   *Explanation:* Read right to left: "``p`` is a ``const`` pointer to
   an ``int``". The ``const`` after the ``*`` freezes the pointer. A and
   D are the same declaration written two ways, both meaning pointer to
   ``const int``, and C freezes both.


----


.. admonition:: Question 7
   :class: hint

   What does ``delete p;`` do?

   A. Erases the bytes at that address and destroys ``p``.
   B. Returns the storage to the allocator and sets ``p`` to ``nullptr``.
   C. Returns the storage to the allocator, and leaves ``p`` holding the
      same address.
   D. Marks the object for collection when memory runs low.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* ``delete`` releases the storage and does nothing else.
   The bytes usually still hold the old value, ``p`` is an ordinary
   variable that still holds the old address, and nothing is
   automatically nulled. That is exactly the state called *dangling*,
   and it is why ``p = nullptr;`` belongs on the next line.


----


.. admonition:: Question 8
   :class: hint

   Which statement about the object created by ``new int{88}`` is true?

   A. It goes out of scope at the end of the enclosing block.
   B. It has no name, and the address returned by ``new`` is the only
      way to reach it.
   C. It is destroyed when the pointer variable holding its address is
      destroyed.
   D. It is destroyed automatically once nothing points at it any more.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* The object is not a variable: it has no identifier and
   it is in no scope, so nothing can end its lifetime except an explicit
   ``delete``. C describes what happens to the *pointer*, which is an
   ordinary automatic variable; the object it addressed survives it, and
   that is a leak. D describes garbage collection, which C++ does not
   do.


----


.. admonition:: Question 9
   :class: hint

   .. code-block:: cpp

      int* p{new int{42}};
      int* q{p};
      delete p;
      p = nullptr;
      delete q;

   What is the result?

   A. Both deletes succeed; the code is correct.
   B. A memory leak.
   C. Undefined behavior: the block is freed twice.
   D. A compilation error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, a double delete.

   *Explanation:* ``int* q{p};`` copies the **address**, not the
   ownership. Nulling ``p`` does nothing to ``q``, which still holds the
   address of a block that has already been returned. Two raw pointers to
   one block, and no record anywhere of which one is supposed to free
   it, is the shape of this bug.


----


.. admonition:: Question 10
   :class: hint

   A program allocates in a loop and never deletes. What is the most
   accurate description of the consequence?

   A. Nothing: the operating system frees everything at exit.
   B. The program crashes immediately when the heap fills.
   C. The process grows for as long as it runs; a short program may
      finish before it matters, a long-running one will not.
   D. Later allocations fail and return ``nullptr``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* A is true but irrelevant. It is why leaks in a
   five-line program are invisible, not why they are acceptable. The
   process that matters in this course is a robot node running for hours,
   where a small leak per callback becomes gigabytes. (D is wrong for a
   further reason: ``new`` does not return ``nullptr`` on failure, it
   throws ``std::bad_alloc``.)


----


.. admonition:: Question 11
   :class: hint

   Valgrind reports ``12 bytes in 1 blocks are definitely lost``. What
   does *definitely lost* mean?

   A. The program read memory it had already freed.
   B. No pointer to that block existed any more when the program exited.
   C. The block was freed twice.
   D. The block was still in use at exit and a pointer to it still
      existed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* *Definitely lost* is a real leak: the block was never
   freed and nothing pointed at it, so nothing could have freed it.
   D describes *still reachable*, which is usually a long-lived global
   rather than a bug. A use-after-free is reported separately, as an
   ``Invalid read``.


----


.. admonition:: Question 12
   :class: hint

   Which flag makes the line number of the allocation appear in
   Valgrind's report?

   A. ``-O2``
   B. ``-Wall``
   C. ``-g``
   D. ``--leak-check=full``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``-g``.

   *Explanation:* ``-g`` puts debug symbols in the binary, which is what
   lets Valgrind map an address back to ``main (leak.cpp:4)``.
   ``--leak-check=full`` asks for the detailed report, but without ``-g``
   that report has no file or line in it.


----


.. admonition:: Question 13
   :class: hint

   ``char* status`` and ``int* altitude`` both hold the very same
   address. What differs when each one is dereferenced?

   A. Nothing: they hold the same address, so they read the same thing.
   B. ``*status`` reads one byte and interprets it as a character;
      ``*altitude`` reads four bytes and interprets them as an ``int``.
   C. ``*status`` reads four bytes, because every pointer is the same
      size.
   D. Nothing compiles: two pointers of different types may not hold the
      same address.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* The address says *where* to start; the **type** says
   how many bytes to read and how to interpret them. That is the whole
   job of a pointer's type. It is not there to change the pointer's
   size, which is 8 bytes either way.


----


.. admonition:: Question 14
   :class: hint

   ``volt_ptr`` is a ``double*`` holding the address ``0x7ffd…a08``.
   What does ``volt_ptr + 1`` hold?

   A. ``0x7ffd…a09``
   B. ``0x7ffd…a0c``
   C. ``0x7ffd…a10``
   D. Nothing useful; pointer arithmetic is only allowed on arrays.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``0x7ffd…a10``.

   *Explanation:* ``+ 1`` moves by one **object**, not one byte, and the
   object here is a ``double``, so the step is ``sizeof(double)`` = 8
   bytes. A is the answer you would get if the step were one byte, and B
   if it were four, which is what an ``int*`` would do. The pointer's
   type decides the size of the step for exactly the same reason it
   decides how many bytes a dereference reads.


----


.. admonition:: Question 15
   :class: hint

   .. code-block:: cpp

      int altitude_m{120};
      int* alt_ptr{&altitude_m};

   Which of these is well defined?

   A. ``*(alt_ptr + 1)``
   B. ``alt_ptr + 1``, as long as it is never dereferenced
   C. ``alt_ptr + 2``
   D. All three: the compiler accepts every one of them.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* For arithmetic, a lone variable counts as an array of
   one element, which gives exactly two legal positions: the object
   itself, and the **one-past-the-end** position ``alt_ptr + 1``. You may
   form that one and compare with it; you may not read through it, so A
   is undefined. C is undefined even though nothing is dereferenced,
   because the position itself does not exist. D is the trap: the
   compiler does accept all three without a warning, which is why
   undefined behaviour here is found at run time with
   ``-fsanitize=address``, or not at all.


----


.. admonition:: Question 16
   :class: hint

   ``int altitude_m{120};`` on the little-endian machines this course
   targets. Reading its four bytes from the **lowest** address upward,
   what do you see?

   A. ``0111 1000``, then three zero bytes.
   B. Three zero bytes, then ``0111 1000``.
   C. ``0000 1111``, then three zero bytes.
   D. It depends on the compiler rather than the machine.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A.**

   *Explanation:* 120 is ``0111 1000``, which fits in a single byte, so
   the other three bytes of the ``int`` are zero. Little-endian puts the
   **least** significant byte at the **lowest** address, so the non-zero
   byte comes first. B is the big-endian arrangement: the order you would
   write the number on paper, and the one network protocols use. C is
   ``0000 1111``, which is 15, not 120. D is wrong in a way worth
   remembering: byte order is a property of the hardware, and the
   compiler simply follows whatever its target does.


----


.. admonition:: Question 17
   :class: hint

   Which of these is the right tool for owning one object on the heap?

   A. A raw ``int*`` with matching ``new``/``delete``.
   B. ``std::unique_ptr<int>``
   C. ``std::shared_ptr<int>``
   D. A reference.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``std::unique_ptr<int>``.

   *Explanation:* One owner means unique ownership, and the destructor
   frees the object on every path out of the scope, including an
   exception. ``shared_ptr`` is for genuinely shared ownership and costs
   more. A reference cannot own anything. A is what this lecture teaches
   you to recognize, not what it teaches you to write.


----


True or False
=============

.. admonition:: Question 18
   :class: hint

   **True or False:** ``sizeof(double*)`` is larger than
   ``sizeof(char*)``, because a ``double`` is larger than a ``char``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* Every pointer holds an address, so every pointer is the
   same size, 8 bytes on the 64-bit machines this course targets. The
   *type* of a pointer does not change its size; it decides how many
   bytes the **dereference** reads and how to interpret them.


----


.. admonition:: Question 19
   :class: hint

   **True or False:** Calling ``delete`` on a null pointer is undefined
   behavior.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* ``delete nullptr`` is guaranteed to do nothing. This is
   why ``p = nullptr;`` after a ``delete`` is worth the line: a second
   ``delete p;`` then becomes harmless instead of undefined. It also
   means ``if (p) { delete p; }`` is redundant.


----


.. admonition:: Question 20
   :class: hint

   **True or False:** A memory leak is what happens when you free memory
   but forget to set the pointer to ``nullptr``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* That is a **dangling pointer**: the memory was freed,
   but the pointer still holds its address. A **leak** is the opposite
   failure: the memory was never freed and no pointer to it remains, so
   it cannot be freed now.


----


.. admonition:: Question 21
   :class: hint

   **True or False:** Given ``int& r{a};``, the statement ``r = b;``
   makes ``r`` refer to ``b``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* A reference cannot be reseated. ``r`` is another name
   for ``a`` for as long as ``a`` lives, so ``r = b;`` assigns the value
   of ``b`` into ``a``. This is the property that makes references
   predictable, and the one that most often surprises people coming from
   pointers.


----


.. admonition:: Question 22
   :class: hint

   **True or False:** A reference cannot be null, so a reference can
   never be invalid.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* A reference cannot be null, but it can **dangle**: if
   the object it names dies first, say a local returned by reference or
   an element of a ``std::vector`` that has since reallocated, then every
   use of the reference is undefined behavior. It is harder to spot than a
   dangling pointer, because nothing at the use site looks like a
   pointer.


----


.. admonition:: Question 23
   :class: hint

   **True or False:** Because ``&r`` and ``&a`` print the same address
   for ``int& r{a};``, a reference must occupy no memory of its own.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* ``&r`` gives the address of ``a`` because ``r`` *is*
   ``a``. There is no way to ask for "the address of the reference".
   That tells you nothing about the implementation: whether a reference
   occupies storage is unspecified, and a compiler commonly implements
   one as a ``const`` pointer when it has to. The language model to keep
   is that a reference is a **name**.

.. admonition:: Question 24
   :class: hint

   A pointer prints as ``0x7ffd…a28``. Another prints as ``0x7ffd…a30``.
   How many bytes apart are the two addresses?

   a) 2
   b) 8
   c) 12
   d) 30

.. dropdown:: Answer
   :class-container: sd-border-success

   **b) 8**

   *Explanation:* Addresses print in **hexadecimal**, so the digits are
   base 16, not base 10. ``0x28`` is :math:`2 \times 16 + 8 = 40`;
   ``0x30`` is :math:`3 \times 16 = 48`. The difference is 8. Reading
   ``28`` and ``30`` as decimal is what makes this look like 2, and it
   is the single most common mistake when reading a debugger.

.. admonition:: Question 25
   :class: hint

   **True or False:** ``typeid(&altitude_m).name()`` and
   ``typeid(altitude_ptr).name()`` print the same thing for
   ``int altitude_m{120}; int* altitude_ptr{&altitude_m};``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   *Explanation:* ``&altitude_m`` does not produce "an address" in some
   generic sense. It produces an ``int*``, which is exactly the type of
   ``altitude_ptr``, and that is why the initialization compiles. Both
   print the mangled name ``Pi`` under GCC; pipe the program through
   ``c++filt -t`` to see ``int*``.

.. admonition:: Question 26
   :class: hint

   You build with VS Code's ``Release`` variant and run Valgrind. It
   reports that 4 bytes are definitely lost, but names no line number.
   Why?

   a) Valgrind cannot detect leaks in optimized builds
   b) ``Release`` adds ``-O3 -DNDEBUG`` and no ``-g``, so there are no
      debug symbols to map the address back to a line
   c) The leak is in the standard library, which has no source
   d) Valgrind needs ``--track-origins=yes`` to report line numbers

.. dropdown:: Answer
   :class-container: sd-border-success

   **b) ``Release`` adds ``-O3 -DNDEBUG`` and no ``-g``**

   *Explanation:* Valgrind still sees the allocation, because it watches
   the allocator rather than the source. What it has lost is the
   **debug information** that maps a machine address back to a file and
   line. ``-g`` is what supplies that, which is why this course builds
   ``Debug``. ``RelWithDebInfo`` (``-O2 -g -DNDEBUG``) gets the line
   numbers back while keeping optimization.

.. admonition:: Question 27
   :class: hint

   **True or False:** Leaving ``CMAKE_BUILD_TYPE`` unset is a safe
   default, because CMake then picks a sensible one for you.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* VS Code calls this ``Unspecified`` and describes it as
   "let CMake pick the default build type", which sounds reassuring.
   What CMake actually adds is **nothing**: no ``-O`` and no ``-g``. You
   get a program that is neither fast nor debuggable, which is the one
   combination with no advantage. Set the build type, or set a default
   in ``CMakeLists.txt`` with
   ``if(NOT CMAKE_BUILD_TYPE) set(CMAKE_BUILD_TYPE Debug ...)``.
