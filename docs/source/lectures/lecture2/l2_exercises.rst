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

    .. dropdown:: Answer
        :class-container: sd-border-success

        .. list-table::
           :widths: 26 18 56
           :header-rows: 1
           :class: compact-table

           * - Name
             - Legal?
             - Comment
           * - ``my_variable``
             - Yes
             - Follows the course convention.
           * - ``2ndPlace``
             - **No**
             - An identifier cannot start with a digit.
           * - ``_internal``
             - Yes
             - Legal, but see the warning below.
           * - ``user-name``
             - **No**
             - ``-`` is not allowed. The compiler reads this as
               ``user`` minus ``name``.
           * - ``MAX_SIZE``
             - Yes
             - ALL_CAPS conventionally signals a macro. Prefer
               ``max_size``.
           * - ``class``
             - **No**
             - Reserved keyword.
           * - ``numberOfStudents``
             - Yes
             - camelCase. Prefer ``number_of_students``.
           * - ``PI_VALUE``
             - Yes
             - Same issue as ``MAX_SIZE``. Prefer
               ``constexpr double pi_value{...};``

        .. warning::

           Leading underscores are a trap. Names beginning with an
           underscore followed by a **capital** letter, and any name
           containing a **double underscore**, are reserved for the
           implementation *everywhere*. A name with a single leading
           underscore is reserved in the **global** namespace. Just do
           not start identifiers with an underscore.


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

    .. dropdown:: Answer
        :class-container: sd-border-success

        **It does not compile.** Line 4 is the problem:

        .. code-block:: text

           error: narrowing conversion of '3.5e+0' from 'double' to 'int'

        All three of lines 2, 3 and 4 request the same ``double`` to
        ``int`` conversion, which discards the fractional part. Only the
        **braced** form rejects it, because uniform initialization
        forbids narrowing conversions.

        With line 4 removed or written as
        ``int d{static_cast<int>(3.5)};``:

        .. code-block:: text

           <garbage>   <- line 1 is uninitialized: undefined behavior
           3           <- 3.2 truncated
           1           <- 1.3 truncated
           3           <- if line 4 was cast explicitly

        Line 1 is the bigger problem of the two. It compiles, it may
        print a plausible number, and it is undefined behavior every
        time. Write ``int a{};``.


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

    .. dropdown:: Answer
        :class-container: sd-border-success

        .. code-block:: text

           Type of result: i        <- 'i' is the mangled name for int
           Value of result: 1

        Both operands are already ``int``, so **no conversion happens**.
        ``3 / 2`` is integer division: the result is ``1`` and the
        remainder is discarded. Nothing here is rounded, and nothing
        warns you.

        ``typeid(...).name()`` prints GCC's mangled code, not the word
        ``int``. See the table of codes in the lecture.


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

    .. dropdown:: Answer
        :class-container: sd-border-success

        Convert **one** operand at the point of use. The usual
        arithmetic conversions then promote the other one to match.

        .. code-block:: cpp

           #include <iostream>
           #include <typeinfo>

           int main() {
               int a{3};
               int b{2};
               std::cout << "Type of result: "
                         << typeid(static_cast<double>(a) / b).name() << '\n';
               std::cout << "Value of result: "
                         << static_cast<double>(a) / b << '\n';
           }

        .. code-block:: text

           Type of result: d
           Value of result: 1.5

        Note what changed and what did not. ``a`` and ``b`` are still
        ``int`` variables; only the **expression** is evaluated in
        ``double``, because ``double`` outranks ``int`` in the priority
        list.

        Casting the whole expression does **not** work:
        ``static_cast<double>(a / b)`` computes ``3 / 2`` as integers
        first, gets ``1``, and then converts ``1`` to ``1.0``. The
        precision is already gone by then.


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

    .. dropdown:: Answer
        :class-container: sd-border-success

        .. list-table::
           :widths: 12 44 44
           :header-rows: 1
           :class: compact-table

           * - #
             - Why it fails
             - Fix
           * - 1
             - ``uninitialized const 'a'``. A ``const`` variable can
               never be assigned to, so it has to get its value at
               declaration or it can never have one.
             - ``const int a{10};``
           * - 2
             - ``'user_input' is not usable in a constant expression``.
               ``constexpr`` demands a value known at **compile time**,
               and ``user_input`` is not read until runtime.
             - ``const int b{user_input};`` --- a runtime constant is
               exactly what is wanted here.
           * - 3
             - ``assignment of read-only variable 'c'``. ``c`` is
               ``const``.
             - Remove the assignment, or drop the ``const`` if ``c``
               really needs to change.

        .. code-block:: cpp

           #include <iostream>

           int main() {
               std::cout << "Enter a number: ";
               int user_input{};
               std::cin >> user_input;

               const int a{10};            // initialized at declaration
               const int b{user_input};    // runtime constant: const, not constexpr
               const int c{42};            // never reassigned

               std::cout << a << " " << b << " " << c << '\n';
           }

        The pattern worth remembering: **``constexpr`` for values the
        compiler can know, ``const`` for values fixed at runtime.**


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

    .. dropdown:: Answer
        :class-container: sd-border-success

        .. list-table::
           :widths: 18 14 14 54
           :header-rows: 1
           :class: compact-table

           * - Expression
             - Type
             - Value
             - Why
           * - ``s + i``
             - ``int``
             - 30
             - No floating point, so step 1 does not apply. Step 2
               promotes ``short`` to ``int``; both operands now match.
           * - ``i * f``
             - ``float``
             - 70
             - Step 1: one operand is floating point, so both become
               the largest floating-point type present, ``float``.
           * - ``f / d``
             - ``double``
             - 1.2963
             - Step 1 again, and ``double`` is the larger of the two,
               so ``f`` becomes ``double``. Printed at the default 6
               significant digits.
           * - ``s + 5.0``
             - ``double``
             - 15
             - Step 1: ``5.0`` is a ``double`` literal, so the ``short``
               is converted straight to ``double``.

        The lesson: the deduced type is decided by the **expression**,
        not by the variable you assign it to. ``auto`` is only as
        predictable as your grasp of the conversion rules.


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

    .. dropdown:: Answer
        :class-container: sd-border-success

        **Line 15 does not compile:**

        .. code-block:: text

           error: 'y' was not declared in this scope

        ``y`` was declared inside the nested block and went out of scope
        at the closing brace on line 12.

        With that line removed, the outputs are:

        .. code-block:: text

           10   <- the outer x
           30   <- the inner x shadows the outer one
           20   <- y, still in scope inside the block
           10   <- the inner x is gone; the outer x was never touched

        The inner ``int x{30};`` does not modify the outer ``x``. It
        creates a **second, distinct variable** that hides the first for
        the duration of the block. Shadowing is legal and occasionally
        useful, but it is a common source of confusion; ``-Wshadow``
        will warn about it if you want it flagged.


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

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           int main() {
               // Uniform initialization
               int robot_id{42};
               double sensor_reading{3.14159};
               float motor_speed{1.5f};
               char status_code{'A'};
               bool sensor_active{true};
               short counter{100};
               unsigned int part_number{50000};

               // Print values and sizes
               std::cout << "robot_id: " << robot_id
                         << " | size: " << sizeof(robot_id) << " bytes\n";
               std::cout << "sensor_reading: " << sensor_reading
                         << " | size: " << sizeof(sensor_reading) << " bytes\n";
               std::cout << "motor_speed: " << motor_speed
                         << " | size: " << sizeof(motor_speed) << " bytes\n";
               std::cout << "status_code: " << status_code
                         << " | size: " << sizeof(status_code) << " bytes\n";
               std::cout << "sensor_active: " << std::boolalpha << sensor_active
                         << " | size: " << sizeof(sensor_active) << " bytes\n";
               std::cout << "counter: " << counter
                         << " | size: " << sizeof(counter) << " bytes\n";
               std::cout << "part_number: " << part_number
                         << " | size: " << sizeof(part_number) << " bytes\n";
           }


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

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <typeinfo>

           int main() {
               // 1. Implicit widening: int -> double
               int int_val{42};
               double widened{int_val};
               std::cout << "=== Implicit Widening ===\n";
               std::cout << "int_val: " << int_val
                         << " (type: " << typeid(int_val).name() << ")\n";
               std::cout << "widened: " << widened
                         << " (type: " << typeid(widened).name() << ")\n\n";

               // 2. Narrowing with static_cast: double -> int
               double pi{3.14159};
               int truncated{static_cast<int>(pi)};
               std::cout << "=== Narrowing with static_cast ===\n";
               std::cout << "pi: " << pi << "\n";
               std::cout << "truncated: " << truncated
                         << " (fractional part lost)\n\n";

               // 3. Bool to int
               int bool_sum{5 + true + false};
               std::cout << "=== Bool to Int ===\n";
               std::cout << "5 + true + false = " << bool_sum
                         << " (true=1, false=0)\n\n";

               // 4. Arithmetic conversion: int + double -> double
               int a{10};
               double b{3.5};
               auto result = a + b;
               std::cout << "=== Arithmetic Conversion ===\n";
               std::cout << "int(10) + double(3.5) = " << result
                         << " (type: " << typeid(result).name() << ")\n\n";

               // 5. Char to int
               char letter{'Z'};
               std::cout << "=== Char to Int ===\n";
               std::cout << "letter as char: " << letter << "\n";
               std::cout << "letter as int: " << static_cast<int>(letter) << "\n";
           }


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

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iomanip>
           #include <iostream>
           #include <numbers>

           int main() {
               // constexpr: evaluated at compile time
               constexpr double pi{std::numbers::pi};  // step 6: was 3.14159265358979
               constexpr int max_joints{6};
               constexpr double radius{5.0};

               // const: computed from constexpr values (also compile-time here)
               const double area{pi * radius * radius};
               const double circumference{2.0 * pi * radius};

               std::cout << "=== Compile-Time Constants ===\n";
               std::cout << "pi: " << pi << "\n";
               std::cout << "max_joints: " << max_joints << "\n";
               std::cout << "radius: " << radius << "\n";
               std::cout << "area: " << area << "\n";
               std::cout << "circumference: " << circumference << "\n\n";

               // const can use runtime values
               std::cout << "Enter a number: ";
               int user_input{};
               std::cin >> user_input;
               const int user_const{user_input};  // OK: const with runtime value

               std::cout << "Your const value: " << user_const << "\n";

               // constexpr CANNOT use runtime values (uncomment to see the error):
               // constexpr int user_constexpr{user_input};
               // Error: the value of 'user_input' is not usable in a constant expression

               // Step 6: the hand-written value against the library's
               std::cout << "\n=== Step 6 ===\n";
               std::cout << std::setprecision(20);
               std::cout << "typed:   " << 3.14159265358979 << '\n';
               std::cout << "library: " << std::numbers::pi << '\n';
           }

        **Step 6.** The two agree to about the 15th significant digit
        and then diverge: the typed literal has no more digits to give,
        while ``std::numbers::pi`` carries every digit a ``double`` can
        hold. For a circle the size of this classroom that
        difference is irrelevant, and for anything involving repeated
        rotation it is not. There is no reason to accept a worse
        constant when the better one is one ``#include`` away.


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

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Part A output:**

        .. code-block:: text

           100
           200
           300
           300
           200
           100

        The global ``value`` (100) is printed first. Then the local ``value`` (200) shadows it.
        Inside the nested block, another ``value`` (300) shadows the local one. The innermost
        block has no new ``value``, so it uses the nearest one (300). After the nested block
        ends, the local ``value`` (200) is back in scope. Finally, ``::value`` accesses the
        global ``value`` (100).

        The ``::`` with nothing on its left is the scope resolution
        operator naming the **global** namespace. It is the only way to
        reach a global that has been shadowed.

        **Part B solution:**

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           std::string robot_name{"GlobalBot"};

           int main() {
               std::string robot_name{"LocalBot"};

               {
                   std::string robot_name{"InnerBot"};
                   std::cout << "Inner scope: " << robot_name << "\n";
               }

               std::cout << "Local scope: " << robot_name << "\n";
               std::cout << "Global scope: " << ::robot_name << "\n";
           }

        This program is a demonstration, not a model. Three variables
        with the same name in three scopes is exactly the situation
        ``R.6`` and ``-Wshadow`` exist to discourage.


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

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>
           #include <string>

           namespace sensors {
               constexpr int max_range{100};
               double current_reading{0.0};
               const std::string type{"LIDAR"};
           }

           namespace actuators {
               constexpr int max_speed{255};
               double current_speed{0.0};
               const std::string type{"DC_MOTOR"};
           }

           int main() {
               // Method 1: Fully qualified names
               std::cout << "=== Fully Qualified ===\n";
               std::cout << "Sensor type: " << sensors::type << "\n";
               std::cout << "Sensor max range: " << sensors::max_range << " cm\n";

               // Method 2: Using declaration (imports a single name)
               std::cout << "\n=== Using Declaration ===\n";
               using sensors::current_reading;
               current_reading = 42.5;
               std::cout << "Sensor reading: " << current_reading << " cm\n";

               // Method 3: Using directive (imports all names -- limited scope)
               std::cout << "\n=== Using Directive (block scope) ===\n";
               {
                   using namespace actuators;
                   current_speed = 128.0;
                   std::cout << "Actuator type: " << type << "\n";
                   std::cout << "Actuator max speed: " << max_speed << "\n";
                   std::cout << "Actuator current speed: " << current_speed << "\n";
               }

               // Summary
               std::cout << "\n=== Summary ===\n";
               std::cout << "Sensor reading: " << sensors::current_reading << " cm\n";
               std::cout << "Actuator speed: " << actuators::current_speed << "\n";
           }

        **Step 6.** ``sensors::type`` and ``actuators::type`` are two
        different names in two different scopes, so there is no
        collision. Adding both ``using namespace`` directives at file
        scope brings both ``type`` names into the same scope, and any
        unqualified use of ``type`` then fails with
        ``reference to 'type' is ambiguous``. This is the entire
        argument against ``using namespace`` in three lines of code.


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

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <iostream>

           namespace conversion {
               constexpr double meters_to_feet{3.28084};
               constexpr double kg_to_pounds{2.20462};
               constexpr double celsius_to_fahrenheit_scale{9.0 / 5.0};
               constexpr double celsius_to_fahrenheit_offset{32.0};
           }

           enum class MenuChoice {
               meters_to_feet = 1,
               kg_to_pounds = 2,
               celsius_to_fahrenheit = 3,
               quit = 4
           };

           int main() {
               bool running{true};

               while (running) {
                   std::cout << "\n=== Unit Converter ===\n";
                   std::cout << "1. Meters to Feet\n";
                   std::cout << "2. Kilograms to Pounds\n";
                   std::cout << "3. Celsius to Fahrenheit\n";
                   std::cout << "4. Quit\n";
                   std::cout << "Enter your choice: ";

                   int raw_choice{};
                   std::cin >> raw_choice;
                   const MenuChoice choice{static_cast<MenuChoice>(raw_choice)};

                   if (choice == MenuChoice::quit) {
                       std::cout << "Goodbye!\n";
                       running = false;

                   } else if (choice == MenuChoice::meters_to_feet) {
                       std::cout << "Enter value in meters: ";
                       double input{};
                       std::cin >> input;
                       const double meters{input};
                       const double feet{meters * conversion::meters_to_feet};
                       std::cout << meters << " m = " << feet << " ft\n";

                   } else if (choice == MenuChoice::kg_to_pounds) {
                       std::cout << "Enter value in kilograms: ";
                       double input{};
                       std::cin >> input;
                       const double kg{input};
                       const double pounds{kg * conversion::kg_to_pounds};
                       std::cout << kg << " kg = " << pounds << " lbs\n";

                   } else if (choice == MenuChoice::celsius_to_fahrenheit) {
                       std::cout << "Enter value in Celsius: ";
                       double input{};
                       std::cin >> input;
                       const double celsius{input};
                       const double fahrenheit{
                           celsius * conversion::celsius_to_fahrenheit_scale
                           + conversion::celsius_to_fahrenheit_offset};
                       std::cout << celsius << " C = " << fahrenheit << " F\n";

                   } else {
                       std::cout << "Invalid choice. Please try again.\n";
                   }
               }
           }

        The ``static_cast`` is required precisely because ``enum class``
        does not convert implicitly. That is the safety feature working:
        the cast is the one place where an arbitrary integer enters the
        enumeration, so it is the one place that needs checking.
