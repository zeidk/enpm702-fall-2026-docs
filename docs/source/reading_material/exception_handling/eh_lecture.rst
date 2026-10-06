====================================================
Lecture
====================================================


.. note::

   **Running the snippets on this page.** Every C++ snippet below is
   collected, commented out, in
   `project/reading_material/src/main.cpp <https://github.com/zeidk/enpm702-fall-2026-cpp/blob/main/project/reading_material/src/main.cpp>`_
   in the course repository. Uncomment one block, build, and run it, then
   comment it back and move on. Blocks are labeled with the section
   heading they come from, so you can read and run side by side.

   The target is not built by default. Uncomment the **last line** of the
   top-level
   `CMakeLists.txt <https://github.com/zeidk/enpm702-fall-2026-cpp/blob/main/CMakeLists.txt>`_:

   .. code-block:: cmake

      add_subdirectory(project/reading_material)

   Then configure and build as usual, and run the ``reading_material``
   target. Every output on this page comes from g++ 13.3 with the course
   flags, ``-std=c++20 -Wall -Wextra -pedantic-errors -Wshadow``.


What Are Exceptions?
====================================================

An **exception** is an object that a function throws to report an error
it cannot handle itself. Throwing it stops the normal flow of the
program: control jumps to the nearest caller that has said it can handle
that kind of error. If no caller can, the program stops.

Some operations of the standard library report errors by throwing:

- ``.at()`` with an index that is out of range throws
  ``std::out_of_range`` (Lecture 4).
- ``new`` throws ``std::bad_alloc`` when memory runs out (Lecture 3).
- ``.value()`` on an empty ``std::optional`` and a call to an empty
  ``std::function`` throw (Lecture 6).

Many common errors do **not** throw:

- Integer division by zero, and ``[]`` with an index out of range, are
  undefined behavior. No exception is thrown and nothing can catch them.
- A file that fails to open, or ``std::cin`` reading a letter where it
  expects a number, sets the stream's fail state, which you check. The
  :doc:`input validation </reading_material/input_validation/iv_index>`
  reading shows how for ``std::cin``.

For errors like these, your own code checks for the error and throws.


``try``, ``catch``, and ``throw``
====================================================

C++ uses three keywords for exception handling:

- ``throw``: raises (throws) an exception.
- ``try``: wraps a block of code that might throw an exception.
- ``catch``: handles the exception if one is thrown.

.. card::
   :class-header: sd-bg-info sd-text-white
   :class-body: sd-bg-light

   Basic Syntax
   ^^^

   .. code-block:: cpp

      try {
          // code that might throw
          throw std::runtime_error{"something went wrong"};
      } catch (const std::runtime_error& e) {
          std::cout << "Error: " << e.what() << '\n';
      }

   Output:

   .. code-block:: text

      Error: something went wrong

Key points:

- ``throw`` creates an exception object and leaves the current block, and
  every enclosing block and function, until it reaches a matching
  ``catch``.
- The ``try`` block marks the region where exceptions might occur.
- The ``catch`` block receives the exception and handles it.
- **Execution flow**: any code after the ``throw`` statement inside the
  ``try`` block is **skipped**. Control transfers directly to the
  matching ``catch`` block.

You can have **multiple catch blocks** to handle different exception
types:

.. code-block:: cpp

   try {
       // code that might throw different exceptions
   } catch (const std::out_of_range& e) {
       std::cout << "Out of range: " << e.what() << '\n';
   } catch (const std::runtime_error& e) {
       std::cout << "Runtime error: " << e.what() << '\n';
   } catch (...) {
       std::cout << "Unknown exception caught\n";
   }

The **catch-all** handler ``catch (...)`` catches any exception type. It
must be the last handler of its ``try`` block: anywhere else, g++ stops
with ``error: '...' handler must be the last handler for its try block``.


Standard Exception Hierarchy
====================================================

All exceptions thrown by the standard library derive from
``std::exception``. It provides the member function ``what()``, which
returns a description of the error as a ``const char*``.

.. list-table:: Standard Exception Classes
   :widths: 30 20 50
   :header-rows: 1
   :class: compact-table

   * - **Class**
     - **Header**
     - **Description**
   * - ``std::exception``
     - ``<exception>``
     - Base class for all standard exceptions. Provides ``what()``.
   * - ``std::runtime_error``
     - ``<stdexcept>``
     - Errors that only show up while the program runs, for example a
       sensor that stops responding.
   * - ``std::logic_error``
     - ``<stdexcept>``
     - Errors in the program's logic, for example a broken
       precondition.
   * - ``std::out_of_range``
     - ``<stdexcept>``
     - Thrown by ``.at()`` when an index is out of range.
   * - ``std::invalid_argument``
     - ``<stdexcept>``
     - Thrown when a function receives an invalid argument.
   * - ``std::bad_alloc``
     - ``<new>``
     - Thrown by ``new`` when memory allocation fails.
   * - ``std::bad_optional_access``
     - ``<optional>``
     - Thrown by ``.value()`` on an empty ``std::optional``.
   * - ``std::bad_function_call``
     - ``<functional>``
     - Thrown by a call to an empty ``std::function``.

The hierarchy (simplified):

.. code-block:: text

   std::exception
   +-- std::logic_error
   |   +-- std::invalid_argument
   |   +-- std::out_of_range
   +-- std::runtime_error
   +-- std::bad_alloc
   +-- std::bad_optional_access
   +-- std::bad_function_call


Exceptions You Have Already Seen
----------------------------------------------------

Lecture 6 showed two programs that stop with a message such as
``terminate called after throwing an instance of 'std::bad_optional_access'``.
Nothing caught the exception, so the program stopped. With a ``try``
block, the same errors are caught and the program goes on:

.. code-block:: cpp

   std::optional<int> idle{};  // empty: no robot found
   try {
       std::cout << idle.value() << '\n';
   } catch (const std::bad_optional_access& e) {
       std::cout << "bad_optional_access: " << e.what() << '\n';
   }

   std::function<void(int)> handler{};  // empty: nothing stored
   try {
       handler(2);
   } catch (const std::bad_function_call& e) {
       std::cout << "bad_function_call: " << e.what() << '\n';
   }

   std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};
   try {
       std::cout << battery_pct.at(4) << '\n';
   } catch (const std::out_of_range& e) {
       std::cout << "out_of_range: " << e.what() << '\n';
   }

Output:

.. code-block:: text

   bad_optional_access: bad optional access
   bad_function_call: bad_function_call
   out_of_range: vector::_M_range_check: __n (which is 4) >= this->size() (which is 4)

The text that ``what()`` returns is chosen by the library, so another
compiler prints different words.


Catching Exceptions
====================================================

Best Practices for Catching
----------------------------------------------------

**Always catch by const reference.** The reference avoids a copy of the
exception object. It also avoids **slicing**: a handler for a base class
that catches by value keeps only the base part of a derived exception.
The ``const`` stops the handler from changing the exception.

.. code-block:: cpp

   catch (const std::exception& e) {  // good: by const reference
       std::cout << e.what() << '\n';
   }

**Catch order matters.** The handlers are tried in order, and the first
one that matches wins. Place more-derived exception types before their
base classes. If you catch ``std::exception`` first, it matches every
standard exception, and the more specific handlers never run. g++ warns
about this case with ``-Wexceptions``.

.. code-block:: cpp

   try {
       std::vector<int> vec{1, 2, 3};
       std::cout << vec.at(10) << '\n';  // throws std::out_of_range
   } catch (const std::out_of_range& e) {
       std::cout << "Out of range: " << e.what() << '\n';
   } catch (const std::exception& e) {
       std::cout << "Exception: " << e.what() << '\n';
   }

Re-throwing Exceptions
----------------------------------------------------

Inside a catch block, you can re-throw the current exception using
``throw;`` (with no argument). This is useful when you want to log an
error but let a higher-level handler deal with it.

.. code-block:: cpp

   try {
       process_data();
   } catch (const std::exception& e) {
       std::cout << "Logging error: " << e.what() << '\n';
       throw;  // re-throw the same exception
   }


Throwing Exceptions
====================================================

You can throw an object of almost any type in C++ (an ``int``, a
``std::string``, a ``struct``), but **best practice is to throw objects
derived from std::exception**. Then every handler can rely on the
``what()`` member function.

.. code-block:: cpp

   #include <iostream>
   #include <stdexcept>

   double divide(double a, double b) {
       if (b == 0.0) {
           throw std::invalid_argument{"division by zero"};
       }
       return a / b;
   }

   int main() {
       try {
           double result{divide(10.0, 0.0)};
           std::cout << "Result: " << result << '\n';
       } catch (const std::invalid_argument& e) {
           std::cout << "Error: " << e.what() << '\n';
       }
   }

Output:

.. code-block:: text

   Error: division by zero

``10.0 / 0.0`` would not throw on its own: for ``double`` it gives
``inf``. ``divide`` checks for the error and throws.

.. admonition:: Guideline
   :class: tip

   Always throw by value and catch by const reference.


Custom Exception Types
====================================================

When the standard exception types do not say enough, you can make your
own. The shortest form is a ``struct`` that builds on
``std::runtime_error``:

.. code-block:: cpp

   #include <iostream>
   #include <stdexcept>
   #include <string>

   struct SensorError : std::runtime_error {
       using std::runtime_error::runtime_error;
   };

- ``: std::runtime_error`` says that a ``SensorError`` **is a**
  ``std::runtime_error``. It has the same ``what()``, and every handler
  for ``std::runtime_error`` or ``std::exception`` catches it.
- ``using std::runtime_error::runtime_error;`` lets you create a
  ``SensorError`` from a message, the same way as a
  ``std::runtime_error``.

This is **inheritance**, which Lectures 8 and 9 cover in full. Here you
only need the two lines above.

Usage:

.. code-block:: cpp

   void read_sensor(const std::string& name, double value) {
       if (value < 0.0) {
           throw SensorError{name + ": negative reading"};
       }
       std::cout << name << ": " << value << '\n';
   }

   int main() {
       try {
           read_sensor("lidar_front", 2.5);
           read_sensor("lidar_rear", -1.5);
       } catch (const SensorError& e) {
           std::cout << "Sensor failure: " << e.what() << '\n';
       }
   }

Output:

.. code-block:: text

   lidar_front: 2.5
   Sensor failure: lidar_rear: negative reading

A handler for ``SensorError`` catches only sensor errors. A handler for
``std::runtime_error`` would catch these and every other runtime error.


``noexcept`` and Exception Safety
====================================================

The ``noexcept`` specifier promises that **no exception leaves** the
function. The compiler does not check the promise. If an exception does
leave a ``noexcept`` function, the program calls ``std::terminate`` and
stops. A ``noexcept`` function may still throw and catch an exception
inside its own body.

.. code-block:: cpp

   int safe_add(int a, int b) noexcept {
       return a + b;
   }

Exception Safety Guarantees
----------------------------------------------------

Library authors describe four levels of exception safety. Each level
promises everything the one below it does.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Guarantee**
     - **Description**
   * - **Nothrow**
     - The function never throws. Destructors and ``swap`` should
       provide this guarantee.
   * - **Strong**
     - If the function throws, the program state is rolled back to the
       state just before the call. ``std::vector::push_back`` gives this
       guarantee.
   * - **Basic**
     - If the function throws, the program is in a valid (but possibly
       changed) state. No resources are leaked.
   * - **None**
     - If the function throws, the program may be in an invalid state:
       resources may leak and objects may be corrupted.

RAII and Exception Safety
----------------------------------------------------

**RAII** (Resource Acquisition Is Initialization) ties a resource to an
object: the object gets the resource when it is created and releases it
when it is destroyed. A ``std::vector`` is an example (Lecture 4): it
frees its heap memory in its destructor. When an exception leaves a
function, the local objects of that function are destroyed on the way
out. This is called **stack unwinding**.

.. code-block:: cpp

   #include <iostream>
   #include <stdexcept>
   #include <vector>

   void process() {
       std::vector<double> readings(1000);  // ( ): 1000 doubles on the heap
       // ... code that might throw ...
       throw std::runtime_error{"something failed"};
   }  // readings is destroyed during unwinding, so its memory is freed

   int main() {
       try {
           process();
       } catch (const std::runtime_error& e) {
           std::cout << "Caught: " << e.what() << '\n';
       }
   }

Output:

.. code-block:: text

   Caught: something failed

Built with ``-fsanitize=address`` (Lecture 3), the same program reports
no leak. With a raw ``new`` in ``process``, the ``delete`` after the
``throw`` would never run, and the memory would leak. Lecture 7 shows
smart pointers, which do for one object what ``std::vector`` does for
many.

.. admonition:: Destructors and Unwinding
   :class: important

   Unwinding happens when some caller **catches** the exception. If
   nothing catches it, g++ calls ``std::terminate`` without running the
   destructors. So a program that relies on RAII still needs a handler,
   at least in ``main``.


When to Use Exceptions
====================================================

**Use exceptions for:**

- Errors that a function cannot handle itself.
- Errors that cross function boundaries (the caller needs to decide how
  to handle them).
- Errors in constructors (Lecture 8): a constructor has no return value
  to report them with.

**Do not use exceptions for:**

- Normal control flow (e.g., ending a loop).
- Expected conditions (e.g., user entering invalid input in a menu).
  Use ``std::optional`` or return codes instead.
- Performance-critical inner loops.

.. admonition:: Performance Note
   :class: note

   With g++ on x86-64, a ``try`` block adds no instructions to the path
   where nothing is thrown. The cost is elsewhere: tables in the program
   file that describe how to unwind, and a slow path when an exception
   is thrown. A throw is much slower than a ``return``, so do not use one
   where a normal return would do.


Best Practices
====================================================

.. admonition:: Do
   :class: tip

   - Throw by value, catch by const reference.
   - Prefer standard exception types (``std::runtime_error``,
     ``std::invalid_argument``, etc.).
   - Use RAII for exception-safe resource management.
   - Provide meaningful error messages in ``what()``.
   - Put a handler in ``main`` for errors nothing else handles.

.. admonition:: Do Not
   :class: warning

   - Never let an exception leave a destructor. Destructors are
     ``noexcept`` by default, so the program calls ``std::terminate``,
     even when no other exception is in flight.
   - Do not use exceptions for normal control flow.
   - Do not catch exceptions you cannot handle. Let them propagate to a
     handler that can.
   - Do not catch by value: it copies the exception, and a base-class
     handler slices a derived one.
