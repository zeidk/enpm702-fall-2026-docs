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

Its ``rosbot_sim`` folder holds the simulation. Install and build it with the steps of the :doc:`ROSbot Simulation </setup/rosbot_simulation>` page. Its last step starts Gazebo with the ROSbot; the first start is the slowest:

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py

Then build this lecture's package, ``L12/l12_rosbot``, from ``~/ros2_ws``:

.. code-block:: bash

   colcon build --packages-select l12_rosbot
   source install/setup.bash

In class, I do not explain the shell commands: you learned them in the shell exercises on ReadTheDocs, which every student was asked to do.

Code for This Lecture
---------------------

The ``L12`` folder of the course repository holds one package, ``l12_rosbot``. It has the two controller nodes of this lecture, a node for the simulation time demo, a configuration folder and a launch folder:

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
   │   ├── distance_controller_node.hpp
   │   └── sim_time_node.hpp
   ├── launch/
   │   ├── heading_launch.py
   │   ├── distance_launch.py
   │   └── remap_launch.py
   └── src/
       ├── heading_controller_main.cpp
       ├── heading_controller_node.cpp
       ├── distance_controller_main.cpp
       ├── distance_controller_node.cpp
       ├── sim_time_main.cpp
       └── sim_time_node.cpp

The code grows in six stages, one commit each. The lecture quotes the stage a listing belongs to, because the line numbers change from stage to stage:

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
     - A parameter callback in ``heading_controller_node``.
   * - 5
     - ``6d2b94b``
     - ``sim_time_node``, which shows what ``use_sim_time`` changes, and ``remap_launch.py``, a launch file with a name, a namespace and two remappings; the :doc:`Namespaces and Remapping </reading_material/remapping/remap_index>` reading uses it.
   * - 6
     - ``fe5d602``
     - The two controllers time their loop with ``create_timer`` instead of ``create_wall_timer``, so they follow the node clock and stop while Gazebo is paused. This is the final code of the package.

To read a stage, check out its commit in the course repository. The listings below name their stage; a listing that says "stage 4" matches the files you get from the repository, except two lines: every listing shows the timer of stage 6, ``create_timer``, where stages 1 to 5 have ``create_wall_timer``, and every listing that shows ``target_yaw`` declares it ``constexpr``, where the repository has ``const double target_yaw``.

Pose
----

A **pose** says where a robot is and which way it faces: a **position** and an **orientation**, measured in a coordinate frame. The position is three numbers, x, y and z, in meters. The orientation says how the robot is turned. ROS writes it in two ways, which this section explains: three angles (roll, pitch and yaw) or a quaternion (four numbers). The controller later in this class needs one part of the orientation, the yaw.

Pose: Position and Orientation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Pose
   :class: tip

   The position and the orientation of a body, measured in a coordinate frame.

- **Position**: where the body is, three numbers, x, y and z, in meters along the frame's axes. In a robot's body frame (``base_link``), x is forward, y left and z up (`REP 103 <https://www.ros.org/reps/rep-0103.html>`__).
- **Orientation**: how the body is turned. An orientation is given by rotations about the axes: **roll** about x, **pitch** about y and **yaw** about z.

**The right-hand rule.** REP 103: "All systems are right handed".

#. Axes: the axes are right-handed. Point the fingers of your right hand along x, bend them toward y, and your thumb points along z.
#. Rotations: a positive rotation follows the right-hand rule. Point your thumb along the axis, and your bent fingers show the turn.
#. With z up, a positive yaw turns counterclockwise, seen from above. So a positive ``angular.z`` turns the ROSbot left. REP 103: "the yaw component of orientation increases as the child frame rotates counter-clockwise".

**Roll, pitch and yaw.** Three angles give an orientation, each a turn about one axis of the frame (REP 103). Three turns in a set order like these are called **Euler angles**:

.. list-table::
   :header-rows: 1
   :widths: 16 22 62

   * - Angle
     - About
     - On the ROSbot
   * - Roll
     - x, forward
     - tilts it sideways: 0 on a flat floor
   * - Pitch
     - y, left
     - tilts its front up or down: 0 on a flat floor
   * - Yaw
     - z, up
     - its heading: changes each time it turns

On the course's flat floor, the ``ekf`` runs in 2D mode (``two_d_mode: true``): roll and pitch stay 0, and only the yaw changes. Angles are in radians, and the yaw is kept between :math:`-\pi` and :math:`\pi`.

The same three turns in another order give another orientation. REP 103 ranks the ways to write an orientation, a quaternion first and fixed-axis roll, pitch and yaw among the angles, and warns: "Euler angles are generally discouraged due to having 24 'valid' conventions with different domains using different conventions by default". 24 orders and axis choices are in use. So a library always says which order it uses.

**The quaternion: four numbers for one turn.** Any orientation is one turn by an angle :math:`\theta` about one axis :math:`(a_x, a_y, a_z)` of length 1. ROS messages store it as a quaternion, four numbers x, y, z, w.

.. admonition:: Quaternion
   :class: tip

   Four numbers :math:`q = (x, y, z, w)` of length 1, :math:`x^2 + y^2 + z^2 + w^2 = 1`, that store one turn: :math:`(x, y, z)` is the axis times :math:`\sin\frac{\theta}{2}`, and :math:`w = \cos\frac{\theta}{2}`.

What it is:

- No turn, :math:`\theta = 0`: (0, 0, 0, 1), the defaults of ``geometry_msgs/msg/Quaternion``.
- 90° about z: half of 90° is 45°, and sin 45° = cos 45° = 0.707, so (0, 0, 0.707, 0.707).

.. dropdown:: More detail: quaternions and complex numbers
   :class-container: more-detail
   :icon: info

   - A quaternion extends the complex numbers: :math:`q = w + x\,i + y\,j + z\,k`, with :math:`i^2 = j^2 = k^2 = ijk = -1`. ROS lists w last.
   - A complex number of length 1 turns a point in the plane; a quaternion of length 1 turns a point in 3D.

Why ROS uses it:

#. Compact: four numbers; a rotation matrix needs nine. REP 103: "Compact representation".
#. No singularities: at a pitch of ±90°, roll and yaw turn about the same axis, so one orientation has many sets of angles (gimbal lock). REP 103: "No singularities".
#. No order to agree on: in another order, the same three angles give another orientation. A quaternion is one turn.

**A turn by an angle about an axis.** Four steps turn an axis and an angle into the quaternion. Here: 90° about (0.707, 0.707, 0), an axis in the x-y plane, halfway between x and y.

.. figure:: /_static/images/l12/quat_axis_turn.png
   :width: 70%
   :alt: An airliner in 3D, its nose along x, its wings along y and its fin up z, turned 90 degrees about a purple axis that lies in the x-y plane halfway between x and y; a faint copy of the airliner stays at the start pose, and the airliner's own x, y and z arrows show where its nose, left wing and fin now point.

   Faint: the airplane before the turn. Purple: the axis.

#. :math:`(a_x, a_y, a_z) = (0.707, 0.707, 0)`, length 1.
#. Half the angle: :math:`\frac{\theta}{2}` = 45°, :math:`\sin\frac{\theta}{2} = \cos\frac{\theta}{2} = 0.707`.
#. The axis times :math:`\sin\frac{\theta}{2}`: x = 0.707 × 0.707 = 0.5, y = 0.707 × 0.707 = 0.5, z = 0 × 0.707 = 0.
#. :math:`w = \cos\frac{\theta}{2} = 0.707`.

So q = (0.5, 0.5, 0, 0.707), of length 1: 0.25 + 0.25 + 0 + 0.5 = 1. The interactive slides let you pick other axes and angles.

**The ROSbot's quaternion on a flat floor: a turn about z.** On a flat floor the ROSbot turns only about z, the axis (0, 0, 1), by its yaw, so the four steps give x = y = 0, :math:`z = \sin\frac{\text{yaw}}{2}`, :math:`w = \cos\frac{\text{yaw}}{2}`. (The quaternion's x, y, z are not the position's x, y, z.) On a ramp it would pitch too, and x and y would not be 0. The course's ``ekf`` sets ``two_d_mode: true`` in ``rosbot_localization/config/config.yaml``; robot_localization says that then "no 3D information will be used in your state estimate", for "a planar environment". The course world is flat.

.. list-table::
   :header-rows: 1
   :widths: 18 22 30 30

   * - Yaw
     - Facing
     - :math:`z = \sin\frac{\text{yaw}}{2}`
     - :math:`w = \cos\frac{\text{yaw}}{2}`
   * - 0
     - +x
     - 0
     - 1
   * - 90°
     - +y
     - 0.707
     - 0.707
   * - 180°
     - −x
     - 1
     - 0
   * - −90°
     - −y
     - −0.707
     - 0.707

The odometry message carries this quaternion; :ref:`l12-yaw-from-quaternion` turns it back into the yaw.

The ROSbot in Gazebo
--------------------

The previous section said how ROS writes a pose. This section puts it to work on a simulated robot, the one GP2 uses. **Gazebo** is a simulator: it runs a robot and its sensors in a virtual world.

Gazebo and the ROSbot
^^^^^^^^^^^^^^^^^^^^^

Gazebo computes the physics of the robot and the readings of its sensors. The ROSbot is the robot you program in Gazebo for the rest of the course.

What Gazebo Simulates
"""""""""""""""""""""

Gazebo runs a robot in a virtual world, so you can test your nodes without a real robot. It computes three things:

- **Physics**: the wheels push the robot over the floor, and the walls stop it.
- **Sensors**: what each sensor would read in that world. The simulation publishes the readings on ROS topics.
- **The world**: walls, doors and objects, read from a world file.

.. figure:: /_static/images/l12/gz_patrol_overview.png
   :alt: Rendered view from the patrol world's fixed camera, high above the south side, looking north and down: a long hall along the bottom with four blue discs, a purple disc, a small orange cylinder, a green cylinder with a round head beside a red door panel, and a brown box against the south wall; two rooms above, joined to the hall by an open doorway on the left and the red door on the right; the small ROSbot near the left end of the hall.
   :align: center
   :width: 90%

   The course's patrol world, from its own fixed camera (``/patrol_cam/image``), saved from the simulation. The robot is the small dark shape at the left of the hall.

Where to read more about Gazebo:

- `Gazebo <https://gazebosim.org/>`__, the simulator's home page, and `Getting Started with Gazebo <https://gazebosim.org/docs/harmonic/getstarted/>`__, the tutorials of Gazebo Harmonic, the version ROS 2 Jazzy uses.
- `SDF worlds <https://gazebosim.org/docs/harmonic/sdf_worlds/>`__ and the `SDFormat specification <http://sdformat.org/spec>`__: how a world file describes walls, objects, lights and robots.
- `Sensors <https://gazebosim.org/docs/harmonic/sensors/>`__: how Gazebo simulates cameras, lidars and IMUs.

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

.. figure:: /_static/images/l12/gz_shapes_world.png
   :alt: Rendered view of the shapes demo world: on a grey ground, from left to right, a yellow capsule, a green cylinder, a red box, a blue sphere, a magenta ellipsoid and an orange cone, each with its shadow.
   :align: center
   :width: 90%

   The six models of ``shapes.sdf``, from left to right: a capsule, a cylinder, a box, a sphere, an ellipsoid and a cone. Saved without a window, from a camera added to a copy of the world; with ``gz sim shapes.sdf``, the window shows the same scene.

.. dropdown:: More detail: more of the Gazebo window
   :class-container: more-detail
   :icon: info

   Three more things the window does, after you have run, inspected and moved a model (``gz sim shapes.sdf``):

   - **Plugins.** The menu at the top right lists the plugins, the panels you can add. Its search field finds one by name: type ``teleop`` and only Teleop is left. Click it and the Teleop panel docks at the bottom right. It publishes speed commands; on the setup page you drive the ROSbot with it.
   - **Pause and Step.** Pause stops the simulation: sim time and the iteration count stay where they were (in the recorded tour, 2:08.977 and 128977). Step runs one iteration while paused: 128977 becomes 128978, and sim time moves 1 ms, to 2:08.978.
   - **Reset.** Reset asks first. It puts every model back where the world file placed it, and the clocks and iterations restart at 0.

.. dropdown:: More detail: the bridge between Gazebo and ROS
   :class-container: sd-border-secondary

   - Gazebo publishes on its own topics, with its own message types. Gazebo's clock is a ``gz.msgs.Clock``; the ROS clock is a ``rosgraph_msgs/msg/Clock``.
   - A bridge node, ``parameter_bridge`` from the package ``ros_gz_bridge``, subscribes on one side, converts each message to the other side's type, and publishes it there.
   - Its configuration file lists the topics to copy: for each one, its name, the two types and the direction. The course simulation's ``rosbot_gazebo/config/gz_bridge.yaml`` copies the clock, from Gazebo to ROS (``GZ_TO_ROS``): the ``/clock`` that ``use_sim_time`` reads.

   .. code-block:: yaml

      - topic_name: /clock
        ros_type_name: rosgraph_msgs/msg/Clock
        gz_type_name: gz.msgs.Clock
        direction: GZ_TO_ROS

   - ``ros2 launch gp2_bringup gp2_sim.launch.py`` runs five bridge nodes: for the clock, the velocity command ``/cmd_vel``, the lidar, the robot's camera, and the patrol camera.
   - More: `Use ROS 2 to interact with Gazebo <https://gazebosim.org/docs/harmonic/ros2_integration/>`__ and the `ros_gz_bridge package <https://github.com/gazebosim/ros_gz/tree/jazzy/ros_gz_bridge>`__.

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
     - Lists the objects it sees, with their names and positions
   * - IMU
     - Measures the robot's orientation, turn rate and acceleration
   * - Odometry
     - The robot's pose, computed from the wheels and the IMU

.. figure:: /_static/images/l12/rosbot.png
   :alt: Photo of the Husarion ROSbot: a black robot with four rubber wheels and red corners, a round RPLIDAR lidar on top, a depth camera on a bracket above the lidar, and an antenna at the back.
   :align: center
   :width: 50%

   The Husarion ROSbot.

The ROSbot is made by `Husarion <https://husarion.com/>`__: see the `ROSbot manual <https://husarion.com/manuals/rosbot/>`__, and `rosbot_ros <https://github.com/husarion/rosbot_ros>`__, the ROS 2 packages the course simulation is built on. The simulated ROSbot uses Husarion's own model, with the same body, wheels and sensor positions:

.. grid:: 2

   .. grid-item::

      .. figure:: /_static/images/l12/gz_rosbot_closeup.png
         :alt: Rendered close view of the simulated ROSbot on a grey floor: a dark grey body on four spiked black wheels, a light grey block on top, and a camera on a curved mast at the back.

         Up close.

   .. grid-item::

      .. figure:: /_static/images/l12/gz_rosbot_hall.png
         :alt: Rendered view from just behind the simulated ROSbot at its start, at robot height, looking east down the hall: the robot in the foreground, blue and purple discs on the floor, a small orange cylinder, a green cylinder with a round head in front of a red door, and a brown box against the right wall.

         At its start, from behind, facing east (+x) down the hall.

Both views were saved from cameras added to the running simulation.

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

.. dropdown:: More detail: where the odometry comes from
   :class-container: sd-border-secondary

   - **Odometry** estimates the robot's pose by adding up its own motion since the start. It adds up small steps, and each step's error stays in the total, so the error grows as the robot drives. It needs no map.
   - ``/odometry/wheels`` comes from the wheels alone: the drive controller turns the wheel rotations into the robot's motion.
   - ``/odometry/filtered`` comes from ``ekf``, which fuses the wheels with the IMU. It takes the heading (yaw) from the IMU, the forward speed from the wheels, and the turn rate from both. It publishes about 20 times a second (19.8 Hz in the course simulation).

Start the world with the robot in it, or the robot alone on an empty floor:

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py
   ros2 launch gp2_bringup gp2_sim.launch.py world:=empty

.. note::

   The ROSbot can also take mecanum wheels, which drive sideways too (``twist.linear.y``). Husarion's packages have a ``mecanum`` option; the course simulation removed its controller and does not offer it.

.. dropdown:: More detail: linear and angular velocity, and the wheels
   :class-container: sd-border-secondary

   - ``linear.x`` is :math:`v`: how fast the middle of the robot moves forward, in m/s, the way it faces. Negative drives backward.
   - ``angular.z`` is :math:`\omega`: how fast it turns about the vertical axis, in rad/s. Positive turns left (counterclockwise from above).
   - No sideways speed: ``linear.y`` does nothing on a differential drive. To reach a point to its side, the robot turns first.
   - The controller gives each side a speed, :math:`v_L = v - \omega\,s/2` and :math:`v_R = v + \omega\,s/2`, and each wheel spins at :math:`v_{side}/r`. In the course simulation, :math:`s` = 0.186 m × 1.36 = 0.253 m and :math:`r` = 0.0425 m (``rosbot_controller/config/rosbot/controllers.yaml``).
   - The pose follows: :math:`\dot x = v\cos\theta`, :math:`\dot y = v\sin\theta`, :math:`\dot\theta = \omega`. With both set, the robot drives a circle of radius :math:`R = v/\omega`.

   .. list-table::
      :header-rows: 1
      :widths: 26 40 34

      * - Command
        - Wheels
        - Motion
      * - :math:`v > 0`, :math:`\omega = 0`
        - both sides the same
        - straight ahead
      * - :math:`v = 0`, :math:`\omega > 0`
        - left back, right forward
        - turns left on the spot
      * - :math:`v > 0`, :math:`\omega > 0`
        - right faster than left
        - a left arc, :math:`R = v/\omega`

.. raw:: html
   :file: widgets/_head.html

Move the two sliders to build a command and see the path the robot would drive for 3 s.

.. raw:: html
   :file: widgets/twist.html

Drag the knob on the pad to drive the robot, and watch its speeds, its wheels and its pose change.

.. raw:: html
   :file: widgets/drive.html

Kinematics: From v and ω to Each Side's Wheels
""""""""""""""""""""""""""""""""""""""""""""""

The drive controller turns :math:`v` and :math:`\omega` into a speed for each side of the robot, :math:`v_L` and :math:`v_R` in m/s. The two wheels of a side turn together (``left_wheel_names: [fl_wheel_joint, rl_wheel_joint]`` in ``controllers.yaml``). :math:`s` is the distance between the two sides, and :math:`r` the wheel radius.

- **From the sides to the robot:** :math:`v = \dfrac{v_R + v_L}{2}`, :math:`\omega = \dfrac{v_R - v_L}{s}`.
- **From the robot to the sides** (what the drive controller does): :math:`v_L = v - \omega\,\dfrac{s}{2}`, :math:`v_R = v + \omega\,\dfrac{s}{2}`. Each wheel turns at :math:`v_{side}/r` rad/s.

The ROSbot turning on the spot at :math:`\omega` = 1.0 rad/s. Its file sets :math:`s` = 0.186 m × 1.36 = 0.253 m (1.36: Husarion's correction, which its file says depends on the floor) and :math:`r` = 0.0425 m.

1. :math:`v_L` = 0 − 1.0 × 0.253 / 2 = −0.1265 m/s, and :math:`v_R` = +0.1265 m/s.
2. Each wheel turns at 0.1265 / 0.0425 = 2.98 rad/s: the left ones backward, the right ones forward.



The Patrol World
""""""""""""""""

The patrol world is a hall and rooms, 20 m by 10 m inside walls 1 m high. The robot starts at the origin and faces east, along +x.

.. figure:: /_static/images/rosbot/patrol_world.png
   :alt: Top view of the patrol world from Gazebo, with x in meters along the bottom and y in meters along the left. A long hall runs along the bottom with the small dark robot at the origin, tag 5, and four blue discs, tags 1 to 4. Two rooms lie above the hall, joined to it by two doorways in the wall at y equals 2: the left doorway, tag 11, is open, and the right one, tag 10, has a red panel. A purple disc, tag 9, a small orange cylinder, tag 6, a green cylinder with a round head, tag 8, and a brown box, tag 7, lie in the hall.
   :align: center
   :width: 90%

   The patrol world. Tags 1 to 4 are checkpoints, 5 is the robot's start, 6 to 9 are objects, 10 is a closed door and 11 is an open door.

Drag to turn and tilt the world, right-drag (or Shift+drag) to pan, and scroll to zoom. The tags are the figure's.

.. raw:: html
   :file: widgets/world.html


Launch the Simulation
^^^^^^^^^^^^^^^^^^^^^

One launch file starts Gazebo, the world and the ROSbot. You start it once, then use it from other terminals.

Start the Simulation
""""""""""""""""""""

One command starts Gazebo, the patrol world and the ROSbot:

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py

- The first start is the slowest, while Gazebo loads its models: wait before you check anything. A later start without a window (``gui:=false``) sent odometry after 8.6 s.
- Check it from a second terminal: ``ros2 topic list`` prints 31 topics.

.. note::

   Keep the launch terminal open: the simulation runs until you stop it. Use other terminals for everything else.

.. dropdown:: More detail: What the launch file starts
   :class-container: more-detail
   :icon: info

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

The launch file takes launch arguments, set on the command line as ``name:=value``, the same ``name:=value`` form as any launch argument. The main ones, all optional:

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
   * - ``logical_camera``
     - ``true``
     - ``false`` leaves out the front-facing logical camera.
   * - ``x``, ``y``, ``yaw``
     - ``0.0``
     - The robot's start pose, in meters and radians.

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py gui:=false rviz:=true

To stop the simulation, press :kbd:`Ctrl+C` in the launch terminal.

Click a value in each row to build the launch command.

.. raw:: html
   :file: widgets/launch-args.html


RViz: What ROS Sees
"""""""""""""""""""

Gazebo draws the simulated world. **RViz**, a ROS node, draws what the robot's topics hold: its model, its frames and the lidar's ranges. It places them all in one frame you choose, the **fixed frame** (here ``odom``). Two ways to start it:

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
     - The objects it sees, with their names and positions.
   * - ``/tf``, ``/tf_static``
     - ``tf2_msgs/msg/TFMessage``
     - The robot's frames, next class.
   * - ``/clock``
     - ``rosgraph_msgs/msg/Clock``
     - The simulation time.

.. note::

   ``/cmd_vel`` takes a ``TwistStamped``: a ``Twist`` with a header that holds a time stamp. The two types do not connect, so a node that publishes ``Twist`` on ``/cmd_vel`` cannot move the robot.

.. dropdown:: More detail: Read the position
   :class-container: more-detail
   :icon: info

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

.. dropdown:: More detail: Drive with the keyboard
   :class-container: more-detail
   :icon: info

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

Press Start publishing, then press Ctrl+C, to see when the controller brakes.

.. raw:: html
   :file: widgets/brake.html


.. _l12-simulation-time:

Simulation Time
^^^^^^^^^^^^^^^

Gazebo keeps its own clock. A node reads either that clock or the computer's, and the choice changes what ``now()`` returns and when a timer fires.

Two Clocks: the Computer's and Gazebo's
"""""""""""""""""""""""""""""""""""""""

Gazebo counts its own time from the moment the simulation starts, and publishes it on ``/clock``:

.. code-block:: bash

   ros2 topic echo --once /clock

.. code-block:: text

   clock:
     sec: 24
     nanosec: 988000000

.. code-block:: bash

   gz topic -e -t /world/patrol/stats -n 1 | grep real_time_factor

It might show, for example:

.. code-block:: text

   real_time_factor: 0.80

In 1 real second, Gazebo simulates 0.80 s. A drive of 10 simulated seconds takes 10 / 0.80 = 12.5 real seconds.

.. dropdown:: More detail: the number in Gazebo's window

   The command's number is the speed of one 4 ms step, so it changes from message to message: 0.08 to 1.40 in one run of 209 messages. Gazebo's window shows a smoothed value, about 80 % in that run. Over the whole run, ``/clock`` advanced 17.03 s in 21.83 real seconds (17.03 / 21.83 = 0.78).

The `ROS 2 design article on time <https://design.ros2.org/articles/clock_and_time.html>`__ names the two clocks a node can read:

- System time: "``SystemTime`` will be directly tied to the system clock."
- ROS time: "``ROSTime`` is considered active when the parameter ``use_sim_time`` is set on the node." It then reports the latest ``/clock``.

In Code: now() and Two Kinds of Timer
"""""""""""""""""""""""""""""""""""""

A node reads its clock with ``now()``. A timer runs on one of two clocks. Lines 13 to 22 of ``include/l12_rosbot/sim_time_node.hpp`` (stage 5, commit ``6d2b94b``):

.. code-block:: cpp
   :linenos:
   :lineno-start: 13
   :emphasize-lines: 5, 8

   class SimTimeNode : public rclcpp::Node {
     public:
       SimTimeNode()
           : rclcpp::Node{"sim_time_node"},
             node_clock_timer_{create_timer(
                 std::chrono::seconds{1},
                 std::bind(&SimTimeNode::node_clock_callback, this))},
             wall_clock_timer_{create_wall_timer(
                 std::chrono::seconds{1},
                 std::bind(&SimTimeNode::wall_clock_callback, this))} {}

- Line 17: a timer "that uses the node clock to drive the callback" (``rclcpp/node.hpp``).
- Line 20: a timer "that uses the wall clock to drive the callback".
- Each callback logs ``now().seconds()``, the node clock's time.

The two timers side by side. Both callbacks read ``now()``, the node clock; what differs is the clock that fires each timer:

.. list-table::
   :header-rows: 1
   :widths: 22 41 37

   * -
     - ``create_timer`` (line 17)
     - ``create_wall_timer`` (line 20)
   * - Its clock
     - the node clock: ROS time
     - the computer's steady clock
   * - ``use_sim_time`` off
     - ROS time is the computer's time: every 1 s of it
     - fires every 1 s of the computer's time
   * - ``use_sim_time`` on
     - ROS time is Gazebo's ``/clock``: every 1 s of simulated time, after the first ``/clock``
     - still fires every 1 s of the computer's time
   * - on, Gazebo paused
     - stops
     - keeps firing, but ``now()`` stays the same

``rcl/time.h``: ROS time "will report the latest value reported by a ROS time source, or if a ROS time source is not active it reports the same as ``RCL_SYSTEM_TIME``"; the steady clock "reports a value from a monotonically increasing clock". So a control loop on ``create_timer`` pauses with Gazebo, while on ``create_wall_timer`` its callback keeps running while the world is paused.

**Use** ``create_timer``. Use ``create_wall_timer`` only for work that must run on the computer's clock even while the simulation is paused. This lecture's controllers use ``create_timer``, every 50 ms of the node clock. ``use_sim_time`` is off with a plain ``ros2 run``: the loop follows the computer's clock. It is on with ``controllers.yaml`` or a launch file: the loop follows ``/clock`` and stops while Gazebo is paused.

Run It: use_sim_time Off, Then On
"""""""""""""""""""""""""""""""""

Start the simulation first: it publishes the ``/clock`` the node reads. With ``use_sim_time`` off, the node also runs without it.

.. code-block:: bash

   ros2 run l12_rosbot sim_time_exe

.. code-block:: text

   [...]: create_wall_timer: now() = 1795198889.261 s
   [...]: create_timer:      now() = 1795198889.261 s

.. code-block:: bash

   ros2 run l12_rosbot sim_time_exe --ros-args -p use_sim_time:=true

The first four lines:

.. code-block:: text

   [...]: create_wall_timer: now() = 0.000 s
   [...]: create_wall_timer: now() = 0.000 s
   [...]: create_timer:      now() = 31.184 s
   [...]: create_wall_timer: now() = 31.896 s

- Off: both read the computer's clock, in seconds since 1 January 1970.
- On: the node subscribes to ``/clock``. Until the first message arrives, ``now()`` is 0: the article says ROS time "will return zero if nothing has been received."

Switch use_sim_time between off and on to see the first lines the node printed.

.. raw:: html
   :file: widgets/sim-time.html


Pause Gazebo: Which Timer Stops
"""""""""""""""""""""""""""""""

With ``use_sim_time`` on, the world was paused, then resumed 4.3 s later with the same command and ``pause: false``:

.. code-block:: bash

   gz service -s /world/patrol/control --reqtype gz.msgs.WorldControl \
     --reptype gz.msgs.Boolean --timeout 3000 --req 'pause: true'

.. list-table::
   :header-rows: 1
   :widths: 34 36 30

   * - Computer's clock (s)
     - What happened
     - ``now()`` (s)
   * - 1795198894.988
     - ``create_timer``
     - 32.000
   * - 1795198895.695
     - Gazebo paused
     -
   * - 1795198895.884 to 1795198899.884
     - ``create_wall_timer``, 5 times
     - 32.892, then 32.896
   * - 1795198899.992
     - Gazebo resumed
     -
   * - 1795198900.401
     - ``create_timer``
     - 33.000
   * - 1795198901.458
     - ``create_timer``
     - 34.000

.. admonition:: Conclusion
   :class: important

   A ``create_timer`` timer follows the simulation: it stopped while Gazebo was paused. A wall timer kept firing, and ``now()`` barely moved: 32.892 s, then 32.896 s.

.. dropdown:: More detail: Simulation time in this lecture's nodes
   :class-container: more-detail
   :icon: info

   - Every node that runs with Gazebo sets ``use_sim_time`` to true: its ``now()``, and so the stamp of every ``TwistStamped``, is then the simulation's time. :ref:`l12-use-sim-time` sets it for both controllers at once.
   - The controllers of the next section run ``control_callback`` on a ``create_timer`` timer. With ``use_sim_time`` on, it fires every 50 ms of simulation; when the simulation runs at 0.78 of real time, that is about 64 ms on the computer's clock (50 / 0.78 = 64.1 ms).
   - A node that must stay in step with the simulation, when it runs slower than real time or is paused, uses ``create_timer``.
   - Elapsed time comes from two readings of the same clock: ``(now() - start).seconds()``.

Replay the measured run, or watch it again, to see which timer stops while Gazebo is paused.

.. raw:: html
   :file: widgets/pause.html



Proportional Control
--------------------

The last section drove the ROSbot by hand with ``ros2 topic pub``. This section replaces your hand with a node: it reads where the ROSbot is and publishes velocity commands that turn it to a heading.

From a Terminal Command to a Node
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A controller node reads where the robot is and publishes a command, every 50 ms.

- ``ekf`` publishes the robot's pose, computed from the wheels and the IMU.
- ``heading_controller_node``, which you write in this section, reads the pose on ``/odometry/filtered`` and sends a ``/cmd_vel`` command that turns the ROSbot to a heading.
- ``differential_drive_controller`` turns each ``/cmd_vel`` command into wheel speeds.
- The graph shows only the nodes your node exchanges data with.

.. figure:: /_static/images/l12/control_graph.png
   :alt: ROS graph drawn top to bottom. A rounded box ekf has an arrow down to a rounded box heading_controller_node, labeled /odometry/filtered and nav_msgs/msg/Odometry. From heading_controller_node, an arrow down to a rounded box differential_drive_controller is labeled /cmd_vel and geometry_msgs/msg/TwistStamped.
   :align: center
   :width: 60%

   ``heading_controller_node`` receives the pose on ``/odometry/filtered`` and publishes the command on ``/cmd_vel``.


One Error, One Gain
^^^^^^^^^^^^^^^^^^^

A proportional controller sets a speed in proportion to the error that is left. One gain sets how strongly it reacts.

Feedback Control: Measure, Compare, Correct
"""""""""""""""""""""""""""""""""""""""""""

.. admonition:: Definition
   :class: definition

   A **feedback controller** measures the result of its own commands, compares it with the target, and uses the difference, the **error**, to choose the next command. It repeats this many times a second.

For the heading controller of this section, one pass of the loop is:

1. The target heading and the measured heading meet: their difference is the error :math:`e`.
2. The controller turns :math:`e` into a command :math:`u`, published on ``/cmd_vel``.
3. The ROSbot turns.
4. The odometry measures the heading it reached, on ``/odometry/filtered``. This measurement is the feedback: it goes back to step 1.

Feedback Controllers You Will Meet
""""""""""""""""""""""""""""""""""

They differ in how they turn the error into a command:

.. list-table::
   :header-rows: 1
   :widths: 15 47 38
   :class: compact-table

   * - Controller
     - The command
     - Where you meet it
   * - On-off
     - full on when the error is positive, full off when it is negative
     - a home thermostat: heater on while the room is colder than its target
   * - P
     - the error times a gain
     - this section's ``heading_controller_node``
   * - PI
     - P, plus a term from the error summed over time
     - a car's cruise control holding the speed uphill
   * - PID
     - PI, plus a term from how fast the error changes
     - motor speed loops; a drone holding its attitude
   * - MPC
     - predicts the next seconds with a model of the robot, then picks the best commands
     - self-driving cars following a path

MPC is model predictive control. P, PI and PID are the same family: PID with some gains set to 0.

.. dropdown:: More detail: the PID controller
   :class-container: more-detail
   :icon: info

   .. admonition:: Definition
      :class: definition

      A **PID controller** is a feedback controller whose control signal adds three terms: one in proportion to the error now (**P**), one to the error summed over time (**I**), and one to how fast the error changes (**D**).

   .. math::

      u = K_p\, e + K_i \sum e\,\Delta t + K_d\, \frac{e_k - e_{k-1}}{\Delta t}

   :math:`K_p`, :math:`K_i`, :math:`K_d` are the gains you choose. :math:`\Delta t` is the time between two commands (0.05 s here). :math:`e_k` and :math:`e_{k-1}` are the error now and one step before.

   **What each term does for a turn.** Each term reads the error in its own way. For a turn to a heading:

   .. list-table::
      :header-rows: 1
      :widths: 10 30 60
      :class: compact-table

      * - Term
        - Reacts to
        - Its job
      * - P
        - the error now
        - turn faster the farther the robot is from the target
      * - I
        - the error summed over time
        - keep pushing when a small error stays, for example when friction stops the turn short
      * - D
        - how fast the error changes
        - slow the turn early, so the robot does not overshoot

   This section's controller is P alone (:math:`K_i = K_d = 0`). It needs neither I nor D: in Step 4's run, it stopped 0.019 rad short of the target. The 0.019 rad left is inside the 0.02 rad tolerance, so I would add nothing, and there was no overshoot for D to slow.

   A controller always has the P term: P, PI, PD or PID. D alone sends nothing while the error holds still, so the turn never starts. I alone starts at zero and keeps pushing after the error reaches zero, so the robot passes the target.

What a Controller Does
""""""""""""""""""""""

A controller brings one measured value to a target. For a turn, the value is the robot's heading, and the target is the heading you want. It repeats four steps:

1. **Measure**: read the heading from the odometry.
2. **Compare**: compute the **error**, the target minus the heading.
3. **Command**: publish a turn rate computed from the error.
4. **Repeat** every 50 ms. The robot has turned a little, so the next error is smaller.

The loop stops when the error is smaller than a **tolerance**, a margin you choose. Without a tolerance, the loop would wait for an error of exactly 0, which the odometry never reads.

Click a step, or press Play, to see what each step adds to the picture.

.. raw:: html
   :file: widgets/loop.html


The Error of a Turn
"""""""""""""""""""

The error of a turn is the angle left to turn, the short way. A positive error means turn left (counterclockwise), a negative one, turn right. Headings are in radians, from -π to π.

Example: the robot faces 3.122 rad (179°), and the target is -90°, which is -1.571 rad.

1. Target minus heading: -1.571 - 3.122 = -4.693 rad. That is a turn right of 269°.
2. Turning left is shorter. Add one full turn, 2π = 6.283 rad: -4.693 + 6.283 = 1.590 rad, a turn left of 91°.
3. The error is 1.590 rad: the robot turns left 91°, past the 180° heading.

.. admonition:: The Shorter Way: Add or Remove 2π
   :class: important

   Target minus heading is between -2π and 2π. Past half a turn (π), the other way is shorter: add or remove one full turn. In pseudo code:

.. code-block:: python

   d = target - heading          # between -2*pi and 2*pi
   if d > pi:     d = d - 2*pi   # turn right instead
   elif d <= -pi: d = d + 2*pi   # turn left instead
   error = d                     # between -pi and pi

Move the heading and the target to see the error the short way round.

.. raw:: html
   :file: widgets/error.html


.. _l12-yaw-from-quaternion:

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

- ``siny_cosp`` is sin(yaw) × cos(pitch), and ``cosy_cosp`` is cos(yaw) × cos(pitch). On a flat floor the pitch is 0, so cos(pitch) = 1: ``atan2`` gets the sine and the cosine of the yaw. On a slope, cos(pitch) multiplies both numbers, and ``atan2`` uses only their ratio and signs, so the yaw stays the same (the pitch is between −90° and 90°, where cos(pitch) is positive).
- The same file holds ``angle_difference``, which computes the error of the last section.
- ROS 2 has the same conversion: ``tf2::getYaw(orientation)``, from ``tf2/utils.hpp`` and ``tf2_geometry_msgs/tf2_geometry_msgs.hpp``. It gives the same yaw; the node keeps its own function, so the package needs no tf2 yet.
- The :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` reading explains the quaternion and this formula.

Move the yaw to see the quaternion that gives it, and the yaw the function returns.

.. raw:: html
   :file: widgets/yaw.html


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

Change the gain and the error to see the command the controller sends.

.. raw:: html
   :file: widgets/law.html


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
             control_timer_{create_timer(
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

- Lines 13 to 16: the unnamed namespace keeps the four constants inside this file. Later, in the parameters section, they become data members, so you can change them without recompiling.
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
       constexpr double target_yaw{
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

- Lines 29 and 30: the target in rad, ``constexpr``: the compiler computes it once, not at each call.
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

Lines 53 and 54 install it, with ``distance_controller_exe``, the package's second controller, which the More detail box after Step 4 explains:

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

.. dropdown:: More detail: Drive a distance
   :class-container: more-detail
   :icon: info

   ``distance_controller_node`` drives the ROSbot straight ahead for one distance. Only the error changes: the distance left to drive.

   .. rubric:: The Error of a Drive

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

   .. rubric:: The Same Law on the Forward Speed

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

   .. rubric:: Run the Distance Controller

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

Replay the log of the turn, or step through it one line at a time.

.. raw:: html
   :file: widgets/turn-log.html


Proportional Control: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Compute an error: the angle left to turn, the short way.
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
- **Another robot or world.** In GP2, ``controller_node`` drives the GP1 stand-in robot and the ROSbot in Gazebo, each run with its world's checkpoints from ``params_stand_in.yaml`` or ``params_gazebo.yaml``.

.. admonition:: Conclusion
   :class: important

   Values that change with the task, the robot or the world belong outside the code: in parameters, which you set when the node starts or while it runs.

Switch between numbers in the code and parameters, and step through the three reasons.

.. raw:: html
   :file: widgets/why-params.html


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

A node must declare a parameter before it uses it. You declare each one with a default value, which sets its type, and then read its value. The listings of this subsection are from stage 2 (commit ``9434e00``), unless they say stage 4.

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

.. dropdown:: More detail: Why a node declares its parameters
   :class-container: more-detail
   :icon: info

   A node accepts only the parameters it declared. Two tries on ``heading_controller_node``:

   1. A misspelled name, while the node runs:

      .. code-block:: bash

         ros2 param set /heading_controller_node kp_lineer 2.0

      The command fails: "parameter 'kp_lineer' cannot be set because it was not declared".

   2. A parameter of the other node, given at start with ``-p kp_linear:=0.8``. The node starts with no message, and ``ros2 param get /heading_controller_node kp_linear`` answers "Parameter not set".

   .. admonition:: Conclusion
      :class: important

      A wrong name on the command line at start is dropped without a message. Check what the node has with ``ros2 param list``.

.. dropdown:: More detail: An array parameter: a list of headings
   :class-container: more-detail
   :icon: info

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

Pick a default for line 39 to see which type the parameter gets.

.. raw:: html
   :file: widgets/declare.html


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

Pick a command to see what it prints for the running node.

.. raw:: html
   :file: widgets/param-list.html


.. dropdown:: More detail: Command-line tools: dump
   :class-container: more-detail
   :icon: info

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

0.5 × 1.583 = 0.792 rad/s: the node uses the new gain from its first command.

.. note::

   Write a double with a decimal point. With ``-p kp_angular:=1``, an integer, the node stops at start with an ``InvalidParameterTypeException``: "Wrong parameter type, parameter {kp_angular} is of type {double}, setting it to {integer} is not allowed".

Pick the value of kp_angular to see what the node reads.

.. raw:: html
   :file: widgets/at-start.html


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

- Line 7: a key names a node; its values are under ``ros__parameters``. Lines 14 to 19 hold the package's other node.
- Line 3: the **wildcard** key ``/**`` matches every node.

From the package folder, ``l12_rosbot``:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe \
     --ros-args --params-file config/controllers.yaml

Pick a node to see which values it gets from the file.

.. raw:: html
   :file: widgets/yaml.html


.. _l12-use-sim-time:

use_sim_time for a Node That Runs with Gazebo
"""""""""""""""""""""""""""""""""""""""""""""

Gazebo publishes its own time on ``/clock`` (:ref:`l12-simulation-time`). With ``use_sim_time`` true, a node's clock follows ``/clock`` instead of the computer's clock: ``now()`` returns the simulation's time, so every ``TwistStamped`` stamp shows it too.

Every node has ``use_sim_time``, and it is false unless you set it:

- With ``controllers.yaml`` (the ``/**`` key): ``ros2 param get`` answers ``True``.
- With a plain ``ros2 run``: it answers ``False``.

.. admonition:: Conclusion
   :class: important

   Set ``use_sim_time`` to true for every node you run with Gazebo. The ``/**`` key of a parameter file does it for all of them.

Pick how the node was started to see its use_sim_time value.

.. raw:: html
   :file: widgets/use-sim-time.html


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

Pick how the launch file was started to see which parameter file the node gets.

.. raw:: html
   :file: widgets/launch-yaml.html


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

.. dropdown:: More detail: From a launch file: values written in it
   :class-container: more-detail
   :icon: info

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

Pick a run to read the time of each of its 90 degree turns.

.. raw:: html
   :file: widgets/gains.html


React to a Change
^^^^^^^^^^^^^^^^^

A node can run a callback when someone sets a parameter. The callback accepts or rejects the new value. The listings of this subsection are from stage 4 (commit ``94d4d64``). Stage 5 does not change these files.

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

   ``ros2 param set`` changes the stored value. The node read ``kp_angular`` once, in its constructor, so its commands do not change. So the node needs a callback that runs when a value is set.

Step through the measured log to see that the set changes the stored value only.

.. raw:: html
   :file: widgets/set-no-effect.html


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

.. dropdown:: More detail: The callback part that refuses ``target_headings_deg``
   :class-container: more-detail
   :icon: info

   The loop of the next part starts with this check. Lines 68 to 81 of ``heading_controller_node.cpp``:

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

The Callback, Part 1: Refuse a Bad Value
""""""""""""""""""""""""""""""""""""""""

Lines 82 to 96 of ``heading_controller_node.cpp``, the loop that checks each value:

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

Pick a parameter and a value to see what the callback answers.

.. raw:: html
   :file: widgets/validator.html


The Callback, Part 2: Store the New Values
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
- The callback refused ``target_headings_deg`` with the check of the More detail box above: the node never reads the list again.
- The turn to 180° took 6.40 s at gain 0.5. The gain changed during the next turn, which took 3.20 s. The last turn, at 1.5, took 2.70 s.

Replay the measured run to see the command change when the gain changes.

.. raw:: html
   :file: widgets/gain-change.html


Parameters: What You Can Do Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. admonition:: Summary
   :class: tip

   - Declare a parameter with a default value, and read it with ``get_parameter``.
   - List, get, set and dump the parameters of a running node.
   - Set parameters at start: with ``-p``, from a YAML file, or from a launch file.
   - Set ``use_sim_time`` for every node that runs with Gazebo.
   - Check and store a new value while the node runs, with a parameter callback.

Next Class
----------

- **Next lecture**: *L13: Frames and Transforms*. Coordinate frames, and broadcasting, listening to and debugging transforms.
- **Pre-work**: complete the L12 :doc:`exercises <l12_exercises>` and :doc:`quiz <l12_quiz>` on ReadTheDocs. The :doc:`GP2 instructions </assignments/gp2>` are on ReadTheDocs: start working on GP2 today. This lecture covers the simulation GP2 runs in, proportional control and parameters. Optional: the :doc:`Namespaces and Remapping </reading_material/remapping/remap_index>` reading, which runs two copies of the heading controller in two namespaces and renames topics, a node and a namespace with rules. Optional, beyond the course: the :doc:`Services and Actions </reading_material/services_actions/sa_index>` reading.
- **Required reading**:

  - `ROS 2 Jazzy: Parameters <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`__
  - :doc:`ROSbot Simulation </setup/rosbot_simulation>`
  - :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>`

.. raw:: html
   :file: widgets/_scripts.html
