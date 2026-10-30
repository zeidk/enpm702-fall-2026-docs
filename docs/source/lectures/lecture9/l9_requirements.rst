.. _l9_requirements:

====================================================
L9 Requirements
====================================================

**Robotaxi Fleet Software: Requirements Specification**

This document states the requirements of the robotaxi fleet software that
Lecture 8 and Lecture 9 build. The :doc:`lecture page <l9_lecture>` says what
each kind of requirement is, and how the nouns and verbs of a requirement give
the classes and methods.


1. Introduction
====================================================

1.1 Purpose
----------------------------------------------------

The document lists what the software must do (functional requirements), how
well it must do it (non-functional requirements), the limits on how it is
built (constraints), and how we check the result (success criteria). Each
requirement has an ID, so the design, the code and the checks can name it.

1.2 Scope
----------------------------------------------------

The software models a company's fleet of vehicles. A **robotaxi** drives
itself and checks its sensors before it moves; a **taxi** is driven by a
driver. Passengers ride the vehicles, and a fleet holds them.

- **In the course code** (``project/week9``): FR-3, FR-4, FR-5, FR-10 and
  FR-12.
- **Not in the course code**: ride requests and dispatch (FR-1, FR-2), status
  queries (FR-6), event logging (FR-7), continuous sensor reading (FR-8),
  route optimization (FR-9), listing available vehicles (part of FR-10) and
  driver management (FR-11). They stay in the document because a later
  version of the software would need them.

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
     - A vehicle with a driver, known by the driver's name.
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
- IDs: **FR-n** for a functional requirement, **NFR-n** for a non-functional
  requirement, **CON-n** for a constraint, **SC-n** for a success criterion.
- **Verified by** names the check that shows the requirement is met. A
  ``702run`` command runs the code of one slide; its output is the one on that
  slide.


2. Functional Requirements
====================================================

.. list-table::
   :header-rows: 1
   :widths: 9 33 30 28

   * - ID
     - Requirement
     - Status and design
     - Verified by
   * - FR-1
     - A Passenger shall be able to request a ride by giving a pickup and a
       dropoff location.
     - Not in the course code.
     -
   * - FR-2
     - The Fleet shall dispatch an available vehicle, a RoboTaxi or a Taxi, to
       a ride request.
     - Not in the course code.
     -
   * - FR-3
     - Each kind of vehicle shall drive in its own way: a RoboTaxi drives
       itself, and a Taxi is driven by its driver.
     - In the code: ``Vehicle::drive`` is pure ``virtual``;
       ``RoboTaxi::drive`` and ``Taxi::drive`` override it.
     - Live Coding Step 4. ``702run week9_playground 83`` (The Whole Program)
       prints ``RoboTaxi: 2 sensors checked, drives 500 m`` and
       ``Taxi: Ana drives 500 m``.
   * - FR-4
     - Each RoboTaxi shall carry one or more Sensors. A RoboTaxi with no
       sensor shall not drive.
     - In the code: a ``Vehicle`` owns its sensors through
       ``std::unique_ptr`` (L8); ``RoboTaxi::drive`` checks
       ``sensor_count()`` first.
     - ``702run week9_appendix vii`` (RoboTaxi and Taxi) prints
       ``RoboTaxi: no sensor, stays parked``, then, with one sensor,
       ``RoboTaxi: 1 sensor checked, drives 500 m``.
   * - FR-5
     - A Vehicle shall follow a Route that it is given for one trip.
     - In the code: ``Vehicle::drive(const Route&)``. The vehicle uses the
       route only during the call.
     - ``702run week9_playground 37`` (A Route for One Call) prints
       ``500 m at 10 m/s: 50 s``.
   * - FR-6
     - The software shall answer status queries: a vehicle's status and
       location, and the driver of a Taxi.
     - Not in the course code.
     -
   * - FR-7
     - The software shall log the key events of a ride, from the request to
       the end of the trip.
     - Not in the course code.
     -
   * - FR-8
     - A RoboTaxi shall read its sensor data continuously while it operates.
     - Not in the course code.
     -
   * - FR-9
     - The software shall create Routes with several waypoints and optimize
       them.
     - Not in the course code.
     -
   * - FR-10
     - The Fleet shall add and remove vehicles, and list the available ones.
     - Adding and removing in the code: ``Fleet::add``, ``Fleet::remove``.
       Listing available vehicles: not in the course code.
     - Live Coding Step 2. ``702run week9_playground 29`` (The Vehicles
       Outlive the Fleet) prints ``2 2``, ``1 1`` and ``1 13.4``.
   * - FR-11
     - The software shall manage the drivers of Taxis: assigning and removing
       a driver.
     - Not in the course code.
     -
   * - FR-12
     - A Passenger shall board and leave a vehicle. Boarding shall not make
       the passenger an owner of the vehicle.
     - In the code: ``Passenger::board``, ``Passenger::leave``; the passenger
       holds a ``std::weak_ptr<Vehicle>``.
     - Live Coding Step 1. ``702run week9_playground 25`` (Two Separate
       Lifetimes) prints ``1``, ``1`` and ``true``.


3. Non-Functional Requirements
====================================================

.. list-table::
   :header-rows: 1
   :widths: 10 22 40 28

   * - ID
     - Quality
     - Requirement
     - Verified by
   * - NFR-1
     - Extensibility
     - A new kind of vehicle shall need no change to ``Fleet`` or
       ``Passenger``.
     - ``702run week9_playground 84`` (Discussion: Add a RoboBus): a
       ``RoboBus`` joins a ``Fleet`` unchanged and prints
       ``RoboBus: 30 seats, drives 500 m``.
   * - NFR-2
     - Valid state
     - Every object shall keep its rule. A value that breaks one shall be
       rejected with ``std::invalid_argument``: a maximum speed that is not
       greater than 0, a speed outside 0 to the maximum speed, a negative
       distance added to the mileage, a negative sensor range, an empty
       passenger name, a null vehicle given to a ``Fleet``.
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
     - The code shall build with no warning under the course flags,
       ``-Wall -Wextra -pedantic-errors -Wshadow``.
     - ``702build`` on ``project/week9``.


4. Constraints
====================================================

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - ID
     - Constraint
   * - CON-1
     - The code shall be C++20 and use only the standard library.
   * - CON-2
     - The code shall build with CMake and g++, as set up in
       :doc:`Setup Before Class </lectures/lecture8/l8_setup>`.
   * - CON-3
     - Every class shall be in the namespace ``fleet``.
   * - CON-4
     - A class shall be declared in a header file. Its constructors shall be
       defined in the class; every other method shall be defined in the source
       file.
   * - CON-5
     - Memory on the heap shall be owned through ``std::unique_ptr`` or
       ``std::shared_ptr``. The code shall not use ``new`` or ``delete``.


5. Success Criteria
====================================================

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - ID
     - Criterion
   * - SC-1
     - Every requirement in the course code (FR-3, FR-4, FR-5, FR-10, FR-12)
       passes the check in its **Verified by** column, with the output shown
       there.
   * - SC-2
     - NFR-1 to NFR-4 hold: a new kind of vehicle needs no change to
       ``Fleet``, every rule is checked, the sanitizers report nothing, and the
       build has no warning.
   * - SC-3
     - The code meets CON-1 to CON-5.
