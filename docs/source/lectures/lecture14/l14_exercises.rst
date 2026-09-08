====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 14: Lifecycle
Nodes. Work through them in order. The final challenge also uses the TF2
material from :doc:`Lecture 13 <../lecture13/l13_index>`. Build and run
each program in a ROS 2 workspace to verify your understanding.

.. note::

   All exercises require a ROS 2 Jazzy workspace. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1: Basic Lifecycle Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a lifecycle node with logging in each transition callback.

    **Specification**

    1. Create a lifecycle node called ``basic_lifecycle_node``.
    2. Inherit from ``rclcpp_lifecycle::LifecycleNode``.
    3. Implement all five transition callbacks:

       - ``on_configure``, log "Configuring..." and return SUCCESS.
       - ``on_activate``, log "Activating..." and return SUCCESS.
       - ``on_deactivate``, log "Deactivating..." and return SUCCESS.
       - ``on_cleanup``, log "Cleaning up..." and return SUCCESS.
       - ``on_shutdown``, log "Shutting down..." and return SUCCESS.

    4. Test using the CLI:

       .. code-block:: bash

          ros2 lifecycle set /basic_lifecycle_node configure
          ros2 lifecycle set /basic_lifecycle_node activate
          ros2 lifecycle set /basic_lifecycle_node deactivate
          ros2 lifecycle set /basic_lifecycle_node cleanup
          ros2 lifecycle set /basic_lifecycle_node shutdown

.. dropdown:: Exercise 2: Lifecycle Sensor Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a lifecycle sensor node that only publishes data when in the
    Active state.

    **Specification**

    1. Create a lifecycle node called ``lifecycle_temperature_sensor``.
    2. In ``on_configure``:

       - Create a ``LifecyclePublisher`` for ``std_msgs::msg::Float64``
         on topic ``/temperature``.
       - Create a timer that fires every 1 second.
       - Initialize a temperature value to 20.0.

    3. In ``on_activate``:

       - Log that the sensor is active and publishing.

    4. In ``on_deactivate``:

       - Log that the sensor has stopped publishing.

    5. In ``on_cleanup``:

       - Reset the publisher and timer.

    6. In ``on_shutdown``:

       - Reset the publisher and timer.

    7. In the timer callback:

       - Check if the node is in the Active state before publishing.
       - Publish the temperature value with a small random fluctuation.
       - Log the published value.

    8. Test: configure, activate, observe data, deactivate, verify data
       stops, re-activate, observe data resumes.

.. dropdown:: Exercise 3 Challenge: Multi-Frame Robot with Lifecycle Management
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete system that combines TF2 frame management with
    lifecycle node control. This exercise integrates all concepts from
    the lecture.

    **Specification**

    1. Create a **lifecycle node** called ``robot_system_node`` that
       manages a robot with sensors.

    2. In ``on_configure``:

       - Create a ``tf2_ros::StaticTransformBroadcaster`` and publish
         two static transforms:

         - ``base_link`` -> ``camera_link`` (0.15 m forward, 0.4 m up)
         - ``base_link`` -> ``lidar_link`` (0.0 m forward, 0.3 m up)

       - Create a ``tf2_ros::TransformBroadcaster`` for the robot's
         dynamic motion.
       - Create a ``LifecyclePublisher`` for ``std_msgs::msg::String``
         on topic ``/sensor_status``.
       - Create a timer at 10 Hz.

    3. In ``on_activate``:

       - Log that the robot system is active.
       - Set a flag ``active_`` to true.

    4. In ``on_deactivate``:

       - Set ``active_`` to false.
       - Log that the robot system is paused.

    5. In the timer callback:

       - If not active, return immediately.
       - Broadcast a dynamic transform from ``world`` to ``base_link``
         (robot moves in a figure-eight pattern):

         - ``x = 3.0 * sin(angle)``
         - ``y = 3.0 * sin(angle) * cos(angle)``

       - Publish a sensor status message with the current position.
       - Increment the angle.

    6. In ``on_cleanup`` and ``on_shutdown``:

       - Reset all publishers, broadcasters, and the timer.

    7. Test the full lifecycle: configure -> activate -> observe frames
       and messages -> deactivate -> verify publishing stops -> activate
       again -> shutdown.

    8. Use ``ros2 run tf2_tools view_frames`` to verify the frame tree.
