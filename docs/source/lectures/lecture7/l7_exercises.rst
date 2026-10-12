====================================================
C++ Exercises
====================================================

This exercise covers Lecture 7: Smart Pointers and Move Semantics. There is
one exercise this week, and it is graded: hand it in on Canvas before
Lecture 8.

The exercise works on the fleet manager from the lecture. Four robots are on
the heap. The fleet owns every robot, the charging queue shares the robots
that are low on battery, and a dashboard watches one robot without keeping it
alive.

.. note::

   Build the exercise from VS Code with CMake, as in the lecture. Add a
   target for it to ``project/week7/CMakeLists.txt``:

   .. code-block:: cmake

      add_executable(week7_charging exercises/charging.cpp)
      target_include_directories(week7_charging PRIVATE common)
      target_compile_options(week7_charging PRIVATE -fsanitize=address)
      target_link_options(week7_charging PRIVATE -fsanitize=address)

   The ``common`` folder holds ``fleet.hpp``, with ``Position`` and
   ``RobotStatus``. ``-fsanitize=address`` turns on LeakSanitizer, so a leak
   is reported when the program ends. The course project already turns on
   the warnings, so fix every warning before you submit.

   Format the output as in the **Example Output**: a title between two lines
   of ``=``, and each part under a heading underlined with ``-``, with the
   numbers in aligned columns.


----


.. dropdown:: Exercise 1: The Charging Queue
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use the three smart pointers of Lecture 7 in one short program: a
    factory that returns a ``std::unique_ptr``, a fleet and a charging queue
    that share robots through ``std::shared_ptr``, and a dashboard that
    watches a robot through a ``std::weak_ptr``.

    **Specification**

    Write one program, ``project/week7/exercises/charging.cpp``, with the
    target ``week7_charging``. Include ``fleet.hpp`` and use its
    ``RobotStatus`` as it is. Write no ``new`` and no ``delete``.

    1. Write ``make_robot``. It takes an id and a battery level in percent,
       and returns a ``std::unique_ptr<RobotStatus>`` made with
       ``std::make_unique``. The robot is at ``{0.0, 0.0}`` and not busy.
    2. Declare ``using Fleet = std::vector<std::shared_ptr<RobotStatus>>;``.
       Put robots 1, 2 and 3 into the fleet straight from ``make_robot``.
       Create robot 4 in a variable ``robot_4``, then move it into the fleet.
       Print the fleet, and whether ``robot_4`` is now empty.
    3. Write ``queue_if_low``. It takes the queue as a ``Fleet&``, a robot
       as a ``const std::shared_ptr<RobotStatus>&``, and a limit in percent.
       It adds the robot to the queue only when its battery is below the
       limit. Call it for every robot in the fleet with ``20.0``. Print the
       number of owners of each robot (``use_count()``) and the size of the
       queue.
    4. Make a ``std::weak_ptr<RobotStatus>`` that watches robot 3, the third
       robot in the fleet. Write ``show``. It takes the ``std::weak_ptr`` by
       ``const`` reference, and calls ``lock()``. It prints the robot's id
       and battery, or ``the robot is gone``.
    5. Robot 3 leaves the fleet. Call ``show``, erase robot 3 from the
       fleet, print the number of owners of robot 3, and call ``show``
       again. Then clear the charging queue, print the number of owners of
       robot 3, and call ``show`` one last time.
    6. The program must end with no LeakSanitizer report.

    Use these robots, in this order:

    .. code-block:: text

       robot 1 : 82.5 %
       robot 2 : 35.0 %
       robot 3 : 14.0 %
       robot 4 : 18.0 %

    **Example Output**

    Use two digits after the decimal point.

    .. code-block:: text

       ====================================
         Charging Queue
       ====================================

       Fleet
       ------------------------------------
         robot 1 :  82.50 %
         robot 2 :  35.00 %
         robot 3 :  14.00 %
         robot 4 :  18.00 %
         robot_4 == nullptr : true

       Owners
       ------------------------------------
         robot 1 : 1
         robot 2 : 1
         robot 3 : 2
         robot 4 : 2
         in the queue : 2

       Robot 3 Leaves
       ------------------------------------
         dashboard : robot 3,  14.00 %
         owners of robot 3 : 1
         dashboard : robot 3,  14.00 %
         owners of robot 3 : 0
         dashboard : the robot is gone
