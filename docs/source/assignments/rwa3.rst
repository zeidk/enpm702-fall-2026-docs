====================================================
RWA3: Smart Pointers and OOP
====================================================

Overview
--------

In this assignment you **redesign** the search-and-rescue simulator
using object-oriented principles. You will create a class hierarchy for
rescue robots and sensors, manage object lifetimes with smart pointers,
and apply polymorphism so that different robot types exhibit distinct
search behaviors, all without a single raw ``new`` or ``delete``.

This assignment continues a deliberate progression. In RWA1 every object
lived on the stack: fixed-size arrays, pointers, and references, with no
dynamic allocation at all. In RWA2 you moved to STL containers
(``std::vector`` and ``std::array``) and organized your logic into
functions. RWA3 takes the next step: you now design real objects with
behavior and you give those objects **dynamic lifetimes**. Because the
number of robots and sensors is decided at run time, these objects must
be heap-allocated. Rather than reaching for raw ``new`` and ``delete``,
you express dynamic allocation **exclusively through smart pointers**
(``std::unique_ptr``, ``std::shared_ptr``, and ``std::weak_ptr``, created
with ``std::make_unique`` and ``std::make_shared``). The smart pointers
own the heap memory and release it automatically, which is how dynamic
allocation is handled safely in modern C++.


Learning Objectives
-------------------

After completing this assignment you will be able to:

1. Design class hierarchies with inheritance.
2. Apply encapsulation with proper access specifiers.
3. Use **virtual functions** for runtime polymorphism.
4. Manage object lifetimes with ``std::unique_ptr`` and
   ``std::shared_ptr``.
5. Implement proper constructors, destructors, and reason about
   the **Rule of Five**.
6. Apply ``const``-correctness throughout a multi-class project.


Requirements
------------

.. dropdown:: R1: Class Design
   :open:

   Create a ``Robot`` **base class** with:

   * **Attributes** (``private``): ``id_`` (``int``), ``callsign_``
     (``std::string``), ``x_position_``, ``y_position_``
     (``double``), ``battery_level_`` (``double``).
   * **Public interface**: ``move()``, ``report_status()``, getters,
     and setters where appropriate.
   * A **default constructor** and a **parameterized constructor**
     using a member initialization list.
   * A **virtual destructor**.

   **Step by step**

   1. Declare the class in ``robot.hpp`` with the five private
      attributes listed above. Give each attribute a sensible default
      member initializer.
   2. Provide a defaulted default constructor and a parameterized
      constructor that initializes all five attributes through a
      member initialization list (no assignment inside the body).
   3. Declare a ``virtual`` destructor so that derived objects are
      destroyed correctly through a ``Robot`` pointer.
   4. Declare ``move(double dx, double dy)`` and
      ``report_status() const`` as ``virtual`` so derived classes can
      override them. ``report_status()`` returns a ``std::string``.
   5. Provide ``const`` getters for every attribute and setters only
      where mutation is meaningful (for example battery level, but not
      ``id_``). Define the method bodies in ``robot.cpp``.

   **Acceptance criteria**

   * The base ``move()`` updates ``x_position_`` and ``y_position_`` and
     decreases ``battery_level_``.
   * The base ``report_status()`` returns a human-readable summary that
     includes the callsign, position, and battery level.
   * Every method that does not modify the object is marked ``const``.

   .. code-block:: cpp

      // robot.hpp (illustrative skeleton, not a solution)
      class Robot {
       public:
          Robot() = default;

          Robot(int id, const std::string& callsign,
                double x, double y, double battery);

          virtual ~Robot() = default;

          // Polymorphic interface (override in derived classes).
          virtual void move(double dx, double dy);
          virtual std::string report_status() const;

          // Getters (const) and selected setters.
          int get_id() const;
          const std::string& get_callsign() const;
          double get_battery_level() const;
          void set_battery_level(double level);

       private:
          int id_{0};
          std::string callsign_;
          double x_position_{0.0};
          double y_position_{0.0};
          double battery_level_{100.0};
      };

      // robot.cpp
      Robot::Robot(int id, const std::string& callsign,
                   double x, double y, double battery) {
          // TODO: initialize all members with a member
          //       initialization list (not assignment in the body).
      }

      void Robot::move(double dx, double dy) {
          // TODO: update x_position_/y_position_ and reduce
          //       battery_level_ to reflect movement cost.
      }

      std::string Robot::report_status() const {
          // TODO: build and return a summary string containing the
          //       callsign, current position, and battery level.
      }

.. dropdown:: R2: Inheritance
   :open:

   Create three derived classes, each with distinct characteristics:

   .. grid:: 3
      :gutter: 3

      .. grid-item-card:: GroundRobot
         :class-header: sd-bg-info sd-text-white

         * Tracked crawler for rubble.
         * Slow but can enter tight voids.
         * Overrides ``move()``, short, careful steps.
         * Overrides ``report_status()``, includes void-access depth.

      .. grid-item-card:: AerialDrone
         :class-header: sd-bg-success sd-text-white

         * Flies above the debris field.
         * Fast coverage, fast battery drain.
         * Overrides ``move()``, long range, faster drain.
         * Overrides ``report_status()``, includes altitude.

      .. grid-item-card:: CanineRobot
         :class-header: sd-bg-warning sd-text-white

         * Legged "rescue dog" platform.
         * Traverses stairs and uneven terrain.
         * Overrides ``move()``, agile over obstacles.
         * Overrides ``report_status()``, includes terrain rating.

   **Step by step**

   1. Each derived class publicly inherits from ``Robot``
      (``public Robot``) and lives in its own header/source pair
      (for example ``ground_robot.hpp`` / ``ground_robot.cpp``).
   2. Each derived class adds one type-specific private attribute:
      ``GroundRobot`` has ``void_access_depth_``, ``AerialDrone`` has
      ``altitude_``, and ``CanineRobot`` has ``terrain_rating_``.
   3. Each constructor forwards the common parameters to the ``Robot``
      base constructor through the member initialization list, then
      initializes its own attribute.
   4. Each derived class **overrides** ``move()`` and
      ``report_status()`` using the ``override`` keyword. The behavior
      must differ per type (see the cards above): for example the
      drone covers more distance and drains battery faster, while the
      ground robot takes short, careful steps.

   **Acceptance criteria**

   * All three derived classes compile and can be instantiated.
   * ``report_status()`` for each type includes the base information
     **plus** that type's extra attribute (void-access depth, altitude,
     or terrain rating).
   * The ``override`` keyword is present on every overriding method.

   .. code-block:: cpp

      // ground_robot.hpp (illustrative skeleton; repeat the same shape
      // for AerialDrone and CanineRobot with their own attributes)
      class GroundRobot : public Robot {
       public:
          GroundRobot(int id, const std::string& callsign,
                      double x, double y, double battery,
                      double void_access_depth);

          void move(double dx, double dy) override;
          std::string report_status() const override;

       private:
          double void_access_depth_{2.0};
      };

      // ground_robot.cpp
      GroundRobot::GroundRobot(int id, const std::string& callsign,
                               double x, double y, double battery,
                               double void_access_depth) {
          // TODO: forward id/callsign/x/y/battery to the Robot base
          //       constructor, then initialize void_access_depth_.
      }

      void GroundRobot::move(double dx, double dy) {
          // TODO: implement short, careful steps with the appropriate
          //       battery cost for a ground crawler.
      }

      std::string GroundRobot::report_status() const {
          // TODO: return the base status plus the void-access depth.
      }

.. dropdown:: R3: Polymorphism
   :open:

   * Store all robots in a
     ``std::vector<std::unique_ptr<Robot>>``.
   * Call ``move()`` and ``report_status()`` through base-class
     pointers.
   * Demonstrate **runtime polymorphism**: each robot type produces
     different output from the same function call.

   **Step by step**

   1. Create a ``std::vector<std::unique_ptr<Robot>>``.
   2. Populate it with at least one instance of each derived type,
      constructing each with ``std::make_unique`` so ownership moves
      into the vector (no raw ``new``).
   3. Iterate over the vector with a range-based ``for`` loop using a
      ``const auto&`` reference to each ``std::unique_ptr``.
   4. Through the base-class pointer, call ``move()`` and then print
      ``report_status()``.

   **Acceptance criteria**

   * The same line of code (``robot->report_status()``) produces
     different output depending on the actual robot type, confirming
     dynamic dispatch through ``virtual`` methods.
   * No object is copied out of the vector; access is through the
     ``unique_ptr`` only.

   .. code-block:: cpp

      // main.cpp (illustrative skeleton)
      std::vector<std::unique_ptr<Robot>> robots;

      // TODO: push_back one std::make_unique<...> for each derived
      //       type (GroundRobot, AerialDrone, CanineRobot) with
      //       suitable constructor arguments.

      for (const auto& robot : robots) {
          // TODO: call move(...) then print report_status() through
          //       the base-class pointer to demonstrate polymorphism.
      }

.. dropdown:: R4: Smart Pointers
   :open:

   Arrange ownership deliberately:

   * Use ``std::unique_ptr`` for **exclusive ownership** of robots
     (the ``CommandCenter`` class owns each robot).
   * Use ``std::shared_ptr`` for **shared sensors**, multiple
     robots may rely on the same fixed sensor (e.g., a beacon dropped
     in a sector).
   * Use ``std::weak_ptr`` for **non-owning references** (e.g., a
     robot holds a weak reference to a sensor it does not own).
   * There must be **no** raw ``new`` or ``delete`` anywhere in
     your code.

   **Step by step**

   1. Create a sensor with ``std::make_shared`` so its lifetime is
      reference-counted.
   2. Give ``Robot`` a way to hold a non-owning reference to a sensor.
      Store it as a ``std::weak_ptr`` so a robot never keeps a sensor
      alive on its own, and provide ``set_sensor(...)`` that accepts a
      ``std::shared_ptr`` and stores it as a ``weak_ptr``.
   3. Point more than one robot at the **same** shared sensor and
      confirm the reference count behaves as expected.
   4. Before using a ``weak_ptr``, call ``lock()`` and check the
      result; only read the sensor if the lock succeeds.

   **Acceptance criteria**

   * Robots own no sensor outright: dropping all shared owners frees
     the sensor even while a robot still holds a ``weak_ptr``.
   * A locked ``weak_ptr`` is always validated before dereferencing.
   * ``grep`` for ``new`` and ``delete`` finds no raw allocation.

   .. code-block:: cpp

      // Illustrative skeleton (not a solution).

      // A shared sensor beacon placed in a sector.
      auto thermal_beacon{
          std::make_shared<ThermalSensor>(/* TODO: ctor args */)};

      // TODO: hand the same shared_ptr to multiple robots via
      //       set_sensor(...); each robot stores it as a weak_ptr.

      // TODO: obtain a weak_ptr to the beacon, lock() it, and only
      //       read() the sensor when the lock succeeds.

.. dropdown:: R5: CommandCenter Class
   :open:

   Create a ``CommandCenter`` class that manages the entire mission:

   * Owns robots via ``std::vector<std::unique_ptr<Robot>>``.
   * Methods:

     - ``add_robot(std::unique_ptr<Robot> robot)``
     - ``remove_robot(int id)``
     - ``find_robot(int id) const``
     - ``print_all_robots() const``

   * Apply ``const``-correctness: mark every method and parameter
     that does not modify state as ``const``.

   **Step by step**

   1. Store the fleet in a private
      ``std::vector<std::unique_ptr<Robot>>`` member.
   2. ``add_robot`` takes the ``std::unique_ptr<Robot>`` **by value**
      and ``std::move``-s it into the vector, transferring ownership
      into the ``CommandCenter``.
   3. ``remove_robot`` erases the robot whose ``get_id()`` matches the
      given ``id``.
   4. ``find_robot`` returns a non-owning observer (a ``Robot*`` or a
      reference) to the matching robot, or a null result if none
      matches; it must not transfer ownership and must be ``const``.
   5. ``print_all_robots`` iterates the fleet and prints each robot's
      ``report_status()``; it is ``const``.

   **Acceptance criteria**

   * Ownership of every robot lives in the ``CommandCenter`` and
     nowhere else.
   * ``find_robot`` and ``print_all_robots`` do not modify the fleet
     and are declared ``const``.
   * Removing a robot destroys it (the ``unique_ptr`` releases its
     memory automatically).

   .. code-block:: cpp

      // command_center.hpp (illustrative skeleton)
      class CommandCenter {
       public:
          void add_robot(std::unique_ptr<Robot> robot);
          void remove_robot(int id);
          Robot* find_robot(int id) const;   // non-owning observer
          void print_all_robots() const;

       private:
          std::string mission_name_{"Default Mission"};
          std::vector<std::unique_ptr<Robot>> robots_;
      };

      // command_center.cpp
      void CommandCenter::add_robot(std::unique_ptr<Robot> robot) {
          // TODO: std::move the unique_ptr into robots_.
      }

      void CommandCenter::remove_robot(int id) {
          // TODO: erase the robot whose get_id() == id.
      }

      Robot* CommandCenter::find_robot(int id) const {
          // TODO: return a non-owning pointer to the match, or nullptr.
      }

      void CommandCenter::print_all_robots() const {
          // TODO: print report_status() for every owned robot.
      }

.. dropdown:: R6: Sensor Hierarchy
   :open:

   Create a ``Sensor`` base class with derived types:

   * ``ThermalSensor``, ``read()`` returns a temperature value
     (used to detect body heat).
   * ``GasSensor``, ``read()`` returns a gas concentration (ppm).
   * ``read()`` is a **virtual** method that returns different data
     per sensor type.
   * Sensors are shared among robots via ``std::shared_ptr``.

   **Step by step**

   1. Make ``Sensor`` an **abstract base class**: declare
      ``read()`` as a pure virtual method (``= 0``) returning
      ``double``, and give ``Sensor`` a ``virtual`` destructor.
   2. Store a ``location_`` string and expose it through a ``const``
      getter.
   3. ``ThermalSensor`` overrides ``read()`` to return a temperature
      near a stored baseline; ``GasSensor`` overrides ``read()`` to
      return a gas concentration in ppm. Each derived class forwards
      ``location`` to the ``Sensor`` base constructor.
   4. Always create sensors with ``std::make_shared`` so they can be
      shared (see R4).

   **Acceptance criteria**

   * ``Sensor`` cannot be instantiated directly (it is abstract).
   * Calling ``read()`` through a ``Sensor`` pointer dispatches to the
     correct derived implementation.
   * Each derived ``read()`` uses the ``override`` keyword.

   .. code-block:: cpp

      // sensor.hpp (illustrative skeleton)
      class Sensor {
       public:
          explicit Sensor(const std::string& location);
          virtual ~Sensor() = default;

          virtual double read() const = 0;   // pure virtual
          const std::string& get_location() const;

       private:
          std::string location_;
      };

      class ThermalSensor : public Sensor {
       public:
          ThermalSensor(const std::string& location, double baseline);
          double read() const override;

       private:
          double baseline_{36.5};
      };

      class GasSensor : public Sensor {
       public:
          GasSensor(const std::string& location, double baseline_ppm);
          double read() const override;

       private:
          double baseline_ppm_{0.0};
      };

      // sensor.cpp
      double ThermalSensor::read() const {
          // TODO: return a temperature near baseline_ (e.g. simulate a
          //       small variation around stored body-heat baseline).
      }

      double GasSensor::read() const {
          // TODO: return a gas concentration in ppm.
      }


Deliverables
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Item
     - Description
   * - Header files (``.hpp``)
     - One header per class (``robot.hpp``, ``ground_robot.hpp``,
       ``command_center.hpp``, ``sensor.hpp``, etc.).
   * - Source files (``.cpp``)
     - Corresponding implementations and ``main.cpp``.
   * - ``CMakeLists.txt``
     - Build configuration targeting C++17 or later.
   * - UML class diagram
     - Shows the full class hierarchy and relationships.
   * - Valgrind output
     - Demonstrates zero memory leaks (even though you use smart
       pointers, this confirms correct usage).


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - Category
     - Weight
     - Criteria
   * - OOP Design
     - 30 %
     - Proper class hierarchy, encapsulation, access specifiers,
       constructors with member initialization lists.
   * - Smart Pointer Usage
     - 25 %
     - Correct use of ``unique_ptr``, ``shared_ptr``, and
       ``weak_ptr``; no raw ``new`` / ``delete``.
   * - Polymorphism
     - 20 %
     - Virtual methods produce distinct behavior per derived class
       when called through base-class pointers.
   * - Code Quality
     - 15 %
     - ``const``-correctness, ``snake_case`` naming, uniform
       initialization, ``'\n'`` usage.
   * - Documentation
     - 10 %
     - Doxygen comments, UML diagram, inline comments for
       non-obvious logic.


Tips
----

.. admonition:: Design Before You Code
   :class: tip

   Sketch your UML class diagram first. Deciding which class owns
   which resource *before* writing code prevents painful refactors
   later.

.. admonition:: One Class at a Time
   :class: tip

   Implement and test the ``Robot`` base class before creating any
   derived classes. Then add one derived class, test polymorphism,
   and repeat.

.. admonition:: Smart Pointer Cheat Sheet
   :class: tip

   * **unique_ptr**, sole owner, cannot be copied, can be moved.
   * **shared_ptr**, reference-counted, multiple owners.
   * **weak_ptr**, observes a ``shared_ptr`` without affecting
     its reference count.
