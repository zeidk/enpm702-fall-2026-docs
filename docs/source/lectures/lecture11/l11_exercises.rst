====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 11: ROS 2
Configuration and Orchestration. Work through them in order, as each exercise
builds on the skills from the previous one. Build and run each program in a
ROS 2 workspace to verify your understanding.

.. note::

   Build all ROS 2 packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1: Parameterized Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring and retrieving parameters on a ROS 2 node.

    **Specification**

    1. Create a node called ``param_demo_node`` that inherits from ``rclcpp::Node``.

    2. In the constructor, declare the following parameters with default values:

       - ``robot_name`` (string): ``"default_robot"``
       - ``max_speed`` (double): ``1.0``
       - ``num_sensors`` (int): ``3``
       - ``verbose`` (bool): ``false``

    3. Retrieve each parameter value using ``get_parameter()`` and log them
       with ``RCLCPP_INFO``.

    4. Create a timer (1-second period) that logs the robot name and speed
       each tick.

    5. Test by running:

       .. code-block:: bash

          ros2 run my_package param_demo_node --ros-args -p robot_name:=atlas -p max_speed:=2.5

.. dropdown:: Exercise 2: Dynamic Parameter Update
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Add a parameter callback that logs and validates parameter changes at
    runtime.

    **Specification**

    1. Start from the node in Exercise 1.

    2. Add a parameter callback using ``add_on_set_parameters_callback`` that:

       - Logs the name and new value of every parameter that changes.
       - Rejects ``max_speed`` values that are negative or greater than ``10.0``.
       - Updates the member variables (``robot_name_``, ``max_speed_``) when
         the change is accepted.

    3. Store the callback handle as a class member.

    4. Test by running the node, then in another terminal:

       .. code-block:: bash

          ros2 param set /param_demo_node max_speed 5.0
          ros2 param set /param_demo_node max_speed -1.0
          ros2 param set /param_demo_node robot_name optimus

    5. Verify that the timer output reflects accepted changes and that the
       negative speed is rejected.

.. dropdown:: Exercise 3: Basic Launch File
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a Python launch file that starts two nodes simultaneously.

    **Specification**

    1. Create a ``launch/`` directory in your package.

    2. Write a ``demo.launch.py`` file that starts two instances of your
       ``param_demo_node`` with different names:

       - Node 1: name ``robot_a``, parameter ``robot_name`` set to ``"alpha"``
       - Node 2: name ``robot_b``, parameter ``robot_name`` set to ``"beta"``

    3. Add the ``install(DIRECTORY launch/ ...)`` directive to your
       ``CMakeLists.txt``.

    4. Build and test:

       .. code-block:: bash

          colcon build --packages-select my_package
          source install/setup.bash
          ros2 launch my_package demo.launch.py

    5. In another terminal, verify both nodes are running:

       .. code-block:: bash

          ros2 node list

.. dropdown:: Exercise 4: Launch with Parameters and YAML
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Pass parameters via a YAML configuration file and use launch arguments to
    make the launch file configurable.

    **Specification**

    1. Create a ``config/params.yaml`` file with the following content:

       .. code-block:: yaml

          robot_a:
            ros__parameters:
              robot_name: "alpha"
              max_speed: 2.0

          robot_b:
            ros__parameters:
              robot_name: "beta"
              max_speed: 3.5

    2. Write a ``system.launch.py`` that:

       - Declares a launch argument ``config_file`` with a default value
         pointing to your YAML file.
       - Starts ``robot_a`` and ``robot_b`` using parameters from the YAML
         file.

    3. Add the ``config/`` directory to your ``CMakeLists.txt`` install rules.

    4. Build and test:

       .. code-block:: bash

          ros2 launch my_package system.launch.py

    5. Override the config file from the command line:

       .. code-block:: bash

          ros2 launch my_package system.launch.py config_file:=/path/to/other.yaml

.. dropdown:: Exercise 5: Multi-Threaded Executor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a node that uses a ``MultiThreadedExecutor`` with callback groups
    to allow concurrent execution of a timer and a subscription.

    **Specification**

    1. Create a node called ``multi_executor_node``.

    2. Create two callback groups:

       - A **mutually exclusive** group for a timer.
       - A **reentrant** group for a subscription.

    3. Create a timer (1-second period) in the exclusive group that:

       - Simulates heavy work with ``std::this_thread::sleep_for(2s)``.
       - Logs the thread ID.

    4. Create a subscription to ``/chatter`` (``std_msgs::msg::String``) in
       the reentrant group that:

       - Logs the received message and thread ID.

    5. In ``main()``, use a ``MultiThreadedExecutor`` instead of
       ``rclcpp::spin()``.

    6. Test:

       - Run the node.
       - In another terminal: ``ros2 topic pub /chatter std_msgs/msg/String "{data: 'hello'}" -r 2``
       - Observe that subscription callbacks are not blocked by the
         long-running timer callback.

.. dropdown:: Exercise 6 Challenge: Configurable Robot System
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete, configurable multi-node robot system that brings
    together parameters, YAML configuration, launch files, and executors.

    **Specification**

    1. Create two node types:

       **SensorNode** (``sensor_node.cpp``):

       - Declares parameters: ``sensor_name`` (string), ``publish_rate_ms`` (int),
         ``noise_level`` (double).
       - Publishes ``std_msgs::msg::Float64`` on a topic ``/<sensor_name>/data``
         at the configured rate.
       - The published value is a simulated reading: a base value plus random
         noise scaled by ``noise_level``.
       - Has a parameter callback that accepts runtime changes to
         ``noise_level`` (must be >= 0).

       **MonitorNode** (``monitor_node.cpp``):

       - Declares parameters: ``sensor_names`` (string array), ``threshold`` (double).
       - Subscribes to each sensor's topic.
       - Uses a ``MultiThreadedExecutor`` with a reentrant callback group
         for all subscriptions.
       - Logs a warning when any reading exceeds ``threshold``.

    2. Create a ``config/robot_system.yaml``:

       .. code-block:: yaml

          lidar_sensor:
            ros__parameters:
              sensor_name: "lidar"
              publish_rate_ms: 200
              noise_level: 0.5

          camera_sensor:
            ros__parameters:
              sensor_name: "camera"
              publish_rate_ms: 100
              noise_level: 0.3

          monitor:
            ros__parameters:
              sensor_names:
                - "lidar"
                - "camera"
              threshold: 8.0

    3. Create a ``launch/robot_system.launch.py`` that:

       - Declares a ``config_file`` launch argument.
       - Starts two ``SensorNode`` instances (``lidar_sensor`` and
         ``camera_sensor``) with parameters from the YAML file.
       - Starts one ``MonitorNode`` (``monitor``) with parameters from the
         YAML file.

    4. Build, launch, and verify:

       - Both sensors publish data.
       - The monitor subscribes and logs warnings when thresholds are
         exceeded.
       - Change ``noise_level`` at runtime:

         .. code-block:: bash

            ros2 param set /lidar_sensor noise_level 5.0
