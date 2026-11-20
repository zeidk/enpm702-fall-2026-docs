====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 12: Robots in Gazebo and Parameters. Topics include the ROSbot in Gazebo (its topics and the ``TwistStamped`` command), proportional control (the error of a turn and of a drive, the gain, the limit and the tolerance) and parameters (declaring and reading them, setting them at start, ``use_sim_time``, and the parameter callback).

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
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

   The distance controller has a target of 1.0 m, a gain of 0.8 (m/s per m) and a limit of 0.5 m/s. The robot is 0.75 m from its start. What command does it publish?

   A. 0.5 m/s

   B. 0.25 m/s

   C. 0.2 m/s

   D. 0.6 m/s

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, 0.2 m/s

   The error is the distance left to drive: 1.0 - 0.75 = 0.25 m. The gain times the error is 0.8 × 0.25 = 0.2 m/s, which is under the 0.5 m/s limit, so it is sent as it is.


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


----


True / False (Questions 11-15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** A node started with ``-p kp_linear:=0.8`` has the parameter ``kp_linear`` even when it did not declare it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   A node accepts only the parameters it declared. The node starts with no message, and ``ros2 param get`` answers "Parameter not set". A wrong name on the command line at start is dropped without a message, so check what the node has with ``ros2 param list``.


.. admonition:: Question 12
   :class: hint

   **True or False:** With gains of 1.5 and 4.0, a 90° turn of the ROSbot takes about the same time, because the speed limit sets the time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The command stays at the 1.0 rad/s limit while the gain times the error is over 1.0: until the error is under 1.0 / 1.5 = 0.67 rad for a gain of 1.5, and under 1.0 / 4.0 = 0.25 rad for 4.0. Most of a 90° turn (1.57 rad) is at the limit either way. In the lecture, the turns took 2.65 s to 2.75 s at 1.5 and 2.70 s at 4.0. A gain of 0.5 never reaches the limit (0.5 × 1.57 = 0.785 rad/s at most), and its turns took 6.25 s to 6.45 s.


.. admonition:: Question 13
   :class: hint

   **True or False:** If a parameter callback returns ``successful = false``, ``ros2 param set`` prints the callback's ``reason``, and the parameter keeps its old value.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   In the lecture, ``ros2 param set /heading_controller_node kp_angular -1.0`` answers "Setting parameter failed: kp_angular must not be negative". The callback checks every value of a set command first, and one bad value rejects the whole command.


.. admonition:: Question 14
   :class: hint

   **True or False:** A parameter callback stays registered even if the node does not keep the handle that ``add_on_set_parameters_callback`` returned.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False.**

   The callback stays registered only while the handle exists. That is why the lecture keeps it in a data member of the node.


.. admonition:: Question 15
   :class: hint

   **True or False:** The turning limit that the lecture's callback uses for ``max_angular_rps`` is 3.14 rad/s, the ROSbot's own turning limit, so ``max_angular_rps 5.0`` is rejected.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True.**

   The callback accepts a ``max_angular_rps`` that is more than 0 and at most 3.14 rad/s. The answer to the set of 5.0 is "Setting parameter failed: max_angular_rps must be more than 0 and at most 3.14 rad/s".
