.. _l7_quiz:

================
Lecture 7 Quiz
================

This quiz covers the key concepts from Lecture 7: Smart Pointers and Move Semantics. Topics include the owner of a heap object and the leak LeakSanitizer reports, moves, value categories, rvalue references, ``std::move``, ``std::unique_ptr``, ``std::shared_ptr``, ``std::weak_ptr``, and reference cycles.

The code uses the types ``Pose`` and ``Obstacle`` from ``project/week7/common/include/obstacle.hpp``, and ``make_path(n)`` returns a ``std::vector<Pose>`` of ``n`` poses, one meter apart, as in the lecture. Each snippet is part of a full program. Every output shown was measured with g++ 13.3 and libstdc++, with ``-std=c++20 -Wall -Wextra -fsanitize=address,undefined``.

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

      An owner of a heap object is code that keeps it alive. An object can have one owner or several: the last owner to let go deletes it. Holding a pointer is not enough: an ``Obstacle*`` looks the same whether it owns the ``Obstacle`` object or only points at it. The Core Guidelines say so in R.3: "A raw pointer (a ``T*``) is non-owning". An owner needs a type that says it owns, and a smart pointer is that type.

.. admonition:: Question 2
   :class: hint

   ``make_track`` creates an ``Obstacle`` with ``new``:

   .. code-block:: cpp

      Obstacle* make_track(int id, Pose pose, double speed) {
        return new Obstacle{id, pose, speed};
      }

      bool needs_braking(int id) {
        Obstacle* track{make_track(id, Pose{12.0, -1.0}, 4.0)};
        if (track->pose.x > 10.0) {
          return false;  // leaves without delete
        }
        delete track;
        return true;
      }

   You compile with ``-fsanitize=address`` and call ``needs_braking(2)``. What happens?

   A. The code does not compile, because one path has no ``delete``.
   B. The program crashes at ``return false;``.
   C. The call returns ``false``. When the program ends, LeakSanitizer reports a leak of 48 bytes and names the line that called ``new``.
   D. Nothing is reported, because the program ends and the memory goes back to the system.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. The call returns false. When the program ends, LeakSanitizer reports a leak of 48 bytes and names the line that called new.**

      The cyclist is 12 m ahead, more than 10 m, so the function returns ``false`` before it reaches ``delete``. The compiler does not check that every path deletes. A ``main`` that prints the result gives this output, with the stack trace shortened:

      .. code-block:: text

         needs_braking(2): false

         =================================================================
         ==327177==ERROR: LeakSanitizer: detected memory leaks

         Direct leak of 48 byte(s) in 1 object(s) allocated from:
             #0 0x7cf67a4fe548 in operator new(unsigned long) ...

         SUMMARY: AddressSanitizer: 48 byte(s) leaked in 1 allocation(s).

      48 bytes is one ``Obstacle``: ``sizeof(Obstacle)`` is 48 with g++ 13.3. You do not need a separate flag: AddressSanitizer "integrates LeakSanitizer and enables it by default on supported platforms".

.. admonition:: Question 3
   :class: hint

   Given these declarations:

   .. code-block:: cpp

      std::vector<Pose> path{make_path(3)};
      int a{2};
      int b{3};

   Which expression is a **prvalue**?

   A. ``path``
   B. ``std::move(path)``
   C. ``a``
   D. ``a + b``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **D. a + b**

      A prvalue does not refer to an object that already exists: it computes a value. ``a + b`` computes 5, and no object held that 5 before, so it is a prvalue. ``path`` and ``a`` name objects that already exist and do not let another object take their contents: they are lvalues. ``std::move(path)`` refers to ``path`` and marks it, so it is an xvalue.

      The program prints each category with the ``decltype((e))`` test from the lecture:

      .. code-block:: text

         path: lvalue
         std::move(path): xvalue
         a: lvalue
         a + b: prvalue

      You can also try to take the address. ``&a`` compiles, but ``&(a + b)`` does not:

      .. code-block:: text

         error: lvalue required as unary ‘&’ operand

.. admonition:: Question 4
   :class: hint

   What is ``decltype((r))`` here?

   .. code-block:: cpp

      std::vector<Pose>&& r{make_path(10)};

   A. ``std::vector<Pose>``
   B. ``std::vector<Pose>&``
   C. ``std::vector<Pose>&&``
   D. ``const std::vector<Pose>&``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. std::vector<Pose>&**

      The **type** of ``r`` is an rvalue reference, ``std::vector<Pose>&&``. That is what ``decltype(r)`` gives, with one pair of parentheses. The **expression** ``r`` is an lvalue: it has a name, and you can use it again on the next line. ``decltype((e))`` gives ``T&`` for an lvalue, so ``decltype((r))`` is ``std::vector<Pose>&``. Both of these compile:

      .. code-block:: cpp

         static_assert(std::is_same_v<decltype(r), std::vector<Pose>&&>);
         static_assert(std::is_same_v<decltype((r)), std::vector<Pose>&>);

      So a function with a ``T&&`` parameter must write ``std::move`` again to move from it.

.. admonition:: Question 5
   :class: hint

   ``path`` holds 1000 poses, and each ``Pose`` is 24 bytes.

   .. code-block:: cpp

      std::vector<Pose> path{make_path(1000)};
      const Pose* where{path.data()};
      std::vector<Pose> moved{std::move(path)};

   How many bytes does the move hand from ``path`` to ``moved``?

   A. 24000
   B. 1000
   C. 24
   D. 0

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. 24**

      ``path`` owns its heap block through three pointers: begin, end and capacity. The move gives those three pointers to ``moved`` and sets ``path``'s to null (libstdc++). No element is copied and nothing is allocated. Only the ``std::vector`` object itself changes hands, and it is 24 bytes, whatever the vector holds. The program prints:

      .. code-block:: text

         moved.data() == where: true
         sizeof(std::vector<Pose>): 24
         sizeof(Pose): 24

      ``moved.data() == where`` shows that ``moved`` holds the same block. ``sizeof(Pose)`` is also 24, three ``double``\ s, but that is not what moves: the 24 bytes are the vector's three pointers. A copy would allocate a new block and copy every element: 1000 times 24 bytes, which is 24000 bytes.

.. admonition:: Question 6
   :class: hint

   ``make_scores`` returns a local ``std::vector<int>`` by value, with ``return scores;``. Which line initializes its destination directly from the prvalue ``make_scores()``, with no move in between?

   .. code-block:: cpp

      std::vector<int> best{make_scores()};          // line 1
      std::vector<std::vector<int>> all;
      all.push_back(make_scores());                  // line 2

   A. Both lines: the compiler elides in both.
   B. Only line 1. In line 2, ``push_back`` takes a reference, so the prvalue becomes a temporary that is moved into the vector.
   C. Only line 2: ``push_back`` takes an rvalue reference, so nothing is moved.
   D. Neither: a vector returned from a function is always moved.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. Only line 1.**

      A prvalue that initializes an object of its own type is used to initialize that object directly (C++20 [dcl.init] 17.6.1), so ``best`` is built in place. ``push_back`` takes a ``std::vector<int>&&``: the reference binds to a temporary, and the element in the vector is move-constructed from it. ``702run week7_playground 14`` prints the address of the local and of its block, then the same two for the caller's vector (one run, g++ 13.3, the course flags):

      .. code-block:: text

         elision:
           inside: 0x7ffce43fc630 0x502000000010
           best:   0x7ffce43fc630 0x502000000010
         move:
           inside: 0x7ffce43fc670 0x502000000030
           all[0]: 0x503000000160 0x502000000030

      ``best`` is ``make_scores``'s local itself. ``all[0]`` is a new vector that holds the same block. (``return scores;`` is NRVO, which is permitted, not guaranteed: if the compiler does not do it, ``scores`` is moved out.)

.. admonition:: Question 7
   :class: hint

   You compile this with ``-Wall -Wextra``:

   .. code-block:: cpp

      std::vector<Pose> plan_path(int n) {
        std::vector<Pose> path{make_path(n)};
        return std::move(path);
      }

      std::vector<Pose> planned{plan_path(1000)};

   What does g++ say?

   A. Nothing. The ``std::move`` makes the return faster.
   B. It warns that moving a local object in a return statement prevents copy elision.
   C. It stops with an error: ``std::move`` cannot be used in a ``return``.
   D. It warns that ``path`` is copied into ``planned``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. It warns that moving a local object in a return statement prevents copy elision.**

      .. code-block:: text

         q07.cpp:4:19: warning: moving a local object in a return statement prevents copy elision [-Wpessimizing-move]
         q07.cpp:4:19: note: remove ‘std::move’ call

      L5: a local returned by value is constructed in place, or moved if it cannot be. It is never copied. ``std::move`` on the return turns the local into an xvalue, and the compiler can no longer build it in place. The program still runs (``planned.size()`` is 1000), but you lost the in-place construction. Write ``return path;``. The Core Guidelines rule is F.48: "Don't ``return std::move(local)``".

.. admonition:: Question 8
   :class: hint

   ``keep_lost`` takes ownership of a lost track:

   .. code-block:: cpp

      std::vector<std::unique_ptr<Obstacle>> lost;

      void keep_lost(std::unique_ptr<Obstacle> track) {  // takes ownership
        lost.push_back(std::move(track));
      }

      auto track{std::make_unique<Obstacle>(2, Pose{12.0, -1.0, 0.0}, 4.0)};

   Which call compiles?

   A. ``keep_lost(track);``
   B. ``keep_lost(std::move(track));``
   C. ``keep_lost(track.get());``
   D. ``keep_lost(*track);``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. keep_lost(std::move(track));**

      The parameter is taken by value, so it is a new owner. The caller must hand the ``Obstacle`` object over with ``std::move``, and the call shows that ownership moves. After it, the program prints:

      .. code-block:: text

         track == nullptr: true, lost.size(): 1

      The other three do not compile. A would copy a ``std::unique_ptr``, and its copy constructor is deleted:

      .. code-block:: text

         error: use of deleted function ‘std::unique_ptr<_Tp, _Dp>::unique_ptr(const std::unique_ptr<_Tp, _Dp>&) [with _Tp = Obstacle; _Dp = std::default_delete<Obstacle>]’

      C passes a plain ``Obstacle*``, and D passes an ``Obstacle``. g++ rejects both with "could not convert ... to ‘std::unique_ptr<Obstacle>’". The Core Guidelines rule is R.32: "Take a ``unique_ptr<widget>`` parameter to express that a function assumes ownership of a ``widget``".

.. admonition:: Question 9
   :class: hint

   What does ``track.use_count()`` return after the last line?

   .. code-block:: cpp

      auto track{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
      std::shared_ptr<Obstacle> in_tracker{track};
      std::shared_ptr<Obstacle> in_hazards{track};
      std::shared_ptr<Obstacle> moved{std::move(in_hazards)};
      in_tracker.reset();

   A. 1
   B. 2
   C. 3
   D. 4

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 2**

      Count the owners line by line:

      1. ``std::make_shared`` creates the ``Obstacle`` object with one owner, ``track``: 1.
      2. ``in_tracker`` is a copy, one more owner: 2.
      3. ``in_hazards`` is a copy, one more owner: 3.
      4. ``moved`` takes ``in_hazards``'s place. A move hands one owner's place to another, so the count stays at 3, and ``in_hazards`` is left empty.
      5. ``in_tracker.reset()`` gives up this owner's place: 2.

      The two owners left are ``track`` and ``moved``. The program prints ``track.use_count(): 2``.

.. admonition:: Question 10
   :class: hint

   A tractor tows a trailer, and each ``Towing`` object holds the other in a ``std::shared_ptr``:

   .. code-block:: cpp

      struct Towing {
        Obstacle obstacle;
        std::shared_ptr<Towing> other;
      };

      {
        auto a{std::make_shared<Towing>(Obstacle{5, {60.0, 0.0}, 8.0})};
        auto b{std::make_shared<Towing>(Obstacle{6, {54.0, 0.0}, 8.0})};
        a->other = b;  // a's Towing owns b's
        b->other = a;  // b's Towing owns a's
        std::cout << "a.use_count(): " << a.use_count() << ", b.use_count(): " << b.use_count()
                  << '\n';
      }  // a and b are destroyed here
      std::cout << "end of main\n";

   What happens to the two ``Towing`` objects at the closing brace?

   A. Both are deleted, because ``a`` and ``b`` are destroyed.
   B. Only the tractor's is deleted, because ``a`` was created first.
   C. Neither is deleted. Each count drops from 2 to 1, never to 0, and LeakSanitizer reports both at exit.
   D. The code does not compile, because a ``struct`` cannot hold a ``std::shared_ptr`` to its own type.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **C. Neither is deleted. Each count drops from 2 to 1, never to 0, and LeakSanitizer reports both at exit.**

      Inside the block, each ``Towing`` object has two owners: its own variable and the other object's ``other``. When ``a`` and ``b`` are destroyed, each count drops to 1. Each object keeps the other alive, and nothing outside can reach either. The output, with the stack traces left out:

      .. code-block:: text

         a.use_count(): 2, b.use_count(): 2
         end of main

         =================================================================
         ==327185==ERROR: LeakSanitizer: detected memory leaks

         Indirect leak of 80 byte(s) in 1 object(s) allocated from:

         Indirect leak of 80 byte(s) in 1 object(s) allocated from:

         SUMMARY: AddressSanitizer: 160 byte(s) leaked in 2 allocation(s).

      Each allocation is 80 bytes: a ``Towing`` (48 bytes for the ``Obstacle``, 16 for the ``std::shared_ptr``: ``sizeof(Towing)`` is 64) and its 16-byte control block, in one ``std::make_shared`` allocation. **Indirect** means each object is reachable only from the other leaked object. The fix is a ``std::weak_ptr<Towing> other``, which does not add to the count. The Core Guidelines rule is R.24: "Use ``std::weak_ptr`` to break cycles of ``shared_ptr``\ s".


True/False (Questions 11 to 15)
=================================

.. admonition:: Question 11
   :class: hint

   **True or False**: The statement ``std::move(path);`` on a line of its own moves the 1000 poses out of ``path``, so ``path.size()`` is 0 afterwards.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      ``std::move(path)`` is a cast to ``std::vector<Pose>&&``. Its result is an xvalue: it marks ``path`` as "may be taken". The move happens later, if a move constructor or a ``&&`` overload takes the result. Here nothing does, so ``path.size()`` is still 1000. g++ warns, because the result is unused:

      .. code-block:: text

         q11.cpp:4:12: warning: ignoring return value of ‘constexpr typename std::remove_reference<_Tp>::type&& std::move(_Tp&&) [with _Tp = vector<Pose>&; typename remove_reference<_Tp>::type = vector<Pose>]’, declared with attribute ‘nodiscard’ [-Wunused-result]

.. admonition:: Question 12
   :class: hint

   **True or False**: After ``std::unique_ptr<Obstacle> other{std::move(track)};``, the C++ standard guarantees that ``track`` is empty. After you move a ``std::vector``, the standard does not guarantee that the source vector is empty.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **True.**

      For the move constructor of ``std::unique_ptr``, C++20 [unique.ptr.single.ctor] states the postcondition ``u.get() == nullptr``. The program prints:

      .. code-block:: text

         track == nullptr: true, other->id: 2

      For other library types, C++20 [lib.types.movedfrom] says only that moved-from objects are left "in a valid but unspecified state". libstdc++ leaves a moved-from ``std::vector`` empty, but another library may not. With a moved-from vector, you may destroy it or assign it a new value, and then use it as before.

.. admonition:: Question 13
   :class: hint

   **True or False**: Making a ``std::weak_ptr`` from a ``std::shared_ptr`` adds 1 to ``use_count()``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      A ``std::weak_ptr`` watches the ``Obstacle`` object without owning it, so the count does not change. In this program, ``track`` is the only owner:

      .. code-block:: cpp

         auto track{std::make_shared<Obstacle>(2, Pose{12.0, -1.0}, 4.0)};
         std::weak_ptr<Obstacle> shown{track};
         std::cout << std::boolalpha;
         std::cout << "track.use_count(): " << track.use_count() << ", shown.expired(): " << shown.expired()
                   << '\n';
         track.reset();  // the only owner lets go
         std::cout << "shown.use_count(): " << shown.use_count() << ", shown.expired(): " << shown.expired()
                   << '\n';

      .. code-block:: text

         track.use_count(): 1, shown.expired(): false
         shown.use_count(): 0, shown.expired(): true

      The count stays at 1 while ``shown`` exists, and the ``Obstacle`` object is deleted as soon as ``track`` lets go. This is why a ``std::weak_ptr`` can break a reference cycle.

.. admonition:: Question 14
   :class: hint

   **True or False**: A ``std::unique_ptr`` converts to a ``std::shared_ptr``, and a ``std::shared_ptr`` converts back to a ``std::unique_ptr``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **False.**

      Only the first direction works. ``std::shared_ptr<Obstacle> hazard{make_track(5)};`` compiles when ``make_track`` returns a ``std::unique_ptr``: one owner becomes the first of several. The other direction does not compile:

      .. code-block:: text

         error: no matching function for call to ‘std::unique_ptr<Obstacle>::unique_ptr(<brace-enclosed initializer list>)’

      Other owners may exist, and a ``std::unique_ptr`` must be the only one. So a function that creates an ``Obstacle`` returns a ``std::unique_ptr``, and the caller turns it into a ``std::shared_ptr`` if it needs to share.

.. admonition:: Question 15
   :class: hint

   What are ``copied.size()`` and ``copied.capacity()``, with libstdc++?

   .. code-block:: cpp

      std::vector<Pose> path{make_path(1000)};
      path.reserve(1024);              // room for 24 more
      std::vector<Pose> copied{path};

   A. 1000 and 1024: the copy takes ``path``'s spare slots too.
   B. 1000 and 1000.
   C. 1024 and 1024.
   D. 0 and 1024: ``reserve`` empties the vector.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **B. 1000 and 1000.**

      ``path`` has 1024 slots, 1000 in use: 24576 bytes. A copy allocates for the elements only, not the spare slots: ``copied`` has 1000 slots, 1000 times 24 bytes, which is 24000 bytes. ``702run week7_playground 12`` prints:

      .. code-block:: text

         path: size 1000, capacity 1024, 24576 bytes
         copied: size 1000, capacity 1000, 24000 bytes

      The standard only asks that a copy hold equal elements; libstdc++'s copy constructor allocates exactly ``size()``.
