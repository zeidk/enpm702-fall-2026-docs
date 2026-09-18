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

   1. Fork the course demo repository on GitHub (your instructor will
      give you the link). Do **not** fork a classmate's assignment
      repository: RWA repositories are private and individual work.
   2. Clone **your fork** to your local machine.
   3. Add the original repository as an ``upstream`` remote.
   4. Create a feature branch called ``feature/add-<your-username>``.
   5. Copy ``contributors/TEMPLATE.md`` to
      ``contributors/<your-github-username>.md`` and fill it in.

      Add a **new file** rather than editing an existing one. If thirty
      people all append to the same ``README.md``, the first pull
      request merges and every later one conflicts. One file each and
      they all merge cleanly, in any order.
   6. Commit and push the feature branch to **your fork** (``origin``).
   7. On GitHub, create a Pull Request from your fork's feature branch
      to the original repository's ``main`` branch.
   8. After the PR is merged (or for practice), sync your fork:

      - Fetch from ``upstream``.
      - Merge ``upstream/main`` into your local ``main``.
      - Push the updated ``main`` to your fork.

.. dropdown:: Exercise 7: Undoing Uncommitted Work
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice the two ``restore`` commands until the difference is
   automatic.

   1. In ``robot-project``, edit ``robot_config.yaml`` and save.
   2. Run ``git status`` and ``git diff``. Then discard the edit and
      confirm the file is back to its committed state.
   3. Edit the file again and stage it with ``git add``.
   4. Run ``git status``. Unstage it **without losing the edit**, then
      confirm with ``git status`` and ``git diff`` that the edit is
      still there.
   5. Now discard it for good.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # 2. discard an unstaged edit
         git diff
         git restore robot_config.yaml

         # 4. unstage, keep the edit on disk
         git restore --staged robot_config.yaml
         git status          # "Changes not staged for commit"
         git diff            # the edit is still there

         # 5. discard it
         git restore robot_config.yaml

      ``git restore --staged`` moves a change from the staging area back
      to the working directory. ``git restore`` throws it away. The
      second one cannot be undone, so check ``git diff`` first.

.. dropdown:: Exercise 8: Fixing and Undoing Commits
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Practice the difference between rewriting a commit and reversing it.

   1. Make a change and commit it with the deliberately bad message
      ``"stuff"``. Do not push.
   2. Reword that message to something descriptive, without creating a
      second commit. Check with ``git log --oneline``.
   3. Create a file ``notes.md``, then realize it belonged in the
      previous commit. Fold it into that commit, keeping the message.
   4. Push to GitHub.
   5. Now commit a change that sets ``max_speed`` to ``15.0``, and push
      that too.
   6. Undo the change from step 5 in the way that is safe on a pushed
      branch, then push again.
   7. Look at ``git log --oneline``. How many commits mention the bad
      value?

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # 2. reword the last commit
         git commit --amend -m "Add obstacle margin to the configuration"

         # 3. fold a forgotten file into the last commit
         git add notes.md
         git commit --amend --no-edit

         # 6. undo a pushed commit
         git log --oneline            # copy the bad commit's hash
         git revert <hash>
         git push

      Step 7: **two**. The bad commit and the commit that undoes it are
      both in the history, which is exactly what you want. ``revert``
      adds; it never removes. Rewriting the pushed commit with
      ``--amend`` or ``reset`` would have broken every clone that
      already had it.

.. dropdown:: Exercise 9: Stashing an Interruption
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Reproduce the interruption from the lecture.

   1. Create a branch ``feature/waypoints`` and commit a small change to
      ``robot_config.yaml`` on it.
   2. Switch to ``main`` and commit a **different** change to the same
      file. Switch back to ``feature/waypoints``.
   3. Start another edit on ``feature/waypoints`` but do not commit it.
   4. Try ``git switch main``. Read the error.
   5. Park the unfinished edit with a descriptive message, then switch,
      make a one-line fix on ``main``, and commit it.
   6. Return to ``feature/waypoints`` and restore your parked edit.
   7. Confirm the parking area is empty.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git stash push -m "half-done waypoint block"
         git switch main
         # fix, add, commit
         git switch feature/waypoints
         git stash pop
         git stash list        # prints nothing

      Step 4 fails only because ``robot_config.yaml`` differs between
      the two branches **and** you have modified it. If the file were
      identical on both branches, Git would carry your edit across
      without complaining. That inconsistency is why "commit or stash
      before switching" is the reliable habit.

.. dropdown:: Exercise 10: Losing and Recovering a Branch
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   The one to practice **before** you need it.

   1. Create a branch ``feature/battery``, add a file, and make two
      commits on it.
   2. Switch to ``main`` and delete the branch with ``git branch -D
      feature/battery``. Note that ``-D`` forces the delete even though
      the branch was never merged.
   3. Confirm the damage: ``git branch``, then ``git log --oneline
      --all``. The commits are nowhere to be seen.
   4. Find them again and put the branch back.
   5. Verify your file is present.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git reflog
         # find the line: "commit: <your second commit message>"
         # copy the hash at the start of that line

         git branch feature/battery <hash>
         git switch feature/battery
         ls

      A branch name is only a pointer to a commit. Deleting the name
      does not delete the commits; it just leaves nothing pointing at
      them. ``git reflog`` lists every position ``HEAD`` has held, so the
      hash is still there to be read off.

      Unreachable commits are eventually cleaned up (30 days by
      default), and the reflog is local to your clone. It is a safety
      net, not a backup.

.. dropdown:: Exercise 11: A Diverged Branch
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   Needs a partner, or a second clone of your own repository in another
   directory.

   1. From clone A, commit a change to ``README.md`` and push.
   2. From clone B (which has not pulled), commit a **different** change
      to ``robot_config.yaml``.
   3. From clone B, run ``git push``. Read the rejection.
   4. Without merging anything yet, work out what each side has:
      ``git fetch``, then list the commits in each direction.
   5. Bring the histories together and push successfully.
   6. Look at the shape with ``git log --oneline --graph --all``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         # 4. look before you leap
         git fetch origin
         git log --oneline main..origin/main    # theirs, not mine
         git log --oneline origin/main..main    # mine, not theirs

         # 5. merge, then push
         git pull
         git push

      If ``git pull`` stops with *"You have divergent branches and need
      to specify how to reconcile them"*, Git is asking which shape you
      want. Set the course default once:

      .. code-block:: bash

         git config --global pull.rebase false

      The two changes touched different files, so the merge is
      automatic. Had they touched the same lines, you would resolve the
      conflict exactly as in Exercise 4.

.. dropdown:: Exercise 12: Tagging a Submission
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   1. Tag the current commit of ``robot-project`` as ``v1.0`` with an
      annotated tag and a message.
   2. Push the tag and find it on GitHub under **Releases** or
      **Tags**.
   3. Make another commit and push it.
   4. Check that ``v1.0`` still points at the older commit, not the new
      one.
   5. Tag that older commit again as ``v0.9`` using its hash.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git tag -a v1.0 -m "First working configuration"
         git push origin v1.0

         # 4. the tag has not moved
         git show v1.0 | head -5
         git log --oneline --decorate -3

         # 5. tag an older commit by hash
         git tag -a v0.9 -m "Before the waypoint work" <hash>
         git push origin v0.9

      A branch pointer follows you forward as you commit. A tag stays
      where it was put. That is what makes a tag usable as "the version
      I submitted".


Live Workshop: The Broken Repository
----------------------------------------------------

The exercises above all start from a clean slate. Real Git problems do
not. These drills drop you into a repository that is **already** in a
mess, and ask you to get it out.

.. admonition:: Why a script instead of a repository to clone
   :class: note

   You cannot clone a broken state. A clone always gives you a clean
   checkout of a branch, so a half-finished merge, a detached ``HEAD``,
   or a dirty working tree cannot travel that way. The script builds the
   mess on your machine instead.

   It also builds a local stand-in for GitHub, so ``push``, ``pull``,
   and ``fetch`` behave exactly as they would against a real remote. No
   account and no network connection are needed.

**Setup:**

.. code-block:: bash

   # Download git-workshop.sh (link below), then:
   chmod +x git-workshop.sh

   ./git-workshop.sh list     # show the seven scenarios
   ./git-workshop.sh 4        # build the sandbox in scenario 4
   ./git-workshop.sh clean    # delete the sandbox when you are done

:download:`git-workshop.sh </_static/files/git-workshop.sh>`

The sandbox lives in ``~/git-workshop`` and is **wiped and rebuilt every
time you run a scenario**. Nothing you do there can touch your real
repositories, and you can restart a scenario as often as you like. Break
things on purpose.

.. warning::

   Read the printed briefing before typing anything. Every one of these
   is solvable with a command covered in the lecture. Identify *where*
   the problem is first (working directory, staging area, repository,
   remote), and the command follows.

.. dropdown:: Scenario 1: Detached HEAD
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 1``

   You went back to inspect an older commit, started tinkering, and
   committed. That commit belongs to no branch. Get it onto
   ``fix/obstacle-margin`` and merge it into ``main``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git status                       # "HEAD detached at ..."
         git switch -c fix/obstacle-margin   # create a branch right here
         git switch main
         git merge fix/obstacle-margin

      A branch is a pointer to a commit. Detached ``HEAD`` means ``HEAD``
      points straight at a commit instead of at a branch name, so nothing
      follows you forward as you commit. Creating a branch where you
      stand attaches a name to the work, and it is safe again.

      Had you switched away first, ``git reflog`` would still have found
      the commit.

.. dropdown:: Scenario 2: A merge stopped halfway
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 2``

   Both branches changed ``navigation.update_rate``. Finish the merge.
   Then run the scenario again and take the other exit: back out
   completely.

   .. dropdown:: Solution
      :class-container: sd-border-success

      Finishing:

      .. code-block:: bash

         git status                       # "You have unmerged paths"
         # edit robot_config.yaml: pick a value, delete <<<<<<< ======= >>>>>>>
         git add robot_config.yaml
         git commit                       # Git pre-fills a merge message

      Backing out:

      .. code-block:: bash

         git merge --abort

      ``git merge --abort`` restores the repository exactly as it was
      before the merge started. Knowing it exists is what stops a
      conflict from being frightening: you can always put it back and
      think again.

.. dropdown:: Scenario 3: A bad commit is already pushed
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 3``

   ``max_speed`` was set to 15.0 m/s and pushed. Undo it safely.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git log --oneline
         git show <hash>          # confirm before you act
         git revert <hash>
         git push

      Why not ``git reset --hard HEAD~1``? It would make **your** copy
      correct by deleting the commit. Everyone who already pulled still
      has it, your next push is rejected as diverged, and forcing it
      through deletes their work too. ``revert`` adds a new commit that
      reverses the change, so every clone converges without anyone doing
      anything.

.. dropdown:: Scenario 4: You deleted a branch you needed
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 4``

   Two afternoons of battery-monitor work were on a branch you just
   deleted. Get them back.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git reflog
         # find "commit: Enable the battery monitor in the robot configuration"
         git branch feature/battery-monitor <hash>
         git switch feature/battery-monitor
         ls src/                  # battery.cpp is back

      The commits were never deleted. Deleting a branch removes a
      *name*, leaving the commits unreachable but still present.
      ``git reflog`` lists every position ``HEAD`` has held, so the hash
      is recoverable for as long as the reflog keeps it (30 days by
      default).

.. dropdown:: Scenario 5: Junk staged, secrets committed
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 5``

   Build output and object files are staged. Worse, a file with a wifi
   password and an API token was committed and pushed one commit ago.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git status
         git restore --staged .           # unstage everything, keep the files

         # write a .gitignore covering build/, *.o, *.log, robot_secrets.yaml
         git add .gitignore
         git commit -m "Add .gitignore for build output and secrets"

         git rm --cached robot_secrets.yaml
         git commit -m "Stop tracking robot_secrets.yaml"
         git push

      The password is **still in the repository**, in the commit that
      added it:

      .. code-block:: bash

         git log --oneline -S "Terrapins2026"   # finds the commit
         git show <hash>                        # prints the password

      ``git rm --cached`` removes a file from the *latest* commit. It
      cannot remove it from history. Anyone with a clone, including
      anyone who cloned before you noticed, can read it.

      The real fix is to **rotate the credential**: change the wifi
      password and revoke the API token. Do that first, and immediately.
      Scrubbing history afterwards (``git filter-repo``) rewrites every
      commit hash and breaks every clone, and it still does not
      un-leak a secret that was public for an hour.

.. dropdown:: Scenario 6: Unfinished work blocks a switch
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 6``

   Half-finished edits on ``feature/waypoints``, and an urgent fix needed
   on ``main``.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git switch main                  # refused: local changes would be lost
         git stash push -m "half-done waypoints"
         git switch main
         # change obstacle_margin to 0.45
         git add robot_config.yaml
         git commit -m "Widen the obstacle margin to 0.45 m"
         git switch feature/waypoints
         git stash pop
         git stash list                   # empty

      The follow-up question: for a three-day interruption, commit the
      work on its branch instead. A commit has a message, a branch, and
      a place in the history. A stash has none of those, and three
      unlabeled stashes from last week are indistinguishable.

.. dropdown:: Scenario 7: Your push is rejected
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   ``./git-workshop.sh 7``

   A teammate pushed while you were working. Get your commit onto the
   remote.

   .. dropdown:: Solution
      :class-container: sd-border-success

      .. code-block:: bash

         git push                                 # "! [rejected] ... (fetch first)"

         git fetch origin
         git log --oneline main..origin/main      # theirs, not mine
         git log --oneline origin/main..main      # mine, not theirs

         git pull                                 # merge their work into mine
         git push
         git log --oneline --graph --all

      If ``git pull`` stops with *"You have divergent branches"*, Git is
      asking which shape you want. ``git config --global pull.rebase
      false`` picks merging, the course default.

      The second time through, use ``git pull --rebase`` instead. Your
      commit is replayed on top of theirs and the history is a straight
      line, with no merge commit. The trade-off: your commit gets a new
      hash. That is harmless here, because nobody else had it yet. It
      would not be harmless on a branch a teammate had already pulled,
      which is the golden rule of rebasing.

.. admonition:: One more habit
   :class: tip

   None of these scenarios needed a command you have not already seen.
   What they needed was a diagnosis. Before reaching for anything, run
   ``git status`` and read it properly: Git tells you what state it is
   in and usually names the command that gets you out.
