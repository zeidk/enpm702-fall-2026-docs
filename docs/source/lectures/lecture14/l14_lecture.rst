====================================================
Lecture
====================================================


Lifecycle Nodes
====================================================

This lecture builds on the coordinate-frame material from
:doc:`Lecture 13 <../lecture13/l13_index>` and covers **lifecycle
(managed) nodes** in detail.

A standard ROS 2 node begins executing as soon as it is started. This
can be problematic in complex systems where nodes depend on each other
or where you need deterministic startup and shutdown behavior.

**Lifecycle nodes** (also called managed nodes) address this by
introducing a **state machine** that controls the node's execution.
This enables:

- **Deterministic startup**, configure resources before activating.
- **Coordinated bringup**, bring up nodes in a specific order.
- **Error handling**, transition to error states and recover.
- **Clean shutdown**, release resources in a controlled manner.


The Lifecycle State Machine
----------------------------------------------------

A lifecycle node can be in one of four **primary states**:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - State
     - Description
   * - **Unconfigured**
     - Initial state. The node has been created but not yet configured.
   * - **Inactive**
     - Configured but not processing. Publishers, subscribers, and
       timers are created but not active.
   * - **Active**
     - Fully operational. The node processes data and executes callbacks.
   * - **Finalized**
     - Terminal state. The node has been shut down and cannot be restarted.

There are also **transition states** (Configuring, Activating,
Deactivating, CleaningUp, ShuttingDown, ErrorProcessing) that exist
while a transition is in progress.


Lifecycle Transitions
----------------------------------------------------

The transitions between primary states are:

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Transition
     - From
     - To
     - Callback
   * - ``configure``
     - Unconfigured
     - Inactive
     - ``on_configure()``
   * - ``activate``
     - Inactive
     - Active
     - ``on_activate()``
   * - ``deactivate``
     - Active
     - Inactive
     - ``on_deactivate()``
   * - ``cleanup``
     - Inactive
     - Unconfigured
     - ``on_cleanup()``
   * - ``shutdown``
     - Any (except Finalized)
     - Finalized
     - ``on_shutdown()``

.. note::

   Each transition callback returns a ``CallbackReturn`` value:

   - ``CallbackReturn::SUCCESS``, transition completes successfully.
   - ``CallbackReturn::FAILURE``, transition fails, node stays in or
     returns to the previous primary state.
   - ``CallbackReturn::ERROR``, a critical error occurred, the node
     transitions to the ErrorProcessing state.


----


Implementing Lifecycle Nodes
====================================================

To create a lifecycle node, inherit from
``rclcpp_lifecycle::LifecycleNode`` instead of ``rclcpp::Node``.


Complete Example: Lifecycle Sensor Node
----------------------------------------------------

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <rclcpp_lifecycle/lifecycle_node.hpp>
   #include <std_msgs/msg/float64.hpp>
   #include <string>

   using CallbackReturn =
       rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

   class LifecycleSensorNode
       : public rclcpp_lifecycle::LifecycleNode {
    public:
     LifecycleSensorNode()
         : LifecycleNode{"lifecycle_sensor_node"} {
       RCLCPP_INFO(this->get_logger(), "Node created (Unconfigured)");
     }

     // Called during the configure transition
     CallbackReturn on_configure(
         const rclcpp_lifecycle::State& /*previous_state*/) override {
       RCLCPP_INFO(this->get_logger(), "Configuring...");

       // Create publisher (inactive until activated)
       publisher_ = this->create_publisher<std_msgs::msg::Float64>(
           "sensor_data", 10);

       // Create timer (inactive until activated)
       timer_ = this->create_wall_timer(
           std::chrono::milliseconds{500},
           std::bind(&LifecycleSensorNode::publish_data, this));

       // Initialize sensor value
       sensor_value_ = 0.0;

       RCLCPP_INFO(this->get_logger(), "Configured successfully");
       return CallbackReturn::SUCCESS;
     }

     // Called during the activate transition
     CallbackReturn on_activate(
         const rclcpp_lifecycle::State& /*previous_state*/) override {
       RCLCPP_INFO(this->get_logger(), "Activating...");
       // The publisher is now active and can send messages
       RCLCPP_INFO(this->get_logger(), "Activated -- publishing data");
       return CallbackReturn::SUCCESS;
     }

     // Called during the deactivate transition
     CallbackReturn on_deactivate(
         const rclcpp_lifecycle::State& /*previous_state*/) override {
       RCLCPP_INFO(this->get_logger(), "Deactivating...");
       // The publisher stops sending messages
       RCLCPP_INFO(this->get_logger(), "Deactivated -- stopped publishing");
       return CallbackReturn::SUCCESS;
     }

     // Called during the cleanup transition
     CallbackReturn on_cleanup(
         const rclcpp_lifecycle::State& /*previous_state*/) override {
       RCLCPP_INFO(this->get_logger(), "Cleaning up...");
       // Release resources
       publisher_.reset();
       timer_.reset();
       RCLCPP_INFO(this->get_logger(), "Cleaned up");
       return CallbackReturn::SUCCESS;
     }

     // Called during the shutdown transition
     CallbackReturn on_shutdown(
         const rclcpp_lifecycle::State& /*previous_state*/) override {
       RCLCPP_INFO(this->get_logger(), "Shutting down...");
       publisher_.reset();
       timer_.reset();
       RCLCPP_INFO(this->get_logger(), "Shut down complete");
       return CallbackReturn::SUCCESS;
     }

    private:
     void publish_data() {
       // Only publish if the node is in the Active state
       if (this->get_current_state().id() !=
           lifecycle_msgs::msg::State::PRIMARY_STATE_ACTIVE) {
         return;
       }

       auto msg = std_msgs::msg::Float64{};
       msg.data = sensor_value_;
       publisher_->publish(msg);
       RCLCPP_INFO(this->get_logger(), "Published: %.2f", sensor_value_);
       sensor_value_ += 0.1;
     }

     rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::Float64>::SharedPtr
         publisher_;
     rclcpp::TimerBase::SharedPtr timer_;
     double sensor_value_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(
         std::make_shared<LifecycleSensorNode>()->get_node_base_interface());
     rclcpp::shutdown();
     return 0;
   }

.. important::

   Lifecycle publishers (``LifecyclePublisher``) only transmit messages
   when the node is in the **Active** state. Messages published in any
   other state are silently dropped.


CMakeLists.txt Additions
----------------------------------------------------

Add the ``rclcpp_lifecycle`` and ``lifecycle_msgs`` dependencies:

.. code-block:: cmake

   find_package(rclcpp_lifecycle REQUIRED)
   find_package(lifecycle_msgs REQUIRED)

   ament_target_dependencies(my_lifecycle_node
     rclcpp
     rclcpp_lifecycle
     lifecycle_msgs
     std_msgs
   )

Also add to ``package.xml``:

.. code-block:: xml

   <depend>rclcpp_lifecycle</depend>
   <depend>lifecycle_msgs</depend>


----


Managing Lifecycle Nodes
====================================================

Once a lifecycle node is running, you can control its state using the
``ros2 lifecycle`` CLI or programmatically.


CLI Commands
----------------------------------------------------

.. code-block:: bash

   # List all lifecycle nodes
   ros2 lifecycle nodes

   # Get the current state of a lifecycle node
   ros2 lifecycle get /lifecycle_sensor_node

   # List available transitions from the current state
   ros2 lifecycle list /lifecycle_sensor_node

   # Trigger a transition
   ros2 lifecycle set /lifecycle_sensor_node configure
   ros2 lifecycle set /lifecycle_sensor_node activate
   ros2 lifecycle set /lifecycle_sensor_node deactivate
   ros2 lifecycle set /lifecycle_sensor_node cleanup
   ros2 lifecycle set /lifecycle_sensor_node shutdown


Typical Startup Sequence
----------------------------------------------------

.. code-block:: bash

   # 1. Start the node (enters Unconfigured state)
   ros2 run my_package lifecycle_sensor_node

   # 2. Configure the node (Unconfigured -> Inactive)
   ros2 lifecycle set /lifecycle_sensor_node configure

   # 3. Activate the node (Inactive -> Active)
   ros2 lifecycle set /lifecycle_sensor_node activate

   # Node is now publishing data

   # 4. Deactivate when done (Active -> Inactive)
   ros2 lifecycle set /lifecycle_sensor_node deactivate

   # 5. Clean up (Inactive -> Unconfigured) or shutdown
   ros2 lifecycle set /lifecycle_sensor_node shutdown


Programmatic Transitions
----------------------------------------------------

You can also trigger transitions programmatically from another node
using the lifecycle service interfaces:

.. code-block:: cpp

   #include <lifecycle_msgs/srv/change_state.hpp>
   #include <lifecycle_msgs/msg/transition.hpp>

   // Create a client for the change_state service
   auto client = this->create_client<lifecycle_msgs::srv::ChangeState>(
       "/lifecycle_sensor_node/change_state");

   // Create a request to configure the node
   auto request =
       std::make_shared<lifecycle_msgs::srv::ChangeState::Request>();
   request->transition.id =
       lifecycle_msgs::msg::Transition::TRANSITION_CONFIGURE;

   // Send the request asynchronously
   auto future = client->async_send_request(request);

This approach is useful for building **lifecycle managers** that
coordinate the startup and shutdown of multiple lifecycle nodes in
a specific order.

