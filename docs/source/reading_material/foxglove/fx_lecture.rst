====================================================
Lecture
====================================================


.. note::

   **Where the outputs come from.** The bridge start-up lines and the topic
   list on this page come from a real run on ROS 2 Jazzy: the ROSbot
   simulation of GP2 and ``foxglove_bridge`` 3.6.0, each started on its own.
   The statements about Foxglove's own program come from Foxglove's
   documentation, linked in the references.


What Foxglove Is
====================================================

In the lectures you looked at topics with ``ros2 topic list`` and
``ros2 topic echo``. Those commands print text. A robot also publishes a
camera image, a laser scan and a model of its body, and text is a poor way
to see those.

Foxglove's documentation describes Foxglove as "a platform to record,
upload, organize, and visualize multimodal log data", most often used in
hardware and robotics. In this course you use one part of it: the **Foxglove
app**, a program that opens a connection to a running robot and shows its
topics in **panels**. A panel is one window of the app, such as a 3D view or
a plot. A set of panels and their arrangement is a **layout**.

.. admonition:: Definition
   :class: definition

   **Foxglove** is a visualization program for robot data. You connect it to
   a running ROS 2 system and arrange panels (a 3D view, an image, a plot,
   the raw messages) to see the topics.

The app does not speak ROS 2 itself. A ROS 2 node called the **Foxglove
bridge** sits between the two. The bridge's README describes it as a "High
performance ROS 2 WebSocket bridge", and Foxglove's ROS 2 guide says that it
"will automatically subscribe to all topics in your ROS system and make them
available for live visualization". A WebSocket is a network connection that
stays open, so the bridge can keep sending new messages. The bridge listens
on port 8765 unless you change it (the ``port`` launch argument, which
defaults to ``8765`` in the README and in the launch file installed with the
package).

.. code-block:: text

   ROSbot simulation  -->  Foxglove bridge  -->  WebSocket, port 8765  -->  Foxglove app
   (ROS 2 topics)          (a ROS 2 node)                                   (panels)

.. important::

   **Foxglove is optional.** No assignment, quiz or exam needs it, and GP2
   uses only what the lectures teach. Try it if you want to see your topics
   drawn instead of printed.


Install
====================================================

You install two things: the bridge, on the computer that runs ROS 2, and the
app, on the computer where you want to look at the data. On your course
setup, both are the same computer.

The Bridge
----------------------------------------------------

The bridge is a ROS 2 package. Foxglove's guide installs it with apt. For
Jazzy, the package name is ``ros-jazzy-foxglove-bridge``:

.. code-block:: bash

   sudo apt update
   sudo apt install ros-jazzy-foxglove-bridge

Check the install. This command prints the path of the package when it is
installed:

.. code-block:: bash

   source /opt/ros/jazzy/setup.bash
   ros2 pkg prefix foxglove_bridge

On the course computer, it printed ``/opt/ros/jazzy``, and ``dpkg`` listed
``ros-jazzy-foxglove-bridge`` at version 3.6.0.

The App
----------------------------------------------------

The app comes in two forms. Foxglove's documentation says that the desktop
app runs on Linux, Windows and macOS, and that the web app runs in Chrome
(version 130 or later). It also says that some features only exist in the
desktop app, such as loading a local URDF and its meshes in the 3D panel.

.. list-table::
   :header-rows: 1
   :widths: 18 40 42
   :class: compact-table

   * - Form
     - Where to get it
     - Notes
   * - Desktop app
     - `foxglove.dev/download <https://foxglove.dev/download>`__
     - On Linux, a ``.deb`` package for Ubuntu or Debian-based systems:
       ``sudo apt install ./foxglove-studio-*.deb`` (run it in the folder of
       the download). Windows has an installer and macOS has a ``.dmg``.
   * - Web app
     - `app.foxglove.dev <https://app.foxglove.dev>`__ in Chrome
     - Nothing to install.

Foxglove's ROS 2 guide lists "Create a free Foxglove account" among the
prerequisites, next to downloading the desktop app or using the web app. The
documentation pages that this reading used do not say whether a connection
to a local robot works without signing in. If the app asks you to sign in,
create the free account.

.. note::

   Foxglove changes its app and its documentation often. If a menu on your
   screen has another name than the one on this page, follow the current
   documentation, linked in the references.


Run It with the Course Simulation
====================================================

Use two terminals, each with ROS 2 sourced (``enpm702_env``), as in
:doc:`ROSbot Simulation </setup/rosbot_simulation>`.

Step 1: Start the Simulation
----------------------------------------------------

.. code-block:: bash

   ros2 launch gp2_bringup gp2_sim.launch.py

The simulation needs about 40 s to start the first time. Leave this terminal
open.

Step 2: Start the Bridge
----------------------------------------------------

In a second terminal:

.. code-block:: bash

   ros2 launch foxglove_bridge foxglove_bridge_launch.xml

The bridge prints that it started and which topics it offers. These are
lines from a real run:

.. code-block:: text

   [foxglove_bridge-1] [INFO] [foxglove_bridge]: Starting foxglove_bridge (jazzy, 3.6.0@)
   [foxglove_bridge-1] [INFO] [foxglove_bridge]: Server listening on port 8765
   [foxglove_bridge-1] [INFO] [foxglove_bridge]: Advertising new channel 6 for topic "/scan_filtered"
   [foxglove_bridge-1] [INFO] [foxglove_bridge]: Advertising new channel 8 for topic "/robot_description"
   [foxglove_bridge-1] [INFO] [foxglove_bridge]: Advertising new channel 13 for topic "/oak/rgb/color"

The bridge calls each topic a *channel*. In that run, it advertised 32
channels: the 31 topics that ``ros2 topic list`` showed, plus its own
``/foxglove_bridge/sysinfo``.

Step 3: Open a Connection in Foxglove
----------------------------------------------------

Foxglove's guide gives these steps. Start the app, then:

1. Select **Open connection** from the dashboard or the left-hand menu.
2. In the **Open a new connection** dialog, select **Foxglove WebSocket**.
3. Enter the URL ``ws://localhost:8765``. The guide says to use this URL when
   the server runs on the same machine as Foxglove.
4. Click **Open**.

If your browser asks to allow access to the local network, click **Allow**,
or the connection fails.

Step 4: Load the Layout
----------------------------------------------------

Download the layout file:
:download:`rosbot_sim_layout.json </_static/files/foxglove/rosbot_sim_layout.json>`.

Foxglove's documentation says to use "the Layouts menu's 'Import from file...'
option to load an exported layout JSON file". Open the Layouts menu in the
app, choose that option, and select the file. The window then shows the four
panels described next.

Stop the bridge and the simulation with :kbd:`Ctrl+C` in their terminals.


The Layout and Its Panels
====================================================

The layout file is a JSON file that Foxglove writes when you export a layout
and reads when you import one. It lists the panels, the settings of each
one, and how the window is split. The course layout has four panels:

.. list-table::
   :header-rows: 1
   :widths: 16 34 50
   :class: compact-table

   * - Panel
     - Topics it uses
     - What it shows
   * - 3D
     - ``/robot_description``, ``/tf``, ``/scan_filtered``
     - The ROSbot's body, drawn from its description, and the laser scan as
       points around it. The display frame is ``odom``, so the view follows
       the ``odom`` frame.
   * - Image
     - ``/oak/rgb/color``
     - The picture from the robot's color camera.
   * - Plot
     - ``/odometry/filtered``
     - Two lines against time: ``twist.twist.linear.x`` (the forward speed,
       in m/s) and ``twist.twist.angular.z`` (the turn rate, in rad/s).
   * - Raw Messages
     - ``/odometry/filtered``
     - The latest ``nav_msgs/msg/Odometry`` message, field by field.

Every one of these topics is in the topic list of the simulation (``ros2 topic
list -t``), with the types the panels expect. For the messages themselves, see
:doc:`/reading_material/robot_messages/rmsg_index`.

The 3D Panel
----------------------------------------------------

The panel draws the robot from ``/robot_description``, the topic that holds
the robot's URDF (the file that describes its links and joints). It places
each link with the transforms of ``/tf``, and it draws ``/scan_filtered`` as
points. Foxglove's documentation describes the display frame as "the coordinate
frame the camera follows". Drive the robot (for example with
``ros2 topic pub`` on ``/cmd_vel``, or your GP2 nodes) and the robot moves
through the scene.

The Image Panel
----------------------------------------------------

The panel shows each image message of ``/oak/rgb/color`` as it arrives.

The Plot Panel
----------------------------------------------------

Each line is one *message path*: a topic name, then the names of the fields
to reach the number, separated by dots. The two paths are
``/odometry/filtered.twist.twist.linear.x`` and
``/odometry/filtered.twist.twist.angular.z``. Command a turn and watch the
second line rise.

The Raw Messages Panel
----------------------------------------------------

The panel prints the newest ``/odometry/filtered`` message. It is the same
text that ``ros2 topic echo`` prints, with each field you can open and close.

Edit the Layout
----------------------------------------------------

Click a panel's settings to change its topic, and use the Layouts menu to
export your own version. Add a panel for another topic the same way: for
example, point the Image panel at ``/patrol_cam/image`` to see the patrol
camera.
