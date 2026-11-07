====================================================
ROS 2 Development Environment
====================================================

.. _setup-ros:

ROS 2 is required starting in **Week 11** (Lecture 10). The instructions
below are for **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04**, the version the
course code is built and tested on.

Checklist
---------

Before the first ROS 2 lecture, do these five steps on your laptop. Each one
links to its section below.

1. Install ROS 2: from `Which ROS 2 Distribution`_ to `Install Development
   Tools`_. On Ubuntu 22.04, follow `If Your Computer Has Ubuntu 22.04`_.
2. Set up your terminal with ``enpm702_env``: `Configure Your Shell`_.
3. Build your workspace with the course code: `ROS 2 Workspace`_.
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
     - `Lyrical on Ubuntu <https://docs.ros.org/en/lyrical/Installation/Ubuntu-Install-Debs.html>`__

The dates come from the `ROS 2 distributions page
<https://docs.ros.org/en/jazzy/Releases.html>`__ and `REP 2000
<https://www.ros.org/reps/rep-2000.html>`__ (checked November 6, 2026).
An **LTS** (long-term support) distribution comes out in an even year and
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
   - ``~/ros2_ws/install/setup.bash`` puts your workspace in front of
     ``/opt/ros/jazzy`` in ``AMENT_PREFIX_PATH``, so ``ros2 run`` finds your
     packages too. This is why ROS 2 is sourced first and the workspace
     second: the workspace is the overlay, on top of ROS 2, the underlay.

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
   prints the line below. That is expected: we fix it in `ROS 2 Workspace`_,
   where you build the workspace.

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


ROS 2 Workspace
---------------

Create your workspace, put the course code in its ``src`` folder, build it,
then run ``enpm702_env`` so this terminal finds it:

.. code-block:: bash

   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws/src
   git clone https://github.com/zeidk/enpm702-fall-2026-ros.git
   cd ~/ros2_ws
   colcon build
   enpm702_env

``enpm702_env`` now prints:

.. code-block:: text

   enpm702_env: ROS 2 jazzy and the workspace /home/<you>/ros2_ws

With the manual alternative, run ``source install/setup.bash`` instead of
``enpm702_env``.


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
receiving them. Press ``Ctrl + C`` in both terminals to stop.


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

2. Update every package first. On 22.04, installing ROS 2 on a system that was
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

   You can add helpful aliases to your shell configuration file:

   .. code-block:: bash

      alias cb='cd ~/ros2_ws && colcon build'
      alias cbs='cd ~/ros2_ws && colcon build && enpm702_env'
