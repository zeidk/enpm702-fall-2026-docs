.. _l9_virtual:

====================================================
virtual Methods in Depth
====================================================

This page is **required reading** after the Lecture 9 class. It is not presented in class. In class, Runtime Polymorphism takes three steps: ``public`` inheritance, a ``virtual`` method that the derived class overrides, and a call through a base reference or pointer. This page explains what happens under those steps: how a ``virtual`` call finds the right method while the program runs, what that costs, and why a base class with a ``virtual`` method needs a ``virtual`` destructor.

The classes on this page are the small ones of the :doc:`lecture page <l9_lecture>`: a ``Vehicle`` with two data members, ``max_speed_`` and ``speed_``, and a ``drive`` method, and the derived classes ``RoboTaxi`` and ``Taxi``. ``maya_ride`` is the 500 m route of the lecture. Every number on this page was measured with g++ 13.3 (``-std=c++20``) on x86_64, the course's setup.

What Runtime Polymorphism Needs
-------------------------------

A call runs the derived class's own method only when three things hold:

1. **Inheritance**: ``RoboTaxi`` and ``Taxi`` derive from ``Vehicle`` with ``public``.
2. **A virtual method** in the base class, which the derived class overrides: ``drive``.
3. **A base reference or pointer** to the object: ``Vehicle&``, ``Vehicle*``, ``std::unique_ptr<Vehicle>`` or ``std::shared_ptr<Vehicle>``.

With only 1 and 3, the static type picks the method. The **static type** of an expression is the type written in the code; the **dynamic type** is the class of the object it refers to while the program runs. Here ``start_shift`` takes a ``const Vehicle&``, so its parameter's static type is ``Vehicle``. Without ``virtual``, ``Vehicle::drive`` runs for a ``RoboTaxi`` and for a ``Taxi`` alike, as in The Challenge: A Base Reference on the lecture page.

One Function for Every Vehicle
------------------------------

Once ``drive`` is ``virtual`` in ``Vehicle`` and each derived class overrides it, the same function serves every vehicle:

.. code-block:: cpp

   void start_shift(const Vehicle& vehicle, const Route& route) {
     vehicle.drive(route);
   }

   start_shift(robotaxi, maya_ride);
   start_shift(taxi, maya_ride);

.. code-block:: text

   RoboTaxi: drives itself 500 m
   Taxi: Ana drives 500 m

- Only ``virtual`` changed. The parameter's static type is still ``Vehicle``, but each object now runs its own ``drive``: the dynamic type picks.
- ``start_shift`` serves every class derived from ``Vehicle``, including classes written after it. Adding a robot bus needs no change to ``start_shift``.

How a virtual Call Finds Its Method: the vtable
-----------------------------------------------

The compiler cannot know, while it compiles ``start_shift``, which class ``vehicle`` will refer to. So for a ``virtual`` call it writes code that looks the method up while the program runs. g++ does this with one table per class, the **vtable** (virtual table):

- g++ builds one vtable for each class that has a ``virtual`` method. Each entry holds the address of one ``virtual`` method, the class's own version.
- Each object of such a class holds a **hidden pointer**, 8 bytes, to the vtable of the class it was made as.

The vtables of the three classes, as ``g++ -fdump-lang-class`` prints them, have 5 entries each: an offset (0), the type information, the destructor twice (g++ keeps two versions of it), then ``drive``. The entries that matter here:

.. list-table::
   :header-rows: 1
   :widths: 19 27 27 27

   * - Entry
     - Vehicle's vtable
     - RoboTaxi's vtable
     - Taxi's vtable
   * - destructor
     - ``Vehicle::~Vehicle``
     - ``RoboTaxi::~RoboTaxi``
     - ``Taxi::~Taxi``
   * - ``drive``
     - ``Vehicle::drive``
     - ``RoboTaxi::drive``
     - ``Taxi::drive``

.. figure:: /_static/images/l9/vtable_memory.png
   :alt: Three columns. On the left, two blue Stack boxes, one above the other. The upper one, under the name tag robotaxi, holds a Vehicle part with three rows: (hidden pointer), max_speed_ 13.4 and speed_ 0.0, then a RoboTaxi part with one gray row, (its own members). The lower one, under the name tag taxi, holds the same Vehicle part, then a Taxi part with one row, driver_name_ "Ana". In the middle, a slate box headed vtables holds two tables, RoboTaxi's vtable and Taxi's vtable, each with two entries, destructor and drive. A blue arrow tagged 1 runs from robotaxi's hidden pointer to RoboTaxi's vtable, and another from taxi's hidden pointer to Taxi's vtable. On the right, a slate box headed Code holds four boxes: RoboTaxi::~RoboTaxi, RoboTaxi::drive, Taxi::~Taxi and Taxi::drive. A slate arrow runs from each entry to the code of the same class; the one from RoboTaxi's drive entry to RoboTaxi::drive is tagged 2.
   :align: center
   :width: 100%

   A ``RoboTaxi`` and a ``Taxi`` on the stack. (1) Each object's hidden pointer leads to its own class's vtable. (2) Each entry leads to the code of that class's method. The figure draws one destructor entry of the two, and leaves out ``RoboTaxi``'s own members.

For ``vehicle.drive(route)``, with ``vehicle`` a ``const Vehicle&`` to a ``RoboTaxi``, the program takes three steps:

1. It reads the object's hidden pointer: the pointer leads to ``RoboTaxi``'s vtable.
2. It reads the ``drive`` entry of that table: ``RoboTaxi::drive``.
3. It calls that method.

Choosing the method while the program runs, from the object's class, is **dynamic binding** (`C++ FAQ: Inheritance, virtual functions <https://isocpp.org/wiki/faq/virtual-functions>`_). A method that is not ``virtual`` has no entry: the compiler writes its address into the call while it compiles, from the static type. That is **static binding** (`Learn C++, lesson 25.5 <https://www.learncpp.com/cpp-tutorial/early-binding-and-late-binding/>`_).

.. figure:: /_static/images/l9/virtual_call_flow.png
   :alt: A flowchart. It starts at the box vehicle.drive(route), where vehicle is a const Vehicle& to a RoboTaxi, then asks: Is drive virtual in Vehicle? On the no branch, one box: Static binding. The compiler calls the version of the static type, Vehicle: Vehicle::drive runs. On the yes branch, three boxes in a row: Dynamic binding, 1. Read the object's hidden pointer: it points to RoboTaxi's vtable; 2. Read the drive entry of that vtable: RoboTaxi::drive; 3. Call it: RoboTaxi::drive runs. Both branches meet and the flowchart ends.
   :align: center
   :width: 70%

   How the call ``vehicle.drive(route)`` is resolved.

The C++ standard does not name the vtable or the hidden pointer: it says what a ``virtual`` call does, and leaves how to the compiler. g++, the compiler of this course, uses a vtable.

The Cost of virtual
-------------------

The hidden pointer and the table are not free. Two classes with the same data members, one with ``virtual`` methods and one without:

.. code-block:: cpp

   namespace compile_time {
   class Vehicle {  // no virtual method
    public:
     void drive() const {}
    private:
     double max_speed_{0.0};
     double speed_{0.0};
   };
   }  // namespace compile_time

   namespace runtime {
   class Vehicle {  // a virtual method
    public:
     virtual ~Vehicle() = default;
     virtual void drive() const {}
    private:
     double max_speed_{0.0};
     double speed_{0.0};
   };
   }  // namespace runtime

   using Plain = compile_time::Vehicle;
   using Poly = runtime::Vehicle;
   std::cout << sizeof(Plain) << ' ' << sizeof(Poly) << '\n';
   std::cout << std::boolalpha << std::is_polymorphic_v<Plain> << ' '
             << std::is_polymorphic_v<Poly> << '\n';

.. code-block:: text

   16 24
   false true

- The class with ``virtual`` methods is 8 bytes larger: the two ``double`` members take 16 bytes, and the hidden pointer takes 8 more.
- ``nm -C`` on the object file lists the table as ``vtable for runtime::Vehicle``. Without ``-C`` (demangle), ``nm`` prints the name the linker uses, ``_ZTVN7runtime7VehicleE``. In this test, the table appeared in the object file only once the program made a ``runtime::Vehicle`` object.
- A ``virtual`` call reads the hidden pointer and the table first, so it costs a little more than a direct call. The compiler usually cannot replace a ``virtual`` call with the method's body either.
- A class with a ``virtual`` method is a **polymorphic class**: "A class that declares or inherits a virtual function is called a polymorphic class". C++20 **[class.virtual]** (11.7.2) paragraph 1. ``std::is_polymorphic_v`` asks exactly that question.

.. note::

   "Redundant ``virtual`` increases run-time and object-code size". Rule: `Core Guidelines C.132 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-virtual>`_, "Don't make a function ``virtual`` without reason". Make a method ``virtual`` only when a derived class overrides it.

Slicing with a virtual Method
-----------------------------

On the lecture page, Slicing copies a ``Taxi`` into a ``Vehicle`` with no ``virtual`` method: only the base part is copied. With a ``virtual`` ``drive``, each object also holds its hidden pointer, and the copy does not take ``taxi``'s:

.. code-block:: cpp

   Taxi taxi{13.4, "Ana"};
   Vehicle copy{taxi};  // not a reference
   copy.drive(maya_ride);

.. code-block:: text

   Vehicle: drives 500 m

.. figure:: /_static/images/l9/slicing_virtual_memory.png
   :alt: Two blue Stack boxes side by side. On the left, under the name tag taxi, one object in two parts. The first part, captioned Vehicle part, has three rows: (hidden pointer) Taxi's vtable, then max_speed_ 13.4 and speed_ 0.0, each marked with a minus sign for private. The second part, captioned Taxi part, has one row: driver_name_ "Ana", marked private, with tag 2 beside it. A measuring line under taxi reads 56 bytes. On the right, under the name tag copy, one part, captioned Vehicle part, with three rows: (hidden pointer) Vehicle's vtable, with tag 3 beside it, then max_speed_ 13.4 and speed_ 0.0. A measuring line under copy reads 24 bytes. A blue arrow tagged 1 runs from the Vehicle part of taxi to the Vehicle part of copy.
   :align: center
   :width: 100%

   ``Vehicle copy{taxi};`` with a ``virtual`` ``drive``.

1. ``copy`` gets the values of the ``Vehicle`` part: ``max_speed_`` and ``speed_``.
2. ``driver_name_`` is left behind: ``copy`` is 24 bytes, ``taxi`` 56.
3. ``copy`` is a ``Vehicle``, made by ``Vehicle``'s copy constructor, so its hidden pointer leads to ``Vehicle``'s vtable (gdb's ``info vtbl`` shows each object's table). ``copy.drive`` runs ``Vehicle::drive``, even with ``drive`` ``virtual``: a copy is not a reference.

virtual Destructors
-------------------

A **virtual destructor** is a destructor declared ``virtual`` in the base class. Deleting a derived object through a base pointer then runs the derived destructor first, then the base destructor.

.. code-block:: cpp

   class Vehicle {
    public:
     virtual ~Vehicle() = default;
     // ...
   };

With ``= default`` (the :doc:`Rule of Five and Rule of Zero </lectures/lecture8/l8_rule_of_five>` reading), the compiler writes the body, which here does nothing. What matters is ``virtual``. The destructors you wrote so far gave back what an object owns. The question here is which destructor runs.

.. note::

   In a delete, if the static type differs from the dynamic type, "the static type shall be a base class of the dynamic type of the object to be deleted and the static type shall have a virtual destructor or the behavior is undefined". C++20 **[expr.delete]** (7.6.2.8) paragraph 3.

Deleting through a Base Pointer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here ``~Vehicle`` is not ``virtual``, and both destructors print their names. The program is built with AddressSanitizer (``-fsanitize=address,undefined``):

.. code-block:: cpp

   {
     // A small Vehicle: two doubles and a virtual drive.
     // ~Vehicle is not virtual. Both destructors print their names.
     std::unique_ptr<Vehicle> vehicle{
         std::make_unique<Taxi>(13.4, "Ana Maria Rodrigues")};
     vehicle->drive(maya_ride);
   }  // vehicle's destructor runs delete on a Vehicle*

The output, then AddressSanitizer's report (stack traces cut):

.. code-block:: text

   Taxi: Ana Maria Rodrigues drives 500 m
   ~Vehicle

.. code-block:: text

   new-delete-type-mismatch
   size of the allocated type:   56 bytes;
   size of the deallocated type: 24 bytes.

- At the closing brace, ``std::unique_ptr<Vehicle>`` deletes through a ``Vehicle*``, and ``~Vehicle`` is not ``virtual``, so only ``~Vehicle`` runs. The static type (``Vehicle``) differs from the dynamic type (``Taxi``), so by [expr.delete] the behavior is undefined. What g++ did here is one possible result, not a rule.
- g++ warns only with ``-Wnon-virtual-dtor``: ``'class Vehicle' has virtual functions and accessible non-virtual destructor``.

The Sizes in the Report
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class Vehicle {  // small: two doubles, one virtual method
    public:
     ~Vehicle();  // not virtual
     virtual void drive(const Route& route) const;
    private:
     double max_speed_;
     double speed_{0.0};
   };
   class Taxi : public Vehicle {  // also ~Taxi and drive
    private:
     std::string driver_name_;
   };

1. ``Vehicle``: two ``double`` members (16 bytes) and the hidden pointer to the vtable (8 bytes): 24 bytes.
2. ``Taxi`` adds a ``std::string`` (32 bytes): 24 + 32 = 56 bytes.
3. The name has 19 characters, more than the 15 a g++ ``std::string`` keeps inside itself, so its characters are on the heap, and only ``~Taxi`` would free them.

With the ``Vehicle`` of the design (six data members), the sizes are 96 and 128 bytes.

With a virtual Destructor
^^^^^^^^^^^^^^^^^^^^^^^^^

The same program, with one change: ``~Vehicle`` is ``virtual``.

.. code-block:: cpp

   class Vehicle {
    public:
     virtual ~Vehicle() { std::cout << "~Vehicle\n"; }
     // ...
   };
   // Taxi and the rest of the code do not change.

.. code-block:: text

   Taxi: Ana Maria Rodrigues drives 500 m
   ~Taxi
   ~Vehicle

- The ``delete`` now runs ``~Taxi``, then ``~Vehicle``. AddressSanitizer reports no error and no leak (measured 2026-11-02, g++ 13.3).
- ``~Taxi`` overrides ``~Vehicle`` although the names differ: the destructor entry of ``Taxi``'s vtable holds ``Taxi::~Taxi`` (see the table above).
- In Live Coding Step 4, you give ``Vehicle`` this ``virtual`` destructor, with ``= default``.

.. figure:: /_static/images/l9/virtual_delete_flow.png
   :alt: A flowchart. It starts at the box delete through a Vehicle* that points to a Taxi, then asks: Is ~Vehicle virtual? On the yes branch, three boxes in a row: 1. ~Taxi runs, then driver_name_ is destroyed; 2. ~Vehicle runs; 3. The whole Taxi is freed. AddressSanitizer reports nothing. On the no branch, one orange box: Undefined behavior. With g++: only ~Vehicle runs, and AddressSanitizer reports new-delete-type-mismatch: 56 bytes allocated, deleted as 24 bytes. Both branches meet and the flowchart ends.
   :align: center
   :width: 70%

   What a ``delete`` through a ``Vehicle*`` does, with and without a ``virtual`` destructor.

.. note::

   "A base class destructor should be either public and virtual, or protected and non-virtual". Rule: `Core Guidelines C.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual>`_.

Discussion: Which drive() Runs?
-------------------------------

``Vehicle::drive`` is ``virtual``, and ``RoboTaxi`` overrides it.

.. code-block:: cpp

   RoboTaxi robotaxi{13.4};
   Vehicle& ref{robotaxi};
   Vehicle* ptr{&robotaxi};
   Vehicle copy{robotaxi};

   robotaxi.drive(maya_ride);  // 1
   ref.drive(maya_ride);       // 2
   ptr->drive(maya_ride);      // 3
   copy.drive(maya_ride);      // 4

For each line: does ``Vehicle::drive`` or ``RoboTaxi::drive`` run? Give the static type and the dynamic type.

.. dropdown:: Answer
   :class-container: sd-border-success

   1. ``RoboTaxi::drive``. Static type ``RoboTaxi``, dynamic type ``RoboTaxi``.
   2. ``RoboTaxi::drive``. Static type ``Vehicle`` (a reference to a ``Vehicle``), dynamic type ``RoboTaxi``: the call goes through the hidden pointer to ``RoboTaxi``'s vtable.
   3. ``RoboTaxi::drive``. ``*ptr`` has static type ``Vehicle`` and dynamic type ``RoboTaxi``, as for line 2.
   4. ``Vehicle::drive``. ``copy`` is a ``Vehicle`` object, sliced from ``robotaxi``: its static and dynamic types are both ``Vehicle``, and its hidden pointer leads to ``Vehicle``'s vtable.

   A run of this code (g++ 13.3) printed ``RoboTaxi::drive`` three times, then ``Vehicle::drive``.

Discussion: Who Needs a virtual Destructor?
-------------------------------------------

Which of these classes of the design needs ``virtual ~ClassName() = default;``?

1. ``Vehicle``, the base of ``RoboTaxi`` and ``Taxi``.
2. ``Sensor`` and ``Route``.
3. ``Fleet``, which has no ``virtual`` method and no derived class.

.. note::

   "A class with a virtual function should have a virtual or protected destructor". Rule: `Core Guidelines C.127 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-dtor>`_. Its reason: "A class with a virtual function is usually (and in general) used via a pointer to base. Usually, the last user has to call delete on a pointer to base, often via a smart pointer to base, so the destructor should be public and virtual."

.. dropdown:: Answer
   :class-container: sd-border-success

   1. **Vehicle: yes.** It has ``virtual`` methods, and code deletes a ``RoboTaxi`` or a ``Taxi`` through a ``Vehicle`` pointer, as a ``std::unique_ptr<Vehicle>`` does in `Deleting through a Base Pointer`_.
   2. **Sensor and Route: no.** Neither has a ``virtual`` method or a derived class, so nothing deletes a derived object through them.
   3. **Fleet: no**, for the same reason. A ``virtual`` destructor would add the hidden pointer and a vtable for nothing (`The Cost of virtual`_).
