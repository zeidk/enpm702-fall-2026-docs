====================================================
Lecture
====================================================


.. note::

   **Draft.** This page states what Lecture 12 covers and holds its
   Parameters part in full. The other parts will be written from the
   slides. Every C++ example in the Parameters part was built with the
   course flags (``-std=c++20 -Wall -Wextra -pedantic-errors -Wshadow``)
   without a warning, on ROS 2 Jazzy, and every output is pasted from a
   run.


What This Lecture Covers
====================================================

Lecture 12 puts a real robot under your code, then makes the code easy
to tune. It has three parts:

1. **The ROSbot in Gazebo.** The Husarion ROSbot is the robot of
   Lecture 12 to Lecture 14 and of Group Project 2. :doc:`ROSbot
   Simulation </setup/rosbot_simulation>` shows how to install, build and
   start it. The topics of the ROSbot and the messages on them are in
   :doc:`Mobile Robot Messages
   </reading_material/robot_messages/rmsg_index>`: read it before this
   lecture.
2. **Proportional control.** A **proportional controller** sets a
   command in proportion to an error. For example, the angular velocity
   of a robot is a gain times the angle between the direction the robot
   faces and the direction it should face. The gain is a number that you
   tune.
3. **Parameters.** A **parameter** is a value of a node that you set
   when the node starts, or change while it runs, without a rebuild. The
   gain of a controller and the speed limit of a robot are parameters.
   This part is below.

Services and actions are not in this lecture. :doc:`Services and
Actions </reading_material/services_actions/sa_index>` is a reading
module with extra material.


Parameters
====================================================

A node has values that you want to change without editing the code and
building again: a speed, a name, the gain of a controller. A ROS 2
**parameter** is such a value. It belongs to one node, it has a name and
a type, and the node declares it. You can set it from the command line,
from a file, from a launch file, or while the node runs.

The example is the robotaxi of Lecture 10. Its node publishes its
position every 0.5 s, and now its name, its speed and its start position
are parameters.

Declare and Read a Parameter
----------------------------------------------------

A node must **declare** a parameter before anyone can use it. The call
``declare_parameter<Type>(name, default)`` declares it with a default
value, and returns the value that the parameter holds. If nobody sets
the parameter, that value is the default.

The type of a parameter is one of ``bool``, ``int64``, ``double``,
``string``, ``byte`` array, or an array of one of the others. The first
declaration fixes the type. The robotaxi has a ``string``, ``robotaxi_name``,
and two ``double`` parameters, ``speed_mps`` (in m/s) and ``start_x_m``
(in m).

``l12_robotaxi/include/l12_robotaxi/robotaxi_node.hpp``:

.. code-block:: cpp

   #pragma once
   #include <chrono>
   #include <functional>
   #include <geometry_msgs/msg/point.hpp>
   #include <memory>
   #include <rcl_interfaces/msg/set_parameters_result.hpp>
   #include <rclcpp/rclcpp.hpp>
   #include <string>
   #include <vector>

   namespace l12_robotaxi {

   // Publishes the robotaxi's position every 0.5 s. Its name, speed and start position
   // are parameters.
   class RobotaxiNode : public rclcpp::Node {
     public:
       RobotaxiNode()
           : rclcpp::Node{"robotaxi_node"},
             // declare_parameter declares the parameter and returns its value.
             robotaxi_name_{declare_parameter<std::string>("robotaxi_name", "robotaxi_1")},
             speed_mps_{declare_parameter<double>("speed_mps", 2.0)},
             x_{declare_parameter<double>("start_x_m", 0.0)},
             publisher_{create_publisher<geometry_msgs::msg::Point>("robotaxi/position", 10)},
             timer_{create_wall_timer(std::chrono::milliseconds{500},
                                      std::bind(&RobotaxiNode::publish_position, this))},
             parameter_callback_{add_on_set_parameters_callback(
                 std::bind(&RobotaxiNode::on_parameters, this, std::placeholders::_1))} {
           RCLCPP_INFO_STREAM(get_logger(), robotaxi_name_ << " starts at x = " << x_
                                                           << " m, speed " << speed_mps_ << " m/s");
       }

     private:
       void publish_position();
       rcl_interfaces::msg::SetParametersResult
       on_parameters(const std::vector<rclcpp::Parameter> &parameters);

       std::string robotaxi_name_;
       double speed_mps_; // in m/s
       double x_;         // position along the street, in m
       rclcpp::Publisher<geometry_msgs::msg::Point>::SharedPtr publisher_;
       rclcpp::TimerBase::SharedPtr timer_;
       rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr parameter_callback_;
   };

   } // namespace l12_robotaxi

The first three members take their values from the three parameters.
``x_`` holds the start position first, and then the current position.
The members are initialized in the order in which they are declared.

``l12_robotaxi/src/robotaxi_node.cpp``:

.. code-block:: cpp

   #include "l12_robotaxi/robotaxi_node.hpp"

   namespace l12_robotaxi {

   void RobotaxiNode::publish_position() {
       x_ += speed_mps_ * 0.5; // the timer period is 0.5 s
       geometry_msgs::msg::Point msg{};
       msg.x = x_;
       publisher_->publish(msg);
       RCLCPP_INFO_STREAM(get_logger(), "x = " << x_ << " m");
   }

   rcl_interfaces::msg::SetParametersResult
   RobotaxiNode::on_parameters(const std::vector<rclcpp::Parameter> &parameters) {
       rcl_interfaces::msg::SetParametersResult result{};
       result.successful = true;
       for (const rclcpp::Parameter &parameter : parameters) {
           if (parameter.get_name() != "speed_mps") {
               continue;
           }
           if (parameter.as_double() < 0.0) {
               result.successful = false;
               result.reason = "speed_mps must not be negative";
               return result;
           }
           speed_mps_ = parameter.as_double();
           RCLCPP_INFO_STREAM(get_logger(), "speed_mps is now " << speed_mps_ << " m/s");
       }
       return result;
   }

   } // namespace l12_robotaxi

``l12_robotaxi/src/robotaxi_main.cpp`` is the ``main`` of
Lecture 10, with ``l12_robotaxi::RobotaxiNode`` as the node:

.. code-block:: cpp

   #include <memory>

   #include <rclcpp/rclcpp.hpp>

   #include "l12_robotaxi/robotaxi_node.hpp"

   int main(int argc, char **argv) {
       rclcpp::init(argc, argv);
       auto node{std::make_shared<l12_robotaxi::RobotaxiNode>()};
       rclcpp::spin(node);
       if (rclcpp::ok()) {
           rclcpp::shutdown();
       }
   }

Run it with no setting. The node uses the defaults:

.. code-block:: bash

   ros2 run l12_robotaxi robotaxi_exe

.. code-block:: text

   [INFO] [...] [robotaxi_node]: robotaxi_1 starts at x = 0 m, speed 2 m/s
   [INFO] [...] [robotaxi_node]: x = 1 m
   [INFO] [...] [robotaxi_node]: x = 2 m
   [INFO] [...] [robotaxi_node]: x = 3 m
   [INFO] [...] [robotaxi_node]: x = 4 m

The speed is 2 m/s, so the position grows by 1 m every 0.5 s.


Set a Parameter When the Node Starts
----------------------------------------------------

There are three ways. They all set the same parameter, so they differ
only in where the value is written.

**On the command line.** ``--ros-args`` starts the ROS arguments, and
``-p name:=value`` sets one parameter:

.. code-block:: bash

   ros2 run l12_robotaxi robotaxi_exe --ros-args -p speed_mps:=3.0 -p robotaxi_name:=taxi_7

.. code-block:: text

   [INFO] [...] [robotaxi_node]: taxi_7 starts at x = 0 m, speed 3 m/s
   [INFO] [...] [robotaxi_node]: x = 1.5 m
   [INFO] [...] [robotaxi_node]: x = 3 m
   [INFO] [...] [robotaxi_node]: x = 4.5 m

**In a YAML file.** A parameter file is a YAML file. It starts with the
name of a node, then ``ros__parameters``, then one line per parameter.
``--params-file`` loads it.

``l12_robotaxi/config/robotaxi_params.yaml``:

.. code-block:: yaml

   robotaxi_node:
     ros__parameters:
       robotaxi_name: "robotaxi_1"
       speed_mps: 2.0
       start_x_m: 0.0

.. code-block:: bash

   ros2 run l12_robotaxi robotaxi_exe --ros-args --params-file <path to the file>

The name at the top of the file must be the name of the node. If you
start the same executable with another node name, the node ignores the
section and uses its defaults. With ``-r __node:=taxi_b`` and the file
above, the node ``taxi_b`` logs a speed of 2 m/s, which is the default,
and not a different value:

.. code-block:: text

   [INFO] [...] [taxi_b]: robotaxi_1 starts at x = 0 m, speed 2 m/s
   [INFO] [...] [taxi_b]: x = 1 m

To give the same value to every node, write ``/**`` instead of a node
name. A node reads the parameters it declares and ignores the others.
This file sets ``speed_mps`` for any node:

``l12_robotaxi/config/fleet_params.yaml``:

.. code-block:: yaml

   /**:
     ros__parameters:
       speed_mps: 1.5

Started with this file, and with the new name ``taxi_b``, the node uses
a speed of 1.5 m/s:

.. code-block:: text

   [INFO] [...] [taxi_b]: robotaxi_1 starts at x = 0 m, speed 1.5 m/s
   [INFO] [...] [taxi_b]: x = 0.75 m

**In a launch file.** A launch file loads the YAML file for you, so you
do not type the path. The launch argument ``params_file`` names the file,
and its default is the file in the package. ``ros2 launch ...
params_file:=<path>`` loads another file.

``l12_robotaxi/launch/robotaxi_launch.py``:

.. code-block:: python

   import os

   from ament_index_python.packages import get_package_share_directory
   from launch import LaunchDescription
   from launch.actions import DeclareLaunchArgument
   from launch.substitutions import LaunchConfiguration
   from launch_ros.actions import Node


   def generate_launch_description():
       default_file = os.path.join(
           get_package_share_directory("l12_robotaxi"), "config", "robotaxi_params.yaml"
       )
       return LaunchDescription(
           [
               # ros2 launch l12_robotaxi robotaxi_launch.py params_file:=<path>
               DeclareLaunchArgument("params_file", default_value=default_file),
               Node(
                   package="l12_robotaxi",
                   executable="robotaxi_exe",
                   parameters=[LaunchConfiguration("params_file")],
                   output="screen",
               ),
           ]
       )

The package must install the folders ``config`` and ``launch``, or the
launch file does not find the YAML file. The line
``install(DIRECTORY config launch ...)`` of ``CMakeLists.txt`` does it:

``l12_robotaxi/CMakeLists.txt``:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.8)
   project(l12_robotaxi)

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
   find_package(geometry_msgs REQUIRED)

   include_directories(include)

   add_executable(robotaxi_exe src/robotaxi_main.cpp src/robotaxi_node.cpp)
   ament_target_dependencies(robotaxi_exe rclcpp geometry_msgs)

   install(TARGETS robotaxi_exe DESTINATION lib/${PROJECT_NAME})

   # Copies config/ and launch/ to install/l12_robotaxi/share/l12_robotaxi, where the launch
   # file looks for the YAML file.
   install(DIRECTORY config launch DESTINATION share/${PROJECT_NAME})

   ament_package()

``l12_robotaxi/package.xml``:

.. code-block:: xml

   <?xml version="1.0"?>
   <package format="3">
     <name>l12_robotaxi</name>
     <version>0.0.0</version>
     <description>A robotaxi node with parameters, loaded from a YAML file by a launch file.</description>
     <maintainer email="zeidk@umd.edu">zeidk</maintainer>
     <license>Apache-2.0</license>

     <buildtool_depend>ament_cmake</buildtool_depend>

     <depend>rclcpp</depend>
     <depend>geometry_msgs</depend>

     <exec_depend>ros2launch</exec_depend>
     <exec_depend>ament_index_python</exec_depend>

     <export>
       <build_type>ament_cmake</build_type>
     </export>
   </package>

Run the launch file with the default file, then with ``fast.yaml``, a
file that sets ``speed_mps`` to 5.0:

``fast.yaml``:

.. code-block:: yaml

   robotaxi_node:
     ros__parameters:
       speed_mps: 5.0

.. code-block:: bash

   ros2 launch l12_robotaxi robotaxi_launch.py
   ros2 launch l12_robotaxi robotaxi_launch.py params_file:=$PWD/fast.yaml

.. code-block:: text

   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: robotaxi_1 starts at x = 0 m, speed 2 m/s
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: x = 1 m

.. code-block:: text

   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: robotaxi_1 starts at x = 0 m, speed 5 m/s
   [robotaxi_exe-1] [INFO] [...] [robotaxi_node]: x = 2.5 m

With the speed of 5 m/s, the position grows by 2.5 m every 0.5 s.


Change a Parameter While the Node Runs
----------------------------------------------------

The ``ros2 param`` command works on a running node:

.. list-table::
   :header-rows: 1
   :widths: 20 80
   :class: compact-table

   * - Command
     - What it does
   * - ``ros2 param list``
     - Lists the parameters of a node, or of every node.
   * - ``ros2 param get``
     - Prints the value of one parameter.
   * - ``ros2 param describe``
     - Prints the type of a parameter, and its description and limits
       if the node gave them.
   * - ``ros2 param set``
     - Sets a parameter of a running node.
   * - ``ros2 param dump``
     - Prints the parameters of a node in the YAML format.
   * - ``ros2 param load``
     - Loads a YAML file into a running node.
   * - ``ros2 param delete``
     - Deletes a parameter.

With ``robotaxi_exe`` running:

.. code-block:: text

   $ ros2 param list /robotaxi_node
     qos_overrides./parameter_events.publisher.depth
     qos_overrides./parameter_events.publisher.durability
     qos_overrides./parameter_events.publisher.history
     qos_overrides./parameter_events.publisher.reliability
     robotaxi_name
     speed_mps
     start_type_description_service
     start_x_m
     use_sim_time
   $ ros2 param get /robotaxi_node speed_mps
   Double value is: 2.0
   $ ros2 param describe /robotaxi_node speed_mps
   Parameter name: speed_mps
     Type: double
     Constraints:
   $ ros2 param set /robotaxi_node speed_mps 4.0
   Set parameter successful
   $ ros2 param set /robotaxi_node speed_mps -1.0
   Setting parameter failed: speed_mps must not be negative
   $ ros2 param set /robotaxi_node speed_mps 3
   Setting parameter failed: Wrong parameter type, parameter {speed_mps} is of type {double}, setting it to {integer} is not allowed.
   $ ros2 param set /robotaxi_node colour red
   Setting parameter failed: parameter 'colour' cannot be set because it was not declared
   $ ros2 param get /robotaxi_node speed_mps
   Double value is: 4.0
   $ ros2 param dump /robotaxi_node
   /robotaxi_node:
     ros__parameters:
       qos_overrides:
         /parameter_events:
           publisher:
             depth: 1000
             durability: volatile
             history: keep_last
             reliability: reliable
       robotaxi_name: robotaxi_1
       speed_mps: 4.0
       start_type_description_service: true
       start_x_m: 0.0
       use_sim_time: false

The list holds the three parameters of the robotaxi, and the parameters
that every node has, such as ``use_sim_time``. Three sets failed, and each
failure has a reason:

- ``-1.0`` failed because of the node's own check, below.
- ``3`` failed because ``3`` is an integer, and ``speed_mps`` is a
  ``double``. Write ``3.0``.
- ``colour`` failed because the node never declared it. A node accepts
  only the parameters that it declares.

The Parameter Callback
----------------------------------------------------

``ros2 param set`` changes the stored value of the parameter. The
variable ``speed_mps_`` of the node is a copy, and it does not change by
itself. To react to a change, the node registers a **parameter
callback** with ``add_on_set_parameters_callback``. In
``robotaxi_node.hpp``, this is the member ``parameter_callback_``, and
its callback is ``on_parameters`` in ``robotaxi_node.cpp``.

ROS calls the callback **before** it stores a new value, with the
parameters that someone wants to set. The callback returns a result:

- ``successful = true``: ROS stores the value.
- ``successful = false``: ROS does not store it, and ``ros2 param set``
  prints the ``reason`` of the callback.

``on_parameters`` copies a valid ``speed_mps`` into ``speed_mps_`` and
rejects a negative one. In a run, ``ros2 param set /robotaxi_node
speed_mps 4.0`` took effect on the next timer call:

.. code-block:: text

   [INFO] [...] [robotaxi_node]: x = 12 m
   [INFO] [...] [robotaxi_node]: x = 13 m
   [INFO] [...] [robotaxi_node]: speed_mps is now 4 m/s
   [INFO] [...] [robotaxi_node]: x = 15 m
   [INFO] [...] [robotaxi_node]: x = 17 m
   [INFO] [...] [robotaxi_node]: x = 19 m
   [INFO] [...] [robotaxi_node]: x = 21 m

The position grew by 1 m per 0.5 s (2 m/s) until 13 m, and by 2 m per
0.5 s (4 m/s) after the callback printed the new speed.

.. note::

   The node registers the callback after it declares the parameters, so
   the callback sees only later changes. A value set before the node
   starts, with ``-p``, a file or a launch file, is the value that
   ``declare_parameter`` returns. In the runs above, no start-up value
   made the node print ``speed_mps is now``.

Summary
----------------------------------------------------

- A **parameter** is a named, typed value of a node. The node declares
  it with ``declare_parameter<Type>(name, default)``, which returns its
  value.
- Set it at start with ``-p name:=value``, with a YAML file
  (``--params-file``), or with a launch file that loads the file.
- A YAML file names the node, then ``ros__parameters``. ``/**`` gives a
  parameter to every node that declares it.
- ``ros2 param set`` changes a running node. A **parameter callback**
  checks the new value and copies it into the node's variable.
