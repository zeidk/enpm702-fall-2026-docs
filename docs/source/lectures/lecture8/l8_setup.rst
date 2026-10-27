.. _l8_setup:

====================================================
Setup Before Class
====================================================

In Lecture 8 you write code with me during class, and you upload it on Canvas before the end of class. Class time is for writing code, so get your workspace ready **before class**.

.. important::

   The code you upload at the end of class is graded.

   - **What you upload:** ``vehicle.hpp``, ``vehicle.cpp`` and ``main.cpp``, from ``project/week8/live``, to the L8 Live Coding assignment on Canvas, before the end of class.
   - **How it is graded:** complete or incomplete, as part of Participation (5% of the grade). Complete means that the code builds and that your **Step 2** block, the step you write on your own, is written.
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

1. Download the script: :download:`enpm702_setup.sh <enpm702_setup.sh>`.

2. Run it. It does not change any file in the repository: it only compiles and runs the live coding program, ``week8_live``.

   .. code-block:: bash

      bash ~/Downloads/enpm702_setup.sh

   The script looks for the repository in ``~/enpm702_cpp/enpm702-fall-2026-cpp``. If you cloned it somewhere else, open ``enpm702_setup.sh`` in VS Code and change **line 18**, between the quotes, to the folder where you cloned it. For example, for a clone in ``~/courses``:

   .. code-block:: bash

      ENPM702_LIVE_WS="$HOME/courses/enpm702-fall-2026-cpp"

   Save the file, then run the script again.

3. Read the output. Each line says ``ok`` or ``FIX``. When all is well, it looks like this:

   .. code-block:: text

      ENPM702: compile and run week8_live
        ok    repository at /home/you/enpm702_cpp/enpm702-fall-2026-cpp
        ok    configured
        ok    built week8_live
        ok    ran week8_live

      Ready for class. In class, type these two lines once in your terminal:
          source /home/you/Downloads/enpm702_setup.sh
          live8
      and type live8 again after each step.

In Class: ``live8``
-------------------

In class, load the script into your terminal once, with ``source`` instead of ``bash``:

.. code-block:: bash

   source ~/Downloads/enpm702_setup.sh

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
     - Clone the repository (Step 1), or change line 18 of the script to the folder where you cloned it.
   * - cmake could not configure the repository
     - Install the tools (Step 1). If ``cmake`` is installed, read the lines printed under the ``FIX`` line.
   * - ``week8_live`` did not build, with ``No rule to make target 'week8_live'``
     - Pull the latest code, and enable week 8 in ``CMakeLists.txt`` (Step 1).
   * - ``week8_live`` did not build, or did not compile, with compiler errors
     - Read the first error: it names the file and the line. If you did not change that file, run ``git status`` in the repository. If the lines do not tell you what to do, send them to me before class.
   * - ``live8: command not found``
     - Type ``source ~/Downloads/enpm702_setup.sh`` in that terminal first.
   * - ``702run: command not found``
     - Type ``enpm702`` first, or use ``live8``.

Lecture 9 uses the same script with the week number: ``bash ~/Downloads/enpm702_setup.sh 9`` before class, and ``live9`` in class.
