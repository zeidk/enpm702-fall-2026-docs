References
==========


.. dropdown:: Lecture 11
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L11: ROS 2 Configuration and Orchestration**

        Python launch files (the ``Node`` action, ``add_action`` and one list, installing the ``launch`` folder), including another launch file, launch arguments and conditions, groups and namespaces, groups with a condition, event handlers, and ``LogInfo``. Executors: ``rclcpp::spin(node)`` and the single-threaded executor, two nodes in one executor, a slow callback, the multi-threaded executor, parallel callbacks and data races, how many threads to give it, and mutually exclusive and reentrant callback groups. Custom interfaces: a ``.msg`` file in an interface package, building it, and using the generated C++ type.

        **Before next class**: complete the L11 exercises and quiz, and build and run ``l11_robotaxi`` in your own workspace.


.. dropdown:: Required Reading
    :class-container: sd-border-secondary
    :open:

    - Open Robotics. `Creating a launch file <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html>`_. ROS 2 Documentation: Jazzy, 2024.
    - Open Robotics. `Executors <https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Executors.html>`_. ROS 2 Documentation: Jazzy, 2024.
    - Open Robotics. `Creating custom msg and srv files <https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html>`_. ROS 2 Documentation: Jazzy, 2024.


.. dropdown:: Sources Cited in the Lecture
    :class-container: sd-border-secondary

    **ROS 2 Documentation: Jazzy** (Open Robotics, 2024)

    - `Integrating launch files into ROS 2 packages <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-system.html>`_
    - `Using Callback Groups <https://docs.ros.org/en/jazzy/How-To-Guides/Using-callback-groups.html>`_
    - `Class MultiThreadedExecutor <https://docs.ros.org/en/jazzy/p/rclcpp/generated/classrclcpp_1_1executors_1_1MultiThreadedExecutor.html>`_ (rclcpp: Jazzy 28.1.23 documentation)

    **C++**

    - cppreference.com. `Multi-threaded executions and data races (since C++11) <https://en.cppreference.com/w/cpp/language/multithread>`_, 2025.
