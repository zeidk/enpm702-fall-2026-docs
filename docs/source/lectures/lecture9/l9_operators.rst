.. _l9_operators:

====================================================
Operator Overloading
====================================================

This page is **required reading** after the Lecture 9 class. It is not presented in class. A slide of Lecture 9, in Compile-Time Polymorphism, links to it. In class, the compiler picks one of several functions with the same name from the types of the arguments. This page applies the same rule to operators: you write a function named ``operator<<`` or ``operator<``, and the compiler calls it when it sees ``<<`` or ``<`` with your type. You write three operators for the classes of the robotaxi program: ``operator<<`` to print a ``Position``, and ``operator<`` and ``operator>`` to compare two ``Route`` objects by length.

.. dropdown:: Code for This Page
   :icon: terminal
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The code of this page is one program in the course repository, ``week9_operators``, in the folder ``project/week9/operators/``. Each part of the page has its own source file in ``operators/src/``, named after the part's **key**: the code of :ref:`l9op-print` is in ``print.cpp``, and its key is ``print``. Each listing on this page shows the line numbers of its file, so "line 21" under ``print.cpp`` is line 21 of ``print.cpp``.

   ``Position`` and ``Route`` are the classes of ``project/week9/common``, in the namespace ``fleet``, with the operators of this page added. The program keeps its own copy of both, in ``operators/include`` and ``operators/src``, so it builds on its own. Each file of `Common Mistakes`_ has its own small ``Position`` or ``Route``, in a namespace named after the key, so that it does not clash with ``fleet``'s. A compiler message names a class with its namespace: ``member_output::Position``.

   Build the program, then run one part by its key, with the ``702`` commands of the :doc:`lecture page <l9_lecture>`:

   .. code-block:: bash

      702build week9_operators
      702run week9_operators print

   The keys, in the order of this page:

   - ``calls``: `What an Operator Overload Is`_.
   - ``print``: :ref:`l9op-print`.
   - ``compare``: :ref:`l9op-compare`.
   - ``member_output``: :ref:`l9op-member-output`.
   - ``by_value``: `Returning the Stream by Value`_.
   - ``no_const``: `A Comparison Without const`_.

   ``702run week9_operators`` with no key runs every part.

What an Operator Overload Is
----------------------------

For two ``int`` values, ``a + b`` uses the ``+`` built into the language. For an object of a class, nothing is built in. The compiler looks for a function named ``operator+`` and calls it. Such a function is an **operator function**: its name is the word ``operator`` followed by the symbol of the operator. Writing one for your own type is **operator overloading**. The copy assignment of a class, ``Vehicle& operator=(const Vehicle& other)``, is an operator function you have already seen.

An operator function can be a member of the class of the left operand, or a free function (a function that is not a member of any class). The standard says how the compiler turns ``x @ y`` into a call, where ``@`` stands for any binary operator, one with two operands:

.. note::

   "For an expression x @ y with subexpressions x and y, the operator function is selected by overload resolution (12.4.1.2). If a member function is selected, the expression is interpreted as x . operator @ ( y ) Otherwise, if a non-member function is selected, the expression is interpreted as operator @ ( x , y )". C++20 **[over.binary]** (12.6.2) paragraph 1.

So ``a < b`` is ``a.operator<(b)`` when the compiler picks a member function, and ``operator<(a, b)`` when it picks a free function. You can write either form yourself. The standard library has both kinds, and this program calls each one twice, once with the operator and once by its name:

.. code-block:: cpp
   :caption: ``operators/src/calls.cpp``, lines 16 to 27
   :lineno-start: 16

   namespace calls {
   void run() {
     const std::string kind{"robo"};
     const std::string vehicle{"taxi"};
     std::cout << kind + vehicle << '\n';            // a free function of <string>
     std::cout << operator+(kind, vehicle) << '\n';  // the same call, by its name
     std::cout << 500 << '\n';                       // a member of std::ostream
     std::cout.operator<<(500) << '\n';              // the same call, by its name
     std::cout << "m\n";                             // a free function of <ostream>
     operator<<(std::cout, "m\n");                   // the same call, by its name
   }
   }  // namespace calls

``702run week9_operators calls`` prints each line twice:

.. code-block:: text

   robotaxi
   robotaxi
   500
   500
   m
   m

- **Lines 20 and 21.** The ``+`` of two ``std::string`` objects is a free function, ``operator+``, so line 21 calls it with both strings as arguments.
- **Lines 22 and 23.** ``std::cout`` is a ``std::ostream``, and the ``<<`` that prints an ``int`` is a member of ``std::ostream``: ``basic_ostream<charT, traits>& operator<<(int n);`` in the class, C++20 **[ostream]** (29.7.5.1). So line 23 calls it on ``std::cout``, with a dot.
- **Lines 24 and 25.** The ``<<`` that prints a C string, such as ``"m\n"``, is a free function of ``<ostream>``, with the stream as its first parameter, C++20 **[ostream.inserters.character]** (29.7.5.2.4). So line 25 passes ``std::cout`` as the first argument.

``<<`` is one name for many functions: one for ``int``, one for ``double``, one for a C string, and more. The compiler picks the one whose parameters match the types of the operands, as it does for any overloaded function. That is compile-time polymorphism. ``operator<<`` for a ``Position``, below, adds one more function to the set.

Which Operators You Can Overload
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C++20 **[over.oper]** (12.6) paragraph 1 lists every operator that can have an operator function:

.. code-block:: text

   new      delete   new[]    delete[] co_await ( )      []       ->       ->*
   ~        !        +        -        *        /        %        ^        &
   |        =        +=       -=       *=       /=       %=       ^=       &=
   |=       ==       !=       <        >        <=       >=       <=>      &&
   ||       <<       >>       <<=      >>=      ++       --       ,

Four cannot:

.. note::

   "The following operators cannot be overloaded: ``.`` ``.*`` ``::`` ``?:`` nor can the preprocessing symbols ``#`` (15.6.2) and ``##`` (15.6.3)". C++20 **[over.oper]** (12.6) paragraph 3, a note.

That is member access (``vehicle.drive``), member access through a pointer to member (``.*``), the scope operator (``fleet::Route``) and the conditional operator (``a ? b : c``).

Paragraph 7 sets two more limits:

.. important::

   "An operator function shall either be a non-static member function or be a non-member function that has at least one parameter whose type is a class, a reference to a class, an enumeration, or a reference to an enumeration. It is not possible to change the precedence, grouping, or number of operands of operators". C++20 **[over.oper]** (12.6) paragraph 7.

- At least one operand is your type. You cannot change what ``+`` does for two ``int`` values.
- You keep the operator's precedence and its number of operands. A ``<`` you write still has two operands, and ``a + b < c`` still means ``(a + b) < c``.

.. _l9op-print:

``operator<<`` for ``Position``
-------------------------------

``std::cout << p`` does not compile for a ``Position`` until you write the function it calls. Here is the ``Position`` of ``project/week9/common``, with that function declared next to it:

.. code-block:: cpp
   :caption: ``operators/include/position.hpp``, lines 14 to 25
   :lineno-start: 14

   namespace fleet {

   /// A point on the map.
   struct Position {
     double x{0.0};  ///< m, east
     double y{0.0};  ///< m, north
   };

   /// Prints p as (x, y) and returns the stream, so that calls can be chained.
   std::ostream& operator<<(std::ostream& out, const Position& p);

   }  // namespace fleet

.. code-block:: cpp
   :caption: ``operators/src/position.cpp``, lines 9 to 16
   :lineno-start: 9

   namespace fleet {

   std::ostream& operator<<(std::ostream& out, const Position& p) {
     out << '(' << p.x << ", " << p.y << ')';
     return out;
   }

   }  // namespace fleet

Line 12 prints the two coordinates with the ``<<`` that already exist for ``char``, ``double`` and C strings. Line 13 returns the stream it was given.

.. code-block:: cpp
   :caption: ``operators/src/print.cpp``, lines 16 to 24
   :lineno-start: 16

   namespace print {
   void run() {
     const fleet::Position start{0.0, 0.0};
     const fleet::Position end{300.0, 400.0};
     std::cout << end << '\n';
     std::cout << "maya_ride: " << start << " to " << end << '\n';
     operator<<(std::cout, end) << '\n';  // std::cout << end, by its name
   }
   }  // namespace print

``start`` and ``end`` are the two ends of ``maya_ride``, the 500 m route of the lecture. ``702run week9_operators print`` prints:

.. code-block:: text

   (300, 400)
   maya_ride: (0, 0) to (300, 400)
   (300, 400)

- **Line 20** calls the ``operator<<`` of ``position.cpp``, with ``std::cout`` as ``out`` and ``end`` as ``p``. A ``double`` that holds 300.0 prints as ``300``: the stream drops the zeros after the point.
- **Line 21** chains four ``<<``: `Why It Returns the Stream`_.
- **Line 22** makes the call of line 20 by its name, as ``calls.cpp`` does for the standard library. It prints the same thing.

``print.cpp`` is in the namespace ``print``, not ``fleet``, and still finds the ``operator<<`` of ``fleet``. For a function call or an operator, the compiler also looks in the namespaces of the types of the arguments. That is **argument-dependent lookup**, C++20 **[basic.lookup.argdep]** (6.5.2). ``end`` is a ``fleet::Position``, so the compiler looks in ``fleet``. Declare the ``operator<<`` of a type in the same namespace as the type, as line 23 of ``position.hpp`` does.

Why It Is a Free Function
^^^^^^^^^^^^^^^^^^^^^^^^^

A member operator function belongs to the class of the **left** operand. The standard says where the compiler looks for one, where ``T1`` is the type of the left operand:

.. note::

   "If T1 is a complete class type or a class currently being defined, the set of member candidates is the result of the qualified lookup of T1::operator@ (12.4.1.1.1); otherwise, the set of member candidates is empty". C++20 **[over.match.oper]** (12.4.1.2) paragraph 3.1.

In ``std::cout << end``, the left operand is ``std::cout``, a ``std::ostream``. A member would have to be ``std::ostream::operator<<(const Position&)``, inside a class of the standard library, which you cannot change. So the function is a free function with two parameters: the stream first, because it is on the left, and the ``Position`` second. :ref:`l9op-member-output` shows what happens when you make it a member of ``Position`` instead.

.. note::

   cppreference says the same about ``<<`` and ``>>`` with a stream on the left: "Since they take the user-defined type as the right argument (b in a @ b), they must be implemented as non-members". `cppreference: operator overloading <https://en.cppreference.com/w/cpp/language/operators>`__.

Why It Returns the Stream
^^^^^^^^^^^^^^^^^^^^^^^^^

"The shift operators << and >> group left-to-right". C++20 **[expr.shift]** (7.6.7) paragraph 1. So line 21 of ``print.cpp`` runs as:

.. code-block:: cpp

   ((((std::cout << "maya_ride: ") << start) << " to ") << end) << '\n';

1. ``std::cout << "maya_ride: "`` prints the text and returns ``std::cout``.
2. That ``std::cout`` is the left operand of the next ``<<``: ``std::cout << start`` calls the ``operator<<`` of ``Position``, which prints ``(0, 0)`` and returns ``out``, which is ``std::cout``.
3. The next three ``<<`` work the same way, each on the stream the previous one returned.

If the function returned nothing (``void``), step 2 would give the next ``<<`` no left operand, and the line would not compile. The function returns a **reference**, ``std::ostream&``, so each step hands on ``std::cout`` itself, not a copy of it. A stream cannot be copied: `Returning the Stream by Value`_.

Why ``const Position&``
^^^^^^^^^^^^^^^^^^^^^^^

- ``const Position& p``: a reference, so the call copies no ``Position``. ``const``, so the function cannot change ``p``, and it accepts a ``const Position``: ``start`` and ``end`` are ``const`` (lines 18 and 19 of ``print.cpp``).
- ``std::ostream& out``: a reference that is **not** ``const``. Printing changes the stream: it adds characters to it, and it sets the stream's error flags when the output fails.

.. _l9op-compare:

``operator<`` and ``operator>`` for ``Route``
---------------------------------------------

A ``Route`` is shorter than another when its ``length()`` is smaller. ``operator<`` and ``operator>`` say that in code:

.. code-block:: cpp
   :caption: ``operators/include/route.hpp``, lines 15 to 32
   :lineno-start: 15

   /// The waypoints of one trip, in order.
   class Route {
    public:
     /// Adds a waypoint at the end of the route.
     void add(Position waypoint);

     /// The length of the route, in m: the sum of the straight segments.
     [[nodiscard]] double length() const;

     /// True when this route is shorter than other.
     [[nodiscard]] bool operator<(const Route& other) const;

     /// True when this route is longer than other.
     [[nodiscard]] bool operator>(const Route& other) const;

    private:
     std::vector<Position> waypoints_;
   };

.. code-block:: cpp
   :caption: ``operators/src/route.cpp``, lines 25 to 31
   :lineno-start: 25

   bool Route::operator<(const Route& other) const {
     return length() < other.length();
   }

   bool Route::operator>(const Route& other) const {
     return other < *this;  // a > b is b < a
   }

``add`` and ``length`` are those of ``project/week9/common``: ``length()`` adds up the straight distance between each waypoint and the next.

Member or Free
^^^^^^^^^^^^^^

Here the left operand is a ``Route``, a class you write, so a member works: ``a < b`` is ``a.operator<(b)``. Inside the function, ``*this`` is ``a``, and ``other`` is ``b``. A member takes one parameter, for the right operand.

A free function works too:

.. code-block:: cpp

   bool operator<(const Route& a, const Route& b);  // in namespace fleet

It takes two parameters, one per operand, and compares ``a.length()`` with ``b.length()``. It can, because ``length()`` is ``public``. This page uses members, so that you see both kinds: ``operator<<`` must be free, and ``operator<`` may be a member.

Why Both Are const
^^^^^^^^^^^^^^^^^^

The ``const`` at the end of lines 25 and 28 of ``route.hpp`` says that the method does not change the ``Route`` it is called on. Comparing two routes changes neither, so both are ``const`` methods, as ``length()`` is. Without it, you cannot compare a ``const Route``, such as a ``const Route&`` parameter. ``operator>`` depends on it too: in ``other < *this`` (line 30 of ``route.cpp``), the left operand is ``other``, a ``const Route&``, so ``operator<`` must be ``const``. `A Comparison Without const`_ shows the error.

Why ``>`` Is Written With ``<``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``a > b`` is true exactly when ``b < a`` is. So line 30 of ``route.cpp`` swaps the operands and calls ``operator<``. The rule "shorter by length" is then written in one place, line 26. If you later compare routes by drive time, you change ``operator<`` only, and ``operator>`` follows.

.. note::

   "Typically, once operator< is provided, the other relational operators are implemented in terms of operator<". `cppreference: operator overloading <https://en.cppreference.com/w/cpp/language/operators>`__.

The compiler does not write ``operator>`` for you from ``operator<``. Delete ``operator>`` from ``route.hpp`` and ``route.cpp`` and build: g++ 13.3 stops at the first ``>`` of ``compare.cpp`` (folders cut to ``...``):

.. code-block:: text

   .../compare.cpp:45:59: error: no match for ‘operator>’ (operand types are ‘fleet::Route’ and ‘fleet::Route’)

Compare Three Routes, Then Sort Them
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp
   :caption: ``operators/src/compare.cpp``, lines 20 to 54
   :lineno-start: 20

   namespace compare {
   namespace {
   void print_lengths(std::string_view label, const std::vector<fleet::Route>& rides) {
     std::cout << label;
     for (const fleet::Route& ride : rides) {
       std::cout << ' ' << ride.length();
     }
     std::cout << '\n';
   }
   }  // namespace

   void run() {
     fleet::Route maya_ride;  // 500 m
     maya_ride.add(fleet::Position{0.0, 0.0});
     maya_ride.add(fleet::Position{300.0, 400.0});
     fleet::Route airport_ride;  // 1000 m
     airport_ride.add(fleet::Position{0.0, 0.0});
     airport_ride.add(fleet::Position{600.0, 800.0});
     fleet::Route campus_ride;  // 300 m north, then 400 m east: 700 m
     campus_ride.add(fleet::Position{0.0, 0.0});
     campus_ride.add(fleet::Position{0.0, 300.0});
     campus_ride.add(fleet::Position{400.0, 300.0});

     std::cout << std::boolalpha;
     std::cout << "maya_ride < airport_ride: " << (maya_ride < airport_ride) << '\n';
     std::cout << "maya_ride > airport_ride: " << (maya_ride > airport_ride) << '\n';
     std::cout << "maya_ride.operator<(airport_ride): "
               << maya_ride.operator<(airport_ride) << '\n';

     std::vector<fleet::Route> rides{airport_ride, maya_ride, campus_ride};
     print_lengths("before std::sort:", rides);
     std::sort(rides.begin(), rides.end());  // calls Route::operator<
     print_lengths("after std::sort: ", rides);
   }
   }  // namespace compare

The waypoints are chosen for the example, so that the lengths are round numbers:

1. ``maya_ride``, lines 32 to 34: one segment from (0, 0) to (300, 400). Its length is the square root of 300 × 300 + 400 × 400 = 250000, which is 500 m.
2. ``airport_ride``, lines 35 to 37: one segment from (0, 0) to (600, 800). The square root of 600 × 600 + 800 × 800 = 1000000 is 1000 m.
3. ``campus_ride``, lines 38 to 41: 300 m north to (0, 300), then 400 m east to (400, 300). 300 + 400 = 700 m.

``702run week9_operators compare`` prints:

.. code-block:: text

   maya_ride < airport_ride: true
   maya_ride > airport_ride: false
   maya_ride.operator<(airport_ride): true
   before std::sort: 1000 500 700
   after std::sort:  500 700 1000

- **Line 44**: 500 is less than 1000, so ``maya_ride < airport_ride`` is ``true``.
- **Line 45**: ``maya_ride > airport_ride`` runs ``airport_ride < maya_ride``, and 1000 is not less than 500: ``false``.
- **Lines 46 and 47** call the ``operator<`` of line 44 by its name, with a dot, because it is a member.
- **Line 49** puts the three routes in a vector, in the order 1000, 500, 700 m. **Line 51** sorts them, and line 52 prints them from the shortest to the longest.

``std::sort`` Uses ``operator<``
""""""""""""""""""""""""""""""""

Line 51 passes ``std::sort`` no rule for the order. It then compares two elements with ``<``, which for a ``Route`` calls ``Route::operator<``:

.. note::

   "For all algorithms that take Compare, there is a version that uses operator< instead. That is, comp(\*i, \*j) != false defaults to \*i < \*j != false". C++20 **[alg.sorting]** (25.8) paragraph 3.

So writing ``operator<`` is enough to sort a ``std::vector<fleet::Route>``. Without it, line 51 does not compile: g++ 13.3 then says ``no match for ‘operator<’``, from inside the standard library.

The same paragraph asks the ``<`` to be a **strict weak ordering**. In plain words: no route is shorter than itself, and if ``a`` is shorter than ``b`` and ``b`` shorter than ``c``, then ``a`` is shorter than ``c``. Comparing lengths with ``<`` meets both. Two routes with the same length are **equivalent** (paragraph 7): neither is shorter than the other. ``std::sort`` does not promise which of the two comes first; ``std::stable_sort`` keeps them in their order, C++20 **[stable.sort]** (25.8.1.2).

C++20: Three-Way Comparison
---------------------------

.. admonition:: Further Reading
   :class: note

   This part is for your own reading. The course writes ``operator<`` and ``operator>`` as above.

   C++20 adds one more operator, ``<=>``, the **three-way comparison**: "The expression p <=> q is a prvalue indicating whether p is less than, equal to, greater than, or incomparable with q". C++20 **[expr.spaceship]** (7.6.8) paragraph 2. One comparison gives one of those four answers.

   - When a class writes ``operator<=>``, the compiler uses it for ``<``, ``>``, ``<=`` and ``>=``: "For the relational (7.6.9) operators, the rewritten candidates include all non-rewritten candidates for the expression x <=> y". C++20 **[over.match.oper]** (12.4.1.2) paragraph 3.4.1. That is why ``operator>`` above has to be written by hand: ``Route`` has an ``operator<``, but no ``operator<=>``.
   - A class can ask the compiler to write ``operator<=>`` with ``= default``. The compiler's version compares the data members one by one, in order, and stops at the first pair that differs, C++20 **[class.spaceship]** (11.11.3) paragraph 3. For ``Route``, that would compare the waypoints, not the lengths, so ``Route`` would still write its own.

   `cppreference: Default comparisons (since C++20) <https://en.cppreference.com/w/cpp/language/default_comparisons>`__ covers ``<=>`` and ``= default`` with examples.

Common Mistakes
---------------

Each mistake below was compiled with g++ 13.3 and the course flags (``-std=c++20 -Wall -Wextra -pedantic-errors -Wshadow``). The code that does not compile is commented out in its file, so the program builds. Uncomment it and run ``702build week9_operators`` to see the message. Folder names are cut to ``...``, and lines that only name the included files are left out. Comment the code out again before you go on.

.. _l9op-member-output:

``operator<<`` as a Member Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This ``Position`` makes ``operator<<`` a member function:

.. code-block:: cpp
   :caption: ``operators/src/member_output.cpp``, lines 16 to 34
   :lineno-start: 16

   namespace member_output {
   struct Position {
     double x{0.0};
     double y{0.0};
     std::ostream& operator<<(std::ostream& out) const;  // a member: wrong
   };

   std::ostream& Position::operator<<(std::ostream& out) const {
     out << '(' << x << ", " << y << ')';
     return out;
   }

   void run() {
     const Position end{300.0, 400.0};
     // std::cout << end << '\n';  // does not compile
     end << std::cout;  // compiles: end.operator<<(std::cout)
     std::cout << '\n';
   }
   }  // namespace member_output

A member operator function belongs to the left operand (`Why It Is a Free Function`_). This one is a member of ``Position``, so it runs only when a ``Position`` is on the left: ``end << std::cout``, line 31, which is ``end.operator<<(std::cout)``. ``702run week9_operators member_output`` prints:

.. code-block:: text

   (300, 400)

The stream is on the wrong side, and no one reads code written that way. Uncomment line 30, the line you would write, and g++ says:

.. code-block:: text

   .../member_output.cpp: In function ‘void member_output::run()’:
   .../member_output.cpp:30:13: error: no match for ‘operator<<’ (operand types are ‘std::ostream’ {aka ‘std::basic_ostream<char>’} and ‘const member_output::Position’)
      30 |   std::cout << end << '\n';  // does not compile
         |   ~~~~~~~~~ ^~ ~~~
         |        |       |
         |        |       const member_output::Position
         |        std::ostream {aka std::basic_ostream<char>}

- The left operand is a ``std::ostream`` and the right one a ``const member_output::Position``. No ``operator<<`` takes them in that order.
- The full message is 338 lines long. After these lines, g++ lists the 47 ``operator<<`` it tried: the members of ``std::ostream`` and the free functions of the standard library. ``Position::operator<<`` is not among them: it would need a ``Position`` on the left.

The fix is the free function of :ref:`l9op-print`.

Returning the Stream by Value
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This ``operator<<`` returns ``std::ostream``, without the ``&``:

.. code-block:: cpp
   :caption: ``operators/src/by_value.cpp``, lines 15 to 27
   :lineno-start: 15

   namespace by_value {
   struct Position {
     double x{0.0};
     double y{0.0};
   };

   // std::ostream operator<<(std::ostream& out, const Position& p) {  // no &
   //   out << '(' << p.x << ", " << p.y << ')';
   //   return out;  // does not compile: this line copies the stream
   // }

   void run() { print_commented_out("operators/src/by_value.cpp"); }
   }  // namespace by_value

``702run week9_operators by_value`` prints where the code is:

.. code-block:: text

   This part's code does not compile, so it is commented out in
   operators/src/by_value.cpp. Uncomment it and build to see the message.

Uncomment lines 21 to 24, and g++ says:

.. code-block:: text

   .../by_value.cpp: In function ‘std::ostream by_value::operator<<(std::ostream&, const Position&)’:
   .../by_value.cpp:23:10: error: use of deleted function ‘std::basic_ostream<_CharT, _Traits>::basic_ostream(const std::basic_ostream<_CharT, _Traits>&) [with _CharT = char; _Traits = std::char_traits<char>]’
      23 |   return out;  // does not compile: this line copies the stream
         |          ^~~
   /usr/include/c++/13/ostream:438:7: note: declared here
     438 |       basic_ostream(const basic_ostream&) = delete;
         |       ^~~~~~~~~~~~~

- To return ``std::ostream`` by value, line 23 must make a new ``std::ostream`` from ``out``, with the copy constructor of ``std::ostream``.
- That copy constructor is **deleted**: ``basic_ostream(const basic_ostream&) = delete;``, in the class ``basic_ostream`` of C++20 **[ostream]** (29.7.5.1). ``std::ostream`` is ``basic_ostream<char>``, which is what ``_CharT = char`` says. So a stream cannot be copied.

The fix is the ``&``: ``std::ostream& operator<<(...)`` returns ``out`` itself, and copies nothing.

A Comparison Without const
^^^^^^^^^^^^^^^^^^^^^^^^^^

This ``Route`` is cut down to its length, so that the file stays short. Its ``operator<`` has no ``const`` at the end:

.. code-block:: cpp
   :caption: ``operators/src/no_const.cpp``, lines 17 to 38
   :lineno-start: 17

   namespace no_const {
   class Route {  // only its length, in m
    public:
     explicit Route(double length) : length_{length} {}
     bool operator<(const Route& other);  // no const at the end: wrong

    private:
     double length_;
   };

   bool Route::operator<(const Route& other) { return length_ < other.length_; }

   // bool is_shorter(const Route& a, const Route& b) {
   //   return a < b;  // does not compile: a is const
   // }

   void run() {
     Route maya_ride{500.0};
     Route airport_ride{1000.0};
     std::cout << std::boolalpha << (maya_ride < airport_ride) << '\n';
   }
   }  // namespace no_const

``maya_ride`` and ``airport_ride`` are not ``const``, so line 36 compiles. ``702run week9_operators no_const`` prints:

.. code-block:: text

   true

``is_shorter``, lines 29 to 31, takes its routes by ``const`` reference, as a function that only reads a ``Route`` should. Uncomment it, and g++ says:

.. code-block:: text

   .../no_const.cpp: In function ‘bool no_const::is_shorter(const Route&, const Route&)’:
   .../no_const.cpp:30:14: error: passing ‘const no_const::Route’ as ‘this’ argument discards qualifiers [-fpermissive]
      30 |   return a < b;  // does not compile: a is const
         |              ^
   .../no_const.cpp:27:6: note:   in call to ‘bool no_const::Route::operator<(const no_const::Route&)’
     27 | bool Route::operator<(const Route& other) { return length_ < other.length_; }
         |      ^~~~~

- ``a < b`` is ``a.operator<(b)``, so ``a`` becomes ``*this`` inside ``operator<``, and ``this`` points at ``a``.
- ``a`` is ``const``, but ``operator<`` is not a ``const`` method: it could change ``*this``. Calling it on ``a`` would **discard** (drop) the ``const`` of ``a``, which C++ does not allow.
- ``b`` is no problem: it binds to the parameter ``other``, which is a ``const Route&``.

The fix is ``const`` at the end of the declaration and of the definition: ``bool operator<(const Route& other) const;``, as in ``route.hpp``.

What to Write
-------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Operator
     - Member or free
     - Declaration, for a class ``T``
   * - ``<<`` with a stream
     - Free, in the namespace of ``T``
     - ``std::ostream& operator<<(std::ostream& out, const T& t);`` It returns ``out``.
   * - ``<``
     - Member or free
     - ``bool operator<(const T& other) const;`` as a member.
   * - ``>``
     - Member or free
     - ``bool operator>(const T& other) const;`` as a member, with the body ``return other < *this;``.

- An operator function keeps the meaning of its operator: ``<`` means "comes before", and ``<<`` with a stream means "print".
- A comparison changes neither operand: ``const`` on the method, ``const T&`` for the parameter.
- ``operator<`` is enough for ``std::sort``.
