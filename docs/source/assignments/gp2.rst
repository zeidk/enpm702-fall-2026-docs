.. _gp2:

=============================================
GP2: Services, Actions, and Robot Inheritance
=============================================

Overview
--------

This assignment extends your GP1 system by adding request-response communication through **services** and long-running task management through **actions**. You will also introduce a robot type hierarchy using C++ inheritance, a base ``RobotNode`` class with derived types that have different ROS parameters and behaviors. By the end, your search-and-rescue simulation will support multiple robot types that can be dispatched via services and sent on search/navigation tasks via actions alongside the existing pub/sub architecture.

-------------------
Learning Objectives
-------------------

By the end of this assignment you will be able to:

#. Implement ROS 2 services for synchronous request-response operations.
#. Implement ROS 2 actions for long-running tasks with periodic feedback.
#. Design a class hierarchy for robot nodes using C++ inheritance.
#. Apply polymorphism to differentiate robot behaviors at runtime.
#. Integrate services and actions with the existing pub/sub system from GP1.

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

.. dropdown:: Integration
   :open:
   :color: primary

   **Goal:** combine the new services and actions with your GP1 pub/sub system
   into one cohesive multi-robot search-and-rescue simulation.

   **Step 1: Preserve the GP1 pipeline.** The publishers and subscribers from
   GP1 (for example, victim reports flowing from sensing to reporting) must keep
   working unchanged. The service and action capabilities are additions, not
   replacements.

   **Step 2: Connect the new pieces to the existing data flow.** For example, a
   victim location detected and published by the GP1 pub/sub system can become
   the goal of a ``NavigateToVictim`` action, and a ``DispatchRobot`` service
   call can select which robot type responds.

   **Step 3: Support multiple robot types at once.** At least two derived robot
   types (for example, ``GroundSearchBot`` and ``AerialSurveyBot``) must run
   concurrently in the same simulation, each with its own node name and
   parameters and without topic, service, or action name collisions (use
   namespaces or remapping as needed).

   **Step 4: Provide a single launch file** that starts every component: Gazebo,
   each robot node, and the service and action servers. Launching this one file
   must bring up the complete system.

   **Acceptance criteria:**

   - After launching, the GP1 topics still publish as before, and the new
     service and action interfaces are both discoverable (for example, with
     ``ros2 service list`` and ``ros2 action list``).
   - Both robot types appear as separate nodes and operate without name
     conflicts.

------------
Deliverables
------------

- Updated ROS 2 package(s) with all source code.
- Custom service (``.srv``) and action (``.action``) definitions.
- Updated launch file that starts all components.
- ``README.md`` with build and run instructions.
- Short video demo showing services being called and actions executing with feedback.

--------------
Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 50 15

   * - Criterion
     - Weight
   * - Services (custom ``.srv``, server implementation, client implementation)
     - 25%
   * - Actions (custom ``.action``, server with feedback, client)
     - 25%
   * - Robot Inheritance (base class, derived types, polymorphism)
     - 25%
   * - Integration (pub/sub still functional, multi-robot, launch file)
     - 15%
   * - Documentation and Demo (README, video)
     - 10%
