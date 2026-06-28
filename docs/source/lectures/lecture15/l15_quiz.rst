====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 15: Robot Autonomy
Architecture. Topics include the Sense-Plan-Act paradigm, mapping the
architecture onto ROS 2 nodes and communication patterns, where AI and
ML fit, C++ inference libraries, and reactive vs. deliberative vs. hybrid
architectures.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-10)
====================================================

.. admonition:: Question 1
   :class: hint

   What are the three stages of the Sense-Plan-Act paradigm?

   A. Sense, Store, Send

   B. Perceive, Decide, Act

   C. Read, Compute, Reset

   D. Detect, Display, Drive

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, Perceive, Decide, Act

   Sense-Plan-Act divides a robot's software into **perception**
   (turning sensor data into a description of the world), **planning/
   decision** (choosing what to do), and **action/control** (executing
   the decision on the actuators).


.. admonition:: Question 2
   :class: hint

   In an autonomy architecture mapped onto ROS 2, what does each "box"
   (layer) correspond to?

   A. A topic

   B. A node

   C. A parameter

   D. A package

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, A node

   Each layer of the architecture is implemented as a **node**, and the
   arrows between layers are **communication primitives** (topics,
   services, or actions).


.. admonition:: Question 3
   :class: hint

   Which layer of the architecture is usually referred to as the robot's
   "intelligence"?

   A. Perception

   B. Decision (planning)

   C. Control

   D. Actuation

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, Decision (planning)

   The decision layer chooses *what to do* given the current
   understanding of the world. This is where AI and ML are typically
   applied.


.. admonition:: Question 4
   :class: hint

   A robot must execute a long-running "navigate to waypoint" goal that
   provides continuous feedback and can be canceled. Which ROS 2
   communication pattern best fits this data flow?

   A. Topic

   B. Service

   C. Action

   D. Parameter

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, Action

   Actions are designed for long-running goals with feedback and the
   ability to cancel, exactly the profile of a navigation goal.


.. admonition:: Question 5
   :class: hint

   You replace a rule-based decision node with a trained neural-network
   policy, keeping the same input and output topics. What happens to the
   other nodes in the system?

   A. They must all be recompiled.

   B. They are unaffected.

   C. The control node must be rewritten.

   D. The perception node must publish a new message type.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, They are unaffected.

   Because the decision node keeps the same topic interface, the rest of
   the system does not change. This modularity is a central advantage of
   the architecture: intelligence is interchangeable.


.. admonition:: Question 6
   :class: hint

   Which of the following is a C++ library used to run a trained model
   for **inference** inside a ROS 2 node?

   A. Matplotlib

   B. ONNX Runtime

   C. colcon

   D. RViz2

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ONNX Runtime

   ONNX Runtime is a portable C++ inference engine. OpenCV DNN and
   LibTorch are other common choices. ``colcon`` is a build tool and
   RViz2 is a visualization tool.


.. admonition:: Question 7
   :class: hint

   A node maps the latest sensor reading directly to a motor command,
   with no internal world model. Which architectural style is this?

   A. Reactive

   B. Deliberative

   C. Hybrid

   D. Lifecycle

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**, Reactive

   A reactive architecture maps sensing directly to action without
   building or reasoning over a world model.


.. admonition:: Question 8
   :class: hint

   Which architectural style builds a world model and plans a sequence
   of actions to reach a goal?

   A. Reactive

   B. Deliberative

   C. Subsumption

   D. Open-loop

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, Deliberative

   A deliberative architecture constructs a model of the world and plans
   over it (for example, computing a path with A*) before acting.


.. admonition:: Question 9
   :class: hint

   Which ROS 2 framework provides a complete hybrid navigation
   architecture for mobile robots?

   A. Nav2

   B. Gazebo

   C. colcon

   D. ament_cmake

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**, Nav2

   Nav2 is the ROS 2 navigation stack: a hybrid architecture combining
   planning, control, and recovery behaviors. Gazebo is a simulator, and
   the others are build tools.


.. admonition:: Question 10
   :class: hint

   In the architecture, which ROS 2 feature is most appropriate for
   tuning a layer's behavior (e.g., a safe-distance threshold) without
   recompiling?

   A. Parameters

   B. Custom messages

   C. Lifecycle states

   D. Quality of Service

.. dropdown:: Answer
   :class-container: sd-border-success

   **A**, Parameters

   Parameters let you adjust values such as speeds and thresholds at
   launch or runtime without rebuilding the node.


----


True / False (Questions 11-15)
====================================================

.. admonition:: Question 11
   :class: hint

   **True or False**: Introducing an autonomy architecture requires new
   ROS 2 features beyond nodes, topics, services, actions, parameters,
   and launch files.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   An autonomy architecture is a *way of composing* the ROS 2 features
   you already know. It does not introduce new primitives.


.. admonition:: Question 12
   :class: hint

   **True or False**: AI and ML in a robotic system live primarily in
   the control (actuation) layer.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   AI and ML live primarily in the **perception and decision** layers.
   The control layer translates decisions into low-level actuator
   commands.


.. admonition:: Question 13
   :class: hint

   **True or False**: A learned (ML) decision policy and a rule-based
   decision policy can expose the same ROS 2 topic interface.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Both are just nodes that subscribe to the same input topic and
   publish to the same output topic. This is why the decision layer's
   implementation is interchangeable.


.. admonition:: Question 14
   :class: hint

   **True or False**: Most real-world robots use a purely reactive
   architecture.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Most real robots use a **hybrid** (three-layer) architecture that
   combines a fast reactive layer with a slower deliberative planner.


.. admonition:: Question 15
   :class: hint

   **True or False**: Neural-network models used on robots are typically
   trained inside the ROS 2 node at runtime.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Models are typically **trained offline** (often in Python), exported,
   and then loaded for **inference** in a C++ ROS 2 node using a library
   such as OpenCV DNN, ONNX Runtime, or LibTorch.
