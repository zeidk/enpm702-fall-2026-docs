.. _l9_quiz:

================
Lecture 9 Quiz
================

This quiz covers the key concepts from Lecture 9: OOP Advanced. Topics include class relationships (association, aggregation, composition, dependency), multiplicity, inheritance with ``public``, ``protected`` and base class initializers, construction order, compile-time and runtime polymorphism, ``override``, ``auto`` against a pointer to the base class, ``virtual`` destructors, abstract and concrete classes, ``final``, and namespaces. No question uses the Further Reading part of the lecture.

Unless a question shows its own classes, ``Vehicle``, ``RoboTaxi``, ``Taxi``, ``Fleet`` and ``Passenger`` are the classes of ``project/week9/common``: ``Vehicle`` is abstract, with ``virtual void drive(const Route& route) const = 0;`` and ``virtual ~Vehicle() = default;``; ``RoboTaxi`` and ``Taxi`` are ``final`` and override ``drive``; ``Fleet`` holds ``std::shared_ptr<Vehicle>``; ``Passenger`` holds a ``std::weak_ptr<Vehicle>``. These classes are in the namespace ``fleet``; the snippets leave out ``fleet::``, as the lecture's listings do (One Namespace: ``fleet``). ``trip`` is the 500 m route of the lecture. Each snippet is part of a full program. Every output shown was measured with g++ 13.3, with ``-std=c++20 -Wall -Wextra -pedantic-errors -Wshadow``.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 11)
=====================================

.. admonition:: Question 1
   :class: hint

   A ``Fleet`` keeps ``std::vector<std::shared_ptr<Vehicle>> vehicles_``. A vehicle can be in two fleets, and it is not destroyed when a fleet is. Which relationship is this, and how does UML draw it?

   A. Composition, a filled diamond at ``Fleet``.
   B. Aggregation, an open diamond at ``Fleet``.
   C. Association, an arrow from ``Vehicle`` to ``Fleet``.
   D. Dependency, a dashed arrow from ``Fleet`` to ``Vehicle``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Aggregation, an open diamond at** ``Fleet``.

      An aggregation is a whole that holds parts it does not own alone: a part can exist before the whole, after it, and in more than one whole. Each ``std::shared_ptr`` makes the fleet one more owner, not the only one. Composition (A) would need one owner, a ``std::unique_ptr`` or a plain member, and the part would die with the whole. A dependency (D) keeps no member at all.

.. admonition:: Question 2
   :class: hint

   In the class diagram, the arrow labeled ``rides`` runs from ``Passenger`` to ``Vehicle``, with ``0..*`` at ``Passenger`` and ``0..1`` at ``Vehicle``. What does it say?

   A. One passenger rides any number of vehicles at a time, and one vehicle carries at most one passenger.
   B. One passenger rides at most one vehicle at a time, and one vehicle carries any number of passengers.
   C. Every passenger must ride exactly one vehicle.
   D. A ``Vehicle`` knows its passengers, and a ``Passenger`` does not know its vehicle.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.**

      The number at an end says how many objects of that end's class take part, for one object at the other end. ``0..1`` at ``Vehicle``: one passenger rides zero or one vehicle. ``0..*`` at ``Passenger``: one vehicle carries any number of passengers. The arrow points at the class that is known: the ``Passenger`` knows its ``Vehicle`` (its ``std::weak_ptr``), not the other way, so D is reversed.

.. admonition:: Question 3
   :class: hint

   What does this program print?

   .. code-block:: cpp

      auto car{std::make_shared<RoboTaxi>(13.4)};
      Fleet fleet;
      fleet.add(car);
      Passenger maya{"Maya"};
      maya.board(car);
      fleet.add(car);
      std::cout << car.use_count() << ' ' << fleet.size() << '\n';

   A. ``2 1``
   B. ``3 1``
   C. ``3 2``
   D. ``4 2``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A.** ``2 1``

      ``car`` is one owner and the fleet's ``std::shared_ptr`` is the second. ``maya`` holds a ``std::weak_ptr``, which is not an owner, so it does not change ``use_count()``: an association. The second ``fleet.add(car)`` adds nothing, because ``Fleet``'s invariant allows no vehicle twice, so the size stays 1.

.. admonition:: Question 4
   :class: hint

   This question shows its own classes: this ``Vehicle`` has no ``virtual`` method. Each constructor and destructor prints its name. What does this program print?

   .. code-block:: cpp

      class Vehicle {
       public:
        explicit Vehicle(double max_speed) : max_speed_{max_speed} {
          std::cout << "Vehicle constructor\n";
        }
        ~Vehicle() { std::cout << "~Vehicle\n"; }

       private:
        double max_speed_;
      };

      struct Lidar {
        Lidar() { std::cout << "Lidar constructor\n"; }
        ~Lidar() { std::cout << "~Lidar\n"; }
      };

      class RoboTaxi : public Vehicle {
       public:
        explicit RoboTaxi(double max_speed) : Vehicle{max_speed} {
          std::cout << "RoboTaxi constructor\n";
        }
        ~RoboTaxi() { std::cout << "~RoboTaxi\n"; }

       private:
        Lidar lidar_;
      };

      {
        RoboTaxi robotaxi{13.4};
      }

   A. ``RoboTaxi constructor``, ``Lidar constructor``, ``Vehicle constructor``, then ``~Vehicle``, ``~Lidar``, ``~RoboTaxi``
   B. ``Lidar constructor``, ``Vehicle constructor``, ``RoboTaxi constructor``, then ``~RoboTaxi``, ``~Vehicle``, ``~Lidar``
   C. ``Vehicle constructor``, ``Lidar constructor``, ``RoboTaxi constructor``, then ``~RoboTaxi``, ``~Lidar``, ``~Vehicle``
   D. ``Vehicle constructor``, ``RoboTaxi constructor``, then ``~RoboTaxi``, ``~Vehicle``: ``lidar_`` is not in the list, so it is never built.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C.**

      .. code-block:: text

         Vehicle constructor
         Lidar constructor
         RoboTaxi constructor
         ~RoboTaxi
         ~Lidar
         ~Vehicle

      The base is built first, then the members in the order they are declared, then the constructor's body. Destruction is the exact reverse. ``lidar_`` has no initializer in the list, and it is still built before the body: every member is (D is wrong).

.. admonition:: Question 5
   :class: hint

   This question shows its own ``Vehicle``: a concrete class with a ``public`` method ``get_speed()``.

   .. code-block:: cpp

      class Vehicle {
       public:
        [[nodiscard]] double get_speed() const noexcept { return speed_; }

       private:
        double speed_{0.0};
      };

      // one of the declarations A to D

      int main() {
        RoboTaxi robotaxi;
        std::cout << robotaxi.get_speed() << '\n';
      }

   With which declaration of ``RoboTaxi`` does the program **not** compile?

   A. ``class RoboTaxi : Vehicle {};``
   B. ``struct RoboTaxi : Vehicle {};``
   C. ``class RoboTaxi : public Vehicle {};``
   D. ``struct RoboTaxi : public Vehicle {};``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A.**

      With no access specifier, the base is ``private`` when the derived class is defined with ``class``, and ``public`` when it is defined with ``struct``. In A, ``Vehicle``'s ``public`` methods become ``private`` in ``RoboTaxi``:

      .. code-block:: text

         error: 'double Vehicle::get_speed() const' is inaccessible within this context
         error: 'Vehicle' is not an accessible base of 'RoboTaxi'

      B, C and D compile, and the program prints ``0``. C++20 [class.access.base] paragraph 2: "In the absence of an access-specifier for a base class, ``public`` is assumed when the derived class is defined with the class-key ``struct`` and ``private`` is assumed when the class is defined with the class-key ``class``". Always write ``public``.

.. admonition:: Question 6
   :class: hint

   In this question, ``Vehicle::drive`` is **not** ``virtual``, and ``RoboTaxi`` redefines it. What does the program print?

   .. code-block:: cpp

      class Vehicle {
       public:
        explicit Vehicle(double max_speed) : max_speed_{max_speed} {}
        void drive(const Route& route) const {
          std::cout << "Vehicle: drives " << route.length() << " m\n";
        }

       private:
        double max_speed_;
      };

      class RoboTaxi : public Vehicle {
       public:
        explicit RoboTaxi(double max_speed) : Vehicle{max_speed} {}
        void drive(const Route& route) const {
          std::cout << "RoboTaxi: drives itself " << route.length() << " m\n";
        }
      };

      void start_shift(const Vehicle& vehicle, const Route& route) {
        vehicle.drive(route);
      }

      RoboTaxi robotaxi{13.4};
      start_shift(robotaxi, trip);

   A. ``Vehicle: drives 500 m``
   B. ``RoboTaxi: drives itself 500 m``
   C. Both lines, the base's first.
   D. It does not compile: a ``RoboTaxi`` cannot bind to a ``const Vehicle&``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A.** ``Vehicle: drives 500 m``

      Without ``virtual``, the compiler picks the method from the **static type** of ``vehicle``, ``const Vehicle&``, so it calls ``Vehicle::drive``. The dynamic type, ``RoboTaxi``, plays no part. A ``Vehicle&`` binds to a ``RoboTaxi`` with no cast, so D is wrong. With ``virtual`` on ``Vehicle::drive``, the same call prints B.

.. admonition:: Question 7
   :class: hint

   Two classes have the same two ``double`` data members. ``Plain`` has no ``virtual`` method; ``Poly`` has a ``virtual`` destructor and a ``virtual`` method. With g++ on the course's 64-bit Linux, what does ``std::cout << sizeof(Plain) << ' ' << sizeof(Poly) << '\n';`` print?

   A. ``16 16``
   B. ``16 24``
   C. ``16 32``
   D. ``24 24``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.** ``16 24``

      Two ``double``\ s take 16 bytes. g++ stores one hidden pointer in each object of a polymorphic class, to the table of its class's ``virtual`` methods (the vtable): 8 bytes more, however many ``virtual`` methods the class has. The C++ standard leaves this to the compiler, which is why the question names g++.

.. admonition:: Question 8
   :class: hint

   What does this program print?

   .. code-block:: cpp

      std::vector<std::unique_ptr<Vehicle>> vehicles;
      auto robotaxi{std::make_unique<RoboTaxi>(13.4)};
      vehicles.push_back(std::move(robotaxi));
      std::cout << vehicles.size() << ' ' << std::boolalpha
                << (robotaxi == nullptr) << '\n';

   A. ``1 true``
   B. ``1 false``
   C. Nothing: ``auto`` deduces ``std::unique_ptr<RoboTaxi>``, which cannot go into a vector of ``std::unique_ptr<Vehicle>``.
   D. Nothing: only ``emplace_back`` accepts it.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A.** ``1 true``

      ``auto`` does deduce ``std::unique_ptr<RoboTaxi>``. But a ``std::unique_ptr<RoboTaxi>`` that is moved converts to a ``std::unique_ptr<Vehicle>``, so ``push_back``, ``emplace_back`` and a ``std::unique_ptr<Vehicle>`` parameter all accept it. The move leaves ``robotaxi`` null. Use ``auto`` while the code needs the ``RoboTaxi`` type, then move the pointer.

.. admonition:: Question 9
   :class: hint

   ``Vehicle`` and ``Taxi`` are the classes of the lecture's slide "Deleting through a Base Pointer": ``~Vehicle`` is **not** ``virtual``, and both destructors print their names. The program is built with AddressSanitizer. Which destructors run, and what does AddressSanitizer report?

   .. code-block:: cpp

      std::unique_ptr<Vehicle> vehicle{
          std::make_unique<Taxi>(13.4, "Ana Maria Rodrigues")};

   A. ``~Taxi``, then ``~Vehicle``; no report.
   B. ``~Vehicle`` only; ``new-delete-type-mismatch``: 56 bytes allocated, 24 freed.
   C. ``~Taxi`` only; a double free.
   D. ``~Vehicle`` only; no report, because ``std::unique_ptr`` knows the type it was made from.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.**

      ``vehicle`` deletes a ``Vehicle*``. Its destructor is not ``virtual``, so the static type picks it: only ``~Vehicle`` runs, which is undefined behavior. AddressSanitizer stops with ``new-delete-type-mismatch``: 56 bytes were allocated for a ``Taxi`` and freed as a 24-byte ``Vehicle``. With that check off, LeakSanitizer reports the 20 bytes of the driver's name, 19 characters and the ``'\0'``, because ``~Taxi`` never ran. A ``virtual`` destructor in ``Vehicle`` gives A.

.. admonition:: Question 10
   :class: hint

   ``Taxi`` is not ``final`` in this question. Which of the two classes compiles?

   .. code-block:: cpp

      class Taxi : public Vehicle {
       public:
        void drive(const Route& route) const final;
      };

      class NightTaxi : public Taxi {  // 1
       public:
        int lamps_{2};
      };

      class LateTaxi : public Taxi {  // 2
       public:
        void drive(const Route& route) const override;
      };

   A. Both.
   B. Only 1.
   C. Only 2.
   D. Neither: ``final`` on a method stops any class from deriving from ``Taxi``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Only 1.**

      ``final`` after a ``virtual`` method stops derived classes from overriding it. ``NightTaxi`` can still derive from ``Taxi`` and add members; only ``drive`` is closed. ``LateTaxi`` tries to override it:

      .. code-block:: text

         error: virtual function 'virtual void LateTaxi::drive(const Route&) const' overriding final function

      ``final`` after the class name, ``class Taxi final``, is what would stop every derived class.


.. admonition:: Question 11
   :class: hint

   Which of the numbered lines compile?

   .. code-block:: cpp

      namespace fleet {
      class Route {};
      }  // namespace fleet

      int main() {
        Route trip;          // 1
        fleet::Route back;   // 2
        using fleet::Route;
        Route next;          // 3
      }

   A. All three.
   B. Only 2.
   C. Only 2 and 3.
   D. Only 1 and 3.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Only 2 and 3.**

      ``Route`` is declared inside ``fleet``, so outside the namespace line 1 does not find it:

      .. code-block:: text

         error: 'Route' was not declared in this scope; did you mean 'fleet::Route'?

      Line 2 names the class in full. The using-declaration brings the one name ``fleet::Route`` into ``main``, so line 3 finds it without ``fleet::``. With line 1 removed, the program compiles.


True/False (Questions 12 to 16)
=================================

.. admonition:: Question 12
   :class: hint

   **True or False**: ``Vehicle`` declares ``virtual void drive(const Route& route) const;``. In ``RoboTaxi``, ``void drive(const Route& route) { /* ... */ }``, with no ``const``, overrides it.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      To override, the derived method must have the same name, parameters and ``const``. Without ``const`` it is a new method of ``RoboTaxi``, which hides ``Vehicle::drive``. It compiles, and ``-Wall`` only warns:

      .. code-block:: text

         warning: 'virtual void Vehicle::drive(const Route&) const' was hidden [-Woverloaded-virtual=]

      Writing ``override`` turns the mistake into an error: "marked 'override', but does not override".

.. admonition:: Question 13
   :class: hint

   **True or False**: ``RoboTaxi`` is declared ``class RoboTaxi final : public Vehicle``. Its ``drive`` must also be marked ``final``, or a class derived from ``RoboTaxi`` could override it.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      No class can derive from a ``final`` class, so nothing can override its methods. A ``final`` class needs no ``final`` on its methods: ``RoboTaxi::drive`` is marked ``override`` only. Core Guidelines C.128: "Virtual functions should specify exactly one of ``virtual``, ``override``, or ``final``".

.. admonition:: Question 14
   :class: hint

   **True or False**: In the lecture's discussion "Which drive() Runs?", ``Vehicle::drive`` is ``virtual`` with a body, ``RoboTaxi`` overrides it, and ``ref`` is a ``Vehicle&`` bound to a ``RoboTaxi``. Then ``ref.Vehicle::drive(trip);`` runs ``RoboTaxi::drive``, because ``drive`` is ``virtual``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Naming the class, ``Vehicle::drive``, turns off the virtual call: the line runs ``Vehicle::drive`` and prints ``Vehicle: drives 500 m``. This is how an override calls the base's version on purpose. ``ref.drive(trip);``, without the class name, runs ``RoboTaxi::drive``.

.. admonition:: Question 15
   :class: hint

   **True or False**: The company adds ``class RoboBus final : public Vehicle``, which overrides ``drive``. ``Fleet`` must get a new overload of ``add`` before it can hold a ``RoboBus``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      ``Fleet`` stores ``std::shared_ptr<Vehicle>`` and names only ``Vehicle``. A ``std::shared_ptr<RoboBus>`` converts to a ``std::shared_ptr<Vehicle>``, as a ``std::shared_ptr<RoboTaxi>`` does, so not one line of ``Fleet`` changes. That is the non-functional requirement of last year's design: a new kind of vehicle needs no change to ``Fleet``.

.. admonition:: Question 16
   :class: hint

   **True or False**: If ``Vehicle`` declares ``speed_`` ``protected`` instead of ``private``, this method of a derived class compiles, and afterwards ``get_speed()`` returns 20, above the maximum speed of 13.4.

   .. code-block:: cpp

      void speed_up() { speed_ = 20.0; }

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      A ``protected`` member can be used by the methods of the derived classes, so the assignment compiles, and it skips ``set_speed``'s check. Every derived class can now break ``Vehicle``'s invariant. That is why every data member is ``private`` in this course's assignments, and why Core Guidelines C.133 says "``protected`` data is a source of complexity and errors. ``protected`` data complicates the statement of invariants".
