References
==========


.. dropdown:: Compiler Warning Flags
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Compiler Warning Flags**

        Covers the warning groups used in this course: ``-Wall``,
        ``-Wextra``, and ``-Wpedantic``, the warnings each one enables,
        the additional flags ``-Wshadow``, ``-Wconversion``, and
        ``-Werror``, and why warnings matter in beginner code.


.. dropdown:: Compiler Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: GCC Warning Options
            :link: https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html
            :class-card: sd-border-secondary

            **GCC: Options to Request or Suppress Warnings**

            The authoritative list of every ``-W`` option ``g++``
            accepts, including exactly which warnings ``-Wall`` and
            ``-Wextra`` enable for C++.

        .. grid-item-card:: GCC Debugging Options
            :link: https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html
            :class-card: sd-border-secondary

            **GCC: Options for Debugging Your Program**

            Documentation for ``-g`` and the related options that
            control the debug information used by ``gdb`` and Valgrind.

        .. grid-item-card:: Clang Diagnostic Flags
            :link: https://clang.llvm.org/docs/DiagnosticsReference.html
            :class-card: sd-border-secondary

            **Clang Diagnostics Reference**

            The equivalent list for ``clang++``, useful when checking
            whether code that compiles cleanly with GCC is portable.

        .. grid-item-card:: C++ Core Guidelines
            :link: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
            :class-card: sd-border-secondary

            **C++ Core Guidelines**

            Guidance on the practices these warnings enforce, including
            arithmetic conversions, initialization, and portability.
