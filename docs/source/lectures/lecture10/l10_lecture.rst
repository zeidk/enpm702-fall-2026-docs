====================================================
Lecture
====================================================

Read the :doc:`l10_prereading` first. This page starts where it ends: it uses its terms (node, process, DDS, workspace, ``colcon build``, the overlay) without defining them again.

Code for This Lecture
---------------------

The package ``robotaxi_demo`` is in the course's ROS repository, `zeidk/enpm702-fall-2026-ros <https://github.com/zeidk/enpm702-fall-2026-ros>`_, cloned into the ``src`` folder of your workspace:

.. code-block:: text

   robotaxi_demo/
   ├── CMakeLists.txt
   ├── package.xml
   ├── include/robotaxi_demo/
   │   ├── hello_node.hpp
   │   ├── robotaxi_node.hpp
   │   └── dispatcher_node.hpp
   └── src/
       ├── hello_main.cpp
       ├── robotaxi_main.cpp
       ├── robotaxi_node.cpp
       ├── dispatcher_main.cpp
       └── dispatcher_node.cpp

Build it from the workspace's top folder, then run one of its three executables (``hello``, ``robotaxi``, ``dispatcher``):

.. code-block:: bash

   colcon build --packages-select robotaxi_demo
   source install/setup.bash
   ros2 run robotaxi_demo robotaxi

What This Lecture Uses from the Pre-Reading
-------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 28 72
   :class: compact-table

   * - Term
     - Meaning
   * - Node
     - A program, or a part of one, that does one job and exchanges data with other nodes, such as ``robotaxi``.
   * - Process
     - A program that is running, with its own memory and process ID.
   * - Distributed
     - Several programs, each its own process, that send each other messages instead of calling functions. ROS 2 works this way.
   * - DDS
     - The middleware that finds the nodes and moves their messages. Nodes see each other only with the same domain ID.
   * - ``rclcpp``
     - The C++ library for writing nodes: ``#include <rclcpp/rclcpp.hpp>``.
   * - Workspace
     - A folder with ``src`` (your code), ``build``, ``install`` and ``log``.
   * - ``colcon build``
     - Builds every package in ``src``, from the workspace's top folder.
   * - ``source install/setup.bash``
     - Lets this terminal find the packages you built. Run it after each build that adds one.
   * - Underlay, overlay
     - ``/opt/ros/jazzy`` is the underlay. Your workspace, sourced after it, is the overlay: when a package is in both, the overlay wins.
   * - ``ros2 pkg create``
     - Created ``robotaxi_demo`` in ``src``, with ``package.xml`` and ``CMakeLists.txt``.

ROS 2 Fundamentals and Architecture
-----------------------------------

ROS 2 nodes exchange data in three ways: **topics**, **services** and **actions**. This section shows the three, then studies topics on a fleet of robotaxis and starts the first nodes.

Communication Paradigms
^^^^^^^^^^^^^^^^^^^^^^^

Three Ways Nodes Talk: Topics, Services, Actions
""""""""""""""""""""""""""""""""""""""""""""""""

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item-card:: Topics (publish-subscribe)

      - A one-way stream of data, for as long as the publisher runs.
      - Sensor readings, speed commands, the robotaxi's position every 0.5 s.
      - Publishers and subscribers do not know each other: adding one changes nothing for the others.

   .. grid-item-card:: Services (request-response)

      - One request, one response.
      - The caller waits for the response, so a service must "return quickly" (`Services <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Services.html>`_).
      - No progress reports, and the caller cannot cancel it.
      - "Close the gripper." "Is this robotaxi free?"

   .. grid-item-card:: Actions (long-running requests)

      - A task that "may take several seconds (or minutes)" (`Actions <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Actions.html>`_).
      - While it runs, it reports its progress (**feedback**), and the caller can cancel it.
      - "Drive to the pickup point." Navigation, manipulation, perception routines.

This lecture is about topics. Services and actions come in a later lecture.

The Three Ways on One Robot: a Camera, a Laptop and an Arm
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/three_ways.png
   :alt: Three white node boxes, camera at the top, planner at the left and arm_controller at the right. An arrow labeled publish goes from camera to a navy box that reads topic, pose, with tag 1 beside it, and an arrow labeled subscribe from the pose box to planner. An arrow goes from planner to a green box that reads service, close gripper, with tag 3 above it, and on to arm_controller. A second arrow goes from planner down to a purple box that reads action, go to pose, with tag 2 below it, and on to arm_controller.
   :align: center
   :width: 60%

   A topic, an action and a service on one robot, tagged 1 to 3 as in the list below.

1. **Topic** ``pose``: ``camera`` publishes an object's pose many times a second. ``planner`` subscribes.
2. **Action** ``go to pose``: ``planner`` sends a goal. ``arm_controller`` reports progress until the arm gets there.
3. **Service** ``close gripper``: ``planner`` sends one request. ``arm_controller`` closes the gripper and responds once.

Each white box is a node. ``planner`` runs on a laptop.

The Computation Graph
^^^^^^^^^^^^^^^^^^^^^

The Computation Graph: Every Node and Every Link
""""""""""""""""""""""""""""""""""""""""""""""""

.. admonition:: Definition: Computation Graph
   :class: tip

   The network of running nodes and the links between them. The nodes are the vertices; the topics, services and actions are the edges. It shows the whole data flow of the robot.

- The graph changes while the robot runs: a node can start, stop or change its links without a restart of the others.
- Because DDS carries the messages over the network, the nodes of one graph can run on several computers. The same code runs on one laptop first and on the robot's computers later.

One Graph on Two Machines
"""""""""""""""""""""""""

.. figure:: /_static/images/l10/two_machines.png
   :alt: Two dashed gray boxes. The left one, Machine 1: Robot Computer, holds the nodes camera, lidar, imu, sensor_fusion and control. Arrows labeled /camera/info, /scan and /imu/data go from camera, lidar and imu into sensor_fusion. A red dashed arrow labeled /reset goes from control back to sensor_fusion. Between the machines, under the words Network: DDS discovery and transport, three arrows cross: /camera/image, from camera to perception, on one row; /fused/obstacles, from sensor_fusion to planning, on one row; /trajectory, from planning to control. The right box, Machine 2: Processing/Monitoring, holds perception and planning, with an arrow labeled /detected_objects from perception to planning.
   :align: center
   :width: 100%

   One computation graph spread over two computers.

- Boxes are nodes. Each arrow is a topic, from the publisher to the subscriber, with the topic's name beside it. Three topics cross the network; the nodes on each side do not know where the other side runs.
- The red dashed arrow, ``/reset``, goes against the data flow: ``control`` asks ``sensor_fusion`` to start over.

Publish/Subscribe Model
^^^^^^^^^^^^^^^^^^^^^^^

Publish and Subscribe: Nodes Share a Topic, Not a Call
""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. admonition:: Definition: Topic
   :class: tip

   A **topic** is a name, such as ``/robotaxi/position``, that nodes use to exchange messages of one type. A **publisher** sends messages to a topic. Every **subscriber** of that topic receives them.

The publisher sends when it has data. It does not wait for an answer, and it never calls the subscriber: the two only share the topic's name.

.. admonition:: What publish and subscribe gives you
   :class: key-box

   - **Loose coupling:** a node does not need to know that the others exist.
   - **Scalability:** a new publisher or subscriber joins without a change to the others.
   - **Fault tolerance:** nodes start and stop on their own.
   - **Flexible patterns:** one to many, many to one, many to many.
   - **Quality of Service:** the delivery settings are chosen per publisher and subscriber.

A Topic Works Like a Bus
""""""""""""""""""""""""

The ROS 2 documentation compares publish/subscribe to a **bus** in electronics: shared wires that many devices connect to, so every device reads what one device sends (`Topics <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Topics.html>`_). A topic has no wire: DDS gives each subscriber its own copy.

One position, from the robotaxi to the dispatcher:

1. **Find.** The two nodes find each other, because they use the same domain ID (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_).
2. **Match.** DDS connects them, because the topic name and the message type are the same.
3. **Send.** DDS turns the ``Point`` into bytes (**serialization**) and sends them with RTPS, the protocol of DDS: over UDP to another computer, or through shared memory on the same computer.
4. **Receive.** DDS turns the bytes back into a ``Point`` (**deserialization**) and hands it to the dispatcher.

Steps 1 and 2 happen when the nodes start. Steps 3 and 4 happen for every message, every 0.5 s.

The Running Example: a Fleet of Robotaxis
"""""""""""""""""""""""""""""""""""""""""

The next parts state four rules and four patterns of topics. All of them use one example, a fleet of robotaxis and the office that dispatches them.

.. figure:: /_static/images/l10/robotaxi_graph.png
   :alt: Two white boxes, robotaxi on the left and dispatcher on the right. An arrow goes from robotaxi to dispatcher, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 80%

   The robotaxi publishes its position; the dispatcher subscribes to it.

- **Nodes:** each robotaxi is a node, and the dispatcher is a node.
- **Topics:** names such as ``/robotaxi/position``. A robotaxi publishes on it; the dispatcher subscribes to it.
- **Messages:** the data, one piece at a time. Here a position of type ``geometry_msgs/msg/Point``: three numbers, ``x``, ``y`` and ``z``.

Four Rules of a Topic
^^^^^^^^^^^^^^^^^^^^^

A publisher and a subscriber never call each other. They only share a topic, so four rules decide whether a message arrives.

Rule 1: Publisher and Subscriber Use the Same Topic Name
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/rule_name.png
   :alt: The node robotaxi on the left, a red dashed box in the middle that reads different names: nothing arrives, and the node dispatcher on the right. An arrow from robotaxi to the box has the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. A red dashed arrow from the box to dispatcher has the topic name /robotaxi/pose above it and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 60%

The dispatcher subscribes to ``/robotaxi/pose`` by mistake. The robotaxi publishes on ``/robotaxi/position``. The dispatcher receives nothing, and no error is printed.

Rule 2: Publisher and Subscriber Use the Same Message Type
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/rule_type.png
   :alt: The node robotaxi on the left, a red dashed box in the middle that reads different types: nothing arrives, and the node dispatcher on the right. An arrow from robotaxi to the box has the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. A red dashed arrow from the box to dispatcher has the topic name /robotaxi/position above it and the message type std_msgs/msg/String below it.
   :align: center
   :width: 60%

Same name, different types: the two do not connect. A subscriber of ``String`` receives nothing from a publisher of ``Point``.

Rule 3: A Publisher Does Not Wait for Subscribers
"""""""""""""""""""""""""""""""""""""""""""""""""

The robotaxi publishes every 0.5 s, whether or not a node listens. A dispatcher that starts late gets only the messages sent after it starts.

.. figure:: /_static/images/l10/rule_no_wait_1.png
   :alt: The node robotaxi on the left. A red dashed arrow goes right to a red dashed box that reads: no subscriber yet, messages are lost. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 1: before the dispatcher starts.

.. figure:: /_static/images/l10/rule_no_wait_2.png
   :alt: The node robotaxi on the left, an arrow to the node dispatcher on the right, marked started later. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 2: after the dispatcher starts.

Rule 4: A Subscriber Does Not Need a Publisher
""""""""""""""""""""""""""""""""""""""""""""""

The dispatcher can start first. It waits, with no error, and its callback runs once a robotaxi starts publishing. So the order in which you start the two nodes does not matter.

.. figure:: /_static/images/l10/rule_no_publisher_1.png
   :alt: A red dashed box on the left reads: no publisher yet. A red dashed arrow goes right to the node dispatcher, marked waits. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 1: before the robotaxi starts.

.. figure:: /_static/images/l10/rule_no_publisher_2.png
   :alt: The node robotaxi on the left, marked started later, an arrow to the node dispatcher on the right. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 2: after the robotaxi starts.

Four Patterns
^^^^^^^^^^^^^

Pattern 1: One Publisher, Many Subscribers
""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_one_to_many.png
   :alt: The node robotaxi on the left. One line goes right from it, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. At a dot the line splits into two arrows: one up to the node dispatcher and one down to the node _ros2cli_84035, marked ros2 topic echo.
   :align: center
   :width: 70%

Every subscriber gets its own copy of each message. ``ros2 topic echo`` runs as a node, ``_ros2cli_84035`` in this run (the number is its process id). Adding it changes nothing for the robotaxi or the dispatcher.

Pattern 2: Many Publishers, One Topic
"""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_many_to_one.png
   :alt: Three nodes on the left, robotaxi_1, robotaxi_2 and robotaxi_3, each with an arrow to the node dispatcher on the right. Along each arrow, the topic name /fleet/position is on one side and the message type geometry_msgs/msg/Point on the other.
   :align: center
   :width: 70%

A fleet of three robotaxis publishes on one topic. The dispatcher gets every position, from all three, in the order they arrive.

Pattern 3: One Node, Several Topics
"""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_two_topics.png
   :alt: The node robotaxi at the top, with two straight arrows down at the same angle: one to the node dispatcher, with the topic name /robotaxi/position on one side and the message type geometry_msgs/msg/Point on the other, and one to the node battery_monitor, with the topic name /robotaxi/battery on one side and the message type sensor_msgs/msg/BatteryState on the other.
   :align: center
   :width: 70%

One topic per kind of data. Each node subscribes only to what it uses: the dispatcher never receives battery messages.

Pattern 4: One Node Publishes and Subscribes
""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_both_ways.png
   :alt: The nodes robotaxi and dispatcher side by side. An arrow goes from robotaxi to dispatcher, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. A second arrow, below the first, goes from dispatcher back to robotaxi, with the message type geometry_msgs/msg/Point above it and the topic name /robotaxi/pickup below it.
   :align: center
   :width: 70%

The dispatcher reads positions and sends back a pickup point on another topic. Each node is a publisher on one topic and a subscriber on the other.

Running Nodes
^^^^^^^^^^^^^

Two Ways to Start Nodes
"""""""""""""""""""""""

1. ``ros2 run <package> <executable>`` starts exactly one node.
2. ``ros2 launch <package> <launch file>`` starts one or more nodes, with their settings.

.. note::

   **When to use each**

   - ``ros2 run``: a quick test, one node to debug, a short demonstration.
   - ``ros2 launch``: a whole system, many nodes, settings that change from one run to the next.

Both need a terminal that has sourced ROS 2 (``source /opt/ros/jazzy/setup.bash``). The next two parts try each one on two nodes that come with ROS 2.

ros2 run: the Talker and the Listener
"""""""""""""""""""""""""""""""""""""

The package ``demo_nodes_cpp`` comes with ROS 2. Its executable ``talker`` publishes a string every second on the topic ``/chatter``; ``listener`` prints what it receives.

.. figure:: /_static/images/l10/talker_listener.png
   :alt: Two white boxes, talker on the left and listener on the right. An arrow goes from talker to listener, with the topic name /chatter above it and the message type std_msgs/msg/String below it.
   :align: center
   :width: 60%

**Terminal 1:** ``ros2 run demo_nodes_cpp talker``

.. code-block:: text

   [INFO] [...] [talker]: Publishing: 'Hello World: 1'
   [INFO] [...] [talker]: Publishing: 'Hello World: 2'

**Terminal 2, 1 s later:** ``ros2 run demo_nodes_cpp listener``

.. code-block:: text

   [INFO] [...] [listener]: I heard: [Hello World: 2]
   [INFO] [...] [listener]: I heard: [Hello World: 3]

The listener's first message is number 2: it started after message 1 was sent, and nothing kept message 1 for it (rule 3). Stop either node with :kbd:`Ctrl+C` and start it again: the other one goes on.

ros2 launch: Both Nodes with One Command
""""""""""""""""""""""""""""""""""""""""

A **launch file** lists the nodes to start and their settings. One command starts them all: ``ros2 launch demo_nodes_cpp talker_listener_launch.py``

.. code-block:: text

   [INFO] [talker-1]: process started with pid [1822961]
   [INFO] [listener-2]: process started with pid [1822962]
   [talker-1] [INFO] [...] [talker]: Publishing: 'Hello World: 1'
   [listener-2] [INFO] [...] [listener]: I heard: [Hello World: 1]

**What a launch file gives you**

- **Automation:** a whole robot system from one command.
- **Configuration:** parameters, namespaces and remapped names.
- **Coordination:** which nodes depend on which, and the start order.
- **Flexibility:** one file per deployment.

**Three file types**

- ``*_launch.py``: Python, the most flexible and the most common.
- ``*_launch.xml``: XML, declarative, good for simple cases.
- ``*_launch.yaml``: YAML, a readable configuration.

Two pids: each node is its own process. One :kbd:`Ctrl+C` stops both. Writing launch files comes in a later lecture.

Introspection Tools
^^^^^^^^^^^^^^^^^^^

Look inside a Running System: the ros2 Command-Line Tools
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

1. ``ros2 node <verb>``: the running nodes.

   - ``ros2 node list`` lists every node. ``ros2 node info <node>`` shows one node's topics and services.

2. ``ros2 topic <verb>``: the topics and their messages.

   - ``ros2 topic list -t`` lists the topics with their types. ``ros2 topic info <topic>`` counts its publishers and subscribers.
   - ``ros2 topic echo <topic>`` prints each message. ``ros2 topic hz <topic>`` measures messages per second.
   - ``ros2 topic pub <topic> <type> <values>`` publishes a message you type.

3. ``ros2 interface <verb>``: the message types.

   - ``ros2 interface list`` lists every type. ``ros2 interface show <type>`` prints its fields.

4. ``rqt_graph``: the computation graph, drawn in a window.

Inspect the Talker and the Listener from a Third Terminal
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 32 24 44
   :class: compact-table

   * - Command
     - What it shows
     - Output
   * - ``ros2 node list``
     - The running nodes
     - ``/listener``, ``/talker``
   * - ``ros2 topic list -t``
     - Each topic and its type
     - ``/chatter [std_msgs/msg/String]``
   * - ``ros2 topic info /chatter``
     - How many publish and subscribe
     - ``Publisher count: 1``, ``Subscription count: 1``
   * - ``ros2 topic echo /chatter``
     - Each message, as it arrives
     - ``data: 'Hello World: 6'``
   * - ``ros2 topic hz /chatter``
     - Messages per second
     - ``average rate: 1.000``
   * - ``rqt_graph``
     - The computation graph, in a window
     - The talker and listener figure

``ros2 topic list -t`` also shows ``/rosout`` and ``/parameter_events``: every node makes them, for its log lines and its parameters.

Packages
^^^^^^^^

Reuse Code: the Package Ecosystem
"""""""""""""""""""""""""""""""""

.. admonition:: Definition: Package
   :class: tip

   A **package** is one folder of nodes, libraries, settings and launch files that does one thing, such as ``demo_nodes_cpp``. Every package has the same layout, so it is easy to build, share and reuse.

- The ecosystem holds packages for drivers, perception, planning, simulators, debugging and visualization.
- Few robots are written from scratch. You combine existing packages and write the ones your robot still needs.
- ``ros2 pkg list`` printed 500 package names on the course laptop, before any package of our own.

Two Places a Package Comes From: apt or Your Workspace
""""""""""""""""""""""""""""""""""""""""""""""""""""""

**Debian packages**

- Installed in ``/opt/ros/jazzy/share``.
- Installed with ``sudo apt install ros-jazzy-<name>``.
- Use them for stable parts and for production: ``apt`` also installs what they depend on.

**Source packages**

- Kept in the ``src`` folder of your workspace.
- Built with ``colcon build``.
- Use them for development: you can read, change and debug the code.

.. note::

   A source package with the same name as an installed one takes its place when you source your workspace (the overlay, from the :doc:`l10_prereading`).

.. warning::

   Never edit the files in ``/opt/ros/jazzy``: the next ``sudo apt upgrade`` replaces them. Copy the source into your workspace instead.

Alternative Frameworks
^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 24 38 38
   :class: compact-table

   * - Framework
     - What it is
     - How it differs from ROS 2
   * - Microsoft Robotics Developer Studio (MRDS)
     - Windows tools, visual programming, a simulator
     - Windows only; little support today, small ecosystem
   * - Open Robot Control Software (OROCOS)
     - Real-time control with fixed timing, for industrial systems
     - More specialized; ROS 2 integrates more parts and is more modular
   * - MOOS-IvP
     - Written for marine robots and their missions
     - Marine only; ROS 2 covers every kind of robot
   * - YARP
     - Strong communication between processes, modular parts
     - Communication only; ROS 2 adds standard DDS middleware and more tools
   * - Custom solutions
     - Written for one robot's hardware and performance needs
     - Hard to port, no community, hard to maintain for years

.. note::

   Choose ROS 2 when you need a fast start, a large set of existing packages, a community, and standard interfaces.

Resources
^^^^^^^^^

- Official website: `ros.org <https://www.ros.org/>`_
- ROS 2 documentation: `docs.ros.org/en/jazzy <https://docs.ros.org/en/jazzy/>`_
- Tutorials: `docs.ros.org/en/jazzy/Tutorials.html <https://docs.ros.org/en/jazzy/Tutorials.html>`_
- Package index: `index.ros.org <https://index.ros.org>`_
- Community forum: `discourse.ros.org <https://discourse.ros.org/>`_
- ROS Enhancement Proposals: `ros.org/reps <https://www.ros.org/reps/>`_
- GitHub organizations: ``ros2``, ``ros-planning``, ``ros-perception``

Workspace and Development Environment
-------------------------------------

In the pre-reading, you built a workspace and created the package ``robotaxi_demo``. This section reads the two files that describe it, ``package.xml`` and ``CMakeLists.txt``, and the commands that use them.

Packages in Your Workspace
^^^^^^^^^^^^^^^^^^^^^^^^^^

Package Discovery: the ros2 pkg Commands
""""""""""""""""""""""""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - Command
     - Output on the course laptop
   * - ``ros2 pkg list``
     - 501 package names, ``robotaxi_demo`` among them
   * - ``ros2 pkg executables robotaxi_demo``
     - ``robotaxi_demo dispatcher``, ``robotaxi_demo hello``, ``robotaxi_demo robotaxi``
   * - ``ros2 pkg prefix robotaxi_demo``
     - ``<workspace>/install/robotaxi_demo``: the overlay
   * - ``ros2 pkg prefix rclcpp``
     - ``/opt/ros/jazzy``: the underlay
   * - ``ros2 pkg xml robotaxi_demo``
     - The package's ``package.xml``

``ros2 pkg prefix`` tells you which layer a package comes from. To change an installed package, copy its source into ``src`` and build it there: the overlay wins.

Package Manifest: package.xml
"""""""""""""""""""""""""""""

The first lines of the repository's ``package.xml``:

.. code-block:: xml
   :linenos:
   :emphasize-lines: 2, 4, 5, 10, 11

   <package format="3">
     <name>robotaxi_demo</name>
     <version>0.0.0</version>
     <description>Robotaxi and dispatcher nodes.</description>
     <maintainer email="zeid.kootbally@gmail.com">zeidk</maintainer>
     <license>Apache-2.0</license>

     <buildtool_depend>ament_cmake</buildtool_depend>

     <depend>rclcpp</depend>
     <depend>geometry_msgs</depend>

- Lines 4 to 6: ``ros2 pkg create`` writes ``TODO`` in the description and the license. Replace both right after you create the package.
- Lines 10 and 11: ``<depend>``: the package needs another package to build and to run.

What package.xml Is Used For
""""""""""""""""""""""""""""

1. **Build order:** ``colcon`` builds a package after the packages it depends on.
2. **Installing what is missing:** from the workspace's top folder, ``rosdep install --from-paths src --ignore-src -y`` installs every ``<depend>`` that is not installed yet. In our workspace it printed ``All required rosdeps installed successfully``.
3. **The package index:** `index.ros.org <https://index.ros.org>`_ reads the same fields when a package is published.

**The fields to fill in**

- ``<description>``: one clear sentence on what the package does.
- ``<maintainer>``: your name and email, for questions.
- ``<license>``: the legal terms (Apache-2.0, MIT, BSD, and others).
- ``<version>``: three numbers, such as 1.0.0.
- Dependencies: ``<depend>``, or ``<build_depend>`` and ``<exec_depend>`` when a package is needed only to build or only to run.

Build Configuration: CMakeLists.txt
"""""""""""""""""""""""""""""""""""

``CMakeLists.txt`` tells ``ament_cmake`` how to build the executables and the libraries of a C++ package, and what to install. The commands of ours, in order:

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - Command
     - What it does in our package
   * - ``cmake_minimum_required``
     - Sets the oldest CMake that can build the package: 3.8.
   * - ``project``
     - Names the package, ``robotaxi_demo``. The name must match ``package.xml``.
   * - ``find_package``
     - Finds one package we depend on, such as ``rclcpp``. One line per dependency.
   * - ``add_executable``
     - Builds the executable ``hello`` from ``src/hello_main.cpp``.
   * - ``ament_target_dependencies``
     - Gives ``hello`` the ROS packages it uses: ``rclcpp``.
   * - ``install``
     - Copies each executable to ``lib/${PROJECT_NAME}``, where ``ros2 run`` looks for it.
   * - ``ament_package``
     - Finishes the package. It must be the last line.

.. warning::

   Each new node needs its lines here: the build system knows only what this file tells it.

Where ros2 run and ros2 launch Find Files
"""""""""""""""""""""""""""""""""""""""""

The ``install`` command in ``CMakeLists.txt`` says what the package installs and where.

.. admonition:: The install folder
   :class: key-box

   ``colcon build`` copies what ``install`` lists (executables, launch files, configuration files) into ``install``. ``ros2 run <package> <executable>`` and ``ros2 launch <package> <file>`` start them from there, not from ``src``.

ROS 2 Daemon
^^^^^^^^^^^^

The first ``ros2`` command starts the **daemon**, a background program that keeps a list of the running nodes, topics, services and actions. The next commands ask it, so they answer at once instead of waiting for discovery.

- ``ros2 daemon status`` says whether it runs, for example ``The daemon is not running``.
- ``ros2 daemon stop`` stops it. The next command starts a fresh one.
- ``ros2 daemon start`` starts it by hand; this is rarely needed.

.. note::

   **When to restart it:** ``ros2 node list`` or ``ros2 topic list`` shows a node you stopped, or misses one you started; you changed ``ROS_DOMAIN_ID``; the network changed. Run ``ros2 daemon stop``, then the command again.

Writing Your First Node
-----------------------

The package of the last section has a build file but no code. This section writes a first node, in two forms: a function, then a class.

- **Goal:** a node that prints ``Hello from hello`` in the terminal.
- **Concepts:** starting ROS 2, logging, and a clean stop.
- **Build:** the lines to add to ``CMakeLists.txt``, and ``colcon build``.
- **Run:** ``ros2 run``.

Simple Functional Node
^^^^^^^^^^^^^^^^^^^^^^

Write a Node with No Class
""""""""""""""""""""""""""

Write a node, without a class of our own, that logs ``Hello from hello`` and ends.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - Package
     - ``robotaxi_demo``
   * - File
     - ``src/hello_function.cpp``
   * - Node
     - ``hello``
   * - Executable
     - ``hello_function``

**Edit** ``src/hello_function.cpp``:

.. code-block:: cpp
   :linenos:

   #include <memory>
   #include <rclcpp/rclcpp.hpp>
   int main(int argc, char** argv) {
     rclcpp::init(argc, argv);
     auto node{std::make_shared<rclcpp::Node>("hello")};
     RCLCPP_INFO_STREAM(node->get_logger(),
                        "Hello from " << node->get_name());
     rclcpp::shutdown();
   }

Understanding the Code
""""""""""""""""""""""

- ``rclcpp::init(argc, argv)``: starts ROS 2 and the middleware. It reads the ROS arguments from the command line. Call it before you make any node.
- ``std::make_shared<rclcpp::Node>("hello")``: makes a node named ``hello``, in a ``std::shared_ptr``. ROS 2 functions such as ``rclcpp::spin`` take the node as a shared pointer. A node's name must be unique on the network.
- ``RCLCPP_INFO_STREAM(node->get_logger(), ...)``: logs one line at the INFO level, with ``<<`` as ``std::cout``. The node's logger adds the time and the node's name. The other levels are ``DEBUG``, ``WARN``, ``ERROR`` and ``FATAL`` (`Logging <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Logging.html>`_).
- ``rclcpp::shutdown()``: stops ROS 2 and frees what ``init`` set up. :kbd:`Ctrl+C` also triggers it.

.. note::

   This node runs once and ends: it logs, then ``main`` returns. The nodes of the next sections stay alive with ``rclcpp::spin``. The file is not in the repository: the class of the next part replaces it.

Build System, Build and Run
"""""""""""""""""""""""""""

**Edit** ``CMakeLists.txt``: these lines go after the ``find_package`` lines and before ``ament_package()``.

.. code-block:: cmake

   add_executable(hello_function src/hello_function.cpp)
   ament_target_dependencies(hello_function rclcpp)

   install(TARGETS hello_function
     DESTINATION lib/${PROJECT_NAME})

**Build and run**, from ``~/ros2_ws``:

.. code-block:: bash

   colcon build --packages-select robotaxi_demo
   source install/setup.bash
   ros2 run robotaxi_demo hello_function

.. code-block:: text

   [INFO] [1793999175.323300565] [hello]: Hello from hello

The line gives the level, the time in seconds since January 1, 1970, the node's name, and the text. Then the program ends: the shell's ``time`` measured 0.3 s from start to end.

Object-Oriented Node Design
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Node as a Class: Derive from rclcpp::Node
"""""""""""""""""""""""""""""""""""""""""""

A node with publishers, timers and data needs a place to keep them. A class gives it data members, so this course writes every node as a class.

- Derive from ``rclcpp::Node``: the class inherits everything a node can do.
- The constructor passes the node's name to the base class constructor.
- The inherited methods, such as ``get_logger()`` and ``get_name()``, are called like your own; ``this->`` is optional.
- The node's logic goes in its methods, and its state in its data members.

.. note::

   Real ROS 2 applications almost always write nodes this way. Learn the pattern now: it is the one the rest of the course uses.

Write the Same Node as a Class
""""""""""""""""""""""""""""""

Write the hello node as a class, ``HelloNode``, in a header and a main file.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - Package
     - ``robotaxi_demo``
   * - Files
     - ``include/robotaxi_demo/hello_node.hpp``, ``src/hello_main.cpp``
   * - Node
     - ``hello``
   * - Executable
     - ``hello``

**Resource:** `ROS 2 Jazzy: Writing a simple publisher and subscriber (C++) <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>`_.

Both files are in the repository, in ``robotaxi_demo``. The next four parts are the four steps: the header, ``main``, ``CMakeLists.txt``, and the build.

Step 1: the Header, hello_node.hpp
""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 6, 8, 9

   #pragma once
   #include <rclcpp/rclcpp.hpp>

   namespace robotaxi_demo {

   class HelloNode : public rclcpp::Node {
    public:
     HelloNode() : rclcpp::Node{"hello"} {
       RCLCPP_INFO_STREAM(get_logger(), "Hello from " << get_name());
     }
   };

   }  // namespace robotaxi_demo

- Line 6: a ``HelloNode`` is an ``rclcpp::Node`` (public inheritance).
- Line 8: the base class constructor gets the node's name, ``hello``.
- Line 9: ``get_logger()`` and ``get_name()`` are public methods inherited from ``rclcpp::Node``. The constructor is short, so it stays in the header.

Step 2: main, in hello_main.cpp
"""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 8, 9, 10

   #include <memory>

   #include <rclcpp/rclcpp.hpp>

   #include "robotaxi_demo/hello_node.hpp"

   int main(int argc, char** argv) {
     rclcpp::init(argc, argv);
     auto node{std::make_shared<
       robotaxi_demo::HelloNode>()};
     rclcpp::spin(node);
     rclcpp::shutdown();
   }

- Line 8: starts ROS 2, as before.
- Lines 9 and 10: make a ``HelloNode`` instead of a plain ``rclcpp::Node``. Its constructor logs the line.
- Line 11: ``rclcpp::spin`` keeps the node running until :kbd:`Ctrl+C`. The next section explains it. Without this line, the program ends right after the log line.
- Line 12: stops ROS 2.

Steps 3 and 4: CMakeLists.txt, then Build and Test
""""""""""""""""""""""""""""""""""""""""""""""""""

**Edit** ``CMakeLists.txt``: the lines of the repository's file for this node.

.. code-block:: cmake
   :linenos:
   :emphasize-lines: 1, 2, 4

   include_directories(include)
   add_executable(hello src/hello_main.cpp)
   ament_target_dependencies(hello rclcpp)
   install(TARGETS hello robotaxi dispatcher
     DESTINATION lib/${PROJECT_NAME})

- Line 1: lets ``#include "robotaxi_demo/hello_node.hpp"`` find the header.
- Line 4: the ``install`` line of the repository names all three executables of the package.

**Build and run**, from ``~/ros2_ws``: ``colcon build --packages-select robotaxi_demo``, then ``source install/setup.bash``, then ``ros2 run robotaxi_demo hello``.

.. code-block:: text

   [INFO] [1793942813.858003271] [hello]: Hello from hello

The node prints its line and keeps running. In another terminal, ``ros2 node list`` shows ``/hello``.

Node Lifecycle and Best Practices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Life of a Node, and How to Log
""""""""""""""""""""""""""""""""""

1. **Initialization:** ``rclcpp::init()`` sets up ROS 2.
2. **Creation:** the constructor runs and makes the publishers, subscriptions and timers.
3. **Execution:** ``rclcpp::spin()`` keeps the node alive (the next section).
4. **Shutdown:** ``rclcpp::shutdown()`` frees everything.

.. list-table::
   :header-rows: 1
   :widths: 32 68
   :class: compact-table

   * - Macro
     - Use it for
   * - ``RCLCPP_DEBUG_STREAM``
     - Details for finding a bug. Not printed by default.
   * - ``RCLCPP_INFO_STREAM``
     - Normal progress.
   * - ``RCLCPP_WARN_STREAM``
     - Something odd that the node can handle.
   * - ``RCLCPP_ERROR_STREAM``
     - Something failed.
   * - ``RCLCPP_FATAL_STREAM``
     - The node cannot go on.

Say what happened and where: ``Camera initialized with resolution 640x480``. The ``_STREAM`` macros take ``<<``, as ``std::cout`` does; ``RCLCPP_INFO`` takes a ``printf`` format instead.

Common Mistakes, and What You See
"""""""""""""""""""""""""""""""""

Each row was run on purpose, to record the symptom.

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - Mistake
     - What you see
   * - The terminal did not source ``install/setup.bash`` after the build
     - ``Package 'robotaxi_demo' not found``
   * - No ``add_executable`` or ``install`` line for the node
     - ``No executable found``
   * - No ``rclcpp::spin`` in ``main``
     - The node logs its first line, and the program ends after 0.3 s
   * - Two nodes with the same name
     - ``ros2 node list`` prints ``WARNING: Be aware that there are nodes in the graph that share an exact name``
   * - A node made before ``rclcpp::init``
     - The program aborts: ``rclcpp::exceptions::RCLInvalidArgument``, the context is null

Two nodes with one name both run. The warning goes on: this "can have unintended side effects". Give each node its own name.

Node Spinning
-------------

**Spinning** keeps a node alive. The node waits for events, a message that arrives, a timer that is due, a service request, and runs the callback of each one.

The hello node of the last section logged one line and ended. From here on, every node stays alive with ``rclcpp::spin``.

Why Spin, and How
^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l10/spin.png
   :alt: From the left, a wavy line labeled main thread leads to an arrow labeled rclcpp::spin(node) that enters a circle. The circle holds the word callbacks and an arrow that goes around it. From the right of the circle, an arrow labeled with the keys Ctrl and C leaves to a second wavy line labeled main thread.
   :align: center
   :width: 90%

   ``rclcpp::spin`` takes the main thread into a loop of callbacks until :kbd:`Ctrl+C`.

**Why spin?**

- To receive messages, and run their callbacks.
- To run timer callbacks.
- To answer service requests and actions.
- To keep the node alive.

**Ways to spin**

- ``rclcpp::spin(node)``: runs until :kbd:`Ctrl+C`.
- ``rclcpp::spin_some(node)``: runs the callbacks that are ready, then returns.
- ``spin_until_future_complete``: spins until one result arrives.
- An executor object: the same loop, with more control (later).

.. warning::

   Without spinning, the node ends right after its constructor, and no callback ever runs.

The Basic Spinning Pattern
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 5

   int main(int argc, char** argv) {
     rclcpp::init(argc, argv);
     auto node{std::make_shared<
       robotaxi_demo::HelloNode>()};
     rclcpp::spin(node);
     rclcpp::shutdown();
   }

This is the ``main`` of every node in the repository, with the class name changed.

**What happens during spin**

1. **Event loop:** it waits for a message, a timer or a request.
2. **Callback execution:** it runs the callback of the event that happened, then waits again.
3. **One at a time:** the default executor runs one callback at a time, on the main thread. A slow callback delays the others.
4. **Signal handling:** :kbd:`Ctrl+C` ends the loop. ``spin`` returns, and ``main`` goes on to ``shutdown``.

The ROS 2 documentation: ``rclcpp::spin(node)`` "expands to an instantiation and invocation of the Single-Threaded Executor" (`Executors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`_).

Spinning Alternatives
^^^^^^^^^^^^^^^^^^^^^

**Spin some:** run the callbacks that are ready, then do other work.

.. code-block:: cpp

   int laps{0};
   while (rclcpp::ok() && laps < 5) {
     rclcpp::spin_some(node);
     RCLCPP_INFO_STREAM(node->get_logger(),
       "other work, lap " << laps);
     std::this_thread::sleep_for(
       std::chrono::milliseconds{100});
     ++laps;
   }

.. code-block:: text

   [...956.587] [loop]: other work, lap 0
   [...956.688] [loop]: other work, lap 1
   [...956.788] [loop]: other work, lap 2

The laps are 100 ms apart: the sleep. ``rclcpp::ok()`` turns false after :kbd:`Ctrl+C`.

**An executor:** the loop as an object, for several nodes or several threads.

.. code-block:: cpp

   rclcpp::executors::SingleThreadedExecutor executor;
   executor.add_node(node);
   executor.spin();

.. note::

   Use ``rclcpp::spin`` for a simple node. Use an executor when you spin several nodes or need threads. Executors come in a later lecture.

Messages
--------

**Messages** are the data structures that nodes send each other. A message type is written in a ``.msg`` file, and every message on a topic has the topic's type.

.. admonition:: What a message type gives you
   :class: key-box

   - **Typed:** each field has a name and a type.
   - **Any language:** the same type works in C++ and in Python.
   - **Serialized:** ROS 2 turns a message into bytes to send it, and back.
   - **Versioned:** a change to the fields is a new type.
   - **Efficient:** made for real-time communication.

`ROS 2 Jazzy: Interfaces <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html>`_, and the `common_interfaces <https://github.com/ros2/common_interfaces>`_ repository.

Message Categories
^^^^^^^^^^^^^^^^^^

- **Standard messages** (``std_msgs``): one basic value, such as ``String``, ``Int32``, ``Bool``.
- **Common messages** (``geometry_msgs``, ``sensor_msgs``): robotics data, such as ``Point``, ``Pose``, ``Twist``, ``Image``, ``LaserScan``.
- **Package-specific messages:** types a package defines for its own needs. Types of your own come in a later lecture.

.. note::

   A message type is a contract between nodes: the publisher and the subscriber must agree on the fields (rule 2).

This lecture's nodes use one common message, ``geometry_msgs/msg/Point``, for the robotaxi's position.

Standard Messages
^^^^^^^^^^^^^^^^^

The std_msgs Package
""""""""""""""""""""

``std_msgs`` holds 30 message types for common data: ``ros2 interface package std_msgs`` lists them.

.. list-table::
   :header-rows: 1
   :widths: 18 46 36
   :class: compact-table

   * - Group
     - Types
     - What they hold
   * - Primitive
     - ``Bool``, ``Byte``, ``Char``, ``String``, ``Empty``
     - One value; ``Empty`` has no data, for an event
   * - Numeric
     - ``Int8``, ``Int16``, ``Int32``, ``Int64``, ``UInt8`` to ``UInt64``, ``Float32``, ``Float64``
     - One integer or one floating-point number
   * - Array
     - ``Int32MultiArray``, ``Float32MultiArray``, ``ByteMultiArray``, and others
     - A multi-dimensional array of one type
   * - Special
     - ``Header``, ``ColorRGBA``
     - A time stamp with a frame name; a color with alpha

``ros2 interface show std_msgs/msg/String`` prints one field, ``string data``, and a comment: the type "is deprecated as of Foxy", and you should "create your own semantically meaningful message". The talker still uses it.

Message Introspection
^^^^^^^^^^^^^^^^^^^^^

Read a Message Type before You Use It
"""""""""""""""""""""""""""""""""""""

``ros2 interface show geometry_msgs/msg/Point``

.. code-block:: text

   # This contains the position of a point in free space
   float64 x
   float64 y
   float64 z

A type's full name is ``package/msg/Type``. A ``float64`` field is a ``double`` in C++.

``ros2 interface show std_msgs/msg/Header``

.. code-block:: text

   builtin_interfaces/Time stamp
   	int32 sec
   	uint32 nanosec
   string frame_id

A field can itself be a message: ``stamp`` is a ``builtin_interfaces/Time``, with two integer fields.

**List the types installed**

- ``ros2 interface list``: every interface. On the course laptop, 752: messages, services and actions.
- ``ros2 interface list -m``: only the messages, 491 of them.
- ``ros2 interface package std_msgs``: the 30 types of one package.

Find a Type, and Get a Template for It
""""""""""""""""""""""""""""""""""""""

**Find types by name.** The list is long, so filter it: ``ros2 interface list | grep String``

.. code-block:: text

   example_interfaces/msg/String
   example_interfaces/msg/WString
   ros_gz_interfaces/msg/StringVec
   std_msgs/msg/String

The first part of each name is the package that provides the type.

**Get a template.** ``ros2 interface proto std_msgs/msg/String`` prints the fields with empty values, ready to fill in for ``ros2 topic pub``:

.. code-block:: text

   "data: ''
   "

.. note::

   Before you use a type in code, run ``ros2 interface show`` on it. The field names and types in your code must match it.

Using Messages
^^^^^^^^^^^^^^

Including Messages in C++
"""""""""""""""""""""""""

Each message type has a C++ header, ``<package>/msg/<message_name>.hpp``:

.. code-block:: cpp

   #include <geometry_msgs/msg/point.hpp>
   #include <std_msgs/msg/string.hpp>
   #include <std_msgs/msg/int32.hpp>
   #include <std_msgs/msg/header.hpp>

.. list-table::
   :header-rows: 1
   :widths: 16 46 38
   :class: compact-table

   * -
     - A position
     - A string
   * - Message type
     - ``geometry_msgs/msg/Point``
     - ``std_msgs/msg/String``
   * - Header
     - ``<geometry_msgs/msg/point.hpp>``
     - ``<std_msgs/msg/string.hpp>``
   * - C++ class
     - ``geometry_msgs::msg::Point``
     - ``std_msgs::msg::String``

- The header's name is the type's name in snake_case: ``Point`` gives ``point.hpp``, ``LaserScan`` gives ``laser_scan.hpp``.
- The C++ class name replaces each ``/`` with ``::``. Each class also defines ``SharedPtr`` and ``ConstSharedPtr``, shared pointers to a message, used by some callbacks.

Creating and Filling Messages
"""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 2, 3

   // The robotaxi's position (robotaxi_node.cpp)
   geometry_msgs::msg::Point msg{};  // x, y and z start at 0.0
   msg.x = x_;

   // A string
   std_msgs::msg::String string_msg{};
   string_msg.data = "Hello ROS 2";

   // A header, with the time: this->now() is the node's clock
   std_msgs::msg::Header header_msg{};
   header_msg.stamp = this->now();
   header_msg.frame_id = "base_link";

- ROS 2 generates the class from the ``.msg`` file. Its fields are public data members, so ``msg.x`` reads and writes ``x``: a message is a struct.
- Lines 2 and 3 are the ones the robotaxi node runs; the other two are shown for the types.

Message Dependencies
^^^^^^^^^^^^^^^^^^^^

Declare the Message Package in Both Build Files
"""""""""""""""""""""""""""""""""""""""""""""""

To use a message package, name it in ``package.xml`` and in ``CMakeLists.txt``. For ``geometry_msgs``, the repository has:

**In** ``package.xml``

.. code-block:: xml

   <depend>rclcpp</depend>
   <depend>geometry_msgs</depend>

**In** ``CMakeLists.txt``

.. code-block:: cmake
   :linenos:
   :emphasize-lines: 3, 6

   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   find_package(geometry_msgs REQUIRED)

   add_executable(robotaxi src/robotaxi_main.cpp src/robotaxi_node.cpp)
   ament_target_dependencies(robotaxi rclcpp geometry_msgs)

- Line 3 finds the package; line 6 links the executable to it. Both are needed, for each message package.
- ``ros2 pkg create --dependencies rclcpp geometry_msgs`` wrote the ``<depend>`` and ``find_package`` lines.

Publishing Test Messages
^^^^^^^^^^^^^^^^^^^^^^^^

Send a Message from the Terminal: ros2 topic pub
""""""""""""""""""""""""""""""""""""""""""""""""

``ros2 topic pub`` publishes a message that you write in the terminal. It tests a subscriber before its publisher exists (rule 4).

.. code-block:: bash

   ros2 topic pub --once /robotaxi/position \
     geometry_msgs/msg/Point "{x: 7.0, y: 4.0}"

.. code-block:: text

   publisher: beginning loop
   publishing #1: geometry_msgs.msg.Point(x=7.0, y=4.0, z=0.0)

- The fields are written as ``{name: value}``. A field you leave out keeps 0.0, here ``z``. A string: ``"data: 'Hello World'"``; an integer: ``"data: 42"``; a boolean: ``"data: true"``.
- ``--once`` (or ``-1``) sends one message and stops. Without it, the command sends one message per second until :kbd:`Ctrl+C`.
- ``--rate 10`` sends 10 per second. ``--times 5`` sends 5 and stops.

Publishers
----------

A **publisher** is the object a node uses to send messages on one topic. One publisher, many subscribers.

**The publisher's steps**

1. **Create the publisher:** message type, topic name, queue size.
2. **Create a message** and fill its fields.
3. **Publish:** send it to every subscriber.
4. **Repeat**, often from a timer.

**Common uses**

- Sensor data (cameras, lidar, IMU).
- The robot's state (position, speed, battery).
- Commands (speed, joint positions).
- Status updates and heartbeats.

`ROS 2 Jazzy: Writing a simple publisher and subscriber (C++) <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>`_, `ROS 2 Jazzy: Topics <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Topics.html>`_.

Creating a Publisher
^^^^^^^^^^^^^^^^^^^^

Write a Node That Publishes Its Position
""""""""""""""""""""""""""""""""""""""""

Write a robotaxi node that publishes its position, a ``Point``, on the topic ``robotaxi/position`` every 0.5 s.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - Package
     - ``robotaxi_demo``
   * - Files
     - ``include/robotaxi_demo/robotaxi_node.hpp``, ``src/robotaxi_node.cpp``, ``src/robotaxi_main.cpp``
   * - Node
     - ``robotaxi``
   * - Executable
     - ``robotaxi``

.. warning::

   The package already depends on ``geometry_msgs``. For a new package, add the dependency to ``package.xml`` and ``CMakeLists.txt`` first.

The robotaxi drives along a street, the x axis, 1 m every 0.5 s. ``robotaxi_main.cpp`` is ``hello_main.cpp`` with ``RoboTaxiNode`` in place of ``HelloNode``.

The Header: a Publisher and a Timer
"""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 5, 6, 7, 8, 11, 12

   class RoboTaxiNode : public rclcpp::Node {
    public:
     RoboTaxiNode()
         : rclcpp::Node{"robotaxi"},
           publisher_{create_publisher<geometry_msgs::msg::Point>(
               "robotaxi/position", 10)},
           timer_{create_wall_timer(std::chrono::milliseconds{500},
                                    [this]() { publish_position(); })} {}
    private:
     void publish_position();
     rclcpp::Publisher<geometry_msgs::msg::Point>::SharedPtr publisher_;
     rclcpp::TimerBase::SharedPtr timer_;
     double x_{0.0};  // position along the street, in m
   };

The constructor makes a publisher (lines 5 and 6) and a timer (lines 7 and 8). The class keeps both in data members (lines 11 and 12). Above the class, the file includes ``<chrono>``, ``<geometry_msgs/msg/point.hpp>`` and ``<rclcpp/rclcpp.hpp>``, inside ``namespace robotaxi_demo``.

Initialize the Publisher
^^^^^^^^^^^^^^^^^^^^^^^^

What the Constructor Makes
""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   publisher_{create_publisher<geometry_msgs::msg::Point>(
       "robotaxi/position", 10)},
   timer_{create_wall_timer(std::chrono::milliseconds{500},
                            [this]() { publish_position(); })} {}

- Lines 1 and 2: a publisher of ``Point`` on the topic ``robotaxi/position``. The 10 is the queue size: up to 10 messages wait for a subscriber that falls behind.
- Lines 3 and 4: every 500 ms, the timer calls the lambda, and the lambda calls ``publish_position``. ``[this]`` lets the lambda call a method of this object. 500 ms is 2 Hz.
- ``create_publisher`` and ``create_wall_timer`` are methods inherited from ``rclcpp::Node``. Each returns a ``std::shared_ptr``.

.. warning::

   **Store the timer.** A timer that is not kept in a data member is destroyed at the end of the constructor, and its callback never runs. A test node with such a timer printed nothing in 1.5 s.

Understanding QoS (Quality of Service)
""""""""""""""""""""""""""""""""""""""

The 10 in ``create_publisher`` is the queue size, with the default settings for everything else. The same settings, written out as a ``rclcpp::QoS`` object (`Quality of Service settings <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html>`_):

.. code-block:: cpp

   rclcpp::QoS qos{10};  // queue size 10
   qos.reliable().durability_volatile().keep_last(10);
   publisher_ = create_publisher<geometry_msgs::msg::Point>(
       "robotaxi/position", qos);

The second line sets the three settings that ``rclcpp::QoS{10}`` already has; a program compared the two objects with ``==``: equal.

.. list-table::
   :header-rows: 1
   :widths: 36 64
   :class: compact-table

   * - Scenario
     - Queue behavior
   * - The subscriber keeps up
     - Each message is delivered at once; the queue stays empty
   * - A slow or disconnected subscriber
     - Messages wait in the queue, up to its size
   * - The queue is full
     - The oldest message is dropped (keep last)

Publish Messages
^^^^^^^^^^^^^^^^

The Timer Callback, in robotaxi_node.cpp: Fill, Publish, Move
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   void RoboTaxiNode::publish_position() {
     geometry_msgs::msg::Point msg{};  // x, y and z start at 0.0
     msg.x = x_;
     publisher_->publish(msg);
     RCLCPP_INFO_STREAM(get_logger(), "Published x = " << msg.x);
     x_ += 1.0;  // 1 m every 0.5 s: 2 m/s
   }

- Line 4: ``publish`` sends a copy of ``msg`` to every subscriber of the topic.
- Line 6: the timer calls this method every 0.5 s, so the robotaxi moves 1 m per 0.5 s. That is 1 / 0.5 = 2 m/s.

**Main function**, ``src/robotaxi_main.cpp``: the spinning pattern, with ``RoboTaxiNode``.

.. code-block:: cpp

   int main(int argc, char** argv) {
     rclcpp::init(argc, argv);
     auto node{std::make_shared<robotaxi_demo::RoboTaxiNode>()};
     rclcpp::spin(node);
     rclcpp::shutdown();
   }

Build and Test the Publisher
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build, Run the Publisher, Check the Topic
"""""""""""""""""""""""""""""""""""""""""

In ``CMakeLists.txt``, the executable lists two source files: ``add_executable(robotaxi src/robotaxi_main.cpp src/robotaxi_node.cpp)``. Then ``colcon build --packages-select robotaxi_demo`` and ``source install/setup.bash``.

**Terminal 1:** ``ros2 run robotaxi_demo robotaxi``

.. code-block:: text

   [INFO] [1793942784.416393304] [robotaxi]: Published x = 0
   [INFO] [1793942784.916529421] [robotaxi]: Published x = 1

**Terminal 2:** ``ros2 topic hz /robotaxi/position``

.. code-block:: text

   average rate: 2.000
     min: 0.500s max: 0.500s std dev: 0.00012s window: 9

**Terminal 2:** ``ros2 topic echo /robotaxi/position --once``

.. code-block:: text

   x: 13.0
   y: 0.0
   z: 0.0

.. admonition:: Conclusion
   :class: tip

   The topic carries 2.000 messages per second, 0.500 s apart: the 500 ms that ``create_wall_timer`` asked for. The log times agree: 784.416, then 784.917.

Subscribers
-----------

A **subscriber** is the object a node uses to receive the messages of one topic. It runs a callback for each message, so the node reacts to data that other nodes publish.

**The subscriber's steps**

1. **Create the subscription:** message type, topic name, queue size, callback.
2. **Define the callback:** the function that handles one message.
3. **Spin:** keep the node alive to receive.
4. **Process:** the callback runs for each message as it arrives.

**Common uses**

- Sensor data, for navigation.
- Commands, to act on them.
- The state of the system, to watch it.
- Logging and visualization.
- An event that triggers an action.

Creating a Subscriber
^^^^^^^^^^^^^^^^^^^^^

Write a Node That Receives the Position
"""""""""""""""""""""""""""""""""""""""

Write a dispatcher node that subscribes to ``robotaxi/position`` and logs, for each position, how far the robotaxi is from a pickup point.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - Package
     - ``robotaxi_demo``
   * - Files
     - ``include/robotaxi_demo/dispatcher_node.hpp``, ``src/dispatcher_node.cpp``, ``src/dispatcher_main.cpp``
   * - Node
     - ``dispatcher``
   * - Executable
     - ``dispatcher``

The pickup point, at x = 10 m and y = 0 m, is chosen for this example. ``dispatcher_main.cpp`` is the spinning pattern with ``DispatcherNode``, and ``CMakeLists.txt`` gets the same two lines as the publisher, with ``dispatcher`` in place of ``robotaxi``.

The Header: a Subscription and a Callback
"""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 5, 6, 7, 8, 9, 12

   class DispatcherNode : public rclcpp::Node {
    public:
     DispatcherNode()
         : rclcpp::Node{"dispatcher"},
           subscription_{create_subscription<geometry_msgs::msg::Point>(
               "robotaxi/position", 10,
               [this](const geometry_msgs::msg::Point& msg) {
                 on_position(msg);
               })} {}
    private:
     void on_position(const geometry_msgs::msg::Point& msg);
     rclcpp::Subscription<geometry_msgs::msg::Point>::SharedPtr subscription_;
     double pickup_x_{10.0};  // pickup point, in m
     double pickup_y_{0.0};   // pickup point, in m
   };

The constructor makes a subscription (lines 5 to 9), kept in a data member (line 12). The file includes ``<geometry_msgs/msg/point.hpp>`` and ``<rclcpp/rclcpp.hpp>``, inside ``namespace robotaxi_demo``.

Initialize the Subscriber
^^^^^^^^^^^^^^^^^^^^^^^^^

What the Subscription Constructor Makes
"""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   subscription_{create_subscription<geometry_msgs::msg::Point>(
       "robotaxi/position", 10,
       [this](const geometry_msgs::msg::Point& msg) {
         on_position(msg);
       })} {}

- Lines 1 and 2: the same message type and the same topic name as the publisher (rules 1 and 2). The 10 is the queue size: up to 10 messages wait while the callback is busy.
- Lines 3 to 5: the callback. ``rclcpp::spin`` calls it once for each message, with the message as its argument. The lambda passes it on to ``on_position``. The parameter's type must be the topic's type; a reference avoids a copy.
- Start the dispatcher before the robotaxi or after it: rule 4 says it waits for a publisher.

Hand Over a Method without a Lambda: std::bind
""""""""""""""""""""""""""""""""""""""""""""""

Many ROS 2 examples write the callback with ``std::bind``, from ``<functional>``. This dispatcher builds and prints the same lines as the lambda version (Jazzy).

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 3, 4

   subscription_{create_subscription<geometry_msgs::msg::Point>(
       "robotaxi/position", 10,
       std::bind(&DispatcherNode::on_position, this,
                 std::placeholders::_1))} {}

- ``&DispatcherNode::on_position``: which method to call.
- ``this``: which object to call it on, this dispatcher.
- ``std::placeholders::_1``: a slot for the first argument. ``spin`` fills it with the message.
- ``std::bind`` returns a callable that does what the lambda does: ``this->on_position(msg)``. The timer takes ``std::bind(&RoboTaxiNode::publish_position, this)``, with no slot.

The course code uses the lambda: you see every argument, and there is no slot to count.

Process Messages
^^^^^^^^^^^^^^^^

The Callback: the Distance to the Pickup Point
""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // src/dispatcher_node.cpp
   void DispatcherNode::on_position(const geometry_msgs::msg::Point& msg) {
     const double distance{
         std::hypot(pickup_x_ - msg.x, pickup_y_ - msg.y)};
     RCLCPP_INFO_STREAM(get_logger(), "RoboTaxi at x = " << msg.x << ", "
                                      << distance << " m from the pickup");
   }

``std::hypot(a, b)``, from ``<cmath>``, is the square root of a\ :sup:`2` + b\ :sup:`2`. For the message ``{x: 7.0, y: 4.0}`` of ``ros2 topic pub``:

1. The robotaxi is 10 − 7 = 3 m short of the pickup point in x, and 4 m away from it in y.
2. 3\ :sup:`2` + 4\ :sup:`2` = 9 + 16 = 25.
3. The square root of 25 is 5, so the dispatcher prints ``RoboTaxi at x = 7, 5 m from the pickup``.

.. warning::

   The callback runs whenever a message arrives, one at a time. Keep it faster than the time between messages, here 0.5 s, or the queue fills and messages are dropped (scenario 3).

Build and Test the Subscriber
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the Complete System
"""""""""""""""""""""""

**Terminal 1:** ``ros2 run robotaxi_demo dispatcher``. **Terminal 2:** ``ros2 run robotaxi_demo robotaxi``.

.. code-block:: text

   [INFO] [...784.416688] [dispatcher]: RoboTaxi at x = 0, 10 m from the pickup
   [INFO] [...784.916901] [dispatcher]: RoboTaxi at x = 1, 9 m from the pickup
   [INFO] [...785.416755] [dispatcher]: RoboTaxi at x = 2, 8 m from the pickup

**Terminal 3:** ``ros2 topic info /robotaxi/position``

.. code-block:: text

   Type: geometry_msgs/msg/Point
   Publisher count: 1
   Subscription count: 1

- Also in terminal 3: ``ros2 topic list`` shows the topic, ``ros2 topic echo /robotaxi/position`` prints each position, and ``ros2 topic hz /robotaxi/position`` gives 2.000 per second.
- The robotaxi logged ``Published x = 0`` at ...784.416393 s. The dispatcher logged x = 0 at ...784.416688 s: 784.416688 − 784.416393 = 0.000295 s. The message took about 0.3 ms, on one computer.

When nothing arrives, check the topic names first: ``ros2 topic list`` shows what each side uses (rule 1).

Publisher-Subscriber Communication
----------------------------------

In DDS, the middleware under ROS 2, two objects carry a topic:

- A **DataWriter**: made by a ROS 2 publisher. It writes the messages to the network.
- A **DataReader**: made by a ROS 2 subscriber. It reads the messages from the network.

A DataWriter and a DataReader connect only when they match: the same topic name, the same type, and compatible QoS settings (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_). The three scenarios that follow show what happens to the messages once they match, or when nobody reads.

Scenario Analysis
^^^^^^^^^^^^^^^^^

Scenario 1: One Publisher, No Subscriber
""""""""""""""""""""""""""""""""""""""""

The robotaxi publishes at 2 Hz, every 0.5 s, with a queue of 10 (the code's values). No subscriber is running.

.. list-table::
   :header-rows: 1
   :widths: 14 22 32 32
   :class: compact-table

   * - Time
     - Publisher
     - Matching DataReaders
     - What happens to the message
   * - 0.0 s
     - Publishes x = 0
     - None
     - Not delivered to anyone
   * - 0.5 s
     - Publishes x = 1
     - None
     - Not delivered to anyone
   * - 1.0 s
     - Publishes x = 2
     - None
     - Not delivered to anyone

.. admonition:: What scenario 1 shows
   :class: key-box

   - **No blocking:** the publisher goes on at 2 Hz (rule 3). The talker alone logged message 1.
   - **Data loss:** a subscriber that starts at 1.5 s gets x = 3 first; x = 0 to 2 are gone.
   - **The exception:** with the durability setting *transient local*, the publisher keeps its samples for a subscriber that joins late (`Quality of Service settings <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html>`_). The default, *volatile*, keeps nothing.

Scenario 2: a Fast Subscriber
"""""""""""""""""""""""""""""

The robotaxi publishes at 2 Hz, every 0.5 s, queues of 10 (the code's values). The callback takes 100 ms, chosen for this example.

.. list-table::
   :header-rows: 1
   :widths: 12 22 30 36
   :class: compact-table

   * - Time
     - Publisher
     - Subscriber's queue
     - Subscriber's callback
   * - 0.0 s
     - Publishes x = 0
     - [ ] then [0] then [ ]
     - Starts on x = 0 at once
   * - 0.1 s
     -
     - [ ]
     - Finishes x = 0; waits
   * - 0.5 s
     - Publishes x = 1
     - [ ] then [1] then [ ]
     - Starts on x = 1 at once
   * - 0.6 s
     -
     - [ ]
     - Finishes x = 1; waits

.. admonition:: What scenario 2 shows
   :class: key-box

   - **The ideal case:** the callback, 100 ms, is much shorter than the period, 500 ms.
   - **Each message is handled at once**, and the queue never holds more than one: 400 ms of idle time before the next.
   - **Load:** busy 100 ms of every 500 ms, that is 100 / 500 = 20% of the time.

Scenario 3: a Slow Subscriber Loses Messages
""""""""""""""""""""""""""""""""""""""""""""

A test version of the dispatcher keeps a queue of 3 and spends 1.7 s in each callback (both chosen for this example). The robotaxi publishes every 0.5 s. Measured:

.. list-table::
   :header-rows: 1
   :widths: 24 28 26 22
   :class: compact-table

   * - A callback ends at
     - Published while it ran
     - Queue: the last 3
     - Next one taken
   * - 1.71 s
     - x = 1, 2, 3
     - 1, 2, 3
     - x = 1
   * - 3.41 s
     - x = 4, 5, 6
     - 4, 5, 6
     - x = 4
   * - 5.11 s
     - x = 7, 8, 9, 10
     - 8, 9, 10
     - x = 8
   * - 6.81 s
     - x = 11, 12, 13
     - 11, 12, 13
     - x = 11

.. admonition:: Conclusion
   :class: tip

   In 11 s the robotaxi published 23 positions, x = 0 to 22. The dispatcher handled 7: x = 0, 1, 4, 8, 11, 15 and 18. At 10.21 s it started on x = 18, published at 9.00 s: 1.2 s old.

- **Data loss:** x = 7 was pushed out by x = 10 before the callback could take it. Each 1.7 s callback sees 3 or 4 new messages, and keeps 3.
- **Stale data:** the dispatcher works on a position that is 1.2 s old.
- **Fixes:** a shorter callback, a lower publish rate, or a larger queue. The larger queue only delays the loss: each message still takes 1.7 s.
