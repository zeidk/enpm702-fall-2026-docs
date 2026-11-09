====================================================
ROS 2 Development Environment
====================================================

.. _setup-ros:

ROS 2 is required starting in **Week 11** (Lecture 10). The instructions
below are for **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04**, the version the
course code is built and tested on.

Checklist
---------

Before the first ROS 2 lecture, do these five steps on your laptop.

1. Install ROS 2: from `Which ROS 2 Distribution`_ to `Install Development
   Tools`_. On Ubuntu 22.04, follow `If Your Computer Has Ubuntu 22.04`_.
2. Set up your terminal with ``enpm702_env``: `Configure Your Shell`_.
3. Put the course code in your own private repository and build your
   workspace: `ROS 2 Workspace`_.
4. Check that ROS 2 works: `Verify ROS 2`_.
5. Install Gazebo: `Gazebo (Simulation)`_.


Which ROS 2 Distribution
------------------------

A ROS 2 *distribution* is a versioned set of ROS 2 packages. Each
distribution is built for one Ubuntu LTS release, so your Ubuntu version
decides which one you can install from packages. Check your Ubuntu
version first:

.. code-block:: bash

   lsb_release -a   # the line "Release:" gives the version, such as 24.04

Then find your row:

.. list-table::
   :header-rows: 1
   :widths: 18 24 14 16 28

   * - Ubuntu
     - ROS 2 distribution
     - Release type
     - Supported until
     - Installation guide
   * - 22.04 (Jammy)
     - Humble Hawksbill
     - LTS
     - May 2027
     - `Humble on Ubuntu <https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html>`__
   * - 24.04 (Noble)
     - **Jazzy Jalisco (this course)**
     - **LTS**
     - May 2029
     - `Jazzy on Ubuntu <https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html>`__
   * - 24.04 (Noble)
     - Kilted Kaiju
     - non-LTS
     - December 2026
     - `Kilted on Ubuntu <https://docs.ros.org/en/kilted/Installation/Ubuntu-Install-Debs.html>`__
   * - 26.04 (Resolute)
     - Lyrical Luth
     - LTS
     - May 2031
     - `Lyrical on Ubuntu <https://docs.ros.org/en/lyrical/Get-Started/Installation/Ubuntu-Install-Debs.html>`__

The dates come from the `ROS 2 distributions page
<https://docs.ros.org/en/jazzy/Releases.html>`__ (checked November 8, 2026).
`REP 2000 <https://www.ros.org/reps/rep-2000.html>`__ gives the support rules;
it ends Kilted one month earlier, in November 2026. An **LTS** (long-term support) distribution comes out in an even year and
is supported for 5 years. A non-LTS distribution comes out in an odd year
and is supported for 1.5 years. Iron Irwini, an older non-LTS distribution
for Ubuntu 22.04, reached its end of life on December 4, 2024: do not
install it.

.. note::

   On Ubuntu 24.04, install **Jazzy**: the course code, the lecture
   commands and the Group Projects use it. You can install it either way:

   - follow the official guide linked in the table (**Jazzy on Ubuntu**), or
   - follow the steps on this page, from `Set Locale`_ to `Gazebo
     (Simulation)`_: they are the official guide's steps, plus Gazebo and
     the course workspace.

   On Ubuntu 22.04, follow :ref:`setup-ros-jammy` instead (or the
   **Humble on Ubuntu** guide in the table).


Set Locale
----------

.. code-block:: bash

   locale  # check for UTF-8

   sudo apt update && sudo apt install locales
   sudo locale-gen en_US en_US.UTF-8
   sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
   export LANG=en_US.UTF-8

   locale  # verify settings


Add the ROS 2 Repository
-------------------------

Enable the Ubuntu Universe repository, then install the
``ros2-apt-source`` package, which adds the ROS 2 repository and its key.
These are the steps of the official Jazzy installation guide.

.. code-block:: bash

   sudo apt install software-properties-common
   sudo add-apt-repository universe

   sudo apt update && sudo apt install curl -y
   export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
   curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
   sudo dpkg -i /tmp/ros2-apt-source.deb

   sudo apt update
   sudo apt upgrade

.. note::

   Older guides download ``ros.key`` with ``curl`` and write
   ``/etc/apt/sources.list.d/ros2.list`` by hand. The official guides
   replaced those steps with ``ros2-apt-source``, which updates the key
   and the repository settings by itself.


Install ROS 2 Jazzy
--------------------

.. code-block:: bash

   sudo apt install ros-jazzy-desktop

This installs ROS 2, RViz, demos, and tutorials.


Install Development Tools
-------------------------

On Ubuntu 24.04, first check the apt sources, as the official Jazzy guide
warns: with only the base ``noble`` suite, ``ros-dev-tools`` can hit
"dependency conflicts".

.. code-block:: bash

   grep Suites /etc/apt/sources.list.d/ubuntu.sources

If the line does not include ``noble-updates`` and ``noble-backports``, edit
that file so it reads ``Suites: noble noble-updates noble-backports``, then run
``sudo apt clean && sudo apt update && sudo apt full-upgrade -y``. Then:

.. code-block:: bash

   sudo apt install ros-dev-tools


Configure Your Shell
--------------------

.. admonition:: What ``source`` does, and why ROS 2 needs it
   :class: important

   ``source file`` runs the commands of ``file`` **in the current terminal**.
   Running the same file as a program, ``bash file``, starts a second shell,
   and every setting it makes disappears when that shell ends. On the course
   laptop, ``ros2`` was still not found after ``bash
   /opt/ros/jazzy/setup.bash``, and was found after ``source
   /opt/ros/jazzy/setup.bash``.

   A ``setup.bash`` file sets **environment variables**: settings that the
   terminal passes to every program it starts. On the course laptop:

   - ``/opt/ros/jazzy/setup.bash`` adds the ROS 2 commands to ``PATH`` (so
     the terminal finds ``ros2``), the ROS 2 libraries to ``LD_LIBRARY_PATH``
     (so your nodes can load them), sets ``AMENT_PREFIX_PATH`` to
     ``/opt/ros/jazzy`` (where ``ros2 run`` looks for packages) and
     ``ROS_DISTRO`` to ``jazzy``.
   - ``~/ros2_ws/install/setup.bash`` puts the install folder of each of your
     packages (``~/ros2_ws/install/<package>``) in front of ``/opt/ros/jazzy``
     in ``AMENT_PREFIX_PATH``, so ``ros2 run`` finds your packages too. This
     is why ROS 2 is sourced first and the workspace second: the workspace is
     the overlay, on top of ROS 2, the underlay.

   These settings last only in that terminal. A new terminal starts without
   them, which is why ``enpm702_env`` goes in ``~/.bashrc``: Bash runs that file
   in every new terminal (Zsh runs ``~/.zshrc``).

Every terminal you use for ROS 2 needs three things: ROS 2 sourced, tab
completion for ``colcon`` (the build tool), and your workspace sourced. The
``enpm702_env`` function does all three. You add it to your shell configuration
file once, and it runs in every new terminal. It works in Bash and in Zsh.

1. Open ``~/.bashrc`` (Zsh users: ``~/.zshrc``) in a text editor, for
   example VS Code:

   .. code-block:: bash

      code ~/.bashrc

2. If your ``~/.bashrc`` already sources ROS 2 or a workspace for another
   course (lines such as ``source /opt/ros/humble/setup.bash`` or
   ``source ~/other_ws/install/setup.bash``), turn them off for ENPM702: put a
   ``#`` at the start of each line. With two ROS 2 versions or two workspaces
   sourced, ``ros2 run`` can start the wrong package, or a node can fail to
   load its libraries. To use them again later, remove the ``#``.

   .. code-block:: bash

      # source /opt/ros/humble/setup.bash
      # source ~/other_ws/install/setup.bash

3. Paste these lines at the bottom of the file and save it:

   .. code-block:: bash

      # enpm702_env sources ROS 2, turns on colcon's tab completion, then sources
      # your workspace, in the current terminal.
      enpm702_env() {
        local distro="${1:-jazzy}"
        local ws="${2:-$HOME/ros2_ws}"
        local sh="bash"
        [ -n "$ZSH_VERSION" ] && sh="zsh"
        if [ ! -f "/opt/ros/$distro/setup.$sh" ]; then
          echo "enpm702_env: ROS 2 $distro is not installed in /opt/ros/$distro"
          return 1
        fi
        source "/opt/ros/$distro/setup.$sh"
        local complete="/usr/share/colcon_argcomplete/hook/colcon-argcomplete.$sh"
        [ -f "$complete" ] && source "$complete"
        if [ -f "$ws/install/setup.$sh" ]; then
          source "$ws/install/setup.$sh"
          echo "enpm702_env: ROS 2 $distro and the workspace $ws"
        else
          echo "enpm702_env: ROS 2 $distro; $ws is not built yet (run colcon build in it)"
        fi
      }
      enpm702_env   # set ROS 2 and the workspace in every new terminal

4. Open a new terminal. Your workspace does not exist yet, so ``enpm702_env``
   prints the line below. That is expected: `ROS 2 Workspace`_ builds it.

   .. code-block:: text

      enpm702_env: ROS 2 jazzy; /home/<you>/ros2_ws is not built yet (run colcon build in it)

5. Check that ROS 2 works:

   .. code-block:: bash

      ros2 --help

How to call it, in any terminal:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Command
     - What it sources
   * - ``enpm702_env``
     - ROS 2 Jazzy, then the workspace ``~/ros2_ws``
   * - ``enpm702_env humble``
     - ROS 2 Humble (Ubuntu 22.04), then ``~/ros2_ws``
   * - ``enpm702_env jazzy ~/my_ws``
     - ROS 2 Jazzy, then another workspace, ``~/my_ws``

- After ``colcon build`` adds a new package, run ``enpm702_env`` again in that
  terminal so it finds the package.
- On Ubuntu 22.04, change the last line you pasted to ``enpm702_env humble``.

.. dropdown:: Manual alternative: three lines instead of the function

   Use either the function or these three lines, not both.

   **Bash** (``~/.bashrc``):

   .. code-block:: bash

      echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
      echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
      echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

   **Zsh** (``~/.zshrc``):

   .. code-block:: bash

      echo "source /opt/ros/jazzy/setup.zsh" >> ~/.zshrc
      echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.zsh" >> ~/.zshrc
      echo "source ~/ros2_ws/install/setup.zsh" >> ~/.zshrc

   Until you build the workspace (next section), the third line prints an
   error in every new terminal, because ``~/ros2_ws/install`` does not exist
   yet.


The colcon Build Tool
---------------------

.. admonition:: Definition: colcon
   :class: tip

   **colcon** (collective construction) is the command-line tool that builds the packages of a workspace. It works out the build order from their dependencies (`colcon documentation <https://colcon.readthedocs.io>`_).

.. admonition:: What colcon gives you
   :class: key-box

   - **Any language:** it builds C++ packages, Python packages and others.
   - **Parallel:** several packages build at the same time.
   - **Isolated:** each package builds in its own folder, so one cannot break another.
   - **Extensible:** plugins add build types.
   - **Cross-platform:** Linux, Windows and macOS.

``ros-dev-tools`` (`Install Development Tools`_) installs colcon. Check it:

.. code-block:: bash

   colcon version-check

It prints one line per part of colcon, such as ``colcon-argcomplete 0.3.3: up-to-date``.

Build Commands
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 50 50
   :class: compact-table

   * - Command
     - What it builds
   * - ``colcon build``
     - Every package in ``src``
   * - ``colcon build --packages-select robotaxi_demo``
     - Only ``robotaxi_demo``
   * - ``colcon build --packages-up-to robotaxi_demo``
     - ``robotaxi_demo`` and the packages of the workspace it depends on
   * - ``colcon build --parallel-workers 4``
     - At most 4 packages at once (the default is the number of CPU cores)
   * - ``colcon build --symlink-install``
     - Installs links to files such as launch files instead of copies, so an edit to them needs no new build. C++ code still needs one.

Run every ``colcon`` command from the workspace's top folder (``~/ros2_ws``), never from ``src``.


ROS 2 Workspace
---------------

The course code is in the repository
`rubixcubic/enpm702-fall-2026-ros <https://github.com/rubixcubic/enpm702-fall-2026-ros>`__,
one folder per lecture (``L10`` to ``L14``). The packages of each lecture
appear in its folder as the course goes on. You keep your own **private**
copy of it on GitHub and get new course code from the course repository. Your clone has two remotes (names for GitHub
repositories):

- ``origin``: your private repository. ``git push`` and ``git pull`` use it.
- ``upstream``: the course repository. You only get code from it.

A fork would not work here: GitHub makes a fork of a public repository
public. Before you start, on each computer you use:

- Set up your GitHub SSH key, as the
  :doc:`Version Control reading </reading_material/version_control/vc_index>`
  shows: ``git push`` to your repository needs it.
- Tell Git your name and email once. Without them, your first ``git commit``
  stops with ``*** Please tell me who you are.``

  .. code-block:: bash

     git config --global user.name "Your Name"
     git config --global user.email "you@umd.edu"

1. **Create your private repository.** On GitHub, click **New repository**.
   Name it ``enpm702-fall-2026-ros``, choose **Private**, and leave it empty:
   no README, no ``.gitignore``, no license. A file in it would make your
   first push fail.

2. **Clone the course repository** into the ``src`` folder of your workspace:

   .. code-block:: bash

      mkdir -p ~/ros2_ws/src
      cd ~/ros2_ws/src
      git clone https://github.com/rubixcubic/enpm702-fall-2026-ros.git

3. **Set the two remotes and push to your repository.** Git names the course
   repository ``origin`` in your clone. Rename it ``upstream``, then add your
   private repository as ``origin`` (write your GitHub username in place of
   ``<you>``):

   .. code-block:: bash

      cd ~/ros2_ws/src/enpm702-fall-2026-ros
      git remote rename origin upstream
      git remote add origin git@github.com:<you>/enpm702-fall-2026-ros.git
      git remote -v
      git push -u origin main

   ``git remote -v`` prints:

   .. code-block:: text

      origin    git@github.com:<you>/enpm702-fall-2026-ros.git (fetch)
      origin    git@github.com:<you>/enpm702-fall-2026-ros.git (push)
      upstream  https://github.com/rubixcubic/enpm702-fall-2026-ros.git (fetch)
      upstream  https://github.com/rubixcubic/enpm702-fall-2026-ros.git (push)

   ``-u`` makes your repository the default, so from now on ``git push`` and
   ``git pull`` with no names use ``origin``.

4. **Build the workspace**, then run ``enpm702_env`` so this terminal finds it:

   .. code-block:: bash

      cd ~/ros2_ws
      colcon build
      enpm702_env

   Until the first lecture package is published, ``colcon build`` finds
   nothing to build and ends with ``Summary: 0 packages finished``. It still
   creates ``build``, ``install`` and ``log``, so ``enpm702_env`` now prints:

   .. code-block:: text

      enpm702_env: ROS 2 jazzy and the workspace /home/<you>/ros2_ws

   With the manual alternative, run ``source install/setup.bash`` instead of
   ``enpm702_env``.

Three jobs come up day to day. Run each one from
``~/ros2_ws/src/enpm702-fall-2026-ros``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - When
     - Commands
   * - You changed files and want them saved on GitHub
     - ``git add <files>``, then ``git commit -m "what you changed"``, then
       ``git push``
   * - The course repository has new code (a new lecture package)
     - ``git fetch upstream``, then ``git merge --no-edit upstream/main``,
       then ``git push`` (so your repository on GitHub has it too), then
       ``colcon build`` in ``~/ros2_ws``
   * - You work on another computer
     - The first time, clone your own repository there
       (``git clone git@github.com:<you>/enpm702-fall-2026-ros.git`` in
       ``~/ros2_ws/src``, with an SSH key on that computer), add ``upstream`` with
       ``git remote add upstream https://github.com/rubixcubic/enpm702-fall-2026-ros.git``,
       and build. After that, ``git pull`` before you start and ``git push``
       when you finish

.. dropdown:: More detail: ``git merge --no-edit upstream/main``
   :class-container: more-detail
   :icon: info

   .. list-table::
      :header-rows: 1
      :widths: 32 68

      * - Argument
        - Meaning (from ``git help merge``)
      * - ``upstream/main``
        - The course repository's ``main``, as ``git fetch upstream`` last downloaded it.
      * - ``--no-edit``
        - "accept the auto-generated message". Without it, Git first opens an editor for the merge message; save and close it to finish the merge.

Commit your own changes before ``git merge``. If Git reports a conflict, the
Version Control reading shows how to resolve it.


Verify ROS 2
------------

Open two terminals and run:

**Terminal 1 Talker:**

.. code-block:: bash

   ros2 run demo_nodes_cpp talker

**Terminal 2 Listener:**

.. code-block:: bash

   ros2 run demo_nodes_cpp listener

You should see the talker publishing messages and the listener
receiving them. Press :kbd:`Ctrl+C` in both terminals to stop.


VS Code for ROS 2
-----------------

VS Code underlines errors and completes names (IntelliSense) only when it
finds the headers your code includes. For ROS 2 code, those are in
``/opt/ros/jazzy``. The extension Robot Developer Extensions for ROS 2 writes
these paths for you. Installing extensions and the ``.vscode`` folder are
covered in :doc:`/reading_material/vscode_cmake/vcm_index`.

1. Install the C/C++ extension and the ROS 2 extension:

   .. code-block:: bash

      code --install-extension ms-vscode.cpptools
      code --install-extension ranch-hand-robotics.rde-ros-2

   Marketplace pages: `C/C++ <https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools>`__,
   `Robot Developer Extensions for ROS 2
   <https://marketplace.visualstudio.com/items?itemName=Ranch-Hand-Robotics.rde-ros-2>`__.

2. Open your workspace from a terminal where ROS 2 is set up:

   .. code-block:: bash

      enpm702_env
      code ~/ros2_ws

3. Press :kbd:`Ctrl+Shift+P` and run **ROS2: Update C++ Properties**. It
   writes ``.vscode/c_cpp_properties.json`` with "ROS installation paths",
   "Your workspace's package include directories" and "Appropriate compiler
   settings" (`the extension's IntelliSense page
   <https://raw.githubusercontent.com/Ranch-Hand-Robotics/rde-ros-2/main/docs/intellisense.md>`__).

4. The command sets the C++ standard to ``c++17`` for Jazzy, and the course
   compiles with C++20. In ``.vscode/c_cpp_properties.json``, change
   ``"cppStandard"`` to ``"c++20"``. The command keeps your value when you
   run it again.

5. Check it: open a ``.cpp`` file that includes ``<rclcpp/rclcpp.hpp>``. The
   include has no red underline, and :kbd:`Ctrl` + click on it opens the
   header. Run the command again after you add a package.


Gazebo (Simulation)
-------------------

Gazebo is the robot simulator of the ROS project, made by Open Robotics. The
Group Projects (GP1 and GP2) need it. ROS 2 Jazzy pairs with **Gazebo
Harmonic**, the version the `Gazebo installation guide for ROS
<https://gazebosim.org/docs/harmonic/ros_installation/>`__ recommends for
Jazzy. On Jazzy, Gazebo comes from the ROS 2 repository you added above, so
you do not add a separate Gazebo repository.

Each ROS 2 distribution has one recommended Gazebo version:

.. list-table::
   :header-rows: 1
   :widths: 22 18 25 35

   * - ROS 2 distribution
     - Ubuntu
     - Gazebo (recommended)
     - Command that starts Gazebo
   * - Humble Hawksbill
     - 22.04
     - Fortress (LTS)
     - ``ign gazebo``
   * - **Jazzy Jalisco (this course)**
     - 24.04
     - **Harmonic (LTS)**
     - ``gz sim``
   * - Kilted Kaiju
     - 24.04
     - Ionic
     - ``gz sim``
   * - Lyrical Luth
     - 26.04
     - Jetty (LTS)
     - ``gz sim``

The pairs come from the `ROS 2 and Gazebo compatibility table
<https://gazebosim.org/docs/latest/ros_installation/>`__ (checked November 6,
2026), which marks every other pair as possible with caution or not possible.
Fortress still uses the older command ``ign gazebo``; later versions use
``gz sim``.

1. Install Gazebo with ``ros_gz``, the packages that connect it to ROS 2:

   .. code-block:: bash

      sudo apt update
      sudo apt install ros-jazzy-ros-gz

2. Open a new terminal, so that ``~/.bashrc`` sources ROS 2, and check the
   version:

   .. code-block:: bash

      gz sim --version

   On the course laptop (November 6, 2026) it printed:

   .. code-block:: text

      Gazebo Sim, version 8.15.0

   Version 8 is Gazebo Harmonic. A later 8.x number is fine.

.. note::

   The ``gz`` command is installed inside ``/opt/ros/jazzy``. If the terminal
   says ``gz: command not found``, that terminal has not sourced
   ``/opt/ros/jazzy/setup.bash``: open a new terminal, or run the ``source``
   line yourself.


.. _setup-ros-jammy:

If Your Computer Has Ubuntu 22.04
---------------------------------

ROS 2 Jazzy has no packages for Ubuntu 22.04. On 22.04, install **ROS 2
Humble** and **Gazebo Fortress**, the pair recommended for Humble. The course
code is built and tested on Jazzy only: Humble may need changes, so move to
Ubuntu 24.04 when you can.

1. Do `Set Locale`_ and `Add the ROS 2 Repository`_ above as written. The
   ``ros2-apt-source`` command reads your Ubuntu version and adds the
   repository for 22.04.

2. If you skipped ``sudo apt upgrade`` above, run it now. On 22.04, installing ROS 2 on a system that was
   not upgraded can remove critical system packages (``systemd`` and ``udev``),
   as the `Humble installation guide
   <https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html>`__
   warns:

   .. code-block:: bash

      sudo apt update
      sudo apt upgrade

3. Install ROS 2 Humble, its development tools and Gazebo Fortress:

   .. code-block:: bash

      sudo apt install ros-humble-desktop ros-dev-tools
      sudo apt install ros-humble-ros-gz

4. In every command of this page and of the lectures, write ``humble`` where it
   says ``jazzy``. In ``~/.bashrc``, the last line of the ``enpm702_env`` block
   (see `Configure Your Shell`_) becomes:

   .. code-block:: bash

      enpm702_env humble

   Then do `ROS 2 Workspace`_ and `Verify ROS 2`_ above, with the same change.

5. Open a new terminal and start Gazebo Fortress with its demo world:

   .. code-block:: bash

      ign gazebo shapes.sdf

   A window opens with a few shapes. Close it to stop Gazebo.


Summary of Shell Configuration
-------------------------------

After completing the setup, the bottom of your ``~/.bashrc`` (or
``~/.zshrc``) holds the ``enpm702_env`` function and the line that runs it:

.. code-block:: bash

   enpm702_env() {
     ...
   }
   enpm702_env

With the manual alternative, it holds the three ``source`` lines instead,
never both.

.. tip::

   Two shortcuts for your shell configuration file:

   .. code-block:: bash

      alias cb='cd ~/ros2_ws && colcon build'
      alias cbs='cd ~/ros2_ws && colcon build && enpm702_env'
