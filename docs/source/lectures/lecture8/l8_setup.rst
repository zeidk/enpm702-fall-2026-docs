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

What You Need
-------------

- Ubuntu, with ``g++``, ``cmake`` and ``git``. The script below tells you if one is missing, and how to install it.
- The course C++ repository, cloned on your machine. The default place is ``~/enpm702_cpp/enpm702-fall-2026-cpp``. If you have not cloned it yet:

  .. code-block:: bash

     git clone https://github.com/zeidk/enpm702-fall-2026-cpp.git ~/enpm702_cpp/enpm702-fall-2026-cpp

Run the Setup Script
--------------------

1. Download the script: :download:`enpm702_setup.sh <enpm702_setup.sh>`.

2. Run it from the folder where you saved it. It does not change any code you wrote.

   .. code-block:: bash

      bash ~/Downloads/enpm702_setup.sh

   If your repository is not in the default place, tell the script where it is:

   .. code-block:: bash

      ENPM702_WS=~/somewhere/enpm702-fall-2026-cpp bash ~/Downloads/enpm702_setup.sh

3. Read the output. The script checks seven things, in order: the tools, the repository, the latest code (a ``git pull`` that never overwrites your own changes), that your terminal loads ``enpm702-cpp.sh``, that week 8 is enabled, that the ``live`` folder is there, and that ``week8_live`` builds and runs. Each line says ``ok`` or ``FIX``. A ``FIX`` line says what to do. Fix it, then run the script again, until it ends with ``Ready``:

   .. code-block:: text

      ENPM702 setup for the week 8 live coding
        ok    g++ is installed
        ok    cmake is installed
        ok    git is installed
        ok    repository at /home/you/enpm702_cpp/enpm702-fall-2026-cpp
        ok    repository is up to date
        ok    /home/you/.bashrc loads enpm702-cpp.sh
        ok    week 8 is enabled in CMakeLists.txt
        ok    project/week8/live is there
        ok    configured (the same as 702configure)
        ok    built week8_live (the same as 702build week8_live)
        ok    ran week8_live (the same as 702run week8_live)

      Ready. In class, open a new terminal and type:
          enpm702
          702build week8_live
          702run week8_live

   Your paths and the list of enabled weeks will differ.

4. Open a **new** terminal, so that it loads the latest ``enpm702-cpp.sh``, and type the three commands the script printed. ``702run week8_live`` prints nothing yet: each block in ``main.cpp`` stays commented out until we reach its step in class.

Common Fixes
------------

.. list-table::
   :header-rows: 1
   :widths: 40 60
   :class: compact-table

   * - The ``FIX`` line says
     - What to do
   * - ``g++``, ``cmake`` or ``git`` is missing
     - Run the ``sudo apt install`` command it prints.
   * - no ENPM702 repository
     - Clone the repository (above), or set ``ENPM702_WS`` to where you cloned it.
   * - git pull did not finish
     - You changed a file that the pull also changes. Run ``git -C ~/enpm702_cpp/enpm702-fall-2026-cpp status`` to see which one. Copy your version somewhere safe, run ``git -C ~/enpm702_cpp/enpm702-fall-2026-cpp restore <file>``, then run the script again.
   * - ``.bashrc`` (or ``.zshrc``) does not load ``enpm702-cpp.sh``
     - Run the ``echo 'source ...' >> ...`` line it prints, **once**.
   * - week 8 is not enabled
     - In the repository's ``CMakeLists.txt``, remove the ``#`` before ``add_subdirectory(project/week8)``.
   * - ``week8_live`` did not build or run
     - Read the lines it prints under the ``FIX`` line. If they do not tell you what to do, send them to me before class.

Lecture 9 uses the same script, with the week number: ``bash ~/Downloads/enpm702_setup.sh 9``.
