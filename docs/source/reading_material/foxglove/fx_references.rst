====================================================
References
====================================================

.. dropdown:: Foxglove
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Foxglove**

        What Foxglove is, how to install the bridge and the app, how to
        connect to the simulation, and what each panel of the course
        layout shows. The layout file is
        :download:`rosbot_sim_layout.json </_static/files/foxglove/rosbot_sim_layout.json>`.
        It is optional reading: no assignment depends on it.


.. dropdown:: Foxglove documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Introduction to the visualization app
            :link: https://docs.foxglove.dev/docs/visualization/introduction
            :class-card: sd-border-secondary

            The desktop app and the web app, the systems they run on, and
            the features that only the desktop app has

        .. grid-item-card:: Get started with ROS 2
            :link: https://docs.foxglove.dev/docs/getting-started/frameworks/ros2
            :class-card: sd-border-secondary

            The prerequisites, the bridge install command, and the steps
            to open a connection

        .. grid-item-card:: Layouts
            :link: https://docs.foxglove.dev/docs/visualization/layouts
            :class-card: sd-border-secondary

            Exporting a layout to a JSON file and importing it again

        .. grid-item-card:: 3D panel
            :link: https://docs.foxglove.dev/docs/visualization/panels/3d
            :class-card: sd-border-secondary

            Display frame, follow mode, topic visibility, and loading a
            URDF

        .. grid-item-card:: Plot panel
            :link: https://docs.foxglove.dev/docs/visualization/panels/plot
            :class-card: sd-border-secondary

            The message path syntax of a plot series

        .. grid-item-card:: Download
            :link: https://foxglove.dev/download
            :class-card: sd-border-secondary

            The desktop app for Linux, Windows and macOS


.. dropdown:: Foxglove bridge
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: foxglove_bridge README
            :link: https://github.com/foxglove/foxglove-sdk/blob/main/ros/src/foxglove_bridge/README.md
            :class-card: sd-border-secondary

            The ROS 2 package: install, launch, the ``port`` parameter
            and the other settings


.. dropdown:: The ROSbot simulation
    :class-container: sd-border-secondary

    The simulation and its topics are described in
    :doc:`ROSbot Simulation </setup/rosbot_simulation>`.
