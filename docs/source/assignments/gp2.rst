:orphan:

.. _gp2:

=====================================================
GP2: Services, Actions, Frames, and a Decision Layer
=====================================================

Overview
--------

This assignment extends your GP1 system and is your team's capstone. You add request-response communication through **services**, long-running tasks through **actions**, and a robot type hierarchy using C++ inheritance: a base ``RobotNode`` class with derived types that have different ROS parameters and behaviors. You then organize the nodes into a **robot autonomy architecture**, the Sense-Plan-Act stack from **Lecture 14**, with coordinate frame management through **TF2** for spatial reasoning. The heart of the assignment is a **decision layer**: the node that turns perception into action, and the place where Artificial Intelligence fits in a robot. By the end, your team has a multi-node ROS 2 search-and-rescue system with publishers, subscribers, services, actions, coordinate frames, and an autonomy decision layer.

.. important::

   **Posted Nov 24, due Dec 11, worth 96 points.** GP2 is the course's
   last group project, so it is larger than GP1 and runs about two and a
   half weeks. Two of the lectures it needs happen while it is open:
   coordinate frames on Dec 1 (Lecture 13) and the autonomy architecture
   on Dec 8 (Lecture 14). The requirements are in that order. Start with
   inheritance (Lecture 9), then the service and the action (Lecture 12,
   on the day GP2 is posted).

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Implement ROS 2 services for synchronous request-response operations.
#. Implement ROS 2 actions for long-running tasks with periodic feedback.
#. Design a class hierarchy for robot nodes using C++ inheritance.
#. Apply polymorphism to differentiate robot behaviors at runtime.
#. Broadcast static and dynamic transforms using TF2 and use them for spatial reasoning.
#. Organize a ROS 2 system into perception, decision, and control layers (Sense-Plan-Act).
#. Implement a decision node that maps perception to action, the layer where AI/ML fits.
#. Integrate all of these with the existing pub/sub system from GP1.

------------
Requirements
------------

.. dropdown:: Robot Inheritance
   :open:
   :color: primary

   **Goal:** build a robot type hierarchy so that all robots share one common
   interface (the base class) while each concrete robot type provides its own
   search-and-rescue behavior (the derived classes).

   **Step 1: Design the base** ``RobotNode`` **class.** It must inherit from
   ``rclcpp::Node`` and contain only the functionality that is common to every
   robot type:

   - Publishers shared by all robots (for example, a velocity command publisher
     and a victim report publisher that reuses your GP1 message).
   - Subscribers shared by all robots (for example, laser scan and odometry).
   - Common parameters declared in the constructor (for example, ``robot_name``
     and ``publish_rate``), each read back into a member variable.
   - At least two pure virtual methods that define the behavior every derived
     type must supply (for example, ``configure_sensors()`` and
     ``execute_task()``). These make ``RobotNode`` abstract: it cannot be
     instantiated on its own.

   **Step 2: Create at least 2 derived robot types** that publicly inherit from
   ``RobotNode``, for example:

   - ``GroundSearchBot``: slow, low to the ground, searches voids and rubble.
   - ``AerialSurveyBot``: fast aerial coverage, surveys the area from above.

   **Step 3:** Each derived type must:

   - Pass its own node name up to the ``RobotNode`` constructor.
   - Set different default parameter values (for example, a lower
     ``linear_speed_`` for the ground bot and a higher one for the aerial bot)
     and a different sensor configuration.
   - Override every pure virtual method with behavior specific to that robot
     type (for example, a different search pattern in ``execute_task()``).

   **Acceptance criteria:**

   - A pointer or reference of type ``RobotNode*`` can hold either derived type
     and calling a virtual method dispatches to the correct override at runtime
     (polymorphism).
   - Common publishers, subscribers, and parameters are declared exactly once in
     the base class and are not duplicated in the derived classes.
   - The base class destructor is ``virtual``.

   The skeleton below shows the structure to follow. Fill in the constructors,
   method bodies, and any additional members yourself.

   .. code-block:: cpp
      :caption: Illustrative class hierarchy skeleton (complete the bodies yourself)

      class RobotNode : public rclcpp::Node {
       public:
        RobotNode(const std::string& node_name, const rclcpp::NodeOptions& options);
        virtual ~RobotNode() = default;

       protected:
        // Pure virtual methods: every derived robot type must implement these.
        virtual void execute_task() = 0;
        virtual void configure_sensors() = 0;

        // Common members shared by all robot types.
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmd_vel_pub_;
        double linear_speed_{0.0};
        double angular_speed_{0.0};
        // TODO: add shared subscribers and parameter members.
      };

      class GroundSearchBot : public RobotNode {
       public:
        explicit GroundSearchBot(const rclcpp::NodeOptions& options);
        // TODO: set ground-specific default parameters in the constructor.

       protected:
        void execute_task() override;       // TODO: implement ground search pattern.
        void configure_sensors() override;  // TODO: configure low, short-range sensors.
      };

      // TODO: declare AerialSurveyBot (or another type) following the same pattern.

.. dropdown:: Custom Service
   :open:
   :color: primary

   **Goal:** add synchronous request-response communication so that a
   coordinator can dispatch a specific robot type to a location and immediately
   learn whether the dispatch succeeded.

   **Step 1: Define a custom** ``.srv`` **file** (for example,
   ``DispatchRobot.srv``) in your package's ``srv/`` directory. A ``.srv`` file
   has a request block and a response block separated by ``---``. Register the
   interface in ``CMakeLists.txt`` with ``rosidl_generate_interfaces`` and
   declare the build/runtime dependencies in ``package.xml``. The definition
   below is an example interface to adapt; change the fields to match your
   design.

   .. code-block:: text
      :caption: Example DispatchRobot.srv (adapt the fields to your design)

      # Request
      string robot_type
      float64 x
      float64 y
      ---
      # Response
      bool success
      string message

   **Step 2: Implement a service server.** It must:

   - Create a service with ``create_service`` using your generated service type
     and a service name.
   - In the callback, read the request (for example, the requested
     ``robot_type`` and target ``x`` / ``y``), perform the dispatch logic (for
     example, validate the robot type and start moving or configuring that
     robot for the search task), and fill in the response.
   - Set ``success`` to indicate the outcome and put a human-readable
     explanation in ``message`` (including the failure reason when applicable).

   **Step 3: Implement a service client.** It must:

   - Create a client with ``create_client`` for the same service name.
   - Wait for the service to become available (for example, with
     ``wait_for_service``) before sending.
   - Build a request, send it asynchronously, and process the returned response
     (log whether the dispatch succeeded and the message).

   **Acceptance criteria:**

   - Calling the service with a valid request returns ``success = true`` and
     triggers the corresponding robot behavior.
   - Calling the service with an invalid request (for example, an unknown robot
     type) returns ``success = false`` with an informative ``message``.

.. dropdown:: Custom Action
   :open:
   :color: primary

   **Goal:** add a long-running, preemptable task with periodic feedback so a
   robot can navigate to a reported victim location while reporting its progress.

   **Step 1: Define a custom** ``.action`` **file** (for example,
   ``NavigateToVictim.action``) in your package's ``action/`` directory. An
   ``.action`` file has three blocks (goal, result, feedback) separated by
   ``---``. Register it in ``CMakeLists.txt`` and ``package.xml`` the same way
   as the service. The definition below is an example interface to adapt.

   .. code-block:: text
      :caption: Example NavigateToVictim.action (adapt the fields to your design)

      # Goal
      float64 x
      float64 y
      ---
      # Result
      bool success
      float64 time_elapsed
      ---
      # Feedback
      float64 distance_remaining

   **Step 2: Implement an action server** with ``rclcpp_action::create_server``.
   It must provide three callbacks:

   - A goal callback that inspects the requested location and decides whether to
     accept or reject it (return ``ACCEPT_AND_EXECUTE`` or ``REJECT``).
   - A cancel callback that decides whether a cancel request is honored.
   - An accepted callback that starts the navigation work (typically on a
     separate thread so the executor is not blocked).

   During execution the server must:

   - Drive the robot toward the goal location, periodically publishing
     **feedback** (for example, ``distance_remaining``).
   - Check for cancellation and call ``canceled`` if a cancel was requested.
   - On arrival, fill in the **result** (for example, ``success`` and
     ``time_elapsed``) and call ``succeed``.

   **Step 3: Implement an action client** with
   ``rclcpp_action::create_client``. It must:

   - Wait for the action server (``wait_for_action_server``).
   - Send a goal and register goal-response, feedback, and result callbacks.
   - Log feedback as it arrives and report the final result.

   **Acceptance criteria:**

   - The client receives at least several feedback messages while the action is
     running, not just a single result at the end.
   - The result reports ``success = true`` once the robot reaches the goal.
   - The skeleton below shows only the goal callback. Implement the remaining
     callbacks and the execution loop yourself.

   .. code-block:: cpp
      :caption: Illustrative action server goal callback (complete the logic yourself)

      rclcpp_action::GoalResponse handle_goal(
          const rclcpp_action::GoalUUID& uuid,
          std::shared_ptr<const NavigateToVictim::Goal> goal)
      {
        // TODO: validate goal->x / goal->y (e.g., reachable, within map bounds)
        //       and return REJECT for invalid goals.
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
      }

      // TODO: implement handle_cancel(...) and handle_accepted(...), plus the
      //       execution loop that publishes feedback and sets the result.

.. dropdown:: Static Transforms
   :open:
   :color: primary

   Static transforms describe spatial relationships that never change at
   runtime, such as where a sensor is bolted onto the robot body. You
   will publish these once at startup.

   **Steps:**

   #. Choose the fixed sensor mounts on your rescue robot and broadcast a
      static transform for each one. Each transform's parent is the
      robot body frame and its child is the sensor frame, for example:

      - ``base_link`` → ``thermal_camera_link`` (the thermal camera used
        to detect victims by heat signature).
      - ``base_link`` → ``gas_sensor_link`` (the gas sensor used to
        detect hazardous atmospheres).

   #. Create a ``tf2_ros::StaticTransformBroadcaster`` and, for each
      mount, fill in a ``geometry_msgs::msg::TransformStamped`` with the
      parent frame, child frame, and the measured offset (translation
      and rotation) of the sensor relative to ``base_link``.
   #. Broadcast each static transform once during node setup.

   The skeleton below shows the API to use. Replace the ``// TODO``
   comments with your implementation.

   .. code-block:: cpp
      :caption: Static transform broadcast (skeleton)

      // TODO: create a StaticTransformBroadcaster member, e.g.
      //       std::make_shared<tf2_ros::StaticTransformBroadcaster>(this)

      geometry_msgs::msg::TransformStamped t;
      // TODO: set t.header.stamp to the current time
      // TODO: set t.header.frame_id to the parent frame (e.g. "base_link")
      // TODO: set t.child_frame_id to the sensor frame (e.g. "thermal_camera_link")
      // TODO: set t.transform.translation (x, y, z) to the measured sensor offset
      // TODO: set t.transform.rotation (from a quaternion) to the sensor orientation

      // TODO: broadcast the transform once with sendTransform(t)

   **Acceptance criteria:**

   - At least two static transforms appear in the TF tree (verified with
     ``view_frames``), each connecting ``base_link`` to a sensor frame.

.. dropdown:: Dynamic Transforms
   :open:
   :color: primary

   Dynamic transforms describe relationships that change as the robot
   moves. The key one is the robot's pose in the world.

   **Steps:**

   #. Broadcast the robot's pose as a dynamic transform from the fixed
      world frame to the robot body frame
      (``world`` → ``robot_base_link``). This places the moving robot
      inside the static map.
   #. Update the transform continuously from the robot's motion. Drive it
      either from an odometry subscription (an ``/odom`` callback) or
      from commanded motion on a timer.
   #. Use a ``tf2_ros::TransformBroadcaster`` and call ``sendTransform``
      each time you have a new pose, stamping each transform with the
      time of the source data.

   The skeleton below shows the API to use. Replace the ``// TODO``
   comments with your implementation.

   .. code-block:: cpp
      :caption: Dynamic transform broadcast (skeleton)

      // TODO: create a TransformBroadcaster member, e.g.
      //       std::make_unique<tf2_ros::TransformBroadcaster>(*this)

      void odom_callback(const nav_msgs::msg::Odometry::SharedPtr msg)
      {
        geometry_msgs::msg::TransformStamped t;
        // TODO: set t.header.stamp from msg->header.stamp
        // TODO: set t.header.frame_id to "world" (parent)
        // TODO: set t.child_frame_id to "robot_base_link" (child)
        // TODO: copy the robot position from msg->pose.pose.position into t.transform.translation
        // TODO: copy the robot orientation from msg->pose.pose.orientation into t.transform.rotation

        // TODO: broadcast the updated transform with sendTransform(t)
      }

   **Acceptance criteria:**

   - The ``world`` → ``robot_base_link`` edge updates over time, and the
     robot frame visibly moves in RViz2 as the robot drives.

.. dropdown:: Transform Listener
   :open:
   :color: primary

   The decision layer needs to compare positions that arrive in
   different frames. A transform listener lets you ask TF2 for the
   relationship between any two connected frames.

   **Steps:**

   #. In the node that feeds the decision layer (perception or the
      decision node itself), create a ``tf2_ros::Buffer`` and a
      ``tf2_ros::TransformListener`` that fills it.
   #. Look up the transform you need with ``lookupTransform``, for
      example ``world`` to ``robot_base_link`` to obtain the robot's
      pose in the world frame, or ``world`` to a reported victim frame.
   #. Compute the spatial relationship the decision layer consumes, for
      example the straight-line distance from the robot to a reported
      victim, expressed in the ``world`` frame, so the decision node can
      pick the closest victim.
   #. Wrap every lookup in a try/catch for ``tf2::TransformException``.
      A transform may not be available yet (frames not connected, data
      not arrived), so a failed lookup must log a warning and skip that
      cycle rather than crash the node.

   The skeleton below shows the API to use. Replace the ``// TODO``
   comments with your implementation.

   .. code-block:: cpp
      :caption: Transform lookup (skeleton)

      // TODO: declare a tf2_ros::Buffer (constructed with this->get_clock())
      // TODO: declare a tf2_ros::TransformListener bound to that buffer

      try {
        // TODO: look up the transform you need, e.g.
        //       tf_buffer_.lookupTransform("world", "robot_base_link", tf2::TimePointZero)
        // TODO: use the translation/rotation to compute a distance or goal
        //       for the decision layer
      } catch (const tf2::TransformException& ex) {
        // TODO: log a warning with ex.what() and skip this cycle
      }

   **Acceptance criteria:**

   - The decision layer uses a value derived from a TF2 lookup (for
     example a robot-to-victim distance in the ``world`` frame).
   - A missing or temporarily unavailable transform is handled
     gracefully (logged warning, no crash).

.. dropdown:: Autonomy Architecture and Decision Layer
   :open:
   :color: primary

   Organize your system into the **Sense-Plan-Act** layers from
   :doc:`Lecture 14 </lectures/lecture14/l14_index>`. Your GP1 nodes and
   the nodes from the requirements above should be reorganized (renamed
   or regrouped) so that every node clearly belongs to exactly one of the
   three layers below.

   - **Perception (Sense)**: a node (or nodes) that turns raw sensor
     data (``/scan``, ``/odom``, victim reports) into a compact,
     higher-level description of the world. Concretely, perception
     should publish a world-state message on a dedicated topic (for
     example ``/world_state``), containing items such as the nearest
     obstacle distance, the list of detected/reported victims, and the
     robot's current pose.
   - **Decision (Plan)**: a node that consumes the world-state output
     and decides what to do next (the robot's "intelligence"). It does
     not read raw sensors directly; it reasons over the perception
     summary plus spatial information from TF2.
   - **Control (Act)**: a node that turns the decision into motion by
     publishing the resulting command (for example ``/cmd_vel``) or by
     sending an action goal (for example a ``NavigateToVictim`` goal from
     the Custom Action requirement) to drive the robot.

   Implement a **decision node** that:

   - **Consumes** perception output. Subscribe to the world-state topic
     (and/or ``/scan``) so the decision is based on the perception
     summary rather than raw sensor noise.
   - **Publishes** a command. Output either a velocity command on
     ``/cmd_vel`` or an action goal on the control layer's interface.
     The decision node must publish on every decision cycle (for
     example on a timer or on each new world-state message).
   - Uses a **rule-based policy** (required). Implement at least one
     clearly documented rule, for example: select the next unsearched
     waypoint, react to a close obstacle by turning away, or choose
     which reported victim to navigate to next (such as the closest
     one).
   - Uses **TF2** to reason spatially before deciding. For example,
     transform a detected victim's position into the ``world`` frame so
     that distances and goals are computed in one consistent frame (see
     the Transform Listener requirement).

   **Acceptance criteria:**

   - The README clearly maps each node to perception, decision, or
     control.
   - The decision node subscribes to perception output (not raw
     sensors) and publishes a command on a control interface.
   - At least one rule-based decision rule is documented and observable
     in the running system (for example, the robot visibly reacts to an
     obstacle or selects a victim).

   .. admonition:: Optional bonus: a learned decision policy
      :class: tip

      For extra credit, replace the rule-based policy with a **learned
      model** loaded for inference in C++ (OpenCV DNN, ONNX Runtime, or
      LibTorch), for example, a small classifier that labels a scan or
      image patch as "victim / no victim". Keep the **same topic
      interface** so no other node changes. This is intentionally
      optional; a rule-based decision earns full marks.


.. dropdown:: Integration
   :open:
   :color: primary

   **Goal:** combine everything into one search-and-rescue system: the GP1
   pub/sub pipeline, the services and actions, several robot types, TF2,
   and the autonomy layers.

   **Step 1: Preserve the GP1 pipeline.** The publishers and subscribers from
   GP1 (for example, victim reports flowing from sensing to reporting) must keep
   working. The new capabilities are additions, not replacements.

   **Step 2: Connect the new pieces to the existing data flow.** For example, a
   victim location detected and published by the GP1 pub/sub system can become
   the goal of a ``NavigateToVictim`` action, and a ``DispatchRobot`` service
   call can select which robot type responds.

   **Step 3: Support multiple robot types at once.** At least two derived robot
   types (for example, ``GroundSearchBot`` and ``AerialSurveyBot``) must run
   concurrently in the same simulation, each with its own node name and
   parameters and without topic, service, or action name collisions (use
   namespaces or remapping as needed).

   **Step 4: Provide a single launch file** that starts every component:
   Gazebo, each robot node, the service and action servers, the TF2
   broadcasters, and the perception, decision, and control nodes. Launching
   this one file must bring up the complete system.

   **Step 5: Verify the TF tree.** Generate the frame tree and confirm that the
   static sensor frames, the dynamic ``world`` → ``robot_base_link`` edge, and
   any victim frames all connect into a single tree with no disconnected
   frames:

   .. code-block:: bash

      ros2 run tf2_tools view_frames

   **Step 6: Visualize the frames in RViz2** (add a TF display) and confirm the
   robot frame moves as the robot drives.

   **Acceptance criteria:**

   - After launching, the GP1 topics still publish as before, and the new
     service and action interfaces are both discoverable (for example, with
     ``ros2 service list`` and ``ros2 action list``).
   - Both robot types appear as separate nodes and operate without name
     conflicts.
   - ``view_frames`` produces a single connected tree containing the
     static, dynamic, and victim frames.
   - The TF display in RViz2 shows the moving robot frame.

------------
Deliverables
------------

- Updated ROS 2 package(s) with all source code, building on GP1.
- Custom service (``.srv``) and action (``.action``) definitions.
- One launch file that starts all components.
- A short **architecture description** in the README mapping your nodes to the perception / decision / control layers.
- TF2 frame tree diagram (generated with ``view_frames``).
- ``README.md`` with complete build, run, and usage documentation.
- Video demo (2 to 3 minutes) showing a service call, an action running with feedback, and the decision layer driving the robot.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - Robot Inheritance (base class, derived types, polymorphism)
     - 15%
   * - Services (custom ``.srv``, server implementation, client implementation)
     - 15%
   * - Actions (custom ``.action``, server with feedback, client)
     - 15%
   * - TF2 Frames (static broadcasts, dynamic broadcasts, transform listener)
     - 15%
   * - Autonomy Architecture and Decision Layer (Sense-Plan-Act organization, decision node)
     - 15%
   * - Integration (GP1 features functional, multi-robot, one launch file, RViz2 visualization)
     - 10%
   * - Code Quality (naming conventions, uniform initialization, ``'\n'`` usage, structure)
     - 5%
   * - Documentation and Demo (README, video, frame tree diagram)
     - 10%

.. note::

   The optional learned decision policy is **extra credit**; a complete
   rule-based decision layer earns full marks on the autonomy criterion.

----------
Final Note
----------

.. admonition:: Congratulations
   :class: tip

   This assignment is the culmination of the entire ENPM702 course, from basic C++ variables and control flow in RWA1 to a full ROS 2 search-and-rescue robot organized as a Sense-Plan-Act autonomy architecture, with services, actions, coordinate frames, and a decision layer. Your final submission should demonstrate mastery of modern C++ programming, object-oriented design, and the ROS 2 framework for building real robotic systems.
