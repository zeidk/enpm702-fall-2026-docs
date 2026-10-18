====================================================
Lecture
====================================================

Learning Objectives
-------------------

1. Say who owns an object on the heap, and find a leak with the sanitizers.
2. Move a ``std::vector`` instead of copying it, and say what is left in the source.
3. Name the value category of an expression (lvalue, prvalue, xvalue) and test it with ``decltype``.
4. Use rvalue references and ``std::move``, and write a function that takes a parameter it moves from.
5. Own a heap object with ``std::unique_ptr``, and pass it to and return it from functions.
6. Share an object with ``std::shared_ptr``, and break a reference cycle with ``std::weak_ptr``.
7. Choose between ``std::unique_ptr``, ``std::shared_ptr``, ``std::weak_ptr``, and a plain pointer or reference.

Code for This Lecture
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   project/week7/
   ├── CMakeLists.txt
   ├── playground/
   ├── appendix/
   ├── common/
   └── undefined/

**Run a Slide's Code**

1. Get the code: ``git pull``, then ``702configure``.
2. Build it: ``702build week7_playground``.
3. Run every slide: ``702run week7_playground``. Run only slide 12: ``702run week7_playground 12``.

**Code That Leaks or Breaks**

- It is in ``undefined``, built with AddressSanitizer. It runs only when you ask for its slide by number.
- The appendix frames are in ``week7_appendix``.

.. dropdown:: How to Run the Code
   :icon: terminal
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The ``702`` commands come from ``enpm702-cpp.sh`` in the repository. Its top comment shows how to load them in every new terminal. Then:

   .. code-block:: bash

      enpm702                            # go to the repository, load the 702 commands
      git pull                           # get this week's code
      702rebuild                         # once after you pull: a fresh build/
      702run week7_playground            # the code of every slide, in order
      702run week7_playground 12         # only the code of slide 12
      702run week7_appendix              # the code of every appendix frame
      702run week7_appendix iv           # only appendix frame iv (4 works too)
      702run week7_allocations           # appendix frame xiv: counts make_shared's allocations

   After you edit a file, build again before you run: ``702build week7_playground`` builds one program, ``702build`` builds all of them.

   .. list-table::
      :header-rows: 1
      :widths: 30 70

      * - Command
        - What it does
      * - ``enpm702``
        - Goes to the repository and loads the other ``702`` commands.
      * - ``702configure``
        - Runs CMake to create ``build/``. Run it again after a ``CMakeLists.txt`` changes.
      * - ``702build [program]``
        - Compiles every program, or only the one you name.
      * - ``702run <program> [arguments]``
        - Runs a program from any folder, and passes it the arguments.
      * - ``702exe``
        - Lists the programs that were built.
      * - ``702bin``
        - Goes to ``build/``. The week 7 programs are in ``build/project/week7``.
      * - ``702clean``
        - Deletes ``build/``.
      * - ``702rebuild``
        - Runs ``702clean``, then ``702configure``, then ``702build``.
      * - ``702help``
        - Prints the list of commands.

   **Why 702rebuild after you pull.** CMake never deletes a program whose target was removed. If you built this week's code before, an old program such as ``week7`` stays in ``build/`` and still runs the old code. ``702rebuild`` starts from an empty ``build/``.

   Code that does not compile is in the programs, commented out: uncomment it to get the slide's error.

   A slide whose code leaks or has undefined behavior, such as slide 9, runs only when you ask for it by number: ``702run week7_playground 9``. A full run skips it.

.. note::

   The `Further Reading`_ part, after the summary, is the appendix of the slides. It is not presented. Read it on your own.

The Program We Will Build
-------------------------

The **fleet manager** of Lecture 6, with its robots now on the heap. The structs ``Position`` and ``RobotStatus`` do not change.

- The **fleet** is a list of robots. It creates each robot, and gives the memory back when the robot leaves.
- The **charging queue** holds robots waiting to charge. A queued robot is still in the fleet: it has two owners, and lives until both let go.
- A **dashboard** shows one robot. It must notice when that robot is gone, but it must not keep the robot alive.

.. note::

   Three kinds of ownership: one owner, several owners, and an observer that owns nothing. Each one gets its own smart pointer today.

.. figure:: /_static/images/l7/owner_map.png
   :alt: A UML object diagram in black and white: six boxes joined by lines, with nothing written on the lines. On the left, a box labeled fleet. In the middle, three boxes labeled robot1 : RobotStatus, robot2 : RobotStatus and robot3 : RobotStatus, one above the other. On the right, a box labeled charging_queue and, below it, a box labeled dashboard : Dashboard. Lines with a filled diamond at the fleet end join the fleet to robot1 and to robot2. Lines with an open diamond at the owner end join the fleet to robot3 and the charging_queue to robot3. A line with no diamond runs from the dashboard to robot3 and ends in an open arrowhead at robot3.
   :align: center
   :width: 100%

   Who owns each robot, as a UML object diagram (Lecture 9): each box is one object. **Filled diamond**: the only owner. **Open diamond**: one of several owners. **Arrow, no diamond**: looks, does not own.

Who Owns This Robot
-------------------

An **owner** of a heap object is code that keeps it alive. An object can have one owner or several: the last owner to let go deletes it.

Rule: `Core Guidelines R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr>`__.

A Robot on the Heap
^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   RobotStatus* make_robot(int id) {
     return new RobotStatus{id, 100.0, {0.0, 0.0}, false};
   }

   RobotStatus* robot{make_robot(3)};
   std::cout << robot->id << ' ' << robot->battery_pct << '\n';  // 3 100
   delete robot;  // the caller must remember this
   robot = nullptr;

- ``make_robot`` creates the robot with Lecture 3's ``new``. The caller must ``delete`` it.
- Nothing in the type says so: ``RobotStatus*`` looks the same whether it owns the robot or only points at it.

.. note::

   The Core Guidelines settle it: "A raw pointer (a ``T*``) is non-owning". An owner needs a type that says it owns. Rule: `Core Guidelines R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr>`__.

Three Ways to Get It Wrong
^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Leak**

.. code-block:: cpp

   auto* r{make_robot(3)};
   if (r->busy) {
     return;  // no delete
   }
   delete r;

**2. Double** ``delete``

.. code-block:: cpp

   // same robot in both
   for (auto r : fleet) {
     delete r;
   }
   for (auto r : idle) {
     delete r;  // again
   }

**3. Dangling Read**

.. code-block:: cpp

   for (auto r : fleet) {
     delete r;
   }
   // idle[0]: freed memory
   std::cout << idle[0]->id;

- **Leak**: one path leaves without ``delete``. The memory is never given back.
- **Double** ``delete``: breaks Lecture 3's rule "``delete`` exactly once". Undefined behavior.
- **Dangling read**: reads an object that was already deleted. Undefined behavior.
- The cause is the same in all three: two lists, or two paths, and no one is marked as the owner.

See `Double Delete, Measured`_ and `Dangling Read, Measured`_ under Further Reading.

The Leak, Measured
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   bool needs_charge(int id) {
     RobotStatus* robot{make_robot(id, 64.0)};  // 64.0: battery_pct
     if (robot->battery_pct > 20.0) {
       return false;  // leaves without delete
     }
     delete robot;
     return true;
   }

.. code-block:: text

   ==1714457==ERROR: LeakSanitizer: detected memory leaks

   Direct leak of 40 byte(s) in 1 object(s) allocated from:
       #0 0x77aa348fe548 in operator new(unsigned long)
       #1 0x5c7541766020 in make_robot .../week7/undefined/undefined.cpp:25
       #2 0x5c7541766277 in undefined::early_return_leak::needs_charge(int) ...
   SUMMARY: AddressSanitizer: 40 byte(s) leaked in 1 allocation(s).

- ``702run week7_playground 9``. At exit, it names the line that called ``new``.
- 40 bytes is one ``RobotStatus``, the size measured in Lecture 6.

.. note::

   LeakSanitizer comes with Lecture 3's ``-fsanitize=address``: AddressSanitizer "integrates LeakSanitizer and enables it by default on supported platforms". See `LeakSanitizer <https://clang.llvm.org/docs/LeakSanitizer.html>`__.

RAII for One Object
^^^^^^^^^^^^^^^^^^^

**Lecture 4, Again**

- A ``std::vector`` gives its memory back by itself when it goes out of scope. That is RAII: the object that holds the memory frees it in its destructor.
- No path can forget: leaving a scope always destroys its objects, after a ``return``, at the end of a loop, or by an exception that is caught.

**The Same for One Object**

- A **smart pointer** is an object that owns one heap object and deletes it when the smart pointer is destroyed.
- Its type says it owns, which a ``RobotStatus*`` cannot.
- Today: ``std::unique_ptr`` for one owner, ``std::shared_ptr`` for several, ``std::weak_ptr`` for an observer.

.. note::

   "Manage resources automatically using resource handles and RAII". Rule: `Core Guidelines R.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-raii>`__.

Move Semantics
--------------

A **copy** makes a second object with its own memory: a new block, every element copied. A **move** hands what one object owns to another: a few pointers change, and no element is copied.

See `cppreference: std::move <https://en.cppreference.com/w/cpp/utility/move>`__.

Handing a Route to a Robot
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> make_route(int n);  // n points, 1 m apart
   std::vector<Position> route{make_route(1000)};  // 1000 waypoints
   const Position* where{route.data()};

   std::vector<Position> copied{route};             // a copy
   std::vector<Position> moved{std::move(route)};   // a move

.. code-block:: text

   copy: copied.data() == route.data(): false, route.size(): 1000
   move: moved.data() == where: true, route.size(): 0
   bytes the copy allocated: 16000

- The copy allocates a new block, 1000 × 16 bytes = 16000 bytes, and copies every ``Position``. ``route`` is unchanged.
- The move allocates nothing. ``moved`` holds the block ``route`` had, at the same address, and ``route`` is left empty.

.. dropdown:: The Definition of ``make_route``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      std::vector<Position> make_route(int n) {
        std::vector<Position> route;
        for (int i{0}; i < n; ++i) {
          route.push_back({static_cast<double>(i), 0.0});
        }
        return route;
      }

   - It builds a route of ``n`` waypoints, one meter apart along an aisle: waypoint ``i`` is at x = ``i`` meters and y = 0 (Lecture 6's ``Position``).
   - ``702run week7_appendix iv`` prints the three waypoints of ``make_route(3)``: (0, 0) (1, 0) (2, 0).
   - It returns the local ``route`` by value: no copy is made (`Return by Value, Again`_).

Inside a Copy
^^^^^^^^^^^^^

.. figure:: /_static/images/l7/vector_copy.png
   :alt: Two blue Stack boxes side by side, named route and copied, each with three fields, begin, end and capacity. Below each one is its own red Heap block, and three blue arrows drop from each box's fields to its own block. Under route, the block is labeled 1024 Position, 16384 bytes, and its last part is shaded gray and marked 24 free: begin points to the first cell, end to the start of the gray part, and capacity to the end of the block. Under copied, the block is labeled 1000 Position, 16000 bytes, with no gray part: begin points to the first cell, and end and capacity both to the end of the last cell. No arrow joins the two sides.
   :align: center
   :width: 100%

   A ``std::vector`` and its copy: each one owns its own block. Gray: unused slots of ``route``'s capacity.

- After ``std::vector<Position> copied{route}``, each vector holds three pointers into its own block (`Handing a Route to a Robot`_: the two ``data()`` differ).
- ``push_back`` grew ``route`` to capacity 1024 (measured): 1024 × 16 = 16384 bytes, 24 unused (gray).
- The copy allocates 1000 × 16 = 16000 bytes. Total: 16384 + 16000 = 32384 bytes.
- Each vector frees its own block when it goes out of scope.

Inside a Move
^^^^^^^^^^^^^

.. figure:: /_static/images/l7/vector_move.png
   :alt: Two panels separated by a thin line, tagged 1 and 2. Panel 1: a blue Stack box named route with three fields, begin, end and capacity. Three blue arrows drop from the fields to a red Heap block below, labeled 1024 Position, 16384 bytes, its last part shaded gray and marked 24 free: begin to its first cell, end to the start of the gray part, and capacity to the end of the block. Panel 2: the same Stack box named route, its three fields now reading nullptr, with no arrows. Below it a second Stack box named moved, with the same three fields, and three blue arrows from them to a red Heap block labeled 1024 Position, 16384 bytes, with the same gray part, pointing the same way as in panel 1.
   :align: center
   :width: 100%

   A ``std::vector`` before and after a move. **1**: ``route`` owns the block. **2**: after the move, ``moved`` owns the block and ``route``'s three pointers are null.

- **1**: ``route`` owns the block through its three pointers (Lecture 4). Gray: 24 unused slots.
- **2**: after ``std::vector<Position> moved{std::move(route)}``, ``moved`` holds the same three pointers and ``route``'s are null (libstdc++, measured).
- Only 24 bytes change hands: one ``std::vector`` object, whatever it holds.

The Moved-from Object
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> route{make_route(1000)};
   std::vector<Position> robot_route{std::move(route)};
   std::cout << route.empty() << '\n';  // 1 (true) with libstdc++
   route = make_route(5);                // assign before you use it again
   std::cout << route.size() << ' ' << robot_route.size();  // 5 1000

- After a move, the source still exists. It is destroyed at the end of its scope, as usual.
- What it holds is not promised by the standard. libstdc++ leaves a moved-from ``std::vector`` empty; another library may not.
- Safe: destroy it, or assign it a new value. Then use it as before.

.. note::

   C++20 **[lib.types.movedfrom]** (16.5.5.16): "Unless otherwise specified, such moved-from objects shall be placed in a valid but unspecified state."

See `The Moved-from std::string`_, `Move Assignment`_ and `std::exchange`_ under Further Reading.

Value Categories
^^^^^^^^^^^^^^^^

.. code-block:: text

            expression
           /          \
       glvalue       rvalue
       /     \      /     \
   lvalue    xvalue      prvalue

- Every expression has a **type** and a **value category**.
- The value category says whether the expression names an object, and whether that object's resources may be taken.
- The three categories: **lvalue**, **xvalue**, **prvalue**. A **glvalue** is an lvalue or an xvalue; an **rvalue** is an xvalue or a prvalue.
- Names (paragraph 3 of **[basic.lval]**): **l**, **r** once meant the left and right side of an assignment; **gl** "generalized", **pr** "pure", **x** "eXpiring".

.. note::

   The tree is Figure 1 of C++20 **[basic.lval]** (7.2.1). Paragraph 2: "Every expression belongs to exactly one of the fundamental classifications in this taxonomy: lvalue, xvalue, or prvalue."

The Five Definitions
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Term
     - C++20 [basic.lval] paragraph 1
     - In plain words
   * - glvalue
     - "an expression whose evaluation determines the identity of an object, bit-field, or function"
     - It names something with an address.
   * - prvalue
     - "an expression whose evaluation initializes an object or a bit-field, or computes the value of an operand of an operator, [...]"
     - A value that will fill an object, not an object yet.
   * - xvalue
     - "a glvalue that denotes an object or bit-field whose resources can be reused (usually because it is near the end of its lifetime)"
     - An object you may take from.
   * - lvalue
     - "a glvalue that is not an xvalue"
     - An object that stays: do not take from it.
   * - rvalue
     - "a prvalue or an xvalue"
     - Something you may move from.

.. note::

   Paragraph 3: "Despite their names, these terms classify expressions, not values." The same variable can appear in an lvalue and in an xvalue.

lvalues
^^^^^^^

An **lvalue** names an object that lives on after the expression. Test: you can take its address with ``&``.

.. code-block:: cpp

   RobotStatus make_robot(int id);  // by value from here on
   RobotStatus& first_robot(std::vector<RobotStatus>& fleet);
   std::vector<Position> route{make_route(3)};
   std::vector<RobotStatus> fleet{make_robot(1), make_robot(2)};
   RobotStatus* robot_ptr{&fleet[1]};

- ``route``: a named variable.
- ``*robot_ptr``: what a pointer points at.
- ``fleet[0]``: an element. ``&fleet[0]`` compiles.
- ``first_robot(fleet)``: a call that returns ``RobotStatus&``.
- ``"dock"``: a string literal, an array with an address.

``702run week7_playground 18`` prints ``lvalue`` for all five.

prvalues
^^^^^^^^

.. code-block:: cpp

   int a{2};
   int b{3};

   42                // a literal (not a string literal)
   a + b             // a built-in arithmetic result
   make_route(3)     // a call that returns by value
   RobotStatus{}     // a temporary of a class type
   [] { return 1; }  // a lambda expression

.. code-block:: text

   error: lvalue required as unary '&' operand

- No object exists yet: a prvalue is the value that will initialize one. All five print ``prvalue``.
- So you cannot take its address: ``&(a + b)`` gives the error above.

xvalues
^^^^^^^

.. code-block:: cpp

   struct Robot {
     RobotStatus status;
     std::vector<Position> route;
   };
   std::vector<Position> route{make_route(3)};
   Robot robot{make_robot(1), make_route(3)};

   std::move(route)                              // a call that returns T&&
   static_cast<std::vector<Position>&&>(route)   // a cast to T&&
   std::move(robot).route                        // a member of an xvalue

- An object you have marked as "you may take from this". All three print ``xvalue``.
- Naming an xvalue moves nothing: afterwards ``route.size()`` is still 3.

.. note::

   Three of the five cases in the note to **[basic.lval]** paragraph 4: a call "whose return type is an rvalue reference to object type", "a cast to an rvalue reference to object type", and a member access "in which the object expression is an xvalue".

Temporary Materialization
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   RobotStatus make_robot(int id);   // returns by value

   make_robot(3)        // prvalue: no object yet
   make_robot(3).id     // xvalue: .id needs an object, so one is made
   int id{make_robot(3).id};  // the robot is created, read, and destroyed

- To read a member, there must be an object. The compiler creates a **temporary** from the prvalue, and the expression becomes an xvalue that names it.
- The temporary is destroyed at the end of the full expression, after ``id`` has its value: 3.

.. note::

   C++20 **[conv.rval]** (7.3.4): "A prvalue of type T can be converted to an xvalue of type T." The standard's own example: ``int k = X().n``, "X() prvalue is converted to xvalue".

The ``decltype`` Test
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> route{make_route(3)};
   static_assert(std::is_same_v<decltype((route)),
                                std::vector<Position>&>);   // lvalue
   static_assert(std::is_same_v<decltype((std::move(route))),
                                std::vector<Position>&&>);  // xvalue
   static_assert(std::is_same_v<decltype((make_route(3))),
                                std::vector<Position>>);    // prvalue

- ``decltype((e))`` gives ``T&`` for an lvalue, ``T&&`` for an xvalue, and ``T`` for a prvalue. The three ``static_assert``\ s compile.
- The second pair of parentheses matters: ``decltype(route)`` gives the declared type of the variable, ``std::vector<Position>``, not its category.
- The playground prints each category with this test.

.. note::

   C++20 **[dcl.type.decltype]** (9.2.8.4) paragraph 1: "if E is an xvalue, decltype(E) is T&&", "if E is an lvalue, decltype(E) is T&", "otherwise, decltype(E) is the type of E".

Exercise 1: Value Categories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   struct Robot {
     RobotStatus status;
     std::vector<Position> route;
   };
   Robot& lookup(
       std::vector<Robot>& robots,
       int i);

   std::vector<Robot> robots{...};
   Robot* p{&robots[0]};
   int n{4};

.. code-block:: cpp

   robots                      // 1
   robots[1].route             // 2
   p->status.id                // 3
   n * 2                       // 4
   lookup(robots, 1)           // 5
   make_route(n)               // 6
   std::move(robots[0])        // 7
   std::move(robots[0]).route  // 8
   make_robot(n).battery_pct   // 9
   ++n                         // 10

- Write lvalue, xvalue or prvalue for each line. Then check: ``702run week7_playground 23``.

rvalue References
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> route{make_route(1000)};
   std::vector<Position>&& temp_ref{make_route(10)};  // OK: an rvalue
   const std::vector<Position>& any_ref{route};       // binds to both
   std::vector<Position>&& lvalue_ref{route};         // does not compile

.. code-block:: text

   error: cannot bind rvalue reference of type 'std::vector<Position>&&' to lvalue
   of type 'std::vector<Position>'

- ``T&&`` is an **rvalue reference**. It binds only to rvalues: prvalues and xvalues.
- ``const T&`` binds to both (Lecture 5), but through it you cannot change the object, so you cannot take from it.
- A ``T&&`` says: whatever this refers to may be taken.

Named rvalue References
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position>&& r{make_route(10)};
   decltype(r)     // std::vector<Position>&&: the type of r
   decltype((r))   // std::vector<Position>&: the expression r is an lvalue

- The **type** of ``r`` is an rvalue reference. The **expression** ``r`` is an lvalue: it has a name, and you can use it again on the next line.
- So a function that receives a ``T&&`` parameter cannot move from it just by using its name. It has to mark it again with ``std::move``.

.. note::

   The note to **[basic.lval]** paragraph 4: "named rvalue references are treated as lvalues and unnamed rvalue references to objects are treated as xvalues".

Overloads for Copy and Move
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void assign_route(const std::vector<Position>& route) {  // 1
     robot_route = route;             // copy
   }
   void assign_route(std::vector<Position>&& route) {       // 2
     robot_route = std::move(route);  // move
   }

   std::vector<Position> route{make_route(1000)};
   std::vector<Position>&& r{make_route(10)};
   assign_route(route);             // lvalue: 1, a copy
   assign_route(make_route(5));     // prvalue: 2, a move
   assign_route(r);                 // named T&&, an lvalue: 1, a copy
   assign_route(std::move(route));  // xvalue: 2, a move

- The compiler picks the overload from the argument's value category: an lvalue gets ``const&``, an rvalue gets ``&&``.
- ``std::vector`` itself has both: a copy constructor and a move constructor. That is how the compiler chose between the copy and the move in `Handing a Route to a Robot`_.

``std::move``, a Cast
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> route{make_route(1000)};
   std::move(route);                      // warns: result unused
   std::cout << route.size() << '\n';     // 1000: nothing moved

.. code-block:: text

   warning: ignoring return value of '... std::move(_Tp&&)
   [with _Tp = vector<Position>&; ...]', declared with attribute 'nodiscard'
   [-Wunused-result]

- ``std::move(route)`` is a cast to ``std::vector<Position>&&``. Its result is an xvalue: it marks ``route`` as "may be taken".
- The move happens later, if a move constructor or a ``&&`` overload takes the result. Here nothing does.

.. note::

   Write ``std::move`` only where the object is handed on, and do not use the source again until you assign it. Rule: `Core Guidelines ES.56 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-move>`__.

See `The Definition of std::move`_ under Further Reading.

``std::move`` on a ``const`` Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   const std::vector<Position> route{make_route(1000)};
   std::vector<Position> robot_route{std::move(route)};  // compiles

.. code-block:: text

   robot_route.data() == route.data(): false, route.size(): 1000

- No warning, and no move: a new block, and ``route`` still holds 1000 waypoints.
- ``std::move(route)`` has type ``const std::vector<Position>&&``. It cannot bind to the move constructor's ``std::vector<Position>&&``, which would change ``route``.
- It does bind to the copy constructor's ``const std::vector<Position>&``, so the compiler copies.

.. note::

   A ``const`` object cannot be moved from. Declare an object ``const`` only if you will not hand it on.

A Parameter the Function Moves From
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void set_route(Robot& robot, std::vector<Position>&& route) {
     robot.route = std::move(route);  // route has a name: move it again
   }

   set_route(robot, route);             // error: route is an lvalue
   set_route(robot, std::move(route));  // the caller says: take it
   set_route(robot, make_route(5));     // a prvalue: no std::move

.. code-block:: text

   robot.route.data() == where: true, route.size(): 0

- ``&&`` makes the caller write ``std::move`` for a named object, so a copy never happens by accident.
- Inside, ``route`` is a named rvalue reference: an lvalue. Without the second ``std::move``, the assignment would copy.

.. note::

   "For 'will-move-from' parameters, pass by ``X&&`` and ``std::move`` the parameter". Rule: `Core Guidelines F.18 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-consume>`__.

Return by Value, Again
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> plan_route(int n) {
     std::vector<Position> route{make_route(n)};
     return route;               // elided or moved, never copied
     // return std::move(route); // warns, and blocks the elision
   }
   std::vector<Position> path{plan_route(1000)};

.. code-block:: text

     inside plan_route, route.data(): 0x529000000200
     in the caller, path.data(): 0x529000000200
   warning: moving a local object in a return statement prevents copy elision
   [-Wpessimizing-move]

- Lecture 5: a local returned by value is constructed in place, or moved if it cannot be. Same address, measured.
- ``std::move`` on the return turns the local into an xvalue, and the compiler can no longer build it in place.

.. note::

   "Don't ``return std::move(local)``". Rule: `Core Guidelines F.48 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-move-local>`__.

``std::unique_ptr``
-------------------

A ``std::unique_ptr`` is the only owner of one object on the heap. It cannot be copied, only moved, and when it is destroyed it deletes the object.

See `cppreference: std::unique_ptr <https://en.cppreference.com/w/cpp/memory/unique_ptr>`__. Rule: `Core Guidelines R.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-owner>`__.

.. _l7-unique-creating-one:

Creating One
^^^^^^^^^^^^

.. code-block:: cpp

   #include <memory>

   std::unique_ptr<RobotStatus> robot{
       std::make_unique<RobotStatus>(3, 64.0, Position{2.0, 3.0}, false)};
   std::cout << robot->id << ' ' << (*robot).battery_pct << '\n';  // 3 64

   auto other{std::make_unique<RobotStatus>()};  // members take defaults
   std::cout << other->battery_pct << '\n';      // 100

- ``std::make_unique<T>(args)`` creates the object on the heap and returns the ``std::unique_ptr`` that owns it.
- The arguments go to the object, as with Lecture 6's ``emplace_back(3, 64.0, ...)``.
- ``->`` and ``*`` work as they do on a ``RobotStatus*``.
- No ``new``, and no ``delete``: ``robot`` deletes its robot when it goes out of scope.

.. note::

   "Use ``make_unique()`` to make ``unique_ptr``\ s". Rule: `Core Guidelines R.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_unique>`__.

See `A unique_ptr with Its Own Deleter`_ under Further Reading.

In Memory
^^^^^^^^^

.. figure:: /_static/images/l7/unique_ptr_memory.png
   :alt: On the left, a blue Stack box named robot with one field, pointer, labeled 8 bytes. A blue arrow runs from it to a red Heap box on the right named RobotStatus, with four rows: id 3, battery_pct 64.0, position {2.0, 3.0}, and busy false, labeled 40 bytes.
   :align: center
   :width: 100%

   A ``std::unique_ptr`` on the stack and the ``RobotStatus`` it owns on the heap.

.. code-block:: text

   sizeof(robot): 8, sizeof(RobotStatus*): 8, sizeof(RobotStatus): 40

- The ``std::unique_ptr`` is one pointer on the stack, the same 8 bytes as a ``RobotStatus*``. The robot itself is on the heap.
- Owning costs no memory. The difference is in the type: only a ``std::unique_ptr`` deletes, and only one can point at the robot as its owner.

The Leak, Fixed
^^^^^^^^^^^^^^^

**From** `The Leak, Measured`_

.. code-block:: cpp

   bool needs_charge(int id) {
     RobotStatus* robot{
         make_robot(id, 64.0)};
     if (robot->battery_pct > 20.0) {
       return false;  // leaks
     }
     delete robot;
     return true;
   }

**With** ``std::unique_ptr``

.. code-block:: cpp

   bool needs_charge(int id) {
     auto robot{std::make_unique<RobotStatus>(
         id, 64.0, Position{}, false)};
     if (robot->battery_pct > 20.0) {
       return false;  // deleted here
     }
     return true;     // and here
   }

- ``702run week7_playground 34`` prints ``needs_charge(3): false`` and no LeakSanitizer report.
- Every path out of the function destroys ``robot``, and ``robot``'s destructor deletes the ``RobotStatus``. There is no ``delete`` to forget.

One Owner Only
^^^^^^^^^^^^^^

.. code-block:: cpp

   auto robot{std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false)};
   std::unique_ptr<RobotStatus> copy{robot};  // does not compile

.. code-block:: text

   error: use of deleted function 'std::unique_ptr<_Tp, _Dp>::unique_ptr(const
   std::unique_ptr<_Tp, _Dp>&) [with _Tp = RobotStatus;
   _Dp = std::default_delete<RobotStatus>]'

- The copy constructor is **deleted**: declared, so that a copy is an error, and never defined.
- Two owners of one robot would both delete it: the double ``delete`` of `Three Ways to Get It Wrong`_. The type rules it out at compile time.
- ``_Dp = std::default_delete<RobotStatus>`` is the **deleter**: what a ``std::unique_ptr`` calls to give the memory back. By default, ``delete``.

See `std::auto_ptr`_ under Further Reading.

Moving Ownership
^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto robot{std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false)};
   RobotStatus* where{robot.get()};
   std::unique_ptr<RobotStatus> other{std::move(robot)};

.. code-block:: text

   robot == nullptr: true, other.get() == where: true, other->id: 3

- The move constructor of `Move Semantics`_ at work: ``other`` takes the pointer, and ``robot`` is left empty. The robot never moved in memory.
- There is still exactly one owner, at every moment.
- Unlike a moved-from ``std::vector``, a moved-from ``std::unique_ptr`` is guaranteed to be empty.

.. note::

   C++20 **[unique.ptr.single.ctor]** (20.11.1.2.1) paragraph 20, for ``unique_ptr(unique_ptr&& u)``: "Postconditions: get() yields the value u.get() yielded before the construction. u.get() == nullptr."

See `Testing for Empty`_ under Further Reading.

A Fleet of ``unique_ptr``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::unique_ptr<RobotStatus>> fleet;
   fleet.push_back(std::make_unique<RobotStatus>(
       1, 82.5, Position{0.0, 0.0}, false));
   auto robot{std::make_unique<RobotStatus>(
       2, 35.0, Position{4.0, 1.0}, true)};
   fleet.push_back(std::move(robot));  // robot is now empty
   // fleet.push_back(robot);          // does not compile: a copy

   for (const auto& r : fleet) {       // a copy would not compile
     std::cout << "robot " << r->id << ": " << r->battery_pct << " %\n";
   }

- The fleet: the vector owns the pointers, and each pointer owns its robot. When ``fleet`` is destroyed, every robot is deleted.
- A temporary from ``std::make_unique`` moves in by itself. A named ``robot`` needs ``std::move``.
- Copying the whole vector does not compile either: it would copy every ``std::unique_ptr``.

See `unique_ptr to an Array`_ under Further Reading.

``get`` and ``reset``
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_status(const RobotStatus* robot);  // only looks

   auto robot{std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false)};
   print_status(robot.get());  // robot still owns it
   robot.reset();              // deletes it now: robot == nullptr
   robot = std::make_unique<RobotStatus>(
       4, 18.0, Position{6.0, 2.0}, false);

- ``get()`` returns the plain pointer. It does not give up ownership: the code that receives it only looks, and must not ``delete`` it.
- ``reset()`` deletes the robot now, without waiting for the end of the scope. ``reset(p)`` takes ``p`` instead.
- Assigning a new ``std::unique_ptr`` deletes the old robot first, as ``reset`` would.

.. note::

   C++20 **[unique.ptr.single.modifiers]** (20.11.1.2.5) paragraph 4, ``reset(p)``: "Assigns p to the stored pointer, and then if and only if the old value of the stored pointer, old_p, was not equal to nullptr, calls get_deleter()(old_p)."

See `swap`_ under Further Reading.

``release``
^^^^^^^^^^^

.. code-block:: cpp

   auto robot{std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false)};
   RobotStatus* raw{robot.release()};  // gives up ownership
   // robot == nullptr: true, raw->id: 3
   delete raw;  // you are the owner now: leave this out and it leaks

- ``release()`` hands the robot back as a plain pointer and forgets it. Nothing owns the robot except your code.
- You are back where `A Robot on the Heap`_ started: a ``RobotStatus*`` that must be deleted exactly once.
- Use it only to hand the robot to code that takes ownership of a plain pointer. Otherwise, move the ``std::unique_ptr``.

.. note::

   C++20 **[unique.ptr.single.modifiers]** paragraphs 1 and 2: "Postconditions: get() == nullptr." "Returns: The value get() had at the start of the call to release."

.. _l7-unique-borrow:

Passing: Borrow
^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_status(const RobotStatus& robot);  // only reads the robot
   void charge(RobotStatus* robot) {              // may get nullptr
     if (robot != nullptr) { robot->battery_pct = 100.0; }
   }

   auto robot{std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false)};
   print_status(*robot);   // 64 %
   charge(robot.get());
   print_status(*robot);   // 100 %: the caller still owns it

- A function that only uses the robot takes the robot, by reference or plain pointer, not the smart pointer. Lecture 5's rules for parameters apply.
- It then works for any robot: on the heap, on the stack, or in a vector.

.. note::

   "Take smart pointers as parameters only to explicitly express lifetime semantics". Rule: `Core Guidelines R.30 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrparam>`__.

Passing: Sink
^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::unique_ptr<RobotStatus>> retired;

   void retire(std::unique_ptr<RobotStatus> robot) {  // takes ownership
     retired.push_back(std::move(robot));
   }

   retire(robot);             // does not compile: a copy
   retire(std::move(robot));  // robot == nullptr, retired.size() == 1

- By value: the parameter is a new owner, so the caller must hand the robot over with ``std::move``. The call says that ownership moves.
- F.18, from `A Parameter the Function Moves From`_, asks for ``&&`` here. Its own exception: a move-only type that is cheap to move, such as ``std::unique_ptr``, can be passed by value.

.. note::

   "Take a ``unique_ptr<widget>`` parameter to express that a function assumes ownership of a ``widget``". Rule: `Core Guidelines R.32 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-uniqueptrparam>`__.

Passing: Reseat
^^^^^^^^^^^^^^^

.. code-block:: cpp

   void replace_robot(std::unique_ptr<RobotStatus>& robot, int new_id) {
     robot = std::make_unique<RobotStatus>(
         new_id, 100.0, Position{0.0, 0.0}, false);
   }  // the assignment deleted the old robot

   auto robot{std::make_unique<RobotStatus>(
       3, 4.0, Position{2.0, 3.0}, false)};
   replace_robot(robot, 7);  // robot->id: 7, robot->battery_pct: 100

- By reference to the ``std::unique_ptr``: the function may make the caller's pointer own a different robot. To **reseat** means exactly that.
- The caller keeps ownership. Only what it owns changes.

.. note::

   "Take a ``unique_ptr<widget>&`` parameter to express that a function reseats the ``widget``". Rule: `Core Guidelines R.33 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-reseat>`__.

.. _l7-unique-returning:

Returning
^^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<RobotStatus> make_robot(int id) {
     auto robot{std::make_unique<RobotStatus>(
         id, 100.0, Position{0.0, 0.0}, false)};
     robot->busy = false;
     return robot;  // no std::move: Lecture 5's implicit move
   }

   std::unique_ptr<RobotStatus> robot{make_robot(5)};  // robot->id: 5

- A factory returns the ``std::unique_ptr`` by value. The caller becomes the owner.
- ``return robot;`` compiles although ``std::unique_ptr`` cannot be copied: a local returned by value is moved, never copied (Lecture 5, and `Return by Value, Again`_).
- Compare `A Robot on the Heap`_: there, a ``RobotStatus*`` came back, and nothing said who must delete it. Here the type says it.

Exercise 2: Lines That Compile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void inspect(const RobotStatus& robot);
   void adopt(std::unique_ptr<RobotStatus> robot);

   auto a{std::make_unique<RobotStatus>(
       1, 50.0, Position{0.0, 0.0}, false)};
   auto b{std::make_unique<RobotStatus>(
       2, 60.0, Position{0.0, 0.0}, false)};

   auto c{a};                                          // 1
   auto d{std::move(a)};                               // 2
   inspect(*d);                                        // 3
   adopt(b);                                           // 4
   adopt(std::move(b));                                // 5
   std::unique_ptr<RobotStatus> e{new RobotStatus{}};  // 6
   RobotStatus* f{d.get()};                            // 7
   std::unique_ptr<RobotStatus> g{f};                  // 8

- For each line: does it compile? If it compiles, is it correct? Then check in ``702run week7_playground 44`` and its comments.

``std::shared_ptr``
-------------------

A ``std::shared_ptr`` is one of several owners of an object on the heap. The owners share a count, and the last one to let go deletes the object.

See `cppreference: std::shared_ptr <https://en.cppreference.com/w/cpp/memory/shared_ptr>`__. Rule: `Core Guidelines R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`__.

A Robot in Two Lists
^^^^^^^^^^^^^^^^^^^^

Robot 3 is down to 14 %. It joins the charging queue, and it stays in the fleet. Three ways to hold it in the queue, all wrong:

1. **A second** ``std::unique_ptr``: does not compile. One owner only (`One Owner Only`_).
2. **A copy of the robot**: now there are two robots. Charging one leaves the other at 14 %.
3. **A** ``RobotStatus*`` **from** ``get()``: the queue does not own it. If the fleet removes robot 3, the queue points at freed memory (`Three Ways to Get It Wrong`_).

.. code-block:: cpp

   std::vector<std::unique_ptr<RobotStatus>> fleet;   // slide 37, 3 robots
   std::vector<RobotStatus*> charging_queue;
   charging_queue.push_back(fleet[2].get());         // looks, does not own
   fleet.erase(fleet.begin() + 2);                   // the queue dangles

The ``fleet`` here is the one from `A Fleet of unique_ptr`_.

.. note::

   Both lists must own robot 3, and it must be deleted when the last of them lets go.

.. _l7-shared-creating-one:

Creating One
^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::shared_ptr<RobotStatus>> fleet;
   std::vector<std::shared_ptr<RobotStatus>> charging_queue;

   auto robot{std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false)};
   fleet.push_back(robot);           // a copy: one more owner
   charging_queue.push_back(robot);  // a copy: one more owner

.. code-block:: text

   robot.use_count(): 3
   fleet[0] == charging_queue[0]: true

- A ``std::shared_ptr`` can be copied. Every copy is one more owner of the same robot, and ``use_count()`` counts them: ``robot``, ``fleet[0]``, ``charging_queue[0]``.
- All three point at one robot: charging it through the queue shows in the fleet.

.. note::

   "Use ``make_shared()`` to make ``shared_ptr``\ s". Rule: `Core Guidelines R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`__.

The Control Block
^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/shared_ptr_memory.png
   :alt: On the left, two blue Stack boxes, named robot and in_queue, one above the other. Each has two rows, object and control, and is labeled 16 bytes. On the right, one red box headed Heap: one allocation, 56 bytes, holding two parts: a RobotStatus labeled 40 bytes, and below it a control block reading use_count: 2 and weak_ptrs: 0. From each stack box, a blue arrow runs from the object row to the RobotStatus and from the control row to the control block.
   :align: center
   :width: 100%

   Two ``std::shared_ptr``\ s to one robot. Both point at the robot and at the control block that ``std::make_shared`` put in the same allocation.

- A ``std::shared_ptr`` is two pointers, 16 bytes: to the robot, and to the **control block** that holds the count.
- ``std::make_shared``: one allocation of 56 bytes for both, measured. With ``new``: two, 40 and 24 bytes.
- A copy adds 1 to the count; destroying a ``std::shared_ptr`` subtracts 1.

See `One Allocation with make_shared`_ under Further Reading.

``use_count``, Step by Step
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto robot{std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false)};                // 1
   std::shared_ptr<RobotStatus> in_queue{robot};            // 2: a copy
   std::shared_ptr<RobotStatus> moved{std::move(in_queue)}; // 2: a move
   moved.reset();                                           // 1

.. code-block:: text

   created: 1
   copied: 2
   moved: 2, in_queue == nullptr: true
   reset: 1

- A copy adds an owner. A move hands one owner's place to another: the count stays at 2, and ``in_queue`` is left empty.
- ``reset()`` gives up this owner's place. The robot is deleted only when the count reaches 0.

Deletion by the Last Owner
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   fleet.push_back(std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false));
   charging_queue.push_back(fleet[0]);
   fleet.clear();           // robot 3 leaves the fleet, still in the queue
   charging_queue.clear();  // the last owner: robot 3 is deleted here

.. code-block:: text

   both lists: 2
   after fleet.clear(): 1, robot 3 still there
   after charging_queue.clear(): no owner left

- The queue keeps robot 3 alive after the fleet lets go. That is what the raw pointer of `A Robot in Two Lists`_ could not do.
- Neither list deletes the robot itself. Whichever lets go last does, and nothing leaks: ``702run week7_playground 50`` ends with no LeakSanitizer report.

.. _l7-shared-borrow:

Passing: Borrow
^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_status(const RobotStatus& robot);  // only reads the robot

   auto robot{std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false)};
   print_status(*robot);
   std::cout << robot.use_count() << '\n';       // 1: no owner added

- The same rule as for ``std::unique_ptr`` (:ref:`l7-unique-borrow`): a function that only uses the robot takes the robot, not the smart pointer.
- A ``std::shared_ptr`` passed by value would add an owner and remove it again: two changes to the count for nothing.

.. note::

   Rule: `Core Guidelines R.30 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrparam>`__, again.

Passing: Share
^^^^^^^^^^^^^^

.. code-block:: cpp

   using Fleet = std::vector<std::shared_ptr<RobotStatus>>;

   void add_to_queue(Fleet& queue, std::shared_ptr<RobotStatus> robot) {
     queue.push_back(std::move(robot));  // keeps it: the queue is an owner
   }

   add_to_queue(charging_queue, robot);
   std::cout << robot.use_count() << '\n';  // 2

- By value: the parameter is one more owner. The function moves it into the queue, so the queue keeps that owner's place.
- ``using Fleet = ...;`` is a type alias (Lecture 2): a shorter name for the long type.

.. note::

   "Take a ``shared_ptr<widget>`` parameter to express shared ownership". Rule: `Core Guidelines R.34 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-owner>`__.

Passing: ``const shared_ptr&``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void queue_if_low(Fleet& queue,
                     const std::shared_ptr<RobotStatus>& robot) {
     if (robot->battery_pct < 20.0) {
       queue.push_back(robot);  // copies only when it keeps it
     }
   }
   queue_if_low(charging_queue, low);   // 14 %: queued
   queue_if_low(charging_queue, full);  // 90 %: not queued

.. code-block:: text

   low.use_count(): 2, full.use_count(): 1, charging_queue.size(): 1

- By ``const&``: no owner is added by the call. The function copies the ``std::shared_ptr`` only if it decides to keep the robot.

.. note::

   "Take a ``const shared_ptr<widget>&`` parameter to express that it might retain a reference count to the object" (a rule the Guidelines have not finished). Rule: `Core Guidelines R.36 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-const>`__.

.. _l7-shared-returning:

Returning
^^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<RobotStatus> make_robot(int id);  // slide 43

   std::shared_ptr<RobotStatus> robot{make_robot(5)};  // compiles
   std::unique_ptr<RobotStatus> back{robot};           // does not compile

.. code-block:: text

   error: no matching function for call to
   'std::unique_ptr<RobotStatus>::unique_ptr(<brace-enclosed initializer list>)'

``make_robot`` is the factory from :ref:`l7-unique-returning`.

- A ``std::unique_ptr`` converts to a ``std::shared_ptr``: one owner becomes the first of several.
- Not the other way: other owners may exist, and a ``std::unique_ptr`` must be the only one.
- So a function that creates a robot returns a ``std::unique_ptr``. The caller turns it into a ``std::shared_ptr`` if it needs to share.

``std::weak_ptr``
-----------------

A ``std::weak_ptr`` watches an object that ``std::shared_ptr``\ s own. It never keeps the object alive, and it can tell whether the object still exists.

See `cppreference: std::weak_ptr <https://en.cppreference.com/w/cpp/memory/weak_ptr>`__. Rule: `Core Guidelines R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`__.

A Cycle
^^^^^^^

.. code-block:: cpp

   struct Robot { RobotStatus status;
                  std::shared_ptr<Robot> partner; };
   auto a{std::make_shared<Robot>(RobotStatus{1, 82.5})};
   auto b{std::make_shared<Robot>(RobotStatus{2, 35.0})};
   a->partner = b;  // a owns b
   b->partner = a;  // b owns a

.. figure:: /_static/images/l7/cycle.png
   :alt: Two panels separated by a thin line, tagged 1 and 2. In each, two red boxes, robot 1 and robot 2, side by side, each with three rows: use_count, status, and partner. A green arrow runs from the partner row of robot 1 straight across to the partner row of robot 2, and another from the bottom of robot 2, under both boxes, up into robot 1. Panel 1: two blue-outlined boxes, a and b, above the robots, with green arrows down to robot 1 and robot 2; both robots read use_count: 2. Panel 2: no a and b boxes; both robots read use_count: 1.
   :align: center
   :width: 100%

   Two robots that own each other. **1**: while ``a`` and ``b`` exist, each robot has two owners. **2**: ``a`` and ``b`` are gone, and each count stays at 1.

- **1**: while ``a`` and ``b`` exist, each robot has two owners.
- **2**: ``a`` and ``b`` are gone. Each count is 1, never 0: each robot keeps the other alive, and nothing outside can reach either.

The Cycle, Measured
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   a.use_count(): 2, b.use_count(): 2

   ==1747904==ERROR: LeakSanitizer: detected memory leaks

   Indirect leak of 72 byte(s) in 1 object(s) allocated from:
       #0 0x737f78afe548 in operator new(unsigned long)
       ...
       #9 0x5e88939d2db1 in undefined::shared_cycle::run() .../undefined.cpp:77
   Indirect leak of 72 byte(s) in 1 object(s) allocated from:
       ...
       #9 0x5e88939d2c05 in undefined::shared_cycle::run() .../undefined.cpp:76

   SUMMARY: AddressSanitizer: 144 byte(s) leaked in 2 allocation(s).

- ``702run week7_playground 57``. Both robots leak, one allocation each: lines 76 and 77 are the two ``std::make_shared`` calls.
- 72 bytes each: a ``Robot`` (40 for the status, 16 for the ``std::shared_ptr``) and its 16-byte control block, in one ``std::make_shared`` allocation.
- **Indirect**: each robot is reachable only from the other leaked robot.

Breaking It
^^^^^^^^^^^

.. code-block:: cpp

   struct Robot {
     RobotStatus status;
     std::weak_ptr<Robot> partner;  // watches, does not own
   };
   a->partner = b;  // b's count stays 1
   b->partner = a;  // a's count stays 1

.. code-block:: text

   a.use_count(): 1, b.use_count(): 1

- A ``std::weak_ptr`` made from a ``std::shared_ptr`` does not add to the count.
- When ``a`` and ``b`` go out of scope, both counts reach 0 and both robots are deleted. ``702run week7_playground 58``: no LeakSanitizer report.

.. note::

   "Use ``std::weak_ptr`` to break cycles of ``shared_ptr``\ s". Rule: `Core Guidelines R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`__.

Reading a ``weak_ptr``
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   struct Dashboard {
     std::weak_ptr<RobotStatus> shown;  // the robot on screen
   };

   void show(const Dashboard& dashboard) {
     if (std::shared_ptr<RobotStatus> robot{dashboard.shown.lock()}) {
       std::cout << "robot " << robot->id << ": "
                 << robot->battery_pct << " %\n";
     } else {
       std::cout << "the robot is gone\n";
     }
   }

- A ``std::weak_ptr`` has no ``->`` and no ``*``. ``lock()`` returns a ``std::shared_ptr``: the robot, or an empty one if it is gone.
- While ``robot`` exists, it is one more owner, so the robot cannot be deleted in the middle of ``show``.
- ``702run week7_playground 59``: ``robot 3: 14 %``, then, after the fleet lets go, ``the robot is gone``.

See `A Dashboard of weak_ptr`_ under Further Reading.

``expired`` and ``use_count``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto robot{std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false)};
   std::weak_ptr<RobotStatus> watch{robot};
   robot.reset();  // the only owner lets go

.. code-block:: text

   watch.use_count(): 1, watch.expired(): false
   watch.use_count(): 0, watch.expired(): true

- ``use_count()`` counts the ``std::shared_ptr``\ s that own the robot. ``expired()`` is ``true`` when that count is 0.
- To use the robot, call ``lock()`` and test the result. ``expired()`` then ``lock()`` is two steps, and the last owner could let go between them.

.. note::

   C++20 **[util.smartptr.weak.obs]** (20.11.4.5): ``expired()`` "Returns: use_count() == 0." ``lock()`` "Returns: expired() ? shared_ptr<T>() : shared_ptr<T>(\*this), executed atomically."

Exercise 3: Use Counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto robot{std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false)};
   std::weak_ptr<RobotStatus> watch{robot};  // 1
   auto a{robot};                            // 2
   auto b{std::move(a)};                     // 3
   std::weak_ptr<RobotStatus> watch_2{b};    // 4
   robot.reset();                            // 5
   b.reset();                                // 6

- After each numbered line: how many ``std::shared_ptr``\ s own the robot, and is ``watch`` expired?
- Check: ``702run week7_playground 61``.

Choosing a Pointer
------------------

The question is always the same: who gives this object's memory back? The answer picks the pointer.

Rule: `Core Guidelines R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`__.

One Table
^^^^^^^^^

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - The code...
     - Use
     - In our fleet
     - Rule
   * - only uses the object
     - ``T&``, ``const T&``, or ``T*``
     - the ``print_status`` of :ref:`l7-unique-borrow`
     - R.30
   * - is its only owner
     - ``std::unique_ptr<T>``, from ``std::make_unique``
     - the fleet's robots
     - R.21, R.23
   * - is one of several owners
     - ``std::shared_ptr<T>``, from ``std::make_shared``
     - robot 3, in the fleet and the queue
     - R.22
   * - watches, and must not keep it alive
     - ``std::weak_ptr<T>``
     - the dashboard; partner robots
     - R.24
   * - calls ``new`` and ``delete`` itself
     - nothing: do not write it
     - `A Robot on the Heap`_ to `The Leak, Measured`_
     - R.11

- Start with ``std::unique_ptr``. Change to ``std::shared_ptr`` only when a second owner appears: it costs a control block and a count.
- Parameters: by value to take ownership (R.32, R.34), ``std::unique_ptr<T>&`` to reseat (R.33), and the object itself to only use it (R.30).

See `More Core Guidelines`_ under Further Reading.

Back to the Fleet
^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/owner_map.png
   :alt: A UML object diagram in black and white: six boxes joined by lines, with nothing written on the lines. On the left, a box labeled fleet. In the middle, three boxes labeled robot1 : RobotStatus, robot2 : RobotStatus and robot3 : RobotStatus, one above the other. On the right, a box labeled charging_queue and, below it, a box labeled dashboard : Dashboard. Lines with a filled diamond at the fleet end join the fleet to robot1 and to robot2. Lines with an open diamond at the owner end join the fleet to robot3 and the charging_queue to robot3. A line with no diamond runs from the dashboard to robot3 and ends in an open arrowhead at robot3.
   :align: center
   :width: 100%

   The fleet with its smart pointers. **Filled diamond**: ``std::unique_ptr``. **Open diamond**: ``std::shared_ptr``. **Arrow, no diamond**: ``std::weak_ptr``.

- One ``std::vector`` holds one type: once robot 3 is shared, the fleet holds a ``std::shared_ptr`` for every robot (:ref:`l7-shared-creating-one`).
- Robots 1 and 2 still have one owner each, through that ``std::shared_ptr``.

Summary
-------

**Who Owns This Robot**

- The last owner of a heap object gives it back. A ``T*`` cannot say it owns, and that causes a leak, a double ``delete`` or a dangling read.
- LeakSanitizer, part of ``-fsanitize=address``, reports a leak with the line that allocated it.

**Move Semantics**

- A move hands over what an object owns: 24 bytes for a ``std::vector``, not its elements. The source is valid but unspecified: assign it before reuse.
- Every expression is an lvalue, an xvalue or a prvalue; ``decltype((e))`` tells which. ``T&&`` binds to rvalues only, and a named ``T&&`` is an lvalue.
- ``std::move`` is a cast; the move happens where the result is taken. Not on a ``const`` object, and not on a returned local.

**std::unique_ptr**

- One owner, 8 bytes, from ``std::make_unique``. Moved, never copied; a moved-from one is null.
- Pass the object to use it, the ``std::unique_ptr`` by value to hand it over, by reference to reseat it. Return it by value.

**std::shared_ptr**

- Several owners and a count in a control block, from ``std::make_shared`` in one allocation. The last owner deletes the object.
- A ``std::unique_ptr`` converts to a ``std::shared_ptr``, not back.

**std::weak_ptr**

- Watches without owning: ``lock()`` gives a ``std::shared_ptr`` or an empty one. It breaks a cycle of ``std::shared_ptr``\ s, which would otherwise leak.

Further Reading
---------------

The sections below come from the appendix of the slides. They are **not presented** in the lecture. Read them on your own.

Double Delete, Measured
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   RobotStatus* robot{make_robot(3, 64.0)};  // make_robot(id, battery_pct)
   std::vector<RobotStatus*> fleet{robot};
   std::vector<RobotStatus*> idle{robot};  // the same robot
   for (RobotStatus* r : fleet) { delete r; }
   for (RobotStatus* r : idle) { delete r; }  // a second delete

.. code-block:: text

   ==1824048==ERROR: AddressSanitizer: attempting double-free on 0x5040000000d0
       #1 0x5f7fd89b28fb in undefined::double_delete::run() .../undefined.cpp:53
   0x5040000000d0 is located 0 bytes inside of 40-byte region [...)
   freed by thread T0 here:
       #1 0x5f7fd89b272d in undefined::double_delete::run() .../undefined.cpp:52

- ``702run week7_appendix ii``. AddressSanitizer stops the program at the second ``delete``, line 53, and names the first one, line 52.
- The region is 40 bytes: one ``RobotStatus``. Without the sanitizer, a double ``delete`` is undefined behavior: a crash, or nothing visible.

Dangling Read, Measured
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   RobotStatus* robot{make_robot(3, 64.0)};  // make_robot(id, battery_pct)
   std::vector<RobotStatus*> fleet{robot};
   std::vector<RobotStatus*> idle{robot};
   for (RobotStatus* r : fleet) { delete r; }
   std::cout << idle[0]->battery_pct << '\n';  // freed memory

.. code-block:: text

   ==1824050==ERROR: AddressSanitizer: heap-use-after-free on address 0x5040000000d8
   0x5040000000d8 is located 8 bytes inside of 40-byte region [...)
   freed by thread T0 here:
       #1 0x61fe445c6e6c in undefined::dangling_read::run() .../undefined.cpp:63
   SUMMARY: AddressSanitizer: heap-use-after-free .../undefined.cpp:64

- ``702run week7_appendix iii``. The read is on line 64; the ``delete`` that freed the robot is on line 63.
- "8 bytes inside": ``battery_pct`` starts at byte 8 of a ``RobotStatus``, as ``offsetof`` showed in Lecture 6.

The Moved-from ``std::string``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::string note{"robot 3 waits at the charging dock"};
   std::string name{"robot 3"};
   std::string taken_note{std::move(note)};
   std::string taken_name{std::move(name)};
   // note.size(): 0, name.size(): 0     (g++ 13.3, libstdc++)
   note = "robot 4 is charging";  // assigning gives it a known value again

- With libstdc++, both moved-from strings are empty, the long one and the short one.
- The standard does not promise that. Another library may leave text behind, so code that reads ``note`` after the move depends on one library.
- What you may do with a moved-from string: assign to it, or destroy it. Both work for any valid state.

.. note::

   C++20 **[string.cons]** (21.3.2.2) paragraph 3, on ``basic_string(basic_string&& str)``: "str is left in a valid but unspecified state."

Move Assignment
^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> current{make_route(3)};
   std::vector<Position> next{make_route(1000)};
   const Position* where{next.data()};
   current = std::move(next);  // current's 3 waypoints are destroyed
   // current.size(): 1000, current.data() == where: true, next.size(): 0

- `Handing a Route to a Robot`_ moved into a new vector. Here ``current`` already exists: the move gives up its old 3 waypoints and takes the 1000 of ``next``, without copying them (same ``data()``).
- ``next.size()`` is 0 with libstdc++. The standard says what ``current`` holds afterwards, and nothing about ``next``.

.. note::

   C++20 **[container.requirements.general]** (22.2.1), Table 76, ``a = rv``: "All existing elements of a are either move assigned to or destroyed." "Postconditions: a is equal to the value that rv had before this assignment."

``std::exchange``
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Position> route{make_route(1000)};
   // take the route, and leave an empty one behind
   std::vector<Position> done{std::exchange(route, {})};
   // done.size(): 1000, route.size(): 0

   int task_id{7};
   int finished{std::exchange(task_id, 0)};  // finished: 7, task_id: 0

- ``std::exchange(obj, new_value)``, from ``<utility>``, sets ``obj`` to ``new_value`` and returns the value ``obj`` had before.
- After ``std::move(route)`` the route is valid but unspecified. After ``std::exchange(route, {})`` it is empty, guaranteed: it was assigned ``{}``.

.. note::

   C++20 **[utility.exchange]** (20.2.3) paragraph 1: "Effects: Equivalent to: ``T old_val = std::move(obj);`` ``obj = std::forward<U>(new_val);`` ``return old_val;``". See `cppreference: std::exchange <https://en.cppreference.com/w/cpp/utility/exchange>`__.

The Definition of ``std::move``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   template <typename T>  // the standard's std::move, under another name
   constexpr std::remove_reference_t<T>&& my_move(T&& t) noexcept {
     return static_cast<std::remove_reference_t<T>&&>(t);
   }

   std::vector<Position> route{make_route(1000)};
   static_assert(std::is_same_v<decltype(my_move(route)),
                                std::vector<Position>&&>);
   std::vector<Position> taken{my_move(route)};  // taken: 1000, route: 0

- In a function template, a ``T&&`` parameter also accepts an lvalue: for ``route``, ``T`` is ``std::vector<Position>&``.
- ``std::remove_reference_t<T>`` removes that ``&``, so the cast is always to ``std::vector<Position>&&``, an xvalue. The function only casts: no data moves until ``taken`` is built.

.. note::

   C++20 **[forward]** (20.2.4) paragraph 5, on ``move(T&& t)``: "Returns: ``static_cast<remove_reference_t<T>&&>(t)``."

A ``unique_ptr`` with Its Own Deleter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto say_and_delete{[](RobotStatus* robot) {
     std::cout << "  deleting robot " << robot->id << '\n';
     delete robot;
   }};
   {
     std::unique_ptr<RobotStatus, decltype(say_and_delete)> robot{
         new RobotStatus{3, 64.0, {2.0, 3.0}, false}, say_and_delete};
     // sizeof(robot): 8
   }  // prints: deleting robot 3

- The second template argument is the **deleter**: what the pointer calls instead of ``delete``. Here a lambda (Lecture 6) that prints first.
- ``std::make_unique`` cannot take a deleter, so the code calls ``new`` and hands the result to the ``std::unique_ptr`` in the same statement.
- A lambda with no captures adds no bytes: 8. A function pointer as the deleter makes it 16 (measured).

.. note::

   Rule: `Core Guidelines R.12 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-immediate-alloc>`__, "Immediately give the result of an explicit resource allocation to a manager object".

``std::auto_ptr``
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::auto_ptr<RobotStatus> a{new RobotStatus{3, 64.0}};
   std::auto_ptr<RobotStatus> b{a};  // looks like a copy
   // a.get() == nullptr: true

.. code-block:: text

   warning: 'template<class> class std::auto_ptr' is deprecated:
            use 'std::unique_ptr' instead [-Wdeprecated-declarations]

- ``std::auto_ptr`` was the owning pointer before C++11. Its "copy" moved: after ``b{a}``, ``a`` was empty.
- ``std::unique_ptr`` transfers ownership too, but only through ``std::move``, so a reader sees it. A plain copy does not compile (`One Owner Only`_).
- g++ 13 still accepts ``std::auto_ptr`` with ``-std=c++20``, with the warning above. Do not use it.

.. note::

   C++20 **[diff.cpp14.depr]** (C.2.11) paragraph 1: "The class templates auto_ptr, unary_function, and binary_function [...] are not defined." "Rationale: Superseded by new features."

Testing for Empty
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<RobotStatus> robot;  // empty
   // robot == nullptr: true
   robot = std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false);
   if (robot) {
     std::cout << "robot " << robot->id << '\n';  // robot 3
   }
   auto other{std::move(robot)};  // !robot: true
   bool has_robot = other;  // does not compile

.. code-block:: text

   error: cannot convert 'std::unique_ptr<RobotStatus>' to 'bool' in initialization

- ``if (robot)``, ``!robot`` and ``robot == nullptr`` all test for empty. The same works for ``std::shared_ptr``.
- The conversion to ``bool`` is ``explicit``: a condition and ``bool has_robot{other};`` use it, but the ``=`` form does not compile.

``unique_ptr`` to an Array
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto readings{std::make_unique<double[]>(5)};  // five doubles, each 0.0
   readings[2] = 14.0;
   for (int i{0}; i < 5; ++i) {
     std::cout << readings[i] << ' ';  // 0 0 14 0 0
   }
   // sizeof(readings): 8, sizeof(std::vector<double>): 24

- ``std::unique_ptr<double[]>`` calls ``delete[]``, not ``delete``, and has ``[]`` instead of ``->``.
- It is 8 bytes because it does not keep the length. No ``size()``, no ``push_back``, no range-based ``for``: the 5 is yours to remember.
- A ``std::vector<double>`` (Lecture 4) keeps the length and grows. Use it unless an interface needs a plain array.

.. note::

   C++20 **[unique.ptr.create]** (20.11.1.4) paragraph 4, ``make_unique<T[]>(n)``: "Returns: ``unique_ptr<T>(new remove_extent_t<T>[n]())``." The ``()`` sets each element to 0. Rule: `Core Guidelines SL.con.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-vector>`__.

``swap``
^^^^^^^^

.. code-block:: cpp

   auto first{std::make_unique<RobotStatus>(
       3, 64.0, Position{2.0, 3.0}, false)};
   auto second{std::make_unique<RobotStatus>(
       4, 90.0, Position{6.0, 2.0}, false)};
   const RobotStatus* robot_3{first.get()};
   first.swap(second);  // the same as std::swap(first, second)
   // first->id: 4, second->id: 3, second.get() == robot_3: true

- ``swap`` exchanges the two stored pointers. No robot is created, copied or deleted: robot 3 is at the same address, now owned by ``second``.
- ``std::shared_ptr`` has the same ``swap``.

.. note::

   C++20 **[unique.ptr.single.modifiers]** (20.11.1.2.5) paragraph 7, ``swap(u)``: "Invokes swap on the stored pointers and on the stored deleters of \*this and u."

One Allocation with ``make_shared``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto made{std::make_shared<RobotStatus>(
       3, 14.0, Position{2.0, 3.0}, false)};
   std::shared_ptr<RobotStatus> from_new{
       new RobotStatus{3, 14.0, {2.0, 3.0}, false}};

.. code-block:: text

   std::make_shared<RobotStatus>: 1 allocation(s): 56 bytes
   std::shared_ptr<RobotStatus>{new ...}: 2 allocation(s): 40 24 bytes

- ``702run week7_allocations`` counts every heap allocation each line makes.
- ``std::make_shared`` puts the robot and the control block in one block of 56 bytes (`The Control Block`_).
- With ``new``, the robot already exists when the ``std::shared_ptr`` is built, so the control block needs a second allocation: 40 bytes for the robot, 24 for the control block.

.. note::

   C++20 **[util.smartptr.shared.create]** (20.11.3.6) paragraph 7.1: "Implementations should perform no more than one memory allocation." Rule: `Core Guidelines R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`__.

A Dashboard of ``weak_ptr``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::weak_ptr<RobotStatus>> shown;
   for (const auto& robot : fleet) {  // robots 1, 2, 3
     shown.push_back(robot);  // watches, does not own
   }
   fleet.erase(fleet.begin() + 1);  // robot 2 is deleted
   for (const auto& watched : shown) {
     if (auto robot{watched.lock()}) {
       std::cout << "  robot " << robot->id << ": "
                 << robot->battery_pct << " %\n";
     } else {
       std::cout << "  (gone)\n";
     }
   }
   std::erase_if(shown, [](const std::weak_ptr<RobotStatus>& w) {
     return w.expired();
   });

- Output: ``robot 1: 82.5 %``, ``(gone)``, ``robot 3: 14 %``, then ``shown.size()`` is 2.
- The dashboard never keeps a robot alive. Lecture 4's ``std::erase_if`` with a lambda (Lecture 6) drops the entries whose robot is gone.

More Core Guidelines
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Rule
     - Title
   * - `R.4 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ref>`__
     - A raw reference (a ``T&``) is non-owning
   * - `R.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-scoped>`__
     - Prefer scoped objects, don't heap-allocate unnecessarily
   * - `R.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-mallocfree>`__
     - Avoid ``malloc()`` and ``free()``
   * - `R.13 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-single-alloc>`__
     - Perform at most one explicit resource allocation in a single expression statement
   * - `R.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam>`__
     - Take a ``shared_ptr<widget>&`` parameter to express that a function might reseat the shared pointer
   * - `R.37 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrget>`__
     - Do not pass a pointer or reference obtained from an aliased smart pointer

- R.5 comes first in practice: a ``RobotStatus`` that lives only inside one function is a local variable, not a heap object.
- R.37: when you pass ``*robot`` or ``robot.get()`` to a function, make sure an owner outlives the call.
