.. _gp3:

============================================================
GP3: Autonomy Frames, Lifecycle, and a Decision Layer
============================================================

Overview
--------

This is the final extension of the Group Project system, and your team's capstone. You will organize your nodes into a **robot autonomy architecture**, the Sense-Plan-Act stack from **Lecture 15**, and complete it with two production-grade capabilities: coordinate frame management with **TF2** for spatial reasoning, and **lifecycle nodes** for managed startup and shutdown. The heart of this assignment is a **decision layer**: the node that turns perception into action and is where Artificial Intelligence fits in a robot. By the end your team will have a complete, multi-node ROS 2 search-and-rescue system spanning publishers, subscribers, services, actions, coordinate frames, lifecycle management, and an autonomy decision layer.

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Organize a ROS 2 system into perception, decision, and control layers (Sense-Plan-Act).
#. Implement a decision node that maps perception to action, the layer where AI/ML fits.
#. Broadcast static and dynamic transforms using TF2 and use them for spatial reasoning.
#. Implement lifecycle nodes for managed startup and shutdown.
#. Coordinate lifecycle transitions across multiple nodes.
#. Build a production-ready, multi-node ROS 2 autonomy system.

------------
Requirements
------------

.. dropdown:: Autonomy Architecture and Decision Layer
   :open:
   :color: primary

   Organize your system into the **Sense-Plan-Act** layers from
   :doc:`Lecture 15 </lectures/lecture15/l15_index>`. Your existing GP1
   and GP2 nodes should be reorganized (renamed or regrouped) so that
   every node clearly belongs to exactly one of the three layers below.

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
     sending an action goal (for example a navigation goal reused from
     GP2) to drive the robot.

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

.. dropdown:: Lifecycle Nodes
   :open:
   :color: primary

   Lifecycle nodes give you explicit, managed startup and shutdown
   instead of nodes that begin running the instant they are launched.
   See :doc:`Lectures 13/14 </lectures/lecture13/l13_index>` for the
   state machine (Unconfigured, Inactive, Active, Finalized) and its
   transitions.

   **Steps:**

   #. Convert **at least 2** existing nodes to lifecycle nodes by
      deriving from ``rclcpp_lifecycle::LifecycleNode`` instead of
      ``rclcpp::Node``. The perception/sensor node and the decision node
      are good candidates.
   #. Implement the transition callbacks, each returning
      ``CallbackReturn::SUCCESS`` on success:

      - ``on_configure``: create publishers, subscribers, timers, and
        read parameters, but do not yet produce output.
      - ``on_activate``: activate lifecycle publishers and enable
        processing so the node starts producing output.
      - ``on_deactivate``: deactivate lifecycle publishers and pause
        processing so the node stops producing output.
      - ``on_cleanup``: release the resources created in
        ``on_configure`` (reset publishers, subscribers, timers).
      - ``on_shutdown``: perform final cleanup before the node is
        destroyed.

   #. Use ``LifecyclePublisher`` for outputs, and ensure a node
      **only** publishes data while it is in the **Active** state. In
      the Inactive state it must be silent.
   #. Make the state changes observable by logging on entry to each
      callback, so a grader can see the transitions in the console.

   The skeleton below shows the API to use. Replace the ``// TODO``
   comments with your implementation.

   .. code-block:: cpp
      :caption: Lifecycle node (skeleton)

      class SensorNode : public rclcpp_lifecycle::LifecycleNode {
       public:
        SensorNode(const rclcpp::NodeOptions& options)
            : rclcpp_lifecycle::LifecycleNode{"sensor_node", options} {}

        CallbackReturn on_configure(const rclcpp_lifecycle::State&) override
        {
          // TODO: log "configuring"
          // TODO: create the lifecycle publisher(s), subscriber(s), and parameters
          // TODO: return CallbackReturn::SUCCESS
        }

        CallbackReturn on_activate(const rclcpp_lifecycle::State&) override
        {
          // TODO: log "activating"
          // TODO: activate the lifecycle publisher(s) and enable processing
          // TODO: return CallbackReturn::SUCCESS
        }

        CallbackReturn on_deactivate(const rclcpp_lifecycle::State&) override
        {
          // TODO: log "deactivating"
          // TODO: deactivate the lifecycle publisher(s) and pause processing
          // TODO: return CallbackReturn::SUCCESS
        }

        // TODO: implement on_cleanup (release resources)
        // TODO: implement on_shutdown (final cleanup)

       private:
        // TODO: declare lifecycle publisher(s), e.g.
        //       rclcpp_lifecycle::LifecyclePublisher<sensor_msgs::msg::LaserScan>::SharedPtr scan_pub_;
      };

   **Acceptance criteria:**

   - At least two nodes are lifecycle nodes with all five transition
     callbacks implemented.
   - A node publishes only in the Active state and is silent in the
     Inactive state, demonstrable by toggling activate/deactivate.
   - Each transition is visible in the logs.

.. dropdown:: System Coordination
   :open:
   :color: primary

   Because the autonomy stack has dependencies (the decision layer is
   useless before perception is producing output), you must bring nodes
   up in a defined order rather than all at once.

   **Steps:**

   #. Create a launch file that starts your lifecycle nodes and drives
      their transitions, either through launch event handlers or an
      explicit coordination node/script.
   #. Demonstrate orderly startup:

      #. Configure all nodes (Unconfigured to Inactive).
      #. Activate the perception/sensor nodes first, so world-state
         output is flowing.
      #. Then activate the decision and control nodes, so commands are
         only issued once perception is live.

   #. Demonstrate orderly shutdown in the reverse order: deactivate
      control and decision first, then perception, then clean up.

   **Acceptance criteria:**

   - Launching the system brings the stack to the fully Active state in
     the order above, observable in the logs.
   - Shutdown deactivates nodes in reverse order without errors.

.. dropdown:: Integration
   :open:
   :color: primary

   The capstone must combine everything: GP1 and GP2 features still work,
   now wrapped in the autonomy architecture, TF2, and lifecycle
   management.

   **Steps:**

   #. Confirm that all components from GP1 and GP2 remain fully
      functional, now organized under the perception/decision/control
      layers (nothing from earlier assignments should regress).
   #. Verify the TF tree. Generate the frame tree and confirm that the
      static sensor frames, the dynamic ``world`` → ``robot_base_link``
      edge, and any victim frames all connect into a single tree with no
      disconnected frames:

      .. code-block:: bash

         ros2 run tf2_tools view_frames

   #. Visualize the frames in RViz2 (add a TF display) and confirm the
      robot frame moves as the robot drives.
   #. Verify lifecycle management from the CLI. List the available
      transitions and drive a node between states, confirming its
      publishing behavior changes accordingly:

      .. code-block:: bash

         ros2 lifecycle list /sensor_node
         ros2 lifecycle set /sensor_node activate
         ros2 lifecycle set /sensor_node deactivate

   **Acceptance criteria:**

   - GP1 and GP2 features still run under the new architecture.
   - ``view_frames`` produces a single connected tree containing the
     static, dynamic, and victim frames.
   - The TF display in RViz2 shows the moving robot frame.
   - Lifecycle nodes can be activated and deactivated from the CLI, with
     publishing starting and stopping accordingly.

------------
Deliverables
------------

- Final ROS 2 package(s) with all features from GP1, GP2, and GP3.
- A short **architecture description** in the README mapping your nodes to the perception / decision / control layers.
- TF2 frame tree diagram (generated via ``view_frames``).
- Updated launch file with lifecycle management.
- Final ``README.md`` with complete build, run, and usage documentation.
- Video demo (2-3 minutes) showing the full system in operation.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - Autonomy Architecture and Decision Layer (Sense-Plan-Act organization, decision node)
     - 20%
   * - TF2 Frames (static broadcasts, dynamic broadcasts, transform listener)
     - 25%
   * - Lifecycle Nodes (transition callbacks, state-dependent behavior, coordination)
     - 25%
   * - Integration (GP1 + GP2 features functional, RViz2 visualization, CLI management)
     - 10%
   * - Code Quality (naming conventions, uniform initialization, ``'\n'`` usage, structure)
     - 10%
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

   This assignment is the culmination of the entire ENPM702 course, from basic C++ variables and control flow in RWA1 to a full ROS 2 search-and-rescue robot organized as a Sense-Plan-Act autonomy architecture, complete with coordinate frames, lifecycle management, and a decision layer. Your final submission should demonstrate mastery of modern C++ programming, object-oriented design, and the ROS 2 framework for building real robotic systems.
