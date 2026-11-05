.. _l9_setup:

====================================================
Setup Before Class
====================================================

In Lecture 9 we review the given steps of the Live Coding together, and we write Steps 4, 5 and 6 together: I type them, and you follow along. Class time is for writing code, so get your workspace ready **before class**. Lecture 9 uses two folders, ``project/week9/ride_service`` and ``project/week9/playground``.

Step 1: Get Your Workspace Ready
--------------------------------

Do these yourself, before class. The script in Step 2 does none of them.

1. **The tools.** On Ubuntu, install ``g++``, ``cmake`` and ``git`` if you have not yet:

   .. code-block:: bash

      sudo apt install build-essential cmake git

2. **The course C++ repository.** Clone it if you have not yet. The default place is ``~/enpm702_cpp/enpm702-fall-2026-cpp``:

   .. code-block:: bash

      git clone https://github.com/zeidk/enpm702-fall-2026-cpp.git ~/enpm702_cpp/enpm702-fall-2026-cpp

3. **The latest code.** Pull it, so that you have the ``project/week9/ride_service`` and ``project/week9/playground`` folders:

   .. code-block:: bash

      cd ~/enpm702_cpp/enpm702-fall-2026-cpp
      git pull

4. **The 702 commands.** Your terminal must load ``enpm702-cpp.sh``, as the setup notes at the top of that file say. If you set this up for Lecture 8, skip this item. Otherwise, add this line once to ``~/.bashrc`` (or ``~/.zshrc`` if you use zsh), then open a new terminal:

   .. code-block:: bash

      source ~/enpm702_cpp/enpm702-fall-2026-cpp/enpm702-cpp.sh

5. **Week 9 enabled.** In the repository's ``CMakeLists.txt``, the line ``add_subdirectory(project/week9)`` must not start with ``#``.

Step 2: Compile and Run, Once
-----------------------------

1. Go to the repository's top folder. The script is in ``project/week9/week9.sh``, since the pull of Step 1. If your clone is somewhere else, use that folder:

   .. code-block:: bash

      cd ~/enpm702_cpp/enpm702-fall-2026-cpp

2. Run it. It does not change any file in the repository: it only compiles and runs the four programs of Lecture 9: ``week9_ride_service``, ``week9_playground``, ``week9_operators`` and ``week9_cycle``.

   .. code-block:: bash

      bash project/week9/week9.sh

   The script finds the repository from its own place in ``project/week9``, so it works wherever you cloned it.

3. Read the output. Each check has a green ✔ when it passed, or a red ✘ and the lines to fix (``ok`` and ``FIX`` when the output is not a terminal). When all is well, it looks like this:

   .. code-block:: text

        ╭──────────────────────────────────────────────╮
        │  ENPM702 · Week 9 check                      │
        ╰──────────────────────────────────────────────╯

        Repository  ~/enpm702_cpp/enpm702-fall-2026-cpp
          ✔ repository found

        week9_ride_service
          ✔ built week9_ride_service (4 s)
          ✔ ran week9_ride_service

        week9_playground
          ✔ built week9_playground (6 s)
          ✔ ran week9_playground

        week9_operators
          ✔ built week9_operators (3 s)
          ✔ ran week9_operators

        week9_cycle
          ✔ built week9_cycle (1 s)
          ✔ ran week9_cycle

        ✔ Ready for class.

        In class, type this once in your terminal, from the repository's top folder:
            source project/week9/week9.sh
        Then:
            week9            build everything, then run the ride service
            week9 75         the code of [Slide 75]

   The times are those of a first build on the instructor's PC; yours depend on your computer.

In Class: ``week9``
-------------------

In class, load the script into your terminal once, from the repository's top folder, with ``source`` instead of ``bash``:

.. code-block:: bash

   source project/week9/week9.sh

This gives the terminal the command ``week9``. After each step, save your files and type:

.. code-block:: bash

   week9

``week9`` builds the four programs of Lecture 9. If they compile, it runs ``week9_ride_service`` and shows what it prints. If one does not compile, it shows the compiler's errors: fix the first one, save, and type ``week9`` again. Each block in ``ride_service/src/main.cpp`` prints ``[Step N]`` and what that step adds; a block stays commented out until we reach its step.

With a slide's number, ``week9`` runs the code of that slide instead: ``week9 75`` for slide 75, ``week9 xl`` for appendix page xl.

``week9`` exists only in the terminal where you typed ``source``. In a new terminal, type the ``source`` line again. The ``702build`` and ``702run`` commands do the same, one program at a time (``702run week9_ride_service``), if your terminal loads ``enpm702-cpp.sh`` and you typed ``enpm702``.

Common Fixes
------------

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - The message says
     - What to do
   * - no ENPM702 repository
     - Clone the repository (Step 1), and keep the script in its ``project/week9/`` folder.
   * - ``No such file or directory``, for ``project/week9/week9.sh``
     - Pull the latest code (Step 1), then run the command from the repository's top folder.
   * - cmake could not configure the repository
     - Install the tools (Step 1). If ``cmake`` is installed, read the lines printed under the ``FIX`` line.
   * - A program did not build, with ``No rule to make target``
     - Pull the latest code, and enable week 9 in ``CMakeLists.txt`` (Step 1). Then configure again, so that CMake sees the change: ``702configure``, or ``cmake -S . -B build`` in the repository.
   * - A program did not build, or did not compile, with compiler errors
     - Read the first error: it names the file and the line. If you did not change that file, run ``git status`` in the repository. If the lines do not tell you what to do, send them to me before class.
   * - ``week9: command not found``
     - In that terminal, from the repository's top folder, type ``source project/week9/week9.sh`` first.
   * - ``702run: command not found``
     - Type ``enpm702`` first, or use ``week9``.
