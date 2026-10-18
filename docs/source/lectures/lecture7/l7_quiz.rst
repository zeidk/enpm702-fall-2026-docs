.. _l7_quiz:

================
Lecture 7 Quiz
================

This quiz covers the key concepts from Lecture 7: Smart Pointers and Move Semantics. Topics include the owner of a heap object and the leak LeakSanitizer reports, moves, value categories, rvalue references, ``std::move``, ``std::unique_ptr``, ``std::shared_ptr``, ``std::weak_ptr``, and reference cycles. Question 15 comes from the Further Reading part of the lecture.

The code uses the fleet types ``Position`` and ``RobotStatus`` from ``project/week7/common/fleet.hpp``, and ``make_route(n)`` returns a ``std::vector<Position>`` of ``n`` waypoints, as in the lecture. Each snippet is part of a full program. Every output shown was measured with g++ 13.3 and libstdc++, with ``-std=c++20 -Wall -Wextra -fsanitize=address,undefined``.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1 to 10)
=====================================

.. admonition:: Question 1
   :class: hint

   In L7, what makes a piece of code the **owner** of a heap object?

   A. It holds a pointer to the object.
   B. It keeps the object alive, and the last owner to let go deletes it.
   C. It called the function that created the object.
   D. It reads the object more often than any other code.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It keeps the object alive, and the last owner to let go deletes it.**

      An owner of a heap object is code that keeps it alive. An object can have one owner or several: the last owner to let go deletes it. Holding a pointer is not enough: a ``RobotStatus*`` looks the same whether it owns the robot or only points at it. The Core Guidelines say so in R.3: "A raw pointer (a ``T*``) is non-owning". An owner needs a type that says it owns, and a smart pointer is that type.

.. admonition:: Question 2
   :class: hint

   ``make_robot`` creates a robot with ``new``:

   .. code-block:: cpp

      RobotStatus* make_robot(int id, double battery_pct) {
        return new RobotStatus{id, battery_pct, {0.0, 0.0}, false};
      }

      bool needs_charge(int id) {
        RobotStatus* robot{make_robot(id, 64.0)};
        if (robot->battery_pct > 20.0) {
          return false;  // leaves without delete
        }
        delete robot;
        return true;
      }

   You compile with ``-fsanitize=address`` and call ``needs_charge(3)``. What happens?

   A. The code does not compile, because one path has no ``delete``.
   B. The program crashes at ``return false;``.
   C. The call returns ``false``. When the program ends, LeakSanitizer reports a leak of 40 bytes and names the line that called ``new``.
   D. Nothing is reported, because the program ends and the memory goes back to the system.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The call returns false. When the program ends, LeakSanitizer reports a leak of 40 bytes and names the line that called new.**

      The robot has 64.0 % battery, which is more than 20.0, so the function returns ``false`` before it reaches ``delete``. The compiler does not check that every path deletes. A ``main`` that prints the result gives this output, with the stack trace shortened:

      .. code-block:: text

         needs_charge(3): false

         =================================================================
         ==1850352==ERROR: LeakSanitizer: detected memory leaks

         Direct leak of 40 byte(s) in 1 object(s) allocated from:
             #0 0x7cb7f1afe548 in operator new(unsigned long) ...

         SUMMARY: AddressSanitizer: 40 byte(s) leaked in 1 allocation(s).

      40 bytes is one ``RobotStatus``, the size measured in L6. You do not need a separate flag: AddressSanitizer "integrates LeakSanitizer and enables it by default on supported platforms".

.. admonition:: Question 3
   :class: hint

   Given these declarations:

   .. code-block:: cpp

      std::vector<Position> route{make_route(3)};
      std::vector<RobotStatus> fleet{make_robot(1), make_robot(2)};
      int a{2};
      int b{3};

   Here ``make_robot(int)`` returns a ``RobotStatus`` by value. Which expression is a **prvalue**?

   A. ``route``
   B. ``fleet[0]``
   C. ``"dock"``
   D. ``a + b``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **D. a + b**

      A prvalue is a value that will initialize an object. No object exists yet. ``a + b`` is a built-in arithmetic result, so it is a prvalue. ``route`` and ``fleet[0]`` name objects that live on after the expression: they are lvalues. A string literal such as ``"dock"`` is an array with an address, so it is an lvalue too.

      The program prints each category with the ``decltype((e))`` test from the lecture:

      .. code-block:: text

         route: lvalue
         fleet[0]: lvalue
         "dock": lvalue
         a + b: prvalue

      You can also try to take the address. ``&fleet[0]`` compiles, but ``&(a + b)`` does not:

      .. code-block:: text

         error: lvalue required as unary ‘&’ operand

.. admonition:: Question 4
   :class: hint

   What is ``decltype((r))`` here?

   .. code-block:: cpp

      std::vector<Position>&& r{make_route(10)};

   A. ``std::vector<Position>``
   B. ``std::vector<Position>&``
   C. ``std::vector<Position>&&``
   D. ``const std::vector<Position>&``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. std::vector<Position>&**

      The **type** of ``r`` is an rvalue reference, ``std::vector<Position>&&``. That is what ``decltype(r)`` gives, with one pair of parentheses. The **expression** ``r`` is an lvalue: it has a name, and you can use it again on the next line. ``decltype((e))`` gives ``T&`` for an lvalue, so ``decltype((r))`` is ``std::vector<Position>&``. Both of these compile:

      .. code-block:: cpp

         static_assert(std::is_same_v<decltype(r), std::vector<Position>&&>);
         static_assert(std::is_same_v<decltype((r)), std::vector<Position>&>);

      So a function with a ``T&&`` parameter must write ``std::move`` again to move from it.

.. admonition:: Question 5
   :class: hint

   ``route`` holds 1000 waypoints, and each ``Position`` is 16 bytes.

   .. code-block:: cpp

      std::vector<Position> route{make_route(1000)};
      const Position* where{route.data()};
      std::vector<Position> moved{std::move(route)};

   How many bytes does the move hand from ``route`` to ``moved``?

   A. 16000
   B. 1000
   C. 24
   D. 0

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. 24**

      ``route`` owns its heap block through three pointers: begin, end and capacity. The move gives those three pointers to ``moved`` and sets ``route``'s to null (libstdc++). No element is copied and nothing is allocated. Only the ``std::vector`` object itself changes hands, and it is 24 bytes, whatever the vector holds. The program prints:

      .. code-block:: text

         moved.data() == where: true
         sizeof(std::vector<Position>): 24
         sizeof(Position): 16

      ``moved.data() == where`` shows that ``moved`` holds the same block. A copy would allocate a new block and copy every element: 1000 times 16 bytes, which is 16000 bytes.

.. admonition:: Question 6
   :class: hint

   What happens here?

   .. code-block:: cpp

      const std::vector<Position> route{make_route(1000)};
      std::vector<Position> robot_route{std::move(route)};

   A. It does not compile, because a ``const`` object cannot be moved.
   B. It moves: ``robot_route`` takes the block, and ``route`` is left empty.
   C. It compiles with no warning, and it copies: ``route`` still holds 1000 waypoints.
   D. It is undefined behavior.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. It compiles with no warning, and it copies: route still holds 1000 waypoints.**

      ``std::move(route)`` has type ``const std::vector<Position>&&``. It cannot bind to the move constructor's ``std::vector<Position>&&``, which would change ``route``. It does bind to the copy constructor's ``const std::vector<Position>&``, so the compiler copies. With ``-Wall -Wextra``, g++ prints no warning. The program prints:

      .. code-block:: text

         robot_route.data() == route.data(): false, route.size(): 1000

      A ``const`` object cannot be moved from. Declare an object ``const`` only if you will not hand it on.

.. admonition:: Question 7
   :class: hint

   You compile this with ``-Wall -Wextra``:

   .. code-block:: cpp

      std::vector<Position> plan_route(int n) {
        std::vector<Position> route{make_route(n)};
        return std::move(route);
      }

      std::vector<Position> path{plan_route(1000)};

   What does g++ say?

   A. Nothing. The ``std::move`` makes the return faster.
   B. It warns that moving a local object in a return statement prevents copy elision.
   C. It stops with an error: ``std::move`` cannot be used in a ``return``.
   D. It warns that ``route`` is copied into ``path``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It warns that moving a local object in a return statement prevents copy elision.**

      .. code-block:: text

         q07.cpp:17:19: warning: moving a local object in a return statement prevents copy elision [-Wpessimizing-move]
            17 |   return std::move(route);
               |          ~~~~~~~~~^~~~~~~
         q07.cpp:17:19: note: remove ‘std::move’ call

      L5: a local returned by value is constructed in place, or moved if it cannot be. It is never copied. ``std::move`` on the return turns the local into an xvalue, and the compiler can no longer build it in place. The program still runs (``path.size()`` is 1000), but you lost the in-place construction. Write ``return route;``. The Core Guidelines rule is F.48: "Don't ``return std::move(local)``".

.. admonition:: Question 8
   :class: hint

   ``retire`` takes ownership of a robot:

   .. code-block:: cpp

      std::vector<std::unique_ptr<RobotStatus>> retired;

      void retire(std::unique_ptr<RobotStatus> robot) {  // takes ownership
        retired.push_back(std::move(robot));
      }

      auto robot{std::make_unique<RobotStatus>(3, 64.0, Position{2.0, 3.0}, false)};

   Which call compiles?

   A. ``retire(robot);``
   B. ``retire(std::move(robot));``
   C. ``retire(robot.get());``
   D. ``retire(*robot);``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. retire(std::move(robot));**

      The parameter is taken by value, so it is a new owner. The caller must hand the robot over with ``std::move``, and the call shows that ownership moves. After it, the program prints:

      .. code-block:: text

         robot == nullptr: true, retired.size(): 1

      The other three do not compile. A would copy a ``std::unique_ptr``, and its copy constructor is deleted:

      .. code-block:: text

         error: use of deleted function ‘std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&) [with _Tp = RobotStatus; _Dp = std::default_delete<RobotStatus>]’

      C passes a plain ``RobotStatus*``, and D passes a ``RobotStatus``. g++ rejects both with "could not convert ... to ‘std::unique_ptr<RobotStatus>’". The Core Guidelines rule is R.32: "Take a ``unique_ptr<widget>`` parameter to express that a function assumes ownership of a ``widget``".

.. admonition:: Question 9
   :class: hint

   What does ``robot.use_count()`` return after the last line?

   .. code-block:: cpp

      auto robot{std::make_shared<RobotStatus>(3, 14.0, Position{2.0, 3.0}, false)};
      std::shared_ptr<RobotStatus> in_fleet{robot};
      std::shared_ptr<RobotStatus> in_queue{robot};
      std::shared_ptr<RobotStatus> moved{std::move(in_queue)};
      in_fleet.reset();

   A. 1
   B. 2
   C. 3
   D. 4

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 2**

      Count the owners line by line:

      1. ``std::make_shared`` creates the robot with one owner, ``robot``: 1.
      2. ``in_fleet`` is a copy, one more owner: 2.
      3. ``in_queue`` is a copy, one more owner: 3.
      4. ``moved`` takes ``in_queue``'s place. A move hands one owner's place to another, so the count stays at 3, and ``in_queue`` is left empty.
      5. ``in_fleet.reset()`` gives up this owner's place: 2.

      The two owners left are ``robot`` and ``moved``. The program prints ``robot.use_count(): 2``.

.. admonition:: Question 10
   :class: hint

   Two robots are partners, and each holds the other in a ``std::shared_ptr``:

   .. code-block:: cpp

      struct Robot {
        RobotStatus status;
        std::shared_ptr<Robot> partner;
      };

      {
        auto a{std::make_shared<Robot>(RobotStatus{1, 82.5})};
        auto b{std::make_shared<Robot>(RobotStatus{2, 35.0})};
        a->partner = b;  // a owns b
        b->partner = a;  // b owns a
        std::cout << "a.use_count(): " << a.use_count() << ", b.use_count(): " << b.use_count()
                  << '\n';
      }  // a and b are destroyed here
      std::cout << "end of main\n";

   What happens to the two robots at the closing brace?

   A. Both robots are deleted, because ``a`` and ``b`` are destroyed.
   B. Only robot 1 is deleted, because ``a`` was created first.
   C. Neither is deleted. Each count drops from 2 to 1, never to 0, and LeakSanitizer reports both robots at exit.
   D. The code does not compile, because a ``struct`` cannot hold a ``std::shared_ptr`` to its own type.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Neither is deleted. Each count drops from 2 to 1, never to 0, and LeakSanitizer reports both robots at exit.**

      Inside the block, each robot has two owners: its own variable and the other robot's ``partner``. When ``a`` and ``b`` are destroyed, each count drops to 1. Each robot keeps the other alive, and nothing outside can reach either. The output, with the stack traces left out:

      .. code-block:: text

         a.use_count(): 2, b.use_count(): 2
         end of main

         =================================================================
         ==1850356==ERROR: LeakSanitizer: detected memory leaks

         Indirect leak of 72 byte(s) in 1 object(s) allocated from:

         Indirect leak of 72 byte(s) in 1 object(s) allocated from:

         SUMMARY: AddressSanitizer: 144 byte(s) leaked in 2 allocation(s).

      Each allocation is 72 bytes: a ``Robot`` (40 bytes for the status, 16 for the ``std::shared_ptr``) and its 16-byte control block, in one ``std::make_shared`` allocation. **Indirect** means each robot is reachable only from the other leaked robot. The fix is a ``std::weak_ptr<Robot> partner``, which does not add to the count. The Core Guidelines rule is R.24: "Use ``std::weak_ptr`` to break cycles of ``shared_ptr``\ s".


True/False (Questions 11 to 15)
=================================

.. admonition:: Question 11
   :class: hint

   **True or False**: The statement ``std::move(route);`` on a line of its own moves the 1000 waypoints out of ``route``, so ``route.size()`` is 0 afterwards.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      ``std::move(route)`` is a cast to ``std::vector<Position>&&``. Its result is an xvalue: it marks ``route`` as "may be taken". The move happens later, if a move constructor or a ``&&`` overload takes the result. Here nothing does, so ``route.size()`` is still 1000. g++ warns, because the result is unused:

      .. code-block:: text

         q11.cpp:17:12: warning: ignoring return value of ‘constexpr typename std::remove_reference<_Tp>::type&& std::move(_Tp&&) [with _Tp = vector<Position>&; typename remove_reference<_Tp>::type = vector<Position>]’, declared with attribute ‘nodiscard’ [-Wunused-result]

.. admonition:: Question 12
   :class: hint

   **True or False**: After ``std::unique_ptr<RobotStatus> other{std::move(robot)};``, the C++ standard guarantees that ``robot`` is empty. After you move a ``std::vector``, the standard does not guarantee that the source vector is empty.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      For the move constructor of ``std::unique_ptr``, C++20 [unique.ptr.single.ctor] states the postcondition ``u.get() == nullptr``. The program prints:

      .. code-block:: text

         robot == nullptr: true, other->id: 3

      For other library types, C++20 [lib.types.movedfrom] says only that moved-from objects are left "in a valid but unspecified state". libstdc++ leaves a moved-from ``std::vector`` empty, but another library may not. With a moved-from vector, you may destroy it or assign it a new value, and then use it as before.

.. admonition:: Question 13
   :class: hint

   **True or False**: Making a ``std::weak_ptr`` from a ``std::shared_ptr`` adds 1 to ``use_count()``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      A ``std::weak_ptr`` watches the robot without owning it, so the count does not change. In this program, ``robot`` is the only owner:

      .. code-block:: cpp

         auto robot{std::make_shared<RobotStatus>(3, 14.0, Position{2.0, 3.0}, false)};
         std::weak_ptr<RobotStatus> watch{robot};
         std::cout << std::boolalpha;
         std::cout << "robot.use_count(): " << robot.use_count() << ", watch.expired(): " << watch.expired()
                   << '\n';
         robot.reset();  // the only owner lets go
         std::cout << "watch.use_count(): " << watch.use_count() << ", watch.expired(): " << watch.expired()
                   << '\n';

      .. code-block:: text

         robot.use_count(): 1, watch.expired(): false
         watch.use_count(): 0, watch.expired(): true

      The count stays at 1 while ``watch`` exists, and the robot is deleted as soon as ``robot`` lets go. This is why a ``std::weak_ptr`` can break a reference cycle.

.. admonition:: Question 14
   :class: hint

   **True or False**: A ``std::unique_ptr`` converts to a ``std::shared_ptr``, and a ``std::shared_ptr`` converts back to a ``std::unique_ptr``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Only the first direction works. ``std::shared_ptr<RobotStatus> robot{make_robot(5)};`` compiles when ``make_robot`` returns a ``std::unique_ptr``: one owner becomes the first of several. The other direction does not compile:

      .. code-block:: text

         error: no matching function for call to ‘std::unique_ptr<RobotStatus>::unique_ptr(<brace-enclosed initializer list>)’

      Other owners may exist, and a ``std::unique_ptr`` must be the only one. So a function that creates a robot returns a ``std::unique_ptr``, and the caller turns it into a ``std::shared_ptr`` if it needs to share.

.. admonition:: Question 15
   :class: hint

   **True or False**: ``other`` is a ``std::unique_ptr<RobotStatus>``. The line ``bool has_robot = other;`` compiles, because a ``std::unique_ptr`` converts to ``bool``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      The conversion to ``bool`` is ``explicit``. A condition may use it, so ``if (other)`` and ``!other`` work. The initialization with ``=`` does not:

      .. code-block:: text

         error: cannot convert ‘std::unique_ptr<RobotStatus>’ to ‘bool’ in initialization

      Write ``bool has_robot{other != nullptr};`` instead. ``if (other)``, ``!other`` and ``other == nullptr`` all test for empty, and the same works for ``std::shared_ptr``.
