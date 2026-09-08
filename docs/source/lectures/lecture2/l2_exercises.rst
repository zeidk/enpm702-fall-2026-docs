====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in
:doc:`Lecture 2 <l2_lecture>`.

**Part A** is a set of short prediction and repair drills taken from the
lecture. Work them out **on paper first**, then compile them to check.
Predicting before compiling is the point of the exercise; the compiler
will happily tell you the answer, but it will not tell you why you were
wrong.

**Part B** is programming work. Write, compile, and run each program.

.. note::

   Compile every program with warnings enabled:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -Wpedantic -g program.cpp -o program


----


Part A: Predict and Fix
========================


.. dropdown:: A1: Valid Identifiers
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Which of these names are **legal** C++ identifiers? For the legal
    ones, which follow the course convention (``snake_case``)?

    .. code-block:: text

       my_variable        2ndPlace         _internal        user-name
       MAX_SIZE           class            numberOfStudents PI_VALUE

----


.. dropdown:: A2: Declarations and Initializations
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Predict the output of this program. If it does not compile, say
    which line is at fault and why.

    .. code-block:: cpp
       :linenos:

       int a;
       int b = 3.2;
       int c(1.3);
       int d{3.5};
       std::cout << a << '\n';
       std::cout << b << '\n';
       std::cout << c << '\n';
       std::cout << d << '\n';

----


.. dropdown:: A3: Arithmetic Conversions I
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Predict the type and the value printed.

    .. code-block:: cpp

       #include <iostream>
       #include <typeinfo>

       int main() {
           int a{3};
           int b{2};
           std::cout << "Type of result: " << typeid(a / b).name() << '\n';
           std::cout << "Value of result: " << a / b << '\n';
       }

----


.. dropdown:: A4: Arithmetic Conversions II
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Starting from the program in A3, make it print ``1.5``.

    **Constraint:** you may not modify the two declarations. ``a`` and
    ``b`` must stay ``int``.

    .. code-block:: cpp
       :linenos:
       :emphasize-lines: 5,6

       #include <iostream>
       #include <typeinfo>

       int main() {
           int a{3};
           int b{2};
           std::cout << "Type of result: " << typeid(a / b).name() << '\n';
           std::cout << "Value of result: " << a / b << '\n';
       }

----


.. dropdown:: A5: Fix the Compilation Errors
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    This program has three errors. Find them, explain each one, and fix
    them.

    .. code-block:: cpp

       #include <iostream>

       int main() {
           std::cout << "Enter a number: ";
           int user_input{};
           std::cin >> user_input;

           const int a;                  // Error 1
           constexpr int b{user_input};  // Error 2
           const int c{42};
           c = 50;                       // Error 3

           std::cout << a << " " << b << " " << c << '\n';
       }

----


.. dropdown:: A6: Type Deduction
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Predict the **type** and the **value** of each deduced variable.

    .. code-block:: cpp

       #include <iostream>
       #include <typeinfo>

       int main() {
           short s{10};
           int i{20};
           float f{3.5f};
           double d{2.7};

           auto result1{s + i};    // Type: _____  Value: _____
           auto result2{i * f};    // Type: _____  Value: _____
           auto result3{f / d};    // Type: _____  Value: _____
           auto result4{s + 5.0};  // Type: _____  Value: _____
       }

----


.. dropdown:: A7: Scope
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Find the compilation error, then predict every output.

    .. code-block:: cpp
       :linenos:

       #include <iostream>

       int main() {
           int x{10};
           std::cout << x << '\n';     // Output?

           {
               int y{20};
               int x{30};
               std::cout << x << '\n'; // Output?
               std::cout << y << '\n'; // Output?
           }

           std::cout << x << '\n';     // Output?
           std::cout << y << '\n';     // Output?
       }

----


Part B: Programming Exercises
==============================


.. dropdown:: B1: Variable Declarations and Initialization
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring and initializing variables of different types using
    uniform (brace) initialization and explore the ``sizeof`` operator.

    **Specification**

    1. Create a file called ``variables.cpp``.
    2. Declare and initialize the following variables using uniform initialization (``{}``):

       - An ``int`` for a robot's ID (e.g., 42).
       - A ``double`` for a sensor reading (e.g., 3.14159).
       - A ``float`` for a motor speed (e.g., 1.5f).
       - A ``char`` for a status code (e.g., 'A').
       - A ``bool`` for whether a sensor is active (e.g., true).
       - A ``short`` for a small counter (e.g., 100).
       - An ``unsigned int`` for a part number (e.g., 50000).

    3. Print each variable's value and its size using ``sizeof``.
    4. Use ``std::boolalpha`` to print the ``bool`` as ``true``/``false`` instead of ``1``/``0``.
    5. Compare your ``sizeof`` output with the table in the lecture. Do
       they match on your machine?

----


.. dropdown:: B2: Type Conversion Explorer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand implicit type conversions, narrowing conversions, and
    arithmetic conversions in C++.

    **Specification**

    1. Create a file called ``conversions.cpp``.
    2. Include ``<iostream>`` and ``<typeinfo>``.
    3. Demonstrate the following conversions and print results with ``typeid().name()``:

       - **Implicit widening:** Assign an ``int`` to a ``double`` and print both values and types.
       - **Narrowing with static_cast:** Assign a ``double`` to an ``int`` using ``static_cast<int>()`` and observe truncation.
       - **Bool to int:** Add ``true`` and ``false`` to an integer and print the result.
       - **Arithmetic conversion:** Add an ``int`` and a ``double`` and show the resulting type.
       - **Char to int:** Print a ``char`` variable as both a character and its integer (ASCII) value.

    4. For each conversion, print a descriptive label explaining what is happening.
    5. Read the ``typeid`` output using the table of GCC type codes in
       the lecture. Which of the five conversions changed the type, and
       which only changed the value?

----


.. dropdown:: B3: Constants and constexpr
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between ``const`` and ``constexpr`` and when
    to use each.

    **Specification**

    1. Create a file called ``constants.cpp``.
    2. Declare the following constants:

       - A ``constexpr double`` for pi (3.14159265358979).
       - A ``constexpr int`` for the maximum number of joints on a robot arm (6).
       - A ``const`` variable initialized from a computation (e.g., circumference = 2 * pi * radius, where radius is a ``constexpr``).

    3. Use the constants to compute and print:

       - The area of a circle with radius 5.0 (area = pi * r * r).
       - The circumference of that circle (circumference = 2 * pi * r).

    4. Show that ``constexpr`` cannot use runtime values:

       - Read an ``int`` from ``std::cin`` and store it in a ``const`` variable (this works).
       - Comment out a line that tries to store the same input in a ``constexpr`` variable, with a comment explaining why it fails.

    5. Print all results.
    6. Now delete your hand-written pi and use ``std::numbers::pi`` from
       the C++20 ``<numbers>`` header instead. Print both to 20 digits
       with ``std::setprecision(20)`` and compare them.

----


.. dropdown:: B4: Scope Detective
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand variable scope, lifetime, and shadowing in C++.

    **Specification**

    1. Create a file called ``scopes.cpp``.
    2. **Part A, Predict the output:** Before running the code below, predict
       what it will print. Then compile and run it to check your prediction.

       .. code-block:: cpp

          #include <iostream>

          int value{100};

          int main() {
              std::cout << value << "\n";
              int value{200};
              std::cout << value << "\n";
              {
                  int value{300};
                  std::cout << value << "\n";
                  {
                      std::cout << value << "\n";
                  }
              }
              std::cout << value << "\n";
              std::cout << ::value << "\n";
          }

    3. **Part B, Write your own:** Write a program that:

       - Declares a global variable ``robot_name`` with value ``"GlobalBot"``.
       - In ``main()``, declares a local ``robot_name`` with value ``"LocalBot"``.
       - Inside a nested block, declares another ``robot_name`` with value ``"InnerBot"``.
       - Prints the innermost, local, and global versions (use ``::`` to access the global one).

----


.. dropdown:: B5: Namespace Organizer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create and use custom namespaces to organize code for different robot
    subsystems.

    **Specification**

    1. Create a file called ``namespaces.cpp``.
    2. Define a namespace ``sensors`` with:

       - A ``constexpr int max_range{100};`` (in centimeters).
       - A ``double current_reading{0.0};``
       - A ``const std::string type{"LIDAR"};``

    3. Define a namespace ``actuators`` with:

       - A ``constexpr int max_speed{255};`` (PWM value).
       - A ``double current_speed{0.0};``
       - A ``const std::string type{"DC_MOTOR"};``

    4. In ``main()``, demonstrate three different ways to access namespace members:

       - **Fully qualified:** Use ``sensors::max_range`` directly.
       - **Using declaration:** Use ``using sensors::current_reading;`` then access ``current_reading`` directly.
       - **Using directive:** Use ``using namespace actuators;`` in a limited block scope.

    5. Set some values and print them with labels showing which subsystem they belong to.
    6. Note that both namespaces declare a name ``type``. Explain why
       that is not an error here, and what would happen if you added
       ``using namespace sensors;`` alongside ``using namespace actuators;``
       at file scope.

----


.. dropdown:: B6 Challenge: Unit Converter
    :icon: rocket
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build an interactive unit converter that uses constants, proper types,
    namespaces, and input/output.

    **Specification**

    1. Create a file called ``converter.cpp``.
    2. Define a namespace ``conversion`` with ``constexpr`` conversion factors:

       - ``meters_to_feet`` (1 meter = 3.28084 feet)
       - ``kg_to_pounds`` (1 kg = 2.20462 pounds)
       - ``celsius_to_fahrenheit_scale`` (9.0 / 5.0)
       - ``celsius_to_fahrenheit_offset`` (32.0)

    3. The program should:

       - Display a menu with options: (1) Meters to Feet, (2) Kilograms to Pounds, (3) Celsius to Fahrenheit, (4) Quit.
       - Read the user's choice using ``std::cin``.
       - For options 1-3, prompt for a value, perform the conversion, and print the result.
       - For option 4, print a goodbye message and exit.
       - For invalid choices, print an error message.

    4. Use ``const`` for the user's input value (it should not change after reading).
    5. Use appropriate types (``double`` for measurements, ``int`` for menu choice).
    6. Define the menu choices as an ``enum class`` instead of bare
       integers, and ``static_cast`` the value read from ``std::cin``.
