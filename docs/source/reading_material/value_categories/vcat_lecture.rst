====================================================
Lecture
====================================================


.. note::

   **Running the examples.** Every example on this page is in the
   program ``week7_value_categories`` of the course repository, in
   `project/week7/value_categories <https://github.com/zeidk/enpm702-fall-2026-cpp/blob/main/project/week7/value_categories>`__. Pull, then build and run it.
   Each part of the page has a key, and the program runs one part when you
   pass its key:

   .. code-block:: bash

      702build week7_value_categories
      702run week7_value_categories            # every part, except dangling
      702run week7_value_categories examples   # only the Worked Examples

   The keys, in the order of the page: ``helper``, ``examples``,
   ``traps``, ``dangling``, ``overloads`` and ``exercises``. To test an
   expression of your own, use `The CATEGORY Helper`_, a complete program
   you can copy into a file.

   Every category on this page was checked with ``static_assert`` on g++
   13.3 with the course flags, ``-std=c++20 -Wall -Wextra -pedantic-errors
   -Wshadow``. Every output and compiler message on this page was copied
   from that compiler.


Three Categories, Two Groups
====================================================

.. figure:: /_static/images/l7/value_categories.png
   :alt: A tree of rounded boxes. At the top, expression. Below it, two boxes joined to it: glvalue on the left, with the label has identity, and rvalue on the right, with the label may be taken. On the bottom row, three boxes: lvalue on the left, joined to glvalue; xvalue in the middle, joined to both glvalue and rvalue; and prvalue on the right, joined to rvalue. The drawing is symmetric about the middle line through expression and xvalue.
   :align: center
   :width: 60%

   The value categories, from Lecture 7.

Every expression in C++ has a **type** and a **value category**. There
are three categories: **lvalue**, **xvalue** and **prvalue**. Every
expression is exactly one of the three.

The two boxes in the middle row of the tree are not categories of their
own. Each one is a name for two of the three bottom boxes together:

- A **glvalue** is an lvalue or an xvalue.
- An **rvalue** is an xvalue or a prvalue.

So the question "is this expression an rvalue, a prvalue or an xvalue?"
mixes two rows of the tree. An rvalue is always a prvalue or an xvalue,
never a third thing. Ask instead which of the three bottom boxes the
expression is in. That answer also tells you whether it is a glvalue and
whether it is an rvalue:

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Category
     - Also a glvalue?
     - Also an rvalue?
   * - lvalue
     - yes
     - no
   * - xvalue
     - yes
     - yes
   * - prvalue
     - no
     - yes

.. note::

   C++20 **[basic.lval]** (7.2.1) paragraph 1: "An lvalue is a glvalue
   that is not an xvalue". "An rvalue is a prvalue or an xvalue".
   Paragraph 2: "Every expression belongs to exactly one of the
   fundamental classifications in this taxonomy: lvalue, xvalue, or
   prvalue".


Two Questions
-------------

The category answers two questions about an expression:

1. **Does it refer to an object that already exists?** An **object** is a
   piece of memory that holds a value. When the answer is yes, the
   object has an address, and the expression is a glvalue. The tree
   calls this "has identity".
2. **May another object take its contents?** To **take** the contents is
   to move them into another object, as the move constructor of
   ``std::vector`` does in Lecture 7: the new vector gets the block on the
   heap, and no element is copied. When the answer is yes, the
   expression is an rvalue.

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Refers to an object that already exists?
     - May another object take its contents?
     - Category
     - Example
   * - yes
     - no
     - lvalue
     - ``path``
   * - yes
     - yes
     - xvalue
     - ``std::move(path)``
   * - no
     - yes
     - prvalue
     - ``make_path(3)``

There is no fourth row. An expression that refers to no object only
computes a value, and nothing else in the program can use that value, so
another object may always take it.


One Object, Three Expressions
-----------------------------

.. code-block:: cpp
   :linenos:

   std::vector<Pose> path{make_path(3)};      // make_path(3): prvalue
   std::vector<Pose> copied{path};            // path: lvalue
   std::vector<Pose> taken{std::move(path)};  // std::move(path): xvalue

- Line 1: ``make_path(3)`` computes a new vector. No object held it
  before, so it is a prvalue, and ``path`` takes it.
- Line 2: ``path`` refers to the vector from line 1. Nothing marks it, so
  ``copied`` gets a copy, and ``path`` keeps its 3 poses.
- Line 3: ``std::move(path)`` refers to the same vector, and **marks** it:
  it says that another object may take its contents. ``taken`` takes
  them, and ``path`` is left empty (libstdc++, measured: ``path.size()``
  printed ``0``).
- ``path`` and ``std::move(path)`` refer to the same object, and their
  categories differ. A category belongs to an expression, not to an
  object.

.. note::

   C++20 **[basic.lval]** paragraph 3: "Despite their names, these terms
   classify expressions, not values".


Finding the Category in Four Steps
====================================================

Look at the **last operation** the expression does: its outermost
operator, call or name. In ``std::move(obstacle).pose``, the last
operation is ``.pose``, a member access, so Step 4 decides. In
``make_path(3).size()``, it is the call to ``size()``, so Step 3 decides.
Go through the steps in order, and stop at the first one that applies.


Step 1: A Name
--------------

The name of a variable, a parameter or a reference is an **lvalue**,
whatever its type. A name declared with ``&&`` is an lvalue too.

A name refers to an object that already exists, and you can use the
name again on the next line. If another object could take its contents
without your saying so, the next line would find it empty. So a name
never lets another object take its contents: you mark it with
``std::move`` when you want that.

.. note::

   ``this`` (Lecture 8) is a keyword, not a name. It is a prvalue, which
   is why ``this = nullptr;`` does not compile. C++20
   **[expr.prim.this]** (7.5.2) paragraph 2: "the expression this is a
   prvalue".


Step 2: A Literal
-----------------

A literal is a value written in the code. A number, a character,
``true``, ``false`` and ``nullptr`` are **prvalues**: each one computes a
value, and no object held it before.

A string literal, such as ``"lidar"``, is the exception: it is an
**lvalue**. The program keeps every string literal in memory, as an array
of ``const char``, for its whole run, so the literal refers to an object
that already exists.

.. note::

   C++20 **[expr.prim.literal]** (7.5.1) paragraph 1: "A string-literal
   is an lvalue [...] and any other literal is a prvalue".
   **[lex.string]** (5.13.5) paragraph 14: "Evaluating a string-literal
   results in a string literal object with static storage duration".


Step 3: A Function Call or a Cast
---------------------------------

Read the **return type** of the function. For a cast, read the type you
cast to.

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Return type
     - Category
     - Why
   * - ``T&`` or ``const T&``
     - lvalue
     - it refers to an object that already exists, and does not mark it
   * - ``T&&``
     - xvalue
     - it refers to an object that already exists, and marks it
   * - ``T``, with no ``&``
     - prvalue
     - it computes a new value

- Only the return type counts. The parameters play no part:
  ``lookup(seen, 1)`` takes a ``std::vector<Obstacle>&`` and returns an
  ``Obstacle&``, and it is an lvalue because of the ``Obstacle&``.
- Member functions follow the same rule: ``seen.size()`` returns a
  ``std::size_t`` by value, a prvalue; ``seen.front()`` returns a
  reference, an lvalue.
- An **overloaded operator** is a function too. ``seen[0]`` calls the
  ``operator[]`` of ``std::vector``, which returns a reference: an lvalue.
  ``a + b`` on two ``std::string`` objects calls ``operator+``, which
  returns a new ``std::string`` by value: a prvalue.
- ``std::move(x)`` returns ``T&&``, so it is an xvalue. It is a cast, and
  it moves nothing (Lecture 7, What ``std::move`` Does).
- A cast follows the same table: ``static_cast<int&&>(count)`` is an
  xvalue, ``static_cast<int&>(count)`` an lvalue, and
  ``static_cast<double>(count)`` a prvalue, a new ``double`` that holds
  3.0.

.. note::

   C++20 **[expr.call]** (7.6.1.2) paragraph 14: "A function call is an
   lvalue if the result type is an lvalue reference type [...], an xvalue
   if the result type is an rvalue reference to object type, and a
   prvalue otherwise". **[basic.lval]** paragraph 2, note: "User-defined
   operators are functions, and the categories of values they expect and
   yield are determined by their parameter and return types".


Step 4: A Built-in Operator
---------------------------

A built-in operator works on built-in types, such as ``int``, ``double``,
a pointer or a plain array. The member access operator ``.`` is always
built-in, and so is ``->`` on a plain pointer. The standard fixes the
category of each one's result:

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Operator
     - Category
     - Why
   * - ``*p``
     - lvalue
     - the object ``p`` points at
   * - ``p->m``
     - lvalue
     - it is ``(*p).m``, and ``*p`` is an lvalue
   * - ``a[i]``, ``a`` a named array
     - lvalue
     - an element of the array, which already exists
   * - ``++x``, ``--x``
     - lvalue
     - the result is ``x`` itself, updated
   * - ``x = y``, ``x += y``
     - lvalue
     - the result is ``x``
   * - ``e.m``
     - lvalue if ``e`` is an lvalue; xvalue otherwise
     - the member of the object ``e`` refers to
   * - ``x++``, ``x--``
     - prvalue
     - a copy of the old value of ``x``
   * - ``x + y``, ``x * y``, ``-x``
     - prvalue
     - a computed number
   * - ``x == y``, ``x < y``, ``!x``
     - prvalue
     - a computed ``bool``
   * - ``&x``
     - prvalue
     - a computed address: the pointer is a new value
   * - ``c ? x : y``
     - lvalue when ``x`` and ``y`` are lvalues of the same type; prvalue
       when one of them is a prvalue, such as ``0``
     - it is one of the two, or a value computed from one of them

When ``e`` in ``e.m`` is a prvalue, there is no object to take a member
of yet. The compiler creates a temporary object from the prvalue
(**temporary materialization**, Lecture 7), and the member of that
temporary is an xvalue: it exists, and nothing else can use it.

.. note::

   C++20 **[expr.unary.op]** (7.6.2.1) paragraph 1: for ``*``, "the
   result is an lvalue referring to the object or function to which the
   expression points". **[expr.pre.incr]** (7.6.2.2): "The result is the
   updated operand; it is an lvalue". **[expr.post.incr]** (7.6.1.5): "The
   result is a prvalue". **[expr.ass]** (7.6.19) paragraph 1: "their result
   is an lvalue referring to the left operand". **[expr.ref]** (7.6.1.4)
   paragraph 6.2: "If E1 is an lvalue, then E1.E2 is an lvalue; otherwise
   E1.E2 is an xvalue".


Checking Your Answer
====================================================

Lecture 7 gave a test that the compiler runs for you: ``decltype((e))``,
with two pairs of parentheses, gives

- ``T&`` when ``e`` is an lvalue,
- ``T&&`` when ``e`` is an xvalue,
- ``T`` when ``e`` is a prvalue.

With one pair around a plain name, ``decltype(e)`` gives the type the
name was declared with instead, and says nothing about the category
(Lecture 7, One Pair or Two Parentheses).


The ``CATEGORY`` Helper
-----------------------

The helper turns the test into a word you can print. It is the one in
``project/week7/playground/src/moves.cpp``, and in
``project/week7/value_categories/include/category.hpp``, in the course
repository. ``702run week7_value_categories helper`` runs the program
below.

.. code-block:: cpp
   :linenos:

   #include <iostream>
   #include <string_view>
   #include <type_traits>
   #include <utility>
   #include <vector>

   // decltype((e)) is T& for an lvalue, T&& for an xvalue and T for a prvalue.
   template <typename T>
   constexpr std::string_view category() {
     if constexpr (std::is_lvalue_reference_v<T>) {
       return "lvalue";
     } else if constexpr (std::is_rvalue_reference_v<T>) {
       return "xvalue";
     } else {
       return "prvalue";
     }
   }
   // A macro, because decltype must see the expression itself, not a copy of it.
   #define CATEGORY(e) category<decltype((e))>()

   struct Pose { double x{0.0}; double y{0.0}; double heading{0.0}; };

   int main() {
     int count{3};
     std::vector<int> path{1, 2, 3};
     std::cout << CATEGORY(count) << '\n';
     std::cout << CATEGORY(count + 1) << '\n';
     std::cout << CATEGORY(std::move(path)) << '\n';
     std::cout << CATEGORY(count++) << ' ' << count << '\n';
     std::cout << path.size() << '\n';
     std::cout << CATEGORY((Pose{1.0, 2.0, 0.0})) << '\n';
     static_assert(CATEGORY(count) == "lvalue");
     static_assert(CATEGORY(std::move(path)) == "xvalue");
     Pose pose{};
     static_assert(CATEGORY(std::move(pose).x) == "xvalue");
   }

Save it as ``categories.cpp``, then build and run it:

.. code-block:: bash

   g++ -std=c++20 -Wall -Wextra -pedantic-errors -Wshadow categories.cpp -o categories
   ./categories

.. code-block:: text

   lvalue
   prvalue
   xvalue
   prvalue 3
   3
   prvalue

- ``decltype`` does not evaluate the expression (Lecture 7). Line 29
  prints ``3`` for ``count`` after ``CATEGORY(count++)``, and line 30
  prints ``3`` for ``path.size()`` after line 28's
  ``CATEGORY(std::move(path))``: nothing was incremented, and nothing was
  moved.
- Lines 32, 33 and 35 check at compile time. If an answer is wrong, the
  build stops at that line.
- ``CATEGORY`` is a macro, and the preprocessor splits a macro's argument
  at every comma that is not inside parentheses. Without the extra pair
  on line 31, ``CATEGORY(Pose{1.0, 2.0, 0.0})`` does not compile:

  .. code-block:: text

     error: macro "CATEGORY" passed 3 arguments, but takes just 1

  Extra parentheses around an expression do not change its category.


Worked Examples
====================================================

Each example below uses these declarations. ``Pose``, ``Obstacle``,
``make_path`` and ``make_obstacle`` are the ones from Lecture 7, and
``lookup`` is the one from its Exercise 2. ``702run
week7_value_categories examples`` prints the category of every
expression in the tables of this section.

.. code-block:: cpp

   struct Pose { double x{0.0}; double y{0.0}; double heading{0.0}; };
   struct Obstacle {
     int id{0};
     Pose pose{};
     double speed{0.0};
     bool is_static{false};
   };

   std::vector<Pose> make_path(int n);                     // returns by value
   Obstacle make_obstacle(int id);                         // returns by value
   Obstacle& lookup(std::vector<Obstacle>& seen, int id);  // returns Obstacle&
   const Pose& first_pose(const std::vector<Pose>& path);  // returns const Pose&

   int count{3};
   int other{7};
   const double limit{40.0};
   int& alias{count};
   int numbers[3]{10, 20, 30};
   int* p{&numbers[1]};
   Pose pose{1.0, 2.0, 0.0};
   Pose* pp{&pose};
   Obstacle obstacle{2, {12.0, -1.0, 0.0}, 4.0};
   std::vector<Pose> path{make_path(3)};
   std::vector<Pose>&& r{make_path(10)};
   std::vector<Obstacle> seen{make_obstacle(0), make_obstacle(1)};
   std::string a{"cyc"};
   std::string b{"list"};


Names (Step 1)
--------------

.. list-table::
   :header-rows: 1
   :class: compact-table
   :widths: 25 15 60

   * - Expression
     - Category
     - Why
   * - ``count``
     - lvalue
     - the name of an ``int`` variable
   * - ``limit``
     - lvalue
     - ``const`` does not change the category. You cannot assign to
       ``limit``, but it is still an object with an address.
   * - ``alias``
     - lvalue
     - a reference is another name for ``count``
   * - ``numbers``
     - lvalue
     - the name of an array
   * - ``p``
     - lvalue
     - the pointer variable itself. What it points at is ``*p``, a
       different expression.
   * - ``path``
     - lvalue
     - the name of a vector
   * - ``r``
     - lvalue
     - the type of ``r`` is ``std::vector<Pose>&&``, but the expression
       ``r`` is a name (`Trap 1: The Type Is Not the Category`_)


Literals (Step 2)
-----------------

.. list-table::
   :header-rows: 1
   :class: compact-table
   :widths: 25 15 60

   * - Expression
     - Category
     - Why
   * - ``42``
     - prvalue
     - a number written in the code
   * - ``3.5``
     - prvalue
     - a number written in the code
   * - ``true``
     - prvalue
     - a ``bool`` literal
   * - ``'a'``
     - prvalue
     - a character literal
   * - ``nullptr``
     - prvalue
     - the null pointer literal
   * - ``"hello"``
     - lvalue
     - a string literal: an array of 6 ``const char`` (5 letters and the
       ``'\0'`` at the end) that exists for the whole run.
       ``decltype(("hello"))`` is ``const char(&)[6]``.


Function Calls and Casts (Step 3)
---------------------------------

.. list-table::
   :header-rows: 1
   :class: compact-table
   :widths: 35 15 50

   * - Expression
     - Category
     - Why
   * - ``make_path(3)``
     - prvalue
     - returns ``std::vector<Pose>``, no ``&``
   * - ``make_obstacle(3)``
     - prvalue
     - returns ``Obstacle``, no ``&``
   * - ``lookup(seen, 1)``
     - lvalue
     - returns ``Obstacle&``
   * - ``first_pose(path)``
     - lvalue
     - returns ``const Pose&``. ``const`` does not change the category.
   * - ``seen[0]``
     - lvalue
     - ``operator[]`` of ``std::vector`` returns a reference
   * - ``seen.front()``
     - lvalue
     - returns a reference to the first element
   * - ``seen.size()``
     - prvalue
     - returns a ``std::size_t`` by value
   * - ``a + b``
     - prvalue
     - ``operator+`` of ``std::string`` returns a new string by value,
       ``"cyclist"``
   * - ``std::move(path)``
     - xvalue
     - returns ``std::vector<Pose>&&``
   * - ``static_cast<std::vector<Pose>&&>(path)``
     - xvalue
     - a cast to ``T&&``: what ``std::move`` does inside
   * - ``static_cast<int&>(count)``
     - lvalue
     - a cast to ``T&``
   * - ``static_cast<double>(count)``
     - prvalue
     - a cast to a type with no ``&``: a new ``double``, 3.0


Built-in Operators (Step 4)
---------------------------

.. list-table::
   :header-rows: 1
   :class: compact-table
   :widths: 35 15 50

   * - Expression
     - Category
     - Why
   * - ``count + 1``
     - prvalue
     - computes 4. No object held that 4 before.
   * - ``count * 2``
     - prvalue
     - computes 6
   * - ``-count``
     - prvalue
     - computes -3
   * - ``count == 3``
     - prvalue
     - computes ``true``
   * - ``&count``
     - prvalue
     - computes an ``int*``. The address is a new value; ``count`` is the
       object.
   * - ``*p``
     - lvalue
     - the object ``p`` points at, ``numbers[1]``
   * - ``numbers[1]``
     - lvalue
     - the second element of ``numbers``
   * - ``++count``
     - lvalue
     - the result is ``count`` itself
   * - ``count++``
     - prvalue
     - a copy of the old value. ``count`` itself is already 1 more.
   * - ``count = 5``
     - lvalue
     - the result is ``count``
   * - ``count += 1``
     - lvalue
     - the result is ``count``
   * - ``count > 0 ? count : other``
     - lvalue
     - both choices are ``int`` lvalues, so the result is one of the two
       variables
   * - ``count > 0 ? count : 0``
     - prvalue
     - ``0`` is a prvalue, so the result is a value, not a variable


Member Access (Step 4)
----------------------

For ``e.m``, find the category of ``e`` first, with the same four steps.

.. list-table::
   :header-rows: 1
   :class: compact-table
   :widths: 35 15 50

   * - Expression
     - Category
     - Why
   * - ``pose.x``
     - lvalue
     - ``pose`` is an lvalue (Step 1), so its member is an lvalue
   * - ``obstacle.pose.x``
     - lvalue
     - ``obstacle`` is an lvalue, so ``obstacle.pose`` is an lvalue, so
       ``.x`` of it is an lvalue
   * - ``seen[1].pose``
     - lvalue
     - ``seen[1]`` is an lvalue (Step 3)
   * - ``pp->x``
     - lvalue
     - ``pp->x`` is ``(*pp).x``, and ``*pp`` is an lvalue
   * - ``std::move(obstacle).pose``
     - xvalue
     - ``std::move(obstacle)`` is an xvalue, so its member is an xvalue.
       When the whole ``Obstacle`` is marked, its ``pose`` is marked too.
   * - ``std::move(obstacle).pose.x``
     - xvalue
     - the same rule twice
   * - ``make_obstacle(3).id``
     - xvalue
     - ``make_obstacle(3)`` is a prvalue. ``.id`` needs an object, so a
       temporary is made, and its member is an xvalue.
   * - ``Pose{}.x``
     - xvalue
     - ``Pose{}`` is a prvalue, so the same as the line above
   * - ``std::move(pp)->x``
     - lvalue
     - ``->`` follows the pointer, and ``*`` always gives an lvalue
       (`Trap 5: The Arrow Always Gives an lvalue`_)
   * - ``make_path(3)[0]``
     - lvalue
     - ``operator[]`` returns ``Pose&`` (Step 3), even on a temporary
       vector (`Trap 4: An lvalue Can Refer Into a Temporary`_)
   * - ``make_path(3)[0].x``
     - lvalue
     - ``make_path(3)[0]`` is an lvalue, so its member is an lvalue
   * - ``make_path(3).size()``
     - prvalue
     - the last operation is the call to ``size()``, which returns by
       value (Step 3)


Objects Made on the Spot
------------------------

A type name followed by braces, such as ``Pose{}``, creates a value of
that type. It is a prvalue: it will initialize an object, and no object
holds it yet.

.. list-table::
   :header-rows: 1
   :class: compact-table
   :widths: 35 15 50

   * - Expression
     - Category
     - Why
   * - ``Pose{}``
     - prvalue
     - a ``Pose`` with every member at its default
   * - ``Pose{1.0, 2.0, 0.0}``
     - prvalue
     - a ``Pose`` with the three values given
   * - ``std::vector<int>{1, 2, 3}``
     - prvalue
     - a new vector of 3 ``int``
   * - ``std::string{"cyclist"}``
     - prvalue
     - a new string

.. note::

   C++20 **[expr.type.conv]** (7.6.1.3) paragraph 2: "the expression is a
   prvalue of the specified type whose result object is direct-initialized
   [...] with the initializer".


Traps
====================================================

``702run week7_value_categories traps`` runs Traps 1, 2, 3 and 5, and
``702run week7_value_categories dangling`` runs Trap 4.

Trap 1: The Type Is Not the Category
------------------------------------

.. code-block:: cpp

   std::vector<Pose>&& r{make_path(10)};
   static_assert(std::is_same_v<decltype(r), std::vector<Pose>&&>);   // the type of r
   static_assert(std::is_same_v<decltype((r)), std::vector<Pose>&>);  // r is an lvalue

- The ``&&`` in a declaration is part of the **type** of ``r``.
- The **category** belongs to an expression, and the expression ``r`` is a
  name: Step 1 says lvalue. Both ``static_assert`` lines compile.
- A parameter is a name too. In the function below, ``path`` has the type
  ``std::vector<Pose>&&``, and the expression ``path`` is still an lvalue:

.. code-block:: cpp
   :linenos:

   void take(const std::vector<Pose>&) { std::cout << "1 const&\n"; }
   void take(std::vector<Pose>&&) { std::cout << "2 &&\n"; }

   void inside(std::vector<Pose>&& path) {
     take(path);             // path is a name: an lvalue
     take(std::move(path));  // an xvalue
   }

   inside(make_path(2));

.. code-block:: text

   1 const&
   2 &&

- Line 5 calls overload 1, the ``const&`` one. If ``take`` copied its
  argument, line 5 would copy.
- To let a function take a parameter's contents, mark it again with
  ``std::move``, as on line 6 (Lecture 7, A Parameter the Function Moves
  From).

.. note::

   C++20 **[basic.lval]** paragraph 4, note: "named rvalue references are
   treated as lvalues and unnamed rvalue references to objects are treated
   as xvalues".


Trap 2: ``std::move`` Moves Nothing
-----------------------------------

- ``std::move(path)`` is a cast to ``std::vector<Pose>&&``. It marks
  ``path``, and nothing more. The move happens later, if a move
  constructor or a ``&&`` overload receives the result. `The CATEGORY
  Helper`_ shows ``path.size()`` still at 3 after
  ``CATEGORY(std::move(path))``.
- On a ``const`` object, ``std::move`` still gives an xvalue, of type
  ``const T&&``. A move would change the object, so the ``T&&`` overload
  and the move constructor cannot receive it. The ``const T&`` ones can,
  so the object is copied:

.. code-block:: cpp

   const std::vector<Pose> fixed{make_path(2)};
   std::vector<Pose> dest{std::move(fixed)};  // an xvalue, and a copy
   std::cout << fixed.size() << '\n';         // 2: nothing was taken

``decltype((std::move(fixed)))`` is ``const std::vector<Pose>&&``.
Lecture 7 shows the same with 1000 poses (``std::move`` on a ``const``
Object).


Trap 3: "Left Side of =" Is Not the Test
----------------------------------------

The names come from history: an lvalue could go on the left of ``=``, an
rvalue only on the right. That rule no longer holds, in both directions.

.. code-block:: cpp
   :linenos:

   const double limit{40.0};
   limit = 2.0;                     // limit is an lvalue: does not compile
   make_obstacle(3) = Obstacle{};   // make_obstacle(3) is a prvalue: compiles
   5 = count;                       // does not compile
   ++count = 3;                     // ++count is an lvalue: compiles
   count++ = 3;                     // count++ is a prvalue: does not compile

.. code-block:: text

   error: assignment of read-only variable 'limit'
   error: lvalue required as left operand of assignment

- Line 2: ``limit`` is an lvalue, but it is ``const``, so it cannot be
  changed. The first message.
- Line 3: for a class type, ``=`` calls the member function
  ``operator=``, and a member function can be called on a temporary. The
  assignment changes the temporary, which is destroyed at the end of the
  line. It compiles, and does nothing useful.
- Lines 4 and 6: for built-in types, the left of ``=`` must be an lvalue
  that can be changed. The second message, for each line.
- Use the four steps, not the side of ``=``.

.. note::

   C++20 **[basic.lval]** paragraph 3, note: "Historically, lvalues and
   rvalues were so-called because they could appear on the left- and
   right-hand side of an assignment (although this is no longer generally
   true)".


Trap 4: An lvalue Can Refer Into a Temporary
--------------------------------------------

.. code-block:: cpp
   :linenos:

   double safe{make_path(3)[1].x};       // reads before the vector is destroyed
   const Pose& second{make_path(3)[1]};  // refers into a destroyed vector
   std::cout << second.x << '\n';        // reads freed memory

- ``make_path(3)[1]`` is an lvalue (Step 3: ``operator[]`` returns
  ``Pose&``). It refers to an element of a temporary vector.
- A temporary is destroyed at the end of the **full expression** that
  created it: here, at the end of each line. Line 1 reads ``x`` before
  that, so it is safe.
- Line 2 binds ``second`` to the element. The temporary vector is
  destroyed at the end of line 2, and with it the block that holds the
  element. Line 3 reads freed memory. g++ warns, and AddressSanitizer
  stops the program at line 3:

.. code-block:: text

   warning: possibly dangling reference to a temporary [-Wdangling-reference]
   ERROR: AddressSanitizer: heap-use-after-free on address ...

- Compare ``const std::vector<Pose>& whole{make_path(3)};``. There the
  reference binds to the temporary itself, so the temporary lives as long
  as ``whole`` (Lecture 7, Category, Type and Lifetime), and
  ``whole[2].x`` prints ``2`` with AddressSanitizer on. In line 2, the
  reference binds to what ``operator[]`` returned, not to the temporary,
  so the temporary's life is not extended.


Trap 5: The Arrow Always Gives an lvalue
----------------------------------------

.. code-block:: cpp

   Pose pose{1.0, 2.0, 0.0};
   Pose* pp{&pose};
   std::move(pose).x   // xvalue: pose is marked, so its member is marked
   std::move(pp)->x    // lvalue: only the pointer pp is marked

- ``std::move(pp)`` marks the pointer, not the ``Pose`` it points at.
- ``std::move(pp)->x`` is ``(*std::move(pp)).x``. ``*`` always gives an
  lvalue (Step 4), so the ``Pose`` is an lvalue, and so is its ``x``.


Why the Category Matters
====================================================

Three things in your code depend on the category.

**1. The built-in** ``&`` **needs an lvalue.**

.. code-block:: cpp

   int* a{&count};             // compiles
   int* b{&(count + 1)};       // a prvalue: does not compile
   int* c{&std::move(count)};  // an xvalue: does not compile

.. code-block:: text

   error: lvalue required as unary '&' operand
   error: taking address of rvalue [-fpermissive]

The built-in ``&`` accepts only an lvalue. An xvalue refers to an object
that has an address, and ``&`` still does not compile on it.

.. note::

   C++20 **[expr.unary.op]** (7.6.2.1) paragraph 3: "if the operand is an
   lvalue of type T, the resulting expression is a prvalue of type
   “pointer to T” [...] Otherwise, the program is ill-formed".


**2. Each kind of reference binds to some categories only.**

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Reference
     - Binds to
     - Example that does not compile
   * - ``T&``
     - lvalues
     - ``int& lr{count + 1};``
   * - ``const T&``
     - lvalues, xvalues and prvalues
     - none
   * - ``T&&``
     - xvalues and prvalues (rvalues)
     - ``int&& rr{count};``

.. code-block:: text

   error: cannot bind non-const lvalue reference of type 'int&' to an rvalue of type 'int'
   error: cannot bind rvalue reference of type 'int&&' to lvalue of type 'int'

**3. The category picks the overload: a copy or a move.** With the two
``take`` functions of `Trap 1: The Type Is Not the Category`_
(``702run week7_value_categories overloads``):

.. code-block:: cpp
   :linenos:

   const std::vector<Pose> fixed{make_path(2)};
   take(path);              // lvalue
   take(make_path(5));      // prvalue
   take(r);                 // lvalue: a name
   take(std::move(r));      // xvalue
   take(std::move(path));   // xvalue
   take(fixed);             // lvalue
   take(std::move(fixed));  // xvalue, but const

.. code-block:: text

   1 const&
   2 &&
   1 const&
   2 &&
   2 &&
   1 const&
   1 const&

- An lvalue picks ``const T&``, overload 1.
- An rvalue picks ``T&&``, overload 2, when it can bind there. That is
  what lets ``std::vector`` move instead of copy (Lecture 7, Overloads for
  Copy and Move).
- Line 8 is the ``const`` case of `Trap 2: std::move Moves Nothing`_: an
  xvalue of type ``const std::vector<Pose>&&`` cannot bind to overload 2.


Summary
====================================================

.. list-table::
   :header-rows: 1
   :class: compact-table

   * - Category
     - Refers to an object that already exists
     - May be taken
     - ``decltype((e))``
     - Common expressions
   * - lvalue
     - yes
     - no
     - ``T&``
     - names (even of type ``T&&``), string literals, ``*p``, ``p->m``,
       ``++x``, ``x = y``, calls that return ``T&``, a member of an lvalue
   * - xvalue
     - yes
     - yes
     - ``T&&``
     - ``std::move(x)``, ``static_cast<T&&>(x)``, calls that return
       ``T&&``, a member of an xvalue or of a prvalue
   * - prvalue
     - no
     - yes
     - ``T``
     - other literals, ``x + y``, ``x++``, ``&x``, calls that return by
       value, ``T{...}``

- **glvalue** = lvalue or xvalue. **rvalue** = xvalue or prvalue.
- To find the category: a name (lvalue), a literal (prvalue, or lvalue for
  a string), a call or cast (read the return type), a built-in operator
  (the table in `Step 4: A Built-in Operator`_).
- Check with ``decltype((e))`` or ``CATEGORY(e)``.
