====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 11: ROS 2 Configuration and
Orchestration. Topics include launch files (Python launch files, launch
arguments, conditions, groups and namespaces, events), executors
(single-threaded, multi-threaded, callback groups) and custom interfaces
(``.msg`` files, interface packages, generated C++ types).

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
====================================================

.. admonition:: Question 1
   :class: hint

   In a Python launch file, which class is used to define a launch argument
   that can be overridden from the command line?

   A. ``LaunchConfiguration``

   B. ``Node``

   C. ``DeclareLaunchArgument``

   D. ``SetParameter``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``DeclareLaunchArgument``

   ``DeclareLaunchArgument`` defines a launch-time argument with a name,
   default value, and description. ``LaunchConfiguration`` is then used
   to *read* the value of a declared argument inside the launch file.


.. admonition:: Question 2
   :class: hint

   Which launch action starts everything another launch file starts?

   A. ``GroupAction``

   B. ``IncludeLaunchDescription``

   C. ``ExecuteProcess``

   D. ``RegisterEventHandler``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``IncludeLaunchDescription``

   It runs every action of the launch file it is given, so a large system
   can be built from small launch files. ``GroupAction`` gives a set of
   actions shared settings, ``ExecuteProcess`` runs any command, and
   ``RegisterEventHandler`` runs actions when an event happens.


.. admonition:: Question 3
   :class: hint

   You put a launch file in the ``launch`` folder of a package and build the
   package. ``ros2 launch`` cannot find the file. What is the most likely
   cause?

   A. The file name ends with ``_launch.py``.

   B. ``CMakeLists.txt`` does not install the ``launch`` folder.

   C. The node names in the file do not end with ``_node``.

   D. The package has no ``include`` folder.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``CMakeLists.txt`` does not install the ``launch`` folder.

   ``ros2 launch`` finds a launch file only in
   ``install/<package>/share/<package>/launch/``. ``colcon build`` copies
   the ``launch`` folder there only when ``CMakeLists.txt`` has
   ``install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})``.


.. admonition:: Question 4
   :class: hint

   A launch file calls ``make_taxi("taxi1")`` and ``make_taxi("taxi2")``.
   Each call returns a ``GroupAction`` that starts a ``robotaxi_node`` with
   ``PushROSNamespace``. The node publishes on the relative topic name
   ``robotaxi/position``. What is the full name of the topic that the
   ``taxi2`` robotaxi publishes?

   A. ``/robotaxi/position``

   B. ``/taxi2/robotaxi/position``

   C. ``/taxi2/position``

   D. ``taxi2/robotaxi``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``/taxi2/robotaxi/position``

   The namespace goes in front of a relative topic name. With no namespace,
   the topic would be ``/robotaxi/position``. A name that starts with ``/``
   would ignore the namespace.


.. admonition:: Question 5
   :class: hint

   A launch file registers
   ``OnProcessStart(target_action=robotaxi, on_start=[LogInfo(...), dispatcher])``.
   When does it start the dispatcher?

   A. At the same time as the robotaxi, in any order.

   B. When the launch shuts down after :kbd:`Ctrl+C`.

   C. When the process of the ``robotaxi`` action has started.

   D. After a fixed delay.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, when the process of the ``robotaxi`` action has started.

   The event handler waits for the event, then logs its line and starts the
   dispatcher. The dispatcher is not added to the launch description: the
   handler starts it, so the event decides the order.


.. admonition:: Question 6
   :class: hint

   What is the default executor used by ``rclcpp::spin()``?

   A. ``MultiThreadedExecutor``

   B. ``SingleThreadedExecutor``

   C. ``StaticSingleThreadedExecutor``

   D. ``EventsExecutor``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``SingleThreadedExecutor``

   When you call ``rclcpp::spin(node)``, ROS 2 creates a
   ``SingleThreadedExecutor``, adds your node to it and calls its
   ``spin()``. All callbacks run one at a time on one thread.


.. admonition:: Question 7
   :class: hint

   A ``main`` function contains ``rclcpp::spin(camera);`` followed by
   ``rclcpp::spin(controller);``. What happens when it runs?

   A. Both nodes run, each on its own thread.

   B. Both nodes run, one callback at a time.

   C. Only the camera's callbacks run; the second call starts only after
      ROS 2 has shut down.

   D. The program does not compile.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   The first ``spin`` returns only when ROS 2 shuts down, after
   :kbd:`Ctrl+C`. Until then, the second line never runs, so the
   controller's callbacks never run. Two nodes in one process need one
   executor that holds both.


.. admonition:: Question 8
   :class: hint

   In a ``MultiThreadedExecutor``, what is the behavior of a **mutually
   exclusive** callback group?

   A. All callbacks in the group run concurrently on separate threads.

   B. Only one callback in the group can execute at a time; others wait.

   C. Callbacks are distributed across executors in a round-robin fashion.

   D. Callbacks are queued and executed in FIFO order on a dedicated thread.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, Only one callback in the group can execute at a time; others
   wait.

   A mutually exclusive callback group ensures that at most one callback
   from the group runs at any given time, even with several threads.
   Callbacks in other groups can still run alongside.


.. admonition:: Question 9
   :class: hint

   A timer has a period of 1 s, its callback works for 1.5 s, and the timer
   is in a **reentrant** group of a ``MultiThreadedExecutor`` with enough
   threads. What happens to its next run?

   A. It waits until the previous run ends.

   B. It is skipped.

   C. It starts on time, so two runs of the callback overlap.

   D. It runs on the main thread only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, it starts on time, so two runs of the callback overlap.

   A reentrant group puts no limit on its callbacks: two runs of the same
   callback can run at the same time. In the demo with two reentrant
   groups, nothing waited and ``timer1`` overlapped itself.


.. admonition:: Question 10
   :class: hint

   The file ``Status.msg`` is in the package ``fleet_interfaces``. What are
   the C++ type and the header that the build generates?

   A. ``fleet_interfaces::Status`` from ``fleet_interfaces/Status.hpp``

   B. ``fleet_interfaces::msg::Status`` from ``fleet_interfaces/msg/status.hpp``

   C. ``msg::Status`` from ``status.hpp``

   D. ``fleet_interfaces::msg::status`` from ``fleet_interfaces/msg/Status.msg``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``fleet_interfaces::msg::Status`` from
   ``fleet_interfaces/msg/status.hpp``

   A file ``Type.msg`` in the package ``pkg`` becomes the C++ type
   ``pkg::msg::Type``, from the header ``pkg/msg/type.hpp``: the name in
   lowercase, with underscores between words.


----


True / False (Questions 11-15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** A ``MultiThreadedExecutor`` can execute callbacks from
   the same mutually exclusive callback group concurrently.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A mutually exclusive callback group guarantees that only one callback in
   the group executes at a time, even when using a ``MultiThreadedExecutor``.
   Concurrent execution is only possible for callbacks in a **reentrant**
   callback group or in separate groups.


.. admonition:: Question 12
   :class: hint

   **True or False:** Python launch files must define a function called
   ``generate_launch_description()`` that returns a ``LaunchDescription``
   object.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The ROS 2 launch system looks for the ``generate_launch_description()``
   function as the entry point of a Python launch file. This function must
   return a ``LaunchDescription`` containing the actions to execute.


.. admonition:: Question 13
   :class: hint

   **True or False:** A single-threaded executor that holds two nodes runs
   each node on its own thread.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A node is not a thread. A single-threaded executor runs the callbacks of
   both nodes on one thread, one at a time, so a slow callback in one node
   delays the callbacks of the other.


.. admonition:: Question 14
   :class: hint

   **True or False:** In a ``.msg`` file, the constant ``uint8 mode_idle=0``
   is valid, because constant names may use lowercase letters.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A constant's name is in uppercase, as in ``MODE_IDLE``. ``mode_idle``
   stops the build with the message ``'mode_idle' is an invalid constant
   name``. Field names, in contrast, use lowercase letters, digits and
   underscores.


.. admonition:: Question 15
   :class: hint

   **True or False:** A condition given to a ``GroupAction`` applies to
   every action in the group.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   A condition on a group starts or skips every action in the group at once.
   In the lecture, ``make_taxi("taxi2", second)`` starts the second robotaxi
   and its dispatcher together, only when ``two_taxis:=true``.
