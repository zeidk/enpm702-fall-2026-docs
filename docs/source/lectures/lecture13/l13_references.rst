References
==========


.. dropdown:: Lecture 13
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L13: Coordinate Frames and Transforms**

        Covers coordinate frame management with TF2: the frame tree
        concept, static and dynamic transform broadcasting, transform
        listening with ``lookupTransform()``, the ``TransformStamped``
        message, and debugging tools (``view_frames``, ``tf2_echo``,
        RViz2).

        These topics support **GP3**. Complete the C++ exercises on TF2
        and take the quiz before starting GP3.


.. dropdown:: ROS 2 TF2 Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: TF2 Tutorials
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: TF2 Tutorials**

            Official ROS 2 tutorials for the TF2 library, covering
            static and dynamic broadcasters, transform listeners,
            frame debugging, and time travel.

            +++

            - Introduction to TF2
            - Writing a static broadcaster (C++)
            - Writing a broadcaster (C++)
            - Writing a listener (C++)
            - Adding a frame
            - Using time with TF2

        .. grid-item-card:: TF2 API Reference
            :link: https://docs.ros.org/en/jazzy/p/tf2_ros/
            :class-card: sd-border-secondary

            **tf2_ros API Reference**

            API documentation for the ``tf2_ros`` package including
            ``TransformBroadcaster``, ``StaticTransformBroadcaster``,
            ``TransformListener``, and ``Buffer``.

            +++

            - ``tf2_ros::TransformBroadcaster``
            - ``tf2_ros::StaticTransformBroadcaster``
            - ``tf2_ros::TransformListener``
            - ``tf2_ros::Buffer``

        .. grid-item-card:: geometry_msgs
            :link: https://docs.ros.org/en/jazzy/p/geometry_msgs/
            :class-card: sd-border-secondary

            **geometry_msgs Message Reference**

            Documentation for geometry message types used with TF2,
            including ``TransformStamped``, ``Transform``, ``Vector3``,
            and ``Quaternion``.

            +++

            - ``TransformStamped``
            - ``Transform``
            - ``Vector3``
            - ``Quaternion``
            - ``Pose`` and ``PoseStamped``

        .. grid-item-card:: REP 105: Coordinate Frames
            :link: https://www.ros.org/reps/rep-0105.html
            :class-card: sd-border-secondary

            **REP 105: Coordinate Frames for Mobile Platforms**

            The ROS Enhancement Proposal that defines standard coordinate
            frame conventions for mobile robots, including ``map``,
            ``odom``, ``base_link``, and ``base_footprint``.

            +++

            - Standard frame names
            - Frame relationships
            - Conventions for mobile robots
