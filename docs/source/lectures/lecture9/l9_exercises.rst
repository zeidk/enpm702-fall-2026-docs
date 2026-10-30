====================================================
C++ Exercises
====================================================

These exercises cover Lecture 9: OOP Advanced. Exercise 1 is graded: hand
it in on Canvas before L10. Exercise 2 is practice, and you do not hand it
in.

The exercise works on the airport shuttles of the robotaxi company. A
``Shuttle`` is an abstract class with two concrete kinds, a dispatcher
shares the shuttles it quotes fares for, and a rider knows the shuttle
it boarded without keeping it alive.

.. note::

   Build the exercise from VS Code with CMake, as in the lecture. Add a
   target for it to ``project/week9/CMakeLists.txt``:

   .. code-block:: cmake

      add_executable(week9_shuttles exercises/shuttles.cpp)
      target_compile_options(week9_shuttles PRIVATE -fsanitize=address)
      target_link_options(week9_shuttles PRIVATE -fsanitize=address)

   ``-fsanitize=address`` turns on AddressSanitizer, so a ``delete``
   through the wrong type or a leak is reported. The course project
   already turns on the warnings, so fix every warning before you submit.

   Format the output as in the **Example Output**: a title between two lines
   of ``=``, and each part under a heading underlined with ``-``, with the
   labels in one column and the values after a ``:``.


----


.. dropdown:: Exercise 1: The Airport Shuttles
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a small class hierarchy as L9 does with ``Vehicle``: an
    abstract base class with pure ``virtual`` methods and a ``virtual``
    destructor, two ``final`` concrete classes that override them, a
    class that holds shuttles it shares (aggregation), a class that
    refers to a shuttle without owning it (association), and a ``struct``
    that the shuttles use for one call (dependency).

    **Specification**

    Write one program, ``project/week9/exercises/shuttles.cpp``, with the
    target ``week9_shuttles``. Write no ``new`` and no ``delete``. Every
    data member of a class is ``private``.

    1. Write a ``struct Trip`` with two members: ``destination`` (a
       ``std::string``) and ``distance_km`` (a ``double``, with the default
       member initializer ``0.0``). Any destination and distance make a
       trip, so it is a ``struct``.
    2. Write an abstract ``class Shuttle`` with two data members: an
       ``int id_`` and an ``int seats_`` (greater than 0, its invariant).
       Give it:

       - ``Shuttle(int id, int seats)``, which sets ``id_`` and
         ``seats_``, and throws ``std::invalid_argument`` with the message
         ``seats must be greater than 0`` when ``seats`` is not greater
         than 0.
       - ``virtual ~Shuttle() = default;``
       - Two pure ``virtual`` methods, both ``[[nodiscard]]`` and
         ``const``: ``double fare(const Trip& trip)``, the fare in dollars,
         and ``std::string kind()``, the name of the class.
       - ``get_id()`` and ``get_seats()``, both ``[[nodiscard]]``,
         ``const`` and ``noexcept``.

    3. Write two concrete classes, each ``final`` and derived from
       ``Shuttle`` with ``public``. Each constructor passes the id and the
       seats to ``Shuttle`` with a base class initializer. Mark each override
       ``override``. The fares are chosen for this exercise.

       - ``RoboShuttle``: ``RoboShuttle(int id, int seats)``. Its fare is
         2.50 + 1.20 × the distance in km, and its ``kind()`` is
         ``"RoboShuttle"``.
       - ``DrivenShuttle``: ``DrivenShuttle(int id, int seats, std::string driver_name)``,
         which moves the name into a ``driver_name_`` member. Its fare is
         6.00 + 0.90 × the distance in km, and its ``kind()`` is
         ``"DrivenShuttle"``.

    4. Write a ``class Dispatcher`` with one data member,
       ``std::vector<std::shared_ptr<Shuttle>> shuttles_``, and these
       methods. None of them names ``RoboShuttle`` or ``DrivenShuttle``.

       - ``void add(std::shared_ptr<Shuttle> shuttle)``, which throws
         ``std::invalid_argument`` with the message
         ``a dispatcher cannot hold a null shuttle`` for a null pointer,
         and does not add a shuttle that is already in the dispatcher.
       - ``bool remove(int id)``, which removes the shuttle with that id
         and returns ``false`` when there is none.
       - ``size()``, ``[[nodiscard]]``, ``const`` and ``noexcept``.
       - ``std::shared_ptr<Shuttle> cheapest(const Trip& trip) const``,
         the shuttle with the lowest fare for the trip. On a tie, the
         shuttle added first wins.
       - ``void print_quotes(const Trip& trip) const``, which prints one
         line per shuttle: its id, its ``kind()`` and its fare.

    5. Write a ``class Rider`` with two data members, ``name_`` (a
       ``std::string``, not empty) and ``ride_``
       (a ``std::weak_ptr<Shuttle>``). Give it:

       - ``explicit Rider(std::string name)``, which throws
         ``std::invalid_argument`` with the message ``a rider has a name``
         when the name is empty.
       - ``void board(const std::shared_ptr<Shuttle>& shuttle)`` and
         ``void leave() noexcept``.
       - ``std::string ride() const``, which returns ``shuttle`` and the
         shuttle's id while the shuttle exists, and ``none`` when it does
         not. Use ``lock()``.

    6. Write ``print_shuttle``. It takes a ``const Shuttle&`` and prints
       one line as in the Example Output.
    7. In ``main``:

       - Create three shuttles with ``std::make_shared`` and ``auto``:
         ``robo_a``, a ``RoboShuttle`` with id 1 and 4 seats; ``robo_b``,
         a ``RoboShuttle`` with id 2 and 6 seats; and ``driven``, a
         ``DrivenShuttle`` with id 3, 12 seats and the driver ``Ana``.
         Print them.
       - Create a ``Dispatcher``. Add ``robo_a``, ``robo_b``, ``driven``,
         and ``robo_a`` a second time. Print its size and
         ``robo_a.use_count()``.
       - For the trips to ``Union Station`` (5.0 km) and to
         ``BWI Airport`` (30.0 km), print the quotes and the cheapest
         shuttle.
       - Create a ``Rider`` named ``Maya`` and board ``driven``. Print her
         ride and ``driven.use_count()``. Remove shuttle 3 from the
         dispatcher, then call ``driven.reset()``. Print her ride and the
         dispatcher's size again.
       - Show that the rules hold: create a ``RoboShuttle`` with id 4 and 0 seats,
         a ``Rider`` with an empty name, and add ``nullptr`` to the
         dispatcher. Catch each exception and print its message.
       - Create ``std::unique_ptr<Shuttle> spare`` that owns a
         ``DrivenShuttle`` with id 5, 8 seats and the driver
         ``Ana Maria Rodrigues``. Print its kind and seats, and its fare to
         ``Inner Harbor`` (10.0 km). Call ``spare.reset()`` and print that
         it was released.

    8. Write the line ``class NightShuttle : public RoboShuttle {};``,
       build, read the error, and leave the line in the file as a comment
       that says why it does not compile.
    9. Remove ``virtual`` from ``~Shuttle``, build, and run. Copy the
       first line of the AddressSanitizer report into a comment, with one
       sentence that says why it happens. Then put ``virtual`` back.
    10. The program must end with no AddressSanitizer report.

    **Example Output**

    Fares have two digits after the decimal point, distances one.

    .. code-block:: text

       ====================================
         The Airport Shuttles
       ====================================

       Shuttles
       ------------------------------------
         shuttle 1 RoboShuttle    : 4 seats
         shuttle 2 RoboShuttle    : 6 seats
         shuttle 3 DrivenShuttle  : 12 seats

       Dispatcher
       ------------------------------------
         shuttles                 : 3
         owners of shuttle 1      : 2

       Quotes to Union Station (5.0 km)
       ------------------------------------
         shuttle 1 RoboShuttle    :   8.50
         shuttle 2 RoboShuttle    :   8.50
         shuttle 3 DrivenShuttle  :  10.50
         cheapest                 : shuttle 1 RoboShuttle

       Quotes to BWI Airport (30.0 km)
       ------------------------------------
         shuttle 1 RoboShuttle    :  38.50
         shuttle 2 RoboShuttle    :  38.50
         shuttle 3 DrivenShuttle  :  33.00
         cheapest                 : shuttle 3 DrivenShuttle

       Rider
       ------------------------------------
         Maya rides               : shuttle 3
         owners of shuttle 3      : 2
         Maya rides               : none
         shuttles                 : 2

       Rules Kept
       ------------------------------------
         caught: seats must be greater than 0
         caught: a rider has a name
         caught: a dispatcher cannot hold a null shuttle

       Owned through a Base Pointer
       ------------------------------------
         spare                    : DrivenShuttle, 8 seats
         to Inner Harbor          :  15.00
         spare                    : released


.. dropdown:: Exercise 2: Reading Association Lines
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    Each line below is written in PlantUML, as on the lecture's A Diagram as
    Text. ``-->`` is an arrow: the class at the arrow's point is the one that
    is known. The numbers are the multiplicities of each end.

    .. code-block:: text

       1.  Passenger "0..*" --> "0..1" Vehicle
       2.  Passenger "1" --> "1" Vehicle
       3.  Vehicle "0..1" --> "0..*" Passenger
       4.  Fleet "1" --> "1..*" Vehicle
       5.  Passenger "0..*" --> "1" Fleet

    For each line:

    a. Which class knows the other one?
    b. Say what the two numbers mean, as one sentence about passengers,
       vehicles or fleets.
    c. Which line is the one of the robotaxi design?

    .. dropdown:: Solution
        :class-container: sd-border-success

        1. A ``Passenger`` knows its ``Vehicle``; the vehicle does not know
           its passengers. A passenger rides at most one vehicle at a time
           (``0..1``), and a vehicle carries any number of passengers
           (``0..*``). This is the line of the robotaxi design: ``Passenger``
           holds ``ride_``, a ``std::weak_ptr<Vehicle>``.
        2. A ``Passenger`` knows its ``Vehicle``. Every passenger always rides
           exactly one vehicle, and every vehicle carries exactly one
           passenger: no passenger waits, and no vehicle drives empty.
        3. The arrow points the other way: a ``Vehicle`` knows its
           passengers, and a passenger does not know its vehicle. The numbers
           are those of line 1, so they say the same thing about how many.
        4. A ``Fleet`` knows its vehicles. A fleet has at least one vehicle
           (``1..*``), and each vehicle belongs to exactly one fleet (``1``).
        5. A ``Passenger`` knows one ``Fleet``: each passenger is a customer
           of exactly one fleet (``1``), and a fleet has any number of
           passengers (``0..*``).
