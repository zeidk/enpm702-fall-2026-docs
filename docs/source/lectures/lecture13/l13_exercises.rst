====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 13: Coordinate
Frames and Transforms (TF2). Work through them in order, as each exercise
builds on the previous one. Build and run each program in a ROS 2
workspace to verify your understanding.

.. note::

   All exercises require a ROS 2 Jazzy workspace. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1: Static Transform Broadcaster
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Broadcast a static transform from ``base_link`` to ``camera_link``.

    **Specification**

    1. Create a ROS 2 node called ``static_camera_broadcaster``.
    2. Use ``tf2_ros::StaticTransformBroadcaster`` to publish a static
       transform from ``base_link`` to ``camera_link``.
    3. The camera is positioned 0.2 m forward (x), 0.0 m to the side (y),
       and 0.5 m above (z) the base_link.
    4. The camera has no rotation relative to base_link (identity
       quaternion).
    5. Log a message confirming the transform was published.
    6. Verify with: ``ros2 run tf2_ros tf2_echo base_link camera_link``

.. dropdown:: Exercise 2: Dynamic Transform Broadcaster (Circular Path)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Broadcast a dynamic transform that moves a robot in a circular path
    in the world frame.

    **Specification**

    1. Create a ROS 2 node called ``circular_motion_broadcaster``.
    2. Use ``tf2_ros::TransformBroadcaster`` to publish the transform
       from ``world`` to ``base_link`` at 10 Hz.
    3. The robot should move in a circle of radius 2.0 m centered at the
       origin:

       - ``x = 2.0 * cos(angle)``
       - ``y = 2.0 * sin(angle)``
       - ``z = 0.0``

    4. Increment the angle by 0.05 radians each timer callback.
    5. Set the rotation quaternion to represent the robot facing the
       direction of travel (yaw = angle + pi/2). For simplicity, you may
       use an identity quaternion.
    6. Verify with: ``ros2 run tf2_ros tf2_echo world base_link``

.. dropdown:: Exercise 3: Transform Listener (Distance Computation)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Listen for transforms and compute the distance between two frames.

    **Specification**

    1. Create a ROS 2 node called ``distance_calculator``.
    2. Use ``tf2_ros::Buffer`` and ``tf2_ros::TransformListener`` to
       listen for transforms.
    3. Every second, look up the transform from ``world`` to
       ``camera_link``.
    4. Compute the Euclidean distance from the world origin to the
       camera_link frame:

       - ``distance = sqrt(x^2 + y^2 + z^2)``

    5. Log the distance.
    6. Handle ``tf2::TransformException`` with a warning message.
    7. Test by running the circular motion broadcaster (Exercise 2) and
       the static camera broadcaster (Exercise 1) simultaneously.
