====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 12: ROS 2
Communication Patterns (Services and Actions). Work through them in
order, as each exercise builds on the skills from the previous one.
Write, compile, and run each program to verify your understanding.

.. note::

   Build all packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-select <package_name>
      source install/setup.bash


----


.. dropdown:: Exercise 1: Custom Service Definition
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice defining a custom ``.srv`` file and building it as a ROS 2
    interface.

    **Specification**

    1. Create an interface package called ``robot_interfaces``:

       .. code-block:: bash

          ros2 pkg create --build-type ament_cmake robot_interfaces

    2. Inside the package, create a ``srv/`` directory and add a file
       ``RobotCommand.srv`` with the following definition:

       - **Request**: a ``string`` field ``command`` and a ``float64``
         field ``value``.
       - **Response**: a ``bool`` field ``success`` and a ``string``
         field ``message``.

    3. Update ``CMakeLists.txt`` and ``package.xml`` so the interface is
       generated.

    4. Build the package and verify the interface exists:

       .. code-block:: bash

          ros2 interface show robot_interfaces/srv/RobotCommand

.. dropdown:: Exercise 2: Service Server
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a service server that processes robot commands.

    **Specification**

    1. Create a package ``robot_service`` that depends on ``rclcpp`` and
       ``robot_interfaces``.

    2. Write a node ``command_server`` that:

       - Advertises a service ``/robot_command`` of type
         ``robot_interfaces/srv/RobotCommand``.
       - Handles the following commands:

         - ``"move"``: responds with ``success = true`` and
           ``message = "Moving at <value> m/s"``.
         - ``"stop"``: responds with ``success = true`` and
           ``message = "Robot stopped"``.
         - Any other command: responds with ``success = false`` and
           ``message = "Unknown command: <command>"``.

    3. Build, run, and test with:

       .. code-block:: bash

          ros2 service call /robot_command robot_interfaces/srv/RobotCommand \
            "{command: 'move', value: 1.5}"

.. dropdown:: Exercise 3: Service Client
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a service client node that sends commands to the server from
    Exercise 2.

    **Specification**

    1. In the same ``robot_service`` package, write a node
       ``command_client`` that:

       - Creates a client for ``/robot_command``.
       - Waits for the service to become available.
       - Sends a ``"move"`` command with ``value = 2.0``.
       - Prints the response ``success`` and ``message`` fields.

    2. Run the server in one terminal and the client in another.
       Verify the output.

.. dropdown:: Exercise 4: Custom Action Definition
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Define a custom ``.action`` file for a robot patrol task.

    **Specification**

    1. In the ``robot_interfaces`` package, create an ``action/``
       directory and add ``Patrol.action``:

       - **Goal**: ``int32 num_waypoints``, how many waypoints to visit.
       - **Result**: ``bool success`` and ``string message``.
       - **Feedback**: ``int32 current_waypoint``, the waypoint
         currently being visited.

    2. Update ``CMakeLists.txt`` to generate the action interface.

    3. Build and verify:

       .. code-block:: bash

          ros2 interface show robot_interfaces/action/Patrol

.. dropdown:: Exercise 5: Action Server with Feedback
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement an action server that simulates visiting waypoints and
    publishes feedback.

    **Specification**

    1. Create a package ``robot_action`` that depends on ``rclcpp``,
       ``rclcpp_action``, and ``robot_interfaces``.

    2. Write a node ``patrol_server`` that:

       - Creates an action server for ``/patrol`` of type
         ``robot_interfaces/action/Patrol``.
       - Rejects goals where ``num_waypoints <= 0``.
       - Simulates visiting each waypoint with a 1-second delay.
       - Publishes feedback with the current waypoint number.
       - Handles cancellation: if canceled, returns
         ``success = false``.
       - On completion, returns ``success = true`` and
         ``message = "Patrol complete. Visited N waypoints."``.

    3. Test with:

       .. code-block:: bash

          ros2 action send_goal /patrol robot_interfaces/action/Patrol \
            "{num_waypoints: 5}" --feedback

.. dropdown:: Exercise 6 Challenge: Integrated Communication System
    :icon: gear
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

    3. **Patrol Action** (action): reuse or extend the patrol server
       from Exercise 5. Before starting the patrol, the server should
       call the ``/get_status`` service to check the system status. If
       the service returns ``success = false``, abort the goal.

    4. **Coordinator** (action client + subscriber): a node that:

       - Subscribes to ``/battery_level``.
       - When battery drops below 50.0, sends a patrol goal to
         ``/patrol`` with 3 waypoints.
       - Logs feedback as it arrives.
       - Logs the final result.

    5. Use a launch file to start all four nodes.
