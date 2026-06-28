====================================================
C++ Exercises
====================================================

These exercises reinforce the autonomy-architecture concepts from
Lecture 15. They combine **design exercises** (decomposing a system into
Sense-Plan-Act and mapping it onto ROS 2) with **coding exercises**
(implementing the layers as ROS 2 nodes). Work through them in order.

.. note::

   The coding exercises require a ROS 2 Jazzy workspace and assume a
   TurtleBot3-style robot (or Gazebo simulation) exposing ``/scan`` and
   ``/cmd_vel``. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1: Decompose a Task (Design)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice decomposing a robotics task into the Sense-Plan-Act
    layers and mapping each data flow onto a ROS 2 communication pattern.

    **Specification**

    A warehouse robot must patrol between two shelves and stop if a
    person steps in front of it. For this task:

    1. Identify what belongs in the **perception**, **decision**, and
       **control** layers.
    2. For each arrow between layers, state which ROS 2 primitive
       (topic, service, or action) you would use and why.
    3. Identify one place where a **parameter** would be useful.

    .. dropdown:: Solution
        :class-container: sd-border-success

        - **Perception:** subscribe to ``/scan`` (and a camera, if person
          detection is needed); publish a compact world state such as
          ``person_ahead`` (bool) and the current pose on a custom topic.
        - **Decision:** subscribe to the world state; decide between
          "drive to next shelf" and "stop". The patrol goal ("go to
          shelf B") is long-running with feedback, so an **action** is a
          good fit; the stop reaction is immediate, so it is driven by a
          **topic**.
        - **Control:** subscribe to the decision and publish ``/cmd_vel``
          (a **topic**, ``geometry_msgs::msg::Twist``).
        - **Parameter:** the stopping distance (how close a person must
          be before stopping) should be a parameter so it can be tuned
          without recompiling.

        The point of the exercise: the *arrows* are topics/services/
        actions, and the *boxes* are nodes, the same tools from
        Lectures 10-12.


.. dropdown:: Exercise 2: Reactive Controller (Front Sector)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a reactive decision/control node that only reacts to
    obstacles **directly ahead**, instead of anywhere in the scan.

    **Specification**

    1. Create a node ``front_reactive_controller``.
    2. Subscribe to ``/scan`` (``sensor_msgs::msg::LaserScan``) and
       publish to ``/cmd_vel`` (``geometry_msgs::msg::Twist``).
    3. Examine only the readings in a **front sector**, the first and
       last 15 readings of ``ranges`` (which straddle straight ahead).
    4. If the nearest reading in the front sector is closer than a
       ``safe_distance`` parameter (default 0.5 m), turn in place;
       otherwise drive forward.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <sensor_msgs/msg/laser_scan.hpp>
           #include <geometry_msgs/msg/twist.hpp>
           #include <algorithm>
           #include <vector>

           class FrontReactiveController : public rclcpp::Node {
            public:
             FrontReactiveController()
                 : Node{"front_reactive_controller"} {
               safe_distance_ =
                   this->declare_parameter<double>("safe_distance", 0.5);
               cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
                   "/cmd_vel", 10);
               scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
                   "/scan", 10,
                   std::bind(&FrontReactiveController::decide, this,
                             std::placeholders::_1));
             }

            private:
             void decide(const sensor_msgs::msg::LaserScan::SharedPtr scan) {
               const std::size_t window{15};
               const std::size_t n{scan->ranges.size()};
               if (n < window) {
                 return;
               }

               // Front sector straddles index 0: first and last `window`
               double nearest{std::numeric_limits<double>::infinity()};
               for (std::size_t i{0}; i < window; ++i) {
                 nearest = std::min(nearest, scan->ranges[i]);
                 nearest = std::min(nearest, scan->ranges[n - 1 - i]);
               }

               auto cmd = geometry_msgs::msg::Twist{};
               if (nearest < safe_distance_) {
                 cmd.angular.z = 0.5;
               } else {
                 cmd.linear.x = 0.2;
               }
               cmd_pub_->publish(cmd);
             }

             rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
             rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
             double safe_distance_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<FrontReactiveController>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 3: Separate Perception from Decision
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Split the monolithic reactive controller into a **perception node**
    and a **decision node** connected by a topic, a true two-layer
    architecture.

    **Specification**

    1. **Perception node** ``obstacle_perception``: subscribe to
       ``/scan``, compute whether an obstacle is within 0.5 m anywhere in
       the scan, and publish a ``std_msgs::msg::Bool`` on
       ``/obstacle_ahead``.
    2. **Decision node** ``obstacle_decision``: subscribe to
       ``/obstacle_ahead`` and publish ``/cmd_vel``, turn if ``true``,
       drive forward if ``false``.
    3. Run both nodes together and confirm the robot behaves as before.

    .. dropdown:: Solution
        :class-container: sd-border-success

        **Perception node:**

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <sensor_msgs/msg/laser_scan.hpp>
           #include <std_msgs/msg/bool.hpp>
           #include <algorithm>

           class ObstaclePerception : public rclcpp::Node {
            public:
             ObstaclePerception()
                 : Node{"obstacle_perception"} {
               pub_ = this->create_publisher<std_msgs::msg::Bool>(
                   "/obstacle_ahead", 10);
               sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
                   "/scan", 10,
                   std::bind(&ObstaclePerception::on_scan, this,
                             std::placeholders::_1));
             }

            private:
             void on_scan(const sensor_msgs::msg::LaserScan::SharedPtr scan) {
               double nearest = *std::min_element(scan->ranges.begin(),
                                                  scan->ranges.end());
               auto msg = std_msgs::msg::Bool{};
               msg.data = (nearest < 0.5);
               pub_->publish(msg);
             }

             rclcpp::Publisher<std_msgs::msg::Bool>::SharedPtr pub_;
             rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr sub_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<ObstaclePerception>());
             rclcpp::shutdown();
             return 0;
           }

        **Decision node:**

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <std_msgs/msg/bool.hpp>
           #include <geometry_msgs/msg/twist.hpp>

           class ObstacleDecision : public rclcpp::Node {
            public:
             ObstacleDecision()
                 : Node{"obstacle_decision"} {
               cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
                   "/cmd_vel", 10);
               sub_ = this->create_subscription<std_msgs::msg::Bool>(
                   "/obstacle_ahead", 10,
                   std::bind(&ObstacleDecision::decide, this,
                             std::placeholders::_1));
             }

            private:
             void decide(const std_msgs::msg::Bool::SharedPtr obstacle) {
               auto cmd = geometry_msgs::msg::Twist{};
               if (obstacle->data) {
                 cmd.angular.z = 0.5;
               } else {
                 cmd.linear.x = 0.2;
               }
               cmd_pub_->publish(cmd);
             }

             rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
             rclcpp::Subscription<std_msgs::msg::Bool>::SharedPtr sub_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<ObstacleDecision>());
             rclcpp::shutdown();
             return 0;
           }

        Because perception and decision are now separate nodes joined by
        ``/obstacle_ahead``, you can replace either one independently,
        for example, swapping the rule-based decision for a learned
        policy, without touching the other.


.. dropdown:: Exercise 4: Where Does the Model Go? (Design)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Reason about integrating a trained ML model into the architecture.

    **Specification**

    Suppose you train a neural network that takes a camera image and
    outputs whether the path ahead is "blocked" or "clear".

    1. Which layer and which node hosts the model?
    2. What is the node's input topic and output topic?
    3. If you later retrain the model to be more accurate, which other
       nodes in the system must change?
    4. Name one C++ library you could use to run the model for inference.

    .. dropdown:: Solution
        :class-container: sd-border-success

        1. The model goes in the **perception layer**, inside a node such
           as ``vision_perception`` (or a combined perception/decision
           node).
        2. Input: the camera image topic (e.g.,
           ``/camera/image_raw``). Output: a world-state topic such as
           ``/path_blocked`` (``std_msgs::msg::Bool``), the same
           interface a rule-based detector would publish.
        3. **None.** Because the node keeps the same input and output
           topics, retraining the model changes only that node. The
           decision and control nodes are unaffected, this is the
           modularity of the architecture.
        4. OpenCV DNN, ONNX Runtime, or LibTorch.


.. dropdown:: Exercise 5: Choose an Architecture Style (Design)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Match architecture styles (reactive, deliberative, hybrid) to
    scenarios.

    **Specification**

    For each scenario, choose the most appropriate style and justify it:

    1. An emergency bumper that stops the robot the instant it touches
       something.
    2. A delivery robot that must find the shortest route across a known
       building map.
    3. A warehouse robot that plans efficient routes but must also avoid
       people who suddenly appear.

    .. dropdown:: Solution
        :class-container: sd-border-success

        1. **Reactive**, the response must be immediate and requires no
           world model; sense maps directly to act.
        2. **Deliberative**, it needs a map and a planner (e.g., A*) to
           compute an optimal path before acting.
        3. **Hybrid**, a deliberative planner produces efficient routes,
           while a fast reactive layer overrides it to avoid people. This
           is what frameworks like Nav2 provide.
