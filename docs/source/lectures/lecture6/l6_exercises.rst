====================================================
C++ Exercises
====================================================

This exercise covers Lecture 6: Functions, Advanced. There is one exercise
this week, because the reading on
:doc:`exception handling </reading_material/exception_handling/eh_index>`
is due before Lecture 7 as well.

The exercise writes software for a charging station that looks after four
delivery drones. Each drone reports its battery level and whether it is in
the air. The station finds the next drone to land and summarizes the
batteries.

.. note::

   Build the exercise from VS Code with CMake, as in the lecture. Add a
   target for it to ``project/week6/CMakeLists.txt``. The course project
   already turns on the warnings, so fix every warning before you submit.

   Format the output as in the **Example Output**: a title between two lines
   of ``=``, and each part under a heading underlined with ``-``, with the
   numbers in aligned columns.


----


.. dropdown:: Exercise 1: The Drone Charging Station
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use the four main tools of Lecture 6 in one short program: a
    ``struct``, a result that may be missing, a function template with a
    concept, and a lambda.

    **Specification**

    Write one program, ``project/week6/exercises/drones.cpp``, with the
    target ``week6_drones``.

    1. Declare a ``struct Drone`` with three members: ``id`` (an
       ``int``), ``battery_pct`` (a ``double``, in percent) and
       ``airborne`` (a ``bool``). Give each member a default: ``0``,
       ``100.0`` and ``false``. Print the fleet below.
    2. Write ``first_low_battery``. It takes the fleet and a limit in
       percent, and returns the id of the first airborne drone whose battery
       is below the limit, as a ``std::optional<int>``. It returns an empty
       optional when there is none. Call it with ``30.0`` and with
       ``20.0``, and print the id, or ``none``.
    3. Write a function template ``average_of`` that returns the average of
       a ``std::vector<T>``, and ``0`` for an empty one. Constrain ``T``
       with the concept ``std::floating_point``. Use it to print the
       average battery level.
    4. Count the drones whose battery is below ``30.0`` percent, with
       ``std::count_if`` and a lambda that captures the limit by value.

    Start from this fleet:

    .. code-block:: cpp

       std::vector<Drone> fleet{{1, 76.0, true}, {2, 22.5, true}, {3, 91.0}, {4, 28.0, true}};

    **Example Output**

    Use two digits after the decimal point.

    .. code-block:: text

       ====================================
         Drone Charging Station
       ====================================

       Fleet
       ------------------------------------
         drone 1 :  76.00 %  airborne
         drone 2 :  22.50 %  airborne
         drone 3 :  91.00 %  landed
         drone 4 :  28.00 %  airborne

       Next to Land
       ------------------------------------
         below 30.00 % : drone 2
         below 20.00 % : none

       Battery
       ------------------------------------
         average battery :  54.38 %
         below 30 %      :      2
