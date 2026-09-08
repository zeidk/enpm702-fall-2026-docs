====================================================
Exercises
====================================================


.. note::

   **Not graded, and not submitted on Canvas.** These exercises belong to
   a self-study reading module: work them at your own pace. Only the
   assignments listed on Canvas are collected.

.. dropdown:: Exercise 1: Install VSCode and Confirm the Version
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

.. dropdown:: Exercise 2: Create the Course Workspace
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Create the workspace folder structure used throughout the course and
   open it in VSCode.

   - Workspace root: ``~/enpm702_ws``
   - One lecture folder: ``week1`` with ``src/`` and ``include/``
     subfolders.
   - An empty ``src/main.cpp`` placeholder.

.. dropdown:: Exercise 3: Configure ``.vscode/extensions.json``
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add the course's recommended extensions to the workspace and install
   them in one click.

   1. Create the ``.vscode`` folder at the workspace root.
   2. Add an ``extensions.json`` file that recommends the six course
      extensions.
   3. Use the Command Palette to install them.

.. dropdown:: Exercise 4: Add Workspace Settings
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add workspace-level editor settings so that every file in the
   workspace formats on save, shows a vertical ruler at column 80, and
   targets the C++20 standard.

.. dropdown:: Exercise 5: Write a Hello-World ``CMakeLists.txt``
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add the source for a small ``Hello, ENPM702!`` program and a
   ``CMakeLists.txt`` that builds it. Use the hybrid layout: one root
   ``CMakeLists.txt`` at the workspace root and one inside ``week1/``.

.. dropdown:: Exercise 6: Build and Run with CMake Tools
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

.. dropdown:: Exercise 7: Bind a ``cout`` Snippet
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Add a workspace snippet so typing ``cout`` and pressing ``Tab``
   inserts a complete ``std::cout`` statement. Verify it works in
   ``week1/src/main.cpp``.
