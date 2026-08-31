====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 1: the Linux shell and
shell configuration, Visual Studio Code, the C++ standards, the build
pipeline from source to executable, and CMake.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is a **shell** in the context of a Linux operating system?

   A. A graphical desktop environment for managing files.

   B. A program that provides a command-line interface to interact with the operating system.

   C. A type of programming language used to write C++ code.

   D. A hardware component that processes user input.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, A program that provides a command-line interface to interact with the operating system.

   *Explanation:* A shell is a program that interprets commands and allows users to execute them, run scripts, manage files, and control processes through a CLI.


.. admonition:: Question 2
   :class: hint

   Which shell is the **default** for most Linux distributions?

   A. Zsh

   B. Fish

   C. Bash

   D. Ksh

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, Bash (Bourne Again Shell)

   *Explanation:* Bash is the default shell for most Linux distributions and is widely used for scripting and interactive command-line use.


.. admonition:: Question 3
   :class: hint

   What is the correct syntax for creating a shell alias?

   A. ``alias identifier = 'value'``

   B. ``alias identifier='value'``

   C. ``set alias identifier 'value'``

   D. ``define identifier='value'``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``alias identifier='value'``

   *Explanation:* The alias command requires no spaces around the equal sign. The value should be enclosed in quotes.


.. admonition:: Question 4
   :class: hint

   Which configuration file does **Zsh** use?

   A. ``.bashrc``

   B. ``.zshrc``

   C. ``config.fish``

   D. ``.kshrc``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``.zshrc``

   *Explanation:* Zsh uses ``.zshrc``, located in the user's home directory. Each shell type has its own configuration file.


.. admonition:: Question 5
   :class: hint

   What does the ``~`` (tilde) symbol represent in a Linux terminal?

   A. The root directory.

   B. The previous directory.

   C. The current user's home directory.

   D. The temporary files directory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, The current user's home directory.

   *Explanation:* In Unix-like operating systems, the tilde ``~`` is a shorthand for the current user's home directory (e.g., ``/home/username``).


.. admonition:: Question 6
   :class: hint

   What is the **Command Palette** in VSCode?

   A. A panel that shows compiler errors and warnings.

   B. A searchable list of all available commands in VSCode.

   C. A tool for managing Git repositories.

   D. A color picker for themes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, A searchable list of all available commands in VSCode.

   *Explanation:* The Command Palette (``Ctrl + Shift + P``) is a universal search box for actions, including built-in commands and those from installed extensions.


.. admonition:: Question 7
   :class: hint

   What is the purpose of the ``CMakeLists.txt`` file?

   A. It stores VSCode workspace settings.

   B. It defines the build configuration for a C++ project.

   C. It lists all installed Linux packages.

   D. It contains shell aliases and functions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, It defines the build configuration for a C++ project.

   *Explanation:* ``CMakeLists.txt`` is used by CMake to specify which source files to compile, which libraries to link against, and other build-related settings.


.. admonition:: Question 8
   :class: hint

   Which file inside the ``.vscode`` folder stores **debug configurations**?

   A. ``settings.json``

   B. ``extensions.json``

   C. ``launch.json``

   D. ``tasks.json``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, ``launch.json``

   *Explanation:* ``launch.json`` contains debug configurations for the project. ``settings.json`` stores workspace settings, ``tasks.json`` automates workflows, and ``extensions.json`` lists recommended extensions.


.. admonition:: Question 9
   :class: hint

   Which C++ standard does **all** code in this course target?

   A. C++14

   B. C++17

   C. C++20

   D. C++23

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, C++20.

   *Explanation:* C++20 is the newest standard that GCC 13, the required compiler, fully supports. GCC's C++23 support is only partial. C++20 is also compatible with the C++17 floor that ROS 2 Jazzy requires, so nothing learned in the first half has to be unlearned in the second.


.. admonition:: Question 10
   :class: hint

   Your program compiles, but the build fails with ``undefined
   reference to``. Which stage produced that message?

   A. The preprocessor.

   B. The compiler.

   C. The linker.

   D. The loader, at run time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, the linker.

   *Explanation:* ``undefined reference to`` means the compiler accepted your code, but the linker could not find the definition of something you used. That is a missing source file or a missing library, not a syntax problem.


.. admonition:: Question 11
   :class: hint

   What does the **preprocessor** operate on?

   A. Machine code, which it optimizes before execution.

   B. Text, with no understanding of C++ syntax or semantics.

   C. The abstract syntax tree produced by the compiler.

   D. Object files, which it merges into an executable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, text, with no understanding of C++ syntax or semantics.

   *Explanation:* The preprocessor removes comments, adjusts whitespace, and handles directives that start with ``#``. ``#include`` is a literal copy-paste of a file. It applies no language rules, which is why preprocessor mistakes often surface as confusing compiler errors later.


.. admonition:: Question 12
   :class: hint

   What does ``g++ -std=c++20 -c main.cpp`` produce?

   A. Preprocessed source, ``main.i``.

   B. An object file, ``main.o``.

   C. An executable named ``main``.

   D. Assembly source, ``main.s``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, an object file, ``main.o``.

   *Explanation:* ``-c`` compiles but does not link. It preprocesses, compiles to assembly, and assembles to machine code, stopping before the linker. Use ``-E`` to stop after preprocessing (``main.i``) instead.


.. admonition:: Question 13
   :class: hint

   What is the effect of ``set(CMAKE_CXX_STANDARD_REQUIRED ON)``?

   A. It installs the compiler needed for the requested standard.

   B. It makes the build fail if the compiler cannot provide the
      requested standard.

   C. It forces ``-std=gnu++20`` rather than ``-std=c++20``.

   D. It has no effect unless ``CMAKE_CXX_EXTENSIONS`` is also set.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, it makes the build fail if the compiler cannot provide the requested standard.

   *Explanation:* Without it, CMake quietly falls back to an older standard when the compiler is too old, and you discover the problem much later. ``CMAKE_CXX_EXTENSIONS OFF`` is the separate setting that asks for ``-std=c++20`` rather than ``-std=gnu++20``.


.. admonition:: Question 14
   :class: hint

   In ``cmake -S . -B build``, what do ``-S`` and ``-B`` specify?

   A. ``-S`` the standard, ``-B`` the build type.

   B. ``-S`` the source directory, ``-B`` the build directory.

   C. ``-S`` silent mode, ``-B`` the binary name.

   D. ``-S`` the system compiler, ``-B`` the build generator.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, ``-S`` is the source directory and ``-B`` is the build directory.

   *Explanation:* This is the *configure* step: CMake reads ``CMakeLists.txt`` from the source directory and generates a build tree in the build directory. ``cmake --build build`` then runs the compiler and linker.


.. admonition:: Question 15
   :class: hint

   Which standard is generally regarded as the point where **modern
   C++** begins?

   A. C++98

   B. C++03

   C. C++11

   D. C++17

.. dropdown:: Answer
   :class-container: sd-border-success

   **C**, C++11.

   *Explanation:* C++11 introduced uniform initialization, ``auto``, range-based ``for``, lambdas, ``nullptr``, move semantics, and smart pointers. Later standards refine that foundation rather than replace it. A tutorial written before 2011 teaches a different language in practice.


.. admonition:: Question 16
   :class: hint

   You used a generative AI tool to help interpret a compiler error
   while working on an RWA. What does the course policy require?

   A. Nothing; AI use does not need to be mentioned.

   B. Disclose it at the top of the submission, naming the tool and how
      it was used.

   C. Remove all AI-assisted code before submitting.

   D. Request written permission from the instructor beforehand.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B**, disclose it at the top of the submission, naming the tool and how it was used.

   *Explanation:* On RWAs, Group Projects, and weekly exercises, AI use is permitted with disclosure; two or three sentences are enough. Disclosure carries no penalty, while undisclosed use is a violation of the Code of Academic Integrity. AI tools are not permitted during quizzes at all.



----

True / False
============

.. admonition:: Question 17
   :class: hint

   **True or False:** Workspace ``settings.json`` takes precedence over
   user ``settings.json`` in VSCode.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Workspace settings override user settings, allowing project-specific configuration without affecting global preferences.


.. admonition:: Question 18
   :class: hint

   **True or False:** Shell aliases persist across terminal sessions
   without being added to a configuration file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Aliases defined directly in a terminal session are temporary. To persist them across sessions, they must be added to a shell configuration file (e.g., ``.bashrc`` or ``.zshrc``).


.. admonition:: Question 19
   :class: hint

   **True or False:** The ``ps -p $$`` command displays the current
   shell being used.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* ``$$`` is a special variable that holds the PID of the current shell process. ``ps -p $$`` displays information about that process, including the shell name.


.. admonition:: Question 20
   :class: hint

   **True or False:** Fish shell uses ``.bashrc`` as its configuration
   file.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Fish uses ``config.fish``, located in ``~/.config/fish/``. ``.bashrc`` is used by Bash.


.. admonition:: Question 21
   :class: hint

   **True or False:** The C++ standard a file is compiled against is a
   property of the source file itself.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* The standard is a compiler flag (``-std=c++20``), or the equivalent CMake setting. Nothing in the ``.cpp`` file records it. Omitting the flag means silently compiling against whatever your compiler happens to default to.


.. admonition:: Question 22
   :class: hint

   **True or False:** Deleting the ``build/`` directory is safe, and is
   a reasonable first response to a build that has started behaving
   strangely.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Everything in ``build/`` is generated by CMake and can be regenerated by configuring again. It should also be listed in ``.gitignore``, since committing a build tree makes a repository unusable for teammates.


.. admonition:: Question 23
   :class: hint

   **True or False:** Generative AI tools may be used during quizzes as
   long as their use is disclosed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Disclosure covers RWAs, Group Projects, and weekly exercises. Quizzes permit open notes, the book, and online references, but no AI assistance and no makeups.


.. admonition:: Question 24
   :class: hint

   **True or False:** ``return 0;`` can be omitted from ``main()``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* ``main()`` is special: reaching its closing brace returns 0 automatically. It must still be declared to return ``int``, never ``void``.
