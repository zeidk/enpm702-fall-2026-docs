====================================================
RWA1: C++ Fundamentals
====================================================

Overview
--------

In this assignment you build a simple disaster-site search-and-rescue
(SAR) simulator in pure C++. This first version models rescue robots,
on-board sensors, and located victims using basic types, fixed-size
arrays, pointers, pointer arithmetic, and references. There is no
dynamic memory allocation (no ``new`` or ``delete``) and no
object-oriented design yet. The goal is to practice foundational C++
constructs before refactoring in later assignments.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Apply variables, types, and constants in a practical context.
2. Use pointers and pointer arithmetic to access and traverse fixed-size arrays.
3. Apply const-correctness with pointers (a pointer to ``const``).
4. Use references to alias and modify variables.
5. Follow ``snake_case`` naming and uniform initialization conventions.
6. Produce formatted console output with ``'\n'`` (not ``std::endl``).

.. note::

   This assignment uses **only stack memory**. You point at variables and
   arrays that already exist; you do **not** allocate memory with
   ``new``. Dynamic allocation and smart pointers come in later
   assignments.


Requirements
------------

.. dropdown:: R1: Search Zone Environment
   :open:

   Set up the variables that describe the disaster site your robots will
   search. These values are the "scene" for the rest of the program.

   Step by step:

   1. Declare ``length`` and ``width`` as ``double`` values for the
      search-zone dimensions, in meters.
   2. Declare ``site_name`` as a ``std::string`` holding the building or
      grid designation (for example, the name of a collapsed structure).
   3. Declare ``num_sectors`` as an ``int`` recording how many sectors
      the zone is divided into.
   4. Declare a ``constexpr`` value for any quantity that is fixed at
      compile time and never changes during the mission, such as the
      maximum number of victims the registry can track. You will reuse
      this capacity to size the array in R4, so choose a sensible
      positive value.

   Acceptance criteria:

   * All five items above exist and use uniform initialization (braces).
   * The compile-time capacity is declared with ``constexpr`` (not a
     plain variable).
   * Each variable has a clear, ``snake_case`` name.

   The block below shows the kinds of declarations expected. Choose your
   own values.

   .. code-block:: cpp

      constexpr int max_victims{200};
      std::string site_name{"Sector 7, Collapsed Office Block"};
      double length{90.0};
      double width{60.0};
      int num_sectors{12};

.. dropdown:: R2: Rescue Robot Representation
   :open:

   Model each rescue robot using a small group of individual variables.
   You do not have classes or structs yet, so every robot is described by
   its own set of plain variables.

   Each robot needs:

   * ``robot_id`` (``int``): a unique identifier.
   * ``x_position`` and ``y_position`` (``double``): the robot's
     coordinates inside the search zone.
   * ``battery_level`` (``double`` in the range 0 to 100): remaining
     charge as a percentage.
   * ``is_operational`` (``bool``): whether the robot is online and able
     to move.

   Step by step:

   1. Create **at least three** robots, each with the five values above.
   2. Give the robots **distinct** values so the output is meaningful
      (different positions, different battery levels, and at least one
      robot that is not operational).
   3. Use a consistent naming scheme so it is obvious which variable
      belongs to which robot (for example, prefix every variable for the
      first robot with ``robot1_``).

   Acceptance criteria:

   * Three or more robots are fully described.
   * No two robots are identical.
   * At least one robot has ``is_operational`` set to ``false`` so the
     report in R6 can distinguish online from offline robots.

   The block below shows the variables for a single robot. Repeat the
   pattern for the other robots with your own values.

   .. code-block:: cpp

      // Robot 1
      int robot1_id{1};
      double robot1_x{0.0};
      double robot1_y{0.0};
      double robot1_battery{100.0};
      bool robot1_operational{true};

.. dropdown:: R3: Sensor Data and Pointers
   :open:

   Each robot carries sensors. In this requirement you store sensor
   readings in fixed-size arrays and then access them through pointers,
   using pointer arithmetic rather than array indexing.

   Step by step:

   1. Create a C-style **fixed-size array** of **thermal** readings
      (temperature in degrees Celsius) with at least 5 elements, and a
      second C-style fixed-size array of **gas concentration** readings
      (carbon monoxide, in ppm) with at least 5 elements. Initialize both
      arrays with sample values.
   2. Declare a **pointer** that points at the first element of an array.
      Remember that the array name decays to the address of its first
      element, so the pointer can be initialized directly from the array.
   3. Traverse one of the arrays using **pointer arithmetic** (for
      example, by dereferencing ``*(ptr + i)``) and print each reading
      with its sensor index. Do **not** use array indexing such as
      ``ptr[i]`` for this traversal; the point is to practice pointer
      arithmetic.
   4. **Modify** at least one reading through the pointer (write a new
      value through the dereferenced pointer), then show that the change
      is visible in the array.

   Acceptance criteria:

   * Two fixed-size arrays exist, each with 5 or more elements.
   * The traversal prints every element of at least one array, labeled
     with its index, using pointer arithmetic.
   * At least one element is changed through the pointer, and the new
     value appears in later output.

   Expected console output (illustrative; your values will differ)::

      Thermal sensor 0: 31.2 C
      Thermal sensor 1: 36.7 C
      ...

   The skeleton below shows the declarations and the pointer setup. Fill
   in the logic where marked.

   .. code-block:: cpp

      double thermal_readings[5]{31.2, 36.7, 29.4, 37.1, 33.8};
      double* thermal_ptr{thermal_readings};

      // TODO: traverse the array using pointer arithmetic, e.g.
      // *(thermal_ptr + i), and print each reading with its index.
      // Do not use array indexing (thermal_ptr[i]) here.

      // TODO: modify at least one reading by writing through the
      // pointer, e.g. *(thermal_ptr + k) = new_value;

      // TODO: repeat the array, pointer, and traversal steps for the
      // gas-concentration readings.

.. dropdown:: R4: Victim Registry (No Dynamic Allocation)
   :open:

   Track located victims using a **fixed-size array on the stack**. Do
   **not** use ``new`` or ``delete``.

   The registry stores the IDs of victims as they are located. Because
   you cannot allocate memory yet, you reserve the maximum space up front
   with a fixed-size array and track how much of it is actually used.

   Step by step:

   1. Declare a fixed-size array of victim IDs sized by your
      ``constexpr`` capacity from R1, for example
      ``int victim_ids[max_victims]``. Value-initialize it so all unused
      entries start at zero.
   2. Keep a separate ``int victim_count`` that records how many victims
      have been located so far. It starts at zero.
   3. Simulate locating several victims: for each one, store its ID in
      the next free slot (the slot at index ``victim_count``) and then
      increase ``victim_count`` by one. Add at least a few victims this
      way.
   4. Print the registry using a **pointer** and **pointer arithmetic**.
      Iterate only over the **filled** entries (indices ``0`` up to but
      not including ``victim_count``), never over the entire capacity, so
      that empty slots are not printed.

   Acceptance criteria:

   * The array is sized by the ``constexpr`` capacity, not a hard-coded
     literal.
   * ``victim_count`` always equals the number of IDs actually stored.
   * The print loop visits exactly ``victim_count`` entries using pointer
     arithmetic, and unused slots are not shown.
   * No ``new`` or ``delete`` appears anywhere.

   Expected console output (illustrative; your values will differ)::

      Victim 0: 500
      Victim 1: 501
      ...

   The skeleton below shows the declarations. Fill in the logic where
   marked.

   .. code-block:: cpp

      int victim_ids[max_victims]{};   // value-initialized, all zeros
      int victim_count{0};

      // TODO: log several located victims. For each one, write its ID
      // into victim_ids[victim_count], then increment victim_count.

      int* victim_ptr{victim_ids};
      // TODO: print only the filled entries (indices 0 .. victim_count-1)
      // using pointer arithmetic, e.g. *(victim_ptr + i).

.. dropdown:: R5: References and Const-Correctness
   :open:

   This requirement contrasts two ideas: a reference, which is an alias
   that lets you change the original variable, and a pointer to
   ``const``, which lets you read data but not change it through that
   pointer.

   Step by step:

   1. Create **reference variables** that alias one robot's position
      variables (its x and y coordinates). A reference must be bound to
      an existing variable when it is declared.
   2. Update the robot's position by assigning **through the
      references**, not through the original variable names.
   3. Print the original position variables afterward to demonstrate that
      writing through a reference changed the original variables (the
      reference and the variable name refer to the same storage).
   4. Create a **pointer to const** (for example,
      ``const double* read_only_ptr``) that points at the thermal
      readings array. Read one or more values through it. Confirm for
      yourself that an attempt to assign through this pointer, such as
      ``*read_only_ptr = ...;``, would fail to compile; do not leave such
      a line in your submission, but explain in a comment why it is
      rejected.

   Acceptance criteria:

   * At least one reference is declared and bound to a robot position
     variable.
   * The position is updated through the reference, and the printed
     original variable reflects that update.
   * A pointer to ``const`` is used for read-only access to the sensor
     data, with a comment noting that modification through it is not
     allowed.

   The skeleton below shows the declarations. Fill in the logic where
   marked.

   .. code-block:: cpp

      double& ref_x{robot1_x};
      double& ref_y{robot1_y};

      // TODO: update the robot's position by assigning through ref_x
      // and ref_y (not through robot1_x / robot1_y directly).

      // TODO: print robot1_x and robot1_y to show the originals changed.

      // Read-only access: the data cannot be changed through this pointer.
      const double* read_only_ptr{thermal_readings};
      // TODO: read and print one or more readings through read_only_ptr.
      // Note in a comment why "*read_only_ptr = ...;" would not compile.

.. dropdown:: R6: Output
   :open:

   Bring everything together into a single, readable situation report
   printed to the console. This report is what a rescue coordinator would
   read at a glance, so group related information under clear headings.

   Your report must include, in clearly separated sections:

   1. **Search-zone information**: the site name, the dimensions (length
      and width), the number of sectors, and the victim capacity from R1.
   2. **Robot statuses**: for every robot, its ID, position (x and y),
      battery level, and whether it is operational or offline. Print the
      word "operational" or "offline" rather than a raw ``true`` or
      ``false`` so the report reads naturally.
   3. **Sensor readings**: all thermal readings and all gas-concentration
      readings from R3, including any value you modified through a
      pointer.
   4. **Victim registry**: the located victims from R4, iterating only
      over the filled entries.

   Acceptance criteria:

   * All four sections appear and are visually separated (for example,
     with a header line before each section).
   * Robot operational status is shown as readable text, not ``1`` or
     ``0``.
   * The sensor and victim output reflects the values produced in R3 and
     R4 (for example, the modified thermal reading appears).
   * Every newline uses ``'\n'``. Do **not** use ``std::endl``.


Deliverables
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Description
   * - ``main.cpp``
     - Single source file containing all code.
   * - ``CMakeLists.txt``
     - Build configuration targeting C++17 or later.
   * - ``README.md``
     - Build and run instructions.


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Category
     - Weight
     - Criteria
   * - Correctness
     - 40 %
     - Program compiles, runs, and produces the required output.
   * - Pointers and References
     - 30 %
     - Correct use of pointers, pointer arithmetic, const-correctness,
       and references. No dynamic allocation (no ``new`` or ``delete``).
   * - Code Quality
     - 20 %
     - Uniform initialization, ``snake_case`` naming, ``'\n'`` usage,
       clear variable names.
   * - Documentation
     - 10 %
     - README with build instructions, plus inline comments explaining
       pointer and reference usage.


Tips
----

.. admonition:: Start Early
   :class: tip

   Begin with the search-zone variables and robot representations, then
   add the sensor arrays and the victim registry.

.. admonition:: Point Only at What Exists
   :class: tip

   Every pointer in this assignment points at a variable or array that
   already exists on the stack. You do not need ``new`` or ``delete``
   anywhere. If you find yourself reaching for ``new``, step back: a
   fixed-size array and a count are enough.

.. admonition:: Follow the Conventions
   :class: tip

   * Use **uniform initialization**: ``int a{1};`` not ``int a = 1;``
   * Use **snake_case**: ``battery_level`` not ``batteryLevel``
   * Use ``'\n'`` instead of ``std::endl``
