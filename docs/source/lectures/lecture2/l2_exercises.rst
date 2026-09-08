====================================================
C++ Exercises
====================================================

Ten exercises reinforcing :doc:`Lecture 2 <l2_lecture>`, in the order the
lecture covers the material.

They come in two kinds, and each is labelled:

- **Written** exercises ask for short answers. The compiler cannot
  answer these for you: they ask you to name a rule, classify what
  happened, or state something that never appears in a program's output.
- **Code** exercises give you starter code with ``TODO`` markers. You
  complete it.

.. note::

   **What to submit.** All ten, in a **single file** named
   ``firstname_lastname.cpp`` --- for example, ``ada_lovelace.cpp`` ---
   uploaded to **Canvas**. Do not submit several files.

   **Your file must build**, and running it must not crash. An exercise
   you could not finish should be left as a comment saying how far you
   got; that is worth more than code that does not compile.

.. note::

   **How to lay the file out.** Written answers go in comments. Each
   code exercise gets its own **block** inside ``main()``. That block is
   the compound statement from the lecture, and it does real work here:
   each block has its own scope, so you can reuse a name like ``count``
   in two exercises without a collision.

   .. code-block:: cpp

      #include <iostream>
      // TODO: add the other headers you need as you go

      // ===== Exercise 2: Valid Identifiers =====
      // my_variable  -- legal, follows the course convention
      // 2ndPlace     -- not legal, an identifier cannot start with a digit
      // ...

      int main() {
          {   // ===== Exercise 1: Robot Telemetry Report =====

          }

          {   // ===== Exercise 3: Initialization and Undefined Behavior =====

          }
      }

   Number every heading and keep the ``=====`` markers. They are how
   your work gets found. A written exercise may sit above ``main()``
   even though the exercise before and after it are blocks inside it.

.. note::

   **Building.** Use the course project in **VS Code**, exactly as in
   Lecture 1: configure, build, and run from the editor. There are no
   compiler flags to type. **C++20** and ``-Wall -Wextra`` are set once
   in ``CMakeLists.txt``, so every build already has warnings enabled.

   The exercises themselves live on this page, not in the course
   repository --- there is nothing to pull to get them.

   Several exercises below are about **warnings** rather than errors, so
   read the build output, not just the final success or failure.


----


.. dropdown:: Exercise 1 (code): Robot Telemetry Report
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Uniform initialization, ``sizeof``, and the stream manipulators.

    .. code-block:: cpp

       {   // ===== Exercise 1: Robot Telemetry Report =====

           // TODO 1: declare these with uniform initialization {}
           //   robot_id       int            42
           //   battery_volts  double         11.1
           //   motor_speed    float          1.5f
           //   status_code    char           'A'
           //   is_active      bool           true
           //   part_number    unsigned int   50000

           // TODO 2: print each one on its own line, with a label.

           // TODO 3: print the size in bytes of each, using sizeof.

           // TODO 4: print is_active again so that it reads true, not 1.

           // TODO 5: print battery_volts to exactly 3 decimal places.

           // TODO 6: print is_active ONE more time, inserting no
           //         manipulator at all. Does it print true or 1?
           //         Explain the result in a comment. This is what
           //         "manipulators are sticky" means.

           // TODO 7: in a comment, name the manipulator you used that
           //         needed a header the others did not, and that header.
       }

----


.. dropdown:: Exercise 2 (written): Valid Identifiers
    :icon: checklist
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    Which of these names are **legal** C++ identifiers? For the legal
    ones, which follow the course convention (``snake_case``)?

    .. code-block:: text

       my_variable        2ndPlace         _internal        user-name
       MAX_SIZE           class            numberOfStudents PI_VALUE

    **Write:** one line per name --- legal or not, and if legal, whether
    it follows the convention. Give the reason in a few words.

    Two of them are legal but still poor choices, for different reasons.
    Say which, and why.

----


.. dropdown:: Exercise 3 (code): Initialization and Undefined Behavior
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    The three initialization forms, and why this course uses braces.

    .. code-block:: cpp

       {   // ===== Exercise 3: Initialization and Undefined Behavior =====

           // TODO 1: declare  int a;  with no initializer, then print it.
           //         Record the value AND the compiler's warning in a
           //         comment. Build and run twice: is the value the same
           //         both times? What does that tell you?

           // TODO 2: fix it so the value is reliably 0, using the form
           //         this course prefers.

           // TODO 3: write all three initialization forms for an int
           //         holding 5 -- copy, direct, and uniform -- and print
           //         each. Label which is which in a comment.

           // TODO 4: write  int narrow{3.9};  and leave it COMMENTED
           //         OUT with the error it produces. Then write the two
           //         forms of the same conversion that DO compile, print
           //         them, and explain in a comment why the braced form
           //         is the one the language rejects.

           // TODO 5: in a comment, name two other sources of undefined
           //         behavior from the lecture.
       }

----


.. dropdown:: Exercise 4 (written): Which Segment?
    :icon: checklist
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    Name the memory segment that holds each numbered item.

    .. code-block:: cpp

       #include <iostream>

       int g_ready{42};        // (1)
       int g_count;            // (2)

       int main() {
           int local{7};       // (3)

           std::cout << "ready\n";   // the text "ready\n" itself -- (4)
           std::cout << g_ready << ' ' << g_count << ' ' << local << '\n';
       }

    **Write:** the segment for each of (1)--(4), then answer:

    - What does ``g_count`` print, and is that value guaranteed?
    - If you moved ``g_count`` inside ``main()`` and still did not
      initialize it, would the answer change? Why?
    - Which of the four items still exists after ``main()`` returns?

----


.. dropdown:: Exercise 5 (code): Conversion Audit
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Make each conversion visible, then account for it.

    .. code-block:: cpp

       {   // ===== Exercise 5: Conversion Audit =====

           int count{7};
           double ratio{2.0};

           // TODO 1: print count / 2. It is not 3.5. Explain in a
           //         comment why no conversion happened here.

           // TODO 2: print count / ratio. In a comment, say which
           //         operand was converted, and to what.

           // TODO 3: print count / 2 again, this time producing 3.5,
           //         WITHOUT changing either declaration above.

           short big{300};
           // TODO 4: print static_cast<char>(big) as an int. Say in a
           //         comment what was lost, and why.

           char letter{'a'};
           // TODO 5: print letter, then letter + 1. Then make it print
           //         the letter b without removing the + 1.

           int a{-1};
           unsigned int b{1};
           // TODO 6: write your prediction for (a < b) in a comment
           //         FIRST. Then print it with std::boolalpha and record
           //         both the output and the compiler's warning.
       }

----


.. dropdown:: Exercise 6 (written): Promotion or Conversion?
    :icon: checklist
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    For each numbered line, give the **resulting type**, then say whether
    what fired was a **promotion** or a **conversion**.

    .. code-block:: cpp

       #include <iostream>
       #include <typeinfo>

       int main() {
           short s{10};
           char c{'A'};
           unsigned int u{3};
           int i{20};
           float f{3.5f};
           double d{2.7};

           std::cout << typeid(s + c).name() << '\n';    // (1)
           std::cout << typeid(i * f).name() << '\n';    // (2)
           std::cout << typeid(f / d).name() << '\n';    // (3)
           std::cout << typeid(i + u).name() << '\n';    // (4)
           std::cout << typeid(s + 5.0).name() << '\n';  // (5)
       }

    ``typeid(...).name()`` prints the compiler's **mangled** name, not
    the word you expect. The single-letter codes are listed in the
    lecture.

    **Write:** five lines, each giving the type and the category.

    Line (1) is worth pausing on: **neither** operand ends up as its own
    type. Name the step of the procedure responsible.

----


.. dropdown:: Exercise 7 (written): Diagnose Four Errors
    :icon: checklist
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    This program has four errors.

    .. code-block:: cpp

       #include <iostream>

       int main() {
           std::cout << "Enter a number: ";
           int user_input{};
           std::cin >> user_input;

           const int a;                   // Error 1
           constexpr int b{user_input};    // Error 2
           const int c{42};
           c = 50;                         // Error 3

           const     double r{2.5};
           constexpr double area{r * r};   // Error 4

           std::cout << a << " " << b << " " << c << " " << area << '\n';
       }

    **Write:** for each of the four, name what is wrong in one sentence.

    Error 4 is the surprising one. Replacing ``const`` with ``constexpr``
    on ``r`` fixes it, yet the same code with ``int`` instead of
    ``double`` compiles as written. **Explain why.**

----


.. dropdown:: Exercise 8 (code): Constants Without Macros
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Replace a macro-based program with one the compiler can check.

    This is the code you are replacing. **Do not submit it working** ---
    submit the version that has no macros in it at all.

    .. code-block:: cpp

       #define PI 3.14159
       #define SQUARE(x) ((x) * (x))

       int i{5};
       std::cout << PI * SQUARE(2.0) << '\n';
       std::cout << SQUARE(i++) << '\n';       // what does this do?

    .. code-block:: cpp

       {   // ===== Exercise 8: Constants Without Macros =====

           // TODO 1: in a comment, write out what SQUARE(i++) expands to
           //         and say why the result is undefined behavior.

           // TODO 2: declare a constexpr for pi using std::numbers::pi
           //         from <numbers>. Do not type the digits yourself.

           // TODO 3: declare  constexpr double wheel_radius{0.05};

           // TODO 4: compute and print the wheel's area and
           //         circumference. No macros anywhere.

           // TODO 5: add a static_assert that wheel_radius is positive.

           // TODO 6: read an int from std::cin into a const variable
           //         (this works). Below it, write the constexpr version
           //         COMMENTED OUT, with the compiler's reason.

           // TODO 7: declare  const double r{2.5};  then try
           //             constexpr double area2{r * r};
           //         Leave it commented with the error it gives, then
           //         write a working version by changing ONE keyword.
       }

----


.. dropdown:: Exercise 9 (code): Scope, Shadowing, and Namespaces
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Two namespaces, one shadowed name, and the ``::`` operator.

    Put the namespaces at **file scope**, above ``main()``:

    .. code-block:: cpp

       // TODO A: define namespace sensors containing
       //           constexpr int max_range{100};
       //           const std::string type{"LIDAR"};

       // TODO B: define namespace actuators containing
       //           constexpr int max_speed{255};
       //           const std::string type{"DC_MOTOR"};

    .. code-block:: cpp

       {   // ===== Exercise 9: Scope, Shadowing, and Namespaces =====

           // TODO 1: print sensors::max_range using full qualification.

           // TODO 2: bring ONE name into scope with a using-declaration
           //         (not a using-directive) and print it unqualified.

           int reading{10};
           // TODO 3: open a nested block. Declare another int reading
           //         with a different value, and print it. Then try to
           //         print the OUTER reading from inside that block.
           //         Explain in a comment what stops you.

           // TODO 4: after the nested block closes, print reading again.
           //         Say in a comment which one you are seeing, and what
           //         happened to the other.

           // TODO 5: print BOTH sensors::type and actuators::type. In a
           //         comment, explain why two variables named type is
           //         not a collision.

           // TODO 6: in a comment, describe what would break if you put
           //         using namespace sensors;  and
           //         using namespace actuators;  at file scope. Try it
           //         if you like, then take it back out.
       }

----


.. dropdown:: Exercise 10 (code, challenge): Unit Converter
    :icon: rocket
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    An interactive program that pulls the lecture together.

    Put these at **file scope**, above ``main()``:

    .. code-block:: cpp

       // TODO A: define a type alias
       //           using Measurement = double;
       //         then use Measurement below instead of writing double.

       // TODO B: define namespace conversion with these constexpr factors:
       //           meters_to_feet                 3.28084
       //           kg_to_pounds                   2.20462
       //           celsius_to_fahrenheit_scale    9.0 / 5.0
       //           celsius_to_fahrenheit_offset   32.0

    .. code-block:: cpp

       {   // ===== Exercise 10: Unit Converter =====

           // TODO 1: give each menu option a named constexpr int rather
           //         than writing bare 1, 2, 3, 4 in your comparisons.

           // TODO 2: print a menu:
           //           1) Meters to Feet
           //           2) Kilograms to Pounds
           //           3) Celsius to Fahrenheit
           //           4) Quit

           // TODO 3: read the user's choice with std::cin.

           // TODO 4: for options 1-3, prompt for a value and read it
           //         into a const Measurement (it must not change once
           //         read), convert it, and print the result.

           // TODO 5: print every result to exactly two decimal places,
           //         using std::fixed and std::setprecision(2).

           // TODO 6: option 4 prints a goodbye message. Anything else
           //         prints an error message.

           // TODO 7: assign a Measurement to a plain double and back.
           //         It compiles. In a comment, say what a type alias
           //         does and does not buy you.
       }
