.. _l8_rule_of_five:

====================================================
Rule of Five and Rule of Zero
====================================================

This page is **required reading** after the Lecture 8 class. It is not presented in class. In class, a ``Vehicle`` owns its ``Sensor``\ s through ``std::unique_ptr`` and writes no destructor, no copy and no move: it follows the **rule of zero**. This page shows why that works. It then builds a ``Vehicle`` that owns its ``Sensor`` through a raw pointer, a plain ``Sensor*``, and shows what goes wrong until the class writes five functions itself: the **rule of five**.

.. dropdown:: Code for This Page
   :icon: terminal
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Every listing on this page is in the course repository, under ``project/week8/``. Each listing shows the line numbers of its file, so "line 170" on this page is line 170 of the file named above the listing.

   - ``playground/src/destructors.cpp``: the ``Vehicle`` of `Rule of Zero`_.
   - ``appendix/src/appendix.cpp``: the code that runs without errors.
   - ``undefined/src/undefined.cpp``: the code that leaks memory or deletes it twice. The build always compiles this file with **AddressSanitizer** (``-fsanitize=address``), a checker that stops the program and prints a report when it deletes memory twice, and reports a leak when the program ends.

   Most parts of this page use a class named ``Vehicle``. Each of these classes sits in its own **namespace**, such as ``five``, so that they do not clash. A compiler message names a class with its namespace: ``five::Vehicle``, or ``destructors::zero::Vehicle``.

   All the code runs in one program, ``week8_appendix``. Each part of this page has a name, its **key**, which is the name of its namespace. Build the program, then run one part by its key, with the ``702`` commands of the :doc:`lecture page <l8_lecture>`:

   .. code-block:: bash

      702build week8_appendix
      702run week8_appendix five

   The keys, in the order of this page:

   - ``which_one``: `Which Function Runs`_.
   - ``zero``: `What the Compiler Writes Now`_.
   - ``raw_owner``: `A Class That Owns Memory`_.
   - ``no_destructor``: `Without the Destructor`_. It ends with a leak report.
   - ``double_free``: `Copying an Owner`_. It stops with a double-free report.
   - ``five``: `All Five, Run`_.
   - ``move_noexcept``: `Why the Moves Are noexcept`_.
   - ``no_move``: `Without the Moves`_. It stops with a double-free report.
   - ``move_bug``: `Discussion: Who Deletes What?`_ It stops with a double-free report.
   - ``move_only``: :ref:`l8r5-default-delete`.
   - ``file_owner``: `Beyond Memory: A File`_.

   ``702run week8_appendix`` with no key runs the code of every appendix frame of the slides, then every part of this page that is safe to run. It skips ``no_destructor``, ``double_free``, ``no_move`` and ``move_bug``, and prints the command that runs each one on its own.

Why It Matters for Vehicle
--------------------------

In the class diagram of the lecture, a filled diamond joins ``Vehicle`` to ``Sensor``: a ``Vehicle`` owns its ``Sensor``\ s. Owning means that the ``Vehicle`` gives the memory of its ``Sensor``\ s back when the ``Vehicle`` is destroyed.

Five member functions decide what happens to what a class owns. With the default constructor, C++ calls them the six **special member functions**. Here are the declarations of the five, for a class named ``ClassName``:

.. code-block:: cpp

   ~ClassName();                                     // destructor
   ClassName(const ClassName& other);                // copy constructor
   ClassName& operator=(const ClassName& other);     // copy assignment
   ClassName(ClassName&& other) noexcept;            // move constructor
   ClassName& operator=(ClassName&& other) noexcept; // move assignment

- The **destructor** runs when an object is destroyed. It gives back what the object owns.
- The **copy constructor** makes a new object from an existing object of the same class.
- The **copy assignment** gives an object that already exists the value of another object, by copying it: ``copy = car_a;``.
- The **move constructor** makes a new object and takes what the source object owns, instead of copying it.
- The **move assignment** gives an object that already exists what the source object owns, by taking it.

The copies take a ``const ClassName&``: they read ``other`` and leave it unchanged. The moves take a ``ClassName&&``, an **rvalue reference**: it binds to an object whose contents may be taken, such as ``std::move(car_b)``. ``std::move`` moves nothing by itself. It marks ``car_b`` as an object you are done with, so the compiler picks the move constructor or the move assignment.

.. note::

   "Default constructors (11.4.4.1), copy constructors, move constructors (11.4.4.2), copy assignment operators, move assignment operators (11.4.5), and prospective destructors (11.4.6) are special member functions". C++20 **[special]** (11.4.3) paragraph 1.

.. important::

   **If you do not write them, the compiler does.** A class that declares none of the five still has all five, because the compiler writes each one. This holds for the destructor too: a class without a destructor of its own gets one from the compiler.

   Each function the compiler writes works one data member at a time. Its destructor destroys each data member. Its copy constructor copies each data member, and its move constructor moves each one. The two assignments do the same for an object that already exists.

   "If a class has no user-declared prospective destructor, a prospective destructor is implicitly declared as defaulted". C++20 **[class.dtor]** (11.4.6) paragraph 2. A **prospective destructor** is the standard's name for a destructor declaration.

   "The implicitly-defined copy/move constructor for a non-union class X performs a memberwise copy/move of its bases and members". C++20 **[class.copy.ctor]** (11.4.4.2) paragraph 14.

Which Function Runs
^^^^^^^^^^^^^^^^^^^

Before you write any of the five, learn which line of code calls which one. This ``Vehicle`` owns nothing. Each of its special member functions prints its own name and the id of the object, so a run shows which one each line calls. A move sets the id of its source to 0 (lines 281 and 286), the way a real move leaves its source owning nothing.

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 266 to 294
   :lineno-start: 266

   class Vehicle {
    public:
     explicit Vehicle(int id) : id_{id} {
       std::cout << "  constructor, id " << id_ << '\n';
     }
     ~Vehicle() { std::cout << "  destructor, id " << id_ << '\n'; }
     Vehicle(const Vehicle& other) : id_{other.id_} {
       std::cout << "  copy constructor, id " << id_ << '\n';
     }
     Vehicle& operator=(const Vehicle& other) {
       id_ = other.id_;
       std::cout << "  copy assignment, id " << id_ << '\n';
       return *this;
     }
     Vehicle(Vehicle&& other) noexcept : id_{other.id_} {
       other.id_ = 0;  // as if the source gave its contents away
       std::cout << "  move constructor, id " << id_ << '\n';
     }
     Vehicle& operator=(Vehicle&& other) noexcept {
       id_ = other.id_;
       other.id_ = 0;
       std::cout << "  move assignment, id " << id_ << '\n';
       return *this;
     }
     [[nodiscard]] int get_id() const noexcept { return id_; }

    private:
     int id_;
   };

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 296 to 318
   :lineno-start: 296

   void park(Vehicle vehicle) {  // takes a Vehicle by value: a new object
     std::cout << "  park(), id " << vehicle.get_id() << '\n';
   }  // vehicle is destroyed here

   void run() {
     std::cout << "1: Vehicle car_a{1};\n";
     Vehicle car_a{1};
     std::cout << "2: Vehicle car_b{2};\n";
     Vehicle car_b{2};
     std::cout << "3: Vehicle copy{car_a};\n";
     Vehicle copy{car_a};
     std::cout << "4: Vehicle other = car_a;\n";
     Vehicle other = car_a;
     std::cout << "5: copy = car_b;\n";
     copy = car_b;
     std::cout << "6: Vehicle moved{std::move(car_a)};\n";
     Vehicle moved{std::move(car_a)};
     std::cout << "7: moved = std::move(car_b);\n";
     moved = std::move(car_b);
     std::cout << "8: park(copy);\n";
     park(copy);
     std::cout << "9: end of run()\n";
   }

``702run week8_appendix which_one`` prints each line of ``run()`` before it runs it, then what that line called:

.. code-block:: text

   1: Vehicle car_a{1};
     constructor, id 1
   2: Vehicle car_b{2};
     constructor, id 2
   3: Vehicle copy{car_a};
     copy constructor, id 1
   4: Vehicle other = car_a;
     copy constructor, id 1
   5: copy = car_b;
     copy assignment, id 2
   6: Vehicle moved{std::move(car_a)};
     move constructor, id 1
   7: moved = std::move(car_b);
     move assignment, id 2
   8: park(copy);
     copy constructor, id 2
     park(), id 2
     destructor, id 2
   9: end of run()
     destructor, id 2
     destructor, id 1
     destructor, id 2
     destructor, id 0
     destructor, id 0

1. Lines 302 and 304 make each ``Vehicle`` from an id, with the constructor of line 268.
2. Line 306 makes a new ``Vehicle``, ``copy``, from ``car_a``: the copy constructor.
3. Line 308 has an ``=`` sign, but ``other`` does not exist before this line. A new object is made, so the copy constructor runs, not the copy assignment.
4. Line 310: ``copy`` already exists, so the copy assignment runs. ``copy`` now has id 2.
5. Line 312 makes ``moved`` from ``std::move(car_a)``: the move constructor. ``moved`` gets id 1, and ``car_a``'s id becomes 0.
6. Line 314: ``moved`` already exists, so the move assignment runs. ``moved`` gets id 2, and ``car_b``'s id becomes 0.
7. Line 316 passes ``copy`` to ``park()``, which takes its parameter **by value** (line 296): the parameter ``vehicle`` is a new ``Vehicle``, made by the copy constructor. It is destroyed at the end of ``park()``, line 298.
8. At the end of ``run()``, line 318, the five objects are destroyed in the reverse order they were created: ``moved`` (id 2), ``other`` (1), ``copy`` (2), ``car_b`` (0) and ``car_a`` (0).

.. tip::

   **Constructor or assignment?** Ask whether the object on the left of ``=`` exists yet. If the line creates it (``Vehicle other = car_a;``), a constructor runs. If it existed before the line (``copy = car_b;``), an assignment runs.

Two rules say which of the five a class writes. The **rule of zero** is for a class whose data members give back their own memory, as the ``Vehicle`` of the lecture does. The **rule of five** is for a class that calls ``new`` and ``delete`` itself.

Rule of Zero
------------

The **rule of zero**: when every data member of a class gives back its own resources, the class writes none of the five special member functions. The compiler provides default versions of all five, and they are enough. A **resource** is something a program must give back when it is done with it, such as memory on the heap.

The default versions are enough because each one calls the matching function of each data member. When a data member already destroys, copies and moves itself correctly, the class has nothing to add.

.. note::

   "If you can avoid defining default operations, do". Rule: `Core Guidelines C.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-zero>`__.

What the Compiler Writes Now
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This ``Vehicle`` holds one ``Sensor`` only, before the lecture gives it a ``std::vector`` of them. It writes none of the five.

.. code-block:: cpp
   :caption: ``playground/src/destructors.cpp``, lines 89 to 109
   :lineno-start: 89

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

   void run() {
     Vehicle car_b{Sensor{2, SensorType::camera, 80.0}};  // one Sensor only
     Vehicle moved{std::move(car_b)};  // OK: moves the unique_ptr
     std::cout << moved.get_sensor().get_id() << '\n';  // 2
     // Vehicle copy{moved};  // does not compile:
     // error: use of deleted function 'destructors::zero::Vehicle::Vehicle(const destructors::zero::Vehicle&)'
     // note: 'destructors::zero::Vehicle::Vehicle(const destructors::zero::Vehicle&)' is implicitly deleted because the
     //       default definition would be ill-formed:
   }

The ``Sensor`` is the lecture's class, in ``common/include/sensor.hpp``. It has three data members: ``id_``, ``type_`` (a ``SensorType``: lidar, camera or radar) and ``range_``, how far it sees, in m.

``sensor_`` (line 98) is a ``std::unique_ptr<Sensor>``, a smart pointer from ``<memory>``. It holds the address of a ``Sensor`` on the heap, and it follows two rules:

- When a ``std::unique_ptr`` is destroyed, it deletes the object it points at.
- A ``std::unique_ptr`` can be moved but not copied. A move hands the object over and leaves the source holding ``nullptr``. So one ``Sensor`` never has two owners.

Here is what each line of ``run()`` does with the functions the compiler wrote.

1. **Line 102** creates ``car_b``. Its constructor (lines 91 and 92) calls ``std::make_unique``, which creates a ``Sensor`` on the heap: id 2, a camera that sees 80.0 m. ``car_b.sensor_`` owns it.
2. **Line 103** creates ``moved`` from ``std::move(car_b)``. The compiler's move constructor moves each data member, so it moves ``car_b.sensor_`` into ``moved.sensor_``. The ``std::unique_ptr`` hands the ``Sensor`` over: ``moved.sensor_`` now holds its address, and ``car_b.sensor_`` holds ``nullptr``. No second ``Sensor`` is made.
3. **Line 104** reads the ``Sensor`` through ``moved`` and prints its id, 2.
4. **Line 105** is commented out because it does not compile: `Why Line 105 Does Not Compile`_, below.
5. **Line 109**, the end of ``run()``, destroys ``moved``, then ``car_b``. The compiler's destructor destroys ``sensor_``. ``moved``'s ``std::unique_ptr`` deletes the ``Sensor``; ``car_b``'s holds ``nullptr`` and deletes nothing. Run with AddressSanitizer, the program reports no leak.

.. figure:: /_static/images/l8/rof_zero_move.png
   :alt: Two Vehicle variables, car_b and moved, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_. car_b's sensor_ is marked nullptr and has no arrow. moved's sensor_ is marked a Sensor*. On the right, a red box with a heap icon and the word Heap holds one Sensor object of three rows: id_ 2, type_ SensorType::camera, range_ 80.0. A blue arrow runs from moved's sensor_ to the object's first row.
   :align: center
   :width: 100%

   After line 103. ``moved.sensor_`` owns the ``Sensor``, and ``car_b.sensor_`` holds ``nullptr``. Each blue box is a ``Vehicle`` on the stack; the red box is the heap, with the ``Sensor`` and its three data members. An arrow is an address: it ends on the object it points at.

Why Line 105 Does Not Compile
"""""""""""""""""""""""""""""

To copy a ``Vehicle``, the compiler's copy constructor would copy each data member, so it would copy ``sensor_``. A ``std::unique_ptr`` cannot be copied: its copy constructor is **deleted**, declared with ``= delete`` so that any call to it is a compile error. The compiler cannot write a copy that needs a deleted function, so it deletes the copy constructor of ``Vehicle`` too.

Uncomment line 105 and run ``702build week8_appendix``. g++ 13.3 (``-std=c++20 -Wall -Wextra``) prints this, with the folder names cut to ``...``:

.. code-block:: text
   :linenos:

   .../destructors.cpp:105:21: error: use of deleted function ‘destructors::zero::Vehicle::Vehicle(const destructors::zero::Vehicle&)’
     105 |   Vehicle copy{moved};  // does not compile:
         |                     ^
   .../destructors.cpp:89:7: note: ‘destructors::zero::Vehicle::Vehicle(const destructors::zero::Vehicle&)’ is implicitly deleted because the default definition would be ill-formed:
      89 | class Vehicle {  // one Sensor only, before sensors_
         |       ^~~~~~~
   .../destructors.cpp:89:7: error: use of deleted function ‘std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&) [with _Tp = Sensor; _Dp = std::default_delete<Sensor>]’
   .../unique_ptr.h:522:7: note: declared here
     522 |       unique_ptr(const unique_ptr&) = delete;
         |       ^~~~~~~~~~

Read it from the top. The numbers below are the lines of the message.

1. **Line 1.** Line 105, column 21, calls the copy constructor of ``Vehicle``, and that function is deleted. ``destructors::zero::`` is the namespace of the class in the repository.
2. **Line 4.** The compiler deleted that copy constructor on its own (**implicitly**), because the version it would write (the **default definition**) would not compile (it would be **ill-formed**). Line 89 is the class it belongs to.
3. **Line 7** gives the reason. The default copy constructor would call the copy constructor of ``std::unique_ptr``, and that one is deleted too. ``_Tp = Sensor`` says that the ``std::unique_ptr`` points at a ``Sensor``. ``_Dp = std::default_delete<Sensor>`` says how it gives the ``Sensor`` back: with ``delete``.
4. **Lines 8 to 10** show the line of the standard library that deletes the copy: ``unique_ptr(const unique_ptr&) = delete;``.

Comment line 105 out again before you go on.

.. important::

   **A class with a std::unique_ptr member is move-only.** You can move it, but you cannot copy it. The compiler enforces one owner per ``Sensor`` for you, without one line of code in the class.

The ``Vehicle`` of the lecture, whose ``sensors_`` is a ``std::vector<std::unique_ptr<Sensor>>``, follows the same rule. It writes none of the five, and copying it does not compile (Live Coding: Step 6 of the :doc:`lecture page <l8_lecture>`).

A Class That Owns Memory
------------------------

This ``Vehicle`` keeps its ``Sensor`` on the heap through a **raw pointer**, ``Sensor* sensor_`` (line 97). A raw pointer is a plain address, with no rule about who deletes what it points at.

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 85 to 109
   :lineno-start: 85

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

   void run() {
     {
       Vehicle car_a{Sensor{1}};
       Vehicle car_b{Sensor{2}};
     }
     auto spare_car{
       std::make_unique<Vehicle>(
           Sensor{3})};
     spare_car.reset();
   }  // prints ~Vehicle: sensor 2, then 1, then 3

The constructor calls ``new`` on line 88, so this class must call ``delete`` itself. The pointer does not do it for the class. When a ``Vehicle`` is destroyed, its ``sensor_`` is destroyed too, but destroying a pointer only throws away the address it holds. The ``Sensor`` at that address stays on the heap. So the destructor, lines 89 to 94, calls ``delete sensor_`` on line 93. It also prints the id of the ``Sensor`` first, so you can see when it runs.

``702run week8_appendix raw_owner`` prints:

.. code-block:: text

   ~Vehicle: sensor 2
   ~Vehicle: sensor 1
   ~Vehicle: sensor 3

- Lines 102 and 103 create ``car_a`` and ``car_b`` inside the block that opens on line 101. At the closing brace of the block, line 104, both are destroyed, in the reverse order they were created: ``car_b`` first, then ``car_a``.
- Lines 105 to 107 create a third ``Vehicle``, on the heap, with ``std::make_unique``. ``spare_car``, a ``std::unique_ptr<Vehicle>``, owns it. Line 108 calls ``reset()``, which tells ``spare_car`` to let go: it deletes the ``Vehicle`` right then, and the ``Vehicle``'s destructor runs.

.. admonition:: Why Learn a Class the Course Does Not Write?
   :class: important

   In this course, a ``std::unique_ptr`` member does the ``delete``, and your classes follow the rule of zero. "Avoid calling ``new`` and ``delete`` explicitly". Rule: `Core Guidelines R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`__. You still need the rule of five, for two reasons.

   - **Someone writes the class that owns.** ``std::unique_ptr``, ``std::vector`` and ``std::string`` are classes that own memory and write their own special member functions. Knowing what they do inside tells you what a copy or a move of them costs.
   - **Not every resource is memory, and not every resource has a class in the standard library.** A C library gives you a **handle**, a value that names the resource, and a function to give it back. ``std::fopen`` opens a file and ``std::fclose`` closes it. ``sqlite3_open`` opens a connection to an SQLite database and ``sqlite3_close`` closes it. On Linux, ``open`` opens the serial port of a robot's motor driver and ``close`` closes it. A class that holds such a handle must give it back exactly once, so it follows the rule of five. `Beyond Memory: A File`_ writes one.

Without the Destructor
^^^^^^^^^^^^^^^^^^^^^^

Remove ``~Vehicle`` from the class, and the compiler writes a destructor instead. That destructor destroys each data member, and the only data member is ``sensor_``, a raw pointer. Destroying a pointer does not delete what it points at, so nothing calls ``delete``.

.. code-block:: cpp
   :caption: ``undefined/src/undefined.cpp``, lines 25 to 43
   :lineno-start: 25

   class Vehicle {  // a Sensor on the heap, never given back
    public:
     explicit Vehicle(const Sensor& sensor)
         : sensor_{new Sensor{sensor}} {}

    private:
     Sensor* sensor_;
   };

   void run() {
     {
       Vehicle car_a{Sensor{1}};
       Vehicle car_b{Sensor{2}};
     }
     auto spare_car{
       std::make_unique<Vehicle>(
           Sensor{3})};
     spare_car.reset();
   }

.. warning::

   **The compiler's destructor is not enough for a raw pointer.** It destroys the pointer, not the object the pointer points at. A class that gets memory with ``new`` must write a destructor that calls ``delete``.

Each ``Sensor`` stays on the heap after its ``Vehicle`` is gone, and no pointer to it is left. That is a **memory leak**: memory the program got and never gives back. When the program ends, LeakSanitizer, the leak checker that comes with AddressSanitizer, prints this report for ``702run week8_appendix no_destructor``. Lines starting with ``...`` are cut, and ``0x...`` stands for an address that changes from run to run:

.. code-block:: text

   ERROR: LeakSanitizer: detected memory leaks

   Direct leak of 16 byte(s) in 1 object(s) allocated from:
       #0 0x... in operator new(unsigned long)
       #1 0x... in undefined::no_destructor::Vehicle::Vehicle(Sensor const&) .../undefined.cpp:28
       #2 0x... in undefined::no_destructor::run() .../undefined.cpp:37
       ...
   (two more blocks like it, one for each Vehicle)

   SUMMARY: AddressSanitizer: 48 byte(s) leaked in 3 allocation(s).

- Read each block from the top: ``#0`` is the call that got the memory, ``operator new``. ``#1`` is the function that called it: the constructor's ``new``, on line 28. ``#2`` called ``#1``: line 37 created ``car_b``.
- The two other blocks point at line 41, the ``Vehicle`` of ``spare_car``, and at line 36, ``car_a``.
- 16 bytes is one ``Sensor``, measured with ``sizeof(Sensor)`` (g++ 13.3, x86-64): a 4-byte ``int`` (its id), a 4-byte ``SensorType`` and an 8-byte ``double`` (its range). Three ``Vehicle``\ s leave three blocks behind: 3 × 16 = 48 bytes.

Copying an Owner
----------------

Put the destructor back, without its print. This ``Vehicle`` declares no copy constructor, so the compiler writes one. That copy constructor copies each data member, and ``sensor_`` is an address: it copies the **address**, not the ``Sensor``.

.. code-block:: cpp
   :caption: ``undefined/src/undefined.cpp``, lines 51 to 68
   :lineno-start: 51

   class Vehicle {  // a Sensor on the heap
    public:
     explicit Vehicle(const Sensor& sensor)
         : sensor_{new Sensor{sensor}} {}
     ~Vehicle() { delete sensor_; }
     [[nodiscard]] const Sensor& get_sensor() const noexcept {
       return *sensor_;
     }

    private:
     Sensor* sensor_;
   };

   void run() {
     Vehicle car_b{Sensor{2, SensorType::camera, 80.0}};
     Vehicle copy{car_b};  // the compiler's copy constructor
     std::cout << copy.get_sensor().get_id() << '\n';  // 2
   }  // copy's destructor deletes the Sensor, then car_b's deletes it again

After line 66, two ``Vehicle``\ s point at one ``Sensor``. A copy that copies only the address is a **shallow copy**.

.. figure:: /_static/images/l8/rof_compiler_copy.png
   :alt: Two Vehicle variables, car_b and copy, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. On the right, a red box with a heap icon and the word Heap holds one Sensor object of three rows: id_ 2, type_ SensorType::camera, range_ 80.0. Two blue arrows, one from each sensor_, end on the same object, at its first row.
   :align: center
   :width: 100%

   After line 66. The compiler's copy constructor copied the address in ``car_b.sensor_``, so ``car_b`` and ``copy`` point at the same ``Sensor``.

At the end of ``run()``, line 68, ``copy`` is destroyed first, since it was created last. Its destructor deletes the ``Sensor``. Then ``car_b``'s destructor deletes the same address again. Deleting the same memory twice is a **double free**. It is **undefined behavior**: the C++ standard sets no rule for what the program does next. It can crash at once, crash much later, or seem to work.

Double Free, Measured
^^^^^^^^^^^^^^^^^^^^^

``702run week8_appendix double_free`` prints 2 (line 67), then AddressSanitizer stops the program with this report (lines cut as before):

.. code-block:: text

   ERROR: AddressSanitizer: attempting double-free on 0x... in thread T0:
       #0 0x... in operator delete(void*, unsigned long)
       #1 0x... in undefined::double_free::Vehicle::~Vehicle() .../undefined.cpp:55
       #2 0x... in undefined::double_free::run() .../undefined.cpp:68
       ...
   0x... is located 0 bytes inside of 16-byte region [0x...,0x...)
   freed by thread T0 here:
       #0 0x... in operator delete(void*, unsigned long)
       #1 0x... in undefined::double_free::Vehicle::~Vehicle() .../undefined.cpp:55
       #2 0x... in undefined::double_free::run() .../undefined.cpp:68
       ...
   previously allocated by thread T0 here:
       #0 0x... in operator new(unsigned long)
       #1 0x... in undefined::double_free::Vehicle::Vehicle(Sensor const&) .../undefined.cpp:54
       #2 0x... in undefined::double_free::run() .../undefined.cpp:65
       ...
   SUMMARY: AddressSanitizer: double-free ...

The report has three parts.

1. **attempting double-free**: the second ``delete``, in the destructor (line 55), called at the end of ``run()`` (line 68). This is ``car_b``'s destructor.
2. **freed by thread T0 here**: the first ``delete`` of the same 16 bytes, also line 55 from line 68. This is ``copy``'s destructor.
3. **previously allocated by thread T0 here**: where the memory came from, the ``new`` on line 54, called when line 65 created ``car_b``. The 16-byte region is the one ``Sensor``.

Rule of Five
------------

The **rule of five**: a class that needs its own destructor also needs its own copy constructor, copy assignment, move constructor and move assignment. Or it deletes the ones it must not have, with ``= delete`` (:ref:`l8r5-default-delete`).

.. note::

   "If you define or ``=delete`` any copy, move, or destructor function, define or ``=delete`` them all". Rule: `Core Guidelines C.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-five>`__.

The class with all five is ``five::Vehicle``, lines 120 to 165 of ``appendix/src/appendix.cpp``. Its constructor and its destructor are those of `A Class That Owns Memory`_, with one change: the destructor prints 0 when the ``Vehicle`` owns no ``Sensor`` (line 126). The sections below go through the four other functions.

The Copies
^^^^^^^^^^

The Copy Constructor
""""""""""""""""""""

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 132 to 133
   :lineno-start: 132

     Vehicle(const Vehicle& other)  // a new Sensor with other's values, if any
         : sensor_{other.sensor_ != nullptr ? new Sensor{*other.sensor_} : nullptr} {}

Here is what each part of it does.

- ``Vehicle(const Vehicle& other)``: a constructor whose parameter is another ``Vehicle``. ``other`` is the ``Vehicle`` to copy. It comes by ``const`` reference: the copy constructor reads it and does not change it.
- ``: sensor_{...}``: the member initializer list sets ``sensor_`` to the value inside the braces.
- ``condition ? a : b`` is the **conditional operator**: its value is ``a`` when ``condition`` is true, and ``b`` otherwise.
- The condition, ``other.sensor_ != nullptr``, asks whether ``other`` owns a ``Sensor``. A ``Vehicle`` that was moved from does not: its ``sensor_`` is ``nullptr`` (`The Move Constructor`_).
- If it does, ``*other.sensor_`` is the ``Sensor`` that ``other`` points at, and ``new Sensor{*other.sensor_}`` creates a new ``Sensor`` on the heap with the same id, type and range. Its address goes into ``sensor_``.
- If it does not, ``sensor_`` is ``nullptr`` too. Without the test, ``*other.sensor_`` would read through a null pointer, which is undefined behavior.

So each ``Vehicle`` owns its own ``Sensor``. A copy that copies what the object owns, not only the address of it, is a **deep copy**. Line 170 of ``run()`` uses it: ``Vehicle copy{car_b};``.

.. figure:: /_static/images/l8/rof_deep_copy.png
   :alt: Two Vehicle variables, car_b and copy, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. On the right, a red box with a heap icon and the word Heap holds two Sensor objects with the same three rows: id_ 2, type_ SensorType::lidar, range_ 100.0. A blue arrow runs from car_b's sensor_ to the upper object, and another from copy's sensor_ to the lower object.
   :align: center
   :width: 100%

   After line 170. The copy constructor made a second ``Sensor`` with the values of ``car_b``'s, so each ``Vehicle`` points at its own. Compare with the shallow copy of `Copying an Owner`_.

The copy constructor reads ``other.sensor_``, a ``private`` data member of another object. That is allowed: a member function may use the ``private`` members of any object of its own class.

The Copy Assignment
"""""""""""""""""""

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 135 to 143
   :lineno-start: 135

     Vehicle& operator=(const Vehicle& other) {
       if (this != &other) {  // v = v must not delete its own Sensor
         // Copy first: if new throws, this Vehicle keeps its old Sensor.
         Sensor* copy{other.sensor_ != nullptr ? new Sensor{*other.sensor_} : nullptr};
         delete sensor_;  // give back what we owned
         sensor_ = copy;
       }
       return *this;
     }

Line 175 of ``run()`` calls it: ``copy = car_a;``. Before that line, ``copy`` owns its own ``Sensor`` with id 2 (from line 170) and ``car_a`` owns a ``Sensor`` with id 1.

.. figure:: /_static/images/l8/rof_copy_assign_1.png
   :alt: Two Vehicle variables, copy and car_a, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. On the right, a red box with a heap icon and the word Heap holds two Sensor objects: the upper one has id_ 2, type_ SensorType::lidar, range_ 100.0, the lower one id_ 1, type_ SensorType::lidar, range_ 100.0. A blue arrow runs from copy's sensor_ to the upper object, and another from car_a's sensor_ to the lower one.
   :align: center
   :width: 100%

   Before line 175: ``copy = car_a;``. Each ``Vehicle`` owns one ``Sensor``.

The function runs in five steps. Inside it, ``*this`` is ``copy``, the object on the left of ``=``, and ``other`` is ``car_a``.

1. **Line 136** compares two addresses: ``this``, the address of ``copy``, and ``&other``, the address of ``car_a``. They differ, so the body runs. They are equal only for ``v = v;``, an object assigned to itself. The body would still work then, but it would make a new ``Sensor`` and delete the old one for nothing, so the test skips it (`Core Guidelines C.62 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-self>`__).
2. **Line 138** makes the new ``Sensor`` first, a copy of ``car_a``'s, and keeps its address in a local pointer, ``copy``. The ``? :`` test is the one of the copy constructor.
3. **Line 139** deletes the ``Sensor`` this ``Vehicle`` owned, the one with id 2.
4. **Line 140** keeps the new one.
5. **Line 142** returns ``*this``, the object itself, by reference. That is what ``=`` does for an ``int`` too, so ``a = b = c;`` works for ``Vehicle``\ s as it does for ``int``\ s.

.. figure:: /_static/images/l8/rof_copy_assign_2.png
   :alt: The same two Vehicle variables, copy and car_a, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. The red Heap box now holds three Sensor objects. The top one, id_ 2, type_ SensorType::lidar, range_ 100.0, is drawn gray with a dashed border: it was deleted. The middle and bottom ones both have id_ 1, type_ SensorType::lidar, range_ 100.0. A blue arrow runs from copy's sensor_ to the middle object, and another from car_a's sensor_ to the bottom object.
   :align: center
   :width: 100%

   After line 175. ``copy`` owns a new ``Sensor`` with id 1, a deep copy of ``car_a``'s. The gray, dashed ``Sensor`` is the one ``copy`` owned before: line 139 gave its memory back.

.. important::

   **Copy first, then delete.** ``new`` can fail: when no memory is left, it throws ``std::bad_alloc``. In the order of lines 138 to 140, a failed ``new`` leaves the ``Vehicle`` with its old ``Sensor``, unchanged. With ``delete`` first, a failed ``new`` would leave ``sensor_`` holding the address of a ``Sensor`` that was already deleted, and the destructor would later delete it a second time.

The Moves
^^^^^^^^^

The Move Constructor
""""""""""""""""""""

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 146 to 148
   :lineno-start: 146

     Vehicle(Vehicle&& other) noexcept : sensor_{other.sensor_} {
       other.sensor_ = nullptr;  // the source owns nothing now
     }

- ``Vehicle(Vehicle&& other)``: the parameter is an rvalue reference, so this constructor runs for ``Vehicle moved{std::move(car_b)};`` (line 178).
- **Line 146**, ``sensor_{other.sensor_}``, copies the address: the new ``Vehicle`` points at ``other``'s ``Sensor``. No new ``Sensor`` is made.
- **Line 147** sets ``other.sensor_`` to ``nullptr``: ``other`` owns nothing now. Without this line, both ``Vehicle``\ s would point at one ``Sensor``, and it would be deleted twice, as in `Copying an Owner`_.

.. figure:: /_static/images/l8/rof_move_1.png
   :alt: One Vehicle variable, car_b, drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. On the right, a red box with a heap icon and the word Heap holds one Sensor object of three rows: id_ 2, type_ SensorType::lidar, range_ 100.0. A blue arrow runs from car_b's sensor_ to the object's first row.
   :align: center
   :width: 100%

   Before line 178: ``Vehicle moved{std::move(car_b)};``. ``car_b`` owns a ``Sensor`` with id 2.

.. figure:: /_static/images/l8/rof_move_2.png
   :alt: The same two Vehicle variables, car_b and moved, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_. car_b's sensor_ is now marked nullptr and has no arrow; moved's is marked a Sensor*. The red Heap box holds the same Sensor object as before, id_ 2, type_ SensorType::lidar, range_ 100.0, and a blue arrow runs from moved's sensor_ to it.
   :align: center
   :width: 100%

   After line 178. ``moved`` owns the same ``Sensor``, and ``car_b.sensor_`` is ``nullptr``. The ``Sensor`` did not move in memory; only its address changed hands.

The Move Assignment
"""""""""""""""""""

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 150 to 157
   :lineno-start: 150

     Vehicle& operator=(Vehicle&& other) noexcept {
       if (this != &other) {   // v = std::move(v) must not delete
         delete sensor_;       // give back what we owned
         sensor_ = other.sensor_;
         other.sensor_ = nullptr;
       }
       return *this;
     }

Line 180 of ``run()`` calls it: ``car_a = std::move(moved);``. Before that line, ``car_a`` owns the ``Sensor`` with id 1 and ``moved`` owns the one with id 2.

.. figure:: /_static/images/l8/rof_move_assign_1.png
   :alt: Two Vehicle variables, car_a and moved, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. On the right, a red box with a heap icon and the word Heap holds two Sensor objects: the upper one has id_ 1, type_ SensorType::lidar, range_ 100.0, the lower one id_ 2, type_ SensorType::lidar, range_ 100.0. A blue arrow runs from car_a's sensor_ to the upper object, and another from moved's sensor_ to the lower one.
   :align: center
   :width: 100%

   Before line 180: ``car_a = std::move(moved);``. Each ``Vehicle`` owns one ``Sensor``.

1. **Line 151** skips the body when an object is moved into itself, ``v = std::move(v);``. Here the test matters: `Discussion: Who Deletes What?`_ shows what goes wrong without it.
2. **Line 152** deletes the ``Sensor`` this ``Vehicle`` owned, the one with id 1.
3. **Line 153** takes ``other``'s address.
4. **Line 154** leaves ``other`` owning nothing.
5. **Line 156** returns ``*this``, as the copy assignment does.

.. figure:: /_static/images/l8/rof_move_assign_2.png
   :alt: The same two Vehicle variables, car_a and moved, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_. car_a's sensor_ is marked a Sensor*; moved's is now marked nullptr and has no arrow. In the red Heap box, the upper Sensor object, id_ 1, type_ SensorType::lidar, range_ 100.0, is drawn gray with a dashed border: it was deleted. A blue arrow runs from car_a's sensor_ to the lower object, id_ 2, type_ SensorType::lidar, range_ 100.0.
   :align: center
   :width: 100%

   After line 180. ``car_a`` owns the ``Sensor`` with id 2, and ``moved.sensor_`` is ``nullptr``. The gray, dashed ``Sensor`` with id 1 was given back on line 152.

Later, the destructor of a moved-from ``Vehicle`` deletes a null pointer. C++ allows that, and it does nothing:

.. note::

   "In a single-object delete expression, the value of the operand of delete may be a null pointer value, a pointer to a non-array object created by a previous new-expression, or a pointer to a subobject (6.7.2) representing a base class of such an object (11.7)". C++20 **[expr.delete]** (7.6.2.8) paragraph 2. Paragraph 6 makes the call of the destructor depend on the pointer: "If the value of the operand of the delete-expression is not a null pointer value ..., the delete-expression will invoke the destructor (if any)".

Neither move can throw: each only copies addresses and calls ``delete``. So both are marked ``noexcept`` (`Core Guidelines C.66 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-move-noexcept>`__). The next section shows why that matters.

Why the Moves Are noexcept
^^^^^^^^^^^^^^^^^^^^^^^^^^

This ``Vehicle`` owns nothing. It only counts how often it is copied and moved:

.. code-block:: cpp
   :linenos:

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

``fleet.emplace_back()`` (line 12) builds a new ``Vehicle`` at the end of the vector. When the vector is full, it gets a bigger block of memory and brings each old element over to it, by a move or by a copy.

``702run week8_appendix move_noexcept`` runs the loop twice: once with the move constructor ``noexcept``, once without it. The repository's version, in namespace ``move_noexcept`` of ``appendix/src/appendix.cpp``, uses a template parameter for that, so both cases fit in one program. It prints:

.. code-block:: text

   with noexcept: 0 copies, 7 moves
   without it: 7 copies, 0 moves

With g++ 13.3, the vector's capacity after each of the five calls is 1, 2, 4, 4, 8 (measured with ``fleet.capacity()``). So the vector grows to 1, 2, 4, then 8 places, and brings over 1, 2, then 4 old elements: 1 + 2 + 4 = 7 moves or copies.

.. important::

   **A vector moves its elements only when the move cannot throw.** A move that throws halfway would leave the old block half emptied, with no way back. A copy leaves the old block whole. So the vector copies its elements unless the move constructor is ``noexcept``. For the raw-pointer ``Vehicle``, a copy means a new ``Sensor`` for each element (`The Copy Constructor`_), and a move only hands over an address (`The Move Constructor`_).

All Five, Run
^^^^^^^^^^^^^

``run()`` of namespace ``five`` calls each of the four functions once, and prints what each ``Vehicle`` owns after it:

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 168 to 183
   :lineno-start: 168

   void run() {
     Vehicle car_b{Sensor{2}};
     Vehicle copy{car_b};
     std::cout << "copy: sensor " << copy.get_sensor().get_id() << ", own Sensor: "
               << std::boolalpha << (&copy.get_sensor() != &car_b.get_sensor())
               << '\n';  // copy: sensor 2, own Sensor: true
     Vehicle car_a{Sensor{1}};
     copy = car_a;
     std::cout << "after copy assignment: sensor " << copy.get_sensor().get_id()
               << '\n';  // 1
     Vehicle moved{std::move(car_b)};
     std::cout << "moved: sensor " << moved.get_sensor().get_id() << '\n';  // 2
     car_a = std::move(moved);
     std::cout << "after move assignment: sensor " << car_a.get_sensor().get_id()
               << '\n';  // 2
   }  // ~Vehicle: sensor 0, 2, 1, 0

``702run week8_appendix five`` prints:

.. code-block:: text

   copy: sensor 2, own Sensor: true
   after copy assignment: sensor 1
   moved: sensor 2
   after move assignment: sensor 2
   ~Vehicle: sensor 0
   ~Vehicle: sensor 2
   ~Vehicle: sensor 1
   ~Vehicle: sensor 0

1. **Line 170**, the copy constructor. Lines 171 to 173 compare the address of ``copy``'s ``Sensor`` with that of ``car_b``'s. "own Sensor: true" says that they differ: the copy constructor made a second ``Sensor``.
2. **Line 175**, the copy assignment: ``copy`` now owns a copy of ``car_a``'s ``Sensor``, id 1.
3. **Line 178**, the move constructor: ``moved`` takes ``car_b``'s ``Sensor``, id 2.
4. **Line 180**, the move assignment: ``car_a`` gives back its ``Sensor`` with id 1 and takes ``moved``'s, id 2.
5. **Line 183**, the end of ``run()``: the four objects are destroyed in the reverse order they were created: ``moved``, ``car_a``, ``copy``, then ``car_b``. ``moved`` and ``car_b`` were moved from, so they print 0: they own no ``Sensor``. ``car_a`` holds sensor 2, and ``copy`` holds sensor 1.

Run with AddressSanitizer, the program reports no leak and no double free. Four ``Sensor``\ s were created on the heap: by ``car_b`` (line 169), ``copy`` (line 170), ``car_a`` (line 174) and the copy assignment (line 175). The copy assignment deleted ``copy``'s first one, the move assignment deleted ``car_a``'s first one, and the two destructors that print 2 and 1 deleted the other two.

Without the Moves
^^^^^^^^^^^^^^^^^

A class that writes a destructor and stops there does not only miss its copies. It also loses its moves.

.. code-block:: cpp
   :caption: ``undefined/src/undefined.cpp``, lines 115 to 128
   :lineno-start: 115

   class Vehicle {  // a destructor, and no copy or move written
    public:
     explicit Vehicle(const Sensor& sensor)
         : sensor_{new Sensor{sensor}} {}
     ~Vehicle() { delete sensor_; }

    private:
     Sensor* sensor_;
   };

   void run() {
     Vehicle car_b{Sensor{2}};
     Vehicle moved{std::move(car_b)};  // the compiler's copy constructor runs
   }  // moved deletes the Sensor, then car_b deletes it again

.. warning::

   **Writing a destructor stops the compiler from writing the moves.** This ``Vehicle`` declares a destructor (line 119), so the compiler writes no move constructor and no move assignment. ``std::move(car_b)`` on line 127 then finds no move constructor, and the compiler's copy constructor runs instead. It copies the address, as in `Copying an Owner`_, and at the end of ``run()`` both destructors delete the same ``Sensor``. Declaring a copy constructor or a copy assignment has the same effect.

   "If the definition of a class X does not explicitly declare a move constructor, a non-explicit one will be implicitly declared as defaulted if and only if X does not have a user-declared copy constructor, X does not have a user-declared copy assignment operator, X does not have a user-declared move assignment operator, and X does not have a user-declared destructor". C++20 **[class.copy.ctor]** (11.4.4.2) paragraph 8, with its list items joined into one sentence. A note in the same paragraph adds: "When the move constructor is not implicitly declared or explicitly supplied, expressions that otherwise would have invoked the move constructor may instead invoke a copy constructor".

``702run week8_appendix no_move`` stops with the same double-free report as `Double Free, Measured`_, pointing at line 119 (the destructor's ``delete``), line 128 (the end of ``run()``) and line 118 (the ``new``).

The course flags, ``-Wall -Wextra``, give no warning for this class. ``-Wdeprecated-copy-dtor`` does, because a copy constructor that the compiler writes for a class with its own destructor is **deprecated**: still allowed, but marked for removal from the language. g++ 13.3 says:

.. code-block:: text

   .../undefined.cpp:127:33: warning: implicitly-declared ‘constexpr undefined::no_move::Vehicle::Vehicle(const undefined::no_move::Vehicle&)’ is deprecated [-Wdeprecated-copy-dtor]
   .../undefined.cpp:119:3: note: because ‘undefined::no_move::Vehicle’ has user-provided ‘undefined::no_move::Vehicle::~Vehicle()’

That is a second reason C.21 asks for all five: write one, and the compiler stops writing some of the others.

Discussion: Who Deletes What?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This class is the ``Vehicle`` of the rule of five, with its copies deleted and one line missing from its move assignment:

.. code-block:: cpp
   :caption: ``undefined/src/undefined.cpp``, lines 87 to 91
   :lineno-start: 87

     Vehicle& operator=(Vehicle&& other) noexcept {
       delete sensor_;
       sensor_ = other.sensor_;
       return *this;
     }

.. code-block:: cpp
   :caption: ``undefined/src/undefined.cpp``, lines 100 to 105
   :lineno-start: 100

   void run() {
     Vehicle car_a{Sensor{1}};
     Vehicle car_b{Sensor{2}};
     car_a = std::move(car_b);
     std::cout << car_a.get_sensor().get_id() << '\n';  // 2
   }

1. Draw ``car_a``, ``car_b`` and the ``Sensor``\ s on paper after line 103. Who deletes what at the end of ``run()``?
2. Add the missing line. What does ``car_a = std::move(car_a);`` do then, without the test ``if (this != &other)``?

.. dropdown:: Answers
   :class-container: sd-border-success

   1. Line 88 deletes the ``Sensor`` with id 1, and line 89 copies ``car_b``'s address into ``car_a``. Nothing sets ``car_b.sensor_`` to ``nullptr``, so after line 103 both ``Vehicle``\ s point at the ``Sensor`` with id 2. At the end of ``run()``, line 105, ``car_b``'s destructor deletes it, then ``car_a``'s deletes it again: a double free. ``702run week8_appendix move_bug`` prints 2 (line 104), then AddressSanitizer reports ``attempting double-free`` at line 81, the destructor's ``delete``, called from line 105.

      .. figure:: /_static/images/l8/rof_move_bug.png
         :alt: Two Vehicle variables, car_a and car_b, each drawn as a name tag over a blue box with a stack icon and the word Stack, holding one field, sensor_, marked a Sensor*. In the red Heap box, the upper Sensor object, id_ 1, type_ SensorType::lidar, range_ 100.0, is drawn gray with a dashed border: it was deleted. Two blue arrows, one from each sensor_, end on the lower object, id_ 2, type_ SensorType::lidar, range_ 100.0, at its first row.
         :align: center
         :width: 100%

         After line 103. ``car_a`` and ``car_b`` point at the same ``Sensor``, id 2. The gray, dashed ``Sensor`` with id 1 was deleted on line 88.

   2. The missing line is ``other.sensor_ = nullptr;``. With it, a move into itself still breaks. ``other`` is ``car_a`` itself, so line 88 deletes ``car_a``'s ``Sensor``, line 89 copies that same deleted address back into ``sensor_``, and the new line sets it to ``nullptr``. ``car_a`` has lost its ``Sensor``, and reading ``*sensor_`` after that is undefined behavior. g++ warns about the line with ``-Wself-move``, which ``-Wall`` turns on. The test ``if (this != &other)`` of `The Move Assignment`_ skips the body in this case.

.. _l8r5-default-delete:

``= default`` and ``= delete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A class that must not be copied says so with ``= delete``:

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 228 to 252
   :lineno-start: 228

   class Vehicle {  // the raw-pointer Vehicle, move-only on purpose
    public:
     explicit Vehicle(const Sensor& sensor)
         : sensor_{new Sensor{sensor}} {}
     ~Vehicle() { delete sensor_; }
     Vehicle(const Vehicle&) = delete;             // no copies
     Vehicle& operator=(const Vehicle&) = delete;
     Vehicle(Vehicle&& other) noexcept : sensor_{other.sensor_} {
       other.sensor_ = nullptr;
     }
     Vehicle& operator=(Vehicle&& other) noexcept {
       if (this != &other) {
         delete sensor_;
         sensor_ = other.sensor_;
         other.sensor_ = nullptr;
       }
       return *this;
     }
     [[nodiscard]] const Sensor& get_sensor() const noexcept {
       return *sensor_;
     }

    private:
     Sensor* sensor_;
   };

``= delete`` (lines 233 and 234) says that the function does not exist, and a call to it is a compile error. This ``Vehicle`` deletes its copies and keeps the moves of `The Moves`_ (lines 235 to 245). It is move-only on purpose, as the ``Vehicle`` of `Rule of Zero`_ is. ``702run week8_appendix move_only`` moves one ``Vehicle`` and prints 2.

``= default`` is the other choice: it asks for the version the compiler would write, for example ``Vehicle(Vehicle&&) = default;``. Use it when the compiler's version is right but declaring something else stopped the compiler from writing it.

Declaring the copies stops the compiler from writing the moves, as for the destructor in `Without the Moves`_. Remove lines 235 to 245, and ``Vehicle moved{std::move(car_b)};`` on line 256 picks the deleted copy constructor, so it does not compile. g++ 13.3 says:

.. code-block:: text

   error: use of deleted function ‘move_only::Vehicle::Vehicle(const move_only::Vehicle&)’

Beyond Memory: A File
^^^^^^^^^^^^^^^^^^^^^

A ``TripLog`` keeps a log of a robotaxi's trips in a file. It owns an open file, a ``std::FILE*`` from the C library (``<cstdio>``). The ``std::FILE*`` is a handle: the program must close the file with ``std::fclose``, once, as it must ``delete`` memory once. No class of the standard library owns a ``std::FILE*``, so ``TripLog`` writes the five itself.

.. code-block:: cpp
   :caption: ``appendix/src/appendix.cpp``, lines 327 to 371
   :lineno-start: 327

   class TripLog {
    public:
     TripLog() : file_{std::tmpfile()} {
       if (file_ == nullptr) {
         throw std::runtime_error{"cannot open a temporary file"};
       }
     }
     ~TripLog() {
       if (file_ != nullptr) {
         std::fclose(file_);
         std::cout << "~TripLog: file closed\n";
       } else {
         std::cout << "~TripLog: no file\n";
       }
     }
     TripLog(const TripLog&) = delete;
     TripLog& operator=(const TripLog&) = delete;
     TripLog(TripLog&& other) noexcept : file_{other.file_} {
       other.file_ = nullptr;
     }
     TripLog& operator=(TripLog&& other) noexcept {
       if (this != &other) {
         if (file_ != nullptr) {
           std::fclose(file_);
         }
         file_ = other.file_;
         other.file_ = nullptr;
       }
       return *this;
     }
     void write(const char* line) {
       std::fputs(line, file_);
       std::fputs("\n", file_);
     }

    private:
     std::FILE* file_;  // the open file, or nullptr after a move
   };

   void run() {
     TripLog log;
     log.write("trip 1: 4.2 km");
     TripLog kept{std::move(log)};
     kept.write("trip 2: 1.5 km");
   }  // ~TripLog: file closed, then ~TripLog: no file

- **Line 329** opens the file. ``std::tmpfile()`` creates a temporary file that the system deletes when the file is closed, so the run leaves nothing on your disk. It returns ``nullptr`` when it fails, and the constructor then throws (line 331).
- **Lines 334 to 341**, the destructor, close the file when the ``TripLog`` owns one, and print what they did.
- **Lines 342 and 343** delete the copies: two ``TripLog``\ s with one handle would close one file twice.
- **Lines 344 to 356**, the moves, hand the handle over and leave the source holding ``nullptr``, as the moves of the ``Vehicle`` do with ``sensor_``.

``702run week8_appendix file_owner`` prints:

.. code-block:: text

   ~TripLog: file closed
   ~TripLog: no file

Line 369 moves the file from ``log`` into ``kept``. At the end of ``run()``, line 371, ``kept`` is destroyed first, since it was created last, and closes the file. ``log`` owns nothing after the move, so its destructor closes nothing. The file is closed exactly once.

Which Rule to Follow
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 15 45

   * - The data members of your class
     - Rule
     - What the class writes
   * - All give back their own resources: ``int``, ``double``, ``std::string``, ``std::vector``, ``std::unique_ptr``, a ``std::vector`` of ``std::unique_ptr``
     - Rule of zero
     - None of the five. The compiler's versions are enough (Core Guidelines C.20).
   * - One holds a resource by hand: a raw pointer from ``new``, a ``std::FILE*`` from ``std::fopen``, any other handle
     - Rule of five
     - A destructor that gives the resource back, and the four copies and moves, written or deleted with ``= delete`` (Core Guidelines C.21).

Follow the **rule of zero** by default. The ``Vehicle`` of the lecture does: its ``sensors_`` is a ``std::vector`` of ``std::unique_ptr``, and it writes none of the five.

Follow the **rule of five** only for a class that manages a resource by hand. In this course you do not write such a class for memory: a ``std::unique_ptr`` member does the ``delete`` (Core Guidelines R.11). You meet the rule of five when a library hands you a resource that no standard class owns, as ``TripLog`` does with its file.
