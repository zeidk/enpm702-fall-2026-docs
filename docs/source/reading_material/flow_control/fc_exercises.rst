====================================================
C++ Exercises
====================================================


.. note::

   **Not graded, and not submitted on Canvas.** These exercises belong to
   a self-study reading module: work them at your own pace. Only the
   assignments listed on Canvas are collected.

.. dropdown:: Exercise 1: If/Else Basics
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that reads a robot sensor reading (an integer) from
   the user and categorizes it as follows:

   - If the reading is less than 0, print ``"Error: negative reading"``
   - If the reading is between 0 and 50 (inclusive), print ``"Low"``
   - If the reading is between 51 and 200 (inclusive), print ``"Normal"``
   - If the reading is greater than 200, print ``"High"``

.. dropdown:: Exercise 2: Switch Statement
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that reads a single character representing a robot
   command and uses a ``switch`` statement to print the corresponding
   action:

   - ``'f'``, ``"Moving forward"``
   - ``'b'``, ``"Moving backward"``
   - ``'l'``, ``"Turning left"``
   - ``'r'``, ``"Turning right"``
   - ``'s'``, ``"Stopping"``
   - Any other character, ``"Unknown command"``

   Accept both uppercase and lowercase letters (e.g., ``'f'`` and ``'F'``
   should both print ``"Moving forward"``).

.. dropdown:: Exercise 3: For Loop
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   A robot has 8 distance sensors. The readings (in centimeters) are
   stored in an array:

   .. code-block:: cpp

      int readings[]{12, 45, 7, 89, 34, 56, 3, 22};

   Write a program that uses a ``for`` loop to:

   1. Calculate the sum of all sensor readings.
   2. Find the minimum reading and its index.
   3. Print the sum, the minimum value, and its index.

.. dropdown:: Exercise 4: While and Do-While
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write two small programs that ask the user to enter a valid motor
   speed (an integer between 0 and 100 inclusive).

   **Part A**, Use a ``while`` loop. If the initial input is valid, the
   loop should not execute at all.

   **Part B**, Use a ``do-while`` loop. The prompt should always appear
   at least once.

   For both parts, once a valid speed is entered, print
   ``"Motor speed set to: <speed>"``.

.. dropdown:: Exercise 5: Nested Loops
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write a program that uses nested ``for`` loops to print the following
   right-triangle pattern. The user enters the number of rows.

   Example output for 5 rows:

   .. code-block:: text

      *
      **
      ***
      ****
      *****

.. dropdown:: Exercise 6 Challenge: Menu-Driven Robot Controller
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Build a simple menu-driven robot controller that combines ``switch``,
   loops, and input validation. The program should:

   1. Display a menu with options:

      - ``1) Move forward``
      - ``2) Move backward``
      - ``3) Turn left``
      - ``4) Turn right``
      - ``5) Set speed``
      - ``6) Quit``

   2. Use a ``do-while`` loop to keep the menu running until the user
      selects ``6) Quit``.
   3. Use a ``switch`` statement to handle each menu option.
   4. For ``5) Set speed``, use input validation (``while`` loop) to
      ensure the speed is between 0 and 100.
   5. After each action, print the current robot state (direction and
      speed).
