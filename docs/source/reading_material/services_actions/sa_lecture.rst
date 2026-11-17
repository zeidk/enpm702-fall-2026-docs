====================================================
Lecture
====================================================


.. note::

   **Where the outputs come from.** Every C++ example on this page was
   built with the course flags (``-std=c++20 -Wall -Wextra
   -pedantic-errors -Wshadow``) without a warning, on ROS 2 Jazzy. Every
   output is pasted from a run of these files. The numbers in the
   examples (a fare of 5 dollars plus 2 dollars per km, a speed of
   2 m/s, a timeout of 3 s) were chosen for the examples.


Three Ways Nodes Talk
====================================================

In :doc:`Lecture 10 </lectures/lecture10/l10_index>`, the robotaxi node
published its position on a **topic**, and the dispatcher node
subscribed to it. A topic is one way for nodes to exchange data. ROS 2
has two more, for jobs that a topic does badly:

- A **service** is a question with one answer. A client sends a
  **request**, the server computes a **response**, and the exchange is
  over. A client that asks for the fare of a ride needs the fare, once.
  A topic would send the fare to every subscriber, all the time.
- An **action** is a task that takes time. A client sends a **goal**.
  While the server works, it sends **feedback**. At the end, it sends a
  **result**. The client can **cancel** the goal before the end. A drive
  to the pickup point is a task of this kind.

.. list-table::
   :header-rows: 1
   :widths: 16 28 28 28
   :class: compact-table

   * -
     - Topic
     - Service
     - Action
   * - What it carries
     - A stream of messages
     - One request, one response
     - One goal, feedback, one result
   * - Who talks
     - Any number of publishers and subscribers
     - Many clients, one server
     - Many clients, one server
   * - The caller waits
     - No
     - For one response
     - For nothing: it receives callbacks
   * - Can stop early
     - Not applicable
     - No
     - Yes, with a cancel request
   * - Robotaxi example
     - ``robotaxi/position``
     - The fare of a ride
     - Drive to x = 10 m

The rest of the page builds one example of each, with two nodes each: a
server and a client. Both use an interface that you define in a package
of your own.


Interfaces in a Package
====================================================

A topic's message type comes from a ``.msg`` file. A service's types
come from a ``.srv`` file, and an action's from an ``.action`` file. All
of them live in one **interface package**, as in :doc:`Lecture 11
</lectures/lecture11/l11_index>`. The package ``sa_interfaces`` holds
one service and one action.

The service ``ComputeFare`` has two parts, separated by ``---``. Above
the line is the request. Below the line is the response.

``sa_interfaces/srv/ComputeFare.srv``:

.. code-block:: text

   # The request: how far the ride is, in m.
   float64 distance_m
   ---
   # The response: what the ride costs, in dollars.
   float64 fare

The action ``Drive`` has three parts, separated by two ``---`` lines:
the goal, the result and the feedback, in that order.

``sa_interfaces/action/Drive.action``:

.. code-block:: text

   # The goal: the x position to drive to, in m.
   float64 target_x
   ---
   # The result: where the robotaxi stopped, in m.
   float64 final_x
   ---
   # The feedback: where the robotaxi is now, in m.
   float64 current_x

The package builds both files with ``rosidl_generate_interfaces``:

``sa_interfaces/CMakeLists.txt``:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.8)
   project(sa_interfaces)

   find_package(ament_cmake REQUIRED)
   find_package(rosidl_default_generators REQUIRED)

   # Generates the C++ code for each file, for example sa_interfaces/srv/compute_fare.hpp.
   rosidl_generate_interfaces(${PROJECT_NAME}
     "srv/ComputeFare.srv"
     "action/Drive.action"
   )

   ament_package()

``sa_interfaces/package.xml``:

.. code-block:: xml

   <?xml version="1.0"?>
   <package format="3">
     <name>sa_interfaces</name>
     <version>0.0.0</version>
     <description>A service and an action for the Services and Actions reading.</description>
     <maintainer email="zeidk@umd.edu">zeidk</maintainer>
     <license>Apache-2.0</license>

     <buildtool_depend>ament_cmake</buildtool_depend>
     <buildtool_depend>rosidl_default_generators</buildtool_depend>

     <exec_depend>rosidl_default_runtime</exec_depend>

     <member_of_group>rosidl_interface_packages</member_of_group>

     <export>
       <build_type>ament_cmake</build_type>
     </export>
   </package>

After ``colcon build`` and ``source install/setup.bash``,
``ros2 interface show`` prints each file:

.. code-block:: bash

   ros2 interface show sa_interfaces/srv/ComputeFare
   ros2 interface show sa_interfaces/action/Drive

.. code-block:: text

   # The request: how far the ride is, in m.
   float64 distance_m
   ---
   # The response: what the ride costs, in dollars.
   float64 fare

.. code-block:: text

   # The goal: the x position to drive to, in m.
   float64 target_x
   ---
   # The result: where the robotaxi stopped, in m.
   float64 final_x
   ---
   # The feedback: where the robotaxi is now, in m.
   float64 current_x

ROS 2 also ships ready-made service types. ``std_srvs/srv/SetBool``
carries one ``bool`` and answers with a ``bool`` and a ``string``.
``std_srvs/srv/Trigger`` has an empty request, so its file starts with
the ``---`` line. ``std_srvs/srv/Empty`` has nothing on either side.

.. code-block:: text

   bool data # e.g. for hardware enabling / disabling
   ---
   bool success   # indicate successful run of triggered service
   string message # informational, e.g. for error messages

.. code-block:: text

   ---
   bool success   # indicate successful run of triggered service
   string message # informational, e.g. for error messages

Use a ready-made type when it says what you need. Write your own when
the request or the response needs fields with names of their own, as
``distance_m`` and ``fare`` do.


Services
====================================================

A service has a **server**, a node that offers the service under a
name, and a **client**, a node that calls it. Here, ``fare_node`` is the
server of ``compute_fare``, and ``dispatcher_node`` is its client.

The Server
----------------------------------------------------

``create_service<Type>(name, callback)`` offers the service. The
callback receives the request and a response that it fills in. It
returns nothing: the server sends the response when the callback ends.
The callback runs in the executor, as a subscription callback does, so
it must end quickly.

``sa_demo/include/sa_demo/fare_node.hpp``:

.. code-block:: cpp

   #pragma once
   #include <functional>
   #include <memory>
   #include <sa_interfaces/srv/compute_fare.hpp>
   #include <rclcpp/rclcpp.hpp>

   namespace sa_demo {

   // Serves compute_fare: the fare is the base fare plus a price for each km.
   class FareNode : public rclcpp::Node {
     public:
       FareNode()
           : rclcpp::Node{"fare_node"},
             service_{create_service<sa_interfaces::srv::ComputeFare>(
                 "compute_fare", std::bind(&FareNode::on_compute_fare, this,
                                           std::placeholders::_1, std::placeholders::_2))} {
           RCLCPP_INFO(get_logger(), "compute_fare is ready");
       }

     private:
       void on_compute_fare(const std::shared_ptr<sa_interfaces::srv::ComputeFare::Request> request,
                            std::shared_ptr<sa_interfaces::srv::ComputeFare::Response> response);
       static constexpr double base_fare_{5.0};    // in dollars, chosen for this example
       static constexpr double price_per_km_{2.0}; // in dollars per km, chosen for this example
       rclcpp::Service<sa_interfaces::srv::ComputeFare>::SharedPtr service_;
   };

   } // namespace sa_demo

``sa_demo/src/fare_node.cpp``:

.. code-block:: cpp

   #include "sa_demo/fare_node.hpp"

   namespace sa_demo {

   void FareNode::on_compute_fare(
       const std::shared_ptr<sa_interfaces::srv::ComputeFare::Request> request,
       std::shared_ptr<sa_interfaces::srv::ComputeFare::Response> response) {
       response->fare = base_fare_ + price_per_km_ * request->distance_m / 1000.0;
       RCLCPP_INFO_STREAM(get_logger(), "distance " << request->distance_m << " m, fare "
                                                    << response->fare);
   }

   } // namespace sa_demo

``sa_demo/src/fare_main.cpp``:

.. code-block:: cpp

   #include <memory>

   #include <rclcpp/rclcpp.hpp>

   #include "sa_demo/fare_node.hpp"

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       auto node{std::make_shared<sa_demo::FareNode>()};
       rclcpp::spin(node);
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

The ``main`` function is the same for every node of this page, except for
the class name and the header.

The Client
----------------------------------------------------

``create_client<Type>(name)`` makes a client. ``async_send_request``
sends a request and returns at once. When the response arrives, the
executor calls the callback you passed, with a ``SharedFuture`` that
already holds the response: ``future.get()`` returns it without waiting.

The client of this page sends one request, 1 s after it starts. The
timer cancels itself in its first call, so the request is sent once.
``service_is_ready()`` tells whether a server for the service exists:
if not, the client says so and does not send.

``sa_demo/include/sa_demo/dispatcher_node.hpp``:

.. code-block:: cpp

   #pragma once
   #include <chrono>
   #include <functional>
   #include <sa_interfaces/srv/compute_fare.hpp>
   #include <rclcpp/rclcpp.hpp>

   namespace sa_demo {

   // After 1 s, asks compute_fare for the fare of one ride, then does nothing.
   // The call never blocks: the response arrives in on_fare.
   class DispatcherNode : public rclcpp::Node {
     public:
       DispatcherNode()
           : rclcpp::Node{"dispatcher_node"},
             client_{create_client<sa_interfaces::srv::ComputeFare>("compute_fare")},
             timer_{create_wall_timer(std::chrono::seconds{1},
                                      std::bind(&DispatcherNode::send_request, this))} {}

     private:
       using Client = rclcpp::Client<sa_interfaces::srv::ComputeFare>;
       void send_request();
       void on_fare(Client::SharedFuture future);
       Client::SharedPtr client_;
       rclcpp::TimerBase::SharedPtr timer_;
   };

   } // namespace sa_demo

``sa_demo/src/dispatcher_node.cpp``:

.. code-block:: cpp

   #include "sa_demo/dispatcher_node.hpp"

   namespace sa_demo {

   void DispatcherNode::send_request() {
       timer_->cancel(); // send one request, not one per second
       if (!client_->service_is_ready()) {
           RCLCPP_WARN(get_logger(), "compute_fare is not available");
           return;
       }
       auto request{std::make_shared<sa_interfaces::srv::ComputeFare::Request>()};
       request->distance_m = 4200.0;
       RCLCPP_INFO_STREAM(get_logger(), "asking the fare of " << request->distance_m << " m");
       client_->async_send_request(request,
                                   std::bind(&DispatcherNode::on_fare, this, std::placeholders::_1));
   }

   void DispatcherNode::on_fare(Client::SharedFuture future) {
       RCLCPP_INFO_STREAM(get_logger(), "the fare is " << future.get()->fare);
   }

   } // namespace sa_demo

The fare of a 4200 m ride is 5.0 + 2.0 × 4.2 = 13.4 dollars. In one
terminal, run ``ros2 run sa_demo fare_exe``. In another, run
``ros2 run sa_demo dispatcher_exe``. The server prints:

.. code-block:: text

   [INFO] [...] [fare_node]: compute_fare is ready
   [INFO] [...] [fare_node]: distance 4200 m, fare 13.4

and the client prints:

.. code-block:: text

   [INFO] [...] [dispatcher_node]: asking the fare of 4200 m
   [INFO] [...] [dispatcher_node]: the fare is 13.4

If you start only the dispatcher, no server exists after 1 s:

.. code-block:: text

   [WARN] [...] [dispatcher_node]: compute_fare is not available

The Build File
----------------------------------------------------

``sa_demo/CMakeLists.txt`` finds ``sa_interfaces``, as it finds any
other dependency. The package also needs ``<depend>sa_interfaces</depend>``
in its ``package.xml``.

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.8)
   project(sa_demo)

   set(CMAKE_CXX_STANDARD 20)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   set(CMAKE_CXX_EXTENSIONS OFF)

   if(NOT CMAKE_BUILD_TYPE)
     set(CMAKE_BUILD_TYPE Debug)
   endif()

   if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
     add_compile_options(-Wall -Wextra -pedantic-errors -Wshadow)
   endif()

   find_package(ament_cmake REQUIRED)
   find_package(rclcpp REQUIRED)
   find_package(rclcpp_action REQUIRED)
   find_package(sa_interfaces REQUIRED)

   include_directories(include)

   # The fare service, and the dispatcher that calls it.
   add_executable(fare_exe src/fare_main.cpp src/fare_node.cpp)
   ament_target_dependencies(fare_exe rclcpp sa_interfaces)
   add_executable(dispatcher_exe src/dispatcher_main.cpp src/dispatcher_node.cpp)
   ament_target_dependencies(dispatcher_exe rclcpp sa_interfaces)

   # The action server, and the client that sends a goal and cancels it on a timeout.
   add_executable(drive_exe src/drive_main.cpp src/drive_node.cpp)
   ament_target_dependencies(drive_exe rclcpp rclcpp_action sa_interfaces)
   add_executable(drive_client_exe src/drive_client_main.cpp src/drive_client_node.cpp)
   ament_target_dependencies(drive_client_exe rclcpp rclcpp_action sa_interfaces)

   install(TARGETS fare_exe dispatcher_exe drive_exe drive_client_exe
     DESTINATION lib/${PROJECT_NAME})

   ament_package()

``sa_demo/package.xml``:

.. code-block:: xml

   <?xml version="1.0"?>
   <package format="3">
     <name>sa_demo</name>
     <version>0.0.0</version>
     <description>A service and an action for a robotaxi.</description>
     <maintainer email="zeidk@umd.edu">zeidk</maintainer>
     <license>Apache-2.0</license>

     <buildtool_depend>ament_cmake</buildtool_depend>

     <depend>rclcpp</depend>
     <depend>rclcpp_action</depend>
     <depend>sa_interfaces</depend>

     <export>
       <build_type>ament_cmake</build_type>
     </export>
   </package>

Command-Line Tools
----------------------------------------------------

With ``fare_exe`` running, ``ros2 service list -t`` shows the service
and its type, and ``ros2 service call`` sends a request from a terminal.
The fare of 1000 m is 5.0 + 2.0 × 1.0 = 7.0 dollars.

.. code-block:: text

   $ ros2 service list -t
   /compute_fare [sa_interfaces/srv/ComputeFare]
   $ ros2 service type /compute_fare
   sa_interfaces/srv/ComputeFare
   $ ros2 service call /compute_fare sa_interfaces/srv/ComputeFare "{distance_m: 1000.0}"
   waiting for service to become available...
   requester: making request: sa_interfaces.srv.ComputeFare_Request(distance_m=1000.0)

   response:
   sa_interfaces.srv.ComputeFare_Response(fare=7.0)


Actions
====================================================

An action has a **server**, which runs the task, and a **client**, which
sends the goal. Here, ``drive_node`` is the server of ``drive``, and
``drive_client_node`` is its client. A goal ``target_x`` asks the
robotaxi to drive from x = 0 to ``target_x``.

The Server
----------------------------------------------------

``rclcpp_action::create_server<Type>`` takes three callbacks, and each
one answers one question:

- ``on_goal``: do you take this goal? It returns ``ACCEPT_AND_EXECUTE``
  or ``REJECT``. Here, the server rejects a ``target_x`` of 0 or less,
  and any goal while it is already driving.
- ``on_cancel``: do you accept this cancel request? It returns
  ``ACCEPT`` or ``REJECT``.
- ``on_accepted``: the goal is accepted, so run it.

The task takes seconds, so ``on_accepted`` starts it in a thread of its
own, ``execute``. A loop of seconds inside ``on_accepted`` would keep
the executor from calling any other callback, ``on_cancel`` included.

``execute`` does the work. Every 0.5 s, it checks ``is_canceling()``,
moves the robotaxi by its speed times 0.5 s, and sends the position with
``publish_feedback``. It ends with ``succeed`` or ``canceled``, and each
one carries the result.

``sa_demo/include/sa_demo/drive_node.hpp``:

.. code-block:: cpp

   #pragma once
   #include <atomic>
   #include <functional>
   #include <memory>
   #include <sa_interfaces/action/drive.hpp>
   #include <rclcpp/rclcpp.hpp>
   #include <rclcpp_action/rclcpp_action.hpp>

   namespace sa_demo {

   // Serves the action drive: the robotaxi drives from x = 0 to target_x at speed_mps,
   // with feedback every 0.5 s.
   class DriveNode : public rclcpp::Node {
     public:
       DriveNode()
           : rclcpp::Node{"drive_node"},
             server_{rclcpp_action::create_server<sa_interfaces::action::Drive>(
                 this, "drive",
                 std::bind(&DriveNode::on_goal, this, std::placeholders::_1, std::placeholders::_2),
                 std::bind(&DriveNode::on_cancel, this, std::placeholders::_1),
                 std::bind(&DriveNode::on_accepted, this, std::placeholders::_1))} {
           RCLCPP_INFO(get_logger(), "drive is ready");
       }

     private:
       using Drive = sa_interfaces::action::Drive;
       using GoalHandle = rclcpp_action::ServerGoalHandle<Drive>;

       rclcpp_action::GoalResponse on_goal(const rclcpp_action::GoalUUID &uuid,
                                           std::shared_ptr<const Drive::Goal> goal);
       rclcpp_action::CancelResponse on_cancel(const std::shared_ptr<GoalHandle> goal_handle);
       void on_accepted(const std::shared_ptr<GoalHandle> goal_handle);
       void execute(const std::shared_ptr<GoalHandle> goal_handle);

       static constexpr double speed_mps_{2.0}; // in m/s, chosen for this example
       std::atomic<bool> busy_{false};
       rclcpp_action::Server<Drive>::SharedPtr server_;
   };

   } // namespace sa_demo

``sa_demo/src/drive_node.cpp``:

.. code-block:: cpp

   #include "sa_demo/drive_node.hpp"

   #include <algorithm>
   #include <thread>

   namespace sa_demo {

   rclcpp_action::GoalResponse DriveNode::on_goal(const rclcpp_action::GoalUUID & /*uuid*/,
                                                  std::shared_ptr<const Drive::Goal> goal) {
       if (goal->target_x <= 0.0 || busy_) {
           RCLCPP_WARN_STREAM(get_logger(), "rejected the goal target_x = " << goal->target_x);
           return rclcpp_action::GoalResponse::REJECT;
       }
       RCLCPP_INFO_STREAM(get_logger(), "accepted the goal target_x = " << goal->target_x);
       return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
   }

   rclcpp_action::CancelResponse DriveNode::on_cancel(const std::shared_ptr<GoalHandle> /*goal_handle*/) {
       RCLCPP_INFO(get_logger(), "cancel request received");
       return rclcpp_action::CancelResponse::ACCEPT;
   }

   void DriveNode::on_accepted(const std::shared_ptr<GoalHandle> goal_handle) {
       busy_ = true;
       // execute loops for seconds, so it runs in its own thread. A loop in this callback
       // would keep the executor from running the cancel callback.
       std::thread{std::bind(&DriveNode::execute, this, std::placeholders::_1), goal_handle}
           .detach();
   }

   void DriveNode::execute(const std::shared_ptr<GoalHandle> goal_handle) {
       const double target_x{goal_handle->get_goal()->target_x};
       auto feedback{std::make_shared<Drive::Feedback>()};
       auto result{std::make_shared<Drive::Result>()};
       rclcpp::Rate rate{2.0}; // one loop every 0.5 s
       double x{0.0};
       while (x < target_x && rclcpp::ok()) {
           if (goal_handle->is_canceling()) {
               result->final_x = x;
               goal_handle->canceled(result);
               RCLCPP_INFO_STREAM(get_logger(), "canceled at x = " << x << " m");
               busy_ = false;
               return;
           }
           x = std::min(x + speed_mps_ * 0.5, target_x);
           feedback->current_x = x;
           goal_handle->publish_feedback(feedback);
           rate.sleep();
       }
       result->final_x = x;
       if (rclcpp::ok()) {
           goal_handle->succeed(result);
           RCLCPP_INFO_STREAM(get_logger(), "reached x = " << x << " m");
       }
       busy_ = false;
   }

   } // namespace sa_demo

The Client
----------------------------------------------------

``async_send_goal(goal, options)`` returns at once, like
``async_send_request``. The options hold three callbacks:

- ``goal_response_callback``: the server accepted the goal, or rejected
  it. A rejected goal gives an empty pointer.
- ``feedback_callback``: the server sent feedback.
- ``result_callback``: the goal ended. ``result.code`` says how:
  ``SUCCEEDED``, ``CANCELED`` or ``ABORTED``.

``drive_client_node`` also gives itself 3 s. A timer runs every 0.1 s,
and it compares ``now()``, the node clock, with the start time. When
``now()`` is more than ``timeout_s_`` after the start, the client calls
``async_cancel_goal``. The node clock is the
clock of the node's time source: the wall clock, or the simulation time
when the parameter ``use_sim_time`` is true. A timeout counted on the
node clock follows the simulation. The drive takes 5 s (10 m at 2 m/s),
so with a timeout of 3 s, the client cancels.

``sa_demo/include/sa_demo/drive_client_node.hpp``:

.. code-block:: cpp

   #pragma once
   #include <chrono>
   #include <functional>
   #include <memory>
   #include <sa_interfaces/action/drive.hpp>
   #include <rclcpp/rclcpp.hpp>
   #include <rclcpp_action/rclcpp_action.hpp>

   namespace sa_demo {

   // After 1 s, sends the goal target_x to the action drive. If the goal takes longer than
   // timeout_s on the node clock, it cancels the goal.
   class DriveClientNode : public rclcpp::Node {
     public:
       DriveClientNode()
           : rclcpp::Node{"drive_client_node"},
             client_{rclcpp_action::create_client<sa_interfaces::action::Drive>(this, "drive")},
             send_timer_{create_wall_timer(std::chrono::seconds{1},
                                           std::bind(&DriveClientNode::send_goal, this))} {}

     private:
       using Drive = sa_interfaces::action::Drive;
       using GoalHandle = rclcpp_action::ClientGoalHandle<Drive>;

       void send_goal();
       void on_goal_response(const GoalHandle::SharedPtr &goal_handle);
       void on_feedback(GoalHandle::SharedPtr goal_handle,
                        const std::shared_ptr<const Drive::Feedback> feedback);
       void on_result(const GoalHandle::WrappedResult &result);
       void check_timeout();

       static constexpr double target_x_{10.0}; // in m, chosen for this example
       static constexpr double timeout_s_{3.0}; // in s, chosen for this example
       rclcpp_action::Client<Drive>::SharedPtr client_;
       rclcpp::TimerBase::SharedPtr send_timer_;
       rclcpp::TimerBase::SharedPtr timeout_timer_;
       GoalHandle::SharedPtr goal_handle_;
       rclcpp::Time start_time_;
       bool cancel_sent_{false};
   };

   } // namespace sa_demo

``sa_demo/src/drive_client_node.cpp``:

.. code-block:: cpp

   #include "sa_demo/drive_client_node.hpp"

   namespace sa_demo {

   void DriveClientNode::send_goal() {
       send_timer_->cancel(); // send one goal, not one per second
       if (!client_->action_server_is_ready()) {
           RCLCPP_WARN(get_logger(), "the action drive is not available");
           rclcpp::shutdown();
           return;
       }
       Drive::Goal goal{};
       goal.target_x = target_x_;
       rclcpp_action::Client<Drive>::SendGoalOptions options{};
       options.goal_response_callback =
           std::bind(&DriveClientNode::on_goal_response, this, std::placeholders::_1);
       options.feedback_callback = std::bind(&DriveClientNode::on_feedback, this,
                                             std::placeholders::_1, std::placeholders::_2);
       options.result_callback = std::bind(&DriveClientNode::on_result, this, std::placeholders::_1);
       // async_send_goal returns at once. The three callbacks run later.
       client_->async_send_goal(goal, options);
       start_time_ = now(); // the node clock: simulation time when use_sim_time is true
       timeout_timer_ = create_wall_timer(std::chrono::milliseconds{100},
                                          std::bind(&DriveClientNode::check_timeout, this));
       RCLCPP_INFO_STREAM(get_logger(), "sent the goal target_x = " << target_x_);
   }

   void DriveClientNode::on_goal_response(const GoalHandle::SharedPtr &goal_handle) {
       if (!goal_handle) {
           RCLCPP_ERROR(get_logger(), "the server rejected the goal");
           timeout_timer_->cancel();
           if (rclcpp::ok()) {
               rclcpp::shutdown();
           }
           return;
       }
       goal_handle_ = goal_handle;
       RCLCPP_INFO(get_logger(), "the server accepted the goal");
   }

   void DriveClientNode::on_feedback(GoalHandle::SharedPtr /*goal_handle*/,
                                     const std::shared_ptr<const Drive::Feedback> feedback) {
       RCLCPP_INFO_STREAM(get_logger(), "feedback: x = " << feedback->current_x << " m");
   }

   void DriveClientNode::on_result(const GoalHandle::WrappedResult &result) {
       timeout_timer_->cancel();
       switch (result.code) {
       case rclcpp_action::ResultCode::SUCCEEDED:
           RCLCPP_INFO_STREAM(get_logger(), "succeeded, final x = " << result.result->final_x);
           break;
       case rclcpp_action::ResultCode::CANCELED:
           RCLCPP_WARN_STREAM(get_logger(), "canceled, final x = " << result.result->final_x);
           break;
       default:
           RCLCPP_ERROR(get_logger(), "aborted or unknown result");
           break;
       }
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

   void DriveClientNode::check_timeout() {
       if (!goal_handle_ || cancel_sent_) {
           return;
       }
       if ((now() - start_time_).seconds() > timeout_s_) {
           RCLCPP_WARN_STREAM(get_logger(), "no result after " << timeout_s_ << " s: canceling");
           client_->async_cancel_goal(goal_handle_);
           cancel_sent_ = true;
       }
   }

   } // namespace sa_demo

Run ``ros2 run sa_demo drive_exe`` in one terminal, and
``ros2 run sa_demo drive_client_exe`` in another. The client prints the
feedback, then cancels at 3 s:

.. code-block:: text

   [INFO] [...] [drive_client_node]: sent the goal target_x = 10
   [INFO] [...] [drive_client_node]: the server accepted the goal
   [INFO] [...] [drive_client_node]: feedback: x = 1 m
   [INFO] [...] [drive_client_node]: feedback: x = 2 m
   [INFO] [...] [drive_client_node]: feedback: x = 3 m
   [INFO] [...] [drive_client_node]: feedback: x = 4 m
   [INFO] [...] [drive_client_node]: feedback: x = 5 m
   [INFO] [...] [drive_client_node]: feedback: x = 6 m
   [WARN] [...] [drive_client_node]: no result after 3 s: canceling
   [WARN] [...] [drive_client_node]: canceled, final x = 6

The server prints, for the same run:

.. code-block:: text

   [INFO] [...] [drive_node]: drive is ready
   [INFO] [...] [drive_node]: accepted the goal target_x = 10
   [INFO] [...] [drive_node]: cancel request received
   [INFO] [...] [drive_node]: canceled at x = 6 m

The robotaxi stopped at x = 6 m: 3 s at 2 m/s.

Command-Line Tools
----------------------------------------------------

``ros2 action send_goal`` is the command-line client. ``--feedback``
prints each feedback message. A goal with a ``target_x`` of 4 m ends
with ``SUCCEEDED``, and a goal with a negative ``target_x`` is rejected
by ``on_goal``:

.. code-block:: text

   $ ros2 action list -t
   /drive [sa_interfaces/action/Drive]
   $ ros2 action info /drive
   Action: /drive
   Action clients: 0
   Action servers: 1
       /drive_node
   $ ros2 action send_goal /drive sa_interfaces/action/Drive "{target_x: 4.0}" --feedback
   Waiting for an action server to become available...
   Sending goal:
        target_x: 4.0

   Feedback:
       current_x: 1.0

   Goal accepted with ID: 1f19c7e7989d437ab557ca89e4844a30

   Feedback:
       current_x: 2.0

   Feedback:
       current_x: 3.0

   Feedback:
       current_x: 4.0

   Result:
       final_x: 4.0

   Goal finished with status: SUCCEEDED
   $ ros2 action send_goal /drive sa_interfaces/action/Drive "{target_x: -5.0}"
   Waiting for an action server to become available...
   Sending goal:
        target_x: -5.0

   Goal was rejected.

An action is not a third kind of connection. It is built from the other
two. Hidden from the default lists, ``drive`` has three services (send
the goal, cancel it, get the result) and two topics (feedback and
status). ``ros2 service list --include-hidden-services`` and
``ros2 topic list --include-hidden-topics`` show them:

.. code-block:: text

   /drive/_action/cancel_goal [action_msgs/srv/CancelGoal]
   /drive/_action/get_result [sa_interfaces/action/Drive_GetResult]
   /drive/_action/send_goal [sa_interfaces/action/Drive_SendGoal]
   /drive/_action/feedback [sa_interfaces/action/Drive_FeedbackMessage]
   /drive/_action/status [action_msgs/msg/GoalStatusArray]
   ---


Choosing Between Them
====================================================

.. list-table::
   :header-rows: 1
   :widths: 40 20 40
   :class: compact-table

   * - The job
     - Use
     - Why
   * - Stream a sensor reading or a velocity command
     - Topic
     - Data keeps coming, and nobody replies.
   * - Ask for a fare, or set a flag
     - Service
     - One request, one quick response.
   * - Drive to a point, and report progress
     - Action
     - It takes seconds and needs feedback.
   * - A task the operator may stop
     - Action
     - Only an action has a cancel request.

.. warning::

   A service callback that works for seconds keeps the executor busy,
   and the client waits for its response all that time. Put work that
   takes seconds in an action.


Summary
====================================================

- A **service** answers one request with one response. Define it in a
  ``.srv`` file, serve it with ``create_service``, and call it with
  ``create_client`` and ``async_send_request``.
- An **action** runs a task that takes time. Define it in an
  ``.action`` file with a goal, a result and feedback. The server has
  three callbacks (goal, cancel, accepted) and runs the task in
  ``execute``. The client sends the goal with ``async_send_goal`` and
  receives three callbacks.
- A cancel and a timeout belong to the client. Count the timeout on
  the node clock.
- Both are in interface packages, built with ``rosidl_generate_interfaces``
  and checked with ``ros2 interface show``.
