====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 13: Coordinate
Frames and Transforms (TF2). Work through them in order, as each exercise
builds on the previous one. Build and run each program in a ROS 2
workspace to verify your understanding.

.. note::

   All exercises require a ROS 2 Jazzy workspace. Build with:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select my_package
      source install/setup.bash


----


.. dropdown:: Exercise 1: Static Transform Broadcaster
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Broadcast a static transform from ``base_link`` to ``camera_link``.

    **Specification**

    1. Create a ROS 2 node called ``static_camera_broadcaster``.
    2. Use ``tf2_ros::StaticTransformBroadcaster`` to publish a static
       transform from ``base_link`` to ``camera_link``.
    3. The camera is positioned 0.2 m forward (x), 0.0 m to the side (y),
       and 0.5 m above (z) the base_link.
    4. The camera has no rotation relative to base_link (identity
       quaternion).
    5. Log a message confirming the transform was published.
    6. Verify with: ``ros2 run tf2_ros tf2_echo base_link camera_link``

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <tf2_ros/static_transform_broadcaster.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>

           class StaticCameraBroadcaster : public rclcpp::Node {
            public:
             StaticCameraBroadcaster()
                 : Node{"static_camera_broadcaster"} {
               static_broadcaster_ =
                   std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

               geometry_msgs::msg::TransformStamped t;
               t.header.stamp = this->get_clock()->now();
               t.header.frame_id = "base_link";
               t.child_frame_id = "camera_link";

               t.transform.translation.x = 0.2;
               t.transform.translation.y = 0.0;
               t.transform.translation.z = 0.5;

               t.transform.rotation.x = 0.0;
               t.transform.rotation.y = 0.0;
               t.transform.rotation.z = 0.0;
               t.transform.rotation.w = 1.0;

               static_broadcaster_->sendTransform(t);
               RCLCPP_INFO(this->get_logger(),
                           "Published static transform: base_link -> camera_link");
             }

            private:
             std::shared_ptr<tf2_ros::StaticTransformBroadcaster> static_broadcaster_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<StaticCameraBroadcaster>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 2: Dynamic Transform Broadcaster (Circular Path)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Broadcast a dynamic transform that moves a robot in a circular path
    in the world frame.

    **Specification**

    1. Create a ROS 2 node called ``circular_motion_broadcaster``.
    2. Use ``tf2_ros::TransformBroadcaster`` to publish the transform
       from ``world`` to ``base_link`` at 10 Hz.
    3. The robot should move in a circle of radius 2.0 m centered at the
       origin:

       - ``x = 2.0 * cos(angle)``
       - ``y = 2.0 * sin(angle)``
       - ``z = 0.0``

    4. Increment the angle by 0.05 radians each timer callback.
    5. Set the rotation quaternion to represent the robot facing the
       direction of travel (yaw = angle + pi/2). For simplicity, you may
       use an identity quaternion.
    6. Verify with: ``ros2 run tf2_ros tf2_echo world base_link``

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <tf2_ros/transform_broadcaster.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>
           #include <cmath>

           class CircularMotionBroadcaster : public rclcpp::Node {
            public:
             CircularMotionBroadcaster()
                 : Node{"circular_motion_broadcaster"}, angle_{0.0} {
               tf_broadcaster_ =
                   std::make_unique<tf2_ros::TransformBroadcaster>(this);

               timer_ = this->create_wall_timer(
                   std::chrono::milliseconds{100},
                   std::bind(&CircularMotionBroadcaster::broadcast_transform,
                             this));
             }

            private:
             void broadcast_transform() {
               geometry_msgs::msg::TransformStamped t;
               t.header.stamp = this->get_clock()->now();
               t.header.frame_id = "world";
               t.child_frame_id = "base_link";

               double radius{2.0};
               t.transform.translation.x = radius * std::cos(angle_);
               t.transform.translation.y = radius * std::sin(angle_);
               t.transform.translation.z = 0.0;

               // Identity quaternion for simplicity
               t.transform.rotation.x = 0.0;
               t.transform.rotation.y = 0.0;
               t.transform.rotation.z = 0.0;
               t.transform.rotation.w = 1.0;

               tf_broadcaster_->sendTransform(t);

               RCLCPP_INFO(this->get_logger(),
                           "Robot at (%.2f, %.2f)",
                           t.transform.translation.x,
                           t.transform.translation.y);

               angle_ += 0.05;
             }

             std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
             rclcpp::TimerBase::SharedPtr timer_;
             double angle_;
           };

           int main(int argc, char* argv[]) {
             rclcpp::init(argc, argv);
             rclcpp::spin(std::make_shared<CircularMotionBroadcaster>());
             rclcpp::shutdown();
             return 0;
           }


.. dropdown:: Exercise 3: Transform Listener (Distance Computation)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Listen for transforms and compute the distance between two frames.

    **Specification**

    1. Create a ROS 2 node called ``distance_calculator``.
    2. Use ``tf2_ros::Buffer`` and ``tf2_ros::TransformListener`` to
       listen for transforms.
    3. Every second, look up the transform from ``world`` to
       ``camera_link``.
    4. Compute the Euclidean distance from the world origin to the
       camera_link frame:

       - ``distance = sqrt(x^2 + y^2 + z^2)``

    5. Log the distance.
    6. Handle ``tf2::TransformException`` with a warning message.
    7. Test by running the circular motion broadcaster (Exercise 2) and
       the static camera broadcaster (Exercise 1) simultaneously.

    .. dropdown:: Solution
        :class-container: sd-border-success

        .. code-block:: cpp

           #include <rclcpp/rclcpp.hpp>
           #include <tf2_ros/buffer.h>
           #include <tf2_ros/transform_listener.h>
           #include <geometry_msgs/msg/transform_stamped.hpp>
           #include <tf2/exceptions.h>
           #include <cmath>

           class DistanceCalculator : public rclcpp::Node {
            public:
             DistanceCalculator()
                 : Node{"distance_calculator"} {
               tf_buffer_ =
                   std::make_unique<tf2_ros::Buffer>(this->get_clock());
               tf_listener_ =
                   std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);

               timer_ = this->create_wall_timer(
                   std::chrono::seconds{1},
                   std::bind(&DistanceCalculator::compute_distance, this));
             }

            private:
             void compute_distance() {
               try {
                 auto t = tf_buffer_->lookupTransform(
                     "world", "camera_link", tf2::TimePointZero);

                 double x{t.transform.translation.x};
                 double y{t.transform.translation.y};
                 double z{t.transform.translation.z};
                 double distance{std::sqrt(x * x + y * y + z * z)};

                 RCLCPP_INFO(this->get_logger(),
                             "Distance from world to camera_link: %.3f m",
                             distance);

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
             rclcpp::spin(std::make_shared<DistanceCalculator>());
             rclcpp::shutdown();
             return 0;
           }
