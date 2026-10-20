====================================================
C++ Exercises
====================================================

This exercise covers Lecture 7: Smart Pointers and Move Semantics. There is
one exercise this week, and it is graded: hand it in on Canvas before
L8.

The exercise works on the sensors of a mobile robot. A sensor manager owns
every sensor, a fusion list shares the sensors fast enough to fuse, and a
logger watches one sensor without keeping it alive.

.. note::

   Build the exercise from VS Code with CMake, as in the lecture. Add a
   target for it to ``project/week7/CMakeLists.txt``:

   .. code-block:: cmake

      add_executable(week7_sensors exercises/sensors.cpp)
      target_compile_options(week7_sensors PRIVATE -fsanitize=address)
      target_link_options(week7_sensors PRIVATE -fsanitize=address)

   ``-fsanitize=address`` turns on LeakSanitizer, so a leak is reported
   when the program ends. The course project already turns on the
   warnings, so fix every warning before you submit.

   Format the output as in the **Example Output**: a title between two lines
   of ``=``, and each part under a heading underlined with ``-``, with the
   numbers in aligned columns.


----


.. dropdown:: Exercise 1: The Sensor Manager
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use the three smart pointers of L7 in one short program: a factory that
    returns a ``std::unique_ptr``, a manager and a fusion list that share
    sensors through ``std::shared_ptr``, and a logger that watches a sensor
    through a ``std::weak_ptr``.

    **Specification**

    Write one program, ``project/week7/exercises/sensors.cpp``, with the
    target ``week7_sensors``. Write no ``new`` and no ``delete``.

    1. Declare a ``struct Sensor`` with four members: ``id`` (an ``int``),
       ``name`` (a ``std::string``), ``rate_hz`` (a ``double``, how many
       readings per second) and ``active`` (a ``bool``). Give ``id``,
       ``rate_hz`` and ``active`` the defaults ``0``, ``0.0`` and ``false``.
    2. Write ``make_sensor``. It takes an id, a name and a rate, and returns
       a ``std::unique_ptr<Sensor>`` made with ``std::make_unique``, with
       ``active`` set to ``true``.
    3. Declare ``using Sensors = std::vector<std::shared_ptr<Sensor>>;``.
       Put sensors 1, 2 and 3 into the manager straight from
       ``make_sensor``. Create sensor 4 in a variable ``gps``, then move it
       into the manager. Print the manager, and whether ``gps`` is now
       empty.
    4. Write ``add_if_fast``. It takes the fusion list as a ``Sensors&``, a
       sensor as a ``const std::shared_ptr<Sensor>&``, and a rate in Hz. It
       adds the sensor to the fusion list only when its rate is at least that
       rate. Call it for every sensor in the manager with ``10.0``. Print the
       number of owners of each sensor (``use_count()``) and the size of the
       fusion list.
    5. Make a ``std::weak_ptr<Sensor>`` named ``logger`` that watches sensor
       2, the second sensor in the manager. Write ``show``. It takes the
       ``std::weak_ptr`` by ``const`` reference, and calls ``lock()``. It
       prints the sensor's name and rate, or ``the sensor is gone``.
    6. The camera is removed. Call ``show``, erase sensor 2 from the manager,
       print the number of owners of the camera, and call ``show`` again.
       Then clear the fusion list, print the number of owners of the camera,
       and call ``show`` one last time.
    7. The program must end with no LeakSanitizer report.

    Use these sensors, in this order:

    .. code-block:: text

       id  name    rate (Hz)
       1   lidar    10.0
       2   camera   30.0
       3   imu     100.0
       4   gps       1.0

    **Example Output**

    Use two digits after the decimal point.

    .. code-block:: text

       ====================================
         The Sensor Manager
       ====================================

       Manager
       ------------------------------------
         sensor 1 : lidar   10.00 Hz
         sensor 2 : camera  30.00 Hz
         sensor 3 : imu    100.00 Hz
         sensor 4 : gps      1.00 Hz
         gps == nullptr : true

       Owners
       ------------------------------------
         sensor 1 : 2
         sensor 2 : 2
         sensor 3 : 2
         sensor 4 : 1
         in the fusion list : 3

       The Camera Is Removed
       ------------------------------------
         logger : camera  30.00 Hz
         owners of the camera : 1
         logger : camera  30.00 Hz
         owners of the camera : 0
         logger : the sensor is gone
