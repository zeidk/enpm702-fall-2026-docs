====================================================
References
====================================================

.. dropdown:: Services and Actions
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Services and Actions**

        The service and the action of ROS 2: the ``.srv`` and ``.action``
        files, a server and a client for each in C++ with ``rclcpp`` and
        ``rclcpp_action``, feedback, a cancel request, a timeout counted on
        the node clock, and the ``ros2 service`` and ``ros2 action``
        commands. It is extra reading, beyond the lectures and the course
        projects.


.. dropdown:: ROS 2 Documentation: Services
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Understanding Services
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Understanding Services**

            The service concept, and the commands that list, call and
            inspect services.

            +++

            - ``ros2 service list``
            - ``ros2 service type``
            - ``ros2 service call``

        .. grid-item-card:: Writing a Service and Client (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Service-And-Client.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Writing a Simple Service and Client (C++)**

            A service server and a client with ``rclcpp``.

            +++

            - ``create_service``
            - ``create_client`` and ``async_send_request``

        .. grid-item-card:: Custom Interfaces
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Custom Interfaces**

            Custom ``.msg`` and ``.srv`` files in an interface package.

            +++

            - ``rosidl_generate_interfaces``
            - ``package.xml`` dependencies


.. dropdown:: ROS 2 Documentation: Actions
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Understanding Actions
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Understanding Actions**

            The goal, feedback and result of an action, and the commands
            that work with actions.

            +++

            - ``ros2 action list``
            - ``ros2 action info``
            - ``ros2 action send_goal --feedback``

        .. grid-item-card:: Writing an Action Server and Client (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Writing-an-Action-Server-Client/Cpp.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Writing an Action Server and Client (C++)**

            An action server with goal handling, feedback and
            cancellation, and an action client, with ``rclcpp_action``.

            +++

            - ``rclcpp_action::create_server``
            - ``rclcpp_action::create_client``
            - ``SendGoalOptions``

        .. grid-item-card:: ROS 2 Design: Actions
            :link: https://design.ros2.org/articles/actions.html
            :class-card: sd-border-secondary

            **ROS 2 Design: Actions**

            The design of actions: the topics and services inside an
            action, and the states of a goal.

        .. grid-item-card:: ``rclcpp_action`` API Reference
            :link: https://docs.ros.org/en/jazzy/p/rclcpp_action/
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: rclcpp_action API**

            The server, client and goal handle classes.
