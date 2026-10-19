====================================================
C++ Exercises
====================================================

This exercise covers Lecture 7: Smart Pointers and Move Semantics. There is
one exercise this week, and it is graded: hand it in on Canvas before
L8.

The exercise works on the software of the autonomous car from the lecture.
Four obstacles are on the heap. The tracker owns every obstacle, the
planner's hazard list shares the obstacles near the ego vehicle, and a
dashboard watches one obstacle without keeping it alive.

.. note::

   Build the exercise from VS Code with CMake, as in the lecture. Add a
   target for it to ``project/week7/CMakeLists.txt``:

   .. code-block:: cmake

      add_executable(week7_hazards exercises/hazards.cpp)
      target_include_directories(week7_hazards PRIVATE common)
      target_compile_options(week7_hazards PRIVATE -fsanitize=address)
      target_link_options(week7_hazards PRIVATE -fsanitize=address)

   The ``common`` folder holds ``obstacle.hpp``, with ``Pose`` and
   ``Obstacle``. ``-fsanitize=address`` turns on LeakSanitizer, so a leak
   is reported when the program ends. The course project already turns on
   the warnings, so fix every warning before you submit.

   Format the output as in the **Example Output**: a title between two lines
   of ``=``, and each part under a heading underlined with ``-``, with the
   numbers in aligned columns.


----


.. dropdown:: Exercise 1: The Hazard List
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use the three smart pointers of L7 in one short program: a
    factory that returns a ``std::unique_ptr``, a tracker and a hazard list
    that share obstacles through ``std::shared_ptr``, and a dashboard that
    watches an obstacle through a ``std::weak_ptr``.

    **Specification**

    Write one program, ``project/week7/exercises/hazards.cpp``, with the
    target ``week7_hazards``. Include ``obstacle.hpp`` and use its
    ``Obstacle`` as it is. Write no ``new`` and no ``delete``.

    1. Write ``make_track``. It takes an id, a ``Pose``, a speed in m/s and
       whether the obstacle is static, and returns a
       ``std::unique_ptr<Obstacle>`` made with ``std::make_unique``.
    2. Declare ``using Tracker = std::vector<std::shared_ptr<Obstacle>>;``.
       Put obstacles 1, 2 and 3 into the tracker straight from
       ``make_track``. Create obstacle 4 in a variable ``track_4``, then move
       it into the tracker. Print the tracker, and whether ``track_4`` is now
       empty.
    3. Write ``add_if_close``. It takes the hazard list as a ``Tracker&``, an
       obstacle as a ``const std::shared_ptr<Obstacle>&``, and a limit in
       meters. It adds the obstacle to the hazard list only when its ``x`` is
       less than the limit. Call it for every obstacle in the tracker with
       ``25.0``. Print the number of owners of each obstacle
       (``use_count()``) and the size of the hazard list.
    4. Make a ``std::weak_ptr<Obstacle>`` that watches obstacle 2, the second
       obstacle in the tracker. Write ``show``. It takes the
       ``std::weak_ptr`` by ``const`` reference, and calls ``lock()``. It
       prints the obstacle's id and speed, or ``the obstacle is gone``.
    5. The tracker loses obstacle 2. Call ``show``, erase obstacle 2 from the
       tracker, print the number of owners of obstacle 2, and call ``show``
       again. Then clear the hazard list, print the number of owners of
       obstacle 2, and call ``show`` one last time.
    6. The program must end with no LeakSanitizer report.

    Use these obstacles, in this order (the table of the lecture):

    .. code-block:: text

       id  x (m)  y (m)  heading (rad)  speed (m/s)  static
       1   20.0   -3.0   0.00            0.0         yes
       2   12.0   -1.0   0.00            4.0         no
       3   30.0    2.5   1.57            1.4         no
       4   38.0    3.5   3.14           13.4         no

    **Example Output**

    Use two digits after the decimal point.

    .. code-block:: text

       ====================================
         The Hazard List
       ====================================

       Tracker
       ------------------------------------
         obstacle 1 : x  20.00 m,   0.00 m/s
         obstacle 2 : x  12.00 m,   4.00 m/s
         obstacle 3 : x  30.00 m,   1.40 m/s
         obstacle 4 : x  38.00 m,  13.40 m/s
         track_4 == nullptr : true

       Owners
       ------------------------------------
         obstacle 1 : 2
         obstacle 2 : 2
         obstacle 3 : 1
         obstacle 4 : 1
         in the hazard list : 2

       Obstacle 2 Is Lost
       ------------------------------------
         dashboard : obstacle 2,   4.00 m/s
         owners of obstacle 2 : 1
         dashboard : obstacle 2,   4.00 m/s
         owners of obstacle 2 : 0
         dashboard : the obstacle is gone
