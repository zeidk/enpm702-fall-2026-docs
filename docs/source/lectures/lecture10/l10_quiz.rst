====================================================
Quiz
====================================================

The questions cover the four rules of a topic, running and inspecting nodes, the build files of a package, spinning, messages, and the robotaxi's publisher and subscriber.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 10)
====================================================

.. admonition:: Question 1
   :class: hint

   The robotaxi publishes on ``/robotaxi/position``. The dispatcher subscribes to ``/robotaxi/pose``, with the same message type. Both run. What happens?

   A. The dispatcher receives every position.

   B. The dispatcher receives nothing, and ROS 2 prints an error.

   C. The dispatcher receives nothing, and no error is printed.

   D. The robotaxi stops publishing until a subscriber matches.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   Rule 1: a publisher and a subscriber connect only when they use the same topic name. The robotaxi goes on publishing (rule 3).


.. admonition:: Question 2
   :class: hint

   You start the talker, then the listener 1 s later. The listener's first line is ``I heard: [Hello World: 2]``. Why not message 1?

   A. The listener drops the first message of every topic.

   B. Message 1 was sent before the listener started, and nothing kept it for the listener.

   C. The talker sends message 1 only to ``ros2 topic echo``.

   D. The listener's queue size is 1.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   Rule 3: a publisher does not wait for subscribers. With the default durability (volatile), it keeps nothing for a subscriber that joins late.


.. admonition:: Question 3
   :class: hint

   Which command counts the publishers and the subscribers of the topic ``/chatter``?

   A. ``ros2 topic echo /chatter``

   B. ``ros2 topic hz /chatter``

   C. ``ros2 topic info /chatter``

   D. ``ros2 node list``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   ``ros2 topic info /chatter`` printed ``Publisher count: 1`` and ``Subscription count: 1``. ``echo`` prints each message, ``hz`` measures messages per second, and ``ros2 node list`` lists the nodes.


.. admonition:: Question 4
   :class: hint

   The robotaxi publishes every 0.5 s. The dispatcher's callback takes 100 ms. What fraction of the time is the dispatcher busy?

   A. 5%

   B. 20%

   C. 50%

   D. 100%

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The callback is busy 100 ms of every 500 ms: 100 / 500 = 20% of the time (scenario 2). It handles each message at once and waits 400 ms for the next.


.. admonition:: Question 5
   :class: hint

   The dispatcher's pickup point is at x = 10 m, y = 0 m. You send it ``{x: 4.0, y: 8.0}`` with ``ros2 topic pub``. What does it print?

   A. ``RoboTaxi at x = 4, 6 m from the pickup``

   B. ``RoboTaxi at x = 4, 8 m from the pickup``

   C. ``RoboTaxi at x = 4, 10 m from the pickup``

   D. ``RoboTaxi at x = 4, 14 m from the pickup``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   ``std::hypot(10.0 - 4.0, 0.0 - 8.0)``:

   1. The robotaxi is 10 − 4 = 6 m short of the pickup point in x, and 8 m away from it in y.
   2. 6\ :sup:`2` + 8\ :sup:`2` = 36 + 64 = 100.
   3. The square root of 100 is 10.


.. admonition:: Question 6
   :class: hint

   A node makes a timer with ``create_wall_timer`` in its constructor, but keeps it in a local variable, not in a data member. What happens?

   A. The timer runs as usual.

   B. The timer runs once, then stops.

   C. The timer is destroyed at the end of the constructor, and its callback never runs.

   D. The program does not compile.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**

   ``create_wall_timer`` returns a ``std::shared_ptr``. When the local variable goes out of scope at the end of the constructor, the timer is destroyed. A test node with such a timer printed nothing in 1.5 s. Store the timer in a data member, as ``timer_`` in ``RoboTaxiNode``.


.. admonition:: Question 7
   :class: hint

   You want to use the message type ``geometry_msgs/msg/Point`` in C++. Which header and which class?

   A. ``<geometry_msgs/Point.h>`` and ``geometry_msgs::Point``

   B. ``<geometry_msgs/msg/point.hpp>`` and ``geometry_msgs::msg::Point``

   C. ``<geometry_msgs/msg/Point.hpp>`` and ``geometry_msgs/msg/Point``

   D. ``<rclcpp/point.hpp>`` and ``rclcpp::Point``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The header's name is the type's name in snake_case, ``point.hpp``, under ``<package>/msg/``. The C++ class name replaces each ``/`` with ``::``.


.. admonition:: Question 8
   :class: hint

   The ``install`` line is missing from ``CMakeLists.txt`` for a node, and the package builds. What does ``ros2 run`` print for that node?

   A. ``Package 'robotaxi_demo' not found``

   B. ``No executable found``

   C. Nothing: the node runs from ``build``.

   D. A compiler error.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   ``install`` copies each executable to ``lib/${PROJECT_NAME}`` in the ``install`` folder, where ``ros2 run`` looks for it. With no ``add_executable`` or ``install`` line, ``ros2 run`` prints ``No executable found``. ``Package 'robotaxi_demo' not found`` is the symptom of a terminal that did not source ``install/setup.bash``.


.. admonition:: Question 9
   :class: hint

   ``main`` makes a ``RoboTaxiNode`` (the first version, which only logs a line) but never calls ``rclcpp::spin``. What happens when you run it?

   A. The node logs its first line, and the program ends.

   B. The node runs until :kbd:`Ctrl+C`.

   C. The program does not compile.

   D. The node logs nothing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**

   The constructor logs the line, then ``main`` goes on to ``rclcpp::shutdown`` and returns: in the lecture, after 0.3 s. No callback ever runs.


.. admonition:: Question 10
   :class: hint

   In scenario 3, the dispatcher keeps a queue of 3 and spends 1.7 s in each callback. The robotaxi publishes every 0.5 s. While one callback runs, x = 7, 8, 9 and 10 arrive. What happens to x = 7?

   A. It waits, and the dispatcher handles it next.

   B. It is pushed out of the queue by x = 10 and never handled.

   C. The robotaxi sends it again later.

   D. The dispatcher handles it at the same time as x = 8.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**

   The queue keeps the last 3 messages. When x = 10 arrives, the queue holds 8, 9 and 10, so x = 7 is dropped. The next callback takes x = 8. In 11 s, the dispatcher handled 7 of the 23 positions.


----


True or False (Questions 11 to 14)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False:** A publisher waits until a subscriber connects before it publishes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Rule 3: the robotaxi publishes every 0.5 s, whether or not a node listens; with no subscriber, each message reaches no one (scenario 1).


.. admonition:: Question 12
   :class: hint

   **True or False:** The dispatcher can start before the robotaxi.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Rule 4: a subscriber does not need a publisher. The dispatcher waits, with no error, and its callback runs once a robotaxi starts publishing.


.. admonition:: Question 13
   :class: hint

   **True or False:** A publisher of ``geometry_msgs/msg/Point`` and a subscriber of ``std_msgs/msg/String`` on the same topic name connect, and the subscriber receives the messages.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Rule 2: a publisher and a subscriber connect only when the message type is the same.


.. admonition:: Question 14
   :class: hint

   **True or False:** ``rclcpp::spin(node)`` runs several callbacks at the same time, each on its own thread.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``rclcpp::spin(node)`` uses the single-threaded executor: one callback at a time, on the main thread. A slow callback delays the others.
