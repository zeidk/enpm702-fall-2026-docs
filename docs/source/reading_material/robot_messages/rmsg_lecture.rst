====================================================
Lecture
====================================================


.. note::

   **Where the outputs come from.** The message definitions on this page
   are the output of ``ros2 interface show`` on ROS 2 Jazzy. Every C++
   example was built with the course flags (``-std=c++20 -Wall -Wextra
   -pedantic-errors -Wshadow``) and run against the messages shown with it.


Why a Robot Needs These Messages
====================================================

In the lectures, the robotaxi published its position as a
``geometry_msgs/msg/Point``: three numbers that you chose. A real mobile
robot already has topics of its own, with message types that the whole
ROS community uses. GP1 and GP2 use the topics of the Husarion ROSbot:

.. list-table::
   :header-rows: 1
   :widths: 22 34 44
   :class: compact-table

   * - Topic
     - Message type
     - What it carries
   * - ``cmd_vel``
     - ``geometry_msgs/msg/Twist`` (GP1), ``geometry_msgs/msg/TwistStamped`` (GP2)
     - The velocity your node asks the robot to drive at.
   * - ``odometry/filtered``
     - ``nav_msgs/msg/Odometry``
     - Where the robot thinks it is, and how fast it moves.
   * - ``scan``
     - ``sensor_msgs/msg/LaserScan``
     - The distances the range sensor measured, one per beam.

In GP1, your stand-in robot node subscribes to ``cmd_vel`` and publishes
the other two. In GP2, the simulated ROSbot does. Because both use the
same names and types, your other nodes do not change between the two
projects.

Every one of these messages measures something in a direction: a speed
forward, a turn, a position, an angle. So before the messages, you need
the directions.


Directions and Units
====================================================

ROS fixes its directions and units in one document,
`REP 103 <https://www.ros.org/reps/rep-0103.html>`__ (a REP is a ROS
Enhancement Proposal, a design rule for the whole community). For a
robot's own body, REP 103 says:

- "x forward", "y left", "z up";
- "All systems are right handed";
- lengths in meters, angles in radians, time in seconds (SI units).

.. figure:: /_static/images/robot_messages/rmsg_axes.png
   :alt: A four-wheeled robot seen from above, its front marked with a triangle on the right side. A red arrow points right from the robot's center, labeled x: forward. A green arrow points up the page, labeled y: left. At the center, a blue circle with a dot is labeled z: up, out of the page. A curved navy arrow turns from the x arrow toward the y arrow, labeled positive yaw: counterclockwise (a turn to the left).
   :align: center
   :width: 55%

   The robot's axes, seen from above. A turn from x toward y is
   counterclockwise, and it is a positive angle.

The angle that a ground robot turns by is its **yaw**: the rotation about
the z axis. Right handed means that a positive yaw turns x toward y. Seen
from above, that is counterclockwise, a turn to the left. REP 103 says it
this way: "the yaw component of orientation increases as the child frame
rotates counter-clockwise". A turn to the right is a negative yaw.

.. important::

   Every sign on this page follows from these two rules. A positive
   ``angular.z`` turns the robot left. A heading of 90° faces +y. A beam
   at a positive angle points to the left of the scanner (the scanner's
   own frame can face another way than the robot: see `Which Beam Is
   Which`_).


Velocity Commands: ``Twist``
====================================================

The Message
----------------------------------------------------

``cmd_vel`` carries a ``geometry_msgs/msg/Twist``:

.. code-block:: bash

   ros2 interface show geometry_msgs/msg/Twist

.. code-block:: text

   # This expresses velocity in free space broken into its linear and angular parts.

   Vector3  linear
   	float64 x
   	float64 y
   	float64 z
   Vector3  angular
   	float64 x
   	float64 y
   	float64 z

A ``Twist`` holds two vectors of type ``geometry_msgs/msg/Vector3``, each
with an ``x``, a ``y`` and a ``z``:

- ``linear`` is a speed along each axis, in m/s.
- ``angular`` is a turn rate about each axis, in rad/s.

That is six numbers, because a drone or an arm can move in all six ways.
A robot that drives on a floor can only do two of them: drive along its
own x axis, and turn about its own z axis. So it reads two numbers and
ignores the other four:

.. list-table::
   :header-rows: 1
   :widths: 20 14 66
   :class: compact-table

   * - Field
     - Unit
     - Meaning on a ground robot
   * - ``linear.x``
     - m/s
     - Forward speed. A negative value drives backward.
   * - ``angular.z``
     - rad/s
     - Turn rate. A positive value turns left (counterclockwise); a
       negative value turns right.
   * - the other four
     -
     - Not used: leave them at 0. The robot cannot slide sideways
       (``linear.y``) or fly (``linear.z``), and it cannot roll or pitch
       (``angular.x``, ``angular.y``).

What the Two Numbers Do
----------------------------------------------------

The values in the figure are chosen for this example.

.. figure:: /_static/images/robot_messages/rmsg_twist.png
   :alt: Three panels, each with the values on top and a sentence below. Left, linear.x = 0.2 and angular.z = 0.0: a robot facing right with a dashed straight arrow ahead of it; it drives straight ahead. Middle, linear.x = 0.0 and angular.z = 0.5: a robot with a dashed circular arrow around it, turning counterclockwise; it turns in place, to the left. Right, linear.x = 0.2 and angular.z = 0.5: a robot facing right and a dashed quarter circle that curves up to a gray copy of the robot, now facing up the page; a dot above the first robot marks the center of the circle, with a dotted line labeled radius; it drives on a circle, to the left.
   :align: center
   :width: 95%

   Three commands. The path in each panel is what the robot drives while
   the command holds.

- **Only** ``linear.x``: the robot drives straight ahead, 0.2 m every
  second.
- **Only** ``angular.z``: the robot turns in place, 0.5 rad every second.
  A full turn, 2π rad, takes 2π / 0.5 = 12.6 s.
- **Both**: the robot drives forward while it turns, so it follows a
  circle to its left. The radius of the circle is the forward speed
  divided by the turn rate: 0.2 / 0.5 = 0.4 m.

A command describes a velocity, not a distance. The robot keeps driving at
it until a new command arrives. To stop, publish a ``Twist`` with every
field at 0.

Sending One
----------------------------------------------------

From a terminal, ``ros2 topic pub`` sends a command. Fields you leave out
are 0:

.. code-block:: bash

   ros2 topic pub --once cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.5}}"

``ros2 topic echo cmd_vel`` shows what arrived:

.. code-block:: text

   linear:
     x: 0.2
     y: 0.0
     z: 0.0
   angular:
     x: 0.0
     y: 0.0
     z: 0.5
   ---

In C++, fill the two fields and publish, with a publisher of
``geometry_msgs::msg::Twist`` and the header
``<geometry_msgs/msg/twist.hpp>``:

.. code-block:: cpp

   geometry_msgs::msg::Twist command;
   command.linear.x = 0.2;   // forward speed, m/s
   command.angular.z = 0.5;  // turn rate, rad/s: positive turns left
   cmd_vel_publisher_->publish(command);

A new ``Twist`` starts with every field at 0, so the four unused fields
need no line.

``TwistStamped`` on the ROSbot (GP2)
----------------------------------------------------

The ROSbot's drive controller is configured to take a
``geometry_msgs/msg/TwistStamped`` on ``cmd_vel``
(``use_stamped_vel: true`` in its configuration). It is the same
``Twist``, with a header in front:

.. code-block:: bash

   ros2 interface show --no-comments geometry_msgs/msg/TwistStamped

.. code-block:: text

   std_msgs/Header header
   	builtin_interfaces/Time stamp
   		int32 sec
   		uint32 nanosec
   	string frame_id
   Twist twist
   	Vector3  linear
   		float64 x
   		float64 y
   		float64 z
   	Vector3  angular
   		float64 x
   		float64 y
   		float64 z

So every field moves one level down, under ``twist``, and the header gets
the time the command was made (header ``<geometry_msgs/msg/twist_stamped.hpp>``):

.. code-block:: cpp

   geometry_msgs::msg::TwistStamped stamped;
   stamped.header.stamp = now();
   stamped.twist.linear.x = 0.2;
   stamped.twist.angular.z = 0.5;

A ``Twist`` published on a topic that expects a ``TwistStamped`` reaches
no subscriber: the two types differ, and ROS 2 connects a publisher and a
subscriber only when their types match.


Where the Robot Is: ``Odometry``
====================================================

The Message
----------------------------------------------------

``odometry/filtered`` carries a ``nav_msgs/msg/Odometry``. Its first
comment line says what it is: "an estimate of a position and velocity in
free space". The fields, without the comments:

.. code-block:: bash

   ros2 interface show --no-comments nav_msgs/msg/Odometry

.. code-block:: text
   :emphasize-lines: 10,11,13,14,15,16,17

   std_msgs/Header header
   	builtin_interfaces/Time stamp
   		int32 sec
   		uint32 nanosec
   	string frame_id
   string child_frame_id
   geometry_msgs/PoseWithCovariance pose
   	Pose pose
   		Point position
   			float64 x
   			float64 y
   			float64 z
   		Quaternion orientation
   			float64 x 0
   			float64 y 0
   			float64 z 0
   			float64 w 1
   	float64[36] covariance
   geometry_msgs/TwistWithCovariance twist
   	Twist twist
   		Vector3  linear
   			float64 x
   			float64 y
   			float64 z
   		Vector3  angular
   			float64 x
   			float64 y
   			float64 z
   	float64[36] covariance

The highlighted lines are the ones GP1 and GP2 use: the position ``x`` and
``y``, and the orientation, a quaternion (`Orientation: Quaternion and
Yaw`_). The parts of the message:

.. list-table::
   :header-rows: 1
   :widths: 34 66
   :class: compact-table

   * - Field
     - What it holds
   * - ``header.stamp``
     - The time of the estimate.
   * - ``header.frame_id``
     - The frame the position is measured in: ``odom`` on the ROSbot
       (next section).
   * - ``child_frame_id``
     - The frame attached to the robot: ``base_link`` on the ROSbot.
   * - ``pose.pose.position``
     - The robot's position, in m: ``x`` and ``y`` (``z`` is 0 for a
       robot on the floor).
   * - ``pose.pose.orientation``
     - The robot's heading, as a quaternion.
   * - ``pose.covariance``
     - How uncertain the pose is: 36 numbers, a 6 × 6 matrix written row
       by row. GP1 leaves them at 0.
   * - ``twist.twist``
     - The robot's velocity, a ``Twist``, in the ``base_link`` frame. GP1
       leaves it empty.

The path to the position is long because the message nests: an
``Odometry`` holds a ``PoseWithCovariance`` named ``pose``, which holds a
``Pose`` also named ``pose``, which holds a ``Point`` named ``position``.
So the x coordinate of a message ``msg`` is ``msg.pose.pose.position.x``.

The ``odom`` Frame
----------------------------------------------------

A position is a distance from somewhere. The ``odom`` frame is that
somewhere: its origin is where the robot started, and its x axis is where
the robot faced at the start. `REP 105 <https://www.ros.org/reps/rep-0105.html>`__
defines it: "The coordinate frame called odom is a world-fixed frame".
It does not move with the robot, so a checkpoint keeps the same
coordinates during the whole run.

.. figure:: /_static/images/robot_messages/rmsg_pose.png
   :alt: The odom frame drawn as two axes, a red x axis to the right and a green y axis up, with tick marks at 1 m and 2 m on x and 1 m on y, and the word odom at the origin. A robot stands at x = 2 m, y = 1 m, with dashed lines down to the x axis and left to the y axis. The robot faces up the page. A dashed line points right from its center, and a navy arrow turns from it to the robot's heading, labeled yaw = 90° (1.57 rad). A label reads position: x = 2.0 m, y = 1.0 m.
   :align: center
   :width: 60%

   A pose in the ``odom`` frame: the position (x, y), and the yaw, measured
   from the x axis of ``odom``.

REP 105 also gives the frame's limit: "The pose of a mobile platform in
the odom frame can drift over time, without any bounds". Odometry adds up
small measurements, and their errors add up too. In the GP2 reference
runs in Gazebo, the odometry and the robot's true position differed by up
to 0.016 m at the checkpoints (R4 of :doc:`/assignments/gp2`).

Where It Comes From
----------------------------------------------------

The name ``odometry/filtered`` says that a filter made the estimate. On
the ROSbot, two sources go into it. The drive controller turns the wheel
encoders into an odometry of its own, ``odometry/wheels``. The IMU (an
inertial measurement unit, which measures turn rates and accelerations)
publishes ``imu/data``. A node named ``ekf``, from the
``robot_localization`` package, combines the two (an extended Kalman
filter) and publishes ``odometry/filtered``. In GP1, your stand-in robot
node publishes ``odometry/filtered`` directly.

.. figure:: /_static/images/robot_messages/rmsg_odometry_sources.png
   :alt: Two rounded frames of ROS nodes and topics. The top frame, In GP1, holds stand_in_robot_node, which publishes the topic odometry/filtered of type nav_msgs/msg/Odometry, read by navigation_node. The bottom frame, On the ROSbot (GP2), holds differential_drive_controller, which publishes odometry/wheels of type nav_msgs/msg/Odometry, and imu_broadcaster, which publishes imu/data of type sensor_msgs/msg/Imu. Both topics go into the node ekf, from robot_localization, which publishes odometry/filtered of type nav_msgs/msg/Odometry, read by your nodes.
   :align: center
   :width: 100%

   Who publishes ``odometry/filtered``. White boxes are nodes; navy boxes
   are topics, with their message type.

Your nodes subscribe to ``odometry/filtered`` in both projects and never
see the difference.

Reading One in C++
----------------------------------------------------

A callback for ``odometry/filtered``, written as the subscriber callbacks
of the lectures (header ``<nav_msgs/msg/odometry.hpp>``):

.. code-block:: cpp

   void on_odometry(const nav_msgs::msg::Odometry &msg) {
     const double x{msg.pose.pose.position.x};  // m, in the odom frame
     const double y{msg.pose.pose.position.y};  // m, in the odom frame
     const double yaw{gp1_patrol::yaw_from_quaternion(msg.pose.pose.orientation)};  // rad
     RCLCPP_INFO(get_logger(), "x = %.2f m, y = %.2f m, yaw = %.2f rad", x, y, yaw);
   }

For a robot at x = 2 m and y = 1 m that faces +y (the pose of the figure),
this callback logs:

.. code-block:: text

   [INFO] [...] [check_node]: x = 2.00 m, y = 1.00 m, yaw = 1.57 rad

``yaw_from_quaternion`` is one of the helpers in ``geometry.hpp``, in the
GP1 starter (next section).


Orientation: Quaternion and Yaw
====================================================

The Message
----------------------------------------------------

ROS gives every orientation as a ``geometry_msgs/msg/Quaternion``:

.. code-block:: text

   float64 x 0
   float64 y 0
   float64 z 0
   float64 w 1

A **quaternion** is four numbers that describe any rotation in three
dimensions. ROS uses it for every robot, because a drone or an arm can
tilt in any direction. The defaults, x, y and z at 0 and w at 1, are no
rotation at all.

A robot on a floor only turns about z: its orientation is its yaw alone.
For a rotation about z by an angle yaw, x and y stay 0, and:

- z = sin(yaw / 2)
- w = cos(yaw / 2)

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25
   :class: compact-table

   * - Heading
     - Yaw (rad)
     - ``z``
     - ``w``
   * - faces +x
     - 0
     - 0
     - 1
   * - 45° left
     - 0.79
     - 0.383
     - 0.924
   * - faces +y (90° left)
     - 1.57
     - 0.707
     - 0.707
   * - faces −x (180°)
     - 3.14
     - 1
     - 0
   * - faces −y (90° right)
     - −1.57
     - −0.707
     - 0.707

So the pose in the figure above, at 90°, has ``z`` = 0.707 and ``w`` =
0.707.

You Do Not Need the Math
----------------------------------------------------

The GP1 starter gives two helpers in
``gp1_patrol/include/gp1_patrol/geometry.hpp`` (GP2's starter has the same
header, in the namespace ``gp2_patrol``):

.. list-table::
   :header-rows: 1
   :widths: 45 55
   :class: compact-table

   * - Helper
     - What it does
   * - ``yaw_from_quaternion(orientation)``
     - Reads the yaw, in rad, counterclockwise from +x, in (−π, π].
   * - ``quaternion_from_yaw(yaw)``
     - Builds the quaternion of a heading, with only ``z`` and ``w`` set.

Read a heading with the first, and write one (in your stand-in robot) with
the second. Compare and subtract headings as yaw angles, never as
quaternions. The header has helpers for that too: ``wrap_angle`` and
``angle_difference``, which keep an angle in (−π, π].


Distances: ``LaserScan``
====================================================

The Message
----------------------------------------------------

``scan`` carries a ``sensor_msgs/msg/LaserScan``: "Single scan from a
planar laser range-finder", in its own words. A range finder sends beams
in a fan, in one plane, and measures how far each beam travels before it
hits something. The definition, with its comments:

.. code-block:: text

   std_msgs/Header header # timestamp in the header is the acquisition time of
                                # the first ray in the scan.
                                #
                                # in frame frame_id, angles are measured around
                                # the positive Z axis (counterclockwise, if Z is up)
                                # with zero angle being forward along the x axis

   float32 angle_min            # start angle of the scan [rad]
   float32 angle_max            # end angle of the scan [rad]
   float32 angle_increment      # angular distance between measurements [rad]

   float32 time_increment       # time between measurements [seconds] - if your scanner
                                # is moving, this will be used in interpolating position
                                # of 3d points
   float32 scan_time            # time between scans [seconds]

   float32 range_min            # minimum range value [m]
   float32 range_max            # maximum range value [m]

   float32[] ranges             # range data [m]
                                # (Note: values < range_min or > range_max should be discarded)
   float32[] intensities        # intensity data [device-specific units].  If your
                                # device does not provide intensities, please leave
                                # the array empty.

The comment under ``header`` follows the rules of `Directions and
Units`_: angle 0 is along the x axis of the scan's own frame, the frame
named in ``header.frame_id``, and angles grow counterclockwise. When that
frame faces the way the robot does, as in GP1, angle 0 is straight ahead,
a beam at a negative angle points to the robot's right, and a beam at a
positive angle to its left.

Which Beam Is Which
----------------------------------------------------

``ranges`` has one distance per beam. The message does not store the
angle of each beam: you compute it. Beam 0 is at ``angle_min``, and each
next beam is ``angle_increment`` further counterclockwise:

- angle of beam ``i`` = ``angle_min`` + ``i`` × ``angle_increment``

.. figure:: /_static/images/robot_messages/rmsg_scan.png
   :alt: Two panels. Left, titled a scan, angles drawn large: a robot facing right sends seven beams in a fan. The lowest beam, labeled ranges[0], is at angle_min, shown by a red arrow that turns clockwise from the dashed straight-ahead line, labeled angle_min (negative: right). The highest beam, labeled ranges[6], is at angle_max, shown by a green arrow turning counterclockwise, labeled angle_max (positive: left). A short blue arc between the straight-ahead line and the next beam is labeled angle_increment. Right, titled GP1's three beams, to scale: a robot facing right sends three nearly parallel beams, labeled from bottom to top ranges[0] (-0.1 rad), ranges[1] (0.0 rad) and ranges[2] (+0.1 rad).
   :align: center
   :width: 100%

   Left: the angles of a scan (drawn larger than a real scanner's step).
   Right: the three beams of GP1's stand-in scan.

In GP1, the stand-in scan has ``angle_min`` −0.1 rad, ``angle_max`` 0.1 rad
and ``angle_increment`` 0.1 rad. So it has three beams:

- beam 0: −0.1 + 0 × 0.1 = −0.1 rad, a little to the right;
- beam 1: −0.1 + 1 × 0.1 = 0 rad, straight ahead;
- beam 2: −0.1 + 2 × 0.1 = 0.1 rad, a little to the left.

The lidar of the simulated ROSbot in GP2 is a Slamtec RPLIDAR S2: 3000
beams over a full circle (:doc:`/setup/rosbot_simulation`). The formula
stays the same; only the three numbers change. One more difference: its
frame, ``laser``, is turned by 180 degrees from the robot. Its x axis
points backward, so the beam straight ahead of the robot is at plus or
minus π, not at angle 0, and a positive angle points to the robot's
right. GP2 asks you to find the index of the beam straight ahead from
``angle_min`` and ``angle_increment`` (:doc:`/assignments/gp2`).

Ranges You Must Not Trust
----------------------------------------------------

A beam that hits nothing within ``range_max`` has no distance to report.
`REP 117 <https://www.ros.org/reps/rep-0117.html>`__ says what to write
instead: "out of range detections will be represented by +Inf", a reading
too close to measure by ``-inf``, and an erroneous one by ``NaN``. The
message's comment says what to do with all three: "values < range_min or >
range_max should be discarded". A ``NaN`` is not equal to anything, so
``<`` and ``>`` are both false for it, and a check with ``<`` or ``>``
alone can let it through. ``std::isfinite`` catches all three: it is
false for ``inf``, ``-inf`` and ``NaN``.

Reading One in C++
----------------------------------------------------

A callback that logs the angle and range of every valid beam (headers
``<sensor_msgs/msg/laser_scan.hpp>``, ``<cmath>`` for ``std::isfinite``
and ``<cstddef>`` for ``std::size_t``):

.. code-block:: cpp

   void on_scan(const sensor_msgs::msg::LaserScan &msg) {
     for (std::size_t i{0}; i < msg.ranges.size(); ++i) {
       const double angle{msg.angle_min + static_cast<double>(i) * msg.angle_increment};
       const float range{msg.ranges[i]};
       if (std::isfinite(range) && range >= msg.range_min && range <= msg.range_max) {
         RCLCPP_INFO(get_logger(), "beam %zu: angle %.2f rad, range %.2f m", i, angle, range);
       }
     }
   }

For a three-beam scan with the GP1 angles and the ranges 2.0 m, 1.5 m and
``inf`` (chosen for this example), it logs:

.. code-block:: text

   [INFO] [...] [check_node]: beam 0: angle -0.10 rad, range 2.00 m
   [INFO] [...] [check_node]: beam 1: angle 0.00 rad, range 1.50 m

Beam 2 is not logged: ``std::isfinite`` is false for ``inf``.


Summary
====================================================

.. list-table::
   :header-rows: 1
   :widths: 20 30 50
   :class: compact-table

   * - Topic
     - Type
     - The fields you use
   * - ``cmd_vel``
     - ``Twist`` (GP1), ``TwistStamped`` (GP2)
     - ``linear.x`` (m/s, forward) and ``angular.z`` (rad/s, positive
       left); under ``twist`` in a ``TwistStamped``.
   * - ``odometry/filtered``
     - ``Odometry``
     - ``pose.pose.position.x`` and ``.y`` (m, in ``odom``), and
       ``pose.pose.orientation``, read with ``yaw_from_quaternion``.
   * - ``scan``
     - ``LaserScan``
     - ``ranges[i]`` (m), at the angle ``angle_min`` + ``i`` ×
       ``angle_increment``; discard values outside ``range_min`` to
       ``range_max``.
