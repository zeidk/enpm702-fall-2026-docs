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

.. dropdown:: Exercise 4: Custom Exception Types
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create a small family of exception types for a robot, each in the short
   form from the reading (``struct ... : base { using base::base; };``):

   1. ``RobotError``: builds on ``std::runtime_error``.
   2. ``MotorError``: builds on ``RobotError``.
   3. ``SensorError``: builds on ``RobotError``.

   Put the robot id and the failed part in the message, for example
   ``"robot 7: left wheel motor stalled"``.

   Write a function ``run_diagnostics(int test_case)`` that throws
   ``MotorError`` when ``test_case == 1`` and ``SensorError`` when
   ``test_case == 2``. In ``main()``, call it with ``1`` and ``2``, and
   catch ``MotorError``, ``SensorError`` and ``RobotError`` in separate
   handlers. Which order must the three handlers be in, and why?

.. dropdown:: Exercise 5: Exception-Safe Resource Management
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write two functions that allocate 100 ``int`` values and then throw an
   exception:

   1. ``unsafe_allocation()``: uses ``new int[100]``, then throws
      **before** the ``delete[]``. This leaks memory.
   2. ``safe_allocation()``: uses a ``std::vector<int>`` of 100 elements,
      then throws. The vector is destroyed during unwinding, so its memory
      is released.

   Call both from ``main()``, each inside its own ``try``/``catch``.
   Build with ``-fsanitize=address`` (Lecture 3) and run the program.
   AddressSanitizer reports the leak, and names the function and line of
   the ``new``:

   .. code-block:: text

      Direct leak of 400 byte(s) in 1 object(s) allocated from:

   There is no report for ``safe_allocation``.

.. dropdown:: Exercise 6: Exception-Safe Config Parser (Challenge)
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Write an exception-safe configuration parser. It reads the lines of a
   configuration, given as a ``std::vector<std::string>``. Each line holds
   a key and a value separated by ``=``. The parser stores them in a
   ``std::map<std::string, std::string>``.

   Requirements:

   1. Create two exception types in the short form, each building on
      ``std::runtime_error``:

      - ``ParseError``: thrown when a line has no ``=`` sign. Put the line
        number, counted from 1, in the message.
      - ``MissingKeyError``: thrown when a required key is not found in
        the configuration. Put the key name in the message.

   2. Write a function
      ``parse_config(const std::vector<std::string>& lines)`` that returns
      a ``std::map<std::string, std::string>``. Skip blank lines.

   3. Write a function ``get_required(const std::map<std::string,
      std::string>& config, const std::string& key)`` that returns the
      value, and throws ``MissingKeyError`` if the key is absent. Look the
      key up without adding it to the map.

   4. In ``main()``, parse this configuration and retrieve the required
      keys ``"robot_name"``, ``"max_speed"`` and ``"sensor_topic"``,
      handling each exception type:

      .. code-block:: cpp

         std::vector<std::string> lines{"robot_name=scout", "",
                                        "max_speed=1.5"};

      Then add a line ``"sensor_topic"`` with no ``=``, and run it again.
