.. _l9_requirements:

====================================================
L9 Requirements
====================================================

**Robotaxi Fleet Software: Requirements Specification**

This document states the requirements of the robotaxi fleet software that
we build in class. The :doc:`lecture page <l9_lecture>` says what
each kind of requirement is, and how the nouns and verbs of a requirement give
the classes and methods.


1. Introduction
====================================================

1.1 Purpose
----------------------------------------------------

The **requirements analysis** says **what** the software must do before the
design says **how**. This document lists what the software must do
(functional requirements), how well it must do it (non-functional
requirements), the limits on how it is built (technical constraints), and how
we check the result (success criteria and verification). Each requirement has
an ID, so the design, the code and the checks can name it.

1.2 Scope
----------------------------------------------------

The software models a ride company's fleet. It serves both kinds of vehicle: a
**robotaxi** drives itself and checks its sensors before it moves; a **taxi**
is driven by a person. Passengers ride the vehicles, and a fleet holds them.

- **In the course code** (``project/week9``): FR-3, FR-4, FR-5, FR-10
  (adding and removing) and FR-12.
- **Not in the course code**: ride requests and dispatch (FR-1, FR-2),
  status queries (FR-6), event logging (FR-7), continuous sensor reading
  (FR-8), route optimization (FR-9), listing available vehicles (part of
  FR-10) and driver management (FR-11). They stay in this document because a
  full product would need them.
- **Out of scope** of the product itself: payment and user authentication.

1.3 Definitions
----------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Term
     - Meaning
   * - Vehicle
     - Anything in the fleet that drives a route: a RoboTaxi or a Taxi. It has
       an id, a maximum speed, a speed, a color and a mileage, and it owns its
       sensors.
   * - RoboTaxi
     - A vehicle that drives itself. It drives only when it has a sensor.
   * - Taxi
     - A vehicle with a driver, known by the driver's name. A taxi with no
       driver does not move.
   * - Fleet
     - The company's set of vehicles. It shares them with the rest of the
       program and does not own them alone.
   * - Passenger
     - A person who rides one vehicle at a time and does not own it.
   * - Route
     - The waypoints of one trip, in order. Its length is the sum of the
       straight segments between them.
   * - Position
     - One point on the map, ``x`` east and ``y`` north.
   * - Sensor
     - A lidar, a camera or a radar, with an id and a range.

All distances are in meters (m) and all speeds in meters per second (m/s).

1.4 Conventions
----------------------------------------------------

- **shall** marks a requirement: the software must meet it.
- **Priority**: **Must** is needed for a first release; **Should** is wanted,
  and can wait for a later one.
- IDs: **FR-n** for a functional requirement, **NFR-n** for a non-functional
  requirement, **TC-n** for a technical constraint, **SC-n** for a success
  criterion.
- **Verified by** names the check that shows the requirement is met. A
  ``702run`` command runs the code of one slide; its output is the one on that
  slide.


2. Functional Requirements
====================================================

.. list-table::
   :header-rows: 1
   :widths: 8 32 8 26 26

   * - ID
     - Requirement
     - Priority
     - Status and design
     - Verified by
   * - FR-1
     - A Passenger shall be able to **request a ride** by giving a pickup and
       a dropoff location.
     - Must
     - Not in the course code.
     -
   * - FR-2
     - The Fleet shall **dispatch an available vehicle**, a RoboTaxi or a
       Taxi, to a ride request.
     - Must
     - Not in the course code.
     -
   * - FR-3
     - Each kind of vehicle shall **drive in its own way**: a RoboTaxi drives
       itself, and a Taxi is driven by its driver.
     - Must
     - In the code: ``Vehicle::drive`` is pure ``virtual``;
       ``RoboTaxi::drive`` and ``Taxi::drive`` override it.
     - Live Coding Step 4. ``702run week9_playground 82`` (The Whole Program)
       prints ``RoboTaxi: 2 sensors checked, drives 500 m`` and
       ``Taxi: Ana drives 500 m``.
   * - FR-4
     - Each RoboTaxi shall carry **one or more Sensors**. A RoboTaxi with no
       sensor shall not drive.
     - Must
     - In the code: a ``Vehicle`` owns its sensors through
       ``std::unique_ptr``; ``RoboTaxi::drive`` checks ``sensor_count()``
       first.
     - ``702run week9_appendix vii`` (RoboTaxi and Taxi) prints
       ``RoboTaxi: no sensor, stays parked``, then, with one sensor,
       ``RoboTaxi: 1 sensor checked, drives 500 m``.
   * - FR-5
     - A Vehicle shall **follow a Route** that it is given for one trip.
     - Must
     - In the code: ``Vehicle::drive(const Route&)``. The vehicle uses the
       route only during the call.
     - ``702run week9_playground 36`` (A Route for One Call) prints
       ``500 m at 10 m/s: 50 s``.
   * - FR-6
     - The software shall answer **status queries**: a vehicle's status and
       location, and the driver of a Taxi.
     - Should
     - Not in the course code.
     -
   * - FR-7
     - The software shall **log the key events** of a ride: ride requested,
       vehicle dispatched, route given, passenger boarded and left, trip
       ended.
     - Should
     - Not in the course code. ``Vehicle`` has a ``protected`` method,
       ``log_event``, that prints one event.
     -
   * - FR-8
     - A RoboTaxi shall **read its sensor data continuously** while it
       operates, to navigate and to find obstacles.
     - Must
     - Not in the course code: a ``Sensor`` holds its type and range, and
       reads nothing.
     -
   * - FR-9
     - The software shall **create Routes** with several waypoints and
       **optimize** them.
     - Should
     - A ``Route`` holds several waypoints and computes its length.
       Optimizing: not in the course code.
     -
   * - FR-10
     - The Fleet shall **add and remove vehicles**, and **list the available
       ones**.
     - Must
     - Adding and removing in the code: ``Fleet::add``, ``Fleet::remove``.
       Listing available vehicles: not in the course code.
     - Live Coding Step 2. ``702run week9_playground 28`` (The Vehicles
       Outlive the Fleet) prints ``2 2``, ``1 1`` and ``1 13.4``.
   * - FR-11
     - The software shall **manage the drivers** of Taxis: assigning and
       removing a driver.
     - Must
     - Not in the course code: a ``Taxi`` gets its driver's name when it is
       made.
     -
   * - FR-12
     - A Passenger shall **board and leave** a vehicle. Boarding shall not
       make the passenger an owner of the vehicle.
     - Must
     - In the code: ``Passenger::board``, ``Passenger::leave``; the passenger
       holds a ``std::weak_ptr<Vehicle>``.
     - Live Coding Step 1. ``702run week9_playground 24`` (Two Separate
       Lifetimes) prints ``1``, ``1`` and ``true``.


3. Non-Functional Requirements
====================================================

A non-functional requirement says how well the software works. The first four
can be checked in the course code. The others are targets for a full product:
they need a part, such as dispatch or sensor reading, that the course code does
not have, so nothing in the course measures them.

.. list-table::
   :header-rows: 1
   :widths: 9 16 45 30

   * - ID
     - Quality
     - Requirement
     - Verified by
   * - NFR-1
     - Extensibility
     - A new kind of vehicle, such as a RoboBus, shall need **no change** to
       ``Fleet`` or ``Passenger``.
     - ``702run week9_playground 83`` (Discussion: Add a RoboBus): a
       ``RoboBus`` joins a ``Fleet`` unchanged and prints
       ``RoboBus: 30 seats, drives 500 m``.
   * - NFR-2
     - Valid state
     - Every object shall keep its rule. A value that breaks one shall be
       rejected with ``std::invalid_argument`` and a message: a maximum speed
       that is not greater than 0, a speed outside 0 to the maximum speed, a
       negative distance added to the mileage, a negative sensor range, an
       empty passenger name, a null vehicle given to a ``Fleet``.
     - The constructors and methods that throw, in ``project/week9/common``.
   * - NFR-3
     - Memory safety
     - The software shall run with no report from AddressSanitizer and
       UndefinedBehaviorSanitizer: no leak, no use after free, no deletion
       through a pointer of the wrong type. The slides in ``undefined/`` show
       such a bug on purpose and run only when asked for by number.
     - ``week9_live``, ``week9_playground`` and ``week9_appendix`` are built
       with both sanitizers. After Live Coding Step 5, ``702run week9_live``
       runs with no report.
   * - NFR-4
     - Code quality
     - The code shall build with **no warning** under the course flags,
       ``-Wall -Wextra -pedantic-errors -Wshadow``.
     - ``702build`` on ``project/week9``.
   * - NFR-5
     - Performance
     - Reading one sensor shall take at most **50 ms**. Optimizing a route of
       up to 20 waypoints shall take at most **500 ms**.
     - Target only.
   * - NFR-6
     - Reliability
     - The software shall handle a failed sensor without stopping, using the
       other sensors. The mean time between failures in autonomous operation
       shall be more than **1000 hours**.
     - Target only.
   * - NFR-7
     - Safety
     - The software shall refuse an unsafe operation, such as boarding a
       vehicle that is moving, with a checked state in ``Vehicle``.
     - Target only.
   * - NFR-8
     - Availability
     - Dispatch and vehicle status shall be available **99.9%** of the
       operating hours.
     - Target only.
   * - NFR-9
     - Observability
     - Every ride request, dispatch, route given and passenger event shall be
       logged with its time, its location and the ids of the objects it
       involves.
     - Target only.


4. Technical Constraints
====================================================

.. list-table::
   :header-rows: 1
   :widths: 9 21 70

   * - ID
     - Constraint
     - Description
   * - TC-1
     - Language
     - The code shall be C++20 and use only the standard library. It shall
       build with CMake and g++, as set up in :doc:`Setup Before Class
       </lectures/lecture8/l8_setup>`.
   * - TC-2
     - Namespace
     - Every class shall be in the namespace ``fleet``: ``Vehicle``,
       ``RoboTaxi``, ``Taxi``, ``Fleet``, ``Passenger``, ``Route``,
       ``Position``, ``Sensor`` and ``SensorType``.
   * - TC-3
     - Encapsulation
     - Code outside ``Vehicle`` shall reach the sensors only through
       ``Vehicle``'s methods: ``add_sensor``, ``sensor_count`` and
       ``get_sensors``. ``get_sensors`` gives read-only access.
   * - TC-4
     - Composition
     - A ``Vehicle`` owns its ``Sensor``\ s: they are made and destroyed with
       it. A ``Route`` owns its ``Position``\ s, held by value.
   * - TC-5
     - Aggregation
     - A ``Fleet`` holds ``Vehicle``\ s that it does not own alone: a vehicle
       can exist without the fleet and outlive it.
   * - TC-6
     - Association
     - A ``Passenger`` refers to at most one ``Vehicle`` and does not own it.
       The vehicle can be destroyed while the passenger still exists.
   * - TC-7
     - Dependency
     - A ``Vehicle`` gets a ``Route`` for one call of ``drive`` and keeps no
       reference to it.
   * - TC-8
     - Driver
     - A ``Taxi`` holds its driver's name. An empty name means no driver, and
       then the taxi does not move.
   * - TC-9
     - Types
     - The class diagram uses the C++ types of the code (``double``,
       ``string``, ``shared_ptr<Vehicle>``), so a box reads like its class.
   * - TC-10
     - Errors
     - A broken rule shall throw ``std::invalid_argument`` with a message that
       says which rule.


5. Implementation Guidance
====================================================

**C++ conventions.** Every class of the course code follows these:

- Each class is declared in a header file that starts with ``#pragma once``.
- Constructors are defined in the class, in the header. Every other method is
  declared in the class and defined in the source file.
- Names are ``snake_case``; a data member ends with an underscore:
  ``max_speed_``, ``sensors_``.
- Data members are ``private``. Only ``log_event`` in ``Vehicle`` is
  ``protected``.
- Composition uses ``std::unique_ptr`` (``Vehicle`` owns its sensors).
  Aggregation uses ``std::shared_ptr`` (``Fleet``). Association uses
  ``std::weak_ptr`` (``Passenger``). A dependency is a ``const`` reference
  parameter (``drive(const Route&)``).
- The abstract method is marked ``= 0``, every override is marked
  ``override``, and ``RoboTaxi`` and ``Taxi`` are ``final``.
- ``Vehicle``, the polymorphic base class, has a ``virtual`` destructor.
- The ``get_`` methods, ``sensor_count`` and ``size`` are ``[[nodiscard]]``,
  ``const`` and ``noexcept``.
- Files and methods are documented in Doxygen format: ``@file``, ``@brief``,
  ``@param``, ``@return``, ``@throw``.

**Namespace structure.**

.. code-block:: cpp

   namespace fleet {

   enum class SensorType;  // lidar, camera, radar
   class Sensor;           // id, type, range
   struct Position;        // x, y in m
   class Route;            // waypoints of one trip
   class Vehicle;          // abstract base class
   class RoboTaxi;         // drives itself, final
   class Taxi;             // has a driver, final
   class Fleet;            // shares its vehicles
   class Passenger;        // rides one vehicle, owns none

   }  // namespace fleet

**Example usage.** This program uses the classes of ``project/week9/common``:

.. code-block:: cpp

   #include <iostream>
   #include <memory>

   #include "fleet.hpp"
   #include "passenger.hpp"
   #include "position.hpp"
   #include "robotaxi.hpp"
   #include "route.hpp"
   #include "taxi.hpp"

   int main() {
     fleet::Route trip;  // 500 m: (0, 0) to (300, 400)
     trip.add(fleet::Position{0.0, 0.0});
     trip.add(fleet::Position{300.0, 400.0});

     auto robotaxi{std::make_shared<fleet::RoboTaxi>(13.4)};
     robotaxi->add_sensor(fleet::SensorType::lidar, 100.0);
     auto taxi{std::make_shared<fleet::Taxi>(13.4, "Ana")};

     fleet::Fleet company;
     company.add(robotaxi);
     company.add(taxi);
     std::cout << company.size() << " vehicles\n";

     fleet::Passenger maya{"Maya"};
     maya.board(robotaxi);
     robotaxi->drive(trip);
     maya.leave();
     taxi->drive(trip);
   }

Built with the course flags and both sanitizers, it compiles with no warning
and prints:

.. code-block:: text

   2 vehicles
   RoboTaxi: 1 sensor checked, drives 500 m
   Taxi: Ana drives 500 m


6. Success Criteria
====================================================

.. list-table::
   :header-rows: 1
   :widths: 9 26 65

   * - ID
     - Criterion
     - Measurable outcome
   * - SC-1
     - Polymorphic driving
     - One loop over ``Vehicle``\ s drives a RoboTaxi and a Taxi, and each
       prints its own line (FR-3), with no change to ``Fleet``.
   * - SC-2
     - Sensors
     - A RoboTaxi with no sensor stays parked, and with one sensor it drives
       (FR-4).
   * - SC-3
     - Routes
     - A vehicle drives two routes, 500 m and 200 m, given one per call
       (FR-5).
   * - SC-4
     - Fleet
     - Adding two vehicles gives a size of 2; removing one by its id gives 1;
       a vehicle lives on after the fleet is destroyed (FR-10).
   * - SC-5
     - Passengers
     - Boarding does not change the vehicle's owner count, and the vehicle can
       be destroyed while the passenger exists (FR-12).
   * - SC-6
     - Extensibility
     - A RoboBus joins a Fleet with no change to ``Fleet`` (NFR-1).
   * - SC-7
     - Quality
     - Every rule of NFR-2 throws; the sanitizers report nothing (NFR-3); the
       build has no warning (NFR-4).
   * - SC-8
     - Constraints
     - The code meets TC-1 to TC-10 and the conventions of section 5.


7. Assumptions
====================================================

- A Fleet holds zero or more vehicles of both kinds, and vehicles can be added
  and removed at any time.
- A Passenger rides zero or one vehicle at a time.
- A Vehicle owns zero or more Sensors. A RoboTaxi needs at least one to drive.
- A Route holds zero or more Positions, in order.
- A Taxi has zero or one driver.
- Sensors are simulated: they hold their type and range, and no data.
- Speeds and distances are plain numbers in m/s and m; time is computed from
  them, not measured.


8. Verification Approach
====================================================

- **Live Coding outputs**: each step prints a block, and the slide shows the
  expected lines (FR-3, FR-5, FR-10, FR-12).
- **Slide programs**: ``702run week9_playground`` and
  ``702run week9_appendix`` run the code of every slide and print its output.
- **Compiler checks**: ``override`` catches a method that does not override,
  ``final`` stops a class from deriving, an abstract ``Vehicle`` cannot be
  made, and the course flags turn on the warnings (NFR-4).
- **Sanitizers**: AddressSanitizer and UndefinedBehaviorSanitizer in
  ``week9_live``, ``week9_playground`` and ``week9_appendix`` (NFR-3).
- **Negative checks**: each rule of NFR-2 is called with a value that breaks
  it, and the call throws.
- **Not in the course**: unit, performance, reliability and availability tests
  for the targets NFR-5 to NFR-9.
