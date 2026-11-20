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

Its ``rosbot_sim`` folder holds the simulation. Install and build it with the steps of the :doc:`ROSbot Simulation </setup/rosbot_simulation>` page. Its last step starts Gazebo with the ROSbot, which needs about 40 s the first time:

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py

Then build this lecture's package, ``L12/l12_rosbot``, from ``~/ros2_ws``:

.. code-block:: bash

   colcon build --packages-select l12_rosbot
   source install/setup.bash

In class, I do not explain the shell commands: you learned them in the shell exercises on ReadTheDocs, which every student was asked to do.

Code for This Lecture
---------------------

The ``L12`` folder of the course repository holds one package, ``l12_rosbot``. It has the two controller nodes of this lecture, a configuration folder and a launch folder:

.. code-block:: text

   enpm702-fall-2026-ros/L12/l12_rosbot/
   ├── CMakeLists.txt
   ├── package.xml
   ├── config/
   │   ├── controllers.yaml
   │   └── low_gain.yaml
   ├── include/l12_rosbot/
   │   ├── geometry.hpp
   │   ├── heading_controller_node.hpp
   │   └── distance_controller_node.hpp
   ├── launch/
   │   ├── heading_launch.py
   │   └── distance_launch.py
   └── src/
       ├── heading_controller_main.cpp
       ├── heading_controller_node.cpp
       ├── distance_controller_main.cpp
       └── distance_controller_node.cpp

The code grows in four stages, one commit each. The lecture quotes the stage a listing belongs to, because the line numbers change from stage to stage:

.. list-table::
   :header-rows: 1
   :widths: 10 14 76

   * - Stage
     - Commit
     - What it adds
   * - 1
     - ``8bd21e7``
     - The two controllers, with the gains and limits as constants in the code.
   * - 2
     - ``9434e00``
     - The controllers read their gains and limits from parameters, once, in the constructor.
   * - 3
     - ``e7048f4``
     - The ``config`` and ``launch`` folders: a parameter file and two launch files.
   * - 4
     - ``94d4d64``
     - A parameter callback in ``heading_controller_node``. This is the final code of the package.

To read a stage, check out its commit in the course repository. The listings below name their stage; a listing that says "stage 4" matches the files you get from the repository.

The ROSbot in Gazebo
--------------------

The previous lecture set up launch files, executors and custom interfaces for the robotaxi. This lecture moves to a simulated robot, the one GP2 uses. **Gazebo** is a simulator: it runs a robot and its sensors in a virtual world.

Gazebo and the ROSbot
^^^^^^^^^^^^^^^^^^^^^

Gazebo computes the physics of the robot and the readings of its sensors. The ROSbot is the robot you program in Gazebo for the rest of the course.

What Gazebo Simulates
"""""""""""""""""""""

Gazebo runs a robot in a virtual world, so you can test your nodes without a real robot. It computes three things:

- **Physics**: the wheels push the robot over the floor, and the walls stop it.
- **Sensors**: what each sensor would read in that world. The simulation publishes the readings on ROS topics.
- **The world**: walls, doors and objects, read from a world file.

Why you use a simulator in this course:

- The simulation uses Husarion's own ROSbot packages, with the real robot's shape, wheels and sensor positions.
- A crash costs nothing, and every student runs the same robot in the same world.

Gazebo on Its Own: gz sim
"""""""""""""""""""""""""

Gazebo is a program of its own, not a ROS node. ROS 2 Jazzy installs it (Gazebo Harmonic), and ``gz sim`` opens a world file. ``shapes.sdf`` is a demo world that comes with Gazebo:

.. code-block:: bash

   gz sim shapes.sdf          # with a window; press Play to start
   gz sim -s -r shapes.sdf    # no window (-s), running at start (-r)

With that world running, Gazebo has its own list of topics, and ROS has another:

.. code-block:: bash

   gz topic -l

.. code-block:: text

   /clock
   /stats
   /world/shapes/pose/info
   /world/shapes/state
   [...]

.. code-block:: bash

   ros2 topic list

.. code-block:: text

   /parameter_events
   /rosout

.. admonition:: Conclusion
   :class: important

   Gazebo's topics are not ROS topics. A bridge node, from the package ``ros_gz_bridge``, copies the ones you need between the two.

The Husarion ROSbot
"""""""""""""""""""

The ROSbot is a small research robot with four wheels. The two wheels on each side turn together, so the robot turns by driving its left and right sides at different speeds: a **differential drive**.

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - Part
     - What it is
   * - Body
     - 0.197 m long, 0.150 m wide, 0.080 m high
   * - Speed limits
     - 1.0 m/s forward, 3.14 rad/s turning
   * - Lidar
     - 3000 beams over a full circle, 0.05 m to 30 m
   * - Logical camera
     - Lists the objects in front of the robot, with the pose of each one
   * - IMU
     - Measures the robot's orientation, turn rate and acceleration
   * - Odometry
     - The robot's pose, computed from the wheels and the IMU

Command the ROSbot and Read Its Pose
"""""""""""""""""""""""""""""""""""""

Your nodes publish commands on ``/cmd_vel`` and read the robot's pose from ``/odometry/filtered``:

.. list-table::
   :header-rows: 1
   :widths: 29 29 42

   * - Topic
     - Message
     - Fields you use
   * - ``/cmd_vel``
     - ``geometry_msgs/msg/TwistStamped``
     - ``twist.linear.x``: forward speed, m/s; ``twist.angular.z``: turn rate, rad/s, positive turns left
   * - ``/odometry/filtered``
     - ``nav_msgs/msg/Odometry``
     - ``pose.pose.position``: x and y in m; ``pose.pose.orientation``: a quaternion, which gives the yaw

Start the world with the robot in it, or the robot alone on an empty floor:

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py
   ros2 launch gp2_bringup gp2_sim.launch.py world:=empty

.. note::

   The ROSbot can also take mecanum wheels, which drive sideways too (``twist.linear.y``). Husarion's packages have a ``mecanum`` option; the course simulation removed its controller and does not offer it.

The Patrol World
""""""""""""""""

The patrol world is one floor, 20 m by 10 m, with walls 1 m high. The robot starts at the origin and faces east, along +x.

.. figure:: /_static/images/rosbot/patrol_world.png
   :alt: Top view of the patrol world from Gazebo, with x in meters along the bottom and y in meters along the left. A long hall runs along the bottom with the small dark robot at the origin, tag 5, and four blue discs, tags 1 to 4. Two rooms lie above the hall, joined to it by two doorways in the wall at y equals 2: the left doorway, tag 11, is open, and the right one, tag 10, has a red panel. A purple disc, tag 9, a small orange cylinder, tag 6, a green cylinder with a round head, tag 8, and a brown box, tag 7, lie in the hall.
   :align: center
   :width: 90%

   The patrol world. Tags 1 to 4 are checkpoints, 5 is the robot's start, 6 to 9 are objects, 10 is a closed door and 11 is an open door.

Launch the Simulation
^^^^^^^^^^^^^^^^^^^^^

One launch file starts Gazebo, the world and the ROSbot. You start it once, then use it from other terminals.

Start the Simulation
""""""""""""""""""""

One command starts Gazebo, the patrol world and the ROSbot:

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py

- The first start takes about 40 s, while Gazebo loads its models. Wait before you check anything. A later start took under 10 s on the course computer.
- Check it from a second terminal: ``ros2 topic list`` prints 31 topics.

.. note::

   Keep the launch terminal open: the simulation runs until you stop it. Use other terminals for everything else.

What the Launch File Starts
"""""""""""""""""""""""""""

``ros2 launch gp2_bringup gp2_sim.launch.py`` starts 10 programs. It also spawns the ROSbot into the world, a step that then ends.

.. list-table::
   :header-rows: 1
   :widths: 41 59

   * - Program
     - What it does
   * - ``gz sim`` with ``patrol.sdf``
     - Gazebo and the patrol world. ``differential_drive_controller`` runs inside it and reads ``/cmd_vel``.
   * - 5 × ``parameter_bridge``
     - Bridges from ``ros_gz_bridge``: they copy topics between Gazebo and ROS, such as the lidar's and the cameras'.
   * - ``robot_state_publisher``
     - Publishes the robot's description and the frames of its parts.
   * - ``ekf``
     - Combines the wheels and the IMU into ``/odometry/filtered``.
   * - ``laser_filters``
     - Publishes ``/scan_filtered``: the scan without the beams that hit the robot.
   * - ``static_transform_publisher``
     - Places the logical camera's frame on the robot.

Launch Arguments
""""""""""""""""

The launch file takes launch arguments, set on the command line as ``name:=value``, the same form as ``with_dispatcher:=false`` in the previous lecture. The main ones, all optional:

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Argument
     - Default
     - What it does
   * - ``gui``
     - ``true``
     - ``false`` runs Gazebo without a window, for a slow computer.
   * - ``world``
     - ``patrol``
     - ``patrol``, ``patrol_doors_swapped`` or ``empty``.
   * - ``rviz``
     - ``false``
     - ``true`` also opens RViz.
   * - ``x``, ``y``, ``yaw``
     - ``0.0``
     - The robot's start pose, in meters and radians.

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py gui:=false rviz:=true

To stop the simulation, press :kbd:`Ctrl+C` in the launch terminal.

RViz: What ROS Sees
"""""""""""""""""""

Gazebo draws the simulated world. **RViz** is a ROS node that draws what the topics carry, in one **fixed frame**: the robot model, its frames, the lidar's ranges. Two ways to start it:

1. With the simulation, using the ROSbot's RViz configuration:

   .. code-block:: bash

      ros2 launch gp2_bringup gp2_sim.launch.py rviz:=true

   Fixed frame ``odom``; the robot model, its frames (TF), the lidar (``/scan_filtered``) and the camera image.

2. By hand, in a second terminal:

   .. code-block:: bash

      ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true

   Set **Fixed Frame** to ``odom``, then **Add** the displays: RobotModel (topic ``/robot_description``), TF and LaserScan (``/scan_filtered``).

``use_sim_time`` gives RViz Gazebo's clock: :ref:`l12-use-sim-time` explains it.

Topics and Driving
^^^^^^^^^^^^^^^^^^

You control the ROSbot with topics. This subsection lists them and drives the robot from a terminal.

The Topics You Use
""""""""""""""""""

Of the 31 topics, your nodes use these:

.. list-table::
   :header-rows: 1
   :widths: 29 38 33

   * - Topic
     - Type
     - What it carries
   * - ``/cmd_vel``
     - ``geometry_msgs/msg/TwistStamped``
     - The velocity command. You publish it.
   * - ``/odometry/filtered``
     - ``nav_msgs/msg/Odometry``
     - The robot's pose, about 20 times per second.
   * - ``/scan``
     - ``sensor_msgs/msg/LaserScan``
     - The lidar's ranges.
   * - ``/logical_camera``
     - ``ros_gz_interfaces/msg/LogicalCameraImage``
     - The objects in front of the robot.
   * - ``/tf``, ``/tf_static``
     - ``tf2_msgs/msg/TFMessage``
     - The robot's frames, next class.
   * - ``/clock``
     - ``rosgraph_msgs/msg/Clock``
     - The simulation time.

.. note::

   ``/cmd_vel`` takes a ``TwistStamped``: a ``Twist`` with a header that holds a time stamp. The two types do not connect, so a node that publishes ``Twist`` on ``/cmd_vel`` cannot move the robot.

Read the Position
"""""""""""""""""

The robot's position is one field of the odometry message. Print it once:

.. code-block:: bash

   ros2 topic echo --once /odometry/filtered --field pose.pose.position

.. code-block:: text

   x: -7.400765781802631e-18
   y: 3.202344653318229e-21
   z: 0.0
   ---

- ``--once`` prints one message and exits. ``--field`` prints only that part of the message.
- At the start, the robot is at the origin: -7.4 × 10\ :sup:`-18` m and 3.2 × 10\ :sup:`-21` m are rounding errors, not distances.
- The fields of ``Odometry`` are in the :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` reading.

Drive Forward and Turn
""""""""""""""""""""""

``ros2 topic pub`` publishes one message again and again; ``-r 10`` sends it 10 times per second. Drive forward at 0.2 m/s:

.. code-block:: bash

   ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/TwistStamped \
     "{twist: {linear: {x: 0.2}}}"

Turn on the spot at 0.5 rad/s:

.. code-block:: bash

   ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/TwistStamped \
     "{twist: {angular: {z: 0.5}}}"

- ``linear.x`` is the forward speed in m/s. ``angular.z`` is the turn rate in rad/s; a positive value turns left.
- :kbd:`Ctrl+C` stops the command. The robot then stops by itself: its controller brakes when no command arrives for 0.5 s.

Drive with the Keyboard
"""""""""""""""""""""""

The node ``teleop_twist_keyboard`` turns key presses into velocity commands:

.. code-block:: bash

   ros2 run teleop_twist_keyboard teleop_twist_keyboard \
     --ros-args -p stamped:=true

.. code-block:: text

   Moving around:
      u    i    o
      j    k    l
      m    ,    .

- ``i`` drives forward, ``,`` drives backward, ``j`` and ``l`` turn on the spot, and ``k`` stops.
- ``-p stamped:=true`` sets a parameter of the node, so it publishes ``TwistStamped``. The Parameters section explains them.
- The keys work only while the teleop terminal has the focus.

Proportional Control
--------------------

The last section drove the ROSbot by hand with ``ros2 topic pub``. This section replaces your hand with a node: it reads where the ROSbot is and publishes velocity commands that turn it to a heading or drive it a distance.

From a Terminal Command to a Node
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With ``ros2 topic pub``, you chose the command and you watched the robot. A controller node does both: every 50 ms, it reads where the robot is and publishes a command.

- ``ekf`` publishes the robot's pose, computed from the wheels and the IMU.
- ``differential_drive_controller`` turns each ``/cmd_vel`` command into wheel speeds.
- You write the node in the middle. The graph shows only the nodes it exchanges data with.

.. figure:: /_static/images/l12/control_graph.png
   :alt: ROS graph drawn top to bottom. A rounded box ekf has an arrow down to a rounded box heading_controller_node, labeled /odometry/filtered and nav_msgs/msg/Odometry. From heading_controller_node, an arrow down to a rounded box differential_drive_controller is labeled /cmd_vel and geometry_msgs/msg/TwistStamped.
   :align: center
   :width: 60%

   ``heading_controller_node`` receives the pose on ``/odometry/filtered`` and publishes the command on ``/cmd_vel``.

One Error, One Gain
^^^^^^^^^^^^^^^^^^^

A proportional controller sets a speed in proportion to the error that is left. One gain sets how strongly it reacts.

What a Controller Does
""""""""""""""""""""""

A controller brings one measured value to a target. For a turn, the value is the robot's heading, and the target is the heading you want. It repeats four steps:

1. **Measure**: read the heading from the odometry.
2. **Compare**: compute the **error**, the target minus the heading.
3. **Command**: publish a turn rate computed from the error.
4. **Repeat** every 50 ms. The robot has turned a little, so the next error is smaller.

The loop stops when the error is smaller than a **tolerance**, a margin you choose. Without a tolerance, the loop would wait for an error of exactly 0, which the odometry never reads.

The Error of a Turn
"""""""""""""""""""

The error of a turn is the angle left to turn, the short way. A positive error means turn left (counterclockwise), a negative one, turn right. Headings are in radians, from -π to π.

Example: the robot faces 3.122 rad (179°), and the target is -90°, which is -1.571 rad.

1. Target minus heading: -1.571 - 3.122 = -4.693 rad. That is a turn right of 269°.
2. Turning left is shorter. Add one full turn, 2π = 6.283 rad: -4.693 + 6.283 = 1.590 rad, a turn left of 91°.
3. The error is 1.590 rad: the robot turns left 91°, past the 180° heading.

.. admonition:: Conclusion
   :class: important

   The error is the target minus the heading, moved into -π to π by adding or removing full turns.

Yaw from the Odometry's Quaternion
""""""""""""""""""""""""""""""""""

The odometry gives the robot's orientation as a **quaternion**, four numbers ``x``, ``y``, ``z`` and ``w``. The controller needs one angle, the **yaw**: the heading, counterclockwise from +x. Lines 15 to 24 of ``include/l12_rosbot/geometry.hpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 15

   inline double yaw_from_quaternion(
       const geometry_msgs::msg::Quaternion &orientation) {
       const double siny_cosp{
           2.0 * (orientation.w * orientation.z +
                  orientation.x * orientation.y)};
       const double cosy_cosp{
           1.0 - 2.0 * (orientation.y * orientation.y +
                        orientation.z * orientation.z)};
       return std::atan2(siny_cosp, cosy_cosp);
   }

- The same file holds ``angle_difference``, which computes the error of the last section.
- The :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` reading explains the quaternion and this formula.

The Proportional Control Law
""""""""""""""""""""""""""""

A **proportional controller** commands a turn rate proportional to the error: the command is the error times a number you choose, the **gain** :math:`k_p`. Then it limits the command to a maximum speed. With :math:`k_p` = 1.5 (rad/s per rad of error) and a limit of 1.0 rad/s:

1. At the start, the error is 1.569 rad: 1.5 × 1.569 = 2.35 rad/s.
2. That is above the limit, so the controller sends 1.0 rad/s.
3. Later, the error is 0.5848 rad: 1.5 × 0.5848 = 0.877 rad/s, under the limit, so it is sent as it is.
4. Near the end, the error is 0.092 rad: 1.5 × 0.092 = 0.138 rad/s.

.. admonition:: Conclusion
   :class: important

   The command shrinks with the error, so the robot slows down as it nears the target heading.

Turn to a Heading
^^^^^^^^^^^^^^^^^

You write ``heading_controller_node``, which turns the ROSbot on the spot to one heading. Its gain and limits are constants in the code, for now. The listings of this subsection are from stage 1 (commit ``8bd21e7``).

Step 1: Create the Files
""""""""""""""""""""""""

The package ``l12_rosbot`` is provided, in the ``L12`` folder of the course repository. It was created with ``ros2 pkg create``, with the dependencies ``rclcpp``, ``geometry_msgs`` and ``nav_msgs``. From ``l12_rosbot``, the node needs four files:

.. code-block:: bash

   cd include/l12_rosbot
   touch geometry.hpp
   touch heading_controller_node.hpp
   cd ../../src
   touch heading_controller_node.cpp
   touch heading_controller_main.cpp

The package after Step 1:

.. code-block:: text

   l12_rosbot/
   ├── include/
   │   └── l12_rosbot/
   │       ├── geometry.hpp
   │       └── heading_controller_node.hpp
   ├── src/
   │   ├── heading_controller_main.cpp
   │   └── heading_controller_node.cpp
   ├── CMakeLists.txt
   └── package.xml

Step 2: Write the Class
"""""""""""""""""""""""

Lines 15 to 30 of ``include/l12_rosbot/heading_controller_node.hpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 15
   :emphasize-lines: 5, 10, 13

   class HeadingControllerNode : public rclcpp::Node {
     public:
       HeadingControllerNode()
           : rclcpp::Node{"heading_controller_node"},
             odometry_subscription_{
                 create_subscription<nav_msgs::msg::Odometry>(
                     "odometry/filtered", 10,
                     std::bind(&HeadingControllerNode::odometry_callback,
                               this, std::placeholders::_1))},
             command_publisher_{
                 create_publisher<geometry_msgs::msg::TwistStamped>(
                     "cmd_vel", 10)},
             control_timer_{create_wall_timer(
                 std::chrono::milliseconds{50},
                 std::bind(&HeadingControllerNode::control_callback,
                           this))} {}

- Line 19: odometry in.
- Line 24: commands out.
- Line 27: the 50 ms timer.

Step 2: Write the Class, Its Members
""""""""""""""""""""""""""""""""""""

Lines 32 to 43 of the same file:

.. code-block:: cpp
   :linenos:
   :lineno-start: 32
   :emphasize-lines: 10, 11

     private:
       void odometry_callback(const nav_msgs::msg::Odometry &msg);
       void control_callback();
       void publish_command(double angular_speed);
       rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr
           odometry_subscription_;
       rclcpp::Publisher<geometry_msgs::msg::TwistStamped>::SharedPtr
           command_publisher_;
       rclcpp::TimerBase::SharedPtr control_timer_;
       double yaw_{0.0};          // the robot's heading, in rad
       bool has_odometry_{false}; // true once odometry arrived
   };

- Lines 41 and 42: ``odometry_callback`` writes them, and ``control_callback`` reads them. The two callbacks never call each other.
- ``has_odometry_`` keeps the controller from acting on a heading of 0 before the first message arrives.

Step 2: Write the Constants and odometry_callback
"""""""""""""""""""""""""""""""""""""""""""""""""

Lines 11 to 23 of ``src/heading_controller_node.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 11
   :emphasize-lines: 3-6, 11

   namespace {
   // Gains and limits, as constants in the code for now.
   constexpr double target_yaw_deg{90.0};    // heading to reach, degrees
   constexpr double kp_angular{1.5};         // gain: rad/s per rad
   constexpr double max_angular_rps{1.0};    // speed limit, rad/s
   constexpr double yaw_tolerance_rad{0.02}; // stop within this, rad
   } // namespace

   void HeadingControllerNode::odometry_callback(
       const nav_msgs::msg::Odometry &msg) {
       yaw_ = yaw_from_quaternion(msg.pose.pose.orientation);
       has_odometry_ = true;
   }

- Lines 13 to 16: the target, the gain, the limit and the tolerance. The unnamed namespace keeps them inside this file.
- Line 21: the helper of the yaw section turns the quaternion into the yaw.

Step 2: Write control_callback, the Error and the Stop
""""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 25 to 41 of the same file:

.. code-block:: cpp
   :linenos:
   :lineno-start: 25
   :emphasize-lines: 9-12

   void HeadingControllerNode::control_callback() {
       if (!has_odometry_) {
           return; // no heading yet
       }
       const double target_yaw{
           target_yaw_deg * std::numbers::pi / 180.0};
       // The error: the angle left to turn, the short way.
       // Positive: turn left.
       const double error{angle_difference(target_yaw, yaw_)};
       if (std::abs(error) < yaw_tolerance_rad) {
           publish_command(0.0);
           control_timer_->cancel(); // done: no more control_callback
           RCLCPP_INFO_STREAM(get_logger(),
                              "heading reached: yaw " << yaw_
                                  << " rad, error " << error << " rad");
           return;
       }

- Line 33: the error.
- Lines 34 to 36: within the tolerance, stop for good.

Step 2: Write control_callback, the Command
"""""""""""""""""""""""""""""""""""""""""""

Lines 43 to 57 of the same file:

.. code-block:: cpp
   :linenos:
   :lineno-start: 43
   :emphasize-lines: 1-3, 13

       const double command{
           std::clamp(kp_angular * error, -max_angular_rps,
                      max_angular_rps)};
       publish_command(command);
       RCLCPP_INFO_STREAM_THROTTLE(
           get_logger(), *get_clock(), 500,
           "error " << error << " rad, command " << command << " rad/s");
   }

   void HeadingControllerNode::publish_command(double angular_speed) {
       geometry_msgs::msg::TwistStamped command{};
       command.header.stamp = now();
       command.twist.angular.z = angular_speed;
       command_publisher_->publish(command);
   }

- Lines 43 to 45: the law of the control-law section, limited by ``std::clamp``.
- Line 55: only ``angular.z`` is set, so the robot turns on the spot.

Step 3: Install the Executable
""""""""""""""""""""""""""""""

``heading_controller_main.cpp`` is the usual ``main``: it creates the node and spins it. In ``CMakeLists.txt``, lines 39 to 43 build the executable:

.. code-block:: cmake
   :linenos:
   :lineno-start: 39

   # Turns the ROSbot on the spot to a heading.
   add_executable(heading_controller_exe
     src/heading_controller_main.cpp src/heading_controller_node.cpp)
   ament_target_dependencies(heading_controller_exe
     rclcpp geometry_msgs nav_msgs)

Lines 53 and 54 install it, with the executable of the next subsection:

.. code-block:: cmake
   :linenos:
   :lineno-start: 53

   install(TARGETS heading_controller_exe distance_controller_exe
     DESTINATION lib/${PROJECT_NAME})

``nav_msgs`` holds the ``Odometry`` message. ``ros2 pkg create`` already added it to ``package.xml`` and to ``find_package``.

Step 4: Build and Run in Gazebo
"""""""""""""""""""""""""""""""

With the simulation running:

.. code-block:: bash

   colcon build --packages-select l12_rosbot
   source install/setup.bash
   ros2 run l12_rosbot heading_controller_exe

.. code-block:: text

   [...]: error 1.56886 rad, command 1 rad/s
   [...]: error 1.20115 rad, command 1 rad/s
   [...]: error 0.58477 rad, command 0.877155 rad/s
   [...]: error 0.24099 rad, command 0.361486 rad/s
   [...]: error 0.0918069 rad, command 0.13771 rad/s
   [...]: heading reached: yaw 1.55212 rad, error 0.0186762 rad

- ``[...]`` is ``[INFO]``, the time and the node's name. The throttled log prints about every 0.5 s.
- The turn took 2.65 s (time stamps 1795157077.809 to 1795157080.459). The command stays at 1.0 rad/s until the error is under 1.0 / 1.5 = 0.67 rad.

.. admonition:: Conclusion
   :class: important

   The robot turned from 0 to 1.552 rad (88.9°) by itself, and stopped within the 0.02 rad tolerance.

Drive a Distance
^^^^^^^^^^^^^^^^

``distance_controller_node`` drives the ROSbot straight ahead for one distance. Only the error changes: the distance left to drive.

The Error of a Drive
""""""""""""""""""""

The same four steps; only the measured value changes, to the distance driven since the start. Lines 16 to 25 of ``src/distance_controller_node.cpp`` (stage 1):

.. code-block:: cpp
   :linenos:
   :lineno-start: 16
   :emphasize-lines: 5-7

   void DistanceControllerNode::odometry_callback(
       const nav_msgs::msg::Odometry &msg) {
       x_ = msg.pose.pose.position.x;
       y_ = msg.pose.pose.position.y;
       if (!has_odometry_) {
           start_x_ = x_; // the first message gives the start
           start_y_ = y_;
           has_odometry_ = true;
       }
   }

Lines 31 to 33, in ``control_callback``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 31

   const double driven{std::hypot(x_ - start_x_, y_ - start_y_)};
   // The error: the distance left to drive.
   const double error{target_distance_m - driven};

- Line 31: ``std::hypot`` gives :math:`\sqrt{\Delta x^2 + \Delta y^2}`, the distance from the start.

The Same Law on the Forward Speed
"""""""""""""""""""""""""""""""""

The constants are a 1.0 m target, a gain of 0.8 (m/s per m of error), a limit of 0.5 m/s and a tolerance of 0.02 m. Lines 43 to 45 and 52 to 57 of the same file:

.. code-block:: cpp
   :linenos:
   :lineno-start: 43

   const double command{
       std::clamp(kp_linear * error, -max_linear_mps,
                  max_linear_mps)};

.. code-block:: cpp
   :linenos:
   :lineno-start: 52
   :emphasize-lines: 4

   void DistanceControllerNode::publish_command(double linear_speed) {
       geometry_msgs::msg::TwistStamped command{};
       command.header.stamp = now();
       command.twist.linear.x = linear_speed;
       command_publisher_->publish(command);
   }

- Line 55: only ``linear.x`` is set, so the robot drives straight ahead and does not turn.
- The stop within the tolerance, the timer and the log are the same as in ``heading_controller_node``.

Run the Distance Controller
"""""""""""""""""""""""""""

``ros2 run l12_rosbot distance_controller_exe``, with the robot facing +y (``[...]`` is the cut prefix):

.. code-block:: text

   [...]: error 1 m, command 0.5 m/s
   [...]: error 0.627905 m, command 0.5 m/s
   [...]: error 0.406843 m, command 0.325475 m/s
   [...]: error 0.252548 m, command 0.202038 m/s
   [...]: error 0.159472 m, command 0.127577 m/s
   [...]: error 0.103942 m, command 0.0831533 m/s
   [...]: distance reached: driven 0.980244 m, error 0.0197556 m

- The command stays at the 0.5 m/s limit while the error is over 0.5 / 0.8 = 0.625 m.
- After that, from one line to the next (about 0.55 s), the error falls to about 63 % of its value: 0.407, 0.253, 0.159, 0.104 m.
- The whole drive took 5.25 s (time stamps 1795157115.823 to 1795157121.073). The last 0.10 m alone took 2.0 s.

.. admonition:: Conclusion
   :class: important

   Near the target the command is small, so a smaller tolerance costs more time.

Proportional Control: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Compute an error: the angle left to turn, the short way, or the distance left to drive.
   - Turn the error into a command with a gain and a limit: ``std::clamp(kp * error, -max, max)``.
   - Stop within a tolerance, and cancel the timer.
   - Run a controller node in Gazebo: odometry in, ``TwistStamped`` out.

The gains and limits of these controllers are constants in the code. They become parameters in the next section.

Parameters
----------

The controller keeps its gains and limits as numbers in its code, so each change needs a rebuild. A **parameter** is a named setting of a node that you change without recompiling.

Why the Controller Needs Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The heading controller of the last section has four numbers in its code: the target (90°), the gain (1.5), the speed limit (1.0 rad/s) and the tolerance (0.02 rad). Each one is a choice, and each one changes with the job:

- **Another target.** Turning to 180° instead of 90° means editing the ``.cpp`` and building again.
- **Tuning.** A good gain is found by trying values: later in this section, a gain of 0.5 takes 6.4 s for a 90° turn, and 1.5 takes 2.7 s. With constants, every try is edit, build, run.
- **Another robot or world.** GP2 runs the same controller against the stand-in robot and in Gazebo, tuned for each: ``params_stand_in.yaml`` and ``params_gazebo.yaml``.

.. admonition:: Conclusion
   :class: important

   Values that change with the task, the robot or the world belong outside the code: in parameters, which you set when the node starts or while it runs.

What a Parameter Holds
^^^^^^^^^^^^^^^^^^^^^^

A parameter belongs to one node and has a name, a type and a value. Its type is one of nine, from ``rcl_interfaces/msg/ParameterType``. In C++, a ``rclcpp::Parameter`` gives its value with an ``as_...()`` function:

.. list-table::
   :header-rows: 1
   :widths: 24 44 32

   * - Type
     - C++ value
     - In this lecture
   * - bool
     - ``bool``, ``as_bool()``
     - ``use_sim_time``
   * - integer
     - ``int64_t``, ``as_int()``
     -
   * - double
     - ``double``, ``as_double()``
     - ``kp_angular``
   * - string
     - ``std::string``, ``as_string()``
     -
   * - double array
     - ``std::vector<double>``, ``as_double_array()``
     - ``target_headings_deg``
   * - other arrays
     - of bytes, bools, integers or strings
     -

Each ``as_...()`` function throws an exception when the parameter has another type.

Declare and Read
^^^^^^^^^^^^^^^^

A node must declare a parameter before it uses it. You declare each one with a type and a default value, and then read its value. The listings of this subsection are from stage 2 (commit ``9434e00``), unless they say stage 4.

Declare, Then Read
""""""""""""""""""

Lines 35 to 49 of ``heading_controller_node.hpp``, the end of the constructor (in the stage 4 file, the same code is on lines 39 to 53):

.. code-block:: cpp
   :linenos:
   :lineno-start: 35
   :emphasize-lines: 2, 5, 11

   // Declare each parameter with its default value.
   declare_parameter(
       "target_headings_deg",
       std::vector<double>{90.0, 180.0, -90.0, 0.0});
   declare_parameter("kp_angular", 1.5);
   declare_parameter("max_angular_rps", 1.0);
   declare_parameter("yaw_tolerance_rad", 0.02);
   // Read each value once, into a data member.
   target_headings_deg_ =
       get_parameter("target_headings_deg").as_double_array();
   kp_angular_ = get_parameter("kp_angular").as_double();
   max_angular_rps_ =
       get_parameter("max_angular_rps").as_double();
   yaw_tolerance_rad_ =
       get_parameter("yaw_tolerance_rad").as_double();

- Line 39: the default value sets the type: 1.5 makes a double.
- Line 45: the constructor reads each value once, into a data member.

Why a Node Declares Its Parameters
""""""""""""""""""""""""""""""""""

A node accepts only the parameters it declared. Two tries on ``heading_controller_node``:

1. A misspelled name, while the node runs:

   .. code-block:: bash

      ros2 param set /heading_controller_node kp_lineer 2.0

   The command fails: "parameter 'kp_lineer' cannot be set because it was not declared".

2. A parameter of the other node, given at start with ``-p kp_linear:=0.8``. The node starts with no message, and ``ros2 param get /heading_controller_node kp_linear`` answers "Parameter not set".

.. admonition:: Conclusion
   :class: important

   A wrong name on the command line at start is dropped without a message. Check what the node has with ``ros2 param list``.

An Array Parameter: a List of Headings
""""""""""""""""""""""""""""""""""""""

``target_headings_deg`` holds four headings, read into a ``std::vector<double>``. The robot turns to each one in order. Lines 21 to 30 of ``heading_controller_node.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 21
   :emphasize-lines: 1, 9

   if (target_index_ >= target_headings_deg_.size()) {
       publish_command(0.0);
       control_timer_->cancel(); // done: no more control_callback
       RCLCPP_INFO_STREAM(get_logger(),
                          "all " << target_headings_deg_.size()
                                 << " headings reached");
       return;
   }
   const double target_deg{target_headings_deg_[target_index_]};
   const double target_yaw{target_deg * std::numbers::pi / 180.0};

- Line 29: ``target_index_`` picks the heading to reach now. Within the tolerance, line 41 adds 1 to it.
- Line 21: after the last heading, the node stops for good.

Command-Line Tools: list and get
""""""""""""""""""""""""""""""""

.. code-block:: bash

   ros2 param list /heading_controller_node

.. code-block:: text

   kp_angular
   max_angular_rps
   qos_overrides./parameter_events.publisher.depth
   qos_overrides./parameter_events.publisher.durability
   qos_overrides./parameter_events.publisher.history
   qos_overrides./parameter_events.publisher.reliability
   start_type_description_service
   target_headings_deg
   use_sim_time
   yaw_tolerance_rad

.. code-block:: bash

   ros2 param get /heading_controller_node kp_angular

.. code-block:: text

   Double value is: 1.5

The node declared four parameters. ROS 2 adds the others to every node, among them ``use_sim_time``.

Setting a Value the Node Already Read
"""""""""""""""""""""""""""""""""""""

The node was started with ``kp_angular`` 0.5. During its first turn, the gain is set to 1.5:

.. code-block:: bash

   ros2 param set /heading_controller_node kp_angular 1.5

.. code-block:: text

   Set parameter successful

``ros2 param get`` then answers 1.5. The node's log, after the set:

.. code-block:: text

   [...]: error 0.068624 rad, command 0.034312 rad/s
   [...]: error 0.0432666 rad, command 0.0216333 rad/s

0.5 × 0.0686 = 0.0343 rad/s: the node still uses 0.5.

.. admonition:: Conclusion
   :class: important

   ``ros2 param set`` changes the stored value. The node read ``kp_angular`` once, in its constructor, so its commands do not change.

Command-Line Tools: dump
""""""""""""""""""""""""

``ros2 param dump`` prints every stored value of a node. In this run, the node started with ``kp_angular`` 1.5, and ``ros2 param set`` then stored 0.5:

.. code-block:: bash

   ros2 param dump /heading_controller_node

.. code-block:: text

   /heading_controller_node:
     ros__parameters:
       kp_angular: 0.5
       max_angular_rps: 1.0
       [...]
       target_headings_deg:
       - 90.0
       - 180.0
       - -90.0
       - 0.0
       use_sim_time: false
       yaw_tolerance_rad: 0.02

The output is a parameter file: the next subsection loads files like it. ``[...]`` cuts the lines ROS 2 adds to every node.

Set a Parameter
^^^^^^^^^^^^^^^

You can set a parameter from the command line, from a YAML file, or from a launch file. The listings of this subsection are from stage 3 (commit ``e7048f4``).

On the Command Line, at Start
"""""""""""""""""""""""""""""

``--ros-args`` starts the arguments for ROS 2, and each ``-p name:=value`` sets one parameter before the constructor reads it:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe \
     --ros-args -p kp_angular:=0.5

.. code-block:: text

   [...]: error 1.58335 rad, command 0.791676 rad/s

0.5 × 1.583 = 0.792 rad/s: the node uses the new gain from its first command. The teleop node of the keyboard section got ``-p stamped:=true`` the same way.

.. note::

   Write a double with a decimal point. ``1`` is an integer, and ``kp_angular`` refuses it: "Wrong parameter type, parameter {kp_angular} is of type {double}, setting it to {integer} is not allowed".

From a YAML File
""""""""""""""""

A parameter file sets many parameters at once: ``config/controllers.yaml``.

.. code-block:: yaml
   :linenos:
   :lineno-start: 3
   :emphasize-lines: 1, 5

   /**:
     ros__parameters:
       use_sim_time: true

   heading_controller_node:
     ros__parameters:
       target_headings_deg: [90.0, 180.0, -90.0, 0.0]
       kp_angular: 1.5
       max_angular_rps: 1.0
       yaw_tolerance_rad: 0.02

- Line 7: a key names a node; its values are under ``ros__parameters``. Lines 14 to 19 hold ``distance_controller_node``'s.
- Line 3: the **wildcard** key ``/**`` matches every node.

From the package folder, ``l12_rosbot``:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe \
     --ros-args --params-file config/controllers.yaml

.. _l12-use-sim-time:

use_sim_time for a Node That Runs with Gazebo
"""""""""""""""""""""""""""""""""""""""""""""

Gazebo publishes its own time on ``/clock``. With ``use_sim_time`` true, a node's clock follows ``/clock`` instead of the computer's clock: ``now()``, and so the stamp of every ``TwistStamped``, gives the simulation's time.

Every node has ``use_sim_time``, and it is false unless you set it:

- With ``controllers.yaml`` (the ``/**`` key): ``ros2 param get`` answers ``True``.
- With a plain ``ros2 run``: it answers ``False``.

.. admonition:: Conclusion
   :class: important

   Set ``use_sim_time`` to true for every node you run with Gazebo. The ``/**`` key of a parameter file does it for all of them.

From a Launch File: a YAML File Named by an Argument
""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 12 to 25 of ``launch/heading_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 12
   :emphasize-lines: 2-5, 12

   params_file = DeclareLaunchArgument(
       "params_file",
       default_value=PathJoinSubstitution(
           [FindPackageShare("l12_rosbot"), "config",
            "controllers.yaml"]
       ),
       description="YAML file with the controller's parameters",
   )
   heading_controller = Node(
       package="l12_rosbot",
       executable="heading_controller_exe",
       parameters=[LaunchConfiguration("params_file")],
       output="screen",
   )

- Lines 13 to 16: the launch argument ``params_file``, by default the installed ``controllers.yaml``.
- Line 23: a list, here with one file: the one the argument names.

Install and Run the Launch File
"""""""""""""""""""""""""""""""

Lines 59 and 60 of ``CMakeLists.txt`` install the ``launch`` and ``config`` folders, where ``ros2 launch`` and ``FindPackageShare`` look:

.. code-block:: cmake
   :linenos:
   :lineno-start: 59

   install(DIRECTORY launch config
     DESTINATION share/${PROJECT_NAME})

After a build, the default file, then another one:

.. code-block:: bash

   ros2 launch l12_rosbot heading_launch.py
   ros2 launch l12_rosbot heading_launch.py \
     params_file:=install/l12_rosbot/share/l12_rosbot/config/low_gain.yaml

``low_gain.yaml`` is ``controllers.yaml`` without the distance controller, and with ``kp_angular`` 0.5 instead of 1.5. The next part compares three gains.

Three Gains, Three Separate Runs
""""""""""""""""""""""""""""""""

Each run turns through the four headings, so each turn is 90°. A turn's time is the gap between two "reached" lines of the log:

.. list-table::
   :header-rows: 1
   :widths: 18 40 42

   * - Gain
     - Set by
     - 90° turns, in s
   * - 0.5
     - ``low_gain.yaml``
     - 6.40, 6.45, 6.25
   * - 1.5
     - ``controllers.yaml``
     - 2.70, 2.75, 2.65
   * - 4.0
     - ``controllers.yaml``, then ``-p kp_angular:=4.0``
     - 2.70, 2.70, 2.70

The command stays at the 1.0 rad/s limit while the gain times the error is over 1.0: with a gain of 1.5, until the error is under 1.0 / 1.5 = 0.67 rad, so for the first 1.57 − 0.67 = 0.90 rad of a 90° turn; with 4.0, until 1.0 / 4.0 = 0.25 rad, so for the first 1.32 rad.

.. admonition:: Conclusion
   :class: important

   A gain of 4.0 kept the command at the limit longer, yet the turn was no faster: 2.70 s with 1.5 and with 4.0.

From a Launch File: Values Written in It
""""""""""""""""""""""""""""""""""""""""

A launch file can also hold the values itself, as a Python dictionary. Lines 8 to 21 of ``launch/distance_launch.py``:

.. code-block:: python
   :linenos:
   :lineno-start: 8
   :emphasize-lines: 5-11

   distance_controller = Node(
       package="l12_rosbot",
       executable="distance_controller_exe",
       parameters=[
           {
               "use_sim_time": True,
               "target_distance_m": 1.0,
               "kp_linear": 0.8,
               "max_linear_mps": 0.5,
               "distance_tolerance_m": 0.02,
           }
       ],
       output="screen",
   )

With this launch file, the robot drove 0.981 m. A new value means editing the launch file, so values you tune belong in a YAML file.

React to a Change
^^^^^^^^^^^^^^^^^

A node can run a callback when someone sets a parameter. The callback accepts or rejects the new value. The listings of this subsection are from stage 4 (commit ``94d4d64``), the final code.

Register the Callback
"""""""""""""""""""""

The node registers ``on_parameters_set`` at the end of its constructor. Lines 55 to 57 of ``heading_controller_node.hpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 55

   parameter_callback_handle_ = add_on_set_parameters_callback(
       std::bind(&HeadingControllerNode::on_parameters_set, this,
                 std::placeholders::_1));

Lines 64 and 65 declare the callback, and lines 73 and 74 keep the handle:

.. code-block:: cpp
   :linenos:
   :lineno-start: 64

   rcl_interfaces::msg::SetParametersResult on_parameters_set(
       const std::vector<rclcpp::Parameter> &parameters);

.. code-block:: cpp
   :linenos:
   :lineno-start: 73

   rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr
       parameter_callback_handle_;

- The callback gets the parameters of one set command, and says if the node accepts them.
- The callback stays registered only while the handle, a data member, exists.
- ``SetParametersResult`` is in ``rcl_interfaces``: add it to ``package.xml`` and ``CMakeLists.txt``.

The Callback, Part 1: Refuse a Parameter Read Only at Start
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Lines 68 to 81 of ``heading_controller_node.cpp``:

.. code-block:: cpp
   :linenos:
   :lineno-start: 68
   :emphasize-lines: 9-13

   rcl_interfaces::msg::SetParametersResult
   HeadingControllerNode::on_parameters_set(
       const std::vector<rclcpp::Parameter> &parameters) {
       rcl_interfaces::msg::SetParametersResult result{};
       // First check every new value. One bad value rejects the whole
       // change.
       for (const auto &parameter : parameters) {
           const std::string &name{parameter.get_name()};
           if (name == "target_headings_deg") {
               result.successful = false;
               result.reason =
                   "target_headings_deg is read once, at start";
               return result;
           }

- Lines 76 to 80: the node never reads the list again, so a new list would change nothing. The callback says so instead of accepting it.

The Callback, Part 2: Refuse a Bad Value
""""""""""""""""""""""""""""""""""""""""

Lines 82 to 96 of the same file, still inside the first loop:

.. code-block:: cpp
   :linenos:
   :lineno-start: 82
   :emphasize-lines: 1, 6-8

       if (name == "kp_angular" && parameter.as_double() < 0.0) {
           result.successful = false;
           result.reason = "kp_angular must not be negative";
           return result;
       }
       if (name == "max_angular_rps" &&
           (parameter.as_double() <= 0.0 ||
            parameter.as_double() > rosbot_max_angular_rps)) {
           result.successful = false;
           result.reason =
               "max_angular_rps must be more than 0 and at most "
               "3.14 rad/s";
           return result;
       }
   }

- Line 82: a negative gain would turn the robot away from its target.
- Lines 87 to 89: 3.14 rad/s is the ROSbot's turning limit.

The Callback, Part 3: Store the New Values
""""""""""""""""""""""""""""""""""""""""""

Lines 97 to 114 of the same file:

.. code-block:: cpp
   :linenos:
   :lineno-start: 97
   :emphasize-lines: 5, 6, 16

   // Every value is good: store the new ones, so the next
   // control_callback uses them.
   for (const auto &parameter : parameters) {
       const std::string &name{parameter.get_name()};
       if (name == "kp_angular") {
           kp_angular_ = parameter.as_double();
       } else if (name == "max_angular_rps") {
           max_angular_rps_ = parameter.as_double();
       } else if (name == "yaw_tolerance_rad") {
           yaw_tolerance_rad_ = parameter.as_double();
       }
       const std::string value{parameter.value_to_string()};
       RCLCPP_INFO_STREAM(get_logger(),
                          "new value: " << name << " = " << value);
   }
   result.successful = true;
   return result;


Change a Gain While the ROSbot Turns
""""""""""""""""""""""""""""""""""""

The node runs with ``low_gain.yaml`` (gain 0.5). Five ``ros2 param set`` commands, in order:

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - Set
     - Answer
   * - ``kp_angular -1.0``
     - Setting parameter failed: kp_angular must not be negative
   * - ``max_angular_rps 5.0``
     - Setting parameter failed: max_angular_rps must be more than 0 and at most 3.14 rad/s
   * - ``kp_angular 2``
     - Setting parameter failed: Wrong parameter type [...]
   * - ``target_headings_deg [10.0]``
     - Setting parameter failed: target_headings_deg is read once, at start
   * - ``kp_angular 1.5``
     - Set parameter successful

- ROS 2's own type check refused ``kp_angular 2``: the answer is its message, not one of the callback's.
- The turn to 180° took 6.40 s at gain 0.5. The gain changed during the next turn, which took 3.20 s. The last turn, at 1.5, took 2.70 s.

Parameters: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Declare a parameter with a default value, and read it with ``get_parameter``.
   - List, get, set and dump the parameters of a running node.
   - Set parameters at start: with ``-p``, from a YAML file, or from a launch file.
   - Set ``use_sim_time`` for every node that runs with Gazebo.
   - Check and store a new value while the node runs, with a parameter callback.

Remapping
---------

Parameters changed a node's settings without recompiling. **Remapping** does the same for the topic names in its code, and a **namespace** puts a prefix in front of them. Both use the same controller, unchanged.

Why Remap: Topic Names Written in the Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``heading_controller_node`` names its two topics in its code: ``"odometry/filtered"`` (line 29 of ``heading_controller_node.hpp``, stage 4) and ``"cmd_vel"`` (line 34). Two jobs need other names:

- **Another source.** ``differential_drive_controller`` also publishes ``/odometry/wheels``, the pose from the wheels alone. To compare the two, the controller must read ``/odometry/wheels``.
- **A fleet.** Each robot of a fleet has its own topics, such as ``/robot1/cmd_vel`` and ``/robot2/cmd_vel``, and each controller must use its own robot's.

Editing the strings means one copy of the code per job. Instead, ``--ros-args`` changes the names when the node starts:

- ``-r from:=to`` **remaps** one name to another.
- ``-r __ns:=/robot1`` puts the node in a **namespace**: "a prefix added to the names of its nodes and of its relative topics", the definition of the previous lecture.

Remap a Topic: Read the Wheel Odometry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe \
     --ros-args -r odometry/filtered:=odometry/wheels

``ros2 node info /heading_controller_node``, first lines:

.. code-block:: text

   Subscribers:
     /odometry/wheels: nav_msgs/msg/Odometry
     /parameter_events: rcl_interfaces/msg/ParameterEvent

- The node turned through its four headings, measured by the wheel odometry.
- After these runs, the two topics gave two headings for the same robot: -0.70° on ``/odometry/filtered``, -84.39° on ``/odometry/wheels``. The first takes its heading from the IMU; the second counts wheel turns only.

.. admonition:: Conclusion
   :class: important

   Remapping changes where a node reads, not what the data means. Check what the new topic carries.

Put the Node in a Namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the previous lecture, ``PushROSNamespace`` put the nodes of a launch file in a namespace. ``__ns`` does the same from the command line:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe --ros-args -r __ns:=/robot1

``ros2 node info /robot1/heading_controller_node``, first lines:

.. code-block:: text

   Subscribers:
     /parameter_events: rcl_interfaces/msg/ParameterEvent
     /robot1/odometry/filtered: nav_msgs/msg/Odometry
   Publishers:
     /parameter_events: rcl_interfaces/msg/ParameterEvent
     /robot1/cmd_vel: geometry_msgs/msg/TwistStamped

- The node and both relative topic names got the prefix ``/robot1``.
- ``ros2 topic info /robot1/odometry/filtered``: "Publisher count: 0". No odometry arrives, so ``control_callback`` returns at once: the node logged nothing and published no command.

A Namespace and Remapping Together
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simulation has one ROSbot, with no namespace. Keep the node's namespace, and remap its two topics to the robot's absolute names:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe --ros-args \
     -r __ns:=/robot1 \
     -r odometry/filtered:=/odometry/filtered -r cmd_vel:=/cmd_vel

.. code-block:: text

   [INFO] [...] [robot1.heading_controller_node]: all 4 headings reached

- ``ros2 node info`` lists ``/odometry/filtered`` and ``/cmd_vel``: a name that starts with ``/`` is absolute, and the namespace does not change it.
- In a launch file, ``Node(...)`` takes the same settings as ``namespace=`` and ``remappings=``.

.. admonition:: Conclusion
   :class: important

   The namespace names the node; the remapping points two of its topics at the robot. The code did not change.

Remapping: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Remap a topic name when a node starts: ``--ros-args -r from:=to``.
   - Put a node in a namespace: ``-r __ns:=/name``. Its relative names get the prefix; its absolute names do not.
   - Combine the two, to give a node its own name and still reach a robot's topics.
   - Check the result with ``ros2 node info`` and ``ros2 topic info``.

Next Class
----------

- **Next lecture**: *L13: Frames and Transforms*. Poses, frames, and broadcasting, listening to and debugging transforms.
- **Pre-work**: complete the L12 :doc:`exercises <l12_exercises>` and :doc:`quiz <l12_quiz>` on ReadTheDocs. GP2 is posted today. This lecture covers the simulation it runs in, proportional control and parameters. Optional, beyond the course: the :doc:`Services and Actions </reading_material/services_actions/sa_index>` reading.
- **Required reading**:

  - `ROS 2 Jazzy: Parameters <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`__
  - :doc:`ROSbot Simulation </setup/rosbot_simulation>`
  - :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>`
