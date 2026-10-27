.. _l8_setup:

====================================================
Setup Before Class
====================================================

In Lecture 8 you write code with me during class, and you upload it on Canvas before the end of class. Class time is for writing code, so get your workspace ready **before class**.

.. important::

   The code you upload at the end of class is graded.

   - **What you upload:** ``vehicle.hpp``, ``vehicle.cpp`` and ``main.cpp``, from ``project/week8/live``, to the L8 Live Coding assignment on Canvas, before the end of class.
   - **How it is graded:** complete or incomplete, as part of Participation (5% of the grade). Complete means that the code builds and that the **Your turn** block, the one you write on your own, is written.
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

Step 2: Compile and Run
-----------------------

1. Download the script: :download:`enpm702_setup.sh <enpm702_setup.sh>`.

2. Run it. It does not change any file in the repository: it only compiles and runs the live coding program, ``week8_live``.

   .. code-block:: bash

      bash ~/Downloads/enpm702_setup.sh

   The script looks for the repository in ``~/enpm702_cpp/enpm702-fall-2026-cpp``. If you cloned it somewhere else, open ``enpm702_setup.sh`` in VS Code and change **line 24**, between the quotes, to the folder where you cloned it. For example, for a clone in ``~/courses``:

   .. code-block:: bash

      ws="$HOME/courses/enpm702-fall-2026-cpp"

   Save the file, then run the script again.

3. Read the output. Each line says ``ok`` or ``FIX``. When all is well, it looks like this:

   .. code-block:: text

      ENPM702: compile and run week8_live
        ok    repository at /home/you/enpm702_cpp/enpm702-fall-2026-cpp
        ok    configured (the same as 702configure)
        ok    built week8_live (the same as 702build week8_live)
        ok    ran week8_live (the same as 702run week8_live)

      Ready for class.

   ``week8_live`` prints nothing yet: each block in ``main.cpp`` stays commented out until we reach its step in class.

Common Fixes
------------

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - The ``FIX`` line says
     - What to do
   * - no ENPM702 repository
     - Clone the repository (Step 1), or change line 24 of the script to the folder where you cloned it.
   * - cmake could not configure the repository
     - Install the tools (Step 1). If ``cmake`` is installed, read the lines printed under the ``FIX`` line.
   * - ``week8_live`` did not build, with ``No rule to make target 'week8_live'``
     - Pull the latest code, and enable week 8 in ``CMakeLists.txt`` (Step 1).
   * - ``week8_live`` did not build, with compiler errors
     - Run ``git status`` in the repository: a file you changed under ``project/week8`` may not compile. If the lines do not tell you what to do, send them to me before class.
   * - ``week8_live`` did not run
     - Read the lines printed under the ``FIX`` line, and send them to me before class.

Lecture 9 uses the same script, with the week number: ``bash ~/Downloads/enpm702_setup.sh 9``.
