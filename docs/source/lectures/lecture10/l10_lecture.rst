====================================================
Lecture
====================================================

Before Class
------------

1. A new GitHub repository holds the ROS packages of this course: `rubixcubic/enpm702-fall-2026-ros <https://github.com/rubixcubic/enpm702-fall-2026-ros>`_. Its ``L10`` folder holds this lecture's package, ``robotaxi_demo``. Clone it into the ``src`` folder of your workspace and push it to your own private GitHub repository, as `ROS 2 Workspace <../../setup/ros_setup.html#ros-2-workspace>`_ in :doc:`/setup/ros_setup` shows (`Create a Workspace`_ explains what a workspace is).
2. Install ROS 2 Jazzy, as in :doc:`/setup/ros_setup`.

Code for This Lecture
---------------------

We have provided this lecture's package, ``robotaxi_demo``, in the ``L10`` folder of the course repository. `Create a Package: ros2 pkg create`_ shows the command we used to create it. Its git history has one commit per step of this lecture, from that command to the subscriber. It holds:

.. code-block:: text

   enpm702-fall-2026-ros/L10/robotaxi_demo/
   ├── CMakeLists.txt
   ├── package.xml
   ├── include/robotaxi_demo/
   │   ├── robotaxi_node.hpp
   │   └── dispatcher_node.hpp
   └── src/
       ├── robotaxi_main.cpp
       ├── robotaxi_node.cpp
       ├── dispatcher_main.cpp
       └── dispatcher_node.cpp

Build it from the workspace's top folder, then run one of its two executables (``robotaxi_exe``, ``dispatcher_exe``):

.. code-block:: bash

   colcon build --packages-select robotaxi_demo
   source install/setup.bash
   ros2 run robotaxi_demo robotaxi_exe

.. dropdown:: More detail: ``colcon build`` and ``ros2 run``
   :class-container: more-detail
   :icon: info

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Meaning (from ``--help``)
      * - ``--packages-select robotaxi_demo``
        - "Only process a subset of packages": ``colcon`` builds ``robotaxi_demo`` and no other package of ``src``.
      * - ``robotaxi_demo`` (``ros2 run``)
        - "Name of the ROS package".
      * - ``robotaxi_exe`` (``ros2 run``)
        - "Name of the executable": one of the package's two, ``robotaxi_exe`` or ``dispatcher_exe``.

.. _l10-pre-reading:

Pre-Reading
-----------

Read this part before class: the lecture opens with six slides on it (what ROS is, monolithic and distributed programs, the ROS 2 layers, DDS and ``rclcpp``) and builds on all of it. The workspace, ``colcon`` and ``ros2 pkg create`` are in `Workspace and Development Environment`_.

What ROS Is: Plumbing, Tools, Capabilities, Community
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**ROS 2** (Robot Operating System 2) is a set of libraries and tools for robot software. It is not an operating system: it runs on one, here Ubuntu 24.04.

.. note::

   ROS 2 breaks a large application into smaller programs. It moves the data between them, on one computer or across several, so you write the behavior of the robot and not the networking.

.. figure:: /_static/images/l10/ros_equation.png
   :alt: The equation ROS equals plumbing plus tools plus capabilities plus community. On the left, a three by three grid of dots and the word ROS, then an equals sign. Then four navy icons joined by plus signs, each with its word below: a faucet, plumbing; a wrench and screwdriver, tools; a person with a check mark, capabilities; a puzzle piece, community.
   :align: center
   :width: 90%

   What ROS is made of, in four parts.

- **Plumbing**: the framework that carries data between parts of a robot, with messaging, standard interfaces and several languages.
- **Tools**: help you build, test and monitor a robot. They add no robot behavior.
- **Capabilities**: ready-to-use packages, such as manipulation, motion planning and perception.
- **Community**: the developers, researchers and companies who share code and ideas (`About ROS <https://docs.ros.org/en/jazzy/About-ROS.html>`_).

Where to find ROS 2 online:

- `ros.org <https://www.ros.org/>`_: the project's home page.
- `ROS 2 Jazzy documentation <https://docs.ros.org/en/jazzy/>`_: the reference for this course.
- `ROS Index <https://index.ros.org/>`_: every released ROS package.
- `github.com/ros2 <https://github.com/ros2>`_: the source code.

**Who maintains ROS:** `Open Robotics <https://www.openrobotics.org/>`_, with the community. It is the Open Source Robotics Foundation (OSRF), a US nonprofit founded in 2012, which also makes the Gazebo simulator.

Designed for Robots That Leave the Lab
""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/what_is_ros_for.jpeg
   :alt: A hand-drawn poster titled ROS 2: designed for robots that leave the lab, built for real-world, commercial and complex environments. Top right, a smiling robot with I love the outside world on its chest walks out of a building marked LAB. Three panels below. Products: a delivery robot hands a box to a man on a city street while a woman pushes a shopping cart; caption: robots that people buy and use, not only research prototypes. Several robots on one network: a drone, two robot arms and a small wheeled robot, labeled nodes and bots, joined by dotted lines to a Wi-Fi router labeled hub; caption: each with many nodes, communicating in complex team environments. Real-time control: smiling packages labeled fast data packets fly along an arrow to a stopwatch marked tick-tock, past a robot arm marked on time; caption: commands that must arrive on time, ensuring safety, accuracy and predictability. Bottom line: ROS 2, empowering the next generation of autonomous systems. Bottom right: based on Macenski et al., 2022.
   :align: center
   :width: 100%

   What ROS 2 was designed for: products, several robots on one network, and commands that must arrive on time (based on Macenski et al., 2022).

The Node: the Unit of Computation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Node
   :class: tip

   A **node** is a program, or a part of one, that does one job and exchanges data with other nodes.

- A full robot runs many nodes: one senses, one filters, one controls, one drives the motors, one logs.
- Each node is written, tested and started on its own. Different people write them, and each runs at its own rate.
- Nodes talk only through defined interfaces: topics, services and actions, explained below. The same camera driver runs, unchanged, on another robot with that camera.

The ROS 2 documentation: "each node should do one logical thing" (`Nodes <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html>`_). The next parts show why a robot's software is split into nodes, with a robotaxi as the example.

From a File on Disk to a Running Program: the Process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Process
   :class: tip

   A program that is running. The operating system gives each process its own memory and a number, its **process ID** (pid).

.. figure:: /_static/images/l10/process.png
   :alt: A box at the top reads ride_service, the executable: a file on disk. Two arrows go down from it, labeled run in terminal 1 and run in terminal 2, to two dashed rounded boxes side by side, labeled process 1 and process 2, each with its own pid. Each dashed box holds two boxes, stack and heap. A red dashed line between the two dashed boxes is labeled no shared memory.
   :align: center
   :width: 60%

   One executable, run in two terminals, makes two processes.

- The executable that CMake builds is a file. Run it, and the operating system starts a process.
- Run it in two terminals: two processes from one file, each with its own stack and heap.
- A variable or a pointer of one process means nothing to the other.
- :kbd:`Ctrl+C` in a terminal stops the process running there.

Monolithic: One Program Does Every Job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Monolithic Architecture
   :class: tip

   One program, run as one process. Its functions and classes call each other.

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 4, 5

   int main() {
     double x{0.0};
     for (int step{0}; step < 3; ++step) {
       x = move_robotaxi(x);
       double d{distance_to_pickup(x)};
       std::cout << "x = " << x << ", "
                 << d << " m to go\n";
     }
   }

``move_robotaxi`` adds 1 m. ``distance_to_pickup`` returns the distance to the pickup at 10 m.

.. figure:: /_static/images/l10/monolithic.png
   :alt: Inside one dashed rounded box, main() on the left. move_robotaxi() sits above it and distance_to_pickup() below it, both shifted to the right. A short straight solid arrow labeled 1: call goes up to move_robotaxi(), and one labeled 2: call goes down to distance_to_pickup(). From the left end of each function, a dashed arrow labeled return bends around the left side back to main().
   :align: center
   :width: 45%

   One process (the dashed box). ``main`` calls each function (lines 4 and 5) and waits for it to return.

The program prints:

.. code-block:: text

   x = 1, 9 m to go
   x = 2, 8 m to go
   x = 3, 7 m to go

Monolithic: Advantages and Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The robotaxi program above, all in one process.

**Advantages**

- One program to build and run: one executable.
- A call passes data directly: ``move_robotaxi(x)`` gets ``x`` with no message to copy and send.
- One debugger session steps through ``main`` and both functions.

**Issues**

- One crash stops every function: a bad pointer in ``distance_to_pickup`` also stops the robotaxi.
- A change to one function means rebuilding and restarting the whole program.
- ``main`` waits for each call: if ``distance_to_pickup`` took 2 s, the robotaxi would not move for those 2 s.
- Both jobs run on one computer: the dispatch office cannot run its part on its own computer.

Distributed: Separate Programs Exchange Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Distributed Architecture
   :class: tip

   Several programs, each run as its own process, on one computer or several. They do not call each other's functions: they send each other messages. ROS 2 works this way: each program is a **node**, and nodes talk within one process, between processes on one computer, or between computers (`Nodes <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html>`_).

.. figure:: /_static/images/l10/distributed.png
   :alt: Two dashed rounded boxes, one around a node named robotaxi_node and one around a node named dispatcher_node. An arrow goes from robotaxi_node to dispatcher_node, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 72%

   The robotaxi and the dispatcher as two programs, each in its own process (a dashed box).

Above the arrow, a **topic**: a name that nodes use to exchange one type of message. Below it, the topic's message type.

**Advantages**

- A crash stops only that program.
- A change rebuilds and restarts one program.
- Each program runs at its own rate.
- Programs can run on several computers.

**Issues**

- Each message is copied: about 0.2 ms per message, measured with the robotaxi and the dispatcher.
- A slow receiver misses messages (shown in class with a slow subscriber).
- More programs to start and watch.
- Both sides must use the same type.

ROS 2 Is Distributed: Nodes on Two Computers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l10/distributed_ros.png
   :alt: Two solid gray rounded boxes, one above the other. The top one is labeled Computer 1: in the robotaxi, and holds a dashed box with a node named robotaxi_node. An arrow labeled publish goes down from robotaxi_node to a navy box that reads /robotaxi/position, and geometry_msgs/msg/Point. An arrow labeled subscribe goes down from the navy box into the bottom gray box, labeled Computer 2: at the dispatch office, to a node named dispatcher_node in a dashed box.
   :align: center
   :width: 45%

   A gray box is a computer, a dashed box a process.

ROS 2 is distributed: a node "can communicate with other nodes within the same process, in a different process, or on a different machine" (`Nodes <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html>`_).

- ``robotaxi_node`` and ``dispatcher_node`` run on two computers with no change to their code. The computers share a network and a domain ID (`Discovery in Practice: Domain IDs and Your Network`_).
- Nodes can also share one process: less overhead, but one crash stops them all (`Composition <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Composition.html>`_).
- Inside a node, the code is the C++ of the first half of the course: classes, function calls and smart pointers.

What Runs under Your Node: the ROS 2 Layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l10/ros2_layers_tags.png
   :alt: Six boxes stacked top to bottom, with a dashed arrow from each box down to the next and a numbered tag to the left of each. Tag 1, Application: RoboTaxiNode, DispatcherNode. Tag 2, Client libraries: rclcpp for C++, rclpy for Python. Tag 3, rcl: one C library. Tag 4, rmw: the middleware interface. Tag 5, DDS: Fast DDS, Cyclone DDS, Connext, GurumDDS. Tag 6, a gray box, Operating system and network: Ubuntu 24.04, Ethernet, Wi-Fi.
   :align: center
   :width: 45%

   The layers under a ROS 2 node, numbered 1 to 6 as in the list below.

Each layer uses the one below it (the dashed arrows). The ROS 2 documentation says the APIs "are stacked such that the typical ROS user will use the client library API, e.g. rclcpp"; the client libraries "use the rcl interface", and "the rcl implementation in turn uses the rmw API" (`Internal ROS 2 interfaces <https://docs.ros.org/en/jazzy/Concepts/Advanced/About-Internal-Interfaces.html>`_).

1. **Application**: your nodes, the topics, services and actions between them, and the node tools (parameters, ``ros2``, ``rqt``). You write only the nodes.
2. **Client library**: your node calls ``rclcpp`` (C++) or ``rclpy`` (Python). The client library also spins: it runs your callbacks. The ROS 2 documentation says ``rcl`` "does not address" the execution model "at all"; each client library provides it.
3. **rcl**: both client libraries call ``rcl``, one C library they share, so client libraries "can be smaller and more consistent with each other".
4. **rmw**: ``rcl`` calls ``rmw``, which only declares functions: "the minimal set of primitive middleware capabilities needed to build ROS on top". The ``rmw`` package itself "contains the C headers which define the interface". Each DDS has its own ``rmw`` package that implements those functions, for example ``rmw_fastrtps_cpp`` for Fast DDS. So a node runs on any DDS without a code change.
5. **DDS**, the **middleware**, does the work: it finds other programs and moves data between them (next section).
6. **Operating system and network**: Ubuntu runs each node. Ethernet or Wi-Fi joins the computers.

Follow One Message down the Layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The robotaxi publishes one message to the dispatcher. The table follows it down the layers, one row per layer.

.. list-table::
   :header-rows: 1
   :widths: 25 75
   :class: compact-table

   * - Layer
     - What happens to the message
   * - Application
     - ``RoboTaxiNode`` calls ``publisher_->publish(msg)``.
   * - Client library
     - ``rclcpp`` passes the message to ``rcl``.
   * - ``rcl``
     - ``rcl`` passes it to ``rmw``. ``rcl`` never talks to DDS directly.
   * - ``rmw``
     - ``rmw_fastrtps_cpp``, the ``rmw`` package for Fast DDS, turns it into Fast DDS calls.
   * - DDS
     - Fast DDS sends it to the dispatcher (next section).
   * - OS and network
     - On two computers, it crosses the network.

Source: `ROS 2 Jazzy: Internal ROS 2 interfaces <https://docs.ros.org/en/jazzy/Concepts/Advanced/About-Internal-Interfaces.html>`_.

What DDS Does: Find the Nodes, Move the Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: DDS
   :class: tip

   **DDS** (Data Distribution Service): the industry-standard middleware that moves ROS 2 messages. Jazzy uses eProsima's Fast DDS by default.

.. figure:: /_static/images/l10/dds_roles.png
   :alt: Two node boxes, robotaxi_node on the left and dispatcher_node on the right, both standing on a wide navy band labeled DDS. Above the nodes, a dashed two-headed arrow between them carries tag 1. Inside the band, a solid arrow runs from under robotaxi_node to under dispatcher_node, with tag 2 and a small box reading position. Below the band, under the dispatcher_node and joined to the band by a line, a small box with tag 3 reads reliable, keep last 10.
   :align: center
   :width: 60%

   The three jobs of DDS, numbered 1 to 3 as in the list below.

1. **Discovery**: each program announces what it sends and what it wants. Programs that match find each other. ROS 1 needed a central program for this, the ROS master; DDS removed it (`ROS on DDS <https://design.ros2.org/articles/ros_on_dds.html>`_).
2. **Transport**: DDS carries each message, here the robotaxi's position, to the dispatcher, on one computer or across a network.
3. **Quality of Service**: delivery settings. The default resends a lost message (reliable) and keeps the last 10 (`Quality of Service settings <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html>`_).

Discovery in Practice: Domain IDs and Your Network
""""""""""""""""""""""""""""""""""""""""""""""""""

- By default, a node finds every node it can reach by **multicast** (one message that every computer on the network can receive) and that has the same **domain ID** (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_). The default domain ID is 0.
- Different domain IDs never see each other: a talker in domain 82 and a listener in 83, and the listener printed nothing in 4 s.

.. note::

   A network that does not pass multicast stops discovery between computers. On eduroam, students' nodes have never appeared on the instructor's laptop, from 2017 to today. Where multicast passes, as on a home router, set your own domain ID, 0 to 101, in ``~/.bashrc``: ``export ROS_DOMAIN_ID=``\ *number*.

Where DDS Comes From: an OMG Standard, Not Only for Robots
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ROS 2 did not invent DDS: it is an industry standard.

- **A standard.** The Object Management Group (OMG) publishes DDS as a protocol and API (`OMG press release, 2024 <https://www.omg.org/news/releases/pr2024/07-09-24.htm>`_). DDS sends data to every program that asked for it (`DDS 1.4 specification <https://www.omg.org/spec/DDS/>`_).
- **Vendors for ROS 2.** ROS 2 supports eProsima Fast DDS (the default), Eclipse Cyclone DDS, RTI Connext DDS and GurumNetworks GurumDDS (`Different ROS 2 middleware vendors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Different-Middleware-Vendors.html>`_). GurumDDS has community support only.
- **Used beyond robots.** 24 industry standards use DDS, such as AUTOSAR (cars), EUROCAE (civil aviation), OpenICE (medical devices) and ROS 2 (`OMG press release, 2024 <https://www.omg.org/news/releases/pr2024/07-09-24.htm>`_).
- **Why industry uses it.** OMG names three reasons: low latency (little delay), high reliability and scalability (`OMG press release, 2020 <https://www.omg.org/news/releases/pr2020/01-29-20.htm>`_).
- **Languages.** DDS has standard APIs for C++, Java and other languages (`OMG press release, 2020 <https://www.omg.org/news/releases/pr2020/01-29-20.htm>`_).
- **Low latency is not real time.** Real time also needs a real-time operating system, and code that is guaranteed to finish each task in time (`Introduction to Real-time Systems <https://design.ros2.org/articles/realtime_background.html>`_).
- **Ubuntu 24.04 is not real time.** Real time needs Ubuntu's real-time kernel, which makes the scheduler priority-based (`Real-time Ubuntu documentation <https://ubuntu.com/real-time/docs/>`_). On 24.04, you get that kernel through Ubuntu Pro (`Enable Real-time Ubuntu <https://canonical-real-time-ubuntu-documentation.readthedocs-hosted.com/how-to/enable-real-time-ubuntu/>`_), free for personal use on up to 5 machines (`Ubuntu Pro <https://ubuntu.com/pro>`_).
- **Security.** DDS-Security can secure ROS 2 (`ROS 2 DDS-Security Integration <https://design.ros2.org/articles/ros2_dds_security.html>`_), but security is off by default (`About Security <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Security.html>`_).

.. dropdown:: More detail: turning on ROS 2 security
   :class-container: more-detail
   :icon: info

   With security on, DDS encrypts the messages, checks who sent each one, checks that no one changed it on the way, and controls which node may use which topic. Each node needs an **enclave**: a folder of six files with its certificates, its private key and its permissions (`About Security <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Security.html>`_).

   The steps from the ROS 2 tutorial (`Setting up security <https://docs.ros.org/en/jazzy/Tutorials/Advanced/Security/Introducing-ros2-security.html>`_):

   .. code-block:: bash

      # 1. Create a keystore (the certificate authorities)
      ros2 security create_keystore demo_keystore
      # 2. Create an enclave for each node
      ros2 security create_enclave demo_keystore /talker_listener/talker
      ros2 security create_enclave demo_keystore /talker_listener/listener
      # 3. Turn security on, in every terminal that runs a node
      export ROS_SECURITY_KEYSTORE=~/sros2_demo/demo_keystore
      export ROS_SECURITY_ENABLE=true
      export ROS_SECURITY_STRATEGY=Enforce
      # 4. Start each node with its enclave
      ros2 run demo_nodes_cpp talker --ros-args --enclave /talker_listener/talker

   - ``ROS_SECURITY_ENABLE=true`` is the master switch. The value is case sensitive.
   - Without ``ROS_SECURITY_STRATEGY=Enforce``, a node whose security files are missing still starts, with no security.
   - Nodes with security on do not talk to nodes with security off.

Write ROS 2 Code in C++: rclcpp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: rclcpp
   :class: tip

   The ROS Client Library for C++: the C++ interface that "provides all of the ROS client functionality like creating nodes, publishers, and subscriptions" (`Client libraries <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Client-Libraries.html>`_). See `rclcpp API (Jazzy) <https://docs.ros.org/en/jazzy/p/rclcpp/>`_.

- One header, ``#include <rclcpp/rclcpp.hpp>``, and one namespace, ``rclcpp::``.
- In this lecture you use ``rclcpp::init``, ``rclcpp::Node``, ``create_publisher``, ``create_subscription``, ``create_wall_timer``, ``rclcpp::spin`` and ``rclcpp::shutdown``.
- ``rclcpp`` builds on ``rcl``, the C library that ``rclpy`` (Python) uses too, so a C++ node and a Python node behave the same and exchange the same messages.
- ``roscpp`` is the C++ library of ROS 1. ROS 2 code uses ``rclcpp``.

Where ROS 2 Is Used
^^^^^^^^^^^^^^^^^^^

Transportation
""""""""""""""

.. figure:: /_static/images/l10/autonomous_machines.jpeg
   :alt: A hand-drawn illustration on cream paper titled Autonomous Transport, subtitled everyday integration and service in our world. Four panels: passenger train, a short train on a railway; autonomous vehicle, a small car with a roof sensor on a road; surroundings vessel, a small boat on the water; drone delivery, a drone carrying a box in flight. Footer: pioneering new ways to serve, assist, and explore.
   :align: center
   :width: 80%

- Self-driving cars: Autoware runs on ROS 2 Jazzy (`Autoware installation <https://docs.autoware.org/main/installation/>`_), Apex.AI's Apex.OS is based on ROS 2 (`The Robot Report <https://www.therobotreport.com/apex-os-1-0-available-brings-ros-2-development-self-driving-cars/>`__), and the CARLA simulator has ROS 2 built in (`CARLA 0.10.0 <https://carla.org/2024/12/19/release-0.10.0/>`_).
- Boats: VRX, the simulator of the RobotX boat competition, runs on ROS 2 (`VRX 2.0 <https://discourse.openrobotics.org/t/announcing-release-2-0-of-the-vrx-simulation-environment/29079>`_).
- Drones: the PX4 autopilot works with ROS 2 (`PX4 Guide <https://docs.px4.io/main/en/ros2/>`_).
- No public source shows a driverless train running ROS 2.

Manufacturing
"""""""""""""

.. figure:: /_static/images/l10/robots_in_manufacturing.jpeg
   :alt: A hand-drawn illustration on cream paper titled Robots in Manufacturing, subtitled increasing safety and efficiency, side by side with humans. Four panels: industrial robot arms, two yellow arms placing parts on a conveyor belt; inspection camera, a camera on a stand checking a part on the belt next to a pass and OK checklist; collaborative robot, a small arm at a bench next to a person in safety glasses who says thanks; warehouse robot, a low mobile robot carrying a shelf of boxes. Footer: designed for collaborative and busy environments.
   :align: center
   :width: 80%

- Robot arms: KUKA and FANUC publish official ROS 2 drivers (`KUKA <https://github.com/kuka-ros>`_, `FANUC <https://www.fanucamerica.com/solutions/ros-2>`_), and Universal Robots maintains its own (`Universal Robots driver <https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver>`_). ABB arms use a driver by PickNik Robotics (`The Robot Report <https://www.therobotreport.com/ros-2-driver-now-available-for-abbs-robot-arms/>`__).
- Inspection cameras: Basler's official driver runs on ROS 2 Jazzy (`pylon-ros-camera <https://github.com/basler/pylon-ros-camera>`_).
- Warehouse robots: Robotnik's RB-THERON has a ROS 2-based architecture (`RB-THERON <https://robotnik.eu/products/mobile-robots/rb-theron/>`_).

Specialized Domains
"""""""""""""""""""

.. figure:: /_static/images/l10/robots_in_specialized_areas.jpeg
   :alt: A hand-drawn illustration on cream paper titled Robots in Specialized Domains, subtitled expanding capabilities across incredible environments. Five panels: a surgical robot with several thin arms over a patient on an operating table; a planetary rover on rocky ground saying bleep bloop; an autonomous tractor in a crop field; a four-legged inspection robot with a camera scanning rubble next to warning signs; a research robot, a small wheeled robot on a table next to a laptop. Footer: solving unique challenges in everyday and extraordinary worlds.
   :align: center
   :width: 80%

- Surgery research: the da Vinci Research Kit (Johns Hopkins) supports ROS 2 (`dVRK wiki <https://github.com/jhu-dvrk/sawIntuitiveResearchKit/wiki/PythonOverROS>`_).
- Space: NASA JPL's Open Source Rover runs ROS 2 (`osr-rover-code <https://github.com/nasa-jpl/osr-rover-code>`_), and NASA's Astrobee has a ROS 2 branch (`astrobee ros2 <https://github.com/nasa/astrobee/tree/ros2>`_).
- Legged robots: ANYbotics is moving ANYmal to ROS 2 (`ANYbotics <https://www.anybotics.com/news/anybotics-anymal-first-research-meet-up-japan/>`_), and Spot has a ROS 2 driver by the RAI Institute (`spot_ros2 <https://github.com/bdaiinstitute/spot_ros2>`_).
- Research: TurtleBot 4, Husarion and Clearpath Husky run ROS 2 (`TurtleBot 4 <https://openrobotics.org/blog/2022/5/3/introducing-the-turtlebot-4>`_, `Husarion <https://husarion.com/blog/panther-ros2-driver/>`_, `Husky <https://clearpathrobotics.com/blog/2022/03/ros-2-now-available-on-husky-ugv/>`_).
- No checked source shows a tractor running ROS 2.

Emerging Areas
""""""""""""""

.. figure:: /_static/images/l10/robots_in_emerging_areas.jpeg
   :alt: A hand-drawn illustration on cream paper titled Robots in Emerging Areas, subtitled everyday integration and service in our world. Four panels: a round robot vacuum circling a living-room floor near a sofa and a plant; a humanoid service robot with a screen on its chest waving to a person at a lobby desk; a security patrol robot shaped like a rounded column, scanning a parking lot at night under a street lamp; an autonomous survey boat with antennas near a rocky coastline, with sonar waves under it. Footer: pioneering new ways to serve, assist, and explore.
   :align: center
   :width: 80%

- Home robots: iRobot's Create 3 educational robot is "entirely based on ROS 2" (`Create 3 Docs <https://iroboteducation.github.io/create3_docs/>`_).
- Service robots: PAL Robotics' humanoid ARI is based on ROS 2 (`ARI <https://docs.pal-robotics.com/edge/ari>`_).
- Security: Robotnik's RB-WATCHER patrol robot is compatible with ROS 2 (`RB-WATCHER <https://robotnik.eu/products/mobile-robots/rb-watcher/>`_).
- Survey boats: UNH's Project 11 ocean-mapping software runs on ROS 2 Jazzy (`unh_marine_autonomy <https://github.com/CCOMJHC/unh_marine_autonomy>`_).

Terms This Lecture Uses
-----------------------

Each term is defined in `Pre-Reading`_ or in `Workspace and Development Environment`_.

.. list-table::
   :header-rows: 1
   :widths: 28 72
   :class: compact-table

   * - Term
     - Meaning
   * - Node
     - A program, or a part of one, that does one job and exchanges data with other nodes, such as ``robotaxi_node``.
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
   :alt: Three node boxes: camera at the top, planner at the left and arm_controller at the right. A navy arrow labeled pose goes from camera down to planner, with tag 1 beside it. From planner to arm_controller, two parallel arrows: the upper one green, labeled close gripper, with tag 3 above it; the lower one purple, labeled go to pose, with tag 2 below it.
   :align: center
   :width: 60%

   A topic, an action and a service on one robot, tagged 1 to 3 as in the list below.

1. **Topic** ``pose``: ``camera`` publishes an object's pose many times a second. ``planner`` subscribes.
2. **Action** ``go to pose``: ``planner`` sends a goal. ``arm_controller`` reports progress until the arm gets there.
3. **Service** ``close gripper``: ``planner`` sends one request. ``arm_controller`` closes the gripper and responds once.

Each box is a node, and each arrow carries the name of a topic, a service or an action. ``planner`` runs on a laptop.

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

   - **Loose coupling:** a node knows the topic's name, not the other nodes.
   - **Scalability:** a new publisher or subscriber uses the same topic; nothing else changes.
   - **Fault tolerance:** a node can stop; the others keep using the topic.
   - **Flexible patterns:** a topic can have one or many publishers, and one or many subscribers.
   - **Quality of Service:** each publisher and subscriber of a topic sets its own delivery.

The Running Example: a Fleet of Robotaxis
"""""""""""""""""""""""""""""""""""""""""

From here on, the lecture uses one example: a fleet of robotaxis and the office that dispatches them.

.. figure:: /_static/images/l10/robotaxi_graph.png
   :alt: Two white boxes, robotaxi_node on the left and dispatcher_node on the right. An arrow goes from robotaxi_node to dispatcher_node, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 80%

   The robotaxi publishes its position; the dispatcher subscribes to it.

- **Nodes:** each robotaxi is a node, and the dispatcher is a node.
- **Topics:** names such as ``/robotaxi/position``. A robotaxi publishes on it; the dispatcher subscribes to it.
- **Messages:** the data, one piece at a time. Here a position of type ``geometry_msgs/msg/Point``: three numbers, ``x``, ``y`` and ``z``.

A Topic Works Like a Bus
""""""""""""""""""""""""

A topic "somewhat resembles a device bus": shared wires that many devices connect to (`Topics <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Topics.html>`_).

- **Alike:** any publisher can send on a topic, and "all subscribers in the system will receive the data", as every device sees a bus's wires.
- **Alike:** nodes "can come and go as needed", as a device joins a bus without rewiring the others.
- **Different:** a topic has no wire. DDS sends each subscriber its own copy (second figure).

.. figure:: /_static/images/l10/computer_buses.png
   :alt: A computer bus diagram. A tall box labeled CPU on the left. Three wide buses run to the right: a yellow address bus with one arrowhead, pointing away from the CPU, then a light blue data bus and a pink control bus with arrowheads at both ends. Each bus branches down into four boxes labeled RAM, ROM, I/O and Other, so all four connect to the same three buses.
   :align: center
   :width: 70%

   A device bus: every device connects to the same wires. Redrawn from `Computer buses <https://commons.wikimedia.org/wiki/File:Computer_buses.svg>`_, by German, Wikimedia Commons, public domain.

.. figure:: /_static/images/l10/topic_copies.png
   :alt: The node robotaxi_node on the left. To its right, an empty dashed band with tag 1 and the topic name /robotaxi/position above it. Three separate arrows leave robotaxi_node, run through the band and turn down, each to its own node below: dispatcher_node, logger_node and map_view_node. Each arrow carries its own small box reading Point, each marked with tag 2.
   :align: center
   :width: 70%

   A topic has no wire. (1) The topic: a name, not a wire. (2) One copy of the ``Point`` per subscriber. ``logger_node`` and ``map_view_node`` are added for this example.

Deliver One Message: Four Steps
"""""""""""""""""""""""""""""""

One position, from the robotaxi to the dispatcher:

1. **Find.** The two nodes find each other, because they use the same domain ID (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_).
2. **Match.** DDS links the publisher to each subscriber with the same topic name and message type (`Who Connects the Nodes: DDS, Not Your Code`_).
3. **Send.** DDS turns the ``Point`` into bytes (**serialization**) and sends them with RTPS, the protocol of DDS: over UDP to another computer, or through shared memory on the same computer.
4. **Receive.** DDS turns the bytes back into a ``Point`` (**deserialization**) and hands it to the dispatcher.

Steps 1 and 2 happen when the nodes start. Steps 3 and 4 happen for every message, every 0.5 s.

Four Rules of a Topic
^^^^^^^^^^^^^^^^^^^^^

A publisher and a subscriber never call each other. They only share a topic, so four rules decide whether a message arrives.

Rule 1: Publisher and Subscriber Use the Same Topic Name
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/rule_name.png
   :alt: The node robotaxi_node on the left, a red dashed box in the middle that reads different names: nothing arrives, and the node dispatcher_node on the right. An arrow from robotaxi_node to the box has the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. A red dashed arrow from the box to dispatcher_node has the topic name /robotaxi/pose above it and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 60%

The dispatcher subscribes to ``/robotaxi/pose`` by mistake. The robotaxi publishes on ``/robotaxi/position``. The dispatcher receives nothing, and no error is printed.

Rule 2: Publisher and Subscriber Use the Same Message Type
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/rule_type.png
   :alt: The node robotaxi_node on the left, a red dashed box in the middle that reads different types: nothing arrives, and the node dispatcher_node on the right. An arrow from robotaxi_node to the box has the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. A red dashed arrow from the box to dispatcher_node has the topic name /robotaxi/position above it and the message type std_msgs/msg/String below it.
   :align: center
   :width: 60%

Same name, different types: the two do not connect. A subscriber of ``String`` receives nothing from a publisher of ``Point``.

Rule 3: A Publisher Does Not Wait for Subscribers
"""""""""""""""""""""""""""""""""""""""""""""""""

The robotaxi publishes every 0.5 s, whether or not a node listens. A dispatcher that starts late gets only the messages sent after it starts.

.. figure:: /_static/images/l10/rule_no_wait_1.png
   :alt: The node robotaxi_node on the left. A red dashed arrow goes right to a red dashed box that reads: no subscriber yet, messages are lost. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 1: before the dispatcher starts.

.. figure:: /_static/images/l10/rule_no_wait_2.png
   :alt: The node robotaxi_node on the left, an arrow to the node dispatcher_node on the right, marked started later. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 2: after the dispatcher starts.

Rule 4: A Subscriber Does Not Need a Publisher
""""""""""""""""""""""""""""""""""""""""""""""

The dispatcher can start first. It waits, with no error, and its callback runs once a robotaxi starts publishing. So the order in which you start the two nodes does not matter.

.. figure:: /_static/images/l10/rule_no_publisher_1.png
   :alt: A red dashed box on the left reads: no publisher yet. A red dashed arrow goes right to the node dispatcher_node, marked waits. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 1: before the robotaxi starts.

.. figure:: /_static/images/l10/rule_no_publisher_2.png
   :alt: The node robotaxi_node on the left, marked started later, an arrow to the node dispatcher_node on the right. The topic name /robotaxi/position is above the arrow and the message type geometry_msgs/msg/Point below it.
   :align: center
   :width: 70%

   Step 2: after the robotaxi starts.

Four Patterns
^^^^^^^^^^^^^

Pattern 1: One Publisher, Many Subscribers
""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_one_to_many.png
   :alt: The node robotaxi_node on the left. One line goes right from it, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. At a dot the line splits into two arrows: one up to the node dispatcher_node and one down to the node _ros2cli_84035, marked ros2 topic echo.
   :align: center
   :width: 70%

Every subscriber gets its own copy of each message. ``ros2 topic echo`` runs as a node, ``_ros2cli_84035`` in this run (the number is its process id). Adding it changes nothing for the robotaxi or the dispatcher.

Pattern 2: Many Publishers, One Topic
"""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_many_to_one.png
   :alt: Three nodes on the left, robotaxi_1_node, robotaxi_2_node and robotaxi_3_node, each with an arrow to the node dispatcher_node on the right. Along each arrow, the topic name /fleet/position is on one side and the message type geometry_msgs/msg/Point on the other.
   :align: center
   :width: 70%

A fleet of three robotaxis publishes on one topic. The dispatcher gets every position, from all three, in the order they arrive.

Pattern 3: One Node, Several Topics
"""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_two_topics.png
   :alt: The node robotaxi_node at the top, with two straight arrows down at the same angle: one to the node dispatcher_node, with the topic name /robotaxi/position on one side and the message type geometry_msgs/msg/Point on the other, and one to the node battery_monitor_node, with the topic name /robotaxi/battery on one side and the message type std_msgs/msg/Float64 on the other.
   :align: center
   :width: 70%

One topic per kind of data. Each node subscribes only to what it uses: the dispatcher never receives battery messages.

Pattern 4: One Node Publishes and Subscribes
""""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l10/pattern_both_ways.png
   :alt: The nodes robotaxi_node and dispatcher_node side by side. An arrow goes from robotaxi_node to dispatcher_node, with the topic name /robotaxi/position above it and the message type geometry_msgs/msg/Point below it. A second arrow, below the first, goes from dispatcher_node back to robotaxi_node, with the message type geometry_msgs/msg/Point above it and the topic name /robotaxi/pickup below it.
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

.. dropdown:: More detail: ``ros2 topic list -t``
   :class-container: more-detail
   :icon: info

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Meaning (from ``ros2 topic list --help``)
      * - ``-t``, ``--show-types``
        - "Additionally show the topic type": each topic is followed by its message type, in brackets.

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

   A source package with the same name as an installed one takes its place when you source your workspace (the overlay, `Underlay and Overlay`_).

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

A **workspace** is a folder that keeps your source code, the build files and the installed packages in one place. One workspace per project, or per ROS version, keeps them apart.

Packages that come with ROS 2 are installed already. Nodes of your own are built in a workspace, then run with the same ``ros2`` tools.

.. code-block:: text

   workspaces/
   ├── ros2_iron_ws/
   │   ├── src/
   │   │   ├── my_robot_bringup/
   │   │   └── my_robot_description/
   │   └── build/  install/  log/
   └── ros2_jazzy_ws/
       ├── src/
       │   ├── nav2_experiments/
       │   └── perception_demos/
       └── build/  install/  log/

**colcon** is the tool that builds the packages of a workspace. What it does, how to check it and its
build commands are in `The colcon Build Tool <../../setup/ros_setup.html#the-colcon-build-tool>`_ on
:doc:`/setup/ros_setup`.

Create a Workspace
^^^^^^^^^^^^^^^^^^

.. code-block:: bash
   :linenos:

   # Create the workspace folders
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws

   # Build, with src still empty
   colcon build

   # Source the workspace
   source install/setup.bash

- Line 2: the workspace's name and place are up to you. ROS 2 does not require a path.
- Line 6: builds every package in ``src``, and makes ``build``, ``install`` and ``log``.
- Line 9: without this line, ``ros2 run`` does not find the packages you built. Forgetting it is the most common mistake with ROS 2.

.. note::

   The first build of an empty workspace is not wasted: it makes the folders and the setup files, and it checks that your build tools work.

The Workspace Folders
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   ros2_ws/
   ├── src/
   ├── build/
   ├── log/
   └── install/
       ├── setup.bash
       ├── setup.zsh
       └── ...

- ``src``: the source code of your packages, and of the packages you cloned. The only folder you write in.
- ``build``: the compiler's intermediate files (object files, CMake's cache).
- ``log``: the log of each build, for when a build fails.
- ``install``: the finished products: executables, libraries, headers.

  - Holds ``setup.bash`` and ``setup.zsh``, the files that set up a terminal.
  - This is what you "source" to use your workspace.

.. note::

   **The build flow:** source code in ``src``, compiled in ``build``, installed in ``install``. The logs go to ``log``. ``colcon`` makes the last three; you can delete them and build again.

Underlay and Overlay
^^^^^^^^^^^^^^^^^^^^

Several workspaces can stack: each one you source adds a layer on top of the ones before it (`Creating a workspace <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html>`_).

- The ROS 2 installation, ``/opt/ros/jazzy``, is the **underlay**. It gives the terminal ``ros2`` and the installed packages.
- Your workspace, sourced after it, is the **overlay**: its packages sit on top of the underlay, they do not replace it.
- When a package is in both layers, the overlay wins. So you can change one package without touching the rest of the installation.

.. code-block:: bash

   source /opt/ros/jazzy/setup.bash      # underlay: ROS 2 itself
   source ~/ros2_ws/install/setup.bash   # overlay: your packages
   source ~/dev_ws/install/setup.bash    # a second overlay

.. warning::

   **A terminal that did not source the overlay** finds only the underlay. ``ros2 run robotaxi_demo robotaxi_exe`` prints ``Package 'robotaxi_demo' not found``, even after a build that worked. Source the overlay again after each build that adds a package or an executable. In zsh, source ``setup.zsh``.

Create a Package: ros2 pkg create
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Package
   :class: tip

   A **package** is one folder of nodes, libraries, settings and launch files that does one thing, such as ``demo_nodes_cpp``. Every package has the same layout, so it is easy to build, share and reuse.

We have provided this lecture's package, ``robotaxi_demo``. Here is the command we used to create it:

.. code-block:: bash
   :linenos:

   cd ~/ros2_ws/src/enpm702-fall-2026-ros/L10
   ros2 pkg create robotaxi_demo --build-type ament_cmake \
     --dependencies rclcpp geometry_msgs
   cd ~/ros2_ws
   colcon build --packages-select robotaxi_demo

.. dropdown:: More detail: ``ros2 pkg create``
   :class-container: more-detail
   :icon: info

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Meaning (from ``ros2 pkg create --help``)
      * - ``robotaxi_demo``
        - "The package name". The command makes a folder of that name in the current folder, here ``L10``. ``colcon build`` finds it there, because it searches every folder under ``src``.
      * - ``--build-type ament_cmake``
        - "The build type to process the package with". The choices are ``cmake``, ``ament_cmake``, ``ament_cargo`` and ``ament_python``; ``ament_cmake`` is the one for C++.
      * - ``--dependencies rclcpp geometry_msgs``
        - "list of dependencies": the packages ours uses, written into ``package.xml`` and ``CMakeLists.txt``.

.. code-block:: text

   robotaxi_demo/
   ├── CMakeLists.txt
   ├── package.xml
   ├── include/robotaxi_demo/
   └── src/

- ``ament_cmake``: the build type for C++. It is the default, so the command without ``--build-type`` creates the same package. **ament** is the set of CMake macros ROS 2 adds, such as ``ament_package()``.
- ``--dependencies``: the packages ours uses. The command writes them into both files.
- Headers go in ``include/robotaxi_demo``, sources in ``src``.

.. warning::

   A package is always created in the ``src`` folder of the workspace (line 1).

With the workspace built and ``robotaxi_demo`` created, the parts below read the two files that describe it, ``package.xml`` and ``CMakeLists.txt``, and the commands that use them.

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
     - ``robotaxi_demo dispatcher_exe``, ``robotaxi_demo robotaxi_exe``
   * - ``ros2 pkg prefix robotaxi_demo``
     - ``<workspace>/install/robotaxi_demo``: the overlay
   * - ``ros2 pkg prefix rclcpp``
     - ``/opt/ros/jazzy``: the underlay
   * - ``ros2 pkg xml robotaxi_demo``
     - The package's ``package.xml``

``ros2 pkg prefix`` tells you which layer a package comes from. To change an installed package, copy its source into ``src`` and build it there: the overlay wins.

Package Manifest: package.xml
"""""""""""""""""""""""""""""

The first lines of your ``package.xml``, once you replace its two ``TODO`` lines:

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

   .. dropdown:: More detail: ``rosdep install --from-paths src --ignore-src -y``
      :class-container: more-detail
      :icon: info

      .. list-table::
         :header-rows: 1
         :widths: 32 68

         * - Argument
           - Meaning (from ``rosdep --help``)
         * - ``install``
           - "download and install the dependencies of a given package or packages".
         * - ``--from-paths src``
           - The arguments are "paths to be searched": rosdep acts on every package it finds in ``src``, so you do not name each one.
         * - ``--ignore-src``
           - ``-i``, ``--ignore-packages-from-source``: "ignore keys that are found to be catkin or ament packages" in the sourced workspaces or in the ``--from-paths`` folders, so rosdep does not try to install your own packages with ``apt``.
         * - ``-y``
           - ``--default-yes``: "Tell the package manager to default to y", so ``apt`` does not stop to ask before each install.
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
     - Builds the executable ``robotaxi_exe`` from ``src/robotaxi_main.cpp``.
   * - ``ament_target_dependencies``
     - Gives ``robotaxi_exe`` the ROS packages it uses: ``rclcpp``.
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

The first command that asks about running nodes, such as ``ros2 node list``, starts the **daemon**: a background program that keeps a list of the running nodes, topics, services and actions. The next commands ask it, so they answer at once instead of waiting for discovery. Commands that only read installed files, such as ``ros2 pkg list``, ``ros2 interface show`` or ``ros2 run``, do not start it (checked on Jazzy with ``ros2 daemon status``).

- ``ros2 daemon status`` says whether it runs, for example ``The daemon is not running``.
- ``ros2 daemon stop`` stops it. The next such command starts a fresh one.
- ``ros2 daemon start`` starts it by hand; this is rarely needed.

.. note::

   **When to restart it:** ``ros2 node list`` or ``ros2 topic list`` shows a node you stopped, or misses one you started; you changed ``ROS_DOMAIN_ID``; the network changed. Run ``ros2 daemon stop``, then the command again.

Writing Your First Node
-----------------------

The package of the last section has a build file but no code. This section writes a first node, as a class.

- **Goal:** a node that prints ``robotaxi_node is ready`` in the terminal.
- **Concepts:** starting ROS 2, logging, and a clean stop.
- **Build:** the lines to add to ``CMakeLists.txt``, and ``colcon build``.
- **Run:** ``ros2 run``.

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

Write a Node as a Class
"""""""""""""""""""""""

Write a node named ``robotaxi_node`` as a class, ``RoboTaxiNode``, in a header and a main file. The publisher section adds to this same class.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - Package
     - ``robotaxi_demo``
   * - Files
     - ``include/robotaxi_demo/robotaxi_node.hpp``, ``src/robotaxi_main.cpp``
   * - Node
     - ``robotaxi_node``
   * - Executable
     - ``robotaxi_exe``

**Resource:** `ROS 2 Jazzy: Writing a simple publisher and subscriber (C++) <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>`_.

Both files go in your ``robotaxi_demo`` package. The next four parts are the four steps: the header, ``main``, ``CMakeLists.txt``, and the build.

Step 1: the Header, robotaxi_node.hpp
"""""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 6, 8, 9

   #pragma once
   #include <rclcpp/rclcpp.hpp>

   namespace robotaxi_demo {

   class RoboTaxiNode : public rclcpp::Node {
    public:
     RoboTaxiNode() : rclcpp::Node{"robotaxi_node"} {
       RCLCPP_INFO_STREAM(get_logger(), get_name() << " is ready");
     }
   };

   }  // namespace robotaxi_demo

- Line 6: a ``RoboTaxiNode`` is an ``rclcpp::Node`` (public inheritance).
- Line 8: the base class constructor gets the node's name, ``robotaxi_node``.
- Line 9: ``RCLCPP_INFO_STREAM`` logs one line at the INFO level, with ``<<`` as in ``std::cout``. ``get_logger()`` and ``get_name()`` are public methods inherited from ``rclcpp::Node``; ``get_name()`` returns ``robotaxi_node``. The constructor is short, so it stays in the header.

Step 2: main, in robotaxi_main.cpp
""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 8, 9, 10

   #include <memory>

   #include <rclcpp/rclcpp.hpp>

   #include "robotaxi_demo/robotaxi_node.hpp"

   int main(int argc, char** argv) {
     rclcpp::init(argc, argv);
     auto node{std::make_shared<
       robotaxi_demo::RoboTaxiNode>()};
     //rclcpp::spin(node);
     rclcpp::shutdown();
   }

- Line 8: starts ROS 2 and the middleware. Call it before you make any node.
- Lines 9 and 10: make a ``RoboTaxiNode`` in a ``std::shared_ptr``, the form ``rclcpp::spin`` takes, instead of a plain ``rclcpp::Node``. Its constructor logs the line.
- Line 11: ``rclcpp::spin`` is commented out for now; `Node Spinning`_ explains it. Without it, the program ends right after the log line.
- Line 12: stops ROS 2 and frees what ``init`` set up.

Step 3: CMakeLists.txt
""""""""""""""""""""""

**Edit** ``CMakeLists.txt``: the lines for this first version of the node. They go after the ``find_package`` lines and before ``ament_package()``.

.. code-block:: cmake
   :linenos:
   :emphasize-lines: 1, 2, 3, 4, 5

   include_directories(include)
   add_executable(robotaxi_exe src/robotaxi_main.cpp)
   ament_target_dependencies(robotaxi_exe rclcpp)
   install(TARGETS robotaxi_exe
     DESTINATION lib/${PROJECT_NAME})

- Line 1: lets ``#include "robotaxi_demo/robotaxi_node.hpp"`` find the header in ``include``.
- Line 2: builds the executable ``robotaxi_exe`` from ``src/robotaxi_main.cpp``. The publisher section adds ``src/robotaxi_node.cpp`` to this line.
- Line 3: links ``robotaxi_exe`` to ``rclcpp``, the package it uses.
- Lines 4 and 5: install the executable "so ``ros2 run`` can find your executable" (`Writing a simple publisher and subscriber (C++) <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html>`_). Each executable of the package gets its own ``install`` lines.

Step 4: Build and Test
""""""""""""""""""""""

**Build and run**, from ``~/ros2_ws``:

.. code-block:: bash

   colcon build --packages-select robotaxi_demo
   source install/setup.bash
   ros2 run robotaxi_demo robotaxi_exe

.. code-block:: text

   [INFO] [1794184675.746034542] [robotaxi_node]: robotaxi_node is ready

- The line gives the level, the time in seconds since January 1, 1970, the node's name, and the text.
- The node prints its line, and the program ends at once: ``main`` does not spin yet. `Node Spinning`_ adds ``rclcpp::spin``, which keeps the node running until :kbd:`Ctrl+C`.

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

Node Spinning
-------------

**Spinning** keeps a node alive. The node waits for events, a message that arrives, a timer that is due, a service request, and runs the callback of each one.

The ``main`` of the robotaxi node does not spin yet: it logs one line and ends. This section explains spinning, starting with the thread that runs it, and adds ``rclcpp::spin`` to that ``main``.

Threads: Who Runs main and the Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Thread
   :class: tip

   A **thread** is "a flow of control within a program that begins with the invocation of a specific top-level function" (`Multi-threaded executions and data races <https://en.cppreference.com/w/cpp/language/multithread>`_). Threads "allow multiple functions to execute concurrently" (`std::thread <https://en.cppreference.com/w/cpp/thread/thread>`_).

- A process starts with one thread, the **main thread**, which runs ``main``.
- Every thread of a process can reach the same objects: "any thread can potentially access any object and function in the program" (cppreference). Two processes cannot.
- With spinning added, the main thread of ``robotaxi_main.cpp`` runs ``rclcpp::init``, makes the node, then enters ``rclcpp::spin`` and stays there until :kbd:`Ctrl+C`. Only then does it reach ``rclcpp::shutdown``.
- While it is inside ``spin``, the main thread runs the node's callbacks. One thread means one callback at a time.
- A program can start more threads, with ``std::thread`` or a multi-threaded executor, to run callbacks at the same time. That comes in a later lecture.

Spinning: the Main Thread Runs the Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Spinning** is a loop that the main thread runs inside ``rclcpp::spin(node)``.

.. figure:: /_static/images/l10/spin_main_thread.png
   :alt: On the left, a wavy line labeled main thread, with init, makes the node, leads to an arrow labeled rclcpp::spin(node) that enters a circle. Inside the circle: main thread, then 1. wait for an event, 2. run its callback, 3. repeat; an arrow runs around the circle. A red X marks the point on the right of the circle where the main thread leaves the loop. From there, an arrow marked with the keys Ctrl and C leads to a second wavy line labeled main thread, with rclcpp::shutdown().
   :align: center
   :width: 90%

   The main thread stays inside ``rclcpp::spin`` until :kbd:`Ctrl+C`, then runs ``rclcpp::shutdown()``.

- ``rclcpp::spin(node)`` makes "a default single-threaded executor" (`rclcpp, executors.hpp <https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/executors.hpp>`_). Its loop runs in the thread that called it, the main thread: "block until work comes in, execute it, and then repeat" (`rclcpp, single_threaded_executor.hpp <https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/executors/single_threaded_executor.hpp>`_). Work is a message that arrives, a timer that is due, or a request.
- One thread runs every callback, one at a time: a slow callback delays the others.

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
       robotaxi_demo::RoboTaxiNode>()};
     rclcpp::spin(node);
     rclcpp::shutdown();
   }

This is the ``main`` of every node in this lecture, with the class name changed. In ``robotaxi_main.cpp``, remove the ``//`` before ``rclcpp::spin(node)``.

**What happens during spin**

1. **Event loop:** it waits for a message, a timer or a request.
2. **Callback execution:** it runs the callback of the event that happened, then waits again.
3. **One at a time:** the default executor runs one callback at a time, on the main thread. A slow callback delays the others.
4. **Signal handling:** :kbd:`Ctrl+C` ends the loop. ``spin`` returns, and ``main`` goes on to ``shutdown``.

The ROS 2 documentation: ``rclcpp::spin(node)`` "expands to an instantiation and invocation of the Single-Threaded Executor" (`Executors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`_).

.. dropdown:: More detail: other ways to spin
   :class-container: more-detail
   :icon: info

   ``rclcpp::spin(node)`` is the default: it returns only after :kbd:`Ctrl+C`.

   **Spin some:** ``rclcpp::spin_some(node)`` runs the callbacks that are ready now, then returns. **Use it when** ``main`` has its own loop with other work.

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

   **An executor:** the same loop as an object. **Use it when** one program spins several nodes, or needs several threads (a later lecture).

   .. code-block:: cpp

      rclcpp::executors::SingleThreadedExecutor executor;
      executor.add_node(node);
      executor.spin();

   .. note::

      Use ``rclcpp::spin`` for a simple node. Use an executor when you spin several nodes or need threads. Executors come in a later lecture.

   rclcpp also has ``spin_all``, which runs all the work that is ready within a time limit, and ``spin_until_future_complete``, which spins until one result arrives (`rclcpp, executors.hpp <https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/executors.hpp>`_).

Build and Test: the Node Runs until Ctrl + C
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In ``robotaxi_main.cpp``, remove the ``//`` before ``rclcpp::spin(node)`` and before the log line after it:

.. code-block:: cpp

   rclcpp::spin(node);
   RCLCPP_INFO(node->get_logger(), "exited the loop...");

Build and run, from ``~/ros2_ws``, then press :kbd:`Ctrl+C`:

.. code-block:: bash

   colcon build --packages-select robotaxi_demo
   source install/setup.bash
   ros2 run robotaxi_demo robotaxi_exe

.. code-block:: text

   [INFO] [1794342586.660525330] [robotaxi_node]: robotaxi_node is ready
   [INFO] [1794342588.480817680] [rclcpp]: signal_handler(SIGINT/SIGTERM)
   [INFO] [1794342588.481109258] [robotaxi_node]: exited the loop...

- Without ``spin``, the program ended after its first line. Now it keeps running: the main thread waits inside ``spin``.
- :kbd:`Ctrl+C` makes ``spin`` return: rclcpp logs the second line. Then ``main`` logs "exited the loop..." and runs ``rclcpp::shutdown``.

Common Mistakes, and What You See
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Messages
--------

**Messages** are the data structures that nodes send each other. A message type is written in a ``.msg`` file, and every message on a topic has the topic's type.

A message type is an **interface**: a text description of data that ROS 2 turns into C++ and Python code. There are three kinds: messages (``.msg``) for topics, services (``.srv``) and actions (``.action``). So the command that reads a message type is ``ros2 interface``. The ROS 2 documentation says ROS applications "typically communicate through interfaces of one of three types", and that the description lets ROS tools "automatically generate source code for the interface type in several target languages" (`ROS 2 Jazzy: Interfaces <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Interfaces.html>`_).

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

  .. dropdown:: More detail: ``ros2 interface list -m``
     :class-container: more-detail
     :icon: info

     .. list-table::
        :header-rows: 1
        :widths: 32 68

        * - Argument
          - Meaning (from ``ros2 interface list --help``)
        * - ``-m``, ``--only-msgs``
          - "Print out only the message types". ``-s`` gives only the services, ``-a`` only the actions.
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

To use a message package, name it in ``package.xml`` and in ``CMakeLists.txt``. For ``geometry_msgs``, your package has:

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

   add_executable(robotaxi_exe src/robotaxi_main.cpp src/robotaxi_node.cpp)
   ament_target_dependencies(robotaxi_exe rclcpp geometry_msgs)

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

.. dropdown:: More detail: ``ros2 topic pub``
   :class-container: more-detail
   :icon: info

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Meaning (from ``ros2 topic pub --help``)
      * - ``--once`` (``-1``)
        - "Publish one message and exit".
      * - ``/robotaxi/position``
        - "Name of the ROS topic to publish to".
      * - ``geometry_msgs/msg/Point``
        - "Type of the ROS message".
      * - ``"{x: 7.0, y: 4.0}"``
        - "Values to fill the message with in YAML format"; a field left out keeps its default value.

- The fields are written as ``{name: value}``. A field you leave out keeps 0.0, here ``z``. A string: ``"data: 'Hello World'"``; an integer: ``"data: 42"``; a boolean: ``"data: true"``.
- ``--once`` (or ``-1``) sends one message and stops. Without it, the command sends one message per second until :kbd:`Ctrl+C`.
- ``--rate 10`` sends 10 per second. ``--times 5`` sends 5 and stops.

Publishers
----------

A **publisher** is the object a node uses to send messages on one topic. One publisher, many subscribers.

.. figure:: /_static/images/l10/publisher_steps.png
   :alt: A flowchart of the publisher's steps. Three boxes in a row, joined by arrows: tag 1, Create the publisher, with message type, topic name, queue size; tag 2, Create a message and fill its fields; tag 3, Publish, to every subscriber. From the Publish box, an arrow loops back to the second box, with tag 4 and the label Repeat, often from a timer.
   :align: center
   :width: 90%

   The publisher's steps: step 1 runs once; steps 2 and 3 repeat.

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

Add a publisher to ``RoboTaxiNode``: the robotaxi publishes its position, a ``Point``, on the topic ``robotaxi/position`` every 0.5 s.

.. list-table::
   :widths: 25 75
   :class: compact-table

   * - Package
     - ``robotaxi_demo``
   * - Files
     - ``include/robotaxi_demo/robotaxi_node.hpp``, ``src/robotaxi_node.cpp``, ``src/robotaxi_main.cpp``
   * - Node
     - ``robotaxi_node``
   * - Executable
     - ``robotaxi_exe``

.. warning::

   The package already depends on ``geometry_msgs``. For a new package, add the dependency to ``package.xml`` and ``CMakeLists.txt`` first.

The robotaxi drives along a street, the x axis, 1 m every 0.5 s. ``robotaxi_main.cpp`` does not change. The new method goes in ``robotaxi_node.cpp``.

The Header: a Publisher and a Timer
"""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 5, 6, 7, 8, 11, 12

   class RoboTaxiNode : public rclcpp::Node {
    public:
     RoboTaxiNode()
         : rclcpp::Node{"robotaxi_node"},
           publisher_{create_publisher<geometry_msgs::msg::Point>(
               "robotaxi/position", 10)},
           timer_{create_wall_timer(std::chrono::milliseconds{500},
               std::bind(&RoboTaxiNode::publish_position, this))} {}
    private:
     void publish_position();
     rclcpp::Publisher<geometry_msgs::msg::Point>::SharedPtr publisher_;
     rclcpp::TimerBase::SharedPtr timer_;
     double x_{0.0};  // position along the street, in m
   };

The constructor makes a publisher (lines 5 and 6) and a timer (lines 7 and 8). The class keeps both in data members (lines 11 and 12). Above the class, the file includes ``<chrono>``, ``<functional>``, ``<geometry_msgs/msg/point.hpp>`` and ``<rclcpp/rclcpp.hpp>``, inside ``namespace robotaxi_demo``.

Initialize the Publisher
^^^^^^^^^^^^^^^^^^^^^^^^

What the Constructor Makes
""""""""""""""""""""""""""

The timer needs a callable to run every 500 ms. The class gives it in one of two ways, and both build and run the same on Jazzy. The slides use ``std::bind``.

.. tab-set::

   .. tab-item:: With std::bind

      .. code-block:: cpp
         :linenos:

         publisher_{create_publisher<geometry_msgs::msg::Point>(
             "robotaxi/position", 10)},
         timer_{create_wall_timer(std::chrono::milliseconds{500},
             std::bind(&RoboTaxiNode::publish_position, this))} {}

      - Lines 3 and 4: every 500 ms (2 Hz), the timer calls ``publish_position`` on this object. ``std::bind``, from ``<functional>``, joins the method, ``&RoboTaxiNode::publish_position``, to the object to call it on, ``this``.

   .. tab-item:: With a lambda

      .. code-block:: cpp
         :linenos:

         publisher_{create_publisher<geometry_msgs::msg::Point>(
             "robotaxi/position", 10)},
         timer_{create_wall_timer(std::chrono::milliseconds{500},
                                  [this]() { publish_position(); })} {}

      - Lines 3 and 4: every 500 ms (2 Hz), the timer calls the lambda, and the lambda calls ``publish_position``. ``[this]`` lets the lambda call a method of this object. This version needs no ``<functional>``.

In both versions:

- Lines 1 and 2: a publisher of ``Point`` on the topic ``robotaxi/position``. The 10 is the queue size: up to 10 messages wait for a subscriber that falls behind.
- Lines 3 and 4: ``create_wall_timer`` takes two arguments (`rclcpp node.hpp, Jazzy <https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/node.hpp>`_). The **period**, the "time interval between triggers of the callback": 500 ms, so 2 Hz. The **callback**, what the timer runs each time.
- ``create_publisher`` and ``create_wall_timer`` are methods inherited from ``rclcpp::Node``. Each returns a ``std::shared_ptr``.

.. warning::

   **Store the timer.** A timer that is not kept in a data member is destroyed at the end of the constructor, and its callback never runs. A test node with such a timer printed nothing in 1.5 s.

Hand the Timer a Method: std::bind
""""""""""""""""""""""""""""""""""

The timer needs something it can call on its own; ``std::bind`` makes one from a method and an object.

- **Why:** the timer runs its callback as ``callback_()``, with no object (`rclcpp timer.hpp, Jazzy <https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/timer.hpp>`_). A method runs only on an object: ``this->publish_position()``. Passing ``&RoboTaxiNode::publish_position`` alone does not compile (Jazzy, g++: ``'operator()' is not a member of 'void (robotaxi_demo::RoboTaxiNode::*)()'``).
- **What:** ``std::bind``, from ``<functional>``, "generates a forwarding call wrapper" (`std::bind <https://en.cppreference.com/w/cpp/utility/functional/bind>`_): a new object that, when called, calls the method on the object you gave it.
- ``&RoboTaxiNode::publish_position``: which method to call. The ``&`` gives the method's address.
- ``this``: which object to call it on, this robotaxi.
- A lambda, ``[this]() { publish_position(); }``, does the same job (the second tab above): ``[this]`` lets its body call a method of this object.

This is the standard C++ ``std::bind``, from ``<functional>``; ROS 2 adds nothing to it.

.. code-block:: cpp
   :linenos:

   int add(int a, int b) { return a + b; }
   auto add2{std::bind(add, 2, std::placeholders::_1)};
   add2(5);  // runs add(2, 5): 7

   auto callback{std::bind(&RoboTaxiNode::publish_position, this)};
   callback();  // runs this->publish_position()

- The member-function form is the part you may not have seen in plain C++. Simple examples often bind a **free function**, a function that is not a method of a class, such as ``std::bind(add, 2, _1)``, which fixes the first argument (lines 1 to 3).
- Here it binds a member function: ``&RoboTaxiNode::publish_position`` is a pointer to a method, and ``this`` is bound as the object to call it on. Calling the result runs ``this->publish_position()`` (lines 5 and 6).
- That is standard C++ too; it would work the same outside ROS, with any class.
- A placeholder is needed only when a value has to come in at call time, such as the message on the subscriber's ``std::placeholders::_1``.
- For the timer, ``publish_position`` takes no parameters and the timer passes nothing, so no placeholder is needed.

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

In ``CMakeLists.txt``, the executable lists two source files: ``add_executable(robotaxi_exe src/robotaxi_main.cpp src/robotaxi_node.cpp)``. Then ``colcon build --packages-select robotaxi_demo`` and ``source install/setup.bash``.

**Terminal 1:** ``ros2 run robotaxi_demo robotaxi_exe``

.. code-block:: text

   [INFO] [1794204168.548507563] [robotaxi_node]: Published x = 0
   [INFO] [1794204169.048440989] [robotaxi_node]: Published x = 1

**Terminal 2:** ``ros2 topic hz /robotaxi/position``

.. code-block:: text

   average rate: 2.000
     min: 0.500s max: 0.500s std dev: 0.00012s window: 9

**Terminal 2:** ``ros2 topic echo /robotaxi/position --once``

.. code-block:: text

   x: 13.0
   y: 0.0
   z: 0.0

.. dropdown:: More detail: ``ros2 topic echo --once``
   :class-container: more-detail
   :icon: info

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Meaning (from ``ros2 topic echo --help``)
      * - ``/robotaxi/position``
        - The topic whose messages are printed.
      * - ``--once``
        - "Print the first message received and then exit".

.. admonition:: Conclusion
   :class: tip

   The topic carries 2.000 messages per second, 0.500 s apart: the 500 ms that ``create_wall_timer`` asked for. The log times agree: 784.416, then 784.917.

Subscribers
-----------

A **subscriber** is the object a node uses to receive the messages of one topic. It runs a callback for each message, so the node reacts to data that other nodes publish.

.. figure:: /_static/images/l10/subscriber_steps.png
   :alt: A flowchart of the subscriber's steps. Four boxes in a row, joined by arrows: tag 1, Create the subscription, with message type, topic name, queue size, callback; tag 2, Define the callback, it handles one message; tag 3, Spin, wait for a message; tag 4, Run the callback, on that message. From the fourth box, an arrow loops back to Spin, labeled Repeat for each message.
   :align: center
   :width: 90%

   The subscriber's steps: steps 3 and 4 repeat for each message.

**The subscriber's steps**

1. **Create the subscription:** message type, topic name, queue size, callback.
2. **Define the callback:** the function that handles one message.
3. **Spin:** wait for a message.
4. **Run the callback** on that message, then go back to step 3.

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
     - ``dispatcher_node``
   * - Executable
     - ``dispatcher_exe``

The pickup point, at x = 10 m and y = 0 m, is chosen for this example. ``dispatcher_main.cpp`` is the spinning pattern with ``DispatcherNode``, and ``CMakeLists.txt`` gets the same three commands as the publisher, ``add_executable``, ``ament_target_dependencies`` and ``install``, with ``dispatcher_exe`` in place of ``robotaxi_exe``.

The Header: a Subscription and a Callback
"""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:
   :emphasize-lines: 5, 6, 7, 8, 11

   class DispatcherNode : public rclcpp::Node {
    public:
     DispatcherNode()
         : rclcpp::Node{"dispatcher_node"},
           subscription_{create_subscription<geometry_msgs::msg::Point>(
               "robotaxi/position", 10,
               std::bind(&DispatcherNode::on_position, this,
                         std::placeholders::_1))} {}
    private:
     void on_position(const geometry_msgs::msg::Point& msg);
     rclcpp::Subscription<geometry_msgs::msg::Point>::SharedPtr subscription_;
     double pickup_x_{10.0};  // pickup point, in m
     double pickup_y_{0.0};   // pickup point, in m
   };

The constructor makes a subscription (lines 5 to 8), kept in a data member (line 11). The file includes ``<functional>``, ``<geometry_msgs/msg/point.hpp>`` and ``<rclcpp/rclcpp.hpp>``, inside ``namespace robotaxi_demo``.

Initialize the Subscriber
^^^^^^^^^^^^^^^^^^^^^^^^^

What the Subscription Constructor Makes
"""""""""""""""""""""""""""""""""""""""

The callback is made in one of two ways, as for the timer. Both build and print the same lines on Jazzy. The slides use ``std::bind``.

.. tab-set::

   .. tab-item:: With std::bind

      .. code-block:: cpp
         :linenos:

         subscription_{create_subscription<geometry_msgs::msg::Point>(
             "robotaxi/position", 10,
             std::bind(&DispatcherNode::on_position, this,
                       std::placeholders::_1))} {}

      - Lines 3 and 4: ``std::bind`` joins ``on_position`` to this object, as for the timer. ``std::placeholders::_1`` is a slot for the first argument: ``spin`` fills it with the message, and the call becomes ``this->on_position(msg)``. The timer passes no argument, so its ``std::bind`` has no slot.

   .. tab-item:: With a lambda

      .. code-block:: cpp
         :linenos:

         subscription_{create_subscription<geometry_msgs::msg::Point>(
             "robotaxi/position", 10,
             [this](const geometry_msgs::msg::Point& msg) {
               on_position(msg);
             })} {}

      - Lines 3 to 5: the lambda takes the message and passes it on to ``on_position``. You see the argument, and there is no slot to count.

In both versions:

- Lines 1 and 2: the same message type and the same topic name as the publisher (rules 1 and 2). The 10 is the queue size: up to 10 messages wait while the callback is busy.
- ``rclcpp::spin`` calls the callback once for each message, with the message as its argument. The type of ``on_position``'s parameter must be the topic's type; a reference avoids a copy.
- Start the dispatcher before the robotaxi or after it: rule 4 says it waits for a publisher.

Process Messages
^^^^^^^^^^^^^^^^

The Callback: the Distance to the Pickup Point
""""""""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // src/dispatcher_node.cpp
   void DispatcherNode::on_position(const geometry_msgs::msg::Point& msg) {
     const double distance{
         std::hypot(pickup_x_ - msg.x, pickup_y_ - msg.y)};
     RCLCPP_INFO_STREAM(get_logger(), distance << " m from the pickup");
   }

``std::hypot(a, b)``, from ``<cmath>``, is the square root of a\ :sup:`2` + b\ :sup:`2`. For ``{x: 7.0, y: 4.0}``, the robotaxi is 3 m from the pickup in x and 4 m in y: the square root of 9 + 16 is 5, so the dispatcher prints ``5 m from the pickup``.

.. warning::

   The callback runs whenever a message arrives, one at a time. Keep it faster than the time between messages, here 0.5 s, or the queue fills and messages are dropped (scenario 3).

Build and Test the Subscriber
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the Complete System
"""""""""""""""""""""""

**Terminal 1:** ``ros2 run robotaxi_demo dispatcher_exe``. **Terminal 2:** ``ros2 run robotaxi_demo robotaxi_exe``.

.. code-block:: text

   [INFO] [...168.548705] [dispatcher_node]: 10 m from the pickup
   [INFO] [...169.048546] [dispatcher_node]: 9 m from the pickup
   [INFO] [...169.548548] [dispatcher_node]: 8 m from the pickup

**Terminal 3:** ``ros2 topic info /robotaxi/position``

.. code-block:: text

   Type: geometry_msgs/msg/Point
   Publisher count: 1
   Subscription count: 1

- Also in terminal 3: ``ros2 topic list`` shows the topic, ``ros2 topic echo /robotaxi/position`` prints each position, and ``ros2 topic hz /robotaxi/position`` gives 2.000 per second.
- The robotaxi logged ``Published x = 0`` at ...168.548507 s. The dispatcher logged ``10 m from the pickup`` for it at ...168.548705 s: 168.548705 − 168.548507 = 0.000198 s. The message took about 0.2 ms, on one computer.

When nothing arrives, check the topic names first: ``ros2 topic list`` shows what each side uses (rule 1).

Who Connects the Nodes: DDS, Not Your Code
""""""""""""""""""""""""""""""""""""""""""

Your code never names another node. DDS, under your code, makes the links.

1. **Discovery:** each node advertises its presence, and the others "respond to this advertisement with information about themselves so that the appropriate connections can be made" (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_).
2. **Matching:** a publisher and a subscription with the same topic name, the same type and compatible QoS are linked. Then they communicate "without the need for a tool like the ROS master" (`ROS 2 with DDS <https://design.ros2.org/articles/ros_on_dds.html>`_).

What DDS knows, with the robotaxi and the dispatcher running (output trimmed):

.. code-block:: bash

   ros2 topic info /robotaxi/position --verbose

.. code-block:: text

   Publisher count: 1

   Node name: robotaxi_node
   Endpoint type: PUBLISHER
   QoS profile:
     Reliability: RELIABLE

   Subscription count: 1

   Node name: dispatcher_node
   Endpoint type: SUBSCRIPTION
   QoS profile:
     Reliability: RELIABLE

.. admonition:: Conclusion
   :class: tip

   The nodes do not know each other; DDS does. A new subscriber is linked when it starts, and no code changes.

Discussion: Three Dispatchers That Hear Nothing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each version builds, runs next to the robotaxi node, and prints nothing (Jazzy). Why? Which ``ros2`` command shows the problem? ``Point`` is ``geometry_msgs::msg::Point``; ``callback`` is the lambda of the dispatcher.

**A.** The constructor:

.. code-block:: cpp

   DispatcherNode() : rclcpp::Node{"dispatcher_node"} {
     auto subscription{create_subscription<Point>(
         "robotaxi/position", 10, callback)};
   }

**B.** The data member's initializer:

.. code-block:: cpp

   subscription_{create_subscription<Point>(
       "robotaxi/positon", 10, callback)}

**C.** ``main``, with the correct node:

.. code-block:: cpp

   rclcpp::init(argc, argv);
   auto node{std::make_shared<DispatcherNode>()};
   rclcpp::shutdown();

.. dropdown:: Answers
   :class-container: sd-border-secondary

   All three were run on Jazzy next to the robotaxi node. A correct dispatcher printed x = 4, 5, 6, 7 in the same run, so the silence is real.

   - **A:** ``subscription`` is a local variable. The ``SharedPtr`` is destroyed when the constructor returns, and the subscription with it. ``ros2 node info /dispatcher_node`` lists only ``/parameter_events`` under Subscribers, and ``ros2 topic info /robotaxi/position`` shows ``Subscription count: 0``. Fix: keep it in a data member, as the repository does.
   - **B:** a typo, ``positon``. ``ros2 topic list`` shows both ``/robotaxi/position`` and ``/robotaxi/positon``: rule 1, no error, nothing arrives.
   - **C:** no ``rclcpp::spin``. ``main`` makes the node and ends at once: the run took 0.34 s. No callback ever runs.
   - A silent subscriber is a name, a lifetime or a missing spin. The ``ros2`` tools tell which.

Publisher-Subscriber Communication
----------------------------------

In DDS, the middleware under ROS 2, two objects carry a topic:

- A **DataWriter**: made by a ROS 2 publisher. It writes the messages to the network.
- A **DataReader**: made by a ROS 2 subscriber. It reads the messages from the network.

A DataWriter and a DataReader connect only when they match: the same topic name, the same type, and compatible QoS settings (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_). The four scenarios that follow show what happens to the messages once they match, or when nobody reads.

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

A test version of the dispatcher keeps a queue of 3 and spends 1.7 s in each callback (both chosen for this example). The robotaxi publishes every 0.5 s. The callback end times and the message each callback takes were measured; a full queue pushes out its oldest message.

.. list-table::
   :header-rows: 1
   :widths: 14 25 31 30
   :class: compact-table

   * - Time
     - Publisher
     - Subscriber's queue
     - Subscriber's callback
   * - 0.0 s
     - Publishes x = 0
     - [ ] then [0] then [ ]
     - Starts on x = 0 at once
   * - 0.5 to 1.5 s
     - Publishes x = 1, 2, 3
     - [1, 2, 3]
     - Still on x = 0
   * - 1.71 s
     -
     - [2, 3]
     - Finishes x = 0; starts x = 1
   * - 2.0 to 3.0 s
     - Publishes x = 4, 5, 6
     - [4, 5, 6]; x = 2, 3 pushed out
     - Still on x = 1
   * - 3.41 s
     -
     - [5, 6]
     - Finishes x = 1; starts x = 4
   * - 3.5 to 5.0 s
     - Publishes x = 7 to 10
     - [8, 9, 10]; x = 5, 6, 7 pushed out
     - Still on x = 4
   * - 5.11 s
     -
     - [9, 10]
     - Finishes x = 4; starts x = 8

Scenario 3: What the Slow Subscriber Lost
"""""""""""""""""""""""""""""""""""""""""

.. admonition:: Conclusion
   :class: tip

   In 11 s the robotaxi published 23 positions, x = 0 to 22. The dispatcher handled 7 of them. At 10.2 s it started on x = 18, published at 9.0 s: 1.2 s old.

Each box is one callback: the message it handled and the time it started.

.. figure:: /_static/images/l10/slow_sub_flow.png
   :alt: Flowchart of seven boxes in a row, joined by arrows: x = 0 at 0.0 s, x = 1 at 1.7 s, x = 4 at 3.4 s, x = 8 at 5.1 s, x = 11 at 6.8 s, x = 15 at 8.5 s, x = 18 at 10.2 s. Under each arrow, the messages pushed out before the next callback: none; 2, 3; 5, 6, 7; 9, 10; 12, 13, 14; 16, 17.
   :align: center
   :width: 100%

   The seven callbacks of the slow dispatcher, and the messages pushed out between them.

- **Data loss:** each 1.7 s callback sees 3 or 4 new messages, and the queue keeps 3.
- **Stale data:** the dispatcher works on a position that is 1.2 s old.
- **Fixes:** a shorter callback, a lower publish rate, or a larger queue. The larger queue only delays the loss: each message still takes 1.7 s.

Scenario 4: the Publisher's Queue Fills Up
""""""""""""""""""""""""""""""""""""""""""

With reliable delivery, the default, the publisher keeps each message in its queue until every subscriber acknowledges it (`Fast DDS: Standard QoS Policies <https://fast-dds.docs.eprosima.com/en/latest/fastdds/dds_layer/core/policy/standardQosPolicies.html>`_). Here the dispatcher stops acknowledging: its process is frozen for 10 s, then resumed. Chosen for this example: 2 Hz, messages of 100 KB (an image), a publisher queue of 10, a subscriber queue of 100. Measured on Jazzy, two test nodes.

.. list-table::
   :header-rows: 1
   :widths: 15 25 32 28
   :class: compact-table

   * - Time
     - Publisher
     - Publisher's queue
     - Dispatcher
   * - 0.5 to 2.5 s
     - Publishes x = 0 to 4
     - Acknowledged, then removed
     - Receives x = 0 to 4
   * - 3.0 to 12.5 s
     - Publishes x = 5 to 24
     - Keeps the last 10 not acknowledged; x = 5 to 14 pushed out
     - Frozen: no acknowledgement
   * - 12.8 s
     -
     - Sends x = 15 to 24 again
     - Resumes: x = 5, 6, then x = 15 to 24

.. admonition:: Conclusion
   :class: tip

   The dispatcher lost x = 7 to 14. It got x = 5 and 6 from its computer's receive buffer, and x = 15 to 24 from the publisher's queue of 10.

.. dropdown:: More detail: how the test was run
   :class-container: more-detail
   :icon: info

   - Both test nodes use reliable delivery and keep last. Each message is a ``std_msgs/msg/String`` of 100,000 characters that starts with its number x.
   - The dispatcher's process is frozen with ``kill -STOP <pid>`` 3 s after the publisher starts, and resumed with ``kill -CONT <pid>`` 10 s later. A frozen process cannot read or acknowledge anything.
   - Both run with ``FASTDDS_BUILTIN_TRANSPORTS=UDPv4``, so the messages go through the network stack, as between two computers. On one computer, Fast DDS can also use shared memory.

Scenario 4: When the Publisher's Queue Fills
""""""""""""""""""""""""""""""""""""""""""""

The publisher's queue fills when acknowledgements stop coming: a subscriber that is frozen or unreachable, or a network that loses packets.

.. admonition:: What scenario 4 shows
   :class: key-box

   - **No blocking:** with keep last, the default, "the system will discard the oldest sample to make room for a new one" (`Fast DDS: Standard QoS Policies <https://fast-dds.docs.eprosima.com/en/latest/fastdds/dds_layer/core/policy/standardQosPolicies.html>`_). Each ``publish`` returned in under 1 ms.
   - **The depth decides what survives:** with a publisher queue of 3, the dispatcher got x = 5, 6, then only x = 22 to 24.
   - **Small messages hide it:** with messages of 10 characters, the same 10 s freeze lost nothing. The receive buffer, 212,992 bytes here, held all of them.
   - **Keep all:** ``publish`` blocks "until the oldest sample has been acknowledged by all readers and can be removed", up to a maximum blocking time, 100 ms by default, then returns an error (`Fast DDS: Standard QoS Policies <https://fast-dds.docs.eprosima.com/en/latest/fastdds/dds_layer/core/policy/standardQosPolicies.html>`_).

Scenario 3 filled the subscriber's queue; this one fills the publisher's.

Investigate a Program You Did Not Write
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must write a node that warns the dispatcher when a robotaxi's battery is low. The robotaxi simulator comes with no source code and no documentation. The topic name ``/robotaxi/battery`` is chosen for this example. A ``ros2`` command answers each question:

.. list-table::
   :header-rows: 1
   :widths: 38 62
   :class: compact-table

   * - Question
     - Command and result
   * - 1. Which nodes are running?
     - ``ros2 node list``. If nothing shows, the simulator and your terminal do not share a domain ID or a network (`Discovery in Practice: Domain IDs and Your Network`_).
   * - 2. Which topic has the battery level?
     - ``ros2 topic list -t``: its type is ``sensor_msgs/msg/BatteryState``. ``ros2 node info`` on the simulator's node lists everything it publishes.
   * - 3. Which fields does the type have?
     - ``ros2 interface show sensor_msgs/msg/BatteryState``: ``percentage`` goes from 0 to 1, NaN if not measured ("Charge percentage on 0 to 1 range (If unmeasured NaN)"). Below 20 % means below 0.2, and your node must check for NaN.
   * - 4. Who publishes it, and how?
     - ``ros2 topic info /robotaxi/battery --verbose``: the publishing node and its QoS, such as ``Reliability: RELIABLE``. Your subscriber must use settings that match.
   * - 5. What do real values look like?
     - ``ros2 topic echo /robotaxi/battery --once``: one real message, so you see the actual numbers before you trust the field names.
   * - 6. How often do messages arrive?
     - ``ros2 topic hz /robotaxi/battery``. The rate tells how fast your callback must be, or messages queue up (scenario 3).
   * - 7. Which package to depend on?
     - ``sensor_msgs``, the first part of the type. It goes in ``package.xml`` and ``CMakeLists.txt``, as ``geometry_msgs`` did.

Recap: the Lecture in One UML Component Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each box is a node. The ball is the interface ``robotaxi_node`` provides (it publishes); the socket is the one ``dispatcher_node`` requires (it subscribes). The notes hold the rest of the lecture.

.. figure:: /_static/images/l10/l10_recap.png
   :alt: UML component diagram. Two components in a row, robotaxi_node : RoboTaxiNode on the left and dispatcher_node : DispatcherNode on the right. Between them, a ball provided by robotaxi_node meets a socket required by dispatcher_node, labeled geometry_msgs/msg/Point on /robotaxi/position. Notes: above robotaxi_node, derives from rclcpp::Node, a publisher with a queue of 10, a 500 ms timer that fills a Point, then publisher_->publish(msg). Above the interface, a message type is an interface (.msg), both sides use the same topic and type. Above dispatcher_node, derives from rclcpp::Node, a subscription with a queue of 10, spin runs on_position for each message, a slow callback loses messages. Below robotaxi_node, package robotaxi_demo holds both nodes, package.xml and CMakeLists.txt declare rclcpp and geometry_msgs, then colcon build, source install/setup.bash, ros2 run. Bottom right, under each node: rclcpp, rcl, rmw, DDS, OS and network; inspect it with ros2 node list, ros2 topic list, echo, hz, info, ros2 interface show.
   :align: center
   :width: 100%

   The robotaxi and the dispatcher as a UML component diagram, with the lecture's main points as notes.
