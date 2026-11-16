:orphan:

.. _gp2:

====================================================
GP2: Patrol and Inspect in Gazebo (DRAFT)
====================================================

Overview
--------

In this second and last group project, your team of three moves the
patrol robot of GP1 into Gazebo. A simulated Husarion ROSbot drives to
each checkpoint of a building and faces its door. The mission node then
reads the lidar and reports the door as open or closed. There is no path
planning: the world lets the robot reach every checkpoint in a straight
line, and the doors are along the walls. A closed door is reported, never
driven through.

The heart of the project is one action, ``GoToCheckpoint``. Its server
holds a proportional controller that drives the robot to a checkpoint.
Its client, in the mission node, sends the goals one after another and
decides what to do with each result. Around it you add parameters in a
YAML file, three services, and one TF frame per checkpoint.

.. raw:: html

   <figure class="align-center">
     <video controls muted playsinline preload="metadata" width="100%"
            poster="../_static/videos/gp2/patrol_gazebo_poster.jpg"
            aria-label="A 46-second video of a Gazebo simulation, seen from above at an angle: a small building with grey walls, a corridor and two rooms, a brown crate and a red closed door. A small four-wheeled ROSbot drives in straight lines to four blue discs on the floor, stopping at each one: facing the room on the left, facing the crate, facing the red door, and facing the open doorway.">
       <source src="../_static/videos/gp2/patrol_gazebo.mp4" type="video/mp4">
     </video>
     <figcaption>The reference solution in Gazebo, sped up 1.5 times. The ROSbot visits the four checkpoints and reports a clear room, a blocked room, a closed door and an open door.</figcaption>
   </figure>

.. warning::

   **Draft notes from the reference solution, to fold into the page.**
   On the simulated ROSbot, ``cmd_vel`` takes
   ``geometry_msgs/msg/TwistStamped``, not ``Twist``. The lidar is mounted
   turned 180 degrees, so the beam straight ahead is at plus or minus pi
   in ``scan``, not in the middle of ``ranges``.

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
     robot, in a terminal.
   * **Week 2 (R7 to R9) needs Lecture 13** (frames and TF; Tue, Dec 1).
     It moves the system to Gazebo Harmonic with the Husarion ROSbot.
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
* **Changed:** ``mission_node`` becomes the action client and reads a
  cone of beams. ``operator_node`` calls services.
* **Added:** parameters, three services, one action, static frames and
  ``gp2_bringup``.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Declare parameters and load them from a YAML file in a launch file.
2. Write service servers, and call them from the command line and a node.
3. Write an action server with feedback, cancel and a timeout, and a
   client that acts on each result.
4. Write a proportional controller that drives a robot to a pose.
5. Publish static frames and look up the robot's pose with TF2.
6. Decide from a lidar cone, and run the system in Gazebo.
7. Split a project among three people and show it in the peer review.


The System
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Node
     - What it does
   * - ``patrol_services_node`` (A)
     - Serves ``set_paused``, ``get_report`` and ``skip_checkpoint``.
       Stores the reports. Publishes ``patrol_status`` at 2 Hz.
   * - ``operator_node`` (A)
     - Calls the three services at set times.
   * - ``controller_node`` (B)
     - Action server ``go_to_checkpoint``. Drives to the checkpoint with
       a proportional controller. Stops on an obstacle or a cancel.
   * - ``mission_node`` (C)
     - Action client. Sends the goals in order, decides from each result,
       checks the door, publishes ``inspection_report``.
   * - ``checkpoint_frames_node`` (C)
     - Broadcasts one static frame per checkpoint.
   * - ``patrol_log_node``
     - As in GP1. Runs with ``mission_node`` in one process.

The interfaces:

* **Topics.** ``cmd_vel`` (``TwistStamped`` on the simulated ROSbot), ``odometry/filtered``
  (``Odometry``) and ``scan`` (``LaserScan``) come from the stand-in
  robot, then the ROSbot. ``inspection_report``
  (``gp2_interfaces/msg/InspectionReport``) goes from ``mission_node``
  to ``patrol_services_node`` and ``patrol_log_node``. ``patrol_status``
  (``PatrolStatus``) goes from ``patrol_services_node`` to
  ``mission_node``.
* **Action.** ``go_to_checkpoint`` (``GoToCheckpoint``): server
  ``controller_node``, client ``mission_node``.
* **Services.** ``set_paused`` (``std_srvs/srv/SetBool``),
  ``get_report`` (``GetReport``), ``skip_checkpoint``
  (``SkipCheckpoint``): server ``patrol_services_node``, client
  ``operator_node``.
* **Frames.** ``odom`` and ``base_link`` come from the ROSbot.
  ``checkpoint_frames_node`` publishes ``checkpoint_<id>``, with ``odom``
  as parent.
* **Parameters.** Per checkpoint: ``checkpoint_ids`` and ``kind``
  (integer arrays), ``x``, ``y``, ``heading`` and ``doorway_distance_m``
  (double arrays). Others: ``kp_linear``, ``kp_angular``,
  ``max_linear_mps``, ``distance_tolerance_m``, ``yaw_tolerance_rad``,
  ``stop_range_m``, ``goal_timeout_s``, ``cone_half_angle_deg``,
  ``door_tolerance_m`` and ``blocked_range_m``.

The instructor provides ``gp2_bringup`` [provided, name TBD]: a package
that starts Gazebo with the ROSbot in the patrol world, and the world
files, with some doors open and some closed. You build everything else.

Team Roles
----------

* **A:** parameters and the three services (R1, R2, R3).
* **B:** the action server with the proportional controller and the
  scan-based stop (R4, R5, R8).
* **C:** frames and TF, the action client and decisions in
  ``mission_node``, the launch files (R6, R7, R9).
* **All:** ``README.md``, ``CONTRIBUTIONS.md``, the demo (R10).

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

   * ``InspectionReport.msg`` from GP1, with two more result constants,
     ``RESULT_NOT_REACHED`` (4) and ``RESULT_SKIPPED`` (5).
   * ``PatrolStatus.msg``: ``bool paused`` and ``uint32[] skipped_ids``.
   * ``action/GoToCheckpoint.action``. Goal: ``checkpoint_id``
     (``uint32``). Feedback: ``distance_left_m`` and
     ``heading_error_rad`` (``float32``). Result: ``outcome`` (``uint8``,
     constants ``OUTCOME_REACHED`` 0, ``OUTCOME_OBSTACLE`` 1,
     ``OUTCOME_CANCELLED`` 2, ``OUTCOME_TIMED_OUT`` 3) and
     ``final_distance_m``.
   * ``srv/GetReport.srv``: request ``checkpoint_id``; response ``found``
     and ``report``. ``srv/SkipCheckpoint.srv``: request
     ``checkpoint_id``; response ``accepted`` and ``message``.

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
   ``params_gazebo.yaml`` with the floor plan of the patrol world [TBD].
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
   * ``skip_checkpoint``: accepts a known id that was not reported yet,
     and refuses the rest with a reason in ``message``.

   The node publishes ``patrol_status`` from the first two. Each
   service is called with ``ros2 service call``. ``operator_node`` calls
   all three with a client and logs each response. It uses timers, never
   ``sleep``.

.. dropdown:: R4: The action server and the controller (Member B, Week 1)

   ``controller_node`` serves ``go_to_checkpoint``. It rejects an id with
   no checkpoint. For an accepted goal, a 20 Hz loop reads the pose from
   ``odometry/filtered`` and publishes a ``Twist``:

   #. Turn toward the checkpoint: ``angular.z`` is ``kp_angular`` times
      the bearing error.
   #. Drive: ``linear.x`` is ``kp_linear`` times the distance left, at
      most ``max_linear_mps``, with the same turn correction.
   #. Turn to the checkpoint's heading, with the same gain.

   The goal succeeds when the distance is within ``distance_tolerance_m``
   and the heading within ``yaw_tolerance_rad``. Send feedback at 2 Hz.
   Checked with ``ros2 action send_goal --feedback`` on each checkpoint
   against the stand-in robot. Put your gains in the README.

.. dropdown:: R5: Stop on an obstacle, cancel and timeout (Member B, Week 1)

   While driving, average the finite ranges of ``scan`` within
   ``cone_half_angle_deg`` of straight ahead.

   * Below ``stop_range_m``: stop, result ``OUTCOME_OBSTACLE``.
     ``stop_range_m`` is below every doorway distance, so a closed door
     in front of the checkpoint does not stop the robot.
   * **A cancel stops the robot**: publish a zero ``Twist``, result
     ``OUTCOME_CANCELLED``.
   * Longer than ``goal_timeout_s``: stop, ``OUTCOME_TIMED_OUT``.

   Checked with a ``ros2 topic pub`` of a short scan, a cancel in the
   middle of a drive (odometry stops changing), and a tiny timeout.

.. dropdown:: R6: The mission node: client and decisions (Member C, Week 1)

   ``mission_node`` (with ``patrol_log_node`` in one
   ``MultiThreadedExecutor``) sends goals 1, 2, ... one at a time, with
   asynchronous calls and callbacks. It never blocks. It acts on
   ``patrol_status`` and on each result:

   * ``OUTCOME_REACHED``: average the cone ahead. At a door, a value no
     more than ``door_tolerance_m`` above the checkpoint's
     ``doorway_distance_m`` is ``RESULT_DOOR_CLOSED``, a longer one or no
     finite range is ``RESULT_DOOR_OPEN``. At a room, below
     ``blocked_range_m`` is ``RESULT_BLOCKED``, else ``RESULT_CLEAR``.
   * ``OUTCOME_OBSTACLE``: ``RESULT_BLOCKED``. ``OUTCOME_TIMED_OUT``:
     ``RESULT_NOT_REACHED``. Report, then go to the next checkpoint.
   * Paused: cancel the active goal. Resumed: send that checkpoint again.
     A skipped id gets ``RESULT_SKIPPED`` and no goal.

   Log ``checkpoint 3 (door): door closed, average 0.6 m`` (the format).
   Checked by the log from an ``operator_node`` run with the stand-in.

Week 2 (Lecture 13, Gazebo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. dropdown:: R7: Checkpoint frames (Member C, Week 2)

   ``checkpoint_frames_node`` reads the checkpoint parameters and
   broadcasts one static transform per checkpoint with
   ``StaticTransformBroadcaster``: ``checkpoint_1``, ... with ``odom`` as
   parent, the position from ``x`` and ``y``, and the heading as a
   quaternion with only ``z`` and ``w`` set. Checked with
   ``ros2 run tf2_ros tf2_echo base_link checkpoint_2``, which prints the
   checkpoint in the robot's frame, and with ``ros2 run tf2_tools
   view_frames``.

.. dropdown:: R8: The controller reads TF (Member B, Week 2)

   Replace the odometry pose of R4 with a TF lookup of ``checkpoint_<id>``
   in ``base_link``. Its position gives the distance left (its length) and
   the bearing error (``atan2`` of y and x). Its rotation gives the heading
   error. The three phases and the feedback stay. Checked in Gazebo: the
   robot ends within both tolerances, and ``tf2_echo`` agrees with the
   last feedback.

.. dropdown:: R9: Launch files and the Gazebo run (Member C, Week 2)

   ``gp2_launch.py`` includes the ``gp2_bringup`` launch file (Gazebo, the
   ROSbot and one world, chosen by an argument), then starts the nodes
   with the YAML file of R2. It starts no stand-in node. ``mission_node``
   starts when ``controller_node`` has started, with an event handler.
   Checked in every handed-out world: the robot visits each checkpoint,
   and each door is reported correctly (``door open`` at a checkpoint
   whose door is open). Tune the gains, tolerances and ranges for Gazebo
   and write the values in the README.

.. dropdown:: R10: Build, demo and documentation (All)

   * ``colcon build`` with ``-Wall -Wextra`` and no warnings.
   * ``run_demo.sh`` runs one world and saves the log in ``evidence/``.
   * ``README.md``: roles, build and run, one section per member, the
     gains and ranges, the AI disclosure, and a paragraph on why
     ``mission_node`` is a decision layer (Lecture 14).
   * ``CONTRIBUTIONS.md``: for each member, what they wrote, tested and
     reviewed.


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
     - 10 %
     - A
   * - R3: Services and the operator client
     - 16 %
     - A
   * - R4: Action server and controller
     - 16 %
     - B
   * - R5: Stop, cancel, timeout
     - 10 %
     - B
   * - R6: Mission node
     - 12 %
     - C
   * - R7: Checkpoint frames
     - 8 %
     - C
   * - R8: Controller on TF
     - 6 %
     - B
   * - R9: Launch files and Gazebo
     - 12 %
     - C
   * - R10: Build, demo, documentation
     - 4 %
     - All

The rubric gives the team grade. The :ref:`syllabus <peer-evaluation>`
explains how the peer review adjusts each member's grade.


Open Questions for the Instructor
---------------------------------

* **The stop topic is dropped.** ``/emergency_stop`` and ``StopCommand``
  go away, since pause and cancel do the job. The GP1 executor lesson
  survives only in ``patrol_log_node`` sharing a process. Is that right?
* **A separate services node and a status topic are my guess.** They give
  Member A a real part. The alternative is the services inside
  ``mission_node``, which merges A's and C's work.
* **The load is uneven.** Member C has four requirements, Member A little
  in Week 2. I suggest A also owns ``run_demo.sh`` and the per-world
  tuning. The weights are 32 % per member and 4 % shared.
* **Hardest to grade:** R5 and R9. Timing differs between computers.
  Grade the end pose, the outcomes and the logs in ``evidence/``.
* **Thanksgiving.** Week 1 has almost no class time. Do you want a graded
  Week 1 checkpoint, or only the advice to merge R1 to R6 by Dec 1?
* **The obstacle test.** The worlds let the robot drive straight. Should
  one world have a box on a path, so R5 can be tested in Gazebo?
* **Numbers are [TBD]:** checkpoint count and poses, doorway distances,
  gains, tolerances and ``goal_timeout_s``. The reference solution chose
  values for all of them (see its ``patrol.yaml``). In its runs, ``odom``
  under-reported travel by about 5 % (0.1 to 0.3 m at a checkpoint).
* **You provide:** ``gp2_bringup`` [provided, name TBD], the world files,
  the floor plan with checkpoint poses and doorway distances, the
  reference video, and starter ``CMakeLists.txt`` and ``package.xml``
  files [TBD].
