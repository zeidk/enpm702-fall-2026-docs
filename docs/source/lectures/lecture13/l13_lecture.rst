====================================================
Lecture
====================================================


Coordinate Frames and Transforms
====================================================

This lecture covers coordinate frames and the **TF2** library, the
ROS 2 framework for tracking and transforming between the many reference
frames on a robot (its base, its sensors, and the world it operates in).
It covers:

- Coordinate frames and the frame tree
- The ``TransformStamped`` message
- Static and dynamic transform broadcasting
- Listening for and looking up transforms
- TF2 debugging tools

Lifecycle (managed) nodes are covered in the next lecture
(:doc:`Lecture 14 <../lecture14/l14_index>`).


----


Coordinate Frames
====================================================

In robotics, a **coordinate frame** (or reference frame) is a set of axes
that defines a position and orientation in space. Every physical component
of a robot, its base, each joint, every sensor, and the end effector,
has its own coordinate frame. Coordinate frames are also used to represent
the world or map that the robot operates in.

Why do we need multiple frames? Consider a mobile robot with a camera and
a lidar sensor:

- The **world frame** is fixed in the environment.
- The **base_link frame** is attached to the robot's body.
- The **camera_link frame** is at the camera's optical center.
- The **lidar_link frame** is at the lidar sensor's origin.

When the camera detects an object, the detection is relative to the
camera frame. To act on that detection, we need to transform it into
the robot's base frame or the world frame. This is where **TF2** comes
in.

.. figure:: /_static/images/l13/frame_tree.png
   :align: center

   A coordinate frame tree showing relationships between world,
   base_link, camera_link, and lidar_link frames.


The Frame Tree
----------------------------------------------------

In ROS 2, coordinate frames are organized in a **tree structure**. Each
frame has exactly one parent (except the root), and the relationship
between a parent and child frame is described by a **transform**
(translation + rotation). This tree structure ensures there is exactly
one path between any two frames, making transform lookups unambiguous.

Common conventions:

- ``map`` or ``world``, a fixed global frame.
- ``odom``, the odometry frame (may drift over time).
- ``base_link``, attached to the robot's body.
- ``base_footprint``, projection of ``base_link`` onto the ground plane.
- Sensor frames (``camera_link``, ``lidar_link``, etc.) are children of ``base_link``.


----


TF2 Basics
====================================================

**TF2** is the ROS 2 library for tracking coordinate frames over time.
It lets any node in the system know the transform between any two
frames at any point in time.

The core components are:

- **Broadcasters**, publish transforms to the ``/tf`` or ``/tf_static`` topics.
- **Listeners**, subscribe to transforms and buffer them for lookup.
- **Buffer**, stores transforms over a configurable time window.


TransformStamped Message
----------------------------------------------------

The fundamental message type is ``geometry_msgs::msg::TransformStamped``:

.. code-block:: cpp

   // geometry_msgs/msg/TransformStamped
   // header.stamp        -- timestamp of the transform
   // header.frame_id     -- parent frame (e.g., "world")
   // child_frame_id      -- child frame (e.g., "base_link")
   // transform.translation.x, .y, .z   -- position offset
   // transform.rotation.x, .y, .z, .w  -- orientation as quaternion

Key fields:

- ``header.frame_id``, the **parent** frame.
- ``child_frame_id``, the **child** frame.
- ``transform.translation``, the position of the child frame's origin in the parent frame.
- ``transform.rotation``, the orientation of the child frame relative to the parent frame, expressed as a quaternion.


Static vs. Dynamic Transforms
----------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Property
     - Static Transform
     - Dynamic Transform
   * - Published to
     - ``/tf_static``
     - ``/tf``
   * - Publish frequency
     - Once (latched)
     - Continuously (e.g., in a timer)
   * - Use case
     - Fixed relationships (sensor to base)
     - Changing relationships (robot in world)
   * - Example
     - camera_link relative to base_link
     - base_link relative to world

**Rule of thumb**: If the relationship between two frames never changes
(e.g., a sensor bolted to the robot), use a static transform. If the
relationship changes over time (e.g., a robot moving in the world), use
a dynamic transform.


----


Static Transform Broadcaster
====================================================

A static transform broadcaster publishes a transform that does not change
over time. This is used for fixed spatial relationships such as the
position of a sensor relative to the robot base.

Using ``tf2_ros::StaticTransformBroadcaster``
----------------------------------------------------

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <tf2_ros/static_transform_broadcaster.h>
   #include <geometry_msgs/msg/transform_stamped.hpp>

   class StaticFramePublisher : public rclcpp::Node {
    public:
     StaticFramePublisher()
         : Node{"static_frame_publisher"} {
       // Create the static transform broadcaster
       static_broadcaster_ =
           std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

       // Build the transform message
       geometry_msgs::msg::TransformStamped t;
       t.header.stamp = this->get_clock()->now();
       t.header.frame_id = "base_link";
       t.child_frame_id = "camera_link";

       // Camera is 0.1 m forward and 0.3 m above the base
       t.transform.translation.x = 0.1;
       t.transform.translation.y = 0.0;
       t.transform.translation.z = 0.3;

       // No rotation (identity quaternion)
       t.transform.rotation.x = 0.0;
       t.transform.rotation.y = 0.0;
       t.transform.rotation.z = 0.0;
       t.transform.rotation.w = 1.0;

       // Publish (latched -- only needs to be called once)
       static_broadcaster_->sendTransform(t);

       RCLCPP_INFO(this->get_logger(), "Static transform published: "
                   "base_link -> camera_link");
     }

    private:
     std::shared_ptr<tf2_ros::StaticTransformBroadcaster> static_broadcaster_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<StaticFramePublisher>());
     rclcpp::shutdown();
     return 0;
   }


Using the CLI
----------------------------------------------------

You can also publish static transforms directly from the command line:

.. code-block:: bash

   # ros2 run tf2_ros static_transform_publisher --x --y --z --yaw --pitch --roll --frame-id --child-frame-id
   ros2 run tf2_ros static_transform_publisher \
     --x 0.1 --y 0.0 --z 0.3 \
     --yaw 0.0 --pitch 0.0 --roll 0.0 \
     --frame-id base_link --child-frame-id camera_link

This is useful for testing or for transforms that are purely
configuration and do not require a custom node.


----


Dynamic Transform Broadcaster
====================================================

A dynamic transform broadcaster publishes transforms that change over
time. This is used for moving relationships such as a robot's position
in the world frame.

Using ``tf2_ros::TransformBroadcaster``
----------------------------------------------------

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <tf2_ros/transform_broadcaster.h>
   #include <geometry_msgs/msg/transform_stamped.hpp>
   #include <cmath>

   class DynamicFramePublisher : public rclcpp::Node {
    public:
     DynamicFramePublisher()
         : Node{"dynamic_frame_publisher"}, time_{0.0} {
       // Create the dynamic transform broadcaster
       tf_broadcaster_ =
           std::make_unique<tf2_ros::TransformBroadcaster>(this);

       // Publish the transform at 10 Hz
       timer_ = this->create_wall_timer(
           std::chrono::milliseconds{100},
           std::bind(&DynamicFramePublisher::broadcast_transform, this));
     }

    private:
     void broadcast_transform() {
       geometry_msgs::msg::TransformStamped t;
       t.header.stamp = this->get_clock()->now();
       t.header.frame_id = "world";
       t.child_frame_id = "base_link";

       // Simulate a robot moving along the x-axis
       t.transform.translation.x = time_ * 0.5;  // 0.5 m/s
       t.transform.translation.y = 0.0;
       t.transform.translation.z = 0.0;

       // No rotation
       t.transform.rotation.x = 0.0;
       t.transform.rotation.y = 0.0;
       t.transform.rotation.z = 0.0;
       t.transform.rotation.w = 1.0;

       tf_broadcaster_->sendTransform(t);

       time_ += 0.1;
     }

     std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
     rclcpp::TimerBase::SharedPtr timer_;
     double time_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<DynamicFramePublisher>());
     rclcpp::shutdown();
     return 0;
   }

.. note::

   Dynamic transforms must be published continuously. If you stop
   publishing, consumers will eventually consider the transform stale
   and ``lookupTransform()`` will fail.


----


Transform Listener
====================================================

A transform listener subscribes to ``/tf`` and ``/tf_static``, buffers
the transforms, and allows you to look up the transform between any two
frames at any time.


Using ``tf2_ros::Buffer`` and ``tf2_ros::TransformListener``
--------------------------------------------------------------

.. code-block:: cpp

   #include <rclcpp/rclcpp.hpp>
   #include <tf2_ros/buffer.h>
   #include <tf2_ros/transform_listener.h>
   #include <geometry_msgs/msg/transform_stamped.hpp>
   #include <tf2/exceptions.h>

   class FrameListener : public rclcpp::Node {
    public:
     FrameListener()
         : Node{"frame_listener"} {
       // Create a tf2 buffer and listener
       tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
       tf_listener_ =
           std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

       // Timer to periodically look up transforms
       timer_ = this->create_wall_timer(
           std::chrono::seconds{1},
           std::bind(&FrameListener::lookup_transform, this));
     }

    private:
     void lookup_transform() {
       try {
         // Look up the transform from world to base_link
         geometry_msgs::msg::TransformStamped t =
             tf_buffer_->lookupTransform(
                 "world",      // target frame
                 "base_link",  // source frame
                 tf2::TimePointZero);  // latest available

         RCLCPP_INFO(this->get_logger(),
                     "Transform world -> base_link: "
                     "x=%.2f, y=%.2f, z=%.2f",
                     t.transform.translation.x,
                     t.transform.translation.y,
                     t.transform.translation.z);

       } catch (const tf2::TransformException& ex) {
         RCLCPP_WARN(this->get_logger(),
                     "Could not get transform: %s", ex.what());
       }
     }

     std::unique_ptr<tf2_ros::Buffer> tf_buffer_;
     std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
     rclcpp::TimerBase::SharedPtr timer_;
   };

   int main(int argc, char* argv[]) {
     rclcpp::init(argc, argv);
     rclcpp::spin(std::make_shared<FrameListener>());
     rclcpp::shutdown();
     return 0;
   }


``lookupTransform()`` Parameters
----------------------------------------------------

.. code-block:: cpp

   tf_buffer_->lookupTransform(
       target_frame,   // frame to express the result in
       source_frame,   // frame we want the pose of
       time);          // timestamp (tf2::TimePointZero = latest)

- **target_frame**: The frame you want to express the result in.
- **source_frame**: The frame whose pose you want.
- **time**: The time at which you want the transform. Use
  ``tf2::TimePointZero`` for the latest available transform.


Error Handling
----------------------------------------------------

Always wrap ``lookupTransform()`` in a try-catch block. Common exceptions:

- ``tf2::LookupException``, the frame does not exist in the tree.
- ``tf2::ConnectivityException``, there is no path between the frames.
- ``tf2::ExtrapolationException``, the requested time is outside the buffer window.
- ``tf2::TransformException``, base class for all TF2 exceptions.


----


TF2 Tools
====================================================

ROS 2 provides several tools for inspecting and debugging the TF2 frame
tree.


``view_frames``
----------------------------------------------------

Generates a PDF of the full frame tree:

.. code-block:: bash

   ros2 run tf2_tools view_frames

This saves a ``frames.pdf`` file in the current directory showing all
frames and their relationships.


``tf2_echo``
----------------------------------------------------

Prints the transform between two frames in real time:

.. code-block:: bash

   ros2 run tf2_ros tf2_echo world base_link

Output updates continuously and shows translation and rotation values.


RViz2 TF Display
----------------------------------------------------

In **RViz2**, add a **TF** display to visualize all coordinate frames
in 3D. This shows frame axes, names, and connections. It is the most
intuitive way to verify that your transforms are correct.
