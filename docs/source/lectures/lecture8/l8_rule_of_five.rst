.. _l8_rule_of_five:

====================================================
Rule of Five and Rule of Zero
====================================================

This page is **required reading** after the Lecture 8 class. It is not presented in class. In class, a ``Vehicle`` owns its ``Sensor``\ s through ``std::unique_ptr`` and writes none of the five special member functions: the rule of zero. This page shows why the compiler gets that class right. It then builds a ``Vehicle`` that owns its ``Sensor`` through a raw pointer, a plain ``Sensor*``, and shows what goes wrong until the class writes all five functions itself: the rule of five.

.. dropdown:: Code for This Page
   :icon: terminal
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Every listing on this page is in the course repository, under ``project/week8/``. Each ``Vehicle`` is a class of its own, in its own namespace, and leaves out the speed members of the lecture.

   - ``playground/src/destructors.cpp``, namespace ``destructors::zero``: the ``Vehicle`` of `Rule of Zero`_.
   - ``appendix/src/appendix.cpp``: namespace ``raw_owner`` (`A Class That Owns Memory`_), ``five`` (the five functions written by hand, run in `All Five, Run`_), ``move_noexcept`` (`Why the Moves Are noexcept`_) and ``move_only`` (:ref:`l8r5-default-delete`).
   - ``undefined/src/undefined.cpp``: namespaces ``undefined::no_destructor`` (the leak), ``undefined::double_free`` (the double free) and ``undefined::move_bug`` (`Discussion: Who Deletes What?`_). The build always compiles this file with AddressSanitizer, the memory checker of L7 (``-fsanitize=address``).

   The code of this page runs in the appendix program, ``week8_appendix``. Each part has a name, its **key**, which is the name of its namespace. Build the program, then run one part by its key, with the ``702`` commands of the :doc:`lecture page <l8_lecture>`:

   .. code-block:: bash

      702build week8_appendix
      702run week8_appendix five

   The keys, in the order of this page:

   - ``zero``: `Rule of Zero`_ and `What the Compiler Writes Now`_.
   - ``raw_owner``: `A Class That Owns Memory`_.
   - ``no_destructor``: `Without the Destructor`_. It ends with a leak report.
   - ``double_free``: `Copying an Owner`_ and `Double Free, Measured`_. It stops with a double-free report.
   - ``five``: `The Copies`_, `The Moves`_ and `All Five, Run`_.
   - ``move_noexcept``: `Why the Moves Are noexcept`_.
   - ``move_bug``: `Discussion: Who Deletes What?`_ It stops with a double-free report.
   - ``move_only``: :ref:`l8r5-default-delete`.

   ``702run week8_appendix`` with no key runs the code of every appendix frame of the slides, then every part of this page that is safe to run. It skips ``no_destructor``, ``double_free`` and ``move_bug``, the parts in ``undefined.cpp``, and prints the command that runs each one on its own.

Why It Matters for Vehicle
--------------------------

In the class diagram of Lecture 8, a filled diamond joins ``Vehicle`` to ``Sensor``: a ``Vehicle`` owns its ``Sensor``\ s. In C++, owning means that the ``Vehicle`` gives the memory of its ``Sensor``\ s back when its lifetime ends. The method that does it is the **destructor**, ``~Vehicle()``. It runs when an object's lifetime ends, and it gives back what the object owns (`Core Guidelines C.31 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-release>`__).

The destructor is one of five member functions that manage what a class owns. A ``Vehicle`` can also be copied, moved, or assigned from another ``Vehicle``, and each of those operations must leave every ``Sensor`` with one owner. These five are **special member functions**: when a class does not declare one, the compiler can write it for you. Here are their declarations, for a class named ``ClassName``:

.. code-block:: cpp

   ~ClassName();                                     // destructor
   ClassName(const ClassName& other);                // copy constructor
   ClassName& operator=(const ClassName& other);     // copy assignment
   ClassName(ClassName&& other) noexcept;            // move constructor
   ClassName& operator=(ClassName&& other) noexcept; // move assignment

- The **destructor** gives back what the object owns.
- The **copy constructor** makes a new object from an existing object of the same class.
- The **copy assignment** gives an object that already exists the value of another object, by copying it: ``copy = car_a;``.
- The **move constructor** makes a new object and takes what the source object owns, instead of copying it.
- The **move assignment** gives an object that already exists what the source object owns, by taking it.

The copies take a ``const&``. The moves take an rvalue reference, ``&&``, from L7.

Two rules say which of the five a class writes. The **rule of zero** is for a class whose members give back their own memory, as the ``Vehicle`` of the lecture does. The **rule of five** is for a class that calls ``new`` and ``delete`` itself.

Rule of Zero
------------

The **rule of zero**: a class whose members give back their own resources writes none of the five special member functions. The ones the compiler writes are right. A resource is something a class must give back, such as the heap memory of a ``Sensor``.

.. code-block:: cpp

   class Vehicle {  // one Sensor only, before sensors_
    public:
     explicit Vehicle(const Sensor& sensor)
         : sensor_{std::make_unique<Sensor>(sensor)} {}
     [[nodiscard]] const Sensor& get_sensor() const noexcept {
       return *sensor_;
     }

    private:
     std::unique_ptr<Sensor> sensor_;  // deletes the Sensor
   };

This ``Vehicle`` holds one ``Sensor`` only, before the lecture gives it ``sensors_``. Its data member ``sensor_`` is a ``std::unique_ptr<Sensor>`` (L7), and the class declares none of the five.

.. note::

   "If you can avoid defining default operations, do". Rule: `Core Guidelines C.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-zero>`__.

What the Compiler Writes Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Vehicle car_b{Sensor{2, SensorType::camera, 80.0}};  // one Sensor only
   Vehicle moved{std::move(car_b)};  // OK: moves the unique_ptr
   std::cout << moved.get_sensor().get_id() << '\n';  // 2
   Vehicle copy{moved};  // does not compile

The last line does not compile. g++ 13.3 (``-std=c++20 -Wall -Wextra``) says:

.. code-block:: text

   error: use of deleted function 'Vehicle::Vehicle(const Vehicle&)'
   note: 'Vehicle::Vehicle(const Vehicle&)' is implicitly deleted because the
         default definition would be ill-formed:

In the repository, the class is in namespace ``destructors::zero``, so the real message names ``destructors::zero::Vehicle``. Run the code with ``702run week8_appendix zero``. The message goes on to name the reason: ``use of deleted function`` for the copy constructor of ``std::unique_ptr<Sensor>``.

The compiler's destructor destroys the ``std::unique_ptr``, and the ``std::unique_ptr`` deletes the ``Sensor``. The compiler's move constructor moves the ``std::unique_ptr``, so ``moved`` now owns the ``Sensor`` with id 2, and the program prints 2. Built with AddressSanitizer, the run reports no leak.

The compiler cannot copy a ``std::unique_ptr`` (L7), so it writes no copy for ``Vehicle``. A ``Vehicle`` is **move-only**: you can move it, but you cannot copy it. So no two ``Vehicle``\ s can own one ``Sensor``.

The ``Vehicle`` of the lecture, whose ``sensors_`` is a ``std::vector<std::unique_ptr<Sensor>>``, follows the same rule: it writes none of the five, and copying it does not compile (the lecture's "Many Sensors" section).

A raw pointer does not delete what it points at. A class that owns memory through a raw pointer must write all five functions itself, or delete them: the rule of five. The rest of this page builds that class one step at a time.

A Class That Owns Memory
------------------------

.. code-block:: cpp

   class Vehicle {  // a Sensor on the heap
    public:
     explicit Vehicle(const Sensor& sensor)
         : sensor_{new Sensor{sensor}} {}
     ~Vehicle() {
       std::cout << "~Vehicle: sensor "
                 << sensor_->get_id()
                 << '\n';
       delete sensor_;
     }

    private:
     Sensor* sensor_;
   };

.. code-block:: cpp

   {
     Vehicle car_a{Sensor{1}};
     Vehicle car_b{Sensor{2}};
   }
   auto spare_car{
     std::make_unique<Vehicle>(
         Sensor{3})};
   spare_car.reset();

.. code-block:: text

   ~Vehicle: sensor 2
   ~Vehicle: sensor 1
   ~Vehicle: sensor 3

This ``Vehicle`` keeps its ``Sensor`` on the heap through a raw pointer, ``Sensor* sensor_``. The constructor calls ``new``, so the destructor must call ``delete``: a raw pointer gives nothing back by itself. The destructor also prints the id of the ``Sensor`` it deletes, so you can see when it runs.

The output follows the order of the lecture's "When It Runs" section. At the end of the scope, ``car_b`` is destroyed first and ``car_a`` second, the reverse of the order they were created. The ``Vehicle`` of ``spare_car`` is destroyed when ``reset()`` lets go of it. The code is in namespace ``raw_owner`` in ``appendix/src/appendix.cpp``: ``702run week8_appendix raw_owner``.

.. note::

   The course does not write classes like this one. "Avoid calling ``new`` and ``delete`` explicitly". Rule: `Core Guidelines R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`__. A ``std::unique_ptr`` member does the ``delete`` (`Rule of Zero`_).

Without the Destructor
^^^^^^^^^^^^^^^^^^^^^^

Remove ``~Vehicle`` from this class, and nothing calls ``delete``. Each ``Sensor`` stays on the heap after its ``Vehicle`` is gone, and no pointer to it is left. That is a **memory leak**: memory the program allocated and never gives back.

The class without its destructor is in namespace ``undefined::no_destructor`` in ``undefined/src/undefined.cpp``, built with ``-fsanitize=address``: ``702run week8_appendix no_destructor``. When the program ends, LeakSanitizer, the leak checker that comes with ``-fsanitize=address``, prints this report. Lines starting with ``...`` are cut, and ``0x...`` stands for an address that changes from run to run:

.. code-block:: text

   ERROR: LeakSanitizer: detected memory leaks
   Direct leak of 16 byte(s) in 1 object(s) allocated from:
       #0 0x... in operator new(unsigned long)
       #1 0x... in undefined::no_destructor::Vehicle::Vehicle(Sensor const&)
                   .../undefined/src/undefined.cpp:28
       #2 0x... in undefined::no_destructor::run()
                   .../undefined/src/undefined.cpp:37
       ...
   (two more blocks like it, one for each Vehicle)
   SUMMARY: AddressSanitizer: 48 byte(s) leaked in 3 allocation(s).

Line 28 of ``undefined.cpp`` is the constructor's ``new``. 16 bytes is one ``Sensor``: a 4-byte ``int`` (its id), a 4-byte ``SensorType`` and an 8-byte ``double`` (its range). Three ``Vehicle``\ s leave three blocks that are never given back: 3 × 16 = 48 bytes.

Copying an Owner
----------------

The **copy constructor** is the constructor that makes a new object from an existing object of the same class: ``Vehicle(const Vehicle& other)``. If a class declares none, the compiler writes one that copies each member.

.. code-block:: cpp

   Vehicle car_b{Sensor{2, SensorType::camera, 80.0}};
   Vehicle copy{car_b};  // the compiler's copy constructor

Take the ``Vehicle`` of `A Class That Owns Memory`_, without the print in its destructor. It holds a pointer, so the compiler's copy constructor copies the **address**, not the ``Sensor``. Now two ``Vehicle``\ s hold one ``Sensor``. At the end of the scope, both destructors run, and both ``delete`` the same address.

Deleting the same memory twice is a **double free**. It is undefined behavior (L2): the C++ rules do not say what the program does next.

Double Free, Measured
^^^^^^^^^^^^^^^^^^^^^

The code is in namespace ``undefined::double_free`` in ``undefined/src/undefined.cpp``: ``702run week8_appendix double_free``. AddressSanitizer stops the program with this report (lines cut as before):

.. code-block:: text

   ERROR: AddressSanitizer: attempting double-free on 0x... in thread T0:
       #0 0x... in operator delete(void*, unsigned long)
       #1 0x... in undefined::double_free::Vehicle::~Vehicle() .../undefined.cpp:55
       #2 0x... in undefined::double_free::run() .../undefined.cpp:68
   0x... is located 0 bytes inside of 16-byte region [0x...,0x...)
   freed by thread T0 here:
       #0 0x... in operator delete(void*, unsigned long)
       #1 0x... in undefined::double_free::Vehicle::~Vehicle() .../undefined.cpp:55
   previously allocated by thread T0 here:
       #0 0x... in operator new(unsigned long)
       #1 0x... in undefined::double_free::Vehicle::Vehicle(Sensor const&)
                   .../undefined.cpp:54
   SUMMARY: AddressSanitizer: double-free ...

``copy`` was created last, so its destructor runs first and frees the block. ``car_b``'s destructor then frees it again: undefined behavior, which AddressSanitizer stops, as with L7's double ``delete``. In ``undefined.cpp``, line 55 is the destructor's ``delete``, line 54 is the constructor's ``new``, and line 68 is the end of ``run()``, where both destructors run. The 16-byte region is the one ``Sensor``.

The class here has no print in its destructor. With the print, ``car_b``'s destructor reads the freed ``Sensor`` before it deletes it, and AddressSanitizer reports a ``heap-use-after-free`` instead: a read of memory that was already given back.

Rule of Five
------------

The **rule of five**: a class that needs its own destructor needs its own copy and move operations too, or must delete them. Those are the five special member functions of `Why It Matters for Vehicle`_.

An **assignment** gives a new value to an object that already exists: ``copy = car_a;``. That is why the class needs a copy assignment and a move assignment, beside the two constructors.

.. note::

   "If you define or ``=delete`` any copy, move, or destructor function, define or ``=delete`` them all". Rule: `Core Guidelines C.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-five>`__.

The sections below write the four missing functions for the raw-pointer ``Vehicle``. The whole class is in namespace ``five`` in ``appendix/src/appendix.cpp``.

The Copies
^^^^^^^^^^

.. code-block:: cpp

   Vehicle(const Vehicle& other)  // a new Sensor with other's values, if any
       : sensor_{other.sensor_ != nullptr ? new Sensor{*other.sensor_} : nullptr} {}

   Vehicle& operator=(const Vehicle& other) {
     if (this != &other) {  // v = v must not delete its own Sensor
       // Copy first: if new throws, this Vehicle keeps its old Sensor.
       Sensor* copy{other.sensor_ != nullptr ? new Sensor{*other.sensor_} : nullptr};
       delete sensor_;  // give back what we owned
       sensor_ = copy;
     }
     return *this;
   }

The copy constructor makes a second ``Sensor`` with the values of ``other``'s, so each ``Vehicle`` owns its own. A copy that copies what the object owns, not only the pointer to it, is a **deep copy**. A ``Vehicle`` that was moved from owns no ``Sensor``: its ``sensor_`` is ``nullptr`` (`The Moves`_, below). Reading ``*other.sensor_`` would then go through a null pointer, which is undefined behavior, so the copy of such a ``Vehicle`` owns no ``Sensor`` either.

The copy assignment makes the new ``Sensor`` first, then deletes the one this ``Vehicle`` owned and keeps the new one. In that order, if ``new`` fails and throws, the ``Vehicle`` still has its old ``Sensor``. The check ``this != &other`` skips ``v = v;``, which would otherwise copy a ``Sensor`` onto itself (Core Guidelines C.62). Like the copy constructor, it works when either ``Vehicle`` was moved from. With AddressSanitizer and UndefinedBehaviorSanitizer on, copying from a moved-from ``Vehicle``, copying into one, and ``v = v;`` run with no report. The assignment returns ``*this``, the object itself, as in the lecture's "Returning ``*this``" section.

Both functions read ``other.sensor_``, a ``private`` member of another object. A method may use the ``private`` members of any object of its own class.

The Moves
^^^^^^^^^

.. code-block:: cpp

   Vehicle(Vehicle&& other) noexcept : sensor_{other.sensor_} {
     other.sensor_ = nullptr;  // the source owns nothing now
   }

   Vehicle& operator=(Vehicle&& other) noexcept {
     if (this != &other) {   // v = std::move(v) must not delete
       delete sensor_;       // give back what we owned
       sensor_ = other.sensor_;
       other.sensor_ = nullptr;
     }
     return *this;
   }

A move takes the pointer and leaves the source null. It makes no new ``Sensor``, in the same way that ``std::vector``'s move took its block in L7.

The move assignment first gives back the ``Sensor`` it owned, then takes ``other``'s. The test ``this != &other`` compares the address of this object with the address of the source. When they are the same object, as in ``v = std::move(v)``, the test skips the body, so the move does not delete the ``Sensor`` it is about to take.

Later, the moved-from ``Vehicle``'s destructor deletes a null pointer, which C++ allows:

.. note::

   "In a single-object delete expression, the value of the operand of delete may be a null pointer value, a pointer to a non-array object created by a previous new-expression, or a pointer to a subobject (6.7.2) representing a base class of such an object (11.7)". C++20 **[expr.delete]** (7.6.2.8) paragraph 2. Paragraph 6 makes the call of the destructor depend on the pointer: "If the value of the operand of the delete-expression is not a null pointer value ..., the delete-expression will invoke the destructor (if any)".

Neither move can throw, so both are ``noexcept`` (Core Guidelines C.66). The next section shows why that matters.

Why the Moves Are noexcept
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int copies{0};
   int moves{0};
   class Vehicle {  // counts its copies and moves
    public:
     Vehicle() = default;
     Vehicle(const Vehicle&) { ++copies; }
     Vehicle(Vehicle&&) noexcept { ++moves; }
   };

   std::vector<Vehicle> fleet;
   for (int i{0}; i < 5; ++i) {
     fleet.emplace_back();
   }  // with noexcept: 0 copies, 7 moves. Without it: 7 copies, 0 moves

This ``Vehicle`` owns nothing. It only counts how often it is copied and moved. ``fleet.emplace_back()`` builds a new ``Vehicle`` at the end of the vector. When the vector is full, it gets a bigger block of memory and brings each old element into it, by a move or by a copy.

The program in namespace ``move_noexcept`` of ``appendix/src/appendix.cpp`` (``702run week8_appendix move_noexcept``) runs the loop twice: once with the move constructor ``noexcept``, once without it. It uses a template parameter for that, so both cases fit in one program. It prints:

.. code-block:: text

   with noexcept: 0 copies, 7 moves
   without it: 7 copies, 0 moves

With g++ 13.3, the vector's capacity after each of the five calls is 1, 2, 4, 4, 8 (measured with ``fleet.capacity()``). So the vector grows to 1, 2, 4, then 8 places, and brings along 1, 2, then 4 old elements: 1 + 2 + 4 = 7 moves or copies.

A move that throws halfway would leave the old block half empty. So the vector copies its elements unless the move is ``noexcept``. For the raw-pointer ``Vehicle``, the difference is a new ``Sensor`` for each element: a copy makes a new ``Sensor`` (`The Copies`_), and a move takes the pointer (`The Moves`_).

All Five, Run
^^^^^^^^^^^^^

.. code-block:: cpp

   Vehicle car_b{Sensor{2}};
   Vehicle copy{car_b};
   // copy: sensor 2, own Sensor: true
   Vehicle car_a{Sensor{1}};
   copy = car_a;
   // after copy assignment: sensor 1
   Vehicle moved{std::move(car_b)};
   // moved: sensor 2
   car_a = std::move(moved);
   // after move assignment: sensor 2

The class is in namespace ``five`` in ``appendix/src/appendix.cpp``: ``702run week8_appendix five``. Its ``~Vehicle`` prints as in `A Class That Owns Memory`_, and prints 0 when the ``Vehicle`` owns nothing. Its ``run()`` prints each comment above as a line, then the destructors print at the end of the scope:

.. code-block:: text

   copy: sensor 2, own Sensor: true
   after copy assignment: sensor 1
   moved: sensor 2
   after move assignment: sensor 2
   ~Vehicle: sensor 0
   ~Vehicle: sensor 2
   ~Vehicle: sensor 1
   ~Vehicle: sensor 0

"own Sensor: true" says that ``copy``'s ``Sensor`` is at a different address than ``car_b``'s: the copy constructor made a second ``Sensor``.

The four objects are destroyed in the reverse order they were created: ``moved``, ``car_a``, ``copy``, then ``car_b``. ``moved`` and ``car_b`` were moved from, so they print 0: they own no ``Sensor``. ``car_a`` holds sensor 2, and ``copy`` holds sensor 1.

Run with AddressSanitizer, the program reports no leak and no double free. Three ``Sensor``\ s were created on the heap, by ``car_b``, ``copy`` and ``car_a``. The move assignment deleted ``car_a``'s own. The two others were deleted at the end of the scope.

Discussion: Who Deletes What?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   Vehicle& operator=(Vehicle&& other) noexcept {
     delete sensor_;
     sensor_ = other.sensor_;
     return *this;
   }

   Vehicle car_a{Sensor{1}};
   Vehicle car_b{Sensor{2}};
   car_a = std::move(car_b);

One line is missing from this move assignment. Draw ``car_a``, ``car_b`` and the ``Sensor``\ s on paper after line 9. Who deletes what at the end of the scope?

Then: what does ``car_a = std::move(car_a);`` do?

.. dropdown:: Answers
   :class-container: sd-border-success

   After line 9, the ``Sensor`` with id 1 is gone, and ``car_a`` and ``car_b`` both point at the ``Sensor`` with id 2. At the end of the scope, ``car_b``'s destructor deletes it, then ``car_a``'s deletes it again. AddressSanitizer reports ``attempting double-free``. The code is in namespace ``undefined::move_bug`` in ``undefined/src/undefined.cpp``: ``702run week8_appendix move_bug``.

   The missing line is ``other.sensor_ = nullptr;``. With it, a self-move still breaks: ``other`` is ``car_a`` itself, so the ``Sensor`` is deleted and the pointer is set to null. g++ warns about the line with ``-Wself-move``, which ``-Wall`` turns on. ``car_a`` is left with a null ``sensor_``: it has lost its ``Sensor``, and reading ``*sensor_`` after that is undefined behavior. The test ``if (this != &other)`` in `The Moves`_ skips the body.

.. _l8r5-default-delete:

``= default`` and ``= delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class Vehicle {  // the raw-pointer Vehicle, move-only on purpose
    public:
     ~Vehicle() { delete sensor_; }
     Vehicle(const Vehicle&) = delete;             // no copies
     Vehicle& operator=(const Vehicle&) = delete;
     Vehicle(Vehicle&& other) noexcept;            // the moves, as before
     Vehicle& operator=(Vehicle&& other) noexcept;
     // ...
   };

``= delete`` says that the operation does not exist, and a call to it is a compile error: ``use of deleted function 'Vehicle::Vehicle(const Vehicle&)'``. This ``Vehicle`` deletes its copies and keeps the moves of `The Moves`_, so it is move-only on purpose, as the ``Vehicle`` of `Rule of Zero`_ is. The class is in namespace ``move_only`` in ``appendix/src/appendix.cpp``: ``702run week8_appendix move_only``.

``= default`` asks for the version the compiler would write, for example ``Vehicle(Vehicle&&) = default;``.

Declaring the copies stops the compiler from writing the moves. Leave out the two move lines, and ``Vehicle moved{std::move(car_b)};`` picks the deleted copy constructor. It does not compile. g++ 13.3 says, for the class in the repository:

.. code-block:: text

   error: use of deleted function 'move_only::Vehicle::Vehicle(const move_only::Vehicle&)'

That is the reason C.21 asks for all five.

Which Rule to Follow
--------------------

Follow the **rule of zero** by default. Give a class members that give back their own resources, such as a ``std::unique_ptr`` or a ``std::vector`` of ``std::unique_ptr``, and write none of the five special member functions. The compiler writes the right ones (Core Guidelines C.20). The ``Vehicle`` of the lecture does this.

Follow the **rule of five** only for a class that manages a resource by hand, such as heap memory through a raw pointer. Such a class writes all five, or deletes the ones it must not have with ``= delete`` (Core Guidelines C.21). The course does not write such classes (Core Guidelines R.11): a ``std::unique_ptr`` member does the ``delete``.
