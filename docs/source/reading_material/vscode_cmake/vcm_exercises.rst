====================================================
Exercises
====================================================


.. dropdown:: Exercise 1 -- Install VSCode and Confirm the Version
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Install Visual Studio Code on your Ubuntu machine and confirm the
   installation works from a terminal.

   1. Download the ``.deb`` package from
      `code.visualstudio.com/download <https://code.visualstudio.com/download>`_.
   2. Install it with ``apt``.
   3. Confirm the installation by printing the version from a
      terminal.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         cd ~/Downloads
         sudo apt install ./code_*_amd64.deb
         code --version

      Expected output (your version numbers will differ):

      .. code-block:: text

         1.95.3
         f1a4fb101478ce6ec82fe9627c43efbf9e98c813
         x64


.. dropdown:: Exercise 2 -- Create the Course Workspace
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create the workspace folder structure used throughout the course and
   open it in VSCode.

   - Workspace root: ``~/enpm702_ws``
   - One lecture folder: ``week1`` with ``src/`` and ``include/``
     subfolders.
   - An empty ``src/main.cpp`` placeholder.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         mkdir -p ~/enpm702_ws/week1/{src,include}
         touch ~/enpm702_ws/week1/src/main.cpp
         cd ~/enpm702_ws
         code .


.. dropdown:: Exercise 3 -- Configure ``.vscode/extensions.json``
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add the course's recommended extensions to the workspace and install
   them in one click.

   1. Create the ``.vscode`` folder at the workspace root.
   2. Add an ``extensions.json`` file that recommends the six course
      extensions.
   3. Use the Command Palette to install them.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         mkdir -p ~/enpm702_ws/.vscode

      Place the following in ``~/enpm702_ws/.vscode/extensions.json``:

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

      In VSCode:

      1. Open the Command Palette with ``Ctrl + Shift + P``.
      2. Run *Extensions: Show Recommended Extensions*.
      3. In the panel that opens, click the cloud icon at the top to
         install all six at once.


.. dropdown:: Exercise 4 -- Add Workspace Settings
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add workspace-level editor settings so that every file in the
   workspace formats on save, shows a vertical ruler at column 80, and
   targets the C++17 standard.

   .. dropdown:: Solution
      :class-container: sd-border-success

      Place the following in ``~/enpm702_ws/.vscode/settings.json``:

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


.. dropdown:: Exercise 5 -- Write a Hello-World ``CMakeLists.txt``
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add the source for a small ``Hello, ENPM702!`` program and a
   ``CMakeLists.txt`` that builds it. Use the hybrid layout: one root
   ``CMakeLists.txt`` at the workspace root and one inside ``week1/``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      ``~/enpm702_ws/week1/src/main.cpp``:

      .. code-block:: cpp

         #include <iostream>

         int main() {
             std::cout << "Hello, ENPM702!" << '\n';
             return 0;
         }

      ``~/enpm702_ws/week1/CMakeLists.txt``:

      .. code-block:: cmake

         add_executable(week1 src/main.cpp)
         target_include_directories(week1 PRIVATE include)

      ``~/enpm702_ws/CMakeLists.txt``:

      .. code-block:: cmake

         cmake_minimum_required(VERSION 3.16)
         project(enpm702_ws LANGUAGES CXX)

         set(CMAKE_CXX_STANDARD 17)
         set(CMAKE_CXX_STANDARD_REQUIRED ON)
         set(CMAKE_CXX_EXTENSIONS OFF)

         add_subdirectory(week1)


.. dropdown:: Exercise 6 -- Build and Run with CMake Tools
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Use the **CMake Tools** extension to configure, build, and run the
   ``week1`` target.

   1. Set the active build target to ``week1``.
   2. Reload the window so the **CMake** view appears in the
      Activity Bar.
   3. Configure the project.
   4. Build the project.
   5. Run it.

   Expected terminal output after running:

   .. code-block:: text

      Hello, ENPM702!

   .. dropdown:: Solution
      :class-container: sd-border-success

      All steps are reached from the Command Palette
      (``Ctrl + Shift + P``):

      1. *CMake: Set Build Target* → choose ``week1``.
      2. *Developer: Reload Window*.
      3. *CMake: Configure*. Choose a GCC compiler kit when prompted.
      4. *CMake: Build*.
      5. Click the ▶ button at the bottom of the window, or run
         *CMake: Run Without Debugging*.


.. dropdown:: Exercise 7 -- Bind a ``cout`` Snippet
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add a workspace snippet so typing ``cout`` and pressing ``Tab``
   inserts a complete ``std::cout`` statement. Verify it works in
   ``week1/src/main.cpp``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      Place the following in
      ``~/enpm702_ws/.vscode/cout.code-snippets``:

      .. code-block:: json

         {
           "cout": {
             "scope": "cpp",
             "prefix": "cout",
             "body": [
               "std::cout << \"$1\" << '\\n';"
             ],
             "description": "Insert a std::cout statement."
           }
         }

      In ``main.cpp``, type ``cout`` and press ``Tab``. The line
      should expand to:

      .. code-block:: cpp

         std::cout << "" << '\n';

      with the cursor placed between the quotes.
