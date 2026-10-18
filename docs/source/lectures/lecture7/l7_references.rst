.. _l7_references:

=====================
Lecture 7 References
=====================

.. dropdown:: Lecture 7 Summary
   :class-container: sd-border-success

   This lecture covered who owns an object on the heap, move semantics, and the three smart pointers of ``<memory>``:

   - **Ownership**: The last owner of a heap object gives it back. A ``T*`` cannot say it owns, and that causes a leak, a double ``delete`` or a dangling read. LeakSanitizer, part of ``-fsanitize=address``, reports a leak with the line that allocated it.

   - **Move Semantics**: A move hands over what an object owns: 24 bytes for a ``std::vector``, not its elements. The source is valid but unspecified: assign it before reuse. Every expression is an lvalue, an xvalue or a prvalue, and ``decltype((e))`` tells which. ``T&&`` binds to rvalues only, and a named ``T&&`` is an lvalue. ``std::move`` is a cast, and the move happens where the result is taken. Do not use it on a ``const`` object, and do not use it on a returned local.

   - **std::unique_ptr**: One owner, 8 bytes, from ``std::make_unique``. It is moved, never copied, and a moved-from one is null. Pass the object to use it, the ``std::unique_ptr`` by value to hand it over, and by reference to reseat it. Return it by value.

   - **std::shared_ptr**: Several owners and a count in a control block, from ``std::make_shared`` in one allocation. The last owner deletes the object. A ``std::unique_ptr`` converts to a ``std::shared_ptr``, not back.

   - **std::weak_ptr**: Watches without owning: ``lock()`` gives a ``std::shared_ptr`` or an empty one. It breaks a cycle of ``std::shared_ptr``\ s, which would otherwise leak.


.. dropdown:: Lecture 7 Bibliography
   :class-container: sd-border-success

   The References frame of the L7 slides lists these four sources.

   - Bjarne Stroustrup. *The C++ Programming Language*. 4th edition. Addison-Wesley, 2013. ISBN 978-0321563842.
   - ISO/IEC. *ISO/IEC 14882:2020: Programming languages, C++*. International Organization for Standardization, Geneva, Switzerland, 2020. Working draft N4861 is freely available from the ISO C++ committee. The slides quote this standard by section name, for example [basic.lval] and [unique.ptr.single.ctor].
   - Bjarne Stroustrup and Herb Sutter. *C++ Core Guidelines*. 2024. `https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_
   - cppreference.com contributors. *cppreference.com*. 2026. Community reference for the C++ language and standard library. `https://en.cppreference.com/w/ <https://en.cppreference.com/w/>`_


.. dropdown:: cppreference Links
   :class-container: sd-border-success

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Dynamic Memory Management
         :link: https://en.cppreference.com/w/cpp/memory
         :class-card: sd-border-secondary

         **cppreference: Dynamic memory management**

         The ``<memory>`` overview, with the smart pointers and the functions that make them. Recommended reading on the Next Class slide.

      .. grid-item-card:: std::move
         :link: https://en.cppreference.com/w/cpp/utility/move
         :class-card: sd-border-secondary

         **cppreference: std::move**

         The cast that marks an object as one you may take from. Cited on the Move Semantics divider.

      .. grid-item-card:: std::unique_ptr
         :link: https://en.cppreference.com/w/cpp/memory/unique_ptr
         :class-card: sd-border-secondary

         **cppreference: std::unique_ptr**

         The only owner of one object on the heap. Cited on the std::unique_ptr divider.

      .. grid-item-card:: std::shared_ptr
         :link: https://en.cppreference.com/w/cpp/memory/shared_ptr
         :class-card: sd-border-secondary

         **cppreference: std::shared_ptr**

         One of several owners that share a count. Cited on the std::shared_ptr divider.

      .. grid-item-card:: std::weak_ptr
         :link: https://en.cppreference.com/w/cpp/memory/weak_ptr
         :class-card: sd-border-secondary

         **cppreference: std::weak_ptr**

         An observer that owns nothing. Cited on the std::weak_ptr divider.

      .. grid-item-card:: std::exchange
         :link: https://en.cppreference.com/w/cpp/utility/exchange
         :class-card: sd-border-secondary

         **cppreference: std::exchange**

         Sets an object to a new value and returns the old one. Cited in Further Reading.


.. dropdown:: C++ Core Guidelines Rules
   :class-container: sd-border-success

   The rules the slides cite, with their titles as the Guidelines write them. Section R of the Guidelines, `R: Resource management <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#s-resource>`_, is recommended reading on the Next Class slide.

   - `R.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-raii>`_: Manage resources automatically using resource handles and RAII (Resource Acquisition Is Initialization)
   - `R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ptr>`_: A raw pointer (a ``T*``) is non-owning
   - `R.4 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-ref>`_: A raw reference (a ``T&``) is non-owning
   - `R.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-scoped>`_: Prefer scoped objects, don't heap-allocate unnecessarily
   - `R.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-mallocfree>`_: Avoid ``malloc()`` and ``free()``
   - `R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`_: Avoid calling ``new`` and ``delete`` explicitly
   - `R.12 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-immediate-alloc>`_: Immediately give the result of an explicit resource allocation to a manager object
   - `R.13 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-single-alloc>`_: Perform at most one explicit resource allocation in a single expression statement
   - `R.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-owner>`_: Use ``unique_ptr`` or ``shared_ptr`` to represent ownership
   - `R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`_: Prefer ``unique_ptr`` over ``shared_ptr`` unless you need to share ownership
   - `R.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_shared>`_: Use ``make_shared()`` to make ``shared_ptr``\ s
   - `R.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-make_unique>`_: Use ``make_unique()`` to make ``unique_ptr``\ s
   - `R.24 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-weak_ptr>`_: Use ``std::weak_ptr`` to break cycles of ``shared_ptr``\ s
   - `R.30 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrparam>`_: Take smart pointers as parameters only to explicitly express lifetime semantics
   - `R.32 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-uniqueptrparam>`_: Take a ``unique_ptr<widget>`` parameter to express that a function assumes ownership of a ``widget``
   - `R.33 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-reseat>`_: Take a ``unique_ptr<widget>&`` parameter to express that a function reseats the ``widget``
   - `R.34 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-owner>`_: Take a ``shared_ptr<widget>`` parameter to express shared ownership
   - `R.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam>`_: Take a ``shared_ptr<widget>&`` parameter to express that a function might reseat the shared pointer
   - `R.36 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-sharedptrparam-const>`_: Take a ``const shared_ptr<widget>&`` parameter to express that it might retain a reference count to the object (the Guidelines mark this rule as not finished)
   - `R.37 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-smartptrget>`_: Do not pass a pointer or reference obtained from an aliased smart pointer
   - `F.18 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-consume>`_: For "will-move-from" parameters, pass by ``X&&`` and ``std::move`` the parameter
   - `F.48 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-return-move-local>`_: Don't ``return std::move(local)``
   - `ES.56 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-move>`_: Write ``std::move()`` only when you need to explicitly move an object to another scope
   - `SL.con.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rsl-vector>`_: Prefer using STL ``vector`` by default unless you have a reason to use a different container


.. dropdown:: Tools
   :class-container: sd-border-success

   - `LeakSanitizer (Clang documentation) <https://clang.llvm.org/docs/LeakSanitizer.html>`_: the leak checker that reports the leaks on the slides. AddressSanitizer "integrates LeakSanitizer and enables it by default on supported platforms", so ``-fsanitize=address`` turns it on.


.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   The Next Class slide recommends these three:

   - `cppreference: dynamic memory management <https://en.cppreference.com/w/cpp/memory>`_
   - `C++ Core Guidelines, R: Resource management <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#s-resource>`_
   - Stroustrup, *The C++ Programming Language* (4th edition, 2013)
