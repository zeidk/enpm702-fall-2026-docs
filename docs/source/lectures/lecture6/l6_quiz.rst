.. _l6_quiz:

================
Lecture 6 Quiz
================

This quiz covers the key concepts from Lecture 6: Functions, Advanced. Topics include ``struct`` layout, ``std::optional``, structured bindings, function templates and template argument deduction, concepts, lambdas and their captures, and ``std::function``. Questions 1, 5, 8 and 9 come from the Further Reading part of the lecture.

.. note::

   **Instructions:**

   - Multiple choice questions have exactly one correct answer.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 10)
=====================================

.. admonition:: Question 1
   :class: hint

   What is the **only** difference between a ``struct`` and a ``class`` in C++?

   A. ``struct`` cannot have methods; ``class`` can.
   B. ``struct`` members are ``public`` by default; ``class`` members are ``private`` by default.
   C. ``struct`` is allocated on the stack; ``class`` is allocated on the heap.
   D. ``struct`` does not support inheritance; ``class`` does.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. struct members are public by default; class members are private by default.**

      ``struct`` and ``class`` make the same kind of type. Both support methods, inheritance and templates. They differ only in default access: ``public`` for a ``struct``, ``private`` for a ``class``, for members and for base classes. Lecture 6 uses ``struct`` for plain data; classes are Lecture 8.

.. admonition:: Question 2
   :class: hint

   What does the compiler do when it encounters a call to a function template with specific types?

   A. It interprets the template at runtime.
   B. It instantiates a concrete function for those types at compile time.
   C. It converts the template to a virtual function.
   D. It stores the template for lazy evaluation.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It instantiates a concrete function for those types at compile time.**

      Templates are blueprints. When you call ``add(3, 4)``, the compiler generates ``int add(int, int)`` at compile time. This is called template instantiation.

.. admonition:: Question 3
   :class: hint

   Why must template definitions be placed in header files (``.hpp``)?

   A. Because the compiler compiles a template once and shares it with every ``.cpp`` file.
   B. Because the compiler needs the full definition to instantiate the template for each type used.
   C. Because the linker cannot resolve template symbols.
   D. Because ``.cpp`` files cannot contain template code.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Because the compiler needs the full definition to instantiate the template for each type used.**

      Templates are not compiled until they are instantiated. If the definition is in a ``.cpp`` file, other translation units cannot see it and cannot instantiate the template, resulting in a linker error.

.. admonition:: Question 4
   :class: hint

   Given ``template<typename T> T add(T a, T b);``, what happens when you call ``add(3, 4.5)``?

   A. The compiler deduces ``T = double`` and converts ``3`` to ``double``.
   B. The compiler deduces ``T = int`` and truncates ``4.5``.
   C. The call fails because the compiler cannot deduce a single consistent ``T``.
   D. The compiler creates two instantiations and picks the best one.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The call fails because the compiler cannot deduce a single consistent T.**

      Both parameters share the same ``T``. Argument ``3`` suggests ``T = int`` while ``4.5`` suggests ``T = double``. The compiler cannot reconcile these, so deduction fails. You must either use explicit template arguments (``add<double>(3, 4.5)``) or use two template parameters.

.. admonition:: Question 5
   :class: hint

   What does ``decltype(x)`` produce when ``x`` is declared as ``int x{10};``?

   A. ``int&``
   B. ``const int``
   C. ``int``
   D. ``int&&``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. int**

      ``decltype(x)`` (without extra parentheses) yields the **declared type** of ``x``, which is ``int``. Note: ``decltype((x))`` would yield ``int&`` because ``(x)`` is an lvalue expression.

.. admonition:: Question 6
   :class: hint

   ``idle`` is an empty ``std::optional<int>``. What does ``*idle`` do?

   A. It throws ``std::bad_optional_access``.
   B. It returns ``0``.
   C. It is undefined behavior.
   D. It does not compile.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. It is undefined behavior.**

      ``*`` does no check. In the lecture it printed ``0`` with no warning, but the next build may print anything. Check with ``if (idle)`` first, or read with ``idle.value()``, which throws ``std::bad_optional_access`` when the optional is empty, or with ``idle.value_or(-1)``, which gives -1.

.. admonition:: Question 7
   :class: hint

   With g++ 13 on x86-64, what is ``sizeof(RobotStatus)``?

   .. code-block:: cpp

      struct Position { double x; double y; };

      struct RobotStatus {
        int id;              // 4 bytes
        double battery_pct;  // 8 bytes
        Position position;   // 16 bytes
        bool busy;           // 1 byte
      };

   A. 29
   B. 32
   C. 33
   D. 40

   .. dropdown:: Answer
      :class-container: sd-border-success

      **D. 40**

      The members hold 4 + 8 + 16 + 1 = 29 bytes of data. The compiler adds **padding** so that each ``double`` starts at a multiple of 8:

      1. ``id`` takes bytes 0 to 3.
      2. Bytes 4 to 7 are padding, so ``battery_pct`` starts at byte 8.
      3. ``position`` takes bytes 16 to 31, and ``busy`` takes byte 32.
      4. Bytes 33 to 39 are padding, so that the next ``RobotStatus`` in an array also starts at a multiple of 8.

      32 is the size with the largest members first (``battery_pct``, ``position``, ``id``, ``busy``): the compiler never reorders members for you.

.. admonition:: Question 8
   :class: hint

   Given the following code, what is the type of ``func_ptr``?

   .. code-block:: cpp

      int multiply(int a, int b) { return a * b; }
      auto func_ptr = &multiply;

   A. ``int*``
   B. ``int(*)(int, int)``
   C. ``int&(int, int)``
   D. ``std::function<int(int, int)>``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. int(\*)(int, int)**

      ``&multiply`` produces a function pointer. The type is "pointer to a function taking two ``int``\s and returning ``int``", written as ``int(*)(int, int)``.

.. admonition:: Question 9
   :class: hint

   What does the ``mutable`` keyword do when used with a lambda?

   A. It allows the lambda to modify global variables.
   B. It allows the lambda to modify its copies of variables captured by value.
   C. It makes the lambda thread-safe.
   D. It allows the lambda to be called multiple times.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It allows the lambda to modify its copies of variables captured by value.**

      By default, variables captured by value are ``const`` inside the lambda. The ``mutable`` keyword removes this restriction, allowing the lambda to modify its internal copies. The original variables in the enclosing scope are not affected.

.. admonition:: Question 10
   :class: hint

   What do the two ``std::count_if`` calls return?

   .. code-block:: cpp

      std::vector<double> battery_pct{82.5, 35.0, 64.0, 18.0};
      double limit_pct{40.0};
      auto is_low = [limit_pct](double pct) { return pct < limit_pct; };
      auto is_low_ref = [&limit_pct](double pct) { return pct < limit_pct; };

      limit_pct = 70.0;
      std::count_if(battery_pct.begin(), battery_pct.end(), is_low);      // ?
      std::count_if(battery_pct.begin(), battery_pct.end(), is_low_ref);  // ?

   A. 2 and 2
   B. 2 and 3
   C. 3 and 3
   D. 3 and 2

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 2 and 3**

      1. ``[limit_pct]`` copies 40 **when the lambda is created**. Changing ``limit_pct`` later does not reach the copy, so ``is_low`` counts the levels under 40: 35.0 and 18.0, so 2.
      2. ``[&limit_pct]`` stores a reference, so ``is_low_ref`` reads ``limit_pct`` **at each call**, when it is 70. The levels under 70 are 35.0, 64.0 and 18.0, so 3.

True/False (Questions 11 to 15)
=================================

.. admonition:: Question 11
   :class: hint

   **True or False**: Structured bindings can only decompose ``struct`` types, not ``std::pair`` or ``std::tuple``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Structured bindings (``auto [a, b] = ...``) work with ``struct`` types, ``std::pair``, ``std::tuple``, and arrays. They bind to the members/elements in declaration order.

.. admonition:: Question 12
   :class: hint

   **True or False**: A lambda with the capture default ``[=]`` copies every local variable its body uses, and the body cannot change those copies unless the lambda is ``mutable``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      ``[=]`` copies each local the body uses, not every variable in scope. A copy captured by value is read-only inside the body: ``++assigned`` fails with ``increment of read-only variable 'assigned'``. ``mutable`` lets the body change its copies; the originals stay unchanged.

.. admonition:: Question 13
   :class: hint

   **True or False**: The call ``same_id(3, 3L)`` compiles with this template.

   .. code-block:: cpp

      template <std::integral T>
      bool same_id(T first, T second) { return first == second; }

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Both parameters are ``T``, so both arguments must give the same ``T``. ``3`` is an ``int`` and ``3L`` is a ``long``, so deduction fails: ``deduced conflicting types for parameter 'T' ('int' and 'long int')``. With form 3, ``bool same_id(std::integral auto first, std::integral auto second)``, each ``auto`` is its own type, and the call compiles.

.. admonition:: Question 14
   :class: hint

   **True or False**: Calling a default-constructed (empty) ``std::function`` object results in a ``std::bad_function_call`` exception.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      A default-constructed ``std::function`` holds no callable. Invoking it throws ``std::bad_function_call``. You should check with ``if (func) { ... }`` before calling it if the function might be empty.

.. admonition:: Question 15
   :class: hint

   **True or False**: ``make_filter`` is safe, because the lambda keeps a reference to ``limit_pct``.

   .. code-block:: cpp

      auto make_filter(double limit_pct) {
        return [&limit_pct](double pct) { return pct < limit_pct; };
      }

      auto is_low = make_filter(40.0);
      is_low(30.0);

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      ``limit_pct`` is a parameter, so it dies when ``make_filter`` returns. The lambda keeps a reference to it, so every call to ``is_low`` reads a dead variable: a dangling reference. AddressSanitizer reports ``stack-use-after-return``. A lambda that leaves the function must capture by value: ``[limit_pct]``. Rule: Core Guidelines F.53.
