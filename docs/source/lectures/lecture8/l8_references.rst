.. _l8_references:

====================
Lecture 8 References
====================

.. dropdown:: Lecture 8 Summary
   :class-container: sd-border-success

   This lecture covered the basics of object-oriented programming, on the ``Vehicle`` of a robotaxi and the ``Sensor``\ s it owns:

   - **Classes and Encapsulation**: Use a ``class`` when the data members must agree (an invariant), a ``struct`` when they vary independently. Data members are ``private``; ``public`` methods keep the invariant. The class goes in a header, its method bodies in a source file, each named ``ClassName::``.

   - **Accessors, Mutators and Constructors**: An accessor is ``const``, and ``[[nodiscard]]`` and ``noexcept`` when true. A mutator checks the new value and throws when it breaks the invariant. A constructor makes the invariant true or throws. Initialize in the member initializer list, in declaration order. Mark a constructor that can take one argument ``explicit``.

   - **The this Pointer**: ``this`` points at the object a method runs on: ``X*``, or ``const X*`` in a ``const`` method. A method that returns ``*this`` as an ``X&`` hands back the object itself.

   - **Destructors**: A destructor gives back what the object owns. At the end of a scope, objects are destroyed in reverse order. A class whose members give back their own memory, such as ``std::unique_ptr``, needs no destructor of its own; the required reading, :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>`, says when a class writes one.

   - **Further Reading** (the appendix, not presented): ``const`` objects allow only ``const`` and ``static`` methods, and a ``static`` member belongs to the class: one copy, no ``this``.


.. dropdown:: Lecture 8 Bibliography
   :class-container: sd-border-success

   The References frame of the L8 slides lists these four sources.

   - Bjarne Stroustrup. *The C++ Programming Language*. 4th edition. Addison-Wesley, 2013. ISBN 978-0321563842.
   - ISO/IEC. *ISO/IEC 14882:2020: Programming languages, C++*. International Organization for Standardization, Geneva, Switzerland, 2020. Working draft N4861 is freely available from the ISO C++ committee. The slides quote this standard by section name, for example [class.access] and [expr.prim.this].
   - Bjarne Stroustrup and Herb Sutter. *C++ Core Guidelines*. 2024. `https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_
   - cppreference.com contributors. *cppreference.com*. 2026. Community reference for the C++ language and standard library. `https://en.cppreference.com/w/ <https://en.cppreference.com/w/>`_


.. dropdown:: cppreference Links
   :class-container: sd-border-success

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Classes
         :link: https://en.cppreference.com/w/cpp/language/classes
         :class-card: sd-border-secondary

         **cppreference: Classes**

         Class types, their members and their special members. Cited on the Classes and Objects divider, and recommended reading on the Next Class slide.

      .. grid-item-card:: Constructors
         :link: https://en.cppreference.com/w/cpp/language/constructor
         :class-card: sd-border-secondary

         **cppreference: Constructors**

         Constructors and member initializer lists. Required reading on the Before the Next Lecture and Next Class slides.

      .. grid-item-card:: The this Pointer
         :link: https://en.cppreference.com/w/cpp/language/this
         :class-card: sd-border-secondary

         **cppreference: The this pointer**

         The pointer to the object a method was called on. Cited on The this Pointer divider.

      .. grid-item-card:: static Members
         :link: https://en.cppreference.com/w/cpp/language/static
         :class-card: sd-border-secondary

         **cppreference: static members**

         Data members and methods that belong to the class. Cited on the static Members divider, in the appendix.


.. dropdown:: C++ Core Guidelines Rules
   :class-container: sd-border-success

   The rules the slides cite, with their titles as the Guidelines write them. C.42 is cited in the appendix, the Further Reading part of the lecture page. C.20, C.21, C.62 and C.66 are on the :doc:`Rule of Five and Rule of Zero <l8_rule_of_five>` reading, not in the slides. Section C of the Guidelines, `C: Classes and class hierarchies <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#s-class>`_, is required reading on the Before the Next Lecture and Next Class slides.

   - `C.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-struct>`_: Use ``class`` if the class has an invariant; use ``struct`` if the data members can vary independently
   - `C.4 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-member>`_: Make a function a member only if it needs direct access to the representation of a class
   - `C.8 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-class>`_: Use ``class`` rather than ``struct`` if any member is non-public
   - `C.9 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-private>`_: Minimize exposure of members
   - `C.31 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-release>`_: All resources acquired by a class must be released by the class's destructor
   - `C.41 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-complete>`_: A constructor should create a fully initialized object
   - `C.42 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-throw>`_: If a constructor cannot construct a valid object, throw an exception
   - `C.45 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-default>`_: Don't define a default constructor that only initializes data members; use default member initializers instead
   - `C.46 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-explicit>`_: By default, declare single-argument constructors explicit
   - `C.47 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-order>`_: Define and initialize data members in the order of member declaration
   - `C.49 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-initialize>`_: Prefer initialization to assignment in constructors
   - `C.51 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-delegating>`_: Use delegating constructors to represent common actions for all constructors of a class
   - `C.131 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-get>`_: Avoid trivial getters and setters
   - `Con.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rconst-fct>`_: By default, make member functions ``const``
   - `E.2 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-throw>`_: Throw an exception to signal that a function can't perform its assigned task
   - `E.17 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-not-always>`_: Don't try to catch every exception in every function
   - `E.18 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#re-catch>`_: Minimize the use of explicit ``try``/``catch``
   - `ES.23 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-list>`_: Prefer the ``{}``-initializer syntax
   - `F.6 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rf-noexcept>`_: If your function must not throw, declare it ``noexcept``
   - `R.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-scoped>`_: Prefer scoped objects, don't heap-allocate unnecessarily
   - `R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-newdelete>`_: Avoid calling ``new`` and ``delete`` explicitly


.. dropdown:: Style Guide
   :class-container: sd-border-success

   - `Google C++ Style Guide: Variable Names <https://google.github.io/styleguide/cppguide.html#Variable_Names>`_: data members of a class end in ``_``, the convention the slides use (``speed_``, ``max_speed_``).


.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   The Next Class slide recommends these two, beside the required reading:

   - `cppreference: Classes <https://en.cppreference.com/w/cpp/language/classes>`_
   - Stroustrup, *The C++ Programming Language* (4th edition, 2013)
