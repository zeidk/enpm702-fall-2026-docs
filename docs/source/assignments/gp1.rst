.. _gp1:

==================================
GP1: ROS 2 Pub/Sub with Gazebo
==================================

Overview
--------

In this first Group Project, your team will bring the search-and-rescue robot concept into ROS 2. You will launch a mobile robot (e.g., TurtleBot3) in a Gazebo simulation of a disaster area, create publisher and subscriber nodes to drive it through a search pattern, define custom interfaces for reporting located victims, and configure the system with parameters and launch files. This assignment bridges the gap between the C++ fundamentals you practiced in the RWAs and real robotic systems built on ROS 2.

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Launch a mobile robot in Gazebo simulation.
#. Create ROS 2 nodes that inherit from ``rclcpp::Node``.
#. Implement publishers and subscribers for robot control.
#. Define and use custom message types for inter-node communication.
#. Configure nodes with parameters and YAML files.
#. Orchestrate multi-node systems with Python launch files.
#. Select and justify an appropriate executor for the system.

------------
Requirements
------------

.. dropdown:: Gazebo Setup
   :open:
   :color: primary

   **Goal:** spawn a mobile robot in a Gazebo world that represents a disaster/search area.

   **Steps:**

   #. Install (or confirm you have) the TurtleBot3 packages and Gazebo for your ROS 2 distribution. You may use another differential-drive robot if your team prefers, but TurtleBot3 is the supported baseline.
   #. Choose a world that represents a simple disaster/search area: scattered obstacles standing in for debris. You may use a stock world (e.g., the TurtleBot3 ``turtlebot3_world`` or ``turtlebot3_house``) or author a small custom ``.world`` file. Document your choice in the README.
   #. Launch the robot into that world so it spawns without errors and remains stable (it should not fall through the floor or drift on its own).

   **Acceptance criteria:**

   - The robot is visible and stationary in Gazebo after launch.
   - The expected topics are advertised. Verify with ``ros2 topic list`` that you see at least ``/cmd_vel``, ``/scan``, and ``/odom``.
   - You can confirm live data by running ``ros2 topic echo /scan`` (ranges update) and by publishing a manual ``/cmd_vel`` command to see the robot move.

.. dropdown:: Publisher Node
   :open:
   :color: primary

   **Goal:** drive the robot through a repeatable search pattern by publishing velocity commands.

   **Steps:**

   #. Create a node class that inherits from ``rclcpp::Node``.
   #. Create a publisher of type ``geometry_msgs::msg::Twist`` on the ``/cmd_vel`` topic.
   #. Create a wall timer whose period is derived from the ``publish_rate`` parameter (see the Parameters requirement). On each tick, the timer callback computes and publishes the next ``Twist`` command.
   #. Implement a predefined **search pattern** in the callback. Examples: a boustrophedon (back-and-forth) sweep, a spiral, or motion between a list of waypoints that covers the search area. The pattern must use ``linear_speed`` and ``angular_speed`` from parameters.

   The skeleton below shows the API calls and structure you are expected to use. Replace the ``TODO`` comments with your own implementation; it is not a complete solution.

   .. code-block:: cpp
      :caption: Illustrative publisher skeleton (adapt, do not copy verbatim)

      class SearchPublisher : public rclcpp::Node {
       public:
        SearchPublisher() : Node("search_publisher") {
          // TODO: declare parameters (linear_speed, angular_speed, publish_rate, ...)

          publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);

          // TODO: compute the timer period from the publish_rate parameter
          timer_ = this->create_wall_timer(
              std::chrono::milliseconds{/* TODO */},
              std::bind(&SearchPublisher::timer_callback, this));
        }

       private:
        void timer_callback() {
          geometry_msgs::msg::Twist cmd;
          // TODO: compute linear.x / angular.z for the current step of the search pattern
          // TODO: advance the pattern state (e.g., next waypoint or turn phase)
          publisher_->publish(cmd);
        }

        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
      };

   **Acceptance criteria:**

   - The robot moves on its own after launch (no manual ``/cmd_vel`` input needed).
   - The motion is a deliberate search pattern that covers the area, not random wandering.
   - Changing ``linear_speed`` / ``angular_speed`` parameters visibly changes how the robot drives.

.. dropdown:: Subscriber Node
   :open:
   :color: primary

   **Goal:** consume sensor data and detect debris (obstacles) and candidate victims from the laser scan.

   **Steps:**

   #. Create a node that subscribes to ``sensor_msgs::msg::LaserScan`` on ``/scan``. You may additionally subscribe to ``nav_msgs::msg::Odometry`` on ``/odom`` to record where a detection happened.
   #. In the scan callback, inspect the ``ranges`` array. Compute the minimum valid range (skip ``inf`` and ``nan`` values).
   #. Compare the closest reading against the ``obstacle_threshold`` parameter. When something is within the threshold, log a warning identifying roughly where it is (e.g., the bearing/index of the closest beam).
   #. Use this same detection logic to flag a **candidate victim** location, which feeds the custom message described in the Custom Interfaces requirement.

   The skeleton below shows the structure. Fill in the ``TODO`` comments with your own logic.

   .. code-block:: cpp
      :caption: Illustrative subscriber skeleton (adapt, do not copy verbatim)

      class SearchSubscriber : public rclcpp::Node {
       public:
        SearchSubscriber() : Node("search_subscriber") {
          // TODO: declare/get the obstacle_threshold parameter

          scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
              "/scan", 10,
              std::bind(&SearchSubscriber::scan_callback, this, std::placeholders::_1));
        }

       private:
        void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) {
          // TODO: iterate msg->ranges, ignore inf/nan, find the closest valid range
          // TODO: if closest < obstacle_threshold, RCLCPP_WARN with the bearing
          // TODO: when a detection qualifies as a candidate victim, trigger a VictimReport
        }

        rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
      };

   **Acceptance criteria:**

   - Driving the robot toward an obstacle produces a warning log when it crosses ``obstacle_threshold``.
   - The log identifies the direction/bearing of the closest object, not just that "something" is near.
   - ``inf`` / ``nan`` scan values are handled and do not crash the node or produce false detections.

.. dropdown:: Custom Interfaces
   :open:
   :color: primary

   **Goal:** define and use a custom message that reports a located victim from the search robot to a command post.

   **Steps:**

   #. Create (or reuse) an interfaces package and define at least one custom message, ``VictimReport.msg``. The fields below are a concrete **example** you should adapt to your design (add or rename fields as needed, e.g., a ``std_msgs/Header`` for timestamping).
   #. Register the message: add the ``.msg`` file and the ``rosidl_default_generators`` / dependency entries to ``CMakeLists.txt`` and ``package.xml`` so the type builds and is importable.
   #. Have the subscriber node (the one processing ``/scan``) publish a ``VictimReport`` on a custom topic (e.g., ``/victim_reports``) whenever it identifies a candidate location.
   #. Create a separate node (e.g., a command-post node) that subscribes to that topic and logs each received report in a human-readable form.

   .. code-block:: text
      :caption: Example VictimReport.msg (adapt the fields to your design)

      int32 victim_id
      float64 x
      float64 y
      float64 confidence
      string detected_by

   **Acceptance criteria:**

   - ``ros2 interface show <pkg>/msg/VictimReport`` displays your message.
   - When the robot identifies a candidate, a message appears on the custom topic (verify with ``ros2 topic echo``).
   - The command-post node logs each report with its fields (id, location, confidence, etc.).

.. dropdown:: Parameters
   :open:
   :color: primary

   **Goal:** make the system tunable without recompiling by exposing key values as ROS 2 parameters loaded from YAML.

   **Steps:**

   #. In each node, declare the parameters it needs with ``this->declare_parameter()`` (provide a sensible default for each), and read them with ``this->get_parameter()``. At a minimum, expose across the system:

      - ``robot_name``
      - ``linear_speed``
      - ``angular_speed``
      - ``publish_rate``
      - ``obstacle_threshold``

   #. Use the parameter values where they matter: ``publish_rate`` sets the timer period, ``linear_speed`` / ``angular_speed`` scale the ``Twist`` commands, and ``obstacle_threshold`` controls obstacle detection.
   #. Provide a YAML configuration file that sets all parameters, keyed by node name. The block below is an **example** to adapt to your node names and values.

   .. code-block:: yaml
      :caption: Example params.yaml (adapt node names and values to your package)

      search_publisher:
        ros__parameters:
          robot_name: "rescue_bot"
          linear_speed: 0.5
          angular_speed: 1.0
          publish_rate: 10.0
          obstacle_threshold: 0.5

   **Acceptance criteria:**

   - ``ros2 param list`` shows the declared parameters on the running nodes.
   - Editing a value in the YAML file and relaunching changes the robot's behavior (e.g., a larger ``linear_speed`` makes it drive faster) with no code changes.
   - Nodes start with working defaults even if the YAML file is not passed.

.. dropdown:: Launch File
   :open:
   :color: primary

   **Goal:** bring up the entire system (simulation plus your nodes) with a single command.

   **Steps:**

   #. Write a Python launch file (``launch/*.launch.py``) that returns a ``LaunchDescription``.
   #. Include the Gazebo launch with the robot model and world (use ``IncludeLaunchDescription`` to pull in the existing Gazebo/TurtleBot3 launch file rather than reimplementing it).
   #. Add a ``Node`` action for each of your nodes (publisher, subscriber, command post), and pass the YAML configuration file to them via the ``parameters`` argument.
   #. Make the path to the YAML file robust by resolving it from the installed package share directory (e.g., with ``get_package_share_directory``), not a hard-coded absolute path.

   **Acceptance criteria:**

   - A single ``ros2 launch`` command starts Gazebo with the robot and all of your nodes.
   - The nodes come up already configured from the YAML file (confirm with ``ros2 param get``).
   - The robot begins its search pattern and detections appear without any extra manual steps.

.. dropdown:: Executors
   :open:
   :color: primary

   **Goal:** run your nodes under a deliberately chosen executor and justify the choice.

   **Steps:**

   #. Decide whether your system needs a single-threaded or a multi-threaded executor. Consider how many callbacks must run, whether any are long-running, and whether callbacks must run concurrently (callback groups).
   #. Set up the chosen executor in your ``main`` (e.g., create the executor, add your node(s), then spin), rather than relying on a bare ``rclcpp::spin(node)`` if your design calls for more.
   #. Document the decision in the README.

   **Acceptance criteria:**

   - The system runs under the executor you selected.
   - The README contains a brief written justification explaining **why** that executor fits this system (reference your callbacks and concurrency needs).

------------
Deliverables
------------

- ROS 2 package(s) with all source code.
- Custom interface definitions (``.msg`` files and ``CMakeLists.txt`` / ``package.xml`` changes).
- Launch file(s) and YAML configuration file.
- ``README.md`` with build and run instructions.
- Short video demo (1-2 minutes) showing the robot searching the area in Gazebo.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - Functionality (robot searches, pub/sub works, obstacle detection)
     - 40%
   * - Custom Interfaces (message definition, publishing, subscribing)
     - 15%
   * - Parameters and Launch File (YAML config, launch orchestration)
     - 15%
   * - Code Quality (naming conventions, uniform initialization, ``'\n'`` usage, structure)
     - 15%
   * - Documentation and Demo (README clarity, video quality)
     - 15%
