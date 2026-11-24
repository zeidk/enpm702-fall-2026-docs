====================================================
ROSbot Simulation
====================================================

.. _setup-rosbot-simulation:

The simulation puts a **Husarion ROSbot**, a small wheeled robot, in a
Gazebo world. Lecture 12 to Lecture 14 and Group Project 2 (GP2) use it as
the robot you program. This page installs it and checks that it runs.

Before you start, finish :doc:`ros_setup`: ROS 2 Jazzy, the course repository
cloned at ``~/ros2_ws/src/enpm702-fall-2026-ros`` (with ``upstream`` set) and
Gazebo (``ros-jazzy-ros-gz``). The simulation is in the folder ``rosbot_sim``
of the course repository.

.. note::

   Gazebo needs a graphics card with working 3D drivers. In a virtual machine
   or in WSL it can run very slowly or not draw anything. See
   `Troubleshooting`_.


Install
-------

The steps run once.

1. **Get the new code.** Commit your own changes first, then:

   .. code-block:: bash

      cd ~/ros2_ws/src/enpm702-fall-2026-ros
      git fetch upstream
      git merge --no-edit upstream/main
      git push

   ``ls`` in that folder now shows ``rosbot_sim``.

2. **Set up rosdep**, the tool that installs the system packages the
   simulation needs. Run ``sudo rosdep init`` only if you have never run it on
   this computer (if you have, it stops with an error that a file already
   exists: ignore it). Then:

   .. code-block:: bash

      sudo rosdep init
      rosdep update

3. **Install what the simulation needs**, from the workspace root:

   .. code-block:: bash

      source /opt/ros/jazzy/setup.bash
      cd ~/ros2_ws
      rosdep install --from-paths src --ignore-src -y

   It asks for your password, because it runs ``sudo apt install``.

.. dropdown:: More detail: what rosdep installs, and what was removed from the Husarion packages
   :class-container: more-detail
   :icon: info

   On a computer that has ``ros-jazzy-desktop``, ``ros-jazzy-ros-gz`` and
   ``ros-dev-tools`` and nothing else, ``rosdep`` installs 13 ROS packages (45
   packages with their dependencies, about 53 MB to download; apt's package
   sizes). Run the command again after a later merge: it installs only what is
   new.

   The Husarion code also drives the real robot, a joystick and a robot arm.
   The simulation uses none of that, so the course copy leaves it out. The
   upstream packages list 83 different dependencies (rosdep keys), among them
   MoveIt, tools that flash the robot's firmware and joystick packages. The
   course copy lists 35. On a computer with only the course setup, that is 112
   packages (about 125 MB) before and 45 packages (about 53 MB) after.
   ``rosbot_sim/README.md`` lists every removed package, and the upstream
   source and license of each one.


Build
-----

.. code-block:: bash

   cd ~/ros2_ws
   colcon build
   source install/setup.bash

The last line lets this terminal find the new packages. Run it in every new
terminal you use for the simulation.


Test the Simulation
-------------------

Start it. In a new terminal, run the ``source`` line first:

.. code-block:: bash

   source ~/ros2_ws/install/setup.bash
   ros2 launch gp2_bringup gp2_sim.launch.py

A Gazebo window opens with the patrol world and the ROSbot at its start.
**Gazebo needs about 40 s to start the first time**: wait until the robot
appears.

Then drive the robot with the **Teleop** panel on the right of the Gazebo
window. Click :guilabel:`▲`: the robot moves forward a little and stops. Try
:guilabel:`◀`, :guilabel:`▶`, :guilabel:`▼` and :guilabel:`Stop`. If the robot
moves, the simulation works. Try it here first:

.. raw:: html
   :file: widgets/gazebo_teleop.html

Each click sends one message on ``/cmd_vel``. The arrows set the direction and
keep it until :guilabel:`Stop`, so :guilabel:`▲` then :guilabel:`◀` drives an
arc. The robot stops by itself 0.5 s after the last message, so one click moves
it about 0.25 m or turns it about 16°. The ↑ and ↓ buttons are for flying
robots: the ROSbot ignores them.

Press :kbd:`Ctrl+C` in the launch terminal to stop the simulation.

.. dropdown:: More detail: check and drive the robot from a terminal
   :class-container: more-detail
   :icon: info

   In a second terminal (after ``source ~/ros2_ws/install/setup.bash``):

   .. code-block:: bash

      ros2 topic list

   The list has 31 topics. These are the ones you use: ``/clock``,
   ``/cmd_vel``, ``/imu/data``, ``/logical_camera``, ``/odometry/filtered``,
   ``/scan``, ``/scan_filtered``, ``/tf`` and ``/tf_static``.

   Read the robot's position, then drive it forward at 0.2 m/s until you
   press :kbd:`Ctrl+C`:

   .. code-block:: bash

      ros2 topic echo --once /odometry/filtered --field pose.pose.position
      ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/TwistStamped "{twist: {linear: {x: 0.2}}}"

   On the course computer, ``x`` was 0.56 to 0.87 m after 5 s of this command
   (six runs). To turn on the spot, use ``"{twist: {angular: {z: 0.5}}}"``. To
   drive with the keyboard, add the parameter ``stamped`` (see `What Surprises
   People`_):

   .. code-block:: bash

      ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true

.. dropdown:: More detail: launch arguments
   :class-container: more-detail
   :icon: info

   All optional, set as ``name:=value``:

   .. list-table::
      :header-rows: 1
      :widths: 22 18 60
      :class: compact-table

      * - Argument
        - Default
        - Meaning
      * - ``gui``
        - ``true``
        - ``false`` runs Gazebo without a window, for a remote or slow computer.
      * - ``world``
        - ``patrol``
        - ``patrol``, ``patrol_doors_swapped``, ``empty``, or the path of an
          ``.sdf`` file.
      * - ``rviz``
        - ``false``
        - ``true`` opens RViz with the ROSbot's configuration.
      * - ``x``, ``y``, ``yaw``
        - ``0.0``
        - Start pose of the robot (meters, radians).
      * - ``logical_camera``
        - ``true``
        - ``false`` leaves out the logical camera.

   For example:

   .. code-block:: bash

      ros2 launch gp2_bringup gp2_sim.launch.py gui:=false rviz:=true


The Robot
---------

The **Husarion ROSbot** is a small research robot with four wheels. The two
wheels on each side turn together, so the robot turns by driving its left and
right sides at different speeds (a *differential drive*). The simulation uses
the ROSbot's real shape, wheels and sensor positions.

.. list-table::
   :header-rows: 1
   :widths: 32 68
   :class: compact-table

   * - Property
     - Value
   * - Body
     - 0.197 m long, 0.150 m wide, 0.080 m high (collision box of the model)
   * - Wheels
     - Radius 0.0425 m, left and right wheels 0.186 m apart
   * - Speed limits (controller configuration)
     - 1.0 m/s forward, 3.14 rad/s turning
   * - Lidar
     - Slamtec RPLIDAR S2: 3000 beams over a full circle, 0.05 m to 30 m,
       published on ``/scan`` (9.6 messages per second measured)
   * - Camera
     - Luxonis OAK-D Pro: color image 1280 by 720 and depth, on the ``/oak``
       topics
   * - Logical camera
     - Gazebo logical camera, added by the course (see below)
   * - IMU
     - Inertial sensor on ``/imu/data``

Topics you will use:

.. list-table::
   :header-rows: 1
   :widths: 28 38 34
   :class: compact-table

   * - Topic
     - Type
     - Meaning
   * - ``/cmd_vel``
     - ``geometry_msgs/msg/TwistStamped``
     - Velocity command (you publish).
   * - ``/odometry/filtered``
     - ``nav_msgs/msg/Odometry``
     - Pose in the ``odom`` frame from wheels and IMU (19.3 messages per
       second measured).
   * - ``/scan``
     - ``sensor_msgs/msg/LaserScan``
     - Lidar, frame ``laser``.
   * - ``/scan_filtered``
     - ``sensor_msgs/msg/LaserScan``
     - The same scan without the beams that hit the robot itself.
   * - ``/logical_camera``
     - ``ros_gz_interfaces/msg/LogicalCameraImage``
     - Models in the camera's view, frame ``logical_camera_link``.
   * - ``/imu/data``
     - ``sensor_msgs/msg/Imu``
     - Orientation, angular velocity and acceleration.
   * - ``/tf``, ``/tf_static``
     - ``tf2_msgs/msg/TFMessage``
     - Frames of the robot.
   * - ``/clock``
     - ``rosgraph_msgs/msg/Clock``
     - Simulation time. Your nodes use the parameter ``use_sim_time:=true``.
   * - ``/patrol_cam/image``
     - ``sensor_msgs/msg/Image``
     - A fixed camera above the building (1920 by 1080). It does not move
       with the robot.

Frames: ``odom`` is the parent of ``base_link``. ``base_link`` is at the
center of the robot, x forward, y left. ``laser`` is fixed to the robot,
0.02 m ahead of and 0.131 m above ``base_link``. ``logical_camera_link`` is
0.12 m ahead of and 0.20 m above ``base_link``. At the start, ``odom`` and the
world frame are the same.

The logical camera
^^^^^^^^^^^^^^^^^^

The simulation has no object detector. A Gazebo **logical camera** stands in
for one. It makes no picture. It lists the models inside its view volume with
each model's name and pose. The camera looks forward: its field of view is 115
degrees (2.0 rad), and it lists models 0.3 m to 3.5 m ahead. Each pose is in
the camera frame, so to get a position in ``odom`` you transform it with TF2.

.. code-block:: bash

   ros2 topic echo --once /logical_camera

Two facts to plan for:

- The camera lists a model when the model's **origin** is inside the view
  volume. The walls, the doors, the blue discs on the floor and the floor
  itself appear in the list too, so you filter the list by name.
- Nothing blocks the view. The camera also lists a model behind a wall.

What Surprises People
^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Two things that differ from what you expect
   :class: important

   1. **The command topic takes a stamped message.** ``/cmd_vel`` has the type
      ``geometry_msgs/msg/TwistStamped``, not ``Twist``. It has a ``header``
      and a ``twist`` field. The two types do not connect, so a node that
      publishes ``Twist`` cannot move the robot.
   2. **The lidar frame is turned by 180 degrees.** ``ros2 run tf2_ros
      tf2_echo base_link laser`` prints a rotation of 180.000 degrees about
      z. The direction straight ahead of the robot is at the angle
      plus or minus pi in ``/scan``, not at 0.


The Environment
---------------

.. raw:: html
   :file: widgets/patrol_world.html

The tags in the 3D view:

.. list-table::
   :header-rows: 1
   :widths: 10 40 50
   :class: compact-table

   * - Tag
     - What
     - Where (x, y in meters)
   * - 1
     - Checkpoint 1 (blue disc)
     - (5.0, -0.5)
   * - 2
     - Checkpoint 2 (blue disc)
     - (9.5, -1.4)
   * - 3
     - Checkpoint 3 (blue disc)
     - (12.0, 0.4)
   * - 4
     - Checkpoint 4 (blue disc)
     - (3.0, 0.4)
   * - 5
     - Start of the robot
     - (0.0, 0.0), facing east
   * - 6
     - ``fire_extinguisher`` (orange cylinder)
     - (7.6, 1.3)
   * - 7
     - ``crate`` (brown box, 1.2 m by 0.8 m)
     - (9.5, -2.4)
   * - 8
     - ``person`` (green cylinder with a head)
     - (11.6, 1.45)
   * - 9
     - ``spill`` (purple disc)
     - (3.6, 1.3)
   * - 10
     - Door 3, closed (red panel)
     - x = 12, in the wall y = 2
   * - 11
     - Door 4, open
     - x = 3, in the wall y = 2

The patrol world
^^^^^^^^^^^^^^^^

The world is one floor, 20 m by 10 m, with walls 1 m high. The x axis points
east and the y axis points north. The robot starts at the origin and faces
east.

- **Hall:** x from -3 to 17 and y from -3 to 2 (5 m wide).
- **Rooms:** two rooms lie north of the hall, at y from 2 to 7, split at
  x = 7. Each opens to the hall through a doorway 3 m wide in the wall
  y = 2.
- **Checkpoints:** the start and each checkpoint are at least 1.5 m from every
  wall.
- **Objects:** each is a Gazebo model with its own name, and the logical
  camera lists it by that name. Each is seen from one checkpoint: the
  ``fire_extinguisher`` from checkpoint 1, the ``crate`` from checkpoint 2,
  the ``person`` from checkpoint 3 and the ``spill`` from checkpoint 4.
  The objects have no collision shape, so the robot drives through them
  instead of getting stuck. The lidar and the camera still see them. The
  walls and the doors keep their collision shapes.

Other worlds
^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 28 72
   :class: compact-table

   * - ``world:=``
     - What it is
   * - ``patrol``
     - The world above (the default).
   * - ``patrol_doors_swapped``
     - The same building with door 3 open and door 4 closed, and without the
       ``fire_extinguisher`` and the ``person``.
   * - ``empty``
     - A flat floor with the fixed camera.

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py world:=patrol_doors_swapped

All three worlds have the logical camera plugin.


Troubleshooting
---------------

.. list-table::
   :header-rows: 1
   :widths: 38 62
   :class: compact-table

   * - Problem
     - What to do
   * - ``Package 'gp2_bringup' not found``
     - The terminal has not sourced your workspace. Run
       ``source ~/ros2_ws/install/setup.bash``. If it still fails, run
       ``colcon build`` in ``~/ros2_ws`` first.
   * - ``ros2 topic list`` has no ``/odometry/filtered``
     - Gazebo is still starting (about 40 s the first time). Wait, then run
       the command again.
   * - The Gazebo window is black, very slow, or does not open
     - You are probably in a virtual machine or in WSL, which have no 3D
       acceleration. Start with ``gui:=false``: the simulation and every
       topic still work. Use RViz (``rviz:=true``) or ``/patrol_cam/image``
       to see the robot.
   * - A classmate's simulation moves your robot, or your topics show
       another robot
     - Two simulations on one network share their topics. Choose a number from
       1 to 100 and use it in every terminal before you launch:
       ``export ROS_DOMAIN_ID=<number>`` and
       ``export GZ_PARTITION=<name>``.
   * - Gazebo is still running after :kbd:`Ctrl+C`
     - Run ``ps aux | grep "gz sim"``. To stop it, run ``pkill -f "gz sim"``.
   * - ``rosdep install`` asks for a key it cannot find
     - Run ``rosdep update``, then try again. If you never ran
       ``sudo rosdep init``, run it first.
