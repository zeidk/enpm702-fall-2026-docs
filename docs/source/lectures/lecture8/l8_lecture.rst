====================================================
Lecture
====================================================

Learning Objectives
-------------------

1. Say when a type should be a ``class`` and when a ``struct``, from its invariant.
2. Write a class with ``private`` data members and ``public`` methods, in a header and a source file.
3. Write accessors and mutators that keep the invariant, with ``const``, ``[[nodiscard]]`` and ``noexcept`` where each one is true.
4. Construct objects with constructors and member initializer lists, and mark a constructor ``explicit``.
5. Say when an object's destructor runs.
6. Use members that give back their own memory, such as ``std::unique_ptr``, so a class needs no destructor of its own.
7. Use the ``this`` pointer.

We write one ``Vehicle`` in five Live Coding steps: Step 1 together (`Live Coding: Step 1`_), Steps 2 to 5 on your own. The `Further Reading`_ part, at the end of this page, is the appendix of the slides. It is not presented. Read it on your own.

Upload Your Live Coding
-----------------------

You type Step 1 with me, in ``project/week8/live``. You write **Steps 2 to 5** on your own, in the time each step gives: 5 minutes for Step 2, 15 for Step 5, 10 for Steps 3 and 4. In class, I walk around and help, but I do not show the answers: the recording would give them away.

- **Before the end of class**, upload ``vehicle.hpp``, ``vehicle.cpp`` and ``main.cpp`` to the L8 Live Coding assignment on Canvas.
- It counts as the L8 exercise (exercises are **5%** of the grade). Class reached Step 4, so it is scored on Steps 2 to 4, 4 points each, out of 12 and scaled to 20. A step earns its points when you wrote it, whether or not the code builds, and part of them when you wrote part of it. Step 5 gets feedback but no points. The upload is not graded for correctness.
- **No AI**: write the code yourself, with neither a chatbot nor the AI in VS Code (Copilot included). Code written with AI gets **0**.
- **Watching the recording?** Upload before the next lecture, on **Nov 3**. The same rules apply.
- The finished code is posted after Nov 3.

:doc:`Setup Before Class <l8_setup>` gets your workspace ready for the Live Coding.

The Program We Will Build
-------------------------

In L8 and L9 we write the ride service program, for a fleet of cars that carry passengers.

- A **Fleet** holds many vehicles. Each one is a **Vehicle**.
- A **Passenger** rides at most one **Vehicle** at a time.
- Each **Vehicle** owns its sensors. Each sensor is a **Sensor**, and its kind is a **SensorType**, an enumeration: lidar, camera or radar.
- A **Vehicle** drives along a **Route**, which holds the points to visit. Each point is a **Position**, a ``struct`` with x and y.
- A **RoboTaxi** drives itself, and a **Taxi** has a driver. Both are kinds of **Vehicle**.

L8 builds **Vehicle**, **Sensor**, **SensorType** and **Position**. **Route** is ready in the course code. L9 builds the rest.

Each bold word is a type we write: a class, the struct ``Position``, or the enumeration ``SensorType``. When you read a problem statement, the nouns that keep data and rules become these types.

The Class Diagram
^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/model_l8_members.png
   :alt: A UML class diagram of the ride service program with nine boxes, each listing its data members and methods. In the middle, Vehicle, purple, with the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor &, plus drive(const Route&) : void, the underlined plus get_next_id() : int, and the protected hash log_event(const string&) : void. On the left, grey: Fleet with plus add(shared_ptr of Vehicle) : void, plus remove(int) : bool, plus size() : size_t; a line labeled holds with an open diamond at Fleet joins it to Vehicle, 1 to 0..*, the Vehicle end named minus vehicles_. Below it, Passenger with minus name_ : string, plus board(shared_ptr of Vehicle) : void and plus leave() : void; an arrow labeled rides runs to Vehicle, 0..* to 0..1, the Vehicle end named minus ride_. Top right, purple: Sensor with minus id_ : int, minus type_ : SensorType, minus range_ : double, plus Sensor(int, SensorType = lidar, double = 100.0), plus get_id() : int, plus get_type() : SensorType and plus get_range() : double; a purple line labeled owns with a filled diamond at Vehicle joins them, 1 to 0..*, the Sensor end named minus sensors_. A purple dashed arrow runs from Sensor to SensorType, purple, marked enumeration, with lidar, camera and radar. A purple dashed arrow labeled uses runs from Vehicle to Route, purple, with plus add(Position) : void and plus length() : double; a purple line labeled has with a filled diamond at Route joins Route to Position, purple, marked struct, with plus x : double and plus y : double, 1 to 0..*, the Position end named minus waypoints_. Lower right, grey: RoboTaxi, marked final, with plus drive(const Route&) : void, and Taxi, marked final, with minus driver_name_ : string and plus drive(const Route&) : void; each joins Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   The ride service program as a UML class diagram, with every data member and method. Purple: L8's part of the program.

- Each box is a type: a class, a «struct» (``Position``) or an «enumeration» (``SensorType``), with its name, data members and methods. A minus sign marks a ``private`` member, a plus sign a ``public`` one, ``#`` a ``protected`` one (L9), and underlining a ``static`` one (`static Members`_). The types are C++ types.
- Each line is a relationship (L9). A member that a line stands for, such as ``sensors_``, is named at the line's end, not in the box: ``vehicles_`` and ``ride_`` at the ``Vehicle`` end of the lines from ``Fleet`` and ``Passenger``, ``sensors_`` at the ``Sensor`` end, and ``waypoints_`` at the ``Position`` end.
- This is the whole program we build in L8 and L9. This is the only time in L8 the diagram shows all of it. From here on (`Class Names Only`_) it shows the class names only, and each member comes in the section that builds it.
- Today we build the purple part: ``Vehicle``, its ``Sensor``\ s with their ``SensorType``, and the ``Position`` struct. ``Route`` is purple too, because ``drive`` takes one; it holds ``Position``\ s, and it is ready in the course code. The grey part, ``Fleet``, ``Passenger``, ``RoboTaxi`` and ``Taxi``, comes in L9, with the meaning of each kind of line.
- The diagram comes back twice: ``Vehicle`` (`Vehicle in the Class Diagram`_), and ``Sensor`` and ``Position`` (`Sensor and Position in the Class Diagram`_). Static members come at the end of the lecture (`static Members`_).

Class Names Only
^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/model_l8.png
   :alt: A UML class diagram of the ride service program, with class names only, in nine boxes. Vehicle is in the middle. On the left, Fleet joins Vehicle by a line with a hollow diamond at Fleet, labeled holds, 1 at Fleet and 0..* at Vehicle; below it, Passenger has an arrow labeled rides to Vehicle, 0..* at Passenger and 0..1 at Vehicle. To the upper right, Sensor joins Vehicle by a line with a filled diamond at Vehicle, labeled owns, 1 at Vehicle and 0..* at Sensor, and a dashed arrow runs from Sensor to SensorType, marked enumeration. To the right, a dashed arrow labeled uses runs from Vehicle to Route, and Route joins Position, marked struct, by a line with a filled diamond at Route, labeled has, 1 at Route and 0..* at Position. Lower right, RoboTaxi and Taxi, both marked final, each have a line with a hollow triangle at Vehicle. Vehicle, Sensor, SensorType, Route and Position, and the lines between them, are purple; Fleet, Passenger, RoboTaxi and Taxi, and their lines, are grey.
   :align: center
   :width: 100%

   The same diagram with class names only. The rest of L8 shows this view, and purple marks the part we build.

- This is the diagram of `The Class Diagram`_ with the members hidden: only the class names, the lines and the numbers on the lines.
- Each later copy colors purple the piece we are about to build and leaves the rest grey. The first one is ``Vehicle`` alone (`Vehicle in the Class Diagram`_).

Code for This Lecture
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   project/week8/
   ├── CMakeLists.txt
   ├── playground/
   ├── live/
   ├── appendix/
   └── rule_of_five/

**live** holds the class you write in the Live Coding steps: ``live8`` builds and runs it.

**Run a Slide's Code**

1. Get the code: ``git pull``.
2. In the top-level ``CMakeLists.txt`` (repository root), check that ``add_subdirectory(project/week8)`` is not commented out.
3. Configure: ``702configure``.
4. Build it: ``702build week8_playground``.
5. Run every slide: ``702run week8_playground``. Run only one slide, for example slide 9 (`Two Ways to Write the Same Program`_): ``702run week8_playground`` followed by the slide's number, ``702run week8_playground 9``.

**Where the Classes Are**

- **live** also holds ``Sensor`` with its ``SensorType``, ``Position``, and a small ``Route`` for ``drive``. **playground** holds the finished ``Vehicle`` that its slides run.
- For the **appendix**, the `Further Reading`_ part of this page: ``702build week8_appendix``, then ``702run week8_appendix ii`` runs appendix frame ii, `One Definition in Many Files`_.
- For the required reading, :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`: the **rule_of_five** folder, one file per part of the reading. ``702build week8_rule_of_five``, then ``702run week8_rule_of_five five`` runs the part ``five``. It is built with AddressSanitizer, and the parts that leak or free memory twice run only when asked for by name.

.. dropdown:: How to Run the Code
   :icon: terminal
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The ``702`` commands come from ``enpm702-cpp.sh`` in the repository. Its top comment shows how to load them in every new terminal. Then:

   .. code-block:: bash

      enpm702                            # go to the repository, load the 702 commands
      git pull                           # get this week's code
      702rebuild                         # once after you pull: a fresh build/
      702run week8_playground            # the code of every slide, in order
      702run week8_playground 27         # only the code of slide 27
      702run week8_appendix              # the code of every appendix frame
      702run week8_appendix ii           # only appendix frame ii (2 works too)
      702run week8_rule_of_five five     # only the part five of the reading

   The number is the one in the top-left corner of the slide. Appendix frames are numbered in roman numerals, i, ii, iii, and so on. After you edit a file, build again before you run: ``702build week8_playground`` builds one program, ``702build`` builds all of them.

   Code that does not compile is in the programs, commented out: uncomment it to get the slide's error.

Classes and Objects
-------------------

**Object-oriented programming** (OOP) builds a program from objects. Each object holds data and has the functions that work on that data.

See `cppreference: Classes <https://en.cppreference.com/w/cpp/language/classes>`__.

Two Ways to Write the Same Program
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **programming paradigm** is a way to organize a program. In the **procedural** way, data and the functions that use it are kept apart. In the **object-oriented** way, a class keeps them together.

Procedural:

.. code-block:: cpp

   // main.cpp
   struct VehicleData {
     double max_speed{13.4};
     double speed{0.0};
   };
   void set_speed(VehicleData& car,
                  double speed);
   VehicleData car_a;
   set_speed(car_a, 12.0);  // ok
   car_a.speed = -50.0;  // compiles

Object-oriented:

.. code-block:: cpp

   // main.cpp
   class Vehicle {
    public:
     void set_speed(double speed);
    private:
     double max_speed_{13.4};
     double speed_{0.0};
   };
   Vehicle car_b;
   car_b.set_speed(12.0);  // ok
   car_b.speed_ = -50.0;  // error

- Both programs call ``set_speed``, which checks the speed. In the ``struct``, any line can still change ``speed`` and skip the check. In the class, only ``Vehicle``'s own methods can (``private``, `Access Specifiers`_).
- Until now we wrote mostly procedural code: structs that hold data, and functions that take them. On the left, ``set_speed(car_a, 12.0)`` checks the speed and sets 12, but nothing makes anyone call it: ``car_a.speed = -50.0;`` compiles, and the program then prints -50 (measured with g++).
- On the right, ``speed_`` is ``private``, so only ``Vehicle``'s methods can change it. The same line does not compile: ``'double Vehicle::speed_' is private within this context``. Every change goes through ``set_speed``, so the check always runs.
- That is the reason for OOP in one example: a class keeps its data and its rules together, and the compiler enforces it.

Four Principles
^^^^^^^^^^^^^^^

A **principle** here is a rule for designing classes: what each class hides, what it shows, and how classes build on each other. This course uses four:

.. list-table::
   :header-rows: 1
   :widths: 20 65 15

   * - Principle
     - What it means
     - Lecture
   * - Encapsulation
     - An object's data members are hidden. Only the object's own functions can change them, so those functions can check every change.
     - L8
   * - Abstraction
     - Code that uses an object calls its functions. It does not need to know how the object stores its data.
     - L8
   * - Inheritance
     - A new class reuses an existing class and adds to it.
     - L9
   * - Polymorphism
     - One call works on objects of different classes that share the same functions.
     - L9

- Today, the vehicle hides its speed, and only its own methods change it.

What OOP Gives and What It Costs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Gives
     - Costs
   * - You can read and test each class on its own: ``Sensor`` works without ``Vehicle``.
     - You write more code before anything runs: each class has a header and a source file.
   * - Each class keeps its own rule in one place: only ``Vehicle``'s methods change ``speed_``.
     - You must decide which data goes in which class. A wrong choice is hard to undo later.
   * - Code that uses a class only calls its methods, so the class can change how it stores its data (`Changing the Inside`_).
     - A ``virtual`` call through a pointer to a base class (L9) can be slower than a direct call.

When Not to Use a Class
^^^^^^^^^^^^^^^^^^^^^^^

- **No rule between the data members**: use a ``struct``. Any ``x`` and any ``y`` make a ``Position``, so it is a ``struct`` (C.2). `Struct or Class`_ comes back to it.
- **A function that needs no private member**: keep it outside the class. A function that computes the distance between two ``Position`` objects reads only public members, so it stays a plain function (C.4). Such a function couples less to the class and has fewer ways to change the object. The distance example is chosen for this page.
- **Nothing to keep between calls**: a function is enough. A class pays off when an object holds data that must stay valid.

.. note::

   "Make a function a member only if it needs direct access to the representation of a class". Rule: `Core Guidelines C.4 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-member>`__.

Vehicle in the Class Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/model_l8_vehicle.png
   :alt: A UML class diagram of the ride service program, with class names only, in nine boxes. Vehicle is in the middle. On the left, Fleet joins Vehicle by a line with a hollow diamond at Fleet, labeled holds, 1 at Fleet and 0..* at Vehicle; below it, Passenger has an arrow labeled rides to Vehicle, 0..* at Passenger and 0..1 at Vehicle. To the upper right, Sensor joins Vehicle by a line with a filled diamond at Vehicle, labeled owns, 1 at Vehicle and 0..* at Sensor, and a dashed arrow runs from Sensor to SensorType, marked enumeration. To the right, a dashed arrow labeled uses runs from Vehicle to Route, and Route joins Position, marked struct, by a line with a filled diamond at Route, labeled has, 1 at Route and 0..* at Position. Lower right, RoboTaxi and Taxi, both marked final, each have a line with a hollow triangle at Vehicle. The Vehicle box is purple; every other box and line is grey.
   :align: center
   :width: 100%

   We write ``Vehicle`` first.

- We start with one box of the diagram, ``Vehicle``. Its data members are the maximum speed, the speed, the color and the mileage; its methods read and change them.
- We chose 13.4 m/s for its maximum speed in the examples, about 30 mph (30 × 0.44704 = 13.41).
- By the end of `The this Pointer`_ we have written most of this box. The sensors come in `Destructors`_, and the id and its static counter in `static Members`_.
- The grey boxes are the rest of the program. We build them in L9.

Class
^^^^^

A **class** is a type you define: a **blueprint**. It declares **data members**, which hold an object's values, and **methods** (member functions), the functions that work on those values.

.. figure:: /_static/images/l8/vehicle_blueprint.png
   :alt: A technical drawing of a sports car in black lines on white: a view from above on the left, three side views on the right, and a view from the front at the bottom left, each with dimension lines and numbers. A title block in the bottom right corner has four rows: MODEL, NOVA GT-1; DESIGNER, AUTO-FABRICA; DATE, 1:10; and DATE, OCT 26, 2023.
   :align: center
   :width: 30%

   The blueprint of a car.

- A car's blueprint says what every car of the model **has** (a color, a speed, a mileage) and what you can **do** with every car (change its speed, drive it).
- You cannot drive a blueprint. From one blueprint, a factory builds as many cars as it wants.
- In this lecture, the blueprint is the class ``Vehicle`` (`The Parts of a Class`_).

The Parts of a Class
""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   // main.cpp
   class Vehicle {  // a first version
    public:
     void set_speed(double speed);
     double get_speed() const;

    private:
     double max_speed_{13.4};  // m/s
     double speed_{0.0};       // m/s
     std::string color_{"white"};
     double mileage_{0.0};     // m driven
   };

- Line 2 starts with ``class``, then the name, in PascalCase.
- Lines 3 and 7 are **access specifiers**. Each applies to the members below it, up to the next one.
- Lines 4 and 5 declare the methods. `Accessors`_ explains the ``const`` on line 5.
- Lines 8 to 11 declare the data members, each with a default value for now (`Constructor with Parameters`_).
- On line 12, ``;`` ends the class, as it ends a ``struct``.

.. note::

   Data members of a class end in ``_``, so you can tell the member ``speed_`` from a parameter or a local variable named ``speed``. See `Google C++ Style: Variable Names <https://google.github.io/styleguide/cppguide.html#Variable_Names>`__.

Object
^^^^^^

An **object** is one car built from the blueprint: a piece of memory that holds one value for each data member of the class. The object is an **instance** of the class.

.. figure:: /_static/images/l8/vehicle_objects.png
   :alt: Two sports cars of the same model side by side on a light grey background, a red one on the left and a blue one on the right, both seen from the front at an angle.
   :align: center
   :width: 50%

   Two cars of the same model.

- The two cars are the same model, built from one blueprint, but each has its own color and mileage. Driving the red car does not add to the blue car's mileage.
- Two ``Vehicle`` objects of one class:

.. code-block:: cpp

   // main.cpp
   Vehicle car_a;
   Vehicle car_b;

- Each has its own ``max_speed_``, ``speed_``, ``color_`` and ``mileage_``, starting at 13.4, 0.0, ``"white"`` and 0.0.

Two Objects in Memory
"""""""""""""""""""""

.. figure:: /_static/images/l8/two_vehicles.png
   :alt: On the left, two panels one above the other, each a rounded name tag over a blue box with a stack icon and the word Stack. The upper tag reads car_a; its box holds four fields in two rows: max_speed_ with 13.4 (double) and speed_ with 12.0 (double), then color_ with "white" (std::string) and mileage_ with 0.0 (double). The lower tag reads car_b; its box holds max_speed_ with 13.4 (double) and speed_ with 10.0 (double), then color_ with "white" (std::string) and mileage_ with 0.0 (double). On the right, one green box with the word Code in its header, as tall as both panels, holds two boxes: set_speed() and get_speed(). From each Stack box, two blue arrows run right, one to each method, so four arrows end on the two methods: both objects use the same two methods, and the methods are not inside either object.
   :align: center
   :width: 78%

   Two ``Vehicle`` objects on the stack, and the one copy of their methods in the program's code.

- Each object holds its own values: 56 bytes with g++, three ``double``\ s and a ``std::string``.
- The methods exist once, in the program's code, and every object uses them. `The this Pointer`_ shows how a method knows which object it works on.

Live Coding: Step 1
"""""""""""""""""""

**10 minutes, with me.** We write the class ``Vehicle`` in ``live/src/main.cpp``, above ``main``, and make two objects of it.

1. Four ``private`` data members: ``max_speed_{13.4}``, ``speed_{0.0}``, ``color_{"white"}`` and ``mileage_{0.0}``.
2. Two ``public`` methods, with their bodies in the class: ``set_speed``, which checks nothing yet, and ``get_speed``.
3. In ``main``, uncomment the Step 1 block. It sets ``car_a`` to 12 m/s and ``car_b`` to 10 m/s, then prints both speeds and ``sizeof(Vehicle)``.

Build and run: ``live8``. The Step 1 block prints:

.. code-block:: text

   [Step 1]
   12 10
   56

- Each object keeps its own **state**, the values of its data members: 56 bytes with g++ (`Two Objects in Memory`_). Three ``double``\ s take 8 bytes each and a ``std::string`` 32; the methods take no room in the object.
- In this step, ``get_speed`` has no ``const`` and ``set_speed`` has no check yet: `Live Coding: Step 4`_ adds both.

Instantiation
^^^^^^^^^^^^^

**Instantiation** is building an object from a class, as a factory builds a car from its blueprint.

.. grid:: 1 1 3 3
   :gutter: 2

   .. grid-item::

      .. figure:: /_static/images/l8/vehicle_blueprint.png
         :alt: The technical drawing of the sports car: views from above, from the side and from the front, with dimension lines.
         :align: center

         **The class** is the blueprint.

   .. grid-item::

      .. figure:: /_static/images/l8/vehicle_instantiation.png
         :alt: A car factory: a grey sports car with its engine bay open sits on a yellow stand, robot arms reach in from both sides, and two workers in grey overalls work on it, one kneeling at a wheel. An engine hangs from a robot arm behind them, and a blue car is built further down the line.
         :align: center

         **Instantiation** is the factory.

   .. grid-item::

      .. figure:: /_static/images/l8/vehicle_objects.png
         :alt: The two sports cars of the same model, a red one and a blue one, side by side.
         :align: center

         **The objects** are the cars.

Live Coding: Step 2
""""""""""""""""""""""

You have **5 minutes** to make one object on the stack and one on the heap, in the Step 2 block of ``live/src/main.cpp``, with the class of Step 1. You write this step on your own:

1. Make ``car_a`` on the stack and set its speed to 12.
2. Make ``car_b`` on the heap with ``std::make_unique<Vehicle>()`` and set its speed to 10.
3. Print each speed. Call a method with ``.`` on an object and with ``->`` through a pointer.

Build and run: ``live8``. The block prints:

.. code-block:: text

   [Step 2]
   12
   10

- An object of a class is created like any other variable: on the stack, or on the heap and owned by a smart pointer.
- **Checkpoint**: in class, you show me your three lines before we start Step 3.

Stack or Heap
"""""""""""""

An object goes on the stack unless one of two reasons sends it to the heap.

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Situation
     - Where
     - Example
   * - 1\. It is used only inside one function or block.
     - The stack. It is destroyed at the end of the scope.
     - ``Vehicle car_a;``
   * - 2\. It must live on after the scope that made it.
     - The heap, owned by a ``std::unique_ptr``.
     - ``auto car_b{std::make_unique<Vehicle>()};``
   * - 3\. It is very large.
     - The heap, inside a ``std::vector``, which keeps its elements on the heap.
     - A lidar scan or a camera image.

- The Step 2 block made ``car_a`` on the stack and ``car_b`` on the heap. Both work, so you need a rule for picking one. The stack is the default, and two reasons send an object to the heap.
- Row 1: ``car_a`` lives inside one function. At the closing brace it is destroyed and its memory is free. Nothing has to be given back.
- Row 2: the object must outlive the block that made it. A ``std::unique_ptr`` owns it and decides when it ends. If the caller only needs the value, returning it by value works too.
- Row 3: the stack is small. ``ulimit -s`` prints its size in kilobytes, 16384 (16 MiB) on the PC used for the slides. A camera image or a lidar scan goes in a ``std::vector``, and the vector keeps its elements on the heap.

.. note::

   "Prefer scoped objects, don't heap-allocate unnecessarily". Rule: `Core Guidelines R.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-scoped>`__. A scoped object, in the Guidelines, is a local variable, a global variable or a data member.

Discussion: Class, Object, or Neither?
""""""""""""""""""""""""""""""""""""""

Class, object, or neither? Vote on each one, then say why.

1. ``std::string``
2. ``std::cout``
3. ``std::vector``, with no type in the angle brackets
4. ``car_b`` of `Live Coding: Step 2`_, made with ``std::make_unique<Vehicle>()``

Can a class exist with no object of it? Can an object exist without its class?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``std::string``: a class. It is another name for ``std::basic_string<char>``, a class made from a template. A ``std::string`` variable, such as ``color_``, is an object.
   2. ``std::cout``: an object, of the class ``std::ostream``. That is why we can use ``<<`` on it: the standard library defines ``<<`` for ``std::ostream`` objects.
   3. ``std::vector`` with nothing in the angle brackets: neither. It is a class template, a blueprint for classes. ``std::vector<Sensor>`` is a class, and a vector named ``sensors`` is an object.
   4. ``car_b``: an object, but not a ``Vehicle``. It is a ``std::unique_ptr<Vehicle>``, on the stack. The ``Vehicle`` it owns is a second object, on the heap, and it has no name.

   The last question: a class can exist with no object; we compiled ``Vehicle`` before we made one. An object cannot exist without its class: the class says how many bytes it takes and what its methods are.

Summary
^^^^^^^

- A class is a blueprint: it declares data members, which hold an object's values, and methods, which work on them.
- Each object holds its own values, 56 bytes for a ``Vehicle`` with g++. The methods exist once, in the program's code.
- An object goes on the stack unless it must outlive its scope, has several owners, has a class picked at run time, or is very large.


Struct or Class
---------------

A ``struct`` and a ``class`` both define a type with data members and methods, and a type with an invariant (`The Invariant`_) is written as a ``class``.

Rule: `Core Guidelines C.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-struct>`__.

The Invariant
^^^^^^^^^^^^^

An **invariant** (a class invariant) is a **condition on an object's data members** that **must be true whenever code outside the class uses the object**.

The section asks struct or class, and the Core Guidelines answer with one word: invariant. The definition has two parts.

- **Condition on an object's data members**: which values the data members may hold. *Example*: a ``Square`` object.

  - **Data members**: ``width_`` and ``height_``.
  - **Condition**: ``width_`` and ``height_`` are always equal. A ``Square`` 10 wide and 4 high is not a square, so an object that says so is wrong.

- **Must be true whenever code outside the class uses the object**: the rule holds before a ``public`` method is called and after it returns. Inside the method, the rule may break for a moment, but it holds again before the method returns. *Example*: the same ``Square``.

  - **Broken**: ``resize(10)`` sets ``width_`` to 10 first. ``height_`` still has the old size, so the rule is broken.
  - **Restored**: ``resize`` sets ``height_`` to 10 before it returns. Outside code never sees the broken state: no code outside the class runs between the two lines.

In `Live Coding: Step 4`_, ``Vehicle``'s ``set_speed`` checks the new value first, then assigns it, so it never breaks its speed rule, even for a moment.

The Invariant of Vehicle
^^^^^^^^^^^^^^^^^^^^^^^^

For ``Vehicle``: ``0.0 <= speed_ && speed_ <= max_speed_``

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Part of the class
     - How it keeps the invariant true
   * - ``private`` data members
     - Only ``Vehicle``'s own methods can change them (`Four Principles`_).
   * - Each method that changes a member
     - It refuses a bad value: ``set_speed(-50.0)`` throws (`Mutators`_).
   * - The constructor
     - It makes the invariant true when the object is created (`Constructors`_).

- In words: ``speed_`` is at least 0, and ``speed_`` is at most ``max_speed_``. A negative speed makes no sense for a car, and neither does a speed above its maximum, 13.4 m/s in our examples.
- Three things keep it: ``private`` data members, methods that check, and a constructor that starts the object with a valid speed. We write the checking ``set_speed`` and the constructor later today.
- We chose -50 for this example: any negative speed throws the same way. Throwing is one choice. The other is to change the value to a valid one.
- Run: ``702run week8_playground 25``.

Sensor and Position in the Class Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/model_l8_sensor_position.png
   :alt: A UML class diagram of the ride service program, with class names only, in nine boxes. Vehicle is in the middle. On the left, Fleet joins Vehicle by a line with a hollow diamond at Fleet, labeled holds, 1 at Fleet and 0..* at Vehicle; below it, Passenger has an arrow labeled rides to Vehicle, 0..* at Passenger and 0..1 at Vehicle. To the upper right, Sensor joins Vehicle by a line with a filled diamond at Vehicle, labeled owns, 1 at Vehicle and 0..* at Sensor, and a dashed arrow runs from Sensor to SensorType, marked enumeration. To the right, a dashed arrow labeled uses runs from Vehicle to Route, and Route joins Position, marked struct, by a line with a filled diamond at Route, labeled has, 1 at Route and 0..* at Position. Lower right, RoboTaxi and Taxi, both marked final, each have a line with a hollow triangle at Vehicle. The Sensor and Position boxes are purple; everything else is grey.
   :align: center
   :width: 100%

   ``Sensor`` is a ``class``, and ``Position`` is a ``struct``.

- Two small types sit next to ``Vehicle``. ``Position`` is two numbers, ``x`` and ``y``. ``Sensor`` is an id, a type from the ``SensorType`` enumeration, and a range.
- ``Sensor`` is a class and ``Position`` a struct. Why? Ask what ``Sensor`` must check that ``Position`` does not. `Which One`_ gives the answer. The constructor that makes the check comes in `Constructors`_ (`The Range Check`_).

The Sensor Class
^^^^^^^^^^^^^^^^

``sensor.hpp``:

.. code-block:: cpp

   // sensor.hpp
   enum class SensorType { lidar, camera, radar };
   class Sensor {
    public:
     explicit Sensor(int id, SensorType type = SensorType::lidar,
                     double range = 100.0)
         : id_{id}, type_{type}, range_{range} {
       if (range_ < 0.0) {
         throw std::invalid_argument{"range must be at least 0"};
       }
     }
     [[nodiscard]] int get_id() const noexcept;
     [[nodiscard]] SensorType get_type() const noexcept;
     [[nodiscard]] double get_range() const noexcept;
    private:
     int id_;           // picked by Vehicle::add_sensor()
     SensorType type_;  // what kind of sensor
     double range_;     // m, at least 0
   };

- ``SensorType`` is a scoped enumeration. We chose the defaults: ``Sensor{1}`` is a 100 m lidar.
- The other parts come later: ``const`` methods (`Accessors`_), ``[[nodiscard]]`` (:ref:`l8-nodiscard`), ``noexcept`` (:ref:`l8-noexcept`), constructors (`Constructors`_), the range check (`The Range Check`_) and ``explicit`` (:ref:`l8-explicit`).
- Run: ``702run week8_playground 27``.

Default Access
^^^^^^^^^^^^^^

.. code-block:: cpp

   // main.cpp
   struct Position {  // no access specifier
     double x{0.0};
     double y{0.0};
   };
   class Sensor {     // no access specifier
     double range_{100.0};
   };

   Position waypoint;
   waypoint.x = 25.0;    // OK: a struct's members are public
   Sensor lidar;
   lidar.range_ = -5.0;  // does not compile

.. code-block:: text

   error: 'double Sensor::range_' is private within this context

- With no access specifier, a member is ``public`` in a ``struct`` and ``private`` in a ``class``. Access to a base class (L9) has the same two defaults.
- So no code outside ``Sensor`` can set a negative range.
- Run: ``702run week8_playground 28``. The line that does not compile is commented out.

.. note::

   "Members of a class defined with the keyword ``class`` are ``private`` by default. Members of a class defined with the keywords ``struct`` or ``union`` are ``public`` by default". C++20 **[class.access]** (11.9) paragraph 3.

A Rule Nothing Checks
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // main.cpp
   struct Vehicle {
     double max_speed{13.4};  // m/s
     double speed{0.0};       // m/s, must stay from 0 to max_speed
   };

   Vehicle vehicle;
   vehicle.speed = 20.0;  // compiles: any code can break the rule
   std::cout << vehicle.speed << " > "
             << vehicle.max_speed << '\n';  // 20 > 13.4

- As a ``struct``, the vehicle's rule is only a comment. Any line of the program can set a speed above the maximum.
- As a ``class``, ``speed_`` is ``private``. Only ``Vehicle``'s own methods can change it, so ``set_speed`` can check every change (`Mutators`_).
- Run: ``702run week8_playground 29``.

Which One
^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 65 15

   * - Type
     - Must its members keep a rule?
     - Keyword
   * - ``Position``
     - No: any ``x`` and any ``y`` make a position on the map.
     - ``struct``
   * - ``Sensor``
     - Yes: its range must be at least 0. Its id and type can be any.
     - ``class``
   * - ``Vehicle``
     - Yes: the speed must stay from 0 to the maximum speed.
     - ``class``

.. note::

   "Use ``class`` if the class has an invariant; use ``struct`` if the data members can vary independently". Rule: `Core Guidelines C.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-struct>`__. "Use ``class`` rather than ``struct`` if any member is non-public". Rule: `C.8 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-class>`__.

Discussion: Struct or Class?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parts of the robotaxi's software. For each one: ``struct`` or ``class``? If a class, what rule must its members keep?

1. A GPS fix: latitude, longitude, and the time it was taken.
2. A battery level: a percentage.
3. A lane: the y of its left edge and the y of its right edge, in m.
4. The color of a car on the screen: red, green and blue, each from 0 to 255.
5. A trajectory: a list of poses, each with the time the robotaxi should reach it.

Who would break each rule by mistake: the code that reads the data, or the code that changes it?

.. dropdown:: Answers
   :class-container: sd-border-success

   If nobody can state a rule, it is a struct.

   1. The GPS fix: a class. Latitude must be from −90 to 90 degrees, and longitude from −180 to 180: a latitude of 1,000,000 is no place on Earth. There is no rule between the two, but each has its own range, like the battery level. In C.2, members that vary independently can each take any value, like ``Position``'s ``x`` and ``y``.
   2. The battery level: a class. The rule is from 0 to 100, and a setter checks it.
   3. The lane: a class. The left edge must be to the left of the right edge, so the two members must agree.
   4. The color: a struct, if each member is a ``std::uint8_t``. The type already keeps each value from 0 to 255, and the three values vary independently. A range rule can sometimes go into the type instead of a class.
   5. The trajectory: a class. The times must go up, so adding a pose must check the time of the last one.

   The last question: the code that changes the data, so the setter is the one place that checks.

Summary
^^^^^^^

- An invariant is a condition on an object's data members that must be true whenever code outside the class uses the object.
- With no access specifier, members are ``public`` in a ``struct`` and ``private`` in a ``class``.
- Use a ``class`` when the members keep an invariant (``Sensor``, ``Vehicle``), a ``struct`` when they vary independently (``Position``).


Encapsulation
-------------

**Encapsulation** keeps a class's data members ``private``. Code outside the class goes through its ``public`` methods, so those methods can keep the invariant.

Rule: `Core Guidelines C.9 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-private>`__.

Access Specifiers
^^^^^^^^^^^^^^^^^

An **access specifier** is a label in a class, ``public:``, ``private:`` or ``protected:``. It says which code may use the members declared after it, up to the next label.

.. code-block:: cpp

   // main.cpp
   class Vehicle {
    public:  // any code may call these
     void set_speed(double speed);
     double get_speed() const;

    private:  // only Vehicle's own methods may use these
     double max_speed_{13.4};  // m/s
     double speed_{0.0};       // m/s
     std::string color_{"white"};
     double mileage_{0.0};     // m driven
   };

Three Levels
""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 20 60 20

   * - Specifier
     - Who may use the member
     - Default in
   * - ``public``
     - Any code.
     - ``struct``
   * - ``private``
     - The class's own methods.
     - ``class``
   * - ``protected``
     - The class's own methods, and the classes that inherit from it (L9).
     -

- A class can also name a function or another class as a **friend**, which may use its ``private`` members too. Today's classes have no friends.
- Access is checked when the code compiles. It costs nothing when the program runs.

.. note::

   A ``private`` member's "name can be used only by members and friends of the class in which it is declared". C++20 **[class.access]** (11.9) paragraph 1.

Access in UML
"""""""""""""

.. figure:: /_static/images/l8/vehicle_access.png
   :alt: A UML class diagram of one class, Vehicle, in a box with three compartments. The top one holds the name, Vehicle. The middle one holds the data members -max_speed_ : double, -speed_ : double, -color_ : string and -mileage_ : double. The bottom one holds the methods +set_speed(double) : void and +get_speed() : double.
   :align: center
   :width: 40%

   The class box of the ``Vehicle`` of `Access Specifiers`_.

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - UML mark
     - C++
     - Who may use the member
   * - ``+``
     - ``public``
     - Any code.
   * - ``-``
     - ``private``
     - The class's own methods.
   * - ``#``
     - ``protected``
     - The class's own methods, and the classes that inherit from it (L9).

- The box shows the ``Vehicle`` of `Access Specifiers`_: the name at the top, its data members in the middle part, its methods in the bottom part.
- Each member starts with its access mark: a minus sign for the four ``private`` data members, a plus sign for the two ``public`` methods. The hash sign is ``protected``, which we use in L9 with inheritance.
- The opening diagram (`The Class Diagram`_) uses the same marks, so you can now read every member in it.

The Rule for Assignments and Group Projects (GPs)
"""""""""""""""""""""""""""""""""""""""""""""""""

- In every assignment and GP of this course, **each data member of a class is** ``private``.
- A class with a data member that is ``public`` gets **0 for the submission**.
- A ``struct`` whose members can vary independently, like ``Position``, keeps its members ``public`` (`Which One`_).

.. important::

   Not sure whether a type is a class or a struct? Ask in office hours before you submit.

Header and Source
^^^^^^^^^^^^^^^^^

A **method defined outside the class**: the class declares the method. Its body can be written outside the class, with the class's name and ``::`` before the method's name.

.. code-block:: cpp

   return_type ClassName::method_name(parameters) { body }

- The class goes in a header, ``vehicle.hpp``. The bodies of its methods go in a source file, ``vehicle.cpp``, as for any header file.
- ``::`` is the scope resolution operator, the same one as in ``std::cout``.

Live Coding: Step 3
"""""""""""""""""""

**10 minutes, on your own.** Move the class to ``live/include/vehicle.hpp`` and the bodies of its methods to ``live/src/vehicle.cpp``.

1. In ``vehicle.hpp``: ``#pragma once``, then the class, with only the declarations of its two methods.
2. In ``vehicle.cpp``: the two bodies, named ``Vehicle::set_speed`` and ``Vehicle::get_speed``.
3. Delete the class from ``main.cpp``, which already includes ``vehicle.hpp``. The output does not change.
4. Delete the ``Vehicle::`` before ``set_speed``, build, and read the error. Then put it back.

Build and run: ``live8``. Item 4 gives:

.. code-block:: text

   error: 'speed_' was not declared in
          this scope; did you mean 'speed'?

- Without ``Vehicle::``, ``set_speed`` is a new function that belongs to no class. It has no object, so it has no ``speed_``.

Abstraction
"""""""""""

**Abstraction** means that code that uses an object calls its ``public`` methods. It does not need to know how the object stores its data or how the methods do their work.

.. figure:: /_static/images/l8/coffee_machine.png
   :alt: Drawing of an espresso machine with dials and buttons on its front panel, two coffee holders with handles, and three glasses of coffee on the drip tray.
   :align: center
   :width: 35%

- You press a button on a coffee machine and get a coffee. You do not need to know the water temperature, the pressure or the order of the steps inside.
- The buttons are the ``public`` methods. The water tank, the heater and the pump are the ``private`` data members and the code behind the methods.
- The maker can change the inside, and you press the same buttons. `Changing the Inside`_ does this to ``Vehicle``.

Changing the Inside
"""""""""""""""""""

``vehicle.hpp``:

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
     // public: the same two declarations
    private:
     double max_speed_kmh_{48.24};
     double speed_kmh_{0.0};
     std::string color_{"white"};
     double mileage_{0.0};  // m driven
   };

``vehicle.cpp``:

.. code-block:: cpp

   // vehicle.cpp
   void Vehicle::set_speed(double speed) {
     speed_kmh_ = speed * 3.6;
   }
   double Vehicle::get_speed() const {
     return speed_kmh_ / 3.6;
   }

- The data members now hold km/h: 48.24 is 13.4 × 3.6. The method bodies convert, so the methods still take and give m/s.
- The speed calls of `Live Coding: Step 1`_ did not change: they still print ``12 10``.
- That is **abstraction**: the calling code depends on the methods, not on how the data is stored.
- With ``public`` members, every line that read ``speed_`` would now fail to compile.
- Run: ``702run week8_playground 41``.

A Body in the Class
"""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     double get_speed() const { return speed_; }  // body here
     void set_speed(double speed);  // body in vehicle.cpp
   };

- A method can also be defined in its class. It is then **inline**: each source file that includes the header may hold its body, and the compiler can put that body in place of a call.

.. warning::

   This course defines every method in ``vehicle.cpp``, even a one-line ``get_speed``: the header lists what the class does, and ``vehicle.cpp`` holds the code that does it. Constructors (`The Default Argument in the Header`_) are the one exception.

See `One Definition in Many Files`_, `A Method Defined in Its Class`_ and :ref:`l8-inline-hint` under Further Reading: why a function defined in a header must be ``inline``, what that means for a method defined in its class, and what ``inline`` does not promise.

Summary
^^^^^^^

- Data members are ``private``, and code outside the class goes through ``public`` methods, so the methods keep the invariant.
- The class goes in a header, ``vehicle.hpp``. Its method bodies go in ``vehicle.cpp``, each named with ``Vehicle::``.
- In a UML class box, ``+`` marks a ``public`` member, ``-`` a ``private`` one and ``#`` a ``protected`` one.
- Callers depend on the methods, not on how the data is stored, so the inside can change: that is abstraction.


Accessors and Mutators
----------------------

An **accessor** (getter) is a ``public`` method that gives a value of the object's state and changes nothing. A **mutator** (setter) is a ``public`` method that changes the state, after it checks that the change keeps the invariant.

Accessors
^^^^^^^^^

A **const method** is a method with ``const`` after its parameter list. It promises not to change the object's data members, and the compiler checks the promise.

.. code-block:: cpp

   // vehicle.hpp
   double get_speed() const {
     return speed_;
   }

- An accessor reads the state, so it is always a ``const`` method.
- Only a ``const`` method can be called on a ``const`` object (`const Objects`_, under Further Reading). Its constructor and destructor still run.

.. note::

   "A member function should be marked ``const`` unless it changes the object's observable state". Rule: `Core Guidelines Con.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-fct>`__.

.. _l8-nodiscard:

``[[nodiscard]]``
"""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   [[nodiscard]] double get_speed() const noexcept {
     return speed_;
   }

   car_a.get_speed();  // the result is thrown away: a warning

.. code-block:: text

   warning: ignoring return value of
            'double Vehicle::get_speed() const',
            declared with attribute 'nodiscard' [-Wunused-result]

- ``[[nodiscard]]``: ignoring an accessor's result is almost always a mistake, so the compiler warns.

.. _l8-noexcept:

``noexcept``
""""""""""""

- **The promise**: ``noexcept`` says that no exception leaves the method. Code can check it: ``noexcept(car_a.get_speed())`` is ``true``.
- **A broken promise**: if a ``noexcept`` method throws anyway, the program stops on the spot (``std::terminate``). A ``catch`` around the call never runs ([except.spec] paragraph 5, quoted in :ref:`l8-not-noexcept`). That is on purpose: the caller was told nothing can fail, so it has no plan for a failure. Stopping is safer than going on with a broken object.
- **Why**: the compiler has fewer paths to plan for, and a failure ends the program at once. For ``get_speed``, g++ ``-O2`` makes the same machine code with or without it. The gain shows up in code that is called often, or that the library picks with a ``noexcept`` test.

A ``noexcept`` ``set_speed`` given a speed of -50, measured with g++: the compiler warns ``throw will always call terminate``, and the run ends with ``terminate called after throwing an instance of std::invalid_argument`` and exit code 134, even with a ``catch`` in ``main``.

Where ``noexcept`` Goes
"""""""""""""""""""""""

- **Where**: it goes on small methods that cannot throw and are called often, such as accessors. Destructors and default constructors should never throw.
- **Not everywhere**: ``set_speed`` throws for a bad speed, and the caller catches it (:ref:`l8-not-noexcept`). Marked ``noexcept``, the same bad speed would stop the whole program.

The Core Guidelines (F.6) say ``noexcept`` is most useful for frequently used, low-level functions, and warn not to put it everywhere: the promise is part of the interface. Code can check it, with ``noexcept()`` or a ``static_assert``, and that code breaks if the promise is taken back.

.. note::

   "If your function must not throw, declare it ``noexcept``". Rule: `Core Guidelines F.6 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-noexcept>`__.

Discussion: Returning a Reference
"""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   // returns a reference to speed_
   double& get_speed() { return speed_; }

Why shouldn't an accessor return a reference to its data member?

.. dropdown:: Answers
   :class-container: sd-border-success

   - With ``double&``, outside code can write through the reference: ``car_a.get_speed() = 50.0;`` compiles with no warning and sets the speed to 50, above the maximum of 13.4 (measured with g++ 13.3). The member is private, but the reference opens it again, and no check runs: the invariant is broken.
   - With ``const double&``, nobody can write through it, but the reference can outlive its object: ``const double& speed = Vehicle{}.get_speed();`` refers to a ``Vehicle`` that no longer exists. g++ with ``-Wextra`` warns ``possibly dangling reference to a temporary``, and AddressSanitizer reports a stack-use-after-scope.
   - A ``double`` costs no more to copy than a reference, so returning by value loses nothing. For a large member, a ``const`` reference does save a copy: `Returning a Large Member`_.

Returning a Large Member
""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     [[nodiscard]] const std::string& get_color() const noexcept {
       return color_;  // no copy of the string
     }
    private:
     std::string color_{"white"};
   };

.. code-block:: cpp

   // main.cpp
   Vehicle car_a;
   std::cout << car_a.get_color() << '\n';  // prints white

- ``get_speed`` returns a ``double`` by value (:ref:`l8-nodiscard`): a copy of 8 bytes costs no more than a reference.
- A copy of a ``std::string`` copies every character, so a large member is returned by ``const&``: no copy, and the caller cannot change it.
- The reference is valid only while the ``Vehicle`` object lives (`Discussion: Returning a Reference`_).
- Run: ``702run week8_playground 50``.

Mutators
^^^^^^^^

A **mutator that checks** tests the new value against the invariant. If the value would break it, the mutator throws an exception and the object keeps its old value.

.. code-block:: cpp

   // vehicle.cpp
   void Vehicle::set_speed(double speed) {
     if (speed < 0.0 || speed > max_speed_) {
       throw std::invalid_argument{
           "speed must be from 0 to the maximum speed"};
     }
     speed_ = speed;
   }

- ``std::invalid_argument`` is in ``<stdexcept>``, as the :doc:`Exception Handling reading </reading_material/exception_handling/eh_index>` explains.
- The test comes first: ``speed_`` changes only when the new value is allowed.

Live Coding: Step 4
"""""""""""""""""""

**10 minutes, on your own.** ``get_speed`` promises to change nothing, and ``set_speed`` keeps the invariant.

1. ``get_speed`` gets ``[[nodiscard]]``, ``const`` and ``noexcept`` in the header. Its body stays in ``vehicle.cpp``, which repeats ``const`` and ``noexcept``.
2. To see what ``const`` checks, add ``speed_ = 0.0;`` as the first line of the body of ``get_speed`` and build. The compiler refuses: ``assignment of member 'Vehicle::speed_' in read-only object``. Delete that line.
3. ``set_speed`` checks first: for a speed below 0 or above ``max_speed_``, it throws ``std::invalid_argument``.
4. Uncomment the Step 4 block: it calls ``set_speed(20.0)`` in a ``try``.

Build and run: ``live8``. The Step 4 block prints:

.. code-block:: text

   [Step 4]
   caught: speed must be from 0 to the maximum speed
   12

- ``car_a`` kept its old speed, 12.

.. _l8-not-noexcept:

Not ``const``, Not ``noexcept``
"""""""""""""""""""""""""""""""

- A mutator changes the object, so it is not ``const``.
- This one can throw, so ``noexcept`` would be a false promise. With ``noexcept`` added, the call with 20.0 gives:

.. code-block:: text

   warning: 'throw' will always call 'terminate' [-Wterminate]

   terminate called after throwing an instance of 'std::invalid_argument'
     what():  speed must be from 0 to the maximum speed

- The warning comes from the compiler, the last two lines from the run. The ``catch`` of the Step 4 block (`Live Coding: Step 4`_) never runs.

.. note::

   "Whenever an exception is thrown and the search for a handler (14.4) encounters the outermost block of a function with a non-throwing exception specification, the function ``std::terminate`` is called (14.6.1)". C++20 **[except.spec]** (14.5) paragraph 5.

A Getter and Setter That Add Nothing
""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // position.hpp
   class Position {  // no rule about x
    public:
     double get_x() const { return x_; }
     void set_x(double x) { x_ = x; }  // takes any value

    private:
     double x_{0.0};
   };

- This setter checks nothing, so the pair only adds lines: any code can still set any ``x``. With no invariant, ``Position`` is the ``struct`` of `Which One`_, with ``public`` members.
- ``Vehicle``'s setter checks the speed, so its pair keeps the invariant.
- Run: ``702run week8_playground 54``.

.. note::

   "A trivial getter or setter adds no semantic value; the data item could just as well be ``public``". Rule: `Core Guidelines C.131 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-get>`__.

Summary
^^^^^^^

- An accessor is ``const``, and the compiler stops it from changing a data member. Add ``[[nodiscard]]`` and ``noexcept`` when each is true.
- A mutator checks the new value and throws when it would break the invariant, so the object keeps its old value. It is neither ``const`` nor ``noexcept``.
- Only a function that can handle the error catches it. The others pass the exception to their own caller.
- A getter and setter that check nothing only add lines: a type with no invariant is a ``struct``.


Constructors
------------

A **constructor** is a method with the class's name and no return type. It runs when an object is created, and it makes the invariant true before the object is used.

Rule: `Core Guidelines C.41 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-complete>`__.

.. note::

   The memory for the object exists before the constructor starts, with no values set. The constructor gives each member its first value and makes the object valid.

Default Constructor
^^^^^^^^^^^^^^^^^^^

A **default constructor** is a constructor that can be called with no arguments. A class that declares no constructor gets one from the compiler. It sets each data member from its **default member initializer**, the value in ``{ }`` after the member's name.

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {  // the first version: no constructor declared
     // ...
    private:
     double max_speed_{13.4};  // default member initializer
     double speed_{0.0};       // default member initializer
     std::string color_{"white"};  // default member initializer
     double mileage_{0.0};     // default member initializer
   };

.. code-block:: cpp

   // main.cpp
   Vehicle car_a;  // the compiler's default constructor runs

.. note::

   "If there is no user-declared constructor for class X, a non-explicit constructor having no parameters is implicitly declared as defaulted". C++20 **[class.default.ctor]** (11.4.4.1) paragraph 1.

A User-Defined Default Constructor
""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     Vehicle() {  // a user-defined default constructor
       std::cout << "a new Vehicle: " << color_ << ", "
                 << max_speed_ << " m/s\n";
     }
    private:
     double max_speed_{13.4};
     double speed_{0.0};
     std::string color_{"white"};
     double mileage_{0.0};
   };

.. code-block:: cpp

   // main.cpp
   Vehicle car_a;  // prints a new Vehicle: white, 13.4 m/s

- It has the class's name, no parameters and no return type. When its body starts, the members already hold their default values.
- Once you write it, the compiler writes none. Write one only when a new object needs more than its members' first values, here a line of output.
- Run: ``702run week8_playground 58`` prints ``a new Vehicle: white, 13.4 m/s``.

.. note::

   "Don't define a default constructor that only initializes data members; use default member initializers instead". Rule: `Core Guidelines C.45 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-default>`__.

A Member with No Initializer
""""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
     // ...
    private:
     double max_speed_{13.4};
     double speed_;  // no { }
     std::string color_{"white"};
     double mileage_{0.0};
   };

.. code-block:: cpp

   // main.cpp
   Vehicle a;    // a.speed_ has an indeterminate value
   Vehicle b{};  // the { } sets every member to zero first: 0

- Reading ``a.get_speed()`` is undefined behavior. g++ does not warn at ``-O0``, the Debug build. At ``-O2``, in a function other than ``main``, it warns: ``'a.Vehicle::speed_' is used uninitialized``.
- ``b`` prints 0 only because of its ``{ }``. Give every member an initializer.
- Run: ``702run week8_playground 59`` (it prints ``b`` only).

.. note::

   An object with no initialization "retains an indeterminate value", and reading one is undefined behavior: C++20 **[basic.indet]** (6.7.4) paragraphs 1 and 2.

Constructor with Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **constructor with parameters** takes the values the object starts from. Here its body stores each value in its data member with an **assignment**, ``member = value;``.

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     Vehicle(double max_speed, const std::string& color = "white") {
       max_speed_ = max_speed;  // assignment
       color_ = color;
       if (max_speed_ <= 0.0) {
         throw std::invalid_argument{
             "maximum speed must be greater than 0"};
       }
     }
     // ...
   };

- This constructor is written in the class: declared and defined in one place. This course writes every constructor this way (`The Default Argument in the Header`_).
- Run: ``702run week8_playground 60``. The ``Vehicle`` of ``vehicle.hpp`` uses the member initializer list instead (`Member Initializer List`_).

Two Kinds of Default Values
"""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     Vehicle(double max_speed, const std::string& color = "white") {
       // the assignments and the check
     }
    private:
     double max_speed_;     // set by the constructor
     double speed_{0.0};    // default member initializer
     std::string color_;    // set by the constructor
     double mileage_{0.0};  // default member initializer
   };

.. code-block:: cpp

   // main.cpp
   Vehicle car_a{13.4};          // white: the default argument
   Vehicle car_b{13.4, "blue"};  // blue

- A **default member initializer**, in the class body, gives a member its value when no constructor sets it: every vehicle starts at speed 0 and mileage 0.
- A **default argument**, in the parameter list, gives a parameter its value when the caller leaves it out. The caller picks the color, so it is a parameter; most cars are white, so it has a default.
- Run: ``702run week8_playground 61``.

The Default Argument in the Header
""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp: the declaration holds the default argument
   Vehicle(double max_speed, const std::string& color = "white");

.. code-block:: cpp

   // vehicle.cpp: the definition does not repeat it
   Vehicle::Vehicle(double max_speed, const std::string& color) {
     // the assignments and the check
   }

- A constructor can also be split into ``vehicle.hpp`` and ``vehicle.cpp``, like a method (`Live Coding: Step 3`_). The default argument is then written once, in the header: the code that creates a ``Vehicle`` sees only the header.
- Writing ``= "white"`` again in ``vehicle.cpp`` does not compile:

.. code-block:: text

   error: default argument given for parameter 2 of
          'Vehicle::Vehicle(double, const std::string&)'
   note: previous specification in
         'Vehicle::Vehicle(double, const std::string&)' here

- This course defines every constructor in the class. Every other method goes in ``vehicle.cpp`` (`A Body in the Class`_).

Discussion: Which Lines Compile?
""""""""""""""""""""""""""""""""

``Vehicle`` is the class of `The Default Argument in the Header`_: its constructor takes a maximum speed and a color, white by default.

.. code-block:: cpp

   // main.cpp
   Vehicle car_a{13.4};
   Vehicle car_b{13.4, "blue"};
   Vehicle parked_car;

Which of these lines compile? Why?

.. dropdown:: Answers
   :class-container: sd-border-success

   - ``car_a`` compiles: its maximum speed is 13.4, and the color takes the default argument, white. ``car_b`` compiles too: it is blue.
   - ``parked_car`` does not compile. Once the class declares a constructor, the compiler writes no default constructor (the rule of `Default Constructor`_). g++ says:

     .. code-block:: text

        error: no matching function for call to 'Vehicle::Vehicle()'

   - That is the right result here. No maximum speed is right for every vehicle, so every ``Vehicle`` must be given one.
   - ``702run week8_playground 63`` runs ``car_a`` and ``car_b``.

Braces or Parentheses
"""""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 16 42 42

   * - Case
     - With ``{ }``
     - With ``( )``
   * - 1\. Arguments
     - ``Vehicle car_b{13.4, "blue"};`` runs the constructor: blue.
     - ``Vehicle car_b(13.4, "blue");`` runs the same constructor: blue.
   * - 2\. Empty
     - ``Vehicle parked_car{};`` asks for the default constructor. This ``Vehicle`` has none: it does not compile.
     - ``Vehicle parked_car();`` declares a function that returns a ``Vehicle``, with a warning.

.. code-block:: text

   warning: empty parentheses were disambiguated as a function
            declaration [-Wvexing-parse]

- With two arguments, braces and parentheses run the same constructor, and both cars are blue.
- Empty is different. With empty parentheses, C++ reads the line as a function named ``parked_car`` that returns a ``Vehicle``. g++ warns, and the first use of ``parked_car`` as an object fails: ``request for member 'get_color' in 'parked_car', which is of non-class type 'Vehicle()'``.
- Run: ``702run week8_playground 64``.

Narrowing and Member Defaults
"""""""""""""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 16 42 42

   * - Case
     - With ``{ }``
     - With ``( )``
   * - 1\. Narrowing
     - ``Sensor lidar_a{1.5};`` does not compile: the id is an ``int``.
     - ``Sensor lidar_b(1.5);`` compiles with no warning, and the id is 1.
   * - 2\. Member default
     - ``double speed_{0.0};`` sets the default.
     - ``double speed_(0.0);`` does not compile: in a class, a default takes only ``{ }`` or ``=``.

.. code-block:: text

   error: narrowing conversion of '1.5e+0' from 'double' to 'int' [-Wnarrowing]
   error: expected identifier before numeric constant

- Braces refuse narrowing, also in a constructor call. ``Sensor``'s id is an ``int``, and the type and the range take their defaults. ``lidar_a``, with braces and 1.5, does not compile. With parentheses it compiles with no warning, even with ``-Wall -Wextra``, and the id is 1.
- Inside a class, a member's default value takes braces or an equals sign, and nothing else: the C++20 grammar for a member, in [class.mem], allows only those two. With parentheses, g++ reads ``speed_(`` as the start of a member function and expects a parameter, so ``0.0`` is an error: ``expected identifier before numeric constant``.
- So we write braces everywhere.

.. note::

   "Prefer the ``{}``-initializer syntax". Rule: `Core Guidelines ES.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-list>`__.

.. _l8-assign-code:

Assignment in the Body: the Code
""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // paper_tray.hpp
   class PaperTray {
    public:
     PaperTray() { std::cout << "PaperTray(): letter\n"; }
     PaperTray(const std::string& size) {
       std::cout << "PaperTray(size): " << size << '\n';
     }
   };

.. code-block:: cpp

   // printer.hpp
   class Printer {
    public:
     Printer(const std::string& paper_size) {
       std::cout << "Printer constructor body\n";
       tray_ = PaperTray{paper_size};
     }
    private:
     PaperTray tray_;
   };

.. figure:: /_static/images/l8/printer_tray.png
   :alt: A UML class diagram of two classes. Class Printer, at the top, has the method +Printer(const string&). Class PaperTray, below it, has the methods +PaperTray() and +PaperTray(const string&). A line joins them, with a filled diamond at Printer and the number 1 beside it; the end at PaperTray is labeled -tray_ 1.
   :align: center
   :width: 30%

   The class diagram of ``Printer`` and ``PaperTray``: composition (L9).

- A printer holds one paper tray. Each constructor of ``PaperTray`` prints a line, so the output of the next section shows which one runs, and when. Without a size, a tray holds letter paper.
- The constructor of ``Printer`` prints a line, then assigns a new ``PaperTray``, built from the paper size, to its member ``tray_``.
- The diagram is the class diagram of this code. A printer has exactly one tray, and a tray belongs to one printer: the 1 at each end. The tray is created with its printer and destroyed with it. That is the filled diamond, which L9 calls composition: the same line as ``Vehicle`` and its ``Sensor``\ s in the ride service program. The member ``tray_`` is named at the line's end, not in the box.

.. _l8-assign-twice:

Assignment Builds a Member Twice
""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // main.cpp
   Printer office_printer{"A4"};

.. code-block:: text

   PaperTray(): letter
   Printer constructor body
   PaperTray(size): A4

- ``tray_`` is created before the body of the ``Printer`` constructor runs, so the default constructor of ``PaperTray`` runs first: a letter tray.
- Then the body builds a second ``PaperTray``, a temporary with no name, for A4, and assigns it to ``tray_``.
- Two ``PaperTray`` constructors run for one member, and the assignment overwrites the letter tray.
- Run: ``702run week8_playground 67``.

.. note::

   Every data member is created before the constructor's body runs. The body can only assign a new value to a member that already exists.

.. _l8-const-member:

Assignment Fails for a ``const`` Member
"""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     Vehicle(double max_speed, const std::string& color = "white") {
       max_speed_ = max_speed;  // assignment: does not compile
       color_ = color;
     }
    private:
     const double max_speed_;  // fixed when the object is made
     double speed_{0.0};
     std::string color_;  // from the constructor
     double mileage_{0.0};
   };

.. code-block:: text

   error: uninitialized const member in 'const double' [-fpermissive]
   error: assignment of read-only member 'Vehicle::max_speed_'

- ``max_speed_`` is created before the body runs (:ref:`l8-assign-twice`), with no value, and a ``const`` member cannot be assigned afterwards.

Member Initializer List
^^^^^^^^^^^^^^^^^^^^^^^

The **member initializer list** is the list after ``:`` in a constructor. It **initializes** each member: it gives the member its first value as the member is created, before the body runs.

.. code-block:: cpp

   ClassName(parameters) : member{value}, member{value} { body }

.. code-block:: cpp

   // vehicle.hpp, in the class
   Vehicle(double max_speed, const std::string& color = "white")
       : max_speed_{max_speed}, color_{color} {
     if (max_speed_ <= 0.0) {
       throw std::invalid_argument{"maximum speed must be greater than 0"};
     }
   }

- The constructor of `Constructor with Parameters`_, with the list: the two assignments are gone, and the body keeps only the check.

The List Fixes Both Problems
""""""""""""""""""""""""""""

.. code-block:: cpp

   // printer.hpp, in the class
   Printer(const std::string& paper_size) : tray_{paper_size} {
     std::cout << "Printer constructor body\n";
   }

.. code-block:: cpp

   // main.cpp
   Printer office_printer{"A4"};

.. code-block:: text

   PaperTray(size): A4
   Printer constructor body

.. code-block:: cpp

   // vehicle.hpp, in the class, with const double max_speed_
   Vehicle(double max_speed, const std::string& color = "white")
       : max_speed_{max_speed}, color_{color} {}

- ``tray_`` is created from ``paper_size``: one ``PaperTray`` constructor instead of two (:ref:`l8-assign-twice`).
- The ``Vehicle`` of :ref:`l8-const-member` compiles: ``max_speed_`` gets its value as it is created.
- Run: ``702run week8_playground 70``.

.. note::

   "Prefer initialization to assignment in constructors". Rule: `Core Guidelines C.49 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-initialize>`__.

The Range Check
"""""""""""""""

.. code-block:: cpp

   // sensor.hpp, in the class
   explicit Sensor(int id, SensorType type = SensorType::lidar,
                   double range = 100.0)
       : id_{id}, type_{type}, range_{range} {
     if (range_ < 0.0) {
       throw std::invalid_argument{"range must be at least 0"};
     }
   }

.. code-block:: cpp

   // main.cpp
   try {
     Sensor radar{3, SensorType::radar, -5.0};
   } catch (const std::invalid_argument& e) {
     std::cout << "caught: " << e.what() << '\n';
   }

.. code-block:: text

   caught: range must be at least 0

- The constructor of `The Sensor Class`_ sets every member in the list, then checks the range.
- A negative range throws, so no ``Sensor`` breaks the rule that makes it a ``class`` (`Which One`_).
- Run: ``702run week8_playground 71``.

Declaration Order
"""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     Vehicle(double max_speed, double speed)
         : speed_{speed}, max_speed_{max_speed}, color_{"white"} {}
    private:
     double max_speed_;     // created first
     double speed_;         // created second
     std::string color_;    // created third
     double mileage_{0.0};  // created fourth
   };

.. code-block:: text

   warning: 'Vehicle::speed_' will be initialized after [-Wreorder]
   warning:   'double Vehicle::max_speed_' [-Wreorder]
   warning:   when initialized here [-Wreorder]

- Members are created in declaration order, whatever the order of the list.
- A value that uses a member declared later reads it before it has a value.

.. note::

   "Define and initialize data members in the order of member declaration". Rule: `Core Guidelines C.47 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-order>`__.

Discussion: Spot the Bug
""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   // following_gap.hpp
   class FollowingGap {  // the robotaxi's gap to the car ahead
    public:
     FollowingGap(double speed): time_{2.0}, distance_{time_ * speed} {}

     [[nodiscard]] double get_distance() const noexcept {
       return distance_;
     }

    private:
     double distance_;  // m
     double time_;      // s: the gap in seconds
   };

- The author wants a 2-second gap: at 12 m/s, 2 × 12 = 24 m. Does ``get_distance()`` return 24?
- Would you catch this in a code review? What would catch it for you?

.. dropdown:: Answers
   :class-container: sd-border-success

   - It does not return 24. ``distance_`` is declared first, on line 11, so it is created first, whatever the order of the list. It reads ``time_``, which has no value yet: undefined behavior.
   - A reviewer reads the list left to right and sees ``time_`` first, so the bug is easy to miss. g++ catches it at ``-O0``: ``will be initialized after [-Wreorder]``, and ``member 'FollowingGap::time_' is used uninitialized [-Wuninitialized]``. This is why the course builds with ``-Wall -Wextra``.
   - Two fixes: compute ``distance_`` from the parameter, ``distance_{2.0 * speed}``, or declare ``time_`` first. The fixed class prints 24: ``702run week8_playground 73`` runs the first fix.

.. _l8-explicit:

``explicit``
^^^^^^^^^^^^

An **explicit constructor**, a constructor marked ``explicit``, runs only when the code names the class. Without ``explicit``, a constructor that can be called with one argument also turns a value of its parameter's type into an object, wherever an object is expected.

.. code-block:: cpp
   :emphasize-lines: 4, 5

   // vehicle.hpp
   class Vehicle {
    public:
     explicit Vehicle(double max_speed,
                      const std::string& color = "white");
     [[nodiscard]] double get_max_speed() const noexcept;
     // get_speed and set_speed as before
    private:
     double max_speed_;     // m/s, greater than 0
     double speed_{0.0};    // m/s
     std::string color_;    // from the constructor
     double mileage_{0.0};  // m driven
   };

.. note::

   "By default, declare single-argument constructors explicit". Rule: `Core Guidelines C.46 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-explicit>`__.

A Conversion Nobody Asked For
"""""""""""""""""""""""""""""

.. code-block:: cpp

   // main.cpp
   void show(const Vehicle& vehicle) {
     std::cout << vehicle.get_max_speed() << ' '
               << vehicle.get_speed() << '\n';
   }

   show(Vehicle{13.4});  // names the class: prints 13.4 0
   show(13.4);           // a double, not a Vehicle

- **Without** ``explicit``, ``show(13.4)`` compiles: the compiler builds a temporary ``Vehicle`` from 13.4, and it prints ``13.4 0``.
- **With** ``explicit``, it does not compile:

.. code-block:: text

   error: invalid initialization of reference of type 'const Vehicle&'
          from expression of type 'double'

- Run: ``702run week8_playground 75``.

Delegating Constructor
^^^^^^^^^^^^^^^^^^^^^^

A **delegating constructor** is a constructor whose member initializer list names another constructor of the same class. That constructor runs first, then this one's body.

.. code-block:: cpp

   // vehicle.hpp, in the class
   Vehicle(double max_speed, double speed)
       : Vehicle{max_speed} {  // checks the maximum speed
     set_speed(speed);         // checks the speed
   }

- The check of the maximum speed is written once, in the constructor of `Member Initializer List`_. The new constructor reuses it, then the setter's check.
- ``Vehicle car_a{13.4, 12.0};`` starts at 12; ``{13.4, 20.0}`` throws the setter's exception.
- Run: ``702run week8_playground 76``.

.. note::

   "Use delegating constructors to represent common actions for all constructors of a class". Rule: `Core Guidelines C.51 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-delegating>`__.

Live Coding: Step 5
"""""""""""""""""""

**15 minutes, on your own.** Every ``Vehicle`` starts with a maximum speed greater than 0, or it is never created.

1. In the class: the ``explicit`` constructor of `Member Initializer List`_ and :ref:`l8-explicit`, the constructor of `Delegating Constructor`_, and the declaration of ``get_color``. ``max_speed_`` and ``color_`` lose their ``{ }`` values.
2. In the source: the body of ``get_color``.
3. ``Vehicle car_a;`` in the Step 1, 2 and 4 blocks gives ``no matching function for call to 'Vehicle::Vehicle()'``: write ``Vehicle car_a{13.4};`` instead, and the same for ``car_b``.
4. Uncomment the Step 5 block.

Build and run: ``live8``. The Step 5 block prints:

.. code-block:: text

   [Step 5]
   white blue 12
   caught: maximum speed must be greater than 0

- The class has no default constructor any more (`Discussion: Which Lines Compile?`_), so ``car_a`` gets ``{13.4}`` in the Step 1, 2 and 4 blocks, ``car_b`` gets ``{13.4}`` in Step 1, and Step 2's ``car_b`` gets ``std::make_unique<Vehicle>(13.4)``.
- ``bad_car{0.0}`` throws, so ``bad_car`` never exists.

Summary
^^^^^^^

- A constructor has the class's name and no return type. It makes the invariant true, or throws, so no object breaks the invariant.
- A class that declares no constructor gets a default constructor from the compiler. A class that declares one gets none.
- Every member is created before the body runs. Initialize members in the member initializer list, in declaration order.
- Create objects with braces: they refuse narrowing and never declare a function. Mark a constructor that can be called with one argument ``explicit``.


The this Pointer
----------------

Inside a method, ``this`` is a pointer to the object the method was called on.

See `cppreference: The this pointer <https://en.cppreference.com/w/cpp/language/this>`__.

One Copy of the Code
^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/two_vehicles.png
   :alt: On the left, two panels one above the other, each a rounded name tag over a blue box with a stack icon and the word Stack. The upper tag reads car_a; its box holds four fields in two rows: max_speed_ with 13.4 (double) and speed_ with 12.0 (double), then color_ with "white" (std::string) and mileage_ with 0.0 (double). The lower tag reads car_b; its box holds max_speed_ with 13.4 (double) and speed_ with 10.0 (double), then color_ with "white" (std::string) and mileage_ with 0.0 (double). On the right, one green box with the word Code in its header, as tall as both panels, holds two boxes: set_speed() and get_speed(). From each Stack box, two blue arrows run right, one to each method, so four arrows end on the two methods: both objects use the same two methods, and the methods are not inside either object.
   :align: center
   :width: 66%

   The figure of `Two Objects in Memory`_: two objects, one copy of the methods.

- Each object has its own data members. ``set_speed`` and ``get_speed`` exist once, in the code (`Two Objects in Memory`_).
- ``car_a.set_speed(12.0)`` and ``car_b.set_speed(10.0)`` run the same ``set_speed``. Each call also passes a hidden pointer, ``this``, to the object it was called on: ``car_a`` in the first call, ``car_b`` in the second. It plays the role of ``self`` in Python, but you do not write it in the parameter list.
- So when ``set_speed`` writes ``speed_``, the call tells it which ``speed_``. `One Method, Many Objects`_ prints both addresses to show they match.

One Method, Many Objects
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // vehicle.cpp
   void Vehicle::set_speed(double speed) {
     std::cout << "this:   " << this << '\n';
     // ... the check of the mutator ...
     speed_ = speed;  // means this->speed_
   }

.. code-block:: cpp

   // main.cpp
   Vehicle car_a{13.4};
   std::cout << "&car_a: " << &car_a << '\n';
   car_a.set_speed(12.0);

.. code-block:: text

   &car_a: 0x7ffe745810b0
   this:   0x7ffe745810b0

- One run; the address changes from run to run, but the two lines always match. Run it yourself: ``702run week8_playground 81``.
- The method reaches the members through ``this``: ``speed_`` means ``this->speed_``.

.. _l8-this-type:

The Type of ``this``
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - Inside
     - Type of ``this``
     - Can change data members?
   * - ``set_speed``
     - ``Vehicle*``
     - Yes
   * - ``get_speed() const``
     - ``const Vehicle*``
     - No

- In a ``const`` method, ``this`` points to a ``const Vehicle``: the method cannot change a data member. ``speed_ = 1.0;`` in ``get_speed`` does not compile.
- ``this`` itself cannot be changed: ``this = nullptr;`` does not compile in any method.

.. _l8-return-this:

Returning ``*this``
^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // vehicle.cpp
   Vehicle& Vehicle::speed_up(double step) {
     set_speed(speed_ + step);  // the check runs here
     return *this;              // the object itself
   }

.. code-block:: cpp

   // main.cpp
   Vehicle car_a{13.4, 12.0};
   car_a.speed_up(0.5).speed_up(0.5);
   std::cout << car_a.get_speed() << '\n';  // 13

- ``*this`` is the object, and the return type ``Vehicle&`` hands back a reference to it, not a copy. The second ``speed_up`` runs on ``car_a`` again: 12 + 0.5 + 0.5 = 13.
- An assignment operator, ``operator=``, returns ``*this`` the same way: see the :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>` reading.
- Run: ``702run week8_playground 83``.

Summary
^^^^^^^

- Inside a method, ``this`` points at the object the method was called on: the call passes the object's address.
- Its type is ``Vehicle*``, or ``const Vehicle*`` in a ``const`` method.
- A method that returns ``*this`` as a ``Vehicle&`` hands back the object itself, so calls can be chained.


Destructors
-----------

A **destructor** is the method ``~ClassName()``, with no parameters and no return type. It runs when an object's lifetime ends, and it gives back what the object owns.

Rule: `Core Guidelines C.31 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-release>`__.

.. important::

   **Reading Instead of an Exercise.** L8 has no C++ exercise. After class, read :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`. **Quiz 4**, at the start of Lecture 9 on Nov 3, includes questions on it.

Destructor
^^^^^^^^^^

**Declaring a destructor**: in the class, ``~`` and the class's name, with no parameters and no return type. A class has one destructor. The compiler calls it when an object's lifetime ends.

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     ~Vehicle() {  // prints, to show when it runs
       std::cout << "~Vehicle: speed " << speed_ << '\n';
     }
     // ... the members we wrote in Steps 1 to 5
   };

- This ``Vehicle`` owns no memory by hand: its ``std::string`` gives back its own. So this destructor only prints.
- A class in this course never calls ``new`` and ``delete`` itself: a ``std::unique_ptr`` member owns the heap memory (`When to Write a Destructor`_).

.. note::

   "Avoid calling ``new`` and ``delete`` explicitly". Rule: `Core Guidelines R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`__.

When It Runs
""""""""""""

.. code-block:: cpp

   // main.cpp
   {
     Vehicle car_a{13.4, 12.0};
     Vehicle car_b{13.4, 10.0};
     std::cout << "end of scope\n";
   }
   auto spare_car{
       std::make_unique<Vehicle>(13.4, 5.0)};
   spare_car.reset();
   std::cout << "after reset\n";

.. code-block:: text

   end of scope
   ~Vehicle: speed 10
   ~Vehicle: speed 12
   ~Vehicle: speed 5
   after reset

- The ``Vehicle`` of `Destructor`_: its destructor prints the speed.
- At the end of a scope, objects are destroyed in the reverse order they were created: ``car_b``, then ``car_a``.
- A heap object is destroyed when its owner lets go: here ``reset()``.
- The destructor, two copies and two moves are five of the six **special member functions**; the default constructor is the sixth. The rule of zero and the rule of five, in the :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>` reading, required after class, say when a class writes these five.
- Run: ``702run week8_playground 87``.

When to Write a Destructor
""""""""""""""""""""""""""

- **No destructor** when no member needs cleanup by hand. A basic type, such as ``double``, holds nothing to give back. An RAII object, such as a ``std::string``, a ``std::vector``, a ``std::unique_ptr`` or a ``std::shared_ptr``, gives back what it holds in its own destructor. The destructor the compiler writes destroys each member, so ``Vehicle`` writes none: that is the **rule of zero**.
- **A destructor** when the class holds a resource by hand: memory it got with ``new``, or a file it opened. The destructor gives it back. The class then also needs its own copies and moves, or a copy frees the same memory twice: the **rule of five**.

.. note::

   Both rules, with code that leaks and code that frees twice, are in the required reading: :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`.

Summary
^^^^^^^

- A destructor, ``~Vehicle()``, runs when an object's lifetime ends and gives back what the object owns.
- At the end of a scope, objects are destroyed in the reverse order they were created. A heap object is destroyed when its owner lets go.
- A class whose members give back their own memory, such as ``std::unique_ptr``, needs no destructor of its own. The rule of zero and the rule of five, in the :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>` reading, say when a class writes one.


static Members
--------------

A ``static`` **data member** belongs to the class, not to an object: there is one, shared by every object. A ``static`` **method** is called on the class, and it has no ``this``.

- Every member so far belongs to one object: each ``Vehicle`` has its own speed and its own color. A ``static`` member belongs to the class instead.
- A ``static`` method is called on the class itself, as ``Vehicle::get_next_id()``. No object is involved, so it has no ``this``.

See `cppreference: static members <https://en.cppreference.com/w/cpp/language/static>`__.

One Counter for Every Vehicle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/model_l8_static.png
   :alt: A UML class diagram of the ride service program, with class names only, in nine boxes. Vehicle is in the middle. On the left, Fleet joins Vehicle by a line with a hollow diamond at Fleet, labeled holds, 1 at Fleet and 0..* at Vehicle; below it, Passenger has an arrow labeled rides to Vehicle, 0..* at Passenger and 0..1 at Vehicle. To the upper right, Sensor joins Vehicle by a line with a filled diamond at Vehicle, labeled owns, 1 at Vehicle and 0..* at Sensor, and a dashed arrow runs from Sensor to SensorType, marked enumeration. To the right, a dashed arrow labeled uses runs from Vehicle to Route, and Route joins Position, marked struct, by a line with a filled diamond at Route, labeled has, 1 at Route and 0..* at Position. Lower right, RoboTaxi and Taxi, both marked final, each have a line with a hollow triangle at Vehicle. The Vehicle box is purple; every other box and line is grey.
   :align: center
   :width: 100%

   ``Vehicle`` gets ``next_id_``.

- Every ``Vehicle`` needs its own id, so the fleet can tell two vehicles apart.
- ``Vehicle`` (purple) gets ``next_id_``, one counter for the whole class, not one in each object. The diagram shows class names only, so ``next_id_`` is not drawn. When a UML diagram shows members, it underlines a static one.
- The constructor sets ``id_`` from the counter, then adds 1 to the counter.

Two Vehicles, the Same Id
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :emphasize-lines: 6, 9

   // vehicle.hpp
   class Vehicle {
    public:
     explicit Vehicle(double max_speed,
                      const std::string& color = "white")
         : id_{next_id_++}, max_speed_{max_speed}, color_{color} {}
     [[nodiscard]] int get_id() const noexcept { return id_; }
    private:
     int next_id_{1};  // one counter in each object
     int id_;
     double max_speed_;
     double speed_{0.0};
     std::string color_;
     double mileage_{0.0};
   };

.. code-block:: cpp

   // main.cpp
   Vehicle car_a{13.4};
   Vehicle car_b{13.4};
   std::cout << car_a.get_id() << '\n';  // 1
   std::cout << car_b.get_id() << '\n';  // 1

- The first try: the counter ``next_id_`` is an ordinary data member that starts at 1. The constructor copies it into ``id_``, then adds 1.
- Each object has its own ``next_id_``, so every counter starts at 1 and every ``Vehicle`` gets id 1: a fleet cannot tell two vehicles apart. Adding 1 to ``car_a``'s counter does nothing for ``car_b``.
- Run: ``702run week8_playground 92``.

One Counter for the Class
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :emphasize-lines: 8, 10

   // vehicle.hpp
   class Vehicle {
    public:
     explicit Vehicle(double max_speed,
                      const std::string& color = "white")
         : id_{next_id_++}, max_speed_{max_speed}, color_{color} {}
     [[nodiscard]] int get_id() const noexcept { return id_; }
     [[nodiscard]] static int get_next_id() noexcept { return next_id_; }
    private:
     inline static int next_id_{1};  // one counter for the class
     int id_;
     double max_speed_;
     double speed_{0.0};
     std::string color_;
     double mileage_{0.0};
   };

- ``static``: one ``next_id_`` for the class, stored in no object. Every constructor call takes the next number from it.
- ``get_next_id()`` is a ``static`` method, so ``Vehicle::get_next_id()`` can be called before any ``Vehicle`` exists: it is 1.
- ``next_id_++`` gives the counter's value first and adds 1 after. So ``car_a`` gets id 1 and the counter becomes 2; then ``car_b`` gets id 2, and ``get_next_id()`` is 3.
- ``inline`` (C++17) lets the header give the counter its first value. `The Counter's First Value`_ shows where it goes without ``inline``.
- Run: ``702run week8_playground 93``.

The Counter's First Value
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // vehicle.hpp, in the class, without inline
   static int next_id_;  // declared only

.. code-block:: cpp

   // vehicle.cpp, outside every function
   int Vehicle::next_id_{1};  // defined once: the first value

- Without ``inline``, the counter takes two steps. Step 1, in the class: ``static int next_id_;`` declares it, with no value. Step 2, in ``vehicle.cpp``, at the top of the file, outside every function: ``int Vehicle::next_id_{1};`` defines it once and gives it its first value.
- In one step, ``static int next_id_{1};`` in the class, it does not compile: g++ 13.3 says "ISO C++ forbids in-class initialization of non-const static member".
- Run: ``702run week8_playground 94``.

.. _l8-static-method:

A ``static`` Method Has No ``this``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // main.cpp
   std::cout << Vehicle::get_next_id() << '\n';  // on the class, no object

.. code-block:: cpp

   // vehicle.hpp
   static double get_speed_kmh() noexcept {  // in Vehicle: an error
     return speed_ * 3.6;
   }

.. code-block:: text

   error: invalid use of member 'Vehicle::speed_' in static member function

- ``Vehicle::get_next_id()`` is called on the class, with no object, so the method has no ``this``.
- ``speed_`` belongs to one ``Vehicle`` object. A ``static`` method has no ``this`` to find ``speed_`` through, so ``get_speed_kmh()`` does not compile.
- A ``static`` method can be called on a ``const`` object too, because it has no ``this`` to make ``const``.
- Run: ``702run week8_playground 95``.

.. note::

   "A static member function does not have a ``this`` pointer". C++20 **[class.static.mfct]** (11.4.8.1) paragraph 2 (a note).

.. important::

   A ``static`` data member: one for the class, shared by every object. A ``static`` method: called on the class, with no ``this``, so it can use only ``static`` members.

Methods With and Without ``this``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l8/static_members.png
   :alt: On the left, two panels one above the other, each a rounded name tag over a blue box with a stack icon and the word Stack. The upper tag reads car_a; its box holds two fields: id_ with 1 (int) and speed_ with 12.0 (double). The lower tag reads car_b; its box holds id_ with 2 (int) and speed_ with 10.0 (double). On the upper right, a green box with the word Code holds three methods: set_speed(), get_id() and static get_next_id(). From each Stack box, two blue arrows run right, one to set_speed() and one to get_id(); a black tag 1 sits between the two panels, by these arrows. No arrow from an object reaches static get_next_id(), which has a black tag 3 at its left. On the lower right, an orange box with the words Static storage holds one field, next_id_ with 3 (int), with a black tag 2 at its left; one orange arrow leaves static get_next_id() on its right, runs down beside the boxes and enters next_id_ from the right.
   :align: center
   :width: 100%

Each object has its own ``id_`` and ``speed_``; the methods exist once, in the code.

1. ``this``: ``set_speed`` and ``get_id`` get the object they are called on, ``car_a`` in one call and ``car_b`` in the other.
2. ``next_id_``, a ``static`` data member: one for the class, in no object.
3. ``get_next_id``, a ``static`` method: no ``this``, so it reaches only ``static`` members.

A Method That Uses No Member
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // vehicle.hpp, in the class Vehicle
   [[nodiscard]] static double mph_to_mps(double mph) noexcept;

.. code-block:: cpp

   // vehicle.cpp
   double Vehicle::mph_to_mps(double mph) noexcept {
     return mph * 0.44704;
   }

.. code-block:: cpp

   // main.cpp
   std::cout << Vehicle::mph_to_mps(30.0) << '\n';  // 13.4112: no object

- ``mph_to_mps`` reads no data member, neither an object's nor a ``static`` one, so it needs no ``this``: make it ``static``, and call it on the class. 30 mph is 13.4112 m/s, and no ``Vehicle`` exists.
- First ask whether it belongs in the class at all. A function that needs no member can live outside the class, in a header of its own (`When Not to Use a Class`_, Core Guidelines C.4). Keep it a ``static`` method when it is part of what the class offers, or a ``private`` helper of the class's own methods.
- Run: ``702run week8_playground 97``.

Discussion: One per Object, or One for the Class?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Should each of these be a ``static`` member, or one per object?

1. In ``Vehicle``: how many ``Vehicle`` objects exist right now.
2. In ``Vehicle``: the ``Sensor``\ s it owns.
3. In ``Vehicle``: the maximum speed.
4. In ``Vehicle``: the number of m/s in one mph, 0.44704.
5. In ``Vehicle``: a method that turns mph into m/s.

The test: does the answer change from one object to the next?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Static: one count for the class, raised in the constructor and lowered in the destructor.
   2. Not static: each vehicle has its own sensors.
   3. Not static: two vehicles can have two different maximum speeds.
   4. The same for every object, so it belongs to the class: a static constant.
   5. It uses no member, so it can be a static method, or a plain function outside the class.

Summary
^^^^^^^

- A ``static`` data member belongs to the class: there is one, shared by every object.
- A counter in each object gave every ``Vehicle`` id 1. An ``inline static`` counter is one for the class, and the header gives its first value.
- A ``static`` method is called on the class and has no ``this``, so without an object it can use only the ``static`` members.

Further Reading
---------------

The sections below are the appendix of the slides. They are **not presented** in the lecture. Read them on your own. The appendix has two parts:

1. **One Definition in Many Files** (frames ii to iv): why a function defined in a header must be ``inline``, and what ``inline`` does not promise, from `One Definition in Many Files`_ to :ref:`l8-inline-hint`.
2. `const Objects`_ (frames v to x): what a ``const`` object cannot do, and a ``const`` reference.

Each section names the appendix frame it comes from. Build the appendix program with ``702build week8_appendix``; each section that has code names its ``702run week8_appendix`` command.

One Definition in Many Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Appendix frame ii, from `A Body in the Class`_.

.. code-block:: cpp

   // speed.hpp
   #pragma once
   inline double kmh(double mps) {
     return mps * 3.6;
   }

.. code-block:: cpp

   // a.cpp
   #include "speed.hpp"
   double a() { return kmh(10.0); }

.. code-block:: cpp

   // main.cpp
   #include <iostream>
   #include "speed.hpp"
   double a();  // defined in a.cpp
   int main() {
     std::cout << kmh(12.0) << ' '
               << a() << '\n';
   }  // prints 43.2 36

- ``#include`` copies the header into each file, so ``a.cpp`` and ``main.cpp`` define ``kmh`` the same way. ``#pragma once`` only stops a second copy in one file.
- Without ``inline``, the program does not link (g++ 13.3, output cut):

.. code-block:: text

   main.cpp:(.text+0x0): multiple definition of `kmh(double)'; ...

.. note::

   "There can be more than one definition of a ... inline function or variable (9.2.7) ... provided that each definition appears in a different translation unit and the definitions satisfy the following requirements". C++20 **[basic.def.odr]** (6.3) paragraph 13. A translation unit is a source file with its headers. The requirements say the definitions must be the same.

- Run: ``702run week8_appendix ii``.

A Method Defined in Its Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Appendix frame iii, from `A Body in the Class`_.

.. note::

   "A member function may be defined (9.5) in its class definition, in which case it is an inline (9.2.7) member function if it is attached to the global module". C++20 **[class.mfct]** (11.4.1) paragraph 1. Code that uses no C++20 modules, as in this course, is attached to the global module.

- So the ``get_speed`` of `A Body in the Class`_ is inline, and so is each constructor this course writes in the class: every source file that includes ``vehicle.hpp`` holds its body, which the rule of `One Definition in Many Files`_ allows.
- Each caller's compiler sees that body and can put it in place of the call. With g++ 13.3 ``-O2``, a call of this ``get_speed`` becomes one read of ``speed_``.
- With the body in ``vehicle.cpp`` instead, a call from another source file stays a call: that file's compiler sees only the declaration.
- The cost: changing a body in the class recompiles every file that includes the header.

.. _l8-inline-hint:

``inline`` Does Not Force Inlining
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Appendix frame iv, from `A Body in the Class`_.

- ``inline`` has two meanings. The first is the rule of `One Definition in Many Files`_: every source file may hold the same definition. The standard guarantees it.
- The second is a hint to replace each call with the function's body, called **inline substitution**. The compiler does not have to follow it:

.. note::

   "The inline specifier indicates to the implementation that inline substitution of the function body at the point of call is to be preferred to the usual function call mechanism. An implementation is not required to perform this inline substitution at the point of call". C++20 **[dcl.inline]** (9.2.7) paragraph 2.

- A method defined in its class is inline without the keyword: [class.mfct] in `A Method Defined in Its Class`_, and the note of [dcl.inline] paragraph 7.
- ``inline static int next_id_{1};`` (`One Counter for the Class`_) is an **inline variable** ([dcl.inline] paragraph 3): the same rule for a variable, so every source file that includes the header may hold the counter's definition.
- The compiler chooses: a call of the in-class ``get_speed`` becomes one read of ``speed_`` with g++ ``-O2``, and stays a call with ``-O0`` (no optimization), the Debug build.

const Objects
^^^^^^^^^^^^^

Appendix frames v to x, from `Accessors`_. A ``const`` **object** cannot change after its constructor ends.

What a ``const`` Object Cannot Do
"""""""""""""""""""""""""""""""""

Here ``car_a`` is a ``const Vehicle``, ``car_b`` a ``Vehicle``, and ``stop`` a ``const Position``.

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - It cannot
     - Example
     - g++ says
   * - change a data member, even a ``public`` one
     - ``stop.x = 5.0;``
     - ``assignment of member 'Position::x' in read-only object``
   * - call a method that is not ``const``
     - ``car_a.set_speed(12.0);``
     - ``passing 'const Vehicle' as 'this' argument discards qualifiers``
   * - take a new value as a whole
     - ``car_a = car_b;``
     - The same error: assignment is a method that is not ``const``.
   * - be reached through a plain reference
     - ``Vehicle& ref{car_a};``
     - ``binding reference of type 'Vehicle&' to 'const Vehicle' discards qualifiers``
   * - be reached through a plain pointer
     - ``Vehicle* ptr{&car_a};``
     - ``invalid conversion from 'const Vehicle*' to 'Vehicle*'``

- It can call its ``const`` methods, be read through a ``const&`` (the next sections) and be copied. The copy is a new object that is not ``const``: its ``set_speed(5.0)`` works, and ``car_a`` still reads 0. Its constructor ran when it was made, and its destructor runs at the end of its scope.
- Without the reference and pointer rows, code could change a ``const`` object through another name. The compiler refuses both.
- Run: ``702run week8_appendix vi``.

Calling a Mutator
"""""""""""""""""

.. code-block:: cpp

   // main.cpp
   const Vehicle logged_car{13.4, 12.0};
   std::cout << logged_car.get_speed() << '\n';  // 12
   logged_car.set_speed(10.0);  // does not compile

.. code-block:: text

   error: passing 'const Vehicle' as 'this' argument discards qualifiers [-fpermissive]

- ``set_speed`` is not ``const``, so it could change ``logged_car``: the compiler refuses the call.
- The error names ``this``, the pointer of `The this Pointer`_.
- Run: ``702run week8_appendix vii``.

.. _l8-const-ref:

Through a ``const`` Reference
"""""""""""""""""""""""""""""

.. code-block:: cpp

   // vehicle.hpp
   class Vehicle {
    public:
     double get_speed() { return speed_; }  // const left out
     // ...
    private:
     double max_speed_;     // m/s, greater than 0
     double speed_{0.0};    // m/s
     std::string color_;    // from the constructor
     double mileage_{0.0};  // m driven
   };

.. code-block:: cpp

   // main.cpp
   void show(const Vehicle& vehicle) {
     std::cout << vehicle.get_speed() << '\n';  // does not compile
   }

.. code-block:: text

   error: passing 'const Vehicle' as 'this' argument discards qualifiers [-fpermissive]

- A ``const Vehicle&`` parameter sees the object as ``const``, so the same rule applies. ``show`` of `A Conversion Nobody Asked For`_ compiles only because the accessors are ``const``.
- That is the reason for Con.2 (`Accessors`_): a method that changes nothing must say so, or no ``const&`` can call it.

Discussion: Will It Compile?
""""""""""""""""""""""""""""

.. code-block:: cpp

   // main.cpp
   void show(const Vehicle& vehicle);
   const Vehicle logged_car{13.4, 12.0};
   Vehicle car_a{13.4};

   double a{logged_car.get_speed()};  // 1
   logged_car.set_speed(5.0);         // 2
   show(car_a);                       // 3
   show(13.4);                        // 4
   Vehicle other_car;                 // 5
   Vehicle fast_car{13.4, 20.0};      // 6
   Vehicle copy_car{logged_car};      // 7
   car_a = logged_car;                // 8

- ``Vehicle`` is the class we wrote in `Live Coding: Step 5`_. Line by line: does it compile? For each line that does not, which rule stops it?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Compiles: ``get_speed`` is ``const``.
   2. Does not compile: ``set_speed`` is not ``const``, and ``logged_car`` is.
   3. Compiles: a non-``const`` object binds to a ``const`` reference.
   4. Does not compile: the constructor is ``explicit``.
   5. Does not compile: there is no default constructor.
   6. Compiles, then throws at run time: 20 is above 13.4, and with nothing to catch it the program stops (exit status 134).
   7. and 8. Compile: the copy constructor and the copy assignment, both written by the compiler. This ``Vehicle`` owns nothing by hand, so the compiler's copy is right: it copies each ``double``, and the ``std::string`` copies its own text. That is the rule of zero, in the :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>` reading.

   ``702run week8_appendix ix`` runs lines 1, 3, 7 and 8 with a copy of a ``Vehicle`` that has the speed members and the two constructors. The ``Vehicle`` of ``vehicle.hpp`` also has ``sensors_``, so it is move-only: with it, lines 7 and 8 do not compile.

Summary: const Objects
""""""""""""""""""""""

- A ``const`` object cannot change after its constructor ends: no data member can change, and no method that is not ``const`` can run on it.
- A plain reference or pointer cannot refer to it, so no other name can change it.
- A ``const&`` parameter sees the object as ``const`` too, so a method that changes nothing must be ``const`` (Con.2).
