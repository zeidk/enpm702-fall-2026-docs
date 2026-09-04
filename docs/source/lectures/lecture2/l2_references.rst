References
==========


.. dropdown:: Lecture 2
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L2: Introduction to C++**

        Covers terminal input and output with ``std::cin`` and
        ``std::cout``; bits, bytes, words, and the memory segments of a
        running process; variables, their five characteristics, naming,
        memory allocation, declaration, assignment, and the three forms
        of initialization; undefined behavior; the integral,
        floating-point, and boolean types; implicit conversions
        (promotions, conversions, narrowing, the usual arithmetic
        conversions); constants (literals, ``const``, ``constexpr``,
        and why not macros); type deduction with ``auto``; compound
        statements; local and global scope; naming collisions and
        namespaces; type aliases; and scoped enumerations. The Linux
        shell material is on the :doc:`l2_shell` page.

        The build pipeline is covered in
        :doc:`Lecture 1 </lectures/lecture1/l1_lecture>`.


.. dropdown:: The C++ Language
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: cppreference.com
            :link: https://en.cppreference.com/w/
            :class-card: sd-border-secondary

            **cppreference**

            Extensive reference for C++ and its standard library. The
            first place to look for everyday questions.

        .. grid-item-card:: C++ Core Guidelines
            :link: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
            :class-card: sd-border-secondary

            **C++ Core Guidelines**

            Stroustrup and Sutter's guidance on writing modern, safe
            C++. The rules cited in this lecture are listed below.

        .. grid-item-card:: cplusplus.com
            :link: https://cplusplus.com/
            :class-card: sd-border-secondary

            **cplusplus.com**

            Tutorials, references, and examples aimed at beginners and
            intermediate learners.

        .. grid-item-card:: Compiler Explorer
            :link: https://godbolt.org/
            :class-card: sd-border-secondary

            **Godbolt Compiler Explorer**

            Shows the assembly the compiler actually generates. Useful
            for seeing constant expressions folded away at compile
            time.


.. dropdown:: Guidelines Cited in This Lecture
    :class-container: sd-border-secondary

    .. list-table::
       :widths: 18 46 36
       :header-rows: 1
       :class: compact-table

       * - Rule
         - Says
         - Topic
       * - `ES.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es10-declare-one-name-only-per-declaration>`_
         - Declare one name (only) per declaration.
         - Declarations
       * - `ES.20 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#es20-always-initialize-an-object>`_
         - Always initialize an object.
         - Initialization
       * - `Con.5 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#con5-use-constexpr-for-values-that-can-be-computed-at-compile-time>`_
         - Use ``constexpr`` for values that can be computed at compile
           time.
         - Constants
       * - `R.6 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#r6-avoid-non-const-global-variables>`_
         - Avoid non-const global variables.
         - Global scope
       * - `NL.8 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl8-use-a-consistent-naming-style>`_
         - Use a consistent naming style.
         - Identifiers
       * - `NL.10 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl10-prefer-underscore_style-names>`_
         - Prefer ``underscore_style`` names.
         - Identifiers
       * - `NL.19 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl19-avoid-names-that-are-easily-misread>`_
         - Avoid names that are easily misread.
         - Identifiers
       * - `NL.26 <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#nl26-use-conventional-const-notation>`_
         - Use conventional ``const`` notation ("west const").
         - Constants


.. dropdown:: Language Reference for This Lecture
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Initialization
            :link: https://en.cppreference.com/w/cpp/language/initialization
            :class-card: sd-border-secondary

            **cppreference: initialization**

            Copy, direct, list (uniform), value, and zero
            initialization, and the rules that separate them.

        .. grid-item-card:: Implicit Conversions
            :link: https://en.cppreference.com/w/cpp/language/implicit_conversion
            :class-card: sd-border-secondary

            **cppreference: implicit conversions**

            The definitive list of promotions, conversions, and the
            usual arithmetic conversions.

        .. grid-item-card:: constexpr
            :link: https://en.cppreference.com/w/cpp/language/constexpr
            :class-card: sd-border-secondary

            **cppreference: constexpr**

            The ``constexpr`` specifier, and what it requires of an
            initializer.

        .. grid-item-card:: Fundamental Types
            :link: https://en.cppreference.com/w/cpp/language/types
            :class-card: sd-border-secondary

            **cppreference: fundamental types**

            Every built-in type, with the guaranteed minimum widths and
            the usual sizes per platform.

        .. grid-item-card:: Enumerations
            :link: https://en.cppreference.com/w/cpp/language/enum
            :class-card: sd-border-secondary

            **cppreference: enumerations**

            Scoped and unscoped enumerations, underlying types, and
            conversion rules.

        .. grid-item-card:: Keywords
            :link: https://en.cppreference.com/w/cpp/keyword
            :class-card: sd-border-secondary

            **cppreference: keyword list**

            Every reserved word, none of which can be used as an
            identifier.


.. dropdown:: C++20 Facilities Used in This Lecture
    :class-container: sd-border-secondary

    All four require GCC 13 or newer, which is the course minimum.
    ``<format>`` is the one that arrived latest in libstdc++, so it is
    the one an older compiler will reject even with ``-std=c++20``.

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: std::numbers
            :link: https://en.cppreference.com/w/cpp/numeric/constants
            :class-card: sd-border-secondary

            **Mathematical constants**

            ``std::numbers::pi``, ``e``, ``sqrt2``, ``ln2``, ``phi`` and
            others, to the full precision of the type. Use these instead
            of typing digits.

        .. grid-item-card:: Integer comparison functions
            :link: https://en.cppreference.com/w/cpp/utility/intcmp
            :class-card: sd-border-secondary

            **std::cmp_less and friends**

            Compare signed against unsigned by mathematical value,
            without the conversion that makes ``-1 < 1u`` false.

        .. grid-item-card:: std::format
            :link: https://en.cppreference.com/w/cpp/utility/format/format
            :class-card: sd-border-secondary

            **Formatting library**

            Formats one value at a time with no sticky state, replacing
            ``std::fixed`` and ``std::setprecision``.

        .. grid-item-card:: Format specification
            :link: https://en.cppreference.com/w/cpp/utility/format/spec
            :class-card: sd-border-secondary

            **What goes inside the braces**

            The grammar behind ``{:.2f}``: fill, alignment, sign, width,
            precision, and type.


.. dropdown:: Compiler and Tools
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: GCC Warning Options
            :link: https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html
            :class-card: sd-border-secondary

            **GCC warning options**

            What ``-Wall``, ``-Wextra``, ``-Wpedantic``,
            ``-Wsign-compare`` and ``-Wshadow`` actually enable.

        .. grid-item-card:: c++filt
            :link: https://sourceware.org/binutils/docs/binutils/c_002b_002bfilt.html
            :class-card: sd-border-secondary

            **binutils: c++filt**

            Demangles compiler-generated names. Use ``c++filt -t`` to
            make ``typeid(...).name()`` readable.

        .. grid-item-card:: Compiler warnings module
            :link: ../../reading_material/compiler_warnings/cw_lecture.html
            :class-card: sd-border-secondary

            **Course reading: compiler warnings**

            The course's warning flags, what each one catches, and how
            to read the diagnostics.

        .. grid-item-card:: Integer literals
            :link: https://en.cppreference.com/w/cpp/language/integer_literal
            :class-card: sd-border-secondary

            **cppreference: integer and floating literals**

            Decimal, hex, octal and binary forms, and every numeric
            suffix.
