References
==========


.. dropdown:: Lecture 15
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L15: Robot Autonomy Architecture**

        A capstone lecture showing how the ROS 2 building blocks compose
        into an autonomy architecture. Covers the Sense-Plan-Act
        paradigm, mapping perception/decision/control layers onto ROS 2
        nodes and communication patterns, where Artificial Intelligence
        and Machine Learning fit (the decision and perception layers),
        the interchangeability of rule-based and learned policies behind
        a shared topic interface, C++ inference libraries (OpenCV DNN,
        ONNX Runtime, LibTorch), and reactive vs. deliberative vs. hybrid
        architectures (Nav2, BehaviorTree.CPP).

        **This is the final lecture.** The advanced ROS 2 capabilities
        that support this architecture (TF2 and lifecycle nodes) are
        covered in Lectures 13 and 14.


.. dropdown:: Autonomy Architectures
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ROS 2 Concepts
            :link: https://docs.ros.org/en/jazzy/Concepts.html
            :class-card: sd-border-secondary

            **ROS 2 Jazzy: Concepts**

            Reference for the core ROS 2 building blocks that an autonomy
            architecture composes: nodes, topics, services, actions,
            parameters, and launch.

            +++

            - Nodes and the discovery graph
            - Topics, services, and actions
            - Parameters and launch

        .. grid-item-card:: Sense-Plan-Act
            :link: https://en.wikipedia.org/wiki/Sense_plan_act
            :class-card: sd-border-secondary

            **Sense-Plan-Act Paradigm**

            Background on the classical robotics control paradigm and the
            reactive, deliberative, and hybrid architectures that build
            on it.

            +++

            - The perception/planning/control loop
            - Reactive vs. deliberative control
            - Hybrid (three-layer) architectures


.. dropdown:: Decision-Making Frameworks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Nav2
            :link: https://docs.nav2.org/
            :class-card: sd-border-secondary

            **Nav2: The ROS 2 Navigation Stack**

            A complete hybrid autonomy architecture for mobile robots,
            integrating planning, control, and recovery behaviors.

            +++

            - Planner, controller, and behavior servers
            - Costmaps and recovery behaviors
            - Behavior-tree-based navigation logic

        .. grid-item-card:: BehaviorTree.CPP
            :link: https://www.behaviortree.dev/
            :class-card: sd-border-secondary

            **BehaviorTree.CPP**

            A C++ library for structuring complex robot decision-making
            as behavior trees; used as the decision layer inside Nav2.

            +++

            - Behavior tree concepts
            - Nodes, sequences, and fallbacks
            - Integration with ROS 2


.. dropdown:: C++ Model Inference
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: ONNX Runtime (C++)
            :link: https://onnxruntime.ai/docs/get-started/with-cpp.html
            :class-card: sd-border-secondary

            **ONNX Runtime: C++ API**

            A portable C++ inference engine for running models exported
            to the ONNX format inside a ROS 2 node.

            +++

            - Loading an ONNX model
            - Running inference in C++
            - Cross-platform deployment

        .. grid-item-card:: LibTorch
            :link: https://pytorch.org/cppdocs/
            :class-card: sd-border-secondary

            **LibTorch: PyTorch C++ API**

            The C++ distribution of PyTorch, used to load and run trained
            models for inference in C++.

            +++

            - Loading a TorchScript model
            - Tensor operations in C++
            - Inference from C++

        .. grid-item-card:: OpenCV DNN
            :link: https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html
            :class-card: sd-border-secondary

            **OpenCV: Deep Neural Network module**

            Run common vision models (classification, detection) directly
            from OpenCV in C++, a convenient option for perception nodes.

            +++

            - Loading models from various frameworks
            - Image classification and detection
            - Forward inference in C++
