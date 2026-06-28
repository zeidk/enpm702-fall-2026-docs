====================================================
VSCode and CMake
====================================================

Overview
--------

This reading material walks you through configuring Visual Studio Code
to write, build, and run C++ programs with CMake on Ubuntu. It is
provided as a self-study reading module. Students should watch this
before the first lecture so that the workspace, extensions, and build
configuration are ready to use during in-class demonstrations.

The material assumes Ubuntu is already installed and that the build
tools (``build-essential``, ``gdb``, ``cmake``) have been installed
following :doc:`/setup/cpp_setup`.


.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Install Visual Studio Code on Ubuntu and launch it from a terminal.
   - Identify the main areas of the VSCode user interface (Activity Bar,
     Editor, Terminal, Status Bar).
   - Organize C++ work into a course-wide workspace with the expected
     folder layout.
   - Configure a workspace with the ``.vscode/`` folder, including
     ``settings.json``, ``extensions.json``, ``launch.json``, and
     ``tasks.json``.
   - Install the recommended VSCode extensions for C++ development.
   - Use the Command Palette to drive common actions.
   - Write a ``CMakeLists.txt`` file that builds a small C++ program.
   - Apply the hybrid CMake approach used in this course (one root
     ``CMakeLists.txt`` plus one per lecture folder).
   - Build and run a target with the **CMake Tools** extension.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   vcm_lecture
   vcm_exercises
   vcm_quiz
   vcm_references
