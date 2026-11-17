References
==========


.. dropdown:: Lecture 12
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L12: Robots in Gazebo and Parameters**

        The ROSbot in Gazebo, a proportional controller, and parameters:
        declaring and reading them, setting them with ``-p``, a YAML file
        and a launch file, and changing them with ``ros2 param`` and a
        parameter callback.

        **Before the lecture**: read :doc:`Mobile Robot Messages
        </reading_material/robot_messages/rmsg_index>` and set up
        :doc:`ROSbot Simulation </setup/rosbot_simulation>`.


.. dropdown:: ROS 2 Documentation: Parameters
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Understanding Parameters
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Understanding Parameters**

            What a parameter is, and the commands that list, get, set,
            dump and load parameters.

            +++

            - ``ros2 param list``
            - ``ros2 param get``
            - ``ros2 param set``

        .. grid-item-card:: Using Parameters in a Class (C++)
            :link: https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Using-Parameters-In-A-Class-CPP.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Using Parameters in a Class (C++)**

            Declare and read a parameter in a node, and change it from the
            command line.

            +++

            - ``declare_parameter``
            - ``get_parameter``

        .. grid-item-card:: Parameters in Launch Files
            :link: https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Using ROS 2 Launch For Large Projects**

            Load a parameter file from a launch file, and pass launch
            arguments to nodes.


.. dropdown:: The ROSbot
    :class-container: sd-border-secondary

    The ROSbot's topics, drive controller and filter come from Husarion's
    ``rosbot_ros`` packages, in the ``rosbot_sim/`` folder of the course
    repository. See :doc:`ROSbot Simulation </setup/rosbot_simulation>`.
