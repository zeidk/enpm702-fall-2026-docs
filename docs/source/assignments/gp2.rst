.. _gp2:

====================================================
GP2: Patrol and Inspect in Gazebo
====================================================

Overview
--------

In this second and last group project, your team of three moves the
patrol robot of GP1 into Gazebo. A simulated Husarion ROSbot drives to
four checkpoints of a building, each on a curved path, and turns to face
its heading. At each checkpoint the mission node reads the lidar and
reports a door as open or closed, or a room as clear or blocked. It also
reads a second sensor, a logical camera, to find objects such as a fire
extinguisher, and reports where each one stands. There is no path
planning: the checkpoints are placed so the robot reaches each one
without a map. A closed door is reported, never driven through.

The heart of the project is one action, ``GoToCheckpoint``. Its server
holds a proportional controller that drives the robot to a checkpoint.
Its client, in the mission node, sends the goals one after another and
decides what to do with each result. Around it you add parameters in a
YAML file, two services, one TF frame per checkpoint, and a tf2
transform for the camera.

.. raw:: html

   <figure class="align-center">
     <video controls muted playsinline preload="metadata" width="100%"
            poster="../_static/videos/gp2/patrol_gazebo_poster.jpg"
            aria-label="A 50-second video of a Gazebo simulation, seen from above at an angle, sped up 1.5 times: a building with grey walls, a hall and two rooms. The small dark ROSbot drives along curved paths and stops on each of four blue discs, the checkpoints. It passes a brown crate, a closed red door and an open doorway, and finds an extinguisher, a person and a spill.">
       <source src="../_static/videos/gp2/patrol_gazebo.mp4" type="video/mp4">
     </video>
     <figcaption>The reference solution in Gazebo, sped up 1.5 times (50.5 s). The ROSbot drives on curved paths and stops on each of the four blue discs. It passes a crate, a closed red door and an open doorway, and finds an extinguisher, a person and a spill.</figcaption>
   </figure>

   <figure class="align-center">
     <video controls muted playsinline preload="metadata" width="100%"
            poster="../_static/videos/gp2/patrol_terminal_poster.jpg"
            aria-label="A 50-second video of three terminal panes, light text on a dark background, sped up 1.5 times. The top pane, mission_node, logs each goal it sends, each checkpoint result (clear, blocked, door closed, door open) and each object with its position. The middle pane prints the front range from the lidar once per second. The bottom pane prints the names of the objects the logical camera sees once per second.">
       <source src="../_static/videos/gp2/patrol_terminal.mp4" type="video/mp4">
     </video>
     <figcaption>The same run in the terminal, at the same speed. Top: the mission node's log. Middle: the lidar's front range, once per second. Bottom: the objects the logical camera sees, once per second. Play it next to the Gazebo video.</figcaption>
   </figure>

.. important::

   **Posted Tue, Nov 24, due Fri, Dec 11 at 11:59 pm. Worth 96 points.**
   The Thanksgiving recess (Nov 25 to 29) falls inside the two weeks.
   One submission per team. Each member emails a peer review within 48
   hours of the deadline. Your individual grade is 60 % the team grade
   and 40 % your peer review score, as the
   :ref:`syllabus <peer-evaluation>` explains.

.. important::

   **The requirements follow the lectures, so you can start today.**

   * **Week 1 (R1 to R6) needs only Lecture 12** (parameters, services,
     actions; Tue, Nov 24). It still runs against your GP1 stand-in
     robot, in a terminal. Merge R1 to R6 into ``main`` by Tue, Dec 1.
   * **Week 2 (R7 to R10) needs Lecture 13** (frames and TF; Tue, Dec 1).
     It moves the system to Gazebo Harmonic with the Husarion ROSbot and
     adds the logical camera.
   * **Lecture 14** (Tue, Dec 8, robot autonomy architecture) adds no
     requirement. It frames ``mission_node`` as the small decision layer
     between the sensors and the controller.

.. admonition:: Using AI on this assignment
   :class: important

   The course AI policy from
   :doc:`Lecture 1 </lectures/lecture1/l1_lecture>` applies here in full.
   In short:

   * You **may** use a tool such as TerpAI, ChatGPT, Claude, Gemini or
     Copilot to explain a concept, read a compiler error, suggest a way
     to debug something, or review code **you have already written**.
   * You **must** say so at the top of your ``README.md``: name the tool
     and describe in two or three sentences what you used it for.
     Disclosure carries no penalty. Undisclosed use is a violation of
     the Code of Academic Integrity.
   * You **may not** submit generated code that you cannot read,
     explain, and change. You are responsible for every line you hand
     in, and you may be asked to walk through any part of it and say why
     it works and what would break it.

   In a group project, this holds for every member and every part: each
   of you must be able to explain the parts your teammates wrote.

.. warning::

   **Share the code through GitHub, and agree on how before anyone
   writes a line.** Do not email zip files or send code over a chat:
   copies passed around by hand overwrite each other's work, and nothing
   records who wrote what. Only the zip file your team submits on Canvas
   is graded. The repository is for you.

   #. **One private repository.** One member creates it and adds the
      other two as collaborators. Nobody forks. Add a ``.gitignore``
      with ``build/``, ``install/`` and ``log/`` first.
   #. **Keep** ``main`` **working.** Nobody commits to it directly.
   #. **One branch per part**, for example ``params``, ``controller``
      and ``mission``. Commit small steps, and push every session.
   #. **Merge through a pull request.** A teammate reads it, builds it
      and approves it. Start each session from the latest ``main``.
   #. **Merge R1 first.** Every other branch needs the interfaces.

   The :doc:`Version Control </reading_material/version_control/vc_lecture>`
   reading covers branches, merging and conflicts.


From GP1
--------

You continue your own GP1 code. The ROSbot publishes the same topics as
the stand-in robot, so most of the system stays.

* **Kept:** ``patrol_log_node`` (still 1.5 s of work every 2 s),
  ``InspectionReport``, and ``stand_in_robot_node`` in Week 1 only.
* **Replaced:** ``navigation_node`` and the hard-coded checkpoint table
  become an action server with a proportional controller, and a YAML
  file. ``/emergency_stop`` and ``Arrival`` go away: a pause service and
  a cancel replace the stop, and the action result replaces the arrival.
* **Dropped:** the second robot and the namespaces. One robot in Gazebo.
* **Changed:** ``mission_node`` becomes the action client, reads a
  cone of beams and, in Gazebo, the logical camera. ``operator_node``
  calls services.
* **Added:** parameters, two services, one action, static frames,
  ``DetectedObject`` and ``gp2_bringup``.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Declare parameters and load them from a YAML file in a launch file.
2. Write service servers, and call them from the command line and a node.
3. Write an action server with feedback, cancel and a timeout, and a
   client that acts on each result.
4. Write a proportional controller that drives a robot to a pose.
5. Publish static frames, and use TF2 to move an object's position from
   the camera frame to ``odom``.
6. Decide from a lidar cone, find objects with a logical camera, and run
   the system in Gazebo.
7. Split a project among three people and show it in the peer review.


The World
---------

The patrol world is a building 20 m long and 10 m wide, with walls 1 m
high. All positions are in meters in the ``odom`` frame. The robot starts
at the origin, ``(0, 0)``, facing east (the positive x direction), and
``odom`` and the Gazebo world frame coincide.

* The building covers x from -3 to 17 and y from -3 to 7.
* The hall covers y from -3 to 2 along the whole length.
* Two rooms, each 5 m deep, lie north of the hall and are split at
  x = 7.
* Two doorways, each 3 m wide, are cut in the wall at y = 2. **Door 4**
  is at x = 3 and is open. **Door 3** is at x = 12 and is closed, with a
  red door in the way, in the patrol world.

The robot visits four checkpoints. The heading is the direction the robot
faces when it arrives: east is 0 rad, north is 1.5708 rad, south is
-1.5708 rad.

.. list-table::
   :header-rows: 1
   :widths: 8 22 12 38 20
   :class: compact-table

   * - Id
     - Position (x, y)
     - Faces
     - What the lidar and the camera find there
     - Kind
   * - 1
     - (5.0, -0.5)
     - east
     - A clear hall. The end wall is 12 m away. The camera sees the
       ``fire_extinguisher`` at (7.6, 1.3).
     - room
   * - 2
     - (9.5, -1.4)
     - south
     - A ``crate`` at (9.5, -2.4), so the room is blocked.
     - room
   * - 3
     - (12.0, 0.4)
     - north
     - Door 3, closed. The camera sees a ``person`` at (11.6, 1.45).
     - door
   * - 4
     - (3.0, 0.4)
     - north
     - Door 4, open. The camera sees a ``spill`` at (3.6, 1.3).
     - door

The table gives the positions you put in your YAML file. Every
checkpoint is at least 1.5 m from every wall. A second world, the
**swapped world**, exchanges doors 3 and 4, so door 3 is open and door 4
is closed. It has no ``fire_extinguisher`` and no ``person``. Your
program must report both worlds correctly.

The reference solution drives the patrol in 62.1 to 62.4 s of simulation
time over 21.7 to 21.8 m (five runs, both worlds), and its closest
approach to any wall is 1.34 m. Gazebo needs about 40 s to start, so wait for the
first pose before you send a goal.

The System
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Node
     - What it does
   * - ``patrol_services_node`` (A)
     - Serves ``set_paused`` and ``get_report``.
       Stores the reports. Publishes ``patrol_status`` at 2 Hz.
   * - ``operator_node`` (A)
     - Calls the two services at set times.
   * - ``controller_node`` (B)
     - Action server ``go_to_checkpoint``. Drives to the checkpoint with
       a proportional controller. Stops on an obstacle or a cancel.
   * - ``mission_node`` (C)
     - Action client. Sends the goals in order, decides from each result,
       checks the door, finds the objects, publishes
       ``inspection_report``.
   * - ``checkpoint_frames_node`` (A)
     - Broadcasts one static frame per checkpoint.
   * - ``patrol_log_node``
     - As in GP1. Runs with ``mission_node`` in one process.

The robot has two sensors. The lidar measures the distance to the nearest
surface in each direction, and you use it for the stop and for the door
or room decision. The second sensor is a **logical camera**, a Gazebo
sensor that reports the name and pose of every model in its view. It
stands in for an object detector, and no real robot has one. These are
the facts you need about it:

* ``gp2_bringup`` mounts it on the ROSbot, on a small rig joined to
  ``base_link``. The launch file publishes the static transform from
  ``base_link`` to the camera frame ``logical_camera_link``. The camera
  is 0.12 m ahead of and 0.20 m above ``base_link``.
* It publishes ``ros_gz_interfaces/msg/LogicalCameraImage`` on
  ``logical_camera`` at about 10 Hz. The view is 2.0 rad wide
  horizontally, and the range is 0.3 to 3.5 m.
* It reports every model whose origin is in the view, with its pose in
  ``logical_camera_link``. The message has a ``header``, the camera's own
  ``pose``, and a ``model`` array. Each element has a ``name`` and a
  ``pose``.
* It **also** lists the walls and the floor pads, and it sees through
  walls. A model name tells you what it is: only some are objects.

A trimmed ``ros2 topic echo`` shows what one image holds. The crate is
in front of the robot, a floor pad is nearer, and a wall is to the side:

.. code-block:: text

   header:
     frame_id: logical_camera_link
   model:
   - name: crate
     pose: position (1.58, 0.00, 0.20)
   - name: checkpoint_pad_2
     pose: position (0.58, 0.00, -0.19)
   - name: wall_south
     pose: position (2.18, -2.50, 0.30)

The interfaces:

* **Topics.** ``cmd_vel``, ``odometry/filtered`` (``Odometry``) and
  ``scan`` (``LaserScan``) come from the stand-in robot, then the ROSbot.
  On the ROSbot, ``cmd_vel`` takes ``geometry_msgs/msg/TwistStamped``.
  ``logical_camera`` (``LogicalCameraImage``) comes from Gazebo.
  ``inspection_report`` (``gp2_interfaces/msg/InspectionReport``) goes
  from ``mission_node`` to ``patrol_services_node`` and
  ``patrol_log_node``. ``patrol_status`` (``PatrolStatus``) goes from
  ``patrol_services_node`` to ``mission_node``.
* **Action.** ``go_to_checkpoint`` (``GoToCheckpoint``): server
  ``controller_node``, client ``mission_node``.
* **Services.** ``set_paused`` (``std_srvs/srv/SetBool``) and
  ``get_report`` (``GetReport``): server ``patrol_services_node``, client
  ``operator_node``.
* **Frames.** ``odom`` and ``base_link`` come from the ROSbot.
  ``logical_camera_link`` comes from the launch file of ``gp2_bringup``.
  ``checkpoint_frames_node`` publishes ``checkpoint_<id>``, with ``odom``
  as parent.
* **Parameters.** Per checkpoint: ``checkpoint_ids`` and ``kind``
  (integer arrays), ``x``, ``y``, ``heading`` and ``doorway_distance_m``
  (double arrays). Others: ``kp_linear``, ``kp_angular``,
  ``max_linear_mps``, ``max_angular_rps``, ``distance_tolerance_m``,
  ``yaw_tolerance_rad``, ``stop_range_m``, ``goal_timeout_s``,
  ``cone_half_angle_deg``, ``door_tolerance_m``, ``blocked_range_m`` and
  the angle of straight ahead in ``scan``. You also choose how to list the
  model names that are not objects.

The instructor provides ``gp2_bringup``: a package that starts Gazebo
with the ROSbot, the lidar and the logical camera in a world chosen by an
argument (the patrol world or the swapped world). It is in the course
repository, in ``rosbot_sim/``; :doc:`ROSbot Simulation </setup/rosbot_simulation>`
says how to install, build and launch it.

The instructor also provides a starter in the folder ``GP2/`` of the same
repository. Get both as you got GP1: run ``git fetch upstream`` and
``git merge upstream/main``. The starter holds ``gp2_interfaces`` and
``gp2_patrol``, each with a complete ``CMakeLists.txt`` and
``package.xml`` with ``TODO`` marks, and ``geometry.hpp``, the helpers of
GP1. Its ``README.md`` lists the steps in order. You build everything
else.

Team Roles
----------

* **A:** the interfaces, parameters, the two services and the
  checkpoint frames (R1, R2, R3, R7).
* **B:** the action server with the proportional controller, the
  scan-based stop, and the controller on the ROSbot (R4, R5, R8).
* **C:** the action client and decisions in ``mission_node``, the launch
  files, and the camera-to-``odom`` transform for the objects (R6, R9,
  R10).
* **All:** ``README.md``, ``CONTRIBUTIONS.md``, the demo (R11).

Every member must be able to explain every part, because the peer review
rates it. Review each other's pull requests.


Requirements
------------

The workspace has two packages, ``gp2_interfaces`` (CMake, interfaces
only) and ``gp2_patrol`` (C++, ``rclcpp``), plus ``gp2_bringup``. Nodes
end in ``_node``, executables in ``_exe``. Files are ``*_node.hpp``,
``*_node.cpp`` and ``*_main.cpp``. Define each constructor in its class
and every other method in the ``.cpp`` file.

Week 1 (Lecture 12, stand-in robot)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. dropdown:: R1: The interface package (Member A, Week 1)

   Merge it on day one. ``gp2_interfaces`` holds:

   * ``DetectedObject.msg``: ``string name`` and
     ``geometry_msgs/Point position``. The position is in the ``odom``
     frame.
   * ``InspectionReport.msg`` from GP1, with one more result constant,
     ``RESULT_NOT_REACHED`` (4), and a new field
     ``DetectedObject[] objects``. It is empty when the camera saw no
     object.
   * ``PatrolStatus.msg``: ``bool paused``.
   * ``action/GoToCheckpoint.action``. Goal: ``checkpoint_id``
     (``uint32``). Feedback: ``distance_left_m`` and
     ``heading_error_rad`` (``float32``). Result: ``outcome`` (``uint8``,
     constants ``OUTCOME_REACHED`` 0, ``OUTCOME_OBSTACLE`` 1,
     ``OUTCOME_CANCELLED`` 2, ``OUTCOME_TIMED_OUT`` 3) and
     ``final_distance_m``.
   * ``srv/GetReport.srv``: request ``checkpoint_id``; response ``found``
     and ``report``, the whole ``InspectionReport``, so the response
     carries ``objects`` too.

   Checked with ``ros2 interface show`` for each file.

.. dropdown:: R2: Parameters and the YAML files (Member A, Week 1)

   Every node declares its parameters with a default and reads no
   constant from the code. The checkpoint arrays sit under ``/**`` in
   the YAML file, so every node reads the same values:

   .. code-block:: yaml

      /**:
        ros__parameters:
          checkpoint_ids: [...]   # one value per checkpoint
          x: [...]

   Write ``params_stand_in.yaml`` with the GP1 checkpoint table and
   ``params_gazebo.yaml`` with the four checkpoints of the patrol world
   (the table in The World).
   The launch file loads the file named by an argument. The heading of
   each checkpoint faces its door. Checked with ``ros2 param get`` on
   two nodes, and by a changed value that takes effect with no rebuild.

.. dropdown:: R3: Services and the operator client (Member A, Week 1)

   ``patrol_services_node`` serves:

   * ``set_paused`` (``std_srvs/srv/SetBool``): ``data: true`` pauses and
     ``false`` resumes. The patrol starts paused. The response message
     says what happened, for example ``patrol resumed``.
   * ``get_report``: the latest ``InspectionReport`` of the checkpoint,
     or ``found: false``.

   The node publishes ``patrol_status`` at 2 Hz with the current
   ``paused`` value. Each service is called with ``ros2 service call``.
   ``operator_node`` calls both with a client and logs each response. It
   uses timers, never ``sleep``. It counts its times with the node clock,
   ``now()``: in Gazebo that is the simulation time, so each call happens
   at the same point of the patrol on every computer.

.. dropdown:: R4: The action server and the controller (Member B, Week 1)

   ``controller_node`` serves ``go_to_checkpoint``. It rejects an id with
   no checkpoint. For an accepted goal, a 20 Hz loop reads the pose from
   ``odometry/filtered`` and computes the distance left to the checkpoint
   and the bearing error, the angle between where the robot faces and the
   direction of the checkpoint. It publishes **both commands at once**, so
   the robot drives a curve:

   #. ``angular.z`` is ``kp_angular`` times the bearing error, at most
      ``max_angular_rps``.
   #. ``linear.x`` is the smaller of ``kp_linear`` times the distance left
      and ``max_linear_mps``, times the larger of 0 and the cosine of the
      bearing error. A robot that points away from the checkpoint turns
      on the spot, and one that points at it drives.
   #. When the distance is within ``distance_tolerance_m``, stop driving
      and turn on the spot to the checkpoint's heading, with the same
      angular gain.

   The goal succeeds when the distance is within ``distance_tolerance_m``
   and the heading within ``yaw_tolerance_rad``. Send feedback at 2 Hz.
   Checked with ``ros2 action send_goal --feedback`` on each checkpoint
   against the stand-in robot. Put your gains in the README. A start that
   worked in Gazebo: ``kp_linear`` 0.8, ``kp_angular`` 1.5,
   ``max_linear_mps`` 0.5, ``max_angular_rps`` 1.0,
   ``distance_tolerance_m`` 0.04 and ``yaw_tolerance_rad`` 0.025. With
   these, the robot's true position ended 0.014 to 0.056 m from each
   checkpoint, with its heading within 1.24 degrees (five runs). The
   tolerance applies to the odometry, which stopped 0.036 to 0.038 m
   away; the odometry and the true position differed by up to 0.023 m.

.. dropdown:: R5: Stop on an obstacle, cancel and timeout (Member B, Week 1)

   While driving, average the finite ranges of ``scan`` within
   ``cone_half_angle_deg`` of straight ahead. The index of straight ahead
   comes from a parameter, because it is not the same on every robot (see
   R8). A start that worked in Gazebo: a half angle of 10 degrees.

   * Below ``stop_range_m`` (0.35 m in the reference solution): stop,
     result ``OUTCOME_OBSTACLE``. ``stop_range_m`` is below every doorway
     distance, so a closed door in front of the checkpoint does not stop
     the robot.
   * **A cancel stops the robot**: publish a zero ``Twist``, result
     ``OUTCOME_CANCELLED``.
   * Longer than ``goal_timeout_s`` (90 s in the reference solution):
     stop, ``OUTCOME_TIMED_OUT``. The clock starts when the first pose
     arrives, not when Gazebo starts. Measure it with ``now()``, the
     node clock: in Gazebo it follows the simulation, so a computer that
     runs Gazebo slower than real time does not time out early.

   Checked with a ``ros2 topic pub`` of a short scan, a cancel in the
   middle of a drive (odometry stops changing), and a tiny timeout.

.. dropdown:: R6: The mission node: client and decisions (Member C, Week 1)

   ``mission_node`` sends goals 1, 2, ... one at a time, with
   asynchronous calls and callbacks. It never blocks. It runs with
   ``patrol_log_node`` in one ``MultiThreadedExecutor`` with 2 threads.
   With one thread, its callbacks would wait while the log node does its
   1.5 s of work, and a pause would cancel the goal up to 1.5 s late.
   It acts on ``patrol_status`` and on each result:

   * ``OUTCOME_REACHED``: average the cone ahead. At a door, a value no
     more than ``door_tolerance_m`` above the checkpoint's
     ``doorway_distance_m`` is ``RESULT_DOOR_CLOSED``, a longer one or no
     finite range is ``RESULT_DOOR_OPEN``. At a room, below
     ``blocked_range_m`` is ``RESULT_BLOCKED``, else ``RESULT_CLEAR``.
     The reference solution uses 1.55 m and 0.4 m at the two doors, and
     1.0 m for a blocked room.
   * ``OUTCOME_OBSTACLE``: ``RESULT_BLOCKED``. ``OUTCOME_TIMED_OUT``:
     ``RESULT_NOT_REACHED``. Report, then go to the next checkpoint.
   * Paused: cancel the active goal. Resumed: send that checkpoint again.

   Log ``checkpoint 3 (door): door closed, average 0.6 m`` (the format).
   Checked by the log from an ``operator_node`` run with the stand-in.

Week 2 (Lecture 13, Gazebo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. dropdown:: R7: Checkpoint frames (Member A, Week 2)

   ``checkpoint_frames_node`` reads the checkpoint parameters and
   broadcasts one static transform per checkpoint with
   ``StaticTransformBroadcaster``: ``checkpoint_1``, ... with ``odom`` as
   parent, the position from ``x`` and ``y``, and the heading as a
   quaternion with only ``z`` and ``w`` set. Checked with
   ``ros2 run tf2_ros tf2_echo base_link checkpoint_2``, which prints the
   checkpoint in the robot's frame, and with ``ros2 run tf2_tools
   view_frames``.

.. dropdown:: R8: The controller on the ROSbot (Member B, Week 2)

   Make the controller of R4 and R5 drive the ROSbot in Gazebo. Two
   things differ from the stand-in robot. ``cmd_vel`` takes
   ``geometry_msgs/msg/TwistStamped``, so the controller publishes that
   type with a header stamp. The lidar frame is turned by 180 degrees, so
   straight ahead is at plus or minus pi in ``scan``, not in the middle of
   ``ranges``: set the angle parameter of R5 in ``params_gazebo.yaml``.
   Tune the gains and tolerances for Gazebo and write the values in the
   README. Checked in Gazebo with ``ros2 action send_goal`` on each
   checkpoint: the robot ends within both tolerances.

.. dropdown:: R9: Launch files and the Gazebo run (Member C, Week 2)

   ``gp2_launch.py`` includes the ``gp2_bringup`` launch file (Gazebo, the
   ROSbot and one world, chosen by an argument), then starts the nodes
   with the YAML file of R2. It starts no stand-in node. ``mission_node``
   starts when ``controller_node`` has started, with an event handler.
   Checked in the patrol world and in the swapped world: the robot
   visits each checkpoint, and each door is reported correctly
   (``door open`` at a checkpoint whose door is open). Tune the door and
   room ranges (``door_tolerance_m``, ``blocked_range_m``) for Gazebo and
   write the values in the README.

.. dropdown:: R10: Detect objects with the logical camera (Member C, Week 2)

   At each checkpoint, after the door or room decision, ``mission_node``
   finds the objects in view and puts them in the report:

   #. Subscribe to ``logical_camera`` and keep the latest image. Use an
      image only if it is recent. If there is none, as with the stand-in
      robot, report no objects.
   #. Keep the models that are objects. Drop walls, floor pads, doors and
      the robot itself, which the camera also lists. Decide by name, and
      read the names from a ``ros2 topic echo`` in the world.
   #. For each object, transform its pose from ``logical_camera_link`` to
      ``odom`` with tf2 (a ``tf2_ros::Buffer`` and a ``TransformListener``).
      Never add the offsets by hand. The static transform from
      ``base_link`` to the camera frame comes from the launch file, and
      the robot's pose comes from ``odom``.
   #. Add one ``DetectedObject`` (the name and the position in ``odom``)
      per object to ``objects`` in the ``InspectionReport``, and log the
      names.

   Checked in the patrol world, where the objects are the ``fire_extinguisher``,
   the ``crate``, the ``person`` and the ``spill``, and in the swapped
   world, which has no ``fire_extinguisher`` and no ``person``. Compare each
   reported position with the world coordinates in The World. The
   reference solution is within 0.023 m of them (five runs). **Allow 0.1 m.** Call
   ``get_report`` and check that the response carries the objects.

.. dropdown:: R11: Build, demo and documentation (All)

   * ``colcon build`` with ``-Wall -Wextra`` and no warnings.
   * ``run_demo.sh`` runs one world and saves the log in ``evidence/``.
   * ``README.md``: roles, build and run, one section per member, the
     gains and ranges, the AI disclosure, and a paragraph on why
     ``mission_node`` is a decision layer (Lecture 14).
   * ``CONTRIBUTIONS.md``: for each member, what they wrote, tested and
     reviewed.

Tips
----

* **Wait for Gazebo.** It takes about 40 s to start. A node that looks
  for the first pose too early sees nothing. Give the controller a
  long wait for the first pose.
* **Publish the right type.** On the ROSbot, ``cmd_vel`` takes a
  ``TwistStamped``, not a ``Twist``.
* **Find straight ahead in the scan.** The lidar frame is turned by 180
  degrees, so the beam straight ahead is at plus or minus pi. Print the
  ``angle_min`` and ``angle_increment`` of one ``LaserScan`` and work out
  the index.
* **The camera sees too much.** It lists walls and floor pads, and it sees
  through walls. Filter by name.

How It Is Graded
----------------

.. list-table::
   :header-rows: 1
   :widths: 60 15 25
   :class: compact-table

   * - Requirement
     - Weight
     - Owner
   * - R1: Interfaces
     - 6 %
     - A
   * - R2: Parameters
     - 8 %
     - A
   * - R3: Services and the operator client
     - 12 %
     - A
   * - R4: Action server and controller
     - 16 %
     - B
   * - R5: Stop, cancel, timeout
     - 8 %
     - B
   * - R6: Mission node
     - 12 %
     - C
   * - R7: Checkpoint frames
     - 6 %
     - A
   * - R8: Controller on the ROSbot
     - 8 %
     - B
   * - R9: Launch files and Gazebo
     - 10 %
     - C
   * - R10: Object detection with the logical camera
     - 10 %
     - C
   * - R11: Build, demo, documentation
     - 4 %
     - All

Each member owns 32 % and the team shares 4 %. The rubric gives the team
grade. The :ref:`syllabus <peer-evaluation>` explains how the peer review
adjusts each member's grade.
