====================================================
RWA3: Smart Pointers and OOP
====================================================

Overview
--------

In this assignment you build a small object-oriented program of your own.
You choose one of three themes, and you do what Lecture 9 did for the ride
service program: you write the requirements, you design the classes and
draw the class diagram, and you write the code that meets them.

The theme gives you a world, not a design. You decide which classes
exist, what each one holds, and how they are related. The report explains
each decision, and the code shows that it works: your program must show
**inheritance**, **polymorphism**, **abstraction**, **aggregation** and
**composition**.

Everything in this assignment comes from Lectures 7 to 9: smart pointers
(Lecture 7), classes (Lecture 8), and relationships, inheritance and
polymorphism (Lecture 9).

.. important::

   **Posted Tue, Nov 3, due Tue, Nov 17.** Start with the requirements
   (R1). The design (R2) comes from them, and the code (R3 to R5) comes
   from the design.


.. admonition:: Using AI on this assignment
   :class: important

   RWA3 is graded on your own decisions, so its rule is **stricter than
   the course AI policy** from :doc:`Lecture 1 </lectures/lecture1/l1_lecture>`:
   a tool may help you understand, debug and test your work, but it may
   not produce any part of it.

   * You **may** use a tool such as TerpAI, ChatGPT, Claude, Gemini or
     Copilot to:

     * explain a concept from the lectures, for example what a
       ``virtual`` destructor does or when to use ``std::shared_ptr``;
     * explain a compiler error or a Valgrind report;
     * suggest how to find a bug in code **you** wrote;
     * suggest test cases for a class **you** wrote;
     * review code **you** wrote and point out problems, which you then
       fix yourself.

   * You **may not** use a tool to write any part of what you hand in: no
     requirement or definition, no class diagram or PlantUML, no
     relationship table or decision chart answer, no class, method or
     ``main.cpp`` code, no test program (including the ungraded ones of the
     Tips: you write those yourself), and no Doxygen comment. Code
     completion that fills in more than the rest of the name you are
     typing (a suggested line or function) counts as generated code: turn
     it off for this assignment. Generated work is not allowed in RWA3,
     even when you disclose it.
   * You **must** say at the top of your ``README.md`` which tool you used
     and what for, in two or three sentences. Disclosing an allowed use
     carries no penalty. Undisclosed use is a violation of the Code of
     Academic Integrity.
   * You are responsible for every line you hand in, and you may be asked
     to walk through any part of your project and say where each decision
     came from.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Write requirements for a program: definitions, functional and
   non-functional requirements, each with its acceptance test.
2. Choose the relationship between two classes from the requirements, and
   the C++ that implements it.
3. Draw a UML class diagram of your design.
4. Write a class hierarchy with an abstract base class whose derived
   classes override its ``virtual`` methods, and call them through a
   pointer to the base class.
5. Implement aggregation with ``std::shared_ptr`` and composition with
   ``std::unique_ptr`` or a member held by value.


Themes
------

Choose **one** theme. Each one describes a world: what is in it, what
happens in it, and which values make no sense. The examples are there to
start you off. Which classes exist, and their names, are your decisions:
you may leave out an example or add your own.

.. dropdown:: Theme A: Drone Fleet
   :open:

   The search-and-rescue team from RWA1 and RWA2 now runs a fleet of
   drones of more than one kind. A **quadrotor** hovers, so it scans a
   small area closely, in a spiral, but its battery lasts only a short
   flight. A **fixed-wing** drone cannot hover; it covers long distances
   in straight passes across a sector. A **tethered** drone stays on a
   cable above the base and relays radio messages. Every drone flies its
   search pattern and reports what it saw, and each kind does both in its
   own way.

   Each drone is built with its own parts: a battery, with a capacity and
   a charge level, a set of motors, and sensors such as a thermal camera
   or a lidar. These parts belong to one drone only, and they are scrapped
   with it.

   The team plans **missions**: a mission searches one sector, and the
   team assigns drones to it. A drone flies one mission at a time. When a
   mission ends, its drones are not scrapped: they return to the base and
   join the next mission.

   Values that make no sense: a charge level outside 0 to 100 %, a speed
   or a flight distance below 0, a drone without a name or an id, a
   mission with no sector.

   Your program could: build a small fleet, assign drones to a mission,
   fly every drone of the mission once, move the drones of a finished
   mission to a new one, and print each drone's report.

.. dropdown:: Theme B: Video Game Monsters
   :open:

   A dungeon video game is about a **hero** who fights monsters. In a fight,
   the hero and the monsters take turns. Each one can **attack** another,
   **block** an attack, **take damage**, and **die** when its health reaches
   0. The hero has a name, a health level with a maximum, an attack power
   and a defense.

   Monsters come in different kinds, and each kind takes damage in its own
   way. A **vampire** dodges an attack 30 % of the time: the attack misses,
   and the vampire loses no health. A **werewolf** resists attacks: an
   attack removes less health from it than from other monsters, for
   example half. A **troll** regenerates: at the start of each of its
   turns, it gets back some of the health it lost, never more than its
   maximum.

   The hero and each monster have parts of their own: the hero's weapon
   and shield, and each monster's statistics (health, attack, defense) and
   the loot it drops when it dies. These belong to one character only, and
   they disappear with it.

   The dungeon has **rooms**, and each room holds the monsters in it. A
   monster can wander from one room to another. When the hero clears a
   room or leaves it, the monsters that are still alive are not destroyed:
   they stay in the dungeon and can be met again in another room.

   Values that make no sense: health below 0 or above its maximum, an
   attack power or a defense below 0, a dodge chance outside 0 to 100 %, a
   hero, a monster or a room without a name.

   Your program could: put the hero in a room with one monster of each
   kind, run the fight turn by turn until the hero or every monster is
   dead, print what each attack does (a hit, a dodge, a blocked or a
   resisted attack), and move a monster that is still alive to another
   room.

   A hint for the vampire: a 30 % chance needs random numbers. Use
   ``<random>`` with a fixed seed, for example ``std::mt19937
   generator{42};``, so every run gives the same fight. A fight you can
   repeat is a fight you can test.

.. dropdown:: Theme C: Planetary Rover Mission
   :open:

   A space agency explores a planet with vehicles of different kinds. A
   **lander** stays where it set down; it measures the weather and
   deploys instruments around it. A **rover** drives a few hundred meters
   a day, and it drills and collects rock samples. An **orbiter** circles
   the planet, takes pictures of the surface, and relays data to Earth.
   Every vehicle carries out its plan for the day (a *sol*, a day on the
   planet), and each kind does it in its own way.

   Each vehicle is built with its instruments, such as a rover's arm,
   drill and cameras, and with its power source, solar panels or a
   radioisotope generator. These belong to that vehicle only, and they are
   lost with it.

   The agency runs **missions**: a mission has a name, a landing site and
   the vehicles assigned to it. When a mission ends, the vehicles that
   still work are not lost: the agency assigns them to the next mission,
   for example an extended mission at the same site.

   Values that make no sense: a power level outside 0 to 100 %, a drive
   distance or a sample mass below 0, a vehicle without a name, a mission
   without a site.

   Your program could: set up a mission with one vehicle of each kind,
   run one sol for every vehicle, collect a sample, end the mission and
   move the working vehicles to an extended one, and print a status
   report.


Requirements
------------

.. dropdown:: R1: The Requirements (Report, Part 1)

   Write the requirements of your program, in the format of the
   :doc:`L9 Requirements </lectures/lecture9/l9_requirements>` page.

   1. **Definitions**: a table of the terms of your world, one sentence
      each. Every class of your design is named here.
   2. **Functional requirements**: at least 8, numbered ``FR-1``,
      ``FR-2``, and so on. Each one says what the system *shall* do, in
      one or two sentences, with a **Rationale** and an **Acceptance**
      line: the check that shows the code meets it.
   3. **Non-functional requirements**: at least 2, numbered ``NFR-1``,
      ``NFR-2``. One of them lists the values your objects reject, as
      NFR-2 does on the L9 page: a broken rule throws
      ``std::invalid_argument``.
   4. The requirements say **what** the program does, never **how**: no
      class names that the definitions do not have, no C++.

.. dropdown:: R2: The Design (Report, Part 2)

   Turn the requirements into classes, in the format of the
   :doc:`L9 Design </lectures/lecture9/l9_design>` page.

   1. **Class diagram**: one UML class diagram of the whole design, written
      in PlantUML. The ``.plantuml`` source goes in ``uml/``, and the
      diagram goes in the report. Each box lists its data members and its
      methods, with ``-``, ``+`` or ``#``. Each line shows its kind of
      relationship and, for an association, an aggregation or a
      composition, its multiplicity at each end.
   2. **Relationship table**: one row per line of the diagram, with the
      two classes, the relationship, the requirement it comes from, and
      the C++ that implements it (for example ``std::shared_ptr<Drone>``
      in a ``std::vector``).
   3. **Why each relationship**: for each line, walk the decision chart of
      Lecture 9 (`Choosing a Relationship and Its C++
      <../lectures/lecture9/l9_lecture.html#choosing-a-relationship-and-its-c>`__) and give each
      answer with the requirement or definition behind it, as Lecture 9
      does for ``Passenger`` and ``Vehicle``.

.. dropdown:: R3: Inheritance, Polymorphism and Abstraction

   1. One base class with **at least two** derived classes, each derived
      with ``public``.
   2. At least one ``virtual`` method in the base class that **each**
      derived class overrides, marked ``override``.
   3. The base class has a ``virtual`` destructor.
   4. The base class keeps its data members ``private``. A derived class
      sets them through the base class constructor, in its member
      initializer list, and reads them through the base class's methods.
   5. Each derived class adds at least one data member or method that the
      base class does not have.
   6. The base class is **abstract**: at least one of its methods is pure
      ``virtual`` (``= 0``), so no object of the base class can be made.
   7. Optional: mark ``final`` what nothing should derive from.

.. dropdown:: R4: Aggregation and Composition

   1. At least one **aggregation**: a whole holds parts that it shares
      with the rest of the program, as ``std::shared_ptr``. A part
      outlives its whole.
   2. At least one **composition**: a whole owns parts that are made and
      destroyed with it, as ``std::unique_ptr`` or as members held by
      value.
   3. No raw ``new`` and no ``delete``: ``std::make_shared`` and
      ``std::make_unique`` make every object on the heap.
   4. Optional: an association (``std::weak_ptr`` or a plain pointer that
      does not own) or a dependency (a parameter, no member).

.. dropdown:: R5: Project, Build and main

   1. The layout of `Deliverables`_. One class per header and source file
      (``robot_arm.hpp`` and ``robot_arm.cpp``), and every class in one
      namespace of your choice.
   2. Constructors are defined in the class. Every other method is
      declared in the header and defined in the ``.cpp`` file.
   3. ``CMakeLists.txt`` builds an executable named ``rwa3`` with
      ``CMAKE_CXX_STANDARD`` 20 and ``-Wall -Wextra``. The build prints no
      warning.
   4. Every file starts with a Doxygen ``@file`` comment with ``@author``
      and ``@brief``. Every class and every method in a header has a
      Doxygen comment, and ``docs/Doxyfile`` uses relative paths.
   5. ``src/main.cpp`` is the starter's (`The Starter Project`_), with each
      ``TODO`` replaced by the code it describes. The program runs to the end, and
      Valgrind reports no leak and no error: paste the last lines of its
      output into ``README.md``.


The Starter Project
-------------------

The starter is in the course repository, in
`project/rwa3_starter <https://github.com/zeidk/enpm702-fall-2026-cpp/tree/main/project/rwa3_starter>`__.
It has the layout of `Deliverables`_, a ``CMakeLists.txt`` that builds
``rwa3``, the ``main.cpp`` of R5, a ``Doxyfile``, a PlantUML file and a
``README.md`` to fill in.

1. Get it: go to the course repository and pull.

   .. code-block:: bash

      enpm702        # go to the repository, load the 702 commands
      git pull

2. Copy the starter out of the repository, under the name of your
   submission. Work in this copy, never in the course repository: the next
   ``git pull`` would collide with your changes.

   .. code-block:: bash

      cp -r project/rwa3_starter ~/rwa3_firstname_lastname

3. Build and run it. It compiles as given and prints the four section
   headers of ``main.cpp``.

   .. code-block:: bash

      cd ~/rwa3_firstname_lastname
      cmake -S . -B build
      cmake --build build
      ./build/rwa3

4. Open the folder in VS Code: ``code .``
5. For each class, add its header to ``include/`` and its source file to
   ``src/``, and add the source file to ``add_executable`` in
   ``CMakeLists.txt``. Build again after each class (see `Tips`_).
6. Fill in each section of ``src/main.cpp``: replace each ``TODO`` with the
   code it describes.
7. Before you submit:

   .. code-block:: bash

      cmake --build build                             # no warning
      valgrind --leak-check=full ./build/rwa3         # no leak, no error
      cd docs && doxygen Doxyfile                     # pages in docs/html

   Paste the last lines of Valgrind's output into ``README.md``, delete
   ``include/README.md``, and zip the folder without ``build/`` and
   ``docs/html/`` (`Deliverables`_).


How Your Documentation Is Graded
--------------------------------

Documentation is worth **10 %** on its own (see the rubric). R5 asks for
the comments to be **there**; this grade is for whether they **help**: a
reader who sees only your headers and the Doxygen pages should be able to
use every class correctly without opening a ``.cpp`` file.

1. **Every class** has a ``@brief`` that says what it is in your world,
   in the words of your Definitions (R1).
2. **Every method**: its ``@brief`` says what it does, in terms of the
   world ("Flies the search pattern over the sector"), not of the code
   ("Loops over ``waypoints_``").
3. **Every** ``@param`` says what the value means, its unit when it has
   one, and any limit on it. **Every** ``@return`` says what the result
   means, and **every** ``@throw`` says which value is rejected.
4. **Every data member** has a ``///`` comment: what it holds, its unit,
   its limits, and, for a smart pointer, whether the class owns the object
   alone, shares it, or only refers to it.
5. **Other comments** explain *why*, not *what*. No commented-out code,
   and no comment that no longer matches the code under it.

A comment that only repeats the names gets no credit:

.. code-block:: cpp

   /**
    * @brief add_mileage function.
    * @param meters meters
    */
   void add_mileage(double meters);

This one, from the ride service program of Lecture 9, tells a caller what
they need to know:

.. code-block:: cpp

   /**
    * @brief Adds the distance of a trip to the mileage.
    * @param meters The trip's distance, in m. At least 0: the mileage never goes down.
    * @throw std::invalid_argument if @p meters is less than 0.
    */
   void add_mileage(double meters);


Deliverables
------------

Submit **one zip file** on Canvas, named after the folder it contains:
``rwa3_firstname_lastname.zip``, for example
``rwa3_bjarne_stroustrup.zip``.

.. code-block:: text

   rwa3_firstname_lastname/
   ├── CMakeLists.txt
   ├── README.md
   ├── report.pdf           # R1 and R2
   ├── docs/
   │   └── Doxyfile
   ├── uml/
   │   └── design.plantuml  # the class diagram of R2
   ├── include/             # one header per class
   └── src/                 # one source file per class, and main.cpp

.. list-table::
   :header-rows: 1
   :widths: 25 75
   :class: compact-table

   * - File
     - Description
   * - ``report.pdf``
     - Part 1, the requirements (R1). Part 2, the design (R2): the class
       diagram, the relationship table, and the decision chart answers.
   * - ``uml/design.plantuml``
     - The PlantUML source of the class diagram in the report.
   * - ``include/``, ``src/``
     - One header and one source file per class, and ``src/main.cpp``.
   * - ``CMakeLists.txt``, ``docs/Doxyfile``
     - The build (R5) and the Doxygen configuration.
   * - ``README.md``
     - Your theme, how to build and run, the last lines of your Valgrind
       output, and your AI disclosure if you used a tool.

.. warning::

   Do **not** include the ``build/`` directory, the pages Doxygen
   generates (``docs/html``, ``docs/latex``), editor folders such as
   ``.vscode/``, or the compiled executable. A submission that does not
   build cannot be graded.


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 32 12 56
   :class: compact-table

   * - Category
     - Weight
     - Criteria
   * - R1: Requirements
     - 15 %
     - The definitions, at least 8 functional and 2 non-functional
       requirements, each testable through its acceptance line, and none
       that names code.
   * - R2: Design
     - 20 %
     - A class diagram that matches the code, a relationship table that
       links each line to a requirement, and decision chart answers that
       the requirements support.
   * - R3: Inheritance, polymorphism and abstraction
     - 25 %
     - The hierarchy, the abstract base class, the overridden
       ``virtual`` method called through the base class in section 1 of
       ``main``, the ``virtual`` destructor, and ``private`` base data.
   * - R4: Aggregation and composition
     - 20 %
     - The ``std::shared_ptr`` whole whose part outlives it (section 2),
       the owned parts destroyed with their whole (section 3), and no raw
       ``new`` or ``delete``.
   * - R5: Project, build and main
     - 10 %
     - The layout, one class per file, a build with no warnings, every
       section of ``main`` filled in, the rejected value of section 4, and
       a clean Valgrind run.
   * - Documentation
     - 10 %
     - Doxygen comments on every file, class and method, and comments
       that explain why.

Code that ignores the course conventions loses marks in the requirement
where it appears: uniform initialization, ``snake_case``, names that say
what the value is, and ``'\n'`` rather than ``std::endl``.


Tips
----

.. admonition:: Requirements first, then the diagram, then the code
   :class: tip

   Write the acceptance line of each requirement first: if you cannot say
   how to check a requirement, it is not a requirement yet. Then draw the
   diagram. A line you cannot justify with the decision chart is a line to
   remove. Six to ten classes are enough to show every relationship.

.. admonition:: Test each class on its own before you test them together
   :class: tip

   Write the classes that hold no other class first (a battery, a set of
   statistics, an instrument), then the base class and its derived
   classes, then the classes that hold the others. After each class, test
   it alone before you use it anywhere else:

   * Write, yourself, a short program that makes one object, calls each of its
     methods, and prints what each one returns. Check every printed value
     against what you expected.
   * Try each value your requirements forbid, and check that the class
     throws ``std::invalid_argument``.
   * Run it under Valgrind (or build it with ``-fsanitize=address``), so a
     leak or a wrong ``delete`` shows up while the class is still small.

   A test program is one more ``add_executable`` line in
   ``CMakeLists.txt``, for example ``test_battery`` built from
   ``tests/test_battery.cpp`` and the class's own ``.cpp`` file. You may
   keep these programs in a ``tests/`` folder; they are not graded. When
   every class passes on its own, a failure in ``main`` comes from how the
   classes work together, not from inside one of them.

.. admonition:: Build after every class
   :class: tip

   Get the project building with an empty ``main`` and one class, then
   add the next class. A link error such as ``undefined reference`` means
   a method is declared but not defined, or its ``.cpp`` file is missing
   from ``CMakeLists.txt``.

.. admonition:: Follow the conventions
   :class: tip

   * Uniform initialization: ``int count{0};``, not ``int count = 0;``
   * ``snake_case``: ``battery_level``, not ``batteryLevel``
   * ``'\n'``, never ``std::endl``

.. admonition:: Use Lecture 9 as your model
   :class: tip

   Read the ride service program again: its
   :doc:`requirements </lectures/lecture9/l9_requirements>`, its
   :doc:`design </lectures/lecture9/l9_design>`, and its code in
   ``project/week9``. Your report follows the same steps for your own
   world.


Troubleshooting
---------------

Problems you may meet while you write the classes, what each one looks like,
and how to fix it. The messages are g++ 13.3's, with the course's flags; the
examples use a ``Robot`` base class and a ``Rover`` derived class. Read the
**first** error a build prints: the ones after it often come from it.

.. dropdown:: Two headers that include each other

   **What you see:** a class that is plainly declared is unknown, for example

   .. code-block:: text

      b.hpp:7:3: error: 'A' does not name a type

   **Why:** ``a.hpp`` includes ``b.hpp``, and ``b.hpp`` includes ``a.hpp``.
   ``#pragma once`` skips the second copy, so one class is compiled before
   the other is declared. This happens with a two-way association, for
   example a ``Hero`` that keeps its ``Monster`` target while the
   ``Monster`` keeps its ``Hero``.

   **Fix:** in a header that only names the other class (a pointer or a
   reference to it), write a forward declaration, ``class A;``, instead of
   the ``#include``, and include the other header in the ``.cpp`` file. See
   "Two Headers That Include Each Other" in the Further Reading of the
   :doc:`Lecture 9 page </lectures/lecture9/l9_lecture>`.

.. dropdown:: Two objects that own each other (a std::shared_ptr cycle)

   **What you see:** the program builds and runs, then a leak report at
   the end of a run with ``-fsanitize=address``, although no ``new`` is
   written anywhere:

   .. code-block:: text

      ERROR: LeakSanitizer: detected memory leaks
      Indirect leak of 80 byte(s) in 1 object(s) allocated from:

   **Why:** two objects hold a ``std::shared_ptr`` to each other. Each
   keeps the other's count at 1, so neither count reaches 0 and neither
   object is deleted.

   **Fix:** decide which side owns. The other side watches with a
   ``std::weak_ptr`` and calls ``lock()`` when it needs the object. In a
   class diagram, a line that does not keep the other object alive is an
   association, not an aggregation. See "Cyclic Reference" and "Breaking
   It" in :doc:`Lecture 7 </lectures/lecture7/l7_lecture>`.

.. dropdown:: The base class's method runs instead of the derived one

   **What you see:** a call through a base reference or pointer prints
   the base class's line, and ``-Wall`` warns:

   .. code-block:: text

      warning: 'virtual void Robot::move() const' was hidden [-Woverloaded-virtual=]
      note:   by 'void Rover::move()'

   **Why:** either the base method is not ``virtual``, or the derived
   method differs from it (here the ``const`` is missing), so it is a new
   method instead of an override.

   **Fix:** make the base method ``virtual``, and write ``override`` on
   every derived method that should override. ``override`` turns this
   mistake into an error:

   .. code-block:: text

      error: 'void Rover::move()' marked 'override', but does not override

.. dropdown:: undefined reference to `vtable for ...`

   **What you see:** the compiler accepts every file, and the link fails:

   .. code-block:: text

      undefined reference to `vtable for Robot'

   **Why:** a ``virtual`` method of that class is declared but never
   defined, or its ``.cpp`` file is not in ``CMakeLists.txt``. g++ writes
   the class's table of ``virtual`` methods next to that missing
   definition, so the table is missing too.

   **Fix:** define every ``virtual`` method that is not pure
   (``= 0``), and list every ``.cpp`` file in ``add_executable``.

.. dropdown:: Cannot make an object of the base class

   **What you see:**

   .. code-block:: text

      error: cannot declare variable 'r' to be of abstract type 'Robot'

   **Why:** ``Robot`` has a pure ``virtual`` method, so it is abstract: no
   object of it can be made. A derived class that does not override every
   pure ``virtual`` method is abstract too.

   **Fix:** make objects of the derived classes, and hold them through a
   ``Robot&``, a ``Robot*`` or a smart pointer to ``Robot``. If the error
   names a derived class, look for a pure ``virtual`` method it does not
   override.

.. dropdown:: no matching function for call to the base constructor

   **What you see:**

   .. code-block:: text

      error: no matching function for call to 'Robot::Robot()'

   **Why:** the derived constructor does not say which base constructor to
   use, and the base class has no default constructor.

   **Fix:** call the base constructor first in the member initializer
   list: ``Rover() : Robot{1.0} {}``.

.. dropdown:: A base member is private within this context

   **What you see:**

   .. code-block:: text

      error: 'double Robot::max_speed_' is private within this context

   **Why:** a derived class cannot use the ``private`` members of its base
   class.

   **Fix:** use the base class's ``public`` methods, or give it a
   ``protected`` method for what only derived classes may do. Keep data
   members ``private`` (Core Guidelines C.133).

.. dropdown:: A std::unique_ptr that does not copy

   **What you see:** a long message whose first line is

   .. code-block:: text

      error: no matching function for call to 'std::unique_ptr<Robot>::unique_ptr(<brace-enclosed initializer list>)'

   **Why:** a ``std::unique_ptr`` is the only owner of its object, so it
   cannot be copied, for example into a ``std::vector`` or into a second
   ``std::unique_ptr``.

   **Fix:** hand the object over with ``std::move``, or pass it by
   reference when the other code only uses it.

.. dropdown:: A delete through a base pointer is reported

   **What you see:** with ``-fsanitize=address``, a run stops with

   .. code-block:: text

      ERROR: AddressSanitizer: new-delete-type-mismatch

   **Why:** a ``std::unique_ptr<Robot>`` (or a ``delete``) destroys a
   ``Rover`` through a ``Robot*``, and ``Robot``'s destructor is not
   ``virtual``. Only the ``Robot`` part is destroyed: undefined behavior.

   **Fix:** give the base class ``virtual ~Robot() = default;`` (Core
   Guidelines C.35). See :doc:`virtual Methods in Depth </lectures/lecture9/l9_virtual>`.

.. dropdown:: Derived objects in a vector act like base objects

   **What you see:** no error. The objects of a ``std::vector<Robot>``
   all run ``Robot``'s methods, and their own data members are gone.

   **Why:** ``push_back`` copies only the ``Robot`` part of a ``Rover``:
   slicing.

   **Fix:** store pointers: ``std::vector<std::unique_ptr<Robot>>`` when
   the vector owns the objects, ``std::vector<std::shared_ptr<Robot>>``
   when they are shared. See "Slicing" in the
   :doc:`Lecture 9 page </lectures/lecture9/l9_lecture>`.


References
----------

The **C++ Core Guidelines** are the rules this course grades against.
These are the ones that apply to RWA3. Read the short entry behind each
link before you write the matching requirement.

.. list-table::
   :header-rows: 1
   :widths: 16 84
   :class: compact-table

   * - Rule
     - Says
   * - `C.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-struct>`_
     - Use ``class`` if the class has an invariant; use ``struct`` if the
       data members can vary independently.
   * - `C.9 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-private>`_
     - Minimize exposure of members.
   * - `C.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual>`_
     - A base class destructor should be either public and virtual, or
       protected and non-virtual.
   * - `C.120 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-domain>`_
     - Use class hierarchies to represent concepts with inherent
       hierarchical structure (only).
   * - `C.128 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-override>`_
     - Virtual functions should specify exactly one of ``virtual``,
       ``override``, or ``final``.
   * - `C.133 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-protected>`_
     - Avoid ``protected`` data.
   * - `R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`_
     - Avoid calling ``new`` and ``delete`` explicitly.
   * - `R.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-owner>`_
     - Use ``unique_ptr`` or ``shared_ptr`` to represent ownership.
   * - `R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`_
     - Prefer ``unique_ptr`` over ``shared_ptr`` unless you need to share
       ownership.
   * - `R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`_
     - Use ``make_shared()`` to make ``shared_ptr``\ s.
   * - `R.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_unique>`_
     - Use ``make_unique()`` to make ``unique_ptr``\ s.
   * - `SF.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-consistency>`_
     - A ``.cpp`` file must include the header file(s) that defines its
       interface.
   * - `ES.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-always>`_
     - Always initialize an object.
   * - `NL.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel>`_
     - Prefer ``underscore_style`` names.
