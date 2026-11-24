====================================================
Lecture
====================================================

This reading builds on the heading controller node of Lecture 12: the
executable ``heading_controller_exe`` of the ``l12_rosbot`` package, and its
parameters, such as ``kp_angular``. It runs that node twice, with namespaces
and remapping rules, and changes none of its code. A parameter changes a
node's settings without recompiling. **Remapping** does the same for the names
a node uses: its topics, its own name and its **namespace**. The line numbers
and commit hashes below are from the stages of the ``l12_rosbot`` package in
the course repository.


Why Remap: Topic Names Written in the Code
==========================================

``heading_controller_node`` names its two topics in its code: ``"odometry/filtered"`` (line 29 of ``heading_controller_node.hpp``, stage 4) and ``"cmd_vel"`` (line 34). Two jobs need other names:

- **Another source.** ``differential_drive_controller`` also publishes ``/odometry/wheels``, the pose from the wheels alone. To compare the two, the controller must read ``/odometry/wheels``.
- **A fleet.** Each robot of a fleet has its own topics, such as ``/robot1/cmd_vel`` and ``/robot2/cmd_vel``, and each controller must use its own robot's.

Editing the strings means one copy of the code per job. Instead, ``--ros-args -r`` changes the names when the node starts:

- A **namespace**, "a prefix added to the names of a node and of its relative topics" (the glossary definition of **ROS Namespace**), gives each robot's controller its own names.
- A **remapping rule** replaces one name with another.

Namespaces
==========

A namespace is a prefix in front of a node's name and of its relative names, so the same code can run once per robot.

Two Controllers with One Name
-----------------------------

A fleet runs one controller per robot: the same executable, started once per robot. Started twice as it is, in two terminals:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe     # in each terminal

- ``ros2 node list`` lists ``/heading_controller_node`` twice, after a warning: "Be aware that there are nodes in the graph that share an exact name, which can have unintended side effects."
- ``ros2 topic info /cmd_vel`` answers "Publisher count: 3": the two controllers and ``rosbot_gz_bridge``.

.. admonition:: Conclusion
   :class: important

   The two nodes share one name, and both send commands on one ``/cmd_vel``. A namespace gives each controller its own names.

One Namespace per Controller
----------------------------

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe --ros-args -r __ns:=/robot1
   ros2 run l12_rosbot heading_controller_exe --ros-args -r __ns:=/robot2

.. code-block:: bash

   ros2 node list | grep heading

.. code-block:: text

   /robot1/heading_controller_node
   /robot2/heading_controller_node

.. code-block:: bash

   ros2 topic list | grep robot

.. code-block:: text

   /robot1/cmd_vel
   /robot1/odometry/filtered
   /robot2/cmd_vel
   /robot2/odometry/filtered
   /robot_description

- ``__ns`` put the prefix in front of each node's name and of its two topics. ``/robot_description`` is the ROSbot's description: ``grep`` matched it too.

.. admonition:: Conclusion
   :class: important

   The same code now runs with two sets of names, one per robot.

Pick a namespace and a node name for each controller to see the graph and its names.

.. raw:: html
   :file: widgets/_head.html

.. raw:: html
   :file: widgets/namespaces.html


Relative, Absolute and Private Names
------------------------------------

Whether a namespace changes a name depends on how the code writes it. The `ROS 2 design article on names <https://design.ros2.org/articles/topic_and_service_names.html>`__:

- **Relative**, such as ``"cmd_vel"``: "A relative name does not begin with a forward slash (/) and does respect the namespace of the node which created them." In ``/robot1``: ``/robot1/cmd_vel``.
- **Absolute**, such as ``"/rosout"``: "An absolute name begins with a forward slash (/) and does not respect namespaces". In ``/robot1``: still ``/rosout``.
- **Private**, such as ``"~/status"``: "The special single character token ~ will be replaced with a namespace snippet that is a concatenation of the namespace for the node and the node name." In ``/robot1``: ``/robot1/heading_controller_node/status``. The controller's code has no private name.

The controllers write ``"odometry/filtered"`` and ``"cmd_vel"`` without a leading ``/``, so a namespace moves them. A name written with ``/`` would stay the same in every namespace.

Pick a namespace and a name written in the code to see the full name it becomes.

.. raw:: html
   :file: widgets/resolver.html


What the Namespace Changed
--------------------------

In a launch file, ``PushROSNamespace`` puts its nodes in a namespace; ``__ns`` does it from the command line. One controller in ``/robot1``:

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
- ``ros2 topic info /robot1/odometry/filtered``: "Publisher count: 0". No odometry arrives, so ``control_callback`` returns at once: the node logged nothing, and by its code it publishes no command.

Remapping Rules
===============

A remapping rule replaces a name the node uses, when the node starts. It renames topics, the node itself and its namespace.

A Rule: match:=replacement
--------------------------

The `ROS 2 design article on remapping <https://design.ros2.org/articles/static_remapping.html>`__: "**Remapping rules** are the instructions describing how a node should change the names it uses." A rule has two parts, written ``match:=replacement`` after ``-r``:

- "The first part is used to determine if the rule applies to a name."
- "The second part is the replacement for a matched name."

Two match parts are special:

- "The strings ``__name`` or ``__node`` can be given on the match part of a rule to signal a change of the node's name."
- "The string ``__ns`` can be given on the match part of a rule to signal a change of the default namespace."

.. dropdown:: More detail: Rename a node: __node
   :class-container: more-detail
   :icon: info

   The two controllers of "Two Controllers with One Name", each with its own name:

   .. code-block:: bash

      ros2 run l12_rosbot heading_controller_exe \
        --ros-args -r __node:=heading_a
      ros2 run l12_rosbot heading_controller_exe \
        --ros-args -r __node:=heading_b

   - ``ros2 node list`` lists ``/heading_a`` and ``/heading_b``, with no warning.
   - ``ros2 topic info /cmd_vel`` still answers "Publisher count: 3".

   .. admonition:: Conclusion
      :class: important

      ``__node`` changed the node names, not the topic names. Both controllers still command the one ``/cmd_vel``.

Remap a Topic: Read the Wheel Odometry
--------------------------------------

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

A Namespace and Remapping Together
----------------------------------

The simulation has one ROSbot, with no namespace. Keep the node's namespace, and remap its two topics to the robot's absolute names:

.. code-block:: bash

   ros2 run l12_rosbot heading_controller_exe --ros-args \
     -r __ns:=/robot1 \
     -r odometry/filtered:=/odometry/filtered -r cmd_vel:=/cmd_vel

.. figure:: /_static/images/l12/remap_graph.png
   :alt: ROS graph drawn top to bottom. A rounded box ekf has an arrow down, labeled /odometry/filtered and nav_msgs/msg/Odometry, with tag 1 beside it, into a dashed box named /robot1 that holds the rounded box heading_controller_node. From that node, an arrow labeled /cmd_vel and geometry_msgs/msg/TwistStamped, with tag 2 beside it, goes down to a rounded box differential_drive_controller.
   :align: center
   :width: 55%

   Tag 1 is the rule for ``odometry/filtered``, tag 2 the rule for ``cmd_vel``; the dashed box is the namespace.

The log ends with ``[robot1.heading_controller_node]: all 4 headings reached``. A name that starts with ``/`` is absolute, so the namespace does not change the two replacements.

Pick a namespace, a node name and the two remapping rules to see the graph they give.

.. raw:: html
   :file: widgets/rule-builder.html


Remapping and Parameters
------------------------

1. A parameter set in a namespace:

   .. code-block:: bash

      ros2 run l12_rosbot heading_controller_exe \
        --ros-args -r __ns:=/robot1 -p kp_angular:=0.5
      ros2 param get /robot1/heading_controller_node kp_angular

   The answer is "Double value is: 0.5": a parameter is reached through the node's full name, namespace included.

2. A rule on a parameter's name, ``-r kp_angular:=gain``: ``ros2 param list`` still lists ``kp_angular``, and no ``gain``.

.. admonition:: Conclusion
   :class: important

   Rules rename the node and its topics; parameter names stay. The design article's example says the same: "the parameter name remains unchanged".

In a Launch File: name, namespace and remappings
------------------------------------------------

Lines 9 to 20 of ``launch/remap_launch.py`` (stage 5, commit ``6d2b94b``):

.. code-block:: python
   :linenos:
   :lineno-start: 9
   :emphasize-lines: 4-9

   heading_controller = Node(
       package="l12_rosbot",
       executable="heading_controller_exe",
       name="heading_a",
       namespace="robot1",
       remappings=[
           ("odometry/filtered", "/odometry/filtered"),
           ("cmd_vel", "/cmd_vel"),
       ],
       parameters=[{"use_sim_time": True}],
       output="screen",
   )

- Line 12 does what ``__node`` does, line 13 what ``__ns`` does, and lines 14 to 17 are two rules, each a (match, replacement) pair.
- ``ros2 launch l12_rosbot remap_launch.py``: the node is ``/robot1/heading_a``, and it turned the ROSbot through its four headings.

Click a button to match each line of the launch file with the part of the command it replaces.

.. raw:: html
   :file: widgets/launch-lines.html


Namespaces and Remapping: What You Can Do Now
=============================================

.. admonition:: Summary
   :class: tip

   - Put a node in a namespace: ``-r __ns:=/robot1``, or ``namespace=`` in a launch file. Relative names get the prefix; absolute names do not.
   - Rename a node: ``-r __node:=heading_a``, or ``name=``.
   - Remap a name: ``-r match:=replacement``, or ``remappings=[(match, replacement)]``.
   - Reach a parameter through the node's full name; rules do not rename parameters.
   - Check the result with ``ros2 node list``, ``ros2 node info``, ``ros2 topic list`` and ``ros2 topic info``.

.. raw:: html
   :file: widgets/_scripts.html
