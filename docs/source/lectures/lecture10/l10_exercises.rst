====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 10: ROS 2
Foundations. Work through them in order, as each exercise builds on the
skills from the previous one. Build and run each program in your ROS 2
workspace to verify your understanding.

.. note::

   Build all exercises with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select <package_name>
      source install/setup.bash


----


.. dropdown:: Exercise 1: Basic Node
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a minimal ROS 2 node that logs a message when it starts.

    **Specification**

    1. Create a new ROS 2 package called ``basic_node_pkg`` with a dependency
       on ``rclcpp``.

    2. Write a node class ``BasicNode`` that inherits from ``rclcpp::Node``
       with:

       - Node name: ``"basic_node"``.
       - In the constructor, log an info message: ``"Basic node has been started"``.

    3. In ``main()``, initialize ROS 2, create the node, spin it, and shut down.

    4. Update ``CMakeLists.txt`` to build and install the executable.

    5. Build, source, and run the node.

.. dropdown:: Exercise 2: Simple Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a publisher node that publishes an incrementing counter on a
    topic every second.

    **Specification**

    1. Create a package ``counter_pub_pkg`` with dependencies on ``rclcpp``
       and ``std_msgs``.

    2. Write a node class ``CounterPublisher`` that:

       - Has node name ``"counter_publisher"``.
       - Publishes ``std_msgs::msg::Int32`` messages on the topic ``"counter"`` (queue size 10).
       - Uses a wall timer with a 1-second period.
       - Maintains a ``count_`` member variable (starting at 0) that increments each time.
       - Logs the published value using ``RCLCPP_INFO``.

    3. Build, source, and run. Verify with ``ros2 topic echo /counter``.

.. dropdown:: Exercise 3: Simple Subscriber
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a subscriber node that listens to the counter topic from
    Exercise 2 and logs the received values.

    **Specification**

    1. Create a package ``counter_sub_pkg`` with dependencies on ``rclcpp``
       and ``std_msgs``.

    2. Write a node class ``CounterSubscriber`` that:

       - Has node name ``"counter_subscriber"``.
       - Subscribes to the ``"counter"`` topic (``std_msgs::msg::Int32``, queue size 10).
       - In the callback, logs the received value: ``"Received: <value>"``.

    3. Build, source, and run alongside the publisher from Exercise 2.

.. dropdown:: Exercise 4: Custom Message
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Define a custom message type and use it in a publisher/subscriber
    pair.

    **Specification**

    1. Create an interface package ``sensor_interfaces`` with:

       - A custom message ``msg/SensorReading.msg`` with fields:

         - ``string sensor_id``
         - ``float64 temperature``
         - ``float64 humidity``
         - ``uint32 timestamp``

    2. Create a node package ``sensor_pub_sub_pkg`` that depends on
       ``rclcpp`` and ``sensor_interfaces``.

    3. Write a publisher node ``SensorPublisher`` that:

       - Publishes ``sensor_interfaces::msg::SensorReading`` on the topic ``"sensor_data"`` every 2 seconds.
       - Populates each field with sample values.

    4. Write a subscriber node ``SensorSubscriber`` that:

       - Subscribes to ``"sensor_data"`` and logs all fields.

    5. Build both packages, source, and run.

.. dropdown:: Exercise 5: Multi-topic Publisher
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a single node that publishes on two different topics
    simultaneously.

    **Specification**

    1. Create a package ``multi_topic_pkg`` with dependencies on ``rclcpp``
       and ``std_msgs``.

    2. Write a node class ``MultiTopicPublisher`` that:

       - Has node name ``"multi_topic_publisher"``.
       - Publishes ``std_msgs::msg::String`` on the topic ``"status"`` every 1 second.
       - Publishes ``std_msgs::msg::Float64`` on the topic ``"temperature"`` every 2 seconds.
       - Uses two separate timers and two separate publishers.
       - Logs each published message.

    3. Build, source, and run. Verify both topics with ``ros2 topic list``
       and ``ros2 topic echo``.

.. dropdown:: Exercise 6: Simulated Robot Pub/Sub System
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal** *(Challenge)*

    Build a complete publisher/subscriber system for a simulated robot.
    The robot publishes its position using a custom message and
    subscribes to velocity commands.

    **Specification**

    1. Create an interface package ``robot_interfaces`` with two custom
       messages:

       - ``msg/RobotPose.msg``:

         - ``string robot_name``
         - ``float64 x``
         - ``float64 y``
         - ``float64 theta``

       - ``msg/VelocityCommand.msg``:

         - ``float64 linear_velocity``
         - ``float64 angular_velocity``

    2. Create a node package ``robot_sim_pkg`` with two nodes:

       **RobotNode** (``robot_node.cpp``):

       - Publishes ``RobotPose`` on ``"robot_pose"`` every 100ms.
       - Subscribes to ``VelocityCommand`` on ``"cmd_vel"``.
       - Maintains internal state (``x_``, ``y_``, ``theta_``), all
         initialized to ``0.0``.
       - When a velocity command is received, updates the pose:

         - ``theta_ += msg->angular_velocity * 0.1``
         - ``x_ += msg->linear_velocity * cos(theta_) * 0.1``
         - ``y_ += msg->linear_velocity * sin(theta_) * 0.1``

       **ControllerNode** (``controller_node.cpp``):

       - Publishes ``VelocityCommand`` on ``"cmd_vel"`` every 500ms.
       - Subscribes to ``RobotPose`` on ``"robot_pose"``.
       - Publishes a constant forward velocity (``linear_velocity = 1.0``,
         ``angular_velocity = 0.1``).
       - Logs the latest received robot pose.

    3. Build all packages, run both nodes, and verify with CLI tools.
