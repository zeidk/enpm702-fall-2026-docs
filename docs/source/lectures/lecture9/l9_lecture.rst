====================================================
Lecture
====================================================

Learning Objectives
-------------------

1. Turn requirements into classes, and read a UML class diagram.
2. Put classes in a namespace.
3. Write association, aggregation, composition and dependency.
4. Derive a class from a base class, and call the base constructor.
5. Write ``virtual`` methods with ``override``, and a ``virtual`` destructor.
6. Write an abstract class, and use ``final``.

The `Further Reading`_ part, at the end of this page, is the appendix of the slides. It is not presented. Read it on your own.

.. _l9-upload-live-coding:

Upload Your Live Coding
^^^^^^^^^^^^^^^^^^^^^^^

You type Step 1 with me, in ``project/week9/live``. You write **Steps 2 to 5** on your own, in the time each step gives: 10 minutes for Steps 2, 3 and 4, and 5 for Step 5. Steps 6 and 7 are homework, not collected. In class, I walk around and help, but I do not show the answers: the recording would give them away. Get your workspace ready before class: follow :doc:`Setup Before Class </lectures/lecture8/l8_setup>` and run the script with the week number, ``bash ~/Downloads/enpm702_setup.sh 9``.

- **Before the end of class**, upload every file of ``live/include`` and ``live/src`` to the L9 Live Coding assignment on Canvas.
- It counts toward **Participation** (5% of the grade), as complete or incomplete. Complete means the code builds and you wrote Steps 2 to 5. I do not grade it for correctness.
- **No AI**: write the code yourself, with neither a chatbot nor the AI in VS Code (GitHub Copilot included), in class or after. Code written with AI gets **0**.
- **Watching the recording?** Upload before the next lecture, on **Nov 10**. The same rules apply.
- The finished code is posted after Nov 10, the deadline for those who watch the recording.

Code for This Lecture
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   project/week9/
   ├── CMakeLists.txt
   ├── playground/
   ├── live/
   ├── appendix/
   ├── common/
   ├── undefined/
   └── uml/

**live** holds the classes you write in the Live Coding steps: ``live9`` builds and runs them. Load it in class with ``source ~/Downloads/enpm702_setup.sh``, as :doc:`Setup Before Class </lectures/lecture8/l8_setup>` shows.

**Run a Slide's Code**

1. Get the code: ``git pull``.
2. In the top-level ``CMakeLists.txt`` (repository root), check that ``add_subdirectory(project/week9)`` is not commented out.
3. Configure: ``702configure``.
4. Build it: ``702build week9_playground``.
5. Run every slide: ``702run week9_playground``. Run only one slide, for example `Through a Base Reference`_: ``702run week9_playground 70``.

**Where the Classes Are**

- **common** holds every class of the diagram: ``Sensor``, ``SensorType``, ``Position`` and ``Route``, and today's ``Vehicle``, ``RoboTaxi``, ``Taxi``, ``Fleet`` and ``Passenger``. Each section file writes the earlier versions its slides need.
- The code with undefined behavior is in the **undefined** folder, built with AddressSanitizer. It runs only when you ask for its slide by number.
- **uml** holds the PlantUML file of the diagram.
- The code of the appendix is in the **appendix** folder. Run appendix frame xi with ``702run week9_appendix xi``.

.. dropdown:: How to Run the Code
   :icon: terminal
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The ``702`` commands come from ``enpm702-cpp.sh`` in the repository. Its top comment shows how to load them in every new terminal. Then:

   .. code-block:: bash

      enpm702                            # go to the repository, load the 702 commands
      git pull                           # get this week's code
      702rebuild                         # once after you pull: a fresh build/
      702run week9_playground            # the code of every slide, in order
      702run week9_playground 70         # only the code of slide 70
      702run week9_appendix xi           # only appendix frame xi (11 works too)
      live9                              # build and run the classes you write in class

   After you edit a file, build again before you run: ``702build week9_playground`` builds one program, ``702build`` builds all of them.

   Code that does not compile is in the programs, commented out: uncomment it to get the slide's error.

   The slide whose code has undefined behavior, slide 80, runs only when you ask for it by number: ``702run week9_playground 80``. A full run skips it.

One Class per File
^^^^^^^^^^^^^^^^^^

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. code-block:: text

         live/
         ├── include/
         │   ├── vehicle.hpp
         │   ├── sensor.hpp
         │   ├── automation_level.hpp
         │   ├── route.hpp
         │   ├── position.hpp
         │   ├── passenger.hpp
         │   ├── fleet.hpp
         │   ├── robotaxi.hpp
         │   └── taxi.hpp
         └── src/
             ├── vehicle.cpp
             ├── sensor.cpp
             ├── route.cpp
             ├── passenger.cpp
             ├── fleet.cpp
             ├── robotaxi.cpp
             ├── taxi.cpp
             └── main.cpp

   .. grid-item::

      - Each class has a header, with its declaration, and a source file, with its method bodies, both named after the class. ``Position``, a ``struct`` with no method, and ``AutomationLevel``, an enumeration, have only a header.
      - ``Vehicle``, ``Sensor``, ``AutomationLevel``, ``Route`` and ``Position`` are given: you read them, you do not write them. You write the other four.
      - You find a class by its file name. A change to a class's header recompiles only the files that include it; a change to its ``.cpp`` recompiles that file alone: a change to ``taxi.cpp`` recompiles only ``taxi.cpp``.
      - A derived class gets its own files too: ``robotaxi.hpp`` includes ``vehicle.hpp``, because ``RoboTaxi`` needs its base. ``vehicle.hpp`` includes none of its derived classes: a base class does not know the classes derived from it.
      - So a new kind of vehicle adds two files and changes no other class. ``CMakeLists.txt`` names every source file, so it gains the new ``.cpp``, and ``main.cpp`` changes if it makes the new vehicle.
      - ``main.cpp`` includes the headers it uses.

.. admonition:: Why one class per file
   :class: important

   Each class has a header and a source file, named after it. A change to a class's header recompiles only the files that include it, and a change to its ``.cpp`` recompiles that file alone. A new kind of vehicle adds two files and one line in ``CMakeLists.txt``, and changes no other class.

One Namespace: ``fleet``
^^^^^^^^^^^^^^^^^^^^^^^^

Every class of the program is in the namespace ``fleet``. ``Vehicle``, ``Route`` and ``Sensor`` are common names: a library with its own ``Vehicle`` would clash with ours. g++ then says ``redefinition of 'class Vehicle'``.

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      ``route.hpp``

      .. code-block:: cpp

         namespace fleet {
         class Route {
          public:
           void add(Position waypoint);
           double length() const;
          private:
           // ...
         };
         }  // namespace fleet

   .. grid-item::

      ``route.cpp``

      .. code-block:: cpp

         namespace fleet {
         void Route::add(Position waypoint) {
           waypoints_.push_back(waypoint);
         }
         }  // namespace fleet

      or

      .. code-block:: cpp

         void fleet::Route::add(Position waypoint) {
           waypoints_.push_back(waypoint);
         }

- The header puts the class inside ``namespace fleet``. The source file opens ``fleet`` again and defines the methods there. Or it names the namespace in front of each method, ``fleet::Route::add``. After that name, the compiler looks in ``Route`` and then in ``fleet``, so ``Position`` needs no prefix. Every file of ``project/week9/common`` does the same, and so does every file of the live code. The comment after the last brace says which brace closes the namespace.
- Inside the namespace, ``Route`` uses ``Position`` with no prefix: both are in ``fleet``.
- Outside ``fleet``, as in ``live/src/main.cpp``, write ``fleet::Route``. The listings on this page leave ``fleet::`` out.

.. admonition:: Namespaces are lowercase
   :class: important

   ``fleet``, not ``Fleet``: classes start with a capital, so the namespace and the class ``Fleet`` never clash. "Namespace names are snake_case (all lowercase, with underscores between words)". Rule: `Google C++ Style Guide <https://google.github.io/styleguide/cppguide.html#Namespace_Names>`_.

Warm-Up
-------

Before the new material, a check on what you already know.

Discussion: Improve This Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class Vehicle {
    public:
     Vehicle(double max_speed, std::string color = "white") {
       max_speed_ = max_speed;
       color_ = color;
     }
     double& get_speed() { return speed_; }
     std::string get_color() { return color_; }
     void set_speed(double speed) { speed_ = speed; }

    private:
     double max_speed_;
     double speed_;
     std::string color_;
   };

It compiles with no warning. It is neither safe nor efficient. With what you already know, find at least nine changes, and say why.

- Work in pairs for three minutes: find every line you would change, and say what goes wrong without the change.
- Hints, if you are stuck: what does ``Vehicle car_a = 13.4;`` do? What is the speed of a new car? Can you call ``get_speed`` on a ``const Vehicle&``?

Owners Keep Objects Alive
^^^^^^^^^^^^^^^^^^^^^^^^^

An **owner** of an object decides when the object is destroyed. While at least one owner holds the object, the object stays alive. "Keeps it alive" means "is one of its owners".

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. code-block:: cpp

         auto car_a{std::make_unique<Vehicle>(13.4)};
         auto car_b{std::make_shared<Vehicle>(13.4)};
         auto copy_b{car_b};  // a second owner
         std::weak_ptr<Vehicle> watcher{car_b};
         std::cout << std::boolalpha << car_b.use_count()
                   << ' ' << watcher.expired() << '\n';
         car_b.reset();
         copy_b.reset();  // the last owner lets go
         std::cout << watcher.expired() << '\n';

   .. grid-item::

      .. code-block:: text

         2 false
         true

- ``car_a`` is the only owner of its ``Vehicle``: a ``std::unique_ptr`` cannot be copied, so its object has one owner.
- ``car_b`` and ``copy_b`` own one ``Vehicle`` together. Each copy of a ``std::shared_ptr`` is one more owner, so ``use_count()`` is 2. ``watcher``, a ``std::weak_ptr``, only observes the object: it does not count, and ``expired()`` is false while an owner remains.
- After ``car_b.reset()`` the ``Vehicle`` lives on, because ``copy_b`` still owns it. After ``copy_b.reset()``, the last owner has let go: the ``Vehicle`` is destroyed and ``expired()`` is true.
- Composition has one owner, aggregation shares ownership, and association and dependency own nothing. Run it with ``702run week9_playground 5``.

The Program We Will Build
-------------------------

.. figure:: /_static/images/l9/model_full.png
   :alt: A UML class diagram of the ride service program, with class names only, in ten boxes; every box and line is black. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. Vehicle, its name in italics, is in the middle. On the left, Fleet joins Vehicle by a line with an open diamond at Fleet, labeled holds, 1 at Fleet and 0..* at Vehicle; below it, Passenger has an arrow labeled rides to Vehicle, 0..* at Passenger and 0..1 at Vehicle. To the upper right, Sensor joins Vehicle by a line with a filled diamond at Vehicle, labeled owns, 1 at Vehicle and 0..* at Sensor; an arrow labeled has type runs from Sensor to SensorType, marked enumeration, at the far upper right, with 1 at SensorType. To the right, a dashed arrow labeled uses runs from Vehicle to Route, and Route joins Position, marked struct, by a line with a filled diamond at Route, labeled has, 1 at Route and 0..* at Position. Lower right, RoboTaxi and Taxi, both marked final, each have a line with a hollow triangle at Vehicle. An arrow labeled has level runs from RoboTaxi to AutomationLevel, marked enumeration, at its right, with 1 at AutomationLevel.
   :align: center
   :width: 100%

   The ride service program as a UML class diagram: the whole program.

- A box is a class, a line is a relationship: today's lecture says what each kind of line means. Later copies show the part being built in orange.
- This is the class diagram of the whole program, with nothing in grey. We already wrote ``Vehicle``, its ``Sensor``\ s, ``Position`` and a small ``Route``.
- Today you write the rest: ``Passenger`` with me, then ``Fleet``, ``RoboTaxi`` and ``Taxi`` on your own, and we name each kind of line between the boxes. ``Vehicle`` changes too: by the end, its ``drive`` is abstract, which is why its name is in italics.
- The diagram comes back at the start of each part, with the piece we are about to build in orange.

Requirements
------------

A **requirement** is a statement of a need the program must meet, with the constraints and conditions that come with it (ISO/IEC/IEEE 29148). See :doc:`L9 Requirements <l9_requirements>`.

Four Kinds of Requirement
^^^^^^^^^^^^^^^^^^^^^^^^^

- A **functional** requirement says what the program does: "a Fleet adds and removes vehicles".
- A **non-functional** requirement says how well it does it: "reading one sensor takes at most 50 ms".
- A **constraint** limits the choices: "the code is C++20".
- A **success criterion** says how we check the result: "every test passes".

The ride service program has twelve functional requirements, FR-1 to FR-12. Today's code uses seven of them: FR-3, FR-4, FR-5, FR-9, FR-10, FR-11 and FR-12. See :doc:`L9 Requirements <l9_requirements>`.

Design
------

A **design** defines the parts of a program and the interfaces between them (ISO/IEC/IEEE 24765). In C++, the parts are classes: the design says what each class holds and does, and how the classes are connected. It comes before the code.

See :doc:`L9 Design <l9_design>`, and `OMG: Unified Modeling Language <https://www.omg.org/spec/UML/>`__.

From Requirements to Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nouns and Classes
""""""""""""""""""

Today's code meets seven requirements. Read each one for its nouns and its verbs. The program shall:

- **FR-3**: let each kind of vehicle, a RoboTaxi or a Taxi, drive in its own way.
- **FR-4**: give each RoboTaxi one or more Sensors.
- **FR-5**: let a Vehicle follow a Route.
- **FR-9**: let a Route be built from several waypoints.
- **FR-10**: let a Fleet add and remove vehicles.
- **FR-11**: let a driver be assigned to a Taxi and removed from it.
- **FR-12**: let a Passenger board and leave a vehicle.

Then:

- A **noun** that holds data and keeps a rule (an **invariant**, such as a speed from 0 to the maximum speed) becomes a class: Fleet (FR-10), Vehicle (FR-5), Sensor (FR-4), RoboTaxi and Taxi (FR-3), Passenger (FR-12).
- Route (FR-5, FR-9) is a class because it hides its waypoints behind ``add`` and ``length``.

See `Verbs and Links`_ and `Discussion: Find the Classes`_ under Further Reading.

UML Class Diagrams
^^^^^^^^^^^^^^^^^^

A **UML class diagram** is a drawing of a program's classes. Each box is a class: its name, then its data members, then its methods. Each line between two boxes is a relationship. UML is the Unified Modeling Language.

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - In the diagram
     - Means
   * - ``+`` ``-`` ``#``
     - ``public``, ``private``, ``protected`` (`protected Members`_)
   * - ``next_id_ : int``, underlined
     - Underlined: a ``static`` member
   * - ``drive(const Route&)``, in italics
     - In italics: an abstract method, with no body in this class (`Pure virtual Methods`_)
   * - ``Vehicle``, a class name in italics
     - An abstract class, which has an abstract method
   * - C, A or E in a circle, before a class name
     - PlantUML's mark, not UML's: C a class, A an abstract class, E an enumeration (UML marks an abstract class with italics)
   * - «struct», «enumeration»
     - A **stereotype**: what kind of type the box is, a ``struct`` or an ``enum class``
   * - «final»
     - No class derives from this one (`Live Coding: Step 7`_)
   * - ``-ride_  0..1`` at a line's end
     - The data member that holds the class at that end, as in the box, and how many (`Multiplicity`_)

The Class Diagram, with Every Member
""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_full_members.png
   :alt: A UML class diagram of the ride service program with ten boxes, each listing its data members and methods, and the line ends also name the data member that holds the class at that end; every box and line is black. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. In the middle, Vehicle, its name in italics, with the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the left, Fleet with minus vehicles_ : vector of shared_ptr of Vehicle, plus add(shared_ptr of Vehicle) : void, plus remove(int) : bool, plus size() : size_t; a line labeled holds with an open diamond at Fleet joins it to Vehicle, 1 to 0..*, the Vehicle end named minus vehicles_. Below it, Passenger with minus name_ : string, minus ride_ : weak_ptr of Vehicle, plus Passenger(string), plus board(shared_ptr of Vehicle) : void and plus leave() : void; an arrow labeled rides runs to Vehicle, 0..* to 0..1, the Vehicle end named minus ride_. Top right, Sensor with minus id_ : int, minus type_ : SensorType, minus range_ : double, plus Sensor(int, SensorType = lidar, double = 100.0), plus get_id() : int, plus get_type() : SensorType and plus get_range() : double; a line labeled owns with a filled diamond at Vehicle joins them, 1 to 0..*, the Sensor end named minus sensors_. an arrow labeled has type runs from Sensor to SensorType, marked enumeration, at the far right, with lidar, camera and radar, the SensorType end named minus type_ with 1. A dashed arrow labeled uses runs from Vehicle to Route, with minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double; a line labeled has with a filled diamond at Route joins Route to Position, marked struct, with plus x : double and plus y : double, 1 to 0..*, the Position end named minus waypoints_. Lower right, RoboTaxi, marked final, with minus operating_zone_ : string, minus automation_level_ : AutomationLevel, plus RoboTaxi(double, string = "College Park", AutomationLevel = level_4), plus get_operating_zone() : const string&, plus get_automation_level() : AutomationLevel, plus change_zone(string) : void and plus drive(const Route&) : void; an arrow labeled has level runs from it to AutomationLevel, marked enumeration, at the far right, with level_0 to level_5, the AutomationLevel end named minus automation_level_ with 1. Below RoboTaxi, Taxi, marked final, with minus driver_name_ : string, plus Taxi(double, string), plus assign_driver(string) : void and plus drive(const Route&) : void. RoboTaxi and Taxi each join Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   The same nine boxes as `The Program We Will Build`_, with their members.

- Read one box, ``Vehicle``: the name on top, in italics, which means abstract; then the data members, each ``name : type``; then the methods.
- A minus sign is ``private``, a plus sign ``public``. ``next_id_`` is underlined: a ``static`` member. ``drive`` is in italics too: a pure ``virtual`` method, which `Abstraction`_ explains.
- Every member here is in ``project/week9/common``, with the same name.

.. admonition:: Write the classes from the diagram
   :class: important

   You should be able to write every class from this diagram alone. So the design deserves the effort: what the diagram leaves out, the programmer guesses.

:doc:`L9 Design <l9_design>` explains every class and every line of this diagram, with the requirements each one meets.

Tools
"""""

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Tool
     - Cost
     - How you make a diagram
   * - PlantUML
     - Free, open source
     - You write a text file; the tool draws it. Used in this course, through its VS Code extension.
   * - Mermaid
     - Free, open source
     - You write text inside a Markdown file; GitHub draws it on the page.
   * - draw.io (diagrams.net)
     - Free
     - You draw the boxes and lines by hand, in a browser or a desktop app.
   * - StarUML, Visual Paradigm, Lucidchart
     - Paid, each with a free version or trial
     - You draw by hand; some also write C++ classes from the diagram.

- A diagram kept as text goes into git like code: ``git diff`` shows what changed in it.

Multiplicity
""""""""""""

**Multiplicity** is the numbers at an end of a line: how many objects of that end's class take part, for one object of the class at the other end.

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Written
     - How many
   * - ``1``
     - exactly one
   * - ``0..1``
     - zero or one
   * - ``*`` or ``0..*``
     - any number
   * - ``1..*``
     - at least one

An end with no number leaves the count open.

.. figure:: /_static/images/l9/multiplicity_examples.png
   :alt: Four lines of the class diagram, with class names only. Passenger has an arrow to Vehicle, labeled rides, with 0..* at Passenger and -ride_ and 0..1 at Vehicle. Fleet joins Vehicle by a line with an open diamond at Fleet, labeled holds, with 1 at Fleet and -vehicles_ and 0..* at Vehicle. Vehicle joins Sensor by a line with a filled diamond at Vehicle, labeled owns, with 1 at Vehicle and -sensors_ and 0..* at Sensor. Route joins Position by a line with a filled diamond at Route, labeled has, with 1 at Route and -waypoints_ and 0..* at Position.
   :width: 80%
   :align: center

A Diagram as Text
"""""""""""""""""

Two boxes of the design, in PlantUML:

.. code-block:: text

   @startuml
   !theme mono
   class Route {
     - waypoints_ : vector<Position>
     + add(Position) : void
     + length() : double
   }
   class Position <<struct>> {
     + x : double
     + y : double
   }
   Route "1" *-- "-waypoints_ 0..*" Position : has
   @enduml

- A class is written like a C++ class, with UML's ``+``, ``-`` and ``: type``.
- A line is written between two class names: ``-->`` is an arrow, ``o--`` an open diamond, ``*--`` a filled diamond, ``<|--`` a hollow triangle, ``..>`` a dashed arrow.
- The VS Code extension draws the file as you type (``Alt+D``).
- The whole diagram is ``project/week9/uml/robotaxi_model.plantuml``.

.. note::

   The PlantUML source of the UML diagrams on the slides is in `project/week9/uml <https://github.com/zeidk/enpm702-fall-2026-cpp/tree/main/project/week9/uml>`__. See `PlantUML: class diagrams <https://plantuml.com/class-diagram>`__.


Class Relationships
-------------------

A **class relationship** says how the objects of two classes are connected: one knows or uses the other, one holds the other, or one is a kind of the other.

Six Relationships
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 16 14 20 28 22

   * - Relationship
     - Read it as
     - UML line
     - In C++
     - In the design
   * - Association
     - knows
     - Arrow to the class it knows
     - A pointer that does not own, here a ``std::weak_ptr`` member
     - Passenger rides Vehicle
   * - Aggregation
     - has, shared
     - Open diamond at the whole
     - A ``std::shared_ptr`` member
     - Fleet holds Vehicles
   * - Composition
     - has, owned alone
     - Filled diamond at the whole
     - A ``std::unique_ptr``, or a plain member
     - Vehicle owns Sensors
   * - Dependency
     - uses for a call
     - Dashed arrow
     - A parameter, no member
     - Vehicle uses Route
   * - Inheritance
     - is a
     - Hollow triangle at the base
     - ``class RoboTaxi : public Vehicle``
     - RoboTaxi is a Vehicle
   * - Realization
     - implements
     - Dashed line, hollow triangle at the interface
     - A ``public`` base with only pure ``virtual`` methods
     - Not in this design: an ``ElectricTaxi`` implements ``Chargeable``

- The first five are in the design, and each has its own part below. Realization is the dashed version of the inheritance line: a class implements an interface, a list of methods with no data. C++ has no ``interface`` keyword, so the interface is a class with only pure ``virtual`` methods. ``Vehicle`` has data, so ``RoboTaxi`` and ``Taxi`` inherit; they do not realize.
- You have seen three of them on the owner map of smart pointers: a filled diamond for ``std::unique_ptr``, an open diamond for ``std::shared_ptr``, an arrow for ``std::weak_ptr``.

Choosing a Relationship and Its C++
"""""""""""""""""""""""""""""""""""

``A`` and ``B`` are two classes of the design. Answer about the design, from the top:

.. figure:: /_static/images/l9/decide_relationship.png
   :alt: A UML activity diagram that starts at a circle. A diamond asks: is an A a kind of B? Yes leads to the box Inheritance: class A : public B; RoboTaxi is a Vehicle. No leads to a diamond: does A use B without keeping it? Yes leads to the box Dependency: a const B& parameter; Vehicle uses a Route. No leads to a diamond: can B exist without A? No leads to the box Composition: std::unique_ptr<B>, or a B member; Vehicle owns its Sensors. Yes leads to a diamond: must A keep B alive? Yes leads to the box Aggregation: std::shared_ptr<B>; Fleet holds Vehicles. No leads to the box Association: std::weak_ptr<B>; Passenger rides a Vehicle. The five paths join and end at a ringed circle.
   :align: center
   :width: 100%

   Four questions about the design lead to a relationship and the C++ that implements it.

Every question is about the design, not about code that already exists.

1. Is an ``A`` a kind of ``B``? A ``RoboTaxi`` is a ``Vehicle``, so inheritance: ``class RoboTaxi : public Vehicle``.
2. If not: does ``A`` use ``B`` without keeping it? A ``Vehicle`` uses a ``Route`` while it drives and keeps nothing of it afterwards, so dependency: a ``const Route&`` parameter of ``drive``.
3. If ``A`` keeps ``B``: can ``B`` exist without ``A``? A ``Sensor`` is part of its ``Vehicle`` and goes with it, so composition: ``std::unique_ptr``, or a plain member as for a ``Route``'s ``Position`` values.
4. If ``B`` lives on its own: must ``A`` keep it alive? The ``Fleet`` must, so aggregation: ``std::shared_ptr``. A ``Passenger`` must not: FR-12.3 says boarding does not keep a vehicle alive, so association: ``std::weak_ptr``.

See `Discussion: Which Relationship?`_ under Further Reading.

Association
^^^^^^^^^^^

An **association** is a relationship between two classes whose objects can be linked: an object of one class refers to an object of the other, in one direction or in both. In this course, neither object owns the other: each is created and destroyed on its own.

.. list-table::
   :widths: 50 50

   * - **One-way**: an arrow. Only the class at the tail has a member.

       .. image:: /_static/images/l9/association_one_way.png
          :alt: Two one-way associations, each a line with an open arrowhead. Passenger points to Vehicle, with -ride_ and 0..1 at the Vehicle end. Reader points to LibraryBook, with -borrowed_ and 0..* at the LibraryBook end.
          :width: 100%
     - **Two-way**: no arrows. Each class has a member.

       .. image:: /_static/images/l9/association_two_way.png
          :alt: Two two-way associations, each a plain line with no arrowheads. Student and Course, with -students_ and 0..* at the Student end and -courses_ and 0..* at the Course end. Doctor and Patient, with -doctor_ and 0..1 at the Doctor end and -patients_ and 0..* at the Patient end.
          :width: 100%

- UML 2.5.1 (`11.5.4 <https://www.omg.org/spec/UML/2.5.1/PDF>`__) lets a diagram hide some arrows. This course uses one of its options: "Suppress arrows for Associations with navigability in both directions, and show arrows only for Associations with one-way navigability".
- A passenger rides a vehicle: the vehicle exists before the ride and after it, and so does the passenger. ``Passenger`` has a member ``ride_`` that refers to its ``Vehicle``; ``Vehicle`` has no member for its passengers, so the association is one-way.
- The definition holds in both directions: an object of one class refers to an object of the other. It does not say that both must refer to each other.
- UML counts aggregation and composition as associations too, with a whole and its parts.

Passenger and Vehicle in the Class Diagram
""""""""""""""""""""""""""""""""""""""""""

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::
      :columns: 12 12 4 4
      :child-direction: column
      :child-align: center

      .. image:: /_static/images/l9/model_l9_association_only.png
         :alt: A UML class diagram with only two boxes, Passenger and Vehicle, both light orange with dark orange lines. Passenger has a circled C, for a class, and Vehicle, in italics, a circled A, for an abstract class. An orange arrow labeled rides runs from Passenger to Vehicle, with 0..* at Passenger and 0..1 at Vehicle.
         :align: center
         :width: 100%

   .. grid-item::
      :columns: 12 12 8 8

      .. image:: /_static/images/l9/decide_relationship_association.png
         :alt: The decision chart of Choosing a Relationship, with the path to Association highlighted: the four questions on the path and the answers taken are dark orange and bold, and the Association box is light orange. Is an A a kind of B? No. Does A use B without keeping it? No. Can B exist without A? Yes. Must A keep B alive? No. That leads to the box Association: std::weak_ptr<B>; Passenger rides a Vehicle. Each branch ends at its box. The other four boxes show only their names, Inheritance, Dependency, Composition and Aggregation, in black, and all arrows are black.
         :align: center
         :width: 100%

- A ``Passenger`` rides a ``Vehicle``: the arrow labeled ``rides``. The chart's answers lead to association: a passenger is not a kind of vehicle, keeps it, the vehicle exists without the passenger, and the passenger need not keep it alive.
- The first new class is ``Passenger``, and the first kind of line is the plain arrow between ``Passenger`` and ``Vehicle``.
- A ``Sensor`` has a ``SensorType``: an association too. ``type_`` is a plain ``SensorType`` member, not a pointer: an enumeration value is copied.
- After the full boxes, we write the class and check in a run that a passenger never keeps the vehicle alive.

A Passenger Rides a Vehicle
"""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_association_members.png
   :alt: A UML class diagram with only two boxes, Passenger on the left and Vehicle on the right, each listing its data members and methods; both boxes and the arrow are orange. Each class name has a circled letter before it: C for a class, on Passenger, and A for the abstract Vehicle. Passenger has minus name_ : string, minus ride_ : weak_ptr of Vehicle, plus Passenger(string), plus board(shared_ptr of Vehicle) : void and plus leave() : void. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. An arrow labeled rides runs from Passenger to Vehicle, 0..* at Passenger and 0..1 at Vehicle, the Vehicle end named minus ride_.
   :align: center
   :width: 100%

   ``Passenger`` and ``Vehicle`` with every member: the arrow labeled ``rides``, its ``Vehicle`` end named ``-ride_``.

- ``0..1`` at ``Vehicle``: a passenger rides at most one vehicle, so ``ride_`` is one ``std::weak_ptr``, not a container. ``0..*`` at ``Passenger`` needs no member: the arrow is one-way.
- The same two boxes as in `Passenger and Vehicle in the Class Diagram`_, with every member. ``Passenger`` is what we write in Step 1: a name, a constructor, ``board`` and ``leave``.
- ``ride_`` is in ``Passenger``'s box, with its type, ``std::weak_ptr<Vehicle>``. Its name is at the ``Vehicle`` end of the arrow too: the line says which data member holds the vehicle.
- ``Vehicle``'s box is the class you are given, in ``vehicle.hpp`` and ``vehicle.cpp``, with the id and the static counter ``next_id_``. ``drive`` is in italics: `Abstraction`_ makes it pure ``virtual``. Step 1 does not touch ``Vehicle``.

Choosing the Type of ``ride_``
""""""""""""""""""""""""""""""

:ref:`FR-12.3 <fr-12-3>`: "Boarding shall not keep a vehicle alive". The company can retire a car during a ride. Three types could hold the car in ``ride_``:

.. list-table::
   :header-rows: 1
   :widths: 24 22 38 16

   * - Type of ``ride_``
     - Keeps the car alive?
     - After the car is destroyed
     - FR-12.3
   * - ``std::shared_ptr<Vehicle>``
     - Yes: the passenger is an owner
     - The car is never destroyed while the passenger rides
     - Broken
   * - ``Vehicle*``
     - No
     - The pointer dangles: the code cannot tell, and reading through it is undefined behavior
     - Met, unsafely
   * - ``std::weak_ptr<Vehicle>``
     - No
     - ``expired()`` is true, and ``lock()`` gives an empty pointer
     - Met

- A ``std::shared_ptr`` makes Maya an owner: a car the company retires would live on as long as Maya rides.
- A plain pointer owns nothing, but when the car is destroyed it still holds the old address. The code cannot tell, and reading through it is undefined behavior.
- A ``std::weak_ptr`` owns nothing and can tell. That is why ``ride_`` is a ``std::weak_ptr``. `Two Separate Lifetimes`_ runs it.
- A plain pointer is safe only when the object it points to surely outlives the pointer. If a ``Sensor`` kept a pointer to the ``Vehicle`` that owns it, that pointer could be plain.

Two Separate Lifetimes
""""""""""""""""""""""

.. code-block:: cpp

   auto car_a{std::make_shared<Vehicle>(13.4)};
   Passenger maya{"Maya"};
   std::cout << car_a.use_count() << '\n';
   maya.board(car_a);
   std::cout << car_a.use_count() << '\n';
   std::weak_ptr<Vehicle> watcher{car_a};
   car_a.reset();  // the only owner lets go
   std::cout << std::boolalpha
             << watcher.expired() << '\n';
   maya.leave();   // maya's ride_ has expired

.. code-block:: text

   1
   1
   true

- ``13.4`` is 13.4 m/s, the maximum speed (about 30 mph).
- ``watcher`` is a second ``std::weak_ptr``, only for the check: ``expired()`` is true once the ``Vehicle`` object is destroyed.

.. admonition:: Conclusion
   :class: tip

   ``use_count()`` stays 1 after ``board``: ``maya``'s ``std::weak_ptr`` is not an owner. When the only owner lets go, the ``Vehicle`` object is destroyed, although ``maya`` still refers to it. FR-12.3 allows it, and ``ride_`` can tell that the car is gone, where a plain pointer could not.

- The type follows a requirement, not the real world: :ref:`FR-12.3 <fr-12-3>` says boarding shall not keep a vehicle alive. In C++, an owner is whoever decides when an object is destroyed, nothing more.
- A ``std::shared_ptr`` would make ``maya`` an owner: the car could not be destroyed while maya holds it, even after the fleet removes it. That breaks FR-12.3: a car outside the fleet, still carrying a passenger.
- Could ``remove`` check ``use_count()`` and refuse when it is above 1? The count counts every owner, not passengers. In Step 2, ``car_b.use_count()`` is 2 just before ``remove``, with no passenger: ``main`` holds one copy and the fleet the other.
- A plain pointer or a reference does not own the car either, but it cannot tell when the car is destroyed: the next use reads freed memory. A ``std::weak_ptr`` refers to the car without owning it, and it can check first.
- Run: ``702run week9_playground 25``.

See `Before reset, in Memory`_ and `After reset, in Memory`_ under Further Reading.

Two Headers That Include Each Other
"""""""""""""""""""""""""""""""""""

If ``A`` refers to a ``B`` and the ``B`` refers back to its ``A``, the association is two-way, and each header would include the other.

.. code-block:: cpp
   :caption: a.hpp

   // a.hpp
   #pragma once
   #include "b.hpp"
   class A {
     // ...
    private:
     B* b_;
   };

.. code-block:: cpp
   :caption: b.hpp
   :linenos:

   // b.hpp
   #pragma once
   #include "a.hpp"
   class B {
     // ...
    private:
     A* a_;
   };

A ``main.cpp`` that includes ``a.hpp`` first stops with this error, the only one (g++ 13.3):

.. code-block:: text

   b.hpp:7:3: error: 'A' does not name a type

- ``a.hpp`` includes ``b.hpp``, which includes ``a.hpp`` again. ``#pragma once`` skips that copy, so ``B`` is compiled before ``A`` is declared.
- The code is in ``project/week9/cycle``. This version, with its errors, is in a comment in ``project/week9/CMakeLists.txt``.

A Forward Declaration Breaks the Cycle
""""""""""""""""""""""""""""""""""""""

A **forward declaration** is a class's name only, with no body: ``class B;``. As a function declaration lets two functions call each other, it lets two classes refer to each other.

.. code-block:: cpp
   :caption: a.hpp

   // a.hpp
   #pragma once
   class B;  // the name only
   class A {
     // ...
    private:
     B* b_;
   };

.. code-block:: cpp
   :caption: b.hpp

   // b.hpp
   #pragma once
   class A;  // the name only
   class B {
     // ...
    private:
     A* a_;
   };

- The ``#include "a.hpp"`` moves to ``b.cpp``: its ``link`` calls ``a->set_b(this)``, and a call needs the full class. Without the ``#include``, g++ stops there with "invalid use of incomplete type".
- ``// ...`` stands for each class's ``public`` method, ``set_b`` and ``link``. The files in ``project/week9/cycle`` have them.
- A pointer or a reference member needs only the name. A by-value member or a call needs the full class.
- Run: ``702run week9_cycle``. It prints ``built``.

Live Coding: Step 1
"""""""""""""""""""

**10 minutes, in class, with me.** The instructions are on the slides.

See `Step 1: A Passenger Rides a Vehicle`_ under Further Reading.

Aggregation
^^^^^^^^^^^

An **aggregation** is an association between a whole and its parts: the **whole** is an object that groups other objects, its **parts**. A ``Fleet`` is a whole, and its vehicles are its parts. The whole does not own its parts alone: a part can exist before the whole, after it, and in more than one whole.

- How it differs from a plain association: a plain association has no whole and no parts, and neither object keeps the other alive. Here the whole is one of the owners: a ``Fleet`` keeps its vehicles alive.
- In UML, a line with an open diamond at the whole. A vehicle can move from one fleet to another, and it is not scrapped when a fleet closes.

.. note::

   "Precise semantics of shared aggregation varies by application area and modeler" (`UML 2.5.1 <https://www.omg.org/spec/UML/2.5.1/PDF>`__, 9.5.3). In this course, an aggregation is a whole that shares ownership of its parts. Other books draw the line elsewhere: when you read one, check what it means by the open diamond.

Fleet and Vehicle in the Class Diagram
""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_aggregation.png
   :alt: The same UML class diagram of the ride service program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi, Taxi and AutomationLevel, joined by the same lines, and RoboTaxi to AutomationLevel by an arrow labeled has level. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. Fleet, Vehicle and the line labeled holds between them, with its open diamond at Fleet, 1 at Fleet and 0..* at Vehicle, are orange; everything else is grey.
   :align: center
   :width: 100%

   A ``Fleet`` holds ``Vehicle`` objects: the line labeled ``holds``, with its open diamond.

- The open diamond sits at ``Fleet``, the whole. One fleet holds any number of vehicles.
- The diamond is open because the fleet shares its vehicles with the rest of the program. Compare the filled diamond between ``Vehicle`` and ``Sensor``, in `Composition`_.

A Fleet Holds Vehicles
""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_aggregation_members.png
   :alt: A UML class diagram with only two boxes, Fleet on the left and Vehicle on the right, each listing its members; both boxes and the line are orange. Each class name has a circled letter before it: C for a class, on Fleet, and A for the abstract Vehicle. Fleet has minus vehicles_ : vector of shared_ptr of Vehicle, plus add(shared_ptr of Vehicle) : void, plus remove(int) : bool and plus size() : size_t. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. A line labeled holds joins them, with an open diamond at Fleet; 1 is above the line next to the diamond, and minus vehicles_ 0..* is under the line at Vehicle.
   :align: center
   :width: 100%

   ``Fleet`` and ``Vehicle`` with every member: the line labeled ``holds``, its ``Vehicle`` end named ``-vehicles_``.

- ``0..*`` at ``Vehicle``: a fleet holds any number of vehicles, so ``vehicles_`` is a ``std::vector``, with one ``std::shared_ptr<Vehicle>`` per vehicle.
- The same two boxes as in `Fleet and Vehicle in the Class Diagram`_, with every member. In Step 2, the class ``Fleet`` is given, and you write the bodies of ``add``, ``remove`` and ``size``.
- ``vehicles_`` is in ``Fleet``'s box, with its type, a ``std::vector`` of ``std::shared_ptr<Vehicle>``. Its name is at the ``Vehicle`` end of the line too.
- ``Vehicle``'s box does not change in Step 2. ``Fleet`` needs only ``get_id``, to remove a vehicle by its id.

Shared Ownership Needs std::shared_ptr
""""""""""""""""""""""""""""""""""""""

:ref:`FR-10.5 <fr-10-5>`: "A vehicle removed from the Fleet, or whose Fleet is destroyed, shall stay usable by the rest of the program". Three types could hold each vehicle in ``vehicles_``:

.. list-table::
   :header-rows: 1
   :widths: 24 22 38 16

   * - Element of ``vehicles_``
     - Keeps the vehicle alive?
     - After the fleet lets go
     - FR-10.5
   * - ``std::unique_ptr<Vehicle>``
     - Yes, alone: the fleet is the only owner
     - The vehicle is destroyed with the fleet, or when it is removed
     - Broken
   * - ``Vehicle*``
     - No
     - The vehicle lives on. When its last owner lets go, the pointer dangles
     - Met, unsafely
   * - ``std::shared_ptr<Vehicle>``
     - Yes: the fleet is one of the owners
     - The vehicle lives while any other owner holds it
     - Met

- A ``Vehicle`` held by value is owned by the fleet alone, as with ``std::unique_ptr``: that is composition.
- Several owners share each vehicle, and the vehicle lives while any of them holds it. Only ``std::shared_ptr`` counts owners. `The Vehicles Outlive the Fleet`_ runs it.

See `Requirements, Not Reality`_ under Further Reading.

The Vehicles Outlive the Fleet
""""""""""""""""""""""""""""""

.. code-block:: cpp

   auto car_a{std::make_shared<Vehicle>(13.4)};
   auto car_b{std::make_shared<Vehicle>(13.4)};
   {
     Fleet fleet;
     fleet.add(car_a);
     fleet.add(car_b);
     std::cout << fleet.size() << ' '
               << car_a.use_count() << '\n';
     fleet.remove(car_b->get_id());
     std::cout << fleet.size() << ' '
               << car_b.use_count() << '\n';
   }  // the Fleet is destroyed here
   std::cout << car_a.use_count() << ' '
             << car_a->get_max_speed() << '\n';

.. code-block:: text

   2 2
   1 1
   1 13.4

- Inside the scope, ``car_a`` and the fleet share the first ``Vehicle``: 2 owners. ``remove`` lets go of the second one, and it lives on with 1 owner. So does the first, after the fleet is gone.
- The last line is the acceptance test of :ref:`FR-10.5 <fr-10-5>`: after the fleet is destroyed, a vehicle it held still answers ``get_max_speed()``.
- Run: ``702run week9_playground 33``.

Live Coding: Step 2
"""""""""""""""""""

**10 minutes, in class, on your own.** The instructions are on the slides.

Composition
^^^^^^^^^^^

A **composition** is an association between a whole and its parts, in which the whole owns its parts alone. Each part belongs to one whole and is destroyed with it.

- In aggregation, several owners share a part. Here one whole owns it alone and decides when it is destroyed.
- UML 2.5.1 (9.5.3): "If a composite object is deleted, all of its part instances that are objects are deleted with it".
- In UML, a line with a filled diamond at the whole. We already built one: a ``Vehicle`` owns its ``Sensor`` objects.

See `Aggregation or Composition`_ under Further Reading.

Two Compositions in the Class Diagram
"""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_composition.png
   :alt: The same UML class diagram of the ride service program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi, Taxi and AutomationLevel, joined by the same lines, and RoboTaxi to AutomationLevel by an arrow labeled has level. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. Vehicle, Sensor, Route and Position, the owns line between Vehicle and Sensor and the has line between Route and Position, with their filled diamonds and numbers, are orange; everything else is grey.
   :align: center
   :width: 100%

   A ``Vehicle`` owns its ``Sensor`` objects, and a ``Route`` has its ``Position`` values.

- Two filled diamonds. ``Vehicle`` owns its sensors through ``std::unique_ptr``, an ownership we already built.
- ``Route`` holds its positions by value, in a ``std::vector``. That is composition too: each position belongs to one route.

A Route Has Its Positions
"""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_composition_route_members.png
   :alt: A UML class diagram with two boxes, Route on the left and Position on the right; both boxes and the line are orange. Each class name has a circled letter before it: C for a class, on Route and on Position. Route has minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double. Position, marked struct, has plus x : double and plus y : double. A long line labeled has joins them, with a filled diamond at Route; 1 is above the line next to the diamond, and minus waypoints_ 0..* is under the line at Position.
   :align: center
   :width: 100%

   ``Route`` and ``Position`` with every member: the line labeled ``has``.

- ``0..*`` at ``Position``: a route has any number of waypoints, so ``waypoints_`` is a ``std::vector``. It holds the ``Position`` values themselves: they are destroyed with the ``Route``.
- ``waypoints_`` is in ``Route``'s box, and its name is at the ``Position`` end of the ``has`` line too. ``Position`` is a ``struct``: any ``x`` and any ``y`` make a position.

A Vehicle Owns Its Sensors
""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_composition_sensor_members.png
   :alt: A UML class diagram with two boxes, Vehicle on the left and Sensor on the right, each listing its members; both boxes and the line are orange. Each class name has a circled letter before it: A for the abstract Vehicle, and C for a class, on Sensor. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the right, Sensor with minus id_ : int, minus type_ : SensorType, minus range_ : double, plus Sensor(int, SensorType = lidar, double = 100.0), plus get_id() : int, plus get_type() : SensorType and plus get_range() : double. A line labeled owns joins Vehicle to Sensor, with a filled diamond at Vehicle; 1 is above the line next to the diamond, and minus sensors_ 0..* is under the line at Sensor.
   :align: center
   :width: 100%

   ``Vehicle`` and ``Sensor`` with every member: the line labeled ``owns``.

- ``Sensor``'s ``type_`` is a ``SensorType``, the enumeration. Its box is not in this diagram, because no composition involves it.
- Nothing here is new code: ``Vehicle``, ``Sensor``, ``Route`` and ``Position`` are all in ``project/week9/common`` already.

Exclusive Ownership Needs std::unique_ptr
"""""""""""""""""""""""""""""""""""""""""

:doc:`TC-4 <l9_requirements>`: "A Vehicle shall own its Sensors, so they are made and destroyed with it". Three types could hold each sensor in ``sensors_``:

.. list-table::
   :header-rows: 1
   :widths: 24 22 38 16

   * - Element of ``sensors_``
     - Owned by the vehicle alone?
     - When the vehicle is destroyed
     - TC-4
   * - ``std::unique_ptr<Sensor>``
     - Yes: the vehicle is the only owner
     - Each sensor is destroyed with it; ``Vehicle`` needs no destructor
     - Met
   * - ``Sensor*``
     - The type does not say
     - ``Vehicle``'s own destructor must delete each sensor, or they leak
     - Met, unsafely
   * - ``std::shared_ptr<Sensor>``
     - No: other code can own it too
     - A sensor lives on while any other owner holds it
     - Broken

- **Review the code**: the starter already has both compositions. In ``vehicle.hpp``, ``sensors_`` is a ``std::vector<std::unique_ptr<Sensor>>``; in ``route.hpp``, ``waypoints_`` is a ``std::vector<Position>``.
- A ``Position`` held by value is made and destroyed with its ``Route``, as with ``std::unique_ptr``: that is composition too.
- ``0..*`` at ``Sensor``: any number of sensors, so ``sensors_`` is a ``std::vector``. When the ``Vehicle`` is destroyed, its ``std::vector`` destroys each ``std::unique_ptr``, and each deletes its ``Sensor``.
- A ``std::unique_ptr`` cannot be copied, so copying a ``Vehicle`` does not compile: two vehicles never share a ``Sensor``. A ``Route`` copies, ``Position`` values and all.

See `Each Route Has Its Own Positions`_ under Further Reading.

Dependency
^^^^^^^^^^

A **dependency**: one class uses another only inside a method, as a parameter or a local variable. It keeps no member of that class.

.. code-block:: cpp

   void drive(const Route& route) const;  // in Vehicle

- In UML, a dashed arrow to the class that is used.
- If ``Route`` changes, ``Vehicle`` may have to change too: that is what "depends on" means. A ``Vehicle`` object holds no ``Route``.

Vehicle and Route in the Class Diagram
""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_dependency.png
   :alt: The same UML class diagram of the ride service program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi, Taxi and AutomationLevel, joined by the same lines, and RoboTaxi to AutomationLevel by an arrow labeled has level. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. Vehicle, Route and the dashed arrow labeled uses between them are orange; everything else is grey.
   :align: center
   :width: 100%

   A ``Vehicle`` uses a ``Route``: the dashed arrow labeled ``uses``.

- **Review the code**: in ``vehicle.hpp``, ``drive(const Route& route) const`` takes the route as a parameter; ``vehicle.cpp`` reads ``route.length()``. ``Vehicle`` keeps no ``Route`` member: that is the dependency.
- The dashed arrow is the weakest line in the diagram. No diamond and no number: a vehicle does not hold a route, it is handed one for each drive.
- ``Sensor`` keeps a ``SensorType`` member, ``type_``, so the line from ``Sensor`` to ``SensorType`` is not a dependency. It is an association, the arrow labeled ``has type``.

A Vehicle Uses a Route
""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_dependency_members.png
   :alt: A UML class diagram with only two boxes, Vehicle on the left and Route on the right, each listing its members; both boxes and the arrow are orange. Each class name has a circled letter before it: A for the abstract Vehicle, and C for a class, on Route. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. Route has minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double. A dashed arrow labeled uses runs from Vehicle to Route.
   :align: center
   :width: 100%

   ``Vehicle`` and ``Route`` with every member: the dashed arrow labeled ``uses``.

- No data member is a ``Route``, only ``drive``'s parameter: a dashed ``uses`` arrow.
- This is the flowchart's dependency question at work: does ``Vehicle`` use ``Route`` without keeping it? The dashed arrow says yes: ``Vehicle`` uses a ``Route`` during a call and keeps nothing.
- ``Route``'s box lists ``waypoints_``, as every box lists its data members; the ``has`` line to ``Position`` is not drawn here.
- The same two boxes as in `Vehicle and Route in the Class Diagram`_, with every member.

See `A Route for One Call`_ under Further Reading.

Inheritance
^^^^^^^^^^^

**Inheritance** is one of the four principles of OOP, with encapsulation, abstraction and polymorphism. A **derived class** is built from a **base class**: it gets the base's data members and methods, and adds its own. Use it when every derived object is also a base object (a ``RoboTaxi`` is a ``Vehicle``): what they share is written once, in the base.

.. code-block:: cpp

   class Derived : public Base { /* what Derived adds */ };
   class Derived : protected Base { /* what Derived adds */ };
   class Derived : private Base { /* what Derived adds */ };

.. figure:: /_static/images/l9/inheritance_kinds.png
   :alt: Three UML panels side by side, one per kind of inheritance, each headed by its syntax: class Derived : public Base, class Derived : protected Base, class Derived : private Base. In each, a Base box lists plus start() : void, hash log_event() : void and minus check() : void, and a Derived box below it joins Base by a line with a hollow triangle at Base. With public inheritance, Derived lists plus start() and hash log_event(). With protected inheritance, hash start() and hash log_event(). With private inheritance, minus start() and minus log_event(). In all three, Derived lists check() in grey as not accessible.
   :align: center
   :width: 100%

   What ``start()``, ``log_event()`` and ``check()`` of ``Base`` become in ``Derived``, for each kind of inheritance.

- The keyword before the base class's name sets the kind of inheritance. With ``public``, ``start()`` stays public; with ``protected``, it becomes protected; with ``private``, both methods become private. ``check()`` is private in ``Base``, so ``Derived`` never reaches it, whatever the keyword.
- This course uses ``public``. `protected and private Inheritance`_, under Further Reading, has the full table.
- UML joins the two classes by a line with a hollow triangle at the base class.
- What every kind of vehicle shares (an id, the speeds and their check, the sensors) is written once, in ``Vehicle``.

Writing Inheritance in C++
""""""""""""""""""""""""""

.. code-block:: cpp

   class Derived
       : public Base {
     // public: public
     // protected:
     //   protected
   };

.. code-block:: cpp

   class Derived
       : protected Base {
     // public: protected
     // protected:
     //   protected
   };

.. code-block:: cpp

   class Derived
       : private Base {
     // public: private
     // protected:
     //   private
   };

- ``Base`` is the base class and ``Derived`` the derived class. Each comment says what ``Base``'s ``public`` and ``protected`` members become in ``Derived``: ``public: protected`` means that ``Base``'s ``public`` members are ``protected`` in ``Derived``.
- ``Base``'s ``private`` members are in every ``Derived`` object, but ``Derived``'s methods can never use them.
- This course uses only ``public`` inheritance: a ``RoboTaxi`` is a ``Vehicle`` for any code.

See `protected and private Inheritance`_ and `When protected and private Inheritance Make Sense`_ under Further Reading.

No Specifier Means private Inheritance
""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   // no public before Vehicle
   class RoboTaxi : Vehicle {
     // ...
   };
   RoboTaxi robotaxi{13.4};
   robotaxi.get_speed();  // an error

.. code-block:: text

   error: 'double Vehicle::get_speed() const' is inaccessible within this context
   error: 'Vehicle' is not an accessible base of 'RoboTaxi'

- With no access specifier, the base of a class defined with ``class`` is ``private``: ``Vehicle``'s ``public`` methods become ``private`` in ``RoboTaxi``. Always write ``public``.

.. note::

   "In the absence of an access-specifier for a base class, ``public`` is assumed when the derived class is defined with the class-key ``struct`` and ``private`` is assumed when the class is defined with the class-key ``class``". C++20 **[class.access.base]** (11.9.2) paragraph 2.

Generalization and Specialization
"""""""""""""""""""""""""""""""""

**1. Generalization**: starting from classes you already have, and moving what they share up into a new base class: bottom-up.

**2. Specialization**: starting from a base class, and writing a derived class for objects that need more: top-down.

.. figure:: /_static/images/l9/generalization.png
   :alt: A class diagram with some of the members of each class. On top, Vehicle, with minus max_speed_ : double, minus speed_ : double, minus sensors_ : vector<unique_ptr<Sensor>>, plus set_speed(double) : void, plus add_sensor(SensorType, double) : int, and plus drive(const Route&) : void. Below it, RoboTaxi, with minus operating_zone_ : string, minus automation_level_ : AutomationLevel, plus RoboTaxi(double, string, AutomationLevel), plus change_zone(string) : void and plus drive(const Route&) : void, and Taxi, with minus driver_name_ : string, plus Taxi(double, string), plus assign_driver(string) : void and plus drive(const Route&) : void. Each joins Vehicle by a line with a hollow triangle at Vehicle. A thick arrow on the left, tagged 1, points up. A thick arrow on the right, tagged 2, points down.
   :align: center
   :width: 70%

   1: generalization, bottom-up. 2: specialization, top-down.

- 1, generalization: if ``RoboTaxi`` and ``Taxi`` had been written first, each with its own speeds, its own sensors and its own speed check, what they share would move up into a new class, ``Vehicle``.
- 2, specialization: ``Vehicle`` came first, so ``RoboTaxi`` and ``Taxi`` derive from it, and each box lists only what it adds: a constructor and its own ``drive``, for ``RoboTaxi`` its operating zone, its level of driving automation and ``change_zone``, and for ``Taxi`` the driver's name and ``assign_driver``. `Discussion: Add a RoboBus`_ specializes ``Vehicle`` once more.
- Both directions end with the same diagram: the shared members in the base class, and a hollow triangle at the base.

Single Inheritance
""""""""""""""""""

.. figure:: /_static/images/l9/single_inheritance.png
   :alt: A UML class diagram. On top, Animal, with minus species_ : string and the method plus make_sound(sound : string) : void. Below it, Bird, with minus wing_span_ : double and plus can_fly() : bool, and Elephant, with plus use_trunk() : void. Each joins Animal by a line with a hollow triangle at Animal.
   :align: center
   :width: 55%

   Single inheritance: Bird and Elephant each have one base class, Animal.

- **Single inheritance**: a class derives from exactly one base class.
- ``Bird`` and ``Elephant`` each derive from ``Animal``, with ``: public Animal``.
- A derived box lists only what it adds. The rest comes from ``Animal``.

.. figure:: /_static/images/l9/elephant_bird.png
   :alt: A drawing of a small blue bird standing on the ground beside a large grey elephant with tusks, on a pale background.
   :align: center
   :width: 30%

   A bird and an elephant: both are animals, and each one does something the other cannot.

This is the kind of inheritance the lecture uses: ``RoboTaxi`` and ``Taxi`` each derive from ``Vehicle``. A class with two base classes is in `Multiple Inheritance`_, under Further Reading.


RoboTaxi and Taxi in the Class Diagram
""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_inheritance.png
   :alt: The same UML class diagram of the ride service program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi, Taxi and AutomationLevel, joined by the same lines, and RoboTaxi to AutomationLevel by an arrow labeled has level. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. Vehicle, RoboTaxi, Taxi and the two lines with a hollow triangle at Vehicle are orange; everything else is grey.
   :align: center
   :width: 100%

   ``RoboTaxi`` and ``Taxi`` each join ``Vehicle`` by a line with a hollow triangle at ``Vehicle``.

- We already wrote ``Vehicle``; ``RoboTaxi`` and ``Taxi`` were still grey. A robotaxi is a kind of vehicle, and so is a taxi. Each line with a hollow triangle says "is a".
- ``RoboTaxi`` and ``Taxi`` get everything ``Vehicle`` has. What they add is small: ``RoboTaxi`` adds its operating zone and its level of driving automation, ``Taxi`` adds the driver's name, and each one will drive in its own way, which is polymorphism, the next section.
- Unlike the other relationships, inheritance needs no data member to hold the base: no pointer and no container.
- Italics and «final» come later, in `Abstraction`_ and `The final Keyword`_.

A RoboTaxi and a Taxi Are Vehicles
""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_inheritance_members.png
   :alt: A UML class diagram with three boxes, each listing its members; every box and line is orange. Each class name has a circled letter before it: A for the abstract Vehicle, and C for a class, on RoboTaxi and Taxi. On the left, Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the right, RoboTaxi, marked final, with minus operating_zone_ : string, minus automation_level_ : AutomationLevel, plus RoboTaxi(double, string = "College Park", AutomationLevel = level_4), plus get_operating_zone() : const string&, plus get_automation_level() : AutomationLevel, plus change_zone(string) : void and plus drive(const Route&) : void, and below it Taxi, marked final, with minus driver_name_ : string, plus Taxi(double, string), plus assign_driver(string) : void and plus drive(const Route&) : void. Each joins Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   ``Vehicle``, ``RoboTaxi`` and ``Taxi`` with every member: a line with a hollow triangle at ``Vehicle`` from each derived class.

- The three boxes of `RoboTaxi and Taxi in the Class Diagram`_, with every member. The boxes of ``RoboTaxi`` and ``Taxi`` are short: a derived class lists only what it adds. Every ``Vehicle`` member is theirs too, through the hollow triangle.
- ``RoboTaxi`` adds ``operating_zone_`` and ``automation_level_``, a constructor with a default for each (``"College Park"`` and ``AutomationLevel::level_4``), a getter for each, ``change_zone`` and its own ``drive``. ``Taxi`` adds ``driver_name_``, a constructor that takes the name, ``assign_driver`` and its own ``drive``. ``change_zone`` and ``assign_driver`` are methods that ``Vehicle`` does not have. You write both classes in Step 3, each in its own files.
- ``automation_level_`` is an ``AutomationLevel``, an enumeration of the six levels of driving automation, ``level_0`` to ``level_5``, defined in ``automation_level.hpp``. See `SAE J3016 <https://saemobilus.sae.org/standards/j3016_202609-taxonomy-definitions-terms-related-driving-automation-systems-road-motor-vehicles>`__.
- Their own ``drive`` comes later, in `Polymorphism`_. ``#`` marks a ``protected`` member: see `protected Members`_.

A RoboTaxi in Memory
""""""""""""""""""""

.. code-block:: cpp

   RoboTaxi car_a{13.4};

.. figure:: /_static/images/l9/robotaxi_memory.png
   :alt: A blue Stack box under the name tag car_a holds one object in two parts. The first part, captioned Vehicle part, has six rows, each name marked with a minus sign for private: id_ 1, max_speed_ 13.4, speed_ 0.0, color_ "white", mileage_ 0.0 and sensors_ (empty). The second part, captioned RoboTaxi part, has two rows, also marked private: operating_zone_ "College Park" and automation_level_ level_4. Under it, a gray dashed row reads 4 bytes of padding. A measuring line under all of it reads 128 bytes.
   :align: center
   :width: 40%

   ``car_a`` on the stack: the ``Vehicle`` part, then the ``RoboTaxi`` part with its two data members.

- A derived object contains every data member of its base class: ``car_a`` holds the six of ``Vehicle``, then the two that ``RoboTaxi`` adds.
- Sizes, measured with g++ 13.3: the ``Vehicle`` part is 88 bytes, ``operating_zone_`` (a ``std::string``) 32 and ``automation_level_`` (an ``AutomationLevel``, an ``int`` underneath) 4. Then 4 bytes of padding make the size a multiple of 8: 88 + 32 + 4 + 4 = 128.
- Whether ``RoboTaxi``'s methods can use a member by name depends on its access specifier in ``Vehicle``. ``-`` marks ``private``, as in the class diagram: the member is there, but reachable only through ``Vehicle``'s ``public`` or ``protected`` methods (`private Stays private`_).
- ``next_id_`` is ``static``: one counter for the class, in no object.
- Run: ``702run week9_playground 50``. It prints each member through ``Vehicle``'s ``public`` methods, then the two sizes: ``88 128``.

A Taxi through a Pointer
""""""""""""""""""""""""

.. code-block:: cpp

   auto taxi{std::make_unique<Taxi>(13.4, "Ana")};

.. figure:: /_static/images/l9/taxi_pointer_memory.png
   :alt: On the left, a blue Stack box under the name tag taxi holds one field, pointer, marked (ptr), with a measuring line under it that reads 8 bytes. On the right, a red Heap box holds one object in two parts. The first part, captioned Vehicle part, has six rows, each name marked with a minus sign for private: id_ 1, max_speed_ 13.4, speed_ 0.0, color_ "white", mileage_ 0.0 and sensors_ (empty). The second part, captioned Taxi part, has one row: driver_name_ "Ana", also marked private. A measuring line under both parts reads one allocation, 120 bytes. A blue arrow runs from the pointer field to the first row of the Vehicle part, the start of the Taxi object.
   :align: center
   :width: 80%

   ``taxi`` on the stack, one pointer; the ``Taxi`` on the heap, its ``Vehicle`` part first.

- ``std::make_unique`` makes the ``Taxi`` on the heap, with no ``new``. On the stack, ``taxi`` is one pointer of 8 bytes: a ``std::unique_ptr<Taxi>``.
- The ``Taxi`` starts with its ``Vehicle`` part (88 bytes), then its own ``private`` member ``driver_name_``, a ``std::string`` (32 bytes): 88 + 32 = 120.
- ``taxi`` holds the address where both start.
- Run: ``702run week9_playground 51``. It prints ``8 120``, then ``white``.

See `Inside a Taxi Object`_ under Further Reading.

A Base Class Reference to a Derived Object
""""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   Taxi taxi{13.4, "Ana"};
   taxi.assign_driver("Ben");  // a Taxi method
   Vehicle& vehicle{taxi};  // no cast needed
   // vehicle.assign_driver("Ben");  // does not compile
   vehicle.set_speed(10.0);
   std::cout << taxi.get_speed() << '\n';

.. code-block:: text

   10

Uncommented, the line ``vehicle.assign_driver("Ben");`` gives:

.. code-block:: text

   error: 'class Vehicle' has no member named 'assign_driver'

- Read ``Vehicle& vehicle{taxi};`` as "``vehicle`` is a ``Vehicle`` reference to ``taxi``". A reference is another name for an object: nothing is copied.
- No cast is needed because a ``Taxi`` is a ``Vehicle``. The reference refers to the ``Vehicle`` part at the start of ``taxi``, its **base subobject**.
- ``assign_driver`` is a ``Taxi`` method that ``Vehicle`` does not have. The compiler checks a call through ``vehicle`` against ``Vehicle``'s members only, so ``assign_driver`` can be called through ``taxi`` and not through ``vehicle``. The object is still a ``Taxi``: ``set_speed`` through ``vehicle`` changed ``taxi`` (10).
- A reference is bound once: ``vehicle`` refers to ``taxi`` for its whole life.
- A ``Vehicle`` copy of ``taxi``, not a reference, keeps only its ``Vehicle`` part: slicing (`Slicing`_).
- Run: ``702run week9_playground 52``.

.. note::

   "the reference is bound to the initializer expression lvalue ... (or, in either case, to the appropriate base class subobject of the object)". C++20 standard, [dcl.init.ref] 9.4.3, paragraph 5.1.

See `Inside a Taxi Object`_ under Further Reading.

A Base Class Pointer to a Derived Object
""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   RoboTaxi robotaxi{13.4};
   robotaxi.change_zone("Silver Spring");  // a RoboTaxi method
   Vehicle* pointer{&robotaxi};  // no cast needed
   // pointer->change_zone("Silver Spring");  // does not compile
   pointer->set_speed(10.0);
   std::cout << robotaxi.get_speed() << '\n';
   Taxi taxi{13.4, "Ana"};
   pointer = &taxi;  // now taxi

.. code-block:: text

   10

Uncommented, the line ``pointer->change_zone("Silver Spring");`` gives:

.. code-block:: text

   error: 'class Vehicle' has no member named 'change_zone'

- Read ``Vehicle* pointer{&robotaxi};`` as "``pointer`` is a ``Vehicle`` pointer to ``robotaxi``": it holds the address of the ``Vehicle`` part of ``robotaxi``. No cast: a ``RoboTaxi`` is a ``Vehicle``.
- As with a reference, the compiler checks a call through ``pointer`` against ``Vehicle``'s members only. ``change_zone``, a ``RoboTaxi`` method, can be called through ``robotaxi`` and not through ``pointer``. ``set_speed`` through ``pointer`` changed ``robotaxi`` (10).
- Unlike a reference, a pointer can change: the same ``pointer`` then points to ``taxi``.
- So ``Fleet``'s ``std::vector<std::shared_ptr<Vehicle>>`` holds robotaxis and taxis.
- Run: ``702run week9_playground 53``.

.. note::

   "The result of the conversion is a pointer to the base class subobject of the derived class object". C++20 standard, [conv.ptr] 7.3.11, paragraph 3.

Not the Other Way
"""""""""""""""""

.. code-block:: cpp

   Vehicle* pointer{&taxi};
   Taxi* back{pointer};  // does not compile

.. code-block:: text

   error: invalid conversion from 'Vehicle*' to 'Taxi*'

- From derived to base, the compiler converts on its own: a ``Taxi`` is always a ``Vehicle``.
- From base to derived, it does not: a ``Vehicle`` is not always a ``Taxi``. The compiler knows only that ``pointer`` points to a ``Vehicle``; it could be a ``RoboTaxi``.

protected Members
"""""""""""""""""

A ``protected`` **member** is a member that the class's own methods and the methods of its derived classes can use. Other code cannot use it, as for a ``private`` member.

.. code-block:: cpp

   class Vehicle {  // the Vehicle you wrote, with one protected method
    public:     // any code
     explicit Vehicle(double max_speed,
                      const std::string& color = "white");
    protected:  // Vehicle's, RoboTaxi's and Taxi's methods
     // its body is in vehicle.cpp
     void log_event(const std::string& event) const;
    private:    // Vehicle's methods only
     int id_;  // and the rest of Vehicle's data members
   };

- A method of ``RoboTaxi`` can call ``log_event("starts")``, which prints ``vehicle 1: starts``. The same call in ``main`` does not compile: g++ says ``'void Vehicle::log_event(const std::string&) const' is protected within this context``.
- ``protected`` is the third access specifier, after ``public`` and ``private``. UML marks it with ``#``.
- Run: ``702run week9_playground 55``.

private Stays private
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class RoboTaxi : public Vehicle {  // the Vehicle you wrote: speed_ is private
    public:
     void go() { speed_ = get_max_speed(); }  // does not compile
     // ...
   };

.. code-block:: text

   error: 'double Vehicle::speed_' is private within this context

- A ``RoboTaxi`` object holds ``speed_``, but ``RoboTaxi``'s methods cannot name it: only ``Vehicle``'s can.
- `Through Vehicle's public Methods`_ shows the fix.

protected Data
~~~~~~~~~~~~~~

.. code-block:: cpp

   class RoboTaxi : public Vehicle {  // speed_ is protected now
    public:
     explicit RoboTaxi(
         double max_speed, std::string operating_zone = "College Park",
         AutomationLevel automation_level = AutomationLevel::level_4)
         : Vehicle{max_speed},
           operating_zone_{std::move(operating_zone)},
           automation_level_{automation_level} {}
     void speed_up() { speed_ = 20.0; }  // compiles: no check

    private:
     std::string operating_zone_;        // the area it may drive in
     AutomationLevel automation_level_;  // SAE J3016 level
   };

- With ``speed_`` ``protected``, this compiles. For a ``RoboTaxi`` built with a maximum speed of 13.4, ``get_speed()`` then returns 20. Every derived class can now break ``Vehicle``'s invariant.
- The rule for assignments stays: **every data member is** ``private``, or the assignment gets 0. Use ``protected`` for methods meant only for derived classes, as ``log_event`` in `protected Members`_.
- Run: ``702run week9_playground 57``. It prints ``20 13.4``: the speed, then the maximum speed.

.. note::

   "``protected`` data is a source of complexity and errors. ``protected`` data complicates the statement of invariants". Rule: `Core Guidelines C.133 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-protected>`__.

Through Vehicle's public Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   class RoboTaxi : public Vehicle {  // speed_ is private
    public:
     explicit RoboTaxi(
         double max_speed, std::string operating_zone = "College Park",
         AutomationLevel automation_level = AutomationLevel::level_4)
         : Vehicle{max_speed},
           operating_zone_{std::move(operating_zone)},
           automation_level_{automation_level} {}
     void slow_down() { set_speed(get_speed() / 2.0); }
     void speed_up() { set_speed(20.0); }  // throws

    private:
     std::string operating_zone_;        // the area it may drive in
     AutomationLevel automation_level_;  // SAE J3016 level
   };

   RoboTaxi car_a{13.4};
   car_a.set_speed(10.0);
   car_a.slow_down();
   std::cout << car_a.get_speed() << '\n';
   try {
     car_a.speed_up();
   } catch (const std::invalid_argument& e) {
     std::cout << e.what() << '\n';
   }
   std::cout << car_a.get_speed() << '\n';

It prints:

.. code-block:: text

   5
   speed must be from 0 to the maximum speed
   5

- ``RoboTaxi`` cannot name ``speed_``, so it uses ``Vehicle``'s ``public`` methods, as any other code does. ``slow_down`` reads the speed with ``get_speed()`` and writes half of it with ``set_speed()``: 10 / 2 = 5.
- ``speed_up``, the same method as in `protected Data`_, now goes through the check: 20 is above 13.4, so ``set_speed`` throws and the speed stays 5. Only ``Vehicle`` checks the rule.
- A method meant only for derived classes is ``protected``, as ``log_event`` is. The data stays ``private``.
- Run: ``702run week9_playground 59``.

Constructors and Inheritance
""""""""""""""""""""""""""""

A **base class initializer**: a derived constructor names its base class first in its member initializer list, with the arguments for a base constructor. The base part is built first, then the derived class's own members.

.. code-block:: cpp

   Derived(parameters) : Base{arguments}, member_{value} { body }

For ``Taxi``:

.. code-block:: cpp

   Taxi(double max_speed, std::string driver_name)
       : Vehicle{max_speed}, driver_name_{std::move(driver_name)} {}

.. admonition:: Each class sets up its own members
   :class: important

   Each constructor sets up its own class's members: ``Vehicle``'s constructor checks the maximum speed and takes the next id, and ``Taxi``'s sets ``driver_name_``.

See `A Base Member in the List`_ under Further Reading.

Construction and Destruction Order
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Each constructor and destructor
   // prints its name.
   {
     RoboTaxi robotaxi{13.4};
     std::cout << "in the scope\n";
   }
   std::cout << "after the scope\n";

.. code-block:: text

   Vehicle constructor
   RoboTaxi constructor
   in the scope
   ~RoboTaxi
   ~Vehicle
   after the scope

- The base is built first, so ``RoboTaxi``'s constructor can use ``Vehicle``'s methods. Destruction runs in reverse: ``~RoboTaxi`` first, while the ``Vehicle`` part still exists.
- Run: ``702run week9_playground 62``.

.. note::

   In a constructor, "direct base classes are initialized in declaration order", "Then, non-static data members are initialized in the order they were declared", "Finally, the compound-statement of the constructor body is executed". C++20 **[class.base.init]** (11.10.2) paragraph 13.

See `Discussion: What Prints First?`_ under Further Reading.

Live Coding: Step 3
"""""""""""""""""""

**10 minutes, in class, on your own.** The instructions are on the slides.


Polymorphism
------------

**Polymorphism** is one of the four principles of OOP, with encapsulation, abstraction and inheritance. It lets one piece of code work with objects of different classes. C++ picks the function a call runs either when it compiles the code or while the program runs.

See `cppreference: virtual function specifier <https://en.cppreference.com/w/cpp/language/virtual>`__.

See `drive in the Class Diagram`_ under Further Reading.

Compile-Time Polymorphism
^^^^^^^^^^^^^^^^^^^^^^^^^

**Compile-time polymorphism**: the compiler picks the function a call runs from the types written in the code.

.. code-block:: cpp

   class Vehicle {  // only what these slides need
    public:
     explicit Vehicle(double max_speed) : max_speed_{max_speed} {}
     void drive(const Route& route) const {
       std::cout << "Vehicle: drives " << route.length() << " m\n";
     }
    private:
     double max_speed_;
     double speed_{0.0};
   };
   class RoboTaxi : public Vehicle {
    public:
     explicit RoboTaxi(
         double max_speed, std::string operating_zone = "College Park",
         AutomationLevel automation_level = AutomationLevel::level_4)
         : Vehicle{max_speed},
           operating_zone_{std::move(operating_zone)},
           automation_level_{automation_level} {}
     void drive(const Route& route) const {  // redefines Vehicle::drive
       std::cout << "RoboTaxi: drives itself " << route.length() << " m\n";
     }

    private:
     std::string operating_zone_;        // the area it may drive in
     AutomationLevel automation_level_;  // SAE J3016 level
   };

Where the Compiler Looks for a Method
"""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   RoboTaxi robotaxi{13.4};
   robotaxi.set_speed(10.0);  // Vehicle's
   std::cout << robotaxi.get_speed() << '\n';

.. code-block:: text

   10

When a method is called on an object of a derived class:

1. The compiler looks for the method in the class of the variable, the type written in the code.
2. If it is not there, it looks in the base class, then in the base's base.
3. It calls the first one it finds.

- ``RoboTaxi`` writes no ``set_speed`` and no ``get_speed``, so both are found in ``Vehicle``. These calls use the full ``Vehicle`` of the project, not the short one in `Compile-Time Polymorphism`_ (compiled with g++ 13.3; it prints ``10``).

Redefinition
""""""""""""

.. code-block:: cpp

   // Taxi redefines drive() too: it prints its driver's name.
   RoboTaxi robotaxi{13.4};
   Taxi taxi{13.4, "Ana"};
   robotaxi.drive(maya_ride);  // maya_ride: the 500 m route
   taxi.drive(maya_ride);

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

**Redefinition**: a derived class **redefines** a base method when it writes a method with the same name.

- The compiler finds ``RoboTaxi::drive`` first and stops looking, so ``Vehicle::drive`` is **hidden**: ``robotaxi.drive(...)`` never reaches it.
- Run: ``702run week9_playground 67``.

Runtime Polymorphism
^^^^^^^^^^^^^^^^^^^^

**Runtime polymorphism**: the method a call runs is picked while the program runs, from the class of the object. A call through a base reference or pointer then runs the derived class's own method.

.. admonition:: Three Conditions for Runtime Polymorphism
   :class: important

   1. A derived class inherits from a base class with ``public``: ``RoboTaxi`` from ``Vehicle``.
   2. The base class declares the method ``virtual``, and the derived class overrides it: ``drive``.
   3. The call goes through a base reference or pointer: ``Vehicle&`` or ``Vehicle*``. A ``Vehicle`` object copied from a ``RoboTaxi`` is sliced (`Slicing`_): it is a plain ``Vehicle``.

The Challenge
"""""""""""""

.. note::

   **Challenge**: drive robotaxis and taxis the same way, although each one drives differently.

.. code-block:: cpp

   for (const auto& vehicle : vehicles) {  // a Fleet's vehicles
     vehicle->drive(maya_ride);  // each its own drive
   }

- One function, or one loop, drives every vehicle.
- Each vehicle runs its own ``drive``: a ``RoboTaxi`` prints that it drives itself, and a ``Taxi`` prints its driver's name.
- A new vehicle class, such as a robot bus, needs no change to that code (NFR-1).

See `One Overload per Class`_ and `Scalability and Redundancy`_ under Further Reading.

Through a Base Reference
""""""""""""""""""""""""

.. code-block:: cpp

   void start_shift(const Vehicle& vehicle,
                    const Route& route) {
     vehicle.drive(route);
   }

   start_shift(robotaxi, maya_ride);
   start_shift(taxi, maya_ride);

.. code-block:: text

   Vehicle: drives 500 m
   Vehicle: drives 500 m

The **static type** of an expression is the type written in the code: ``vehicle`` is a ``const Vehicle&``. The **dynamic type** is the class of the object it refers to while the program runs: ``RoboTaxi``, then ``Taxi``.

- The compiler sees only the static type, so it calls ``Vehicle::drive`` for both. Each object's own ``drive`` is lost.
- Run: ``702run week9_playground 70``.

See `What Runtime Polymorphism Needs`_ under Further Reading.

virtual Methods in the Base Class
"""""""""""""""""""""""""""""""""

A ``virtual`` **method** is a method declared ``virtual`` in a base class. A call through a base reference or pointer runs the version of the dynamic type, picked while the program runs. This is **runtime polymorphism**.

.. code-block:: cpp

   class Vehicle {
    public:
     virtual ~Vehicle() = default;  // why: virtual Destructors
     virtual void drive(const Route& route) const { /* as before */ }
   };

   class RoboTaxi : public Vehicle {
    public:
     explicit RoboTaxi(
         double max_speed, std::string operating_zone = "College Park",
         AutomationLevel automation_level = AutomationLevel::level_4)
         : Vehicle{max_speed},
           operating_zone_{std::move(operating_zone)},
           automation_level_{automation_level} {}
     void drive(const Route& route) const override { /* as before */ }

    private:
     std::string operating_zone_;        // the area it may drive in
     AutomationLevel automation_level_;  // SAE J3016 level
   };

- A derived method with the same name, parameters and ``const`` **overrides** the ``virtual`` one. ``override`` is explained in `override`_, the destructor in `virtual Destructors`_.
- You make ``drive`` ``virtual`` in Step 4, after the ``override`` part.

See `The Cost of virtual`_ under Further Reading.

Slicing
"""""""

**Slicing**: copying a derived object into an object of its base class copies only the base part. The copy is a plain ``Vehicle``.

.. code-block:: cpp

   // Small Vehicle: two doubles, virtual drive
   Taxi taxi{13.4, "Ana"};
   Vehicle copy{taxi};  // not a reference
   copy.drive(maya_ride);
   std::vector<Vehicle> parked;
   parked.push_back(taxi);  // sliced too
   parked[0].drive(maya_ride);
   std::cout << sizeof(Vehicle) << ' '
             << sizeof(Taxi) << '\n';

.. code-block:: text

   Vehicle: drives 500 m
   Vehicle: drives 500 m
   24 56

- 24 of the 56 bytes are copied: ``driver_name_`` is left behind, and the copy's dynamic type is ``Vehicle``. Rule: `Core Guidelines ES.63 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-slice>`__, "Don't slice".
- These are the ``runtime::`` classes of `virtual Methods in the Base Class`_: 24 bytes for ``Vehicle``, plus the 32-byte ``std::string`` of ``Taxi``.
- Run: ``702run week9_playground 73``.

See `Copying a Vehicle of the Design`_ and `Discussion: Which drive() Runs?`_ under Further Reading.

override
^^^^^^^^

``override`` is written after a derived method's parameter list and its ``const``. The compiler checks that the method overrides a ``virtual`` method of a base class, and stops with an error if it does not.

.. code-block:: cpp

   class RoboTaxi : public Vehicle {
    public:
     explicit RoboTaxi(
         double max_speed, std::string operating_zone = "College Park",
         AutomationLevel automation_level = AutomationLevel::level_4)
         : Vehicle{max_speed},
           operating_zone_{std::move(operating_zone)},
           automation_level_{automation_level} {}
     void drive(const Route& route) const override;  // must override

    private:
     std::string operating_zone_;        // the area it may drive in
     AutomationLevel automation_level_;  // SAE J3016 level
   };

- ``RoboTaxi::drive`` is ``virtual`` too, without the keyword. C++20 **[class.virtual]** (11.7.2) paragraph 1: "A non-static member function is a virtual function if it is first declared with the keyword virtual or if it overrides a virtual member function declared in a base class".

.. note::

   "Virtual functions should specify exactly one of ``virtual``, ``override``, or ``final``". Rule: `Core Guidelines C.128 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-override>`__. In the base: ``virtual``. In a derived class: ``override``.

A Typo That Compiles
""""""""""""""""""""

.. code-block:: cpp

   class RoboTaxi : public Vehicle {
    public:
     void drvie(const Route& route) const;  // mistake 1: a typo
     void drive(const Route& route);        // mistake 2: no const
   };
   start_shift(robotaxi, maya_ride);  // prints Vehicle: drives 500 m

- Neither line overrides ``drive``: each one declares a new method of ``RoboTaxi``, so ``Vehicle::drive`` runs.
- Mistake 1: g++ gives no warning. Mistake 2: the name matches, the ``const`` does not. It compiles; ``-Wall`` only warns:

.. code-block:: text

   warning: 'virtual void Vehicle::drive(const Route&) const'
            was hidden [-Woverloaded-virtual=]
   note:   by 'void RoboTaxi::drive(const Route&)'

- Run: ``702run week9_playground 76``.

override Catches Both
"""""""""""""""""""""

.. code-block:: cpp

   void drvie(const Route& route) const override;  // does not compile
   void drive(const Route& route) override;        // does not compile

.. code-block:: text

   error: 'void RoboTaxi::drvie(const Route&) const' marked 'override',
          but does not override
   error: 'void RoboTaxi::drive(const Route&)' marked 'override',
          but does not override

- Both mistakes now stop the build, on the line that has them. Without ``override``, mistake 1 showed only as a wrong line of output.

.. note::

   "If a virtual function is marked with the virt-specifier ``override`` and does not override a member function of a base class, the program is ill-formed". C++20 **[class.virtual]** (11.7.2) paragraph 5.

Live Coding: Step 4
"""""""""""""""""""

**10 minutes, in class, on your own.** The instructions are on the slides.

See `Step 4: One Function for Every Vehicle`_ and `auto or a Base Pointer`_ under Further Reading.

virtual Destructors
^^^^^^^^^^^^^^^^^^^

A ``virtual`` **destructor** is a destructor declared ``virtual`` in the base class. Deleting a derived object through a base pointer then runs the derived destructor first, then the base destructor.

.. code-block:: cpp

   class Vehicle {
    public:
     virtual ~Vehicle() = default;
     // ...
   };

- With ``= default`` (the reading :doc:`Rule of Five and Rule of Zero </lectures/lecture8/l8_rule_of_five>`), the compiler writes the body, which here does nothing. What matters is ``virtual``.
- The destructors you already wrote gave back what an object owns. The question now is which destructor runs.

.. note::

   In a ``delete``, if the static type differs from the dynamic type, "the static type shall be a base class of the dynamic type of the object to be deleted and the static type shall have a virtual destructor or the behavior is undefined". C++20 **[expr.delete]** (7.6.2.8) paragraph 3.

Deleting through a Base Pointer
"""""""""""""""""""""""""""""""

.. code-block:: cpp

   {
     // A small Vehicle: two doubles and a virtual drive.
     // ~Vehicle is not virtual. Both destructors print their names.
     std::unique_ptr<Vehicle> vehicle{
         std::make_unique<Taxi>(13.4, "Ana Maria Rodrigues")};
     vehicle->drive(maya_ride);
   }  // vehicle's destructor runs delete on a Vehicle*

**Output:**

.. code-block:: text

   Taxi: Ana Maria Rodrigues drives 500 m
   ~Vehicle

- At the closing brace, ``std::unique_ptr<Vehicle>`` deletes through a ``Vehicle*``, and ``~Vehicle`` is not ``virtual``, so only ``~Vehicle`` runs. ``~Taxi`` never runs, and neither does the destructor of its ``std::string``: undefined behavior (`virtual Destructors`_).
- Run: ``702run week9_playground 80``. It prints the two lines above, then AddressSanitizer stops the run:

.. code-block:: text

   ERROR: AddressSanitizer: new-delete-type-mismatch on 0x... in thread T0:
     object passed to delete has wrong type:
     size of the allocated type:   56 bytes;
     size of the deallocated type: 24 bytes.

**With that check off** (``ASAN_OPTIONS=new_delete_type_mismatch=0``):

.. code-block:: text

   ERROR: LeakSanitizer: detected memory leaks
   Direct leak of 20 byte(s) in 1 object(s) allocated from:
   SUMMARY: AddressSanitizer: 20 byte(s) leaked in 1 allocation(s).

- The code is in ``undefined/``. The stack traces are cut.
- 56 bytes were allocated for a ``Taxi``, and ``delete`` freed them as a 24-byte ``Vehicle``.
- The 20 bytes that leak are the driver's name: 19 characters and the ``'\0'`` that ends them, never freed because ``~Taxi`` never ran.
- The course flags do not catch this at compile time: with ``-Wall -Wextra``, g++ gives no warning. With ``-Wnon-virtual-dtor``, it warns: ``'class Vehicle' has virtual functions and accessible non-virtual destructor``.

The Sizes in the Report
"""""""""""""""""""""""

.. code-block:: cpp

   class Vehicle {  // small: two doubles, one virtual method
    public:
     ~Vehicle();  // not virtual
     virtual void drive(const Route& route) const;
    private:
     double max_speed_;
     double speed_{0.0};
   };
   class Taxi : public Vehicle {  // also ~Taxi and drive
    private:
     std::string driver_name_;
   };

1. ``Vehicle``: two doubles (16 bytes) and the vtable pointer (8 bytes, `The Cost of virtual`_): 24 bytes.
2. ``Taxi`` adds a ``std::string`` (32 bytes): 24 + 32 = 56 bytes.
3. The name has 19 characters, more than the 15 a g++ ``std::string`` keeps inside itself, so it is on the heap, and only ``~Taxi`` would free it.

- With the design's ``Vehicle`` (six data members): 96 and 128 bytes.
- The sizes were measured with ``sizeof`` in g++ 13.3, with the course flags.

See `Discussion: Who Needs a virtual Destructor?`_ under Further Reading.

Live Coding: Step 5
"""""""""""""""""""

**5 minutes, in class, on your own.** The instructions are on the slides.

See `Step 5: With a virtual Destructor`_ under Further Reading.

Abstraction
-----------

**Abstraction**, one of the four principles of OOP, hides how a class does its work behind what it offers. An **abstract class** declares what every derived class must do, and leaves how to each one. You make a class abstract by giving it at least one **pure** ``virtual`` **method** (`Pure virtual Methods`_). No object of an abstract class can be created.

See `cppreference: Abstract class <https://en.cppreference.com/w/cpp/language/abstract_class>`__.

Pure virtual Methods
^^^^^^^^^^^^^^^^^^^^

A **pure** ``virtual`` **method** is a ``virtual`` method declared with ``= 0``. The class gives it no body, and a class with one is abstract. Every derived class must override it before you can create objects of that class; a derived class that does not override it is abstract too.

.. code-block:: cpp

   class Vehicle {  // abstract
    public:
     virtual ~Vehicle() = default;
     virtual void drive(const Route& route) const = 0;  // no body
     // ... constructors, id, speeds, color, mileage, sensors
   };

- FR-3: each kind of vehicle drives in its own way, so ``Vehicle::drive`` has no body that makes sense.
- Only the methods each derived class must do its own way are pure virtual. In ``Vehicle``, only ``drive`` is: ``set_speed`` and ``get_speed`` keep one body for every vehicle.
- UML sets an abstract class's name in italics: ``Vehicle`` on the class diagram.

.. note::

   "A class is an abstract class if it has at least one pure virtual function". C++20 **[class.abstract]** (11.7.3) paragraph 2.

Live Coding: Step 6
"""""""""""""""""""

**Homework, not collected.** The instructions are on the slides.

See `Step 6: No Vehicle Objects`_ and `Step 6: RoboTaxi and Taxi`_ under Further Reading.

Concrete Classes
^^^^^^^^^^^^^^^^

A **concrete class** is a class with no pure ``virtual`` method left: it overrides every one it inherits. Objects of a concrete class can be created.

.. code-block:: cpp

   void RoboTaxi::drive(const Route& route) const {
     if (sensor_count() == 0) {  // FR-4: no sensor, no driving
       std::cout << "RoboTaxi: no sensor, stays parked\n";
       return;
     }
     std::cout << "RoboTaxi: " << sensor_count()
               << (sensor_count() == 1 ? " sensor" : " sensors")
               << " checked, drives " << route.length() << " m\n";
   }

- ``sensors_`` is ``Vehicle``'s ``private`` member, so ``RoboTaxi`` asks through the ``public`` ``sensor_count()``.

Forgetting One Override
"""""""""""""""""""""""

.. code-block:: cpp

   class Taxi : public Vehicle {  // no drive()
     // ...
   };
   Taxi taxi{13.4, "Ana"};  // does not compile

.. code-block:: text

   error: cannot declare variable 'taxi' to be of abstract type 'Taxi'
   note:   because the following virtual functions are pure within 'Taxi':
   note:     'virtual void Vehicle::drive(const Route&) const'

- ``Taxi`` inherits ``drive(...) = 0`` and gives it no body, so ``Taxi`` is abstract too. The note names the method that is missing.

.. note::

   "A class is abstract if it contains or inherits at least one pure virtual function for which the final overrider is pure virtual". C++20 **[class.abstract]** (11.7.3) paragraph 4.

Fleet and Passenger Do Not Change
"""""""""""""""""""""""""""""""""

.. code-block:: cpp

   auto robotaxi{std::make_shared<RoboTaxi>(13.4)};
   robotaxi->add_sensor(SensorType::lidar, 100.0);
   robotaxi->add_sensor(SensorType::camera, 80.0);
   auto taxi{std::make_shared<Taxi>(13.4, "Ana")};
   Fleet fleet;
   fleet.add(robotaxi);  // converts to std::shared_ptr<Vehicle>
   fleet.add(taxi);
   Passenger maya{"Maya"};
   maya.board(robotaxi);
   const std::vector<std::shared_ptr<Vehicle>> today{robotaxi, taxi};
   for (const std::shared_ptr<Vehicle>& vehicle : today) {
     vehicle->drive(maya_ride);  // maya_ride: the 500 m route
   }

.. code-block:: text

   RoboTaxi: 2 sensors checked, drives 500 m
   Taxi: Ana drives 500 m

- ``Fleet`` and ``Passenger`` are the classes of Steps 1 and 2 (`Live Coding: Step 1`_ and `Live Coding: Step 2`_). Step 6 made ``Vehicle`` abstract and changed not one line of them: they name only ``Vehicle``.
- Run: ``702run week9_playground 88``.

See `Discussion: Add a RoboBus`_ under Further Reading.

The final Keyword
-----------------

``final`` after a class name stops other classes from deriving from it. ``final`` after a ``virtual`` method stops derived classes from overriding it.

See `cppreference: final specifier <https://en.cppreference.com/w/cpp/language/final>`__.

See `final in the Class Diagram`_ under Further Reading.

final Class and final Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 16 42 42

   * -
     - ``final`` class
     - ``final`` method
   * - Syntax
     - ``class RoboTaxi final : public Vehicle``
     - ``void drive(const Route& route) const final;`` in a ``Taxi`` that is not ``final``
   * - What it stops
     - Every class deriving from ``RoboTaxi``, such as ``SuperRoboTaxi``
     - A class derived from ``Taxi``, such as ``NightTaxi``, overriding ``drive``. It can still derive from ``Taxi``.
   * - The error
     - ``cannot derive from 'final' base 'RoboTaxi' in derived type 'SuperRoboTaxi'``
     - ``virtual function '...NightTaxi::drive(...) const' overriding final function``
   * - Why use it
     - A derived class could override ``drive`` and skip the sensor check (`The Reason for Each final`_).
     - The design has none. It keeps one method fixed while the class stays open to deriving (`A final Method`_).

virtual, override and final
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 45 35

   * - On a method
     - Means (C.128)
     - Example
   * - ``virtual``
     - "this is a new virtual function"
     - ``Vehicle::drive``, ``~Vehicle``
   * - ``override``
     - "this is a non-final overrider"
     - ``RoboTaxi::drive``, ``Taxi::drive``
   * - ``final``
     - "this is a final overrider"
     - ``Taxi::drive`` in `A final Method`_, not the design

- A ``final`` class needs no ``final`` on its methods: nothing can derive from it to override them.
- ``final`` closes a design for every later programmer. Use it when deriving would break something, not by habit.

.. note::

   "Capping a hierarchy with ``final`` classes is rarely needed for logical reasons and can be damaging to the extensibility of a hierarchy". Rule: `Core Guidelines C.139 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-final>`__, "Use ``final`` on classes sparingly".

The Reason for Each final
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class FastRoboTaxi : public RoboTaxi {  // if RoboTaxi were not final
    public:
     // ... a constructor
     void drive(const Route& route) const override {
       std::cout << "FastRoboTaxi: drives " << route.length() << " m\n";
     }  // no sensor check: it drives with 0 sensors
   };

- ``RoboTaxi::drive`` keeps FR-4: with no sensor, the robotaxi stays parked. A class derived from ``RoboTaxi`` could override ``drive`` and skip that check, so ``RoboTaxi`` is ``final``.
- ``Taxi`` is ``final`` for the same reason: in ``project/week9/common``, its ``drive`` stays parked when the taxi has no driver.
- This passes the test of `virtual, override and final`_: deriving would break a requirement.

See `Discussion: A Keyword for Each Method`_ under Further Reading.

Live Coding: Step 7
^^^^^^^^^^^^^^^^^^^

**Homework, not collected.** The instructions are on the slides.

See `Step 7: A final Class`_ under Further Reading.

Further Reading
---------------

The sections below come from the appendix of the slides. They are **not presented** in the lecture, and the quizzes do not test them. Read them on your own.

.. list-table::
   :header-rows: 1
   :widths: 22 42 36

   * - Topic
     - Section (appendix frames)
     - What it adds
   * - Requirements
     - `All Twelve Requirements`_ (ii)
     - The full list, FR-1 to FR-12
   * - Live Coding
     - `What the Live Coding Replaces`_ (iii to viii)
     - The finished code of Steps 1 and 4 to 7, with its output
   * - The final Keyword
     - `A final Method`_ (ix)
     - A method that no derived class can override, in a class that is not final
   * - Class Relationships
     - `Multiple Inheritance`_ (x to xi)
     - A class with two base classes, in UML and in C++
   * - Class Relationships
     - `protected and private Inheritance`_ (xii)
     - The access of each base member for each keyword
   * - Class Relationships
     - `When protected and private Inheritance Make Sense`_ (xiii)
     - When each keyword fits, with an example, and what the isocpp FAQ and the Google C++ Style Guide advise
   * - Class Relationships
     - `A Base Member in the List`_ (xiv)
     - Why a derived constructor cannot set a base member
   * - Polymorphism
     - `auto or a Base Pointer`_ (xv to xviii)
     - The type ``auto`` deduces for a pointer, and what each static type allows
   * - Polymorphism
     - `Copying a Vehicle of the Design`_ (xix)
     - Why the copy fails, and how to delete it
   * - Polymorphism
     - `The Cost of virtual`_ (xx)
     - The hidden vtable pointer: what it adds to each object and to each call
   * - Each part
     - `Verbs and Links`_ (xxi to xxxiii)
     - More code, memory pictures and UML for the slides of each part, in the order of the lecture
   * - Discussions
     - `Discussions`_ (xxxiv to xl)
     - The questions of the discussions, with their answers
   * - Live Coding
     - `std::find on a Vector`_ and `std::erase_if on a Vector`_ (xli to xlii)
     - Code to copy for Step 2: ``std::find`` and ``std::erase_if`` on a vector of numbers

All Twelve Requirements
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 12 88

   * - ID
     - The system shall
   * - FR-1
     - allow a Passenger to request a ride by giving pickup and dropoff locations.
   * - FR-2
     - allow a Fleet to dispatch an available vehicle, a RoboTaxi or a Taxi, to a ride request.
   * - FR-3
     - support polymorphic vehicle behavior: RoboTaxi and Taxi implement their own driving.
   * - FR-4
     - make each RoboTaxi contain one or more Sensors.
   * - FR-5
     - allow a Vehicle to follow an optional Route.
   * - FR-6
     - answer status queries: vehicle status, location, and the driver of a Taxi.
   * - FR-7
     - log the key events of a ride, from the request to the end of the trip.
   * - FR-8
     - read sensor data continuously while a RoboTaxi operates.
   * - FR-9
     - allow creating and optimizing Routes with several waypoints.
   * - FR-10
     - support Fleet operations: adding and removing vehicles, and listing available ones.
   * - FR-11
     - support driver management for Taxis: assigning and removing drivers.
   * - FR-12
     - support passengers boarding and leaving, which updates the vehicle.

- Today's code covers FR-3, FR-4, FR-5, FR-9 (building a route, not optimizing it), FR-10, FR-11 and FR-12, listed with their code on :doc:`L9 Requirements <l9_requirements>`.

Back to `Requirements`_.

What the Live Coding Replaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The finished code of Steps 1 and 4 to 7, with its output, in six appendix frames.

Step 1: A Passenger Rides a Vehicle
"""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   class Passenger {
    public:
     explicit Passenger(std::string name) : name_{std::move(name)} {
       if (name_.empty()) {
         throw std::invalid_argument{"a passenger has a name"};
       }
     }
     void board(const std::shared_ptr<Vehicle>& vehicle);
     void leave() noexcept;
    private:
     std::string name_;
     std::weak_ptr<Vehicle> ride_;  // does not own the Vehicle
   };

- ``board`` and ``leave`` are defined in ``passenger.cpp``: ``board`` stores the pointer in ``ride_``, and ``leave`` resets it.
- ``Vehicle`` is the class given in ``vehicle.hpp``. The program keeps each ``Vehicle`` in a ``std::shared_ptr``, so a ``std::weak_ptr`` can refer to it without owning it.

Back to `Live Coding: Step 1`_.

Step 4: One Function for Every Vehicle
""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   void start_shift(const Vehicle& vehicle,
                    const Route& route) {
     vehicle.drive(route);
   }

   start_shift(robotaxi, maya_ride);
   start_shift(taxi, maya_ride);

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- The same ``start_shift`` as in `Through a Base Reference`_. Only ``virtual`` changed, and each object now runs its own ``drive``.
- ``start_shift`` serves every class derived from ``Vehicle``, including classes written after it.

Back to `Live Coding: Step 4`_.

Step 5: With a virtual Destructor
"""""""""""""""""""""""""""""""""

.. code-block:: cpp

   class Vehicle {
    public:
     virtual ~Vehicle() {
       std::cout << "~Vehicle\n";
     }
     // ...
   };
   // Taxi and the rest of the
   // code do not change.

.. code-block:: text

   Taxi: Ana Maria Rodrigues drives 500 m
   ~Taxi
   ~Vehicle

- The ``delete`` of `Deleting through a Base Pointer`_ now runs ``~Taxi``, then ``~Vehicle``. Built with AddressSanitizer: no error, no leak.
- ``~Taxi`` overrides ``~Vehicle`` although the names differ ([class.virtual], 11.7.2 paragraph 7).

.. note::

   "A base class destructor should be either public and virtual, or protected and non-virtual". Rule: `Core Guidelines C.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual>`__.

Back to `Live Coding: Step 5`_.

Step 6: No Vehicle Objects
""""""""""""""""""""""""""

.. code-block:: cpp

   Vehicle vehicle{13.4};  // does not compile

.. code-block:: text

   error: cannot declare variable 'vehicle' to be of abstract type 'Vehicle'
   note:   because the following virtual functions are pure within 'Vehicle':
   note:     'virtual void Vehicle::drive(const Route&) const'

.. code-block:: cpp

   RoboTaxi robotaxi{13.4};
   robotaxi.add_sensor(SensorType::lidar, 100.0);
   const Vehicle& vehicle{robotaxi};  // a reference to Vehicle is fine
   vehicle.drive(maya_ride);

.. code-block:: text

   RoboTaxi: 1 sensor checked, drives 500 m

- References and pointers to ``Vehicle`` are fine: they refer to a ``RoboTaxi`` or a ``Taxi``. Slicing cannot be written now: ``Vehicle copy{robotaxi};`` gives the same first error.

Back to `Live Coding: Step 6`_.

Step 6: RoboTaxi and Taxi
"""""""""""""""""""""""""

.. code-block:: cpp

   RoboTaxi robotaxi{13.4};
   robotaxi.drive(maya_ride);
   robotaxi.add_sensor(SensorType::lidar, 100.0);
   robotaxi.drive(maya_ride);
   Taxi taxi{13.4, "Ana"};
   taxi.drive(maya_ride);

.. code-block:: text

   RoboTaxi: no sensor, stays parked
   RoboTaxi: 1 sensor checked, drives 500 m
   Taxi: Ana drives 500 m

- ``Taxi`` overrides ``drive`` too: it prints its driver's name, as in `Redefinition`_.
- Both are concrete: each overrides ``drive``.

Back to `Live Coding: Step 6`_.

Step 7: A final Class
"""""""""""""""""""""

.. code-block:: cpp

   class RoboTaxi final : public Vehicle {
     // ...
   };

   class SuperRoboTaxi : public RoboTaxi {};  // does not compile

.. code-block:: text

   error: cannot derive from 'final' base 'RoboTaxi' in derived type 'SuperRoboTaxi'

- ``RoboTaxi`` and ``Taxi`` are ``final`` in ``project/week9/common``: each ``drive`` has a check that no override may skip (`The Reason for Each final`_).

.. note::

   "If a class is marked with the class-virt-specifier ``final`` and it appears as a class-or-decltype in a base-clause (11.7), the program is ill-formed". C++20 [class.pre], 11.1 paragraph 5.

Back to `Live Coding: Step 7`_.

A final Method
^^^^^^^^^^^^^^

.. code-block:: cpp

   class Taxi : public Vehicle {  // Taxi is not final here
    public:
     void drive(const Route& route) const final;  // the last override
   };

   class NightTaxi : public Taxi {
    public:
     void drive(const Route& route) const override;  // does not compile
   };

.. code-block:: text

   error: virtual function 'virtual void NightTaxi::drive(const Route&) const'
          overriding final function
   note: overridden function is 'virtual void Taxi::drive(const Route&) const'

- ``NightTaxi`` can still derive from ``Taxi`` and add members; only ``drive`` is closed.

Multiple Inheritance
^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/multiple_inheritance.png
   :alt: A UML class diagram. On top, two boxes side by side: Animal, with minus has_tail_, minus has_wings_ and minus has_horns_, each a bool, and the method plus can_fly() : bool; and Human, with minus is_bipedal_ : bool and the method plus speak() : void. Below them, MythicalCreature, with minus powers_ : vector<string> and plus use_power(power : string) : void. MythicalCreature joins each of the two boxes by a line with a hollow triangle at the box above.
   :align: center
   :width: 55%

   Multiple inheritance: MythicalCreature has two base classes.

- **Multiple inheritance**: a class derives from more than one base class, separated by commas.
- A ``MythicalCreature``, such as a sphinx, is an ``Animal`` and a ``Human``. It gets the ``public`` members of both. A ``MythicalCreature`` object holds the data of both, and its code can call the ``public`` methods of both: ``can_fly`` from ``Animal``, ``speak`` from ``Human``. The data stays ``private`` to each base class.

.. figure:: /_static/images/l9/sphinx.png
   :alt: An engraving of a winged sphinx: a human head with long hair on a lion's body, with feathered wings and a curled tail, one front paw resting on a ball.
   :align: center
   :width: 35%

   A sphinx: a human head on a lion's body.

.. note::

   We use single inheritance in class. In assignments and projects, you may also use multiple inheritance, always with ``public``.

The code:

.. code-block:: cpp

   class Animal {
    public:
     explicit Animal(
         bool has_wings);
     bool can_fly() const;
    private:
     bool has_tail_{true};
     bool has_wings_{false};
     bool has_horns_{false};
   };

   class Human {
    public:
     void speak() const;
    private:
     bool is_bipedal_{true};
   };

   class MythicalCreature
       : public Animal, public Human {
    public:
     MythicalCreature(bool has_wings,
         std::vector<std::string> powers)
         : Animal{has_wings},
           powers_{std::move(powers)} {}
     void use_power(
         const std::string& power) const;

    private:
     std::vector<std::string> powers_;
   };

- The base classes are separated by commas. The constructor passes ``has_wings`` to ``Animal``'s constructor: ``Animal``'s data stays ``private``.
- A ``const Animal&`` and a ``const Human&`` can both refer to a ``MythicalCreature``.
- Run: ``702run week9_appendix xi``. A sphinx with wings and the power ``riddle`` prints ``true`` for ``can_fly`` through the ``const Animal&``, ``Human: speaks`` through the ``const Human&``, then ``uses riddle``.

Back to `Single Inheritance`_.

protected and private Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - In the base
     - ``: public B``
     - ``: protected B``
     - ``: private B``
   * - ``public``
     - ``public``
     - ``protected``
     - ``private``
   * - ``protected``
     - ``protected``
     - ``protected``
     - ``private``
   * - ``private``
     - there, but not usable
     - there, but not usable
     - there, but not usable

- Each cell is the access the member has in the derived class. The ``private`` members of the base are inherited (they are in the object) but cannot be named.
- With ``protected`` or ``private`` inheritance, outside code cannot use a derived object as a base object: the "is a" is hidden. This course uses only ``public`` inheritance.

.. note::

   C++20 **[class.access.base]** (11.9.2) paragraph 1 states the ``public`` and ``protected`` rows of each column. Its footnote 112 gives the ``private`` row: private members of a base class "remain inaccessible even to derived classes", unless the base class declares the derived class a friend.

Back to `Writing Inheritance in C++`_.

When protected and private Inheritance Make Sense
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class PreTripCheck {
    protected:
     ~PreTripCheck() = default;
     void check() const {
       std::cout << (ok() ? "go\n" : "stop\n");
     }
     virtual bool ok() const = 0;
   };

   class Shuttle : private PreTripCheck {
    public:
     void start() const { check(); }

    private:
     bool ok() const override { return true; }
   };

   Shuttle shuttle;
   shuttle.start();

Output:

.. code-block:: text

   go

- Use ``private`` inheritance when three things hold:

  1. A class ``Shuttle`` reuses the code of a class ``PreTripCheck``.
  2. That code calls a function that ``Shuttle`` overrides, or ``Shuttle`` needs the ``protected`` members of ``PreTripCheck``. Here ``check()`` calls the pure virtual ``ok()``, and ``Shuttle`` overrides ``ok()``.
  3. A ``Shuttle`` is not a kind of ``PreTripCheck``.
- Outside code cannot use a ``Shuttle`` as a ``PreTripCheck``. ``const PreTripCheck& base{shuttle};`` does not compile. g++ 13.3 says ``'PreTripCheck' is an inaccessible base of 'Shuttle'``.
- Use ``protected`` inheritance in the same case, when the classes derived from ``Shuttle`` also need to use ``PreTripCheck``. The "is a" is then visible to the classes derived from ``Shuttle``, and still hidden from outside code.
- In every other case, use a member (composition): ``Shuttle`` holds the object it needs as a data member. This course uses only ``public`` inheritance.
- The destructor of ``PreTripCheck`` is ``protected`` and non-virtual, one of the two choices of `Core Guidelines C.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual>`__. Outside code cannot delete a ``Shuttle`` through a ``PreTripCheck*``.
- Run: ``702run week9_appendix xiii``.

.. note::

   "Use composition when you can, private inheritance when you have to". For the FAQ, a long-term use of private inheritance is when "you want to build a class Fred that uses code in a class Wilma, and the code from class Wilma needs to invoke member functions from your new class, Fred". In the code above, ``Shuttle`` is Fred and ``PreTripCheck`` is Wilma. See `isocpp FAQ: composition or private inheritance <https://isocpp.org/wiki/faq/private-inheritance#priv-inherit-vs-compos>`__.

   On ``protected`` and ``private`` inheritance: "both allow overriding virtual functions in the private/protected base class, neither claims the derived is a kind-of its base". The difference: "protected inheritance allows derived classes of derived classes to know about the inheritance relationship". See `isocpp FAQ: protected and private inheritance <https://isocpp.org/wiki/faq/private-inheritance#prot-vs-priv-inherit>`__.

   "All inheritance should be public. If you want to do private inheritance, you should be including an instance of the base class as a member instead". Rule: `Google C++ Style Guide <https://google.github.io/styleguide/cppguide.html#Inheritance>`__.

Back to `Writing Inheritance in C++`_.

A Base Member in the List
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   explicit RoboTaxi(
       double max_speed, std::string operating_zone = "College Park",
       AutomationLevel automation_level = AutomationLevel::level_4)
       : max_speed_{max_speed},  // does not compile
         operating_zone_{std::move(operating_zone)},
         automation_level_{automation_level} {}

.. code-block:: text

   error: 'double Vehicle::max_speed_' is private within this context
   error: class 'RoboTaxi' does not have any field named 'max_speed_'
   error: no matching function for call to 'Vehicle::Vehicle()'

- A member initializer list names only the class's own members and its base classes. ``max_speed_`` belongs to ``Vehicle``, so only ``Vehicle``'s constructor can initialize it.
- With ``max_speed_`` ``protected``, the second and third errors stay.

Back to `Constructors and Inheritance`_.

auto or a Base Pointer
^^^^^^^^^^^^^^^^^^^^^^

**The type** ``auto`` **deduces**: ``auto`` takes the type of its initializer. ``std::make_unique<RoboTaxi>`` returns a ``std::unique_ptr<RoboTaxi>``, so that is the type ``auto`` gives, not ``std::unique_ptr<Vehicle>``.

.. code-block:: cpp

   auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
   // robotaxi is a std::unique_ptr<RoboTaxi>

   std::unique_ptr<Vehicle> vehicle{std::make_unique<RoboTaxi>(13.4)};
   // vehicle is a std::unique_ptr<Vehicle> to a RoboTaxi

- Both own a ``RoboTaxi``. They differ in the static type, so they differ in what the variable can hold later and what the code can call.

Back to `Live Coding: Step 4`_.

Two Pointers, Two Static Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
   std::unique_ptr<Vehicle> vehicle{std::make_unique<RoboTaxi>(13.4)};
   robotaxi->drive(maya_ride);  // RoboTaxi: drives itself 500 m
   vehicle->drive(maya_ride);   // RoboTaxi: drives itself 500 m
   vehicle = std::make_unique<Taxi>(13.4, "Ana");   // any Vehicle: OK
   vehicle->drive(maya_ride);   // Taxi: Ana drives 500 m
   robotaxi = std::make_unique<Taxi>(13.4, "Ana");  // does not compile

.. code-block:: text

   error: no match for 'operator=' (operand types are
          'std::unique_ptr<RoboTaxi, std::default_delete<RoboTaxi> >'
          and 'std::__detail::__unique_ptr_t<Taxi>')

- A ``std::unique_ptr<Vehicle>`` can own any kind of vehicle, one after the other. A ``std::unique_ptr<RoboTaxi>`` owns robotaxis only.
- The compiler checks every name against the static type. With the design's ``RoboTaxi``, ``robotaxi->get_operating_zone()`` compiles and ``vehicle->get_operating_zone()`` does not.
- Run: ``702run week9_appendix xvi``.

Back to `Live Coding: Step 4`_.

From auto into a Vector of Vehicles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void hand_over(std::unique_ptr<Vehicle> vehicle, const Route& route) {
     vehicle->drive(route);
   }

   std::vector<std::unique_ptr<Vehicle>> vehicles;
   auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
   vehicles.push_back(std::move(robotaxi));              // converts
   auto taxi{std::make_unique<Taxi>(13.4, "Ana")};
   vehicles.emplace_back(std::move(taxi));               // converts too
   std::cout << vehicles.size() << '\n';                 // 2
   hand_over(std::make_unique<RoboTaxi>(13.4), maya_ride);
   // prints RoboTaxi: drives itself 500 m

- A ``std::unique_ptr<RoboTaxi>`` that is moved converts to a ``std::unique_ptr<Vehicle>``: ``push_back``, ``emplace_back`` and the parameter of ``hand_over`` all accept it.
- Each ``std::unique_ptr`` is the only owner of its vehicle. ``Fleet`` shares its vehicles, so it holds ``std::shared_ptr<Vehicle>`` instead.
- Run: ``702run week9_appendix xvii``.

Back to `Live Coding: Step 4`_.


auto or a Base Pointer: Summary
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 56 22 22

   * - What the code does with the pointer
     - From ``auto``
     - Declared as base
   * - Call a method only ``RoboTaxi`` has
     - Yes
     - No
   * - Call ``drive``, which runs ``RoboTaxi::drive``
     - Yes
     - Yes
   * - Move it into a vector of ``std::unique_ptr<Vehicle>``
     - Yes, converts
     - Yes
   * - Pass it to a ``std::unique_ptr<Vehicle>`` parameter
     - Yes, converts
     - Yes
   * - Hold a ``Taxi`` later, in the same variable
     - No
     - Yes

- From ``auto``: a ``std::unique_ptr<RoboTaxi>``. Declared as base: a ``std::unique_ptr<Vehicle>`` that owns a ``RoboTaxi``.
- Every "Yes" and "No" was compiled with g++ 13.3, C++20. The first row used ``get_operating_zone()``, which only the design's ``RoboTaxi`` has.

Back to `Live Coding: Step 4`_.

Copying a Vehicle of the Design
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Taxi taxi{13.4, "Ana"};      // project/week9/common
   Taxi copy{taxi};             // does not compile
   Taxi moved{std::move(taxi)};  // does not compile either

.. code-block:: text

   error: static assertion failed: result type must be constructible from input type

- Each line gives the same 4 errors, from inside ``std::vector``: copying ``Vehicle`` copies ``sensors_``, and a ``std::unique_ptr`` cannot be copied. The move falls back to the copy: ``Vehicle`` declares its destructor, so the compiler writes no moves (Core Guidelines C.21).
- The copy is not suppressed: ``std::is_copy_constructible_v<Taxi>`` is ``true``. The copy constructor exists, and fails only when a copy is compiled. To suppress it, ``Vehicle`` deletes it (``= delete``, in the reading :doc:`Rule of Five and Rule of Zero </lectures/lecture8/l8_rule_of_five>`):

.. code-block:: cpp

   Vehicle(const Vehicle&) = delete;             // in Vehicle
   Vehicle& operator=(const Vehicle&) = delete;  // no moves either

- Then the trait is ``false``, and ``Taxi copy{taxi};`` stops with ``use of deleted function 'Taxi::Taxi(const Taxi&)'``.

.. note::

   "A polymorphic class should suppress public copy/move". Rule: `Core Guidelines C.67 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-virtual>`__.

Back to `Slicing`_.

The Cost of virtual
^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   using Plain = compile_time::Vehicle;  // no virtual method
   using Poly = runtime::Vehicle;        // virtual methods
   std::cout << sizeof(Plain) << ' ' << sizeof(Poly) << '\n';  // 16 24
   std::cout << std::boolalpha << std::is_polymorphic_v<Plain> << ' '
             << std::is_polymorphic_v<Poly> << '\n';  // false true

- ``compile_time::Vehicle`` (`Compile-Time Polymorphism`_) and ``runtime::Vehicle`` (`virtual Methods in the Base Class`_), both in ``playground/src/polymorphism.cpp`` (``week9_appendix`` runs copies of them), have the same data members, ``max_speed_`` and ``speed_``. The polymorphic one is 8 bytes larger: g++ stores a hidden pointer in it, to a table of its class's ``virtual`` methods, the **vtable**. The C++ standard leaves this to the compiler.
- ``nm -C polymorphism.cpp.o`` lists ``vtable for polymorphism::runtime::Vehicle``. Without ``-C`` (demangle), ``nm`` prints the linker's name, ``_ZTVN12polymorphism7runtime7VehicleE``. The object file is in ``build/project/week9/CMakeFiles/week9_playground.dir/playground/src/``.
- A ``virtual`` call reads that table first, so it costs a little more than a direct call.
- A **polymorphic class** is one that "declares or inherits a virtual function" (C++20 **[class.virtual]** (11.7.2) paragraph 1).
- Run: ``702run week9_appendix xx``.

.. note::

   "Redundant ``virtual`` increases run-time and object-code size". Rule: `Core Guidelines C.132 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-virtual>`__, "Don't make a function ``virtual`` without reason".

Back to `virtual Methods in the Base Class`_.

Verbs and Links
^^^^^^^^^^^^^^^

- A **verb** becomes a method of the class that does it: "a Fleet adds vehicles" (FR-10) gives ``Fleet::add``.
- A **link between two nouns** becomes a relationship: "a Passenger boards a vehicle" (FR-12) gives an association (`Association`_).
- "**is a**" becomes inheritance: a RoboTaxi is a kind of Vehicle (FR-3, `Inheritance`_).

.. note::

   Not every noun is a class. A waypoint (FR-9) is a ``Position``: a ``struct``, because its ``x`` and ``y`` follow no rule and it has nothing to hide.

Back to `Nouns and Classes`_.


Before reset, in Memory
^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/step1_memory_1.png
   :alt: On the left, three blue Stack boxes under name tags car_a, maya and watcher. car_a holds two fields, object and control, each marked (ptr). maya holds name_, "Maya", then ride_.object and ride_.control, each marked (ptr). watcher holds object and control, each marked (ptr). On the right, a red Heap box holds one allocation, measured as 104 bytes: a control block with use_count 1 and weak_ptrs 2, then a Vehicle object with id_ 1, max_speed_ 13.4, speed_ 0.0, color_ "white", mileage_ 0.0 and sensors_ (empty). Solid green arrows run from car_a's object field to the Vehicle object and from its control field to the control block. Dashed orange arrows run from ride_.object to the Vehicle object and from ride_.control to the control block; dashed dark blue arrows do the same from watcher's object and control fields.
   :align: center
   :width: 90%

   This code in memory, after ``std::weak_ptr<Vehicle> watcher{car_a};``.

- ``make_shared`` made one allocation of 104 bytes, measured with g++ 13.3: a 16-byte control block first, then the 88-byte ``Vehicle`` right after it.
- Each smart pointer on the stack holds two pointers: one to the object, one to the control block.
- Solid arrows: ``car_a``, the only owner. ``use_count`` is 1.
- Dashed arrows: ``ride_`` and ``watcher``, two weak pointers. They point at the same object and control block, but they do not own it. The control block counts them: 2.

Back to `Two Separate Lifetimes`_.


After reset, in Memory
^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/step1_memory_2.png
   :alt: On the left, three blue Stack boxes under name tags car_a, maya and watcher. car_a holds two fields, object and control, each marked nullptr, with no arrows. maya holds name_, "Maya", then ride_.object and ride_.control, each marked (ptr). watcher holds object and control, each marked (ptr). On the right, a red Heap box holds one allocation, measured as 104 bytes: a control block with use_count 0 and weak_ptrs 2, then a gray dashed block under the caption Vehicle, marked destroyed: its memory stays allocated until the last weak_ptr goes. Dashed orange arrows run from ride_.object to the gray block and from ride_.control to the control block; dashed dark blue arrows do the same from watcher's object and control fields.
   :align: center
   :width: 90%

   The same code after ``car_a.reset();``.

- ``reset`` empties ``car_a``: both its pointers are null, and ``use_count`` drops to 0. With no owner left, the ``Vehicle`` is destroyed.
- The control block stays and still counts 2 weak pointers. That is how ``watcher.expired()`` can answer ``true``: it reads the control block, not the destroyed object.
- The object and its control block are one allocation, so the object's memory stays too: "the memory occupied by T persists until all weak owners get destroyed as well" (`cppreference, std::make_shared <https://en.cppreference.com/w/cpp/memory/shared_ptr/make_shared>`__, Notes). Traced with g++ 13.3: nothing is freed at ``reset`` or at ``leave``.
- ``maya.leave()`` empties ``ride_``. The 104 bytes are freed when ``watcher`` goes, at the end of the scope.

Back to `Two Separate Lifetimes`_.


Each Route Has Its Own Positions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Route maya_ride;
   maya_ride.add(Position{0.0, 0.0});      // pickup
   maya_ride.add(Position{300.0, 400.0});  // Maya's stop: 500 m
   Route shared_ride{maya_ride};           // copies the Positions too
   shared_ride.add(Position{300.0, 0.0});  // Ana's stop: 400 m more
   std::cout << maya_ride.length() << ' '
             << shared_ride.length() << '\n';  // 500 900

- Positions in m, chosen for this example: from the pickup (0, 0) to Maya's stop (300, 400) is 500 m, the long side of a 300, 400, 500 right triangle. Ana's stop is 400 m straight down, at (300, 0): 500 + 400 = 900.
- The copy has its own ``Position`` values: adding Ana's stop to ``shared_ride`` leaves ``maya_ride`` at 500 m. A part belongs to one whole.
- Run: ``702run week9_appendix xxiv``.

Back to `Exclusive Ownership Needs std::unique_ptr`_.


Aggregation or Composition
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 24 38 38

   * -
     - Aggregation
     - Composition
   * - Owners of a part
     - Several: ``std::shared_ptr``
     - One: ``std::unique_ptr``, or a plain member
   * - A part's lifetime
     - Its own
     - Its whole's
   * - UML
     - Open diamond
     - Filled diamond
   * - In the design
     - ``Fleet`` and its vehicles
     - ``Vehicle`` and its sensors

- Share only when the requirements say several objects keep the part alive, as a ``Fleet`` and ``main`` do. Otherwise one owner: ``std::unique_ptr`` or a plain member.

.. note::

   "Prefer ``unique_ptr`` over ``shared_ptr`` unless you need to share ownership". Rule: `Core Guidelines R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`__.

Back to `Composition`_.


Requirements, Not Reality
^^^^^^^^^^^^^^^^^^^^^^^^^

A program models the part of reality that its requirements need. "Owner" here means the C++ owner of `Owners Keep Objects Alive`_, not the owner in the real world.

The code departs from reality where the requirements say so:

- The company owns the cars. In the code, ``Fleet`` and ``main`` share them.
- Nothing owns a point on a map, yet a ``Route`` holds its ``Position`` values: they are destroyed with it.

.. note::

   :ref:`FR-12.3 <fr-12-3>` is why ``ride_`` is a ``std::weak_ptr``. Change the requirement and the code changes, while the real world stays the same.

- Start from reality: classes named after the domain are easy to read. When reality and the requirements disagree, the requirements win.
- The test to use: what must happen to ``B`` when ``A`` is destroyed, and which requirement says so?

Back to `Shared Ownership Needs std::shared_ptr`_.


A Route for One Call
^^^^^^^^^^^^^^^^^^^^

Here ``Vehicle`` is the concrete class you already have; the Abstraction section makes ``drive`` pure virtual.

.. code-block:: cpp

   Vehicle car_a{13.4};
   car_a.set_speed(10.0);
   {
     Route maya_ride;  // 500 m
     maya_ride.add(Position{0.0, 0.0});
     maya_ride.add(Position{300.0, 400.0});
     car_a.drive(maya_ride);
   }  // maya_ride is gone
   Route next;  // 200 m
   next.add(Position{0.0, 0.0});
   next.add(Position{0.0, 200.0});
   car_a.drive(next);

.. code-block:: text

   500 m at 10 m/s: 50 s
   200 m at 10 m/s: 20 s

- This ``drive`` prints the length and the time, length / speed: 500 / 10 = 50 s, 200 / 10 = 20 s. The speed, 10 m/s, is chosen for this example.
- ``maya_ride`` is destroyed; the ``Vehicle`` kept nothing of it.
- A dependency needs no smart pointer: a reference parameter. Core Guidelines `F.7 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-smart>`__: "For general use, take ``T*`` or ``T&`` arguments rather than smart pointers".
- Run: ``702run week9_appendix xxvii``.

Back to `A Vehicle Uses a Route`_.


Inside a Taxi Object
^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Taxi taxi{13.4, "Ana"};
   std::cout << sizeof(Vehicle) << ' '
             << sizeof(RoboTaxi) << ' '
             << sizeof(Taxi) << '\n';
   std::cout << sizeof(std::string) << '\n';

.. code-block:: text

   88 128 120
   32

The **base subobject**: the whole ``Vehicle`` at the start of every ``Taxi`` object.

- A ``Taxi`` object starts with its base subobject: 88 bytes with g++. Then its own member, a ``std::string``, 32 bytes on the second line: 88 + 32 = 120.
- ``RoboTaxi`` adds a ``std::string`` (32 bytes) and an ``int`` (4 bytes), then 4 bytes of padding: 88 + 32 + 4 + 4 = 128.
- Run: ``702run week9_appendix xxviii``.

Back to `A Base Class Reference to a Derived Object`_.


drive in the Class Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/model_l9_drive.png
   :alt: A UML class diagram with three orange boxes that each list one method. Each class name has a circled C before it, for a class: here Vehicle is not abstract. On the left, Vehicle, its name upright, with plus drive(const Route&) : void. On the right, RoboTaxi and, below it, Taxi, each with plus drive(const Route&) : void, and neither marked final. Each joins Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   Each kind of vehicle runs the ``drive`` of ``Vehicle`` in its own way (FR-3).

Each box shows only ``drive``: ``Vehicle``, ``RoboTaxi`` and ``Taxi`` each have one.

Today a ``RoboTaxi`` and a ``Taxi`` both run ``Vehicle``'s ``drive``, so they print the same trip. FR-3 asks each kind to drive its own way.

Back to `Polymorphism`_.


One Overload per Class
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void start_shift(const RoboTaxi& robotaxi, const Route& route) {
     robotaxi.drive(route);
   }
   void start_shift(const Taxi& taxi, const Route& route) {
     taxi.drive(route);
   }

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- ``start_shift(robotaxi, maya_ride)`` and ``start_shift(taxi, maya_ride)`` each pick their overload, and each vehicle drives its own way.
- Run: ``702run week9_appendix xxx``.

Back to `The Challenge`_.


Scalability and Redundancy
^^^^^^^^^^^^^^^^^^^^^^^^^^

- There is one overload per vehicle class. A robot bus needs a third ``start_shift``, and the code that calls it changes too (NFR-1 says it must not).
- Every overload has the same body, a call to ``drive(route)`` on its parameter: the same code, written again and again.
- A ``Fleet`` holds robotaxis and taxis in one ``std::vector<std::shared_ptr<Vehicle>>``. Each element is a ``std::shared_ptr<Vehicle>``, so ``*element`` has static type ``Vehicle`` and no overload can be picked for each one.

.. note::

   We need one function that takes any ``Vehicle``, and still runs each object's own ``drive``.

Back to `The Challenge`_.


What Runtime Polymorphism Needs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Inheritance**: ``RoboTaxi`` and ``Taxi`` derive from ``Vehicle``. Done.
2. **A base reference or pointer** to the object: ``Vehicle&``, ``Vehicle*``, ``std::unique_ptr<Vehicle>`` or ``std::shared_ptr<Vehicle>``. ``start_shift`` has a ``const Vehicle&``. Done.
3. **A virtual method** in the base class. Not yet.

- With 1 and 2 only, the static type picks: ``Vehicle::drive`` runs for both, as in `Through a Base Reference`_.

Back to `Through a Base Reference`_.


final in the Class Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/model_l9_final.png
   :alt: The same UML class diagram of the ride service program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi, Taxi and AutomationLevel, joined by the same lines, and RoboTaxi to AutomationLevel by an arrow labeled has level. Each class name has a circled letter before it: A for the abstract Vehicle, E for the enumerations SensorType and AutomationLevel, and C for a class on every other box, Position included. Only the RoboTaxi and Taxi boxes, each marked final, are orange; everything else is grey.
   :align: center
   :width: 100%

   ``RoboTaxi`` and ``Taxi`` are each marked «final».

- ``RoboTaxi`` and ``Taxi`` are marked «final»: the course's notation.
- «final» is not a standard UML stereotype. UML 2.5.1 calls the property isFinalSpecialization ("If true, the Classifier cannot be specialized", 9.9.4), gives it no notation, and has no «final» in its standard stereotypes (22.3, Table 22.1).

Back to `The final Keyword`_.


Discussions
^^^^^^^^^^^

The discussions of the slides, with their answers.


Discussion: Find the Classes
""""""""""""""""""""""""""""

Three new requirements for the robotaxi company:

1. A charging station charges up to four robotaxis at a time, and a robotaxi can leave the station.
2. Each taxi has a fare meter that counts the fare of the current ride.
3. An electric robotaxi is a robotaxi with a battery level from 0 to 100 %.

Which nouns become classes? Which verbs become methods?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. A ``ChargingStation`` class, with ``charge`` and ``release`` methods. The station holds robotaxis it does not own: they arrive and leave, and they live on. Its rule is at most four at a time.
   2. A ``Meter`` class, with a fare that is never below 0, so it is a class and not a struct. The meter is part of the taxi and goes away with it.
   3. An ``ElectricRoboTaxi`` is a ``RoboTaxi``: inheritance. The battery level from 0 to 100 is a data member with a rule. In the diagram, ``RoboTaxi`` is marked final, so this requirement would make us change that.

   Nouns like fare and battery level are data members, not classes. The test from `From Requirements to Classes`_: does the noun hold data and keep a rule of its own? The relationships get their names in `Class Relationships`_; `Discussion: Which Relationship?`_ comes back to the station and the meter.

Back to `Nouns and Classes`_.


Discussion: What Prints First?
""""""""""""""""""""""""""""""

.. code-block:: cpp

   struct Meter {  // the fare meter
     Meter() { std::cout << "Meter constructor\n"; }
     ~Meter() { std::cout << "~Meter\n"; }
   };
   class Taxi : public Vehicle {
    public:
     Taxi(double max_speed, std::string driver_name)
         : Vehicle{max_speed},
           driver_name_{std::move(driver_name)} {
       std::cout << "Taxi constructor\n";
     }
     ~Taxi() { std::cout << "~Taxi\n"; }
    private:
     std::string driver_name_;
     Meter meter_;
   };

``Vehicle`` prints as in `Construction and Destruction Order`_. Write the six lines one ``Taxi`` prints, from its creation to the end of its scope. Then swap the two initializers. What changes?

.. dropdown:: Answers
   :class-container: sd-border-success

   .. code-block:: text

      Vehicle constructor
      Meter constructor
      Taxi constructor
      ~Taxi
      ~Meter
      ~Vehicle

   - The base first, then the members in the order they are declared, then the body. Destruction is the reverse.
   - ``meter_`` has no initializer in the list, and it is still built before the body: every member is built before the body runs, whether the list names it or not.
   - Swapping the two initializers changes nothing in the output. g++ warns ``'Taxi::driver_name_' will be initialized after [-Wreorder]``, then ``base 'Vehicle'``. The order comes from the class, not from the list, as for members.
   - Run: ``702run week9_appendix xxxv``.

Back to `Construction and Destruction Order`_.


Discussion: Which Relationship?
"""""""""""""""""""""""""""""""

For each pair: association, aggregation, composition, dependency or inheritance? Which member or parameter would you write in C++?

1. A ``Fleet`` and a ``RoboTaxi`` it runs.
2. A ``Vehicle`` and its roof lidar.
3. A ``Taxi`` and the person who drives it.
4. A ``Taxi`` and its fare meter.
5. A charging station and the robotaxis plugged into it.
6. A ``Fleet`` and the map it plans tomorrow's routes on.

Use the questions of the chart in `Choosing a Relationship and Its C++`_, in order.

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Aggregation: a ``std::shared_ptr`` in the fleet.
   2. Composition: a ``std::unique_ptr``, as in ``Vehicle``.
   3. Association: the driver exists without the taxi, so a ``Driver`` class would be held by a ``std::weak_ptr``. The ``Taxi`` class you wrote in `Live Coding: Step 3`_ keeps only the driver's name, a ``std::string``.
   4. Composition: the meter goes with the taxi, so a plain ``Meter`` member is enough.
   5. This one can be argued. The station does not decide when a robotaxi is destroyed, so it is not composition. If it only looks at them, it is an association; if it keeps them alive while they charge, it is an aggregation.
   6. A dependency: a ``plan`` method takes the map as a parameter, and the fleet keeps no map.

Back to `Choosing a Relationship and Its C++`_.


Discussion: Which drive() Runs?
"""""""""""""""""""""""""""""""

.. code-block:: cpp

   // Vehicle::drive is virtual, and RoboTaxi overrides it.
   RoboTaxi robotaxi{13.4};
   Vehicle& ref{robotaxi};
   Vehicle* ptr{&robotaxi};
   Vehicle copy{robotaxi};

   robotaxi.drive(maya_ride);  // 1
   ref.drive(maya_ride);       // 2
   ptr->drive(maya_ride);      // 3
   copy.drive(maya_ride);      // 4

For each line: ``Vehicle::drive`` or ``RoboTaxi::drive``? Give the static type and the dynamic type.

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``RoboTaxi::drive``. The static type and the dynamic type are both ``RoboTaxi``.
   2. ``RoboTaxi::drive``. The static type is ``Vehicle``, the dynamic type is ``RoboTaxi``, and ``drive`` is ``virtual``.
   3. ``RoboTaxi::drive``, for the same reason, through a ``Vehicle*``.
   4. ``Vehicle::drive``. ``copy`` is a ``Vehicle`` object, sliced: its static type and its dynamic type are both ``Vehicle``.

   ``702run week9_appendix xxxvii`` prints ``RoboTaxi: drives itself 500 m`` three times, then ``Vehicle: drives 500 m`` once.

Back to `Slicing`_.


Discussion: Who Needs a virtual Destructor?
"""""""""""""""""""""""""""""""""""""""""""

Which of these classes of the design needs ``virtual ~ClassName() = default;``?

1. ``Vehicle``, the base of ``RoboTaxi`` and ``Taxi``.
2. ``Sensor`` and ``Route``.
3. ``Fleet``, which has no ``virtual`` method and no derived class.

A class with a ``virtual`` method gets a ``virtual`` destructor: code can then delete a derived object through a pointer to it. Rule: `Core Guidelines C.127 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-dtor>`__.

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Yes: ``Vehicle`` has a ``virtual`` method. A ``std::unique_ptr<Vehicle>`` or a ``std::shared_ptr<Vehicle>`` can own a ``RoboTaxi``, and its ``delete`` goes through ``Vehicle``.
   2. No: ``Sensor`` and ``Route`` have no ``virtual`` method, and no class derives from them, so nothing deletes them through a base pointer. A ``virtual`` destructor there would add the 8-byte vtable pointer of `The Cost of virtual`_ for nothing.
   3. No, for the same reason: ``Fleet`` has no ``virtual`` method, and no class derives from it.

   C.127 says: "A class with a virtual function should have a virtual or protected destructor". ``RoboTaxi`` and ``Taxi`` need nothing written: their destructors are already ``virtual``, because they override ``Vehicle``'s.

   ``702run week9_appendix xxxviii`` prints ``std::has_virtual_destructor_v`` for six classes: ``true`` for ``Vehicle``, ``RoboTaxi`` and ``Taxi``, ``false`` for ``Sensor``, ``Route`` and ``Fleet``.

Back to `The Sizes in the Report`_.


Discussion: Add a RoboBus
"""""""""""""""""""""""""

The company adds a robot bus with 30 seats and a maximum speed of 11.2 m/s, about 25 mph: 1 mph is 0.44704 m/s, and 25 × 0.44704 = 11.18. Both numbers are chosen for this example.

1. Which class do you write, and what must it contain?
2. Which lines of ``Fleet`` change?
3. What happens if you forget ``drive``?
4. Should ``RoboBus`` derive from ``RoboTaxi`` instead?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``class RoboBus : public Vehicle``, with a constructor that passes the maximum speed to ``Vehicle`` and sets ``seats_``, and ``drive(const Route&) const override``. The seats need a rule, more than 0, so the constructor checks it.
   2. None. NFR-1: adding a vehicle kind changes no line of ``Fleet`` or ``Passenger``. ``Fleet`` stores ``std::shared_ptr<Vehicle>``. ``702run week9_appendix xxxix`` adds a ``RoboBus`` to a ``Fleet`` and prints ``RoboBus: 30 seats, drives 500 m``.
   3. ``RoboBus`` is abstract, and creating one stops the build, as in `Forgetting One Override`_.
   4. Only if a robot bus is a robotaxi. It is a bus, so it derives from ``Vehicle``. Rule: `Core Guidelines C.120 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-domain>`__, "Use class hierarchies to represent concepts with inherent hierarchical structure (only)". The design marks ``RoboTaxi`` ``final``, as `The final Keyword`_ shows.

Back to `Fleet and Passenger Do Not Change`_.


Discussion: A Keyword for Each Method
"""""""""""""""""""""""""""""""""""""

For each method of the design, which keyword goes on it?

1. ``Vehicle::drive``
2. ``Vehicle::set_speed``
3. ``Vehicle::~Vehicle``
4. ``RoboTaxi::drive``
5. ``Vehicle::add_sensor``
6. ``Route::length``

For ``set_speed``: ``Vehicle`` promises a speed from 0 to the maximum speed. What could a derived class that overrides ``set_speed`` do to that promise?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``virtual``, and pure: ``= 0``.
   2. Nothing. If ``set_speed`` were ``virtual``, a derived class could override it and skip the check, and then ``Vehicle`` could no longer promise its invariant. C.132: "Don't make a function ``virtual`` without reason".
   3. ``virtual``, with ``= default``.
   4. ``override``. ``RoboTaxi`` is ``final``, so ``final`` on the method would say nothing more.
   5. Nothing, for the same reason as 2: ``add_sensor`` picks the sensor ids.
   6. Nothing. ``Route`` has no derived class.

Back to `The Reason for Each final`_.

std::find on a Vector
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> numbers{4, 8, 15, 16, 23, 42};
   // std::find returns end() when 15 is not there
   if (std::find(numbers.begin(), numbers.end(), 15) != numbers.end()) {
     std::cout << "15 is there\n";
   }
   // add 7 only if it is not there yet
   if (std::find(numbers.begin(), numbers.end(), 7) == numbers.end()) {
     numbers.push_back(7);
   }
   std::cout << numbers.size() << '\n';

.. code-block:: text

   15 is there
   7

- ``std::find`` is in ``<algorithm>``. It returns an iterator to the first element equal to the value, or ``end()`` when there is none.
- In ``Fleet``, the elements are ``std::shared_ptr<Vehicle>``, so ``std::find`` compares the pointers.
- Run: ``702run week9_appendix xli``.

std::erase_if on a Vector
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> numbers{4, 8, 15, 16, 23, 42};
   // erase every element the lambda accepts; it returns how many it erased
   auto erased{std::erase_if(numbers, [](int n) { return n % 2 == 0; })};
   std::cout << erased << " erased, " << numbers.size() << " left\n";
   int target{23};
   std::erase_if(numbers, [target](int n) { return n == target; });
   for (int n : numbers) {
     std::cout << n << ' ';
   }

.. code-block:: text

   4 erased, 2 left
   15

- The ``std::erase_if`` for a vector is in ``<vector>`` (C++20). The lambda gets each element and returns ``true`` for the ones to erase.
- In ``Fleet``, the lambda takes ``const std::shared_ptr<Vehicle>& vehicle`` and returns ``vehicle->get_id() == id``.
- Run: ``702run week9_appendix xlii``.
