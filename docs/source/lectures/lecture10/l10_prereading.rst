====================================================
Pre-Reading
====================================================

Read this page before Lecture 10, and do the two steps of `Before Class`_. The lecture does not repeat this material: it starts with the three ways nodes talk, then builds a publisher and a subscriber in the workspace you create here.

Before Class
------------

1. A new GitHub repository holds the ROS packages of this course: `rubixcubic/enpm702-fall-2026-ros <https://github.com/rubixcubic/enpm702-fall-2026-ros>`_. Clone it into the ``src`` folder of your workspace and push it to your own private GitHub repository, as `ROS 2 Workspace <../../setup/ros_setup.html#ros-2-workspace>`_ in :doc:`/setup/ros_setup` shows (`Create a Workspace`_ explains what a workspace is).
2. Install ROS 2 Jazzy, as in :doc:`/setup/ros_setup`.

ROS 2
-----

**ROS 2** (Robot Operating System 2) is a set of libraries and tools for robot software. It is not an operating system: it runs on one, here Ubuntu 24.04.

.. note::

   ROS 2 breaks a large application into smaller programs. It moves the data between them, on one computer or across several, so you write the behavior of the robot and not the networking.

- `ros.org <https://www.ros.org/>`_: the project's home page.
- `ROS 2 Jazzy documentation <https://docs.ros.org/en/jazzy/>`_: the reference for this course.
- `ROS Index <https://index.ros.org/>`_: every released ROS package.
- `github.com/ros2 <https://github.com/ros2>`_: the source code.

**Who maintains ROS:** `Open Robotics <https://www.openrobotics.org/>`_, with the community. It is the Open Source Robotics Foundation (OSRF), a US nonprofit founded in 2012, which also makes the Gazebo simulator.

Designed for Robots That Leave the Lab
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l10/what_is_ros_for.jpeg
   :alt: A hand-drawn poster titled ROS 2: designed for robots that leave the lab, built for real-world, commercial and complex environments. Top right, a smiling robot with I love the outside world on its chest walks out of a building marked LAB. Three panels below. Products: a delivery robot hands a box to a man on a city street while a woman pushes a shopping cart; caption: robots that people buy and use, not only research prototypes. Several robots on one network: a drone, two robot arms and a small wheeled robot, labeled nodes and bots, joined by dotted lines to a Wi-Fi router labeled hub; caption: each with many nodes, communicating in complex team environments. Real-time control: smiling packages labeled fast data packets fly along an arrow to a stopwatch marked tick-tock, past a robot arm marked on time; caption: commands that must arrive on time, ensuring safety, accuracy and predictability. Bottom line: ROS 2, empowering the next generation of autonomous systems. Bottom right: based on Macenski et al., 2022.
   :align: center
   :width: 100%

   What ROS 2 was designed for: products, several robots on one network, and commands that must arrive on time (based on Macenski et al., 2022).

What Runs under Your Node: the ROS 2 Layers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l10/ros2_layers.png
   :alt: A layered diagram, top to bottom, with a dashed arrow from each layer down to the next. At the top, a wide box, the application layer, holds three boxes: your nodes, robotaxi and dispatcher; topics, services and actions; node tools, parameters, ros2 and rqt. Below it: client libraries, rclcpp for C++ and rclpy for Python, one per language; rcl, the C library every client library shares; rmw, the middleware interface, so a node runs on any DDS; DDS, the middleware, Fast DDS by default, Cyclone DDS or Connext. At the bottom, a wide gray band: the operating system and the network, Ubuntu 24.04, Ethernet and Wi-Fi.
   :align: center
   :width: 100%

   The layers under a ROS 2 node, from the application down to the network.

You write the top layer: your **nodes**, programs that each do one job and exchange data with each other. **Middleware** is software that finds other programs and moves data between them. Source: `ROS 2 Jazzy: Internal ROS 2 interfaces <https://docs.ros.org/en/jazzy/Concepts/Advanced/About-Internal-Interfaces.html>`_.

What DDS Does: Find the Nodes, Move the Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: DDS
   :class: tip

   **DDS** (Data Distribution Service): the industry-standard middleware that moves ROS 2 messages. Jazzy uses eProsima's Fast DDS by default.

.. figure:: /_static/images/l10/dds_jobs.png
   :alt: Two node boxes, robotaxi on the left and dispatcher on the right, both standing on a wide navy band labeled DDS. Above the nodes, a dashed two-headed arrow between them carries tag 1. Inside the band, a solid arrow runs from under robotaxi to under dispatcher, with tag 2 and a small box reading position. Below the band, under the dispatcher and joined to the band by a line, a small box with tag 3 reads reliable, keep last 10.
   :align: center
   :width: 60%

   The three jobs of DDS, numbered 1 to 3 as in the list below.

1. **Discovery**: each program announces what it sends and what it wants. Programs that match find each other, with no central program.
2. **Transport**: DDS carries each message, here the robotaxi's position, to the dispatcher, on one computer or across a network.
3. **Quality of Service**: delivery settings. The default resends a lost message (reliable) and keeps the last 10 (`Quality of Service settings <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html>`_).

Discovery in Practice: Domain IDs and Your Network
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- By default, a node finds every node it can reach by **multicast** (one message that every computer on the network can receive) and that has the same **domain ID** (`Discovery <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Discovery.html>`_). The default domain ID is 0.
- Different domain IDs never see each other: a talker in domain 82 and a listener in 83, and the listener printed nothing in 4 s.

.. note::

   A network that does not pass multicast stops discovery between computers. On eduroam, students' nodes have never appeared on the instructor's laptop, from 2017 to today. Where multicast passes, as on a home router, set your own domain ID, 0 to 101, in ``~/.bashrc``: ``export ROS_DOMAIN_ID=``\ *number*.

Write ROS 2 Code in C++: rclcpp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: rclcpp
   :class: tip

   The ROS Client Library for C++: the C++ interface that "provides all of the ROS client functionality like creating nodes, publishers, and subscriptions" (`Client libraries <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Client-Libraries.html>`_). See `rclcpp API (Jazzy) <https://docs.ros.org/en/jazzy/p/rclcpp/>`_.

- One header, ``#include <rclcpp/rclcpp.hpp>``, and one namespace, ``rclcpp::``.
- In Lecture 10 you use ``rclcpp::init``, ``rclcpp::Node``, ``create_publisher``, ``create_subscription``, ``create_wall_timer``, ``rclcpp::spin`` and ``rclcpp::shutdown``.
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

The Node: the Unit of Computation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Node
   :class: tip

   A **node** is a program, or a part of one, that does one job and exchanges data with other nodes.

- A full robot runs many nodes: one senses, one filters, one controls, one drives the motors, one logs.
- Each node is written, tested and started on its own. Different people write them, and each runs at its own rate.
- Nodes talk only through defined interfaces: topics, services and actions, explained in Lecture 10. The same camera driver runs, unchanged, on another robot with that camera.

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

   Several programs, each run as its own process, on one computer or several. They do not call each other's functions: they send each other messages.

.. figure:: /_static/images/l10/distributed.png
   :alt: A dashed rounded box holds a box labeled robotaxi, which has an arrow labeled publish to a navy box that reads /robotaxi/position, and geometry_msgs/msg/Point. An arrow labeled subscribe goes from the navy box to a box labeled dispatcher, inside a second dashed rounded box.
   :align: center
   :width: 100%

   The robotaxi and the dispatcher as two programs, each in its own process (a dashed box).

The navy box is a **topic**: a name that nodes use to exchange one type of message.

**Advantages**

- A crash stops only that program.
- A change rebuilds and restarts one program.
- Each program runs at its own rate.
- Programs can run on several computers.

**Issues**

- Each message is copied: about 0.3 ms per message, measured in class with the robotaxi and the dispatcher.
- A slow receiver misses messages (shown in class with a slow subscriber).
- More programs to start and watch.
- Both sides must use the same type.

ROS 2 Is Distributed: Nodes on Two Computers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l10/distributed_ros.png
   :alt: Two solid gray rounded boxes, one above the other. The top one is labeled Computer 1: in the robotaxi, and holds a dashed box with a node named robotaxi. An arrow labeled publish goes down from robotaxi to a navy box that reads /robotaxi/position, and geometry_msgs/msg/Point. An arrow labeled subscribe goes down from the navy box into the bottom gray box, labeled Computer 2: at the dispatch office, to a node named dispatcher in a dashed box.
   :align: center
   :width: 45%

   A gray box is a computer, a dashed box a process.

ROS 2 is distributed: a node "can communicate with other nodes within the same process, in a different process, or on a different machine" (`Nodes <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Nodes.html>`_).

- ``robotaxi`` and ``dispatcher`` run on two computers with no change to their code. The computers share a network and a domain ID (`Discovery in Practice: Domain IDs and Your Network`_).
- Nodes can also share one process: less overhead, but one crash stops them all (`Composition <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Composition.html>`_).
- Inside a node, the code is the C++ of the first half of the course: classes, function calls and smart pointers.

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

The colcon Build Tool
^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: colcon
   :class: tip

   **colcon** (collective construction) is the command-line tool that builds the packages of a workspace. It works out the build order from their dependencies (`colcon documentation <https://colcon.readthedocs.io>`_).

.. admonition:: What colcon gives you
   :class: key-box

   - **Any language:** it builds C++ packages, Python packages and others.
   - **Parallel:** several packages build at the same time.
   - **Isolated:** each package builds in its own folder, so one cannot break another.
   - **Extensible:** plugins add build types.
   - **Cross-platform:** Linux, Windows and macOS.

**Install** it, then check it: ``colcon version-check`` prints one line per part, such as ``colcon-core 0.21.3: up-to-date``.

.. code-block:: bash

   sudo apt install python3-colcon-common-extensions
   colcon version-check

Build Operations
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 50 50
   :class: compact-table

   * - Command
     - What it builds
   * - ``colcon build``
     - Every package in ``src``
   * - ``colcon build --packages-select robotaxi_demo``
     - Only ``robotaxi_demo``
   * - ``colcon build --packages-up-to robotaxi_demo``
     - ``robotaxi_demo`` and the packages of the workspace it depends on
   * - ``colcon build --parallel-workers 4``
     - At most 4 packages at once (the default is the number of CPU cores)
   * - ``colcon build --symlink-install``
     - Installs links to files such as launch files instead of copies, so an edit to them needs no new build. C++ code still needs one.

Run every ``colcon`` command from the workspace's top folder, never from ``src``. In our workspace, ``colcon build`` ended with ``Summary: 1 package finished``.

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

   **A terminal that did not source the overlay** finds only the underlay. ``ros2 run robotaxi_demo robotaxi`` prints ``Package 'robotaxi_demo' not found``, even after a build that worked. Source the overlay again after each build that adds a package or an executable. In zsh, source ``setup.zsh``.

Create a Package: ros2 pkg create
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Definition: Package
   :class: tip

   A **package** is one folder of nodes, libraries, settings and launch files that does one thing, such as ``demo_nodes_cpp``. Every package has the same layout, so it is easy to build, share and reuse.

.. code-block:: bash
   :linenos:

   cd ~/ros2_ws/src
   ros2 pkg create robotaxi_demo --build-type ament_cmake \
     --dependencies rclcpp geometry_msgs

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
