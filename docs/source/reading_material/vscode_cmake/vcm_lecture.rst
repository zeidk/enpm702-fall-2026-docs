====================================================
Lecture
====================================================


Visual Studio Code
====================================================

`Visual Studio Code <https://code.visualstudio.com/>`_ (VSCode) is a
free, open-source code editor available on Windows, macOS, and Linux.
It is consistently ranked as one of the most popular code editors in
developer surveys, and it supports virtually every major programming
language either natively or through extensions.

VSCode is used in this course for the following reasons:

- It runs on the same Ubuntu environment used for ROS 2 development.
- It provides
  `IntelliSense <https://code.visualstudio.com/docs/editor/intellisense>`_
  (intelligent code completion), inline diagnostics,
  `integrated debugging <https://code.visualstudio.com/docs/editor/debugging>`_,
  `source-control views <https://code.visualstudio.com/docs/sourcecontrol/overview>`_,
  and an `integrated terminal <https://code.visualstudio.com/docs/terminal/basics>`_.
- The
  `extension ecosystem <https://marketplace.visualstudio.com/vscode>`_
  covers everything we need for C++ work: the ``C/C++`` language
  server, ``CMake Tools``, ``CMake`` syntax highlighting, ``Doxygen``
  comment generation, and ``GitLens``. See :doc:`vcm_references` for
  direct Marketplace links to each extension.

.. note::

   VSCode is *not* the only acceptable editor. Lectures and
   assignments are demonstrated in VSCode, so the configuration in
   this document is the one the instructor will reference when
   showing solutions.


Installation
----------------------------------------------------

VSCode is distributed for Ubuntu as a ``.deb`` package. The official
`VSCode on Linux <https://code.visualstudio.com/docs/setup/linux>`_
guide covers every install option; the steps below match the workflow
used in class.

1. Download the ``.deb`` installer from
   `code.visualstudio.com/download <https://code.visualstudio.com/download>`_.
2. Open a terminal, change into the folder containing the download,
   and install it with ``apt``:

   .. code-block:: bash

      cd ~/Downloads
      sudo apt install ./code_*_amd64.deb

3. Launch VSCode in one of two ways:

   - From a terminal, run ``code``.
   - From the Ubuntu **Applications** menu, search for *Visual Studio
     Code*.

.. tip::

   Launching VSCode from a terminal with ``code .`` opens the current
   working directory as the workspace. This is the workflow we will
   use throughout the course.


Essential Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

VSCode is organized into a small number of regions you will use
constantly. Each region is documented in the
`User Interface <https://code.visualstudio.com/docs/getstarted/userinterface>`_
guide.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Region
     - Purpose
   * - **Activity Bar** (left edge)
     - Switches between the File Explorer, Search, Source Control,
       Run and Debug, Extensions, and any view added by an extension.
   * - **Editor**
     - The main area where source code is read and written. Files
       open in tabs, and the editor can be split horizontally or
       vertically.
   * - **Terminal**
     - An integrated terminal that runs the same shell as your
       login session (``bash`` or ``zsh``). Open it with
       ``Ctrl + ` `` (backtick).
   * - **Status Bar** (bottom edge)
     - Shows the active build target, the current Git branch, line
       and column position, errors and warnings, and any indicators
       added by extensions.


Workspace
----------------------------------------------------

A `workspace <https://code.visualstudio.com/docs/editor/workspaces>`_
is the folder that VSCode treats as the root of the project.
Workspace-level settings, recommended extensions, debug
configurations, and build tasks all live inside that folder.

For this course, use a single workspace for all C++ lectures. Each
weekly lecture lives in its own subfolder:

.. code-block:: text

   enpm702_ws/
   ├── CMakeLists.txt          # root CMakeLists.txt (hybrid approach)
   └── weekX/
       ├── CMakeLists.txt      # lecture-level CMakeLists.txt
       ├── src/
       │   └── *.cpp
       └── include/
           └── *.hpp

Open the workspace in VSCode from a terminal:

.. code-block:: bash

   cd ~/enpm702_ws
   code .

.. tip::

   Keeping every lecture under one workspace lets the **CMake Tools**
   extension see them all at once. You can switch the active build
   target from one lecture to another without closing or reopening
   VSCode.


Configuration
====================================================

The ``.vscode`` Folder
----------------------------------------------------

The ``.vscode/`` folder is a special directory inside the workspace
root that holds workspace-specific configuration. Settings placed
here apply only to this workspace; they do not override your global
user settings.

The four files we use in this course are linked below to their
official VSCode reference page:

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - File
     - Purpose
   * - `settings.json <https://code.visualstudio.com/docs/getstarted/settings>`_
     - Workspace-specific editor settings (font size, format on
       save, ruler positions, etc.). Overrides the matching user
       settings only inside this workspace.
   * - `launch.json <https://code.visualstudio.com/docs/editor/debugging#_launch-configurations>`_
     - Debug configurations. Tells VSCode how to start your program
       under ``gdb``.
   * - `tasks.json <https://code.visualstudio.com/docs/editor/tasks>`_
     - Automation for repeated commands (build, clean, run). Can be
       triggered from the Command Palette or bound to a key.
   * - `extensions.json <https://code.visualstudio.com/docs/editor/extension-marketplace#_workspace-recommended-extensions>`_
     - The list of recommended extensions for this workspace. When a
       collaborator opens the workspace, VSCode prompts them to
       install anything missing.

A minimal ``extensions.json`` for this course looks like this:

.. code-block:: json

   {
     "recommendations": [
       "ms-vscode.cpptools",
       "ms-vscode.cmake-tools",
       "twxs.cmake",
       "cschlosser.doxdocgen",
       "usernamehw.errorlens",
       "eamodio.gitlens"
     ]
   }

Download a ready-made copy: :download:`extensions.json
</_static/files/extensions.json>`.

After placing the file in ``.vscode/``, prompt VSCode to install the
recommended extensions:

1. Open the Command Palette with ``Ctrl + Shift + P``.
2. Type *Extensions: Show Recommended Extensions* and press
   ``Enter``.
3. In the Extensions view, click the cloud icon at the top to install
   all recommended extensions at once.

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Extension
     - Purpose
   * - `C/C++ <https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools>`_ (Microsoft)
     - IntelliSense, inline diagnostics, debugging, and code
       browsing for C and C++. See the
       `C++ in VSCode <https://code.visualstudio.com/docs/languages/cpp>`_
       guide.
   * - `CMake Tools <https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools>`_ (Microsoft)
     - Configures, builds, and debugs CMake projects from inside
       VSCode. See the
       `CMake Tools documentation <https://code.visualstudio.com/docs/cpp/CMake-linux>`_.
   * - `CMake <https://marketplace.visualstudio.com/items?itemName=twxs.cmake>`_ (twxs)
     - Syntax highlighting for ``CMakeLists.txt``.
   * - `Doxygen Documentation Generator <https://marketplace.visualstudio.com/items?itemName=cschlosser.doxdocgen>`_
     - Generates Doxygen comment blocks when you type ``/**`` above
       a function.
   * - `Error Lens <https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens>`_
     - Shows compiler errors and warnings inline next to the code.
   * - `GitLens <https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens>`_
     - Adds blame annotations and rich Git history to the editor.


Settings
----------------------------------------------------

VSCode has two layers of
`settings <https://code.visualstudio.com/docs/getstarted/settings>`_:

- **User settings**: apply to every workspace you open.
- **Workspace settings**: apply only to the current workspace and
  override the matching user settings.

Open the settings UI with ``File`` → ``Preferences`` → ``Settings``
or with the keyboard shortcut ``Ctrl + ,``. The full list of
configurable options is in the
`default settings reference <https://code.visualstudio.com/docs/getstarted/settings#_default-settings>`_.

Workspace settings live in ``.vscode/settings.json``. A minimal
configuration that keeps source consistent across the class:

.. code-block:: json

   {
     "editor.formatOnSave": true,
     "editor.rulers": [80],
     "editor.tabSize": 4,
     "editor.insertSpaces": true,
     "files.insertFinalNewline": true,
     "files.trimTrailingWhitespace": true,
     "C_Cpp.default.cppStandard": "c++17"
   }

Download a ready-made copy: :download:`settings.json
</_static/files/settings.json>`.

.. warning::

   Workspace ``settings.json`` takes precedence over user
   ``settings.json``. If something behaves differently from what your
   user settings say, look in the workspace file first.


The Command Palette
----------------------------------------------------

The
`Command Palette <https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette>`_
is a searchable list of every command available in VSCode, including
those added by extensions. Think of it as a universal action bar.

- Open it with ``Ctrl + Shift + P``.
- Start typing the action you want; matches narrow as you type.
- Press ``Enter`` to run the highlighted action.

Examples of commands we will use often:

- *CMake: Configure*
- *CMake: Build*
- *CMake: Set Build Target*
- *Extensions: Show Recommended Extensions*
- *Developer: Reload Window*
- *Format Document*


CMake
====================================================

`CMake <https://cmake.org/>`_ is an open-source, cross-platform family
of tools designed to build, test, and package software. Rather than
writing a different build script for every compiler, you describe the
build once in a
`CMakeLists.txt <https://cmake.org/cmake/help/latest/guide/tutorial/index.html>`_
file and CMake generates the platform-specific build files
(Makefiles, Ninja files, Visual Studio projects, etc.) for you. A
gentle starting point is the official
`Basic Starting Point <https://cmake.org/cmake/help/latest/guide/tutorial/A%20Basic%20Starting%20Point.html>`_
tutorial.

Install CMake with ``apt`` and verify the version:

.. code-block:: bash

   sudo apt install cmake
   cmake --version

A ``CMakeLists.txt`` is the input file CMake reads. It specifies the
project name, the C++ standard, which source files to compile, which
headers to expose, and any libraries to link against.

A minimal ``CMakeLists.txt`` for a single executable:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.16)
   project(week1 LANGUAGES CXX)

   set(CMAKE_CXX_STANDARD 17)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   set(CMAKE_CXX_EXTENSIONS OFF)

   add_executable(week1 src/main.cpp)
   target_include_directories(week1 PRIVATE include)

Each command above is documented in the official CMake reference:

- `cmake_minimum_required <https://cmake.org/cmake/help/latest/command/cmake_minimum_required.html>`_
  pins the minimum CMake version required to process the file.
- `project <https://cmake.org/cmake/help/latest/command/project.html>`_
  declares the project name and enabled languages.
- `set <https://cmake.org/cmake/help/latest/command/set.html>`_ +
  `CMAKE_CXX_STANDARD <https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD.html>`_
  /
  `CMAKE_CXX_STANDARD_REQUIRED <https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD_REQUIRED.html>`_
  /
  `CMAKE_CXX_EXTENSIONS <https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_EXTENSIONS.html>`_
  pin the C++ standard for every target in the project.
- `add_executable <https://cmake.org/cmake/help/latest/command/add_executable.html>`_
  declares a build target and its source files.
- `target_include_directories <https://cmake.org/cmake/help/latest/command/target_include_directories.html>`_
  exposes header search paths to a specific target.


Hybrid Approach
----------------------------------------------------

The hybrid approach lets each lecture compile on its own *and* lets
you compile every lecture together from the workspace root. It uses
`add_subdirectory <https://cmake.org/cmake/help/latest/command/add_subdirectory.html>`_
to compose:

- a **root** ``CMakeLists.txt`` at the top of ``enpm702_ws/`` that
  defines settings common to every lecture, and
- one ``CMakeLists.txt`` **per lecture folder** that defines the
  executable for that lecture.

A minimal root ``CMakeLists.txt``:

.. code-block:: cmake

   cmake_minimum_required(VERSION 3.16)
   project(enpm702_ws LANGUAGES CXX)

   set(CMAKE_CXX_STANDARD 17)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   set(CMAKE_CXX_EXTENSIONS OFF)

   add_subdirectory(week1)
   # add_subdirectory(week2)
   # add_subdirectory(week3)
   # ... add more as the semester progresses

Each lecture folder then has a much smaller ``CMakeLists.txt``:

.. code-block:: cmake

   add_executable(week1 src/main.cpp)
   target_include_directories(week1 PRIVATE include)

Workflow with the
`CMake Tools <https://code.visualstudio.com/docs/cpp/CMake-linux>`_
extension:

1. Make sure ``build-essential`` and ``gdb`` are installed:

   .. code-block:: bash

      sudo apt install build-essential gdb

2. Place the root ``CMakeLists.txt`` at the top of the workspace.
3. Open the Command Palette (``Ctrl + Shift + P``) and run
   *CMake: Set Build Target* to choose the lecture you want to
   build.
4. Open the Command Palette again and run *Developer: Reload
   Window*. The **CMake** view should appear in the Activity Bar.
5. Run *CMake: Configure* once. This selects a compiler kit and
   generates the underlying build system.
6. Run *CMake: Build* once to compile the current target.
7. From now on, the play button (▶) at the bottom of the window
   builds and runs the active target in a single click. Use the bug
   icon next to it to launch under ``gdb``.

.. tip::

   The active build target is shown in the Status Bar. Click it to
   switch from one lecture to another without leaving VSCode.


Keyboard Shortcuts and Snippets
====================================================

You will type ``std::cout`` constantly. VSCode supports two ways to
shorten it:

- `User snippet <https://code.visualstudio.com/docs/editor/userdefinedsnippets>`_:
  drop a ``cout.code-snippets`` file in ``.vscode/`` so the workspace
  has a ``cout`` snippet available.
- `Keyboard shortcut <https://code.visualstudio.com/docs/getstarted/keybindings>`_:
  bind the snippet to a key chord through ``File`` → ``Preferences``
  → ``Keyboard Shortcuts``.

A small snippet that expands ``cout`` into a full statement:

.. code-block:: json

   {
     "cout": {
       "prefix": "cout",
       "body": [
         "std::cout << \"$1\" << '\\n';"
       ],
       "description": "Insert a std::cout statement."
     }
   }

After saving the file, type ``cout`` in any C++ file and press
``Tab`` to expand it. The cursor will land between the quotes so you
can immediately type the message.

Download ready-made copies: :download:`cout.code-snippets
</_static/files/cout.code-snippets>` (place in ``.vscode/``) and
:download:`cout-snippet-key-binding.txt
</_static/files/cout-snippet-key-binding.txt>` (the key-chord binding to
paste into your ``keybindings.json``). A printable
:download:`VSCode keyboard shortcuts reference (Linux)
</_static/files/keyboard-shortcuts-linux.pdf>` is also available.


Wrap-Up
====================================================

You should now have:

- VSCode installed and launchable with ``code``.
- A workspace at ``~/enpm702_ws/`` with a ``.vscode/`` folder.
- ``extensions.json``, ``settings.json``, and a ``cout.code-snippets``
  file inside ``.vscode/``.
- A root ``CMakeLists.txt`` and at least one lecture folder with its
  own ``CMakeLists.txt``.
- The ability to build and run a target with the **CMake Tools**
  extension.

Move on to :doc:`vcm_exercises` to apply the configuration to a small
hello-world project before the first lecture.
