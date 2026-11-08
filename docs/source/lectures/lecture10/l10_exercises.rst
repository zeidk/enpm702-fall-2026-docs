====================================================
ROS Exercises
====================================================

These exercises use the package ``robotaxi_demo`` of the lecture, in your own workspace. Exercise 3 uses the battery topic that Exercise 2 adds.

.. note::

   Build and run from the workspace's top folder:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select robotaxi_demo
      source install/setup.bash


----


.. dropdown:: Exercise 1: Test the Dispatcher from the Terminal
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Test a subscriber before its publisher runs (rule 4), and check its arithmetic.

    **Specification**

    1. Run only the dispatcher: ``ros2 run robotaxi_demo dispatcher``.
    2. Before you send each message below, compute the line the dispatcher will print. Its pickup point is at x = 10 m, y = 0 m. Write the steps, as the lecture does for ``{x: 7.0, y: 4.0}``.

       - ``{x: 4.0, y: 8.0}``
       - ``{x: 13.0, y: 4.0}``

    3. Send each one with ``ros2 topic pub --once /robotaxi/position geometry_msgs/msg/Point "<fields>"``, and compare the printed line with your result.
    4. Send ``{x: 2.0}`` with no ``y``. Which value does ``y`` take, and what does the dispatcher print?

.. dropdown:: Exercise 2: A Second Topic for the Battery
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Give one node a second publisher on its own topic (pattern 3), with a message package the package does not use yet.

    **Specification**

    1. Add ``std_msgs`` to ``robotaxi_demo`` in both build files: a ``<depend>`` line in ``package.xml``, and a ``find_package`` line and the ``ament_target_dependencies`` entry for ``robotaxi`` in ``CMakeLists.txt``.
    2. In ``RoboTaxiNode``, add a second publisher of ``std_msgs::msg::Float64`` on the topic ``robotaxi/battery``, queue size 10, kept in a data member.
    3. Add a data member ``battery_`` that starts at 100.0. In ``publish_position``, publish ``battery_`` on the new topic, then lower it by 0.5.
    4. Build, source and run the robotaxi. Check both topics with ``ros2 topic list -t`` and ``ros2 topic hz``. What rate does each one have, and why?
    5. Run the dispatcher too. Does it receive battery messages? Say why, with the lecture's pattern 3.

.. dropdown:: Exercise 3: A Battery Monitor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a subscriber of your own, with a callback that decides what to log.

    **Specification**

    1. In ``robotaxi_demo``, write a class ``BatteryMonitorNode`` named ``battery_monitor``, in a header and a ``.cpp`` file, with its own ``main``. It subscribes to ``robotaxi/battery`` (``std_msgs::msg::Float64``, queue size 10), with a lambda that calls a method ``on_battery``.
    2. ``on_battery`` logs the level with ``RCLCPP_INFO_STREAM`` when it is 20.0 or more, and with ``RCLCPP_WARN_STREAM`` when it is below 20.0.
    3. Add the executable ``battery_monitor`` to ``CMakeLists.txt``, build and run it with the robotaxi of Exercise 2.
    4. Before you run it, compute how long after the robotaxi starts the first warning appears, and the level it shows. Then measure it from the log times.
