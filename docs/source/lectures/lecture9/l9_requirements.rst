.. _l9_requirements:

====================================================
L9 Requirements
====================================================

**Robotaxi Fleet Software: Software Requirements Specification**

This document states the requirements of the robotaxi fleet software that
we build in class. The :doc:`lecture page <l9_lecture>` says what
each kind of requirement is, and how the nouns and verbs of a requirement give
the classes and methods.


1. Introduction
====================================================

1.1 Purpose
----------------------------------------------------

This specification states what the robotaxi fleet software shall do and how
well it shall do it, so that the design, the code and the tests can be checked
against one list. It is written for the developers who build the software and
for the reviewers who accept it.

1.2 Scope
----------------------------------------------------

The software manages a ride company's fleet. The fleet has two kinds of
vehicle: a **robotaxi**, which drives itself using its sensors, and a
**taxi**, which a person drives. Passengers request rides, board a vehicle and
leave it.

Payment, user accounts and user authentication are outside the scope of this
specification.

Section 8 traces each requirement to the course code: which ones the code of
``project/week9`` meets, and the check that shows it.

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
     - A vehicle that drives itself.
   * - Taxi
     - A vehicle driven by a person, its driver.
   * - Fleet
     - The company's set of vehicles.
   * - Passenger
     - A person who rides a vehicle.
   * - Route
     - The waypoints of one trip, in order.
   * - Waypoint
     - One point of a route, given as a Position.
   * - Position
     - One point on the map, ``x`` east and ``y`` north, in meters.
   * - Sensor
     - A lidar, a camera or a radar mounted on a vehicle, with an id and a
       range.
   * - Available vehicle
     - A vehicle of the fleet that is not on a trip.

All distances are in meters (m) and all speeds in meters per second (m/s).

1.4 How to Read a Requirement
----------------------------------------------------

Each requirement has:

- an **ID**: FR for functional, NFR for non-functional, TC for a technical
  constraint. A requirement split into parts keeps its number: FR-10.1,
  FR-10.2.
- a **statement** with **shall**. It names one behavior, and a test can show
  whether the software has it.
- a **rationale**: why the requirement exists.
- a **priority**: **Must** is needed for the first release; **Should** is
  wanted, and can wait for a later release.
- a **verification method**: **Test** (run the software with set inputs and
  compare the output with the expected one), **Demonstration** (run it and
  watch it work), **Inspection** (read the code or the design) or
  **Analysis** (compute or estimate from a model).
- an **acceptance criterion**: the result that passes the check.


2. Functional Requirements
====================================================

2.1 Ride Requests and Dispatch
----------------------------------------------------

**FR-1. Request a ride**

The system shall accept a ride request from a Passenger that gives a pickup
location and a dropoff location.

:Rationale: A ride starts from a passenger's request.
:Priority: Must
:Verification: Test
:Acceptance: A request with both locations is accepted. A request with a
   missing location is rejected, and the passenger is told why.

**FR-2. Dispatch a vehicle**

When the system accepts a ride request, the Fleet shall assign one available
vehicle, a RoboTaxi or a Taxi, to it.

:Rationale: Every accepted request needs a vehicle, of either kind.
:Priority: Must
:Verification: Test
:Acceptance: After the assignment, the request has exactly one vehicle, and
   that vehicle is no longer available.

2.2 Driving
----------------------------------------------------

**FR-3. Vehicle-specific driving**

When a vehicle is given a route to drive, the system shall run the driving
procedure of that vehicle's kind: a RoboTaxi drives itself, and a Taxi is
driven by its driver.

:Rationale: The two kinds drive differently, and code that drives a vehicle
   must not need to know which kind it has.
:Priority: Must
:Verification: Test
:Acceptance: One call that drives a list of vehicles makes each vehicle run
   its own procedure: a RoboTaxi reports its sensors and the distance; a Taxi
   reports its driver and the distance.

**FR-4.1. Sensors of a RoboTaxi**

Each RoboTaxi shall be able to carry one or more Sensors, of the types lidar,
camera and radar.

:Rationale: A robotaxi sees its surroundings only through its sensors.
:Priority: Must
:Verification: Test
:Acceptance: Mounting a sensor raises the vehicle's sensor count by 1, and
   gives the new sensor the next id: 1, then 2.

**FR-4.2. No sensor, no driving**

A RoboTaxi with no sensor shall not move when it is given a route.

:Rationale: Driving without any sensor is unsafe.
:Priority: Must
:Verification: Test
:Acceptance: A RoboTaxi with 0 sensors reports that it stays parked. After one
   sensor is mounted, the same RoboTaxi drives the route.

**FR-5. Follow a route**

A vehicle shall drive the route it is given for a trip, from the first
waypoint to the last, in order.

:Rationale: A trip is a sequence of waypoints from the pickup to the dropoff.
:Priority: Must
:Verification: Test
:Acceptance: For a route from (0, 0) to (300, 400), the vehicle drives 500 m.
   The vehicle keeps no reference to the route after the trip.

**FR-5.1. Taxi without a driver**

A Taxi with no driver shall not move when it is given a route.

:Rationale: A taxi needs a person to drive it.
:Priority: Must
:Verification: Test
:Acceptance: A Taxi made with an empty driver name reports that it stays
   parked.

2.3 Status and Logging
----------------------------------------------------

**FR-6. Status queries**

The system shall answer a query for a vehicle's status and location, and for
the driver of a Taxi.

:Rationale: Dispatchers and passengers need to know where vehicles are and
   who drives them.
:Priority: Should
:Verification: Test
:Acceptance: A query returns the current status, the current location and,
   for a Taxi, the driver.

**FR-7. Event log**

The system shall log each key event of a ride: ride requested, vehicle
dispatched, route given, passenger boarded, passenger left, trip ended.

:Rationale: The log is the record used to investigate a ride after the fact.
:Priority: Should
:Verification: Test
:Acceptance: An end-to-end ride produces one log entry for each of the six
   events, in order.

2.4 Sensors
----------------------------------------------------

**FR-8. Continuous sensor reading**

While a RoboTaxi operates, the system shall read the data of each of its
sensors continuously, to navigate and to detect obstacles.

:Rationale: A robotaxi navigates and avoids obstacles from current sensor
   data.
:Priority: Must
:Verification: Test
:Acceptance: During operation, every sensor of the RoboTaxi delivers new
   readings. A sensor that stops delivering is detected (see NFR-6).

2.5 Routes
----------------------------------------------------

**FR-9.1. Build a route**

The system shall let a route be built by adding waypoints, in order.

:Rationale: A trip has a pickup, a dropoff and stops between them.
:Priority: Must
:Verification: Test
:Acceptance: A route with waypoints added in an order keeps that order.

**FR-9.2. Route length**

The system shall compute a route's length as the sum of the straight segments
between consecutive waypoints.

:Rationale: The length is needed to plan the trip and to update the vehicle's
   mileage.
:Priority: Must
:Verification: Test
:Acceptance: A route through (0, 0), (300, 400) and (300, 0) has a length of
   900 m.

**FR-9.3. Optimize a route**

The system shall reorder the waypoints between the first and the last one to
shorten a route.

:Rationale: Shorter routes save time and energy.
:Priority: Should
:Verification: Test
:Acceptance: The optimized route is never longer than the original, and keeps
   the same first and last waypoints.

2.6 Fleet
----------------------------------------------------

**FR-10.1. Add a vehicle**

The Fleet shall add a vehicle of either kind.

:Rationale: The company adds vehicles to its fleet.
:Priority: Must
:Verification: Test
:Acceptance: Adding two vehicles gives a fleet size of 2.

**FR-10.2. Reject a missing vehicle**

The Fleet shall reject an attempt to add a null vehicle, and shall stay
unchanged.

:Rationale: A fleet entry that holds no vehicle would fail later, far from the
   mistake.
:Priority: Must
:Verification: Test
:Acceptance: Adding a null vehicle throws ``std::invalid_argument``, and the
   fleet size does not change.

**FR-10.3. No duplicates**

Adding a vehicle that is already in the Fleet shall leave the Fleet unchanged.

:Rationale: A vehicle counted twice would be dispatched twice.
:Priority: Must
:Verification: Test
:Acceptance: Adding the same vehicle twice gives a fleet size of 1.

**FR-10.4. Remove a vehicle**

The Fleet shall remove the vehicle with a given id, and shall report whether
it found one.

:Rationale: Vehicles leave the fleet for service or sale.
:Priority: Must
:Verification: Test
:Acceptance: Removing an id in the fleet reduces the size by 1 and reports
   success. Removing an unknown id reports failure and changes nothing.

**FR-10.5. The fleet does not own its vehicles**

A vehicle removed from the Fleet, or whose Fleet is destroyed, shall stay
usable by the rest of the program.

:Rationale: A vehicle can move between fleets, and other parts of the
   program may still use it.
:Priority: Must
:Verification: Test
:Acceptance: After the fleet is destroyed, a vehicle it held still answers
   ``get_max_speed()``.

**FR-10.6. List available vehicles**

The Fleet shall list its available vehicles.

:Rationale: Dispatch (FR-2) picks from this list.
:Priority: Must
:Verification: Test
:Acceptance: The list holds every vehicle of the fleet that is not on a trip,
   and no other.

2.7 Drivers
----------------------------------------------------

**FR-11. Manage drivers**

The system shall let a driver be assigned to a Taxi and removed from it.

:Rationale: Drivers change between shifts.
:Priority: Must
:Verification: Test
:Acceptance: After an assignment, the Taxi drives with that driver. After the
   removal, it does not move (FR-5.1).

2.8 Passengers
----------------------------------------------------

**FR-12.1. Board a vehicle**

A Passenger shall be able to board one vehicle.

:Rationale: A ride needs the passenger in the vehicle.
:Priority: Must
:Verification: Test
:Acceptance: After boarding, the passenger refers to that vehicle.

**FR-12.2. Leave a vehicle**

A Passenger shall be able to leave the vehicle they boarded.

:Rationale: A ride ends when the passenger leaves.
:Priority: Must
:Verification: Test
:Acceptance: After leaving, the passenger refers to no vehicle.

**FR-12.3. A passenger does not own the vehicle**

Boarding shall not keep a vehicle alive: a vehicle shall be destroyed when its
last owner lets it go, even while a passenger still refers to it.

:Rationale: A passenger's ride must not stop the company from retiring a
   vehicle.
:Priority: Must
:Verification: Test
:Acceptance: Boarding leaves the vehicle's owner count unchanged (1). After
   the only owner lets go, the vehicle is destroyed while the passenger
   exists.

**FR-12.4. A passenger has a name**

The system shall reject a Passenger with an empty name.

:Rationale: A ride is booked under a name.
:Priority: Must
:Verification: Test
:Acceptance: Creating a passenger with an empty name throws
   ``std::invalid_argument``.


3. Non-Functional Requirements
====================================================

**NFR-1. Extensibility**

Adding a new kind of vehicle shall require no change to the source code of
``Fleet`` or ``Passenger``.

:Rationale: The company will add kinds of vehicle, such as a robotic bus.
:Priority: Must
:Verification: Demonstration
:Acceptance: A new vehicle kind, written in its own files, joins a Fleet and is
   boarded by a Passenger, with ``fleet.hpp``, ``fleet.cpp``,
   ``passenger.hpp`` and ``passenger.cpp`` unchanged.

**NFR-2. Valid state**

Every object shall reject a value that breaks its rule, with
``std::invalid_argument`` and a message that names the rule, and shall stay
unchanged. The rules are:

- NFR-2.1: a vehicle's maximum speed is greater than 0 m/s;
- NFR-2.2: a vehicle's speed is from 0 to its maximum speed;
- NFR-2.3: a distance added to a vehicle's mileage is at least 0 m;
- NFR-2.4: a sensor's range is at least 0 m;
- NFR-2.5: a passenger's name is not empty (FR-12.4);
- NFR-2.6: a fleet holds no null vehicle (FR-10.2).

:Rationale: An object that keeps its rule never needs to be checked again by
   the code that uses it.
:Priority: Must
:Verification: Test
:Acceptance: For each rule, one value just outside it throws, and one value
   just inside it is accepted.

**NFR-3. Memory safety**

The software shall have no memory leak, no use of freed memory, and no
deletion through a pointer of the wrong type.

:Rationale: These errors corrupt data silently and are hard to find later.
:Priority: Must
:Verification: Test
:Acceptance: All programs, built with AddressSanitizer and
   UndefinedBehaviorSanitizer, run with no report.

**NFR-4. Clean build**

The code shall compile with no warning under ``-Wall -Wextra
-pedantic-errors -Wshadow``.

:Rationale: Warnings point at likely bugs; a clean build keeps new ones
   visible.
:Priority: Must
:Verification: Inspection
:Acceptance: A full build prints no warning.

**NFR-5. Performance**

Reading one sensor shall take at most 50 ms, and optimizing a route of up to
20 waypoints shall take at most 500 ms.

:Rationale: Driving decisions need current data, and dispatch must not wait on
   route planning.
:Priority: Must
:Verification: Test
:Acceptance: Measured on the target computer, every sensor reading and every
   optimization of a 20-waypoint route meets its limit.

**NFR-6. Reliability**

When one sensor fails, a RoboTaxi shall keep operating on its other sensors.
The mean time between failures in autonomous operation shall be more than
1000 hours.

:Rationale: One failed sensor must not stop a vehicle in traffic.
:Priority: Must
:Verification: Test (sensor failure), Analysis (mean time between failures)
:Acceptance: With one sensor disabled, the RoboTaxi still drives, and the
   failure is logged.

**NFR-7. Safety**

The system shall refuse to let a passenger board a vehicle that is moving.

:Rationale: Boarding a moving vehicle can injure the passenger.
:Priority: Must
:Verification: Test
:Acceptance: A boarding attempt on a vehicle with a speed above 0 m/s is
   rejected, and the passenger stays off the vehicle.

**NFR-8. Availability**

Dispatch and status queries shall be available 99.9% of the operating hours.

:Rationale: Passengers cannot book a ride while dispatch is down.
:Priority: Should
:Verification: Analysis
:Acceptance: The measured downtime of a month of operation is at most 0.1% of
   its operating hours.

**NFR-9. Observability**

Each logged event (FR-7) shall carry its time, its location and the ids of the
objects it involves.

:Rationale: An event without these cannot be traced back to a vehicle and a
   ride.
:Priority: Should
:Verification: Inspection
:Acceptance: Every entry of an end-to-end ride's log has the three fields.


4. Technical Constraints
====================================================

.. list-table::
   :header-rows: 1
   :widths: 9 21 70

   * - ID
     - Constraint
     - Statement
   * - TC-1
     - Language
     - The software shall be written in C++20, with only the standard
       library, and built with CMake and g++, as set up in
       :doc:`Setup Before Class </lectures/lecture8/l8_setup>`.
   * - TC-2
     - Namespace
     - Every class shall be in the namespace ``fleet``.
   * - TC-3
     - Encapsulation
     - Code outside ``Vehicle`` shall reach the sensors only through
       ``Vehicle``'s methods ``add_sensor``, ``sensor_count`` and
       ``get_sensors``. ``get_sensors`` shall give read-only access.
   * - TC-4
     - Composition
     - A ``Vehicle`` shall own its ``Sensor``\ s, so they are made and
       destroyed with it. A ``Route`` shall hold its ``Position``\ s by
       value.
   * - TC-5
     - Aggregation
     - A ``Fleet`` shall share its vehicles with the rest of the program, not
       own them alone (FR-10.5).
   * - TC-6
     - Association
     - A ``Passenger`` shall refer to at most one ``Vehicle``, without owning
       it (FR-12.3).
   * - TC-7
     - Dependency
     - A ``Vehicle`` shall receive a ``Route`` for one call of ``drive`` and
       keep no reference to it (FR-5).
   * - TC-8
     - Errors
     - A broken rule shall be reported with ``std::invalid_argument`` and a
       message that names the rule (NFR-2).
   * - TC-9
     - Design types
     - The class diagram shall use the C++ types of the code (``double``,
       ``string``, ``shared_ptr<Vehicle>``).


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

The first release is accepted when:

- **SC-1**: every **Must** requirement of sections 2 and 3 passes its
  acceptance criterion;
- **SC-2**: the code meets every technical constraint of section 4;
- **SC-3**: the whole test run is repeated on the release build, with no
  failure.


7. Assumptions
====================================================

- A Fleet holds zero or more vehicles of both kinds.
- A Passenger rides zero or one vehicle at a time.
- A Vehicle carries zero or more Sensors; a RoboTaxi needs at least one to
  drive.
- A Taxi has zero or one driver.
- A Route holds zero or more waypoints.
- Sensor readings are simulated: a timing in NFR-5 refers to the software on
  the target computer, not to the sensor hardware.


8. Traceability to the Course Code
====================================================

The course code, ``project/week9``, meets part of this specification. A
``702run`` command runs the code of one slide; its output is the one on that
slide.

.. list-table::
   :header-rows: 1
   :widths: 11 34 55

   * - ID
     - In the course code
     - Evidence
   * - FR-1, FR-2
     - No.
     -
   * - FR-3
     - Yes: ``Vehicle::drive`` is pure ``virtual``; ``RoboTaxi::drive`` and
       ``Taxi::drive`` override it.
     - Live Coding Step 4. ``702run week9_playground 87`` (The Whole
       Program) prints ``RoboTaxi: 2 sensors checked, drives 500 m`` and
       ``Taxi: Ana drives 500 m``.
   * - FR-4.1, FR-4.2
     - Yes: ``Vehicle::add_sensor``; ``RoboTaxi::drive`` checks
       ``sensor_count()`` first.
     - ``702run week9_appendix vii`` (RoboTaxi and Taxi) prints
       ``RoboTaxi: no sensor, stays parked``, then ``RoboTaxi: 1 sensor
       checked, drives 500 m``.
   * - FR-5
     - Yes: ``Vehicle::drive(const Route&)``.
     - ``702run week9_playground 40`` (A Route for One Call) prints
       ``500 m at 10 m/s: 50 s``.
   * - FR-5.1
     - Yes: ``Taxi::drive`` checks for an empty driver name.
     - Measured: a Taxi made with an empty name prints
       ``Taxi: no driver, stays parked``.
   * - FR-6, FR-7, FR-8
     - No. ``Vehicle::log_event`` prints one event, without a time or a
       location.
     -
   * - FR-9.1, FR-9.2
     - Yes: ``Route::add``, ``Route::length``.
     - The Composition section of the lecture: a route of 500 m and a longer
       one of 900 m.
   * - FR-9.3
     - No.
     -
   * - FR-10.1 to FR-10.5
     - Yes: ``Fleet::add``, ``Fleet::remove``, ``Fleet::size``.
     - Live Coding Step 2. ``702run week9_playground 30`` (The Vehicles
       Outlive the Fleet) prints ``2 2``, ``1 1`` and ``1 13.4``. Measured:
       adding the same vehicle twice gives a size of 1, and removing an
       unknown id returns ``false``.
   * - FR-10.6
     - No.
     -
   * - FR-11
     - No: a Taxi gets its driver's name when it is made.
     -
   * - FR-12.1 to FR-12.4
     - Yes: ``Passenger::board``, ``Passenger::leave``; the passenger holds a
       ``std::weak_ptr<Vehicle>``.
     - Live Coding Step 1. ``702run week9_playground 25`` (Two Separate
       Lifetimes) prints ``1``, ``1`` and ``true``.
   * - NFR-1
     - Yes, for ``Fleet``: a new kind joins it unchanged.
     - ``702run week9_playground 88`` (Discussion: Add a RoboBus) prints
       ``RoboBus: 30 seats, drives 500 m``.
   * - NFR-2
     - Yes: every rule throws ``std::invalid_argument``.
     - The constructors and methods of ``project/week9/common``.
   * - NFR-3
     - Yes, apart from the slides in ``undefined/``, which show such a bug on
       purpose and run only when asked for by number.
     - ``week9_live``, ``week9_playground`` and ``week9_appendix`` are built
       with both sanitizers. After Live Coding Step 5, ``live9`` runs
       ``week9_live`` with no report.
   * - NFR-4
     - Yes.
     - ``702build`` on ``project/week9``.
   * - NFR-5 to NFR-9
     - No: they need dispatch, sensor reading or logging, which the course
       code does not have.
     -
   * - TC-1 to TC-9
     - Yes.
     - Inspection of ``project/week9/common``.
