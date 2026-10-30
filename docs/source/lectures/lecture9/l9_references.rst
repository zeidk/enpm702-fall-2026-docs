.. _l9_references:

====================
Lecture 9 References
====================

.. dropdown:: Lecture 9 Summary
   :class-container: sd-border-success

   This lecture covered advanced object-oriented programming, on the robotaxi program whose class diagram L8 and L9 share:

   - **Design and Relationships**: Requirements say what the program does. Their nouns give classes, their verbs methods, their links relationships, drawn in a UML class diagram. Association knows (``std::weak_ptr``), aggregation shares (``std::shared_ptr``), composition owns alone (``std::unique_ptr`` or a member), dependency uses for one call (a parameter).

   - **Namespaces**: A namespace keeps two classes with the same name apart: every class of the program is in ``fleet``. Each file opens it again and adds its names. Outside it, write ``fleet::Vehicle`` or use a using-declaration, never ``using namespace`` in a header. A helper of one source file goes in an unnamed namespace.

   - **Inheritance**: ``class D : public B`` adds to ``B``. ``private`` members of ``B`` stay ``private``; data members are never ``protected`` in this course. The constructor names ``B{...}`` first in its list. The base is built first and destroyed last.

   - **Polymorphism**: Without ``virtual``, the static type picks the method. With ``virtual`` and a base reference or pointer, the dynamic type picks it while the program runs. Mark every override ``override``. Copying into a base object slices. ``auto`` keeps the derived type; moving converts to a base pointer. A base class whose objects are deleted through base pointers needs a ``virtual`` destructor.

   - **Abstraction and final**: A pure ``virtual`` method (``= 0``) makes a class abstract: no objects, only derived classes. A concrete class overrides every pure ``virtual`` method. ``final`` closes a class or a method. Use it sparingly.


.. dropdown:: Lecture 9 Bibliography
   :class-container: sd-border-success

   The References frame of the L9 slides lists these four sources.

   - Bjarne Stroustrup. *The C++ Programming Language*. 4th edition. Addison-Wesley, 2013. ISBN 978-0321563842.
   - ISO/IEC. *ISO/IEC 14882:2020: Programming languages, C++*. International Organization for Standardization, Geneva, Switzerland, 2020. Working draft N4861 is freely available from the ISO C++ committee. The slides quote this standard by section name, for example [class.access.base], [class.virtual] and [expr.delete].
   - Bjarne Stroustrup and Herb Sutter. *C++ Core Guidelines*. 2024. `https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_
   - cppreference.com contributors. *cppreference.com*. 2026. Community reference for the C++ language and standard library. `https://en.cppreference.com/w/ <https://en.cppreference.com/w/>`_


.. dropdown:: cppreference Links
   :class-container: sd-border-success

   .. grid:: 1 1 2 2
      :gutter: 2

      .. grid-item-card:: Namespaces
         :link: https://en.cppreference.com/w/cpp/language/namespace
         :class-card: sd-border-secondary

         **cppreference: Namespaces**

         Named, nested and unnamed namespaces. Cited on the Namespaces divider.

      .. grid-item-card:: Derived Classes
         :link: https://en.cppreference.com/w/cpp/language/derived_class
         :class-card: sd-border-secondary

         **cppreference: Derived classes**

         Base classes, derived classes and the access of inherited members. Recommended reading on the Next Class slide.

      .. grid-item-card:: virtual Function Specifier
         :link: https://en.cppreference.com/w/cpp/language/virtual
         :class-card: sd-border-secondary

         **cppreference: virtual function specifier**

         ``virtual`` methods, overriding and ``virtual`` destructors. Cited on the Polymorphism divider, and required reading on the Before the Next Lecture slide.

      .. grid-item-card:: Abstract Class
         :link: https://en.cppreference.com/w/cpp/language/abstract_class
         :class-card: sd-border-secondary

         **cppreference: Abstract class**

         Pure ``virtual`` methods and the classes that have them. Cited on the Abstraction divider.

      .. grid-item-card:: final Specifier
         :link: https://en.cppreference.com/w/cpp/language/final
         :class-card: sd-border-secondary

         **cppreference: final specifier**

         ``final`` on a class and on a ``virtual`` method. Cited on The final Keyword divider.


.. dropdown:: C++ Core Guidelines Rules
   :class-container: sd-border-success

   The rules the slides and their notes cite, with their titles as the Guidelines write them. The section `C.hier: Class hierarchies (OOP) <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ss-hier>`_ is required reading on the Before the Next Lecture slide and recommended reading on the Next Class slide.

   - `C.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-five>`_: If you define or ``=delete`` any copy, move, or destructor function, define or ``=delete`` them all
   - `C.35 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-dtor-virtual>`_: A base class destructor should be either public and virtual, or protected and non-virtual
   - `C.67 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rc-copy-virtual>`_: A polymorphic class should suppress public copy/move
   - `C.120 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-domain>`_: Use class hierarchies to represent concepts with inherent hierarchical structure (only)
   - `C.127 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-dtor>`_: A class with a virtual function should have a virtual or protected destructor
   - `C.128 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-override>`_: Virtual functions should specify exactly one of ``virtual``, ``override``, or ``final``
   - `C.132 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-virtual>`_: Don't make a function ``virtual`` without reason
   - `C.133 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-protected>`_: Avoid ``protected`` data
   - `C.139 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-final>`_: Use ``final`` on classes sparingly
   - `C.145 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rh-poly>`_: Access polymorphic objects through pointers and references
   - `ES.63 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#res-slice>`_: Don't slice
   - `R.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rr-unique>`_: Prefer ``unique_ptr`` over ``shared_ptr`` unless you need to share ownership
   - `SF.7 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-using-directive>`_: Don't write ``using namespace`` at global scope in a header file
   - `SF.21 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed>`_: Don't use an unnamed (anonymous) namespace in a header
   - `SF.22 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-unnamed2>`_: Use an unnamed (anonymous) namespace for all internal/non-exported entities


.. dropdown:: UML
   :class-container: sd-border-success

   - `OMG: Unified Modeling Language <https://www.omg.org/spec/UML/>`_: the specification of UML, cited on the Design divider.


.. dropdown:: Recommended Reading
   :class-container: sd-border-success

   The Next Class slide recommends these three:

   - `cppreference: Derived classes <https://en.cppreference.com/w/cpp/language/derived_class>`_
   - `C++ Core Guidelines, C.hier: Class hierarchies (OOP) <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#ss-hier>`_
   - Stroustrup, *The C++ Programming Language* (4th edition, 2013)
