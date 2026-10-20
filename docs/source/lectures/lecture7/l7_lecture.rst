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
   │   ├── include/
   │   └── src/
   ├── appendix/
   │   └── src/
   ├── common/
   │   ├── include/
   │   └── src/
   └── undefined/
       ├── include/
       └── src/

**Run a Slide's Code**

1. Get the code: ``git pull``.
2. In the top-level ``CMakeLists.txt`` (repository root), check that ``add_subdirectory(project/week7)`` is not commented out.
3. Configure: ``702configure``.
4. Build it: ``702build week7_playground``.
5. Run every slide: ``702run week7_playground``. Run only one slide, for example `Inside a Copy`_: ``702run week7_playground 12``.

**Code That Leaks or Breaks**

- The code that leaks or breaks is in the **undefined** folder, built with AddressSanitizer. It runs only when you ask for its slide by number.
- The code of the appendix is in the **appendix** folder. Run appendix frame ii with ``702run week7_appendix ii``.

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

   A slide whose code leaks or has undefined behavior, such as slide 78, runs only when you ask for it by number: ``702run week7_playground 78``. A full run skips it.

.. note::

   The `Further Reading`_ part, after the summary, is the appendix of the slides. It is not presented. Read it on your own.

Reminder: Returning by Value
----------------------------

From L5. **Copy elision**: the compiler builds the returned object **directly in the caller's destination**, so the copy or move from the function's object is never made.

.. figure:: /_static/images/l7/return_by_value.png
   :alt: A UML activity diagram in black and white. From a start dot, an arrow leads to a decision: a function returns an object by value: what does it return? Three arrows leave it. The first leads to the box Elision: built in the caller's destination. From it a second decision, which kind?, leads to two boxes: RVO: a temporary, return std::vector<double>(n); always, since C++17; and NRVO: a named local, return v; usually, but not required. The second arrow leads to the box Implicit move: a named local, when NRVO is not done, return v; the local is moved: its elements are handed over. The third arrow leads to the box Copy: anything that is not the plain name of a local, return first ? x : y; every element is copied.
   :align: center
   :width: 100%

   What the compiler does with a return by value, as a UML activity diagram: one branch for each kind of returned expression.

- **RVO** is Return Value Optimization. The N is for **named**.
- The order is elide, then move, then copy.
- This lecture shows what a move does inside a ``std::vector`` (`Inside a Move`_).

The Program We Will Build
-------------------------

An autonomous car, the **ego vehicle**, drives along a two-lane road. Its software has a **tracker**, which sees four obstacles; a **planner**, which plans a path past them; and a **dashboard**, which shows the driver one obstacle. In this lecture we write all three.

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - id
     - What it is
     - x (m)
     - y (m)
     - heading (rad)
     - speed (m/s)
     - static
   * - 1
     - parked car
     - 20.0
     - -3.0
     - 0.00
     - 0.0
     - yes
   * - 2
     - cyclist
     - 12.0
     - -1.0
     - 0.00
     - 4.0
     - no
   * - 3
     - pedestrian crossing
     - 30.0
     - 2.5
     - 1.57
     - 1.4
     - no
   * - 4
     - oncoming car
     - 38.0
     - 3.5
     - 3.14
     - 13.4
     - no

**Who Holds an Obstacle**

- **tracker**: one record per obstacle it sees; deletes it when the track is lost.
- **planner**: shares the obstacles near its path, the **hazards**.
- **dashboard**: shows one obstacle; only looks.

**The Road**

- x: along the road, from where the ego vehicle starts.
- y: to the left of the center of its lane. Lanes are 3.5 m wide.
- heading: 0 along the road, counterclockwise.

.. note::

   The values are chosen for this example. The obstacles are data in the program, not cars on a street: losing track of the cyclist deletes an ``Obstacle`` object, and nothing on the road moves.

.. figure:: /_static/images/l7/av_road.png
   :alt: A top view of a straight two-lane road, drawn to scale, with an x axis along the bottom marked 0, 10, 20, 30 and 40 meters and a y axis on the left marked 0.0 and 3.5 meters at the two lane centers. From the bottom up: a lighter parking strip, the lane of the ego vehicle, a dashed yellow center line, and the oncoming lane. The ego vehicle, a blue car seen from above and tagged E, sits at x 0 in the center of its lane, facing plus x, with a white arrow pointing in plus x. Tag 1: an amber car of another shape, parked in the parking strip at x 20, facing plus x. Tag 2: a green cyclist seen from above, at x 12 near the right edge of the ego lane, facing plus x, with an arrow in plus x. Tag 3: a gray circle, the pedestrian, at x 30 in the oncoming lane, with an arrow pointing up, toward plus y. Tag 4: a coral red car of a third shape, at x 38 in the oncoming lane, facing minus x, with an arrow pointing in minus x.
   :align: center
   :width: 100%

   The table, drawn to scale.

- Tags 1 to 4: the obstacles of the table, by id. Tag E: the ego vehicle.
- Arrows: the direction of travel of what moves. Their length is not to scale.

One Row, One Obstacle
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   struct Pose {
     double x{0.0};       // m
     double y{0.0};       // m
     double heading{0.0}; // rad
   };

   struct Obstacle {
     int id{0};
     Pose pose{};
     double speed{0.0}; // m/s
     bool is_static{false};
   };

- The tracker keeps one ``Obstacle`` object for each row of the table.
- The cyclist, id 2: ``Obstacle{2, {12.0, -1.0, 0.0}, 4.0}``. ``is_static`` is not given, so it takes its default, ``false``.
- ``sizeof(Pose)`` is 24 bytes, ``sizeof(Obstacle)`` 48: 4 bytes of padding after ``id`` and 7 after ``is_static`` (L6).

Who Owns Each Obstacle
^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/av_owner_map.png
   :alt: A UML object diagram in black and white: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner.
   :align: center
   :width: 80%

   Who owns each ``Obstacle`` object, as a UML object diagram.

- A UML object diagram (L9): one box per object. ``: Obstacle`` is an ``Obstacle`` object on the heap, with no name; under the line, its members' values (the table above).
- **Filled diamond**, the only owner: ``tracker`` owns ids 1, 3 and 4. **Open diamond**, one of several owners: ``tracker`` and ``planner`` own id 2, the cyclist. In the code, the planner's list is ``hazards``.
- **Arrow, no diamond**, looks without owning: ``dashboard`` looks at id 2.

Ownership
---------

An **owner** of a heap object is code that keeps it alive. An object can have one owner or several: the last owner to let go deletes it.

Rule: `Core Guidelines R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr>`__.

An Obstacle on the Heap
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Obstacle* make_track(int id, Pose pose, double speed) {
     return new Obstacle{id, pose, speed};
   }

   Obstacle* cyclist{make_track(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   std::cout << cyclist->id << ' ' << cyclist->speed << '\n';  // 2 4
   delete cyclist;  // the caller must remember this
   cyclist = nullptr;

- ``make_track`` creates the ``Obstacle`` object with ``new``. The caller must ``delete`` it.

.. note::

   "A raw pointer (a ``T*``) is non-owning". Rule: `Core Guidelines R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr>`__.

See `Double Delete, Measured`_ and `Dangling Read, Measured`_ under Further Reading: the double ``delete`` and the dangling read that raw ``new`` and ``delete`` allow.

RAII
^^^^

**RAII**, resource acquisition is initialization: the object that holds a resource, such as memory, gives it back in its destructor.

- A ``std::vector`` is RAII: the planner's path, a ``std::vector<Pose>``, frees its heap block when it goes out of scope.
- A **smart pointer** that owns is RAII for one heap object (`Smart Pointers`_): ``std::unique_ptr`` (the only owner) or ``std::shared_ptr`` (one of several owners). ``std::weak_ptr`` only observes.

.. note::

   "Manage resources automatically using resource handles and RAII". Rule: `Core Guidelines R.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-raii>`__.

Move Semantics
--------------

**Move semantics** are the rules that let one object take over what another object owns, such as its heap memory, instead of copying it.

A **copy** makes a second object with its own memory: a new block, every element copied. A **move** hands what one object owns to another: a few pointers change, and no element is copied.

See `cppreference: std::move <https://en.cppreference.com/w/cpp/utility/move>`__.

Inside a Copy
^^^^^^^^^^^^^

.. dropdown:: The Definition of ``make_path``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      std::vector<Pose> make_path(int n) {
        std::vector<Pose> path;
        path.reserve(n);  // room for n poses: one allocation
        for (int i{0}; i < n; ++i) {
          path.push_back({static_cast<double>(i), 0.0, 0.0});
        }
        return path;
      }

   - It builds a path of ``n`` poses, one meter apart along the road: pose ``i`` is at x = ``i`` meters, y = 0, heading 0.
   - ``reserve(n)`` allocates room for ``n`` poses before the loop. Without it, ``push_back`` allocates 11 times for 1000 poses, and ends with room for 1024.
   - ``702run week7_appendix iv`` prints the three poses of ``make_path(3)``: (0, 0, 0) (1, 0, 0) (2, 0, 0).
   - It returns the local ``path`` by value: no copy is made (`Returning a Local`_, under Further Reading).

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   path.reserve(1024);              // room for 24 more
   std::vector<Pose> copied{path};  // a copy

.. figure:: /_static/images/l7/av_vector_copy.png
   :alt: Two panels side by side, one per vector, each under a rounded name tag: path on the left, copied on the right. In each panel, a blue box with a stack icon and the word Stack holds three fields, begin, end and capacity, each marked ptr. Below it, a red box with a heap icon and the word Heap holds a strip of cells, and three blue arrows run from the fields down to the top edge of the strip. Under path, the strip ends in a gray part marked 24 free: the begin arrow ends at the left end of the first cell, the end arrow at the start of the gray part, and the capacity arrow at the right end of the strip. A measuring line under it reads 1024 Pose, 24576 bytes. Under copied, the strip has no gray part: the begin arrow ends at the left end of the first cell, and the end and capacity arrows both at the right end of the last cell. Its measuring line reads 1000 Pose, 24000 bytes. No arrow joins the two panels.
   :align: center
   :width: 100%

   A ``std::vector`` and its copy: each one owns its own block, and the copy has no spare slots.

- ``path.reserve(1024)`` gives ``path`` room for 24 more poses, so its block has spare slots. The copy shows that they are not copied.
- ``begin`` points at the first ``Pose``, ``end`` one past the last one (the right edge of the last cell), ``capacity`` one past the last slot.
- ``path``: 1024 slots (libstdc++ reserves exactly 1024), 1000 in use: 1024 × 24 = 24576 bytes, 24 unused (gray).
- ``copied``: 1000 × 24 = 24000 bytes. A copy allocates for the elements only, not the spare slots: its ``end`` equals its ``capacity``.
- Each vector frees its own block at the end of its scope. ``702run week7_playground 12`` prints both sizes and capacities.

Inside a Move
^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   path.reserve(1024);                        // room for 24 more
   const Pose* where{path.data()};            // where path's block is
   std::vector<Pose> moved{std::move(path)};  // std::move marks path

.. figure:: /_static/images/l7/av_vector_move.png
   :alt: Two panels separated by a thin line, tagged 1 and 2. Panel 1: a name tag reading path over a blue box with a stack icon and the word Stack, holding three fields, begin, end and capacity, each marked ptr. Below, a red box with a heap icon and the word Heap holds a strip of cells that ends in a gray part labeled 24 free. Three blue arrows run from the fields down to the top edge of the strip: begin ends at the left end of the first cell, end at the right end of the last cell in use, where the gray part starts, and capacity at the right end of the gray part. A measuring line under the whole strip reads 1024 Pose, 24576 bytes. Panel 2: a name tag reading path over the same Stack box, its three fields now reading nullptr, with no arrows. Below it a name tag reading moved over a second Stack box with the same three fields, each marked ptr, and three blue arrows from them to a strip of cells like the one in panel 1, with the same gray part labeled 24 free, ending at the same places, with the same measuring line, 1024 Pose, 24576 bytes.
   :align: center
   :width: 100%

   A ``std::vector`` before and after a move. **1**: ``path`` owns the block. **2**: after the move, ``moved`` owns the block and ``path``'s three pointers are null.

- **1**: ``path`` owns the block through its three pointers (L4): 1024 slots, 1000 in use.
- **2**: after the move, ``moved`` holds the same three pointers (``moved.data() == where``), and ``path``'s are null (libstdc++, measured). ``702run week7_playground 13`` prints ``moved.data() == where: true, path.size(): 0, path.data() == nullptr: true``.
- Only 24 bytes change hands, the three 8-byte pointers, so the block keeps its 24 spare slots: ``moved.capacity()`` is 1024. A copy leaves them out (`Inside a Copy`_). ``702run week7_playground 13`` also prints ``moved: size 1000, capacity 1024, 24576 bytes``.

Elision or a Move
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> make_scores() {
     std::vector<int> scores{90, 75, 82};
     std::cout << &scores << ' ' << scores.data() << '\n';  // local, block
     return scores;  // no std::move
   }

.. code-block:: cpp

   std::vector<int> best{make_scores()};  // elision: same two addresses
   std::cout << &best << ' ' << best.data() << '\n';

   std::vector<std::vector<int>> all;
   all.push_back(make_scores());  // a move: new vector, same block
   std::cout << &all[0] << ' ' << all[0].data() << '\n';

``make_scores`` prints the address of its local vector and of that vector's block. Each caller then prints the same two addresses for the vector it got. ``702run week7_playground 14`` prints, in one run (the addresses change from run to run):

.. code-block:: text

   elision:
     inside: 0x7ffce43fc630 0x502000000010
     best:   0x7ffce43fc630 0x502000000010
   move:
     inside: 0x7ffce43fc670 0x502000000030
     all[0]: 0x503000000160 0x502000000030

- ``best`` **is** ``scores``: a prvalue that initializes an object of its own type is elided (C++20 **[dcl.init]** 17.6.1). ``push_back`` takes a reference: it gets a temporary and moves it into ``all[0]``, a new vector that holds the same block (`Overloads for Copy and Move`_).
- ``return scores;`` may be elided (NRVO), but that is only permitted (**[class.copy.elision]** 11.10.5). Without it, ``best`` gets a new address, the same block: ``scores`` is moved out, an implicit move (`Returning a Local`_, under Further Reading). Compiled with ``-fno-elide-constructors``, which turns NRVO off, that is what happens.

The Moved-from Object
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   std::vector<Pose> controller_path{std::move(path)};
   std::cout << path.empty() << '\n';  // 1 (true) with libstdc++
   path = make_path(5);                // assign before you use it again
   std::cout << path.size() << ' ' << controller_path.size();  // 5 1000

- After a move, the source still exists. It is destroyed at the end of its scope.
- What it holds is not promised by the standard. libstdc++ leaves a moved-from ``std::vector`` empty; another library may not.
- Safe: destroy it, or assign it a new value. Then use it as before.

.. note::

   C++20 **[lib.types.movedfrom]** (16.5.5.16): "Unless otherwise specified, such moved-from objects shall be placed in a valid but unspecified state."

See `The Moved-from std::string`_, `Move Assignment`_ and `std::exchange`_ under Further Reading.

Exercise 1: Copy and Move
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   std::vector<Pose> a{make_path(3)};
   std::vector<Pose> b{a};
   std::vector<Pose> c{std::move(a)};
   a = std::move(b);

- At the board, after each line: draw ``a``, ``b`` and ``c`` on the stack, each with its ``begin``, ``end`` and ``capacity`` pointers (`Inside a Copy`_), and every block on the heap they point at.
- Line 4 is a move into a vector that already exists. What does ``a`` hold before it, and after?
- After line 4: how many blocks are on the heap? Which variable owns each one? Was any block freed?
- Check: ``702run week7_playground 16`` prints each vector's size, capacity and block after every line.

Value Categories
^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/value_categories.png
   :alt: A tree of rounded boxes. At the top, expression. Below it, two boxes joined to it: glvalue on the left, with the label has identity, and rvalue on the right, with the label may be taken. On the bottom row, three boxes: lvalue on the left, joined to glvalue; xvalue in the middle, joined to both glvalue and rvalue; and prvalue on the right, joined to rvalue. The drawing is symmetric about the middle line through expression and xvalue.
   :align: center
   :width: 60%

   The value categories.

- Every expression has a **type** and a **value category**.
- The category answers two questions: does it refer to an object that already exists (**identity**)? May another object **take** its contents?

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Category
     - Identity
     - May be taken
   * - lvalue
     - yes
     - no
   * - xvalue
     - yes
     - yes
   * - prvalue
     - no
     - yes

- Names (paragraph 3 of **[basic.lval]**): **l**, **r** once meant the left and right side of an assignment; **gl** "generalized", **pr** "pure", **x** "eXpiring".

.. note::

   The tree is Figure 1 of C++20 **[basic.lval]** (7.2.1); the labels under glvalue and rvalue are ours. Paragraph 2: "Every expression belongs to exactly one of the fundamental classifications in this taxonomy: lvalue, xvalue, or prvalue."

The Five Definitions
^^^^^^^^^^^^^^^^^^^^

The slide steps through the tree above one box at a time, from the top: expression, then glvalue and rvalue, then lvalue, xvalue and prvalue. The quotes are C++20 **[basic.lval]** paragraph 1.

**expression.** In plain words: code the program evaluates. A name or a literal alone is one, with no operator: C++20 calls it a primary expression (**[expr.prim]**). Operators build larger ones.

.. code-block:: cpp

   int count{3};
   int a{count};      // a name
   int b{42};         // a literal
   int c{count + 1};  // an operator

Each expression is exactly one of the three bottom boxes (lvalue, xvalue, prvalue); the middle two group them.

**glvalue**, a "generalized" lvalue. C++20: "an expression whose evaluation determines the identity of an object, bit-field, or function". In plain words: it refers to an object that already exists, so the object has an address.

.. code-block:: cpp

   int count{3};
   std::vector<int> scores{90, 75, 82};
   int* p{&count};  // has an address
   // refers to the object scores:
   auto best{std::move(scores)};

**rvalue.** C++20: "a prvalue or an xvalue". In plain words: an expression whose contents may be taken. An xvalue lets another object take them. A prvalue passed to a ``T&&`` parameter gets a temporary object (`Temporary Materialization`_), and nothing else can use it, so the function may take it (`Overloads for Copy and Move`_).

.. code-block:: cpp

   std::vector<int> scores{90, 75, 82};
   int next{scores[0] + 1};  // computed
   // marked:
   auto best{std::move(scores)};

**lvalue.** C++20: "a glvalue that is not an xvalue". In plain words: it refers to an object that already exists, and does not let another object take its contents.

.. code-block:: cpp

   int count{3};
   std::vector<int> scores{90, 75, 82};
   int* p{&count};     // count: lvalue
   auto copy{scores};  // scores: lvalue

**xvalue**, an "eXpiring" lvalue. C++20: "a glvalue that denotes an object or bit-field whose resources can be reused (usually because it is near the end of its lifetime)". In plain words: it refers to an object that already exists, and lets another object take its contents.

.. code-block:: cpp

   std::vector<int> scores{90, 75, 82};
   // std::move(scores): an xvalue
   auto best{std::move(scores)};

**prvalue**, a "pure" rvalue. C++20: "an expression whose evaluation initializes an object or a bit-field, or computes the value of an operand of an operator, [...]". In plain words: it refers to no object that already exists; it computes a value.

.. code-block:: cpp

   int count{3};         // 3
   int next{count + 1};  // count + 1

.. note::

   Paragraph 3: "Despite their names, these terms classify expressions, not values." The same variable can appear in an lvalue and in an xvalue.

lvalue: A Named Object
^^^^^^^^^^^^^^^^^^^^^^

An **lvalue** is an expression that (1) refers to an object that already exists, and (2) does not let another object take its contents. If you make a new object from it, the new object gets a copy, and the original keeps its contents.

.. code-block:: cpp
   :linenos:

   int count{3};        // makes an int object that holds 3
   count = 4;           // the same object now holds 4
   int* where{&count};  // where holds that object's address

- An **object** is a piece of memory that holds a value. Line 1 makes one and names it ``count``.
- In line 2, ``count`` is an lvalue. Part (1) of the definition holds: it refers to the object from line 1, which already exists. Part (2) holds: ``count`` is a plain name, with no ``std::move``, so nothing takes its contents. `lvalue: Copied, Not Taken`_ shows what taking looks like.
- In line 3, ``count`` in ``&count`` is an lvalue for the same two reasons.

lvalue: Copied, Not Taken
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   std::vector<int> scores{90, 75, 82};
   std::vector<int> copied{scores};
   std::vector<int> best{std::move(scores)};

- To **take** an object's contents is to move them into another object. To **mark** an object, with ``std::move``, is to say another object may take them. Line 3 takes the three numbers that ``scores`` keeps on the heap.
- In line 2, ``scores`` is an lvalue. Part (2) holds: ``copied`` gets its own copy, and ``scores`` keeps its three numbers.
- In line 3, ``std::move(scores)`` **marks** ``scores``. ``best`` takes its contents, and ``scores`` is left empty (libstdc++, measured). Part (2) fails: ``std::move(scores)`` is not an lvalue (`xvalue: Marked by std::move`_).
- One exception: ``return path;`` may move from a local variable even though ``path`` is an lvalue (`Elision or a Move`_).

lvalue: Checking with ``&``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   int count{3};
   int* a{&count};        // compiles
   int* b{&(count + 1)};  // does not compile

.. code-block:: text

   error: lvalue required as unary '&' operand

- The built-in ``&`` compiles only on an lvalue: parts (1) and (2) of the definition must both hold. Line 3 fails part (1); `Ways to Mark`_, under Further Reading, shows part (2) failing.
- In line 2, ``count`` is an lvalue: parts (1) and (2) hold (`lvalue: A Named Object`_). So ``&count`` compiles.
- In line 3, ``count + 1`` computes 4, but no object that already exists holds that 4. Part (1) fails: ``count + 1`` is not an lvalue, and ``&(count + 1)`` does not compile. `prvalue: A Computed Value`_ says what it is.

See `A Reference, an Element, *p`_ under Further Reading.

prvalue: A Computed Value
^^^^^^^^^^^^^^^^^^^^^^^^^

A **prvalue** is an expression that (1) does not refer to an object that already exists: it computes a value, and (2) lets another object take that value.

.. code-block:: cpp
   :linenos:

   int count{3};
   int next{count + 1};  // the 4 initializes next
   std::vector<Pose> path;
   path = make_path(5);  // path takes the block

- Part (1): does ``count + 1`` refer to an object that already exists? No. It computes 4, and no object held that 4 before line 2.
- Part (2): ``next``, a new object, takes the 4. ``count`` is unchanged.
- Line 4: ``make_path(5)``, a call that returns by value, is a prvalue too. ``path`` takes the block of 5 poses that ``make_path`` allocated: no pose is copied. ``702run week7_playground 24`` prints ``path took make_path's block: true``.
- An lvalue and an xvalue both refer to an object that already exists, and every expression is exactly one of the three (C++20 **[basic.lval]** paragraph 2). So ``count + 1`` is a prvalue. That is also why ``&(count + 1)`` does not compile (`lvalue: Checking with &`_).

See `Literals, Results, Calls`_ under Further Reading.

xvalue: Marked by ``std::move``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An **xvalue** is an expression that (1) refers to an object that already exists, and (2) lets another object take its contents: the object may be moved from.

.. code-block:: cpp
   :linenos:

   std::vector<int> scores{90, 75, 82};
   std::vector<int> best{std::move(scores)};

- Part (1): ``std::move(scores)`` refers to ``scores``, made in line 1.
- Part (2): ``std::move`` marks ``scores``, so another object may take its contents (`lvalue: Copied, Not Taken`_).
- Both hold, so in line 2, ``std::move(scores)`` is an xvalue.
- ``std::move`` only marks ``scores``: it moves nothing. ``best`` takes the three numbers when it is built from the xvalue, and ``scores`` is left empty (libstdc++, measured). ``702run week7_playground 26`` prints ``best.size(): 3, scores.size(): 0``.

See `Ways to Mark`_ under Further Reading.

Temporary Materialization
^^^^^^^^^^^^^^^^^^^^^^^^^

To read a member, there must be an object, so the compiler creates a **temporary** from the prvalue.

.. code-block:: cpp

   Obstacle make_obstacle(int id);   // returns by value

With the declaration above:

- ``make_obstacle(3)``: a prvalue. No object exists yet.
- ``make_obstacle(3).id``: an xvalue. ``.id`` needs an object, so a temporary is made; it exists before ``.id`` reads it, so part (1) holds.
- ``int id{make_obstacle(3).id}``: the temporary is created, read, and destroyed at the end of the full expression, after ``id`` has its value: 3.

.. note::

   C++20 **[conv.rval]** (7.3.4): "A prvalue of type T can be converted to an xvalue of type T." The standard's own example: ``int k = X().n``, "X() prvalue is converted to xvalue".

.. dropdown:: The Definition of ``make_obstacle`` by Value
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      Obstacle make_obstacle(int id) {
        return Obstacle{id};  // the other members take their defaults
      }

   - ``make_obstacle`` returns a new ``Obstacle`` by value. `Temporary Materialization`_ and `Exercise 2: Value Categories`_ use it.

``decltype``
^^^^^^^^^^^^

``decltype`` (short for *declared type*) yields the type of an expression ``e``, determined at compile time. The expression ``e`` is never evaluated, and the result can be used anywhere a type is expected.

.. code-block:: cpp
   :linenos:

   int count{3};
   const double limit{40.0};
   std::vector<Pose> path{make_path(3)};
   Pose& first{path[0]};
   auto copy{limit};            // double: auto drops const
   decltype(count) other{5};    // a new variable: an int, set to 5

With the declarations above:

- ``decltype(count)`` is ``int``, so line 6 declares ``other`` as an ``int``.
- ``decltype(limit)`` is ``const double``. Line 5's ``auto`` drops the ``const``; ``decltype`` keeps it.
- ``decltype(first)`` is ``Pose&``: it keeps the ``&`` too.
- ``decltype(path.size())`` is ``std::size_t`` (libstdc++). ``size()`` is not called.

.. note::

   C++20 **[dcl.type.decltype]** (9.2.8.4) paragraph 1: for a plain name, "decltype(E) is the type of the entity named by E". "The operand of the decltype specifier is an unevaluated operand".

``std::is_same_v``
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   #include <type_traits>

   static_assert(std::is_same_v<int, int>);         // the same type
   static_assert(!std::is_same_v<int, int&>);       // int& is another type
   static_assert(!std::is_same_v<int, const int>);  // const int is too

- ``std::is_same_v<A, B>`` is ``true`` when ``A`` and ``B`` are the same type, and ``false`` otherwise. An ``&`` or a ``const`` makes another type.
- ``static_assert`` (L2) stops the build when its condition is ``false``. ``!`` (not) turns ``false`` into ``true``, so all three lines compile.

.. note::

   C++20 **[meta.rel]** (20.15.6), Table 51, ``is_same``: "T and U name the same type with the same cv-qualifications". A cv-qualification is ``const`` or ``volatile``.

The ``decltype`` Test
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(3)};
   static_assert(std::is_same_v<decltype((path)),
                                std::vector<Pose>&>);       // lvalue
   static_assert(std::is_same_v<decltype((std::move(path))),
                                std::vector<Pose>&&>);      // xvalue
   static_assert(std::is_same_v<decltype((make_path(3))),
                                std::vector<Pose>>);        // prvalue

- Each ``static_assert`` compiles only if ``decltype((e))`` is the type written after it (`std::is_same_v`_).
- ``decltype((e))`` gives ``T&`` for an lvalue, ``T&&`` for an xvalue, and ``T`` for a prvalue. All three lines compile. The playground prints each category with this test.

.. note::

   ``T&&`` is an **rvalue reference**: a reference to an object whose contents may be taken (`Binding to rvalues`_). ``std::move(path)`` returns ``std::vector<Pose>&&``: that is its type. A call that returns an rvalue reference is an xvalue (**[basic.lval]** paragraph 4.1): that is its category. It marks ``path`` and moves nothing (`xvalue: Marked by std::move`_).

See `One Pair or Two Parentheses`_ under Further Reading.

Exercise 2: Value Categories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Obstacle& lookup(
       std::vector<Obstacle>& seen,
       int id);

   std::vector<Obstacle> seen{...};
   Obstacle* p{&seen[0]};
   int n{4};

.. code-block:: cpp

   seen                      // 1
   seen[1].pose              // 2
   p->pose.x                 // 3
   n * 2                     // 4
   lookup(seen, 1)           // 5
   make_path(n)              // 6
   std::move(seen[0])        // 7
   std::move(seen[0]).pose   // 8
   make_obstacle(n).speed    // 9
   ++n                       // 10

- Write lvalue, xvalue or prvalue for each line. Then check: ``702run week7_playground 32``.

.. dropdown:: Answers
   :class-container: sd-border-success

   An lvalue refers to an object that already exists, and nothing marks it (`lvalue: A Named Object`_).

   1. ``seen``: **lvalue**. The name ``seen`` refers to a vector that already exists.
   2. ``seen[1].pose``: **lvalue**. ``seen[1]`` refers to the second ``Obstacle`` object in ``seen``, and ``.pose`` to its ``pose`` member. Both already exist.
   3. ``p->pose.x``: **lvalue**. ``p->pose`` is ``(*p).pose``. ``*p`` is the ``Obstacle`` object ``p`` points at, ``seen[0]``, so the expression refers to its ``x``.
   4. ``n * 2``: **prvalue**. It computes 8 from the value of ``n``. No object held that 8 before (`prvalue: A Computed Value`_).
   5. ``lookup(seen, 1)``: **lvalue**, because of its return type, ``Obstacle&``: the call refers to an ``Obstacle`` object that is already in ``seen``. The ``&`` on the parameter plays no part.
   6. ``make_path(n)``: **prvalue**. ``make_path`` returns a ``std::vector<Pose>`` by value. A call that returns by value computes a value: no object exists yet (`prvalue: A Computed Value`_).
   7. ``std::move(seen[0])``: **xvalue**. It refers to ``seen[0]``, which already exists, and marks it: its return type is ``Obstacle&&`` (`xvalue: Marked by std::move`_).
   8. ``std::move(seen[0]).pose``: **xvalue**. A member of an xvalue is an xvalue: when the whole ``Obstacle`` object is marked, its ``pose`` is marked too.
   9. ``make_obstacle(n).speed``: **xvalue**. ``make_obstacle(n)`` is a prvalue. ``.speed`` needs an object, so a temporary is made, and its member is an xvalue (`Temporary Materialization`_).
   10. ``++n``: **lvalue**. Prefix ``++`` adds 1 to ``n``, and the result is ``n`` itself, now 5.

   .. note::

      C++20 **[expr.call]** (7.6.1.2) paragraph 14: "A function call is an lvalue if the result type is an lvalue reference type [...], an xvalue if the result type is an rvalue reference to object type, and a prvalue otherwise."

   .. note::

      C++20 **[basic.lval]** paragraph 4.4: an xvalue is "a class member access expression [...] in which the object expression is an xvalue". **[expr.pre.incr]** (7.6.2.2): "The result is the updated operand; it is an lvalue".

Binding to rvalues
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   std::vector<Pose>&& temp_ref{make_path(10)};       // OK: an rvalue
   const std::vector<Pose>& any_ref{path};            // lvalue or rvalue
   std::vector<Pose>&& lvalue_ref{path};              // does not compile

.. code-block:: text

   error: cannot bind rvalue reference of type 'std::vector<Pose>&&' to lvalue
   of type 'std::vector<Pose>'

- ``T&&`` is an **rvalue reference**. It binds only to rvalues: prvalues and xvalues.
- Bound to the prvalue ``make_path(10)``, ``temp_ref`` gets a temporary that lives as long as ``temp_ref``.
- ``const T&`` binds to lvalues and rvalues alike, but through it you cannot change the object, so you cannot take from it.

See `Category, Type and Lifetime`_ and `Giving It a Name`_ under Further Reading.

What Each Reference Refers To
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/av_binding.png
   :alt: In the middle, two name tags, each over a blue box with a stack icon and the word Stack holding three fields in rows, begin, end and capacity, each marked ptr: the upper one reads path, the lower one reads (temporary). On the right, one red box with a heap icon and the word Heap holds two blocks, each a column of cells with dots in it and a dashed empty slot under its last cell. The upper block, level with path, is measured as 1000 Pose, 24000 bytes; the lower one, level with the temporary, as 10 Pose, 240 bytes. From each Stack box, a blue arrow runs from begin to the block's first cell, and two blue arrows run from end and capacity to the dashed slot. On the left, three references, each a name tag with its type under it and a numbered tag beside it. Tag 2, any_ref, type const std::vector<Pose>&: a solid dark blue arrow runs from it to path's Stack box. Tag 3, lvalue_ref, type std::vector<Pose>&&: a gray dashed arrow runs from it to path's Stack box, crossed out by a circled X halfway along. Tag 1, temp_ref, type std::vector<Pose>&&: a solid dark blue arrow runs from it to the temporary's Stack box.
   :align: center
   :width: 100%

   The code of `Binding to rvalues`_, in memory: each reference, the object it refers to, and the block each vector owns on the heap.

- **1**, line 2: ``temp_ref`` binds the temporary from ``make_path(10)`` and keeps it alive, with its 10 poses (240 bytes) on the heap (C++20 **[class.temporary]** paragraph 6: the temporary "persists for the lifetime of the reference").
- **2**, line 3: ``any_ref``, a ``const&``, binds ``path``, an lvalue.
- **3**, line 4: a ``T&&`` cannot bind ``path``, an lvalue, so it does not compile. The figure draws it dashed and crossed out.
- A reference has no box and owns no block: each block on the heap belongs to a vector, 1000 poses (24000 bytes) for ``path``. C++20 **[dcl.ref]** paragraph 4: "It is unspecified whether or not a reference requires storage."

Overloads for Copy and Move
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> controller_path;  // what the controller follows

   void assign_path(const std::vector<Pose>& path) {        // 1
     controller_path = path;             // copy
   }
   void assign_path(std::vector<Pose>&& path) {             // 2
     controller_path = std::move(path);  // move
   }

   std::vector<Pose> path{make_path(1000)};
   std::vector<Pose>&& r{make_path(10)};
   assign_path(path);               // lvalue: 1, a copy
   assign_path(make_path(5));       // prvalue: 2, a move
   assign_path(r);                  // named T&&, an lvalue: 1, a copy
   assign_path(std::move(path));    // xvalue: 2, a move

- The compiler picks the overload from the argument's value category: an lvalue gets ``const&``, an rvalue gets ``&&``.
- ``std::vector`` itself has both: a copy constructor and a move constructor. That is how the compiler chose between the copy in `Inside a Copy`_ and the move in `Inside a Move`_.

See `Inside std::vector's Move and Copy`_ under Further Reading.

What ``std::move`` Does
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   std::move(path);                       // warns: result unused
   std::cout << path.size() << '\n';      // 1000: nothing moved

.. code-block:: text

   warning: ignoring return value of '... std::move(_Tp&&)
   [with _Tp = vector<Pose>&; ...]', declared with attribute 'nodiscard'
   [-Wunused-result]

- ``std::move`` moves nothing: it gives permission to move.
- ``std::move(path)`` is a cast to ``std::vector<Pose>&&``. Its result is an xvalue: it marks ``path`` as "may be taken".
- The move happens later, if a move constructor or a ``&&`` overload takes the result. Here nothing does.

.. note::

   Write ``std::move`` only where the object is handed on, and do not use the source again until you assign it. Rule: `Core Guidelines ES.56 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-move>`__.

See `The Definition of std::move`_ and `std::move on a const Object`_ under Further Reading.

Categories and References
^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Category
     - Refers to an object that already exists
     - May be taken
     - ``decltype((e))``
     - Example
   * - lvalue
     - yes
     - no
     - ``T&``
     - ``path``
   * - xvalue
     - yes
     - yes
     - ``T&&``
     - ``std::move(path)``
   * - prvalue
     - no
     - yes
     - ``T``
     - ``make_path(3)``

.. list-table::
   :header-rows: 1

   * - Reference
     - Binds to
     - What it means
   * - ``T&``
     - lvalues only
     - another name for an object that already exists
   * - ``const T&``
     - lvalues and rvalues
     - read-only, so a temporary may bind: no change to it can be lost
   * - ``T&&``
     - rvalues only: xvalues and prvalues
     - a function that takes one may take the contents

- ``std::move(x)`` is a cast to ``T&&``: an xvalue. It moves nothing (`What std::move Does`_).
- A named ``T&&`` is an lvalue (`Giving It a Name`_, under Further Reading).
- One ``const T&`` parameter called with each category: :ref:`l7-const-ref-binds`, under Further Reading.

Smart Pointers
--------------

A **smart pointer** is an object that points at one heap object. The owning ones delete the object when its last owner lets go.

Three class templates in ``<memory>``, one for each kind of ownership in `Who Owns Each Obstacle`_. C++20 lists all three under smart pointers (20.11).

.. figure:: /_static/images/l7/av_owner_map.png
   :alt: A UML object diagram in black and white: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner.
   :align: center
   :width: 80%

   Filled diamond: ``std::unique_ptr``. Open diamond: ``std::shared_ptr``. Arrow: ``std::weak_ptr``.

``std::unique_ptr``
^^^^^^^^^^^^^^^^^^^

A ``std::unique_ptr`` is the only owner of one object on the heap. It cannot be copied, only moved, and when it is destroyed it deletes the object.

.. figure:: /_static/images/l7/av_owner_map_unique.png
   :alt: A UML object diagram in black, with one part in orange: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner. In orange, with thick borders: tracker, the boxes with id 1, 3 and 4, and the three lines with filled diamonds.
   :align: center
   :width: 80%

   Orange, from the map in `Who Owns Each Obstacle`_: each filled diamond is one ``std::unique_ptr`` in the list ``tracker``. ``tracker`` is a ``std::vector<std::unique_ptr<Obstacle>>`` (`The Tracker's List`_): three pointers, each the only owner of one ``Obstacle`` object.

See `cppreference: std::unique_ptr <https://en.cppreference.com/w/cpp/memory/unique_ptr>`__. Rule: `Core Guidelines R.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-owner>`__.

.. _l7-unique-syntax:

The Syntax
""""""""""

.. code-block:: cpp

   #include <memory>

   std::unique_ptr<T> name{std::make_unique<T>(args)};  // 1
   auto name{std::make_unique<T>(args)};                // 2
   std::unique_ptr<T> name{new T(args)};                // 3

- ``T``: the type of the object on the heap. ``name``: the ``std::unique_ptr``'s name. ``args``: the values that initialize the object.
- 1 and 2 declare the same type: ``auto`` takes ``std::unique_ptr<T>`` from ``std::make_unique``. 3 compiles too, but you write ``new`` yourself: the rule in :ref:`l7-unique-creating-one` says to use 1 or 2.

.. code-block:: cpp

   auto count{std::make_unique<int>(10)};  // an int on the heap
   *count += 1;                            // as with an int*
   std::cout << *count << '\n';            // 11

.. _l7-unique-creating-one:

Creating One
""""""""""""

.. code-block:: cpp

   #include <memory>

   Pose parked_pose{20.0, -3.0, 0.0};  // from the table
   auto parked_car{std::make_unique<Obstacle>(1, parked_pose, 0.0, true)};
   std::cout << parked_car->id << ' ' << (*parked_car).speed << '\n';  // 1 0
   auto empty{std::make_unique<Obstacle>()};  // members take defaults
   std::cout << empty->id << ' ' << empty->speed << '\n';    // 0 0

- ``std::make_unique<T>(args)`` creates the object on the heap and returns the ``std::unique_ptr`` that owns it.
- The arguments go to the object, as with L6's ``emplace_back``.
- ``->`` and ``*`` work as they do on an ``Obstacle*``.
- No ``new``, and no ``delete``: ``parked_car`` deletes the ``Obstacle`` object when it goes out of scope.

.. note::

   "Use ``make_unique()`` to make ``unique_ptr``\ s". Rule: `Core Guidelines R.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_unique>`__.

See `A unique_ptr with Its Own Deleter`_ under Further Reading.

In Memory
"""""""""

.. figure:: /_static/images/l7/av_unique_ptr_memory.png
   :alt: On the left, a name tag reading parked_car over a blue box with a stack icon and the word Stack, holding one field, pointer, marked an Obstacle*. A measuring line under it reads 8 bytes. On the right, under a name tag reading Obstacle, a red box with a heap icon and the word Heap holds a block of four rows: id 1, pose {20.0, -3.0, 0.0}, speed 0.0, and is_static true. A blue arrow runs from the pointer field to the left edge of that block, at its first row, id. A measuring line under the block reads 48 bytes.
   :align: center
   :width: 100%

   A ``std::unique_ptr`` on the stack and the ``Obstacle`` object it owns on the heap.

- The ``std::unique_ptr`` is one pointer on the stack, the same 8 bytes as an ``Obstacle*``. The resource, the ``Obstacle`` object, is on the heap.
- Using a ``std::unique_ptr`` instead of an ``Obstacle*`` adds no bytes. It adds two rules: it deletes the ``Obstacle`` object when it is destroyed, and no other ``std::unique_ptr`` can own that object.

The Leak, Fixed
"""""""""""""""

**With a regular pointer**

.. code-block:: cpp

   bool needs_braking(int id) {
     Obstacle* track{make_track(
         id, Pose{20.0, -3.0}, 0.0)};
     if (track->pose.x > 10.0) {
       return false;  // leaks
     }
     delete track;
     return true;
   }

.. dropdown:: The Definition of ``make_track``, with ``new``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      Obstacle* make_track(int id, Pose pose, double speed) {
        return new Obstacle{id, pose, speed};
      }

   - `An Obstacle on the Heap`_'s ``make_track``: it creates the ``Obstacle`` object with ``new``, and the caller must ``delete`` it.
   - `The Leak, Fixed`_ and Further Reading's `Double Delete, Measured`_ and `Dangling Read, Measured`_ call it.

**With** ``std::unique_ptr``

.. code-block:: cpp

   bool needs_braking(int id) {
     auto track{std::make_unique<Obstacle>(
         id, Pose{20.0, -3.0}, 0.0)};
     if (track->pose.x > 10.0) {
       return false;  // deleted here
     }
     return true;     // and here
   }

- The first one leaks 48 bytes: the parked car is 20 m ahead, past the 10 m chosen for this example, so the early return skips the ``delete``.
- ``702run week7_playground 44`` runs the second one: ``needs_braking(1): false``, and no LeakSanitizer report.
- Every path out of the function destroys ``track``, and its destructor deletes the ``Obstacle`` object.

One Owner Only
""""""""""""""

.. code-block:: cpp

   auto track{std::make_unique<Obstacle>()};
   std::unique_ptr<Obstacle> copy{track};  // does not compile

.. code-block:: text

   error: use of deleted function 'std::unique_ptr<_Tp, _Dp>::unique_ptr(const
   std::unique_ptr<_Tp, _Dp>&) [with _Tp = Obstacle;
   _Dp = std::default_delete<Obstacle>]'

- A **deleted function** is declared with ``= delete``: any call to it is a compile error. A **deleter** is what a ``std::unique_ptr`` calls to give its object back.
- The copy constructor is deleted, so a copy does not compile.
- Two owners of one ``Obstacle`` object would both delete it: the double ``delete`` of `Double Delete, Measured`_ (Further Reading). The type rules it out at compile time.
- ``_Dp = std::default_delete<Obstacle>`` is the deleter; it calls ``delete``.

See `std::auto_ptr`_ under Further Reading.

``get``
"""""""

.. code-block:: cpp

   void print_obstacle(const Obstacle* target);  // only looks

   auto parked_car{
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0, 0.0}, 0.0, true)};
   print_obstacle(parked_car.get());  // parked_car still owns it

.. dropdown:: The Definition of ``print_obstacle``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      void print_obstacle(const Obstacle* target) {  // only looks
        std::cout << "  obstacle " << target->id << ": " << target->speed << " m/s\n";
      }

- ``get()`` returns the plain pointer, an ``Obstacle*``. It does not give up ownership: ``parked_car`` still deletes the ``Obstacle`` object when it goes out of scope.
- The code that receives the pointer only looks. It must not ``delete`` it: ``parked_car`` would delete the object a second time (`Double Delete, Measured`_, under Further Reading).

.. note::

   C++20 **[unique.ptr.single.observers]** (20.11.1.2.4) paragraph 6, ``get()``: "Returns: The stored pointer."

``release``
"""""""""""

.. code-block:: cpp

   auto parked_car{
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0, 0.0}, 0.0, true)};
   Obstacle* raw{parked_car.release()};  // gives up ownership
   // parked_car == nullptr: true, raw->id: 1
   delete raw;  // you are the owner now: leave this out and it leaks

- ``release()`` hands the ``Obstacle`` object back as a plain pointer and forgets it.
- You are back where `An Obstacle on the Heap`_ started: an ``Obstacle*`` that must be deleted exactly once.
- Use it only to hand the object to code that takes ownership of a plain pointer. Otherwise, move the ``std::unique_ptr``.

.. note::

   C++20 **[unique.ptr.single.modifiers]** (20.11.1.2.5) paragraphs 1 and 2: "Postconditions: get() == nullptr." "Returns: The value get() had at the start of the call to release."

.. figure:: /_static/images/l7/av_unique_ptr_release.png
   :alt: Three panels separated by thin lines, tagged 1 to 3. Each has, at the top, name tags over blue boxes with a stack icon and the word Stack, each holding one field, pointer, and below them a red box with a heap icon and the word Heap. Panel 1: only parked_car, its pointer marked an Obstacle*; a solid blue arrow runs from it straight down to the top edge of an object in the Heap box with four rows: id 1, pose {20.0, -3.0, 0.0}, speed 0.0, is_static true. Panel 2: parked_car's pointer is marked nullptr, with no arrow; beside it, raw's pointer is marked an Obstacle*, and a dashed blue arrow runs from it straight down to the same object. Panel 3: parked_car's pointer is marked nullptr and raw's is marked dangling, with no arrows; in the Heap box the same place is a gray dashed block labeled freed: 48 bytes.
   :align: center
   :width: 100%

   ``parked_car`` and ``raw`` after each statement of the code above.

- **1** to **3**: after each of the three statements.
- **2**: ``raw`` is a plain pointer (dashed): nothing deletes the object now unless the code does.
- **3**: ``delete raw`` frees the 48 bytes, and ``raw`` still holds the old address: it dangles.

``reset``
"""""""""

.. code-block:: cpp
   :linenos:

   auto parked_car{
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0, 0.0}, 0.0, true)};
   parked_car.reset();           // deletes it now: parked_car == nullptr
   parked_car =
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0, 0.0}, 0.0, true);

- ``reset()`` deletes the ``Obstacle`` object now, without waiting for the end of the scope. ``reset(p)`` stores ``p``, then deletes the old object, if there was one.
- Assigning a new ``std::unique_ptr`` stores the new object's address, then deletes the old object, as ``reset`` does.

.. note::

   C++20 **[unique.ptr.single.modifiers]** (20.11.1.2.5) paragraph 4, ``reset(p)``: "Assigns p to the stored pointer, and then if and only if the old value of the stored pointer, old_p, was not equal to nullptr, calls get_deleter()(old_p)."

.. figure:: /_static/images/l7/av_unique_ptr_reset.png
   :alt: Three panels separated by thin lines, tagged 1 to 3. Each has, at the top, a blue box with a stack icon and the word Stack under a name tag reading parked_car, holding one field, pointer, and below it a red box with a heap icon and the word Heap. Panel 1: the pointer is marked an Obstacle*, and a blue arrow runs from it down to the top edge of an object in the Heap box with four rows: id 1, pose {20.0, -3.0, 0.0}, speed 0.0, is_static true. Panel 2: the pointer is marked nullptr, with no arrow, and in the Heap box the same place is a gray dashed block labeled freed: 48 bytes. Panel 3: the pointer is marked an Obstacle*, and a blue arrow runs from it down to an object in the same place with the same four rows: id 1, pose {20.0, -3.0, 0.0}, speed 0.0, is_static true.
   :align: center
   :width: 100%

   ``parked_car`` after each statement of the code above.

- **1** to **3**: after each of the three statements.
- **2**: ``reset()`` deletes the ``Obstacle`` object with id 1 and frees its 48 bytes. ``parked_car`` holds ``nullptr``.
- **3**: the last statement makes a new ``Obstacle`` object for the parked car, seen again. It may get the freed bytes: with g++ 13.3 it lands at the old address, and under AddressSanitizer it does not (measured).

See `swap`_ under Further Reading.

Moving Ownership
""""""""""""""""

.. code-block:: cpp
   :linenos:

   auto parked_car{
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0, 0.0}, 0.0, true)};
   Obstacle* where{parked_car.get()};
   std::unique_ptr<Obstacle> other{std::move(parked_car)};

- Line 3: ``where`` only points at the ``Obstacle`` object; ``parked_car`` still owns it.
- Line 4, the move constructor (`Inside a Move`_): ``other`` takes the pointer, and ``parked_car`` is left empty. ``other.get() == where``: the ``Obstacle`` object did not move.
- Unlike a moved-from ``std::vector``, a moved-from ``std::unique_ptr`` is guaranteed to be empty.

.. note::

   C++20 **[unique.ptr.single.ctor]** (20.11.1.2.1) paragraph 20, for ``unique_ptr(unique_ptr&& u)``: "Postconditions: get() yields the value u.get() yielded before the construction. u.get() == nullptr."

See `Testing for Empty`_ under Further Reading.

Step 1: Before the Move
"""""""""""""""""""""""

.. figure:: /_static/images/l7/av_unique_ptr_move_1.png
   :alt: Two name tags, parked_car and where, each over a blue box with a stack icon and the word Stack holding one field, pointer, marked an Obstacle*. On the right, under a name tag reading Obstacle, a red box with a heap icon and the word Heap holds one object of four rows: id 1, pose {20.0, -3.0, 0.0}, speed 0.0, and is_static true. A solid blue arrow runs from parked_car's pointer to the left edge of the object, at its first row, id. A dashed blue arrow runs from where's pointer to the same row, just below the solid arrow.
   :align: center
   :width: 100%

- After line 3 of `Moving Ownership`_: ``parked_car`` owns the ``Obstacle`` object (solid arrow).
- ``where`` holds the same address (dashed arrow), but an ``Obstacle*`` owns nothing: it never deletes the object.
- Both arrows end at ``id``: the object's address is where it starts, at its first member.

Step 2: After the Move
""""""""""""""""""""""

.. figure:: /_static/images/l7/av_unique_ptr_move_2.png
   :alt: Three name tags, parked_car, where and other, each over a blue box with a stack icon and the word Stack holding one field, pointer: parked_car's is marked nullptr, with no arrow; where's and other's are marked an Obstacle*. On the right, under a name tag reading Obstacle, a red box with a heap icon and the word Heap holds the same object as before, four rows: id 1, pose {20.0, -3.0, 0.0}, speed 0.0, and is_static true. A dashed blue arrow runs from where's pointer to the left edge of the object, at its first row, id. A solid blue arrow runs from other's pointer to the same row, just below the dashed arrow.
   :align: center
   :width: 100%

- After line 4: ``other`` owns the ``Obstacle`` object, and ``parked_car`` holds ``nullptr``.
- ``where`` still holds the same address: the object did not move.
- ``parked_car`` points at nothing, so it deletes nothing when it goes out of scope.

Exercise 3: Handing Over a Track
""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   auto p{std::make_unique<Obstacle>(1)};
   auto q{std::move(p)};
   p = std::make_unique<Obstacle>(3);
   q = std::move(p);

- At the board, after each line: draw ``p`` and ``q`` on the stack, every ``Obstacle`` object on the heap, and an arrow from each pointer to the object it owns.
- On which line is the ``Obstacle`` object with id 1 deleted, and what deletes it? Nothing in the code says ``delete``.
- Check: ``702run week7_playground 54``.

.. dropdown:: Answers
   :class-container: sd-border-success

   .. figure:: /_static/images/l7/av_handover_states.png
      :alt: Four panels in a 2 by 2 grid, tagged 1 to 4. Each has, on the left, name tags p and q, each over a blue box with a stack icon and the word Stack holding one field, pointer, and on the right a red box with a heap icon and the word Heap. An Obstacle object is drawn with four rows: id, pose {0.0, 0.0, 0.0}, speed 0.0, is_static false. Panel 1: only p, its pointer marked an Obstacle*, with a blue arrow to the object with id 1. Panel 2: p's pointer is marked nullptr, with no arrow; q's, marked an Obstacle*, has a blue arrow to the object with id 1. Panel 3: p has a blue arrow to a new object with id 3, drawn above the object with id 1; q still has its arrow to the object with id 1. Panel 4: p's pointer is marked nullptr; q has a blue arrow to the object with id 3; where the object with id 1 was, a gray dashed block reads id 1: freed, 48 bytes.
      :align: center
      :width: 100%

      ``p`` and ``q`` after each line.

   - **1** to **4**: after lines 1 to 4.
   - Line 4 deletes the ``Obstacle`` object with id 1: the move assignment gives ``q`` the new pointer, then deletes the object ``q`` owned before.

The Tracker's List
""""""""""""""""""

.. code-block:: cpp

   std::vector<std::unique_ptr<Obstacle>> tracker;
   tracker.push_back(std::make_unique<Obstacle>(2, Pose{12.0, -1.0}, 4.0));
   auto parked_car{
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0}, 0.0, true)};
   tracker.push_back(std::move(parked_car));  // parked_car is now empty
   // tracker.push_back(parked_car);     // does not compile: a copy
   for (const auto& t : tracker) {       // a copy would not compile
     std::cout << "obstacle " << t->id << ": " << t->speed << " m/s\n";
   }

- The tracker: the vector owns the pointers, and each pointer owns its ``Obstacle`` object. When ``tracker`` is destroyed, every ``Obstacle`` object is deleted.
- A temporary moves in by itself; a named ``parked_car`` needs ``std::move``. ``Pose{20.0, -3.0}``: ``heading`` takes its default, 0.
- Copying the whole vector does not compile either.

.. figure:: /_static/images/l7/av_tracker_list.png
   :alt: On the left, two name tags over blue boxes with a stack icon and the word Stack. The upper one, tracker, holds three fields in rows, begin, end and capacity, each marked ptr. The lower one, parked_car, holds one field, pointer, marked nullptr, with no arrow. On the right, a red box with a heap icon and the word Heap holds tracker's block: two slots, [0] and [1], each marked ptr, with a dashed empty slot under them and the label 2 slots, 16 bytes. Blue arrows run from tracker's begin to slot [0], and from end and capacity to the dashed slot. Further right, two objects with four rows each: id 2, pose {12.0, -1.0, 0.0}, speed 4.0, is_static false; and below it id 1, pose {20.0, -3.0, 0.0}, speed 0.0, is_static true. A solid blue arrow runs from slot [0] to the object with id 2, and one from slot [1] to the object with id 1.
   :align: center
   :width: 100%

   The tracker's list in memory, after the code above.

- ``tracker``'s block holds two ``std::unique_ptr`` slots, 8 bytes each (measured).
- Each slot is the only owner of one ``Obstacle`` object. ``parked_car`` handed its pointer to slot ``[1]`` and holds ``nullptr``.
- Destroying ``tracker`` destroys both slots; each deletes its ``Obstacle`` object.

See `unique_ptr to an Array`_ under Further Reading.

.. _l7-unique-borrow:

Passing and Returning
"""""""""""""""""""""

Required reading: the four sections in the table, under Further Reading, show how a function takes or gives back a ``std::unique_ptr``. Exercise 4 uses them.

.. list-table::
   :header-rows: 1

   * - The function...
     - Parameter or return type
     - Rule
     - Further Reading
   * - only uses the object
     - ``const T&`` or ``T*``
     - R.30
     - :ref:`Borrow <l7-app-unique-borrow>`
   * - takes ownership (a sink), by value
     - ``std::unique_ptr<T>``
     - R.32
     - :ref:`Sink <l7-app-unique-sink>`
   * - may replace the object (reseat)
     - ``std::unique_ptr<T>&``
     - R.33
     - :ref:`Reseat <l7-app-unique-reseat>`
   * - creates the object, returns it by value
     - ``std::unique_ptr<T>``
     - 
     - :ref:`Returning <l7-unique-returning>`

Exercise 4: Lines That Compile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void inspect(const Obstacle& target);
   void adopt(std::unique_ptr<Obstacle> track);

   auto a{std::make_unique<Obstacle>(1)};
   auto b{std::make_unique<Obstacle>(3)};
   auto c{a};                                    // 1
   auto d{std::move(a)};                         // 2
   inspect(*d);                                  // 3
   adopt(b);                                     // 4
   adopt(std::move(b));                          // 5
   std::unique_ptr<Obstacle> e{new Obstacle{}};  // 6
   Obstacle* f{d.get()};                         // 7
   std::unique_ptr<Obstacle> g{f};               // 8

- For each line: does it compile? If it compiles, is it correct? Then check in ``702run week7_playground 58`` and its comments.

.. dropdown:: Answers
   :class-container: sd-border-success

   A ``std::unique_ptr`` cannot be copied: its copy constructor is deleted.

   1. ``auto c{a};``: **does not compile**. It would copy ``a``, and then two owners would both delete the ``Obstacle`` object with id 1.
   2. ``auto d{std::move(a)};``: **compiles, correct**. ``d`` now owns the object with id 1, and ``a`` is empty.
   3. ``inspect(*d);``: **compiles, correct**. ``inspect`` only reads the object, through a ``const Obstacle&`` (:ref:`Borrow <l7-app-unique-borrow>`, under Further Reading). ``d`` still owns it.
   4. ``adopt(b);``: **does not compile**. ``adopt`` takes its parameter by value, so the parameter would be a copy of ``b``.
   5. ``adopt(std::move(b));``: **compiles, correct**. The parameter is moved from ``b``: ``adopt`` is a sink (:ref:`Sink <l7-app-unique-sink>`, under Further Reading). It owns the object with id 3 and deletes it when the parameter is destroyed. ``b`` is empty.
   6. ``std::unique_ptr<Obstacle> e{new Obstacle{}};``: **compiles, correct**. ``e`` owns the new object. R.23 asks for ``std::make_unique<Obstacle>()`` instead, so the code has no ``new``.
   7. ``Obstacle* f{d.get()};``: **compiles, correct**. ``f`` points at the object with id 1 but does not own it. ``d`` still deletes it.
   8. ``std::unique_ptr<Obstacle> g{f};``: **compiles, wrong**. ``g`` and ``d`` both own the object with id 1, and both delete it. AddressSanitizer reports it:

   .. code-block:: text

      ERROR: AddressSanitizer: attempting double-free on 0x504000000010 in thread T0:

``std::shared_ptr``
^^^^^^^^^^^^^^^^^^^

A ``std::shared_ptr`` is one of several owners of an object on the heap. The owners share a count, and the last one to let go deletes the object.

.. figure:: /_static/images/l7/av_owner_map_shared.png
   :alt: A UML object diagram in black, with one part in orange: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner. In orange, with thick borders: tracker, the box with id 2, planner, and the two lines with open diamonds.
   :align: center
   :width: 80%

   Orange, from the map in `Who Owns Each Obstacle`_: the open diamonds, several owners. In the code, the planner's list is ``hazards``.

See `cppreference: std::shared_ptr <https://en.cppreference.com/w/cpp/memory/shared_ptr>`__. Rule: `Core Guidelines R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`__.

A Hazard in Two Lists
"""""""""""""""""""""

The planner puts the cyclist, id 2, in its hazard list; the tracker keeps it too. Three ways to hold it, all wrong:

1. **A second** ``std::unique_ptr``: does not compile. One owner only (`One Owner Only`_).
2. **A copy of the** ``Obstacle``: two objects. The tracker's speed updates never reach the planner's copy.
3. **An** ``Obstacle*`` **from** ``get()``: the hazard list does not own it. When the track is lost, it points at freed memory (`Dangling Read, Measured`_, Further Reading).

.. code-block:: cpp

   std::vector<std::unique_ptr<Obstacle>> tracker;  // as on slide 58
   std::vector<Obstacle*> hazards;
   hazards.push_back(tracker[0].get());  // id 2: looks, does not own
   tracker.erase(tracker.begin());       // the track is lost: it dangles

The ``tracker`` here is the one from `The Tracker's List`_.

.. note::

   Both lists must own the ``Obstacle`` object with id 2, and it must be deleted when the last of them lets go.

.. _l7-shared-syntax:

The Syntax
""""""""""

.. code-block:: cpp

   #include <memory>

   std::shared_ptr<T> name{std::make_shared<T>(args)};  // 1
   auto name{std::make_shared<T>(args)};                // 2
   std::shared_ptr<T> name{new T(args)};                // 3
   std::shared_ptr<T> other{name};                      // 4

- ``T``, ``name`` and ``args`` as for ``std::unique_ptr`` (:ref:`l7-unique-syntax`). 1 and 2 declare the same type. 3 compiles, but you write ``new`` yourself, and it makes two allocations (`One Allocation with make_shared`_, under Further Reading).
- 4: unlike a ``std::unique_ptr``, a ``std::shared_ptr`` can be copied. ``other`` is a second owner of the same object.

.. code-block:: cpp

   auto count{std::make_shared<int>(10)};  // an int on the heap
   auto other{count};                      // a copy: a second owner
   *other += 1;                            // through either owner
   std::cout << *count << '\n';            // 11: the same int

.. _l7-shared-creating-one:

Creating One
""""""""""""

.. code-block:: cpp

   std::vector<std::shared_ptr<Obstacle>> tracker;
   std::vector<std::shared_ptr<Obstacle>> hazards;
   auto hazard{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   tracker.push_back(hazard);  // a copy: one more owner
   hazards.push_back(hazard);  // a copy: one more owner

- A ``std::shared_ptr`` can be copied. Every copy is one more owner of the same ``Obstacle`` object, and ``use_count()`` counts them: 3, ``hazard``, ``tracker[0]`` and ``hazards[0]``.
- All three point at one ``Obstacle`` object: when the tracker updates its speed, the planner reads the new speed.

.. note::

   "Use ``make_shared()`` to make ``shared_ptr``\ s". Rule: `Core Guidelines R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`__.

The Control Block
"""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_memory.png
   :alt: On the left, two blue Stack boxes under name tags cyclist and hazard, each holding two fields, object and control, each marked (ptr), with a measuring line of 16 bytes under each box. On the right, a red Heap box holds one allocation, with a measuring line reading one allocation, 64 bytes: at the top a control block with use_count 2 and weak_ptrs 0, then right below it the Obstacle object with id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. Green arrows run from each object field to the first row of the Obstacle object, id, and from each control field to the first row of the control block.
   :align: center
   :width: 100%

   Two ``std::shared_ptr``\ s, one allocation: the control block first, then the ``Obstacle`` object.

- A **control block** is the block a ``std::shared_ptr`` keeps beside its object: it holds the count of owners.
- A ``std::shared_ptr`` is two pointers, 16 bytes: ``object`` and ``control``.
- A copy adds 1 to the count; destroying a ``std::shared_ptr`` subtracts 1.
- ``weak_ptrs``: the ``std::weak_ptr``\ s watching (`std::weak_ptr`_); 0 here.

See `One Allocation with make_shared`_ under Further Reading.

``use_count``
"""""""""""""

.. code-block:: cpp

   auto cyclist{std::make_shared<Obstacle>(2)};
   std::cout << cyclist.use_count() << '\n';             // 1
   std::shared_ptr<Obstacle> hazard{cyclist};            // a copy
   std::cout << cyclist.use_count() << '\n';             // 2
   std::shared_ptr<Obstacle> moved{std::move(hazard)};   // a move
   std::cout << cyclist.use_count() << '\n';             // 2
   moved.reset();
   std::cout << cyclist.use_count() << '\n';             // 1

- ``use_count()`` returns how many ``std::shared_ptr`` objects own the object. Each line asks ``cyclist``, one of the owners.
- A move hands one owner's place to another: the count stays at 2, and ``hazard`` is left empty.
- ``reset()`` gives up this owner's place. The ``Obstacle`` object is deleted only when the count reaches 0.
- Check: ``702run week7_playground 64``.

Three Ways to Let Go
""""""""""""""""""""

.. code-block:: cpp

   auto cyclist{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   {
     std::shared_ptr<Obstacle> hazard{cyclist};  // 1: count 2
   }                                             // 2: count 1

   // Three separate runs, each from 2:
   cyclist = std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0);  // 3a
   cyclist.reset();                                                 // 3b
   // 3c: cyclist's scope ends

- An owner lets go when its scope ends (2, 3c), when it is assigned another pointer (3a), or when it calls ``reset()`` (3b). Each one subtracts 1 from the count.
- In all three, ``cyclist`` is the last owner, so its ``Obstacle`` object is deleted: ``=`` and ``reset()`` swap it into a temporary that is destroyed (C++20 20.11.3.2 to 20.11.3.4).
- In 3a, the tracker sees the cyclist again: a new ``Obstacle`` object. Run it: ``702run week7_playground 65``.

Step 1: Two Owners
""""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_1.png
   :alt: On the left, two blue Stack boxes under name tags cyclist and hazard, each holding two fields, object and control, each marked (ptr). On the right, a red Heap box holds one allocation, measured as 64 bytes: at the top a control block with use_count 2 and weak_ptrs 0, then right below it an Obstacle object with id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. Green arrows run from each object field to the first row of the Obstacle object, id, and from each control field to the first row of the control block.
   :align: center
   :width: 100%

- After step 1 of `Three Ways to Let Go`_: ``hazard`` copies ``cyclist``. Both hold the same two pointers, so ``use_count`` is 2.
- Each green arrow is one pointer of a ``std::shared_ptr``: ``object`` ends at the object's first member, ``control`` at the control block.

Step 2: One Owner
"""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_2.png
   :alt: On the left, a blue Stack box under the name tag cyclist holds two fields, object and control, each marked (ptr). Below it, hazard is gray and dashed, marked scope ended, with no arrows. On the right, a red Heap box holds one allocation, measured as 64 bytes: a control block with use_count 1 and weak_ptrs 0, then the Obstacle object with id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. Green arrows run from cyclist's object field to the object's first row, id, and from its control field to the control block's first row.
   :align: center
   :width: 100%

- Step 2: ``hazard``'s scope ends. Its destructor subtracts 1, so ``use_count`` is 1.
- ``cyclist`` still owns the ``Obstacle`` object, so nothing is freed.

Step 3a: A New Object
"""""""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_3.png
   :alt: On the left, a blue Stack box under the name tag cyclist holds two fields, object and control, each marked (ptr). Below it, hazard is gray and dashed, marked scope ended. On the right, a red Heap box holds a new allocation, measured as 64 bytes: a control block with use_count 1 and weak_ptrs 0, then a new Obstacle object for the cyclist, seen again: id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. To its right, a gray dashed block marked freed: 64 bytes, the first control block and object. Green arrows run from cyclist's object field to the new object's first row, id, and from its control field to the new control block's first row.
   :align: center
   :width: 100%

- 3a, 3b and 3c are separate runs, each from step 2.
- 3a: ``std::make_shared`` makes a second allocation, for the cyclist seen again. ``cyclist`` lets go of the first: its count drops to 0, so its object is destroyed and its 64 bytes freed.

Step 3b: reset()
""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_4.png
   :alt: On the left, a blue Stack box under the name tag cyclist holds two fields, object and control, each marked nullptr, with no arrows. Below it, hazard is gray and dashed, marked scope ended. On the right, a red Heap box holds one gray dashed block marked freed: 64 bytes, the control block and object.
   :align: center
   :width: 100%

- 3b: ``cyclist.reset()`` leaves both of ``cyclist``'s pointers ``nullptr``.
- ``cyclist`` was the last owner, so the count drops to 0: the object is destroyed and the allocation freed.

Step 3c: The Scope Ends
"""""""""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_5.png
   :alt: On the left, cyclist and hazard are both gray and dashed, marked scope ended, with no arrows. On the right, a red Heap box holds one gray dashed block marked freed: 64 bytes, the control block and object.
   :align: center
   :width: 100%

- 3c: ``cyclist``'s scope ends, and its destructor runs.
- ``cyclist`` was the last owner, so the count drops to 0: the object is destroyed and the allocation freed.

Deletion by the Last Owner
""""""""""""""""""""""""""

.. code-block:: cpp

   tracker.push_back(std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0));
   hazards.push_back(tracker[0]);  // count 2
   tracker.clear();  // count 1: the planner still owns it
   hazards.clear();  // the last owner deletes the Obstacle

- The hazard list keeps the ``Obstacle`` object alive after the tracker lets go. That is what the raw pointer of `A Hazard in Two Lists`_ could not do.
- Whichever list lets go last deletes the ``Obstacle`` object, and nothing leaks: ``702run week7_playground 71`` ends with no LeakSanitizer report.

Passing and Returning
"""""""""""""""""""""

Required reading: the four sections in the table, under Further Reading, show how a function takes or gives back a ``std::shared_ptr``.

.. list-table::
   :header-rows: 1

   * - The function...
     - Parameter or return type
     - Rule
     - Further Reading
   * - only uses the object
     - ``const T&``
     - R.30
     - :ref:`Borrow <l7-shared-borrow>`
   * - becomes one more owner, by value
     - ``std::shared_ptr<T>``
     - R.34
     - :ref:`Share <l7-app-shared-share>`
   * - might keep the object
     - ``const std::shared_ptr<T>&``
     - R.36
     - :ref:`const& <l7-app-shared-const-ref>`
   * - creates the object, returns it; the caller converts it
     - ``std::unique_ptr<T>``
     - 
     - :ref:`Returning <l7-shared-returning>`

``std::weak_ptr``
^^^^^^^^^^^^^^^^^

A ``std::weak_ptr`` watches an object that ``std::shared_ptr``\ s own. It never keeps the object alive, and it can tell whether the object still exists.

.. figure:: /_static/images/l7/av_owner_map_weak.png
   :alt: A UML object diagram in black, with one part in orange: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner. In orange, with thick borders: the box with id 2, dashboard, and the arrow from dashboard.
   :align: center
   :width: 80%

   Orange, from the map in `Who Owns Each Obstacle`_: the arrow, a look without owning.

See `cppreference: std::weak_ptr <https://en.cppreference.com/w/cpp/memory/weak_ptr>`__. Rule: `Core Guidelines R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`__.

.. _l7-weak-syntax:

The Syntax
""""""""""

.. code-block:: cpp

   #include <memory>

   std::weak_ptr<T> name{owner};  // 1
   std::weak_ptr<T> name;         // 2
   name = owner;                  // 3
   auto locked{name.lock()};      // 4

- ``owner`` is a ``std::shared_ptr<T>``. 1 and 3 watch its object; 2 watches nothing. There is no ``make_weak``.
- 4: no ``*`` and no ``->``. ``lock()`` returns a ``std::shared_ptr<T>`` that owns the object while you use it, or an empty one if it is gone (`lock`_).
- Two uses: a watcher that must not keep the object alive (the dashboard in `Who Owns Each Obstacle`_), and breaking a cycle of owners (`Cyclic Reference`_).

.. code-block:: cpp

   auto cyclist{std::make_shared<Obstacle>(2)};
   std::weak_ptr<Obstacle> shown{cyclist};    // adds no owner
   std::cout << cyclist.use_count() << '\n';  // 1

Cyclic Reference
""""""""""""""""

Two more obstacles ahead in the ego lane: a tractor, id 5, at 60 m, towing a trailer, id 6, at 54 m, both at 8 m/s (chosen for this example).

.. figure:: /_static/images/l7/av_road_towing.png
   :alt: A top view of a straight two-lane road, drawn to scale, with an x axis along the bottom marked 0 to 60 meters every 10 meters and a y axis on the left marked 0.0 and 3.5 meters at the two lane centers. From the bottom up: a lighter parking strip, the lane of the ego vehicle, a dashed yellow center line, and the oncoming lane. The ego vehicle, a blue car tagged E, sits at x 0 in the center of its lane, facing plus x, with a white arrow pointing in plus x. Tag 1: an amber car parked in the parking strip at x 20. Tag 2: a green cyclist at x 12 near the right edge of the ego lane, with an arrow in plus x. Tag 3: a gray circle, the pedestrian, at x 30 in the oncoming lane, with an arrow pointing up. Tag 4, to the right of it: a coral red car at x 38 in the oncoming lane, facing minus x, with an arrow in minus x. Ahead in the ego lane, centered in it: tag 6, a light purple trailer, a long rectangle from about x 50 to 57 with a wheel on each side, joined by a short dark bar to tag 5, a purple tractor from x 58 to 62 with two large rear wheels and two small front wheels, facing plus x, with a white arrow pointing in plus x. Tag 5 sits just above the tractor, and tag 6 on the trailer.
   :align: center
   :width: 100%

   The road, with the tractor (5) towing the trailer (6) in the ego lane.

.. code-block:: cpp

   struct Towing { Obstacle obstacle;
                   std::shared_ptr<Towing> other; };
   auto a{std::make_shared<Towing>(Obstacle{5, {60.0, 0.0}, 8.0})};
   auto b{std::make_shared<Towing>(Obstacle{6, {54.0, 0.0}, 8.0})};
   a->other = b;  // a's Towing owns b's
   b->other = a;  // b's Towing owns a's

- ``a->other = b``: the ``Towing`` object that ``a`` owns becomes an owner of the one ``b`` owns. ``b->other = a`` does the reverse.

Step 1: Two Owners Each
"""""""""""""""""""""""

.. figure:: /_static/images/l7/av_cycle_1.png
   :alt: Two blue Stack boxes at the top, under name tags a and b, each holding two fields side by side, object and control, each marked (ptr). Below, one red Heap box holds two allocations side by side: each a control block with use_count 2 and weak_ptrs 0, then a Towing object with rows obstacle.id, obstacle.pose, obstacle.speed, obstacle.is_static, other: object and other: control. The left Towing holds 5, {60.0, 0.0, 0.0}, 8.0, false; the right one 6, {54.0, 0.0, 0.0}, 8.0, false. Green arrows run from a's fields to the left allocation, entering from the left: object to the Towing object's first row, control to the control block's first row. Green arrows run from b's fields to the right allocation, entering from the right. The left Towing's other rows send green arrows to the right allocation's Towing first row and control block, and the right Towing's other rows send green arrows to the left allocation's, so the arrows cross between the two allocations.
   :align: center
   :width: 100%

- While ``a`` and ``b`` exist, each ``Towing`` object has two owners: a variable on the stack and the other ``Towing``'s ``other``. Each count is 2.

Step 2: Neither Is Deleted
""""""""""""""""""""""""""

.. figure:: /_static/images/l7/av_cycle_2.png
   :alt: At the top, a and b are gray and dashed, marked scope ended, with no arrows. Below, one red Heap box holds two allocations side by side: each a control block with use_count 1 and weak_ptrs 0, then a Towing object with rows obstacle.id, obstacle.pose, obstacle.speed, obstacle.is_static, other: object and other: control. The left Towing holds 5, {60.0, 0.0, 0.0}, 8.0, false; the right one 6, {54.0, 0.0, 0.0}, 8.0, false. The left Towing's other rows send green arrows to the right allocation's Towing first row and control block, and the right Towing's other rows send green arrows to the left allocation's, so each allocation is still owned by the other.
   :align: center
   :width: 100%

- ``a`` and ``b`` are destroyed when their scope ends: each count drops to 1, never 0.
- Each ``Towing`` object keeps the other alive: 2 × 80 bytes leak (`Cyclic Reference, Measured`_).

Cyclic Reference, Measured
""""""""""""""""""""""""""

.. code-block:: text

   a.use_count(): 2, b.use_count(): 2

   ==143323==ERROR: LeakSanitizer: detected memory leaks

   Indirect leak of 80 byte(s) in 1 object(s) allocated from:
       #0 0x749b09afe548 in operator new(unsigned long)
       ...
       #9 0x608b6a9fd7cc in undefined::shared_cycle::run() .../undefined.cpp:38
   Indirect leak of 80 byte(s) in 1 object(s) allocated from:
       ...
       #9 0x608b6a9fd5f2 in undefined::shared_cycle::run() .../undefined.cpp:37

   SUMMARY: AddressSanitizer: 160 byte(s) leaked in 2 allocation(s).

- An **indirect leak** is LeakSanitizer's name for leaked memory reachable only from other leaked memory.
- ``702run week7_playground 78``: lines 37 and 38 are the two ``std::make_shared`` calls.
- 80 bytes each, one allocation: a ``Towing`` (48 + 16) and its 16-byte control block.

Breaking It
"""""""""""

.. code-block:: cpp

   struct Towing {
     Obstacle obstacle;
     std::weak_ptr<Towing> other;  // watches, does not own
   };
   a->other = b;  // b's count stays 1
   b->other = a;  // a's count stays 1

- A ``std::weak_ptr`` made from a ``std::shared_ptr`` does not add to the count.
- When ``a`` and ``b`` go out of scope, both counts reach 0 and both ``Towing`` objects are deleted. ``702run week7_playground 79``: no LeakSanitizer report.

.. note::

   "Use ``std::weak_ptr`` to break cycles of ``shared_ptr``\ s". Rule: `Core Guidelines R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`__.

``lock``
""""""""

.. code-block:: cpp

   struct Dashboard {
     std::weak_ptr<Obstacle> shown;  // the obstacle on screen
   };
   void show(const Dashboard& dashboard) {
     if (std::shared_ptr<Obstacle> target{dashboard.shown.lock()}) {
       std::cout << "obstacle " << target->id << ": "
                 << target->speed << " m/s\n";
     } else {
       std::cout << "the obstacle is gone\n";
     }
   }

- A ``std::weak_ptr`` has no ``->`` and no ``*``. ``lock()`` returns an owning ``std::shared_ptr``, or an empty one if the object is gone.
- While ``target`` exists, it is one more owner, so the ``Obstacle`` object cannot be deleted in the middle of ``show``.
- ``702run week7_playground 80``: ``obstacle 2: 4 m/s``, then, after the tracker and the planner let go, ``the obstacle is gone``.

See `A Dashboard of weak_ptr`_ under Further Reading.

``expired`` and ``use_count``
"""""""""""""""""""""""""""""

.. code-block:: cpp

   auto cyclist{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   std::weak_ptr<Obstacle> shown{cyclist};  // use_count 1, not expired
   cyclist.reset();  // use_count 0, expired

- ``use_count()`` counts the ``std::shared_ptr``\ s that own the ``Obstacle`` object. ``expired()`` is ``true`` when that count is 0.
- To use the object, call ``lock()`` and test the result. ``expired()`` then ``lock()`` is two steps, and another thread could make the last owner let go between them.

.. note::

   C++20 **[util.smartptr.weak.obs]** (20.11.4.5): ``expired()`` "Returns: use_count() == 0." ``lock()`` "Returns: expired() ? shared_ptr<T>() : shared_ptr<T>(\*this), executed atomically."

Passing
"""""""

Required reading: the section in the table, under Further Reading, shows how a function takes a ``std::weak_ptr``.

.. list-table::
   :header-rows: 1

   * - The function...
     - Parameter type
     - Rule
     - Further Reading
   * - keeps a watcher
     - ``const std::weak_ptr<T>&``
     - R.24
     - :ref:`Passing: weak_ptr <l7-weak-passing>`
   * - only uses the object
     - ``const T&``, after ``lock()``
     - R.30
     - :ref:`Passing: weak_ptr <l7-weak-passing>`

Exercise 5: Use Counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto cyclist{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   std::weak_ptr<Obstacle> shown{cyclist};  // 1
   auto a{cyclist};                       // 2
   auto b{std::move(a)};                  // 3
   std::weak_ptr<Obstacle> shown_2{b};    // 4
   cyclist.reset();                       // 5
   b.reset();                             // 6

- After each numbered line: how many ``std::shared_ptr``\ s own the ``Obstacle`` object, and is ``shown`` expired?
- Check: ``702run week7_playground 83``.

Choosing a Pointer
------------------

Who gives this object's memory back? The answer picks the pointer.

Rule: `Core Guidelines R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`__.

One Table
^^^^^^^^^

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - The code...
     - Use
     - In our program
     - Rule
   * - only uses the object
     - ``T&``, ``const T&``, or ``T*``
     - the ``print_obstacle`` of :ref:`l7-unique-borrow`
     - R.30
   * - is its only owner
     - ``std::unique_ptr<T>``, from ``std::make_unique``
     - the tracker of `The Tracker's List`_
     - R.21, R.23
   * - is one of several owners
     - ``std::shared_ptr<T>``, from ``std::make_shared``
     - the hazard, id 2, in the tracker and the planner
     - R.22
   * - watches, and must not keep it alive
     - ``std::weak_ptr<T>``
     - the dashboard; the towing pair
     - R.24
   * - calls ``new`` and ``delete`` itself
     - nothing: do not write it
     - `An Obstacle on the Heap`_
     - R.11

- Start with ``std::unique_ptr``. Change to ``std::shared_ptr`` only when a second owner appears: it costs a control block.
- Parameters: by value to take ownership (R.32, R.34), ``std::unique_ptr<T>&`` to reseat (R.33), and the object itself to only use it (R.30).

See `More Core Guidelines`_ under Further Reading.

Back to the Tracker
^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/av_owner_map.png
   :alt: A UML object diagram in black and white: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner.
   :align: center
   :width: 80%

   The tracker, the planner and the dashboard with their smart pointers.

- **Filled diamond**: the only owner. **Open diamond**: one of several owners. **Arrow, no diamond**: looks without owning. The planner's list is ``hazards``.
- The tracker is one ``std::vector``, so its elements share one type. Once id 2 needs a ``std::shared_ptr``, all four get one (:ref:`l7-shared-creating-one`).
- The ``Obstacle`` objects with ids 1, 3 and 4 still have one owner each, through that ``std::shared_ptr``.

Summary
-------

**Ownership**

- The last owner of a heap object gives it back. With a raw ``T*`` and ``delete``, a mistake causes a leak, a double ``delete`` or a dangling read.
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

   Obstacle* cyclist{make_track(2, Pose{12.0, -1.0}, 4.0)};
   std::vector<Obstacle*> tracker{cyclist};
   std::vector<Obstacle*> hazards{cyclist};  // the same Obstacle
   for (Obstacle* t : tracker) { delete t; }
   for (Obstacle* t : hazards) { delete t; }  // a second delete

.. code-block:: text

   ==143386==ERROR: AddressSanitizer: attempting double-free on 0x504000000090
       #1 0x6352de22e888 in undefined::double_delete::run() .../undefined.cpp:53
   0x504000000090 is located 0 bytes inside of 48-byte region [...)
   freed by thread T0 here:
       #1 0x6352de22e6ba in undefined::double_delete::run() .../undefined.cpp:52

- ``702run week7_appendix ii``. AddressSanitizer stops the program at the second ``delete`` and names the first one.
- The region is 48 bytes: one ``Obstacle``. Without the sanitizer, a double ``delete`` is undefined behavior: a crash, or nothing visible.

Dangling Read, Measured
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Obstacle* cyclist{make_track(2, Pose{12.0, -1.0}, 4.0)};
   std::vector<Obstacle*> tracker{cyclist};
   std::vector<Obstacle*> hazards{cyclist};
   for (Obstacle* t : tracker) { delete t; }
   std::cout << hazards[0]->speed << '\n';  // freed memory

.. code-block:: text

   ==143390==ERROR: AddressSanitizer: heap-use-after-free on address 0x5040000000b0
   0x5040000000b0 is located 32 bytes inside of 48-byte region [...)
   freed by thread T0 here:
       #1 0x5dc9c2397e51 in undefined::dangling_read::run() .../undefined.cpp:63
   SUMMARY: AddressSanitizer: heap-use-after-free .../undefined.cpp:64

- ``702run week7_appendix iii``. AddressSanitizer names the read and the ``delete`` that freed the ``Obstacle`` object.
- "32 bytes inside": ``speed`` starts at byte 32 of an ``Obstacle``: ``id`` (4), 4 bytes of padding, ``pose`` (24), as ``offsetof`` shows (L6).

The Moved-from ``std::string``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::string note{"cyclist ahead, keeping to the right"};
   std::string name{"cyclist"};
   std::string taken_note{std::move(note)};
   std::string taken_name{std::move(name)};
   // note.size(): 0, name.size(): 0     (g++ 13.3, libstdc++)
   note = "pedestrian crossing at 30 m";  // a known value again

- With libstdc++, both moved-from strings are empty, the long one and the short one.
- The standard does not promise that. Another library may leave text behind, so code that reads ``note`` after the move depends on one library.
- What you may do with a moved-from string: assign to it, or destroy it. Both work for any valid state.

.. note::

   C++20 **[string.cons]** (21.3.2.2) paragraph 3, on ``basic_string(basic_string&& str)``: "str is left in a valid but unspecified state."

Move Assignment
^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> current{make_path(3)};
   std::vector<Pose> next{make_path(1000)};
   const Pose* where{next.data()};
   current = std::move(next);  // current's 3 poses are destroyed
   // current.size(): 1000, current.data() == where: true, next.size(): 0

- `Inside a Move`_ moved into a new vector. Here ``current`` already exists: the move gives up its old 3 poses and takes the 1000 of ``next``, without copying them (same ``data()``).
- ``next.size()`` is 0 with libstdc++. The standard says what ``current`` holds afterwards, and nothing about ``next``.

.. note::

   C++20 **[container.requirements.general]** (22.2.1), Table 76, ``a = rv``: "All existing elements of a are either move assigned to or destroyed." "Postconditions: a is equal to the value that rv had before this assignment."

``std::exchange``
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   // take the path, and leave an empty one behind
   std::vector<Pose> done{std::exchange(path, {})};
   // done.size(): 1000, path.size(): 0

   int track_id{7};
   int lost{std::exchange(track_id, 0)};  // lost: 7, track_id: 0

- ``std::exchange(obj, new_value)``, from ``<utility>``, sets ``obj`` to ``new_value`` and returns the value ``obj`` had before.
- After ``std::move(path)`` the path is valid but unspecified. After ``std::exchange(path, {})`` it is empty, guaranteed: it was assigned ``{}``.

.. note::

   C++20 **[utility.exchange]** (20.2.3) paragraph 1: "Effects: Equivalent to: ``T old_val = std::move(obj);`` ``obj = std::forward<U>(new_val);`` ``return old_val;``". See `cppreference: std::exchange <https://en.cppreference.com/w/cpp/utility/exchange>`__.

The Definition of ``std::move``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   template <typename T>  // the standard's std::move, under another name
   constexpr std::remove_reference_t<T>&& my_move(T&& t) noexcept {
     return static_cast<std::remove_reference_t<T>&&>(t);
   }

   std::vector<Pose> path{make_path(1000)};
   static_assert(std::is_same_v<decltype(my_move(path)),
                                std::vector<Pose>&&>);
   std::vector<Pose> taken{my_move(path)};  // taken: 1000, path: 0

- In a function template, a ``T&&`` parameter also accepts an lvalue: for ``path``, ``T`` is ``std::vector<Pose>&``.
- ``std::remove_reference_t<T>`` removes that ``&``, so the cast is always to ``std::vector<Pose>&&``, an xvalue. The function only casts: no data moves until ``taken`` is built.

.. note::

   C++20 **[forward]** (20.2.4) paragraph 5, on ``move(T&& t)``: "Returns: ``static_cast<remove_reference_t<T>&&>(t)``."

A ``unique_ptr`` with Its Own Deleter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto say_and_delete{[](Obstacle* target) {
     std::cout << "  deleting obstacle " << target->id << '\n';
     delete target;
   }};
   {
     std::unique_ptr<Obstacle, decltype(say_and_delete)> parked_car{
         new Obstacle{1}, say_and_delete};
     // sizeof(parked_car): 8
   }  // prints: deleting obstacle 1

- The second template argument is the deleter (`One Owner Only`_). Here a lambda (L6) that prints first.
- ``std::make_unique`` cannot take a deleter, so the code calls ``new`` and hands the result to the ``std::unique_ptr`` in the same statement.
- A lambda with no captures adds no bytes: 8. A function pointer as the deleter makes it 16 (measured).

.. note::

   Rule: `Core Guidelines R.12 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-immediate-alloc>`__, "Immediately give the result of an explicit resource allocation to a manager object".

``std::auto_ptr``
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::auto_ptr<Obstacle> a{new Obstacle{1}};
   std::auto_ptr<Obstacle> b{a};  // looks like a copy
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

   std::unique_ptr<Obstacle> parked_car;  // empty
   // parked_car == nullptr: true
   parked_car = std::make_unique<Obstacle>(1);
   if (parked_car) {
     std::cout << "obstacle " << parked_car->id << '\n';  // obstacle 1
   }
   auto other{std::move(parked_car)};  // !parked_car: true
   bool has_track = other;  // does not compile

.. code-block:: text

   error: cannot convert 'std::unique_ptr<Obstacle, std::default_delete<Obstacle> >'
          to 'bool' in initialization

- ``if (parked_car)``, ``!parked_car`` and ``parked_car == nullptr`` all test for empty. The same works for ``std::shared_ptr``.
- The conversion to ``bool`` is ``explicit``: a condition and ``bool has_track{other};`` use it, but the ``=`` form does not compile.

``unique_ptr`` to an Array
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto ranges{std::make_unique<double[]>(5)};  // five distances, each 0.0
   ranges[2] = 12.0;
   for (int i{0}; i < 5; ++i) {
     std::cout << ranges[i] << ' ';  // 0 0 12 0 0
   }
   // sizeof(ranges): 8, sizeof(std::vector<double>): 24

- ``std::unique_ptr<double[]>`` calls ``delete[]``, not ``delete``, and has ``[]`` instead of ``->``.
- It is 8 bytes because it does not keep the length. No ``size()``, no ``push_back``, no range-based ``for``: the 5 is yours to remember.
- A ``std::vector<double>`` (L4) keeps the length and grows. Use it unless an interface needs a plain array.

.. note::

   C++20 **[unique.ptr.create]** (20.11.1.4) paragraph 4, ``make_unique<T[]>(n)``: "Returns: ``unique_ptr<T>(new remove_extent_t<T>[n]())``." The ``()`` sets each element to 0. Rule: `Core Guidelines SL.con.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-vector>`__.

``swap``
^^^^^^^^

.. code-block:: cpp

   auto first{std::make_unique<Obstacle>(1)};
   auto second{std::make_unique<Obstacle>(4)};
   const Obstacle* id_1{first.get()};
   first.swap(second);  // the same as std::swap(first, second)
   // first->id: 4, second->id: 1, second.get() == id_1: true

- No ``Obstacle`` object is created, copied or deleted: the one with id 1 stays at the same address, now owned by ``second``.
- ``std::shared_ptr`` has the same ``swap``.

.. note::

   C++20 **[unique.ptr.single.modifiers]** (20.11.1.2.5) paragraph 7, ``swap(u)``: "Invokes swap on the stored pointers and on the stored deleters of \*this and u."

One Allocation with ``make_shared``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto made{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   std::shared_ptr<Obstacle> from_new{new Obstacle{2, Pose{12.0, -1.0}, 4.0}};

.. code-block:: text

   std::make_shared<Obstacle>: 1 allocation(s): 64 bytes
   std::shared_ptr<Obstacle>{new ...}: 2 allocation(s): 48 24 bytes

- ``702run week7_allocations`` counts every heap allocation each line makes.
- ``std::make_shared`` puts the ``Obstacle`` object and the control block in one block of 64 bytes (`The Control Block`_).
- With ``new``, the ``Obstacle`` object already exists when the ``std::shared_ptr`` is built, so the control block needs a second allocation: 48 bytes for the object, 24 for the control block.

.. note::

   C++20 **[util.smartptr.shared.create]** (20.11.3.6) paragraph 7.1: "Implementations should perform no more than one memory allocation." Rule: `Core Guidelines R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`__.

A Dashboard of ``weak_ptr``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::weak_ptr<Obstacle>> shown;
   for (const auto& track : tracker) {  // ids 1, 2, 3
     shown.push_back(track);  // watches, does not own
   }
   tracker.erase(tracker.begin() + 1);  // deletes the Obstacle with id 2
   for (const auto& watched : shown) {
     if (auto target{watched.lock()}) {
       std::cout << "  obstacle " << target->id << ": "
                 << target->speed << " m/s\n";
     } else {
       std::cout << "  (gone)\n";
     }
   }
   std::erase_if(shown, [](const std::weak_ptr<Obstacle>& w) {
     return w.expired();
   });

- Output: ``obstacle 1: 0 m/s``, ``(gone)``, ``obstacle 3: 1.4 m/s``, then ``shown.size()`` is 2.
- L4's ``std::erase_if`` with a lambda (L6) drops the entries whose object is gone.

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

- R.5 comes first in practice: an ``Obstacle`` that lives only inside one function is a local variable, not a heap object.
- R.37: when you pass ``*track`` or ``track.get()`` to a function, make sure an owner outlives the call.

Category, Type and Lifetime
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(3)};
   std::vector<Pose>&& r{make_path(10)};

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Expression
     - Category
     - ``decltype((e))``
     - The object
   * - ``make_path(3)``
     - prvalue
     - ``V``
     - none yet: a value that will initialize one
   * - ``r``
     - lvalue
     - ``V&``
     - a temporary that lives as long as ``r``
   * - ``path``
     - lvalue
     - ``V&``
     - lives until the end of its scope
   * - ``std::move(path)``
     - xvalue
     - ``V&&``
     - the same object as ``path``, marked "may be taken"

- ``V`` is ``std::vector<Pose>``. The type of the variable ``r`` is ``V&&``; the expression ``r`` is an lvalue (`Giving It a Name`_).
- Binding a prvalue to a reference extends the temporary's life. ``std::move`` creates nothing: it marks an object that already exists.

.. note::

   C++20 **[class.temporary]** (6.7.7) paragraph 6: the temporary object to which the reference is bound "persists for the lifetime of the reference".

Inside ``std::vector``'s Move and Copy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class Path {  // a sketch of std::vector<Pose>
     Pose* begin_; Pose* end_; Pose* cap_;
    public:
     Path(Path&& other) noexcept      // move: take the three pointers
         : begin_{other.begin_}, end_{other.end_}, cap_{other.cap_} {
       other.begin_ = other.end_ = other.cap_ = nullptr;
     }
     Path(const Path& other)          // copy: a new block, every element
         : begin_{new Pose[other.end_ - other.begin_]},
           end_{begin_ + (other.end_ - other.begin_)}, cap_{end_} {
       std::copy(other.begin_, other.end_, begin_);
     }
   };

- The move takes the pointers and leaves the source null: nothing is allocated and no element is copied (`Inside a Move`_).
- The copy allocates a block for the elements in use and copies each one, so its capacity equals its size (`Inside a Copy`_).
- Constructors are L8. For an rvalue, the ``Path&&`` one is chosen (`Overloads for Copy and Move`_).

A Reference, an Element, ``*p``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int count{3};
   int& alias{count};           // another name for count (L3)
   int numbers[3]{10, 20, 30};
   int* p{&numbers[1]};         // p holds the address of numbers[1]

- ``alias``: refers to the object ``count`` names, since a reference is another name for an object: ``&alias == &count`` (part 1). Nothing marks it (part 2), so ``alias`` is an lvalue.
- ``numbers[2]``: refers to the third ``int`` inside ``numbers``, which exists as long as ``numbers`` does (part 1). Nothing marks it (part 2), so ``numbers[2]`` is an lvalue.
- ``*p``: refers to the object ``p`` points at, ``numbers[1]``: ``&*p == &numbers[1]`` (part 1). Nothing marks it (part 2), so ``*p`` is an lvalue.

``702run week7_appendix xxi`` prints ``lvalue`` for all three, and ``true`` for both address comparisons.

Literals, Results, Calls
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   int twice(int n) { return 2 * n; }  // returns an int by value
   int count{3};
   int doubled{count * 2};
   int again{twice(count)};

- In line 2, ``3`` is a number written in the code: no object holds it until it initializes ``count``. ``3`` is a prvalue.
- In line 3, ``count * 2`` computes 6 from the value of ``count``. The 6 is a new value, not ``count``. ``count * 2`` is a prvalue.
- In line 4, ``twice(count)`` returns an ``int`` by value: a value, not an object that already exists. ``twice(count)`` is a prvalue.

``&`` on any of them gives:

.. code-block:: text

   error: lvalue required as unary '&' operand

``702run week7_appendix xxii`` prints ``prvalue`` for all three.

Ways to Mark
^^^^^^^^^^^^

.. code-block:: cpp

   struct Point { int x; int y; };
   int count{3};
   Point pt{1, 2};

``int&&`` reads "rvalue reference to ``int``": a reference whose object may be taken (`Binding to rvalues`_). Each expression below refers to an object that already exists and marks it:

- ``std::move(count)``: a call to a function that returns ``int&&``. It refers to ``count``. ``std::move(count)`` is an xvalue.
- ``static_cast<int&&>(count)``: the same mark, written as a cast to ``int&&``. It is an xvalue.
- ``std::move(pt).x``: ``std::move`` marks ``pt``, so its member ``x`` is marked too. ``std::move(pt).x`` is an xvalue.

``702run week7_appendix xxiii`` prints ``xvalue`` for all three. ``&`` fails on each: ``taking address of rvalue``.

Giving It a Name
^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose>&& r{make_path(10)};
   decltype(r)     // std::vector<Pose>&&: the type of r
   decltype((r))   // std::vector<Pose>&: the expression r is an lvalue

- The **type** of ``r`` is an rvalue reference. The **expression** ``r`` is an lvalue: it has a name, and you can use it again on the next line.
- So a function that receives a ``T&&`` parameter cannot move from it just by using its name. It has to mark it again with ``std::move``.

.. note::

   The note to **[basic.lval]** paragraph 4: "named rvalue references are treated as lvalues and unnamed rvalue references to objects are treated as xvalues".

``std::move`` on a ``const`` Object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   const std::vector<Pose> path{make_path(1000)};
   std::vector<Pose> controller_path{std::move(path)};   // compiles

.. code-block:: text

   controller_path.data() == path.data(): false, path.size(): 1000

- No warning, and no move: a new block, and ``path`` still holds 1000 poses.
- ``std::move(path)`` returns ``const std::vector<Pose>&&``. It cannot bind to the move constructor's ``std::vector<Pose>&&``, which would change ``path``.
- It does bind to the copy constructor's ``const std::vector<Pose>&``, so the compiler copies.

.. note::

   A ``const`` object cannot be moved from. Declare an object ``const`` only if you will not hand it on.

One Pair or Two Parentheses
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(3)};
   static_assert(std::is_same_v<decltype(path),
                                std::vector<Pose>>);        // one pair
   static_assert(std::is_same_v<decltype((path)),
                                std::vector<Pose>&>);       // two pairs

- One pair around a plain name: ``decltype`` gives the type ``path`` was declared with, ``std::vector<Pose>``. It says nothing about the category.
- Two pairs: ``(path)`` is no longer a plain name, so ``decltype`` follows its category. ``path`` is an lvalue, so the result is ``std::vector<Pose>&``.

.. note::

   C++20 **[dcl.type.decltype]** (9.2.8.4) paragraph 1: "if E is an unparenthesized id-expression [...], decltype(E) is the type of the entity named by E"; "otherwise, if E is an xvalue, decltype(E) is T&&", "if E is an lvalue, decltype(E) is T&", "otherwise, decltype(E) is the type of E".

A Parameter the Function Moves From
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   struct Controller { std::vector<Pose> path; };  // the part that steers
   void set_path(Controller& controller, std::vector<Pose>&& path) {
     controller.path = std::move(path);  // path is named: move it again
   }
   Controller controller{};
   std::vector<Pose> path{make_path(1000)};
   const Pose* where{path.data()};         // where path's block is

   set_path(controller, path);             // error: path is an lvalue
   set_path(controller, std::move(path));  // the caller says: take it
   set_path(controller, make_path(5));     // a prvalue: no std::move

- After line 10, ``controller.path`` holds ``path``'s block (``where``), and ``path`` is empty. After line 11, it holds 5 poses. ``702run week7_appendix xxvii``
- ``&&`` makes the caller write ``std::move`` for a named object. Inside, ``path`` has a name, so it is an lvalue: without the second ``std::move``, the assignment copies.

.. note::

   "For 'will-move-from' parameters, pass by ``X&&`` and ``std::move`` the parameter". Rule: `Core Guidelines F.18 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-consume>`__.

Returning a Local
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> plan_path(int n) {
     std::vector<Pose> path{make_path(n)};
     return path;                // elided or moved, never copied
     // return std::move(path);  // warns, and blocks the elision
   }
   std::vector<Pose> path{plan_path(1000)};

.. code-block:: text

   warning: moving a local object in a return statement prevents copy elision
   [-Wpessimizing-move]

- L5 (`Reminder: Returning by Value`_): a local returned by value is constructed in place, or moved if it cannot be. ``702run week7_appendix xxviii`` prints the same address twice.
- ``std::move`` on the return turns the local into an xvalue, and the compiler can no longer build it in place.

.. note::

   "Don't ``return std::move(local)``". Rule: `Core Guidelines F.48 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-move-local>`__.

.. _l7-app-unique-borrow:

Passing: Borrow
^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_obstacle(const Obstacle& target);  // only reads it
   void set_speed(Obstacle* target, double speed) {      // may get nullptr
     if (target != nullptr) { target->speed = speed; }
   }

   auto parked_car{
       std::make_unique<Obstacle>(1, Pose{20.0, -3.0, 0.0}, 0.0, true)};
   print_obstacle(*parked_car);  // 0 m/s
   set_speed(parked_car.get(), 2.0);
   print_obstacle(*parked_car);  // 2 m/s: the caller still owns it

.. dropdown:: The Definition of ``print_obstacle``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      void print_obstacle(const Obstacle& target) {  // only reads it
        std::cout << "  obstacle " << target.id << ": " << target.speed << " m/s\n";
      }

- A function that only uses the ``Obstacle`` object takes it by reference or plain pointer, not the smart pointer.
- It then works for any ``Obstacle``: on the heap, on the stack, or in a vector.

.. note::

   "Take smart pointers as parameters only to explicitly express lifetime semantics". Rule: `Core Guidelines R.30 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrparam>`__.

.. _l7-app-unique-sink:

Passing: Sink
^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<std::unique_ptr<Obstacle>> lost;      // lost tracks, kept
   void keep_lost(std::unique_ptr<Obstacle> track) {  // takes ownership
     lost.push_back(std::move(track));
   }

   auto parked_car{std::make_unique<Obstacle>(1)};
   keep_lost(parked_car);        // does not compile: a copy
   keep_lost(std::move(parked_car));  // parked_car is now empty

- A **sink** is a parameter that takes ownership: the function keeps the object or deletes it.
- By value: the parameter is a new owner; the caller hands the object over with ``std::move``.
- F.18, from `A Parameter the Function Moves From`_ under Further Reading, asks for ``&&`` here. Its own exception: a move-only type that is cheap to move, such as ``std::unique_ptr``, can be passed by value.

.. note::

   "Take a ``unique_ptr<widget>`` parameter to express that a function assumes ownership of a ``widget``". Rule: `Core Guidelines R.32 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-uniqueptrparam>`__.

.. _l7-app-unique-reseat:

Passing: Reseat
^^^^^^^^^^^^^^^

.. code-block:: cpp

   void replace_track(std::unique_ptr<Obstacle>& track, int new_id) {
     track = std::make_unique<Obstacle>(new_id);
   }  // the assignment deleted the old Obstacle object

   auto track{std::make_unique<Obstacle>(1, Pose{20.0, -3.0}, 0.0, true)};
   replace_track(track, 7);  // track->id: 7, track->speed: 0

- To **reseat** a pointer is to make it own, or point at, a different object. By reference to the ``std::unique_ptr``, the function may reseat the caller's pointer.
- The caller keeps ownership. Only what it owns changes.

.. note::

   "Take a ``unique_ptr<widget>&`` parameter to express that a function reseats the ``widget``". Rule: `Core Guidelines R.33 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-reseat>`__.

.. _l7-unique-returning:

Returning
^^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<Obstacle> make_track(int id) {
     auto track{std::make_unique<Obstacle>(id)};
     return track;  // no std::move: L5's implicit move
   }

   auto oncoming_car{make_track(4)};  // oncoming_car->id: 4

- A function that creates the object, such as ``make_track``, returns the ``std::unique_ptr`` by value. The caller becomes the owner.
- ``return track;`` compiles although ``std::unique_ptr`` cannot be copied: a local returned by value is moved, never copied (L5, and `Returning a Local`_ under Further Reading).
- Compare `An Obstacle on the Heap`_: there, the caller had to ``delete`` the ``Obstacle*`` that ``make_track`` returned. Here the ``std::unique_ptr`` deletes it.

.. _l7-shared-borrow:

Passing: Borrow
^^^^^^^^^^^^^^^

.. code-block:: cpp

   void print_obstacle(const Obstacle& target);  // only reads it

   auto hazard{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   print_obstacle(*hazard);
   std::cout << hazard.use_count() << '\n';  // 1: no owner added

.. dropdown:: The Definition of ``print_obstacle``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      void print_obstacle(const Obstacle& target) {  // only reads it
        std::cout << "  obstacle " << target.id << ": " << target.speed << " m/s\n";
      }

- The same rule as for ``std::unique_ptr`` (:ref:`l7-unique-borrow`): a function that only uses the ``Obstacle`` object takes it, not the smart pointer.
- A ``std::shared_ptr`` passed by value would add an owner and remove it again: two changes to the count for nothing.

.. note::

   Rule: `Core Guidelines R.30 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrparam>`__.

.. _l7-app-shared-share:

Passing: Share
^^^^^^^^^^^^^^

.. code-block:: cpp

   using Hazards = std::vector<std::shared_ptr<Obstacle>>;
   void add_hazard(Hazards& hazards, std::shared_ptr<Obstacle> hazard) {
     hazards.push_back(std::move(hazard));  // the list keeps this owner
   }

   Hazards hazards;
   auto cyclist{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   add_hazard(hazards, cyclist);
   std::cout << cyclist.use_count() << '\n';  // 2

- By value: the parameter is one more owner. The function moves it into the list, so the list keeps that owner's place.
- ``using Hazards = ...;`` is a type alias (L2): a shorter name for the long type.

.. note::

   "Take a ``shared_ptr<widget>`` parameter to express shared ownership". Rule: `Core Guidelines R.34 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-owner>`__.

.. _l7-app-shared-const-ref:

Passing: ``const shared_ptr&``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void add_if_close(Hazards& hazards,
                     const std::shared_ptr<Obstacle>& track) {
     if (track->pose.x < 25.0) {
       hazards.push_back(track);  // copies only when it keeps it
     }
   }

   add_if_close(hazards, near);  // x = 12 m: kept, near's count 2
   add_if_close(hazards, far);   // x = 38 m: not kept, far's count 1

- By ``const&``: the call adds no owner. The function copies the ``std::shared_ptr`` only if it decides to keep the ``Obstacle`` object.
- ``near``: id 2; ``far``: id 4. The 25 m limit is chosen for this example.

.. note::

   "Take a ``const shared_ptr<widget>&`` parameter to express that it might retain a reference count to the object" (a rule the Guidelines have not finished). Rule: `Core Guidelines R.36 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-const>`__.

.. _l7-shared-returning:

Returning
^^^^^^^^^

.. code-block:: cpp

   std::unique_ptr<Obstacle> make_track(int id);  // returns a std::unique_ptr
   std::shared_ptr<Obstacle> hazard{make_track(5)};  // compiles
   std::unique_ptr<Obstacle> back{hazard};           // does not compile

.. code-block:: text

   error: no matching function for call to
   'std::unique_ptr<Obstacle>::unique_ptr(<brace-enclosed initializer list>)'

``make_track`` is the function from :ref:`l7-unique-returning`.

- A ``std::unique_ptr`` converts to a ``std::shared_ptr``: one owner becomes the first of several.
- Not the other way: other owners may exist, and a ``std::unique_ptr`` must be the only one.
- So a function that creates an ``Obstacle`` returns a ``std::unique_ptr``. The caller turns it into a ``std::shared_ptr`` if it needs to share.

.. _l7-weak-passing:

Passing: ``weak_ptr``
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   struct Dashboard { std::weak_ptr<Obstacle> shown; };
   void watch(Dashboard& dashboard,
              const std::weak_ptr<Obstacle>& target) {
     dashboard.shown = target;  // stores a watcher, not an owner
   }
   void print_obstacle(const Obstacle& target);  // only reads it

   auto cyclist{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   Dashboard dashboard{};
   watch(dashboard, cyclist);  // a shared_ptr converts to a weak_ptr
   if (auto target{dashboard.shown.lock()}) {
     print_obstacle(*target);  // lock first, then pass the object
   }

- A function that keeps a watcher takes ``const std::weak_ptr<T>&`` and stores a copy. ``cyclist.use_count()`` stays 1.
- A function that only uses the object takes ``const T&``. The caller locks first, then passes the object (R.30).
- The Core Guidelines have no rule for ``std::weak_ptr`` parameters. The first bullet follows the example in `Core Guidelines R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`__.

.. _l7-const-ref-binds:

``const T&`` with Each Category
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<int> make_path(int n) { return std::vector<int>(n, 7); }
   void print_size(const std::vector<int>& path) {
     std::cout << path.size() << '\n';
   }

   std::vector<int> path{make_path(3)};
   print_size(path);              // 1. lvalue: prints 3
   print_size(make_path(5));      // 2. prvalue: prints 5
   print_size(std::move(path));   // 3. xvalue: prints 3
   std::cout << path.size();

- 1: ``path`` is an lvalue. The reference is another name for ``path``.
- 2: ``make_path(5)`` is a prvalue. A temporary vector is made, the reference binds to it, and it is destroyed at the end of the line. ``print_size`` only reads it, so nothing is lost.
- 3: ``std::move(path)`` is an xvalue. Through a ``const&``, ``print_size`` cannot take the contents, so the last line prints 3.
