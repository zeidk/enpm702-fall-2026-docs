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

1. Get the code: ``git pull``.
2. In the top-level ``CMakeLists.txt`` (repository root), check that ``add_subdirectory(project/week7)`` is not commented out.
3. Configure: ``702configure``.
4. Build it: ``702build week7_playground``.
5. Run every slide: ``702run week7_playground``. Run only one slide, for example `Handing a Path to the Controller`_: ``702run week7_playground 14``.

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
      702run week7_playground 14         # only the code of slide 14
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

   A slide whose code leaks or has undefined behavior, such as slide 89, runs only when you ask for it by number: ``702run week7_playground 89``. A full run skips it.

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

An autonomous car, the **ego vehicle**, drives along a two-lane road. The ego vehicle has a **tracker**, which sees four obstacles. In this lecture we write the tracker, the **planner** and the **dashboard**.

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
- **Filled diamond**, the only owner: ``tracker`` owns ids 1, 3 and 4. **Open diamond**, one of several owners: ``tracker`` and ``planner`` own id 2, the cyclist.
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

   Obstacle* track{make_track(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   std::cout << track->id << ' ' << track->speed << '\n';  // 2 4
   delete track;  // the caller must remember this
   track = nullptr;

- ``make_track`` creates the ``Obstacle`` object with ``new``. The caller must ``delete`` it.
- Nothing in the type says so: ``Obstacle*`` looks the same whether it owns the ``Obstacle`` object or only points at it.

.. note::

   "A raw pointer (a ``T*``) is non-owning". An owner needs a type that says it owns. Rule: `Core Guidelines R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr>`__.

Reminder: Three Ways to Get It Wrong
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Leak**: a function returns early and skips its ``delete``. The ``Obstacle`` object's memory is never given back.
2. **Double** ``delete``: the same ``Obstacle`` object is in the tracker's list and the planner's hazard list, and each list deletes it. It breaks the rule "``delete`` exactly once" and is undefined behavior.
3. **Dangling read**: the tracker deletes the ``Obstacle`` object when the track is lost, and the planner still reads it. Undefined behavior.

.. note::

   The cause is the same in all three: no code is marked as the owner.

See `Double Delete, Measured`_ and `Dangling Read, Measured`_ under Further Reading.

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

Handing a Path to the Controller
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> make_path(int n);        // n poses, 1 m apart
   std::vector<Pose> path{make_path(1000)};   // pose i at x = i m
   const Pose* where{path.data()};

   std::vector<Pose> copied{path};            // a copy
   std::vector<Pose> moved{std::move(path)};  // a move

.. code-block:: text

   copy: copied.data() == path.data(): false, path.size(): 1000
   move: moved.data() == where: true, path.size(): 0
   bytes the copy allocated: 24000

- The copy allocates a new block, 1000 × 24 bytes (``sizeof(Pose)``: three ``double``\ s) = 24000 bytes, and copies every ``Pose``. ``path`` is unchanged.
- The move allocates nothing. ``moved`` holds the block ``path`` had, at the same address, and ``path`` is left empty.

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
   - It returns the local ``path`` by value: no copy is made (`Returning a Local`_).

An Implicit Move
^^^^^^^^^^^^^^^^

.. code-block:: cpp

   const Pose* made{nullptr};             // where plan's block is made
   std::vector<Pose> plan(int n) {        // a custom function
     std::vector<Pose> path{make_path(n)};
     made = path.data();
     return path;                         // no std::move
   }

   std::vector<std::vector<Pose>> plans;
   plans.push_back(plan(500));            // no std::move

.. code-block:: text

   plans[0].data() == made: true, plans[0].size(): 500

- No ``std::move``, and still no copy: the block made inside ``plan`` is the block in ``plans[0]``.
- ``return path;`` moves the local out of the function, or builds it in place (`Returning a Local`_).
- ``push_back`` gets a temporary, so it takes the overload that moves (`Overloads for Copy and Move`_).
- ``702run week7_playground 15`` prints the line above.

Inside a Copy
^^^^^^^^^^^^^

.. figure:: /_static/images/l7/av_vector_copy.png
   :alt: Two panels side by side, one per vector, each under a rounded name tag: path on the left, copied on the right. In each panel, a blue box with a stack icon and the word Stack holds three fields, begin, end and capacity, each marked ptr. Below it, a red box with a heap icon and the word Heap holds a strip of cells, and three blue arrows run from the fields down to the top edge of the strip. The two panels are drawn the same way: the begin arrow ends at the left end of the first cell, and the end and capacity arrows both at the right end of the last cell. Each measuring line reads 1000 Pose, 24000 bytes. No arrow joins the two panels.
   :align: center
   :width: 100%

   A ``std::vector`` and its copy: each one owns its own block.

- After ``std::vector<Pose> copied{path}``, each vector has its own block and frees it at the end of its scope.
- ``begin`` points at the first ``Pose``, ``end`` one past the last one (the right edge of the last cell), ``capacity`` one past the last slot.
- ``make_path`` reserved 1000 slots, and a copy allocates exactly its size: in both, ``end`` equals ``capacity``. Each block: 1000 × 24 = 24000 bytes; total 48000.

Inside a Move
^^^^^^^^^^^^^

.. figure:: /_static/images/l7/av_vector_move.png
   :alt: Two panels separated by a thin line, tagged 1 and 2. Panel 1: a name tag reading path over a blue box with a stack icon and the word Stack, holding three fields, begin, end and capacity, each marked ptr. Below, a red box with a heap icon and the word Heap holds a strip of cells, and three blue arrows run from the fields down to the top edge of the strip: begin ends at the left end of the first cell, and end and capacity both at the right end of the last cell. A measuring line under it reads 1000 Pose, 24000 bytes. Panel 2: a name tag reading path over the same Stack box, its three fields now reading nullptr, with no arrows. Below it a name tag reading moved over a second Stack box with the same three fields, each marked ptr, and three blue arrows from them to the strip of cells in a Heap box like the one in panel 1, ending at the same places, with the same measuring line, 1000 Pose, 24000 bytes.
   :align: center
   :width: 100%

   A ``std::vector`` before and after a move. **1**: ``path`` owns the block. **2**: after the move, ``moved`` owns the block and ``path``'s three pointers are null.

- **1**: ``path`` owns the block through its three pointers (L4).
- **2**: after ``std::vector<Pose> moved{std::move(path)}``, ``moved`` holds the same three pointers and ``path``'s are null (libstdc++, measured).
- Only 24 bytes change hands: the three 8-byte pointers, whatever the vector holds.

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
- Check: ``702run week7_playground 19`` prints each vector's size, capacity and block after every line.

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

An **lvalue** is an expression that (1) refers to an object that already exists, and (2) does not let another object take its contents: an object made from it is a copy.

.. code-block:: cpp
   :linenos:

   int count{3};        // makes an int object that holds 3
   count = 4;           // the same object now holds 4
   int* where{&count};  // where holds that object's address

.. code-block:: text

   count: 4, where == &count: true

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

.. code-block:: text

   after line 2: scores.size(): 3, copied.size(): 3
   after line 3: scores.size(): 0, best.size(): 3

- To **take** an object's contents is to move them into another object. To **mark** an object, with ``std::move``, is to say another object may take them. Line 3 takes the three numbers that ``scores`` keeps on the heap.
- In line 2, ``scores`` is an lvalue. Part (2) holds: ``copied`` gets its own copy, and ``scores`` keeps its three numbers.
- In line 3, ``std::move(scores)`` **marks** ``scores``. ``best`` takes its contents, and ``scores`` is left empty (libstdc++, measured). Part (2) fails: ``std::move(scores)`` is not an lvalue (`xvalue: Marked by std::move`_).
- One exception: ``return path;`` may move from a local variable even though ``path`` is an lvalue (`An Implicit Move`_).

lvalue: Checking with ``&``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :linenos:

   int count{3};
   int* a{&count};        // compiles
   int* b{&(count + 1)};  // does not compile

.. code-block:: text

   error: lvalue required as unary '&' operand

- The built-in ``&`` compiles only on an lvalue: parts (1) and (2) of the definition must both hold. Line 3 fails part (1); `xvalue: Ways to Mark`_ shows part (2) failing.
- In line 2, ``count`` is an lvalue: parts (1) and (2) hold (`lvalue: A Named Object`_). So ``&count`` compiles.
- In line 3, ``count + 1`` computes 4, but no object that already exists holds that 4. Part (1) fails: ``count + 1`` is not an lvalue, and ``&(count + 1)`` does not compile. `prvalue: A Computed Value`_ says what it is.

lvalue: A Reference, an Element, ``*p``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int count{3};
   int& alias{count};           // another name for count (L3)
   int numbers[3]{10, 20, 30};
   int* p{&numbers[1]};         // p holds the address of numbers[1]

- ``alias``: refers to the object ``count`` names, since a reference is another name for an object: ``&alias == &count`` (part 1). Nothing marks it (part 2), so ``alias`` is an lvalue.
- ``numbers[2]``: refers to the third ``int`` inside ``numbers``, which exists as long as ``numbers`` does (part 1). Nothing marks it (part 2), so ``numbers[2]`` is an lvalue.
- ``*p``: refers to the object ``p`` points at, ``numbers[1]``: ``&*p == &numbers[1]`` (part 1). Nothing marks it (part 2), so ``*p`` is an lvalue.

``702run week7_playground 26`` prints ``lvalue`` for all three, and ``true`` for both address comparisons.

lvalue: In the Tracker
^^^^^^^^^^^^^^^^^^^^^^

Test for an **lvalue** (`lvalue: A Named Object`_): ``&`` compiles on it.

.. code-block:: cpp

   Obstacle make_obstacle(int id);
   Obstacle& first_obstacle(std::vector<Obstacle>& seen);
   std::vector<Pose> path{make_path(3)};
   std::vector<Obstacle> seen{make_obstacle(1), make_obstacle(2)};
   Obstacle* last{&seen[1]};

With the declarations above, each expression below refers to an object that already exists, and none marks it, so each is an lvalue:

- ``path``: the variable ``path`` itself.
- ``*last``: the ``Obstacle`` object ``last`` points at, ``seen[1]``.
- ``seen[0]``: the first ``Obstacle`` object stored in ``seen``.
- ``first_obstacle(seen)``: the ``Obstacle`` object the returned ``Obstacle&`` refers to, ``seen[0]``.
- ``"stop"``: a ``const char[5]`` array that the program keeps until it ends.

``&`` compiles on all five. ``702run week7_playground 27`` prints ``lvalue`` for each.

.. dropdown:: The Definitions of ``make_obstacle`` by Value and ``first_obstacle``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      Obstacle make_obstacle(int id) {
        return Obstacle{id};  // the other members take their defaults
      }

      Obstacle& first_obstacle(std::vector<Obstacle>& seen) {
        return seen[0];
      }

   - ``make_obstacle`` returns a new ``Obstacle`` by value. `lvalue: In the Tracker`_, `xvalue: In the Tracker`_, `Temporary Materialization`_ and `Exercise 2: Value Categories`_ use it.
   - ``first_obstacle`` returns a reference to the first ``Obstacle``, so a call to it is an lvalue.

prvalue: A Computed Value
^^^^^^^^^^^^^^^^^^^^^^^^^

A **prvalue** is an expression that does not refer to an object that already exists. It computes a value, and that value can initialize a new object.

.. code-block:: cpp
   :linenos:

   int count{3};
   int next{count + 1};  // the 4 initializes next

.. code-block:: text

   next: 4, count: 3
   count + 1: prvalue

- Part (1) of the lvalue definition: does ``count + 1`` refer to an object that already exists? No. It computes 4, and no object held that 4 before line 2.
- The 4 initializes ``next``, a new object. ``count`` is unchanged.
- Part (1) fails, so in line 2, ``count + 1`` is a prvalue. That is also why ``&(count + 1)`` does not compile (`lvalue: Checking with &`_).

prvalue: Literals, Results, Calls
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

``702run week7_playground 30`` prints ``prvalue`` for all three.

prvalue: In the Tracker
^^^^^^^^^^^^^^^^^^^^^^^

Test for a **prvalue** (`prvalue: A Computed Value`_): ``&`` does not compile on it.

.. code-block:: cpp

   std::vector<Pose> make_path(int n);
   int a{2};
   int b{3};

With the declarations above, each expression below is a prvalue:

- ``42``: a literal (not a string literal).
- ``a + b``: a built-in arithmetic result. ``&(a + b)`` does not compile.
- ``make_path(3)``: a call that returns by value.
- ``Obstacle{}``: a value of a class type, made with braces.
- ``[] { return 1; }``: a lambda expression.

.. code-block:: text

   &(a + b):      error: lvalue required as unary '&' operand
   &make_path(3): error: taking address of rvalue

``702run week7_playground 31`` prints ``prvalue`` for all five.

xvalue: Marked by ``std::move``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An **xvalue** is an expression that (1) refers to an object that already exists, and (2) lets another object take its contents: the object may be moved from.

.. code-block:: cpp
   :linenos:

   std::vector<int> scores{90, 75, 82};
   std::vector<int> best{std::move(scores)};

.. code-block:: text

   best.size(): 3, scores.size(): 0

- Part (1): ``std::move(scores)`` refers to ``scores``, made in line 1.
- Part (2): ``std::move`` marks ``scores``, so another object may take its contents (`lvalue: Copied, Not Taken`_).
- Both hold, so in line 2, ``std::move(scores)`` is an xvalue. ``best`` takes the three numbers, and ``scores`` is left empty (libstdc++, measured).

xvalue: Ways to Mark
^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   struct Point { int x; int y; };
   int count{3};
   Point pt{1, 2};

``int&&`` reads "rvalue reference to ``int``": a reference whose object may be taken (`Binding to rvalues`_). Each expression below refers to an object that already exists and marks it:

- ``std::move(count)``: a call to a function that returns ``int&&``. It refers to ``count``. ``std::move(count)`` is an xvalue.
- ``static_cast<int&&>(count)``: the same mark, written as a cast to ``int&&``. It is an xvalue.
- ``std::move(pt).x``: ``std::move`` marks ``pt``, so its member ``x`` is marked too. ``std::move(pt).x`` is an xvalue.

``702run week7_playground 34`` prints ``xvalue`` for all three. ``&`` fails on each: ``taking address of rvalue``.

xvalue: In the Tracker
^^^^^^^^^^^^^^^^^^^^^^

Marking an **xvalue** (`xvalue: Marked by std::move`_) moves nothing.

.. code-block:: cpp

   std::vector<Pose> path{make_path(3)};
   Obstacle cyclist{make_obstacle(2)};

``T&&`` reads "rvalue reference to ``T``": a reference whose object may be taken (`Binding to rvalues`_). Here ``T`` is ``std::vector<Pose>``. Each expression below is an xvalue:

- ``std::move(path)``: a call to a function whose return type is ``T&&``. It refers to ``path``, now marked.
- ``static_cast<std::vector<Pose>&&>(path)``: the same marking, written as a cast to ``T&&``.
- ``std::move(cyclist).pose``: ``std::move`` marks ``cyclist``, so its member ``pose`` is marked too. Its ``decltype((e))`` is ``Pose&&``, the same form with ``T`` = ``Pose`` (`The decltype Test`_).

``702run week7_playground 35`` prints ``xvalue`` for all three. Afterwards ``path.size()`` is still 3. The three are cases 4.1, 4.2 and 4.4 in the note to **[basic.lval]** paragraph 4.

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

``decltype``
^^^^^^^^^^^^

``decltype(e)`` names a type: the type of ``e``, worked out by the compiler without running ``e``. You can use it wherever you would write a type.

.. code-block:: cpp

   int count{3};
   const double limit{40.0};
   std::vector<Pose> path{make_path(3)};
   Pose& first{path[0]};
   auto copy{limit};            // double: auto drops const

With the declarations above:

- ``decltype(count)`` is ``int``, so ``decltype(count) other{5};`` declares an ``int``.
- ``decltype(limit)`` is ``const double``: unlike ``auto``, ``decltype`` keeps ``const``.
- ``decltype(first)`` is ``Pose&``: it keeps the ``&`` too.
- ``decltype(path.size())`` is ``std::size_t`` (libstdc++), the type the call returns. ``size()`` is not called.

.. note::

   C++20 **[dcl.type.decltype]** (9.2.8.4) paragraph 1: for a plain name, "decltype(E) is the type of the entity named by E". "The operand of the decltype specifier is an unevaluated operand".

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

- ``decltype((e))`` gives ``T&`` for an lvalue, ``T&&`` for an xvalue, and ``T`` for a prvalue. The three ``static_assert``\ s compile.
- The second pair of parentheses matters: ``decltype(path)`` gives the declared type of the variable, ``std::vector<Pose>``, not its category.
- The playground prints each category with this test.

.. note::

   C++20 **[dcl.type.decltype]** (9.2.8.4) paragraph 1: "if E is an xvalue, decltype(E) is T&&", "if E is an lvalue, decltype(E) is T&", "otherwise, decltype(E) is the type of E".

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

- Write lvalue, xvalue or prvalue for each line. Then check: ``702run week7_playground 40``.

Binding to rvalues
^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<Pose> path{make_path(1000)};
   std::vector<Pose>&& temp_ref{make_path(10)};       // OK: an rvalue
   const std::vector<Pose>& any_ref{path};            // binds to both
   std::vector<Pose>&& lvalue_ref{path};              // does not compile

.. code-block:: text

   error: cannot bind rvalue reference of type 'std::vector<Pose>&&' to lvalue
   of type 'std::vector<Pose>'

- ``T&&`` is an **rvalue reference**. It binds only to rvalues: prvalues and xvalues.
- Bound to the prvalue ``make_path(10)``, ``temp_ref`` gets a temporary that lives as long as ``temp_ref``.
- ``const T&`` binds to both (L5), but through it you cannot change the object, so you cannot take from it.

See `Category, Type and Lifetime`_ under Further Reading.


What Each Reference Refers To
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: /_static/images/l7/av_binding.png
   :alt: On the right, two name tags, each over a blue box with a stack icon and the word Stack holding three fields, begin, end and capacity, each marked ptr: the upper one reads path, the lower one reads (temporary). On the left, three references, each a name tag with its type under it and a numbered tag beside it. Tag 2, any_ref, type const std::vector<Pose>&: a solid dark blue arrow runs from it to the path box. Tag 3, lvalue_ref, type std::vector<Pose>&&: a gray dashed arrow runs from it to the path box, crossed out by a circled X halfway along. Tag 1, temp_ref, type std::vector<Pose>&&: a solid dark blue arrow runs from it to the temporary's box.
   :align: center
   :width: 100%

   The code of `Binding to rvalues`_, in memory: each reference and the object it refers to.

- **1**, line 2: ``temp_ref`` binds the temporary from ``make_path(10)`` and keeps it alive (C++20 **[class.temporary]** paragraph 6: the temporary "persists for the lifetime of the reference").
- **2**, line 3: ``any_ref``, a ``const&``, binds ``path``, an lvalue.
- **3**, line 4: a ``T&&`` cannot bind ``path``, an lvalue, so it does not compile. The figure draws it dashed and crossed out.
- A reference has no box. C++20 **[dcl.ref]** paragraph 4: "It is unspecified whether or not a reference requires storage."

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

Overloads for Copy and Move
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

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
- ``std::vector`` itself has both: a copy constructor and a move constructor. That is how the compiler chose between the copy and the move in `Handing a Path to the Controller`_.

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

See `The Definition of std::move`_ under Further Reading.

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

A Parameter the Function Moves From
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

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

.. code-block:: text

   controller.path.data() == where: true, path.size(): 0
   controller.path.size(): 5

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

     inside plan_path, path.data(): 0x52a000000200
     in the caller, path.data(): 0x52a000000200
   warning: moving a local object in a return statement prevents copy elision
   [-Wpessimizing-move]

- L5 (`Reminder: Returning by Value`_): a local returned by value is constructed in place, or moved if it cannot be. Same address, measured.
- ``std::move`` on the return turns the local into an xvalue, and the compiler can no longer build it in place.

.. note::

   "Don't ``return std::move(local)``". Rule: `Core Guidelines F.48 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-move-local>`__.

Smart Pointers
--------------

A **smart pointer** is an object that points at one heap object and says, in its type, how that object is owned. The owning ones delete the object when its last owner lets go.

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

   Orange, from the map in `Who Owns Each Obstacle`_: the filled diamonds, one owner.

See `cppreference: std::unique_ptr <https://en.cppreference.com/w/cpp/memory/unique_ptr>`__. Rule: `Core Guidelines R.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-owner>`__.

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

   Pose at{12.0, -1.0, 0.0};  // the cyclist's pose, from the table
   std::unique_ptr<Obstacle> track{std::make_unique<Obstacle>(2, at, 4.0)};
   std::cout << track->id << ' ' << (*track).speed << '\n';  // 2 4
   auto empty{std::make_unique<Obstacle>()};  // members take defaults
   std::cout << empty->id << ' ' << empty->speed << '\n';    // 0 0

- ``std::make_unique<T>(args)`` creates the object on the heap and returns the ``std::unique_ptr`` that owns it.
- The arguments go to the object, as with L6's ``emplace_back``.
- ``->`` and ``*`` work as they do on an ``Obstacle*``.
- No ``new``, and no ``delete``: ``track`` deletes the ``Obstacle`` object when it goes out of scope.

.. note::

   "Use ``make_unique()`` to make ``unique_ptr``\ s". Rule: `Core Guidelines R.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_unique>`__.

See `A unique_ptr with Its Own Deleter`_ under Further Reading.

In Memory
"""""""""

.. figure:: /_static/images/l7/av_unique_ptr_memory.png
   :alt: On the left, a name tag reading track over a blue box with a stack icon and the word Stack, holding one field, pointer, marked an Obstacle*. A measuring line under it reads 8 bytes. On the right, under a name tag reading Obstacle, a red box with a heap icon and the word Heap holds a block of four rows: id 2, pose {12.0, -1.0, 0.0}, speed 4.0, and is_static false. A blue arrow runs from the pointer field to the left edge of that block, at its first row, id. A measuring line under the block reads 48 bytes.
   :align: center
   :width: 100%

   A ``std::unique_ptr`` on the stack and the ``Obstacle`` object it owns on the heap.

.. code-block:: text

   sizeof(track): 8, sizeof(Obstacle*): 8, sizeof(Obstacle): 48

- The ``std::unique_ptr`` is one pointer on the stack, the same 8 bytes as an ``Obstacle*``. The resource, the ``Obstacle`` object, is on the heap.
- Using a ``std::unique_ptr`` instead of an ``Obstacle*`` adds no bytes. It adds two rules: it deletes the ``Obstacle`` object when it is destroyed, and no other ``std::unique_ptr`` can own that object.

The Leak, Fixed
"""""""""""""""

**With a regular pointer**

.. code-block:: cpp

   bool needs_braking(int id) {
     Obstacle* track{make_track(
         id, Pose{12.0, -1.0}, 4.0)};
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
         id, Pose{12.0, -1.0}, 4.0)};
     if (track->pose.x > 10.0) {
       return false;  // deleted here
     }
     return true;     // and here
   }

- The first one leaks 48 bytes: the cyclist is 12 m ahead, past the 10 m chosen for this example, so the early return skips the ``delete``.
- ``702run week7_playground 55`` runs the second one: ``needs_braking(2): false``, and no LeakSanitizer report.
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
- Two owners of one ``Obstacle`` object would both delete it: the double ``delete`` of `Reminder: Three Ways to Get It Wrong`_. The type rules it out at compile time.
- ``_Dp = std::default_delete<Obstacle>`` is the deleter; it calls ``delete``.

See `std::auto_ptr`_ under Further Reading.

``get`` and ``reset``
"""""""""""""""""""""

.. code-block:: cpp

   void print_obstacle(const Obstacle* target);  // only looks

   auto track{std::make_unique<Obstacle>(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   print_obstacle(track.get());  // track still owns it
   track.reset();                // deletes it now: track == nullptr
   track = std::make_unique<Obstacle>(3, Pose{30.0, 2.5, 1.57}, 1.4);

.. dropdown:: The Definition of ``print_obstacle``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. code-block:: cpp

      void print_obstacle(const Obstacle* target) {  // only looks
        std::cout << "  obstacle " << target->id << ": " << target->speed << " m/s\n";
      }

- ``get()`` returns the plain pointer. It does not give up ownership: the code that receives it only looks, and must not ``delete`` it.
- ``reset()`` deletes the ``Obstacle`` object now, without waiting for the end of the scope. ``reset(p)`` stores ``p``, then deletes the old object, if there was one.
- Assigning a new ``std::unique_ptr`` stores the new object's address, then deletes the old object, as ``reset`` does.

.. note::

   C++20 **[unique.ptr.single.modifiers]** (20.11.1.2.5) paragraph 4, ``reset(p)``: "Assigns p to the stored pointer, and then if and only if the old value of the stored pointer, old_p, was not equal to nullptr, calls get_deleter()(old_p)."

See `swap`_ under Further Reading.

Moving Ownership
""""""""""""""""

.. code-block:: cpp
   :linenos:

   auto track{std::make_unique<Obstacle>(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   Obstacle* where{track.get()};
   std::unique_ptr<Obstacle> other{std::move(track)};

.. code-block:: text

   track == nullptr: true, other.get() == where: true, other->id: 2

- Line 2: ``where`` only points at the ``Obstacle`` object; ``track`` still owns it.
- Line 3, the move constructor (`Inside a Move`_): ``other`` takes the pointer, and ``track`` is left empty. ``other.get() == where``: the ``Obstacle`` object did not move.
- Unlike a moved-from ``std::vector``, a moved-from ``std::unique_ptr`` is guaranteed to be empty.

.. note::

   C++20 **[unique.ptr.single.ctor]** (20.11.1.2.1) paragraph 20, for ``unique_ptr(unique_ptr&& u)``: "Postconditions: get() yields the value u.get() yielded before the construction. u.get() == nullptr."

See `Testing for Empty`_ under Further Reading.

Step 1: Before the Move
"""""""""""""""""""""""

.. figure:: /_static/images/l7/av_unique_ptr_move_1.png
   :alt: A blue box with a stack icon and the word Stack holds two fields: track, of type std::unique_ptr, and where, of type Obstacle*. On the right, under a name tag reading Obstacle, a red box with a heap icon and the word Heap holds one object of four rows: id 2, pose {12.0, -1.0, 0.0}, speed 4.0, and is_static false. A solid blue arrow runs from track to the left edge of the object, at its first row, id. A dashed blue arrow runs from where to the same row, just below the solid arrow.
   :align: center
   :width: 100%

- After line 2 of `Moving Ownership`_: ``track`` owns the ``Obstacle`` object (solid arrow).
- ``where`` holds the same address (dashed arrow), but an ``Obstacle*`` owns nothing: it never deletes the object.
- Both arrows end at ``id``: the object's address is where it starts, at its first member.

Step 2: After the Move
""""""""""""""""""""""

.. figure:: /_static/images/l7/av_unique_ptr_move_2.png
   :alt: A blue box with a stack icon and the word Stack holds three fields: track, of type std::unique_ptr, marked nullptr, with no arrow; where, of type Obstacle*; and other, of type std::unique_ptr. On the right, under a name tag reading Obstacle, a red box with a heap icon and the word Heap holds the same object as before, four rows: id 2, pose {12.0, -1.0, 0.0}, speed 4.0, and is_static false. A dashed blue arrow runs from where to the left edge of the object, at its first row, id. A solid blue arrow runs from other to the same row, just below the dashed arrow.
   :align: center
   :width: 100%

- After line 3: ``other`` owns the ``Obstacle`` object, and ``track`` holds ``nullptr``.
- ``where`` still holds the same address: the object did not move.
- ``track`` points at nothing, so it deletes nothing when it goes out of scope.

Exercise 3: Handing Over a Track
""""""""""""""""""""""""""""""""

.. code-block:: cpp
   :linenos:

   auto p{std::make_unique<Obstacle>(1)};
   auto q{std::move(p)};
   p = std::make_unique<Obstacle>(2);
   q = std::move(p);

- At the board, after each line: draw ``p`` and ``q`` on the stack, every ``Obstacle`` object on the heap, and an arrow from each pointer to the object it owns.
- On which line is the ``Obstacle`` object with id 1 deleted, and what deletes it? Nothing in the code says ``delete``.
- Check: ``702run week7_playground 61``.

The Tracker's List
""""""""""""""""""

.. code-block:: cpp

   std::vector<std::unique_ptr<Obstacle>> tracker;
   tracker.push_back(std::make_unique<Obstacle>(2, Pose{12.0, -1.0}, 4.0));
   auto track{std::make_unique<Obstacle>(1, Pose{20.0, -3.0}, 0.0, true)};
   tracker.push_back(std::move(track));  // track is now empty
   // tracker.push_back(track);          // does not compile: a copy
   for (const auto& t : tracker) {       // a copy would not compile
     std::cout << "obstacle " << t->id << ": " << t->speed << " m/s\n";
   }

- The tracker: the vector owns the pointers, and each pointer owns its ``Obstacle`` object. When ``tracker`` is destroyed, every ``Obstacle`` object is deleted.
- A temporary from ``std::make_unique`` moves in by itself. A named ``track`` needs ``std::move``. ``Pose{20.0, -3.0}``: ``heading`` takes its default, 0.
- Copying the whole vector does not compile either: it would copy every ``std::unique_ptr``.

See `unique_ptr to an Array`_ under Further Reading.

``release``
"""""""""""

.. code-block:: cpp

   auto track{std::make_unique<Obstacle>(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   Obstacle* raw{track.release()};  // gives up ownership
   // track == nullptr: true, raw->id: 2
   delete raw;  // you are the owner now: leave this out and it leaks

- ``release()`` hands the ``Obstacle`` object back as a plain pointer and forgets it.
- You are back where `An Obstacle on the Heap`_ started: an ``Obstacle*`` that must be deleted exactly once.
- Use it only to hand the object to code that takes ownership of a plain pointer. Otherwise, move the ``std::unique_ptr``.

.. note::

   C++20 **[unique.ptr.single.modifiers]** paragraphs 1 and 2: "Postconditions: get() == nullptr." "Returns: The value get() had at the start of the call to release."

.. _l7-unique-borrow:

Passing: Borrow
"""""""""""""""

.. code-block:: cpp

   void print_obstacle(const Obstacle& target);  // only reads it
   void set_speed(Obstacle* target, double speed) {      // may get nullptr
     if (target != nullptr) { target->speed = speed; }
   }

   auto track{std::make_unique<Obstacle>(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   print_obstacle(*track);       // 4 m/s
   set_speed(track.get(), 2.0);
   print_obstacle(*track);       // 2 m/s: the caller still owns it

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

Passing: Sink
"""""""""""""

.. code-block:: cpp

   std::vector<std::unique_ptr<Obstacle>> lost;      // lost tracks, kept
   void keep_lost(std::unique_ptr<Obstacle> track) {  // takes ownership
     lost.push_back(std::move(track));
   }

   auto track{std::make_unique<Obstacle>(2)};
   keep_lost(track);             // does not compile: a copy
   keep_lost(std::move(track));  // track == nullptr, lost.size() == 1

- By value: the parameter is a new owner, so the caller must hand the ``Obstacle`` object over with ``std::move``.
- F.18, from `A Parameter the Function Moves From`_, asks for ``&&`` here. Its own exception: a move-only type that is cheap to move, such as ``std::unique_ptr``, can be passed by value.

.. note::

   "Take a ``unique_ptr<widget>`` parameter to express that a function assumes ownership of a ``widget``". Rule: `Core Guidelines R.32 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-uniqueptrparam>`__.

Passing: Reseat
"""""""""""""""

.. code-block:: cpp

   void replace_track(std::unique_ptr<Obstacle>& track, int new_id) {
     track = std::make_unique<Obstacle>(new_id);
   }  // the assignment deleted the old Obstacle object

   auto track{std::make_unique<Obstacle>(2, Pose{12.0, -1.0, 0.0}, 4.0)};
   replace_track(track, 7);  // track->id: 7, track->speed: 0

- To **reseat** a pointer is to make it own, or point at, a different object. By reference to the ``std::unique_ptr``, the function may reseat the caller's pointer.
- The caller keeps ownership. Only what it owns changes.

.. note::

   "Take a ``unique_ptr<widget>&`` parameter to express that a function reseats the ``widget``". Rule: `Core Guidelines R.33 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-reseat>`__.

.. _l7-unique-returning:

Returning
"""""""""

.. code-block:: cpp

   std::unique_ptr<Obstacle> make_track(int id) {
     auto track{std::make_unique<Obstacle>(id)};
     return track;  // no std::move: L5's implicit move
   }

   std::unique_ptr<Obstacle> track{make_track(5)};  // track->id: 5

- A function that creates the object, such as ``make_track``, returns the ``std::unique_ptr`` by value. The caller becomes the owner.
- ``return track;`` compiles although ``std::unique_ptr`` cannot be copied: a local returned by value is moved, never copied (L5, and `Returning a Local`_).
- Compare `An Obstacle on the Heap`_: there, ``make_track`` returned an ``Obstacle*``, and nothing said who must delete it. Here the type says it.

Exercise 4: Lines That Compile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void inspect(const Obstacle& target);
   void adopt(std::unique_ptr<Obstacle> track);

   auto a{std::make_unique<Obstacle>(1)};
   auto b{std::make_unique<Obstacle>(2)};
   auto c{a};                                    // 1
   auto d{std::move(a)};                         // 2
   inspect(*d);                                  // 3
   adopt(b);                                     // 4
   adopt(std::move(b));                          // 5
   std::unique_ptr<Obstacle> e{new Obstacle{}};  // 6
   Obstacle* f{d.get()};                         // 7
   std::unique_ptr<Obstacle> g{f};               // 8

- For each line: does it compile? If it compiles, is it correct? Then check in ``702run week7_playground 68`` and its comments.

``std::shared_ptr``
^^^^^^^^^^^^^^^^^^^

A ``std::shared_ptr`` is one of several owners of an object on the heap. The owners share a count, and the last one to let go deletes the object.

.. figure:: /_static/images/l7/av_owner_map_shared.png
   :alt: A UML object diagram in black, with one part in orange: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner. In orange, with thick borders: tracker, the box with id 2, planner, and the two lines with open diamonds.
   :align: center
   :width: 80%

   Orange, from the map in `Who Owns Each Obstacle`_: the open diamonds, several owners.

See `cppreference: std::shared_ptr <https://en.cppreference.com/w/cpp/memory/shared_ptr>`__. Rule: `Core Guidelines R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`__.

A Hazard in Two Lists
"""""""""""""""""""""

The planner puts the cyclist, id 2, in its hazard list; the tracker keeps it too. Three ways to hold it, all wrong:

1. **A second** ``std::unique_ptr``: does not compile. One owner only (`One Owner Only`_).
2. **A copy of the** ``Obstacle``: two objects. The tracker's speed updates never reach the planner's copy.
3. **An** ``Obstacle*`` **from** ``get()``: the hazard list does not own it. When the track is lost, it points at freed memory (`Reminder: Three Ways to Get It Wrong`_).

.. code-block:: cpp

   std::vector<std::unique_ptr<Obstacle>> tracker;  // as on slide 62
   std::vector<Obstacle*> hazards;
   hazards.push_back(tracker[0].get());  // id 2: looks, does not own
   tracker.erase(tracker.begin());       // the track is lost: it dangles

The ``tracker`` here is the one from `The Tracker's List`_.

.. note::

   Both lists must own the ``Obstacle`` object with id 2, and it must be deleted when the last of them lets go.

.. _l7-shared-creating-one:

Creating One
""""""""""""

.. code-block:: cpp

   std::vector<std::shared_ptr<Obstacle>> tracker;
   std::vector<std::shared_ptr<Obstacle>> hazards;
   auto hazard{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   tracker.push_back(hazard);  // a copy: one more owner
   hazards.push_back(hazard);  // a copy: one more owner

.. code-block:: text

   hazard.use_count(): 3
   tracker[0] == hazards[0]: true

- A ``std::shared_ptr`` can be copied. Every copy is one more owner of the same ``Obstacle`` object, and ``use_count()`` counts them: ``hazard``, ``tracker[0]``, ``hazards[0]``.
- All three point at one ``Obstacle`` object: when the tracker updates its speed, the planner reads the new speed.

.. note::

   "Use ``make_shared()`` to make ``shared_ptr``\ s". Rule: `Core Guidelines R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`__.

The Control Block
"""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_memory.png
   :alt: On the left, two blue Stack boxes under name tags track and hazard, each holding two fields, object and control, each marked (ptr), with a measuring line of 16 bytes under each box. On the right, a red Heap box holds one allocation, with a measuring line reading one allocation, 64 bytes: at the top a control block with use_count 2 and weak_ptrs 0, then right below it the Obstacle object with id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. Green arrows run from each object field to the first row of the Obstacle object, id, and from each control field to the first row of the control block.
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

   auto track{std::make_shared<Obstacle>(2)};            // 1
   std::shared_ptr<Obstacle> hazard{track};              // 2: a copy
   std::shared_ptr<Obstacle> moved{std::move(hazard)};   // 2: a move
   moved.reset();                                        // 1

.. code-block:: text

   created: 1
   copied: 2
   moved: 2, hazard == nullptr: true
   reset: 1

- A move hands one owner's place to another: the count stays at 2, and ``hazard`` is left empty.
- ``reset()`` gives up this owner's place. The ``Obstacle`` object is deleted only when the count reaches 0.

Three Ways to Let Go
""""""""""""""""""""

.. code-block:: cpp

   auto track{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   {
     std::shared_ptr<Obstacle> hazard{track};  // 1
   }                                           // 2
   // three separate runs, each from 2:
   track = std::make_shared<Obstacle>(4);      // 3a
   track.reset();                              // 3b
                                    // 3c: track's scope ends

.. code-block:: text

   1: 2
   2: 1
   3a: track->id: 4, use_count: 1
   3b: track == nullptr: true

- An owner lets go when its scope ends (2, 3c), when it is assigned another pointer (3a), or when it calls ``reset()`` (3b). Each one subtracts 1 from the count.
- In all three, ``track`` is the last owner, so its ``Obstacle`` object is deleted: ``=`` and ``reset()`` swap it into a temporary that is destroyed (C++20 20.11.3.2 to 20.11.3.4).
- In 3a, id 4 is chosen; the rest take defaults. Run it: ``702run week7_playground 74``.

Step 1: Two Owners
""""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_1.png
   :alt: On the left, two blue Stack boxes under name tags track and hazard, each holding two fields, object and control, each marked (ptr). On the right, a red Heap box holds one allocation, measured as 64 bytes: at the top a control block with use_count 2 and weak_ptrs 0, then right below it an Obstacle object with id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. Green arrows run from each object field to the first row of the Obstacle object, id, and from each control field to the first row of the control block.
   :align: center
   :width: 100%

- After line 1 of `Three Ways to Let Go`_: ``hazard`` copies ``track``. Both hold the same two pointers, so ``use_count`` is 2.
- Each green arrow is one pointer of a ``std::shared_ptr``: ``object`` ends at the object's first member, ``control`` at the control block.

Step 2: One Owner
"""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_2.png
   :alt: On the left, a blue Stack box under the name tag track holds two fields, object and control, each marked (ptr). Below it, hazard is gray and dashed, marked scope ended, with no arrows. On the right, a red Heap box holds one allocation, measured as 64 bytes: a control block with use_count 1 and weak_ptrs 0, then the Obstacle object with id 2, pose {12.0, -1.0, 0.0}, speed 4.0 and is_static false. Green arrows run from track's object field to the object's first row, id, and from its control field to the control block's first row.
   :align: center
   :width: 100%

- Line 2: ``hazard``'s scope ends. Its destructor subtracts 1, so ``use_count`` is 1.
- ``track`` still owns the ``Obstacle`` object, so nothing is freed.

Step 3a: A New Object
"""""""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_3.png
   :alt: On the left, a blue Stack box under the name tag track holds two fields, object and control, each marked (ptr). Below it, hazard is gray and dashed, marked scope ended. On the right, a red Heap box holds a new allocation, measured as 64 bytes: a control block with use_count 1 and weak_ptrs 0, then an Obstacle object with id 4, pose {0.0, 0.0, 0.0}, speed 0.0 and is_static false. To its right, a gray dashed block marked freed: 64 bytes, the first control block and object. Green arrows run from track's object field to the new object's first row, id, and from its control field to the new control block's first row.
   :align: center
   :width: 100%

- 3a, 3b and 3c are separate runs, each from step 2.
- 3a: ``std::make_shared<Obstacle>(4)`` makes a second allocation. ``track`` lets go of the first: its count drops to 0, so its object is destroyed and its 64 bytes freed.

Step 3b: reset()
""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_4.png
   :alt: On the left, a blue Stack box under the name tag track holds two fields, object and control, each marked nullptr, with no arrows. Below it, hazard is gray and dashed, marked scope ended. On the right, a red Heap box holds one gray dashed block marked freed: 64 bytes, the control block and object.
   :align: center
   :width: 100%

- 3b: ``track.reset()`` leaves both of ``track``'s pointers ``nullptr``.
- ``track`` was the last owner, so the count drops to 0: the object is destroyed and the allocation freed.

Step 3c: The Scope Ends
"""""""""""""""""""""""

.. figure:: /_static/images/l7/av_shared_ptr_let_go_5.png
   :alt: On the left, track and hazard are both gray and dashed, marked scope ended, with no arrows. On the right, a red Heap box holds one gray dashed block marked freed: 64 bytes, the control block and object.
   :align: center
   :width: 100%

- 3c: ``track``'s scope ends, and its destructor runs.
- ``track`` was the last owner, so the count drops to 0: the object is destroyed and the allocation freed.

Deletion by the Last Owner
""""""""""""""""""""""""""

.. code-block:: cpp

   tracker.push_back(std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0));
   hazards.push_back(tracker[0]);
   tracker.clear();  // the track is lost; the planner still owns it
   hazards.clear();  // the last owner deletes the Obstacle

.. code-block:: text

   both lists: 2
   after tracker.clear(): 1, hazards[0]->id: 2
   after hazards.clear(): no owner left

- The hazard list keeps the ``Obstacle`` object alive after the tracker lets go. That is what the raw pointer of `A Hazard in Two Lists`_ could not do.
- Whichever list lets go last deletes the ``Obstacle`` object, and nothing leaks: ``702run week7_playground 80`` ends with no LeakSanitizer report.

.. _l7-shared-borrow:

Passing: Borrow
"""""""""""""""

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

Passing: Share
""""""""""""""

.. code-block:: cpp

   using Hazards = std::vector<std::shared_ptr<Obstacle>>;
   void add_hazard(Hazards& hazards, std::shared_ptr<Obstacle> hazard) {
     hazards.push_back(std::move(hazard));  // the list keeps this owner
   }

   Hazards hazards;
   auto track{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   add_hazard(hazards, track);
   std::cout << track.use_count() << '\n';  // 2

- By value: the parameter is one more owner. The function moves it into the list, so the list keeps that owner's place.
- ``using Hazards = ...;`` is a type alias (L2): a shorter name for the long type.

.. note::

   "Take a ``shared_ptr<widget>`` parameter to express shared ownership". Rule: `Core Guidelines R.34 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-owner>`__.

Passing: ``const shared_ptr&``
""""""""""""""""""""""""""""""

.. code-block:: cpp

   void add_if_close(Hazards& hazards,
                     const std::shared_ptr<Obstacle>& track) {
     if (track->pose.x < 25.0) {
       hazards.push_back(track);  // copies only when it keeps it
     }
   }

   add_if_close(hazards, near);  // x = 12 m: a hazard
   add_if_close(hazards, far);   // x = 38 m: not a hazard

.. code-block:: text

   near.use_count(): 2, far.use_count(): 1, hazards.size(): 1

- By ``const&``: the call adds no owner. The function copies the ``std::shared_ptr`` only if it decides to keep the ``Obstacle`` object.
- ``near``: id 2; ``far``: id 4. The 25 m limit is chosen for this example.

.. note::

   "Take a ``const shared_ptr<widget>&`` parameter to express that it might retain a reference count to the object" (a rule the Guidelines have not finished). Rule: `Core Guidelines R.36 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-const>`__.

.. _l7-shared-returning:

Returning
"""""""""

.. code-block:: cpp

   std::unique_ptr<Obstacle> make_track(int id);  // slide 67
   std::shared_ptr<Obstacle> hazard{make_track(5)};  // compiles
   std::unique_ptr<Obstacle> back{hazard};           // does not compile

.. code-block:: text

   error: no matching function for call to
   'std::unique_ptr<Obstacle>::unique_ptr(<brace-enclosed initializer list>)'

``make_track`` is the function from :ref:`l7-unique-returning`.

- A ``std::unique_ptr`` converts to a ``std::shared_ptr``: one owner becomes the first of several.
- Not the other way: other owners may exist, and a ``std::unique_ptr`` must be the only one.
- So a function that creates an ``Obstacle`` returns a ``std::unique_ptr``. The caller turns it into a ``std::shared_ptr`` if it needs to share.

``std::weak_ptr``
^^^^^^^^^^^^^^^^^

A ``std::weak_ptr`` watches an object that ``std::shared_ptr``\ s own. It never keeps the object alive, and it can tell whether the object still exists.

.. figure:: /_static/images/l7/av_owner_map_weak.png
   :alt: A UML object diagram in black, with one part in orange: seven boxes joined by lines, with nothing written on the lines. Across the top, three boxes each labeled : Obstacle, each listing four members: id = 1, pose = {20.0, -3.0, 0.00}, speed = 0.0, is_static = true; then id = 3, pose = {30.0, 2.5, 1.57}, speed = 1.4, is_static = false; then id = 4, pose = {38.0, 3.5, 3.14}, speed = 13.4, is_static = false. Below them, in the middle, a box labeled tracker. A line runs from each of the three top boxes down to tracker and ends in a filled diamond at tracker. Below tracker, a fourth : Obstacle box, listing id = 2, pose = {12.0, -1.0, 0.00}, speed = 4.0, is_static = false, joined to tracker by a line with an open diamond at tracker. On the left of the id 2 box, a box labeled dashboard, with an arrow from dashboard that ends in an arrowhead at the id 2 box, with no diamond. On its right, a box labeled planner, joined to it by a line with an open diamond at planner. In orange, with thick borders: the box with id 2, dashboard, and the arrow from dashboard.
   :align: center
   :width: 80%

   Orange, from the map in `Who Owns Each Obstacle`_: the arrow, a look without owning.

See `cppreference: std::weak_ptr <https://en.cppreference.com/w/cpp/memory/weak_ptr>`__. Rule: `Core Guidelines R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`__.

A Cycle
"""""""

Two more obstacles ahead in the ego lane: a tractor, id 5, at 60 m, towing a trailer, id 6, at 54 m, both at 8 m/s (chosen for this example).

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
- Each ``Towing`` object keeps the other alive: 2 × 80 bytes leak (`The Cycle, Measured`_).

The Cycle, Measured
"""""""""""""""""""

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
- ``702run week7_playground 89``: lines 37 and 38 are the two ``std::make_shared`` calls.
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

.. code-block:: text

   a.use_count(): 1, b.use_count(): 1

- A ``std::weak_ptr`` made from a ``std::shared_ptr`` does not add to the count.
- When ``a`` and ``b`` go out of scope, both counts reach 0 and both ``Towing`` objects are deleted. ``702run week7_playground 90``: no LeakSanitizer report.

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
- ``702run week7_playground 91``: ``obstacle 2: 4 m/s``, then, after the tracker and the planner let go, ``the obstacle is gone``.

See `A Dashboard of weak_ptr`_ under Further Reading.

``expired`` and ``use_count``
"""""""""""""""""""""""""""""

.. code-block:: cpp

   auto track{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   std::weak_ptr<Obstacle> shown{track};
   track.reset();  // the only owner lets go

.. code-block:: text

   shown.use_count(): 1, shown.expired(): false
   shown.use_count(): 0, shown.expired(): true

- ``use_count()`` counts the ``std::shared_ptr``\ s that own the ``Obstacle`` object. ``expired()`` is ``true`` when that count is 0.
- To use the object, call ``lock()`` and test the result. ``expired()`` then ``lock()`` is two steps, and another thread could make the last owner let go between them.

.. note::

   C++20 **[util.smartptr.weak.obs]** (20.11.4.5): ``expired()`` "Returns: use_count() == 0." ``lock()`` "Returns: expired() ? shared_ptr<T>() : shared_ptr<T>(\*this), executed atomically."

Exercise 5: Use Counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   auto track{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
   std::weak_ptr<Obstacle> shown{track};  // 1
   auto a{track};                         // 2
   auto b{std::move(a)};                  // 3
   std::weak_ptr<Obstacle> shown_2{b};    // 4
   track.reset();                         // 5
   b.reset();                             // 6

- After each numbered line: how many ``std::shared_ptr``\ s own the ``Obstacle`` object, and is ``shown`` expired?
- Check: ``702run week7_playground 93``.

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
     - `An Obstacle on the Heap`_ and `Reminder: Three Ways to Get It Wrong`_
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

- **Filled diamond**: the only owner. **Open diamond**: one of several owners. **Arrow, no diamond**: looks without owning.
- One ``std::vector`` holds one type: once the ``Obstacle`` object with id 2 is shared, the tracker holds a ``std::shared_ptr`` for every ``Obstacle`` object (:ref:`l7-shared-creating-one`).
- The ``Obstacle`` objects with ids 1, 3 and 4 still have one owner each, through that ``std::shared_ptr``.

Summary
-------

**Ownership**

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

   Obstacle* track{make_track(2, Pose{12.0, -1.0}, 4.0)};
   std::vector<Obstacle*> tracker{track};
   std::vector<Obstacle*> hazards{track};  // the same Obstacle
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

   Obstacle* track{make_track(2, Pose{12.0, -1.0}, 4.0)};
   std::vector<Obstacle*> tracker{track};
   std::vector<Obstacle*> hazards{track};
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

- `Handing a Path to the Controller`_ moved into a new vector. Here ``current`` already exists: the move gives up its old 3 poses and takes the 1000 of ``next``, without copying them (same ``data()``).
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
     std::unique_ptr<Obstacle, decltype(say_and_delete)> track{
         new Obstacle{2}, say_and_delete};
     // sizeof(track): 8
   }  // prints: deleting obstacle 2

- The second template argument is the deleter (`One Owner Only`_). Here a lambda (L6) that prints first.
- ``std::make_unique`` cannot take a deleter, so the code calls ``new`` and hands the result to the ``std::unique_ptr`` in the same statement.
- A lambda with no captures adds no bytes: 8. A function pointer as the deleter makes it 16 (measured).

.. note::

   Rule: `Core Guidelines R.12 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-immediate-alloc>`__, "Immediately give the result of an explicit resource allocation to a manager object".

``std::auto_ptr``
^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::auto_ptr<Obstacle> a{new Obstacle{2}};
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

   std::unique_ptr<Obstacle> track;  // empty
   // track == nullptr: true
   track = std::make_unique<Obstacle>(2);
   if (track) {
     std::cout << "obstacle " << track->id << '\n';  // obstacle 2
   }
   auto other{std::move(track)};  // !track: true
   bool has_track = other;  // does not compile

.. code-block:: text

   error: cannot convert 'std::unique_ptr<Obstacle, std::default_delete<Obstacle> >'
          to 'bool' in initialization

- ``if (track)``, ``!track`` and ``track == nullptr`` all test for empty. The same works for ``std::shared_ptr``.
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

   auto first{std::make_unique<Obstacle>(2)};
   auto second{std::make_unique<Obstacle>(4)};
   const Obstacle* id_2{first.get()};
   first.swap(second);  // the same as std::swap(first, second)
   // first->id: 4, second->id: 2, second.get() == id_2: true

- ``swap`` exchanges the two stored pointers. No ``Obstacle`` object is created, copied or deleted: the one with id 2 stays at the same address, now owned by ``second``.
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
- The dashboard never keeps an ``Obstacle`` object alive. L4's ``std::erase_if`` with a lambda (L6) drops the entries whose object is gone.

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
