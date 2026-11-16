====================================================
ROS Exercises
====================================================

This exercise brings together the concepts of Lecture 11: a custom
interface, launch files with arguments, conditions, groups and events, and
an executor.

.. note::

   Build all ROS 2 packages with:

   .. code-block:: bash

      cd ~/ros2_ws && colcon build --packages-up-to my_package
      source install/setup.bash

.. note::

   **Naming.** A node's name ends with ``_node`` and its executable's name
   with ``_exe``. A node class lives in ``<name>_node.hpp`` and
   ``<name>_node.cpp``, and its ``main`` in ``<name>_main.cpp``.

----


.. dropdown:: Exercise: Depot Chargers
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a depot with one or two chargers. Each charger reports its
    state in a message type you write yourself. A launch file starts the
    chargers in namespaces, and one executable runs a charger and a
    monitor in one executor.

    **Specification**

    1. Create an interface package ``l11_depot_interfaces`` with the
       message ``msg/ChargerStatus.msg``:

       - Two constants of type ``uint8``: ``STATE_FREE`` (0) and
         ``STATE_BUSY`` (1).
       - A ``std_msgs/Header header``.
       - A ``string charger_name`` and a ``uint8 state``, the state being
         one of the constants above.

       Generate its code from ``CMakeLists.txt`` and ``package.xml``, and
       check it with ``ros2 interface show``.

    2. Create a package ``l11_depot`` that depends on
       ``l11_depot_interfaces``, with two nodes:

       **ChargerNode** (``charger_node.hpp``, ``charger_node.cpp``;
       executable ``charger_exe``, node name ``charger_node``):

       - Publishes a ``ChargerStatus`` every 1 s on the relative topic
         name ``charger/status``.
       - Reports ``STATE_FREE`` for the first 3 messages, then
         ``STATE_BUSY``.

       **DepotMonitorNode** (``depot_monitor_node.hpp``,
       ``depot_monitor_node.cpp``; executable ``depot_monitor_exe``, node
       name ``depot_monitor_node``):

       - Subscribes to the relative topic name ``charger/status``.
       - Compares the state with the constants by name, and logs the
         charger's name and the state as a word, ``free`` or ``busy``.

    3. Create a ``launch/depot_launch.py`` that:

       - Declares a launch argument ``two_chargers``, ``"false"`` by
         default, with a description.
       - Has a function ``make_charger(namespace, condition=None)`` that
         returns a ``GroupAction`` holding a ``PushROSNamespace`` and the
         ``charger_exe`` and ``depot_monitor_exe`` nodes.
       - Adds the group for the namespace ``charger1`` always, and the
         group for ``charger2`` only when ``two_chargers`` is true.
       - Registers an ``OnShutdown`` handler that logs ``Depot closed``
         with ``LogInfo``.

       Install the ``launch`` folder from ``CMakeLists.txt``.

    4. Create a third executable, ``depot_exe``, whose ``main`` adds one
       ``ChargerNode`` and one ``DepotMonitorNode`` to one
       ``SingleThreadedExecutor``.

    5. Build, run, and verify:

       - ``ros2 launch l11_depot depot_launch.py --show-args`` lists
         ``two_chargers`` and starts nothing.
       - Without the argument, ``ros2 node list`` shows two nodes, both
         in ``/charger1``.
       - With ``two_chargers:=true``, it shows four nodes, in
         ``/charger1`` and ``/charger2``.
       - After :kbd:`Ctrl+C`, the launch prints ``Depot closed``.
       - ``ros2 run l11_depot depot_exe`` logs the same states with both
         nodes in one process.
       - ``ros2 topic echo --once`` on a charger's topic shows the state
         as a number.
