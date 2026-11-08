====================================================
C++ Exercises
====================================================

These exercises use the package ``robotaxi_demo`` of the lecture, in your own workspace. Work through them in order: each one uses what the one before built.

.. note::

   Build and run from the workspace's top folder:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select robotaxi_demo
      source install/setup.bash


----


.. dropdown:: Exercise 1: Inspect the Talker and the Listener
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use the ``ros2`` command-line tools on two nodes that come with ROS 2, and see rule 3 at work.

    **Specification**

    1. In terminal 1, run ``ros2 run demo_nodes_cpp talker``. Wait a few seconds, then run ``ros2 run demo_nodes_cpp listener`` in terminal 2.
    2. Write down the number of the listener's first message, and say why it is not 1.
    3. In terminal 3, run ``ros2 node list``, ``ros2 topic list -t``, ``ros2 topic info /chatter``, ``ros2 topic echo /chatter`` and ``ros2 topic hz /chatter``. Write down what each prints.
    4. Stop the listener with :kbd:`Ctrl+C` and start it again. Does the talker notice? Which message does the listener print first this time?
    5. Run ``rqt_graph`` and compare its window with the talker and listener figure of the lecture.

.. dropdown:: Exercise 2: A Node as a Class
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a node as a class, build it with ``colcon``, and see what happens when two nodes share a name.

    **Specification**

    1. In ``robotaxi_demo``, write a class ``GreeterNode`` that derives from ``rclcpp::Node``, in ``include/robotaxi_demo/greeter_node.hpp``, inside ``namespace robotaxi_demo``. The node's name is ``greeter``.
    2. In the constructor, log one line at each level, from ``RCLCPP_DEBUG_STREAM`` to ``RCLCPP_FATAL_STREAM``. Each line says its level and the node's name (``get_name()``).
    3. Write ``src/greeter_main.cpp`` with the spinning pattern of the lecture.
    4. Add the ``add_executable``, ``ament_target_dependencies`` and ``install`` lines for an executable named ``greeter`` to ``CMakeLists.txt``.
    5. Build, source and run ``ros2 run robotaxi_demo greeter``. Which level does not print, and why?
    6. Run a second ``greeter`` in another terminal, then ``ros2 node list`` in a third. Write down the warning, and say how to avoid it.

.. dropdown:: Exercise 3: Test the Dispatcher from the Terminal
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

.. dropdown:: Exercise 4: A Second Topic for the Battery
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

.. dropdown:: Exercise 5: A Battery Monitor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a subscriber of your own, with a callback that decides what to log.

    **Specification**

    1. In ``robotaxi_demo``, write a class ``BatteryMonitorNode`` named ``battery_monitor``, in a header and a ``.cpp`` file, with its own ``main``. It subscribes to ``robotaxi/battery`` (``std_msgs::msg::Float64``, queue size 10), with a lambda that calls a method ``on_battery``.
    2. ``on_battery`` logs the level with ``RCLCPP_INFO_STREAM`` when it is 20.0 or more, and with ``RCLCPP_WARN_STREAM`` when it is below 20.0.
    3. Add the executable ``battery_monitor`` to ``CMakeLists.txt``, build and run it with the robotaxi of Exercise 4.
    4. Before you run it, compute how long after the robotaxi starts the first warning appears, and the level it shows. Then measure it from the log times.

.. dropdown:: Exercise 6: Reproduce the Slow Subscriber
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal** *(Challenge)*

    Measure scenario 3 of the lecture yourself, then change one setting and predict the result before you measure it.

    **Specification**

    1. Make a test copy of the dispatcher, ``slow_dispatcher``, with a queue size of 3. At the start of its callback, sleep 1.7 s with ``std::this_thread::sleep_for``.
    2. Start ``slow_dispatcher``, then the robotaxi. Stop both after 11 s.
    3. List the positions the dispatcher handled, and compare them with the lecture: x = 0, 1, 4, 8, 11, 15 and 18. Explain each position that is missing.
    4. Change the queue size to 10. Before you run it, predict which positions it handles in 11 s and how old the last one is. Then measure, and compare.
    5. The lecture says a larger queue only delays the loss. Use your two runs to say why.
