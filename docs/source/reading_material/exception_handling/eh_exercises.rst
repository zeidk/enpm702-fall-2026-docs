====================================================
C++ Exercises
====================================================


.. note::

   **Not graded, and not submitted on Canvas.** These exercises belong to
   a self-study reading module: work them at your own pace. Only the
   assignments listed on Canvas are collected.

.. dropdown:: Exercise 1: Basic Try-Catch
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that creates a ``std::vector<int>`` with 5 elements
   and attempts to access an out-of-bounds index using ``.at()``. Catch
   the resulting ``std::out_of_range`` exception and print the error
   message from ``what()``.

   Expected output (approximately):

   .. code-block:: text

      Caught out_of_range: vector::_M_range_check: __n (which is 10) >= this->size() (which is 5)

.. dropdown:: Exercise 2: Throwing Exceptions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a function ``validate_speed(double speed)`` that checks whether
   a robot's speed is valid. The function should:

   - Throw ``std::invalid_argument`` if ``speed`` is negative.
   - Throw ``std::out_of_range`` if ``speed`` exceeds 10.0 (the
     maximum allowed speed).
   - Print ``"Speed OK: <speed>"`` if the speed is valid.

   In ``main()``, call ``validate_speed`` with values ``5.0``, ``-1.0``,
   and ``15.0``, catching and printing each exception.

.. dropdown:: Exercise 3: Multiple Catch Blocks
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a function ``process_command(int code)`` that:

   - Throws ``std::invalid_argument`` if ``code`` is negative.
   - Throws ``std::out_of_range`` if ``code`` is greater than 100.
   - Throws ``std::runtime_error`` if ``code`` equals 42 (a simulated
     hardware fault).
   - Prints ``"Executing command <code>"`` otherwise.

   In ``main()``, test with values ``10``, ``-5``, ``42``, and ``200``.
   Use separate ``catch`` blocks for each exception type, plus a
   catch-all ``catch (...)`` as a safety net.

.. dropdown:: Exercise 4: Custom Exception Class
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create a small exception hierarchy for a robot system:

   1. ``RobotError``, base class inheriting from ``std::runtime_error``.
      Stores a ``robot_id`` (``std::string``).
   2. ``MotorError``, derived from ``RobotError``. Stores which motor
      failed (``std::string motor_name``).
   3. ``SensorError``, derived from ``RobotError``. Stores which
      sensor failed (``std::string sensor_name``).

   Write a function ``run_diagnostics(int test_case)`` that throws
   ``MotorError`` when ``test_case == 1`` and ``SensorError`` when
   ``test_case == 2``. In ``main()``, catch each type separately and
   print the details.

.. dropdown:: Exercise 5: Exception-Safe Resource Management
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write two functions that allocate an ``int`` array and then throw an
   exception:

   1. ``unsafe_allocation()``, Uses ``new`` to allocate an array,
      throws an exception **before** calling ``delete[]``. This leaks
      memory.
   2. ``safe_allocation()``, Uses ``std::unique_ptr`` to manage the
      array. Even when an exception is thrown, the memory is
      automatically released.

   Call both from ``main()`` inside try-catch blocks. Add print
   statements in appropriate places to show when memory is (or is not)
   cleaned up.

.. dropdown:: Exercise 6: Exception-Safe Config Parser (Challenge)
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Write an exception-safe configuration file parser. The parser reads a
   text file containing key-value pairs (one per line, separated by
   ``=``) and stores them in a ``std::map<std::string, std::string>``.

   Requirements:

   1. Create three custom exception classes derived from
      ``std::runtime_error``:

      - ``FileError``, thrown when the file cannot be opened.
      - ``ParseError``, thrown when a line has invalid format (no ``=``
        sign). Store the line number.
      - ``MissingKeyError``, thrown when a required key is not found
        in the config. Store the key name.

   2. Write a function ``parse_config(const std::string& filename)``
      that returns a ``std::map<std::string, std::string>``.

   3. Write a function ``get_required(const std::map<...>& config,
      const std::string& key)`` that throws ``MissingKeyError`` if the
      key is absent.

   4. In ``main()``, parse a config file and retrieve required keys
      ``"robot_name"``, ``"max_speed"``, and ``"sensor_topic"``,
      handling each exception type.
