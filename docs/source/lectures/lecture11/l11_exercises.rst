====================================================
ROS Exercise
====================================================

This exercise brings together the concepts of Lecture 11: parameters,
YAML configuration, launch files and executors.

.. note::

   Build all ROS 2 packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-select my_package
      source install/setup.bash

.. note::

   **Naming.** A node's name ends with ``_node`` and its executable's name
   with ``_exe``. A node class lives in ``<name>_node.hpp`` and
   ``<name>_node.cpp``, and its ``main`` in ``<name>_main.cpp``.

----


.. dropdown:: Exercise: Configurable Robot System
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete, configurable multi-node robot system that brings
    together parameters, YAML configuration, launch files, and executors.

    **Specification**

    1. Create two node types:

       **SensorNode** (``sensor_node.hpp``, ``sensor_node.cpp``; executable ``sensor_exe``):

       - Declares parameters: ``sensor_name`` (string), ``publish_rate_ms`` (int),
         ``noise_level`` (double).
       - Publishes ``std_msgs::msg::Float64`` on a topic ``/<sensor_name>/data``
         at the configured rate.
       - The published value is a simulated reading: a base value plus random
         noise scaled by ``noise_level``.
       - Has a parameter callback that accepts runtime changes to
         ``noise_level`` (must be >= 0).

       **MonitorNode** (``monitor_node.hpp``, ``monitor_node.cpp``; executable ``monitor_exe``):

       - Declares parameters: ``sensor_names`` (string array), ``threshold`` (double).
       - Subscribes to each sensor's topic.
       - Uses a ``MultiThreadedExecutor`` with a reentrant callback group
         for all subscriptions.
       - Logs a warning when any reading exceeds ``threshold``.

    2. Create a ``config/robot_system.yaml``:

       .. code-block:: yaml

          lidar_sensor_node:
            ros__parameters:
              sensor_name: "lidar"
              publish_rate_ms: 200
              noise_level: 0.5

          camera_sensor_node:
            ros__parameters:
              sensor_name: "camera"
              publish_rate_ms: 100
              noise_level: 0.3

          monitor_node:
            ros__parameters:
              sensor_names:
                - "lidar"
                - "camera"
              threshold: 8.0

    3. Create a ``launch/robot_system.launch.py`` that:

       - Declares a ``config_file`` launch argument.
       - Starts two ``SensorNode`` instances (``lidar_sensor_node`` and
         ``camera_sensor_node``) with parameters from the YAML file.
       - Starts one ``MonitorNode`` (``monitor_node``) with parameters from the
         YAML file.

    4. Build, launch, and verify:

       - Both sensors publish data.
       - The monitor subscribes and logs warnings when thresholds are
         exceeded.
       - Change ``noise_level`` at runtime:

         .. code-block:: bash

            ros2 param set /lidar_sensor_node noise_level 5.0
