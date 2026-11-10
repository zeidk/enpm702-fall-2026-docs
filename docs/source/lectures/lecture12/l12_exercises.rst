====================================================
ROS Exercise
====================================================

This exercise brings together the three communication patterns of
Lecture 12: topics, services and actions.

.. note::

   Build all packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-select <package_name>
      source install/setup.bash

.. note::

   **Naming.** A node's name ends with ``_node`` and its executable's name
   with ``_exe``. A node class lives in ``<name>_node.hpp`` and
   ``<name>_node.cpp``, and its ``main`` in ``<name>_main.cpp``.

----


.. dropdown:: Exercise: Integrated Communication System
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a system that uses all three communication patterns working
    together.

    **Specification**

    Design and implement a multi-node system with the following
    components:

    1. **Sensor Publisher** (topic): a node that publishes simulated
       battery level (``std_msgs/msg/Float64``) on ``/battery_level``
       at 2 Hz. The level starts at 100.0 and decreases by 1.0 each
       publication.

    2. **Status Service** (service): a node that provides a
       ``/get_status`` service using ``std_srvs/srv/Trigger``. When
       called, it returns ``success = true`` and a message with the
       current system status (e.g., ``"System OK"``).

    3. **Patrol Action** (action): in a package ``robot_interfaces``,
       define ``action/Patrol.action``:

       - **Goal**: ``int32 num_waypoints``, how many waypoints to visit.
       - **Result**: ``bool success`` and ``string message``.
       - **Feedback**: ``int32 current_waypoint``, the waypoint
         currently being visited.

       Write a node ``patrol_server_node`` that serves ``/patrol``. It rejects
       goals where ``num_waypoints <= 0``, visits each waypoint with a
       1-second delay, and publishes the current waypoint as feedback.
       Before it starts a patrol, it calls the ``/get_status`` service to
       check the system status. If the service returns
       ``success = false``, it aborts the goal.

    4. **Coordinator** (action client + subscriber): a node that:

       - Subscribes to ``/battery_level``.
       - When battery drops below 50.0, sends a patrol goal to
         ``/patrol`` with 3 waypoints.
       - Logs feedback as it arrives.
       - Logs the final result.

    5. Use a launch file to start all four nodes.
