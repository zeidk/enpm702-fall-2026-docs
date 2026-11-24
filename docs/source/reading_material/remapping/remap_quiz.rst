====================================================
Quiz
====================================================

This quiz covers :doc:`remap_lecture`: namespaces, relative and absolute names, and remapping rules.

.. note::

   **Instructions:**

   - Each question has exactly one correct answer.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
====================================================

.. admonition:: Question 1
   :class: hint

   A node subscribes to the relative topic name ``odometry/filtered``. It starts with ``--ros-args -r __ns:=/robot1``, and the robot publishes on ``/odometry/filtered``. What happens?

   A. The node subscribes to ``/odometry/filtered`` and works as before.

   B. The node does not start, because ``/robot1`` does not exist.

   C. The node subscribes to ``/robot1/odometry/filtered``. No publisher is there, so the controller gets no odometry, does nothing and logs nothing.

   D. The node subscribes to ``/robot1/odometry/filtered``, and the namespace copies the robot's messages to it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   The namespace puts the prefix ``/robot1`` in front of the node's name and of its relative topic names. In the reading, ``ros2 topic info /robot1/odometry/filtered`` shows "Publisher count: 0". ``control_callback`` returns at once while it has no odometry, so the node logged nothing and published no command. Adding ``-r odometry/filtered:=/odometry/filtered -r cmd_vel:=/cmd_vel`` points the two topics back at the robot.


----


True / False
====================================================

.. admonition:: Question 2
   :class: hint

   **True or False:** A node runs with ``-r __ns:=/robot1 -r cmd_vel:=/cmd_vel``. It publishes on ``/robot1/cmd_vel``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A name that starts with ``/`` is absolute, and the namespace does not change it. The remapped name ``/cmd_vel`` is absolute, so the node publishes on ``/cmd_vel``. Only a relative name, such as ``cmd_vel`` without the slash, gets the prefix.
