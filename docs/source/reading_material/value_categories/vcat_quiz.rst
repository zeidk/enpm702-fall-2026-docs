====================================================
Value Categories: Quiz
====================================================

The questions use the :ref:`declarations <vcat-declarations>` at the
start of Finding the Category in Four Steps, in :doc:`vcat_lecture`.

.. dropdown:: The Definitions of ``make_obstacle``, ``lookup`` and ``first_pose``
   :icon: code
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   .. include:: vcat_definitions.inc

   With the mouse over one of these names anywhere on this page, its
   definition shows in a box. On a phone, tap the name.


.. admonition:: Question 1
   :class: hint

   How many of the categories lvalue, xvalue and prvalue does one
   expression belong to?

   a) Exactly one
   b) One or two
   c) Any number, depending on where the expression is used
   d) None, if it is a temporary

   .. dropdown:: Answer
      :class-container: sd-border-success

      **a) Exactly one**

      glvalue and rvalue are not categories of their own: each is a name
      for two of the three. C++20 **[basic.lval]** paragraph 2: "Every expression belongs to
      exactly one of the fundamental classifications in this taxonomy:
      lvalue, xvalue, or prvalue".


.. admonition:: Question 2
   :class: hint

   What is an **rvalue**?

   a) A fourth category, next to lvalue, xvalue and prvalue
   b) An xvalue or a prvalue
   c) Any expression on the right of ``=``
   d) A temporary object

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) An xvalue or a prvalue**

      "rvalue" is a name for two of the three categories together, like
      "glvalue" (an lvalue or an xvalue). An expression on the right of
      ``=`` can be an lvalue: in ``copy = path;``, ``path`` is one.


.. admonition:: Question 3
   :class: hint

   After ``std::vector<Pose>&& r{make_path(10)};``, what is the category
   of the expression ``r``?

   a) lvalue
   b) xvalue
   c) prvalue
   d) rvalue, a fourth category

   .. dropdown:: Answer
      :class-container: sd-border-success

      **a) lvalue**

      ``std::vector<Pose>&&`` is the type of ``r``. The expression ``r``
      is a name, and a name is an lvalue (Step 1).
      ``decltype((r))`` is ``std::vector<Pose>&``.


.. admonition:: Question 4
   :class: hint

   With ``int count{3};``, which expression is an lvalue?

   a) ``count++``
   b) ``count + 0``
   c) ``++count``
   d) ``-count``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c)** ``++count``

      Prefix ``++`` gives ``count`` itself, updated. ``count++`` gives a
      copy of the old value, a prvalue. ``count + 0`` and ``-count``
      compute new values: prvalues.


.. admonition:: Question 5
   :class: hint

   ``Obstacle& lookup(std::vector<Obstacle>& seen, int id);`` What decides
   the category of the call ``lookup(seen, 1)``?

   a) The ``&`` on the parameter ``seen``: it makes the call an lvalue
   b) The return type ``Obstacle&``: it makes the call an lvalue
   c) The argument ``1``, a prvalue: it makes the call a prvalue
   d) Every call that returns a class type is a prvalue

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)**

      Step 3: only the return type counts. ``T&`` gives an lvalue, ``T&&``
      an xvalue, and a type with no ``&`` a prvalue (C++20
      **[expr.call]** paragraph 14).


.. admonition:: Question 6
   :class: hint

   ``make_obstacle`` returns an ``Obstacle`` by value. What is the
   category of ``make_obstacle(3).id``?

   a) lvalue
   b) xvalue
   c) prvalue
   d) It does not compile: a prvalue has no members

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) xvalue**

      The outermost operation is ``.id`` (Step 4), so find the category
      of ``make_obstacle(3)`` first: a prvalue (Step 3). To read ``.id``,
      the compiler creates a temporary object from it (temporary
      materialization). The member of that temporary is an xvalue.


.. admonition:: Question 7
   :class: hint

   What is the category of ``"lidar"``?

   a) prvalue, like every literal
   b) xvalue
   c) lvalue
   d) A string literal has no category

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) lvalue**

      A string literal is an array of ``const char`` that exists for the
      whole run of the program. C++20 **[expr.prim.literal]**: "A
      string-literal is an lvalue [...] and any other literal is a
      prvalue".


.. admonition:: Question 8
   :class: hint

   With ``std::vector<Pose> path{make_path(3)};``, what is
   ``decltype((std::move(path)))``?

   a) ``std::vector<Pose>``
   b) ``std::vector<Pose>&``
   c) ``std::vector<Pose>&&``
   d) ``const std::vector<Pose>&``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c)** ``std::vector<Pose>&&``

      ``std::move(path)`` is an xvalue, and ``decltype((e))`` gives
      ``T&&`` for an xvalue.


.. admonition:: Question 9
   :class: hint

   With ``Pose pose{};`` and ``Pose* pp{&pose};``, what is the category of
   ``std::move(pp)->x``?

   a) lvalue
   b) xvalue
   c) prvalue
   d) It does not compile

   .. dropdown:: Answer
      :class-container: sd-border-success

      **a) lvalue**

      ``std::move(pp)`` marks the pointer, not the ``Pose``. ``->``
      follows the pointer, and the object a pointer points at is an
      lvalue, so its member ``x`` is an lvalue too. Compare
      ``std::move(pose).x``, an xvalue.


.. admonition:: Question 10
   :class: hint

   With ``int count{3};``, which line does **not** compile?

   a) ``const int& a{count + 1};``
   b) ``int&& b{count + 1};``
   c) ``int&& c{count};``
   d) ``int& d{count};``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c)**

      ``int&&`` binds only to rvalues, and ``count`` is an lvalue. g++
      says: ``cannot bind rvalue reference of type 'int&&' to lvalue of
      type 'int'``. b) compiles because ``count + 1`` is a prvalue, an
      rvalue. ``const int&`` binds to every category, and ``int&`` binds
      to the lvalue ``count``.


.. admonition:: Question 11
   :class: hint

   .. code-block:: cpp

      std::vector<Pose> controller_path;

      void set_path(std::vector<Pose>&& path) {
        controller_path = path;
      }

      set_path(make_path(1000));

   Does the assignment inside ``set_path`` copy or move the 1000 poses?

   a) It moves: the parameter is ``std::vector<Pose>&&``
   b) It moves: the argument ``make_path(1000)`` is a prvalue
   c) It copies: the expression ``path`` is an lvalue
   d) It does not compile

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c)**

      Inside the function, ``path`` is a name, so it is an lvalue (Step 1),
      and the copy assignment runs. To move, write
      ``controller_path = std::move(path);``.


.. admonition:: Question 12
   :class: hint

   .. code-block:: cpp

      const std::vector<Pose> fixed{make_path(2)};
      std::vector<Pose> dest{std::move(fixed)};
      std::cout << fixed.size() << '\n';

   What does the last line print?

   a) ``0``: ``dest`` took the contents
   b) ``2``: ``std::move(fixed)`` cannot bind to the move constructor, so
      ``dest`` is a copy
   c) Nothing: line 2 does not compile
   d) The result is undefined

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)**

      ``std::move(fixed)`` is an xvalue of type
      ``const std::vector<Pose>&&``. The move constructor takes
      ``std::vector<Pose>&&``, which cannot refer to a ``const`` object.
      The copy constructor takes ``const std::vector<Pose>&``, so it runs.
      Measured with g++ 13.3: the line prints ``2``.


.. admonition:: Question 13
   :class: hint

   Which statement is true?

   a) Every lvalue can appear on the left of ``=``.
   b) A prvalue of a class type, such as ``make_obstacle(3)``, can appear
      on the left of ``=``, and the line compiles.
   c) An xvalue does not refer to an object.
   d) ``std::move(path)`` moves the contents of ``path``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b)**

      ``make_obstacle(3) = Obstacle{};`` compiles: for a class, ``=``
      calls the member function ``operator=``, which can run on a
      temporary. a) is false: a ``const`` lvalue cannot be assigned. c) is
      false: an xvalue refers to an object that already exists. d) is
      false: ``std::move`` is a cast and moves nothing.
