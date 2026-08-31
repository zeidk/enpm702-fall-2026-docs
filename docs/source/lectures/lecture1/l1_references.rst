References
==========


.. dropdown:: Lecture 1
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L1: Course Introduction**

        Covers the course structure, grading and AI policies, and the
        weekly cycle; C++ as a statically typed, compiled,
        multi-paradigm language and the standards timeline through
        C++20; the build pipeline from source through preprocessor,
        compiler, and linker to a loaded and executing process;
        building the same program with CMake and inside VSCode; and
        an in-class verification of the development environment. The
        Linux shell material is on the :doc:`l1_shell` page.


.. dropdown:: Course Files (Downloads)
    :class-container: sd-border-secondary
    :open:

    - **Course code repository**: `github.com/zeidk/enpm702-fall-2026-cpp <https://github.com/zeidk/enpm702-fall-2026-cpp>`_ --- one folder per lecture. Clone it once, then ``git pull`` before every lecture.
    - :download:`Cpp17_standard.pdf </_static/files/Cpp17_standard.pdf>` --- the C++17 standard working draft (N4659), provided for reference.

    .. note::

       Course code targets **C++20**, not C++17. The published ISO
       document is paid, but
       `N4868 <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4868.pdf>`_,
       the final working draft of C++20, is free from the ISO C++
       committee; it is what people cite in practice and what this
       course refers to.
       The standard is a dense reference, not a tutorial, and you are
       **not** expected to read it cover to cover. For everyday lookups
       prefer `cppreference.com <https://en.cppreference.com/w/>`_;
       reach for the standard when you need the exact, definitive rule.



.. dropdown:: The C++ Language
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: cppreference.com
            :link: https://en.cppreference.com/w/
            :class-card: sd-border-secondary

            **cppreference**

            Extensive reference for C++ and its standard library,
            covering syntax, functions, and the standards themselves.
            The first place to look for everyday questions.

        .. grid-item-card:: C++ Core Guidelines
            :link: https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines
            :class-card: sd-border-secondary

            **C++ Core Guidelines**

            Stroustrup and Sutter's guidance on writing modern,
            safe C++.

        .. grid-item-card:: cplusplus.com
            :link: https://cplusplus.com/
            :class-card: sd-border-secondary

            **cplusplus.com**

            Tutorials, references, and examples aimed at beginners and
            intermediate learners.

        .. grid-item-card:: C++20 Working Draft (N4868)
            :link: https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4868.pdf
            :class-card: sd-border-secondary

            **ISO C++20 working draft**

            The freely available draft of the standard targeted by all
            code in this course.


.. dropdown:: Build Process and Toolchain
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: GCC Option Summary
            :link: https://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html
            :class-card: sd-border-secondary

            **GCC options**

            Every flag ``g++`` accepts, including ``-std``, ``-Wall``,
            ``-Wextra``, ``-E``, and ``-c``.

        .. grid-item-card:: CMake: cmake(1)
            :link: https://cmake.org/cmake/help/latest/manual/cmake.1.html
            :class-card: sd-border-secondary

            **cmake command line**

            Reference for ``cmake -S . -B build`` and
            ``cmake --build build``.

        .. grid-item-card:: CMAKE_CXX_STANDARD
            :link: https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD.html
            :class-card: sd-border-secondary

            **CMake docs: CMAKE_CXX_STANDARD**

            How the C++ standard is selected in a CMake project, with
            ``CMAKE_CXX_STANDARD_REQUIRED`` and
            ``CMAKE_CXX_EXTENSIONS``.

        .. grid-item-card:: GDB Documentation
            :link: https://sourceware.org/gdb/current/onlinedocs/gdb/
            :class-card: sd-border-secondary

            **GDB manual**

            The debugger used from Lecture 3 onward, and behind
            **CMake: Debug** in VSCode.


.. dropdown:: Linux Shells
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Bash
            :link: https://www.gnu.org/software/bash/
            :class-card: sd-border-secondary

            **GNU Bash**

            The default shell for most Linux distributions, known for its
            scripting capabilities.

        .. grid-item-card:: Zsh
            :link: https://www.zsh.org/
            :class-card: sd-border-secondary

            **Z Shell**

            Similar to Bash, with additional features like better
            autocompletion and customization options.

        .. grid-item-card:: Fish
            :link: https://fishshell.com/
            :class-card: sd-border-secondary

            **Friendly Interactive Shell**

            User-friendly and highly customizable, with a focus on
            simplicity.

        .. grid-item-card:: Ksh
            :link: http://www.kornshell.com/
            :class-card: sd-border-secondary

            **Korn Shell**

            A shell with advanced scripting features, sometimes used in
            enterprise environments.


.. dropdown:: Tools
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Visual Studio Code
            :link: https://code.visualstudio.com
            :class-card: sd-border-secondary

            **VSCode**

            Free, lightweight code editor with a rich extension ecosystem.
            Used in this course for C++ development.

            +++

            - `Download <https://code.visualstudio.com/download>`_
            - `Keyboard Shortcuts (Linux) <https://code.visualstudio.com/shortcuts/keyboard-shortcuts-linux.pdf>`_

        .. grid-item-card:: CMake
            :link: https://cmake.org/cmake/help/latest/index.html
            :class-card: sd-border-secondary

            **CMake Documentation**

            Open-source, cross-platform build system used to build, test,
            and package C++ software.

            +++

            - `CMake Quick Start in VSCode <https://code.visualstudio.com/docs/cpp/cmake-quickstart>`_

        .. grid-item-card:: Valgrind
            :link: https://valgrind.org/
            :class-card: sd-border-secondary

            **Valgrind**

            Memory debugging, memory leak detection, and profiling tool
            for C++ programs.

        .. grid-item-card:: Doxygen
            :link: https://www.doxygen.nl/
            :class-card: sd-border-secondary

            **Doxygen**

            Documentation generator for C++ source code. Generates
            documentation from annotated source files.


.. dropdown:: Recommended Reading
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Ubuntu
            :link: https://ubuntu.com/download/desktop
            :class-card: sd-border-secondary

            **Ubuntu Desktop**

            Download Ubuntu Desktop 24.04 LTS (Noble Numbat) or 22.04 LTS
            (Jammy Jellyfish).

        .. grid-item-card:: ROS 2
            :link: https://docs.ros.org/en/jazzy/
            :class-card: sd-border-secondary

            **ROS 2 Jazzy Documentation**

            Official documentation for ROS 2 Jazzy Jalisco (used with
            Ubuntu 24.04).
