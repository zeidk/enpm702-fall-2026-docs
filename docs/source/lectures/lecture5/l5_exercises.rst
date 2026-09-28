====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 5: Functions.
They follow the order of the lecture. Work through them in order, as
each exercise builds on the skills from the previous one.

Every exercise writes software for one robot: an autonomous rover in an
underground mine. It drives along the tunnels, reads gas sensors, drills rock
samples and loads ore carts. Its three-joint arm is the program in
``project/week5/arm_demo`` of the course repository.

Exercises 1 and 2 are single-file programs. Exercise 3 is a program split into
headers and source files. Exercise 4 extends ``arm_demo``.

.. note::

   Build every exercise from VS Code with CMake, as in the lecture. Add a
   target for each new program to ``project/week5/CMakeLists.txt``. The course
   project already turns on the warnings, so fix every warning before you move
   on.

   Format the output as in each exercise's **Example Output**: a title
   between two lines of ``=``, and each part under a heading underlined with
   ``-``, with the numbers in aligned columns.


----


.. dropdown:: Exercise 1: Rover Sensor Functions
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write functions that pass their arguments and return their results in
    the right way: by value, by reference, by reference to ``const``,
    ``std::span`` and pointer.

    **Specification**

    Write one program, ``project/week5/exercises/sensors.cpp``, with the
    target ``week5_sensors``. You choose every parameter type and
    return type. Nothing may be copied that does not need to be, and nothing
    may be changed that should not be.

    1. ``wrap_heading``: changes the caller's rover heading, in degrees, so
       that it is at least ``-180.0`` and below ``180.0``. It returns
       nothing.
    2. ``mean_gas_ppm``: returns the mean of a sequence of methane readings,
       in parts per million, and ``0.0`` for an empty sequence. The same
       function must accept a C array, a ``std::array<double, 4>`` and a
       ``std::vector<double>``.
    3. ``count_above_limit``: returns how many readings in a
       ``std::vector<double>`` are above a threshold.
    4. ``print_reading``: prints a value followed by its unit, such as
       ``12.5 ppm``. When the caller gives no unit, only the value is
       printed.
    5. ``plan_drill_depths``: takes a count ``n`` and a step in metres, and
       returns a ``std::vector<double>`` of ``n`` depths: ``0``, ``step``,
       ``2 * step``, and so on.
    6. ``richest_sample``: returns a reference to the largest ore grade in a
       ``std::vector<double>``, so the caller can change that element.
    7. ``find_first_fault``: returns a pointer to the first negative reading
       in a ``std::vector<double>``, or ``nullptr`` when there is none.

    In ``main``:

    - Wrap the headings ``190.0``, ``-190.0`` and ``540.0`` and print each
      result.
    - Print the mean of three sets of gas readings, in ppm: a C array
      ``{12.0, 18.0, 54.0}``, a ``std::array<double, 4>``
      ``{10.0, 20.0, 30.0, 40.0}`` and a ``std::vector<double>``
      ``{45.0, 52.5, 61.0, 38.0, 70.5}``. Then print how many readings in
      the vector are above ``50.0`` ppm.
    - Print one reading with a unit and one without.
    - Plan 5 depths with a step of ``0.25`` m and print them.
    - Print the ore grades ``{1.2, 3.8, 2.4, 0.9}``, in percent. Set the
      richest sample to ``0.0``, marking it as processed, and print them
      again.
    - Call ``find_first_fault`` on ``{4.1, -1.0, 3.3}`` and on
      ``{4.1, 3.3}``. Print the fault, or ``no fault``.

    **Example Output**

    Use two digits after the decimal point.

    .. code-block:: text

       ============================================
         Rover Sensor Report
       ============================================

       Headings (deg)
       --------------------------------------------
           190.00  ->   -170.00
          -190.00  ->    170.00
           540.00  ->   -180.00

       Methane (ppm)
       --------------------------------------------
         mean, C array      :    28.00
         mean, std::array   :    25.00
         mean, std::vector  :    53.40
         above 50 ppm       :        3

       Readings
       --------------------------------------------
         12.50 ppm
         12.50

       Drill Plan (m)
       --------------------------------------------
         hole 1 :   0.00
         hole 2 :   0.25
         hole 3 :   0.50
         hole 4 :   0.75
         hole 5 :   1.00

       Ore Grades (%)
       --------------------------------------------
         before :   1.20   3.80   2.40   0.90
         after  :   1.20   0.00   2.40   0.90

       Faults
       --------------------------------------------
         readings :   4.10  -1.00   3.30
         -> fault: -1.00
         readings :   4.10   3.30
         -> no fault

.. dropdown:: Exercise 2: Sample Log and Cart Counter
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write overloaded functions, give parameters default arguments, and keep
    state between calls with static local variables.

    **Specification**

    Write one program, ``project/week5/exercises/sample_log.cpp``, with the
    target ``week5_sample_log``. Use no global variables: every value that
    lives between calls is a static local.

    1. Write three overloads of ``log_sample``. Each prints one line:

       - ``log_sample(int id)`` prints ``sample 7``
       - ``log_sample(int id, double grade)`` prints ``sample 7: grade 3.2 %``
       - ``log_sample(std::string_view drift, double grade)`` prints
         ``drift B4: grade 3.2 %``

    2. Write ``clamp_speed``, which clamps the rover's speed, in metres per
       second, to the range from ``0.0`` to a limit. The limit is a default
       argument of ``1.5``.
    3. Write ``next_cart_id``, which returns ``1`` on its first call, ``2``
       on its second, and so on. It takes no parameters.
    4. Write ``warn_gas``, which takes a methane reading in percent. The
       first time a reading is above ``1.0``, it prints
       ``WARNING: methane 1.3 %``. Every later call prints nothing.
    5. Write ``deg_to_rad_table``, which converts a whole number of degrees,
       from ``0`` to ``360``, to radians by looking it up in a table. Build
       the table in a separate function that prints ``building table``. The
       table must be built on the first call only.

    In ``main``:

    - Call each ``log_sample`` overload once.
    - Print ``clamp_speed(2.0)``, ``clamp_speed(2.0, 0.5)`` and
      ``clamp_speed(-0.3)``.
    - Load four carts in a loop and print ``cart <id> loaded`` for each.
    - Call ``warn_gas`` with ``0.4``, ``1.3``, ``0.2`` and ``1.8``. Only one
      warning is printed.
    - Call ``deg_to_rad_table`` with ``0``, ``90``, ``180``, ``270`` and
      ``360`` and print each result. ``building table`` is printed once.

    **Example Output**

    ``building table`` appears once, before the first row of the table.

    .. code-block:: text

       ============================================
         Sample Log and Cart Counter
       ============================================

       Sample Log
       --------------------------------------------
         sample 7
         sample 7: grade 3.2 %
         drift B4: grade 3.2 %

       Speed Limit (m/s)
       --------------------------------------------
         clamp_speed(2.0)       :  1.50
         clamp_speed(2.0, 0.5)  :  0.50
         clamp_speed(-0.3)      :  0.00

       Ore Carts
       --------------------------------------------
         cart 1 loaded
         cart 2 loaded
         cart 3 loaded
         cart 4 loaded

       Gas Alarm
       --------------------------------------------
         WARNING: methane 1.3 %

       Angle Table
       --------------------------------------------
         building table
            0 deg  ->  0.0000 rad
           90 deg  ->  1.5708 rad
          180 deg  ->  3.1416 rad
          270 deg  ->  4.7124 rad
          360 deg  ->  6.2832 rad

.. dropdown:: Exercise 3: The Gas Monitor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a program split into a header and two source files, read its input
    from the command line, and document it with Doxygen.

    **Specification**

    Create ``project/week5/gas_monitor`` with this layout, the same as
    ``arm_demo``:

    .. code-block:: text

       gas_monitor/
       ├── include/
       │   └── gas.hpp
       └── src/
           ├── gas.cpp
           └── main.cpp

    1. In ``gas.hpp``, declare three functions. In ``gas.cpp``, define them.

       - ``mean_percent``: the mean of a sequence of methane readings, in
         percent.
       - ``peak_percent``: the largest reading.
       - ``gas_level``: returns ``"safe"`` below ``1.0`` percent,
         ``"warning"`` from ``1.0`` to below ``1.5``, and ``"evacuate"`` from
         ``1.5`` up. The two thresholds are ``constexpr`` constants in
         ``gas.hpp``, and ``gas_level`` takes them as default arguments.

    2. Protect ``gas.hpp`` with ``#pragma once``. No function body goes in
       the header.
    3. In ``main.cpp``, write ``int main(int argc, char* argv[])``. Each
       command-line argument is one reading. Convert each one with
       ``std::from_chars``. When there is no reading, print
       ``usage: gas_monitor <reading>...``. When an argument is not a number,
       print ``not a number: <arg>``. An argument such as ``1.2x`` is not a
       number either: the whole argument must be read. Both messages go to
       ``std::cerr``, and ``main`` returns ``1``.
    4. Print the number of readings, the mean, the peak and the level of the
       peak, one per line, with two digits after the decimal point.
    5. Add a target ``week5_gas_monitor`` to
       ``project/week5/CMakeLists.txt``: both source files, and the
       ``include`` folder as its include directory.
    6. Give every file an ``@file`` comment, and every function in
       ``gas.hpp`` ``@brief``, ``@param`` and ``@return``. Copy
       ``arm_demo/docs/Doxyfile`` into a new ``gas_monitor/docs`` folder and
       change ``PROJECT_NAME`` to ``"Gas Monitor"``. Generate the pages from
       ``gas_monitor/docs`` and check that all three functions appear.

    .. warning::

       Hand in the ``Doxyfile``, not the pages it generates. Delete
       ``gas_monitor/docs/html`` (and ``latex`` or ``xml``, if Doxygen made them)
       before you zip your work. The pages are regenerated from your comments
       when your work is graded, by running ``doxygen Doxyfile`` in
       ``gas_monitor/docs``. Keep the paths in the ``Doxyfile`` relative, such as
       ``INPUT = ../include ../src``, so it works on another machine.

    Build it, then run it from ``build/project/week5``:

    .. code-block:: bash

       ./week5_gas_monitor 0.4 0.9 1.2
       ./week5_gas_monitor 0.4 1.7
       ./week5_gas_monitor 0.4 abc
       ./week5_gas_monitor

    **Example Output**

    The last two runs print only their message and return ``1``.

    .. code-block:: text

       $ ./week5_gas_monitor 0.4 0.9 1.2
       ============================================
         Gas Monitor
       ============================================
         readings :      3
         mean     :   0.83 %
         peak     :   1.20 %
       --------------------------------------------
         level    : warning
       ============================================
       $ ./week5_gas_monitor 0.4 1.7
       ============================================
         Gas Monitor
       ============================================
         readings :      2
         mean     :   1.05 %
         peak     :   1.70 %
       --------------------------------------------
         level    : evacuate
       ============================================
       $ ./week5_gas_monitor 0.4 abc
       not a number: abc
       $ ./week5_gas_monitor
       usage: gas_monitor <reading>...

.. dropdown:: Exercise 4: Extending the Rover's Arm (Challenge)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Add functions to an existing multi-file program in the right places, use
    them from ``main``, and document them.

    **Specification**

    Work in ``project/week5/arm_demo`` (target ``week5_arm_demo``). Do not
    create new ``.hpp`` or ``.cpp`` files. The target is not built by
    default: in ``project/week5/CMakeLists.txt``, uncomment the four lines
    that define ``week5_arm_demo``.

    1. Add ``convert_rad_to_deg``, the reverse of ``convert_deg_to_rad``,
       marked ``[[nodiscard]]``: the declaration in
       ``include/kinematics.hpp``, the definition in ``src/kinematics.cpp``.
    2. Add ``tool_distance``, marked ``[[nodiscard]]``, in the same two
       files. It takes the tool's ``x`` and ``y`` and returns the distance
       from the arm's base to the tool, in metres. ``forward_kinematics``
       measures ``x`` and ``y`` from the base, so the base is at ``(0, 0)``.
    3. Add ``can_reach``, which takes the tool distance and the distance to
       a rock face, in metres, and returns ``true`` when the two differ by
       at most a tolerance, on either side. Make the tolerance a default
       argument of ``0.05`` m.
    4. In ``src/main.cpp``:

       - Put a title above the joint table.
       - After the tool position, print the distance to the tool with three
         digits after the decimal point.
       - Print the direction of the tool as seen from the base, in degrees,
         with one digit after the decimal point. ``std::atan2(y, x)`` from
         ``<cmath>`` gives it in radians; use ``convert_rad_to_deg`` for the
         rest.
       - Accept an optional fourth command-line argument: the distance to
         the rock face, in metres. Check it the same way as the angles. When
         it is given, print it followed by ``in reach`` or ``out of reach``.
         When the program asks for the angles, it does not ask for the rock
         face.
       - Update the usage message to
         ``usage: ./week5_arm_demo [q1_deg q2_deg q3_deg [face_m]]``.

    5. Give every new function a Doxygen comment on its declaration, with
       ``@brief``, ``@param`` and ``@return``, and update the ``@brief`` of
       ``main``. Generate the pages from ``arm_demo/docs`` and check that
       every new function appears.

    .. warning::

       Hand in the ``Doxyfile``, not the pages it generates. Delete
       ``arm_demo/docs/html`` (and ``latex`` or ``xml``, if Doxygen made them)
       before you zip your work. The pages are regenerated from your comments
       when your work is graded, by running ``doxygen Doxyfile`` in
       ``arm_demo/docs``. Keep the paths in the ``Doxyfile`` relative, such as
       ``INPUT = ../include ../src``, so it works on another machine.

    Build ``week5_arm_demo`` and run it from ``build/project/week5``:

    .. code-block:: bash

       ./week5_arm_demo 180 95 -10
       ./week5_arm_demo 180 95 -10 0.9
       ./week5_arm_demo 180 95 -10 2.0
       ./week5_arm_demo
       ./week5_arm_demo 180 95 -10 abc

    **Example Output**

    ``...`` marks lines that are the same as in the first run. Without a
    fourth argument, the rock face line is left out.

    .. code-block:: text

       $ ./week5_arm_demo 180 95 -10 0.9
       ============================================
         Rover Arm
       ============================================
       joint   input deg   clamped deg   radians
       q1         180.0         135.0     2.356
       q2          95.0          90.0     1.571
       q3         -10.0         -10.0    -0.175
       tool: x = -0.882 m, y = -0.101 m
       --------------------------------------------
       distance  :    0.888 m
       direction :   -173.4 deg
       rock face :    0.900 m, in reach
       ============================================
       $ ./week5_arm_demo 180 95 -10 2.0
       ...
       --------------------------------------------
       distance  :    0.888 m
       direction :   -173.4 deg
       rock face :    2.000 m, out of reach
       ============================================
       $ ./week5_arm_demo
       Enter angle 1 (deg): 180
       Enter angle 2 (deg): 95
       Enter angle 3 (deg): -10
       ...
       --------------------------------------------
       distance  :    0.888 m
       direction :   -173.4 deg
       ============================================
       $ ./week5_arm_demo 180 95 -10 abc
       not a number: abc
