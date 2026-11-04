.. _l9_setup:

====================================================
Setup Before Class
====================================================

In Lecture 9 we review the given steps of the Live Coding together, you write Steps 4, 5 and 6 in class, on your own, and you upload the code on Canvas before the end of class. Class time is for writing code, so get your workspace ready **before class**. Lecture 9 uses only the ``live`` folder, ``project/week9/live``.

.. important::

   The code you upload at the end of class is graded.

   - **What you upload:** after Step 6, zip the ``live`` folder: in ``project/week9``, run ``zip -r live.zip live`` (if ``zip`` is missing: ``sudo apt install zip``). Upload ``live.zip`` to the L9 Live Coding assignment on Canvas, before the end of class.
   - **How it is graded:** as the L9 exercise (exercises are 5% of the grade), as complete or incomplete. Complete means the code builds and you wrote Steps 4, 5 and 6. It is not graded for correctness.
   - **No AI:** you write the code yourself. No chatbot, and no AI in VS Code (GitHub Copilot or any other AI extension): turn it off before class. Code written with AI gets **0**.
   - **Watching the recording?** Upload before the next lecture, on **Nov 10**. The same rules apply.

Step 1: Get Your Workspace Ready
--------------------------------

Do these yourself, before class. The script in Step 2 does none of them.

1. **The tools.** On Ubuntu, install ``g++``, ``cmake`` and ``git`` if you have not yet:

   .. code-block:: bash

      sudo apt install build-essential cmake git

2. **The course C++ repository.** Clone it if you have not yet. The default place is ``~/enpm702_cpp/enpm702-fall-2026-cpp``:

   .. code-block:: bash

      git clone https://github.com/zeidk/enpm702-fall-2026-cpp.git ~/enpm702_cpp/enpm702-fall-2026-cpp

3. **The latest code.** Pull it, so that you have the ``project/week9/live`` folder:

   .. code-block:: bash

      cd ~/enpm702_cpp/enpm702-fall-2026-cpp
      git pull

4. **The 702 commands.** Your terminal must load ``enpm702-cpp.sh``, as the setup notes at the top of that file say. If you set this up for Lecture 8, skip this item. Otherwise, add this line once to ``~/.bashrc`` (or ``~/.zshrc`` if you use zsh), then open a new terminal:

   .. code-block:: bash

      source ~/enpm702_cpp/enpm702-fall-2026-cpp/enpm702-cpp.sh

5. **Week 9 enabled.** In the repository's ``CMakeLists.txt``, the line ``add_subdirectory(project/week9)`` must not start with ``#``.

Step 2: Compile and Run, Once
-----------------------------

1. Go to the repository's top folder. The script is in it, in ``project/enpm702_setup.sh``, since the pull of Step 1. If your clone is somewhere else, use that folder:

   .. code-block:: bash

      cd ~/enpm702_cpp/enpm702-fall-2026-cpp

2. Run it. It does not change any file in the repository: it only compiles and runs the live coding programs of Lectures 8 and 9, ``week8_live`` and ``week9_live``. To check only Lecture 9, add the week number: ``bash project/enpm702_setup.sh 9``.

   .. code-block:: bash

      bash project/enpm702_setup.sh

   The script finds the repository from its own place in ``project/``, so it works wherever you cloned it.

3. Read the output. Each check has a green ✔ when it passed, or a red ✘ and the lines to fix (``ok`` and ``FIX`` when the output is not a terminal). When all is well, it looks like this:

   .. code-block:: text

        ╭──────────────────────────────────────────────╮
        │  ENPM702 · Setup check                       │
        ╰──────────────────────────────────────────────╯

        Repository  ~/enpm702_cpp/enpm702-fall-2026-cpp
          ✔ repository found

        week8_live
          ✔ built week8_live (1 s)
          ✔ ran week8_live

        week9_live
          ✔ built week9_live (3 s)
          ✔ ran week9_live

        ✔ Ready for class.

        In class, type this once in your terminal, from the repository's top folder:
            source project/enpm702_setup.sh
        Then, after each step:
            live8            Lecture 8
            live9            Lecture 9

   The times are those of a first build on the instructor's PC; yours depend on your computer.

In Class: ``live9``
-------------------

In class, load the script into your terminal once, from the repository's top folder, with ``source`` instead of ``bash``:

.. code-block:: bash

   source project/enpm702_setup.sh

This gives the terminal the command ``live9``. After each step, save your files and type:

.. code-block:: bash

   live9

``live9`` builds ``week9_live``. If the code compiles, it runs the program and shows what it prints. If it does not compile, it shows the compiler's errors: fix the first one, save, and type ``live9`` again. Each block in ``main.cpp`` prints ``[Step N]`` and what that step adds; the block of a step you have not reached yet stays commented out.

``live9`` exists only in the terminal where you typed ``source``. In a new terminal, type the ``source`` line again. The ``702build week9_live`` and ``702run week9_live`` commands do the same two things, if your terminal loads ``enpm702-cpp.sh`` and you typed ``enpm702``.

Common Fixes
------------

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - The message says
     - What to do
   * - no ENPM702 repository
     - Clone the repository (Step 1), and keep the script in its ``project/`` folder.
   * - ``No such file or directory``, for ``project/enpm702_setup.sh``
     - Pull the latest code (Step 1), then run the command from the repository's top folder.
   * - cmake could not configure the repository
     - Install the tools (Step 1). If ``cmake`` is installed, read the lines printed under the ``FIX`` line.
   * - ``week9_live`` did not build, with ``No rule to make target 'week9_live'``
     - Pull the latest code, and enable week 9 in ``CMakeLists.txt`` (Step 1). Then configure again, so that CMake sees the change: ``702configure``, or ``cmake -S . -B build`` in the repository.
   * - ``week9_live`` did not build, or did not compile, with compiler errors
     - Read the first error: it names the file and the line. If you did not change that file, run ``git status`` in the repository. If the lines do not tell you what to do, send them to me before class.
   * - ``live9: command not found``
     - In that terminal, from the repository's top folder, type ``source project/enpm702_setup.sh`` first.
   * - ``702run: command not found``
     - Type ``enpm702`` first, or use ``live9``.
