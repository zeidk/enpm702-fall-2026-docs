====================================================
C++ Exercises
====================================================


.. note::

   **Not graded, and not submitted on Canvas.** These exercises belong to
   a self-study reading module: work them at your own pace. Write your
   answer for each expression first, then check it with the ``CATEGORY``
   helper from :doc:`vcat_lecture` and open the solution.
   ``702run week7_value_categories exercises`` prints the answers of
   Exercises 1 to 5 and 7, and ``702run week7_value_categories dangling``
   shows Exercise 6: ``whole`` works, and ``second`` stops the program.

.. dropdown:: Exercise 1: Names, Literals and Operators
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write lvalue, xvalue or prvalue for each expression, and the step
   (1 to 4) that decides it.

   .. code-block:: cpp

      int speed{30};
      const int limit{50};
      int& ref{speed};
      int lanes[2]{1, 2};
      int* lane{&lanes[0]};

   .. code-block:: cpp

      speed            // 1
      limit            // 2
      ref              // 3
      30               // 4
      speed - 5        // 5
      *lane            // 6
      lanes[1]         // 7
      speed--          // 8
      --speed          // 9
      speed < limit    // 10
      &speed           // 11
      speed = limit    // 12
      "lane"           // 13

   .. dropdown:: Solution
      :class-container: sd-border-success

      1. ``speed``: **lvalue**. Step 1: a name.
      2. ``limit``: **lvalue**. Step 1: a name. ``const`` does not change
         the category.
      3. ``ref``: **lvalue**. Step 1: a reference is another name for
         ``speed``.
      4. ``30``: **prvalue**. Step 2: a number literal.
      5. ``speed - 5``: **prvalue**. Step 4: a computed number.
      6. ``*lane``: **lvalue**. Step 4: the object ``lane`` points at,
         ``lanes[0]``.
      7. ``lanes[1]``: **lvalue**. Step 4: an element of a named array.
      8. ``speed--``: **prvalue**. Step 4: postfix ``--`` gives a copy of
         the old value.
      9. ``--speed``: **lvalue**. Step 4: prefix ``--`` gives ``speed``
         itself.
      10. ``speed < limit``: **prvalue**. Step 4: a computed ``bool``.
      11. ``&speed``: **prvalue**. Step 4: a computed address.
      12. ``speed = limit``: **lvalue**. Step 4: the result of ``=`` is
          ``speed``.
      13. ``"lane"``: **lvalue**. Step 2: a string literal.


.. dropdown:: Exercise 2: Function Calls and Casts
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Write lvalue, xvalue or prvalue for each expression. Only the
   declarations are given: the return types are enough.

   .. code-block:: cpp

      struct Sensor { int id{0}; double range{0.0}; };

      Sensor make_sensor(int id);                                 // by value
      Sensor& front_sensor(std::vector<Sensor>& sensors);
      const Sensor& rear_sensor(const std::vector<Sensor>& sensors);
      Sensor&& release(Sensor& sensor);                           // returns std::move(sensor)

      std::vector<Sensor> sensors{make_sensor(1), make_sensor(2)};
      std::string name{"lidar"};

   .. code-block:: cpp

      make_sensor(1)                         // 1
      front_sensor(sensors)                  // 2
      rear_sensor(sensors)                   // 3
      release(sensors[0])                    // 4
      sensors.size()                         // 5
      sensors.back()                         // 6
      name + "_front"                        // 7
      std::move(name)                        // 8
      static_cast<double>(sensors.size())    // 9
      static_cast<Sensor&&>(sensors[0])      // 10

   .. dropdown:: Solution
      :class-container: sd-border-success

      Step 3 decides every line: read the return type, or the type of
      the cast.

      1. ``make_sensor(1)``: **prvalue**. Returns ``Sensor``, no ``&``.
      2. ``front_sensor(sensors)``: **lvalue**. Returns ``Sensor&``. The
         ``&`` on the parameter plays no part.
      3. ``rear_sensor(sensors)``: **lvalue**. Returns ``const Sensor&``.
      4. ``release(sensors[0])``: **xvalue**. Returns ``Sensor&&``, the
         same as ``std::move``.
      5. ``sensors.size()``: **prvalue**. Returns ``std::size_t`` by value.
      6. ``sensors.back()``: **lvalue**. Returns a reference to the last
         element.
      7. ``name + "_front"``: **prvalue**. ``operator+`` returns a new
         ``std::string`` by value.
      8. ``std::move(name)``: **xvalue**. Returns ``std::string&&``.
      9. ``static_cast<double>(sensors.size())``: **prvalue**. A cast to a
         type with no ``&``.
      10. ``static_cast<Sensor&&>(sensors[0])``: **xvalue**. A cast to
          ``Sensor&&``.


.. dropdown:: Exercise 3: Member Access and Temporaries
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Use the declarations of Exercise 2. For each expression, find the
   category of the part before ``.`` or ``->`` first.

   .. code-block:: cpp

      sensors[0].range                 // 1
      make_sensor(1).range             // 2
      std::move(sensors[0]).id         // 3
      release(sensors[0]).range        // 4
      front_sensor(sensors).id         // 5
      Sensor{}.id                      // 6
      Sensor{}                         // 7
      sensors.data()->range            // 8
      std::vector<Sensor>{}.size()     // 9
      (*sensors.data()).id             // 10

   ``sensors.data()`` returns a ``Sensor*`` that points at the first
   element.

   .. dropdown:: Solution
      :class-container: sd-border-success

      1. ``sensors[0].range``: **lvalue**. ``sensors[0]`` is an lvalue, so
         its member is an lvalue.
      2. ``make_sensor(1).range``: **xvalue**. ``make_sensor(1)`` is a
         prvalue. A temporary is made for ``.range``, and its member is an
         xvalue.
      3. ``std::move(sensors[0]).id``: **xvalue**. A member of an xvalue.
      4. ``release(sensors[0]).range``: **xvalue**. ``release`` returns
         ``Sensor&&``, so the call is an xvalue, and so is its member.
      5. ``front_sensor(sensors).id``: **lvalue**. A member of an lvalue.
      6. ``Sensor{}.id``: **xvalue**. ``Sensor{}`` is a prvalue, so the
         same as line 2.
      7. ``Sensor{}``: **prvalue**. A type name followed by braces.
      8. ``sensors.data()->range``: **lvalue**. ``->`` follows a pointer,
         and the object a pointer points at is an lvalue.
      9. ``std::vector<Sensor>{}.size()``: **prvalue**. The last operation
         is the call to ``size()``, which returns by value.
      10. ``(*sensors.data()).id``: **lvalue**. The same as line 8, written
          with ``*`` and ``.``.


.. dropdown:: Exercise 4: Copy or Move?
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   With the declarations of Exercise 2, predict what each call prints.

   .. code-block:: cpp
      :linenos:

      void store(const Sensor&) { std::cout << "copy\n"; }
      void store(Sensor&&) { std::cout << "move\n"; }

      Sensor lidar{1, 100.0};
      Sensor&& radar{make_sensor(2)};
      const Sensor camera{3, 50.0};

      store(lidar);
      store(make_sensor(4));
      store(radar);
      store(std::move(radar));
      store(camera);
      store(std::move(camera));
      store(Sensor{5, 20.0});
      store(release(lidar));

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: text

         copy
         move
         copy
         move
         copy
         copy
         move
         move

      - Line 8: ``lidar`` is an lvalue: ``copy``.
      - Line 9: ``make_sensor(4)`` is a prvalue: ``move``.
      - Line 10: ``radar`` has the type ``Sensor&&``, but the expression is
        a name, an lvalue: ``copy``.
      - Line 11: ``std::move(radar)`` is an xvalue: ``move``.
      - Line 12: ``camera`` is an lvalue: ``copy``.
      - Line 13: ``std::move(camera)`` is an xvalue of type
        ``const Sensor&&``. It cannot bind to ``Sensor&&``, so: ``copy``.
      - Line 14: ``Sensor{5, 20.0}`` is a prvalue: ``move``.
      - Line 15: ``release`` returns ``Sensor&&``, an xvalue: ``move``.


.. dropdown:: Exercise 5: Find the Copy
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The caller below wants ``planner.path`` to take the block of 1000 poses
   that ``path`` holds, with no pose copied.

   .. code-block:: cpp
      :linenos:

      struct Planner { std::vector<Pose> path; };

      void give_path(Planner& planner, std::vector<Pose>&& path) {
        planner.path = path;
      }

      Planner planner{};
      std::vector<Pose> path{make_path(1000)};
      const Pose* where{path.data()};  // where path's block is
      give_path(planner, std::move(path));
      std::cout << std::boolalpha << (planner.path.data() == where) << ' '
                << path.size() << '\n';

   1. What does line 11 print?
   2. Which line copies, and why?
   3. Fix it with one change.

   .. dropdown:: Solution
      :class-container: sd-border-success

      1. It prints ``false 1000``: ``planner.path`` got a new block, and
         ``path`` still holds its 1000 poses.
      2. Line 4. Inside ``give_path``, ``path`` has the type
         ``std::vector<Pose>&&``, but the expression ``path`` is a name,
         an lvalue (Step 1). The assignment receives an lvalue, so it
         copies. The ``std::move`` on line 10 only lets ``give_path``
         receive the vector; it does not carry into the function.
      3. Mark the parameter again:

         .. code-block:: cpp

            planner.path = std::move(path);

         Line 11 then prints ``true 0``: ``planner.path`` holds the block
         ``path`` had, and ``path`` is empty (libstdc++).


.. dropdown:: Exercise 6: A Reference Into a Temporary
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   .. code-block:: cpp
      :linenos:

      const std::vector<Pose>& whole{make_path(3)};
      const Pose& second{make_path(3)[1]};
      std::cout << whole[2].x << '\n';
      std::cout << second.x << '\n';

   1. What is the category of ``make_path(3)`` on line 1, and of
      ``make_path(3)[1]`` on line 2?
   2. Line 3 prints ``2``. Built with ``-fsanitize=address``, line 4
      stops the program with ``heap-use-after-free``. Why does one
      reference work and the other not?

   .. dropdown:: Solution
      :class-container: sd-border-success

      1. ``make_path(3)`` is a **prvalue** (it returns by value).
         ``make_path(3)[1]`` is an **lvalue**: ``operator[]`` returns
         ``Pose&``.
      2. On line 1, ``whole`` binds to the temporary vector itself, so the
         temporary lives as long as ``whole``. On line 2, ``second`` binds
         to the ``Pose&`` that ``operator[]`` returned, not to the
         temporary vector. The vector is destroyed at the end of line 2,
         and the block that held the element is freed with it. Line 4
         reads freed memory. g++ warns about line 2 with
         ``-Wdangling-reference``.


.. dropdown:: Exercise 7: Write One of Each
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Using only ``std::vector<Pose> seen{make_path(3)};``, write an
   expression of each category: one lvalue, one xvalue and one prvalue.
   Check each one with ``static_assert(CATEGORY(e) == "...");``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      Many answers work. One set:

      .. code-block:: cpp

         static_assert(CATEGORY(seen) == "lvalue");             // a name
         static_assert(CATEGORY(std::move(seen)) == "xvalue");  // returns T&&
         static_assert(CATEGORY(seen.size()) == "prvalue");     // returns by value

      Others: ``seen[0]`` and ``seen.front().x`` are lvalues,
      ``std::move(seen[0])`` is an xvalue, and ``seen.empty()`` is a
      prvalue.
