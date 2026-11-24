====================================================
Reading Material
====================================================

Supplemental topics provided as self-study reading modules. Students
are expected to work through these outside of class.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Covers**
   * - :doc:`compiler_warnings/cw_index`
     - Compiler warning flags: ``-Wall``, ``-Wextra``, ``-pedantic-errors``,
       the warnings each one enables, and the additional flags
       ``-Wshadow``, ``-Wconversion``, and ``-Werror``
   * - :doc:`sphinx_breathe/sb_index`
     - Reference pages built from Doxygen comments with Sphinx and the
       Breathe extension: Doxygen XML output, ``conf.py``, Breathe
       directives, rebuilding after a change
   * - :doc:`exception_handling/eh_index`
     - Exception handling with ``try``, ``catch``, ``throw``, standard
       and custom exception classes, ``noexcept``, RAII
   * - :doc:`flow_control/fc_index`
     - Selection statements (``if``, ``switch``), iteration statements
       (``while``, ``do-while``, ``for``), operators (arithmetic,
       relational, logical)
   * - :doc:`foxglove/fx_index`
     - Foxglove, a program that draws ROS 2 topics: what it is, installing
       the ``foxglove_bridge`` package and the app, connecting to the ROSbot
       simulation at ``ws://localhost:8765``, and a layout file with a 3D,
       an Image, a Plot and a Raw Messages panel. Optional reading, not needed
       for any assignment
   * - :doc:`linux_shell/ls_index`
     - The Linux command-line shell: common shell types, configuration
       files (``.bashrc``, ``.zshrc``), aliases, and functions
   * - :doc:`robot_messages/rmsg_index`
     - The messages of a mobile robot in GP1 and GP2: directions and units
       (REP 103), ``Twist`` and ``TwistStamped`` on ``cmd_vel``,
       ``Odometry`` and the ``odom`` frame, quaternion and yaw,
       ``LaserScan`` and the angle of each beam
   * - :doc:`remapping/remap_index`
     - Namespaces and remapping rules: a namespace in front of a node's name
       and relative names, relative, absolute and private names, a rule
       ``match:=replacement`` for a topic, a node name and a namespace, on
       the command line and in a launch file
   * - :doc:`services_actions/sa_index`
     - Services and actions in C++: the ``.srv`` and ``.action`` files, a
       server and a client for each, feedback, a cancel request and a
       timeout, and the ``ros2 service`` and ``ros2 action`` commands.
       Extra reading, beyond the course projects
   * - :doc:`input_validation/iv_index`
     - Validating terminal input: what ``std::cin >> value`` does when the
       input is not a number, stream state and recovery, and whole-line
       parsing with ``std::getline`` and ``std::from_chars``
   * - :doc:`value_categories/vcat_index`
     - lvalue, xvalue and prvalue: four steps to find the category of an
       expression, checking with ``decltype((e))``, worked examples,
       common traps, and how the category picks a copy or a move
   * - :doc:`version_control/vc_index`
     - Git fundamentals, branching, merging, GitHub, pull requests,
       fork workflow
   * - :doc:`vscode_cmake/vcm_index`
     - VSCode installation and interface, workspace layout, the
       ``.vscode`` folder, recommended extensions, Command Palette,
       ``CMakeLists.txt``, hybrid per-lecture build setup


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   compiler_warnings/cw_index
   sphinx_breathe/sb_index
   exception_handling/eh_index
   flow_control/fc_index
   foxglove/fx_index
   linux_shell/ls_index
   robot_messages/rmsg_index
   remapping/remap_index
   services_actions/sa_index
   input_validation/iv_index
   value_categories/vcat_index
   version_control/vc_index
   vscode_cmake/vcm_index
