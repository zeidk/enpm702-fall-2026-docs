References
==========


.. dropdown:: Lecture 14
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L14: Lifecycle Nodes**

        Covers managed (lifecycle) nodes in ROS 2: the state machine
        (Unconfigured, Inactive, Active, Finalized), transition callbacks
        (``on_configure``, ``on_activate``, ``on_deactivate``,
        ``on_cleanup``, ``on_shutdown``), ``CallbackReturn`` values,
        ``LifecyclePublisher`` behavior, and managing lifecycle nodes via
        the CLI and programmatic interfaces.

        These topics support **GP3**. Complete the C++ exercises on
        lifecycle nodes and take the quiz before starting GP3.


.. dropdown:: ROS 2 Lifecycle Node Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Managed Nodes Tutorial
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Managing-Nodes-Lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Managing Nodes with Lifecycle**

            Official tutorial on lifecycle (managed) nodes, covering the
            state machine, transition callbacks, and CLI management.

            +++

            - Lifecycle state machine overview
            - Implementing transition callbacks
            - CLI commands for lifecycle management
            - Coordinated system bringup

        .. grid-item-card:: rclcpp_lifecycle API
            :link: https://docs.ros.org/en/jazzy/p/rclcpp_lifecycle/
            :class-card: sd-border-secondary

            **rclcpp_lifecycle API Reference**

            API documentation for the ``rclcpp_lifecycle`` package
            including ``LifecycleNode``, ``LifecyclePublisher``, and
            transition callback types.

            +++

            - ``rclcpp_lifecycle::LifecycleNode``
            - ``rclcpp_lifecycle::LifecyclePublisher``
            - ``CallbackReturn`` enum
            - State and transition types

        .. grid-item-card:: lifecycle_msgs
            :link: https://docs.ros.org/en/jazzy/p/lifecycle_msgs/
            :class-card: sd-border-secondary

            **lifecycle_msgs Message/Service Reference**

            Documentation for lifecycle message and service types
            including ``State``, ``Transition``, ``ChangeState``, and
            ``GetState``.

            +++

            - ``lifecycle_msgs::msg::State``
            - ``lifecycle_msgs::msg::Transition``
            - ``lifecycle_msgs::srv::ChangeState``
            - ``lifecycle_msgs::srv::GetState``

        .. grid-item-card:: Lifecycle Node Design Document
            :link: https://design.ros2.org/articles/node_lifecycle.html
            :class-card: sd-border-secondary

            **ROS 2 Design: Managed Nodes**

            The original design document for the ROS 2 lifecycle node
            concept, explaining the motivation, state machine design,
            and intended usage patterns.

            +++

            - Design rationale
            - State machine specification
            - Transition callbacks
            - Error handling model
