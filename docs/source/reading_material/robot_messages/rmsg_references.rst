====================================================
References
====================================================

.. dropdown:: Mobile Robot Messages
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Mobile Robot Messages**

        The directions and units of ROS, the velocity command (``Twist``
        and ``TwistStamped``), odometry (``Odometry``, the ``odom`` frame,
        where the ROSbot's estimate comes from), orientation as a
        quaternion and as a yaw, and the range sensor (``LaserScan``, the
        angle of each beam, the ranges to discard). It explains the topics
        of :doc:`GP1 </assignments/gp1>` and :doc:`GP2 </assignments/gp2>`.


.. dropdown:: ROS Enhancement Proposals
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: REP 103
            :link: https://www.ros.org/reps/rep-0103.html
            :class-card: sd-border-secondary

            **Standard Units of Measure and Coordinate Conventions**: SI
            units, x forward, y left, z up, right-handed axes

        .. grid-item-card:: REP 105
            :link: https://www.ros.org/reps/rep-0105.html
            :class-card: sd-border-secondary

            **Coordinate Frames for Mobile Platforms**: the ``base_link``,
            ``odom`` and ``map`` frames

        .. grid-item-card:: REP 117
            :link: https://www.ros.org/reps/rep-0117.html
            :class-card: sd-border-secondary

            **Informational Distance Measurements**: ``-inf``, ``NaN`` and
            ``+inf`` in range readings


.. dropdown:: The ROSbot
    :class-container: sd-border-secondary

    The ROSbot's topics, drive controller and filter come from Husarion's
    ``rosbot_ros`` packages, in the ``rosbot_sim/`` folder of the course
    repository. See :doc:`ROSbot Simulation </setup/rosbot_simulation>`.
