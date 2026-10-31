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

Seven Live Coding steps: Step 1 with me (`Live Coding: Step 1`_), Steps 2 to 7 on your own.

.. _l9-upload-live-coding:

Upload Your Live Coding
^^^^^^^^^^^^^^^^^^^^^^^

You type Step 1 with me, in ``project/week9/live``. You write **Steps 2 to 7** on your own, in the time each step gives: 15 minutes for Steps 2 and 4, 10 for Step 3, and 5 for each of Steps 5 to 7. In class, I walk around and help, but I do not show the answers: the recording would give them away. Get your workspace ready before class: follow :doc:`Setup Before Class </lectures/lecture8/l8_setup>` and run the script with the week number, ``bash ~/Downloads/enpm702_setup.sh 9``.

- **Before the end of class**, upload every file of ``live/include`` and ``live/src`` to the L9 Live Coding assignment on Canvas.
- It counts toward **Participation** (5% of the grade), as complete or incomplete. Complete means the code builds and you wrote Steps 2 to 7. I do not grade it for correctness.
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
5. Run every slide: ``702run week9_playground``. Run only one slide, for example `Through a Base Reference`_: ``702run week9_playground 63``.

**Where the Classes Are**

- **common** holds every class of the diagram: ``Sensor``, ``SensorType``, ``Position`` and ``Route``, and today's ``Vehicle``, ``RoboTaxi``, ``Taxi``, ``Fleet`` and ``Passenger``. Each section file writes the earlier versions its slides need.
- The code with undefined behavior is in the **undefined** folder, built with AddressSanitizer. It runs only when you ask for its slide by number.
- **uml** holds the PlantUML file of the diagram.
- The code of the appendix is in the **appendix** folder. Run appendix frame x with ``702run week9_appendix x``.

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
      702run week9_playground 63         # only the code of slide 63
      702run week9_appendix x            # only appendix frame x (10 works too)
      live9                              # build and run the classes you write in class

   After you edit a file, build again before you run: ``702build week9_playground`` builds one program, ``702build`` builds all of them.

   Code that does not compile is in the programs, commented out: uncomment it to get the slide's error.

   The slide whose code has undefined behavior, slide 78, runs only when you ask for it by number: ``702run week9_playground 78``. A full run skips it.

.. note::

   The `Further Reading`_ part, at the end of this page, is the appendix of the slides. It is not presented. Read it on your own.

One Class per File
^^^^^^^^^^^^^^^^^^

.. grid:: 1 1 2 2
   :gutter: 2

   .. grid-item::

      .. code-block:: text

         live/
         ├── include/
         │   ├── vehicle.hpp
         │   ├── passenger.hpp
         │   ├── fleet.hpp
         │   ├── robotaxi.hpp
         │   └── taxi.hpp
         └── src/
             ├── vehicle.cpp
             ├── passenger.cpp
             ├── fleet.cpp
             ├── robotaxi.cpp
             ├── taxi.cpp
             └── main.cpp

   .. grid-item::

      - Each class has a header, with its declaration, and a source file, with its method bodies, both named after the class.
      - You find a class by its file name. A change to one class recompiles only the files that include its header: a change to ``Taxi`` recompiles ``taxi.cpp`` and the files that include ``taxi.hpp``.
      - A derived class gets its own files too: ``robotaxi.hpp`` includes ``vehicle.hpp``, because ``RoboTaxi`` needs its base. ``vehicle.hpp`` includes none of its derived classes: a base class does not know the classes derived from it.
      - So a new kind of vehicle adds two files and changes none.
      - ``main.cpp`` includes the headers it uses.

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

The Program We Will Build
-------------------------

.. figure:: /_static/images/l9/model_full.png
   :alt: A UML class diagram of the robotaxi program, with class names only, in nine boxes; every box and line is black. Vehicle, its name in italics, is in the middle. On the left, Fleet joins Vehicle by a line with an open diamond at Fleet, labeled holds, 1 at Fleet and 0..* at Vehicle; below it, Passenger has an arrow labeled rides to Vehicle, 0..* at Passenger and 0..1 at Vehicle. To the upper right, Sensor joins Vehicle by a line with a filled diamond at Vehicle, labeled owns, 1 at Vehicle and 0..* at Sensor, and a dashed arrow runs from Sensor to SensorType, marked enumeration. To the right, a dashed arrow labeled uses runs from Vehicle to Route, and Route joins Position, marked struct, by a line with a filled diamond at Route, labeled has, 1 at Route and 0..* at Position. Lower right, RoboTaxi and Taxi, both marked final, each have a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   The robotaxi program as a UML class diagram: the whole program.

- A box is a class, a line is a relationship: today's lecture says what each kind of line means. Later copies show the part being built in purple.
- This is the class diagram of the whole program, with nothing in grey. We already wrote ``Vehicle``, its ``Sensor``\ s, ``Position`` and a small ``Route``.
- Today you write the rest: ``Passenger`` with me, then ``Fleet``, ``RoboTaxi`` and ``Taxi`` on your own, and we name each kind of line between the boxes. ``Vehicle`` changes too: by the end, its ``drive`` is abstract, which is why its name is in italics.
- The diagram comes back at the start of each part, with the piece we are about to build in purple.

Requirements
------------

A **requirement** is a sentence that says what the program must do, or how well it must do it. The requirements say **what**; the design that follows says **how**. See :doc:`L9 Requirements <l9_requirements>`.

Four Kinds of Requirement
^^^^^^^^^^^^^^^^^^^^^^^^^

- A **functional** requirement says what the program does: "a Fleet adds and removes vehicles".
- A **non-functional** requirement says how well it does it: "a new kind of vehicle needs no change to Fleet".
- A **constraint** limits the choices: "the code is C++20".
- A **success criterion** says how we check the result: "every test passes".

The robotaxi program has twelve functional requirements, FR-1 to FR-12. Today's code uses five of them. See :doc:`L9 Requirements <l9_requirements>`.

Design
------

A **design** says which classes a program needs, what each class holds and does, and how the classes are connected. It comes before the code.

See :doc:`L9 Design <l9_design>`, and `OMG: Unified Modeling Language <https://www.omg.org/spec/UML/>`__.

From Requirements to Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Read each requirement for its nouns and its verbs.

- A **noun** that holds data and keeps a rule becomes a class: Fleet, Vehicle, RoboTaxi, Taxi, Passenger, Route.
- A **verb** becomes a method of the class that does it: "a Fleet adds vehicles" gives ``Fleet::add``.
- A **link between two nouns** becomes a relationship: "a Passenger boards a vehicle" (FR-12) gives an association (`Association`_).
- "**is a**" becomes inheritance: a RoboTaxi is a Vehicle (`Inheritance`_).

.. note::

   Not every noun is a class. "range" is a data member of ``Sensor``, and "Ana" is a value. A noun whose data members follow no rule is a ``struct``, like ``Position``.

Discussion: Find the Classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Three new requirements for the robotaxi company:

1. A charging station charges up to four robotaxis at a time, and a robotaxi can leave the station.
2. Each taxi has a fare meter that counts the fare of the current ride.
3. An electric robotaxi is a robotaxi with a battery level from 0 to 100 %.

Which nouns become classes? Which verbs become methods? Which link between two classes does each sentence give?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. A ``ChargingStation`` class, with ``charge`` and ``release`` methods. The station holds robotaxis it does not own: they arrive and leave, and they live on. Its rule is at most four at a time, which is the multiplicity ``0..4`` (`Multiplicity`_).
   2. A ``Meter`` class, with a fare that is never below 0, so it is a class and not a struct. The meter is part of the taxi and goes away with it.
   3. An ``ElectricRoboTaxi`` is a ``RoboTaxi``: inheritance. The battery level from 0 to 100 is a data member with a rule. In the diagram, ``RoboTaxi`` is marked final, so this requirement would make us change that.

   Nouns like fare and battery level are data members, not classes. The test from `From Requirements to Classes`_: does the noun hold data and keep a rule of its own? The relationships get their names in the next section; `Discussion: Which Relationship?`_ comes back to the station and the meter.

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
   * - «struct», «enumeration»
     - A **stereotype**: what kind of type the box is, a ``struct`` or an ``enum class``
   * - «final»
     - No class derives from this one (`Live Coding: Step 7`_)
   * - ``-ride_  0..1`` at a line's end
     - The data member that holds the class at that end, as in the box, and how many (`Multiplicity`_)

The Class Diagram, with Every Member
""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_full_members.png
   :alt: A UML class diagram of the robotaxi program with nine boxes, each listing its data members and methods, and the line ends also name the data member that holds the class at that end; every box and line is black. In the middle, Vehicle, its name in italics, with the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the left, Fleet with minus vehicles_ : vector of shared_ptr of Vehicle, plus add(shared_ptr of Vehicle) : void, plus remove(int) : bool, plus size() : size_t; a line labeled holds with an open diamond at Fleet joins it to Vehicle, 1 to 0..*, the Vehicle end named minus vehicles_. Below it, Passenger with minus name_ : string, minus ride_ : weak_ptr of Vehicle, plus Passenger(string), plus board(shared_ptr of Vehicle) : void and plus leave() : void; an arrow labeled rides runs to Vehicle, 0..* to 0..1, the Vehicle end named minus ride_. Top right, Sensor with minus id_ : int, minus type_ : SensorType, minus range_ : double, plus Sensor(int, SensorType = lidar, double = 100.0), plus get_id() : int, plus get_type() : SensorType and plus get_range() : double; a line labeled owns with a filled diamond at Vehicle joins them, 1 to 0..*, the Sensor end named minus sensors_. A dashed arrow runs from Sensor to SensorType, marked enumeration, with lidar, camera and radar. A dashed arrow labeled uses runs from Vehicle to Route, with minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double; a line labeled has with a filled diamond at Route joins Route to Position, marked struct, with plus x : double and plus y : double, 1 to 0..*, the Position end named minus waypoints_. Lower right, RoboTaxi, marked final, with plus RoboTaxi(double) and plus drive(const Route&) : void, and Taxi, marked final, with minus driver_name_ : string, plus Taxi(double, string) and plus drive(const Route&) : void; each joins Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   The same nine boxes as `The Program We Will Build`_, with their members.

- Read one box, ``Vehicle``: the name on top, in italics, which means abstract; then the data members, each ``name : type``; then the methods.
- A minus sign is ``private``, a plus sign ``public``. ``next_id_`` is underlined: a ``static`` member. ``drive`` is in italics too: a pure ``virtual`` method, which `Abstraction`_ explains.
- Every member here is in ``project/week9/common``, with the same name.

.. note::

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

Summary
^^^^^^^

- Requirements say what the program must do; the design says how. Today's code uses five of the twelve functional requirements.
- In a requirement, a noun that holds data and keeps a rule becomes a class, a verb becomes a method, and a link between two nouns becomes a relationship.
- A UML class diagram draws each class as a box with its name, data members and methods, and each relationship as a line.


Class Relationships
-------------------

A **class relationship** says how the objects of two classes are connected: one knows or uses the other, one holds the other, or one is a kind of the other.

Five Relationships
^^^^^^^^^^^^^^^^^^

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
     - A ``std::weak_ptr`` member
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
     - ``class Taxi : public Vehicle``
     - RoboTaxi is a Vehicle

- You have seen three of them on the owner map of smart pointers: a filled diamond for ``std::unique_ptr``, an open diamond for ``std::shared_ptr``, an arrow for ``std::weak_ptr``.

Association, Aggregation or Dependency
""""""""""""""""""""""""""""""""""""""

``A`` and ``B`` are two classes, joined by a line that starts at ``A``. Answer from the top:

.. list-table::
   :header-rows: 1
   :widths: 19 27 27 27

   * -
     - Dependency
     - Association
     - Aggregation
   * - Is ``B`` a data member of ``A``?
     - No: a parameter, a local variable or a return type
     - Yes
     - Yes
   * - Does ``A`` keep ``B`` alive?
     - No
     - No: ``std::weak_ptr``, or a pointer that does not own
     - Yes, with other owners: ``std::shared_ptr``
   * - UML
     - Dashed arrow
     - Solid line, or an arrow to ``B``
     - Open diamond at ``A``
   * - In the design
     - ``Vehicle`` uses ``Route``
     - ``Passenger`` rides ``Vehicle``
     - ``Fleet`` holds ``Vehicle``

- ``Vehicle`` never stores a ``Route``: it gets one as the parameter of ``drive``. That is a dependency.
- ``Passenger`` stores its ``Vehicle`` in a ``std::weak_ptr``, which never keeps the vehicle alive: association. ``Fleet`` stores ``std::shared_ptr``, so the fleet is one of the owners of each vehicle: aggregation.

.. note::

   "Precise semantics of shared aggregation varies by application area and modeler" (`UML 2.5.1 <https://www.omg.org/spec/UML/2.5.1/PDF>`__, 9.5.3). In this course, an aggregation is a whole that shares ownership of its parts. Other books draw the line elsewhere: when you read one, check what it means by the open diamond.

Association
^^^^^^^^^^^

An **association**: objects of two classes work together, and neither owns the other. Each object is created and destroyed on its own.

- A passenger rides a vehicle. The vehicle exists before the ride and after it, and so does the passenger.
- In UML, a line with an arrow. The arrow points at the class that is known: a ``Passenger`` knows its ``Vehicle``; the ``Vehicle`` does not know its passengers.

Passenger and Vehicle in the Class Diagram
""""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_association.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Passenger, Vehicle and the arrow labeled rides between them, with 0..* at Passenger and 0..1 at Vehicle, are purple; everything else is grey.
   :align: center
   :width: 100%

   A ``Passenger`` rides a ``Vehicle``: the arrow labeled ``rides``.

- The first new class is ``Passenger``, and the first kind of line is the plain arrow between ``Passenger`` and ``Vehicle``.
- The numbers at the ends are in `Multiplicity`_. Then we write the class and check in a run that a passenger never keeps the vehicle alive.

Passenger and Vehicle, Every Member
"""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_association_members.png
   :alt: A UML class diagram with only two boxes, Passenger on the left and Vehicle on the right, each listing its data members and methods; both boxes and the arrow are purple. Passenger has minus name_ : string, minus ride_ : weak_ptr of Vehicle, plus Passenger(string), plus board(shared_ptr of Vehicle) : void and plus leave() : void. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. An arrow labeled rides runs from Passenger to Vehicle, 0..* at Passenger and 0..1 at Vehicle, the Vehicle end named minus ride_.
   :align: center
   :width: 100%

   ``Passenger`` and ``Vehicle`` with every member: the arrow labeled ``rides``, its ``Vehicle`` end named ``-ride_``.

- The same two boxes as in `Passenger and Vehicle in the Class Diagram`_, with every member. ``Passenger`` is what we write in Step 1: a name, a constructor, ``board`` and ``leave``.
- ``ride_`` is in ``Passenger``'s box, with its type, ``std::weak_ptr<Vehicle>``. Its name is at the ``Vehicle`` end of the arrow too: the line says which data member holds the vehicle.
- ``Vehicle``'s box is the class you are given, in ``vehicle.hpp`` and ``vehicle.cpp``, with the id and the static counter ``next_id_``. ``drive`` is in italics: `Abstraction`_ makes it pure ``virtual``. Step 1 does not touch ``Vehicle``.

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
     - one or more

- ``0..1`` at ``Vehicle``: one passenger rides at most one vehicle at a time.
- ``0..*`` at ``Passenger``: one vehicle carries any number of passengers.
- An end with no number leaves the count open.

Live Coding: Step 1
"""""""""""""""""""

**10 minutes, with me.** We write ``Passenger`` in ``passenger.hpp`` and ``passenger.cpp``. ``Vehicle`` is given, in ``vehicle.hpp`` and ``vehicle.cpp``.

1. ``private``: ``std::string name_`` and ``std::weak_ptr<Vehicle> ride_``.
2. An ``explicit`` constructor, defined in the class. It throws for an empty name: it checks the invariant, a name that is not empty.
3. In ``passenger.cpp``, ``board`` stores the vehicle in ``ride_``, and ``leave`` resets it.
4. Uncomment the Step 1 block in ``main.cpp``: ``maya`` boards ``car_a``, then ``car_a.reset()``.

Build and run: ``live9``. The Step 1 block prints:

.. code-block:: text

   [Step 1]
   1
   true

- 1: ``board`` added no owner. ``true``: ``watcher``, a second ``std::weak_ptr``, finds the ``Vehicle`` destroyed, while ``maya`` still exists.
- The ``Vehicle`` in ``live/include/vehicle.hpp`` and ``live/src/vehicle.cpp`` is given: you do not write it. Its ``get_id`` and static counter ``next_id_`` give each vehicle an id, which ``Fleet`` needs in Step 2.
- **Checkpoint**: show me your three lines before we start Step 2.

The class we write is in `A Passenger Rides a Vehicle`_, under Further Reading.

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
   maya.leave();   // maya still exists

.. code-block:: text

   1
   1
   true

- ``13.4`` is 13.4 m/s, the maximum speed (about 30 mph).
- ``use_count()`` stays 1 after ``board``: the ``std::weak_ptr`` is not an owner.
- ``watcher`` is a second ``std::weak_ptr``, only for the check. ``reset()`` ends the only owner, and ``expired()`` is true: the ``Vehicle`` object is destroyed, although ``maya`` still refers to it.
- ``maya`` lives on: that is what "neither owns the other" means in the code.
- The type follows a requirement, not the real world: :doc:`FR-12.3 <l9_requirements>` says boarding shall not keep a vehicle alive. In C++, an owner is whoever decides when an object is destroyed, nothing more.
- A ``std::shared_ptr`` would make ``maya`` an owner: the car could not be destroyed while she holds it, even after the fleet removes it. That breaks FR-12.3: a car outside the fleet, still carrying a passenger.
- Could ``remove`` check ``use_count()`` and refuse when it is above 1? The count counts every owner, not passengers. In Step 2, ``car_b.use_count()`` is 2 just before ``remove``, with no passenger: ``main`` holds one copy and the fleet the other.
- A plain pointer or a reference does not own the car either, but it cannot tell when the car is destroyed: the next use reads freed memory. A ``std::weak_ptr`` refers to the car without owning it, and it can check first.
- Run: ``702run week9_playground 26``.

Requirements, Not Reality
"""""""""""""""""""""""""

A program models the part of reality that its requirements need. It departs from reality where they say so:

- The company owns the cars. In the code, ``Fleet`` and ``main`` share them.
- Nothing owns a point on a map, yet a ``Route`` holds its ``Position`` values: they are destroyed with it.
- In C++, an owner is whoever decides when an object is destroyed, nothing more.

.. note::

   ``Passenger`` holds a ``std::weak_ptr`` because of :doc:`FR-12.3 <l9_requirements>`: "Boarding shall not keep a vehicle alive". Change the requirement and the code changes, while the real world stays the same.

- Start from reality: classes named after the domain are easy to read. When reality and the requirements disagree, the requirements win.
- The test to use: what must happen to ``B`` when ``A`` is destroyed, and which requirement says so?

Aggregation
^^^^^^^^^^^

An **aggregation** is a whole that holds parts it does not own alone. A part can exist before the whole, after it, and in more than one whole.

- In UML, a line with an open diamond at the whole.
- A vehicle can move from one fleet to another, and it is not scrapped when a fleet closes.

Fleet and Vehicle in the Class Diagram
""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_aggregation.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Fleet, Vehicle and the line labeled holds between them, with its open diamond at Fleet, 1 at Fleet and 0..* at Vehicle, are purple; everything else is grey.
   :align: center
   :width: 100%

   A ``Fleet`` holds ``Vehicle`` objects: the line labeled ``holds``, with its open diamond.

- The open diamond sits at ``Fleet``, the whole. One fleet holds any number of vehicles.
- The diamond is open because the fleet shares its vehicles with the rest of the program. Compare the filled diamond between ``Vehicle`` and ``Sensor``, in `Composition`_.

Fleet and Vehicle, Every Member
"""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_aggregation_members.png
   :alt: A UML class diagram with only two boxes, Fleet on the left and Vehicle on the right, each listing its members; both boxes and the line are purple. Fleet has minus vehicles_ : vector of shared_ptr of Vehicle, plus add(shared_ptr of Vehicle) : void, plus remove(int) : bool and plus size() : size_t. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. A line labeled holds joins them, with an open diamond at Fleet; 1 is above the line next to the diamond, and minus vehicles_ 0..* is under the line at Vehicle.
   :align: center
   :width: 100%

   ``Fleet`` and ``Vehicle`` with every member: the line labeled ``holds``, its ``Vehicle`` end named ``-vehicles_``.

- The same two boxes as in `Fleet and Vehicle in the Class Diagram`_, with every member. ``Fleet`` is what you write in Step 2: ``add``, ``remove`` and ``size``.
- ``vehicles_`` is in ``Fleet``'s box, with its type, a ``std::vector`` of ``std::shared_ptr<Vehicle>``. Its name is at the ``Vehicle`` end of the line too.
- ``Vehicle``'s box does not change in Step 2. ``Fleet`` needs only ``get_id``, to remove a vehicle by its id.

Live Coding: Step 2
"""""""""""""""""""

**15 minutes, on your own.** Write ``Fleet`` in ``fleet.hpp`` and ``fleet.cpp``. A fleet shares its vehicles. Its invariant: no null pointer and no vehicle twice.

1. ``private``: ``vehicles_``, a ``std::vector<std::shared_ptr<Vehicle>>``.
2. ``add`` throws for a null pointer, and skips a vehicle already in the fleet. It checks the invariant before it changes anything.
3. ``remove(int id)`` erases by id with ``std::erase_if``. ``size`` returns the count. The three bodies go in ``fleet.cpp``.
4. Uncomment the Step 2 block: ``car_a`` is added twice, then ``car_b`` is removed.

Build and run: ``live9``. The Step 2 block prints:

.. code-block:: text

   [Step 2]
   2 2
   1 1

- 2 2: two vehicles, each with two owners. 1 1: after ``remove``, one vehicle, and ``car_b`` alone owns the second ``Vehicle``, which lives on.

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
- Run: ``702run week9_playground 32``.

Composition
^^^^^^^^^^^

A **composition** is a whole that owns its parts alone. Each part belongs to one whole and is destroyed with it.

- In UML, a line with a filled diamond at the whole.
- We already built one: a ``Vehicle`` owns its ``Sensor`` objects.

Two Compositions in the Class Diagram
"""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_composition.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Vehicle, Sensor, Route and Position, the owns line between Vehicle and Sensor and the has line between Route and Position, with their filled diamonds and numbers, are purple; everything else is grey.
   :align: center
   :width: 100%

   A ``Vehicle`` owns its ``Sensor`` objects, and a ``Route`` has its ``Position`` values.

- Two filled diamonds. ``Vehicle`` owns its sensors through ``std::unique_ptr``, an ownership we already built.
- ``Route`` holds its positions by value, in a ``std::vector``. That is composition too: each position belongs to one route.

The Two Compositions, Every Member
""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_composition_members.png
   :alt: A UML class diagram with four boxes, each listing its members; every box and line is purple. Top left, Route with minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double. Top right, Position, marked struct, with plus x : double and plus y : double. A line labeled has joins Route to Position, with a filled diamond at Route, 1 under the diamond and minus waypoints_ 0..* at Position. Below, on the left, Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the right, Sensor with minus id_ : int, minus type_ : SensorType, minus range_ : double, plus Sensor(int, SensorType = lidar, double = 100.0), plus get_id() : int, plus get_type() : SensorType and plus get_range() : double. A line labeled owns joins Vehicle to Sensor, with a filled diamond at Vehicle; 1 is above the line next to the diamond, and minus sensors_ 0..* is under the line at Sensor.
   :align: center
   :width: 100%

   ``Vehicle``, ``Sensor``, ``Route`` and ``Position`` with every member: the lines labeled ``owns`` and ``has``.

- The four boxes of the two compositions, with every member. ``sensors_`` is in ``Vehicle``'s box and at the ``Sensor`` end of the ``owns`` line; ``waypoints_`` is in ``Route``'s box and at the ``Position`` end of the ``has`` line.
- ``Sensor``'s ``type_`` is a ``SensorType``, the enumeration. Its box is not in this diagram, because no composition involves it.
- Nothing here is new code: ``Vehicle``, ``Sensor``, ``Route`` and ``Position`` are all in ``project/week9/common`` already.

Owned through std::unique_ptr, or by Value
""""""""""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   class Vehicle {  // cut
     // ...
    private:
     std::vector<std::unique_ptr<Sensor>>
         sensors_;
   };

   class Route {  // cut
     // ...
    private:
     std::vector<Position>
         waypoints_;
   };

- A ``Sensor`` lives on the heap, owned by one ``std::unique_ptr``. When the ``Vehicle`` is destroyed, its ``std::vector`` destroys each ``std::unique_ptr``, and each deletes its ``Sensor`` (the rule of zero).
- A ``Position`` lives inside the ``Route``'s own ``std::vector``: a plain member, no pointer.
- A ``Vehicle`` cannot be copied: two vehicles cannot share a ``Sensor``.

Each Route Has Its Own Positions
""""""""""""""""""""""""""""""""

.. code-block:: cpp

   Route trip;
   trip.add(Position{0.0, 0.0});
   trip.add(Position{300.0, 400.0});  // 500 m from the first
   Route longer{trip};                 // copies the Positions too
   longer.add(Position{300.0, 0.0});   // 400 m more
   std::cout << trip.length() << ' '
             << longer.length() << '\n';  // 500 900

- Positions in m, chosen for this example: (0, 0) to (300, 400) is 500 m, the long side of a 300, 400, 500 right triangle. Then 400 m straight down, from (300, 400) to (300, 0): 500 + 400 = 900.
- The copy has its own ``Position`` values: adding one to ``longer`` leaves ``trip`` at 500 m. A part belongs to one whole.
- Run: ``702run week9_playground 37``.

Aggregation or Composition
""""""""""""""""""""""""""

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

- When in doubt, start with composition: one owner is simpler to follow, and a ``std::unique_ptr`` can still be moved to a new owner.

.. note::

   "Prefer ``unique_ptr`` over ``shared_ptr`` unless you need to share ownership". Rule: `Core Guidelines R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`__.

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
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Vehicle, Route and the dashed arrow labeled uses between them are purple; everything else is grey.
   :align: center
   :width: 100%

   A ``Vehicle`` uses a ``Route``: the dashed arrow labeled ``uses``.

- The dashed arrow is the weakest line in the diagram. No diamond and no number: a vehicle does not hold a route, it is handed one for each drive.
- The other dashed arrow, from ``Sensor`` to ``SensorType``, is a dependency too: ``Sensor`` uses the enumeration as the type of a member.

Vehicle and Route, Every Member
"""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_dependency_members.png
   :alt: A UML class diagram with only two boxes, Vehicle on the left and Route on the right, each listing its members; both boxes and the arrow are purple. Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. Route has minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double. A dashed arrow labeled uses runs from Vehicle to Route.
   :align: center
   :width: 100%

   ``Vehicle`` and ``Route`` with every member: the dashed arrow labeled ``uses``.

- The same two boxes as in `Vehicle and Route in the Class Diagram`_, with every member. ``Route`` is in one place only in ``Vehicle``'s box: the parameter of ``drive``.
- No data member of ``Vehicle`` is a ``Route``. That is what the dashed arrow says: ``Vehicle`` uses a ``Route`` during a call and keeps nothing.
- ``Route``'s box lists ``waypoints_``, as every box lists its data members; the ``has`` line to ``Position`` is not drawn here.

A Route for One Call
""""""""""""""""""""

.. code-block:: cpp

   Vehicle car_a{13.4};
   car_a.set_speed(10.0);
   {
     Route trip;  // 500 m
     trip.add(Position{0.0, 0.0});
     trip.add(Position{300.0, 400.0});
     car_a.drive(trip);
   }  // trip is gone
   Route next;  // 200 m
   next.add(Position{0.0, 0.0});
   next.add(Position{0.0, 200.0});
   car_a.drive(next);

.. code-block:: text

   500 m at 10 m/s: 50 s
   200 m at 10 m/s: 20 s

- ``Vehicle``'s ``drive`` prints the length and the time: 500 / 10 = 50 s, 200 / 10 = 20 s. The speed, 10 m/s, is chosen for this example.
- ``trip`` is destroyed and the ``Vehicle`` is not affected: it kept nothing of it.
- Run: ``702run week9_playground 42``.

Discussion: Which Relationship?
"""""""""""""""""""""""""""""""

For each pair: association, aggregation, composition, dependency or inheritance? Which member or parameter would you write in C++?

1. A ``Fleet`` and a ``RoboTaxi`` it runs.
2. A ``Vehicle`` and its roof lidar.
3. A ``Taxi`` and the person who drives it.
4. A ``Taxi`` and its fare meter.
5. A charging station and the robotaxis plugged into it.
6. A ``Fleet`` and the map it plans tomorrow's routes on.

The test: if the first object is destroyed, is the second one destroyed too?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Aggregation: a ``std::shared_ptr`` in the fleet.
   2. Composition: a ``std::unique_ptr``, as in ``Vehicle``.
   3. Association: the driver exists without the taxi, so a ``Driver`` class would be held by a ``std::weak_ptr``. The ``Taxi`` class you write in `Live Coding: Step 3`_ keeps only the driver's name, a ``std::string``.
   4. Composition: the meter goes with the taxi, so a plain ``Meter`` member is enough.
   5. This one can be argued. The station does not decide when a robotaxi is destroyed, so it is not composition. If it only looks at them, it is an association; if it keeps them alive while they charge, it is an aggregation.
   6. A dependency: a ``plan`` method takes the map as a parameter, and the fleet keeps no map.

Inheritance
^^^^^^^^^^^

**Inheritance**: a **derived class** is built from a **base class**. It gets the base's data members and methods, and adds its own. Every derived object is also a base object: a ``RoboTaxi`` is a ``Vehicle``.

.. code-block:: cpp

   class Derived : public Base { /* what Derived adds */ };

- In UML, a hollow triangle at the base class.
- What every kind of vehicle shares (an id, the speeds and their check, the sensors) is written once, in ``Vehicle``.
- This course uses one base class per class (single inheritance).

See `Generalization and Specialization`_ and `Multiple Inheritance`_ under Further Reading.

RoboTaxi and Taxi in the Class Diagram
""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_inheritance.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Vehicle, RoboTaxi, Taxi and the two lines with a hollow triangle at Vehicle are purple; everything else is grey.
   :align: center
   :width: 100%

   ``RoboTaxi`` and ``Taxi`` each join ``Vehicle`` by a line with a hollow triangle at ``Vehicle``.

- We already wrote ``Vehicle``; ``RoboTaxi`` and ``Taxi`` were still grey. A robotaxi is a kind of vehicle, and so is a taxi. Each line with a hollow triangle says "is a".
- ``RoboTaxi`` and ``Taxi`` get everything ``Vehicle`` has. What they add is small: ``Taxi`` adds the driver's name, and each one will drive in its own way, which is polymorphism, the next section.

Vehicle, RoboTaxi and Taxi, Every Member
""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_inheritance_members.png
   :alt: A UML class diagram with three boxes, each listing its members; every box and line is purple. On the left, Vehicle, its name in italics, has the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the right, RoboTaxi, marked final, with plus RoboTaxi(double) and plus drive(const Route&) : void, and below it Taxi, marked final, with minus driver_name_ : string, plus Taxi(double, string) and plus drive(const Route&) : void. Each joins Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   ``Vehicle``, ``RoboTaxi`` and ``Taxi`` with every member: a line with a hollow triangle at ``Vehicle`` from each derived class.

- The three boxes of `RoboTaxi and Taxi in the Class Diagram`_, with every member. The boxes of ``RoboTaxi`` and ``Taxi`` are short: a derived class lists only what it adds or overrides. The rest comes from ``Vehicle`` through the hollow triangle.
- ``RoboTaxi`` adds a constructor and its own ``drive``. ``Taxi`` adds ``driver_name_``, a constructor that takes the name, and its own ``drive``. You write both in Step 3, each in its own files.

Live Coding: Step 3
"""""""""""""""""""

**10 minutes, on your own.** Derive ``RoboTaxi`` and ``Taxi`` from ``Vehicle``, each in its own files: ``robotaxi.hpp``, ``taxi.hpp`` and their ``.cpp`` files. Each line with a hollow triangle becomes one class.

1. ``class RoboTaxi : public Vehicle``. Its ``explicit`` constructor passes the maximum speed on: ``: Vehicle{max_speed}`` (`Constructors and Inheritance`_). This base class initializer builds the ``Vehicle`` part, with ``Vehicle``'s own check of the maximum speed.
2. ``class Taxi : public Vehicle``, plus a ``private`` ``driver_name_``. Its constructor passes the maximum speed on too, and ``std::move`` moves the name into ``driver_name_``.
3. Uncomment the Step 3 block: a lidar on a ``RoboTaxi``, a ``Taxi`` at 10 m/s, and one of each in a ``Fleet``.

Build and run: ``live9``. The Step 3 block prints:

.. code-block:: text

   [Step 3]
   1 10
   2

- 1 10: the ``RoboTaxi`` has one sensor and the ``Taxi`` drives at 10 m/s, all through ``Vehicle``'s methods. ``add_sensor``, ``set_speed`` and the rest come from ``Vehicle``.
- 2: a ``Fleet`` of ``Vehicle``\ s takes both kinds.

Inside a Taxi Object
""""""""""""""""""""

.. code-block:: cpp

   Taxi taxi{13.4, "Ana"};
   Vehicle& vehicle{taxi};  // no cast needed
   std::cout << sizeof(Vehicle) << ' '
             << sizeof(RoboTaxi) << ' '
             << sizeof(Taxi) << '\n';
   std::cout << sizeof(std::string) << '\n';
   std::cout << &taxi << '\n'
             << &vehicle << '\n';

.. code-block:: text

   88 88 120
   32
   0x7ffca4b98ee0
   0x7ffca4b98ee0

- A ``Taxi`` object starts with a whole ``Vehicle``, the **base subobject**: 88 bytes with g++. Then its own member, a ``std::string``, 32 bytes on the second line: 88 + 32 = 120. ``RoboTaxi`` adds nothing: 88.
- A ``Vehicle&`` binds to a ``Taxi`` with no cast: it names the ``Vehicle`` part, at the same address. The addresses are from one run; they change from run to run.
- Run: ``702run week9_playground 48``.

protected Members
^^^^^^^^^^^^^^^^^

A ``protected`` **member** is a member that the class's own methods and the methods of its derived classes can use. Other code cannot use it, as for a ``private`` member.

.. code-block:: cpp

   class Vehicle {  // the Vehicle you wrote, with one protected method
    public:     // any code
     explicit Vehicle(double max_speed,
                      const std::string& color = "white");
    protected:  // Vehicle's, RoboTaxi's and Taxi's methods
     void log_event(const std::string& event) const {
       std::cout << "vehicle " << id_ << ": " << event << '\n';
     }
    private:    // Vehicle's methods only
     int id_;  // and the rest of Vehicle's data members
   };

- A method of ``RoboTaxi`` can call ``log_event("starts")``, which prints ``vehicle 1: starts``. The same call in ``main`` does not compile: g++ says ``'void Vehicle::log_event(const std::string&) const' is protected within this context``.
- ``protected`` is the third access specifier, after ``public`` and ``private``. UML marks it with ``#``.
- Run: ``702run week9_playground 49``.

private Stays private
"""""""""""""""""""""

.. code-block:: cpp

   class RoboTaxi : public Vehicle {  // the Vehicle you wrote: speed_ is private
    public:
     void go() { speed_ = get_max_speed(); }  // does not compile
     // ...
   };

.. code-block:: text

   error: 'double Vehicle::speed_' is private within this context

- A ``RoboTaxi`` object holds ``speed_``, but ``RoboTaxi``'s methods cannot name it: only ``Vehicle``'s can.
- The fix goes through ``Vehicle``'s ``public`` method, so the check of the invariant runs:

.. code-block:: cpp

   void go() { set_speed(get_max_speed()); }

protected Data
""""""""""""""

.. code-block:: cpp

   class RoboTaxi : public Vehicle {  // speed_ is protected now
    public:
     void speed_up() { speed_ = 20.0; }  // compiles: no check
   };

- With ``speed_`` ``protected``, this compiles, and ``get_speed()`` then returns 20, above the maximum speed of 13.4. Every derived class can now break ``Vehicle``'s invariant.
- The rule for assignments stays: **every data member is** ``private``, or the assignment gets 0. Use ``protected`` for methods meant only for derived classes, as ``log_event`` in `protected Members`_.
- Run: ``702run week9_playground 51``. It prints ``20 13.4``: the speed, then the maximum speed.

.. note::

   "``protected`` data is a source of complexity and errors. ``protected`` data complicates the statement of invariants". Rule: `Core Guidelines C.133 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-protected>`__.

public Inheritance
""""""""""""""""""

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - In ``Vehicle``
     - In ``RoboTaxi``, with ``: public``
   * - ``public``
     - ``public``
   * - ``protected``
     - ``protected``
   * - ``private``
     - there, but not usable

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

See `protected and private Inheritance`_ under Further Reading.

Constructors and Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **base class initializer**: a derived constructor names its base class first in its member initializer list, with the arguments for a base constructor. The base part is built first, then the derived class's own members.

.. code-block:: cpp

   Derived(parameters) : Base{arguments}, member_{value} { body }

For ``Taxi``:

.. code-block:: cpp

   Taxi(double max_speed, std::string driver_name)
       : Vehicle{max_speed}, driver_name_{std::move(driver_name)} {}

- Each constructor sets up its own class's members: ``Vehicle``'s constructor checks the maximum speed and takes the next id, and ``Taxi``'s sets ``driver_name_``.

Without the Base Class Initializer
""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   class RoboTaxi : public Vehicle {
    public:
     explicit RoboTaxi(double max_speed) {}  // does not compile
     // ...
   };

.. code-block:: text

   error: no matching function for call to 'Vehicle::Vehicle()'
   note: candidate: 'Vehicle::Vehicle(double, double)'
   note:   candidate expects 2 arguments, 0 provided
   note: candidate: 'Vehicle::Vehicle(double, const std::string&)'
   note:   candidate expects 2 arguments, 0 provided

- With no base class initializer, C++ builds the base part with the base's default constructor. ``Vehicle`` has none: every ``Vehicle`` needs a maximum speed. The output is cut: g++ lists more candidates after these two.
- The ``Vehicle`` part must exist before the ``RoboTaxi`` constructor's body runs, so the body is too late to call ``Vehicle``'s constructor.

A Base Member in the List
"""""""""""""""""""""""""

.. code-block:: cpp

   explicit RoboTaxi(double max_speed)
       : max_speed_{max_speed} {}  // does not compile

.. code-block:: text

   error: 'double Vehicle::max_speed_' is private within this context
   error: class 'RoboTaxi' does not have any field named 'max_speed_'
   error: no matching function for call to 'Vehicle::Vehicle()'

- A member initializer list names only the class's own members and its base classes. ``max_speed_`` belongs to ``Vehicle``, so only ``Vehicle``'s constructor can initialize it.
- With ``max_speed_`` ``protected``, the second and third errors stay.

Construction and Destruction Order
""""""""""""""""""""""""""""""""""

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
- Run: ``702run week9_playground 56``.

.. note::

   In a constructor, "direct base classes are initialized in declaration order", "Then, non-static data members are initialized in the order they were declared", "Finally, the compound-statement of the constructor body is executed". C++20 **[class.base.init]** (11.10.2) paragraph 13.

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
   - Run: ``702run week9_playground 57``.

Summary
^^^^^^^

- Association knows (``std::weak_ptr``), aggregation shares (``std::shared_ptr``), composition owns alone (``std::unique_ptr`` or a plain member), dependency uses for one call (a parameter).
- Inheritance is "is a": ``class RoboTaxi : public Vehicle`` gets ``Vehicle``'s members and adds its own. Always write ``public``.
- The base's ``private`` members stay ``private``; data members are never ``protected`` in this course.
- A derived constructor names the base first in its list, ``Vehicle{max_speed}``. The base is built first and destroyed last.


Polymorphism
------------

**Polymorphism** lets one piece of code work with objects of different classes. C++ picks the function a call runs either when it compiles the code or while the program runs.

See `cppreference: virtual function specifier <https://en.cppreference.com/w/cpp/language/virtual>`__.

drive in the Class Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/model_l9_abstract.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Only the Vehicle box, its name in italics, is purple; everything else is grey.
   :align: center
   :width: 100%

   Each kind of vehicle runs the ``drive`` of ``Vehicle`` in its own way (FR-3).

- So far a ``RoboTaxi`` and a ``Taxi`` drive with ``Vehicle``'s ``drive``: they print the same trip. FR-3 asks that each kind of vehicle drives in its own way.
- The next section takes ``drive`` out of ``Vehicle`` altogether: that is why ``Vehicle`` is in italics on the diagram.

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
     explicit RoboTaxi(double max_speed) : Vehicle{max_speed} {}
     void drive(const Route& route) const {  // redefines Vehicle::drive
       std::cout << "RoboTaxi: drives itself " << route.length() << " m\n";
     }
   };

Redefinition
""""""""""""

.. code-block:: cpp

   // Taxi redefines drive() too: it prints its driver's name.
   RoboTaxi robotaxi{13.4};
   Taxi taxi{13.4, "Ana"};
   robotaxi.drive(trip);  // trip: the 500 m route
   taxi.drive(trip);

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- **Redefinition**: a derived class writes a method with the name of a base method, as ``RoboTaxi`` does in `Compile-Time Polymorphism`_. Overloading is another kind of compile-time polymorphism.
- The compiler looks for ``drive`` in the class of the object first, then in its base. ``RoboTaxi::drive`` and ``Taxi::drive`` **hide** ``Vehicle::drive``.
- A method the derived class does not write, such as ``set_speed``, is found in ``Vehicle``.
- Run: ``702run week9_playground 62``.

Through a Base Reference
""""""""""""""""""""""""

.. code-block:: cpp

   void start_shift(const Vehicle& vehicle,
                    const Route& route) {
     vehicle.drive(route);
   }

   start_shift(robotaxi, trip);
   start_shift(taxi, trip);

.. code-block:: text

   Vehicle: drives 500 m
   Vehicle: drives 500 m

The **static type** of an expression is the type written in the code: ``vehicle`` is a ``const Vehicle&``. The **dynamic type** is the class of the object it refers to while the program runs: ``RoboTaxi``, then ``Taxi``.

- The compiler sees only the static type, so it calls ``Vehicle::drive`` for both. Each object's own ``drive`` is lost.
- Run: ``702run week9_playground 63``.

One Overload per Class
""""""""""""""""""""""

.. code-block:: cpp

   void start_shift(const RoboTaxi& robotaxi,
                    const Route& route) {
     robotaxi.drive(route);
   }
   void start_shift(const Taxi& taxi,
                    const Route& route) {
     taxi.drive(route);
   }

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- The same two calls as in `Through a Base Reference`_. Overloading picks the right function, but each new kind of vehicle needs one more overload with the same body.
- A ``Fleet`` holds RoboTaxis and Taxis in one ``std::vector``. Overloads cannot help there: the elements of one ``std::vector`` all have one type.
- Run: ``702run week9_playground 64``.

Runtime Polymorphism
^^^^^^^^^^^^^^^^^^^^

A ``virtual`` **method** is a method declared ``virtual`` in a base class. A call through a base reference or pointer runs the version of the dynamic type, picked while the program runs. This is **runtime polymorphism**.

.. code-block:: cpp

   class Vehicle {
    public:
     virtual ~Vehicle() = default;  // why: virtual Destructors
     virtual void drive(const Route& route) const { /* as before */ }
   };

   class RoboTaxi : public Vehicle {
    public:
     void drive(const Route& route) const override { /* as before */ }
   };

- A derived method with the same name, parameters and ``const`` **overrides** the ``virtual`` one. ``override`` is explained in `override`_, the destructor in `virtual Destructors`_.

Live Coding: Step 4
"""""""""""""""""""

**15 minutes, on your own.** Make ``drive`` ``virtual``: one loop drives both kinds.

1. In ``Vehicle``: ``virtual void drive(const Route& route) const``, with a body in ``vehicle.cpp``.
2. In ``RoboTaxi`` and ``Taxi``: the same ``drive``, marked ``override``, each printing its own line.
3. In ``Fleet``: ``drive_all``, which calls ``drive`` on each vehicle. ``drive_all`` knows only ``Vehicle``.
4. Uncomment the Step 4 block: one of each kind in a ``Fleet``, on ``trip``, the 500 m route at the top of ``main``.

Build and run: ``live9``. The Step 4 block prints:

.. code-block:: text

   [Step 4]
   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- ``drive_all`` names only ``Vehicle``. Each object runs its own ``drive``.
- The Step 4 block prints one line for each kind. ``Vehicle``'s ``drive`` never runs here.

Under Further Reading, `One Function for Every Vehicle`_ shows the same calls without the live code.

Three Things Runtime Polymorphism Needs
"""""""""""""""""""""""""""""""""""""""

1. **Inheritance**: ``RoboTaxi`` and ``Taxi`` derive from ``Vehicle``.
2. **A base reference or pointer** to the object: ``Vehicle&``, ``Vehicle*``, ``std::unique_ptr<Vehicle>`` or ``std::shared_ptr<Vehicle>``.
3. **A** ``virtual`` **method** in the base, overridden in the derived class.

- Without 2, the static type is already the derived class, and there is nothing to pick. Without 3, the static type picks, as in `Through a Base Reference`_.

.. note::

   "A class that declares or inherits a virtual function is called a polymorphic class". C++20 **[class.virtual]** (11.7.2) paragraph 1.

The Cost of virtual
"""""""""""""""""""

.. code-block:: cpp

   using Plain = compile_time::Vehicle;  // no virtual method
   using Poly = runtime::Vehicle;        // virtual methods
   std::cout << sizeof(Plain) << ' ' << sizeof(Poly) << '\n';  // 16 24
   std::cout << std::boolalpha << std::is_polymorphic_v<Plain> << ' '
             << std::is_polymorphic_v<Poly> << '\n';  // false true

- ``compile_time::Vehicle`` is the class of `Compile-Time Polymorphism`_, and ``runtime::Vehicle`` the class of `Runtime Polymorphism`_, both in ``playground/src/polymorphism.cpp``, with the same two ``double`` members. The polymorphic one is 8 bytes larger: g++ stores a hidden pointer in it, to a table of its class's ``virtual`` methods, the **vtable**. The C++ standard leaves this to the compiler.
- ``nm -C polymorphism.cpp.o`` lists ``vtable for polymorphism::runtime::Vehicle``. Without ``-C`` (demangle), ``nm`` prints the linker's name, ``_ZTVN12polymorphism7runtime7VehicleE``. The object file is in ``build/project/week9/CMakeFiles/week9_playground.dir/playground/src/``.
- A ``virtual`` call reads that table first, so it costs a little more than a direct call.
- Run: ``702run week9_playground 68``.

.. note::

   "Redundant ``virtual`` increases run-time and object-code size". Rule: `Core Guidelines C.132 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-virtual>`__, "Don't make a function ``virtual`` without reason".

Slicing
"""""""

**Slicing**: copying a derived object into an object of its base class copies only the base part. The copy is a plain ``Vehicle``.

.. code-block:: cpp

   Taxi taxi{13.4, "Ana"};
   Vehicle copy{taxi};  // not a reference
   copy.drive(trip);
   std::vector<Vehicle> parked;
   parked.push_back(taxi);  // sliced too
   parked[0].drive(trip);
   std::cout << sizeof(Vehicle) << ' '
             << sizeof(Taxi) << '\n';

.. code-block:: text

   Vehicle: drives 500 m
   Vehicle: drives 500 m
   24 56

- 24 of the 56 bytes are copied: ``driver_name_`` is left behind, and the copy's dynamic type is ``Vehicle``. Rule: `Core Guidelines ES.63 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-slice>`__, "Don't slice".
- These are the ``runtime::`` classes of `The Cost of virtual`_: 24 bytes for ``Vehicle``, plus the 32-byte ``std::string`` of ``Taxi``.
- Run: ``702run week9_playground 69``.

See `Copying a Vehicle of the Design`_ under Further Reading.

Discussion: Which drive() Runs?
"""""""""""""""""""""""""""""""

.. code-block:: cpp

   // Vehicle::drive is virtual, and RoboTaxi overrides it.
   RoboTaxi robotaxi{13.4};
   Vehicle& ref{robotaxi};
   Vehicle* ptr{&robotaxi};
   Vehicle copy{robotaxi};

   robotaxi.drive(trip);      // 1
   ref.drive(trip);           // 2
   ptr->drive(trip);          // 3
   copy.drive(trip);          // 4
   ref.Vehicle::drive(trip);  // 5

For each line: ``Vehicle::drive`` or ``RoboTaxi::drive``? Give the static type and the dynamic type.

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``RoboTaxi::drive``. The static type and the dynamic type are both ``RoboTaxi``.
   2. ``RoboTaxi::drive``. The static type is ``Vehicle``, the dynamic type is ``RoboTaxi``, and ``drive`` is ``virtual``.
   3. ``RoboTaxi::drive``, for the same reason, through a ``Vehicle*``.
   4. ``Vehicle::drive``. ``copy`` is a ``Vehicle`` object, sliced: its static type and its dynamic type are both ``Vehicle``.
   5. ``Vehicle::drive``. Naming the class, ``Vehicle::drive``, turns off the virtual call. This is how an override calls the base's version on purpose.

   ``702run week9_playground 70`` prints ``RoboTaxi: drives itself 500 m`` three times, then ``Vehicle: drives 500 m`` twice.

override
^^^^^^^^

``override`` is written after a derived method's parameter list and its ``const``. The compiler checks that the method overrides a ``virtual`` method of a base class, and stops with an error if it does not.

.. code-block:: cpp

   class RoboTaxi : public Vehicle {
    public:
     void drive(const Route& route) const override;  // must override
   };

- ``RoboTaxi::drive`` is ``virtual`` too, without the keyword. C++20 **[class.virtual]** (11.7.2) paragraph 1: "A non-static member function is a virtual function if it is first declared with the keyword virtual or if it overrides a virtual member function declared in a base class".

.. note::

   "Virtual functions should specify exactly one of ``virtual``, ``override``, or ``final``". Rule: `Core Guidelines C.128 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-override>`__. In the base: ``virtual``. In a derived class: ``override``.

A Typo That Compiles
""""""""""""""""""""

.. code-block:: cpp

   class RoboTaxi : public Vehicle {
    public:
     void drvie(const Route& route) const {  // a typo, and no override
       std::cout << "RoboTaxi: drives itself " << route.length() << " m\n";
     }
   };
   start_shift(robotaxi, trip);  // prints Vehicle: drives 500 m

- ``drvie`` is a new method of ``RoboTaxi``. Nothing overrides ``drive``, and g++ gives no warning.
- With ``drive(const Route& route)`` and no ``const``, the name matches but the ``const`` does not: it is still a new method. It compiles; ``-Wall`` only warns:

.. code-block:: text

   warning: 'virtual void Vehicle::drive(const Route&) const'
            was hidden [-Woverloaded-virtual=]
   note:   by 'void RoboTaxi::drive(const Route&)'

- Run: ``702run week9_playground 72``.

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

- Both mistakes now stop the build, on the line that has them. Without ``override``, the first one showed only as a wrong line of output.

.. note::

   "If a virtual function is marked with the virt-specifier ``override`` and does not override a member function of a base class, the program is ill-formed". C++20 **[class.virtual]** (11.7.2) paragraph 5.

auto or a Base Pointer
^^^^^^^^^^^^^^^^^^^^^^

**The type** ``auto`` **deduces**: ``auto`` takes the type of its initializer. ``std::make_unique<RoboTaxi>`` returns a ``std::unique_ptr<RoboTaxi>``, so that is the type ``auto`` gives, not ``std::unique_ptr<Vehicle>``.

.. code-block:: cpp

   auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
   // robotaxi is a std::unique_ptr<RoboTaxi>: checked with static_assert

   std::unique_ptr<Vehicle> vehicle{std::make_unique<RoboTaxi>(13.4)};
   // vehicle is a std::unique_ptr<Vehicle> to a RoboTaxi

- Both own a ``RoboTaxi``. They differ in the static type, so they differ in what the variable can hold later and what the code can call.

Two Pointers, Two Static Types
""""""""""""""""""""""""""""""

.. code-block:: cpp

   auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
   std::unique_ptr<Vehicle> vehicle{std::make_unique<RoboTaxi>(13.4)};
   robotaxi->drive(trip);  // RoboTaxi: drives itself 500 m
   vehicle->drive(trip);   // RoboTaxi: drives itself 500 m
   vehicle = std::make_unique<Taxi>(13.4, "Ana");   // any Vehicle: OK
   vehicle->drive(trip);   // Taxi: Ana drives 500 m
   robotaxi = std::make_unique<Taxi>(13.4, "Ana");  // does not compile

.. code-block:: text

   error: no match for 'operator=' (operand types are
          'std::unique_ptr<RoboTaxi, std::default_delete<RoboTaxi> >'
          and 'std::__detail::__unique_ptr_t<Taxi>')

- A ``std::unique_ptr<Vehicle>`` can own any kind of vehicle, one after the other. A ``std::unique_ptr<RoboTaxi>`` owns robotaxis only.
- The compiler checks every name against the static type. If ``RoboTaxi`` had a method of its own, only ``robotaxi`` could call it.
- Run: ``702run week9_playground 75``.

From auto into a Vector of Vehicles
"""""""""""""""""""""""""""""""""""

.. code-block:: cpp

   void start_shift(std::unique_ptr<Vehicle> vehicle, const Route& route) {
     vehicle->drive(route);
   }

   std::vector<std::unique_ptr<Vehicle>> vehicles;
   auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
   vehicles.push_back(std::move(robotaxi));              // converts
   auto taxi{std::make_unique<Taxi>(13.4, "Ana")};
   vehicles.emplace_back(std::move(taxi));               // converts too
   std::cout << vehicles.size() << '\n';                 // 2
   start_shift(std::make_unique<RoboTaxi>(13.4), trip);  // RoboTaxi::drive

- A ``std::unique_ptr<RoboTaxi>`` that is moved converts to a ``std::unique_ptr<Vehicle>``: ``push_back``, ``emplace_back`` and a ``std::unique_ptr<Vehicle>`` parameter all accept it.
- Use ``auto`` while the code needs the ``RoboTaxi`` type, then move the pointer.
- Run: ``702run week9_playground 76``.

See `auto or a Base Pointer: Summary`_ under Further Reading.

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

   // ~Vehicle is not virtual. Both destructors print their names.
   std::unique_ptr<Vehicle> vehicle{
       std::make_unique<Taxi>(13.4, "Ana Maria Rodrigues")};
   vehicle->drive(trip);

**Output:**

.. code-block:: text

   Taxi: Ana Maria Rodrigues drives 500 m
   ~Vehicle

- ``vehicle`` deletes a ``Vehicle*``. Its destructor is not ``virtual``, so the static type picks it: only ``~Vehicle`` runs. ``~Taxi`` never runs, and neither does the destructor of its ``std::string``: undefined behavior (`virtual Destructors`_).
- The name has 19 characters, more than the 15 a ``std::string`` of g++ keeps inside itself, so the name is on the heap.
- Run: ``702run week9_playground 78``. It prints the two lines above, then AddressSanitizer stops the run:

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

Live Coding: Step 5
"""""""""""""""""""

**5 minutes, on your own.** Delete a ``Taxi`` through a ``Vehicle`` pointer, as in `Deleting through a Base Pointer`_, then add a ``virtual`` destructor. Your ``Vehicle`` has a ``virtual`` method since Step 4, but its destructor is not ``virtual`` yet.

1. Uncomment the Step 5 block: a ``std::unique_ptr<Vehicle>`` owns a ``Taxi`` driven by Ana Maria Rodrigues. Build: no warning. Run: the ``Taxi`` drives 500 m, then AddressSanitizer stops the program.
2. In ``Vehicle``, in ``vehicle.hpp``: ``virtual ~Vehicle() = default;``. Run again: the same line, and no report.

Item 1 gives (the stack traces are cut):

.. code-block:: text

   ERROR: AddressSanitizer: new-delete-type-mismatch on 0x... in thread T0:
     object passed to delete has wrong type:
     size of the allocated type:   128 bytes;
     size of the deallocated type: 96 bytes.

- AddressSanitizer saw 128 bytes allocated for a ``Taxi`` and freed as a 96-byte ``Vehicle``.
- 96: your ``Vehicle``, 88 bytes measured with g++, and the 8-byte vtable pointer of Step 4 (`The Cost of virtual`_). A ``Taxi`` adds its ``std::string``, 32 bytes: 96 + 32 = 128. These sizes differ from the 56 and 24 of `Deleting through a Base Pointer`_ because your ``Vehicle`` is the full class, with every data member.
- After item 2, the program ends normally. The ``delete`` now runs ``~Taxi`` first, which frees the driver's name, then ``~Vehicle``.

The code this step replaces is in `With a virtual Destructor`_, under Further Reading.

Discussion: Who Needs a virtual Destructor?
"""""""""""""""""""""""""""""""""""""""""""

Which of these classes of the design needs ``virtual ~ClassName() = default;``?

1. ``Vehicle``, the base of ``RoboTaxi`` and ``Taxi``.
2. ``RoboTaxi``, which no class derives from.
3. ``Sensor`` and ``Route``.
4. ``Fleet``, which has no ``virtual`` method and no derived class.
5. ``Vehicle`` as you first wrote it, before anything derived from it.

The test: can some code delete an object of a derived class through a pointer to this class?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Yes: a ``std::unique_ptr<Vehicle>`` or a ``std::shared_ptr<Vehicle>`` can own a ``RoboTaxi``, and its ``delete`` goes through ``Vehicle``.
   2. Nothing to write: its destructor is already ``virtual``, because it overrides ``Vehicle``'s.
   3. No: no class derives from ``Sensor`` or ``Route``, so nothing deletes them through a base pointer. A ``virtual`` destructor there would add the 8 bytes of `The Cost of virtual`_ for no reason.
   4. No, for the same reason: no class derives from ``Fleet``.
   5. No, until we derived from it and kept RoboTaxis behind ``Vehicle`` pointers. Adding the first ``virtual`` method to a class is the moment to add the ``virtual`` destructor: "A class with a virtual function should have a virtual or protected destructor". Rule: `Core Guidelines C.127 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-dtor>`__.

   ``702run week9_playground 80`` prints ``std::has_virtual_destructor_v`` for six classes: ``true`` for ``Vehicle``, ``RoboTaxi`` and ``Taxi``, ``false`` for ``Sensor``, ``Route`` and ``Fleet``.

Summary
^^^^^^^

- Without ``virtual``, the static type picks the method. With ``virtual`` and a base reference or pointer, the dynamic type picks it while the program runs.
- Mark every override ``override``: a typo or a missing ``const`` then stops the build. Copying into a base object slices.
- ``auto`` keeps the derived type; moving the pointer converts it to a base pointer.
- A base class whose objects are deleted through base pointers needs a ``virtual`` destructor.


Abstraction
-----------

An **abstract class** declares what every derived class must do, and leaves how to each one. No object of an abstract class can be created.

See `cppreference: Abstract class <https://en.cppreference.com/w/cpp/language/abstract_class>`__.

Pure virtual Methods
^^^^^^^^^^^^^^^^^^^^

A **pure** ``virtual`` **method** is a ``virtual`` method declared with ``= 0``. The class gives it no body, and a class with one is abstract.

.. code-block:: cpp

   class Vehicle {  // abstract
    public:
     explicit Vehicle(double max_speed,
                      const std::string& color = "white");
     virtual ~Vehicle() = default;
     virtual void drive(const Route& route) const = 0;  // no body
     // ... the rest of Vehicle's members: id, speeds, color, mileage, sensors
   };

- A vehicle that is neither a robotaxi nor a taxi has no way to drive, so ``Vehicle::drive`` has no right body to write. FR-3 says the same: each kind of vehicle drives in its own way.

.. note::

   "A class is an abstract class if it has at least one pure virtual function". C++20 **[class.abstract]** (11.7.3) paragraph 2.

Live Coding: Step 6
"""""""""""""""""""

**5 minutes, on your own.** Make ``drive`` pure ``virtual``, so ``Vehicle`` is abstract: no ``Vehicle`` object can be created.

1. In ``Vehicle``, ``drive`` ends with ``= 0``. Delete its body from ``vehicle.cpp``: a pure ``virtual`` method has no body here.
2. In the Step 1 and Step 2 blocks, ``std::make_shared<Vehicle>`` becomes ``std::make_shared<RoboTaxi>``.
3. Uncomment ``Vehicle vehicle{13.4}``, build, and read the error. Then comment it out again.
4. Build and run: the Step 4 block still drives a ``RoboTaxi`` and a ``Taxi``.

Item 3 gives:

.. code-block:: text

   error: cannot declare variable 'vehicle' to be of abstract type 'Vehicle'
   note:   because the following virtual functions are pure within 'Vehicle':
   note:     'virtual void Vehicle::drive(const Route&) const'

- Without item 2, the Step 1 and Step 2 blocks fail inside ``std::make_shared``: ``invalid new-expression of abstract class type 'Vehicle'``. They create ``Vehicle`` objects. ``Passenger`` and ``Fleet`` do not change: they only point to ``Vehicle``\ s.
- The note of the error names the pure ``virtual`` method.
- ``RoboTaxi`` and ``Taxi`` override ``drive``, so their objects can still be created, and a pointer to ``Vehicle`` that points to one is fine.

Under Further Reading, `No Vehicle Objects`_ and `RoboTaxi and Taxi`_ show the code this step replaces.

The Abstract Vehicle in the Class Diagram
"""""""""""""""""""""""""""""""""""""""""

.. figure:: /_static/images/l9/model_l9_abstract.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Only the Vehicle box, its name in italics, is purple; everything else is grey.
   :align: center
   :width: 100%

   The name ``Vehicle`` is in italics: UML's mark for an abstract class.

- The same diagram as in `drive in the Class Diagram`_, and now the italics can be read. ``Vehicle`` is abstract, and so is its ``drive``, in italics in `The Class Diagram, with Every Member`_.
- ``Fleet``, ``Passenger`` and ``Route`` name only ``Vehicle``, so their boxes do not change. `The Whole Program`_ checks it.

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

The Whole Program
"""""""""""""""""

.. code-block:: cpp

   auto robotaxi{std::make_shared<RoboTaxi>(13.4)};
   robotaxi->add_sensor(SensorType::lidar, 100.0);
   robotaxi->add_sensor(SensorType::camera, 80.0);
   auto taxi{std::make_shared<Taxi>(13.4, "Ana")};
   Fleet fleet;
   fleet.add(robotaxi);  // std::shared_ptr<RoboTaxi> converts
   fleet.add(taxi);
   Passenger maya{"Maya"};
   maya.board(robotaxi);
   const std::vector<std::shared_ptr<Vehicle>> today{robotaxi, taxi};
   for (const std::shared_ptr<Vehicle>& vehicle : today) {
     vehicle->drive(trip);
   }

.. code-block:: text

   RoboTaxi: 2 sensors checked, drives 500 m
   Taxi: Ana drives 500 m

- ``Fleet`` and ``Passenger`` are the classes of Steps 1 and 2 (`Live Coding: Step 1`_ and `Live Coding: Step 2`_). Step 6 made ``Vehicle`` abstract and changed not one line of them: they name only ``Vehicle``.
- Run: ``702run week9_playground 88``.

Discussion: Add a RoboBus
"""""""""""""""""""""""""

The company adds a robot bus with 30 seats and a maximum speed of 11.2 m/s, about 25 mph: 1 mph is 0.44704 m/s, and 25 × 0.44704 = 11.18. Both numbers are chosen for this example.

1. Which class do you write, and what must it contain?
2. Which lines of ``Fleet`` change?
3. What happens if you forget ``drive``?
4. Should ``RoboBus`` derive from ``RoboTaxi`` instead?

The design has a non-functional requirement for this case: a new kind of vehicle needs no change to ``Fleet``.

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``class RoboBus final : public Vehicle``, with a constructor that passes the maximum speed to ``Vehicle`` and sets ``seats_``, and ``drive(const Route&) const override``. The seats need a rule, more than 0, so the constructor checks it.
   2. None. ``Fleet`` stores ``std::shared_ptr<Vehicle>``. ``702run week9_playground 89`` adds a ``RoboBus`` to a ``Fleet`` and prints ``RoboBus: 30 seats, drives 500 m``.
   3. ``RoboBus`` is abstract, and creating one stops the build, as in `Forgetting One Override`_.
   4. Only if a robot bus is a robotaxi. It is a bus, so it derives from ``Vehicle``. Rule: `Core Guidelines C.120 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-domain>`__, "Use class hierarchies to represent concepts with inherent hierarchical structure (only)". And ``RoboTaxi`` is ``final``: nothing derives from it.

Summary
^^^^^^^

- A pure ``virtual`` method (``= 0``) has no body and makes its class abstract: no object of it can be created, but references and pointers to it can.
- A concrete class overrides every pure ``virtual`` method it inherits. A class that forgets one is abstract too.
- ``Fleet`` and ``Passenger`` name only ``Vehicle``, so not one line of them changed when ``Vehicle`` became abstract.


The final Keyword
-----------------

``final`` after a class name stops other classes from deriving from it. ``final`` after a ``virtual`` method stops derived classes from overriding it.

See `cppreference: final specifier <https://en.cppreference.com/w/cpp/language/final>`__.

Live Coding: Step 7
^^^^^^^^^^^^^^^^^^^

**5 minutes, on your own.** Mark ``RoboTaxi`` and ``Taxi`` ``final``: no class can derive from them. The last step is one word in each class.

1. ``class RoboTaxi final : public Vehicle``, and the same for ``Taxi``.
2. In ``main.cpp``, above ``main``, write ``class SuperRoboTaxi : public RoboTaxi {};``. Build, read the error, then delete it.
3. Build and run: the output does not change. It is the output of Steps 1 to 5 again.

Item 2 gives:

.. code-block:: text

   error: cannot derive from 'final' base 'RoboTaxi' in derived type 'SuperRoboTaxi'

- ``RoboTaxi`` and ``Taxi`` are the leaves of the design: no class derives from them, and ``final`` makes the compiler check it.

The code this step replaces is in `A final Class`_, under Further Reading.

final in the Class Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l9/model_l9_final.png
   :alt: The same UML class diagram of the robotaxi program, with class names only: Fleet, Passenger, Vehicle, Sensor, SensorType, Route, Position, RoboTaxi and Taxi, joined by the same lines. Only the RoboTaxi and Taxi boxes, each marked final, are purple; everything else is grey.
   :align: center
   :width: 100%

   ``RoboTaxi`` and ``Taxi`` are each marked «final».

- The last word of the diagram: ``final``, on ``RoboTaxi`` and ``Taxi``. They are the leaves of the hierarchy, and the design says nothing derives from them.
- ``final`` is not a relationship: it is a promise the compiler checks.

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

virtual, override and final
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 45 35

   * - On a method
     - Means (C.128)
     - In the design
   * - ``virtual``
     - "this is a new virtual function"
     - ``Vehicle::drive``, ``~Vehicle``
   * - ``override``
     - "this is a non-final overrider"
     - ``RoboTaxi::drive``, ``Taxi::drive``
   * - ``final``
     - "this is a final overrider"
     - ``Taxi::drive`` in `A final Method`_

- A ``final`` class needs no ``final`` on its methods: nothing can derive from it to override them.
- ``final`` closes a design for every later programmer. Use it when deriving would break something, not by habit.

.. note::

   "Capping a hierarchy with ``final`` classes is rarely needed for logical reasons and can be damaging to the extensibility of a hierarchy". Rule: `Core Guidelines C.139 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-final>`__, "Use ``final`` on classes sparingly".

Discussion: virtual, override, final or Nothing?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each method of the design, which keyword goes on it?

1. ``Vehicle::drive``
2. ``Vehicle::set_speed``
3. ``Vehicle::~Vehicle``
4. ``RoboTaxi::drive``
5. ``Vehicle::add_sensor``
6. ``Route::length``

For ``set_speed``: what would a derived class that overrides it be able to do to the invariant?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. ``virtual``, and pure: ``= 0``.
   2. Nothing. If ``set_speed`` were ``virtual``, a derived class could override it and skip the check, and then ``Vehicle`` could no longer promise its invariant. C.132: "Don't make a function ``virtual`` without reason".
   3. ``virtual``, with ``= default``.
   4. ``override``. ``RoboTaxi`` is ``final``, so ``final`` on the method would say nothing more.
   5. Nothing, for the same reason as 2: ``add_sensor`` picks the sensor ids.
   6. Nothing. ``Route`` has no derived class.

Summary
^^^^^^^

- ``final`` after a class name stops other classes from deriving from it. After a ``virtual`` method, it stops derived classes from overriding it.
- In the base, ``virtual``; in a derived class, ``override``; on the last override, ``final`` (C.128).
- ``final`` closes a design for every later programmer, so use it sparingly (C.139).


Further Reading
---------------

The sections below come from the appendix of the slides. They are **not presented** in the lecture, and the quizzes and the exercise do not test them. Read them on your own.

.. list-table::
   :header-rows: 1
   :widths: 22 42 36

   * - Topic
     - Section (appendix frames)
     - What it adds
   * - Design
     - `All Twelve Requirements`_ (ii)
     - The full list, FR-1 to FR-12
   * - Live Coding
     - `What the Live Coding Replaces`_ (iii to viii)
     - The class of Step 1, and code that goes with Steps 4 to 7, each with a link back
   * - Class Relationships
     - `Generalization and Specialization`_ (ix)
     - Two ways to find a base class
   * - Class Relationships
     - `Multiple Inheritance`_ (x)
     - A class with two base classes
   * - Class Relationships
     - `protected and private Inheritance`_ (xi)
     - The full access table
   * - Polymorphism
     - `auto or a Base Pointer: Summary`_ (xii)
     - What each one allows
   * - Polymorphism
     - `Copying a Vehicle of the Design`_ (xiii)
     - Why the copy fails, and how to delete it

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

- Today's code covers FR-3, FR-4, FR-5, FR-10 and FR-12, listed with their code on :doc:`L9 Requirements <l9_requirements>`.

Back to `Requirements`_.

What the Live Coding Replaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These sections show the class of Live Coding Step 1, and code that goes with Steps 4 to 7, as slides, in the order of the lecture.

A Passenger Rides a Vehicle
"""""""""""""""""""""""""""

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

One Function for Every Vehicle
""""""""""""""""""""""""""""""

.. code-block:: cpp

   void start_shift(const Vehicle& vehicle,
                    const Route& route) {
     vehicle.drive(route);
   }

   start_shift(robotaxi, trip);
   start_shift(taxi, trip);

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- The same ``start_shift`` as in `Through a Base Reference`_. Only ``virtual`` changed, and each object now runs its own ``drive``.
- ``start_shift`` serves every class derived from ``Vehicle``, including classes written after it.
- Run: ``702run week9_appendix iv``.

Back to `Live Coding: Step 4`_.

With a virtual Destructor
"""""""""""""""""""""""""

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

**Output:**

.. code-block:: text

   Taxi: Ana Maria Rodrigues drives 500 m
   ~Taxi
   ~Vehicle

- The ``delete`` of `Deleting through a Base Pointer`_ now runs ``~Taxi``, then ``~Vehicle``. Built with AddressSanitizer: no error, no leak.
- ``~Taxi`` overrides ``~Vehicle`` although the names differ (**[class.virtual]** (11.7.2) paragraph 7).
- Run: ``702run week9_appendix v``.

.. note::

   "A base class destructor should be either public and virtual, or protected and non-virtual". Rule: `Core Guidelines C.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual>`__.

Back to `Live Coding: Step 5`_.

No Vehicle Objects
""""""""""""""""""

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
   vehicle.drive(trip);

.. code-block:: text

   RoboTaxi: 1 sensor checked, drives 500 m

- References and pointers to ``Vehicle`` are fine: they refer to a ``RoboTaxi`` or a ``Taxi``. Slicing cannot be written now: ``Vehicle copy{robotaxi};`` gives the same first error.
- Run: ``702run week9_appendix vi``.

Back to `Live Coding: Step 6`_.

RoboTaxi and Taxi
"""""""""""""""""

.. code-block:: cpp

   RoboTaxi robotaxi{13.4};
   robotaxi.drive(trip);
   robotaxi.add_sensor(SensorType::lidar, 100.0);
   robotaxi.drive(trip);
   Taxi taxi{13.4, "Ana"};
   taxi.drive(trip);

.. code-block:: text

   RoboTaxi: no sensor, stays parked
   RoboTaxi: 1 sensor checked, drives 500 m
   Taxi: Ana drives 500 m

- ``Taxi`` overrides ``drive`` too: it prints its driver's name, as in `Redefinition`_.
- Both are concrete: each overrides ``drive``.
- Run: ``702run week9_appendix vii``.

Back to `Live Coding: Step 6`_.

A final Class
"""""""""""""

.. code-block:: cpp

   class RoboTaxi final : public Vehicle {
     // ...
   };

   class SuperRoboTaxi : public RoboTaxi {};  // does not compile

.. code-block:: text

   error: cannot derive from 'final' base 'RoboTaxi' in derived type 'SuperRoboTaxi'

- ``RoboTaxi`` and ``Taxi`` are the leaves of the design, so both are ``final`` in ``project/week9/common``.

.. note::

   "If a class is marked with the class-virt-specifier ``final`` and it appears as a class-or-decltype in a base-clause (11.7), the program is ill-formed". C++20 **[class.pre]** (11.1) paragraph 5.

Back to `Live Coding: Step 7`_.

Generalization and Specialization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Generalization**: starting from classes you already have, and moving what they share up into a new base class: bottom-up.

**Specialization**: starting from a base class, and writing a derived class for objects that need more: top-down.

.. figure:: /_static/images/l9/generalization.png
   :alt: A class diagram: Vehicle, in italics, on top; RoboTaxi and Taxi, each marked final, below it, each joined to Vehicle by a line with a hollow triangle at Vehicle. A thick arrow on the left, tagged 1, points up. A thick arrow on the right, tagged 2, points down.
   :align: center
   :width: 60%

   1: generalization, bottom-up. 2: specialization, top-down.

- 2, specialization: ``Vehicle`` came first. Today, ``RoboTaxi`` and ``Taxi`` derive from it, and `Discussion: Add a RoboBus`_ adds ``RoboBus``.
- 1, generalization: if a program had separate ``RoboTaxi`` and ``Taxi`` classes, each with its own speeds and its own check, the shared part would move up into a new ``Vehicle``.
- Both end with the same diagram: a hollow triangle at the base.

Back to `Inheritance`_.

Multiple Inheritance
^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class Chargeable {  // can be charged
    public:
     virtual ~Chargeable() = default;
     virtual void charge() = 0;
   };

   class ElectricTaxi final
       : public Vehicle, public Chargeable {
    public:
     explicit ElectricTaxi(double max_speed)
         : Vehicle{max_speed} {}
     void drive(const Route& route) const override;
     void charge() override;
   };

- A class can have more than one base class, separated by commas. An ``ElectricTaxi`` is a ``Vehicle`` and a ``Chargeable``.
- A ``Vehicle&`` and a ``Chargeable&`` can both refer to it.
- This course uses single inheritance.
- Run: ``702run week9_appendix x``. It prints ``ElectricTaxi: drives 500 m`` through the ``Vehicle&``, then ``ElectricTaxi: charges`` through the ``Chargeable&``.

Back to `Inheritance`_.

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
     - not usable
     - not usable
     - not usable

- Each cell is the access the member has in the derived class. The ``private`` members of the base are inherited (they are in the object) but cannot be named.
- With ``protected`` or ``private`` inheritance, outside code cannot use a derived object as a base object: the "is a" is hidden. This course uses only ``public`` inheritance.

.. note::

   C++20 **[class.access.base]** (11.9.2) paragraph 1 states the ``public`` and ``protected`` rows of each column. Its footnote 112 gives the ``private`` row: private members of a base class "remain inaccessible even to derived classes", unless the base class declares the derived class a friend.

Back to `public Inheritance`_.

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
- Every "Yes" and "No" was compiled with g++ 13.3, C++20. The first row used a test method added to ``RoboTaxi``, which the design does not have.

Back to `From auto into a Vector of Vehicles`_.

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
