.. _l9_design:

====================================================
L9 Design
====================================================

**Robotaxi Fleet Software: Design**

This document says how the robotaxi fleet software meets the
:doc:`L9 Requirements <l9_requirements>`: the requirements say **what** the
software shall do, and the design says **how**. It explains the class diagram
of the program, one class and one relationship at a time, and the decisions
behind it. The notation (``+``, ``-``, ``#``, the lines and the numbers at
their ends) is in the :doc:`lecture page <l9_lecture>`: Reading a Class Box,
Five Relationships and Multiplicity.

Every class described here is in ``project/week9/common``, with the same
names.


1. Class Diagram
====================================================

.. figure:: /_static/images/l9/model_full_members.png
   :alt: A UML class diagram of the robotaxi program with nine boxes, each listing its data members and methods, and the line ends also name the data member that holds the class at that end; every box and line is black. In the middle, Vehicle, its name in italics, with the data members minus id_ : int, the underlined minus next_id_ : int, minus max_speed_ : double, minus speed_ : double, minus color_ : string, minus mileage_ : double and minus sensors_ : vector of unique_ptr of Sensor, and the methods plus Vehicle(double, const string& = "white"), plus Vehicle(double, double), plus get_id() : int, plus get_color() : const string&, plus get_max_speed() : double, plus get_speed() : double, plus set_speed(double) : void, plus get_mileage() : double, plus add_mileage(double) : void, plus add_sensor(SensorType, double) : int, plus sensor_count() : size_t, plus get_sensors() : const vector of unique_ptr of Sensor&, plus drive(const Route&) : void in italics, the underlined plus next_id() : int, and the protected hash log_event(const string&) : void. On the left, Fleet with minus vehicles_ : vector of shared_ptr of Vehicle, plus add(shared_ptr of Vehicle) : void, plus remove(int) : bool, plus size() : size_t; a line labeled holds with an open diamond at Fleet joins it to Vehicle, 1 to 0..*, the Vehicle end named minus vehicles_. Below it, Passenger with minus name_ : string, minus ride_ : weak_ptr of Vehicle, plus Passenger(string), plus board(shared_ptr of Vehicle) : void and plus leave() : void; an arrow labeled rides runs to Vehicle, 0..* to 0..1, the Vehicle end named minus ride_. Top right, Sensor with minus id_ : int, minus type_ : SensorType, minus range_ : double, plus Sensor(int, SensorType = lidar, double = 100.0), plus get_id() : int, plus get_type() : SensorType and plus get_range() : double; a line labeled owns with a filled diamond at Vehicle joins them, 1 to 0..*, the Sensor end named minus sensors_. A dashed arrow runs from Sensor to SensorType, marked enumeration, with lidar, camera and radar. A dashed arrow labeled uses runs from Vehicle to Route, with minus waypoints_ : vector of Position, plus add(Position) : void and plus length() : double; a line labeled has with a filled diamond at Route joins Route to Position, marked struct, with plus x : double and plus y : double, 1 to 0..*, the Position end named minus waypoints_. Lower right, RoboTaxi, marked final, with plus RoboTaxi(double) and plus drive(const Route&) : void, and Taxi, marked final, with minus driver_name_ : string, plus Taxi(double, string) and plus drive(const Route&) : void; each joins Vehicle by a line with a hollow triangle at Vehicle.
   :align: center
   :width: 100%

   The robotaxi fleet software: nine types, each with every member.

- Every data member is in its box. A name at the end of a line, such as
  ``-ride_``, is the data member that holds the class at that end, listed in
  the box too.
- The diagram uses the C++ types of the code: ``double``, ``string``,
  ``shared_ptr<Vehicle>``.


2. Classes
====================================================

Each class has a **responsibility** (the one job it does), an **invariant**
(the rule its data members always keep, checked by the constructor and by every
method that changes them) and the requirements it serves.

.. list-table::
   :header-rows: 1
   :widths: 14 30 30 26

   * - Class
     - Responsibility
     - Invariant
     - Requirements
   * - ``Vehicle``
     - Anything that drives a route. Abstract: ``drive`` is pure ``virtual``,
       so no ``Vehicle`` object can be made, only a ``RoboTaxi`` or a
       ``Taxi``. It owns its sensors.
     - The maximum speed is greater than 0; the speed stays from 0 to the
       maximum speed; the mileage never goes down.
     - FR-3, FR-4.1, FR-5, NFR-1, NFR-2
   * - ``RoboTaxi``
     - A vehicle that drives itself. Its ``drive`` checks the sensors first: with
       no sensor, it stays parked. ``final``.
     - ``Vehicle``'s. It adds no data member.
     - FR-3, FR-4.2
   * - ``Taxi``
     - A vehicle that a person drives. Its ``drive`` checks the driver first:
       with an empty name, it stays parked. ``final``.
     - ``Vehicle``'s. An empty ``driver_name_`` means no driver.
     - FR-3, FR-5.1
   * - ``Fleet``
     - The company's vehicles, shared with the rest of the program. It names
       only ``Vehicle``, never ``RoboTaxi`` or ``Taxi``.
     - No null pointer and no vehicle twice.
     - FR-10.1 to FR-10.5, NFR-1
   * - ``Passenger``
     - A person who rides at most one vehicle at a time, and owns none.
     - The name is not empty.
     - FR-12.1 to FR-12.4
   * - ``Sensor``
     - One lidar, camera or radar on a vehicle. ``Vehicle::add_sensor`` picks
       its id.
     - The range is at least 0.
     - FR-4.1
   * - ``SensorType``
     - What kind a sensor is: ``lidar``, ``camera`` or ``radar``. An
       ``enum class``.
     - None: any of the three values is valid.
     - FR-4.1
   * - ``Route``
     - The waypoints of one trip, in order, and their length: the sum of the
       straight segments.
     - None: any list of waypoints is a route.
     - FR-5, FR-9.1, FR-9.2
   * - ``Position``
     - One point on the map: ``x`` east and ``y`` north, in m. A ``struct``.
     - None: any ``x`` and any ``y`` make a position.
     - FR-9.1

A type with an invariant is a ``class`` with ``private`` data members, and its
constructor checks the rule. A type with no rule to check, such as
``Position``, is a ``struct``.


3. Relationships
====================================================

Each line of the diagram is a relationship, and each relationship becomes a
C++ member or parameter. The lifetime rule says what happens to the class at
the far end when the first class is destroyed.

.. list-table::
   :header-rows: 1
   :widths: 19 17 24 24 16

   * - Classes
     - Relationship
     - In C++
     - Lifetime rule
     - Requirement
   * - ``Fleet`` and ``Vehicle``
     - Aggregation: open diamond at ``Fleet``, 1 to 0..*
     - ``std::vector<std::shared_ptr<Vehicle>> vehicles_``
     - A vehicle can exist before the fleet, after it, and in another fleet.
     - FR-10.5, TC-5
   * - ``Passenger`` and ``Vehicle``
     - Association: arrow to ``Vehicle``, 0..* to 0..1
     - ``std::weak_ptr<Vehicle> ride_``
     - Boarding keeps no vehicle alive; the passenger can check that the
       vehicle still exists.
     - FR-12.3, TC-6
   * - ``Vehicle`` and ``Sensor``
     - Composition: filled diamond at ``Vehicle``, 1 to 0..*
     - ``std::vector<std::unique_ptr<Sensor>> sensors_``
     - The sensors are destroyed with their vehicle.
     - TC-4
   * - ``Route`` and ``Position``
     - Composition: filled diamond at ``Route``, 1 to 0..*
     - ``std::vector<Position> waypoints_``, by value
     - The positions are destroyed with their route.
     - TC-4
   * - ``Vehicle`` and ``Route``
     - Dependency: dashed arrow to ``Route``
     - The parameter of ``drive(const Route&)``; no member
     - ``Vehicle`` keeps nothing of the route after the call.
     - FR-5, TC-7
   * - ``Sensor`` and ``SensorType``
     - Dependency: dashed arrow to ``SensorType``
     - ``SensorType type_``, a value
     - A ``SensorType`` is a value from a fixed list, not an object that
       ``Sensor`` refers to.
     - FR-4.1
   * - ``RoboTaxi``, ``Taxi`` and ``Vehicle``
     - Inheritance: hollow triangle at ``Vehicle``
     - ``class RoboTaxi final : public Vehicle``, and the same for ``Taxi``
     - A ``RoboTaxi`` or a ``Taxi`` object holds a ``Vehicle`` part, with
       every data member of ``Vehicle``: it is made first and destroyed last.
     - FR-3


4. Design Decisions
====================================================

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Decision
     - Reason
   * - Every class is in the namespace ``fleet``.
     - ``Vehicle``, ``Route`` and ``Sensor`` are common names: a library with
       its own ``Vehicle`` would clash with ours (TC-2).
   * - One header and one source file per class, named after it. A derived
       class has its own files and includes ``vehicle.hpp``; ``vehicle.hpp``
       includes none of its derived classes.
     - You find a class by its file name, and a change to one class recompiles
       only the files that include its header. A new kind of vehicle adds two
       files and changes none (NFR-1).
   * - ``Vehicle`` is abstract: ``drive`` is pure ``virtual``.
     - Each kind of vehicle drives in its own way (FR-3), and a vehicle that is
       neither a robotaxi nor a taxi has no way to drive.
   * - ``Vehicle`` has a ``virtual`` destructor.
     - Deleting a ``RoboTaxi`` or a ``Taxi`` through a ``Vehicle`` pointer then
       runs its own destructor first (NFR-3).
   * - ``Fleet`` and ``Passenger`` name only ``Vehicle``.
     - A new kind of vehicle joins a fleet and is boarded with no change to
       either class (NFR-1).
   * - ``RoboTaxi`` and ``Taxi`` are ``final``.
     - No class derives from them: a new kind of vehicle derives from
       ``Vehicle``.
   * - A broken rule throws ``std::invalid_argument``, with a message that
       names the rule.
     - The object stays as it was, and the caller learns which rule it broke
       (NFR-2, TC-8).


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


6. Traceability
====================================================

Each requirement that the course code meets, with the classes and members
that meet it. The :doc:`L9 Requirements <l9_requirements>` page gives the
check for each one.

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Requirement
     - Classes and members
   * - FR-3
     - ``Vehicle::drive``, pure ``virtual``; ``RoboTaxi::drive`` and
       ``Taxi::drive`` override it.
   * - FR-4.1, FR-4.2
     - ``Vehicle::add_sensor``, ``Vehicle::sensor_count``, ``Sensor``,
       ``SensorType``; ``RoboTaxi::drive`` checks ``sensor_count()`` first.
   * - FR-5, FR-5.1
     - ``Vehicle::drive(const Route&)``; ``Taxi::drive`` checks for an empty
       driver name.
   * - FR-9.1, FR-9.2
     - ``Route::add``, ``Route::length``, ``Position``.
   * - FR-10.1 to FR-10.5
     - ``Fleet::add``, ``Fleet::remove``, ``Fleet::size``; ``vehicles_`` holds
       ``std::shared_ptr<Vehicle>``.
   * - FR-12.1 to FR-12.4
     - ``Passenger`` and its constructor, ``Passenger::board``,
       ``Passenger::leave``; ``ride_`` is a ``std::weak_ptr<Vehicle>``.
   * - NFR-1
     - ``Fleet`` and ``Passenger`` name only ``Vehicle``.
   * - NFR-2
     - The constructors of ``Vehicle``, ``Sensor`` and ``Passenger``,
       ``Vehicle::set_speed``, ``Vehicle::add_mileage`` and ``Fleet::add``.
