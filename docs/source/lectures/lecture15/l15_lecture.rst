====================================================
Lecture
====================================================


Robot Autonomy Architecture
====================================================

Throughout the ROS 2 lectures you have learned the individual building
blocks of a robotic system: **nodes**, **topics**, **services**,
**actions**, **parameters**, **launch files**, **executors**, and, in
Lectures 13-14, **coordinate frames (TF2)** and **lifecycle nodes**.
Each of these was introduced in isolation.

This final lecture answers a different question: *how do these pieces
fit together to make a robot behave intelligently?* The answer is an
**autonomy architecture**, a standard way of organizing perception,
decision-making, and control into cooperating nodes. This is also where
**Artificial Intelligence (AI)** and **Machine Learning (ML)** enter a
robotic system.

.. admonition:: The key idea
   :class: important

   An autonomy architecture is not a new ROS 2 feature, it is a *way
   of composing the features you already know*. Every box in the
   architecture is a **node**, and every arrow between boxes is a
   **communication primitive** (a topic, service, or action) you have
   already used.


----


The Sense-Plan-Act Paradigm
====================================================

The classical and most widely used way to structure an autonomous robot
is the **Sense-Plan-Act** (SPA) paradigm. It divides the robot's
software into three responsibilities:

- **Sense (Perception)**, read raw sensor data and turn it into a
  meaningful description of the world (e.g., "there is an obstacle 0.4 m
  ahead", "the robot is at pose (x, y, θ)").
- **Plan (Decision)**, decide *what to do* given the current
  understanding of the world (e.g., "turn left", "navigate to the
  charging station"). **This is the layer we usually call the robot's
  "intelligence."**
- **Act (Control)**, translate the decision into commands the robot's
  actuators can execute (e.g., velocity commands to the wheels).

.. code-block:: text

   ┌───────────┐      ┌───────────┐      ┌───────────┐
   │  PERCEIVE │────► │   PLAN    │────► │    ACT    │
   │ (sensing) │      │ (decision)│      │ (control) │
   └───────────┘      └───────────┘      └───────────┘
        ▲                                      │
        │                                      ▼
        └─────────────  the robot  ◄───────────┘
                    (sensors / actuators)

The cycle repeats continuously: the robot senses the world, plans an
action, acts on it, and the action changes the world, which the robot
senses again. This loop is the heart of every autonomous system, from a
search-and-rescue robot to a self-driving car.


----


Mapping the Architecture to ROS 2
====================================================

The reason Sense-Plan-Act maps so cleanly onto ROS 2 is that each
stage is naturally a **node**, and the data flowing between stages uses
the **communication patterns** you already learned. Nothing here is new.
It is the same toolbox, organized into a system.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35
   :class: compact-table

   * - Architecture element
     - ROS 2 concept
     - Where you learned it
   * - Raw sensor streams (lidar, camera, odometry)
     - **Topics** (publish/subscribe)
     - Lecture 10
   * - Velocity / actuator commands
     - **Topics** (publish/subscribe)
     - Lecture 10
   * - Custom "world state" or "decision" messages
     - **Custom interfaces** (``.msg``)
     - Lecture 10
   * - One-shot queries ("is the path clear?")
     - **Services** (request/response)
     - Lecture 12
   * - Long-running goals ("navigate to waypoint")
     - **Actions** (goal/feedback/result)
     - Lecture 12
   * - Tuning behavior (speeds, thresholds)
     - **Parameters**
     - Lecture 11
   * - Bringing the whole system up
     - **Launch files** + **executors**
     - Lecture 11
   * - Spatial relationships between frames
     - **TF2** (coordinate frames)
     - Lecture 13
   * - Ordered, deterministic bringup of components
     - **Lifecycle nodes**
     - Lecture 14


----


The Three Layers as ROS 2 Nodes
====================================================

A minimal autonomy stack is three nodes connected by topics. Consider
the search-and-rescue **TurtleBot3** from the Group Projects, which
exposes ``/scan`` (lidar), ``/odom`` (odometry), and ``/cmd_vel``
(velocity command):

.. code-block:: text

           /scan, /odom                /world_state               /cmd_vel
   robot ──────────────► ┌────────────┐ ──────────► ┌──────────┐ ──────────► ┌─────────┐ ──────► robot
   sensors  (topics)     │ PERCEPTION │  (topic,     │ DECISION │  (topic)    │ CONTROL │ (topic)
                         │   node     │   custom msg)│   node   │             │  node   │
                         └────────────┘              └──────────┘             └─────────┘
                                                          ▲
                                                  parameters (tuning)
                                                  lifecycle (managed bringup)

- **Perception node**, subscribes to ``/scan`` and ``/odom``, fuses
  them into a compact description of the world, and publishes it on a
  custom topic (e.g., ``/world_state``).
- **Decision node**, subscribes to ``/world_state`` and decides on an
  action, which it publishes (e.g., a desired velocity or a higher-level
  command). **This is the node that contains the robot's intelligence.**
- **Control node**, subscribes to the decision and publishes the final
  ``/cmd_vel`` (``geometry_msgs::msg::Twist``) that drives the robot.

.. note::

   In small systems the perception and decision layers are often
   combined into a single node, and the control layer is sometimes
   provided by an off-the-shelf driver. The number of nodes is a design
   choice; the **separation of responsibilities** is what matters.


----


Where AI and Machine Learning Fit
====================================================

The **decision (and perception) layer is where AI lives**. There are two
broad ways to implement it, and, this is the central lesson of the
lecture, **both expose the same ROS 2 interface**:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40
   :class: compact-table

   * - Approach
     - Examples
     - Characteristics
   * - **Classical AI**
     - Rule-based logic, finite state machines, search/path planning
       (A*, Dijkstra), behavior trees
     - Deterministic, easy to inspect and debug, no training data
   * - **Learned (ML)**
     - Image classifiers, object detectors, reinforcement-learning
       policies, learned controllers
     - Handle high-dimensional input (images, point clouds), require
       training data, harder to interpret

The crucial architectural insight:

.. admonition:: Swapping the brain does not change the wiring
   :class: important

   Whether the decision node runs a hand-written ``if`` statement or a
   trained neural network, it is **still just a ROS 2 node** that
   subscribes to the same input topic and publishes to the same output
   topic. You can replace a rule-based policy with a learned model
   **without changing any other node in the system**. This is what makes
   the architecture so powerful: intelligence is modular.

In production robotics, the learned models in the perception/decision
layer are typically run in C++ for performance. The model itself is
trained offline (often in Python), exported, and then loaded for
**inference** inside a ROS 2 node using one of:

- **OpenCV DNN**, run common vision models directly from OpenCV.
- **ONNX Runtime**, a portable C++ inference engine for models
  exported to the ONNX format.
- **LibTorch**, the C++ API of PyTorch.

.. note::

   Integrating these inference libraries is beyond the scope of this
   course, they are mentioned so you know *where* a trained model
   plugs into the architecture. The take-away is conceptual: the ML
   model occupies the **decision/perception box**, behind the same ROS 2
   topic interface as any other implementation.


----


A Concrete Example: A Reactive Decision Node
====================================================

The smallest useful autonomy example is a **reactive** decision node:
it maps the latest sensor reading directly to an action, with no
internal world model. The node below performs simple obstacle avoidance
on the TurtleBot3, it drives forward, and turns when the lidar reports
an obstacle ahead.

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <sensor_msgs/msg/laser_scan.hpp>
   #include <geometry_msgs/msg/twist.hpp>
   #include <algorithm>

   class ReactiveController : public rclcpp::Node {
    public:
     ReactiveController()
         : Node{"reactive_controller"} {
       // Tunable behavior via parameters (see Lecture 11)
       safe_distance_ = this->declare_parameter<double>("safe_distance", 0.5);
       forward_speed_ = this->declare_parameter<double>("forward_speed", 0.2);
       turn_speed_ = this->declare_parameter<double>("turn_speed", 0.5);

       // ACT: publish velocity commands to the robot
       cmd_pub_ = this->create_publisher<geometry_msgs::msg::Twist>(
           "/cmd_vel", 10);

       // SENSE: subscribe to the lidar
       scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
           "/scan", 10,
           std::bind(&ReactiveController::decide, this, std::placeholders::_1));
     }

    private:
     // PLAN: the decision layer -- this is where the "intelligence" lives
     void decide(const sensor_msgs::msg::LaserScan::SharedPtr scan) {
       // Closest obstacle anywhere in the scan
       double nearest = *std::min_element(scan->ranges.begin(),
                                          scan->ranges.end());

       auto cmd = geometry_msgs::msg::Twist{};
       if (nearest < safe_distance_) {
         cmd.angular.z = turn_speed_;  // obstacle ahead -> turn in place
       } else {
         cmd.linear.x = forward_speed_;  // clear -> drive forward
       }
       cmd_pub_->publish(cmd);
     }

     rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_pub_;
     rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
     double safe_distance_;
     double forward_speed_;
     double turn_speed_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<ReactiveController>());
     rclcpp::shutdown();
     return 0;
   }

The decision logic here is a single hand-coded rule inside ``decide()``.
That method is exactly the **decision box** of the architecture. To make
this robot "smarter", you would replace the body of ``decide()`` with a
planner, a behavior tree, or a learned policy, **the subscription, the
publisher, and every other node would stay the same**.


----


Architectural Styles
====================================================

The example above is a **reactive** architecture: sense directly drives
act, with no internal model or memory. Robotics distinguishes three
broad styles:

.. list-table::
   :header-rows: 1
   :widths: 22 78
   :class: compact-table

   * - Style
     - Description
   * - **Reactive**
     - Sensor data maps directly to actions. Fast and robust, but
       cannot reason about goals (e.g., simple obstacle avoidance).
   * - **Deliberative**
     - Build a world model, then plan a sequence of actions to reach a
       goal (e.g., compute a path with A* and follow it). Powerful, but
       slower and dependent on an accurate model.
   * - **Hybrid (three-layer)**
     - Combine a fast reactive layer with a slower deliberative planner
       and an executive that mediates between them. This is the
       architecture used by most real robots.

Modern ROS 2 systems rarely build these from scratch. Two widely used
frameworks implement the decision layer for you:

- **Nav2**, the ROS 2 navigation stack, a complete hybrid architecture
  for autonomous mobile-robot navigation (planning, control, recovery).
- **BehaviorTree.CPP**, a C++ library for structuring complex
  decision-making as behavior trees, used heavily inside Nav2.


----


Coordinating the System
====================================================

Once the architecture spans several nodes, the ROS 2 features from the
earlier lectures become the glue that holds it together:

- **Launch files** (Lecture 11) start the perception, decision, and
  control nodes together as one system.
- **Parameters** (Lecture 11) tune the behavior of each layer (speeds,
  thresholds, model paths) without recompiling.
- **TF2** (Lecture 13) lets the perception and decision layers
  reason about *where* things are, by transforming sensor detections
  into a common frame.
- **Lifecycle nodes** (Lecture 14) bring the layers up in a
  deterministic order, for example, configuring perception before the
  decision node is activated.


----


Summary
====================================================

- An **autonomy architecture** composes the ROS 2 building blocks you
  already know into a system that senses, decides, and acts.
- The **Sense-Plan-Act** paradigm maps each stage onto a **node**, and
  each data flow onto a **topic, service, or action**.
- The **decision/perception layer is where AI and ML live**. Classical
  and learned approaches expose the **same ROS 2 interface**, so the
  "brain" can be swapped without rewiring the rest of the system.
- Trained models are integrated for **inference** in C++ via libraries
  such as OpenCV DNN, ONNX Runtime, or LibTorch, they sit behind the
  decision node's topic interface like any other implementation.
- Real systems use **hybrid** architectures, often built on frameworks
  like **Nav2** and **BehaviorTree.CPP**.
