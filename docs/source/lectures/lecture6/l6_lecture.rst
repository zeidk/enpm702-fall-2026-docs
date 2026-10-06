====================================================
Lecture
====================================================

Learning Objectives
-------------------

1. Group values with a ``struct``, a ``std::pair``, or a ``std::tuple``, and predict a ``struct``'s size.
2. Return several values, or a value that may be missing, and unpack them with structured bindings.
3. Write a function template, and constrain it with a concept.
4. Write lambdas with captures, and pass them to the standard algorithms.
5. Write higher-order functions: pass, store, and adapt callables with ``std::function`` and ``std::bind``.

Code for This Lecture
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   project/week6/
   ├── CMakeLists.txt
   ├── fleet/
   │   ├── include/
   │   ├── src/
   │   └── docs/
   ├── snippets/
   ├── throws/
   └── undefined/

**Run the finished program first**

1. Get the code: ``git pull``, then ``702configure``.
2. Build it: ``702build week6_fleet``.
3. Run it: ``702run week6_fleet``. It prints the fleet, a summary, the robot chosen for a task at (5, 5), and three commands.

**Run a slide's code**

- One program per section, ``week6_grouping`` to ``week6_higher_order``. ``702run week6_grouping`` runs all of Section 1, Grouping Values; ``702run week6_grouping 7`` only slide 7.
- Code that does not compile is in the programs, commented out: uncomment it to get the slide's error.

``fleet`` holds the finished program; its Doxyfile is in ``fleet/docs``. ``throws`` and ``undefined`` hold one program per slide; ``week6_dangling`` is always built with AddressSanitizer.

.. note::

   The `Further Reading`_ part, after the summary, is the appendix of the slides. It is not presented. Read it on your own.

The Program We Will Build
-------------------------

A warehouse runs four robots. Today we write the **fleet manager**, a C++ program that tracks each robot's battery, position and state and picks a robot for each new task. Its **dispatcher**, the part that sends commands, tells a robot to "dock".

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Robot
     - Battery
     - Position (m, from the dock)
     - State
   * - 1
     - 82.5 %
     - (0, 0)
     - idle
   * - 2
     - 35.0 %
     - (4, 1)
     - busy
   * - 3
     - 64.0 %
     - (2, 3)
     - idle
   * - 4
     - 18.0 %
     - (6, 2)
     - idle

**States**

- **idle**: free to take a task.
- **busy**: carrying out a task.

**Commands**

- **dock**: return to the charging dock.
- **pause**: stop and hold position.
- **resume**: continue after a pause.
- Any other name is refused.

.. note::

   The robots are data in the program, not machines. Sending **dock** to robot 4 prints the line ``robot 4: go to dock``. Its position, battery and state do not change.

.. figure:: /_static/images/l6/narrative_gemini.jpeg
   :alt: An illustrated drawing on a parchment background. Left: the warehouse floor seen from above, on a 1 meter grid with x pointing right from 0 to 7 and y pointing up from 0 to 5. The origin is the charging dock, a yellow charging station in the bottom left corner. Four small wheeled robots, each with a numbered disc, stand on the floor, each labeled with its id, its state and a battery bar. Robot 1, idle, 82.5 %, sits in the dock at (0, 0). Robot 2, busy, 35 %, is at (4, 1) and is drawn in amber. Robot 3, idle, 64 %, is at (2, 3). Robot 4, idle, 18 %, is at (6, 2). Idle robots have a green ring. A row of wooden shelves runs along x at y = 4, and above it a blue star marks a new task, pickup at (5, 5). Right: a panel labeled Fleet manager, a C++ program, which tracks each robot's battery, position and state and picks a robot for each new task. Inside it, a panel labeled Dispatcher sends the commands dock, pause and resume, and for dock to robot 4 prints the line robot 4: go to dock. An arrow labeled status runs from the floor to the fleet manager, and an arrow labeled commands runs from the dispatcher back to the floor.
   :align: center
   :width: 100%

   The warehouse floor, seen from above, with the four robots and the new task at (5, 5). The fleet manager receives each robot's status, and its dispatcher sends the commands.

Grouping Values
---------------

A ``struct`` is a type you define. It gives one name to a group of variables, called **members**, that belong together. ``std::pair`` and ``std::tuple`` are ready-made groups from the standard library.

See `cppreference: classes <https://en.cppreference.com/w/cpp/language/classes>`__. Rule: `Core Guidelines C.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-org>`__.

Three Values, One Status
^^^^^^^^^^^^^^^^^^^^^^^^

The fleet manager asks robot 3 for its **status**: its battery level and its position x, y. A function that reads the status has three numbers to give back.

**Without a struct**

.. code-block:: cpp

   void get_status(int id,
       double& battery_pct,
       double& x, double& y);

   double battery_pct{};
   double x{};
   double y{};
   get_status(3, battery_pct, x, y);

**With a struct**

.. code-block:: cpp

   struct RobotStatus {
     double battery_pct;
     double x;
     double y;
   };

   RobotStatus get_status(int id);
   RobotStatus status{get_status(3)};

- Lecture 5 had only one way to give back three values: three reference parameters.
- A ``struct`` puts the three in one object. The function **returns** it, the way Lecture 5 says results should go back. Rule: `Core Guidelines F.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out>`__.

Declaring a ``struct``
^^^^^^^^^^^^^^^^^^^^^^

A ``struct`` is a type made of named members. Every object of the type holds its own copy of each member.

.. code-block:: cpp

   struct Position {
     double x;  // meters
     double y;
   };

.. code-block:: cpp

   struct RobotStatus {
     int id;
     double battery_pct;
     Position position;  // a struct
     bool busy;
   };  // the semicolon is required

- The declaration makes a **type**. No memory is used until you make an object: ``RobotStatus r{};``.
- A member can be a ``struct``: ``Position`` must be declared first. Leave out a final ``;`` and GCC says ``expected ';' after struct definition``.
- Type names on these slides start with a capital letter, so a type and a variable never share a name.

Where a ``struct`` Goes
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   struct RobotStatus;  // declared, not defined

   RobotStatus robot_status{};  // an object needs the size

.. code-block:: text

   incomplete_type.cpp:3:13: error: variable 'RobotStatus robot_status' has
     initializer but incomplete type

- To make an object, the compiler needs the **whole** definition in this ``.cpp``: the size and where each member sits.
- The linker cannot help. It joins functions by name and never sees types.
- A function is defined once per program (Lecture 5). A ``struct`` is defined once per ``.cpp``, and all copies must match.
- So the definition goes in one **header**, ``fleet/include/robot.hpp``, and every ``.cpp`` that uses it includes it.

See `struct or class`_ under Further Reading.

Initializing a ``struct``
^^^^^^^^^^^^^^^^^^^^^^^^^

In **aggregate initialization**, the members take their values from a braced list, in the order they are declared. It works because a plain ``struct`` is an **aggregate** (Lecture 4).

.. code-block:: cpp

   RobotStatus robot_3{3, 64.0, {2.0, 3.0}, false};  // all four
   RobotStatus id_only{3};   // the rest are 0 and false
   RobotStatus all_zero{};   // each member value-initialized: 0 and false
   RobotStatus no_braces;    // garbage, like int n;

- The inner ``{2.0, 3.0}`` initializes the ``Position`` member the same way.
- Members the list does not reach are set to zero. ``-Wextra`` warns about ``id_only`` anyway: ``missing initializer for member 'RobotStatus::battery_pct'``.
- ``no_braces`` holds garbage. Always use braces. Rule: `Core Guidelines ES.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-always>`__.

Default Member Initializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   struct RobotStatus {
     int id{0};
     double battery_pct{100.0};  // a new robot starts charged
     Position position{};        // Position has defaults too
     bool busy{false};
   };

   RobotStatus new_robot{};  // 0 100 (0, 0) idle
   RobotStatus robot_4{4, 18.0};                    // 4 18 (0, 0) idle
   RobotStatus robot_2{2, 35.0, {4.0, 1.0}, true};  // 2 35 (4, 1) busy

- A member can carry its own initializer. It is used whenever the braced list does not reach that member.
- The ``struct`` is still an aggregate, so the braced list works as before. This is the version in ``robot.hpp``.
- A member with a default never holds garbage, even after ``RobotStatus no_braces;``: it printed ``0 100 (0, 0) idle``.

Designated Initializers (C++20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   RobotStatus robot_1{.id = 1, .battery_pct = 82.5};  // idle at (0, 0)
   RobotStatus robot_2{.id = 2, .busy = true};         // battery 100
   RobotStatus robot_5{.battery_pct = 50.0, .id = 5};  // wrong order

.. code-block:: text

   designated_order.cpp:16:51: error: designator order for field 'RobotStatus::id'
     does not match declaration order in 'RobotStatus'

- Name the members you set, in declaration order. You may skip members, but you may not mix named and unnamed values.
- The file declares ``Position`` and ``RobotStatus`` above ``main``, so the error is on line 16.

.. note::

   C++20, **[dcl.init.list]**, section 9.4.4, paragraph 3.1: the designators *shall form a subsequence of the ordered identifiers in the direct non-static data members*.

Member Access
^^^^^^^^^^^^^

**Member access** names one member of an object: ``.`` on the object itself, ``->`` through a pointer to it (Lecture 3).

.. code-block:: cpp

   RobotStatus robot_status{3, 64.0, {2.0, 3.0}, false};
   std::cout << robot_status.id << ' '
             << robot_status.position.x << '\n';  // 3 2

   RobotStatus* status_ptr{&robot_status};
   // the same as (*status_ptr).battery_pct -= 10.0;
   status_ptr->battery_pct -= 10.0;
   std::cout << robot_status.battery_pct << '\n';  // 54

- ``robot_status.position.x`` reads two levels down: the ``x`` of the ``position`` of ``robot_status``.
- ``status_ptr->battery_pct`` is short for ``(*status_ptr).battery_pct``. Without the parentheses, ``*status_ptr.battery_pct`` means ``*(status_ptr.battery_pct)``, which does not compile.

A ``struct`` in Memory
^^^^^^^^^^^^^^^^^^^^^^

**Padding** is the unused bytes the compiler adds so each member's address is a multiple of its type's **alignment**: a power of 2, such as 4 for ``int`` and 8 for ``double``.

.. code-block:: cpp

   struct RobotStatus {
     int id;              // 4
     double battery_pct;  // 8
     Position position;   // 16
     bool busy;           // 1
   };
   // data: 4 + 8 + 16 + 1 = 29
   sizeof(RobotStatus);   // 40

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Bytes
     - Holds
     - Why
   * - 0 to 3
     - ``id``
     - first member
   * - 4 to 7
     - padding
     - next ``double`` at 8
   * - 8 to 15
     - ``battery_pct``
     - 8 is a multiple of 8
   * - 16 to 31
     - ``position``
     - two ``double``\ s
   * - 32
     - ``busy``
     - 
   * - 33 to 39
     - padding
     - ``sizeof`` goes from 33 to 40

- Offsets measured with ``offsetof``, alignments with ``alignof`` (g++ 13, x86-64). 11 of the 40 bytes hold nothing.

See `offsetof`_ and `alignof`_ under Further Reading.

Byte by Byte
~~~~~~~~~~~~

.. figure:: /_static/images/l6/struct_memory.png
   :alt: One row of 40 byte cells with a blue stack tab on the left. The members are outlined in blue and split into byte cells: id in bytes 0 to 3, then 4 gray padding bytes, 4 to 7, then battery_pct in bytes 8 to 15, position.x in bytes 16 to 23, position.y in bytes 24 to 31, busy in byte 32, labeled above the row, and 7 gray padding bytes, 33 to 39. The byte range of each part is printed under it. A brace under the whole row reads 40 bytes: 29 of data, 11 of padding, and a caption reads each double starts at a byte that is a multiple of 8: 8, 16, 24.
   :align: center
   :width: 100%

   The 40 bytes of a ``RobotStatus``, member by member. Gray bytes are padding.

- Gray bytes hold nothing. The 4 after ``id`` move ``battery_pct`` to byte 8, a multiple of 8.
- The 7 after ``busy`` make ``sizeof`` go from 33 to 40.

See `Without End Padding`_ under Further Reading.

Member Order
~~~~~~~~~~~~

.. code-block:: cpp

   struct RobotStatusSorted {
     double battery_pct;
     Position position;
     int id;
     bool busy;
   };
   // sizeof: 32

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Bytes
     - Holds
     - Why
   * - 0 to 7
     - ``battery_pct``
     - first member
   * - 8 to 23
     - ``position``
     - 8 is a multiple of 8
   * - 24 to 27
     - ``id``
     - 24 is a multiple of 4
   * - 28
     - ``busy``
     - any address
   * - 29 to 31
     - padding
     - ``sizeof`` goes from 29 to 32

- Same four members, 8 bytes smaller. Putting the largest members first leaves fewer gaps.
- It adds up: a log of one million status reports takes 40 MB in the first order and 32 MB in this one (10⁶ × 40 bytes against 10⁶ × 32 bytes).
- The compiler never reorders members for you. Their order in memory is the order you wrote.

Passing a ``struct``
^^^^^^^^^^^^^^^^^^^^

A copy of a ``struct`` copies every member, in order. Passing one by value copies all of it.

.. code-block:: cpp

   double get_battery(RobotStatus robot_status);  // copies 40 bytes
   double get_battery(const RobotStatus& robot_status);  // copies nothing
   RobotStatus make_new_robot(int id);  // returns by value

- Every rule from Lecture 5 applies unchanged. A ``struct`` is passed and returned like an ``int`` or a ``std::string``.
- ``RobotStatus`` is 40 bytes, more than Lecture 5's "small" (16 to 24 bytes on x86-64), so pass it by ``const&``.
- Rule: `Core Guidelines F.16 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-in>`__.

A Vector of ``RobotStatus``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{{1, 82.5, {0.0, 0.0}, false},
                                  {2, 35.0, {4.0, 1.0}, true},
                                  {3, 64.0, {2.0, 3.0}, false},
                                  {4, 18.0, {6.0, 2.0}, false}};

   for (const auto& robot : fleet) {
     std::cout << "robot " << robot.id << ": "
               << robot.battery_pct << " %"
               << (robot.busy ? ", busy\n" : ", idle\n");
   }

.. code-block:: text

   robot 1: 82.5 %, idle
   robot 2: 35 %, busy
   robot 3: 64 %, idle
   robot 4: 18 %, idle

- Each inner ``{...}`` initializes one ``RobotStatus``. Every container from Lecture 4 holds a type you wrote, with no change.
- ``const auto&`` again: read each element without copying its 40 bytes.

``push_back`` and ``emplace_back``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{};

   // push_back takes a whole RobotStatus: build one, then it goes in
   fleet.push_back(RobotStatus{1, 82.5, {0.0, 0.0}, false});

   // braces build it too: 2 fits int id
   fleet.push_back({2, 35.0, {4.0, 1.0}, true});

   // emplace_back builds it inside the vector, from the arguments
   fleet.emplace_back(3, 64.0, Position{2.0, 3.0}, false);
   fleet.emplace_back(4, 18.0);  // position and busy: defaults

.. code-block:: text

   robot 1: 82.5 % at (0, 0), idle
   robot 2: 35 % at (4, 1), busy
   robot 3: 64 % at (2, 3), idle
   robot 4: 18 % at (0, 0), idle

- ``push_back`` puts a finished ``RobotStatus`` into the vector. ``emplace_back`` passes its arguments on, as ``RobotStatus(3, 64.0, ...)``, and builds the robot in place.
- Building a ``struct`` from ``( )`` is new in C++20. Under ``-std=c++17``, both ``emplace_back`` lines fail: ``no matching function for call to 'RobotStatus::RobotStatus(int, double)'``.

Braces and ``emplace_back``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{};  // empty
   fleet.emplace_back({5, 90.0, {1.0, 1.0}, false});        // error
   fleet.emplace_back(5, 90.0, {1.0, 1.0}, false);          // error
   fleet.emplace_back(5, 90.0, Position{1.0, 1.0}, false);  // OK

   fleet.emplace_back(4.9, 50.0);  // OK, and the id is 4
   fleet.push_back({4.9, 50.0});   // error: 4.9 cannot narrow into int id

.. code-block:: text

   error: no matching function for call to
     'std::vector<RobotStatus>::emplace_back(int, double,
     <brace-enclosed initializer list>, bool)'

- ``emplace_back`` works out the type of each argument from the call. A braced list has no type, so that fails. Name the type: ``Position{1.0, 1.0}``.
- Parentheses allow narrowing: 4.9 becomes the id 4, with no warning even under ``-Wconversion``. Braces refuse it, so the ``push_back`` line is a compile error.

``std::pair``
^^^^^^^^^^^^^

``std::pair`` is a standard ``struct`` with two members, ``first`` and ``second``, of any two types. In ``<utility>``.

.. code-block:: cpp

   std::pair<int, double> reading{3, 64.0};  // robot 3, battery 64 %
   std::cout << reading.first << ' ' << reading.second << '\n'; // 3 64

   reading.second = 60.0;                    // first and second are public
   std::cout << reading.second << '\n';      // 60

- ``<int, double>`` gives the type of ``first``, then of ``second``.
- The braces fill ``first`` from 3 and ``second`` from 64.0, in that order, as for a ``struct``.

``std::tuple``
^^^^^^^^^^^^^^

``std::tuple`` is a standard type that holds any number of values, of any types, read by position. In ``<tuple>``.

.. code-block:: cpp

   // the id, the battery, busy
   std::tuple<int, double, bool> status{3, 64.0, false};
   std::cout << std::get<0>(status) << ' '
             << std::get<1>(status) << ' '
             << std::get<2>(status) << '\n';  // 3 64 0
   std::get<1>(status) = 60.0;
   std::cout << std::get<1>(status) << '\n';  // 60

- The number in ``std::get<1>`` is a position, counted from 0. It must be a constant.
- The values have no names: the reader must remember that 1 is the battery.
- ``std::get<3>(status)`` does not compile: ``tuple index must be in range``.
- Besides ``std::get``, there are three other ways to read a ``std::tuple``. Structured bindings come in `Structured Bindings`_. For the other two, see cppreference: `std::tie <https://en.cppreference.com/w/cpp/utility/tuple/tie>`__ and `std::apply <https://en.cppreference.com/w/cpp/utility/apply>`__.

Multiple and Optional Results
-----------------------------

A function returns one object. To give back several values, return one object that holds them. To give back a value that may be missing, return an object that can be **empty**.

Rule: `Core Guidelines F.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out-multi>`__.

Returning Several Values
^^^^^^^^^^^^^^^^^^^^^^^^

Returning a ``std::pair``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // How many full boxes, and how many parts are left over.
   std::pair<int, int> pack(int parts, int per_box) {
     // a braced list, as for a struct
     return {parts / per_box, parts % per_box};
   }

   std::pair<int, int> packed{pack(17, 5)};
   std::cout << packed.first << '\n';  // 3
   std::cout << packed.second << '\n';  // 2

- 17 parts, 5 per box: 17 / 5 = 3 full boxes, and 17 % 5 = 2 parts left over. Integer division drops the remainder; ``%`` gives it.
- ``first`` holds the boxes, ``second`` the parts left over: the order of the braced list.
- One function returns two values, with no reference parameters: compare ``get_status`` in `Three Values, One Status`_.

Returning a ``std::tuple``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // full boxes, parts left over, boxes needed
   std::tuple<int, int, int> pack_as_tuple(int parts, int per_box) {
     int full_boxes{parts / per_box};
     int left_over{parts % per_box};
     int boxes_needed{full_boxes};
     if (left_over > 0) { ++boxes_needed; }  // one more box for the rest
     return {full_boxes, left_over, boxes_needed};
   }

   std::tuple<int, int, int> packed{pack_as_tuple(17, 5)};
   std::cout << std::get<0>(packed) << '\n'; // 3
   std::cout << std::get<1>(packed) << '\n'; // 2
   std::cout << std::get<2>(packed) << '\n'; // 4

- A third value: the boxes needed. 3 full boxes hold 15 parts, and the 2 left over need one more box: 4.
- The tuple comes back from a braced list, in order, as the pair did.
- The caller reads by position. ``std::get<2>(packed)`` is the boxes needed, but nothing in the code says so.

Returning a ``struct``
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   struct Packing {
     int full_boxes;
     int left_over;
     int boxes_needed;
   };

   Packing pack_as_struct(int parts, int per_box) {
     int full_boxes{parts / per_box};
     int left_over{parts % per_box};
     int boxes_needed{full_boxes};
     if (left_over > 0) { ++boxes_needed; }
     return {full_boxes, left_over, boxes_needed};
   }

   Packing packing{pack_as_struct(17, 5)};
   std::cout << packing.boxes_needed << '\n';  // 4

- The same body and the same braced list: it fills the members in declaration order.
- The caller reads by name. ``packing.boxes_needed`` says what the value is.

``std::pair``, ``std::tuple``, or ``struct``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Return type
     - Read with
     - The caller sees
   * - ``std::pair``
     - ``.first``
     - which value is which? Check the function.
   * - ``std::tuple``
     - ``std::get<0>``
     - any number of values, still unnamed
   * - a ``struct``
     - ``.boxes_needed``
     - the meaning, in the member name

.. admonition:: Best Practice
   :class: tip

   Prefer a ``struct``: its member names say what comes back. Rule: `Core Guidelines F.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-out-multi>`__.

Structured Bindings
^^^^^^^^^^^^^^^^^^^

A **structured binding** is a declaration that gives a new name to each member of a ``struct``, a pair or a tuple, in declaration order. C++17.

.. code-block:: cpp

   auto [boxes, left_over] = pack(17, 5);
   std::cout << boxes << ' ' << left_over << '\n'; // 3 2

   auto [full, left, needed] = pack_as_struct(17, 5);
   std::cout << full << ' ' << left << ' ' << needed << '\n';  // 3 2 4

- The names are yours: ``full`` takes the first member, ``full_boxes``, and ``left`` the second, ``left_over``.
- The declaration always starts with ``auto``. You cannot give each name its own type.
- See `cppreference: structured binding <https://en.cppreference.com/w/cpp/language/structured_binding>`__.

By Value and by Reference
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::pair<int, int> packed{3, 2}; // full boxes, parts left over

   // copies packed
   auto [boxes, left_over] = packed;
   left_over = 0;
   std::cout << packed.second << '\n'; // 2: unchanged

   // refers to packed
   auto& [ref_boxes, ref_left_over] = packed;
   ref_left_over = 0;
   std::cout << packed.second << '\n'; // 0

- With ``auto``, the compiler makes one hidden copy of ``packed``. The names refer to the members of that copy.
- With ``auto&``, there is no copy. The names refer to the members of ``packed`` itself.
- The same three choices as a range-based ``for`` (Lecture 4): ``auto``, ``auto&``, ``const auto&``.

See `The Lecture 4 Map Loop`_ under Further Reading.

One Name per Member
~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   int main() {
     Packing packing{3, 2, 4};
     auto [full, left] = packing;
   }

.. code-block:: text

   binding_count.cpp:9:8: error: only 2 names provided for structured binding
   binding_count.cpp:9:8: note: while 'Packing' decomposes into 3 elements

- ``Packing`` has three members, so a binding needs three names. There is no way to skip one.

.. note::

   C++20, **[dcl.struct.bind]**, section 9.6, paragraph 5: *the number of elements in the identifier-list shall be equal to the number of non-static data members*.

``std::optional``
^^^^^^^^^^^^^^^^^

``std::optional<T>`` is a standard type that holds either one value of type ``T`` or nothing. In ``<optional>``, C++17.

**Without** ``std::optional``

.. code-block:: cpp

   int find_age(const std::string& name) {
     if (name == "Ana") { return 31; }
     if (name == "Ben") { return 24; }
     return -1;  // -1 means "no age"
   }

**With** ``std::optional``

.. code-block:: cpp

   std::optional<int> find_age(const std::string& name) {
     if (name == "Ana") { return 31; }
     if (name == "Ben") { return 24; }
     return std::nullopt;  // no age
   }

- Without: -1 is an ``int`` like any other. Nothing in the type says it means "missing", so a caller that forgets computes with it: ``find_age("Cy") + 1`` is 0, with no warning.
- With: the return type says the answer can be missing. ``return 31;`` fills the optional; ``return std::nullopt;`` returns it empty.

Finding an Idle Robot
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Id of the first idle robot with enough battery, if there is one.
   std::optional<int> find_idle_robot(
       const std::vector<RobotStatus>& fleet, double min_battery_pct) {
     for (const auto& robot : fleet) {
       if (!robot.busy && robot.battery_pct >= min_battery_pct) {
         return robot.id;
       }
     }
     return std::nullopt;  // the empty value
   }

- When no robot qualifies, there is no id to give back. The return type says that the answer can be missing.
- ``return robot.id;`` fills the optional. ``return std::nullopt;`` returns it empty.

Reading an Optional
~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{  // id, battery_pct, position, busy
       {1, 82.5, {0.0, 0.0}, false}, {2, 35.0, {4.0, 1.0}, true},
       {3, 64.0, {2.0, 3.0}, false}, {4, 18.0, {6.0, 2.0}, false}};

   std::optional<int> idle{find_idle_robot(fleet, 50.0)};

   if (idle) {                                 // or idle.has_value()
     std::cout << "robot " << *idle << '\n';   // robot 1
   }

- Robot 1 is idle with 82.5 %, the first robot that qualifies, so ``idle`` holds 1.
- ``if (idle)`` is true when the optional holds a value. ``idle.has_value()`` says the same.
- ``*idle`` gives the value inside. ``idle`` is not a pointer: ``std::optional`` defines ``*`` and ``->`` so it reads like one.

A Fallback Value
~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{  // id, battery_pct, position, busy
       {1, 82.5, {0.0, 0.0}, false}, {2, 35.0, {4.0, 1.0}, true},
       {3, 64.0, {2.0, 3.0}, false}, {4, 18.0, {6.0, 2.0}, false}};

   std::optional<int> none{find_idle_robot(fleet, 90.0)};

   // prints 0 -1
   std::cout << none.has_value() << ' ' << none.value_or(-1) << '\n';

- No robot has 90 %, so ``none`` is empty: ``has_value()`` is false, printed as 0.
- ``value_or(-1)`` gives the value inside, or -1 when there is none.
- Here the caller chooses -1, to print something. ``find_idle_robot`` itself never returns -1: its type says the answer can be missing.

Three Ways to Read
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Read with
     - If the optional is empty
   * - ``*idle``
     - undefined behavior: check first
   * - ``idle.value()``
     - **throws** ``std::bad_optional_access``
   * - ``idle.value_or(fallback)``
     - gives ``fallback``

- Check with ``if (idle)`` before ``*idle``, or use ``value()`` or ``value_or()``.

An Empty Optional
~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::optional<int> idle;
   std::cout << idle.value();

.. code-block:: text

   terminate called after throwing
     an instance of
     'std::bad_optional_access'
     what():  bad optional access

.. code-block:: cpp

   std::optional<int> idle;
   std::cout << *idle;

.. code-block:: text

   0

- ``value()`` **throws**: it reports the problem in a way the program can catch. Nothing catches it here, so the program stops with exit status 134. Lecture 4's ``at()`` behaves the same way.
- ``*`` does no check. It printed ``0``, with no warning and no error. That is undefined behavior: the next build may print anything.
- How to catch a thrown exception is in the **exceptions reading**.

``std::optional``, Pointer, or Special Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``find_idle_robot`` looks for a robot and may find none. Here are three separate ways to write it, one version at a time.

1. **A special value.** It returns the robot's id as an ``int``, and -1 means "none". That works only because ids are never negative. Nothing makes the caller check: one who forgets uses -1 as an id.
2. **A null pointer** (Lecture 3). It returns ``const RobotStatus*``, the address of the robot inside the vector, and ``nullptr`` means "none". When the vector grows, ``push_back`` moves every robot to new memory (Lecture 4), and the pointer then points where the robot used to be.
3. **An empty ``std::optional``.** It returns ``std::optional<int>``, which holds its own copy of the id. "None" is its own state, empty, instead of a number that only looks like an id.

.. note::

   Pick the pointer when the caller must change the robot itself, for example to mark it busy: a copy would change only the copy. Pick ``std::optional`` when the answer is a value, such as an id. The empty state costs memory: with g++ 13, ``std::optional<int>`` takes 8 bytes and an ``int`` takes 4. See `cppreference: std::optional <https://en.cppreference.com/w/cpp/utility/optional>`__.

Function Templates
------------------

A **function template** is a pattern for a family of functions. The compiler writes one function from it for each set of types you call it with.

See `cppreference: function template <https://en.cppreference.com/w/cpp/language/function_template>`__.

One Body, Several Overloads
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // a speed command, in percent
   int clamp_value(int value, int low, int high) {
     if (value < low) { return low; }
     if (value > high) { return high; }
     return value;
   }

   // a battery reading, in percent
   double clamp_value(double value, double low, double high) {
     if (value < low) { return low; }
     if (value > high) { return high; }
     return value;
   }

- Lecture 5's overloads, one per type. A speed command of 130 % becomes 100; a faulty battery reading of 104.2 % becomes 100.0.
- The bodies are **identical**. Only the type changes. A fix to one must be copied into every other.
- Overloads are right when each type needs **different** code. Here the code is the same, so the type should be a parameter.

See `Overload or Specialize`_ under Further Reading.

Declaring a Template
^^^^^^^^^^^^^^^^^^^^

A **template parameter** is a name, here ``T``, that stands for a type in a function template. The line ``template <typename T>`` introduces it.

.. code-block:: cpp

   template <typename T>
   T clamp_value(T value, T low, T high) {
     if (value < low) { return low; }
     if (value > high) { return high; }
     return value;
   }

- Read it as: "for any type ``T``, here is a function that takes three ``T``\ s and returns a ``T``".
- ``typename`` and ``class`` mean the same thing in this line. These slides use ``typename``.
- The body needs ``<`` and ``>`` on ``T``. A type without them cannot be used here.

Instantiation
~~~~~~~~~~~~~

**Instantiation** is the compiler writing a real function from a template, for the types of one call.

.. code-block:: cpp

   int speed_pct{clamp_value(130, 0, 100)};            // 100
   double battery_pct{clamp_value(104.2, 0.0, 100.0)}; // 100
   int other_pct{clamp_value(50, 0, 100)};             // 50

.. code-block:: bash

   nm -C week6_templates | grep 'clamp_value<'
   ... W double clamp_value<double>(double, double, double)
   ... W int clamp_value<int>(int, int, int)

- Two functions in the program, one per type. The third call reuses ``clamp_value<int>``.
- ``nm`` lists the functions in a compiled program; ``-C`` shows their C++ names. ``702bin`` takes you to the folder that holds ``week6_templates``.

Templates Go in Headers
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // Split like a normal function (Lecture 5): does NOT link
   // stats.hpp: the declaration only
   template <typename T> T clamp_value(T value, T low, T high);
   // stats.cpp: includes stats.hpp, then the definition
   template <typename T> T clamp_value(T value, T low, T high) { ... }
   // main.cpp: includes stats.hpp, then
   double pct{clamp_value(104.2, 0.0, 100.0)};

.. code-block:: text

   main.cpp:(.text+0x29): undefined reference to
     `double clamp_value<double>(double, double, double)'

.. code-block:: cpp

   // The fix: the whole template in stats.hpp, and no stats.cpp
   template <typename T> T clamp_value(T value, T low, T high) { ... }

- The same three files with a regular function link and run (Lecture 5). With a template, the linker finds nothing.
- The fix is what ``fleet/include/stats.hpp`` does: the exception to Lecture 5's rule.

Why a Regular Function Links
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The same split, compiled twice. ``nm -C`` lists what an object file **defines** (``T``) and what it **needs** from another file (``U``).

**Regular function**, with ``double`` in place of ``T``:

.. code-block:: text

   stats.o:  T clamp_value(double, double, double)
   main.o:   U clamp_value(double, double, double)

**Template**, as in `Templates Go in Headers`_:

.. code-block:: text

   stats.o:  (nothing)
   main.o:   U double clamp_value<double>(double, double, double)

- Regular function: ``stats.cpp`` compiles the body once. The linker matches the ``U`` in ``main.o`` with the ``T`` in ``stats.o``, and the program prints 100.
- Template: a version is compiled only where a call needs it. ``stats.cpp`` has the body but no call; ``main.cpp`` has the call but no body. No ``T`` anywhere.
- So the body goes in the header, where every call can see it.

Template Argument Deduction
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In **template argument deduction**, the compiler works out ``T`` from the types of the arguments in the call.

.. code-block:: cpp

   clamp_value(130, 0, 100);          // three ints:    T is int
   clamp_value(104.2, 0.0, 100.0);    // three doubles: T is double

- You call a template the way you call any function. The ``<int>`` is filled in for you.
- Each argument is compared with its parameter. Here all three parameters are ``T``, so all three arguments must give the **same** ``T``.

One T for Every Argument
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   template <typename T>
   T clamp_value(T value, T low, T high) {
     if (value < low) { return low; }
     if (value > high) { return high; }
     return value;
   }

   int main() {
     double pct{clamp_value(104, 0.0, 100.0)};
     return pct > 50.0;
   }

.. code-block:: text

   deduce_conflict.cpp:9:25: error: no matching function for call to
     'clamp_value(int, double, double)'
   deduce_conflict.cpp:9:25: note:   deduced conflicting types for parameter 'T'
     ('int' and 'double')

- ``104`` says ``T`` is ``int``; ``0.0`` says ``double``. Deduction does not pick one: it fails.
- An ordinary function would have converted ``104`` to ``104.0``. Deduction looks at the types exactly as written, with no conversions.

Explicit Template Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   template <typename T>
   T make_zero() { return T{}; }

   int speed_reading{104};  // from a sensor, an int
   double pct{clamp_value<double>(speed_reading, 0.0, 100.0)};  // 100
   double zero{make_zero<double>()};                            // 0

- ``<double>`` sets ``T`` yourself, so there is nothing to deduce. ``speed_reading`` then converts from ``int`` to ``double`` like any argument.
- Why not write ``104.0``? That works only for a number you type in. Without ``<double>``, ``clamp_value(speed_reading, 0.0, 100.0)`` fails with ``deduced conflicting types``.
- No argument of ``make_zero`` mentions ``T``, and the variable that receives the result is not used for deduction. So ``<double>`` is the only way: ``make_zero()`` fails with ``couldn't deduce template parameter 'T'``.

.. note::

   C++20, **[temp.arg.explicit]**, section 13.10.1, paragraph 7: *Template parameters do not participate in template argument deduction if they are explicitly specified*, so the argument is converted to the parameter's type.

Two Template Parameters
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   template <typename T, typename U>
   auto add_offset(T value, U offset) {
     return value + offset;
   }

   add_offset(80, 15);     // T int,   U int:    returns int 95
   add_offset(80, 2.5);    // T int,   U double: returns double 82.5
   add_offset(80.5f, 2);   // T float, U int:    returns float 82.5

- Two parameters, deduced separately, so the arguments may differ in type.
- What is the return type? It depends on ``T`` and ``U``. ``auto`` lets the compiler take it from the ``return`` statement, by the arithmetic conversions of Lecture 2.
- The three return types are checked with ``static_assert`` in ``templates.cpp``.

See `decltype and Trailing Return Types`_ under Further Reading.

Abbreviated Templates
^^^^^^^^^^^^^^^^^^^^^

An **abbreviated function template** is a function with ``auto`` as a parameter type. It is a template, written without the ``template`` line. C++20.

.. code-block:: cpp

   void print_all(const auto& values) {
     for (const auto& value : values) {
       std::cout << value << ' ';
     }
     std::cout << '\n';
   }

   print_all(std::vector<int>{1, 2, 3, 4});
   print_all(std::vector<double>{82.5, 35.0});

.. code-block:: text

   1 2 3 4
   82.5 35

- It means ``template <typename T> void print_all(const T& values)``.
- Each ``auto`` parameter gets its **own** template parameter. Two ``auto``\ s can be two different types.
- It is still a template, so it still goes in the header.

Concepts
^^^^^^^^

A **concept** is a named test on a template parameter. The compiler runs it at each call, before it writes the function. If the test fails, the call does not compile. C++20, header ``<concepts>``.

**Without a concept**

.. code-block:: cpp

   template <typename T>
   T average_of(
       const std::vector<T>& values);

**With a concept**

.. code-block:: cpp

   template <std::floating_point T>
   T average_of(
       const std::vector<T>& values);

- The two are the same function with the same body. Only the first line differs.
- Left: ``T`` can be any type, ``int`` included. Right: ``T`` must pass ``std::floating_point``, a standard concept that ``float``, ``double`` and ``long double`` pass, and ``int`` does not.
- Why it matters: the body divides the sum by the count. With ``int``, that is integer division, and the average loses its fraction (see `A Call That Compiles and Is Wrong`_).
- See `cppreference: constraints and concepts <https://en.cppreference.com/w/cpp/language/constraints>`__.

A Call That Compiles and Is Wrong
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // with template <typename T>: no concept
   average_of(std::vector<double>{82.5, 35.0, 64.0, 18.0});  // 49.875
   average_of(std::vector<int>{80, 35, 64, 18});  // 49, not 49.25

   // with template <std::floating_point T>
   average_of(std::vector<int>{80, 35, 64, 18});  // rejected

.. code-block:: text

   average_int.cpp:5:3: note: constraints not satisfied

- Some robots report their battery as a whole-number percent. Without the concept, ``T`` is ``int``: 80 + 35 + 64 + 18 = 197, and 197 / 4 is integer division, 49.
- No warning, even under ``-Wall -Wextra``. The concept turns that silent wrong answer into a compile error.
- The requirement is part of the declaration, where the caller reads it. Rule: `Core Guidelines T.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concepts>`__.

Form 1: In Place of ``typename``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   template <std::integral T>   // T must be an integral type
   bool is_valid_id(T id) { return id > 0; }

   is_valid_id(3);      // true
   is_valid_id(-2L);    // false: -2L is a long, also integral
   is_valid_id(true);   // true: bool is integral too
   is_valid_id(2.5);    // does not compile: double is not integral

- Read the first line as: ``T`` is any type that passes ``std::integral``. The concept takes the place of ``typename``.
- The rejected call stops with ``constraints not satisfied``.

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Standard concept
     - Accepts
   * - ``std::integral``
     - ``bool``, the ``char`` types, and the signed and unsigned integer types (``int``, ``long``, ...)
   * - ``std::floating_point``
     - ``float``, ``double``, ``long double``
   * - ``std::totally_ordered``
     - types whose values compare with ``==``, ``<``, ``>``, ``<=``, ``>=`` in one consistent order

See `std::totally_ordered`_ under Further Reading.

Form 2: A ``requires`` Clause
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   template <typename T>
     requires std::integral<T> && (!std::same_as<T, bool>)
   bool is_valid_id(T id) { return id > 0; }

   is_valid_id(3);      // true
   is_valid_id(true);   // does not compile now: T is bool

- ``requires`` is followed by a condition that the compiler checks at each call. Here: ``T`` is integral, and ``T`` is not ``bool``.
- ``std::integral<T>`` is true or false for one type. So is ``std::same_as<T, bool>``, a standard concept that is true when the two types are the same.
- Why exclude ``bool``: in form 1, ``is_valid_id(true)`` compiles and returns true, but a ``bool`` is not an id.
- Only this form can join tests with ``&&`` and ``||``. A test that starts with ``!`` needs parentheses. Without them, g++ stops with ``expression must be enclosed in parentheses``.

Form 3: Before ``auto``
~~~~~~~~~~~~~~~~~~~~~~~

**Form 1: the type has a name**

.. code-block:: cpp

   template <std::integral T>
   bool same_id(T first, T second) {
     return first == second;
   }
   same_id(3, 3);   // true
   same_id(3, 3L);  // does not compile

**Form 3: no name**

.. code-block:: cpp

   bool same_id(
       std::integral auto first,
       std::integral auto second) {
     return first == second;
   }
   same_id(3, 3);   // true
   same_id(3, 3L);  // true

- With one parameter the two forms accept the same calls: ``is_valid_id(std::integral auto id)`` behaves like form 1.
- With two, they differ. Form 1 names the type ``T``, and both parameters are ``T``, so they must be one type: ``3`` is an ``int``, ``3L`` a ``long``, and the call fails (see `One T for Every Argument`_).
- Form 3 has no name. Each ``auto`` is its own type, so ``int`` and ``long`` are both accepted.

See `Documenting a Template`_ under Further Reading.

Which Form to Use
~~~~~~~~~~~~~~~~~

1. **Form 3 by default:** each parameter has its own simple requirement, and the types may differ.

   .. code-block:: cpp

      bool same_id(std::integral auto first, std::integral auto second);

2. **Form 1** when two parameters must be one type, or the body or return type needs the name ``T``.

   .. code-block:: cpp

      template <std::integral T>
      bool same_id(T first, T second);

3. **Form 2** when the condition joins tests with ``&&``, ``||`` or ``!``.

   .. code-block:: cpp

      template <typename T>
        requires std::integral<T> && (!std::same_as<T, bool>)
      bool is_valid_id(T id);

.. admonition:: Best Practice
   :class: tip

   Constrain every template parameter; a bare ``typename T`` only when any type works (`T.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-concepts>`__). For a simple concept, the shorter form: `Core Guidelines T.13 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-shorthand>`__ ranks ``requires`` "correct but verbose", form 1 "better" and form 3 "best".

Higher-Order Functions
----------------------

A **callable** is anything you can call with parentheses: a function, a lambda, a pointer to a function, or an object that holds one of them. A **higher-order function** takes a callable as a parameter, or returns one.

See `cppreference: Callable <https://en.cppreference.com/w/cpp/named_req/Callable>`__.

A Condition instead of a Value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   bool is_low(double pct) { return pct < 40.0; }  // outside main

   std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};

   std::count(battery_pct.begin(), battery_pct.end(), 35.0);       // 1
   std::count_if(battery_pct.begin(), battery_pct.end(), is_low);  // 2

A **predicate** is a function that answers yes or no: it returns a ``bool``. ``std::count_if`` wants one that takes one value; some algorithms want one that takes two.

- ``std::count`` (Lecture 4) asks: how many levels **equal** 35.0? One does, so it returns 1.
- ``std::count_if`` asks: for how many levels does ``is_low`` say yes? It calls ``is_low`` on 82.5, 35.0, 64.0 and 18.0 and gets false, true, false, true. Two yeses, so it returns 2.
- ``std::count_if`` is a higher-order function. Pass the name ``is_low``, with no parentheses: ``std::count_if`` makes the calls. ``is_low()`` would call it right there, with no argument, and fails with ``too few arguments to function``.
- The catch: ``is_low`` sits outside ``main``, far from the one line that uses it, and 40 is fixed inside it. Counting levels below 50 would need a second function.

Lambdas
-------

The callable in `A Condition instead of a Value`_, ``is_low``, is a function defined far from its one use. A **lambda** is a callable written right where it is used.

See `cppreference: lambda expressions <https://en.cppreference.com/w/cpp/language/lambda>`__. Rule: `Core Guidelines F.50 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-capture-vs-overload>`__.

Lambda Expressions
^^^^^^^^^^^^^^^^^^

A **lambda expression** is an expression that creates a function object. It has three parts: captures in ``[ ]``, parameters in ``( )``, and a body in ``{ }``.

.. code-block:: cpp

   [captures](parameters) { body }

.. code-block:: cpp

   // create it and call it at once: true
   [](double pct) { return pct < 40.0; }(35.0);
   // create it and store it
   auto is_low = [](double pct) { return pct < 40.0; };
   is_low(35.0);  // true: call it like a function
   is_low(64.0);  // false

- The test of the function ``is_low``: ``(double pct)`` is the parameter, the body returns a ``bool``. ``[]`` is empty: it uses nothing around it.
- ``(35.0)`` right after the closing brace calls the lambda once, where it is made: a lambda is a callable.
- To call it again, store it in ``is_low``. Its type has no name you can write, so ``auto``.

Passing a Lambda
~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};
   auto is_low = [](double pct) { return pct < 40.0; };
   std::count_if(battery_pct.begin(), battery_pct.end(), is_low);  // 2

   // the same lambda, written directly in the call
   std::count_if(battery_pct.begin(), battery_pct.end(),
                 [](double pct) { return pct < 40.0; });  // 2

- ``std::count_if`` takes the lambda where `A Condition instead of a Value`_ passed the function ``is_low``. Both are callables, and both answer the same test.
- Written in the call, the lambda needs no name: it is used once, on the line that defines it. The test sits next to the one line that uses it, which fixes half of the catch in `A Condition instead of a Value`_.

``std::find_if`` with a Lambda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{  // id, battery_pct, position, busy
       {1, 82.5, {0.0, 0.0}, false}, {2, 35.0, {4.0, 1.0}, true},
       {3, 64.0, {2.0, 3.0}, false}, {4, 18.0, {6.0, 2.0}, false}};
   auto is_busy = [](const RobotStatus& robot) { return robot.busy; };
   auto first_busy = std::find_if(fleet.begin(), fleet.end(), is_busy);
   first_busy->id;  // 2

- ``std::find_if`` searches a range for the **first** element for which a predicate returns ``true``, and returns an iterator to it.
- ``is_busy`` is that predicate: a lambda kept in a variable, written next to the line that uses it.
- ``std::find_if`` calls ``is_busy`` on each robot, in order, and stops at the first ``true``. Robot 1 is idle, robot 2 is busy: two calls, and it stops at robot 2.
- It returns an iterator to that robot, so ``first_busy->id`` is 2. If no robot is busy, it returns ``fleet.end()``, which must not be dereferenced (Lecture 4).

``std::sort`` with a Lambda
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<RobotStatus> fleet{  // id, battery_pct, position, busy
       {1, 82.5, {0.0, 0.0}, false}, {2, 35.0, {4.0, 1.0}, true},
       {3, 64.0, {2.0, 3.0}, false}, {4, 18.0, {6.0, 2.0}, false}};
   // true when left must come before right: more battery first
   auto higher_battery = [](const RobotStatus& left,
                            const RobotStatus& right) {
     return left.battery_pct > right.battery_pct;
   };
   std::sort(fleet.begin(), fleet.end(), higher_battery);
   // ids in order: 1 3 2 4

- ``std::sort`` puts the elements of a range in order, in place: the vector itself is rearranged. With no rule, it compares with ``<``.
- ``RobotStatus`` has no ``<``, so the sort needs a rule that says which of two robots comes first. The lambda takes two robots and returns ``true`` when ``left`` must come before ``right``.
- With ``>``, more battery comes first: 82.5, 64, 35 and 18 % put the robots in the order 1, 3, 2, 4.

See `std::transform`_ and `Projections (C++20)`_ under Further Reading.

Captures
^^^^^^^^

A **capture** is a local variable of the enclosing function that the lambda keeps and uses. You list it in the ``[ ]``.

.. code-block:: cpp

   std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};
   double limit_pct{40.0};  // a local variable of main
   auto is_low = [limit_pct](double pct) { return pct < limit_pct; };
   std::count_if(battery_pct.begin(), battery_pct.end(), is_low);  // 2

- ``[limit_pct]`` captures ``limit_pct``: the lambda keeps its own copy, made when the lambda is created.
- In the body, ``pct`` comes from each call and ``limit_pct`` from the capture. A lambda body sees only its parameters and its captures.
- The limit is no longer written inside the test, the catch in `A Condition instead of a Value`_: the code around the lambda chooses it.

By Value and by Reference
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};
   double limit_pct{40.0};
   auto is_low = [limit_pct](double pct) { return pct < limit_pct; };
   auto is_low_ref = [&limit_pct](double pct) { return pct < limit_pct; };

   limit_pct = 70.0;
   std::count_if(battery_pct.begin(), battery_pct.end(), is_low);      // 2
   std::count_if(battery_pct.begin(), battery_pct.end(), is_low_ref);  // 3
   limit_pct = 20.0;
   std::count_if(battery_pct.begin(), battery_pct.end(), is_low_ref);  // 1

- ``[limit_pct]`` copies 40 **when the lambda is created**. It counts levels under 40 on every call: 35 and 18, so 2.
- ``[&limit_pct]`` stores a reference. Each call reads ``limit_pct`` **at that moment**: under 70 gives 3, under 20 gives 1.
- The same choice as a parameter in Lecture 5: by value or by reference.

Capture Lists
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Capture list
     - The lambda gets
   * - ``[]``
     - nothing
   * - ``[limit_pct]``
     - a copy of ``limit_pct``
   * - ``[&limit_pct]``
     - a reference to ``limit_pct``
   * - ``[limit_pct, &fleet]``
     - a copy of ``limit_pct`` and a reference to ``fleet``
   * - ``[=]``
     - a copy of every local the body uses
   * - ``[&]``
     - a reference to every local the body uses

- ``[=]`` and ``[&]`` are **capture defaults**. Naming each variable shows the reader exactly what the lambda depends on.

.. admonition:: Best Practice
   :class: tip

   By reference is fine for a lambda used here and now, such as one passed to an algorithm (`F.52 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-reference-capture>`__). Capture by value for a lambda that is returned or stored (`F.53 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-value-capture>`__).

See `mutable and Init-capture`_ under Further Reading.

What the Compiler Writes
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   double limit_pct{40.0};
   auto is_low =
       [limit_pct](double pct) {
         return pct < limit_pct;
       };

.. code-block:: cpp

   struct IsLow {
     double limit_pct;  // the capture
     bool operator()(double pct) const {
       return pct < limit_pct;
     }
   };
   IsLow is_low_struct{limit_pct};

- The lambda is an object of an unnamed ``struct``. Each capture is a **member**; the body becomes a member function named ``operator()``, which runs when you write ``a(30.0)``. Member functions are Lecture 8.
- Both count 2 levels, and both are 8 bytes: one ``double``. A lambda with no capture measured 1 byte, one with two references 16.
- The ``const`` on ``operator()`` is why a capture copied by value is read-only inside the body.

.. note::

   C++20, **[expr.prim.lambda.closure]**, section 7.5.5.1, paragraph 1: the type of a lambda-expression *is a unique, unnamed non-union class type, called the closure type*.

A Dangling Capture
~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   auto make_filter(double limit_pct) {
     return [&limit_pct](double pct) { return pct < limit_pct; };
   }

   int main() {
     auto is_low = make_filter(40.0);
     std::cout << is_low(30.0) << '\n';  // should be 1
   }

.. code-block:: text

   702run week6_dangling                 # always built with AddressSanitizer
   ERROR: AddressSanitizer: stack-use-after-return on address 0x...
       #0 0x... in operator() dangling_capture.cpp:4

- ``limit_pct`` is a parameter. It dies when ``make_filter`` returns, and the lambda keeps a reference to it: Lecture 5's dangling reference, hidden in a capture list.
- Built without the sanitizer, it printed ``0`` with no warning. At ``-O2`` GCC warns, under a misleading name: ``'limit_pct' is used uninitialized``.
- The fix is ``[limit_pct]``. A lambda that leaves the function captures by value (F.53).

Generic Lambdas
^^^^^^^^^^^^^^^

A **generic lambda** is a lambda with ``auto`` as a parameter type. Like an abbreviated function template, it works for any types that the body accepts.

.. code-block:: cpp

   auto larger = [](const auto& left, const auto& right) {
     return left > right ? left : right;
   };

   larger(3, 7);                                          // 7
   larger(82.5, 64.0);                                    // 82.5
   larger(std::string{"dock"}, std::string{"aisle 4"});   // dock

- One lambda, three calls, three types. The compiler instantiates its call for each, as for a template.
- Each ``auto`` is separate, so ``larger(3, 7.5)`` also compiles and returns ``7.5``.

See `The Return Type of a Lambda`_ under Further Reading.

Storing and Adapting Callables
------------------------------

``std::count_if`` calls ``is_low`` right away (see `A Condition instead of a Value`_). To keep a callable for later, store it in a ``std::function``. To fix some of its arguments, make a new callable with ``std::bind``.

See `cppreference: function objects <https://en.cppreference.com/w/cpp/utility/functional>`__.

``std::function``
^^^^^^^^^^^^^^^^^

``std::function`` is a standard type that can hold any callable with a given signature, captures included. In ``<functional>``.

.. code-block:: cpp

   std::function<double(double)> convert{to_fraction};
   std::cout << convert(64.0) << '\n';  // 0.64

   double scale{2.0};
   convert = [scale](double pct) { return scale * pct; };
   std::cout << convert(64.0) << '\n';  // 128

- ``double(double)`` in the brackets is the signature: one ``double`` in, one ``double`` out.
- The same variable held a function, then a capturing lambda. Their types differ; the signature is what they share.

A Table of Commands
~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::map<std::string, std::function<void(int)>> on_command;

   on_command["dock"] = [](int id) {
     std::cout << "robot " << id << ": go to dock\n";
   };
   on_command["pause"] = [](int id) {
     std::cout << "robot " << id << ": paused\n";
   };

   on_command["dock"](4);   // robot 4: go to dock
   on_command["pause"](2);  // robot 2: paused

- A **callback** is a function you hand over now, for other code to call later. Each command name maps to its callback.
- The dispatcher only has to look up the command and call what it finds. A new command means a new entry, not a new ``if``. The full version is ``fleet/src/dispatcher.cpp``.

An Empty std::function
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   std::map<std::string, std::function<void(int)>> on_command;
   on_command["reboot"](2);   // no handler was ever stored

.. code-block:: text

   terminate called after throwing an instance of 'std::bad_function_call'
     what():  bad_function_call

- Lecture 4's trap: ``operator[]`` on a map **inserts** a missing key. Here it inserts an empty ``std::function``.
- Calling an empty ``std::function`` **throws**. Nothing catches it, so the program stops with exit status 134, as an empty optional's ``value()`` did.
- Look first, without inserting: ``auto handler{on_command.find("reboot")};`` then call ``handler->second(2)`` only if ``handler != on_command.end()``. ``fleet/src/dispatcher.cpp`` does exactly that.

See `std::source_location`_ under Further Reading.

Choosing a Parameter Type
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Parameter
     - Accepts
     - Use it when
   * - ``double (*convert)(double)``
     - functions, lambdas with no capture
     - a C library asks for one
   * - ``auto convert``
     - any callable
     - the function calls ``convert`` before it returns
   * - ``std::function<double(double)>``
     - any callable with that signature
     - ``convert`` is stored to be called later

- The standard algorithms take the second form: the callable is a template parameter, passed by value, so each call is instantiated for the exact lambda type.
- ``std::function`` pays for holding any callable: its ``sizeof`` measured 32 bytes, against 8 for a function pointer.

.. admonition:: Best Practice
   :class: tip

   Pass an operation as a lambda, not a function pointer. To store one, use ``std::function``. Rule: `Core Guidelines T.40 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-fo>`__.

See `Function Pointers`_ under Further Reading.

``std::bind``
^^^^^^^^^^^^^

``std::bind`` is a standard function that makes a new callable from an existing one, with some arguments fixed. In ``<functional>``.

.. code-block:: cpp

   double charge_time_h(double missing_pct, double rate_pct_per_h) {
     return missing_pct / rate_pct_per_h;
   }
   using namespace std::placeholders;  // _1, _2, ...
   auto at_fast_dock = std::bind(charge_time_h, _1, 40.0);  // (x, 40.0)
   auto to_half = std::bind(charge_time_h, 50.0, _1);       // (50.0, x)
   auto swapped = std::bind(charge_time_h, _2, _1);         // (y, x)
   at_fast_dock(60.0);   // 1.5
   to_half(25.0);        // 2
   swapped(20.0, 60.0);  // 3

- ``_1`` is "the first argument of the new call", ``_2`` the second. A plain value is fixed. Each comment shows the arguments ``charge_time_h`` receives.

Reading ROS 2 Code
~~~~~~~~~~~~~~~~~~

.. code-block:: cpp

   // ros2/examples, line 34 of
   // rclcpp/topics/minimal_subscriber/member_function.cpp
   subscription_ = this->create_subscription<std_msgs::msg::String>(
     "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));

- ``create_subscription`` wants a callback with one parameter, the message. ROS 2 calls it each time a message arrives.
- ``std::bind`` builds that callback: ``_1`` is the message. ``this`` and ``&MinimalSubscriber::topic_callback`` name a member function of an object, which is Lecture 8.
- The same repository has ``lambda.cpp``, which writes the callback as a lambda capturing ``[this]`` instead.

.. admonition:: Best Practice
   :class: tip

   Write a lambda. Learn ``std::bind`` to **read** it: older code and many ROS 2 examples use it.

See `bind_front and Lambdas`_ under Further Reading.

Summary
-------

**Grouping Values**

- A ``struct`` groups members. Initialize it with braces, by position or by name in declaration order. Give members defaults.
- The compiler pads between members for alignment, and at the end so that arrays work. Largest members first wastes the fewest bytes.
- ``std::pair`` has ``first`` and ``second``; ``std::tuple`` is read by position with ``std::get<0>``.

**Multiple and Optional Results**

- Return several values as a ``struct``; unpack with ``auto [a, b]``, or ``auto&`` to change the original.
- Return ``std::optional`` when the answer may be missing. ``*`` on an empty one is undefined behavior; ``value()`` throws.

**Function Templates**

- One template, one function per set of types used. Deduction needs one consistent ``T`` and ignores the return type. The template goes in the header.
- A concept states what ``T`` must be, and rejects calls that would compile with a wrong result. Form 3 by default; form 1 to share one type; form 2 to join tests.

**Lambdas**

- ``[captures](parameters) { body }`` makes an object of an unnamed ``struct``. Captures are its members.
- By value copies at creation; by reference reads at each call. A lambda that outlives its scope captures by value.

**Storing and Adapting Callables**

- Take a callable you call right away as ``auto``. ``std::function`` holds any callable with one signature, to store it, at a cost.
- Prefer a lambda to ``std::bind``; learn ``std::bind`` to read ROS 2 code.

Further Reading
---------------

The sections below come from the appendix of the slides. They are **not presented** in the lecture. Read them on your own.

``struct`` or ``class``
^^^^^^^^^^^^^^^^^^^^^^^

- C++ has a second keyword, ``class``. The two make the same kind of type. They differ only in default access, which matters once a type has private members (Lecture 8).
- This lecture uses ``struct`` for plain data: members that can each take any value, independently of the others.
- When the members have to agree with each other, for example a battery level that must stay between 0 and 100, you want a ``class`` that checks every change. Lecture 8 covers classes.

.. admonition:: Best Practice
   :class: tip

   Use ``class`` if the class has an invariant; use ``struct`` if the data members can vary independently. Rule: `Core Guidelines C.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-struct>`__.

``offsetof``
^^^^^^^^^^^^

``offsetof`` is a macro from ``<cstddef>``. ``offsetof(Type, member)`` is the number of bytes from the start of the object to that member.

.. code-block:: cpp

   std::cout << offsetof(RobotStatus, id) << ' '
             << offsetof(RobotStatus, battery_pct) << ' '
             << offsetof(RobotStatus, position) << ' '
             << offsetof(RobotStatus, busy) << '\n';  // 0 8 16 32

- A macro, not a function: a function cannot take a type and a member name as its arguments.
- ``id`` is bytes 0 to 3, and ``battery_pct`` starts at byte 8. So bytes 4 to 7 are padding: 4 bytes.

.. note::

   C++20, **[support.types.layout]**, section 17.2.4, paragraph 1: *Use of the offsetof macro with a type other than a standard-layout class is conditionally-supported*. A plain ``struct`` such as ``RobotStatus`` is standard-layout.

``alignof``
^^^^^^^^^^^

``alignof`` is an operator that gives a type's alignment in bytes: every object of that type starts at an address that is a multiple of it. C++11.

.. code-block:: cpp

   std::cout << alignof(bool) << ' ' << alignof(int) << ' '
             << alignof(double) << ' ' << alignof(Position) << ' '
             << alignof(RobotStatus) << '\n';  // 1 4 8 8 8
   std::cout << sizeof(RobotStatus) << ' '
             << sizeof(RobotStatus[2]) << '\n';  // 40 80
   struct IdFlag { int id; bool busy; };
   std::cout << sizeof(IdFlag) << ' ' << alignof(IdFlag) << '\n';  // 8 4

- Here a ``struct`` takes the largest alignment of its members: 8 for ``RobotStatus``, from its ``double``\ s, but 4 for ``IdFlag``, from its ``int``. ``IdFlag`` holds 5 bytes of data and rounds up to 8, a multiple of 4.
- ``busy`` is byte 32, so the data is bytes 0 to 32: 33 bytes. The next multiple of 8 is 40, so the second ``RobotStatus`` of an array starts at byte 40.

.. note::

   C++20, **[expr.sizeof]**, section 7.6.2.4, paragraph 2: for a class, ``sizeof`` counts *any padding required for placing objects of that type in an array*.

Without End Padding
^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   struct StatusReport {
     RobotStatus status;  // bytes 0 to 39
     int sequence;        // bytes 40 to 43
   };
   sizeof(StatusReport);  // 48

- Suppose ``RobotStatus`` had no end padding: 33 bytes, bytes 0 to 32. Two separate cases follow.

1. **An ``int`` after it.** The compiler chooses where ``sequence`` goes. It adds bytes 33 to 35 as padding and puts ``sequence`` at byte 36, a multiple of 4. Nothing breaks.
2. **A second ``RobotStatus`` in an array.** The compiler cannot choose: elements sit exactly ``sizeof`` bytes apart. The second one starts at byte 33, and its ``battery_pct`` at byte 33 + 8 = 41, not a multiple of 8.

.. note::

   End padding exists for case 2, so it is part of the type. C++20, **[basic.align]**, section 6.7.6, paragraph 1: alignment requirements *place restrictions on the addresses at which an object of that type may be allocated*.

The Lecture 4 Map Loop
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::map<int, std::string> zone_of{
     {1, "dock"}, {2, "aisle 4"}, {3, "aisle 7"}};
   for (const auto& [id, zone] : zone_of) {
     std::cout << "robot " << id << ": " << zone << '\n';
   }

.. code-block:: text

   robot 1: dock
   robot 2: aisle 4
   robot 3: aisle 7

- Each element of a ``std::map<K, V>`` is a ``std::pair<const K, V>``. The binding names its two members.
- ``const auto&`` reads each pair in place, with no copy of the string.
- Lecture 4 asked you to read this form as "a way to avoid ``.first`` and ``.second``". That is what it does.

Overload or Specialize
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   template <typename T>
   T larger_of(T left, T right) { return left > right ? left : right; }

   const char* imu_name{"imu"};
   const char* gps_name{"gps"};
   larger_of(imu_name, gps_name);  // "gps": compares the two addresses

   // an overload for C-strings compares the text
   const char* larger_of(const char* left, const char* right) {
     return std::strcmp(left, right) > 0 ? left : right;
   }
   larger_of(imu_name, gps_name);  // "imu"

- ``T`` is ``const char*``, so ``>`` compares addresses, and ``"imu"`` sat lower.
- A **specialization**, ``template <> const char* larger_of<const char*>(...)``, also works here.

.. note::

   Prefer the overload. Specializations *don't participate in overloading, they don't act as you probably wanted*. Rule: `Core Guidelines T.144 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rt-specialize-function>`__.

decltype and Trailing Return Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``decltype`` is an operator that gives the type of a name or an expression, without evaluating it.

.. code-block:: cpp

   const double limit_pct{40.0};
   decltype(limit_pct) other{20.0};  // const double
   std::vector<double> battery_pct{82.5, 35.0};
   decltype(battery_pct[0]) first{battery_pct[0]};  // double&
   first = 9.0;  // battery_pct[0] is now 9

   template <typename T, typename U>
   auto add_offset(T value, U offset) -> decltype(value + offset) {
     return value + offset;
   }

- ``-> type`` after the parameters is a **trailing return type**. It can name the parameters, which the front of the line cannot.
- ``operator[]`` returns a reference, so its ``decltype`` is ``double&``. Before C++14, this was the only way to write ``add_offset``.

``std::totally_ordered``
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   template <std::totally_ordered T>
   T largest_of(const std::vector<T>& values) {
     T largest{values.front()};
     for (const T& value : values) {
       if (value > largest) { largest = value; }
     }
     return largest;
   }
   std::vector<int> ids{3, 1, 4, 2};
   std::vector<std::string> zones{"dock", "aisle 4", "aisle 7"};
   std::vector<RobotStatus> fleet{{1, 82.5}, {2, 35.0}};
   largest_of(ids);    // 4
   largest_of(zones);  // "dock"
   largest_of(fleet);  // does not compile

- ``int`` and ``std::string`` pass. Strings compare character by character.
- ``RobotStatus`` fails: it has no ``==`` or ``<``, so two robots cannot be compared.

.. note::

   C++20, **[concept.totallyordered]**, section 18.5.4, paragraph 1.1: *Exactly one of bool(a < b), bool(a > b), or bool(a == b) is true.*

Documenting a Template
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   /**
    * @brief Average of a list of values.
    *
    * @tparam T A floating-point type, so the division is not integer division.
    * @param values The values to average.
    * @return Their average, or 0 for an empty list.
    */
   template <std::floating_point T>
   T average_of(const std::vector<T>& values);

- ``@tparam`` documents a template parameter, the way ``@param`` documents a function parameter (Lecture 5).
- Say **why** the requirement is there. The concept already says **what** it is.
- This is the comment in ``fleet/include/stats.hpp``.

See `Three Attributes`_.

Three Attributes
^^^^^^^^^^^^^^^^

.. code-block:: cpp

   [[nodiscard("the result is the clamped value")]]
   double clamp_battery(double pct);

   [[deprecated("use clamp_battery")]]
   double limit_battery(double pct);

   void log_reading([[maybe_unused]] int robot_id, double battery_pct);

.. code-block:: text

   warning: ignoring return value of 'double clamp_battery(double)', declared with
     attribute 'nodiscard': 'the result is the clamped value'
   warning: 'double limit_battery(double)' is deprecated: use clamp_battery

- ``[[nodiscard]]`` is Lecture 5's. Since C++20 it takes a reason, which appears in the warning.
- ``[[deprecated]]`` warns at every call: keep an old name working while callers move to the new one.
- ``[[maybe_unused]]`` silences ``-Wunused-parameter`` for one parameter on purpose.

``std::transform``
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};
   std::vector<double> fraction(battery_pct.size());  // 4 elements, all 0
   std::transform(battery_pct.begin(), battery_pct.end(), fraction.begin(),
                  [](double pct) { return pct / 100.0; });
   // fraction is now {0.825, 0.35, 0.64, 0.18}

- ``std::transform`` calls the lambda on each element and writes the result into the destination, one element at a time.
- It writes over elements that already exist; it never adds any. So ``fraction`` is built with 4 elements first, with ``( )``, not ``{ }`` (Lecture 4).

Projections (C++20)
^^^^^^^^^^^^^^^^^^^

A **projection** is a function that a ``std::ranges`` algorithm calls on each element before it compares. It turns an element into the value to compare.

.. code-block:: cpp

   std::vector<std::string> zones{"charging bay", "dock", "aisle 4"};
   // the projection turns each zone into its length
   std::ranges::sort(zones, {}, [](const std::string& zone) {
     return zone.size();
   });
   // zones is now {"dock", "aisle 4", "charging bay"}: lengths 4, 7, 12

- The purpose: you say **what** to compare, here the length, instead of **how** to compare two elements. Without a projection, the sort needs a lambda with two parameters (see `std::sort with a Lambda`_).
- To compare two zones, the algorithm calls the projection on each one and compares the two results with ``<``: 4 < 7, so ``"dock"`` comes before ``"aisle 4"``.
- The arguments: the whole vector, with no ``begin()`` or ``end()``; then ``{}``, the comparison, where empty braces mean the default, ``<``; then the projection.

Projections with ``RobotStatus``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<RobotStatus> fleet{  // id, battery_pct, position, busy
       {1, 82.5, {0.0, 0.0}, false}, {2, 35.0, {4.0, 1.0}, true},
       {3, 64.0, {2.0, 3.0}, false}, {4, 18.0, {6.0, 2.0}, false}};
   std::ranges::sort(fleet, {}, [](const RobotStatus& robot) {
     return robot.battery_pct;
   });  // ids in order: 4 2 3 1
   auto closest = std::ranges::min_element(
       fleet, {}, [](const RobotStatus& robot) {
         return std::hypot(robot.position.x - 5.0, robot.position.y - 5.0);
       });  // closest->id is 4

- Sort: the projection gives each robot's battery, 82.5, 35, 64 and 18 %. Smallest first gives ids 4, 2, 3, 1.
- ``min_element``: the projection gives each robot's distance to a task at (5, 5). ``std::hypot(dx, dy)`` is the square root of dx² + dy²: robot 4 is 3.16 m away, robot 3 3.61 m, robot 2 4.12 m, robot 1 7.07 m.
- But robot 4 has 18 %. Choosing well needs the battery limit too, which a capture gives the lambda: see `Captures`_.

mutable and Init-capture
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int assigned{0};
   auto assign = [assigned]() { ++assigned; };

.. code-block:: text

   capture_const.cpp:3:34: error: increment of read-only variable 'assigned'

.. code-block:: cpp

   auto next_task_id = [id = 100]() mutable { return ++id; };
   std::cout << next_task_id() << ' ' << next_task_id() << ' '
             << next_task_id() << '\n';  // 101 102 103

   auto copy = next_task_id;  // copies the lambda, with id at 103
   std::cout << copy() << ' ' << next_task_id() << '\n';  // 104 104

- A copy captured by value is read-only inside the body. ``mutable`` lets the body change it.
- ``[id = 100]`` is an **init-capture**: it makes a new variable that only the lambda has, here a task counter.
- The counter lives **inside the lambda object**. Copy the lambda and the copy counts on its own.

The Return Type of a Lambda
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto speed_for = [](double battery_pct) {
     if (battery_pct < 20.0) { return 0; }
     return 0.01 * battery_pct;
   };

.. code-block:: text

   lambda_return.cpp:4:17: error: inconsistent types 'int' and 'double' deduced
     for lambda return type

.. code-block:: cpp

   auto speed_for = [](double battery_pct) -> double {
     if (battery_pct < 20.0) { return 0; }   // 0 converts to 0.0
     return 0.01 * battery_pct;              // m/s
   };
   speed_for(15.0);  // 0
   speed_for(80.0);  // 0.8

- Every ``return`` must give the same type, or the compiler cannot choose. ``0`` is an ``int``.
- ``-> double`` after the parameters states the return type. Each ``return`` then converts to it.

Template Lambdas (C++20)
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int main() {
     auto larger = [](const auto& left, const auto& right) {
       return left > right ? left : right;
     };
     auto larger_same = []<typename T>(const T& left, const T& right) {
       return left > right ? left : right;
     };
     larger(3, 7.5);       // 7.5
     larger_same(3, 7.5);  // rejected
   }

.. code-block:: text

   template_lambda.cpp:9:14: note:   deduced conflicting types for parameter
     'const T' ('int' and 'double')

- ``<typename T>`` after the ``[]`` gives the lambda a named template parameter.
- Using ``T`` twice forces both arguments to one type, with the same deduction rule as ``clamp_value``. Two ``auto``\ s cannot say that.

Function Pointers
^^^^^^^^^^^^^^^^^

A **function pointer** is a pointer that holds the address of a function. Calling through it calls that function.

.. code-block:: cpp

   return_type (*name)(parameter_types)

.. code-block:: cpp

   double to_fraction(double pct) {
     return pct / 100.0;
   }
   double to_pct(double fraction) { return fraction * 100.0; }

   double (*convert)(double){to_fraction};
   std::cout << convert(82.5) << '\n';  // 0.825
   convert = to_pct;
   std::cout << convert(0.35) << '\n';  // 35

- ``convert`` points to any function that takes a ``double`` and returns a ``double``. The parentheses around ``*convert`` are required.

Passing a Function
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void convert_all(double* values, int count, double (*convert)(double)) {
     for (int i{0}; i < count; ++i) { values[i] = convert(values[i]); }
   }

   int main() {
     double battery[]{82.5, 35.0};
     double scale{2.0};
     convert_all(battery, 2, [](double pct) { return pct / 100.0; });
     convert_all(battery, 2, [scale](double pct) { return scale * pct; });
   }

.. code-block:: text

   fnptr_capture.cpp:9:27: error: cannot convert 'main()::<lambda(double)>' to
     'double (*)(double)'

- ``convert_all(battery, 2, to_pct)`` works too: a function name turns into a pointer to the function, the way an array name turns into a pointer (Lecture 4).
- A lambda with **no** capture converts. One that captures carries data, and a function pointer cannot.

Function Pointer Syntax
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   double (*convert)(double){&to_fraction};  // & is optional
   (*convert)(82.5);   // 0.825: explicit dereference
   convert(82.5);      // 0.825: the same call

   // NOT a pointer: a function returning double*
   double* make_buffer(double);

   using Conversion = double (*)(double);     // an alias (Lecture 2)
   Conversion table[]{to_fraction, to_pct};
   table[1](0.35);                            // 35

   Conversion from_lambda{[](double value) { return 2 * value; }};
   from_lambda(1.5);                          // 3

- Without the parentheses, ``*`` binds to the return type. GCC's message for assigning ``make_buffer`` to ``convert`` shows both types: ``invalid conversion from 'double* (*)(double)' to 'double (*)(double)'``.
- An alias makes the type readable, and an array of function pointers is a lookup table.

``std::source_location``
^^^^^^^^^^^^^^^^^^^^^^^^

``std::source_location`` is a standard type that records a file, a line and a function name. C++20.

.. code-block:: cpp

   void log_message(
     std::string_view text,
     std::source_location at = std::source_location::current()) {
     std::string_view file{at.file_name()};
     file.remove_prefix(file.rfind('/') + 1);  // the name only
     std::cout << file << ':' << at.line() << ' '
               << at.function_name() << ": " << text << '\n';
   }

.. code-block:: text

   higher_order.cpp:150 void assign_task(int, int): task 17 to robot 3
   higher_order.cpp:154 void end_shift(): shift over

- A default argument is evaluated **at the call** (Lecture 5), so ``current()`` records the caller's line, not ``log_message``'s.

bind_front and Lambdas
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto to_half = std::bind_front(charge_time_h, 50.0);  // C++20
   to_half(25.0);                                         // 2
   auto fast_l = [](double missing_pct) {
     return charge_time_h(missing_pct, 40.0);
   };
   auto swap_l = [](double rate_pct_per_h, double missing_pct) {
     return charge_time_h(missing_pct, rate_pct_per_h);
   };
   fast_l(60.0);        // 1.5
   swap_l(20.0, 60.0);  // 3
   at_fast_dock(60.0, 99.0);   // compiles, returns 1.5: 99.0 is dropped

- ``std::bind_front`` fixes arguments from the left, with no placeholders.
- A lambda does everything ``std::bind`` does, in plain C++. And ``fast_l(60.0, 99.0)`` does not compile, which is what you want.
