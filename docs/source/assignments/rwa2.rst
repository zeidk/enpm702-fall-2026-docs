====================================================
RWA2: STL Containers and Functions
====================================================

Overview
--------

In this assignment you **refactor RWA1** to replace its fixed-size raw
arrays with STL containers and to extract repeated logic into
well-designed functions.

RWA1 stored its data in fixed-size, C-style arrays on the stack (for
example ``double thermal_readings[5]``, ``double gas_readings[...]``, and
an ``int victim_ids[max_victims]`` paired with a separate ``int
victim_count``). Those arrays are rigid and unsafe: their size is baked
in at compile time, they cannot grow when a search team reports more
victims than expected, they silently overflow when you write past the
end, and they force you to carry around a separate count variable. RWA1
never used ``new`` or ``delete``, so the problem is not manual memory
management: the problem is that fixed-size arrays do not adapt to the
data and give you no bounds safety.

In RWA2 you replace those raw arrays with ``std::vector`` and
``std::array``, which grow on demand, track their own size, and offer
bounds-checked access. You also move repeated blocks of logic into
reusable functions with proper parameter passing. By the end you will
have a cleaner, safer search-and-rescue simulator that demonstrates
exactly *why* the Standard Library exists.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Use ``std::vector`` and ``std::array`` instead of fixed-size C-style
   arrays.
2. Write functions with appropriate parameter passing (by value,
   by reference, by ``const`` reference).
3. Apply **function overloading** to provide multiple call signatures.
4. Use **iterators** and **range-based for loops** for container traversal.
5. Perform common ``std::string`` operations (``find``, ``substr``,
   ``insert``, ``erase``).
6. Document all functions with **Doxygen** comments.


Requirements
------------

.. dropdown:: R1: Replace Raw Arrays
   :open:

   Replace every fixed-size raw array from RWA1 with an STL container.
   The goal is to remove the rigid compile-time sizes and the separate
   count variables.

   **Steps**

   #. Convert the **victim registry** from ``int victim_ids[max_victims]``
      plus ``int victim_count`` to a single ``std::vector<int>``. Delete
      the separate count variable: use ``size()`` instead.
   #. Convert the **sensor readings** (thermal and gas) from
      ``double thermal_readings[5]`` and ``double gas_readings[...]`` to
      ``std::vector<double>``.
   #. Use ``std::array`` for data whose size is genuinely fixed and known
      at compile time (for example a fixed set of robot IDs or a fixed
      number of search sectors). Choose ``std::array`` over ``std::vector``
      only when the count never changes.
   #. Somewhere in your program, demonstrate each of the following
      member functions at least once: ``push_back``, ``emplace_back``,
      ``erase``, ``size``, and ``capacity``.

   **Acceptance criteria**

   * No fixed-size C-style arrays remain in the refactored code.
   * No standalone ``victim_count`` (or equivalent) variable remains.
   * The victim registry can grow at runtime without a compile-time
     size limit.

   .. code-block:: cpp

      // Illustrative skeleton: a growable victim registry.
      std::vector<int> victim_ids;

      // TODO: reserve capacity for the expected number of victims.
      // TODO: add victim IDs to the registry using push_back (and try
      //       emplace_back for at least one insertion).

      // TODO: print the registry's size() and capacity() and observe how
      //       capacity grows as elements are added.

      // A reported victim turned out to be a false positive.
      // TODO: erase the corresponding element using an iterator
      //       (for example victim_ids.begin() + index).

.. dropdown:: R2: Extract Functions
   :open:

   Move repeated or logically distinct blocks of ``main`` into named
   functions. At a minimum, implement the following four functions:

   * ``print_site_info()``: display the search-zone name, dimensions, and
     sector count to the console.
   * ``add_robot()``: add a robot to the robot collection (a
     ``std::vector<Robot>``).
   * ``remove_robot()``: remove a robot from the collection by its ID;
     report whether a robot was actually removed.
   * ``update_robot_position()``: change a robot's coordinates by a given
     displacement.

   **Parameter-passing guidelines**

   * **Pass by const reference** for read-only parameters that are
     expensive to copy (for example ``const std::string&`` and
     ``const std::vector<Robot>&``).
   * **Pass by reference** for parameters the function must modify (for
     example the robot collection in ``add_robot`` / ``remove_robot``).
   * **Pass by value** for cheap-to-copy parameters (``int``, ``double``,
     ``bool``).
   * **Return a value** rather than writing through an output parameter
     when practical.

   **Acceptance criteria**

   * Each function has a single, clear responsibility.
   * ``remove_robot`` returns a ``bool`` (or similar) indicating success.
   * ``add_robot`` increases the collection size by exactly one.
   * No logic that belongs in these functions remains duplicated in
     ``main``.

   .. code-block:: cpp

      /**
       * @brief Print search-zone information to the console.
       * @param name    Site name (read-only).
       * @param length  Search-zone length in meters.
       * @param width   Search-zone width in meters.
       * @param sectors Number of sectors in the zone.
       */
      void print_site_info(const std::string& name,
                           double length,
                           double width,
                           int sectors) {
          // TODO: print the site name, the length x width dimensions,
          //       and the sector count in a readable format.
      }

      /**
       * @brief Add a robot to the rescue fleet.
       * @param fleet  Robot collection to modify (by reference).
       * @param robot  Robot to add (read-only).
       */
      void add_robot(std::vector<Robot>& fleet, const Robot& robot) {
          // TODO: append the robot to the fleet.
      }

.. dropdown:: R3: Function Overloading
   :open:

   Overload at least one function so it accepts different parameter
   types. A good candidate is ``find_victim``, which should support
   searching the victim collection in three different ways:

   * Find a victim **by ID** (``int``).
   * Find a victim **by sector name** (``const std::string&``).
   * Find a victim **by position** (``double x``, ``double y``).

   **Acceptance criteria**

   * All overloads share the same function name and differ only in their
     parameter lists.
   * Each overload returns the index of the matching victim, or ``-1``
     when no victim matches.
   * Calling code selects the correct overload purely by the argument
     types (no manual flags or mode parameters).

   .. code-block:: cpp

      /**
       * @brief Find a located victim by ID.
       * @param victims  Vector of victims (read-only).
       * @param id       Victim ID to search for.
       * @return Index of the victim, or -1 if not found.
       */
      int find_victim(const std::vector<Victim>& victims, int id);

      /**
       * @brief Find a located victim by sector name.
       * @param victims  Vector of victims (read-only).
       * @param sector   Sector designation to search for.
       * @return Index of the victim, or -1 if not found.
       */
      int find_victim(const std::vector<Victim>& victims,
                      const std::string& sector);

      /**
       * @brief Find a located victim by position.
       * @param victims  Vector of victims (read-only).
       * @param x        X-coordinate to match.
       * @param y        Y-coordinate to match.
       * @return Index of the victim, or -1 if not found.
       */
      int find_victim(const std::vector<Victim>& victims,
                      double x, double y);

      // TODO: implement each overload by traversing the victims vector
      //       and returning the index of the first match (or -1).

   .. note::

      At this stage ``Victim`` (and ``Robot``) can be a simple
      ``struct``; full class design is deferred to RWA3.

.. dropdown:: R4: Iterators
   :open:

   Demonstrate both iterator-based and range-based traversal of your
   containers.

   **Steps**

   #. Use explicit **iterators** (not index-based ``for`` loops) to
      traverse a container in at least two places.
   #. Use **range-based for loops** where the loop only needs each
      element and not its position.
   #. When you only read elements, bind them with ``const auto&`` to
      avoid copies.

   **Acceptance criteria**

   * At least two distinct iterator-based traversals appear in your code.
   * At least one range-based for loop appears in your code.
   * No raw index arithmetic is used where an iterator or range-based
     loop would be clearer.

   .. code-block:: cpp

      // Iterator-based traversal.
      for (auto it{victim_ids.begin()}; it != victim_ids.end(); ++it) {
          // TODO: dereference the iterator (*it) and print the victim ID.
      }

      // Range-based for loop over read-only elements.
      for (const auto& reading : thermal_readings) {
          // TODO: print the thermal reading.
      }

.. dropdown:: R5: String Operations
   :open:

   Use ``std::string`` for robot callsigns and victim location
   descriptions, and exercise the string member functions taught in
   lecture.

   **Steps**

   #. Store at least one robot callsign and one victim location
      description as a ``std::string``.
   #. Demonstrate at least **four** of the following operations:
      ``insert``, ``erase``, ``find``, ``substr``, ``append``,
      ``replace``.
   #. Guard any ``find`` result against ``std::string::npos`` before you
      use it.

   **Acceptance criteria**

   * At least four distinct string operations are used.
   * Every ``find`` result is checked against ``std::string::npos``
     before being used as an index.

   .. code-block:: cpp

      std::string robot_callsign{"Rescue_Alpha_01"};

      // find + substr: extract the unit name from the callsign.
      auto pos{robot_callsign.find("Alpha")};
      if (pos != std::string::npos) {
          // TODO: use substr to extract the unit substring and print it.
      }

      // TODO: use insert to add a prefix (for example "ENPM702_") to the
      //       callsign.

      // TODO: use erase (and/or replace/append) to demonstrate a fourth
      //       distinct string operation.

.. dropdown:: R6: Documentation
   :open:

   Document **every** function with Doxygen-style comments so the
   generated documentation is complete.

   **Steps**

   #. Add a ``@brief`` one-line summary to each function.
   #. Add a ``@param`` line describing each parameter.
   #. Add a ``@return`` line for every function that returns a value.

   **Acceptance criteria**

   * Every function (declaration or definition) carries a Doxygen
     comment block.
   * Each parameter has a matching ``@param`` entry, and each
     non-``void`` function has a ``@return`` entry.

   .. code-block:: cpp

      /**
       * @brief Update the position of a rescue robot.
       * @param x  Reference to the robot's x-coordinate (modified).
       * @param y  Reference to the robot's y-coordinate (modified).
       * @param dx Displacement in x.
       * @param dy Displacement in y.
       */
      void update_robot_position(double& x, double& y,
                                 double dx, double dy) {
          // TODO: apply the displacement (dx, dy) to the robot's
          //       coordinates (x, y).
      }


Deliverables
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Description
   * - Header files (``.hpp``)
     - Declarations for all functions and structs.
   * - Source files (``.cpp``)
     - Implementations and ``main.cpp``.
   * - ``CMakeLists.txt``
     - Build configuration targeting C++17 or later.
   * - Doxygen output
     - Generated HTML documentation (or a ``Doxyfile`` that produces it).


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Category
     - Weight
     - Criteria
   * - Correctness
     - 35 %
     - Program compiles, runs, and produces correct output.
   * - Function Design
     - 25 %
     - Proper parameter passing, clear interfaces, no unnecessary
       globals.
   * - STL Usage
     - 20 %
     - Effective use of ``std::vector``, ``std::array``, ``std::string``,
       and iterators.
   * - Documentation
     - 20 %
     - Complete Doxygen comments on every function; readable code.


Tips
----

.. admonition:: Refactor Incrementally
   :class: tip

   Start by copying your RWA1 code. Replace one fixed-size array at a
   time (and remove its matching count variable) and verify the output
   still matches before moving on.

.. admonition:: Compile Often
   :class: tip

   Each time you extract a function, compile and test immediately.
   Small, frequent compilations catch errors early.

.. admonition:: Parameter Passing Rule of Thumb
   :class: tip

   * **Cheap to copy** (``int``, ``double``, ``bool``): pass by value.
   * **Expensive to copy** and read-only: pass by ``const`` reference.
   * **Needs modification**: pass by reference.
