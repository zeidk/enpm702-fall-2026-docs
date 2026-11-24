====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: Simulation, Control and Parameters. Topics include the pose and the quaternion, the ROSbot in Gazebo (Gazebo's topics and the bridge, its topics and the ``TwistStamped`` command), simulation time (``/clock``, ``use_sim_time`` and the two kinds of timer), proportional control (the error of a turn, the gain, the limit and the tolerance), parameters (declaring and reading them, setting them at start, ``use_sim_time``, and the parameter callback).

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-13)
====================================================

.. admonition:: Question 1
   :class: hint

   A node publishes ``geometry_msgs/msg/Twist`` messages on ``/cmd_vel``. The ROSbot in Gazebo does not move. What is the cause?

   A. ``/cmd_vel`` takes a ``TwistStamped``, and the two types do not connect.

   B. A ``Twist`` message can set only the angular speed.

   C. The node must publish at 50 Hz or faster.

   D. The simulation must be started with ``gui:=true``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**

   ``/cmd_vel`` takes a ``TwistStamped``: a ``Twist`` with a header that holds a time stamp. A publisher of another type on the same topic name does not connect to the subscriber, so no command arrives.


.. admonition:: Question 2
   :class: hint

   The ROSbot faces 3.122 rad (179°). The target heading is -1.571 rad (-90°). What error does the controller compute?

   A. -4.693 rad

   B. 1.590 rad

   C. 4.693 rad

   D. -1.590 rad

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, 1.590 rad

   Target minus heading is -1.571 - 3.122 = -4.693 rad, a turn right of 269°. Adding one full turn, 2π = 6.283 rad, gives 1.590 rad, a turn left of 91°. The error is the angle left to turn the short way, in -π to π. A positive error means turn left.


.. admonition:: Question 3
   :class: hint

   A heading controller has a gain of 1.5 (rad/s per rad) and a limit of 1.0 rad/s. The error is 1.2 rad. What command does it publish?

   A. 1.2 rad/s

   B. 1.8 rad/s

   C. 1.0 rad/s

   D. 0.8 rad/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, 1.0 rad/s

   The gain times the error is 1.5 × 1.2 = 1.8 rad/s. That is above the limit, so the controller sends the limit, 1.0 rad/s. In the lecture, the command is 1.0 rad/s until the error is under 1.0 / 1.5 = 0.67 rad.


.. admonition:: Question 4
   :class: hint

   Why does a controller stop within a tolerance, and not at an error of exactly 0?

   A. The ROSbot cannot turn slower than 0.02 rad/s.

   B. The odometry never reads an error of exactly 0, so the loop would never end.

   C. A tolerance makes the gain smaller.

   D. ``std::clamp`` fails for an error of 0.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Without a tolerance, the loop would wait for an error of exactly 0, which the odometry never reads. The tolerance is a margin you choose: the heading controller of the lecture stops within 0.02 rad.


.. admonition:: Question 5
   :class: hint

   Which command makes the ROSbot turn on the spot, without driving forward?

   A. A ``TwistStamped`` with only ``twist.linear.x`` set.

   B. A ``TwistStamped`` with only ``twist.angular.z`` set.

   C. A ``Twist`` with only ``angular.z`` set.

   D. A ``TwistStamped`` with ``twist.linear.x`` and ``twist.angular.z`` both set to 0.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   ``angular.z`` is the turn rate in rad/s, and a positive value turns left. With ``linear.x`` left at 0, the robot does not drive forward. Answer A drives straight, C has the wrong type for ``/cmd_vel``, and D is a stop command.


.. admonition:: Question 6
   :class: hint

   A heading controller has a gain of 1.5 (rad/s per rad) and a limit of 1.0 rad/s. The error is 0.5848 rad. What command does it publish?

   A. 1.0 rad/s

   B. 0.877 rad/s

   C. 0.39 rad/s

   D. 2.35 rad/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, 0.877 rad/s

   The gain times the error is 1.5 × 0.5848 = 0.877 rad/s. That is under the 1.0 rad/s limit, so it is sent as it is. The limit applies only when the gain times the error is above it, which happens while the error is over 1.0 / 1.5 = 0.67 rad.


.. admonition:: Question 7
   :class: hint

   A node calls ``declare_parameter("kp_angular", 1.5)``. What type does the parameter have?

   A. integer, because of the name

   B. double, because the default value 1.5 is a double

   C. string, because the name is a string

   D. It has no type until the first ``ros2 param set``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The default value sets the type: 1.5 makes a double. That is why ``ros2 param set /heading_controller_node kp_angular 2`` fails: 2 is an integer, and the answer is "Wrong parameter type".


.. admonition:: Question 8
   :class: hint

   A node reads ``kp_angular`` once, in its constructor. While it turns, you run ``ros2 param set /heading_controller_node kp_angular 1.5``. The answer is "Set parameter successful". What happens to the commands the node publishes?

   A. They use the new gain from the next ``control_callback``.

   B. They use the new gain after the current turn.

   C. They do not change: the node still uses the value it read.

   D. The node stops, because the parameter changed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   ``ros2 param set`` changes the stored value. The node copied the value into a data member in its constructor and never reads the parameter again, so its commands do not change. In the lecture, the node started with 0.5 and kept commanding 0.5 × error after the set. A parameter callback is what copies a new value into the data member.


.. admonition:: Question 9
   :class: hint

   A parameter file has this content:

   .. code-block:: yaml

      /**:
        ros__parameters:
          use_sim_time: true

      heading_controller_node:
        ros__parameters:
          kp_angular: 1.5

   Which statement is true?

   A. Only ``heading_controller_node`` gets ``use_sim_time: true``.

   B. Every node that loads the file gets ``use_sim_time: true``, and only ``heading_controller_node`` gets ``kp_angular``.

   C. ``/**`` is a comment.

   D. The file sets ``kp_angular`` for every node.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The wildcard key ``/**`` matches every node. A key with a node's name sets parameters of that node only, under ``ros__parameters``.


.. admonition:: Question 10
   :class: hint

   What does ``use_sim_time`` set to true do for a node that runs with Gazebo?

   A. It makes the node run faster than real time.

   B. It makes the node's clock follow the ``/clock`` topic, so ``now()`` gives the simulation's time.

   C. It starts Gazebo.

   D. It makes the node publish on ``/clock``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Gazebo publishes its own time on ``/clock``. With ``use_sim_time`` true, the node's clock follows it, so ``now()``, and the stamp of every ``TwistStamped``, gives the simulation's time. It is false unless you set it.


.. admonition:: Question 11
   :class: hint

   Gazebo runs the demo world ``shapes.sdf`` with ``gz sim -s -r shapes.sdf``, and no ROS node runs. ``gz topic -l`` lists ``/clock``, ``/stats`` and ``/world/shapes/state``. ``ros2 topic list`` lists only ``/parameter_events`` and ``/rosout``. What does this show?

   A. Gazebo's topics are not ROS topics. A bridge node from ``ros_gz_bridge`` copies the ones you need between the two.

   B. ``ros2 topic list`` must be started before Gazebo.

   C. Gazebo publishes its topics on ROS only when it has a window.

   D. ``/clock`` is a ROS topic that ``ros2 topic list`` hides.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**

   Gazebo is a program of its own, not a ROS node, and it has its own topics. The ROS list shows only ``/parameter_events`` and ``/rosout``. A bridge node from ``ros_gz_bridge`` copies the topics you need between Gazebo and ROS.


.. admonition:: Question 12
   :class: hint

   A node runs with ``use_sim_time`` true. It has one timer made with ``create_timer`` and one made with ``create_wall_timer``. Gazebo is paused. What happens?

   A. Both timers stop, because the node's clock is the simulation's.

   B. Both timers keep firing, and ``now()`` keeps counting.

   C. The ``create_timer`` timer stops. The ``create_wall_timer`` timer keeps firing, and ``now()`` does not move.

   D. The ``create_wall_timer`` timer stops. The ``create_timer`` timer keeps firing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   A ``create_timer`` timer runs on the node's clock, which follows ``/clock``, so it stops while Gazebo is paused. A ``create_wall_timer`` timer runs on the computer's clock, so it keeps firing, and ``now()`` stays at the last simulation time. In the lecture's run, the wall timer fired 5 times during the pause, and ``now()`` read 32.892 s, then 32.896 s. After Gazebo resumed, the ``create_timer`` timer fired again, at 33.000 s.



.. admonition:: Question 13
   :class: hint

   On a flat floor, the ROSbot starts facing :math:`+x` (yaw 0°). It turns 90° to the left, counterclockwise seen from above, and now faces :math:`+y`. Which orientation :math:`(x, y, z, w)` does ``/odometry/filtered`` report?

   A. :math:`(0, 0, 0, 1)`

   B. :math:`(0, 0, 0.707, 0.707)`

   C. :math:`(0, 0, 1, 0)`

   D. :math:`(0.707, 0, 0, 0.707)`

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Yaw is 90°, :math:`\frac{\pi}{2}` rad, about z: :math:`z = \sin\frac{\pi}{4} = 0.707` and :math:`w = \cos\frac{\pi}{4} = 0.707`. A is no turn at all, C is a turn of 180° (facing :math:`-x`), and D is a roll of 90° about x.

----


True / False (Questions 14-19)
====================================================

.. admonition:: Question 14
   :class: hint

   **True or False:** A node declared ``kp_angular`` with the default 1.5. Started with ``-p kp_angular:=1``, it uses a gain of 1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   ``1`` is an integer, and ``kp_angular`` is a double, so the node does not start: it stops with an ``InvalidParameterTypeException``, "Wrong parameter type, parameter {kp_angular} is of type {double}, setting it to {integer} is not allowed". Write a double with a decimal point: ``-p kp_angular:=1.0``.


.. admonition:: Question 15
   :class: hint

   **True or False:** In the lecture's runs, raising the gain from 1.5 to 4.0 made a 90° turn of the ROSbot faster.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The turns took 2.65 s to 2.75 s at a gain of 1.5 and 2.70 s at 4.0. A gain of 4.0 keeps the command at the 1.0 rad/s limit longer (until the error is under 1.0 / 4.0 = 0.25 rad, against 1.0 / 1.5 = 0.67 rad), but the turn was no faster. A gain of 0.5 never reaches the limit (0.5 × 1.57 = 0.785 rad/s at most), and its turns took 6.25 s to 6.45 s.


.. admonition:: Question 16
   :class: hint

   **True or False:** If a parameter callback returns ``successful = false``, ``ros2 param set`` prints the callback's ``reason``, and the parameter keeps its old value.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   In the lecture, ``ros2 param set /heading_controller_node kp_angular -1.0`` answers "Setting parameter failed: kp_angular must not be negative". The callback checks the values of a set command first, and stores the new ones only when every value is good, so one bad value rejects the whole command.


.. admonition:: Question 17
   :class: hint

   **True or False:** A parameter callback stays registered even if the node does not keep the handle that ``add_on_set_parameters_callback`` returned.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The callback stays registered only while the handle exists. That is why the lecture keeps it in a data member of the node.


.. admonition:: Question 18
   :class: hint

   **True or False:** The turning limit that the lecture's callback uses for ``max_angular_rps`` is 3.14 rad/s, the ROSbot's own turning limit, so ``max_angular_rps 5.0`` is rejected.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The callback accepts a ``max_angular_rps`` that is more than 0 and at most 3.14 rad/s. The answer to the set of 5.0 is "Setting parameter failed: max_angular_rps must be more than 0 and at most 3.14 rad/s".


.. admonition:: Question 19
   :class: hint

   **True or False:** A node starts with ``-p use_sim_time:=true``, and Gazebo is not running. ``now()`` returns the computer's time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   With ``use_sim_time`` true, the node's clock follows ``/clock``, and ROS time "will return zero if nothing has been received." No message arrives, so ``now()`` is 0. In the lecture's run with Gazebo, the first two lines read ``now() = 0.000 s`` before the first ``/clock`` message arrived. With ``use_sim_time`` false, ``now()`` was 1795198889.261 s, the computer's clock in seconds since 1 January 1970.
