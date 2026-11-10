====================================================
ROS Exercise
====================================================

This exercise uses the concepts of Lecture 13: Coordinate Frames and
Transforms (TF2). Build and run the program in a ROS 2 workspace.

.. note::

   The exercise requires a ROS 2 Jazzy workspace. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash

.. note::

   **Naming.** A node's name ends with ``_node`` and its executable's name
   with ``_exe``. A node class lives in ``<name>_node.hpp`` and
   ``<name>_node.cpp``, and its ``main`` in ``<name>_main.cpp``.

----


.. dropdown:: Exercise: Transform Listener (Distance Computation)
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Listen for transforms and compute the distance between two frames.

    **Specification**

    1. Create a ROS 2 node called ``distance_calculator_node``.
    2. Use ``tf2_ros::Buffer`` and ``tf2_ros::TransformListener`` to
       listen for transforms.
    3. Every second, look up the transform from ``world`` to
       ``camera_link``.
    4. Compute the Euclidean distance from the world origin to the
       camera_link frame:

       - ``distance = sqrt(x^2 + y^2 + z^2)``

    5. Log the distance.
    6. Handle ``tf2::TransformException`` with a warning message.
    7. Test it without writing a broadcaster: in two other terminals,
       publish two static transforms with the ``tf2_ros`` command-line
       tool. The robot stands 2.0 m along x from the world origin, and the
       camera sits 0.2 m forward and 0.5 m above the robot.

       .. code-block:: bash

          ros2 run tf2_ros static_transform_publisher --x 2.0 --frame-id world --child-frame-id base_link
          ros2 run tf2_ros static_transform_publisher --x 0.2 --z 0.5 --frame-id base_link --child-frame-id camera_link

    8. Before you run your node, compute the distance it should log. Then
       compare it with the logged value.
