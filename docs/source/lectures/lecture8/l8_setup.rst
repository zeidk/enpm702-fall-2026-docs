.. _l8_setup:

====================================================
Setup Before Class
====================================================

In Lecture 8 you write Step 1 of the Live Coding with me and Steps 2 to 5 on your own, and you upload the code on Canvas before the end of class. Class time is for writing code, so get your workspace ready **before class**.

.. important::

   The code you upload at the end of class is graded.

   - **What you upload:** ``vehicle.hpp``, ``vehicle.cpp`` and ``main.cpp``, from ``project/week8/live``, to the L8 Live Coding assignment on Canvas, before the end of class.
   - **How it is graded:** as the L8 exercise (exercises are 5% of the grade). Class reached Step 4, so the score counts **Steps 2 to 4**, 4 points each, out of 12 and scaled to 20. A step earns its 4 points when you wrote it, whether or not the code builds, and part of them when you wrote part of it. Step 5 gets feedback but no points.
   - **No AI:** you write the code yourself. No chatbot, and no AI in VS Code (GitHub Copilot or any other AI extension): turn it off before class. Code written with AI gets **0**.
   - **Watching the recording?** Upload before the next lecture, on **Nov 3**. The same rules apply.

Step 1: Get Your Workspace Ready
--------------------------------

Do these yourself, before class. The script in Step 2 does none of them.

1. **The tools.** On Ubuntu, install ``g++``, ``cmake`` and ``git`` if you have not yet:

   .. code-block:: bash

      sudo apt install build-essential cmake git

2. **The course C++ repository.** Clone it if you have not yet. The default place is ``~/enpm702_cpp/enpm702-fall-2026-cpp``:

   .. code-block:: bash

      git clone https://github.com/zeidk/enpm702-fall-2026-cpp.git ~/enpm702_cpp/enpm702-fall-2026-cpp

3. **The latest code.** Pull it, so that you have the ``project/week8/live`` folder:

   .. code-block:: bash

      cd ~/enpm702_cpp/enpm702-fall-2026-cpp
      git pull

4. **The 702 commands.** Your terminal must load ``enpm702-cpp.sh``, as the setup notes at the top of that file say. Add this line once to ``~/.bashrc`` (or ``~/.zshrc`` if you use zsh), then open a new terminal:

   .. code-block:: bash

      source ~/enpm702_cpp/enpm702-fall-2026-cpp/enpm702-cpp.sh

5. **Week 8 enabled.** In the repository's ``CMakeLists.txt``, the line ``add_subdirectory(project/week8)`` must not start with ``#``.

Step 2: Compile and Run, Once
-----------------------------

1. Go to the repository's top folder. The script is in ``project/week8/week8.sh``, since the pull of Step 1. If your clone is somewhere else, use that folder:

   .. code-block:: bash

      cd ~/enpm702_cpp/enpm702-fall-2026-cpp

2. Run it. It does not change any file in the repository: it only compiles and runs the live coding program of Lecture 8, ``week8_live``.

   .. code-block:: bash

      bash project/week8/week8.sh

   The script finds the repository from its own place in ``project/week8``, so it works wherever you cloned it.

3. Read the output. Each check has a green ✔ when it passed, or a red ✘ and the lines to fix (``ok`` and ``FIX`` when the output is not a terminal). When all is well, it looks like this:

   .. code-block:: text

        ╭──────────────────────────────────────────────╮
        │  ENPM702 · Week 8 check                      │
        ╰──────────────────────────────────────────────╯

        Repository  ~/enpm702_cpp/enpm702-fall-2026-cpp
          ✔ repository found

        week8_live
          ✔ built week8_live (1 s)
          ✔ ran week8_live

        ✔ Ready for class.

        In class, type this once in your terminal, from the repository's top folder:
            source project/week8/week8.sh
        Then, after each step:
            live8

   The times are those of a first build on the instructor's PC; yours depend on your computer.

In Class: ``live8``
-------------------

In class, load the script into your terminal once, from the repository's top folder, with ``source`` instead of ``bash``:

.. code-block:: bash

   source project/week8/week8.sh

This gives the terminal one new command, ``live8``. After each step, save your files and type:

.. code-block:: bash

   live8

``live8`` builds ``week8_live``. If the code compiles, it runs the program and shows what it prints. If it does not compile, it shows the compiler's errors: fix the first one, save, and type ``live8`` again. At the start, ``week8_live`` prints nothing: each block in ``main.cpp`` stays commented out until we reach its step.

``live8`` exists only in the terminal where you typed ``source``. In a new terminal, type the ``source`` line again. The ``702build week8_live`` and ``702run week8_live`` commands do the same two things, if your terminal loads ``enpm702-cpp.sh`` and you typed ``enpm702``.

Common Fixes
------------

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - The message says
     - What to do
   * - no ENPM702 repository
     - Clone the repository (Step 1), and keep the script in its ``project/week8/`` folder.
   * - ``No such file or directory``, for ``project/week8/week8.sh``
     - Pull the latest code (Step 1), then run the command from the repository's top folder.
   * - cmake could not configure the repository
     - Install the tools (Step 1). If ``cmake`` is installed, read the lines printed under the ``FIX`` line.
   * - ``week8_live`` did not build, with ``No rule to make target 'week8_live'``
     - Pull the latest code, and enable week 8 in ``CMakeLists.txt`` (Step 1). Then configure again, so that CMake sees the change: ``702configure``, or ``cmake -S . -B build`` in the repository.
   * - ``week8_live`` did not build, or did not compile, with compiler errors
     - Read the first error: it names the file and the line. If you did not change that file, run ``git status`` in the repository. If the lines do not tell you what to do, send them to me before class.
   * - ``live8: command not found``
     - In that terminal, from the repository's top folder, type ``source project/week8/week8.sh`` first.
   * - ``702run: command not found``
     - Type ``enpm702`` first, or use ``live8``.

Lecture 9 has its own script, ``project/week9/week9.sh``: :doc:`Setup Before Class </lectures/lecture9/l9_setup>` of Lecture 9.
