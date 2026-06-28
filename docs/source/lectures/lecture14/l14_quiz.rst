====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 14: Lifecycle Nodes.
Topics include the lifecycle state machine, primary states, transitions,
transition callbacks, ``CallbackReturn`` values, and ``LifecyclePublisher``
behavior.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-5)
====================================================

.. admonition:: Question 1
   :class: hint

   What are the four **primary states** of a lifecycle node?

   A. Created, Running, Paused, Destroyed

   B. Unconfigured, Inactive, Active, Finalized

   C. Initialized, Configured, Active, Shutdown

   D. Starting, Ready, Running, Stopped

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, Unconfigured, Inactive, Active, Finalized

   The lifecycle state machine defines four primary states:
   **Unconfigured** (initial), **Inactive** (configured but not
   processing), **Active** (fully operational), and **Finalized**
   (terminal, cannot be restarted).


.. admonition:: Question 2
   :class: hint

   Which transition moves a lifecycle node from the **Unconfigured**
   state to the **Inactive** state?

   A. ``activate``

   B. ``configure``

   C. ``cleanup``

   D. ``shutdown``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``configure``

   The ``configure`` transition takes a lifecycle node from
   **Unconfigured** to **Inactive**. During this transition, the
   ``on_configure()`` callback is executed.


.. admonition:: Question 3
   :class: hint

   What happens when a lifecycle transition callback returns
   ``CallbackReturn::ERROR``?

   A. The node stays in the current state.

   B. The node transitions to the Finalized state.

   C. The node transitions to the ErrorProcessing state.

   D. The transition is retried automatically.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, The node transitions to the ErrorProcessing state.

   Returning ``ERROR`` indicates a critical failure. The node enters the
   **ErrorProcessing** state, where the ``on_error()`` callback is
   invoked if implemented. Returning ``FAILURE`` keeps the node in (or
   returns it to) the previous primary state.


.. admonition:: Question 4
   :class: hint

   Which base class must you inherit from to create a lifecycle node?

   A. ``rclcpp::Node``

   B. ``rclcpp_lifecycle::LifecycleNode``

   C. ``rclcpp::ManagedNode``

   D. ``rclcpp_lifecycle::StateMachineNode``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``rclcpp_lifecycle::LifecycleNode``

   To create a lifecycle node in C++, inherit from
   ``rclcpp_lifecycle::LifecycleNode`` instead of ``rclcpp::Node``.
   This gives you access to the lifecycle state machine and the
   transition callbacks.


.. admonition:: Question 5
   :class: hint

   What does a ``LifecyclePublisher`` do when you call ``publish()``
   and the node is in the **Inactive** state?

   A. It publishes the message normally.

   B. It throws an exception.

   C. It silently drops the message.

   D. It buffers the message until the node is activated.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, It silently drops the message.

   A ``LifecyclePublisher`` only transmits messages when the node is in
   the **Active** state. In any other state, calls to ``publish()``
   are silently ignored.


----


True / False (Questions 6-7)
====================================================

.. admonition:: Question 6
   :class: hint

   **True or False**: The ``cleanup`` transition moves a lifecycle node
   from the **Inactive** state back to the **Unconfigured** state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The ``cleanup`` transition takes a node from **Inactive** back to
   **Unconfigured**, invoking the ``on_cleanup()`` callback. This
   allows the node to release resources and be reconfigured.


.. admonition:: Question 7
   :class: hint

   **True or False**: You can trigger a ``shutdown`` transition only
   from the **Active** state.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``shutdown`` transition can be triggered from any primary state
   except **Finalized**. It can be called from **Unconfigured**,
   **Inactive**, or **Active**, and it always transitions the node to
   the **Finalized** state.
