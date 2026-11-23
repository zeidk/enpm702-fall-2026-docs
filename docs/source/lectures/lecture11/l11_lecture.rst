====================================================
Lecture
====================================================

Before Class
------------

Before this class, get the latest edits of the course repository into your copy (assuming you have already followed the `instructions <../../setup/ros_setup.html#ros-2-workspace>`__), from ``~/ros2_ws/src/enpm702-fall-2026-ros``:

.. code-block:: bash

   git fetch upstream
   git merge --no-edit upstream/main
   git push

Its ``L11`` folder holds this lecture's two packages, ``l11_robotaxi`` and ``l11_robotaxi_interfaces``. Then build them, from ``~/ros2_ws``:

.. code-block:: bash

   colcon build --packages-up-to l11_robotaxi
   source install/setup.bash

``--packages-up-to`` builds ``l11_robotaxi`` and the packages it depends on, so ``l11_robotaxi_interfaces`` is built first.

In class, I do not explain the shell commands: you learned them in the shell exercises on ReadTheDocs, which every student was asked to do.

Code for This Lecture
---------------------

The ``L11`` folder of the course repository holds two packages:

.. code-block:: text

   enpm702-fall-2026-ros/L11/
   ├── l11_robotaxi/
   │   ├── CMakeLists.txt
   │   ├── package.xml
   │   ├── include/l11_robotaxi/
   │   │   ├── robotaxi_node.hpp
   │   │   ├── dispatcher_node.hpp
   │   │   ├── camera_node.hpp
   │   │   ├── controller_node.hpp
   │   │   ├── sensors_node.hpp
   │   │   ├── health_node.hpp
   │   │   ├── callback_groups_node.hpp
   │   │   ├── status_node.hpp
   │   │   ├── fleet_monitor_node.hpp
   │   │   ├── colors.hpp
   │   │   └── work.hpp
   │   ├── launch/
   │   │   ├── robotaxi_launch.py
   │   │   ├── robotaxi_list_launch.py
   │   │   ├── include_launch.py
   │   │   ├── argument_launch.py
   │   │   ├── group_launch.py
   │   │   ├── group_condition_launch.py
   │   │   └── event_launch.py
   │   └── src/
   │       ├── *_node.cpp          (one per node class)
   │       └── *_main.cpp          (one per executable)
   └── l11_robotaxi_interfaces/
       ├── CMakeLists.txt
       ├── package.xml
       └── msg/RobotaxiStatus.msg

``l11_robotaxi`` holds the two nodes of the previous lecture, ``robotaxi_node`` and ``dispatcher_node``, under a new package name. Your workspace holds the folders of both lectures, and ``colcon build`` stops when two packages have the same name.

Launch Files
------------

A **launch file** lists the nodes to start and their settings. One command, ``ros2 launch``, starts them all.

What Launch Files Do
^^^^^^^^^^^^^^^^^^^^

The previous lecture listed four jobs of a launch file: automation, configuration, coordination and flexibility. It has other jobs too, each done by a launch action:

.. list-table::
   :header-rows: 1
   :widths: 18 44 38

   * - Job
     - What the launch file does
     - Launch action
   * - Reuse
     - Starts another launch file.
     - ``IncludeLaunchDescription``
   * - Conditions
     - Starts a node only if an argument says so.
     - ``IfCondition``
   * - Groups
     - Gives a set of nodes shared settings, such as a namespace.
     - ``GroupAction``, ``PushROSNamespace``
   * - Timing and events
     - Starts a node after a delay or when a process ends.
     - ``TimerAction``, ``RegisterEventHandler``
   * - Python logic
     - Computes settings in Python before nodes start.
     - ``OpaqueFunction``
   * - Logging
     - Prints its own messages.
     - ``LogInfo``
   * - Other programs
     - Runs any command, not only nodes.
     - ``ExecuteProcess``

This section uses reuse, conditions, groups, events and logging.

The Three Parts of a Python Launch File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The previous lecture named three file types for launch files: Python, XML and YAML. This course writes them in Python. A Python launch file is a Python program with three parts:

1. **Imports**: ``LaunchDescription`` from the ``launch`` package, and ``Node`` from ``launch_ros.actions``.
2. **The function** ``generate_launch_description()``: ``ros2 launch`` looks for a function with this exact name, calls it, and runs what it returns.
3. **The launch description**: a ``LaunchDescription`` object that holds the **actions** to run. A ``Node`` action starts one executable, named by its package and its executable.

.. note::

   A ``Node`` action can also set the node's namespace, parameters and remapped names. This section sets namespaces. Parameters come in Lecture 12.

Configurations
^^^^^^^^^^^^^^

You can write a launch file in two ways: add the nodes one at a time, or pass them all in one list. Both start the same nodes.

The task: write a launch file that starts the robotaxi and the dispatcher with one command.

.. list-table::
   :widths: 22 78

   * - Package
     - ``l11_robotaxi``
   * - File
     - ``launch/robotaxi_launch.py``
   * - Nodes
     - ``robotaxi_node``, ``dispatcher_node``
   * - Executables
     - ``robotaxi_exe``, ``dispatcher_exe``

Resource: `ROS 2 Jazzy: Creating a launch file <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`__.

Step 1: Create the Launch File in a launch Folder
"""""""""""""""""""""""""""""""""""""""""""""""""

From the package folder, ``l11_robotaxi``, create a ``launch`` folder and an empty file in it:

.. code-block:: bash

   mkdir launch
   touch launch/robotaxi_launch.py

A launch file name must end with ``launch.py`` "to be recognized and autocompleted by ros2 launch" (`Integrating launch files into ROS 2 packages <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-system.html>`__). This course ends names with ``_launch.py``, as the documentation recommends.

The package after Step 1:

.. code-block:: text

   l11_robotaxi/
   ├── include/
   │   └── l11_robotaxi/
   ├── launch/
   │   └── robotaxi_launch.py
   ├── src/
   ├── CMakeLists.txt
   └── package.xml

Step 2: Write the Launch File, Adding Each Node with add_action
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python
   :linenos:
   :emphasize-lines: 7-14

   from launch import LaunchDescription
   from launch_ros.actions import Node


   # ros2 launch calls this function and starts the actions it returns.
   def generate_launch_description():
       ld = LaunchDescription()
       robotaxi = Node(package="l11_robotaxi", executable="robotaxi_exe")
       dispatcher = Node(
           package="l11_robotaxi", executable="dispatcher_exe"
       )
       ld.add_action(robotaxi)
       ld.add_action(dispatcher)
       return ld

- Line 7: an empty launch description.
- Lines 8 to 11: two ``Node`` actions. Creating an action starts nothing yet.
- Lines 12 to 14: ``add_action`` adds each action, and the function returns the description. ``ros2 launch`` then starts both nodes.

Step 2, Written Another Way: All Nodes in One List
""""""""""""""""""""""""""""""""""""""""""""""""""

The same file, its actions in one list (kept as ``launch/robotaxi_list_launch.py``):

.. code-block:: python
   :linenos:
   :emphasize-lines: 7-12

   from launch import LaunchDescription
   from launch_ros.actions import Node


   # The same two nodes as robotaxi_launch.py, given as one list.
   def generate_launch_description():
       return LaunchDescription(
           [
               Node(package="l11_robotaxi", executable="robotaxi_exe"),
               Node(package="l11_robotaxi", executable="dispatcher_exe"),
           ]
       )

- Lines 7 to 12: the list goes straight into ``LaunchDescription``, so no variable is needed.
- Both versions start the same two processes. The rest of this section uses the ``add_action`` version: each action gets a name before it is added.

Step 3: Install the Launch Folder from CMakeLists.txt
"""""""""""""""""""""""""""""""""""""""""""""""""""""

Add these lines to ``CMakeLists.txt``, before ``ament_package()``:

.. code-block:: cmake

   install(DIRECTORY launch
     DESTINATION share/${PROJECT_NAME})

.. important::

   ``ros2 launch`` finds a launch file only in ``install/l11_robotaxi/share/l11_robotaxi/launch/``. ``colcon build`` copies the ``launch`` folder there only when ``CMakeLists.txt`` installs it, as above.

Then declare the launch tool in ``package.xml``, as the documentation advises (`Creating a launch file <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`__):

.. code-block:: xml

   <exec_depend>ros2launch</exec_depend>

Step 4: Build and Run the Launch File
"""""""""""""""""""""""""""""""""""""

.. code-block:: bash

   colcon build --packages-select l11_robotaxi
   source install/setup.bash
   ros2 launch l11_robotaxi robotaxi_launch.py

.. code-block:: text

   [INFO] [robotaxi_exe-1]: process started with pid [1936121]
   [INFO] [dispatcher_exe-2]: process started with pid [1936122]
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 0
   [dispatcher_exe-2] [INFO] [...] [dispatcher_node]: 10 m from the pickup
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 1
   [dispatcher_exe-2] [INFO] [...] [dispatcher_node]: 9 m from the pickup

- The launch system names each process after its executable and a number: ``robotaxi_exe-1``, ``dispatcher_exe-2``. Each line a process prints starts with that name.
- Two pids: two processes, as with two ``ros2 run`` commands in two terminals. One :kbd:`Ctrl+C` stops both.

Advanced Features
^^^^^^^^^^^^^^^^^

A launch file can do more than start nodes. It can include another launch file, take arguments, start a node only when an argument says so, and start nodes as a group.

Include a Launch File
"""""""""""""""""""""

One launch file can start everything another launch file starts, with ``IncludeLaunchDescription``. A large system is then built from small launch files, each kept in its own package.

**Write the launch file that includes another.** Lines 8 to 18 of ``launch/include_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 8
   :emphasize-lines: 3-6, 8

   def generate_launch_description():
       ld = LaunchDescription()
       demo_share = FindPackageShare("demo_nodes_cpp")
       talker_listener_file = PathJoinSubstitution(
           [demo_share, "launch", "topics", "talker_listener_launch.py"]
       )
       robotaxi = Node(package="l11_robotaxi", executable="robotaxi_exe")
       talker_listener = IncludeLaunchDescription(talker_listener_file)
       ld.add_action(robotaxi)
       ld.add_action(talker_listener)
       return ld

- Line 10: ``FindPackageShare`` finds the ``share`` folder of ``demo_nodes_cpp``. It is a **substitution**: a value computed when the file runs.
- Lines 11 to 13: ``PathJoinSubstitution`` adds the rest of the path.
- Line 15: ``IncludeLaunchDescription`` runs every action of the previous lecture's ``talker_listener_launch.py``; line 17 adds it.

**Run the launch file that includes another:**

.. code-block:: bash

   ros2 launch l11_robotaxi include_launch.py

.. code-block:: text

   [INFO] [robotaxi_exe-1]: process started with pid [1936220]
   [INFO] [talker-2]: process started with pid [1936221]
   [INFO] [listener-3]: process started with pid [1936222]
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 0
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 1
   [talker-2] [INFO] [...] [talker]: Publishing: 'Hello World: 1'
   [listener-3] [INFO] [...] [listener]: I heard: [Hello World: 1]

- Three processes: the robotaxi from this file, the talker and the listener from the included file.
- The launch file needs ``demo_nodes_cpp`` installed, so ``package.xml`` declares it: ``<exec_depend>demo_nodes_cpp</exec_depend>``.

Arguments and Conditions
""""""""""""""""""""""""

A **launch argument** is a value you set on the ``ros2 launch`` command, such as ``with_dispatcher:=false``. A **condition** reads it and decides whether an action runs.

**Part 1: declare a launch argument.** Lines 8 to 14 of ``launch/argument_launch.py``; lines 1 to 5 are its imports.

.. code-block:: python
   :linenos:
   :lineno-start: 8
   :emphasize-lines: 3-7

   def generate_launch_description():
       ld = LaunchDescription()
       with_dispatcher = DeclareLaunchArgument(
           "with_dispatcher",
           default_value="true",
           description="Start the dispatcher node too",
       )

- Lines 10 to 14: a **launch argument**, ``with_dispatcher``, is ``"true"`` unless the command sets it.
- The description is the text that ``--show-args`` prints.

**Part 2: start the dispatcher only when the argument says so.** Lines 15 to 23 of ``launch/argument_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 15
   :emphasize-lines: 5, 7

       robotaxi = Node(package="l11_robotaxi", executable="robotaxi_exe")
       dispatcher = Node(
           package="l11_robotaxi",
           executable="dispatcher_exe",
           condition=IfCondition(LaunchConfiguration("with_dispatcher")),
       )
       ld.add_action(with_dispatcher)
       ld.add_action(robotaxi)
       ld.add_action(dispatcher)

- Line 19: ``LaunchConfiguration`` reads the argument when the file runs. ``IfCondition`` starts the dispatcher only when the value is true.
- Line 21 adds the argument to the launch description, so ``--show-args`` lists it.

**Part 3: log the argument's value with LogInfo.** Lines 24 to 31 of ``launch/argument_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 24
   :emphasize-lines: 1-7

       log_value = LogInfo(
           msg=[
               "with_dispatcher = ",
               LaunchConfiguration("with_dispatcher"),
           ]
       )
       ld.add_action(log_value)
       return ld

- Lines 24 to 29: ``LogInfo`` is an action that prints a message while the launch runs. Its ``msg`` is a list: the text, then the argument's value, read with ``LaunchConfiguration``.
- Line 30 adds it, as any other action. The launch system prints it under the name ``launch.user``.

**List the arguments, then set one.** ``--show-args`` lists a launch file's arguments and starts nothing:

.. code-block:: bash

   ros2 launch l11_robotaxi argument_launch.py --show-args

.. code-block:: text

   Arguments (pass arguments as '<name>:=<value>'):

       'with_dispatcher':
           Start the dispatcher node too
           (default: 'true')

An argument is set with ``name:=value``. Here, the robotaxi starts alone:

.. code-block:: bash

   ros2 launch l11_robotaxi argument_launch.py with_dispatcher:=false

.. code-block:: text

   [INFO] [launch.user]: with_dispatcher = false
   [INFO] [robotaxi_exe-1]: process started with pid [1936360]
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 0
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 1

The first line comes from ``LogInfo``. Without the argument, both processes start.

Groups and Namespaces
"""""""""""""""""""""

A **group** gives a set of actions shared settings. With a namespace as that setting, two copies of the same nodes run side by side, and their names do not collide.

**Part 1: a group of nodes in a namespace.** Lines 6 to 13 of ``launch/group_launch.py``; lines 1 to 3 import ``GroupAction`` and ``PushROSNamespace``, with ``LaunchDescription`` and ``Node``.

.. code-block:: python
   :linenos:
   :lineno-start: 6
   :emphasize-lines: 2, 4

   def make_taxi(namespace):
       return GroupAction(
           [
               PushROSNamespace(namespace),
               Node(package="l11_robotaxi", executable="robotaxi_exe"),
               Node(package="l11_robotaxi", executable="dispatcher_exe"),
           ]
       )

- Line 7: a ``GroupAction`` holds a list of actions that share settings.
- Line 9: ``PushROSNamespace`` puts every node of the group in a **namespace**: a prefix added to the names of its nodes and of its relative topics.

**Part 2: two robotaxis, each in its own namespace.** Lines 16 to 20 of ``launch/group_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 16
   :emphasize-lines: 3-4

   def generate_launch_description():
       ld = LaunchDescription()
       ld.add_action(make_taxi("taxi1"))
       ld.add_action(make_taxi("taxi2"))
       return ld

- Lines 18 and 19: ``make_taxi`` is an ordinary Python function, called once per robotaxi. Each call returns one group, which ``add_action`` adds like any other action.

**Run the group, then list nodes and topics.** Start ``ros2 launch l11_robotaxi group_launch.py``, then, in a second terminal:

.. code-block:: bash

   ros2 node list

.. code-block:: text

   /taxi1/dispatcher_node
   /taxi1/robotaxi_node
   /taxi2/dispatcher_node
   /taxi2/robotaxi_node

.. code-block:: bash

   ros2 topic list

.. code-block:: text

   /parameter_events
   /rosout
   /taxi1/robotaxi/position
   /taxi2/robotaxi/position

- Four nodes: ``taxi1`` and ``taxi2`` each run a ``robotaxi_node`` and a ``dispatcher_node``. Their namespaces keep them apart.
- The code of the previous lecture already named the topic ``robotaxi/position``, with no leading ``/``: a **relative** name. With no namespace, it became ``/robotaxi/position``. Here the namespace goes in front of it, so each dispatcher hears only its own robotaxi. A name that starts with ``/`` would ignore the namespace.

.. _l11-groups-with-a-condition:

Groups with a Condition
"""""""""""""""""""""""

A condition on a group starts or skips every action in the group at once: here, the second robotaxi together with its dispatcher.

**Part 1: give make_taxi a condition.** ``launch/group_condition_launch.py`` starts the second robotaxi only when an argument asks for it. Its ``make_taxi`` takes a condition, lines 8 to 16:

.. code-block:: python
   :linenos:
   :lineno-start: 8
   :emphasize-lines: 1, 8

   def make_taxi(namespace, condition=None):
       return GroupAction(
           [
               PushROSNamespace(namespace),
               Node(package="l11_robotaxi", executable="robotaxi_exe"),
               Node(package="l11_robotaxi", executable="dispatcher_exe"),
           ],
           condition=condition,
       )

- Line 15: a condition on a group applies to every action in it.
- Line 8: ``None``, the default, means no condition: the group always starts.

**Part 2: start the second robotaxi only when asked.** Lines 19 to 30 of ``launch/group_condition_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 19
   :emphasize-lines: 8, 11

   def generate_launch_description():
       ld = LaunchDescription()
       two_taxis = DeclareLaunchArgument(
           "two_taxis",
           default_value="false",
           description="Start a second robotaxi in taxi2",
       )
       second = IfCondition(LaunchConfiguration("two_taxis"))
       ld.add_action(two_taxis)
       ld.add_action(make_taxi("taxi1"))
       ld.add_action(make_taxi("taxi2", second))
       return ld

- Line 26 builds the condition from the argument. Line 29: only the ``taxi2`` group gets it.
- With no argument, ``ros2 node list`` shows two nodes, ``/taxi1/dispatcher_node`` and ``/taxi1/robotaxi_node``. With ``two_taxis:=true``, it shows the four nodes of the group run above.

.. _l11-launch-events:

Events
""""""

An **event handler** waits for something to happen, such as a process that starts or a launch that shuts down, and then runs actions.

**Part 1: start the dispatcher when the robotaxi has started.** Lines 13 to 22 of ``launch/event_launch.py``; lines 9 to 12 create the robotaxi and dispatcher actions, as in Step 2.

.. code-block:: python
   :linenos:
   :lineno-start: 13
   :emphasize-lines: 2-7

       # When the robotaxi starts: log a line, start the dispatcher.
       start_dispatcher = RegisterEventHandler(
           OnProcessStart(
               target_action=robotaxi,
               on_start=[
                   LogInfo(msg="robotaxi started, starting dispatcher"),
                   dispatcher,
               ],
           )
       )

- Line 14: ``RegisterEventHandler`` is an action that registers a handler.
- Lines 15 and 16: ``OnProcessStart`` waits for the process of the ``robotaxi`` action to start.
- Lines 17 to 19: then it logs a line and starts the dispatcher. The dispatcher is not added to the launch description: the handler starts it.

**Part 2: log a last line on Ctrl + C.** Lines 23 to 30 of ``launch/event_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 23
   :emphasize-lines: 2-4

       # When the launch shuts down (Ctrl+C), log a last line.
       goodbye = RegisterEventHandler(
           OnShutdown(on_shutdown=[LogInfo(msg="Fleet stopped")])
       )
       ld.add_action(robotaxi)
       ld.add_action(start_dispatcher)
       ld.add_action(goodbye)
       return ld

- Lines 24 to 26: ``OnShutdown`` runs its actions when the launch shuts down, here after :kbd:`Ctrl+C`.
- Lines 27 to 29: the robotaxi and the two handlers are added; the dispatcher is not.

**Run the launch file with events.** Start ``ros2 launch l11_robotaxi event_launch.py``, then press :kbd:`Ctrl+C`:

.. code-block:: text

   [INFO] [robotaxi_exe-1]: process started with pid [1940213]
   [INFO] [launch.user]: robotaxi started, starting dispatcher
   [INFO] [dispatcher_exe-2]: process started with pid [1940214]
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: Published x = 0
   [dispatcher_exe-2] [INFO] [...] [dispatcher_node]: 10 m from the pickup

After :kbd:`Ctrl+C`:

.. code-block:: text

   [WARNING] [launch]: user interrupted with ctrl-c (SIGINT)
   [INFO] [launch.user]: Fleet stopped

- The handler's line comes after the robotaxi process started and before the dispatcher process: the event decides the order.
- ``Fleet stopped`` prints right after :kbd:`Ctrl+C`, before the two nodes finish.

Launch Files: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Write a Python launch file, with ``add_action`` or with one list, and install its folder from ``CMakeLists.txt``.
   - Start another package's launch file with ``IncludeLaunchDescription``.
   - Declare an argument, list it with ``--show-args``, and start a node or a group only when the argument is true.
   - Run two copies of the same nodes in two namespaces.
   - Log with ``LogInfo``, and run actions when a process starts or the launch shuts down.

A launch file can also set a node's parameters and remap its names. Parameters come in Lecture 12.

Executors
---------

.. admonition:: Definition: Executor
   :class: tip

   The part of a ROS 2 program that runs callbacks. You add nodes to it. It waits for events, such as a timer's period ending or a message arriving, and runs the callback of each event, on one thread or on several. ``rclcpp::spin(node)``, which you used in the previous lecture, creates an executor for you and adds the node to it.

Launch files chose which nodes start. This section is about how a process runs their callbacks, and its programs start with ``ros2 run``.

A Robot Runs Many Tasks at Once
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Tasks that run at the same time:**

- Process sensor data: cameras, lidar, IMU.
- Update control commands, each at its own rate.
- Monitor the system's health and safety.
- Handle user commands.
- Log data for later analysis.

**Questions they raise:**

- How do we handle many callbacks?
- What if one callback blocks the others?
- Can we process sensors in parallel?
- How do we put critical tasks first?
- When do we use threads, and when one callback after another?

An executor answers these questions: it decides which callback runs, when, and on which thread.

Before Executors: What Starts a Callback
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the C++ nodes you have written so far, a callback runs when an event happens. How many kinds of event start a callback, and what are they?

.. dropdown:: Answer
   :class-container: sd-border-success

   Two: a timer's period ends, and a message arrives on a topic. The timer callbacks of this lecture are the first kind, ``command_callback`` below is the second.

Scenario: a Robotaxi Drives Toward a Traffic Cone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The single-threaded executor parts use this scenario. A robotaxi drives toward a traffic cone, and two nodes set its speed. ``camera_node`` stands for the windshield camera (green wedge); the roof lidar and the other two cameras are not used. The distance to the cone starts at 10 m and drops 1 m per reading, until the robotaxi stops at 5 m.

.. figure:: /_static/images/l11/cone_scene.png
   :alt: Side view of a black car driving to the right on a road, toward a red and white traffic cone farther ahead. Green sensors on the car: a lidar on the roof, and three cameras, at the top of the windshield, on the front bumper and at the rear. A light green wedge, the front camera's view, opens from the windshield camera and covers the road up to and past the cone. Three gray horizontal lines behind the car show that it is moving.
   :align: center
   :width: 70%

   The robotaxi, the traffic cone and the windshield camera's view.

.. figure:: /_static/images/l11/cone_graph.png
   :alt: ROS graph. A rounded box camera_node has an arrow to a rounded box controller_node, labeled /camera/cone_distance above and std_msgs/msg/Float64 below. From controller_node, an arrow labeled /cmd_vel above and geometry_msgs/msg/Twist below ends in open space.
   :align: center
   :width: 95%

   The two nodes: the camera publishes the distance to the cone, the controller publishes the speed command.

``camera_node`` has two timer callbacks:

- ``sensor_callback``, every 0.5 s, publishes the distance to the cone.
- ``health_callback``, every 1 s, logs how many readings the camera took since its last run.

``controller_node`` has a subscriber callback and a timer callback:

- ``command_callback`` runs each time a distance arrives and publishes a speed: 2 m/s, 1 m/s within 8 m, 0 within 5 m.
- ``watchdog_callback``, every 1 s, publishes a stop when no distance came for over 1 s. ``command_callback`` cannot: it runs only when a distance arrives.

Single-Threaded Executors
^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Single-Threaded Executor
   :class: tip

   An executor that runs every callback on one thread, one at a time. ``rclcpp::spin(node)`` uses one.

.. figure:: /_static/images/l11/spin_main_thread.png
   :alt: On the left, a wavy line labeled main thread, with init, makes the node, leads to an arrow labeled rclcpp::spin(node) that enters a circle. Inside the circle: main thread, then 1. wait for an event, 2. run its callback, 3. repeat; an arrow runs clockwise around the circle. Six dots on the circle, clockwise from the upper right: callback1, callback2, callback1, callback2, callback1, callback2; callback1 dots and names are black, callback2 dots and names grey. On the right, an arrow marked with the keys Ctrl and C leaves the circle and leads to a second wavy line labeled main thread, with rclcpp::shutdown().
   :align: center
   :width: 100%

   The main thread starts ``rclcpp::spin(node)``, which loops until :kbd:`Ctrl+C`.

The one thread runs the callbacks one at a time, in the order their events happen: here ``callback1``, then ``callback2``, around the circle until :kbd:`Ctrl+C`.

What a Single-Threaded Executor Does Well, and Its Limit
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

In the scenario above, ``command_callback`` waits until ``sensor_callback`` returns. That wait has a good side and a bad side:

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * -
     - With a single-threaded executor
   * - **Strength**
     - Simple and predictable: one callback at a time, so two callbacks never change the same data at once.
   * - **Limit**
     - Independent tasks wait for each other: a slow callback delays every other callback of the executor.

rclcpp::spin(node) Is a Shortcut
""""""""""""""""""""""""""""""""

Every node so far ran with one line in ``main``:

.. code-block:: cpp

   rclcpp::spin(node);

It "expands to an instantiation and invocation of the Single-Threaded Executor" (`ROS 2 Jazzy: Executors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`__). In steps, ``rclcpp::spin(node)``:

1. creates a ``SingleThreadedExecutor``;
2. adds your node to it;
3. calls the executor's ``spin()``;
4. returns only when ROS 2 shuts down, after :kbd:`Ctrl+C`.

One Node: the Executor Written Out Does What spin Does
""""""""""""""""""""""""""""""""""""""""""""""""""""""

The camera of the scenario has two timer callbacks: ``sensor_callback`` every 0.5 s, and ``health_callback`` every 1 s.

Lines 9 and 10 of ``src/camera_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 9
   :emphasize-lines: 2

   auto node{std::make_shared<l11_robotaxi::CameraNode>()};
   rclcpp::spin(node);

Lines 10 to 13 of ``src/camera_executor_main.cpp``, the same ``main`` with the executor written out:

.. code-block:: cpp
   :linenos:
   :lineno-start: 10
   :emphasize-lines: 2-4

   auto node{std::make_shared<l11_robotaxi::CameraNode>()};
   rclcpp::executors::SingleThreadedExecutor executor{};
   executor.add_node(node);
   executor.spin();

Lines 11 to 13 do what line 10 of the first snippet, ``rclcpp::spin(node)``, does.

**Run both programs: the same output.**

.. code-block:: bash

   ros2 run l11_robotaxi camera_exe

or

.. code-block:: bash

   ros2 run l11_robotaxi camera_executor_exe

Each run prints the same lines, in the same order:

.. code-block:: text

   [INFO] [...] [camera_node]: sensor_callback: cone at 10 m
   [INFO] [...] [camera_node]: health_callback: readings since the last check = 1
   [INFO] [...] [camera_node]: sensor_callback: cone at 9 m
   [INFO] [...] [camera_node]: sensor_callback: cone at 8 m

.. figure:: /_static/images/l11/camera_alone.png
   :alt: One circle labeled main thread, with an arrow running clockwise around it. Six numbered dots on the circle, clockwise from the upper right: 1 green, 2 purple, 3 green, 4 green, 5 purple, 6 green. Under the circle, sensor_callback (0.5 s) in green and health_callback (1 s) in purple.
   :align: center
   :width: 40%

   The camera's callbacks on the main thread.

**Key:** each dot is one callback run, numbered in the order the main thread ran them. The code does not set which one runs first when both are ready.

.. admonition:: Conclusion
   :class: important

   For one node, ``rclcpp::spin(node)`` and the executor written out do the same thing.

Two Nodes: Two spin Calls Run Only the First Node
"""""""""""""""""""""""""""""""""""""""""""""""""

To run both nodes in one process, a first try calls ``spin`` once per node. Lines 12 to 15 of ``src/spin_twice_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 12
   :emphasize-lines: 3-4

   auto camera{std::make_shared<l11_robotaxi::CameraNode>()};
   auto controller{std::make_shared<l11_robotaxi::ControllerNode>()};
   rclcpp::spin(camera);
   rclcpp::spin(controller);

- Line 14 runs the camera's callbacks and returns only when ROS 2 shuts down, after :kbd:`Ctrl+C`.
- Until then, line 15 never runs: the controller's callbacks never run.

.. figure:: /_static/images/l11/spin_twice.png
   :alt: Two circles side by side. Left: a circle labeled main thread with a clockwise arrow and six numbered dots, 1 green, 2 purple, 3 green, 4 green, 5 purple, 6 green; under it, sensor_callback (0.5 s) in green and health_callback (1 s) in purple. Right: a gray dashed circle with no arrow and no dots, labeled never starts; under it, command_callback (each reading) in orange and watchdog_callback (1 s) in blue.
   :align: center
   :width: 80%

   The camera's callbacks run. The controller's circle never starts.

**Run it: the controller never runs.** Run ``ros2 run l11_robotaxi spin_twice_exe``, then press :kbd:`Ctrl+C` after 7.5 s:

.. code-block:: text

   [INFO] [...] [camera_node]: sensor_callback: cone at 10 m
   [INFO] [...] [camera_node]: health_callback: readings since the last check = 1
   ...
   [INFO] [...] [rclcpp]: signal_handler(SIGINT/SIGTERM)
   terminate called after throwing an instance of 'rclcpp::exceptions::RCLError'
     what():  failed to create guard condition: the given context is not valid, ...
   [ros2run]: Aborted

In 7.5 s, ``controller_node`` logged nothing. After :kbd:`Ctrl+C`, line 15 ran on a ROS 2 that was already shut down, and ``rclcpp::spin`` threw an exception.

.. admonition:: Conclusion
   :class: important

   Two nodes in one process need one executor that holds both.

Write the Executor Out: Two Nodes in One Executor
"""""""""""""""""""""""""""""""""""""""""""""""""

Lines 9 to 20 of ``src/single_executor_main.cpp`` run the camera and the controller in one executor:

.. code-block:: cpp
   :linenos:
   :lineno-start: 9
   :emphasize-lines: 5-8

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       auto camera{std::make_shared<l11_robotaxi::CameraNode>()};
       auto controller{std::make_shared<l11_robotaxi::ControllerNode>()};
       rclcpp::executors::SingleThreadedExecutor executor{};
       executor.add_node(camera);
       executor.add_node(controller);
       executor.spin();
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

- Line 13: the executor. Lines 14 and 15: ``add_node`` gives it both nodes. Line 16: ``spin`` runs the four callbacks of both nodes on the main thread, until :kbd:`Ctrl+C`.
- A node is not a thread: the second node adds no thread. Another executor type changes only line 13.

Two Processes: Each Node Runs on Its Own Main Thread
""""""""""""""""""""""""""""""""""""""""""""""""""""

``src/camera_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 9

   auto node{std::make_shared<l11_robotaxi::CameraNode>()};
   rclcpp::spin(node);

``src/controller_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 9

   auto node{std::make_shared<l11_robotaxi::ControllerNode>()};
   rclcpp::spin(node);

.. figure:: /_static/images/l11/two_processes.png
   :alt: Two circles side by side, each labeled main thread, with an arrow running clockwise around it. Left circle: six numbered dots, 1 green, 2 purple, 3 green, 4 green, 5 purple, 6 green; under it, sensor_callback (0.5 s) in green, health_callback (1 s) in purple, then camera_exe. Right circle: six numbered dots, 1 orange, 2 blue, 3 orange, 4 orange, 5 blue, 6 orange; under it, command_callback (each reading) in orange, watchdog_callback (1 s) in blue, then controller_exe.
   :align: center
   :width: 70%

   Two processes: each has its own main thread and its own circle.

One Executor: One Thread Runs Both Nodes
""""""""""""""""""""""""""""""""""""""""

One ``main`` function adds both nodes to one executor. Lines 13 to 16 of ``src/single_executor_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 13

   rclcpp::executors::SingleThreadedExecutor executor{};
   executor.add_node(camera);
   executor.add_node(controller);
   executor.spin();

.. figure:: /_static/images/l11/one_process.png
   :alt: One circle labeled main thread, with an arrow running clockwise around it. Eight numbered dots clockwise from the upper right: 1 green, 2 orange, 3 purple, 4 green, 5 orange, 6 blue, 7 green, 8 orange. Under it, sensor_callback (0.5 s) in green and health_callback (1 s) in purple on the left, command_callback (each reading) in orange and watchdog_callback (1 s) in blue on the right, then single_executor_exe.
   :align: center
   :width: 35%

   One process: one main thread runs the callbacks of both nodes.

**Run the two nodes in one process:**

.. code-block:: bash

   ros2 run l11_robotaxi single_executor_exe

.. code-block:: text

   [INFO] [...] [camera_node]: sensor_callback: cone at 10 m
   [INFO] [...] [controller_node]: command_callback: cone at 10 m, speed 2 m/s
   [INFO] [...] [camera_node]: health_callback: readings since the last check = 1
   [INFO] [...] [camera_node]: sensor_callback: cone at 9 m
   [INFO] [...] [controller_node]: command_callback: cone at 9 m, speed 2 m/s
   [INFO] [...] [controller_node]: watchdog_callback: last reading 0.00 s ago

- One thread, the main thread, runs both nodes (see the circle above): each reading, then its command, 0.04 to 0.29 ms later.
- The process has 15 threads, started by ROS 2 and DDS, but none of the others ran a callback.
- As two processes, the same two nodes need two ``ros2 run`` commands: ``camera_exe`` and ``controller_exe``.

What a Slow Callback Does to the Other Callbacks
""""""""""""""""""""""""""""""""""""""""""""""""

.. important::

   **One thread, one callback at a time.** A single-threaded executor has one thread, and it runs one callback at a time. While a callback runs, every other callback waits, in every node the executor runs.

A callback is **ready** when its timer's period ends or a message arrives on its topic. When one callback runs long:

1. The callbacks that become ready meanwhile wait, and run late.
2. A timer that missed several periods runs once, so it runs less often.
3. A callback slower than its own period runs back to back.

Demo: a Slow Callback in a Single-Threaded Executor
"""""""""""""""""""""""""""""""""""""""""""""""""""

The camera and the controller above, in one ``SingleThreadedExecutor``. Lines 12 and 13 of ``src/controller_node.cpp``, inside ``command_callback``, hold a delay, commented out:

.. code-block:: cpp
   :linenos:
   :lineno-start: 12
   :emphasize-lines: 2

   // TODO: uncomment the next line: 1.4 s of work.
   // std::this_thread::sleep_for(std::chrono::milliseconds{1400});

.. code-block:: bash

   colcon build --packages-select l11_robotaxi
   source install/setup.bash
   ros2 run l11_robotaxi single_executor_exe

.. admonition:: Your turn
   :class: hint

   Run it as it is. Then uncomment line 13, build and run again. The delay is in the controller. Does the camera's ``sensor_callback`` still run every 0.5 s?

A Slow Callback Delays Every Other Callback
"""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l11/executor_timeline_slow_command.png
   :alt: Timeline with four lanes, from 0 to 5 s, and a dashed line between the top two lanes and the bottom two. Above the line, labeled no delay: sensor_callback and command_callback both have black ticks every 0.5 s from 0 to 5 s; each command_callback tick sits just right of a sensor_callback tick. Below the line, labeled 1.4 s delay: sensor_callback has black ticks at 0, 1.4, 2.8 and 4.2 s; command_callback has black bars back to back, from 0 to 1.4, 1.4 to 2.8 and 2.8 to 4.2 s, and one starting at 4.2 s. The lane labels read sensor_callback (0.5 s) and command_callback (each reading).
   :align: center
   :width: 85%

   The same two callbacks without and with the 1.4 s delay.

Above the line, command ticks are drawn 0.06 s late so both show; the real gap was 0.04 to 0.29 ms (the run above).

**Key:** each mark is one callback run: a thin tick is a fast run, a long bar is a slow one.

.. admonition:: Conclusion
   :class: important

   Each ``command_callback`` ran for 1.4 s on the one thread, so the camera read only once every 1.4 s.

Multi-Threaded Executors
^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Multi-Threaded Executor
   :class: tip

   An executor with several threads. Each thread runs one callback at a time, so several callbacks can run at the same time.

.. figure:: /_static/images/l11/mte_loops.png
   :alt: On the left, a wavy line labeled main thread, with init, makes the nodes, leads to executor.spin(). The line branches: a solid arrow into a circle labeled thread 1, the main thread, and a dashed arrow labeled starts into a circle labeled thread 2, started by spin(). Each circle holds 1. wait for an event, 2. run its callback, 3. repeat. Thread 1 has dots callback1 and callback2; thread 2 has dots callback3 and callback1. The dashed line continues down past thread 2 to three dots and the text thread 3, thread 4, ... as many as you ask for. On the right, a solid arrow from thread 1 and a dashed arrow labeled joins from thread 2 meet, past the keys Ctrl and C, at a wavy line labeled main thread, rclcpp::shutdown().
   :align: center
   :width: 85%

   A multi-threaded executor: ``executor.spin()`` starts the extra threads, and each thread loops. You choose how many threads there are.

**Key:** solid line, the main thread, which becomes thread 1 inside ``spin()``; dashed line, a thread that ``spin()`` starts and waits for after :kbd:`Ctrl+C`.

One Thread or Several Threads
"""""""""""""""""""""""""""""

A thread runs one callback at a time. Think of a thread as a cook, and a callback as an order.

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Executor
     - Threads
     - What happens
   * - Single-threaded
     - 1
     - One cook: the orders wait their turn. A slow order holds up all the others.
   * - Multi-threaded
     - You choose
     - Several cooks: several orders are made at the same moment, one per cook.

.. admonition:: Definition: Parallelism
   :class: tip

   Running two or more callbacks at the same moment, each on its own thread. Such callbacks run **in parallel**. C++ allows true parallelism: since C++11, the threads of one program (``std::thread``) can run at the same moment, each on its own CPU core.

With 3 threads, up to 3 callbacks run in parallel. A fourth waits until a thread is free.

Concurrency and Parallelism
"""""""""""""""""""""""""""

.. admonition:: Definition: Concurrency
   :class: tip

   Running two or more callbacks during the same period of time, taking turns. On one thread, they never run at the same moment: a single-threaded executor is concurrent, not parallel.

.. figure:: /_static/images/l11/concurrency_vs_parallelism.png
   :alt: Timeline with four lanes and a dashed line between the top two and the bottom two; time runs to the right, with no numbers. Above the line, labeled concurrency, 1 thread: callback1 and callback2 each have three bars, and the bars take turns, never at the same time; the last bar ends at the right of the axis. Below the line, labeled parallelism, 2 threads: callback1 and callback2 each have three bars side by side, at the same moments, and the last bars end halfway along the axis.
   :align: center
   :width: 90%

   Each bar is one callback run. The figure is drawn for illustration, not measured.

.. admonition:: Conclusion
   :class: important

   On one thread the runs take turns; on two threads they happen at the same moment, and the same work ends in half the time.

Why Not Run Every Callback in Parallel
""""""""""""""""""""""""""""""""""""""

Running callbacks in parallel is fast, but it is not always safe.

- **Safe:** two callbacks that share nothing. One reads the lidar, the other checks the battery.
- **Not safe:** two callbacks that change the same variable. If both run in parallel, each can overwrite the other's work, and the result is wrong. C++ calls this a **data race** (`cppreference: Multi-threaded executions and data races <https://en.cppreference.com/w/cpp/language/multithread>`__).

.. figure:: /_static/images/l11/racecondition.jpeg
   :alt: Screenshot of an online comment, white text on a black background, three quoted lines in the wrong order: "knock knock", "race condition", "who's there?". Below it, a thumbs-up icon with 3 thousand likes and 24 replies.
   :align: center
   :width: 40%

   A joke about a race condition: the lines come in the wrong order.

So you need a way to tell the executor which callbacks may run in parallel and which must take turns. ROS 2 calls it a **callback group**.

Callback Groups
"""""""""""""""

.. admonition:: Definition: Callback Group
   :class: tip

   A set of callbacks of one node, with one rule: may its callbacks run in parallel, or must they take turns? You create the groups and put each callback in one.

Two Types of Callback Group
"""""""""""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 28 72

   * - Type
     - Rule for the callbacks in the group
   * - **Mutually exclusive**
     - Never in parallel: one at a time. While one runs, the others wait, even when threads are free.
   * - **Reentrant**
     - In parallel, any number of them. Nothing waits. A callback can even run in parallel with itself.

- A group's rule is only about its own callbacks. Callbacks in two different groups never wait for each other.
- A callback you create without a group goes in the node's **default group**, which is mutually exclusive (`Using Callback Groups <https://docs.ros.org/en/jazzy/How-To-Guides/Using-callback-groups.html>`__). So a node's callbacks take turns unless you make groups.

The Test Node: Four Timers in Two Groups
""""""""""""""""""""""""""""""""""""""""

To see the two rules at work, we use a test node, ``callback_groups_node``. It is not the robotaxi: it has four timers, two per group. In each group, one callback is slow and one is fast.

.. list-table::
   :header-rows: 1
   :widths: 18 18 22 42

   * - Timer
     - Group
     - Runs every
     - Each run takes
   * - ``timer1``
     - group 1
     - 1 s
     - 1.5 s (slow)
   * - ``timer2``
     - group 1
     - 0.5 s
     - almost nothing (fast)
   * - ``timer3``
     - group 2
     - 1 s
     - 1.5 s (slow)
   * - ``timer4``
     - group 2
     - 0.5 s
     - almost nothing (fast)

The question for each demo: does the slow callback make the fast one wait? The numbers are chosen for this example.

The Test Node's Constructor: the Groups, and Group 1's Timers
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 14 to 26 of ``include/l11_robotaxi/callback_groups_node.hpp`` (the constructor continues below):

.. code-block:: cpp
   :linenos:
   :lineno-start: 14
   :emphasize-lines: 4-5, 9, 13

       CallbackGroupsNode(rclcpp::CallbackGroupType group1_type,
                          rclcpp::CallbackGroupType group2_type)
           : rclcpp::Node{"callback_groups_node"},
             group1_{create_callback_group(group1_type)},
             group2_{create_callback_group(group2_type)},
             timer1_{create_wall_timer(
                 std::chrono::milliseconds{1000},
                 std::bind(&CallbackGroupsNode::timer1_callback, this),
                 group1_)},
             timer2_{create_wall_timer(
                 std::chrono::milliseconds{500},
                 std::bind(&CallbackGroupsNode::timer2_callback, this),
                 group1_)},

- **Lines 17 and 18** make the two groups, of the types the constructor is given.
- **Lines 22 and 26:** the third argument puts each timer's callback in group 1.

The Test Node's Constructor: Group 2's Timers
"""""""""""""""""""""""""""""""""""""""""""""

Lines 27 to 34 of the same file, the end of the constructor:

.. code-block:: cpp
   :linenos:
   :lineno-start: 27
   :emphasize-lines: 4, 8

             timer3_{create_wall_timer(
                 std::chrono::milliseconds{1000},
                 std::bind(&CallbackGroupsNode::timer3_callback, this),
                 group2_)},
             timer4_{create_wall_timer(
                 std::chrono::milliseconds{500},
                 std::bind(&CallbackGroupsNode::timer4_callback, this),
                 group2_)} {}

- **Lines 30 and 34:** ``timer3`` and ``timer4`` go in group 2.
- Without that third argument, a timer's callback goes in the node's default group.

The Test Node: What the Four Callbacks Do
"""""""""""""""""""""""""""""""""""""""""

Lines 12 to 28 of ``src/callback_groups_node.cpp``. A slow callback waits 1.5 s (line 3 below); a fast one logs one line. Each callback prints its name in its own color:

.. code-block:: cpp
   :linenos:
   :lineno-start: 12
   :emphasize-lines: 3

   void CallbackGroupsNode::slow_work(const std::string &name, const char *color) {
       RCLCPP_INFO_STREAM(get_logger(), color << name << color::reset << " start");
       std::this_thread::sleep_for(std::chrono::milliseconds{1500});
       RCLCPP_INFO_STREAM(get_logger(), color << name << color::reset << " end");
   }

   void CallbackGroupsNode::timer1_callback() { slow_work("timer1", color::timer1); }

   void CallbackGroupsNode::timer2_callback() {
       RCLCPP_INFO_STREAM(get_logger(), color::timer2 << "timer2" << color::reset);
   }

   void CallbackGroupsNode::timer3_callback() { slow_work("timer3", color::timer3); }

   void CallbackGroupsNode::timer4_callback() {
       RCLCPP_INFO_STREAM(get_logger(), color::timer4 << "timer4" << color::reset);
   }

The ``color::`` names come from ``include/l11_robotaxi/colors.hpp``. Each one is an ANSI escape code that sets the terminal's text color, and ``color::reset`` goes back to the terminal's own color. Lines 16 to 20 of that file:

.. code-block:: cpp
   :linenos:
   :lineno-start: 16

   inline constexpr const char *timer1{"\033[38;2;21;101;192m"};   // blue
   inline constexpr const char *timer2{"\033[38;2;27;122;58m"};    // green
   inline constexpr const char *timer3{"\033[38;2;106;61;154m"};   // purple
   inline constexpr const char *timer4{"\033[38;2;179;89;0m"};     // orange
   inline constexpr const char *reset{"\033[0m"};

The main Function: Make the Node, Run It on 6 Threads
"""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 7 to 20 of ``src/two_mutex_main.cpp``, the whole ``main``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 7
   :emphasize-lines: 4-5, 7-8

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       using Type = rclcpp::CallbackGroupType;
       auto node{std::make_shared<l11_robotaxi::CallbackGroupsNode>(
           Type::MutuallyExclusive, Type::MutuallyExclusive)};
       // 6 threads: enough that no callback ever waits for a free thread.
       rclcpp::executors::MultiThreadedExecutor executor{
           rclcpp::ExecutorOptions{}, 6};
       executor.add_node(node);
       executor.spin();
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

Lines 10 and 11 make the node and choose each group's type. Lines 13 and 14 make the executor: the 6 is the number of threads (next part).

Why 6 Threads for 4 Callbacks
"""""""""""""""""""""""""""""

There are 4 callbacks, but a slow one can run **twice at the same time** (in a reentrant group, whose rule lets a callback overlap itself; demo 2 below shows it). ``timer1`` starts every 1 s and one run takes 1.5 s, so a second run starts while the first is still going. That needs 2 threads.

.. list-table::
   :header-rows: 1
   :widths: 34 40 26

   * - Callbacks
     - Most runs at the same time
     - Threads needed
   * - ``timer1``, ``timer3`` (slow)
     - 2 each
     - 2 + 2 = 4
   * - ``timer2``, ``timer4`` (fast)
     - 1 each
     - 1 + 1 = 2

With 6 threads, no run ever waits for a free thread. When a callback waits in the demos, its group is the reason.

What Happens If You Give No Number of Threads
"""""""""""""""""""""""""""""""""""""""""""""

The same line with no arguments:

.. code-block:: cpp

   rclcpp::executors::MultiThreadedExecutor executor{};

The executor then makes one thread per CPU core, and at least 2 (`rclcpp: Class MultiThreadedExecutor <https://docs.ros.org/en/jazzy/p/rclcpp/generated/classrclcpp_1_1executors_1_1MultiThreadedExecutor.html>`__).

.. list-table::
   :header-rows: 1
   :widths: 26 20 54

   * - Computer
     - Threads made
     - For our node, which uses 6 at most
   * - 32 cores
     - 32
     - 26 threads are made and never run a callback.
   * - 4 cores
     - 4
     - Too few: a run can wait for a free thread.

Extra threads do no harm, but they are wasted. Too few threads add waiting that has nothing to do with groups. So we write 6.

In the timelines below, time 0 is the first fast run. A fast timer that nothing delays runs 11 times from 0 to 5 s (5 / 0.5 + 1 = 11).

Demo 1: Both Groups Mutually Exclusive
""""""""""""""""""""""""""""""""""""""

The same ``main``, in ``src/two_mutex_main.cpp``. Only line 11 changes:

.. code-block:: cpp
   :linenos:
   :lineno-start: 7
   :emphasize-lines: 5

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       using Type = rclcpp::CallbackGroupType;
       auto node{std::make_shared<l11_robotaxi::CallbackGroupsNode>(
           Type::MutuallyExclusive, Type::MutuallyExclusive)};
       // 6 threads: enough that no callback ever waits for a free thread.
       rclcpp::executors::MultiThreadedExecutor executor{
           rclcpp::ExecutorOptions{}, 6};
       executor.add_node(node);
       executor.spin();
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

Guess first: while ``timer1`` works, does ``timer2`` wait? Does ``timer4``?

.. code-block:: bash

   ros2 run l11_robotaxi two_mutex_exe

Demo 1: The Fast Callback Waits for the Slow One of Its Group
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l11/executor_timeline_two_mutex.png
   :alt: Timeline with four lanes, timer1 to timer4, from 0 to 5 s, and a dashed line between timer2 and timer3. timer1 and timer3 each show navy bars back to back, from 0.5 to 2, 2 to 3.5 and 3.5 to 5 s, and one more starting at 5 s. timer2 and timer4 each show black ticks at 0, 0.5, 2, 3.5 and 5 s only. The lane labels give each timer's period: timer1 (1 s), timer2 (0.5 s), timer3 (1 s), timer4 (0.5 s).
   :align: center
   :width: 85%

   Two mutually exclusive groups: the slow timers run back to back, and each fast timer waits for its own group's slow timer.

**Key:** a long bar is one slow run (1.5 s); a tick is one fast run.

This is the waiting of the single-threaded executor (see "A Slow Callback Delays Every Other Callback" above), but it now stays inside each group: ``timer1`` delays ``timer2``, and never ``timer4``.

.. admonition:: Conclusion
   :class: important

   In a mutually exclusive group, the fast callback waits for the slow one: ``timer2`` ran 5 times, not 11.

Demo 1 Explained: What Mutually Exclusive Does
""""""""""""""""""""""""""""""""""""""""""""""

.. admonition:: Definition: Mutually Exclusive Group
   :class: tip

   A group whose callbacks run one at a time. While one of them runs, every other callback of the group waits, even when threads are free. A node's default group is of this type.

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Time
     - What happens in group 1
   * - 0.0 s, 0.5 s
     - ``timer2`` runs. At 0.5 s, ``timer1`` starts 1.5 s of work.
   * - 1.0 s, 1.5 s
     - ``timer2`` is ready, but waits: ``timer1`` is running.
   * - 2.0 s
     - ``timer1`` ends. ``timer2`` runs once, then ``timer1`` starts again.

.. admonition:: Conclusion
   :class: important

   ``timer2`` runs only in the short gap between two runs of ``timer1``: at 2.0, 3.5 and 5.0 s, so 5 times instead of 11.

Demo 2: Both Groups Reentrant
"""""""""""""""""""""""""""""

The same ``main``, in ``src/two_reentrant_main.cpp``. Only line 11 changes:

.. code-block:: cpp
   :linenos:
   :lineno-start: 7
   :emphasize-lines: 5

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       using Type = rclcpp::CallbackGroupType;
       auto node{std::make_shared<l11_robotaxi::CallbackGroupsNode>(
           Type::Reentrant, Type::Reentrant)};
       // 6 threads: enough that no callback ever waits for a free thread.
       rclcpp::executors::MultiThreadedExecutor executor{
           rclcpp::ExecutorOptions{}, 6};
       executor.add_node(node);
       executor.spin();
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

Guess first: does ``timer2`` still wait? And ``timer1`` starts every 1 s but works 1.5 s: what happens?

.. code-block:: bash

   ros2 run l11_robotaxi two_reentrant_exe

Demo 2: Nothing Waits, and the Slow Callback Runs Twice at Once
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l11/executor_timeline_two_reentrant.png
   :alt: Timeline with four lanes, timer1 to timer4, from 0 to 5 s, and a dashed line between timer2 and timer3. timer1 and timer3 each show navy bars 1.5 s long starting every 1 s, at 0.5, 1.5, 2.5, 3.5 and 4.5 s, drawn on two half rows because each overlaps the next. timer2 and timer4 each show black ticks every 0.5 s from 0 to 5 s. The lane labels give each timer's period: timer1 (1 s), timer2 (0.5 s), timer3 (1 s), timer4 (0.5 s).
   :align: center
   :width: 85%

   Two reentrant groups: the slow runs overlap, and every fast timer runs on time.

**Key:** a long bar is one slow run (1.5 s); a tick is one fast run.

.. admonition:: Conclusion
   :class: important

   In a reentrant group nothing waits: ``timer2`` ran 11 times, and two runs of ``timer1`` overlapped.

Demo 2 Explained: Why Two Runs of timer1 Overlap
""""""""""""""""""""""""""""""""""""""""""""""""

``timer1`` does not fire more often: it is ready once every second, as before. What changes is that a new run no longer waits for the one before it.

.. list-table::
   :header-rows: 1
   :widths: 18 82

   * - Time
     - What happens to ``timer1``
   * - 0.5 s
     - Run 1 starts. Its work takes 1.5 s, so it ends at 2.0 s.
   * - 1.5 s
     - One second has passed: the timer is ready again. Run 1 is still working.
   * - 1.5 s
     - The group is reentrant, so run 2 starts now, on another thread.
   * - 1.5 to 2.0 s
     - Runs 1 and 2 work in parallel.

In a mutually exclusive group, run 2 would wait until run 1 ends, at 2.0 s. That is what demo 1 showed.

Demo 2 Explained: What Reentrant Does
"""""""""""""""""""""""""""""""""""""

.. admonition:: Definition: Reentrant Group
   :class: tip

   A group with no "one at a time" rule. The executor starts each of its callbacks as soon as it is ready, whatever else in the group is running, even an earlier run of the same callback.

**Why the fast callbacks never overlap.** A run of ``timer2`` logs one line and ends, in far less than a millisecond. When the timer is ready again, 0.5 s later, that run ended long ago. There is nothing to overlap with.

.. admonition:: Conclusion
   :class: important

   A callback overlaps itself only when one run lasts longer than its period: 1.5 s of work every 1 s for ``timer1``.

Demo 3: One Group of Each Type
""""""""""""""""""""""""""""""

The same ``main``, in ``src/mutex_reentrant_main.cpp``. Only line 11 changes:

.. code-block:: cpp
   :linenos:
   :lineno-start: 7
   :emphasize-lines: 5

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       using Type = rclcpp::CallbackGroupType;
       auto node{std::make_shared<l11_robotaxi::CallbackGroupsNode>(
           Type::Reentrant, Type::MutuallyExclusive)};
       // 6 threads: enough that no callback ever waits for a free thread.
       rclcpp::executors::MultiThreadedExecutor executor{
           rclcpp::ExecutorOptions{}, 6};
       executor.add_node(node);
       executor.spin();
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

Guess first: group 1 is reentrant, group 2 is mutually exclusive. Which fast callback waits?

.. code-block:: bash

   ros2 run l11_robotaxi mutex_reentrant_exe

Demo 3: Only the Mutually Exclusive Group Waits
"""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l11/executor_timeline_mutex_reentrant.png
   :alt: Timeline with four lanes, timer1 to timer4, from 0 to 5 s, and a dashed line between timer2 and timer3. timer1 shows navy bars 1.5 s long starting every 1 s, at 0.5, 1.5, 2.5, 3.5 and 4.5 s, on two half rows. timer2 shows black ticks every 0.5 s from 0 to 5 s. timer3 shows navy bars back to back from 0.5 to 2, 2 to 3.5 and 3.5 to 5 s. timer4 shows black ticks at 0, 0.5, 2, 3.5 and 5 s only. The lane labels give each timer's period: timer1 (1 s), timer2 (0.5 s), timer3 (1 s), timer4 (0.5 s).
   :align: center
   :width: 85%

   Group 1 reentrant, group 2 mutually exclusive: only group 2's fast timer waits.

**Key:** a long bar is one slow run (1.5 s); a tick is one fast run.

.. admonition:: Conclusion
   :class: important

   Each group follows its own rule: ``timer4`` waited (5 runs), and ``timer2`` did not (11 runs).

The Three Demos Side by Side
""""""""""""""""""""""""""""

In 5 s, a fast timer that never waits runs 11 times:

.. list-table::
   :header-rows: 1
   :widths: 12 22 22 22 22

   * - Demo
     - Group 1
     - Group 2
     - ``timer2`` runs (group 1)
     - ``timer4`` runs (group 2)
   * - 1
     - mutually exclusive
     - mutually exclusive
     - 5
     - 5
   * - 2
     - reentrant
     - reentrant
     - 11
     - 11
   * - 3
     - reentrant
     - mutually exclusive
     - 11
     - 5

.. important::

   **What a slow callback delays.** A slow callback makes the other callbacks of its own mutually exclusive group wait, and nothing else. Give a callback that must not wait its own group.

More Multi-Threaded Examples: Two Nodes on Three Threads
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The test node showed what groups decide. The next parts run two other nodes on three threads, to show how the executor hands callbacks to threads.

Scenario: the Robotaxi's Other Sensors and Its Health Checks
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

The next parts use this scenario, not the traffic cone and not the test node. Two nodes use their default callback group, which is mutually exclusive (see the two types of callback group above). Two more nodes of the robotaxi have three timer callbacks each, and no topics. Every callback runs every 1 s and takes 0.3 s of work: it logs a start line, waits 0.3 s, and logs an end line.

``sensors_node`` reads the other sensors:

- ``lidar_callback``
- ``radar_callback``
- ``gps_callback``

``health_node`` checks the robotaxi's parts:

- ``battery_callback``
- ``tire_callback``
- ``door_callback``

Three Threads for One Node: the Code
""""""""""""""""""""""""""""""""""""

The multi-threaded executor runs ``sensors_node`` alone first. Lines 10 to 14 of ``src/mte_one_node_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 10
   :emphasize-lines: 2-3

   auto sensors{std::make_shared<l11_robotaxi::SensorsNode>()};
   rclcpp::executors::MultiThreadedExecutor executor{
       rclcpp::ExecutorOptions{}, 3};
   executor.add_node(sensors);
   executor.spin();

Lines 11 and 12 ask for 3 threads: ``spin`` starts two and uses the main thread as the third. Run it:

.. code-block:: bash

   ros2 run l11_robotaxi mte_one_node_exe

One Node: Its Three Callbacks Still Run One at a Time
"""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l11/mte_one_node.png
   :alt: Three circles side by side, each with a clockwise arrow and a label under it: thread 1, the main thread; thread 2 and thread 3, started by spin(). Each dot holds a start time and has its callback's color: gps blue, lidar gold, radar teal. The names under each circle list its dots clockwise, each followed by (1 s). Thread 1: gps at 0.0 and lidar at 1.6. Thread 2: radar at 0.3 and gps at 1.0. Thread 3: lidar at 0.6 and radar at 1.3.
   :align: center
   :width: 70%

   ``sensors_node`` on three threads: a circle is a thread, a dot is a callback run.

**Key:** a circle is a thread; a dot is a callback run, with the second it started; one color per callback.

The three timers are ready together, and they run one after another. The executor gives each run to an available thread, so a callback changes threads from run to run: in the figure, ``gps`` runs on thread 1 at 0.0 s and on thread 2 at 1.0 s.

.. important::

   **One node, one callback at a time.** A node's default callback group runs one callback at a time, so more threads do not let its callbacks overlap (see the two types of callback group above).

Two Nodes in One Multi-Threaded Executor: the Code
""""""""""""""""""""""""""""""""""""""""""""""""""

The same executor now also runs ``health_node``. Lines 12 to 18 of ``src/mte_two_nodes_main.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 12
   :emphasize-lines: 2, 6

   auto sensors{std::make_shared<l11_robotaxi::SensorsNode>()};
   auto health{std::make_shared<l11_robotaxi::HealthNode>()};
   rclcpp::executors::MultiThreadedExecutor executor{
       rclcpp::ExecutorOptions{}, 3};
   executor.add_node(sensors);
   executor.add_node(health);
   executor.spin();

Lines 13 and 17 are the only new lines: the same three threads now hold two nodes, six timers. Run it:

.. code-block:: bash

   ros2 run l11_robotaxi mte_two_nodes_exe

Two Nodes: One Callback of Each Node at a Time
""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l11/mte_two_nodes.png
   :alt: Three circles side by side, each with a clockwise arrow and a label under it: thread 1, the main thread; thread 2 and thread 3, started by spin(). Each dot holds a start time and has its callback's color: gps blue, lidar gold, radar teal, battery magenta, tire purple, door red. The names under each circle list its dots clockwise, one per line, each followed by (1 s). Thread 1: gps 0.0, tire 0.3, gps 1.0, tire 1.3. Thread 2: door 0.0, lidar 0.6, radar 1.3, battery 1.6. Thread 3: radar 0.3, battery 0.6, door 1.0, lidar 1.6.
   :align: center
   :width: 85%

   ``sensors_node`` and ``health_node`` on three threads.

**Key:** a circle is a thread; a dot is a callback run, with the second it started; one color per callback.

Each node's three timers are ready together, and each node runs one callback at a time. The executor gives each run to an available thread, so a callback changes threads from run to run: in the figure, ``lidar`` runs on thread 2 at 0.6 s and on thread 3 at 1.6 s.

.. admonition:: Conclusion
   :class: important

   Callbacks of two nodes can run at the same time; callbacks of one node cannot.


Custom Interfaces
-----------------

A **custom interface** is a message type you write yourself, in a ``.msg`` file, when no type that ROS 2 provides fits your data.

The last two sections chose which nodes start and how they run their callbacks. This section changes what the nodes send each other, and its two nodes start with ``ros2 run``. In the previous lecture, the robotaxi published its position as a ``geometry_msgs/msg/Point``, a message type that ROS 2 provides.

Three Kinds of Interface
^^^^^^^^^^^^^^^^^^^^^^^^

An **interface** is the data structure two nodes agree on. ROS 2 has three kinds, each written in its own kind of file:

.. list-table::
   :header-rows: 1
   :widths: 16 14 52 18

   * - Kind
     - File
     - Carries
     - Taught in
   * - Message
     - ``.msg``
     - The data a publisher sends on a topic to its subscribers.
     - The previous lecture and today
   * - Service
     - ``.srv``
     - A request, then one response.
     - Reading material
   * - Action
     - ``.action``
     - A goal, feedback while it runs, then a result.
     - Reading material

The message type the robotaxi published in the previous lecture, as ROS 2 shows it:

.. code-block:: bash

   ros2 interface show geometry_msgs/msg/Point

.. code-block:: text

   # This contains the position of a point in free space
   float64 x
   float64 y
   float64 z

The Fleet Needs More Than a Position
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The fleet's depot needs four things about each robotaxi, in one message, taken at one time: which robotaxi it is, what it is doing, where it is, and how much battery it has left. A ``geometry_msgs/msg/Point`` holds only the position, so you write a message type of your own, ``RobotaxiStatus``.

.. figure:: /_static/images/l11/status_graph.png
   :alt: ROS graph. A rounded box status_node has an arrow to a rounded box fleet_monitor_node, labeled /robotaxi/status above and l11_robotaxi_interfaces/msg/RobotaxiStatus below.
   :align: center
   :width: 95%

   ``status_node`` publishes ``RobotaxiStatus`` messages on ``/robotaxi/status``, and ``fleet_monitor_node`` receives them.

- ``status_node`` runs on the robotaxi and publishes its status every 1 s.
- ``fleet_monitor_node`` runs at the depot and receives each status.

Define the Message
^^^^^^^^^^^^^^^^^^

A custom message lives in a package of its own, an interface package, as a ``.msg`` file. Each line of the file is a comment, a constant or a field.

Write the Message in Its Own Package
""""""""""""""""""""""""""""""""""""

Write ``RobotaxiStatus.msg`` in a new package, then send and receive it with two new nodes of ``l11_robotaxi``.

.. list-table::
   :widths: 22 78

   * - Package
     - ``l11_robotaxi_interfaces``
   * - File
     - ``msg/RobotaxiStatus.msg``
   * - Nodes
     - none: the package holds no node
   * - Executables
     - none

Resource: `ROS 2 Jazzy: Creating custom msg and srv files <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html>`__.

.. admonition:: Definition: Interface Package
   :class: tip

   A package that holds only interface files, and no node code. Its name ends with ``_interfaces`` or ``_msgs``. Every package whose nodes use one of its messages depends on it.

Step 1: Create the Package and Its msg Folder
"""""""""""""""""""""""""""""""""""""""""""""

From the ``L11`` folder:

.. code-block:: bash

   ros2 pkg create l11_robotaxi_interfaces --license Apache-2.0 \
       --dependencies std_msgs geometry_msgs
   cd l11_robotaxi_interfaces
   rm -r include src
   mkdir msg
   touch msg/RobotaxiStatus.msg

- ``std_msgs`` and ``geometry_msgs`` hold the message types the new one uses inside it.
- The package holds no C++ code, so ``include`` and ``src`` go.

The package after Step 1:

.. code-block:: text

   l11_robotaxi_interfaces/
   ├── msg/
   │   └── RobotaxiStatus.msg
   ├── CMakeLists.txt
   ├── LICENSE
   └── package.xml

Step 2: Write RobotaxiStatus.msg
""""""""""""""""""""""""""""""""

.. code-block:: text
   :linenos:

   # The robotaxi's modes: each constant has a fixed value.
   uint8 MODE_IDLE=0
   uint8 MODE_EN_ROUTE=1
   uint8 MODE_PICKING_UP=2
   uint8 MODE_CHARGING=3

   # When the status was taken, and the frame the position is in.
   std_msgs/Header header

   string robotaxi_name          # which robotaxi of the fleet
   uint8 mode                    # one of the MODE_ constants above
   geometry_msgs/Point position  # where the robotaxi is, in m
   float32 battery               # battery level, in percent

The file name, without ``.msg``, is the type's name: ``RobotaxiStatus``. It starts with an uppercase letter, and each word starts with one too.

Why the Message Has Constants
"""""""""""""""""""""""""""""

The field ``mode`` is a number, but only four values mean something: 0, 1, 2 and 3. The constants give each one a name, as an ``enum`` does in C++.

.. list-table::
   :header-rows: 1
   :widths: 16 30 54

   * -
     - With a number
     - With a constant
   * - **The code**
     - ``msg.mode = 0;``
     - ``msg.mode = RobotaxiStatus::MODE_IDLE;``
   * - **Reading it**
     - You must remember what 0 means.
     - The name says it.
   * - **A mistake**
     - ``msg.mode = 7;`` builds and runs. The receiver gets a mode that does not exist.
     - A misspelled name does not build: the compiler finds the mistake.
   * - **Both sides agree**
     - The sender and the receiver each write their own 0.
     - Both use the one definition in the message file.

``mode`` must hold one of the four ``MODE_`` constants, and nothing else. ROS 2 does not check this: the field is a plain ``uint8``. Always assign a constant, never a number.

The Four Kinds of Line in a Message File
""""""""""""""""""""""""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 13 20 22 45

   * - Lines
     - Kind
     - Form
     - Rule
   * - 2 to 5
     - Constant
     - ``type NAME=value``
     - The name is in uppercase. ``mode_idle`` stops the build: "``'mode_idle' is an invalid constant name``".
   * - 10, 11, 13
     - Field of a built-in type
     - ``type name``
     - The name uses lowercase letters, digits and underscores, and starts with a letter.
   * - 8, 12
     - Field of another message type
     - ``package/Type name``
     - That type's package is a dependency of this one (Step 3).
   * - 1, 7
     - Comment
     - ``# text``
     - A comment can also end a line, as on lines 10 to 13.

A message is a list of fields. A field of another message type, such as ``header`` and ``position``, holds that type's own fields.

Build the Message
^^^^^^^^^^^^^^^^^

``colcon build`` turns the ``.msg`` file into C++ and Python code, once ``CMakeLists.txt`` and ``package.xml`` ask for it.

Step 3: Generate the Code from CMakeLists.txt and package.xml
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 12 to 18 of ``CMakeLists.txt``:

.. code-block:: cmake
   :linenos:
   :lineno-start: 12
   :emphasize-lines: 4-7

   find_package(rosidl_default_generators REQUIRED)

   # Generates C++ and Python code for each interface file.
   rosidl_generate_interfaces(${PROJECT_NAME}
     "msg/RobotaxiStatus.msg"
     DEPENDENCIES std_msgs geometry_msgs
   )

Add these three lines to ``package.xml``:

.. code-block:: xml
   :linenos:

   <buildtool_depend>rosidl_default_generators</buildtool_depend>
   <exec_depend>rosidl_default_runtime</exec_depend>
   <member_of_group>rosidl_interface_packages</member_of_group>

- Lines 15 to 18 turn each listed file into code. ``DEPENDENCIES`` names the packages of the types used inside: ``Header`` and ``Point``.
- In ``package.xml``, line 1: the build needs the code generators. Line 2: a node that uses the message needs the runtime library. Line 3: this is an interface package, with code for every client library.

Step 4: Build the Package and Show the Message
""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: bash

   colcon build --packages-select l11_robotaxi_interfaces
   source install/setup.bash
   ros2 interface show l11_robotaxi_interfaces/msg/RobotaxiStatus

.. code-block:: text

   std_msgs/Header header
       builtin_interfaces/Time stamp
           int32 sec
           uint32 nanosec
       string frame_id
   ...
   geometry_msgs/Point position  # where the robotaxi is, in m
       float64 x
       float64 y
       float64 z
   float32 battery               # battery level, in percent

The output repeats the file; this part skips the constants. Each field of another message type is shown with its own fields, indented under it.

What the Build Generated: a C++ Type
""""""""""""""""""""""""""""""""""""

The build first turns ``RobotaxiStatus.msg`` into an ``.idl`` file (IDL stands for Interface Definition Language), then generates the C++ and Python code from it, in ``install/l11_robotaxi_interfaces``. In C++:

.. list-table::
   :header-rows: 1
   :widths: 22 78

   * - You need
     - You write
   * - The header
     - ``#include <l11_robotaxi_interfaces/msg/robotaxi_status.hpp>``
   * - The type
     - ``l11_robotaxi_interfaces::msg::RobotaxiStatus``
   * - A constant
     - ``RobotaxiStatus::MODE_EN_ROUTE``
   * - A field, and a field's field
     - ``msg.mode``, ``msg.position.x``, ``msg.header.stamp``

.. important::

   **From a .msg file to a C++ type.** A file ``Type.msg`` in the package ``pkg`` becomes the C++ type ``pkg::msg::Type``, from the header ``pkg/msg/type.hpp``: the name in lowercase, with underscores between words (``robotaxi_status.hpp``).

Use the Message
^^^^^^^^^^^^^^^

Two new nodes of ``l11_robotaxi`` send and receive ``RobotaxiStatus``. Their package depends on ``l11_robotaxi_interfaces``, and their code includes the generated header.

Depend on the Interface Package
"""""""""""""""""""""""""""""""

In ``l11_robotaxi``, line 15 of ``package.xml``:

.. code-block:: xml

   <depend>l11_robotaxi_interfaces</depend>

Line 30 and lines 64 and 65 of ``CMakeLists.txt``; lines 66 and 67 do the same for ``fleet_monitor_exe``:

.. code-block:: cmake
   :linenos:
   :lineno-start: 30

   find_package(l11_robotaxi_interfaces REQUIRED)

.. code-block:: cmake
   :linenos:
   :lineno-start: 64

   add_executable(status_exe src/status_main.cpp src/status_node.cpp)
   ament_target_dependencies(status_exe rclcpp l11_robotaxi_interfaces)

Build both packages with ``colcon build --packages-up-to l11_robotaxi``: it builds ``l11_robotaxi_interfaces`` first, since ``l11_robotaxi`` depends on it.

status_node: Fill the Message and Publish It
""""""""""""""""""""""""""""""""""""""""""""

Lines 8 to 22 of ``src/status_node.cpp``, in the timer callback ``publish_status``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 8
   :emphasize-lines: 1, 8, 12, 15

   RobotaxiStatus msg{};
   msg.header.stamp = now();
   msg.header.frame_id = "map";
   msg.robotaxi_name = "robotaxi_1";
   // The rider waits 3 m ahead: drive 1 m per status until there.
   if (x_ < 3.0) {
       x_ += 1.0;
       msg.mode = RobotaxiStatus::MODE_EN_ROUTE;
   } else {
       msg.mode = RobotaxiStatus::MODE_PICKING_UP;
   }
   msg.position.x = x_;
   battery_ -= 0.5F;
   msg.battery = battery_;
   publisher_->publish(msg);

Line 8 makes a message, every field zero or empty. Line 15 uses a constant, line 19 a field's field, and line 22 publishes.

fleet_monitor_node: Read the Mode with the Constants
""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 9 to 19 of ``src/fleet_monitor_node.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 9
   :emphasize-lines: 3, 5, 7, 9

   void FleetMonitorNode::on_status(const RobotaxiStatus &msg) {
       std::string mode{"unknown"};
       if (msg.mode == RobotaxiStatus::MODE_IDLE) {
           mode = "idle";
       } else if (msg.mode == RobotaxiStatus::MODE_EN_ROUTE) {
           mode = "en route";
       } else if (msg.mode == RobotaxiStatus::MODE_PICKING_UP) {
           mode = "picking up";
       } else if (msg.mode == RobotaxiStatus::MODE_CHARGING) {
           mode = "charging";
       }

Lines 11 to 17 compare ``msg.mode`` with the constants by name, not with the numbers 0 to 3. Lines 20 to 22 then log the name, the mode, ``x`` and the battery level.

Run the Two Nodes
"""""""""""""""""

Terminal 1:

.. code-block:: bash

   ros2 run l11_robotaxi fleet_monitor_exe

Terminal 2:

.. code-block:: bash

   ros2 run l11_robotaxi status_exe

Terminal 1 shows (``[...]`` stands for the log level and the time):

.. code-block:: text

   [...] [fleet_monitor_node]: on_status: robotaxi_1 en route at x = 1 m, 79.5 %
   [...] [fleet_monitor_node]: on_status: robotaxi_1 en route at x = 2 m, 79 %
   [...] [fleet_monitor_node]: on_status: robotaxi_1 en route at x = 3 m, 78.5 %
   [...] [fleet_monitor_node]: on_status: robotaxi_1 picking up at x = 3 m, 78 %

``ros2 topic echo --once /robotaxi/status``, in part:

.. code-block:: text

   robotaxi_name: robotaxi_1
   mode: 2
   position:
     x: 3.0
   battery: 78.0

.. admonition:: Conclusion
   :class: important

   The monitor received the whole status in one message; on the topic the mode is the number 2, which the monitor prints as "picking up".

Custom Interfaces: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Write a message type in a ``.msg`` file: constants, fields of built-in types, and fields of other message types.
   - Put it in an interface package, and generate its code from ``CMakeLists.txt`` and ``package.xml``.
   - Check it with ``ros2 interface show``.
   - Use it from another package's nodes: depend on the interface package, include the generated header, fill and read the fields.

Services and actions are written the same way, in ``.srv`` and ``.action`` files: see the reading material :doc:`Services and Actions </reading_material/services_actions/sa_index>`.

Next Class
----------

- **Next lecture**: *L12: Simulation, Control and Parameters*. The ROSbot in Gazebo, driven by a proportional controller, then parameters. Quiz 5.
- **Pre-work**: install the :doc:`ROSbot simulation </setup/rosbot_simulation>`, and complete the L11 exercises and quiz on ReadTheDocs.
- **Required reading**:

  - `ROS 2 Jazzy: Creating a launch file <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`__
  - `ROS 2 Jazzy: Executors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`__
  - `ROS 2 Jazzy: Creating custom msg and srv files <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html>`__
