References
==========


.. dropdown:: Lecture 12
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L12: Simulation, Control and Parameters**

        The ROSbot in Gazebo: ``gz sim`` and the bridge between Gazebo's topics and ROS, its sensors, the patrol world, starting the simulation, RViz, the topics, and driving it with ``ros2 topic pub``. Simulation time: ``/clock``, the computer's clock and ROS time, and which timer stops when Gazebo is paused. Proportional control: the error of a turn, the control law with a gain, a limit and a tolerance, and a heading controller. Parameters: declaring and reading them, ``ros2 param list``, ``get`` and ``set``, setting them with ``-p``, a YAML file and a launch file, ``use_sim_time``, and a parameter callback.

        **Before the lecture**: read :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>` and set up :doc:`ROSbot Simulation </setup/rosbot_simulation>`.

        **Before next class**: complete the L12 exercises and quiz, and build and run ``l12_rosbot`` in your own workspace.


.. dropdown:: Required Reading
    :class-container: sd-border-secondary
    :open:

    - Open Robotics. `Parameters <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`_. ROS 2 Documentation: Jazzy, 2024.
    - :doc:`ROSbot Simulation </setup/rosbot_simulation>`
    - :doc:`Mobile Robot Messages </reading_material/robot_messages/rmsg_index>`


.. dropdown:: Sources Cited in the Lecture
    :class-container: sd-border-secondary

    **ROS 2 Documentation: Jazzy** (Open Robotics, 2024)

    - `Parameters <https://docs.ros.org/en/jazzy/Concepts/Basic/About-Parameters.html>`_

    **ROS 2 Design** (Open Robotics)

    - `Clock and Time <https://design.ros2.org/articles/clock_and_time.html>`_
