.. _l9_requirements:

====================================================
L9 Requirements
====================================================

The requirements of the robotaxi program of Lecture 8 and Lecture 9, shortened
from last year's design of this system. The :doc:`lecture page <l9_lecture>`
says what a requirement is and how its nouns and verbs give the classes and
methods.


Today's Requirements
====================================================

Today's code uses five of the twelve functional requirements.

.. list-table::
   :header-rows: 1
   :widths: 12 50 38

   * - ID
     - The program shall
     - In the code
   * - FR-3
     - let each kind of vehicle drive in its own way.
     - ``drive``, one per class
   * - FR-4
     - give each RoboTaxi one or more Sensors.
     - ``Vehicle`` owns its sensors (L8)
   * - FR-5
     - let a Vehicle follow a Route.
     - ``drive(const Route&)``
   * - FR-10
     - let a Fleet add and remove vehicles.
     - ``Fleet::add``, ``remove``
   * - FR-12
     - let a Passenger board and leave a vehicle.
     - ``Passenger::board``, ``leave``

- Each line is shortened from last year's text. Requesting and dispatching a
  ride (FR-1, FR-2), optimizing routes (FR-9) and managing drivers (FR-11) are
  not in today's code.


All Twelve Requirements
====================================================

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
