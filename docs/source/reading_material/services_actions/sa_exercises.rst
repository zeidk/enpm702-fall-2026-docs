====================================================
ROS Exercises
====================================================

.. note::

   **Not graded, and not submitted on Canvas.** Build the packages of
   :doc:`sa_lecture` first. Each exercise says what to predict before you
   run anything.

.. note::

   **Naming.** A node's name ends with ``_node`` and its executable's name
   with ``_exe``. A node class lives in ``<name>_node.hpp`` and
   ``<name>_node.cpp``, and its ``main`` in ``<name>_main.cpp``.


.. dropdown:: Exercise 1: Call a Service from the Terminal
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``fare_node`` charges 5.0 dollars plus 2.0 dollars per km. Without
   running anything, write the fare of a ride of 0 m and of a ride of
   10000 m. Then start ``fare_exe`` and call ``compute_fare`` for each
   distance with ``ros2 service call``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      A ride of 0 m costs 5.0 + 2.0 × 0 = 5.0 dollars. A ride of 10000 m
      is 10 km, so it costs 5.0 + 2.0 × 10 = 25.0 dollars.

      .. code-block:: bash

         ros2 run sa_demo fare_exe
         ros2 service call /compute_fare sa_interfaces/srv/ComputeFare "{distance_m: 0.0}"
         ros2 service call /compute_fare sa_interfaces/srv/ComputeFare "{distance_m: 10000.0}"

      The responses are ``fare=5.0`` and ``fare=25.0``.


.. dropdown:: Exercise 2: A Longer Timeout
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   In ``drive_client_node.hpp``, change ``timeout_s_`` from 3.0 to 6.0.
   The drive to 10 m takes 5 s. Predict what the client prints at the
   end. Then build, run ``drive_exe`` and ``drive_client_exe``, and
   compare.

   .. dropdown:: Solution
      :class-container: sd-border-success

      The goal ends after 5 s, before the 6 s timeout, so the client never
      cancels. The last lines are:

      .. code-block:: text

         [INFO] [...] [drive_client_node]: feedback: x = 10 m
         [INFO] [...] [drive_client_node]: succeeded, final x = 10


.. dropdown:: Exercise 3: Reject a Goal
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Make ``on_goal`` of ``drive_node`` reject a ``target_x`` above 50 m.
   Check it with ``ros2 action send_goal``, once with 40 m and once with
   60 m, and say which line of the output tells that the goal was
   rejected.

   .. dropdown:: Solution
      :class-container: sd-border-success

      Change the test of ``on_goal`` to ``goal->target_x <= 0.0 ||
      goal->target_x > 50.0 || busy_``. A goal of 40 m is accepted and,
      after 20 s (40 m at 2 m/s), ends with ``Goal finished with status:
      SUCCEEDED``. A goal of 60 m
      prints ``Goal was rejected.``.


.. dropdown:: Challenge: Three Patterns in One System
   :icon: rocket
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Build a system in which a topic, a service and an action work
   together.

   **Specification**

   1. ``battery_node`` publishes a ``std_msgs/msg/Float64`` on
      ``battery_level`` at 2 Hz. The level starts at 100.0 and drops by
      1.0 at each publication.
   2. ``status_node`` serves ``get_status`` of type
      ``std_srvs/srv/Trigger``. It answers with ``success`` true and the
      message ``System OK``.
   3. In a package ``robot_interfaces``, define ``action/Patrol.action``.
      The goal is ``int32 num_waypoints``. The result is ``bool success``
      and ``string message``. The feedback is ``int32 current_waypoint``.
   4. ``patrol_node`` serves the action ``patrol``. It rejects a goal with
      ``num_waypoints`` of 0 or less. Before it starts, it calls
      ``get_status``, and it aborts the goal when ``success`` is false.
      It visits one waypoint per second and sends the waypoint as
      feedback.
   5. ``coordinator_node`` subscribes to ``battery_level``. When the level
      falls below 50.0, it sends a ``patrol`` goal with 3 waypoints, and
      it logs the feedback and the result.
   6. A launch file starts the four nodes.
