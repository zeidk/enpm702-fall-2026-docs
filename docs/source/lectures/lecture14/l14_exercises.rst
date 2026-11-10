====================================================
ROS Exercise
====================================================

This exercise turns the lecture's one-node reactive controller into a
two-layer architecture: a perception node and a decision node.

.. note::

   The exercise requires a ROS 2 Jazzy workspace and assumes a
   TurtleBot3-style robot (or Gazebo simulation) exposing ``/scan`` and
   ``/cmd_vel``. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash

.. note::

   **Naming.** A node's name ends with ``_node`` and its executable's name
   with ``_exe``. A node class lives in ``<name>_node.hpp`` and
   ``<name>_node.cpp``, and its ``main`` in ``<name>_main.cpp``.

----


.. dropdown:: Exercise: Separate Perception from Decision
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Split the lecture's ``ReactiveController`` into a **perception node**
    and a **decision node** connected by a topic, a true two-layer
    architecture.

    **Specification**

    1. **Perception node** ``obstacle_perception_node``: subscribe to
       ``/scan``, compute whether an obstacle is within 0.5 m anywhere in
       the scan, and publish a ``std_msgs::msg::Bool`` on
       ``/obstacle_ahead``.
    2. **Decision node** ``obstacle_decision_node``: subscribe to
       ``/obstacle_ahead`` and publish ``/cmd_vel``, turn if ``true``,
       drive forward if ``false``.
    3. Run both nodes together and confirm the robot behaves as before.
