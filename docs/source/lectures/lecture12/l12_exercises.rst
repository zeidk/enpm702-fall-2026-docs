====================================================
ROS Exercises
====================================================

These exercises use the package ``l12_rosbot`` of the lecture, in your own workspace, with the Gazebo simulation running (``ros2 launch gp2_bringup gp2_sim.launch.py``). Start from the final code of the package (stage 5). Restart the simulation before each run, so the robot starts at the origin and faces east.

.. note::

   Build and run from the workspace's top folder:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build --packages-select l12_rosbot
      source install/setup.bash

----


.. dropdown:: Exercise 1: Your Own Headings and Gain
    :icon: rocket
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Change what ``heading_controller_node`` does without touching its C++ code: only a parameter file and a launch argument.

    **Specification**

    1. Create ``config/my_headings.yaml`` in ``l12_rosbot``. It has the ``/**`` key with ``use_sim_time: true``, and a ``heading_controller_node`` key with these parameters:

       - ``target_headings_deg``: ``[60.0, 0.0, -60.0, 0.0]``
       - ``kp_angular``: ``1.0``
       - ``max_angular_rps``: ``0.8``
       - ``yaw_tolerance_rad``: ``0.02``

    2. Before you run anything, work out the four turns. The robot starts at 0°. For each target heading, write the error the controller computes at the start of that turn (the angle left, the short way, in radians) and its sign.
    3. With a gain of 1.0 and a limit of 0.8 rad/s, the command equals the error while the error is 0.8 rad or less, and it stays at 0.8 rad/s above that. Predict the first command of the first turn, and the error at which the command leaves the limit.
    4. Run the node with the file, from the package folder:

       .. code-block:: bash

          ros2 run l12_rosbot heading_controller_exe \
            --ros-args --params-file config/my_headings.yaml

       Compare the first ``error`` and ``command`` lines of the log with your prediction. Check that the node logs ``heading 60 deg reached``, ``heading 0 deg reached``, and so on, and ``all 4 headings reached`` at the end.
    5. Read each turn's time from the time stamps of two ``reached`` lines. Are the four turns about equally long? Say why, from the errors of step 2.
    6. Rebuild, so the ``config`` folder is installed, then start the node with the launch file and your file as the ``params_file`` argument:

       .. code-block:: bash

          ros2 launch l12_rosbot heading_launch.py \
            params_file:=install/l12_rosbot/share/l12_rosbot/config/my_headings.yaml

    7. While the node runs, check the values with ``ros2 param get`` for ``kp_angular`` and ``use_sim_time``. Then run the node with a plain ``ros2 run`` and no file, and check ``use_sim_time`` again. What changed, and why?


.. dropdown:: Exercise 2: A Stricter Parameter Callback
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    ``on_parameters_set`` in ``heading_controller_node`` checks ``kp_angular`` and ``max_angular_rps``, but it accepts any ``yaw_tolerance_rad`` and a gain of exactly 0. Close both gaps.

    **Specification**

    1. Before you change anything, explain what each value would do to a turn:

       - ``yaw_tolerance_rad`` 0.0 or less: when does ``control_callback`` decide that the heading is reached?
       - ``kp_angular`` 0.0: what command does the proportional control law give, whatever the error?

    2. In the first loop of ``on_parameters_set``, which checks every new value before anything is stored, add two checks, each with a ``reason`` that names the parameter:

       - ``yaw_tolerance_rad`` must be more than 0.
       - ``kp_angular`` must be more than 0 (today the check refuses only a negative gain).

    3. In the second loop, nothing changes: it already stores ``yaw_tolerance_rad`` and ``kp_angular``.
    4. Build, start the simulation, and run the node with ``config/low_gain.yaml``, so each turn takes several seconds:

       .. code-block:: bash

          ros2 run l12_rosbot heading_controller_exe \
            --ros-args --params-file config/low_gain.yaml

    5. While the robot turns, send these ``ros2 param set`` commands and write down each answer:

       - ``yaw_tolerance_rad 0.0``
       - ``yaw_tolerance_rad -0.01``
       - ``kp_angular 0.0``
       - ``kp_angular 0`` (what does ROS 2 answer, and who refuses it: your callback or ROS 2?)
       - ``yaw_tolerance_rad 0.05``

    6. After the last set, read the ``error`` of the next ``heading ... deg reached`` lines. Is it now under 0.05 rad instead of under 0.02 rad? Does the turn end sooner?
