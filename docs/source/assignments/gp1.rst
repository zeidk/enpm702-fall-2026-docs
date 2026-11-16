.. _gp1:

====================================================
GP1: Patrol and Inspect
====================================================

Overview
--------

In this first group project, your team of three writes the software of a
patrol robot in ROS 2. The robot visits a list of four checkpoints in a
building. At each checkpoint it reads its range sensor and files one
inspection report: the checkpoint is clear or blocked, or, for a
doorway, the door is open or closed. A log node writes the patrol log,
and an operator can stop the robots at once and start them again.

There is no simulator in GP1. A stand-in robot node, written by your
team, plays the robot: it moves an imaginary robot when it receives
velocity commands, and it publishes odometry and a scan. Every node runs
in a terminal, and you check the system with its log lines and the
``ros2`` command-line tools. Two robots patrol at the same time, in the
namespaces ``robot_1`` and ``robot_2``.

GP2 runs the same nodes on a simulated ROSbot in Gazebo. That is why the
nodes of GP1 use the topic names and message types of the real robot:
the stand-in node is the only part you replace.

Everything in this assignment comes from Lectures 10 and 11: nodes,
publishers, subscribers and timers, then launch files, executors,
callback groups and custom interfaces. Parameters, services and actions
come later: do not use them in GP1.

.. important::

   **Posted Tue, Nov 17, due Tue, Nov 24 at 11:59 pm. Worth 44 points.**
   One submission per team. After the deadline, each member rates the
   other two in a peer review, due Wed, Nov 25 at 11:59 pm, the day
   before Thanksgiving. Your individual GP1 grade is 60 % the team grade and 40 %
   your peer review score, as the :ref:`syllabus <peer-evaluation>`
   explains.


.. warning::

   **Share the code through GitHub, and agree on how before anyone
   writes a line.** Do not email zip files to each other, and do not
   send code over WhatsApp or any chat. With three people, copies passed
   around by hand overwrite each other's work, nobody knows which copy
   is the current one, and there is no record of who wrote what. Only the
   zip file your team submits on Canvas is graded, so the repository is
   for you: it keeps the team's work in one place.

   A strategy that works for a team of three:

   #. **One private repository.** One member creates it on GitHub and
      adds the other two as collaborators (Settings, Collaborators).
      Nobody forks: all three clone the same repository.
   #. **Add a ``.gitignore`` first** that lists ``build/``, ``install/``
      and ``log/``, so nobody commits build output.
   #. **Keep ``main`` working.** ``main`` always builds. Nobody commits
      to it directly.
   #. **One branch per part.** Each member works on their own branch,
      named after their part, for example ``stand-in``, ``navigation`` and
      ``launch``. Commit small steps often, and push the branch at the
      end of each work session.
   #. **Merge through a pull request.** When a part builds, open a pull
      request into ``main``. A teammate reads it, builds it and approves
      it, then you merge. That review is also how each of you learns
      the parts you did not write.
   #. **Start each session from the latest ``main``.** Run
      ``git switch main`` and ``git pull``, then bring it into your
      branch with ``git switch <your-branch>`` and ``git merge main``.
      Small, frequent merges keep conflicts small.
   #. **Merge R1 first.** The three messages go into ``main`` on day one,
      because every other branch needs them.

   The :doc:`Version Control </reading_material/version_control/vc_lecture>`
   reading covers branches, merging and conflicts.


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


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Define custom message types, with constants, in their own interface
   package, and use them from another package.
2. Write nodes as classes that publish, subscribe and run timers, and
   use relative and absolute topic names.
3. Simulate a sensor and a robot with a node, so other nodes can run
   without hardware.
4. Choose between a single-threaded and a multi-threaded executor, and
   show the difference with timestamps from your own runs.
5. Start two copies of a system with Python launch files that use an
   include, launch arguments, conditions, groups with namespaces, and
   event handlers.
6. Split a ROS 2 project among three people, and build, test and
   document it as one system.


The Patrol
----------

.. raw:: html

   <figure class="align-center">
     <video controls autoplay muted loop playsinline preload="metadata" width="100%"
            poster="../_static/videos/gp1/patrol_poster.jpg"
            aria-label="A 30-second looping animation: an isometric grey cutaway of a building floor where a small four-wheeled robot patrols four numbered checkpoints, sweeping a lidar cone and showing a report card at each: a clear room, a room blocked by a crate, a closed red door, and an open doorway. It pauses once for an operator stop, then returns home.">
       <source src="../_static/videos/gp1/patrol.mp4" type="video/mp4">
     </video>
     <figcaption>The robot inspects four checkpoints and reports each one. In GP1 the robot is a stand-in node in a terminal; in GP2 it is a ROSbot in Gazebo.</figcaption>
   </figure>

Every robot has the same nodes, in its own namespace. One operator node,
at the root namespace, talks to every robot.

.. list-table::
   :header-rows: 1
   :widths: 24 76
   :class: compact-table

   * - Node
     - What it does
   * - ``stand_in_robot_node``
     - Subscribes to ``cmd_vel``, moves an imaginary robot, and publishes
       ``odometry/filtered`` and ``scan``. The scan comes from a table
       that depends on where the robot stands (R2).
   * - ``navigation_node``
     - Drives the robot through the checkpoints, using only odometry. At
       each checkpoint it announces the arrival and waits for the report.
       On STOP it publishes a zero velocity at once.
   * - ``mission_node``
     - Reads the scan at each arrival and publishes the inspection
       report: clear, blocked, door open or door closed.
   * - ``patrol_log_node``
     - Counts the reports. Every 2 s it writes the patrol log, which
       takes 1.5 s of work.
   * - ``operator_node``
     - Sends STOP to every robot, then RESUME, on ``/emergency_stop``.

The topics of one robot, with the operator's:

.. list-table::
   :header-rows: 1
   :widths: 26 36 38
   :class: compact-table

   * - Topic (relative to the robot)
     - Message type
     - Publisher; subscribers
   * - ``cmd_vel``
     - ``geometry_msgs/msg/Twist``
     - ``navigation_node``; ``stand_in_robot_node``
   * - ``odometry/filtered``
     - ``nav_msgs/msg/Odometry``
     - ``stand_in_robot_node``; ``navigation_node``
   * - ``scan``
     - ``sensor_msgs/msg/LaserScan``
     - ``stand_in_robot_node``; ``mission_node``
   * - ``arrival``
     - ``gp1_interfaces/msg/Arrival``
     - ``navigation_node``; ``mission_node``
   * - ``inspection_report``
     - ``gp1_interfaces/msg/InspectionReport``
     - ``mission_node``; ``navigation_node``, ``patrol_log_node``
   * - ``/emergency_stop`` (absolute)
     - ``gp1_interfaces/msg/StopCommand``
     - ``operator_node``; ``navigation_node`` of every robot

``navigation_node`` and ``patrol_log_node`` of one robot run in **one
process**. R5 decides how that process runs their callbacks, so that a
STOP reaches the navigation node at once, even while the log node is in
the middle of its 1.5 s of work.

The four checkpoints are the same for both robots. The positions are in
meters, in the robot's odometry frame, which starts at the origin. The
ranges are what the stand-in scan returns straight ahead when the robot
is within 0.3 m of the checkpoint. This table is chosen for the
assignment.

.. list-table::
   :header-rows: 1
   :widths: 14 12 12 14 48
   :class: compact-table

   * - Checkpoint
     - x
     - y
     - Kind
     - Stand-in range straight ahead
   * - 1
     - 2.0
     - 0.0
     - room
     - 4.0 m (long): the room is clear
   * - 2
     - 2.0
     - 2.0
     - room
     - 0.6 m (short): something blocks the room
   * - 3
     - 0.0
     - 2.0
     - door
     - 0.6 m (short): the door is closed
   * - 4
     - 0.0
     - 4.0
     - door
     - 4.0 m (long): the door is open

Away from every checkpoint, the stand-in scan returns 4.0 m.


Team Roles
----------

Each member owns one part of the project and is graded on it as part of
the team grade. Agree on the message definitions (R1) first: every other
part depends on them.

.. list-table::
   :header-rows: 1
   :widths: 14 56 30
   :class: compact-table

   * - Member
     - Owns
     - Requirements
   * - A
     - The interface package, ``stand_in_robot_node``, ``patrol_log_node``
     - R1, R2, R3
   * - B
     - ``navigation_node``, the two patrol executables, the timing
       evidence
     - R4, R5
   * - C
     - ``mission_node``, ``operator_node``, the launch files, the demo
       script
     - R6, R7
   * - All
     - The build, ``README.md``, ``CONTRIBUTIONS.md``
     - R8

* Keep the project in one GitHub repository, as the box at the top of
  this page describes.
* Each member writes the ``README.md`` section of their part.
* ``CONTRIBUTIONS.md`` lists, for each member, what they wrote, tested
  and reviewed.
* Ownership is not a wall. Review each other's code, and help when a
  teammate is stuck. Every member must be able to explain every part of
  the submission: the peer review rates it.


Starter Package
---------------

The instructor provides a starter package in the course ROS repository,
in the folder ``GP1/``. Get it as you got the lecture code: run
``git fetch upstream`` and ``git merge upstream/main``. It holds:

* ``gp1_interfaces`` and ``gp1_patrol``, each with a complete
  ``CMakeLists.txt`` and ``package.xml``. They contain ``TODO`` marks:
  the list of messages, the executables you uncomment as you write each
  source file, and the maintainers.
* Two headers in ``gp1_patrol/include/gp1_patrol/``:
  ``checkpoints.hpp``, the checkpoint table (``kCheckpoints``), and
  ``geometry.hpp``, six helper functions: ``yaw_from_quaternion``,
  ``quaternion_from_yaw``, ``distance_between``, ``bearing_between``,
  ``wrap_angle`` and ``angle_difference``. Each one is documented in the
  header. ``checkpoints.hpp`` uses ``KIND_ROOM`` and ``KIND_DOOR`` from
  your ``Arrival`` message, so it compiles once R1 is done.

Everything else is your team's work: every node, every message file,
every ``main``, and both launch files.


Requirements
------------

The project is a ROS 2 Jazzy workspace with two packages:
``gp1_interfaces`` (CMake, messages only) and ``gp1_patrol`` (C++,
``rclcpp``). Follow the course naming: nodes end in ``_node``,
executables in ``_exe``; files are ``*_node.hpp``, ``*_node.cpp`` and
``*_main.cpp``. Define each constructor in its class and every other
method in the ``.cpp`` file.

.. dropdown:: R1: The interface package (Member A)
   :open:

   Create ``gp1_interfaces`` with three messages. Each message has a
   comment line at the top, and each field and constant has a comment.
   The constants are ``uint8``.

   * ``Arrival.msg``: constants ``KIND_ROOM`` (0) and ``KIND_DOOR`` (1);
     fields ``header``, ``checkpoint_id`` (``uint32``, 1 to 4) and
     ``kind``. The robot publishes it when it reaches a checkpoint.
   * ``InspectionReport.msg``: constants ``RESULT_CLEAR`` (0),
     ``RESULT_BLOCKED`` (1), ``RESULT_DOOR_OPEN`` (2) and
     ``RESULT_DOOR_CLOSED`` (3); fields ``header``, ``checkpoint_id``,
     ``result`` and ``range_m`` (``float32``, the range in meters that
     the decision used).
   * ``StopCommand.msg``: constants ``STOP`` (0) and ``RESUME`` (1);
     fields ``header``, ``command`` and ``reason`` (``string``, why the
     operator sent the command). ``header.stamp`` is the time the
     command was sent: the receiver uses it to measure the delay.

   Check each message with ``ros2 interface show``, and check that a
   second package builds against ``gp1_interfaces``.

.. dropdown:: R2: stand_in_robot_node (Member A)

   Executable ``stand_in_robot_exe``. The node plays the real robot, so
   it uses the real robot's topic names (relative).

   * Subscribes to ``cmd_vel``. A 20 Hz timer moves the imaginary robot:
     the pose changes by ``linear.x`` and ``angular.z`` times the time
     since the last tick. The robot starts at the origin, facing +x.
   * Publishes ``odometry/filtered`` at 20 Hz with the position, and the
     heading as a quaternion with only ``z`` and ``w`` set.
   * Publishes ``scan`` at 5 Hz, with three beams straight ahead:
     ``angle_min`` -0.1 rad, ``angle_max`` 0.1 rad, ``angle_increment``
     0.1 rad, ``range_min`` 0.1 m, ``range_max`` 10.0 m. All three
     ranges follow the checkpoint table above.
   * Sets ``header.stamp`` of both messages to ``now()``.
   * Logs once each time the robot comes within 0.3 m of a checkpoint:
     ``stand-in robot near checkpoint 3``.

   Use the checkpoint table in ``checkpoints.hpp`` and the helpers in
   ``geometry.hpp`` for the heading and the quaternion; do not write
   that math again. Check the node by publishing a
   ``cmd_vel`` with ``ros2 topic pub`` and reading ``odometry/filtered``
   and ``scan`` with ``ros2 topic echo``.

.. dropdown:: R3: patrol_log_node (Member A)

   ``patrol_log_node`` subscribes to ``inspection_report`` and counts the
   reports per result.

   * A 2 s timer writes the patrol log. The callback calls
     ``std::this_thread::sleep_for`` for 1.5 s in place of real work,
     then logs the four counts:
     ``patrol log: clear 1, blocked 1, door open 0, door closed 1``.
   * The subscription and the timer share the counts: both stay in the
     node's default callback group.

   The node has no executable of its own: the patrol executables of R5
   run it. Check it with the log line after each report.

.. dropdown:: R4: navigation_node (Member B)

   ``navigation_node`` drives through checkpoints 1 to 4, in order, using
   only ``odometry/filtered``. It does not use a controller with gain:
   it turns, then drives.

   * A 10 Hz timer decides the command. If the heading differs from the
     bearing to the checkpoint by more than 0.1 rad, publish only
     ``angular.z`` of 0.5 rad/s in the right direction. Otherwise publish
     only ``linear.x`` of 0.3 m/s. Within 0.15 m, publish zero. Take the
     checkpoints from ``checkpoints.hpp``, and the yaw, the distance, the
     bearing and the wrapped heading difference from the helpers in
     ``geometry.hpp``, so the robot turns the short way.
   * On arrival, publish ``Arrival`` and log ``arrived at checkpoint 2``.
     Wait for the ``InspectionReport`` with the same ``checkpoint_id``,
     then go to the next checkpoint. A report with another
     ``checkpoint_id`` is ignored. After checkpoint 4, log
     ``patrol complete``.
   * Subscribe to the absolute topic ``/emergency_stop``. On STOP, publish
     a zero ``Twist`` inside the callback, and stay stopped. On RESUME,
     continue. Log each command and how long it took to arrive: the time
     now minus ``header.stamp``, in milliseconds, with one decimal:
     ``STOP (operator stop) received 0.6 ms after it was sent``.
     ``rclcpp::Time{msg.header.stamp}`` turns the stamp into a time you
     can subtract from ``now()``.

   Check the arrival and report log lines in order, and check that the
   robot does not move (odometry unchanged) between a STOP and the next
   RESUME.

.. dropdown:: R5: Two executables and the timing evidence (Member B)

   One patrol process runs one robot's ``navigation_node`` and
   ``patrol_log_node``. Write it twice:

   * ``patrol_single_exe`` (``src/patrol_single_main.cpp``): both nodes
     in one ``SingleThreadedExecutor``.
   * ``patrol_exe`` (``src/patrol_main.cpp``): both nodes in one
     ``MultiThreadedExecutor`` with 2 threads
     (``rclcpp::ExecutorOptions{}, 2``).

   Run each one **three times** with the stand-in robot, the mission node
   and the operator, until the RESUME. With ``patrol_single_exe`` the
   robot may never reach checkpoint 1: that is part of what you explain.
   Keep every log in ``evidence/`` and fill this table in ``README.md``
   from the STOP line, ``STOP ... received ... ms after it was sent``:

   .. list-table::
      :header-rows: 1
      :widths: 20 40 40
      :class: compact-table

      * - Run
        - STOP delay, ``patrol_single_exe`` (ms)
        - STOP delay, ``patrol_exe`` (ms)
      * - 1 to 5
        - from your logs
        - from your logs

   Answer these in ``README.md``, in a few sentences each, with your
   numbers:

   1. Why does the STOP wait in ``patrol_single_exe``, and which callback
      does it wait for?
   2. Why does it not wait in ``patrol_exe``, when you made no callback
      group? (Lecture 11: which group does each node's callback join?)
   3. Why do the navigation node's callbacks stay in one mutually
      exclusive group? Say what could go wrong in a reentrant group.
   4. Why does the robot fail to arrive in ``patrol_single_exe``?

   The difference between the two columns of the table must show.
   ``patrol_launch.py`` (R7) starts ``patrol_exe``.

.. dropdown:: R6: mission_node and operator_node (Member C)

   ``mission_node`` (executable ``mission_exe``) keeps the latest
   ``scan``. On each ``Arrival`` it reads the middle beam,
   ``ranges[ranges.size() / 2]``, and publishes an ``InspectionReport``:

   * ``KIND_ROOM``: ``RESULT_BLOCKED`` if the range is under 1.0 m,
     otherwise ``RESULT_CLEAR``.
   * ``KIND_DOOR``: ``RESULT_DOOR_CLOSED`` if the range is under 1.0 m,
     otherwise ``RESULT_DOOR_OPEN``.
   * Log one line: ``checkpoint 3 (door): door closed, range 0.6 m``.

   ``operator_node`` (executable ``operator_exe``) runs at the root
   namespace. 13 s after it starts, it sends STOP with the reason
   ``operator stop``. Five seconds later it sends RESUME with the
   reason ``operator resume``. It uses timers, not ``sleep``. It logs each
   command: ``sent STOP (operator stop)``. Check the log lines:
   checkpoint 3 reports ``door closed`` and checkpoint 4 reports
   ``door open``.

.. dropdown:: R7: The launch files (Member C)

   Two launch files, in ``gp1_patrol/launch/``, installed by
   ``CMakeLists.txt``.

   Two tools these files need were not shown in class and are in the
   Lecture 11 notes: :ref:`groups with a condition <l11-groups-with-a-condition>`
   (for ``robot_2``) and :ref:`event handlers <l11-launch-events>`
   (``OnProcessStart``, ``OnShutdown``). Read both sections before you
   start.

   ``robots_launch.py`` starts the robots.

   * A launch argument ``two_robots``, ``false`` by default.
   * A helper function that returns one robot: a group with the robot's
     namespace, its ``patrol_exe`` and ``stand_in_robot_exe``, and an
     event handler that starts its ``mission_exe`` once the patrol
     process has started, with a ``LogInfo``
     (``robot_1 patrol started, starting mission``). The mission node
     must run in the robot's namespace too (see the `Tips`_).
   * ``robot_1`` always starts; ``robot_2`` starts only when
     ``two_robots`` is ``true``.

   ``patrol_launch.py`` starts the whole patrol.

   * It includes ``robots_launch.py``.
   * A launch argument ``with_operator``, ``true`` by default, decides
     whether ``operator_exe`` starts.
   * A ``LogInfo`` prints both arguments:
     ``two_robots = false, with_operator = true``.
   * An event handler logs ``Patrol stopped`` when the launch shuts
     down.

   ``ros2 launch gp1_patrol patrol_launch.py two_robots:=true`` must
   start both robots, although ``two_robots`` is declared in the
   included file. Check every node's full name with ``ros2 node list``:
   every robot node has the namespace of its robot, including the node
   that the event handler starts.

.. dropdown:: R8: Build, demo script and documentation (All)

   * ``colcon build`` builds both packages with ``-Wall -Wextra`` and no
     warnings.
   * ``run_demo.sh``, at the workspace root (Member C): sources the
     workspace, runs ``patrol_launch.py`` with two robots for 75 s
     (``timeout -s INT 75``), saves the output in ``evidence/demo.log``
     (creating ``evidence/`` if needed), and prints the STOP and RESUME
     lines with ``ms after`` and the ``patrol complete`` lines. A full
     patrol takes about 40 s, so 75 s is long enough for both robots to
     finish.
   * Both ``package.xml`` files list all three team members as
     maintainers, one ``<maintainer email="...">Name</maintainer>``
     line per member, in place of the starter's placeholder.
   * ``README.md``: the team's names and roles, how to build and run,
     one section per member about their part, the R5 table and answers,
     and your AI disclosure if you used a tool.
   * ``CONTRIBUTIONS.md``: for each member, what they wrote, tested and
     reviewed.


Expected Output
---------------

Your timestamps differ. The order and the text of the lines do not. This
is one robot with ``patrol_exe`` (``two_robots`` is ``false``), cut to
the important lines. A ``[...]`` stands for a timestamp. Between these
lines, ``patrol_log_node`` writes its log every 2 s.

.. code-block:: text

   [INFO] [launch.user]: two_robots = false, with_operator = true
   [INFO] [launch.user]: robot_1 patrol started, starting mission
   [stand_in_robot_exe-2] [INFO] [...] [robot_1.stand_in_robot_node]: stand-in robot near checkpoint 1
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: arrived at checkpoint 1
   [mission_exe-4] [INFO] [...] [robot_1.mission_node]: checkpoint 1 (room): clear, range 4.0 m
   [operator_exe-3] [INFO] [...] [operator_node]: sent STOP (operator stop)
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: STOP (operator stop) received 0.6 ms after it was sent
   [operator_exe-3] [INFO] [...] [operator_node]: sent RESUME (operator resume)
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: RESUME (operator resume) received 0.5 ms after it was sent
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: arrived at checkpoint 2
   [mission_exe-4] [INFO] [...] [robot_1.mission_node]: checkpoint 2 (room): blocked, range 0.6 m
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: arrived at checkpoint 3
   [mission_exe-4] [INFO] [...] [robot_1.mission_node]: checkpoint 3 (door): door closed, range 0.6 m
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: arrived at checkpoint 4
   [mission_exe-4] [INFO] [...] [robot_1.mission_node]: checkpoint 4 (door): door open, range 4.0 m
   [patrol_exe-1] [INFO] [...] [robot_1.navigation_node]: patrol complete

The last patrol log line of that run:

.. code-block:: text

   [patrol_exe-1] [INFO] [...] [robot_1.patrol_log_node]: patrol log: clear 1, blocked 1, door open 1, door closed 1

The nodes of ``two_robots:=true`` with the operator:

.. code-block:: console

   $ ros2 node list
   /operator_node
   /robot_1/mission_node
   /robot_1/navigation_node
   /robot_1/patrol_log_node
   /robot_1/stand_in_robot_node
   /robot_2/mission_node
   /robot_2/navigation_node
   /robot_2/patrol_log_node
   /robot_2/stand_in_robot_node

The instructor's numbers come from five runs of each executable, more than you do. The STOP waited 500.0 to
517.7 ms in ``patrol_single_exe`` and 0.2 to 0.7 ms in ``patrol_exe``.
Your numbers depend on when the STOP falls in the log node's 1.5 s of
work, so they can differ; the difference between the two executables
must show.


Deliverables
------------

Submit **one zip file per team** on Canvas, named ``gp1_team<N>.zip``
with your team number, for example ``gp1_team4.zip``. Only this zip
file is graded.

.. code-block:: text

   gp1_team4/
   ├── README.md
   ├── CONTRIBUTIONS.md
   ├── run_demo.sh
   ├── evidence/              # the six R5 logs and demo.log
   └── src/
       ├── gp1_interfaces/
       └── gp1_patrol/

.. warning::

   Do **not** include ``build/``, ``install/`` or ``log/``, a ``.git``
   folder, or editor folders such as ``.vscode/``. A submission that does
   not build cannot be graded.


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 34 12 54
   :class: compact-table

   * - Requirement
     - Weight
     - What is checked
   * - R1: Interface package (A)
     - 8 %
     - Three messages, constants, fields and comments.
   * - R2: ``stand_in_robot_node`` (A)
     - 12 %
     - Motion from ``cmd_vel``, odometry, the scan table.
   * - R3: ``patrol_log_node`` (A)
     - 8 %
     - Counts, the slow timer, the log line.
   * - R4: ``navigation_node`` (B)
     - 14 %
     - Order of the checkpoints, wait for the report, immediate STOP.
   * - R5: Executors and timing (B)
     - 15 %
     - Both executables, six logs, the table, answers that use your
       numbers.
   * - R6: ``mission_node`` and ``operator_node`` (C)
     - 15 %
     - The four results at the four checkpoints, the timed commands.
   * - R7: Launch files (C)
     - 18 %
     - Include, arguments, condition, namespaces, event handlers.
   * - R8: Build, demo script, documentation (all)
     - 10 %
     - No warnings, the demo log, ``README.md``, ``CONTRIBUTIONS.md``.
       Each ``package.xml`` lists all three members as maintainers.

Code that ignores the course conventions loses marks in the requirement
where it appears: uniform initialization, ``snake_case``, names that say
what the value is, and ``'\n'`` rather than ``std::endl``.

The rubric gives the **team** grade. Your individual grade combines it
with your peer review score, as the
:ref:`syllabus <peer-evaluation>` explains.


Peer Review
-----------

After the deadline, each member emails a peer evaluation of the other
two, and of themselves, by **Wed, Nov 25 at 11:59 pm**. That is one day
after the deadline, not the syllabus's usual 48 hours, so that nothing is
due on Thanksgiving.
The form and how the score is computed are in the
:ref:`syllabus <peer-evaluation>`. The subject line is
``[ENPM702] GP1 peer evaluation - Team X``, with your team number for X. A member who does not send one loses their own peer
review score for GP1.


Tips
----

* **Use your own ROS domain.** On a shared network, every team's nodes
  see each other. Before you run anything, each member sets
  ``export ROS_DOMAIN_ID=<N>``, with your team number, in every terminal.
  Check with ``ros2 node list`` that you see only your own nodes.
* **Build the interfaces first.** ``colcon build --packages-up-to
  gp1_patrol`` builds ``gp1_interfaces`` before the package that uses
  it.
* **Start with one robot and no launch file.** Run the stand-in robot in
  ``robot_1`` from the command line
  (``ros2 run gp1_patrol stand_in_robot_exe --ros-args -r __ns:=/robot_1``),
  then the patrol executable, the mission node and the operator the same
  way. Write the launch files once the nodes work.
* **A node started by an event handler is outside the group.** The
  handler runs later, when the patrol process has started, outside the
  group that pushed the robot's namespace. Give the mission node its own
  ``GroupAction`` with ``PushROSNamespace`` inside ``on_start``, or it
  starts as ``/mission_node``. Check with ``ros2 node list``.
* **Agree on R1 on day one.** Every other part uses the three messages.
  Once they build, A, B and C can work at the same time.


.. raw:: html

   <p><small>The animation on this page was made with Claude.</small></p>
