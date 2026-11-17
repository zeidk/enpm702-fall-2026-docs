====================================================
Quiz
====================================================

This quiz covers :doc:`sa_lecture`: services, actions, the ``.srv`` and ``.action`` files, the callbacks of a server and a client, and the command-line tools. It is not graded.

.. note::

   Each multiple choice question has one correct answer. Open the dropdown after a question to read the answer.

----

Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   Which pattern fits the job "ask for the fare of one ride, once"?

   a) Topic
   b) Service
   c) Action
   d) Parameter

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Service**

      A service answers one request with one response. A topic would keep sending data to every subscriber, and an action is for a task that takes time.


.. admonition:: Question 2
   :class: hint

   In a ``.srv`` file, what separates the request from the response?

   a) ``===``
   b) ``---``
   c) ``***``
   d) A blank line

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)** ``---``

      A line of three dashes. The request is above it and the response is below it.


.. admonition:: Question 3
   :class: hint

   How many ``---`` lines does an ``.action`` file have, and in which order are its parts?

   a) One: goal, then result
   b) Two: goal, result, feedback
   c) Two: goal, feedback, result
   d) Three: goal, result, feedback, status

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Two: goal, result, feedback**

      Two lines make three parts: the goal, the result and the feedback, as in ``Drive.action`` of the lecture.


.. admonition:: Question 4
   :class: hint

   Which method sends a service request from a client in ``rclcpp`` and returns at once?

   a) ``send_request()``
   b) ``call_service()``
   c) ``async_send_request()``
   d) ``request_service()``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c)** ``async_send_request()``

      ``async_send_request()`` returns at once. The executor calls the callback you passed when the response arrives.


.. admonition:: Question 5
   :class: hint

   Which of the three callbacks of ``rclcpp_action::create_server`` returns ``ACCEPT_AND_EXECUTE`` or ``REJECT``?

   a) The cancel callback
   b) The accepted callback
   c) The goal callback
   d) ``execute``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) The goal callback**

      The goal callback decides whether the server takes the goal. The cancel callback answers a cancel request, and the accepted callback runs after the goal is accepted. ``execute`` is not a callback of ``create_server``: the accepted callback starts it.


.. admonition:: Question 6
   :class: hint

   Why does the accepted callback of ``drive_node`` start ``execute`` in a thread?

   a) Because ``execute`` must run on a second computer
   b) Because a loop of seconds inside the callback would keep the executor from calling any other callback, the cancel callback included
   c) Because ROS 2 forbids loops in callbacks
   d) Because a thread makes the robotaxi drive faster

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Because a loop of seconds inside the callback would keep the executor from calling any other callback, the cancel callback included**

      The executor calls one callback at a time. A loop in the accepted callback would hold it, so a cancel request would wait until the loop ended.


.. admonition:: Question 7
   :class: hint

   Which call sends feedback from an action server?

   a) ``goal_handle->send_feedback()``
   b) ``goal_handle->publish_feedback()``
   c) ``goal_handle->update()``
   d) ``goal_handle->notify()``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)** ``goal_handle->publish_feedback()``

      ``publish_feedback()`` on the goal handle sends the feedback message to the client.


.. admonition:: Question 8
   :class: hint

   Which command calls a service from the terminal?

   a) ``ros2 service send``
   b) ``ros2 service request``
   c) ``ros2 service call``
   d) ``ros2 service invoke``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c)** ``ros2 service call``

      ``ros2 service call <name> <type> "<request>"`` sends a request and prints the response.


.. admonition:: Question 9
   :class: hint

   What does ``--feedback`` do in ``ros2 action send_goal``?

   a) It makes the action synchronous
   b) It prints each feedback message while the goal runs
   c) It sends extra data with the goal
   d) It turns on verbose logging in the server

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) It prints each feedback message while the goal runs**

      With it, the command also prints each feedback message, as in the lecture's run with a ``target_x`` of 4 m.


.. admonition:: Question 10
   :class: hint

   Which package must an action server or client list as a dependency in C++?

   a) ``rclcpp_components``
   b) ``rclcpp_action``
   c) ``action_msgs``
   d) ``rosidl_default_generators``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)** ``rclcpp_action``

      ``rclcpp_action`` provides ``create_server`` and ``create_client``. It goes in ``find_package`` and in ``package.xml``.


.. admonition:: Question 11
   :class: hint

   Which of these are values of ``rclcpp_action::ResultCode`` that say how an accepted goal ended?

   a) ``OK``, ``FAILED``, ``TIMEOUT``
   b) ``SUCCEEDED``, ``CANCELED``, ``ABORTED``
   c) ``ACCEPTED``, ``REJECTED``, ``DONE``
   d) ``START``, ``RUN``, ``STOP``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)** ``SUCCEEDED``, ``CANCELED``, ``ABORTED``

      ``SUCCEEDED``, ``CANCELED`` and ``ABORTED`` are values of ``rclcpp_action::ResultCode``, which also has ``UNKNOWN``. A goal that the server rejects never reaches the result callback: the goal response callback gets an empty pointer.


----

True or False
=============

.. admonition:: Question 12
   :class: hint

   **True or false:** A service callback that works for 30 s is fine, because the client keeps working meanwhile.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      A service callback keeps the executor busy while it works, and the client waits for the response. Work that takes seconds belongs in an action.


.. admonition:: Question 13
   :class: hint

   **True or false:** An action client can cancel a goal that the server is executing.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      The client sends a cancel request. The server's cancel callback answers it, and ``execute`` ends the goal with ``canceled``.


.. admonition:: Question 14
   :class: hint

   **True or false:** The ``---`` line of a ``.srv`` file is optional when the response is empty.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False**

      The line is always there. ``std_srvs/srv/Empty`` is only the line ``---``, with nothing on either side.


.. admonition:: Question 15
   :class: hint

   **True or false:** An action is built from services and topics.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      ``ros2 service list --include-hidden-services`` shows ``drive/_action/send_goal``, ``cancel_goal`` and ``get_result``, and ``ros2 topic list --include-hidden-topics`` shows ``drive/_action/feedback`` and ``status``.


.. admonition:: Question 16
   :class: hint

   **True or false:** A timeout counted with ``now()`` on the node follows the simulation when ``use_sim_time`` is true.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True**

      ``now()`` reads the node's clock. With ``use_sim_time`` true, that clock is the simulation time.

