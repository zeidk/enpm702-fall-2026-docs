.. _l4-quiz:

====================================================
Quiz
====================================================

This self-check quiz covers :doc:`Lecture 4 <l4_lecture>`.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - True/False questions ask whether the statement is correct as
     written.
   - Answer first, then open the dropdown. Reading the answer before
     committing to one teaches you nothing.
   - Every number in the answers was measured on the course machine,
     GCC 13 with libstdc++. Where the standard leaves a choice to the
     implementation, the answer says so.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   ``std::size_t n{3};`` and then ``n - 5``. What is the value of that
   expression?

   A. ``-2``.
   B. ``0``, because unsigned arithmetic stops at zero.
   C. A very large positive number, ``18446744073709551614``.
   D. It does not compile: you cannot subtract past zero.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* ``std::size_t`` is unsigned, so it has no negative
   values at all. Subtracting past zero wraps to the top of the range.
   That is why ``for (std::size_t i{n - 1}; i >= 0; --i)`` never ends:
   ``i >= 0`` is true for every unsigned value.


----


.. admonition:: Question 2
   :class: hint

   A loop's body runs ½n² − ½n times for an input of size *n*. Which of
   these is its time complexity, and why?

   A. O(½n²), because the constant is part of the count.
   B. O(n²), because Big-O keeps the fastest-growing term and drops
      constant factors and lower terms.
   C. O(n), because the −½n term cancels most of the growth.
   D. O(n²) at n = 1000 and O(n) for smaller inputs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* Time complexity names the shape of the growth, not a
   count. ½n² − ½n, ½n², n² and 3n² + 7 all quadruple when *n* doubles,
   and that shared shape is what O(n²) means. The check is to double *n*
   and look at the ratio: 4 for O(n²), 2 for O(n), about 1 for O(log n).


----


.. admonition:: Question 3
   :class: hint

   Which loop is O(n²)?

   A. ``for (int i{0}; i < n; ++i) stmt;``
   B. ``for (int i{0}; i < n; ++i) { stmt; stmt; }``
   C. ``for (int i{0}; i < n; ++i) for (int j{0}; j < i; ++j) stmt;``
   D. ``for (int i{0}; i < n; ++i) for (int j{0}; j < 3; ++j) stmt;``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* Count how many times ``stmt`` runs. A runs it *n*
   times, B 2n times and D 3n times; the constants 2 and 3 are dropped,
   so all three are O(n). C runs it 0 + 1 + ... + (n − 1) = ½n² − ½n
   times. Doubling *n* from 1000 to 2000 takes the count from 499,500 to
   1,999,000, four times as many, which is the O(n²) signature.


----


.. admonition:: Question 4
   :class: hint

   ``std::array<int, 6> joint_deg;`` and ``int joint_deg[6];`` are
   compared on the slides. Which statement is true?

   A. The ``std::array`` takes more bytes, because it stores its size.
   B. Both take 24 bytes; the ``std::array`` adds member functions and
      nothing else.
   C. The C array is smaller because it has no ``size()`` field to
      store.
   D. The ``std::array`` stores its elements on the heap.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* ``std::array`` is a class template wrapping the same
   ``int[6]``: six ``int`` values, four bytes each, side by side, with
   no header, no pointer and no size field. The size lives in the
   *type*, ``std::array<int, 6>``, which costs no bytes at all. The
   members are what the C array cannot have, because a built-in type has
   nowhere to hang a function.


----


.. admonition:: Question 5
   :class: hint

   .. code-block:: cpp

      void report(int joint_deg[6]) {
          std::cout << sizeof(joint_deg) / sizeof(joint_deg[0]);
      }

   On the course machine, what does ``report`` print, and why?

   A. ``6``, because the parameter says ``[6]``.
   B. ``2``, because the parameter decayed to ``int*``, and 8 bytes of
      pointer divided by 4 bytes of ``int`` is 2.
   C. ``24``, the size of the array in bytes.
   D. It does not compile: ``sizeof`` cannot be applied to a parameter.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* The ``[6]`` in a parameter list is decoration. The
   compiler reads the parameter as ``int*`` and never checks the number.
   ``sizeof`` of a pointer is 8 on this machine, so the division gives 2
   instead of 6. GCC warns under ``-Wall``, but only for this one
   spelling; write ``int* joint_deg`` and the warning goes away while the
   bug stays.


----


.. admonition:: Question 6
   :class: hint

   Which of these asks for an array's length and **refuses to compile**
   once the array has decayed to a pointer, rather than giving a wrong
   number?

   A. ``sizeof(a) / sizeof(a[0])``
   B. ``std::size(a)``
   C. ``a.length``
   D. ``strlen(a)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* ``std::size``, from ``<iterator>``, has no overload for
   a pointer: ``no matching function for call to 'size(int*&)'``. A
   compile error is much better than a wrong number, which is what A
   gives after decay. C is not C++, and D only walks to a ``'\0'``.


----


.. admonition:: Question 7
   :class: hint

   ``int grid[3][4]{};`` is stored in row-major order. Which element of
   the flat block does ``grid[2][1]`` occupy?

   A. Element 3.
   B. Element 6.
   C. Element 9.
   D. Element 21.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* Rows are stored one after another, so ``grid[i][j]``
   sits at i × cols + j with cols = 4: 2 × 4 + 1 = 9. That 4 is the
   column count, not ``sizeof(int)``, which happens to be 4 as well.


----


.. admonition:: Question 8
   :class: hint

   The slides measured a 4000 × 4000 grid at 1.8 ms with one loop order
   and 19 ms with the other. Which order is the fast one, and what makes
   it fast?

   A. Column index in the outer loop, row index inside: each step lands
      on the next value in memory.
   B. Row index in the outer loop, column index inside: each step lands
      on the next value in memory.
   C. Either order: the compiler reorders the loops.
   D. Row index inside: it keeps the loop counter small.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* The last index belongs in the inner loop. With rows
   outside and columns inside, the visit order matches the row-major
   layout, so every step lands on the next ``int`` in memory. Swap the
   loops and every read jumps a whole row ahead. The rule follows from
   row-major order and nothing else.


----


.. admonition:: Question 9
   :class: hint

   .. code-block:: cpp

      std::array<int, 6> joint_deg{10, 20, 30, 40, 50, 60};
      auto first{joint_deg.begin()};
      auto last{joint_deg.end()};

   What does ``last - first`` evaluate to, and what does ``*last`` do?

   A. 5, and ``*last`` reads 60.
   B. 6, and ``*last`` reads 60.
   C. 6, and ``*last`` is undefined behaviour.
   D. 7, and ``*last`` reads the terminator.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* The range is half-open, [begin, end): ``end()`` is
   the position one past the last element, so the difference is the
   length, 6, with no plus or minus one. ``end()`` is a position, not an
   element. Dereferencing it is undefined behaviour, exactly like
   dereferencing a one-past-the-end pointer in Lecture 3.


----


.. admonition:: Question 10
   :class: hint

   ``std::vector<int> b(3, 7);`` and ``std::vector<int> c{3, 7};``
   differ by one character. What do they hold?

   A. Both hold ``7 7 7``.
   B. Both hold ``3 7``.
   C. ``b`` holds ``7 7 7`` and ``c`` holds ``3 7``.
   D. ``b`` holds ``3 7`` and ``c`` holds ``7 7 7``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* If the braces can be read as a list of elements, they
   will be, so ``c{3, 7}`` is two elements. Parentheses are the only way
   to say count first, then value: ``b(3, 7)`` is three copies of 7.
   This is the documented exception to Lecture 2's braces-everywhere
   rule.


----


.. admonition:: Question 11
   :class: hint

   An empty ``std::vector<int>`` receives six ``push_back`` calls. On
   the course machine, at which pushes does a reallocation happen?

   A. At every push.
   B. At pushes 0, 1, 2 and 4.
   C. At pushes 0, 2 and 4.
   D. Only at push 0, when the block is first allocated.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* Capacity runs 0, 1, 2, 4, 4, 8, 8. The block is
   replaced whenever ``size() == capacity()`` and another element
   arrives: at pushes 0, 1, 2 and 4. Pushes 3 and 5 go into spare room.
   The exact numbers belong to libstdc++; what the standard promises is
   that growth is geometric.


----


.. admonition:: Question 12
   :class: hint

   Why does ``push_back`` count as **amortized** O(1) when a single
   reallocation moves every element and costs O(n)?

   A. Because reallocation is done by the operating system, not the
      program.
   B. Because capacity grows by a factor, so reallocations get rarer as
      the vector grows and their total cost, spread over all the pushes,
      is a constant per push.
   C. Because the moved elements are never more than 16.
   D. Because the standard forbids reallocation more than once per
      vector.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* One million pushes cost 21 reallocations rather than a
   million. *n* pushes move about 2n elements in total, so each push
   pays for about two moves on average, whatever *n* is. "Amortized"
   names exactly that averaging over a long run.


----


.. admonition:: Question 13
   :class: hint

   .. code-block:: cpp

      std::vector<int> ranges_m{10, 20, 30};
      int* first{&ranges_m[0]};
      ranges_m.push_back(40);
      std::cout << *first;

   What does AddressSanitizer report for the last line, and why?

   A. Nothing: ``first`` still points at 10.
   B. ``stack-buffer-overflow``: the vector lives on the stack.
   C. ``heap-use-after-free``: the push reallocated, the old block was
      freed, and ``first`` still holds its address.
   D. A leak: the old block was never freed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* Size was equal to capacity, so the fourth push
   allocated a bigger block, moved the three elements, and freed the old
   one. ``first`` still holds the old address. This is Lecture 3's
   dangling pointer in code with no ``new`` and no ``delete``: the
   container saves you from calling ``delete``, not from knowing when
   the storage moves. ``reserve(4)`` before the push would have
   prevented it.


----


.. admonition:: Question 14
   :class: hint

   .. code-block:: cpp

      auto name{"John Doe"};

   What is the type of ``name``, and where are the eight characters?

   A. ``std::string``, on the heap.
   B. ``char[9]``, on the stack.
   C. ``const char*`` on the stack, pointing at characters in the
      read-only ``.rodata`` segment.
   D. ``const char*`` on the stack, pointing at characters on the heap.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* ``"John Doe"`` is a ``const char[9]`` with static
   storage in ``.rodata``, next to the code. Handed to ``auto`` it
   decays, so ``name`` is a pointer and nothing more, and ``typeid``
   prints ``PKc``, which ``c++filt`` reads as ``char const*``. The
   characters are ``const``: ``name = "Jane Doe"`` repoints the pointer
   and leaves ``"John Doe"`` untouched, and ``name[0] = 'j'`` does not
   compile.


----


.. admonition:: Question 15
   :class: hint

   ``topic.find("imu")`` on a string that does not contain ``imu``
   returns ``std::string::npos``. What is ``npos``?

   A. ``-1``.
   B. ``0``.
   C. The largest possible ``std::size_t``, 18446744073709551615.
   D. A null pointer.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* ``npos`` is not a special marker. It is the largest
   value ``std::size_t`` can hold, which is why using a "not found"
   result as an index is a disaster and why it will not show up as −1 in
   a debugger. Always compare against ``npos``. A result of 0 means
   "found at the start", but as a bool it reads ``false``.


----


.. admonition:: Question 16
   :class: hint

   .. code-block:: cpp

      std::map<std::string, double> sensors{{"lidar", 0.25}, {"imu", 0.01}};
      double period{sensors["camera"]};

   After this, what is ``sensors.size()``?

   A. 2: reading a missing key returns 0 and changes nothing.
   B. 2: the line throws ``std::out_of_range``.
   C. 3: ``operator[]`` inserted ``{"camera", 0.0}``.
   D. It does not compile: ``camera`` is not in the map.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C.**

   *Explanation:* Given a missing key, ``operator[]`` builds a default
   value, inserts it, and hands you a reference to it. A read made the
   map bigger. To read without inserting use ``at()``, which throws on a
   missing key; to ask whether a key is there use ``contains()`` or
   ``find()``. None of those three insert anything.


----


.. admonition:: Question 17
   :class: hint

   A calibration table is looked up by sensor name and, at shutdown,
   printed sorted by name. Which container fits best?

   A. ``std::vector<double>``, indexed by a sensor number.
   B. ``std::map<std::string, double>``: keyed lookup, and the sorted
      order comes free.
   C. ``std::unordered_map<std::string, double>``: keyed lookup is
      faster on average.
   D. ``std::array<double, 6>``: the number of sensors is fixed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* The handle is a key, which rules out A and D. Between
   the two maps, ``std::map`` keeps its keys in sorted order, so the
   report needs no sorting step. Without the report, C would be the
   default, since hashed lookup is O(1) on average against O(log n).


----


.. admonition:: Question 18
   :class: hint

   .. code-block:: cpp

      std::vector<double> ranges_m{2.31, 0.42, 5.00, 0.18, 1.75};
      std::accumulate(ranges_m.begin(), ranges_m.end(), 0);

   What does this return?

   A. ``9.66``.
   B. ``8``.
   C. ``9``.
   D. It does not compile: the seed must be a ``double``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B.**

   *Explanation:* The seed's type becomes the accumulator's type. ``0``
   is an ``int``, so every addition is truncated to an ``int`` as it
   goes: 2, 2, 7, 7, 8. Write ``0.0`` and the answer is 9.66. Both
   compile without a warning, and ``std::accumulate`` lives in
   ``<numeric>``, not ``<algorithm>``.


----


True or False
=============

.. admonition:: Question 19
   :class: hint

   ``std::array`` never decays to a pointer, so passing one to a function
   by value keeps its length in the type.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   *Explanation:* The length is a template argument, part of the type
   ``std::array<int, 6>``, and no expression turns a class object into a
   pointer. To get a pointer you ask for one with ``data()``.


----


.. admonition:: Question 20
   :class: hint

   After ``v.clear()`` on a vector with capacity 16, ``v.capacity()`` is
   0.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* ``clear()`` sets the size to 0 and leaves the capacity
   alone. Verified: 10/16 becomes 0/16. It destroys the elements, not
   the block. To give the memory back, follow it with
   ``shrink_to_fit()``, which is a non-binding request that libstdc++
   honours.


----


.. admonition:: Question 21
   :class: hint

   ``shrink_to_fit()`` can release spare capacity without moving any
   element, because it only changes the capacity pointer.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* The allocator has no way to give back the tail of a
   block, so a smaller block means a new block: allocate, move every
   element, free the old one. That is a reallocation, and it invalidates
   every iterator, pointer and reference, exactly like growth does.


----


.. admonition:: Question 22
   :class: hint

   ``std::vector<std::vector<int>>`` with three rows stores all twelve
   cells in one contiguous block, the same as ``int grid[3][4]``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* The outer vector owns one block of three vector
   objects, and each of those owns its own block of four ``int``. That is
   four allocations, and the row blocks need not be adjacent; on the
   course machine row 1 started 8 ints after row 0, not 4. For a real map
   or costmap use one flat vector and index with ``i * cols + j``.


----


.. admonition:: Question 23
   :class: hint

   ``sensors.insert({"imu", 99.0})`` on a map that already holds the key
   ``imu`` overwrites the old value with 99.0.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* ``insert`` and ``emplace`` never overwrite. Given an
   existing key they return without changing anything, and the value you
   wanted to store is thrown away; the ``bool`` they return says so. To
   overwrite, use ``insert_or_assign`` or ``sensors["imu"] = 99.0``.


----


.. admonition:: Question 24
   :class: hint

   A ``std::string_view`` owns no characters, so returning one from a
   function that built a local ``std::string`` produces a dangling view.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   *Explanation:* A view is a pointer and a length over someone else's
   characters. The local string dies at the closing brace, and the view
   outlives it: that is Lecture 3's dangling pointer with a length
   attached. Store the ``std::string``, pass the ``std::string_view``,
   never store or return a view.


----


.. admonition:: Question 25
   :class: hint

   Every algorithm in ``<algorithm>`` takes a container as its argument.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   *Explanation:* They take a pair of iterators marking a half-open
   range, which is why one ``std::sort`` serves a vector, a string and a
   C array, and why you can sort only the first ten elements by passing
   ``v.begin()`` and ``v.begin() + 10``. The C++20 ``std::ranges::``
   versions accept the container directly, but the two-iterator form is
   the one every codebase uses.
