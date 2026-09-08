====================================================
Git/Github Exercises
====================================================


.. note::

   **Not graded, and not submitted on Canvas.** These exercises belong to
   a self-study reading module: work them at your own pace. Only the
   assignments listed on Canvas are collected.

.. dropdown:: Exercise 1: Git Basics
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice the fundamental Git workflow: initialize a repository, add
   files, and make commits.

   1. Create a new directory called ``robot-project`` and initialize a
      Git repository inside it.
   2. Create a file called ``robot_config.yaml`` with some content.
   3. Stage the file and make your first commit.
   4. Modify the file by adding a new line.
   5. Check the status, view the diff, stage, and commit again.
   6. View the commit log.

.. dropdown:: Exercise 2: Branching
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice creating branches and switching between them.

   1. Starting from the repository created in Exercise 1, create a new
      branch called ``feature/sensor-config``.
   2. Switch to the new branch.
   3. Add a file called ``sensor_config.yaml`` with some sensor settings.
   4. Stage and commit the new file.
   5. Switch back to ``main`` and verify that ``sensor_config.yaml`` does
      not exist on ``main``.
   6. List all branches and view the log with ``--all --graph``.

.. dropdown:: Exercise 3: Merging
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice merging a feature branch into ``main``.

   1. Ensure you are on the ``main`` branch.
   2. Merge the ``feature/sensor-config`` branch into ``main``.
   3. Verify that ``sensor_config.yaml`` now exists on ``main``.
   4. View the log to see the merge.
   5. Delete the ``feature/sensor-config`` branch.

.. dropdown:: Exercise 4: Merge Conflict Resolution
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Intentionally create a merge conflict and resolve it.

   1. Create a new branch called ``feature/speed-update`` and switch to
      it.
   2. In ``robot_config.yaml``, change the ``max_speed`` value to
      ``3.0``. Stage and commit.
   3. Switch back to ``main``.
   4. On ``main``, change the ``max_speed`` value to ``1.5``. Stage and
      commit.
   5. Attempt to merge ``feature/speed-update`` into ``main``. This
      should produce a conflict.
   6. Open ``robot_config.yaml``, resolve the conflict by choosing an
      appropriate value, and remove all conflict markers.
   7. Stage the resolved file and complete the merge with a commit.

.. dropdown:: Exercise 5: GitHub Remote
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice pushing to a remote repository and cloning.

   1. Create an empty repository on GitHub called ``robot-project``
      (do not add a README, .gitignore, or license).
   2. Add the GitHub repository as a remote named ``origin``.
   3. Push your local ``main`` branch to GitHub.
   4. Verify the push by checking GitHub in your browser.
   5. In a separate directory, clone the repository.
   6. In the cloned repo, make a change, commit, and push.
   7. In the original repo, pull the latest changes.

.. dropdown:: Exercise 6 Challenge: Fork Workflow
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   Practice the complete fork workflow used in open source and in this
   course.

   1. Fork a classmate's repository (or use a public test repository)
      on GitHub.
   2. Clone **your fork** to your local machine.
   3. Add the original repository as an ``upstream`` remote.
   4. Create a feature branch called ``feature/add-readme-section``.
   5. Make changes (e.g., add a section to the README).
   6. Commit and push the feature branch to **your fork** (``origin``).
   7. On GitHub, create a Pull Request from your fork's feature branch
      to the original repository's ``main`` branch.
   8. After the PR is merged (or for practice), sync your fork:

      - Fetch from ``upstream``.
      - Merge ``upstream/main`` into your local ``main``.
      - Push the updated ``main`` to your fork.
