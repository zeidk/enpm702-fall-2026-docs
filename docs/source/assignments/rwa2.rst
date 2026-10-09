====================================================
RWA2: Sector Sweep Mission Planner
====================================================

.. figure:: /_static/images/rwa2/rwa2.jpeg
   :align: center
   :alt: A pencil sketch of a quadrotor drone flying over a mountain valley divided into eight numbered sectors. Each sector is labeled with its probability and its place in the visiting order: sector 4 first, then 7, 6, 8, 5 and 2, with sector 1 eighth. A dashed flight path runs between the sectors. In sector 3, labeled 8 percent, a person is marked with the note "Victim ID 5017 found?". Two "battery limit" markers show where the drone runs short of power. A box in the top left reads "Mission plan: search sectors", shows a battery gauge, and lists the order by probability.

   The drone sweeping the search area in the order of the "probability"
   strategy. The numbers in the sketch are illustrative: your program
   uses the data in `The Mission Model`_.

Overview
--------

The search-and-rescue drone from RWA1 now has a search area. The area is
split into eight **sectors**, and each sector has a probability that the
victim is there. Your program decides the order in which the drone visits
the sectors, flies them while the battery allows, and reports what it
found.

The order comes from a **search strategy**. You write two: "highest
probability first" and "nearest first". The program runs both on the same
data, so you can compare them. With the data in this assignment they give
different answers: one finds the victim, and the other runs out of battery
reserve before it gets there.

Everything in this assignment comes from Lectures 1 to 6. The new material
is functions: header and source files, parameter passing, default
arguments, overloading, static locals and ``main``'s arguments (Lecture 5),
then ``struct``, ``std::optional``, structured bindings, templates with
concepts, lambdas and ``std::function`` (Lecture 6). Containers from
Lecture 4 hold the data. There are no classes, no smart pointers, no
``new`` or ``delete`` and no exceptions. Those arrive in later lectures.

.. important::

   **Posted Fri, Oct 9, due Fri, Oct 23.** Everything it asks for is
   covered by Lecture 6, so you can start the day it is posted. The
   requirements are in the order you should write them, and each one
   builds on the one before.


.. admonition:: Using AI on this assignment
   :class: important

   The course AI policy from
   :doc:`Lecture 1 </lectures/lecture1/l1_lecture>` applies here in full.
   In short:

   * You **may** use a tool such as TerpAI, ChatGPT, Claude, Gemini or
     Copilot to explain a concept, read a compiler error, suggest a way
     to debug something, or review code **you have already written**.
   * You **must** say so at the top of your ``README.md``: name the tool
     and describe in two or three sentences what you used it for.
     Disclosure carries no penalty. Undisclosed use is a violation of
     the Code of Academic Integrity.
   * You **may not** submit generated code that you cannot read,
     explain, and change. You are responsible for every line you hand
     in, and you may be asked to walk through any part of it and say why
     it works and what would break it.

   A warning specific to RWA2. Most of the marks are for choices: how
   each parameter is passed, which form of a concept to use, when a
   callable is ``auto`` and when it is ``std::function``. A tool will
   make those choices for you, often differently from the lectures, and
   you will not be able to defend them in the walkthrough.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Split a program into header and source files, build it with CMake,
   and document it with Doxygen.
2. Choose how to pass each parameter (by value, by ``const`` reference,
   by reference, as a ``std::span``) and return results by value.
3. Use default arguments and overloading where each one fits.
4. Group related values in a ``struct``, return several values as a
   ``struct``, and unpack them with structured bindings.
5. Use ``std::optional`` for a value that may be missing, instead of a
   null pointer or a special value.
6. Write a function template constrained by a concept.
7. Pass operations as lambdas, and store them in ``std::function`` when
   they must be kept.
8. Read and check command-line arguments.


The Mission Model
-----------------

Read this section before you start. Every number your program prints
follows from these rules and the data below, so your numbers must match
the expected output exactly.

**Positions.** The drone's base is at (0, 0). A position is an ``x`` and
a ``y`` in meters from the base. The distance between two positions is
the straight-line distance, ``std::hypot(x2 - x1, y2 - y1)``.

**Battery use.** These two values are chosen for this assignment:

* Flying costs **0.1 %** of battery per meter.
* Scanning a sector costs **4.0 %**.

So a **leg** to a sector, which is the flight to it plus its scan, costs
``distance × 0.1 + 4.0`` percent. The flight home from a sector costs
``distance to base × 0.1`` percent, with no scan.

**The reserve rule.** Before each leg, the drone checks that it could fly
the leg **and then fly home** and still have at least
``min_battery_pct`` (20.0 %, from RWA1) left. If it could not, it skips
that sector and checks the next one. It does not stop at the first sector
it cannot reach.

**The search.**

1. The drone takes off from the base.
2. It visits the sectors in the order the strategy gives, applying the
   reserve rule to each one.
3. It stops searching when it scans the sector that holds the victim, or
   when no sector is left.
4. It returns to base from wherever it is, then lands.

A worked example, with the drone at the base and 100.0 % battery,
deciding whether to visit sector 4 at (150, 80):

1. Leg distance: ``hypot(150, 80)`` = 170.0 m.
2. Leg energy: 170.0 × 0.1 + 4.0 = 21.0 %.
3. Energy home from sector 4: 170.0 × 0.1 = 17.0 %.
4. Battery left after the leg and the flight home: 100.0 less 21.0 less
   17.0 = 62.0 %. That is at least 20.0 %, so the leg is feasible.

**Probability.** A sector's probability is the search team's estimate
before the flight. It is used only to order the sectors; the victim is
wherever ``victim_id`` says, and scanning that sector always finds it.
Nothing in the program is random.

**The data.** ``make_sectors`` (R3) returns these sectors. Copy the
list into it as it is. The victim, id 5017, is in sector 3.

.. code-block:: cpp

   return {
       {.id = 1, .center = {.x_m = 40.0, .y_m = 30.0}, .probability = 0.05},
       {.id = 2, .center = {.x_m = 90.0, .y_m = -20.0}, .probability = 0.10},
       {.id = 3, .center = {.x_m = -60.0, .y_m = 50.0}, .probability = 0.08, .victim_id = 5017},
       {.id = 4, .center = {.x_m = 150.0, .y_m = 80.0}, .probability = 0.30},
       {.id = 5, .center = {.x_m = -120.0, .y_m = -90.0}, .probability = 0.12},
       {.id = 6, .center = {.x_m = 200.0, .y_m = -60.0}, .probability = 0.20},
       {.id = 7, .center = {.x_m = 60.0, .y_m = 140.0}, .probability = 0.25},
       {.id = 8, .center = {.x_m = -30.0, .y_m = -150.0}, .probability = 0.15},
   };

No two sectors have the same probability or the same distance from the
base, so each strategy gives exactly one order.


Requirements
------------

.. dropdown:: R1: Project Layout, CMake and Doxygen

   Split the program into two headers and three source files:

   .. code-block:: text

      rwa2_firstname_lastname/
      ├── CMakeLists.txt
      ├── README.md
      ├── docs/
      │   └── Doxyfile
      ├── include/
      │   ├── drone.hpp        # R2 and R4: the drone, its limits, is_within
      │   └── mission.hpp      # R3 and R5: sectors, legs, the planner
      └── src/
          ├── drone.cpp        # definitions of the drone.hpp functions
          ├── mission.cpp      # definitions of the mission.hpp functions
          └── main.cpp         # main() only

   1. Protect each header with ``#pragma once``.
   2. A header holds declarations, constants and ``struct`` definitions.
      Function **bodies** go in the ``.cpp`` files, with one exception:
      a template's body goes in the header (Lecture 6, "Templates Go in
      Headers"). This assignment has two templates, ``is_within`` (R4)
      and ``run_mission`` (R5).
   3. Each ``.cpp`` file includes its own header first among the project
      headers.
   4. ``CMakeLists.txt`` builds an executable named ``rwa2`` from the
      three source files, sets ``CMAKE_CXX_STANDARD`` to 20, adds
      ``include`` as the include directory, and compiles with ``-Wall
      -Wextra``.
   5. Every file starts with a Doxygen ``@file`` comment with ``@author``
      and ``@brief``. Every function declared in a header has ``@brief``,
      one ``@param`` per parameter and, unless it returns ``void``,
      ``@return``. ``is_within`` also gets ``@tparam`` for ``T``.
   6. Put a ``Doxyfile`` in ``docs`` with relative paths
      (``INPUT = ../include ../src``), so that running ``doxygen
      Doxyfile`` in ``docs`` works on another machine.
   7. Keep ``main`` minimal. It creates values and calls functions, and
      nothing else: no loops, no lambdas, and no printing of its own.
      Each requirement below names the function that does its work.
      ``main`` is about a dozen lines of code, laid out as shown in
      `Deliverables`_.
   8. Generate the pages and check them before you submit:

      .. code-block:: bash

         cd docs
         doxygen Doxyfile

      Open ``docs/html/index.html`` in a browser. Under **Files**, open
      ``drone.hpp`` and ``mission.hpp`` and check that every function
      appears with its description, each of its parameters and, where
      there is one, its return value. A missing entry or an empty
      description means a comment is missing or misplaced: fix the
      comment and run Doxygen again.

      Then **delete** ``docs/html`` (and ``docs/latex``, if Doxygen made
      it). The pages are not part of your submission. They are
      regenerated from your comments when your work is graded.

   Acceptance criteria:

   * The project configures and builds from a fresh ``build`` folder
     with **no warnings** under ``-Wall -Wextra``.
   * No function body outside the two templates appears in a header.
   * ``main`` has no loops, no lambdas and no output statements. Every
     line in it creates a value or calls a function.
   * Running Doxygen in ``docs`` lists every function in both headers,
     with its parameters and return value described.
   * The zip contains ``docs/Doxyfile`` and no generated pages.

.. dropdown:: R2: The Drone, from RWA1 to Functions

   RWA1 kept the drone's state in loose variables and its victim record
   on the heap. Here the state becomes one ``struct``, the victim becomes
   a ``std::optional``, and the report becomes functions.

   In ``drone.hpp``, declare:

   1. The two RWA1 limits as compile-time constants with their RWA1
      values: ``max_altitude_m`` (``int``, 120) and ``min_battery_pct``
      (``double``, 20.0). Add two more, chosen for this assignment:
      ``cruise_altitude_m`` (``int``, 95) and ``cruise_rotor_rpm``
      (``double``, 5400.0).
   2. RWA1's scoped enumeration ``MissionPhase``, with ``idle``,
      ``searching`` and ``returning``.
   3. Three structs, each member with a default member initializer:

      .. list-table::
         :header-rows: 1
         :widths: 20 80
         :class: compact-table

         * - Struct
           - Members (default)
         * - ``Point``
           - ``double x_m`` (0.0), ``double y_m`` (0.0)
         * - ``Victim``
           - ``int id`` (0), ``int sector_id`` (0)
         * - ``DroneStatus``
           - ``int altitude_m`` (0), ``double battery_pct`` (100.0),
             ``double rotor_rpm`` (0.0), ``bool airborne`` (false),
             ``MissionPhase phase`` (``idle``), ``Point position``
             (the base), ``std::optional<Victim> victim`` (empty)

   4. These four functions, exactly as declared here:

      .. code-block:: cpp

         std::string_view to_string(MissionPhase phase);
         [[nodiscard]] bool battery_ok(double battery_pct, double min_pct = min_battery_pct);
         void print_report(const DroneStatus& status, int precision = 1);
         void print_preflight(const DroneStatus& drone);

      * ``to_string`` returns the phase's name. Use a ``switch`` with
        ``using enum``, as in RWA1.
      * ``battery_ok`` returns ``true`` when ``battery_pct`` is at least
        ``min_pct``. Ignoring its result is always a bug, which is what
        ``[[nodiscard]]`` is for.
      * ``print_report`` prints the block shown below, with
        ``precision`` digits after the decimal point. It prints the
        warning line when ``battery_ok`` is ``false``, and the victim
        line from the ``std::optional``.
      * ``print_preflight`` prints the ``DRONE`` header, calls
        ``print_report``, and prints the cruise altitude check from R4.

   5. In ``main``, create the drone with a designated initializer that
      sets only the battery, leaving every other member at its default.
      Pass it to ``print_preflight``.

   .. admonition:: Why ``std::optional`` replaces the heap record
      :class: note

      In RWA1, ``nullptr`` meant "no victim found", and the record
      needed one ``new`` and one ``delete``. A ``std::optional<Victim>``
      says "a victim, or nothing" in its type, needs no heap memory, and
      is copied along with the ``DroneStatus`` that holds it. Read it
      with ``has_value()`` and ``->``. Do not call ``value()``: it throws
      an exception when the optional is empty, and exceptions are not
      covered yet.

   Acceptance criteria:

   * No loose telemetry variables remain: the drone is one
     ``DroneStatus``.
   * No ``new``, ``delete`` or raw pointer is used for the victim.
   * ``battery_ok`` and ``print_report`` take their defaults from the
     declaration, and the defaults appear only there.
   * The phase prints as text, the state as "airborne" or "grounded".

   Expected output of this part, with no command-line arguments:

   .. code-block:: text

      ===== DRONE =====
      phase    : idle
      altitude : 0 m
      battery  : 100.0 %
      rotors   : 0.0 rpm
      state    : grounded
      position : (0.0, 0.0) m
      victim   : none on record
      cruise altitude 95 m within limits: yes

   The last line comes from R4.

.. dropdown:: R3: Sectors, Legs and the Log

   In ``mission.hpp``, declare:

   1. The two battery constants from the mission model:
      ``battery_pct_per_m`` (0.1) and ``scan_cost_pct`` (4.0).
   2. Three structs, each member with a default member initializer:

      .. list-table::
         :header-rows: 1
         :widths: 20 80
         :class: compact-table

         * - Struct
           - Members (default)
         * - ``Sector``
           - ``int id`` (0), ``Point center`` (the base),
             ``double probability`` (0.0),
             ``std::optional<int> victim_id`` (empty)
         * - ``LegPlan``
           - ``double distance_m`` (0.0), ``double energy_pct`` (0.0),
             ``bool feasible`` (false)
         * - ``MissionResult``
           - ``std::vector<int> visited_ids`` (empty),
             ``double distance_m`` (0.0), ``DroneStatus drone``
             (default)

      ``victim_id`` is a ``std::optional<int>`` rather than an ``int``
      where 0 means "no victim", so no id has to be reserved as a special
      value.

   3. These functions, exactly as declared here:

      .. code-block:: cpp

         double distance(Point from, Point to = Point{});
         std::optional<Sector> find_sector(std::span<const Sector> sectors, int id);
         LegPlan plan_leg(Point from, Point to, double battery_pct);
         double return_to_base(DroneStatus& drone);
         void log_event(std::string_view message);
         void print(const Sector& sector);
         void print(const MissionResult& result);
         std::vector<Sector> make_sectors();
         void print_sectors(std::span<const Sector> sectors);

      * ``distance`` returns the straight-line distance. Its default
        argument makes ``distance(p)`` the distance from the base, so no
        second function is needed (Core Guidelines F.51).
      * ``find_sector`` returns the sector with that id, or an empty
        optional when there is none. ``std::span`` lets it take the
        vector without copying it, and would take any other contiguous
        sequence of sectors as well. At its definition, add a one-line
        comment on ``sectors`` saying why it is a span.
      * ``plan_leg`` applies the mission model: the leg's distance, its
        energy, and whether the reserve rule allows it. Use
        ``battery_ok`` for the reserve check.
      * ``return_to_base`` flies the drone home. It sets the
        ``returning`` phase, logs ``returning to base``, subtracts the
        energy of the flight home, and moves the drone to the base. It
        returns the distance flown, in meters. It takes the drone by
        non-``const`` reference because changing the caller's drone is
        its job (Core Guidelines F.17).
      * ``log_event`` prints one numbered line, ``[01] takeoff``, and
        numbers its lines across the **whole run** of the program, so the
        second strategy's log continues where the first one stopped. Keep
        the counter in a ``static`` local variable, not a global.
      * The two ``print`` overloads take different types, which a default
        argument cannot do. ``print(const Sector&)`` prints one sector
        line. ``print(const MissionResult&)`` prints the visited ids and
        the distance, then calls ``print_report`` on the drone.

      * ``make_sectors`` returns the eight sectors from
        `The Mission Model`_.
      * ``print_sectors`` prints the ``SECTORS`` header, then:

        * every sector, with ``print``;
        * the number of sectors whose probability is at least 0.15,
          counted with ``std::count_if`` and a lambda that **captures the
          threshold by value**;
        * the result of ``find_sector`` for sector 4 and for sector 42:
          the position of the one that exists, and "no such sector" for
          the other.

   4. In ``main``, after the drone, store the result of ``make_sectors``
      in a ``const std::vector<Sector>`` and pass it to
      ``print_sectors``.

   Acceptance criteria:

   * ``find_sector`` returns a ``std::optional`` and never a pointer or a
     made-up sector.
   * ``plan_leg`` returns one ``LegPlan``, not three output parameters.
   * ``return_to_base`` changes the drone through its reference parameter
     and returns only the distance.
   * ``log_event`` has no global state.
   * The ``count_if`` lambda captures its threshold; it does not hard-code
     0.15 in its body.

   Expected output of this part:

   .. code-block:: text

      ===== SECTORS =====
      sector 1 : (  40,   30) m  p 0.05
      sector 2 : (  90,  -20) m  p 0.10
      sector 3 : ( -60,   50) m  p 0.08
      sector 4 : ( 150,   80) m  p 0.30
      sector 5 : (-120,  -90) m  p 0.12
      sector 6 : ( 200,  -60) m  p 0.20
      sector 7 : (  60,  140) m  p 0.25
      sector 8 : ( -30, -150) m  p 0.15
      sectors with p >= 0.15 : 4
      find sector 4 : at (150.0, 80.0) m
      find sector 42 : no such sector

.. dropdown:: R4: One Template, Two Types

   ``max_altitude_m`` is an ``int`` and the battery is a ``double``. A
   range check on each needs one function template, not two copies of the
   same body.

   1. In ``drone.hpp``, write the template ``is_within(value, low,
      high)``, which returns ``true`` when ``low <= value <= high``. All
      three parameters have the same type ``T``.
   2. Constrain ``T`` to integer **or** floating-point types. The test
      joins two concepts, ``std::integral`` and ``std::floating_point``,
      with ``||``, so use the form Lecture 6 gives for joined tests: a
      ``requires`` clause.
   3. Use it twice:

      * In ``print_preflight`` (R2), on ``int`` values: check that
        ``cruise_altitude_m`` lies between 0 and ``max_altitude_m``, and
        print the result.
      * In R6, on ``double`` values: check the battery level read from
        the command line.

   Acceptance criteria:

   * One template, called with ``T`` deduced as ``int`` once and as
     ``double`` once.
   * The constraint is a ``requires`` clause that joins
     ``std::integral<T>`` and ``std::floating_point<T>`` with ``||``.
   * The template is documented with ``@tparam``.

.. dropdown:: R5: Search Strategies

   A strategy is an ordering of the sectors: a function that takes two
   sectors and returns ``true`` when the first should be visited before
   the second. That is the comparison ``std::sort`` takes.

   1. In ``mission.hpp``, write the planner with exactly this signature,
      and give it the body there, since it is a template (the ``auto``
      parameter makes it one):

      .. code-block:: cpp

         MissionResult run_mission(std::vector<Sector> sectors, DroneStatus drone, auto order);

      ``sectors`` is taken **by value** on purpose: the planner sorts the
      sectors, and sorting the caller's vector would change data the
      caller still uses. Sorting a copy leaves the original alone. At the
      definition, add a one-line comment on ``sectors`` saying so.

      ``order`` is ``auto`` because ``run_mission`` calls it before it
      returns and never keeps it. Lecture 6, "Choosing a Parameter Type",
      gives that rule.

   2. ``run_mission`` follows the search in the mission model:

      1. Sort ``sectors`` with ``std::sort`` and ``order``.
      2. Take off: set ``airborne``, ``cruise_altitude_m``,
         ``cruise_rotor_rpm`` and the ``searching`` phase. Log
         ``takeoff``.
      3. For each sector, call ``plan_leg`` and unpack its result with a
         **structured binding**. If the leg is not feasible, log
         ``sector N skipped: no reserve to get home`` and go on to the
         next sector. Otherwise subtract the leg's energy, move the drone
         to the sector, add the distance, record the id, and log
         ``scanned sector N``.
      4. If the scanned sector holds the victim, store a ``Victim`` in
         the drone's ``std::optional``, log ``victim N located``, and
         stop the search.
      5. Call ``return_to_base`` and add the distance it returns. Then
         land: grounded, altitude 0, rotors 0.0, phase ``idle``. Log
         ``landed``.
      6. Return the ``MissionResult``.

   3. Store the two strategies in a table, so that the program can look
      one up by name and run each in turn. In ``mission.hpp``, declare
      these, exactly as written here:

      .. code-block:: cpp

         using Order = std::function<bool(const Sector&, const Sector&)>;
         using StrategyTable = std::vector<std::pair<std::string_view, Order>>;

         StrategyTable make_strategies();
         void run_strategies(const StrategyTable& strategies, std::string_view chosen,
                             const std::vector<Sector>& sectors, const DroneStatus& drone);

      * ``make_strategies`` returns the table with two entries, each a
        lambda:

        * ``"probability"``: the sector with the **higher** probability
          comes first.
        * ``"nearest"``: the sector **closer to the base** comes first.

        The table needs ``std::function`` because it **stores** the
        lambdas, and every lambda has its own type: a container needs one
        element type that can hold either.
      * ``run_strategies`` loops over the table. For each strategy whose
        name is ``chosen``, or every strategy when ``chosen`` is
        ``"all"``, it prints the strategy's header, calls ``run_mission``
        with ``sectors`` and ``drone``, and prints the result.
        ``run_mission`` makes its own copy of the vector, so
        ``run_strategies`` only needs a ``const`` reference.

   4. In ``main``, create the table with ``make_strategies`` (first, since
      R6 needs it), and at the end call ``run_strategies``.

   Acceptance criteria:

   * ``run_mission`` takes the sectors by value, the drone by value and
     the order as ``auto``. It returns one ``MissionResult``.
   * The strategies are lambdas stored in a ``std::function`` table, and
     ``run_strategies`` runs them with one loop over the table.
   * ``plan_leg``'s result is unpacked with a structured binding.
   * The skipped sectors appear in the log, and the search goes on after
     a skip.

   Expected output of this part, with no command-line arguments:

   .. code-block:: text

      ===== STRATEGY: probability =====
      [01] takeoff
      [02] scanned sector 4
      [03] scanned sector 7
      [04] sector 6 skipped: no reserve to get home
      [05] sector 8 skipped: no reserve to get home
      [06] sector 5 skipped: no reserve to get home
      [07] scanned sector 2
      [08] sector 3 skipped: no reserve to get home
      [09] scanned sector 1
      [10] returning to base
      [11] landed
      visited  : 4 7 2 1
      distance : 561.7 m
      phase    : idle
      altitude : 0 m
      battery  : 27.8 %
      rotors   : 0.0 rpm
      state    : grounded
      position : (0.0, 0.0) m
      victim   : none on record

      ===== STRATEGY: nearest =====
      [12] takeoff
      [13] scanned sector 1
      [14] scanned sector 3
      [15] victim 5017 located
      [16] returning to base
      [17] landed
      visited  : 1 3
      distance : 230.1 m
      phase    : idle
      altitude : 0 m
      battery  : 69.0 %
      rotors   : 0.0 rpm
      state    : grounded
      position : (0.0, 0.0) m
      victim   : id 5017 in sector 3

   "Probability" flies to the likely sectors first. They are far from the
   base, so by the time it reaches sector 3 it no longer has the reserve
   for it, and it lands without finding the victim. "Nearest" reaches
   sector 3 on its second leg.

.. dropdown:: R6: Command-Line Arguments and a Clean Valgrind Run

   The program takes up to two arguments:

   .. code-block:: text

      rwa2 [battery_pct] [strategy]

   1. With no arguments, the battery starts at 100.0 % and both
      strategies run.
   2. The first argument is the starting battery level. Convert it with
      ``std::from_chars``, as in the Input Validation reading. The
      **whole** argument must be read: ``1.2x`` is not a number. Then
      check it with ``is_within`` (R4) on ``double`` values: it must lie
      between 0.0 and 100.0.
   3. The second argument is the name of one strategy. Only that strategy
      runs. Look the name up in the table from R5.
   4. Do all of this in one function. In ``mission.hpp``, declare these,
      exactly as written here:

      .. code-block:: cpp

         struct Options {
             double battery_pct{100.0};
             std::string_view strategy{"all"};
         };

         std::optional<Options> parse_arguments(int argc, char* argv[], const StrategyTable& strategies);

      ``parse_arguments`` returns the options, or an empty optional when
      an argument is wrong. In ``main``, call it right after
      ``make_strategies``, and return ``1`` when the optional is empty.
   5. Check every argument **before** printing anything else. On an
      error, ``parse_arguments`` prints one of these messages to
      ``std::cerr``:

      .. list-table::
         :header-rows: 1
         :widths: 40 60
         :class: compact-table

         * - Case
           - Message
         * - More than two arguments
           - ``usage: rwa2 [battery_pct] [strategy]``
         * - First argument not a number
           - ``not a number: <arg>``
         * - Number outside 0 to 100
           - ``battery out of range: <arg>``
         * - Unknown strategy name
           - ``unknown strategy: <arg>``

   6. Build the project, run it under Valgrind with no arguments, and
      paste the last lines of Valgrind's output into ``README.md``.

   Acceptance criteria:

   * Each error case prints its message on ``std::cerr``, prints nothing
     on ``std::cout``, and returns 1.
   * The battery argument goes through ``std::from_chars`` and
     ``is_within``.
   * Valgrind reports ``All heap blocks were freed -- no leaks are
     possible`` and ``ERROR SUMMARY: 0 errors``.

   Expected output, one strategy with a lower starting battery. The
   drone and sector blocks are the same as before, except that the
   drone's battery reads 60.0 %, so only the strategy block is shown:

   .. code-block:: text

      $ ./rwa2 60 nearest
      ...
      ===== STRATEGY: nearest =====
      [01] takeoff
      [02] scanned sector 1
      [03] scanned sector 3
      [04] victim 5017 located
      [05] returning to base
      [06] landed
      visited  : 1 3
      distance : 230.1 m
      phase    : idle
      altitude : 0 m
      battery  : 29.0 %
      rotors   : 0.0 rpm
      state    : grounded
      position : (0.0, 0.0) m
      victim   : id 5017 in sector 3

   With 60.0 % the drone still finds the victim, and lands with 29.0 %,
   which is 40.0 % less than the 100.0 % run. The legs and the flight
   home cost the same in both runs.

   The error cases print only their message:

   .. code-block:: text

      $ ./rwa2 80 nearest extra
      usage: rwa2 [battery_pct] [strategy]
      $ ./rwa2 abc
      not a number: abc
      $ ./rwa2 1.2x
      not a number: 1.2x
      $ ./rwa2 150
      battery out of range: 150
      $ ./rwa2 80 zigzag
      unknown strategy: zigzag


How Your Documentation Is Graded
--------------------------------

Documentation is worth **10 %** on its own (see the rubric). R1 asks for
the comments to be **there**; this grade is for whether they **help**: a
reader who sees only ``drone.hpp``, ``mission.hpp`` and the Doxygen pages
should be able to call every function correctly without opening a
``.cpp`` file.

1. **Every** ``@brief`` says what the function does, in one sentence, in
   terms of the mission ("Plan a leg to a sector"), not of the code
   ("Calls distance and battery_ok").
2. **Every** ``@param`` says what the value means, its unit (meters,
   percent) when it has one, and any limit on it.
3. **Every** ``@return`` says what each possible result means, including
   an empty ``std::optional`` and what ``false`` means for a ``bool``.
4. **Every constant** has a ``///`` comment saying what it is, its unit,
   and where its value comes from: RWA1, or chosen for this assignment.
   **Every struct** has a one-line ``///`` comment.
5. **The two parameter comments** (on ``sectors`` in ``find_sector`` and
   in ``run_mission``) give the reason for the choice. Restating the type
   ("sectors is a span") earns nothing.
6. **Other comments** explain *why*, not *what*. No commented-out code,
   and no comment that no longer matches the code under it.

A comment that only repeats the names gets no credit:

.. code-block:: cpp

   /**
    * @brief plan_leg function.
    * @param from from
    * @param to to
    * @param battery_pct battery
    * @return LegPlan
    */
   LegPlan plan_leg(Point from, Point to, double battery_pct);

This one tells a caller what they need to know:

.. code-block:: cpp

   /**
    * @brief Plan a leg to a sector, including the scan and the flight home.
    * @param from Where the drone is.
    * @param to Center of the next sector.
    * @param battery_pct Battery level before the leg, in percent.
    * @return The leg's distance in meters and energy in percent, and whether
    *         the drone could fly it and still get home with at least
    *         min_battery_pct left.
    */
   LegPlan plan_leg(Point from, Point to, double battery_pct);


Deliverables
------------

Submit **one zip file** on Canvas, named after the folder it contains:
``rwa2_firstname_lastname.zip``, for example
``rwa2_bjarne_stroustrup.zip``.

The zip holds exactly the layout shown in R1, and nothing else.

.. list-table::
   :header-rows: 1
   :widths: 25 75
   :class: compact-table

   * - File
     - Description
   * - ``CMakeLists.txt``
     - Builds the three source files into an executable named ``rwa2``,
       as described in R1.
   * - ``include/drone.hpp``, ``include/mission.hpp``
     - The declarations, constants, structs and the two templates.
   * - ``src/drone.cpp``, ``src/mission.cpp``
     - The definitions of the functions declared in the matching header.
   * - ``src/main.cpp``
     - ``main`` only, and only calls (see R1).
   * - ``docs/Doxyfile``
     - The Doxygen configuration, with relative paths.
   * - ``README.md``
     - How to build and run, the last lines of your Valgrind output, and
       your AI disclosure if you used a tool.

``src/main.cpp`` is laid out like this. The markers are how your work
gets found when it is graded, so keep them in this order. The ``TODO``
comments say what goes under each marker: one value to create and one
function to call, plus the early ``return`` in R6. Replace each ``TODO``
with the code it describes.

.. code-block:: cpp

   /**
    * @file main.cpp
    * @author Firstname Lastname (your_email@umd.edu)
    * @brief RWA2: a sector sweep mission planner.
    * @version 0.1
    * @date 2026-10-23
    *
    * @copyright Copyright (c) 2026
    */

   #include "drone.hpp"
   #include "mission.hpp"
   // TODO: add the standard headers main uses (std::optional, std::vector)

   int main(int argc, char* argv[]) {
       // ===== R5: the strategy table =====
       // TODO: create a const StrategyTable named strategies from make_strategies().
       //       It comes first because parse_arguments (R6) needs it to check
       //       the strategy name.

       // ===== R6: command-line arguments =====
       // TODO: call parse_arguments with argc, argv and strategies, and keep the
       //       result in a const std::optional<Options> named options.
       // TODO: if options is empty, return 1. parse_arguments has already
       //       printed the error message, so main prints nothing.

       // ===== R2 and R4: the drone =====
       // TODO: create a const DroneStatus named drone with a designated
       //       initializer that sets only battery_pct, taken from options.
       // TODO: pass drone to print_preflight. It prints the drone and runs the
       //       R4 altitude check.

       // ===== R3: the sectors =====
       // TODO: create a const std::vector<Sector> named sectors from make_sectors().
       // TODO: pass sectors to print_sectors.

       // ===== R5: run the strategies =====
       // TODO: call run_strategies with strategies, the strategy name from
       //       options, sectors and drone.
   }

.. warning::

   Do **not** include the ``build/`` directory, the pages Doxygen
   generates (``docs/html``, ``docs/latex``), editor folders such as
   ``.vscode/``, or the compiled executable. The project is graded by
   configuring and building it from your ``CMakeLists.txt`` and running
   Doxygen from ``docs``, so a submission that does not build cannot be
   graded.


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 32 12 56
   :class: compact-table

   * - Category
     - Weight
     - Criteria
   * - R1: Project and documentation
     - 10 %
     - The layout, ``#pragma once``, no function bodies in headers except
       the templates, a build with no warnings under ``-Wall -Wextra``,
       Doxygen comments on every file and function, a working
       ``Doxyfile``, no generated pages in the zip, and a ``main`` that
       only creates values and calls functions.
   * - R2: The drone as functions
     - 15 %
     - ``DroneStatus`` with defaults, ``std::optional<Victim>``, the
       four functions, with the defaults only in the declaration.
   * - R3: Sectors, legs and the log
     - 20 %
     - The structs, the ``distance`` default, the ``print`` overloads,
       ``find_sector`` returning an optional, ``plan_leg`` returning a
       struct, ``return_to_base`` changing the drone through a reference,
       ``log_event`` with a ``static`` counter, ``make_sectors``, and
       ``print_sectors`` with the capturing ``count_if`` lambda.
   * - R4: The template
     - 10 %
     - One constrained template with a ``requires`` clause, used on
       ``int`` and on ``double``.
   * - R5: Search strategies
     - 20 %
     - ``run_mission`` with its parameters passed as specified, the
       search following the mission model, a structured binding, the
       ``std::function`` table of lambdas from ``make_strategies``, and
       ``run_strategies``. The numbers match the expected output.
   * - R6: Command line and Valgrind
     - 15 %
     - ``parse_arguments`` returning an optional ``Options``, all four
       error cases, ``std::from_chars`` and ``is_within`` on the battery,
       and a clean Valgrind run in ``README.md``.
   * - Documentation
     - 10 %
     - The six points in `How Your Documentation Is Graded`_: useful
       ``@brief``, ``@param`` and ``@return`` text, commented constants
       and structs, the two parameter comments giving their reasons, and
       comments that explain why.

Code that ignores the course conventions loses marks in the requirement
where it appears: uniform initialization, ``snake_case``, names that say
what the value is, and ``'\n'`` rather than ``std::endl``.


Tips
----

.. admonition:: Check the worked example first
   :class: tip

   Write ``distance`` and ``plan_leg``, then call ``plan_leg`` from the
   base to sector 4 with 100.0 % battery. You should get 170.0 m, 21.0 %
   and a feasible leg. If you do not, the rest of the numbers cannot
   match either.

.. admonition:: Your layout may differ, your numbers may not
   :class: tip

   The spacing and labels of the expected output are a guide. The
   numbers, the order of the visited sectors, and the sequence of log
   events must match, since they follow from the mission model and the
   data. Print percentages and distances with one digit after the
   decimal point.

.. admonition:: Build after every requirement
   :class: tip

   R1 to R6 are in dependency order. Get R1 building with an empty
   ``main``, then add R2, and so on. A link error such as ``undefined
   reference`` means a function is declared but not defined, or its
   ``.cpp`` file is missing from ``CMakeLists.txt``.

.. admonition:: Follow the conventions
   :class: tip

   * Uniform initialization: ``int count{0};``, not ``int count = 0;``
   * ``snake_case``: ``battery_pct``, not ``batteryPct``
   * ``'\n'``, never ``std::endl``


References
----------

The **C++ Core Guidelines** are the rules this course grades against.
These are the ones that apply to RWA2. Read the short entry behind each
link before you write the matching requirement.

.. list-table::
   :header-rows: 1
   :widths: 16 84
   :class: compact-table

   * - Rule
     - Says
   * - `F.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-logical>`_
     - A function should perform a single logical operation.
   * - `F.16 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-in>`_
     - For "in" parameters, pass cheaply-copied types by value and others
       by reference to ``const``.
   * - `F.17 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-inout>`_
     - For "in-out" parameters, pass by reference to non-``const``.
   * - `F.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out>`_
     - For "out" output values, prefer return values to output
       parameters.
   * - `F.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out-multi>`_
     - To return multiple "out" values, prefer returning a struct.
   * - `F.51 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-default-args>`_
     - Where there is a choice, prefer default arguments over
       overloading.
   * - `C.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-org>`_
     - Organize related data into structures (``struct``\ s or
       ``class``\ es).
   * - `T.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concepts>`_
     - Specify concepts for all template arguments.
   * - `T.40 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-fo>`_
     - Use function objects to pass operations to algorithms.
   * - `SF.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-inline>`_
     - A header file must not contain object definitions or non-inline
       function definitions.
   * - `SF.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-consistency>`_
     - A ``.cpp`` file must include the header file(s) that defines its
       interface.
   * - `R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`_
     - Avoid calling ``new`` and ``delete`` explicitly.
   * - `ES.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-always>`_
     - Always initialize an object.
   * - `NL.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rl-camel>`_
     - Prefer ``underscore_style`` names.
