====================================================
Lecture
====================================================


Validating Input
================

``std::cin >> age`` does not promise you a number. It promises to *try*.
What happens when the user types something else is worth knowing before
you write a program that trusts its input.

There are **three** distinct outcomes, and only one of them is obvious.

.. list-table:: What ``std::cin >> age`` does with each input, for ``int age{42};``
   :widths: 16 12 16 56
   :header-rows: 1
   :class: compact-table

   * - Typed
     - ``age``
     - Stream state
     - What happened
   * - ``42``
     - ``42``
     - good
     - Clean success.
   * - ``abc``
     - ``0``
     - **fail**
     - Extraction **failed**. Since C++11 the variable is set to ``0``,
       so your previous value of ``42`` is **destroyed**. ``abc`` is
       still sitting in the buffer.
   * - ``3.7``
     - ``3``
     - **good**
     - **Partial read.** It stopped at the ``.`` and succeeded with
       ``3``. ``.7`` is still in the buffer.
   * - ``12abc``
     - ``12``
     - **good**
     - Partial read again: ``12`` extracted, ``abc`` left behind.

.. warning::

   The two partial reads leave the stream **good**. Checking whether the
   read "worked" will not catch them — as far as the stream is concerned,
   it did work. And in the failure case the offending text stays in the
   buffer, so the *next* read fails immediately too. A loop that reads
   without clearing spins forever.

Approach 1: check the stream, then recover
------------------------------------------

A stream converts to ``bool``, so ``if (std::cin >> value)`` tests
whether the extraction succeeded. To recover you must do **two** things:
clear the error flags, then throw away the text that caused the problem.

.. code-block:: cpp

   #include <iostream>
   #include <limits>

   int main() {
       int value{};

       std::cout << "Enter an integer: ";
       while (!(std::cin >> value)) {
           std::cin.clear();   // drop the failbit; the stream is usable again
           std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
           std::cout << "That is not an integer. Try again: ";
       }

       std::cout << "Got " << value << '\n';
   }

``clear()`` alone is not enough: without the ``ignore()`` the bad
characters are still queued and the next read fails on them again.
``std::numeric_limits<std::streamsize>::max()`` means "as many
characters as it takes", and the ``'\n'`` says "stop at the end of the
line".

.. note::

   This handles ``abc``. It does **not** reject ``3.7`` or ``12abc``,
   because those succeeded.

Approach 2: read a whole line, then parse it
--------------------------------------------

The robust approach separates the two jobs. Read one whole line with
``std::getline``, then require the **entire** line to parse as a number.
Anything left over means the input was not a number.

.. code-block:: cpp

   #include <charconv>
   #include <iostream>
   #include <string>

   int main() {
       std::cout << "Enter an integer: ";

       std::string line;
       std::getline(std::cin, line);

       int value{};
       const char* first{line.data()};
       const char* last{line.data() + line.size()};
       auto [ptr, ec] = std::from_chars(first, last, value);

       if (ec == std::errc{} && ptr == last) {   // parsed, and consumed it ALL
           std::cout << "Got " << value << '\n';
       } else {
           std::cout << "That was not an integer.\n";
       }
   }

The ``ptr == last`` test is the important half. ``ec == std::errc{}``
only says *some* number was parsed; ``ptr == last`` says nothing was
left over, which is exactly what rejects ``3.7`` and ``12abc``.

.. list-table:: Whole-line parsing, measured.
   :widths: 22 22 56
   :header-rows: 1
   :class: compact-table

   * - Typed
     - Result
     - Why
   * - ``42``
     - accept, ``42``
     - the whole line is a number
   * - ``-5``
     - accept, ``-5``
     - leading sign is fine
   * - ``abc``
     - reject
     - nothing parsed
   * - ``3.7``
     - reject
     - stopped at ``.``, so ``ptr != last``
   * - ``12abc``
     - reject
     - stopped at ``a``, so ``ptr != last``
   * - ``  7``
     - reject
     - ``from_chars`` does **not** skip leading whitespace
   * - (empty line)
     - reject
     - nothing to parse

.. important::

   **Which should you use?**

   - Reach for **Approach 1** when you just need to keep asking until the
     user cooperates, and a value like ``3`` from ``3.7`` is acceptable.
     It is short, and it is what most textbooks show.
   - Reach for **Approach 2** when the input must be *exactly* a number —
     a robot configuration value, a menu choice, anything where silently
     accepting ``3`` for ``3.7`` would be a bug.

   ``std::from_chars`` is the C++17 parser: no exceptions, no locale, and
   it tells you where it stopped. ``std::stoi`` is the older alternative,
   but it throws on failure and ignores trailing junk unless you check
   its ``pos`` output, so it needs more care to use correctly.

.. seealso::

   `cppreference: std::from_chars <https://en.cppreference.com/w/cpp/utility/from_chars>`_,
   `cppreference: std::basic_istream::ignore <https://en.cppreference.com/w/cpp/io/basic_istream/ignore>`_.
