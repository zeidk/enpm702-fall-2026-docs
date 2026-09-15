.. _l3-references:

====================================================
References
====================================================


.. dropdown:: Lecture 3
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L3: Pointers and Memory Management**

        Covers the three storage durations and which one you manage
        yourself; the stack and the heap; what a pointer is, and how to
        declare, initialize and dereference one; the address-of and
        dereference operators; null pointers, ``nullptr``, and wild
        pointers; why every pointer is the same size and what a
        pointer's type is actually for; const-correctness
        (``const int*``, ``int* const``, ``const int* const``); dynamic
        allocation with ``new`` and ``delete``;
        memory leaks, dangling pointers, double deletes and null
        dereferences; Valgrind and the sanitizers; RAII and why the
        course prefers containers and smart pointers; references and
        their five properties; and a preview of the C++20 facilities
        that apply here, which are covered in
        :doc:`Lecture 5 </lectures/lecture5/l5_index>`. The
        Linux shell material is on the :doc:`l3_shell` page.

        Memory segments and storage duration are covered in
        :doc:`Lecture 2 </lectures/lecture2/l2_lecture>`; smart
        pointers are :doc:`Lecture 7 </lectures/lecture7/l7_index>`.


.. dropdown:: Guidelines Cited in This Lecture
    :class-container: sd-border-secondary

    .. list-table::
       :widths: 18 46 36
       :header-rows: 1
       :class: compact-table

       * - Rule
         - Says
         - Topic
       * - `R.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r3-a-raw-pointer-a-t-is-non-owning>`_
         - A raw pointer (a ``T*``) is non-owning.
         - Ownership
       * - `R.11 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r11-avoid-calling-new-and-delete-explicitly>`_
         - Avoid calling ``new`` and ``delete`` explicitly.
         - Dynamic memory
       * - `R.1 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r1-manage-resources-automatically-using-resource-handles-and-raii-resource-acquisition-is-initialization>`_
         - Manage resources automatically using RAII.
         - Ownership
       * - `ES.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es20-always-initialize-an-object>`_
         - Always initialize an object.
         - Wild pointers
       * - `ES.65 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es65-dont-dereference-an-invalid-pointer>`_
         - Don't dereference an invalid pointer.
         - Dangling and null
       * - `F.60 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#f60-prefer-t-over-t-when-no-argument-is-a-valid-option>`_
         - Prefer ``T*`` over ``T&`` when "no argument" is a valid
           option.
         - Pointers vs. references
       * - `Con.3 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con3-by-default-pass-pointers-and-references-to-consts>`_
         - By default, pass pointers and references to ``const``.
         - Const-correctness
       * - `ES.42 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es42-keep-use-of-pointers-simple-and-straightforward>`_
         - Keep use of pointers simple and straightforward.
         - Pointer arithmetic


.. dropdown:: Language Reference for This Lecture
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Hexadecimal
            :link: https://en.wikipedia.org/wiki/Hexadecimal
            :class-card: sd-border-secondary

            **Wikipedia: hexadecimal**

            Base 16: place value, the digits ``0`` to ``f``, and
            converting to and from decimal in both directions.

        .. grid-item-card:: Integer literals
            :link: https://en.cppreference.com/w/cpp/language/integer_literal
            :class-card: sd-border-secondary

            **cppreference: integer literals**

            Writing constants in hex (``0x``), binary (``0b``) and octal,
            and the suffixes that pin a literal's type.

        .. grid-item-card:: Pointer declaration
            :link: https://en.cppreference.com/w/cpp/language/pointer
            :class-card: sd-border-secondary

            **cppreference: pointers**

            Declaration syntax, pointers to objects and to functions,
            null pointers, and pointer arithmetic.

        .. grid-item-card:: Reference declaration
            :link: https://en.cppreference.com/w/cpp/language/reference
            :class-card: sd-border-secondary

            **cppreference: references**

            Lvalue references, what they bind to, and the rules that
            make them non-reseatable.

        .. grid-item-card:: new expression
            :link: https://en.cppreference.com/w/cpp/language/new
            :class-card: sd-border-secondary

            **cppreference: new**

            Allocation, initialization, and what happens when
            allocation fails (``std::bad_alloc``, not ``nullptr``).

        .. grid-item-card:: delete expression
            :link: https://en.cppreference.com/w/cpp/language/delete
            :class-card: sd-border-secondary

            **cppreference: delete**

            What ``delete`` does to the storage, and why deleting a
            null pointer is safe.

        .. grid-item-card:: nullptr
            :link: https://en.cppreference.com/w/cpp/language/nullptr
            :class-card: sd-border-secondary

            **cppreference: nullptr**

            The null pointer literal and its type,
            ``std::nullptr_t``.

        .. grid-item-card:: const and volatile
            :link: https://en.cppreference.com/w/cpp/language/cv
            :class-card: sd-border-secondary

            **cppreference: cv qualifiers**

            Where ``const`` may appear in a declaration, and what each
            position means.


.. dropdown:: C++20 Facilities Mentioned in This Lecture
    :class-container: sd-border-secondary

    The lecture names these but does not use them: both need functions,
    so they are covered in
    :doc:`Lecture 5 </lectures/lecture5/l5_index>`. All of them require
    GCC 13 or newer, which is the course minimum.

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Constant expressions
            :link: https://en.cppreference.com/w/cpp/language/constant_expression
            :class-card: sd-border-secondary

            **Allocation during constant evaluation**

            C++20 permits ``new`` and ``delete`` inside a ``constexpr``
            function, provided everything allocated is freed before the
            evaluation ends, so a leak becomes a compile error.

        .. grid-item-card:: std::to_address
            :link: https://en.cppreference.com/w/cpp/memory/to_address
            :class-card: sd-border-secondary

            **Getting the raw address out of a handle**

            Works for raw pointers and for smart pointers alike, without
            dereferencing. Useful when interfacing with C APIs.

        .. grid-item-card:: std::addressof
            :link: https://en.cppreference.com/w/cpp/memory/addressof
            :class-card: sd-border-secondary

            **The address, even when & is overloaded**

            A class may overload ``operator&``. ``std::addressof(x)``
            returns the real address regardless (C++11, listed here
            because it belongs with the above).


.. dropdown:: Memory Tools
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Valgrind Quick Start
            :link: https://valgrind.org/docs/manual/quick-start.html
            :class-card: sd-border-secondary

            **Valgrind: quick start**

            The five-minute version: compile with ``-g``, run under
            ``valgrind --leak-check=full``, read the report.

        .. grid-item-card:: Memcheck manual
            :link: https://valgrind.org/docs/manual/mc-manual.html
            :class-card: sd-border-secondary

            **Memcheck**

            The default tool. Every error message it can produce, and
            what the four leak categories mean.

        .. grid-item-card:: AddressSanitizer
            :link: https://github.com/google/sanitizers/wiki/AddressSanitizer
            :class-card: sd-border-secondary

            **-fsanitize=address**

            Compile-time instrumentation: far faster than Valgrind, and
            catches use-after-free, overruns, and leaks.

        .. grid-item-card:: GCC instrumentation options
            :link: https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html
            :class-card: sd-border-secondary

            **GCC: -fsanitize=...**

            Every sanitizer GCC supports, including
            ``undefined``, and how they combine.


.. dropdown:: Going Further
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Smart pointers
            :link: https://en.cppreference.com/w/cpp/memory
            :class-card: sd-border-secondary

            **cppreference: dynamic memory management**

            ``unique_ptr``, ``shared_ptr``, ``weak_ptr`` and the
            ``make_`` functions, the subject of Lecture 7.

        .. grid-item-card:: Compiler Explorer
            :link: https://godbolt.org/
            :class-card: sd-border-secondary

            **Godbolt Compiler Explorer**

            Worth using this week to see that a reference and a
            ``const`` pointer often compile to the same instructions.

        .. grid-item-card:: What every programmer should know about memory
            :link: https://people.freebsd.org/~lstewart/articles/cpumemory.pdf
            :class-card: sd-border-secondary

            **Ulrich Drepper (2007)**

            Long, and still the standard reference on how memory
            actually behaves underneath the model in this lecture.

        .. grid-item-card:: Stroustrup on nullptr
            :link: https://www.stroustrup.com/bs_faq2.html#null
            :class-card: sd-border-secondary

            **Stroustrup's C++ style FAQ**

            Why ``nullptr`` exists and why ``NULL`` was a problem worth
            fixing.
