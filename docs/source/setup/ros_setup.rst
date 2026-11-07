====================================================
ROS 2 Development Environment
====================================================

.. _setup-ros:

ROS 2 is required starting in **Week 10**. The instructions below are
for **ROS 2 Jazzy Jalisco** on **Ubuntu 24.04**, the version the course
code is built and tested on.


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
   commands and the Group Projects use it. With another distribution,
   replace ``jazzy`` with its name in every command on this page (for
   example ``ros-humble-desktop`` and ``/opt/ros/humble``), and expect
   some lecture code to need changes.


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

Add the ROS 2 setup script to your shell configuration file so that
ROS 2 is available in every new terminal session.

**For Bash users** (``~/.bashrc``):

.. code-block:: bash

   echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
   source ~/.bashrc

**For Zsh users** (``~/.zshrc``):

.. code-block:: bash

   echo "source /opt/ros/jazzy/setup.zsh" >> ~/.zshrc
   source ~/.zshrc

Verify the installation:

.. code-block:: bash

   ros2 --help

.. warning::

   You must source the setup file in **every terminal** you use for
   ROS 2 development. Adding it to your shell configuration file
   automates this.


Configure colcon
^^^^^^^^^^^^^^^^

``colcon`` is the build tool used for ROS 2 workspaces. Add
autocompletion to your shell:

**For Bash users:**

.. code-block:: bash

   echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

**For Zsh users:**

.. code-block:: bash

   echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.zsh" >> ~/.zshrc


ROS 2 Workspace
---------------

Create and build a ROS 2 workspace:

.. code-block:: bash

   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   colcon build
   source install/setup.bash

Add the workspace overlay to your shell configuration file:

**For Bash users:**

.. code-block:: bash

   echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

**For Zsh users:**

.. code-block:: bash

   echo "source ~/ros2_ws/install/setup.zsh" >> ~/.zshrc

.. note::

   After making changes to your ``~/.bashrc`` or ``~/.zshrc``, either
   open a new terminal or run ``source ~/.bashrc`` (or ``source
   ~/.zshrc``) to apply the changes.


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


Summary of Shell Configuration
-------------------------------

After completing the setup, your ``~/.bashrc`` (or ``~/.zshrc``)
should contain these lines at the bottom:

.. code-block:: bash

   # ROS 2 Jazzy
   source /opt/ros/jazzy/setup.bash

   # colcon autocompletion
   source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash

   # ROS 2 workspace overlay
   source ~/ros2_ws/install/setup.bash

.. tip::

   You can add helpful aliases to your shell configuration file:

   .. code-block:: bash

      alias cb='cd ~/ros2_ws && colcon build'
      alias cbs='cd ~/ros2_ws && colcon build && source install/setup.bash'
      alias sw='source ~/ros2_ws/install/setup.bash'
