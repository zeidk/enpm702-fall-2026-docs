====================================================
VSCode and CMake: Quiz
====================================================


.. admonition:: Question 1
   :class: hint

   Which keyboard shortcut opens the VSCode Command Palette?

   a) ``Ctrl + P``
   b) ``Ctrl + Shift + P``
   c) ``Ctrl + Alt + P``
   d) ``F1`` only

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Ctrl + Shift + P**

      ``Ctrl + P`` opens the *Go to File* picker, not the Command
      Palette. ``F1`` is a valid alternative for the Command Palette,
      but ``Ctrl + Shift + P`` is the standard binding used in the
      lectures.


.. admonition:: Question 2
   :class: hint

   Where does VSCode look for workspace-specific configuration?

   a) ``~/.config/Code/User/``
   b) ``<workspace>/.code/``
   c) ``<workspace>/.vscode/``
   d) ``<workspace>/settings/``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) <workspace>/.vscode/**

      ``settings.json``, ``launch.json``, ``tasks.json``, and
      ``extensions.json`` all live in the ``.vscode`` folder at the
      workspace root. The ``~/.config/Code/User/`` path holds *user*
      settings instead.


.. admonition:: Question 3
   :class: hint

   If a key has different values in user ``settings.json`` and
   workspace ``settings.json``, which one wins?

   a) The user settings.
   b) The workspace settings.
   c) Whichever was edited last.
   d) Neither, VSCode refuses to start.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) The workspace settings.**

      Workspace settings always take precedence over user settings
      inside that workspace. The user settings still apply in every
      other workspace.


.. admonition:: Question 4
   :class: hint

   What is the purpose of ``.vscode/extensions.json``?

   a) It blocks extensions from being installed.
   b) It lists recommended extensions for the workspace.
   c) It controls auto-updates for extensions.
   d) It stores the configuration of each installed extension.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) It lists recommended extensions for the workspace.**

      When a collaborator opens the workspace, VSCode prompts them to
      install anything in the recommendations list that is missing.


.. admonition:: Question 5
   :class: hint

   What does CMake actually produce when it is run?

   a) A compiled executable.
   b) A platform-specific build system (for example, Makefiles or
      Ninja files).
   c) A debug symbol file.
   d) A package archive.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) A platform-specific build system.**

      CMake reads ``CMakeLists.txt`` and generates the underlying
      build files. A separate build tool (``make``, ``ninja``, ...)
      then turns those files into an executable.


.. admonition:: Question 6
   :class: hint

   In the hybrid CMake approach used in this course, which file
   defines the C++ standard for the whole workspace?

   a) Each ``weekX/CMakeLists.txt``.
   b) ``.vscode/settings.json``.
   c) The root ``CMakeLists.txt``.
   d) Nothing, CMake defaults to C++17.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) The root CMakeLists.txt.**

      The root file sets ``CMAKE_CXX_STANDARD`` once and the lecture
      folders inherit that setting through ``add_subdirectory``.


.. admonition:: Question 7
   :class: hint

   Which extension provides IntelliSense and inline diagnostics for
   C++ in VSCode?

   a) **CMake Tools** (Microsoft).
   b) **C/C++** (Microsoft).
   c) **GitLens**.
   d) **Error Lens**.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) C/C++ (Microsoft).**

      **CMake Tools** drives the build, **Error Lens** decorates
      diagnostics already produced by the language server, and
      **GitLens** is unrelated to C++ at all.


.. admonition:: Question 8
   :class: hint

   You have set up the workspace, written ``CMakeLists.txt``, and
   selected a build target, but the **CMake** icon does not appear in
   the Activity Bar. Which Command Palette action is the recommended
   next step?

   a) *CMake: Clean Rebuild*.
   b) *Developer: Reload Window*.
   c) *File: Revert File*.
   d) *Extensions: Uninstall*.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **b) Developer: Reload Window.**

      Reloading the window lets the **CMake Tools** extension pick
      up the new configuration. It is the third step in the hybrid
      workflow described in the lecture.


.. admonition:: Question 9
   :class: hint

   In the recommended workspace layout, where do C++ implementation
   files live?

   a) ``weekX/CMakeLists.txt``
   b) ``weekX/include/``
   c) ``weekX/src/``
   d) ``weekX/build/``

   .. dropdown:: Answer
      :class-container: sd-border-success

      **c) weekX/src/**

      ``include/`` holds header files (``*.hpp``), and ``build/`` is
      created by CMake to store generated build files. Implementation
      files (``*.cpp``) live in ``src/``.


.. admonition:: Question 10
   :class: hint

   You change ``.vscode/settings.json`` to set ``"editor.tabSize":
   2``, but the editor still inserts four spaces. What is the most
   likely cause?

   a) The ``settings.json`` file has a syntax error.
   b) The setting is not valid for C++ files.
   c) Workspace settings are cached and require a reinstall of
      VSCode.
   d) You also need to set ``"editor.insertSpaces": true``.

   .. dropdown:: Answer
      :class-container: sd-border-success

      **a) The settings.json file has a syntax error.**

      If JSON parsing fails, VSCode silently falls back to user
      settings. Open the Problems panel or the *Status Bar* error
      indicator to see the parse error. (Options b and c are not
      true; option d does not change tab *size*.)
