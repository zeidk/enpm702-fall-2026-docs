====================================================
ROS Exercise
====================================================

This exercise uses the package ``robotaxi_demo`` of the lecture, in your own workspace.

.. note::

   Build and run from the workspace's top folder:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select robotaxi_demo
      source install/setup.bash


----


.. dropdown:: Exercise: A Battery Topic and Its Monitor
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Give the robotaxi a second topic for its battery (pattern 3), with a message package the package does not use yet. Then write a subscriber of your own, with a callback that decides what to log.

    **Specification**

    1. Add ``std_msgs`` to ``robotaxi_demo`` in both build files: a ``<depend>`` line in ``package.xml``, and a ``find_package`` line and the ``ament_target_dependencies`` entry for ``robotaxi_exe`` in ``CMakeLists.txt``.
    2. In ``RoboTaxiNode``, add a second publisher of ``std_msgs::msg::Float64`` on the topic ``robotaxi/battery``, queue size 10, kept in a data member.
    3. Add a data member ``battery_`` that starts at 100.0. In ``publish_position``, publish ``battery_`` on the new topic, then lower it by 0.5.
    4. Build, source and run the robotaxi. Check both topics with ``ros2 topic list -t`` and ``ros2 topic hz``. What rate does each one have, and why?
    5. In ``robotaxi_demo``, write a class ``BatteryMonitorNode`` named ``battery_monitor_node``, in ``battery_monitor_node.hpp`` and ``battery_monitor_node.cpp``, with its own ``main`` in ``battery_monitor_main.cpp``. It subscribes to ``robotaxi/battery`` (``std_msgs::msg::Float64``, queue size 10), with ``std::bind`` (or a lambda) that calls a method ``on_battery``.
    6. ``on_battery`` logs the level with ``RCLCPP_INFO_STREAM`` when it is 20.0 or more, and with ``RCLCPP_WARN_STREAM`` when it is below 20.0.
    7. Add the executable ``battery_monitor_exe`` to ``CMakeLists.txt``, build and run it with the robotaxi.
    8. Before you run it, compute how long after the robotaxi starts the first warning appears, and the level it shows. Then measure it from the log times.
