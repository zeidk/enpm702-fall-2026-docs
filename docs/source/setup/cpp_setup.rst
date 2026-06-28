====================================================
C++ Development Environment
====================================================

.. _setup-cpp:

Complete this setup before the first lecture. Make sure you have
:doc:`Ubuntu installed <ubuntu_setup>` first.


Build Tools
-----------

Install the essential build tools, debugger, CMake, and Valgrind:

.. code-block:: bash

   sudo apt update
   sudo apt install build-essential gdb cmake valgrind

Verify the installation:

.. code-block:: bash

   g++ --version
   cmake --version
   gdb --version
   valgrind --version

.. note::

   ``build-essential`` includes ``g++`` (the GNU C++ compiler),
   ``make``, and other libraries needed to compile C++ programs.
   ``valgrind`` is a memory debugging and leak detection tool used
   throughout the course.


Visual Studio Code
------------------

Installing and configuring VSCode (including the recommended
extensions, the ``.vscode`` folder, the course workspace layout, and
the CMake build flow) is covered in its own reading material:
:doc:`/reading_material/vscode_cmake/vcm_index`. Work through that
reading module and its exercises before the first lecture.


Doxygen
-------

Doxygen generates documentation from annotated C++ source code.

.. code-block:: bash

   sudo apt install doxygen doxygen-gui


Git
---

Install Git and configure your identity:

.. code-block:: bash

   sudo apt install git
   git config --global user.name "Your Name"
   git config --global user.email "your_email@example.com"

Create a `GitHub <https://github.com>`_ account if you do not already
have one.

.. tip::

   Work through the **Version Control** reading module for a
   full walkthrough of Git and GitHub workflows used in this course.
