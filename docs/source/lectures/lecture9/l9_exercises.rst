====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 9: OOP Advanced.
Work through them in order, as each exercise builds on the skills from the
previous one. Write, compile, and run each program to verify your understanding.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1: Basic Inheritance
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice creating a base class and a derived class using public
    inheritance, and understand how constructors are chained.

    **Specification**

    1. Create a ``Vehicle`` base class with:

       - A ``protected`` ``std::string`` attribute ``name_``.
       - A ``protected`` ``int`` attribute ``year_``.
       - A constructor that initializes both attributes.
       - A ``public`` method ``display_info()`` that prints the vehicle name and year.

    2. Create a ``Car`` derived class (public inheritance from ``Vehicle``) with:

       - A ``private`` ``int`` attribute ``num_doors_``.
       - A constructor that takes ``name``, ``year``, and ``num_doors``, and explicitly calls the ``Vehicle`` constructor.
       - A ``public`` method ``display_car_info()`` that calls ``display_info()`` and also prints the number of doors.

    3. In ``main()``, create a ``Car`` object and call ``display_car_info()``.

.. dropdown:: Exercise 2: Method Overriding with ``virtual``
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between static binding (no ``virtual``) and
    dynamic binding (with ``virtual``), and practice using ``override``.

    **Specification**

    1. Create a ``Vehicle`` base class with:

       - A ``virtual`` method ``drive()`` that prints ``"Vehicle is driving"``.
       - A ``virtual`` destructor (``= default``).

    2. Create a ``RoboTaxi`` class (derived from ``Vehicle``) with:

       - An overridden ``drive()`` method that prints ``"RoboTaxi is driving autonomously"``.
       - Use the ``override`` keyword.

    3. Create a ``Taxi`` class (derived from ``Vehicle``) with:

       - An overridden ``drive()`` method that prints ``"Taxi is driving with a human driver"``.

    4. In ``main()``:

       a. Create a ``std::unique_ptr<Vehicle>`` pointing to a ``RoboTaxi``.
       b. Create a ``std::unique_ptr<Vehicle>`` pointing to a ``Taxi``.
       c. Call ``drive()`` on both pointers and observe runtime polymorphism.
       d. Create a ``std::vector<std::unique_ptr<Vehicle>>`` and iterate through it calling ``drive()`` on each element.

.. dropdown:: Exercise 3: Abstract Class with Pure Virtual Methods
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice defining an abstract base class with pure virtual methods and
    implementing concrete derived classes.

    **Specification**

    1. Create an abstract ``Sensor`` class with:

       - A ``protected`` ``std::string`` attribute ``sensor_id_``.
       - A constructor that initializes ``sensor_id_``.
       - A ``virtual`` destructor (``= default``).
       - A pure virtual method ``double read_value() const = 0``.
       - A pure virtual method ``std::string get_type() const = 0``.
       - A non-virtual method ``void display() const`` that prints the sensor ID, type, and current reading.

    2. Create a ``TemperatureSensor`` class that:

       - Inherits from ``Sensor``.
       - Has a ``private`` ``double`` attribute ``temperature_``.
       - Implements ``read_value()`` to return ``temperature_``.
       - Implements ``get_type()`` to return ``"Temperature"``.

    3. Create a ``DistanceSensor`` class that:

       - Inherits from ``Sensor``.
       - Has a ``private`` ``double`` attribute ``distance_``.
       - Implements ``read_value()`` to return ``distance_``.
       - Implements ``get_type()`` to return ``"Distance"``.

    4. In ``main()``, create a vector of ``unique_ptr<Sensor>`` and add both sensor types. Iterate and call ``display()`` on each.

    5. Verify that attempting to instantiate ``Sensor`` directly causes a compile error.

.. dropdown:: Exercise 4: Composition vs. Inheritance
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between "has-a" (composition) and "is-a"
    (inheritance) relationships by implementing both.

    **Specification**

    1. Create an ``Engine`` class with:

       - A ``private`` ``int`` attribute ``horsepower_``.
       - A ``public`` method ``start()`` that prints ``"Engine started (<hp> HP)"``.
       - A ``public`` method ``stop()`` that prints ``"Engine stopped"``.

    2. Create a ``GPS`` class with:

       - A ``private`` ``std::string`` attribute ``model_``.
       - A ``public`` method ``get_location()`` that prints ``"GPS (<model>): Location acquired"``.

    3. Create a ``Vehicle`` base class with:

       - **Composition**: An ``Engine`` member and a ``GPS`` member (has-a relationships).
       - A ``virtual`` destructor (``= default``).
       - A ``virtual`` method ``describe()`` that prints the vehicle type.

    4. Create a ``Truck`` class (derived from ``Vehicle``) that:

       - Has an additional ``private`` ``double`` attribute ``payload_capacity_``.
       - Overrides ``describe()`` to include payload capacity.

    5. In ``main()``, create a ``Truck``, start its engine, get its GPS location, and call ``describe()``.

.. dropdown:: Exercise 5: Virtual Destructors
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand why virtual destructors are essential in polymorphic
    hierarchies and observe the difference between virtual and non-virtual
    destructors.

    **Specification**

    1. Create a ``Base`` class with:

       - A **non-virtual** destructor that prints ``"~Base()"``.

    2. Create a ``Derived`` class (derived from ``Base``) with:

       - A ``private`` ``int*`` attribute ``data_`` allocated with ``new int[100]``.
       - A destructor that ``delete[]``'s ``data_`` and prints ``"~Derived()"``.

    3. In ``main()``:

       a. Create a ``Derived`` object on the stack and observe both destructors run.
       b. Create a ``Base*`` pointer to a ``new Derived()`` object, then ``delete`` it. Observe that only ``~Base()`` runs (resource leak).

    4. Now fix the problem by making the ``Base`` destructor ``virtual``. Re-run step 3b and confirm both destructors run.

    5. Run the fixed and unfixed versions through Valgrind and compare the memory leak reports.

.. dropdown:: Exercise 6 Challenge: Shape Hierarchy with Polymorphic Area Calculation
    :icon: rocket
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Build a complete shape hierarchy using abstract classes, pure virtual
    methods, ``override``, ``final``, virtual destructors, and smart pointers.

    **Specification**

    1. Create an abstract ``Shape`` class with:

       - A ``virtual`` destructor (``= default``).
       - A pure virtual method ``double area() const = 0``.
       - A pure virtual method ``std::string name() const = 0``.
       - A non-virtual method ``void print() const`` that prints the shape name and area.

    2. Create the following concrete classes:

       - ``Circle`` with a ``double`` radius. ``area()`` returns pi * r * r.
       - ``Rectangle`` with ``double`` width and height. ``area()`` returns width * height.
       - ``Triangle`` with ``double`` base and height. ``area()`` returns 0.5 * base * height.
       - ``Square final`` that inherits from ``Rectangle``. Constructor takes a single side length. Mark the class ``final``.

    3. In ``main()``:

       a. Create a ``std::vector<std::unique_ptr<Shape>>`` containing one of each shape type.
       b. Iterate through the vector and call ``print()`` on each shape.
       c. Calculate and print the total area of all shapes.
       d. Find and print the shape with the largest area.

    4. Verify that attempting to derive from ``Square`` causes a compile error.
