.. _l8_quiz:

================
Lecture 8 Quiz
================

This quiz covers the key concepts from Lecture 8: OOP Basics. Topics include classes and objects, when a type is a ``struct`` and when a ``class``, encapsulation, accessors and mutators, ``noexcept``, constructors and ``explicit``, the ``this`` pointer, and destructors. Question 9 uses the required reading, :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`. No question uses the Further Reading part of the lecture (the appendix of the slides).

Unless a question shows its own class, ``Vehicle`` is the class of ``project/week8/common/include/vehicle.hpp``: ``explicit Vehicle(double max_speed, const std::string& color = "white")``, ``Vehicle(double max_speed, double speed)``, a ``set_speed`` that throws ``std::invalid_argument`` when the speed is not from 0 to the maximum speed, and ``const`` accessors. Each snippet is part of a full program. Every output shown was measured with g++ 13.3, with ``-std=c++20 -Wall -Wextra -pedantic-errors -Wshadow``.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 10)
=====================================

.. admonition:: Question 1
   :class: hint

   By Core Guidelines C.2, which of these types should be a ``class``?

   A. A point in space: ``x``, ``y`` and ``z``, in m.
   B. A time window for a pickup: a start time and an end time, where the end must not come before the start.
   C. A reading: the id of the sensor that took it, and the value it read.
   D. The color of a car on the screen: red, green and blue, each a ``std::uint8_t``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. The time window.**

      C.2 says: "Use ``class`` if the class has an invariant; use ``struct`` if the data members can vary independently". The time window has a rule between its two members, the end must not come before the start, so a setter or a constructor must check it: that makes it a ``class`` with ``private`` members. In A and C, any values make a valid point or reading. In D, each ``std::uint8_t`` already holds only 0 to 255, and the three values vary independently, so the type keeps the range and a ``struct`` is enough.

.. admonition:: Question 2
   :class: hint

   What does this program print?

   .. code-block:: cpp

      class Vehicle {
       public:
        void set_speed(double speed) { speed_ = speed; }
        double get_speed() const { return speed_; }

       private:
        double max_speed_{13.4};  // m/s
        double speed_{0.0};       // m/s
        std::string color_{"white"};
        double mileage_{0.0};     // m driven
      };

      std::cout << sizeof(Vehicle) << '\n';

   A. 56
   B. 72: 56 for the data members and 8 for each of the two methods.
   C. 64: 56 for the data members and 8 for a pointer to the methods.
   D. 0, because a class is only a blueprint.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **A. 56**

      An object holds one value for each data member: three ``double``\ s, 8 bytes each (24 bytes), and a ``std::string``, 32 bytes with g++. The methods are not inside the object. They exist once, in the program's code, and every object uses them. The call passes the object's address, which the method sees as ``this``.

.. admonition:: Question 3
   :class: hint

   What does this program print?

   .. code-block:: cpp

      Vehicle car{13.4, 10.0};
      try {
        car.set_speed(-1.0);
      } catch (const std::invalid_argument& e) {
        std::cout << "caught: " << e.what() << '\n';
      }
      std::cout << car.get_speed() << '\n';

   A. ``-1``
   B. ``caught: speed must be from 0 to the maximum speed``, then ``-1``
   C. ``caught: speed must be from 0 to the maximum speed``, then ``10``
   D. Nothing: the program stops with ``terminate called``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C.**

      .. code-block:: text

         caught: speed must be from 0 to the maximum speed
         10

      ``set_speed`` tests the new value first. -1 is below 0, so it throws before it changes ``speed_``, and the car keeps 10, the value the delegating constructor set. ``set_speed`` is not ``noexcept``, so the exception reaches the ``catch``. With ``noexcept`` on ``set_speed``, the program would stop instead (answer D).

.. admonition:: Question 4
   :class: hint

   ``Vehicle`` has only the constructor ``explicit Vehicle(double max_speed, const std::string& color = "white")``. What does this line declare?

   .. code-block:: cpp

      Vehicle parked_car();

   A. A ``Vehicle`` built by the default constructor.
   B. A function named ``parked_car`` that takes no arguments and returns a ``Vehicle``.
   C. Nothing: it does not compile, because ``Vehicle`` has no default constructor.
   D. A ``Vehicle`` whose maximum speed is 0.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.**

      With empty parentheses, C++ reads the line as the declaration of a function. g++ compiles it with a warning:

      .. code-block:: text

         warning: empty parentheses were disambiguated as a function declaration [-Wvexing-parse]

      The first use of ``parked_car`` as an object fails: ``request for member 'get_color' in 'parked_car', which is of non-class type 'Vehicle()'``. With braces, ``Vehicle parked_car{};`` asks for the default constructor, and this ``Vehicle`` has none, so that line does not compile (answer C describes the braces, not the parentheses). Braces never declare a function, which is one reason to create objects with them.

.. admonition:: Question 5
   :class: hint

   What happens when this code runs ``Vehicle car{13.4};``?

   .. code-block:: cpp

      class Vehicle {
       public:
        explicit Vehicle(double max_speed)
            : max_speed_{max_speed}, speed_{max_speed_ / 2.0} {}

       private:
        double speed_;
        double max_speed_;
      };

   A. ``max_speed_`` is 13.4 and ``speed_`` is 6.7: the list runs left to right.
   B. ``speed_`` is created first, from ``max_speed_``, which has no value yet: undefined behavior.
   C. It does not compile: a member cannot appear in another member's initializer.
   D. ``speed_`` is 0: members without a value are set to zero.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.**

      Members are created in the order the class declares them, whatever the order of the list. ``speed_`` is declared first, so it is created first, and it reads ``max_speed_`` before ``max_speed_`` has its value. g++ warns, even at ``-O0``:

      .. code-block:: text

         warning: 'Vehicle::max_speed_' will be initialized after [-Wreorder]
         warning:   'double Vehicle::speed_' [-Wreorder]
         warning:   when initialized here [-Wreorder]
         warning: member 'Vehicle::max_speed_' is used uninitialized [-Wuninitialized]
         warning: '*this.Vehicle::max_speed_' is used uninitialized [-Wuninitialized]

      Core Guidelines C.47: "Define and initialize data members in the order of member declaration".

.. admonition:: Question 6
   :class: hint

   ``Vehicle(double max_speed, const std::string& color = "white")`` is ``explicit``, and ``show`` takes a ``const Vehicle&``. Which call compiles?

   A. ``show(13.4);``
   B. ``show(Vehicle{13.4});``
   C. ``show({13.4});``
   D. ``show(13);``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.**

      An ``explicit`` constructor runs only when the code names the class. B names it. A and D pass a number, and C a braced list, so each would need the compiler to build a ``Vehicle`` on its own. g++ refuses:

      .. code-block:: text

         error: converting to 'const Vehicle' from initializer list would use explicit constructor 'Vehicle::Vehicle(double, const std::string&)'
         error: invalid initialization of reference of type 'const Vehicle&' from expression of type 'int'

      The first error is for C, the second for D. A gives the same error as D, with ``'double'``.

.. admonition:: Question 7
   :class: hint

   What does this program print?

   .. code-block:: cpp

      class Vehicle {
       public:
        explicit Vehicle(int id) : id_{id} {}
        ~Vehicle() { std::cout << id_ << ' '; }

       private:
        int id_;
      };

      {
        Vehicle a{1};
        Vehicle b{2};
        Vehicle c{3};
      }
      std::cout << '\n';

   A. ``1 2 3``
   B. ``3 2 1``
   C. Nothing: the destructor runs only for objects on the heap.
   D. ``1 2 3``, but only when the program ends.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 3 2 1**

      At the end of a scope, objects are destroyed in the reverse order they were created: ``c``, then ``b``, then ``a``. Each destructor runs at the closing brace, not when the program ends.

.. admonition:: Question 8
   :class: hint

   What does this program print?

   .. code-block:: cpp

      class Vehicle {
       public:
        explicit Vehicle(int id) : id_{id} {}
        ~Vehicle() { std::cout << id_ << ' '; }

       private:
        int id_;
      };

      {
        Vehicle a{1};
        auto b{std::make_unique<Vehicle>(2)};
        {
          Vehicle c{3};
          b.reset();
        }
        std::cout << "| ";
      }
      std::cout << '\n';

   A. ``3 2 | 1``
   B. ``2 3 | 1``
   C. ``3 | 2 1``
   D. ``2 3 1 |``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 2 3 | 1**

      A heap object is destroyed when its owner lets go: ``b.reset()`` destroys the ``Vehicle`` with id 2 at once, so 2 comes first. ``c`` is destroyed at the end of the inner block, then ``|`` is printed, and ``a`` is destroyed at the end of the outer block.

.. admonition:: Question 9
   :class: hint

   This question uses the required reading, :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`. This ``Vehicle`` follows the rule of zero:

   .. code-block:: cpp

      class Vehicle {
       public:
        explicit Vehicle(const Sensor& sensor)
            : sensor_{std::make_unique<Sensor>(sensor)} {}

       private:
        std::unique_ptr<Sensor> sensor_;
      };

      Vehicle a{Sensor{1}};
      Vehicle c{Sensor{3}};

   Which line compiles?

   A. ``Vehicle d{c};``
   B. ``Vehicle b{std::move(a)};``
   C. ``a = c;``
   D. None of them: a class with a ``std::unique_ptr`` member must write its own destructor, copies and moves.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B.**

      The compiler writes the destructor and the moves: they destroy and move the ``std::unique_ptr``. It cannot copy a ``std::unique_ptr``, so it writes no copy, and the class is move-only. A and C fail:

      .. code-block:: text

         error: use of deleted function 'Vehicle::Vehicle(const Vehicle&)'
         error: use of deleted function 'Vehicle& Vehicle::operator=(const Vehicle&)'

.. admonition:: Question 10
   :class: hint

   What does this program print?

   .. code-block:: cpp

      class Vehicle {
       public:
        void set_speed(double speed) noexcept {
          if (speed < 0.0) {
            throw std::invalid_argument{"negative speed"};
          }
          speed_ = speed;
        }

       private:
        double speed_{0.0};
      };

      int main() {
        Vehicle car;
        try {
          car.set_speed(-1.0);
        } catch (const std::invalid_argument& e) {
          std::cout << "caught: " << e.what() << '\n';
        }
        std::cout << "done\n";
      }

   A. ``caught: negative speed``, then ``done``
   B. ``done`` only: the exception is ignored.
   C. Neither line: the program stops in ``std::terminate``.
   D. Nothing: it does not compile, because a ``noexcept`` method cannot contain ``throw``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C.**

      ``noexcept`` promises that no exception leaves ``set_speed``. When one does, C++ calls ``std::terminate``, and the ``catch`` in ``main`` never runs (C++20 [except.spec] paragraph 5). The program compiles, with a warning:

      .. code-block:: text

         warning: 'throw' will always call 'terminate' [-Wterminate]

      The run prints nothing on standard output. On standard error it prints the lines below, and it ends with exit status 134:

      .. code-block:: text

         terminate called after throwing an instance of 'std::invalid_argument'
           what():  negative speed

      A mutator that can throw must not be ``noexcept``.


True/False (Questions 11 to 15)
=================================

.. admonition:: Question 11
   :class: hint

   **True or False**: A ``struct`` can have methods and ``private`` members, as a ``class`` can. When no access specifier is written, a member is ``public`` in a ``struct`` and ``private`` in a ``class``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      ``struct`` and ``class`` make the same kind of type. C++20 [class.access] paragraph 3: "Members of a class defined with the keyword ``class`` are ``private`` by default. Members of a class defined with the keywords ``struct`` or ``union`` are ``public`` by default". Access to a base class (L9) has the same two defaults. Which one to write is a design choice: ``class`` when there is an invariant (Core Guidelines C.2).

.. admonition:: Question 12
   :class: hint

   **True or False**: Inside ``double get_speed() const``, a method of ``Vehicle``, ``this`` has the type ``Vehicle*``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      In a ``const`` method, ``this`` is a ``const Vehicle*``: a pointer to a ``const Vehicle``, so no line there can change a data member. In a method that is not ``const``, such as ``set_speed``, it is a ``Vehicle*``. This compiles:

      .. code-block:: cpp

         double get_speed() const {
           static_assert(std::is_same_v<decltype(this), const Vehicle*>);
           return speed_;
         }

.. admonition:: Question 13
   :class: hint

   **True or False**: ``vehicle.hpp`` defines ``get_speed`` inside the class, and two source files of one program include it. The program links, even though both source files hold the definition of ``get_speed``.

   .. code-block:: cpp

      // vehicle.hpp
      #pragma once
      class Vehicle {
       public:
        double get_speed() const { return speed_; }

       private:
        double speed_{0.0};
      };

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      A method defined in its class is inline, and every source file that includes the header may hold its definition. C++20 [class.mfct] paragraph 1: "A member function may be defined (9.5) in its class definition, in which case it is an inline (9.2.7) member function if it is attached to the global module". Code that uses no C++20 modules is attached to the global module. Written instead outside the class in the header, as ``double Vehicle::get_speed() const { return speed_; }``, the definition is not inline, and the link fails:

      .. code-block:: text

         multiple definition of `Vehicle::get_speed() const'

.. admonition:: Question 14
   :class: hint

   **True or False**: This class declares no constructor. ``Vehicle b{};`` gives ``b.get_speed()`` the value 0, but ``Vehicle a;`` leaves ``a.speed_`` with an indeterminate value.

   .. code-block:: cpp

      class Vehicle {
       public:
        double get_speed() const { return speed_; }

       private:
        double max_speed_{13.4};
        double speed_;  // no { }
      };

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      The ``{ }`` in ``Vehicle b{};`` sets every member to zero first, then the default member initializers run, so ``b`` prints 0. ``Vehicle a;`` runs only the compiler's default constructor, which sets ``max_speed_`` from its initializer and leaves ``speed_`` alone. Reading ``a.get_speed()`` is undefined behavior, and with the Debug build (``-O0``) g++ gives no warning. Give every member its own initializer, so the result does not depend on how the caller wrote the object.

.. admonition:: Question 15
   :class: hint

   **True or False**: An invariant must be true at every line inside a ``public`` method of the class, not only before and after the call.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      An invariant must be true whenever code outside the class uses the object: before a ``public`` method is called and after it returns. Inside the method, it may break for a moment, as long as it holds again before the method returns. An elevator whose display must always show its current floor is an example: ``go_to(5)`` sets ``current_floor`` first, which breaks the rule, then sets ``display_floor``, which restores it. No code outside the class runs between the two lines, so outside code never sees the broken state.
