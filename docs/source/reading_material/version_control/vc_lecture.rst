Lecture
====================================================

Introduction
----------------------------------------------------


Version control is a system that tracks changes to files over time,
allowing you to:

- **Track History**: See exactly what changed, when, and who made the
  change.
- **Revert Changes**: Go back to any previous version of your files.
- **Branch and Merge**: Work on different features simultaneously
  without conflicts.
- **Collaborate**: Multiple people can work on the same project without
  overwriting each other's work.
- **Backup**: Distributed copies serve as automatic backups.


Why Version Control
----------------------------------------------------


A typical project directory without version control might look like
this:

::

   my_project/
       final_version.doc
       final_version_v2.doc
       final_version_REALLY_FINAL.doc
       final_version_REALLY_FINAL_fixed.doc
       final_version_REALLY_FINAL_fixed_john_edits.doc

**With version control**, the same project looks like this:

::

   my_project/
       document.doc
       .git/        (tracks all versions automatically)

- ``document.doc`` has complete history.
- ``.git/`` tracks all versions automatically.


Types of Version Control Systems
----------------------------------------------------


1. **Local Version Control:**

   - Copies files to different directories.
   - Simple but error-prone.
   - *Example*: RCS (Revision Control System)

2. **Centralized Version Control:**

   - Single server contains all versions.
   - Clients check out files from central place.
   - *Examples*: CVS, Subversion (SVN), Perforce.

3. **Distributed Version Control:**

   - Every client has complete repository copy.
   - No single point of failure.
   - *Examples*: Git, Mercurial, Bazaar.


Centralized Version Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. figure:: /_static/images/version_control/centralized.png
   :align: center
   :width: 80%

   Centralized version control architecture.

- **Single source of truth**: Central server has master repository.
- **Client-server model**: Developers have working copies only.
- **Network dependent**: Most operations require server connection.

**Typical Workflow:**

.. code-block:: bash

   # SVN Example
   svn checkout https://server.com/repo/trunk # Get working copy
   svn update                                 # Get latest changes
   # Make changes...
   svn commit -m "My changes"                 # Save to server
   svn log                                    # View history (needs network)

.. grid:: 2

   .. grid-item-card:: Advantages

      - Simple mental model, one central authority
      - Fine-grained access control
      - Storage efficient for clients
      - Easy administration and compliance

   .. grid-item-card:: Disadvantages

      - Single point of failure
      - Network required for most operations
      - Limited offline capabilities
      - Expensive branching operations


Distributed Version Control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. figure:: /_static/images/version_control/distributed.png
   :align: center
   :width: 80%

   Distributed version control architecture.

- **Complete local repositories**: Full history everywhere.
- **Peer-to-peer model**: Repositories sync with any other.
- **Offline capable**: All operations work without network.

**Typical Workflow:**

.. code-block:: bash

   # Git Example
   git clone https://github.com/user/project.git   # Get complete repo
   git log                                         # View history (offline)
   git branch feature                              # Create branch (instant)
   git switch feature                            # Switch branch (instant)
   # Make changes...
   git commit -m "My changes"                      # Save locally
   git push origin feature                         # Share when ready

.. grid:: 2

   .. grid-item-card:: Advantages

      - No single point of failure
      - Fast local operations
      - Excellent offline capabilities
      - Flexible workflows
      - Cheap branching and merging

   .. grid-item-card:: Disadvantages

      - Steeper learning curve
      - More complex concepts
      - Larger local storage requirements
      - Less granular access control

The last two are expanded below. Both recur later in this module.

.. dropdown:: Why "larger local storage requirements"?
   :class-container: sd-border-info

   ``git clone`` copies **every version of every file ever committed**,
   not just the one you checked out. That is what lets ``git log``,
   ``git diff`` and ``git switch`` work with no network. An ``svn
   checkout`` gives you one revision, plus a pristine copy of it for
   offline diffs, so roughly twice that one revision.

   **In practice this is usually a non-issue.** Git compresses every
   object, and packs similar objects as **deltas**, storing only the
   differences. Source code is text, and two versions of a text file
   differ by a few lines, so the deltas are tiny.

   Measured in September 2026 on the repositories behind this course,
   comparing the full history against the files in their latest version.
   The commit counts are part of the measurement, so the figures stay
   readable as the repositories grow:

   .. list-table::
      :widths: 40 15 15 15 15
      :header-rows: 1
      :class: compact-table

      * - Repository
        - Commits
        - ``.git``
        - Checkout
        - Ratio
      * - Course C++ code
        - 17
        - 0.4 MB
        - 1.2 MB
        - **0.34x**
      * - These docs
        - 51
        - 104 MB
        - 78 MB
        - 1.34x
      * - Lecture slides (LaTeX)
        - 24
        - 61 MB
        - 39 MB
        - 1.58x

   In the first row, seventeen commits of complete history occupy
   **less space than a single checkout**. For plain source code the
   storage cost of full history is negligible.

   **Where it is real: binary files.** They do not delta-compress,
   because changing one pixel rewrites most of the compressed stream, so
   Git keeps a whole new copy of each version forever. Breaking the
   slides repository's history down by file type shows it plainly:

   .. code-block:: text

      pdf   42.1 MB
      png   19.5 MB
      otf   11.1 MB
      ttf    8.8 MB
      tex    2.6 MB     <- the only part anyone actually edits
      svg    0.9 MB

   Scale that up and it bites: a 50 MB bag file committed ten times is
   500 MB in ``.git``, in every clone, forever.

   .. important::

      **Deleting the file does not reclaim the space.** ``git rm``
      removes it from the latest commit; every earlier version is still
      in the history and still ships with every clone.

      This is the same mechanism as the committed password later in this
      module, and it is the real argument for ``.gitignore``. Build
      output can be regenerated, so every byte of it in history is
      permanent waste in every clone anyone ever makes. For genuinely
      large assets that must be versioned, the escape hatch is Git LFS,
      which keeps a small pointer in history and the bytes elsewhere.

.. dropdown:: Cloning only part of a repository
   :class-container: sd-border-info

   ``git clone`` has no option to fetch a single directory. Two separate
   features together get close, and they solve different halves of the
   problem:

   - ``--sparse`` controls **which paths** appear in the working tree.
     Used alone, it shrinks the checkout but ``.git`` still holds
     everything.
   - ``--filter=blob:none`` makes it a **partial clone**: file contents
     are downloaded only when something needs them. This is what shrinks
     ``.git``. It requires server support, which GitHub, GitLab and
     Bitbucket all provide.

   .. code-block:: bash

      git clone --filter=blob:none --sparse <url>
      cd <repo>
      git sparse-checkout set docs/source/reading_material/version_control

   Measured on this course's documentation repository:

   .. list-table::
      :widths: 46 27 27
      :header-rows: 1
      :class: compact-table

      * - Clone type
        - ``.git``
        - Working tree
      * - Normal clone
        - 102 MB
        - 79 MB
      * - ``--depth 1`` (shallow)
        - 58 MB
        - 79 MB
      * - ``--filter=blob:none --sparse``
        - **384 KB**
        - **204 KB**

   ``--depth 1`` is a third, independent axis: it reduces the number of
   **commits**, not the number of paths, so the working tree stays full
   size. In this repository it saves less than the other two, because
   the weight is images rather than history.

   Adjust or undo the path selection at any time:

   .. code-block:: bash

      git sparse-checkout list         # what is currently checked out
      git sparse-checkout add <path>   # add another directory
      git sparse-checkout disable      # restore the full working tree

   ``disable`` on a partial clone downloads every blob it had been
   skipping. In the repository above, ``.git`` grows from 384 KB back to
   58 MB and the working tree returns to 79 MB. Use ``add`` to widen the
   selection a directory at a time if that download is unwanted.

   .. important::

      This is a bandwidth and disk convenience, not access control. The
      repository is complete: ``git log`` still lists every commit,
      including commits touching files never checked out, and
      ``git sparse-checkout disable`` restores everything. It cannot be
      used to give somebody one directory and withhold the rest, for the
      reasons in the next dropdown.

   Two limitations to expect:

   - **Cone mode.** ``sparse-checkout set`` defaults to cone mode, which
     also materialises files sitting at each directory level along the
     path, such as ``README.md``, ``conf.py`` and ``docs/Makefile``.
     Builds usually need those. ``--no-cone`` takes exact patterns
     instead, but is slower and is being phased out.
   - **``git archive --remote`` does not work on GitHub.** That command
     fetches one directory as a tarball with no clone at all, and GitHub
     rejects it with ``fatal: operation not supported by protocol``. It
     works against some self-hosted servers. The older workaround,
     ``svn export`` on a GitHub URL, stopped working when GitHub retired
     Subversion support in January 2024.

   Use this for a large repository where only one subtree is needed, for
   example a robot or a CI runner that builds a single package. For the
   group projects it is unnecessary, since those repositories are small.
   The structural answer to "I only want this directory" is to split the
   work into separate repositories.

.. dropdown:: Why "less granular access control"?
   :class-container: sd-border-info

   The question is what unit a permission can be attached to.

   **Centralized: per path.** The server handles every operation, so it
   can decide per directory, per file, per user. An SVN rules file can
   say:

   .. code-block:: ini

      [repo:/trunk/docs]
      priya = rw
      [repo:/trunk/firmware]
      priya = r
      [repo:/trunk/contracts]
      priya =            # no access at all, not even visible

   Because ``svn checkout`` can fetch a single subdirectory, a
   contractor can be handed one folder of a large tree and never see the
   rest.

   **Git: per repository.** You get read, or write, or nothing. No Git
   command or setting says "this person may not read ``src/crypto/``".

   That is structural, not an oversight. A clone is the whole history,
   and a commit's hash covers the whole tree. Hide a subdirectory and
   the hashes stop verifying, so what you handed over is no longer a Git
   repository. Partial access and Git's integrity model are in direct
   conflict.

   GitHub and GitLab add controls on top, each with its own unit:

   .. list-table::
      :widths: 46 24 30
      :header-rows: 1
      :class: compact-table

      * - Control
        - Unit
        - Restricts a path?
      * - Roles (read, write, maintain, admin)
        - repository
        - No
      * - Branch protection rules
        - branch
        - No
      * - Required reviews
        - branch
        - No
      * - ``CODEOWNERS``
        - path
        - **Only routes reviews**

   ``CODEOWNERS`` is not path permissions. It specifies that changes
   under a path require review from named people. It does not restrict
   who may read the file, and without a matching branch rule it does not
   restrict who may commit to it.

   **So teams split the repository instead.** If ``firmware/`` needs
   different access from ``docs/``, those become two repositories. This
   is much of why Git projects tend towards many small repositories,
   where centralized shops keep one large tree with a permissions table.
   The access model ends up shaping the architecture.

   .. note::

      This lands on your group project directly. You cannot give a
      teammate write access to only their own package: everyone with
      write has write everywhere, including the shared line of
      development. That is exactly why :ref:`branch protection
      <vc-protect>` matters. It is the
      substitute Git offers for the path-level control it structurally
      cannot provide, trading a technical restriction for a process one.

      It also reinforces the rule about secrets from a second direction.
      Anyone who can clone gets everything, including every version in
      the history. There is no "only I can read that file" in Git, which
      is why the only real answer is to keep it out of the repository.


Git: Background
====================================================

.. note::

   This part is background. Nothing here needs to be typed. The
   hands-on work begins at :ref:`Installing and Configuring Git
   <vc-setup>`, and from that point on every section is either an
   explanation or the exercise that follows it.

Overview
----------------------------------------------------


Git is a version control system that tracks changes in your files over
time.

- Save snapshots of your project at different points.
- See what changed between versions.
- Collaborate with others without overwriting each other's work.
- Revert to previous versions if something breaks.


Why Git Dominates
----------------------------------------------------


.. grid:: 2

   .. grid-item-card:: Technical Advantages

      - **Speed**, Operations like commits and diffs execute in
        milliseconds.
      - **Distributed Nature**, Every developer has a complete copy of
        the project history.
      - **Branching Model**, Creating and merging branches is
        lightweight and fast.
      - **Data Integrity**, every commit is named by a checksum of its
        own contents, so corruption cannot pass unnoticed.

   .. grid-item-card:: Ecosystem Advantages

      - **GitHub Integration**, Seamless hosting with powerful
        collaboration features.
      - **Tool Support**, Every major IDE and editor has excellent Git
        integration.
      - **Industry Adoption**, Used by virtually all major tech
        companies and open source projects.


Git vs. GitHub
----------------------------------------------------


Git and GitHub are often confused, but they are **not** the same
thing.

.. grid:: 2

   .. grid-item-card:: Git
      :class-card: sd-border-info

      - A **tool** that runs on your computer.
      - Tracks changes to files.
      - Works **entirely offline**.
      - Free and open source.
      - Created by **Linus Torvalds** in 2005.
      - Example commands: ``git init``, ``git commit``, ``git branch``.

   .. grid-item-card:: GitHub
      :class-card: sd-border-info

      - A **website/service** that hosts Git repositories.
      - Adds collaboration features: pull requests, issues, project
        boards, CI/CD pipelines, wikis.
      - Requires an account and a network connection.
      - Founded in 2008, acquired by **Microsoft** in 2018.
      - Example actions: create a pull request, review code,
        open an issue.

You can use Git without ever using GitHub. The reverse is not true:
every repository on GitHub is a Git repository, and Git is the only
version control system GitHub speaks.

.. note::

   That has not always been true. Until **8 January 2024** GitHub also
   accepted Subversion clients, so you could ``svn checkout`` a GitHub
   repository. GitHub retired that bridge once SVN traffic fell below
   0.02% of requests. Today it is Git or nothing.

   One fair quibble: you can use GitHub without ever *running* Git. Edit
   a file in the browser, open a pull request, merge it, and GitHub
   makes the commits for you. The storage is still Git, but the person
   need not touch it.


How Git and GitHub Work Together
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


In a typical workflow, Git tracks changes locally on your machine
while GitHub stores a remote copy of the repository that your
teammates can also reach.

.. figure:: /_static/images/version_control/git-github.png
   :alt: Laptop running local Git connected to a GitHub cloud repository
   :align: center
   :width: 100%

   Local Git tracks changes on your machine; GitHub stores a remote
   copy. ``git push`` uploads commits; ``git clone``, ``git fetch``,
   and ``git pull`` bring commits down.

- **Push from local to GitHub:** ``git push`` uploads new commits
  from your local branch to the matching branch on GitHub.
- **Pull from GitHub to local:** ``git pull`` (or ``git fetch`` +
  ``git merge``) downloads new commits and merges them into your
  current branch.
- **Clone from GitHub to local:** ``git clone <url>`` copies the
  entire repository (history, branches, tags) to your machine.

.. note::

   When you create a pull request or review code in a browser, you
   are using **GitHub**. When you stage, commit, branch, or merge
   from the command line, you are using **Git**.


Comparison Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Question
     - Git
     - GitHub
   * - What is it?
     - Software / tool
     - Website / service
   * - Where does it run?
     - Your computer
     - The cloud
   * - Internet required?
     - **No**
     - Yes
   * - Account required?
     - **No**
     - Yes
   * - Cost?
     - Free (open source)
     - Free tier + paid plans
   * - Created by
     - Linus Torvalds (2005)
     - Preston-Werner et al. (2008)
   * - Example actions
     - ``git commit``, ``git branch``
     - Create PR, review code


Other Git Hosting Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


GitHub is the most popular host, but it is far from the only one.
Every service below is built on top of Git, so the commands
(``git clone``, ``git push``, ``git pull``, ...) are identical,
only the remote URL changes.

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Service
     - Notes
   * - `GitLab <https://about.gitlab.com/>`_
     - Popular alternative; strong CI/CD features; can be self-hosted.
   * - `Bitbucket <https://bitbucket.org/>`_
     - Owned by Atlassian; integrates with Jira and Trello.
   * - `Gitea <https://about.gitea.com/>`_
     - Lightweight, self-hosted option.
   * - `Azure DevOps <https://azure.microsoft.com/en-us/products/devops>`_
     - Microsoft's enterprise offering.
   * - `SourceForge <https://sourceforge.net/>`_
     - One of the oldest; still used for open source.
   * - `Codeberg <https://codeberg.org/>`_
     - Non-profit, community run, powered by Forgejo.


Git Without a Host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Git does not require a server.** This is what "distributed" means in
practice.

A remote is not a special kind of service. It is just another Git
repository that your Git can reach, and "reach" can mean a folder on
your own disk. Nothing about ``git push`` requires a company to exist.

.. list-table::
   :widths: 30 44 26
   :header-rows: 1
   :class: compact-table

   * - Where the "remote" lives
     - What you type
     - Needs
   * - Nowhere. Local only
     - ``git init``, then never push
     - Nothing
   * - A folder on the same disk
     - ``git clone /srv/git/robot.git``
     - Nothing
   * - A USB stick
     - ``git clone /media/usb/robot.git``
     - Nothing
   * - Any machine you can SSH to
     - ``git clone user@host:/srv/git/robot.git``
     - SSH and ``git``, nothing else
   * - A single file you can email
     - ``git clone robot.bundle``
     - Nothing
   * - A hosting service
     - ``git clone git@github.com:you/robot.git``
     - An account

**Your own remote, in three commands.** A ``--bare`` repository is one
with history but no checked-out files, which is exactly what a server
holds:

.. code-block:: bash

   git init --bare /media/usb/robot.git      # the "server"
   git remote add usb /media/usb/robot.git   # in your working repo
   git push usb main

That is a fully functional remote. You can hand the stick to a teammate,
they clone from it, and both of you have complete history. No account,
no network, no company.

.. admonition:: You have already seen this work
   :class: tip

   The workshop script for this module, ``git-workshop.sh``, builds
   exactly that: a bare repository next to your sandbox, added as
   ``origin``. Every ``push``, ``pull``, ``fetch`` and rejected-push
   drill you do there runs against a folder on your own disk. Nothing in
   those exercises touches the network, and Git cannot tell the
   difference.

**A repository in one file.** ``git bundle`` packs commits into a single
file you can put on a USB stick, attach to an email, or carry through an
air gap:

.. code-block:: bash

   git bundle create robot.bundle --all   # one file, whole history
   git clone robot.bundle recovered       # clone it like any remote

.. note::

   A one-commit repository bundles to a few hundred bytes. In robotics
   this applies to a robot on a test range with no connectivity, an
   air-gapped lab machine, or a field site where the only transfer
   method is physical.

**Git can also talk to non-Git servers.** ``git svn`` lets you work
against a Subversion server while using Git locally, and ``git p4`` does
the same for Perforce. So the asymmetry runs the other way too: Git can
be a client to Subversion, while GitHub cannot be a server for it.

On Ubuntu these ship separately, so ``git svn`` reports "is not a git
command" until you install it:

.. code-block:: bash

   sudo apt install git-svn

.. important::

   Your clone is not a view of the real repository somewhere else. It **is** a complete
   repository, equal to every other copy. GitHub is a convenience, and a
   good one, but it is a convention rather than a requirement: one copy
   that everybody agrees to treat as the shared one.

   Which means your work is never held hostage. If GitHub is down, or
   your account is locked, or the company disappears, every clone still
   has the full history and any of them can become the new origin.


Git: Getting Started
====================================================


.. _vc-setup:

Installing and Configuring Git
----------------------------------------------------


You only need to do this **once per machine**.

**Install Git:**

.. code-block:: bash

   sudo apt update && sudo apt install git

**Configure your identity** (used in every commit):

.. code-block:: bash

   git config --global user.name "Your Full Name"
   git config --global user.email "your.email@university.edu"

**Set your default editor:**

.. code-block:: bash

   git config --global core.editor "code --wait"

Other common choices: ``nano`` for a simple terminal editor, or
``vim`` if you already know it.

**Verify the settings:**

.. code-block:: bash

   git config --list

.. note::

   Use your real name and your university email so that commits are
   unambiguously attributed to you in team projects.

.. tip::

   No Git commands need to be memorized. Four printable cheat sheets and
   a set of interactive visualizers are collected on the
   :doc:`vc_references` page, and the :ref:`Quick Reference
   <vc-quickref>` at the end of this page lists the commands used here.
   Open one of them now and keep it beside you.


The Scenario
----------------------------------------------------


.. admonition:: Scenario
   :class: note

   To illustrate how these concepts work in practice, we will walk
   through a realistic, day-long scenario. You will take on the role of
   a robotics engineer at ENPM702Tech Labs.

   Throughout the day, you will use Git to:

   - Initialize a new project for an autonomous robot's configuration.
   - Use branching to develop a new feature (GPS navigation).
   - Handle a critical hotfix for a performance bug.
   - Navigate and resolve a merge conflict that arises from these
     parallel lines of work.


Git: Core Concepts
====================================================


The Three Areas of Git
----------------------------------------------------


.. important::

   **A commit is one saved snapshot of your project**, together with a
   note saying what changed and why. It records the state of every file
   Git is watching at that moment, plus who made it and when.

   The word works as both a noun and a verb: "a commit" is the saved
   snapshot, "to commit" is the act of saving one. Your project's
   history is nothing more than its commits, in order.

   Everything else in this module is built on that one idea. A branch
   points at a commit. A merge joins two lines of commits. Pushing sends
   commits to GitHub.


Understanding Git means understanding the **three areas** where your
files live. Each step is intentional, you choose what goes into
each commit.

.. figure:: /_static/images/version_control/three-areas-of-git.png
   :alt: Working Directory to Staging Area to Repository
   :align: center
   :width: 100%

   The three areas of Git: ``git add`` moves changes from the working
   directory into the staging area, and ``git commit`` records the
   staged snapshot into the repository.

.. grid:: 3

   .. grid-item-card:: Working Directory
      :class-card: sd-border-info

      - Your actual files on disk.
      - What you see in the file explorer.
      - Where you edit code.

   .. grid-item-card:: Staging Area
      :class-card: sd-border-info

      - A "draft box" of changes you want to record next.
      - Like writing an email before you send it.
      - Filled by ``git add``; emptied by ``git commit``.

   .. grid-item-card:: Repository
      :class-card: sd-border-info

      - Permanent history.
      - Hidden ``.git/`` folder at the project root.
      - ``git commit`` is the act of sending a staged snapshot into
        the repository.


.. _vc-add-forms:

Tracked and Untracked Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Inside the working directory, Git splits your files in two:

- **Tracked**: files Git already knows about, because some earlier
  ``git add`` introduced them. Git watches these and reports when they
  change.
- **Untracked**: everything else. Git can see the file sitting there
  and deliberately does nothing about it until you ``git add`` it.

``git status`` lists the two groups separately. The split is also what
decides how each form of ``git add`` behaves:

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: compact-table

   * - Form
     - What it stages
   * - ``git add <file>``
     - Exactly that file, whether it was tracked or not.
   * - ``git add .``
     - Everything under the current directory, **including untracked
       files**. This is how build output and password files get into
       repositories by accident.
   * - ``git add -A``
     - Everything in the **whole repository**, wherever you are standing.
       Unlike ``git add .``, running it from a subdirectory still stages
       changes in the parent.
   * - ``git add -u``
     - Changes to **tracked files only**: both edits and deletions. New
       files are left alone. The ``u`` stands for "update".
   * - ``git add -p``
     - Walks you through your changes one **hunk** at a time (a hunk is
       one contiguous block of changed lines) and asks yes or no for
       each. Use it when one file holds two unrelated changes that
       belong in separate commits.

.. tip::

   ``git add .`` is what every tutorial shows, including the examples
   further down this page, because it is short. ``git add -u`` is the
   preferred form on a real project: it cannot stage a file that was
   never intended to be added.

.. warning::

   Two behaviours of ``git add .`` surprise people.

   **It stages deletions.** Since Git 2.0, removing a file and running
   ``git add .`` stages the removal:

   .. code-block:: text

      rm a.txt && git add .   ->   D  a.txt

   **It is scoped to your current directory.** Run from ``src/``, it
   does not stage an edit to a file in the directory above. Work spread
   across two directories gets half committed. ``git add -A`` is the
   form that means the whole repository.

.. danger::

   ``git add *`` is not a Git feature. The ``*`` is expanded by your
   **shell** before Git ever sees it, and shell globs skip files
   beginning with a dot:

   .. code-block:: text

      $ git add *
      A  a.txt
      A  sub/b.txt
      ?? .gitignore     <- silently missed

   A ``.gitignore`` that was never committed protects nobody. Use
   ``git add .`` or ``git add -A``, never ``git add *``.


.. _vc-pointers:

Branches and Pointers
----------------------------------------------------


Three names appear in every diagram from here on, so they are worth
having straight before the explanation starts:

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - Name
     - What it is
   * - **branch**
     - A movable marker on one commit. ``git init`` creates one.
       Creating another copies no files.
   * - ``main``
     - The name ``git init`` gives that first branch. By convention it
       holds the version of the project everyone treats as current.
       Repositories created before 2020 usually call it ``master``
       instead; nothing else differs.
   * - ``HEAD``
     - The marker for "which branch am I on right now".

The next section replaces these one-line descriptions with what Git
actually stores on disk, which is simpler than the words suggest.


What a Pointer Really Is
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**A commit never changes.** Once made, its contents and its hash are
fixed forever. A commit also records the hash of the commit before it,
its **parent**, so commits form a chain running backwards through
history.

No commit in that chain records a branch name. Branch names are stored
separately.

**A branch is a file containing a commit hash.** You can read it:

.. code-block:: bash

   cat .git/refs/heads/main

.. code-block:: text

   a1b2c3d4e5f60718293a4b5c6d7e8f9012345678

Forty-one bytes: forty hex characters and a newline. That file **is**
the branch. Creating a branch writes one more such file, which is why
``git switch -c`` finishes instantly on a repository of any size.

``HEAD`` is one more file:

.. code-block:: bash

   cat .git/HEAD

.. code-block:: text

   ref: refs/heads/main

``HEAD`` does **not** contain a commit hash. It contains the name of a
branch. There are two steps, not one:

.. figure:: /_static/images/version_control/git-pointers-two-files.png
   :alt: .git/HEAD holds a branch name, which holds a commit hash
   :align: center
   :width: 100%

   Two files and two steps. ``.git/HEAD`` holds the **name of a
   branch**. ``.git/refs/heads/main`` holds a **commit hash**. Follow
   both and you arrive at commit ``A``.

**What happens when you commit**, in order:

1. Git writes a new commit object, whose parent is the commit you were
   on.
2. Git overwrites the file for the branch ``HEAD`` names, so it now
   holds the new commit's hash.
3. ``HEAD`` itself is not touched. It still says ``ref:
   refs/heads/main``.

So the branch moves forward and you move with it, without anything
having to update ``HEAD``.

.. figure:: /_static/images/version_control/git-pointers-commit-moves-branch.png
   :alt: after a commit the branch file holds a new hash and HEAD is unchanged
   :align: center
   :width: 100%

   A commit rewrites one file. ``.git/refs/heads/main`` now holds
   ``B``'s hash; ``.git/HEAD`` still reads ``ref: refs/heads/main``.
   The new commit records ``A`` as its parent, which is the black
   arrow.

**What happens when you switch branches:** Git rewrites the one line in
``.git/HEAD`` and makes your working directory match the commit that
branch points at.

.. code-block:: text

   on feature:  .git/HEAD -> ref: refs/heads/feature
   on main:     .git/HEAD -> ref: refs/heads/main

.. admonition:: So which does ``HEAD`` point to, a branch or a commit?
   :class: important

   Usually a branch, and through it a commit. Captions in this module
   sometimes say "``HEAD`` points to commit A" as shorthand for "``HEAD``
   points to ``main``, which points to commit A". The diagrams draw both
   steps: one arrow from ``HEAD`` to a branch, a second from that branch
   to a commit.

   The shorthand stops being harmless in one case. ``HEAD`` **can** hold
   a raw commit hash instead of a branch name:

   .. code-block:: text

      ref: refs/heads/main                        normal
      a1b2c3d4e5f60718293a4b5c6d7e8f9012345678    detached HEAD

   .. figure:: /_static/images/version_control/git-pointers-detached-head.png
      :alt: on a branch HEAD names a branch; detached, HEAD holds a hash
      :align: center
      :width: 100%

      Both states, side by side. On a branch, ``.git/HEAD`` names
      ``main`` and reaches a commit in two steps. Detached, it holds a
      commit hash and reaches ``A`` directly, with no branch in
      between.

   That second form is what Git calls a **detached HEAD**. You are on a
   commit, not on a branch. Everything still works, and you can even
   commit, but step 2 above has no branch file to update, so nothing
   moves forward with you. Switch away and the commits you made have
   nothing pointing at them.

   They are not deleted (see :ref:`git reflog <vc-reflog>`), but they are
   invisible to ``git log`` and ``git branch``. This is a common cause
   of work appearing to be lost.

Several commands are the same operation on these files:

.. list-table::
   :widths: 34 66
   :header-rows: 1
   :class: compact-table

   * - What you type
     - What it does to the pointers
   * - ``git commit``
     - Adds a commit, moves the current branch file to it.
   * - ``git switch -c <name>``
     - Writes a new 41-byte file, points ``HEAD`` at it.
   * - ``git branch -d <name>``
     - Deletes one file. The commits are untouched.
   * - ``git merge``
     - Adds a commit with **two** parents, moves the branch to it.
   * - ``git reset --hard <hash>``
     - Rewrites the current branch file to a different hash.
   * - Fast-forward
     - No new commit needed: the branch file is simply overwritten with
       a commit that is already ahead of it.

So the three names at the top of this section are three files:

- ``HEAD`` is ``.git/HEAD``, holding the name of the branch you are on.
- A **branch** is a file under ``.git/refs/heads/``, holding one commit
  hash.
- ``main`` is simply the one of those files that ``git init`` created.


Git: A Day's Work
====================================================

.. figure:: /_static/images/version_control/labtech.jpeg
   :alt: Two sidewalk delivery robots, numbered 01 and 02, on a
         university campus between buildings
   :align: center
   :width: 100%

   Two of the eleven robots on the ENPM702Tech test fleet, out on
   campus. Every one of them boots from the ``robot_config.yaml`` you
   are about to put under version control. Image generated by Google
   Gemini.


9:00 Setting Up the Project
----------------------------------------------------


ENPM702Tech Labs builds a sidewalk delivery robot: a four-wheeled
platform that carries parcels between buildings on a university campus.
Eleven of them are on the test fleet, and every one of them boots from
the same file.

That file is ``robot_config.yaml``. It sets how fast the robot may
travel, how often the navigation stack recalculates its position, how
much clearance it leaves around an obstacle, and which sensors are
active. A wrong number in it does not break one robot. It reaches all
eleven the next time they are flashed.

Last week the file lived on one engineer's laptop and was copied around
by email. Two robots are now running configurations nobody can account
for. Putting the file under version control is this morning's job.

By the end of the day, three separate changes will have been made to the
same few lines of it, one of them urgent, and two of them at the same
time.

.. admonition:: **Monday, 9:00 AM** · Setting Up the Project
   :class: vc-stage

   You begin your week by creating the baseline configuration for a new
   autonomous delivery robot platform.

1. **Create a new project directory.**

   .. code-block:: bash

      # Create a new project directory
      mkdir robot-config   # kebab-case: see below

.. dropdown:: Why ``robot-config`` and not ``robot_config`` or ``RobotConfig``?
   :class-container: sd-border-info

   This directory becomes the repository, and the repository name
   becomes part of its URL:

   .. code-block:: text

      https://github.com/yourusername/robot-config

   Three properties matter for a name in that position:

   - **Hyphens survive a URL; underscores can vanish.** Links are
     commonly rendered underlined, and an underscore sits on the same
     line as the underline. ``robot_config`` can read as ``robot config``
     or ``robotconfig`` when someone copies it off a slide.
   - **Lowercase avoids a real portability problem.** Linux filesystems
     are case-sensitive; macOS and Windows normally are not. A
     repository containing both ``RobotConfig/`` and ``robotconfig/``
     works on Linux and breaks on a teammate's Mac, where the two
     collapse into one directory.
   - **No spaces.** ``robot config`` has to be quoted in every single
     command that touches it.

   It is also the prevailing convention: ``enpm702-fall-2026-docs``,
   ``enpm702-fall-2026-cpp``, and most repositories you will clone.

   .. important::

      Three conventions coexist in this course, and each is required by
      something different. They are not interchangeable.

      .. list-table::
         :widths: 32 24 44
         :header-rows: 1
         :class: compact-table

         * - Thing being named
           - Convention
           - Why
         * - Repositories and directories
           - ``robot-config``
           - URL-safe and case-portable, as above.
         * - C++ variables and functions
           - ``max_speed``
           - A hyphen is the subtraction operator, so
             ``max-speed`` is parsed as ``max`` minus ``speed``.
         * - ROS 2 packages
           - ``robot_bringup``
           - Required by the tooling. ``ros2 pkg create
             my-robot-pkg`` exits with an error and creates nothing;
             ``my_robot_pkg`` succeeds.

      So a repository named ``robot-config`` can perfectly well contain
      a ROS 2 package named ``robot_config`` holding a C++ variable
      named ``max_speed``. All three are correct in their own context.

2. **Initialize version control.**

   .. code-block:: bash

      cd robot-config
      git init

   ``git init`` creates a new Git repository in your current directory.

   - Creates the ``.git`` directory: This hidden folder contains all of
     Git's internal files and metadata for the repository, including the
     object database, configuration files, and references.
   - Initializes an empty repository: The repository starts with no
     commits, branches, or tracked files. It is essentially a *blank
     slate* ready for you to start adding content.
   - Sets up the default branch: Modern Git versions create a default
     branch.

   .. admonition:: What is the default branch?
      :class: note

      Think of the default branch as the official, stable version of
      your project, like the **master copy** of a document that everyone
      refers to. The default branch is usually called ``master`` or
      ``main``.

   .. note::

      GitHub and many organizations switched from ``master`` to ``main``
      for inclusive language reasons. Git itself updated to allow
      configurable default branch names.

3. **Create the files you need to track in the current folder.**

   - ``robot_config.yaml``, the configuration the whole fleet boots
     from.
   - ``README.md``, the front door for anyone meeting the project for
     the first time.
   - ``.gitignore``, which tells Git what to leave alone.

   .. admonition:: Download the starter files
      :class: tip

      Rather than typing them, download all three and unzip them into
      ``robot-config``:

      :download:`robot-config-starter.zip </_static/files/robot-config-starter.zip>`

      .. code-block:: bash

         cd robot-config
         unzip ~/Downloads/robot-config-starter.zip
         mv robot-config-starter/.gitignore robot-config-starter/* .
         rmdir robot-config-starter
         ls -a          # robot_config.yaml, README.md, .gitignore

      Individually:
      :download:`robot_config.yaml </_static/files/robot-config-starter/robot_config.yaml>`,
      :download:`README.md </_static/files/robot-config-starter/README.md>`,
      :download:`.gitignore </_static/files/robot-config-starter/.gitignore>`.
      Browsers sometimes refuse to save a file whose name begins with a
      dot, so the zip is the reliable route for that one.

   The starting configuration, matching what the test fleet runs:

   .. code-block:: yaml

      # robot_config.yaml
      #
      # Baseline configuration for the ENPM702Tech delivery robot fleet.
      # Every robot boots from this file, so a wrong value here reaches the
      # whole fleet at the next flash.

      robot:
        name: "delivery-bot"
        wheel_radius: 0.08      # meters
        max_speed: 1.5          # m/s

      navigation:
        # General navigation settings for the robot
        update_rate: 5          # Hz
        coordinate_system: "WGS84"
        obstacle_margin: 0.35   # meters

      sensors:
        lidar: true
        imu: true
        gps: false

   ``update_rate`` is the line to watch. It changes three times before
   the day is out, and two of those changes collide.

   .. code-block:: bash

      git status

.. dropdown:: Why Use ``.gitignore``?
   :class-container: sd-border-info

   Avoid tracking files that:

   - Are generated automatically (build artifacts, compiled code).
   - Contain sensitive information (passwords, API keys).
   - Are user-specific (IDE settings, OS files).
   - Are too large or binary (datasets, videos, executables).
   - Change frequently but are not important (log files, cache).

   Every entry in such a list shares one property: **something other
   than you created it.** A compiler, a linker, a file manager or an
   editor produced it, and running the same tools again produces it
   afresh. The test for any other file: if deleting it costs nothing
   because it can be regenerated, it does not belong in the history.

   **The file to use in this course.** This is exactly the
   ``.gitignore`` in the starter download, so you already have it:

   .. code-block:: text

      # --- C++ and CMake build output ---
      build/
      *.o
      *.a
      *.so
      CMakeCache.txt
      CMakeFiles/
      cmake_install.cmake
      Makefile
      compile_commands.json

      # --- Python ---
      __pycache__/
      *.py[cod]
      *.egg-info/
      .eggs/
      dist/
      .venv/
      venv/
      .mypy_cache/
      .pytest_cache/
      .ipynb_checkpoints/

      # --- ROS 2 / colcon workspace output ---
      install/
      log/

      # --- Editor and OS clutter ---
      .vscode/
      .idea/
      .DS_Store
      *.swp
      *~

      # --- Never commit these ---
      *.pem
      *.key
      secrets.yaml
      .env

   The patterns use four pieces of syntax:

   .. list-table::
      :widths: 16 84
      :header-rows: 1
      :class: compact-table

      * - Syntax
        - Meaning
      * - ``*``
        - Matches any run of characters within one path segment.
          ``*.o`` matches ``main.o`` and ``src/main.o``.
      * - ``/`` at the end
        - Match a **directory only**. ``build/`` ignores the directory
          and everything under it, but leaves a file named ``build``
          alone.
      * - ``/`` at the start
        - Anchor to the repository root. ``/build`` ignores only the
          top-level one, not ``src/build``.
      * - ``!``
        - Negate an earlier rule, which is how the ``.vscode`` example
          below keeps two files while ignoring the rest.
      * - ``#``
        - A comment. Write them. A bare list of patterns tells the next
          person nothing about why each one is there.


   The generic advice above becomes concrete here. Two kinds of files must
   never reach a commit in ENPM702: **build output** and **secrets**.

   Put this at the root of every C++ assignment repository, before your
   first commit:

   .. code-block:: text

      # --- C++ and CMake build output ---
      build/
      *.o
      *.a
      *.so
      CMakeCache.txt
      CMakeFiles/
      cmake_install.cmake
      Makefile
      compile_commands.json

      # --- ROS 2 / colcon workspace output ---
      install/
      log/

      # --- Editor and OS clutter ---
      .vscode/
      .idea/
      .DS_Store
      *.swp

      # --- Never commit these ---
      *.pem
      *.key
      secrets.yaml
      .env

   .. note::

      Keep ``.vscode/`` ignored by default. If your team agrees to share
      editor settings, unignore those two files and nothing else:

      .. code-block:: text

         .vscode/*                    # ignore everything INSIDE .vscode/
         !.vscode/settings.json       # except this one: put it back
         !.vscode/extensions.json     # and this one

      ``!`` cancels an earlier rule, so the last two lines re-include files
      the first line had ignored. The result: ``settings.json`` and
      ``extensions.json`` are tracked, everything else in ``.vscode/`` is
      not.

      Those two are the ones worth sharing. ``settings.json`` holds project
      choices such as formatter and indent width, and ``extensions.json``
      recommends extensions to anyone opening the project. The rest is
      per-machine: ``launch.json`` usually contains absolute paths, and the
      remaining files are local editor state.

      .. warning::

         Write ``.vscode/*``, not ``.vscode/``. The two are not
         interchangeable here.

         A trailing slash ignores **the directory itself**, and Git does
         not look inside a directory it has already excluded, so a ``!``
         rule for a file in there is never reached. ``/*`` ignores the
         **contents** one by one and leaves the directory itself visible,
         which is what gives the negations something to cancel.

         .. code-block:: text

            .vscode/                  settings.json IGNORED   <- negation has no effect
            .vscode/*                 settings.json tracked   <- works

         The same trap applies to any "ignore a directory except one file"
         rule, for example ``data/*`` with ``!data/README.md``.


   **What ``.gitignore`` does not do**


   **It does not untrack files that are already tracked.** Adding
   ``build/`` to ``.gitignore`` changes nothing for files Git is already
   following. Stop tracking them, keeping your local copies:

   .. code-block:: bash

      git rm -r --cached build/
      git commit -m "Stop tracking build output"

   **It does not erase history.**

   .. code-block:: bash

      git rm --cached robot_secrets.yaml
      git commit -m "Stop tracking robot_secrets.yaml"

   After this the file is gone from the latest commit, and the password is
   still sitting in the commit that added it. Anyone with the repository can
   read it:

   .. code-block:: bash

      git log --oneline -S "Terrapins2026"   # finds the commit that added it
      git show <hash>                        # prints the password

   .. danger::

      **If you commit a credential, treat it as leaked.** Rotate it: change
      the password, revoke the token, regenerate the key. Do that first.

      Removing the secret from history is possible (``git filter-repo``, or
      GitHub's support team for a public repository) but it rewrites every
      commit hash, breaks every clone, and does nothing about the copy an
      automated scanner already took. Rotation is the fix. Rewriting is
      cleanup.

      The reliable version of this advice is the boring one: write the
      ``.gitignore`` before the first commit.


   .. admonition:: Best Practices
      :class: tip

      - **Create early**: Add ``.gitignore`` before making your first
        commit.
      - **Already tracked files**: ``.gitignore`` will not affect files
        already being tracked.
      - **Remove tracked files**: Use ``git rm --cached filename`` to
        stop tracking.

        .. code-block:: bash

           # Remove file from tracking but keep locally
           git rm --cached sensitive_config.yaml

4. **Stage the files.**

   .. code-block:: bash

      git status          # look before staging, every time
      git add .

   Staging puts your changes in a **draft box** called the *staging
   area*. You are preparing what you want to include in your next save
   point, but you have not saved it yet.

   - *Analogy*: Drafting an email, your email is ready to be sent but
     not sent yet.

   .. note::

      ``git add .`` stages every untracked file under the current
      directory. That is safe **here**, because you created all three
      files a moment ago and the ``.gitignore`` is already in place, so
      there is nothing else to sweep up.

      It is not a safe habit. On a working project the same command
      picks up build output, editor files and anything else lying
      around, which is how credentials reach repositories. Name the
      files you mean (``git add robot_config.yaml``) or use ``git add
      -u`` for tracked files only. The forms are compared in
      :ref:`Tracked and Untracked Files <vc-add-forms>`.

5. **Commit changes.**

   .. code-block:: bash

      git commit -m "Initial commit: Add basic robot configuration

      - Add robot_config.yaml with hardware and navigation settings
      - Add README.md with project description
      - Add .gitignore"

   Committing takes everything from your staging area (draft box) and
   creates a permanent save point in your project's history.

   - *Analogy*: Sending an email, it is now permanently sent and
     becomes part of your email history.

   .. admonition:: Best Practice
      :class: tip

      Write detailed commit messages. The subject line says what
      changed; the body says why. See :ref:`How to Commit Well
      <vc-commit-well>`.

6. **Verify the commit.**

   .. code-block:: bash

      git log --oneline --graph --decorate

   .. code-block:: text

      * a1b2c3d (HEAD -> main) Initial commit: Add basic robot configuration

   ``--decorate`` prints the labels in brackets. Git turns it on
   automatically when it is writing to a terminal, so you will normally
   see them without asking. You can pass other options to ``git log``.
   Run ``git log --help`` for the full list.

   .. figure:: /_static/images/version_control/git-graph-initial-commit.png
      :alt: Git graph after the initial commit
      :align: center
      :width: 100%

      After the initial commit, ``main`` points to commit ``A`` and
      ``HEAD`` points to ``main``. Read the arrows right to left: they
      are the two steps. Keeping them separate is what lets a later
      commit move ``main`` forward without touching ``HEAD``.

   .. note::

      Open the folder ``robot-config`` in VS Code and use the Git Graph
      extension to visualize branches and commits.


Why Use Branches
----------------------------------------------------


.. grid:: 2

   .. grid-item-card:: Why Use Branches?
      :class-card: sd-border-info

      - **Isolate features**, develop without breaking stable code.
      - **Experiment safely**, if it does not pan out, delete the
        branch.
      - **Parallel development**, multiple teammates work at the
        same time.
      - **Hotfixes**, fix urgent production bugs while feature
        work continues elsewhere.

   .. grid-item-card:: Standard Branch Naming
      :class-card: sd-border-info

      Use a short prefix that describes intent:

      - ``feature/<description>``, new features
      - ``hotfix/<description>``, urgent production fixes
      - ``bugfix/<description>``, non-urgent bug fixes

      Examples:

      - ``feature/user-authentication``
      - ``hotfix/fix-timeout-value``
      - ``bugfix/correct-spelling-error``

.. tip::

   Use lowercase, hyphens instead of spaces, and be descriptive.
   Your future self, and your teammates, will thank you.


10:00 Adding GPS Navigation
----------------------------------------------------


.. admonition:: **10:00 AM** · Adding GPS Navigation
   :class: vc-stage

   You receive a task to add GPS navigation capabilities to the
   robot.

1. **Create a feature branch for GPS navigation.**

   .. code-block:: bash

      git switch -c feature/gps-navigation

   - ``git switch`` = "Switch to a branch"
   - ``-c`` = "Create it first, from wherever you are right now"
   - **Combined:** "Create a new branch AND switch to it immediately"
   - ``feature/`` is a naming convention (like organizing folders).
   - ``gps-navigation`` describes what this branch is for.

   **Long way (two separate commands):**

   .. code-block:: bash

      git branch feature/gps-navigation     # Create the branch
      git switch feature/gps-navigation   # Switch to it

   .. note::

      When you use ``git switch -c <new-branch-name>``, the new
      branch is created from the current branch you are on. For
      instance, to create ``feature/gps-navigation`` from ``main``:

      .. code-block:: bash

         git switch main                        # Switch to main
         git switch -c feature/gps-navigation   # Create and switch

      Alternative:

      .. code-block:: bash

         git switch -c feature/gps-navigation main

2. **Check you are on the current branch.**

   .. code-block:: bash

      git branch

      # output
      * feature/gps-navigation
        main

   .. figure:: /_static/images/version_control/git-graph-feature-branch.png
      :alt: Git graph after creating the feature branch
      :align: center
      :width: 100%

      Both branches point to the **same commit** ``A``. No files were
      copied. Git wrote one 41-byte file,
      ``.git/refs/heads/feature/gps-navigation``, holding ``A``'s hash,
      and rewrote ``.git/HEAD`` to name that branch instead of
      ``main``.

3. **Modify robot_config.yaml for GPS Feature.**

   Two changes. Add a ``gps`` block, and lower
   ``navigation.update_rate`` from 5 to 3 Hz, because the GPS fix needs
   time to settle between updates and at 5 Hz the reported position
   jumps around.

   Here is the file afterwards. The highlighted lines are the ones you
   changed:

   .. code-block:: yaml
      :emphasize-lines: 14, 18-22, 27

      # robot_config.yaml
      #
      # Baseline configuration for the ENPM702Tech delivery robot fleet.
      # Every robot boots from this file, so a wrong value here reaches the
      # whole fleet at the next flash.

      robot:
        name: "delivery-bot"
        wheel_radius: 0.08      # meters
        max_speed: 1.5          # m/s

      navigation:
        # General navigation settings for the robot
        update_rate: 3          # Hz. Lowered from 5 for GPS settling.
        coordinate_system: "WGS84"
        obstacle_margin: 0.35   # meters

      gps:
        enabled: true
        port: "/dev/ttyUSB0"
        baud_rate: 9600
        fix_timeout: 5          # seconds

      sensors:
        lidar: true
        imu: true
        gps: true

   .. note::

      The ``update_rate`` change matters later. The hotfix in the next
      section edits that same line, which is how most merge conflicts
      arise.

4. **Check what changed.**

   .. code-block:: bash

      git diff

   .. code-block:: diff

      diff --git a/robot_config.yaml b/robot_config.yaml
      index a295ea8..cdf7c1a 100644
      --- a/robot_config.yaml
      +++ b/robot_config.yaml
      @@ -11,11 +11,17 @@ robot:

       navigation:
         # General navigation settings for the robot
      -  update_rate: 5          # Hz
      +  update_rate: 3          # Hz. Lowered from 5 for GPS settling.
         coordinate_system: "WGS84"
         obstacle_margin: 0.35   # meters

      +gps:
      +  enabled: true
      +  port: "/dev/ttyUSB0"
      +  baud_rate: 9600
      +  fix_timeout: 5          # seconds
      +
       sensors:
         lidar: true
         imu: true
      -  gps: false
      +  gps: true

   Reading it from the top:

   .. list-table::
      :widths: 34 66
      :header-rows: 1
      :class: compact-table

      * - Line
        - What it means
      * - ``diff --git a/... b/...``
        - The file being compared. ``a/`` is the old version, ``b/`` the
          new one.
      * - ``index a295ea8..cdf7c1a 100644``
        - Hashes of the two stored versions, and the file's permissions.
          You can ignore this line.
      * - ``--- a/robot_config.yaml``
        - The old version. Its lines are the ones marked ``-``.
      * - ``+++ b/robot_config.yaml``
        - The new version. Its lines are the ones marked ``+``.
      * - ``@@ -11,11 +11,17 @@ robot:``
        - A **hunk** header, one per changed region. It reads: from the
          old file, 11 lines starting at line 11; from the new file, 17
          lines starting at line 11. The trailing ``robot:`` is the
          nearest heading above the change, shown for orientation.
      * - Lines starting with a space
        - Unchanged **context**, printed so you can see where the change
          sits. Three lines either side, by default.
      * - Lines starting with ``-``
        - Removed from the old version.
      * - Lines starting with ``+``
        - Added in the new version.

   Three things worth noticing:

   - **There is no "changed" marker.** Editing a line shows up as a
     ``-`` immediately followed by a ``+``, which is what happened to
     ``update_rate``.
   - **You only see the changed regions**, not the whole file. The
     header comment and the ``robot:`` block are absent because nothing
     in them changed.
   - **Blank-looking ``+`` lines are real.** The ``+`` on its own after
     ``fix_timeout`` is the blank line separating the new ``gps`` block
     from ``sensors:``.

   ``git diff`` with no arguments compares your working directory
   (current files) against the staging area. Once you ``git add`` these
   changes, this command prints nothing, because there is no longer any
   difference between the two. Use ``git diff --staged`` to see what you
   have staged.

5. **Stage and commit the changes.**

   .. code-block:: bash

      git add robot_config.yaml
      git commit

   Write this in the editor that opens:

   .. code-block:: text

      Add GPS receiver configuration

      Set the receiver up on /dev/ttyUSB0 at 9600 baud and turn on the
      gps sensor flag, so the navigation stack starts consuming fixes.

      Lower navigation.update_rate from 5Hz to 3Hz. At 5Hz the stack
      polls the receiver before it has finished producing a fix, so the
      reported position jumps around. 3Hz gives the fix time to settle.

   .. code-block:: bash

      # Check commit history or use Git Graph
      git log --oneline --all --graph

   .. dropdown:: Why not ``-m "Feature: Add GPS navigation capabilities to the robot"``?
      :class-container: sd-border-info

      That subject line is what most people write, and it fails three of
      the tests in :ref:`How to Commit Well <vc-commit-well>`:

      .. list-table::
         :widths: 32 68
         :header-rows: 1
         :class: compact-table

         * - Problem
           - Why it matters
         * - ``Feature:`` repeats the branch
           - The commit is on ``feature/gps-navigation``. The prefix
             adds nothing and eats characters from a 50-character
             budget.
         * - "to the robot" is filler
           - Every commit in this repository is about the robot.
         * - "capabilities" names nothing
           - The diff sets a serial port, a baud rate, a fix timeout and
             a polling rate. "Capabilities" covers all of it and
             identifies none of it.
         * - No body at all
           - The ``update_rate`` change is the one nobody can guess
             from the diff, and it is the line the hotfix collides with
             in the next section. With ``-m`` there is nowhere to put
             the reason.

      The replacement keeps the subject at 30 characters and puts the
      reasoning in the body. Six weeks from now, ``git blame`` on the
      ``update_rate`` line lands on this commit, and the answer to "why
      3 and not 5?" is right there.

      .. note::

         Running ``git commit`` with no ``-m`` is what makes a body
         convenient: Git opens your editor, and you type a subject, a
         blank line, then the body. ``-m`` is fine for genuinely
         one-line changes, which is why the rest of this module uses it.

   .. figure:: /_static/images/version_control/git-graph-branch-ahead.png
      :alt: main still at commit A while feature/gps-navigation is ahead at B
      :align: center
      :width: 100%

      ``feature/gps-navigation`` is **ahead of** ``main``. ``main``
      still points at ``A``; the feature branch advanced to ``B``. The
      feature branch has a commit that ``main`` does not, and ``main``
      has nothing the feature branch is missing.

   .. dropdown:: Seeing this without the picture
      :class-container: sd-border-info

      The figure is a drawing of what these commands print.

      **The shape of the history**, with both branch labels:

      .. code-block:: bash

         git log --oneline --graph --all --decorate

      .. code-block:: text

         * 6bfb4a3 (HEAD -> feature/gps-navigation) Add GPS receiver configuration
         * 746fda5 (main) Initial commit: Add basic robot configuration

      One line per commit, and the labels in brackets show where each
      branch points. Note the commits are in a straight line, with no
      fork, because nothing has happened on ``main`` yet.

      **Where each branch points**, one line each:

      .. code-block:: bash

         git branch -v

      .. code-block:: text

         * feature/gps-navigation 6bfb4a3 Add GPS receiver configuration
           main                   746fda5 Initial commit: Add basic robot configuration

      The ``*`` marks the branch you are on.

      **What each branch has that the other does not.** This is the
      question the caption is answering, and ``..`` is how you ask it:

      .. code-block:: bash

         git log --oneline main..feature/gps-navigation   # feature has, main lacks
         git log --oneline feature/gps-navigation..main   # main has, feature lacks

      The first prints one commit. The second prints **nothing**, which
      is what "ahead" means: everything on ``main`` is already on the
      feature branch.

      ``git branch --no-merged main`` says the same thing from the other
      direction: it lists ``feature/gps-navigation``, because that
      branch holds work ``main`` has not taken in yet.

      .. important::

         **Ahead is not the same as diverged.** Diverged means *both*
         branches have commits the other lacks, so neither can simply
         fast-forward to the other.

         Right now only one of those two ranges has anything in it, so
         the branches have not diverged. That changes at
         :ref:`11:30 <vc-diverge>`, when a hotfix lands on ``main``
         while the feature branch sits at ``B``. Then both ranges are
         non-empty, the graph forks, and one command says it outright:

         .. code-block:: bash

            git rev-list --left-right --count main...feature/gps-navigation

         Note the **three** dots. Two dots ask "what is on one side",
         three dots ask "what is on either side but not both".


.. _vc-diverge:

11:30 An Emergency Fix
----------------------------------------------------


.. admonition:: **11:30 AM** · Emergency Fix Needed
   :class: vc-stage

   You get an urgent message: the robot's overall responsiveness is
   sluggish. The default navigation ``update_rate`` of 5Hz is too slow
   for real-time obstacle avoidance.

   .. warning::

      This is a critical issue. You must fix this on ``main``
      immediately.

1. Check what we are working on.

   .. code-block:: bash

      git status


   .. code-block:: bash

      # On branch feature/gps-navigation
      # nothing to commit, working tree clean

   Your GPS work is safe on its own branch. You can switch away without
   losing anything.

2. **Create and switch to the new branch.** The fix needs to be based
   on the official ``main`` branch, not your
   ``feature/gps-navigation`` branch.

   .. code-block:: bash

      git switch main                         # switch to main
      git switch -c hotfix/fix-navigation-rate

   Or, more concisely:

   .. code-block:: bash

      git switch -c hotfix/fix-navigation-rate main

   .. figure:: /_static/images/version_control/git-graph-hotfix-branch.png
      :alt: Git graph showing the hotfix branch created from main
      :align: center
      :width: 100%

      The feature work on ``B`` is safe and untouched. The hotfix
      branch starts from ``main`` (``A``), not from the feature
      branch.

3. **Increase navigation update_rate to 10Hz.** Change the
   ``update_rate`` in ``robot_config.yaml`` from 5Hz to 10Hz.

4. **Check the changes.**

   .. code-block:: bash

      git diff


5. **Stage and commit.**

   .. code-block:: bash

      git add robot_config.yaml
      git commit -m "HOTFIX: Increase navigation update rate to 10Hz

      - Critical performance fix to improve robot responsiveness.
      - Increases the navigation update rate from 5Hz to 10Hz."

   .. figure:: /_static/images/version_control/git-graph-hotfix-commit.png
      :alt: Git graph after committing the hotfix
      :align: center
      :width: 100%

      The hotfix branch now has its own commit ``C``. ``main`` still
      sits at ``A``; the feature branch is unchanged at ``B``.

6. **Merge hotfix back to main.**

   .. code-block:: bash

      git switch main                        # switch to main
      git merge hotfix/fix-navigation-rate

   a. Go to the ``main`` version of the project.
   b. Apply all the changes made on the
      ``hotfix/fix-navigation-rate`` branch into this ``main`` branch.

   .. figure:: /_static/images/version_control/git-graph-after-merge-hotfix.png
      :alt: Git graph after merging the hotfix into main
      :align: center
      :width: 100%

      Both ``main`` and ``hotfix/fix-navigation-rate`` now point at
      ``C``. ``main`` has fast-forwarded onto the hotfix commit.

7. **Clean up the hotfix branch.**

   Step 6 left you on ``main``, which is where this has to run from.

   .. code-block:: bash

      git branch -d hotfix/fix-navigation-rate

   .. note::

      You cannot delete the branch you are standing on, and you do not
      have to remember that: Git refuses.

      .. code-block:: text

         error: cannot delete branch 'hotfix/fix-navigation-rate' used by
         worktree at '/home/you/robot-config'

      "Worktree" here just means your checkout. The fix is to move off
      the branch first, which is what ``git switch main`` in step 6 did.
      This refusal is not overridable: ``-D`` is rejected for the same
      reason.

      ``-d`` has a second refusal that **is** overridable. It declines
      to delete a branch whose commits are not merged anywhere, so you
      cannot lose work by accident:

      .. code-block:: text

         error: the branch 'tmp/experiment' is not fully merged.
         If you are sure you want to delete it, run 'git branch -D tmp/experiment'

      Here the merge in step 6 already moved ``main`` onto commit ``C``,
      so the hotfix branch is fully merged and ``-d`` is happy. Reach for
      ``-D`` only when you mean to throw the commits away, and even then
      :ref:`git reflog <vc-reflog>` can usually get them back.

   .. figure:: /_static/images/version_control/git-graph-delete-hotfix.png
      :alt: Git graph after deleting the hotfix branch
      :align: center
      :width: 100%

      The hotfix branch label is gone; commit ``C`` is still in
      history under ``main``. The feature branch is untouched.

8. **Check current state.**

   .. code-block:: bash

      git log --oneline --all --graph


12:30 A Merge Conflict
----------------------------------------------------


.. admonition:: **12:30 PM** · Handling Merge Conflicts
   :class: vc-stage

   After the hotfix is deployed, you return to your GPS feature. To
   stay up to date, you must merge the changes from ``main`` into your
   feature branch.

1. **Switch back to the GPS feature branch.**

   .. code-block:: bash

      git switch feature/gps-navigation


2. **Attempt the merge.**

   .. code-block:: bash

      git merge main


   .. code-block:: bash

      # Auto-merging robot_config.yaml
      # CONFLICT (content): Merge conflict in robot_config.yaml
      # Automatic merge failed; fix conflicts and then commit the result.

3. **Check the conflict status.**

   .. code-block:: bash

      git status


   .. code-block:: bash

      # On branch feature/gps-navigation
      # You have unmerged paths.
      #   (fix conflicts and run "git commit")
      #   (use "git merge --abort" to abort the merge)
      #
      # Unmerged paths:
      #   (use "git add <file>..." to mark resolution)
      #   both modified:    robot_config.yaml

.. warning::

   We have a **Merge Conflict** because both branches modified the same
   line in ``robot_config.yaml``. Instead of guessing, Git pauses the
   merge and inserts conflict markers into the file, asking you to
   resolve the situation manually.

.. code-block:: text

   navigation:
     # General navigation settings for the robot
   <<<<<<< HEAD
     update_rate: 3  # Hz. Lowered from 5 to 3 so the GPS fix can settle.
   =======
     update_rate: 10  # Hz. Raised from 5 to 10 for responsiveness.
   >>>>>>> main
     coordinate_system: "WGS84"

- ``<<<<<<< HEAD``: Marks the beginning of the change from your current
  branch (``feature/gps-navigation``).
- ``=======``: Separates the two conflicting changes.
- ``>>>>>>> main``: Marks the end of the change from the branch you are
  merging in (``main``).

4. Open ``robot_config.yaml`` in your editor to see the conflict
   markers.
5. Edit the file to contain only the final, correct code and remove all
   conflict markers.

   .. tip::

      VS Code offers a **Resolve in Merge Editor** button on a
      conflicted file. It shows three panes: your branch on the left,
      the incoming branch on the right, and the result at the bottom.
      Click **Accept Incoming**, **Accept Current**, or edit the result
      pane by hand.

      Learn to read the raw markers first. The merge editor is faster
      once you already know what it is doing, and useless if you do
      not.

   .. warning::

      Resolving a conflict is a decision, not a cleanup job. Neither
      side is automatically right. Read both, work out what the code is
      supposed to do, and write the answer. "Accept incoming" is a
      choice you have to be able to defend.

6. **Stage the file.**

   .. code-block:: bash

      git add robot_config.yaml

7. **Complete the merge with a descriptive commit message:**

   .. code-block:: bash

      git commit -m "Merge main into feature/gps-navigation

      Resolved the navigation update_rate conflict:
      - The GPS work lowered the rate to 3Hz; the hotfix raised it to 10Hz.
      - Settled on 8Hz: measured on the test robot, the GPS fix still
        settles at 8Hz and responsiveness stays acceptable."

.. note::

   If you get lost partway through a conflict, you are not stuck.
   ``git merge --abort`` puts the repository back exactly as it was
   before you typed ``git merge``, as if nothing had happened.

8. **Verify the merge history.**

   .. code-block:: bash

      git log --oneline --graph


   .. figure:: /_static/images/version_control/git-graph-after-merge-conflict.png
      :alt: Git graph after resolving the merge conflict
      :align: center
      :width: 100%

      The new commit ``D`` is a **merge commit** with two parents
      (``B`` and ``C``). It brings the hotfix into the feature
      branch; the feature branch is now up-to-date with ``main``.


2:00 Completing the Feature
----------------------------------------------------


.. admonition:: **2:00 PM** · Completing the Feature
   :class: vc-stage

   You add final touches to the GPS feature.

   - Add waypoint information to define how the robot handles mission
     destinations based on GPS coordinates.
   - Update ``README.md`` file.

1. **Add GPS waypoint configuration in** ``robot_config.yaml``.

   A waypoint is one destination on a mission, given as a latitude and
   longitude. Add a ``waypoints`` block after ``gps``, since waypoints
   are useless without a fix:

   .. code-block:: yaml
      :emphasize-lines: 24-29

      # robot_config.yaml
      #
      # Baseline configuration for the ENPM702Tech delivery robot fleet.
      # Every robot boots from this file, so a wrong value here reaches the
      # whole fleet at the next flash.

      robot:
        name: "delivery-bot"
        wheel_radius: 0.08      # meters
        max_speed: 1.5          # m/s

      navigation:
        # General navigation settings for the robot
        update_rate: 8          # Hz. The compromise from the 12:30 conflict.
        coordinate_system: "WGS84"
        obstacle_margin: 0.35   # meters

      gps:
        enabled: true
        port: "/dev/ttyUSB0"
        baud_rate: 9600
        fix_timeout: 5          # seconds

      waypoints:
        max_count: 50           # destinations one mission may carry
        precision_m: 1.0        # how close counts as "arrived"
        home:                   # where auto-return sends the robot
          latitude: 38.9869
          longitude: -76.9426

      sensors:
        lidar: true
        imu: true
        gps: true

   ``coordinate_system`` is already ``WGS84``, so ``latitude`` and
   ``longitude`` are plain decimal degrees. ``update_rate`` is 8 here
   because that is what you settled on when you resolved the conflict at
   12:30.

2. **Update** ``README.md``.

   The README documents what each setting does, so it needs the new
   keys. Add a **GPS and waypoints** section after *Settings that
   matter* and before *Changing a value*, so the two settings sections
   sit together and the how-to stays last:

   .. code-block:: markdown
      :emphasize-lines: 26-40

      # robot-config

      Baseline configuration for the ENPM702Tech sidewalk delivery robot.

      Eleven robots on the test fleet boot from `robot_config.yaml`. Changes
      here reach every one of them, so they go through a branch and a pull
      request rather than straight onto `main`.

      ## Files

      | File | Purpose |
      |---|---|
      | `robot_config.yaml` | Drive limits, navigation settings, sensor list |
      | `.gitignore` | What Git should leave alone |

      ## Settings that matter

      - `robot.max_speed` is capped at 1.5 m/s by the campus operating
        agreement. Do not raise it without sign-off.
      - `navigation.update_rate` is how often the navigation stack recomputes
        position. Higher is more responsive and costs CPU; lower gives a GPS
        fix more time to settle.
      - `navigation.obstacle_margin` is the clearance kept around detected
        obstacles, in meters.

      ## GPS and waypoints

      The robot takes its position from a GPS receiver on `gps.port`.
      Because `navigation.coordinate_system` is WGS84, waypoint
      latitude and longitude are plain decimal degrees.

      - `waypoints.max_count` caps how many destinations one mission
        may carry.
      - `waypoints.precision_m` is how close the robot must get before
        a waypoint counts as reached. Tightening it past the accuracy
        of the GPS fix makes the robot circle.
      - `waypoints.home` is where auto-return sends the robot when a
        mission ends or the battery runs low.
      - `gps.fix_timeout` is how long the stack waits for a position
        before falling back to dead reckoning.

      ## Changing a value

      ```bash
      git switch -c feature/short-description
      # edit robot_config.yaml
      git add robot_config.yaml
      git commit
      ```

      Say in the commit message why the value changed, not just what changed.

      Once this repository has a remote, push the branch and open a pull
      request rather than merging it yourself.

3. Review all changes.

   .. code-block:: bash

      git status

4. Stage.

   .. code-block:: bash

      git add .

5. Commit:

   .. code-block:: bash

      git commit -m "Complete GPS navigation feature

      - Add waypoint navigation configuration
      - Set home coordinates for auto-return functionality
      - Update README with GPS feature documentation
      - Support up to 50 waypoints with 1-meter precision"

6. The feature is complete, merge back to ``main``:

   .. code-block:: bash

      git switch main
      git merge --no-ff feature/gps-navigation

   Git opens your editor with a one-line default,
   ``Merge branch 'feature/gps-navigation'``, which says nothing a
   reader could not already see. Replace it:

   .. code-block:: text

      Merge feature/gps-navigation into main

      Brings GPS receiver support and waypoint navigation into the
      fleet configuration:

      - gps block: receiver on /dev/ttyUSB0 at 9600 baud, 5s fix timeout
      - waypoints block: up to 50 per mission, 1 m arrival precision,
        and home coordinates for auto-return

      navigation.update_rate goes from 10Hz to 8Hz on main. The 11:30
      hotfix raised it to 10Hz for responsiveness; the GPS work needed a
      lower rate so each fix has time to settle. 8Hz is the value agreed
      when this branch merged the hotfix at 12:30.

      Merged with --no-ff so the feature branch stays visible in the
      history.

   .. note::

      The third paragraph is the one that earns its place. Looking at
      ``main`` alone, ``update_rate`` drops from 10 to 8 and nothing
      explains why: the reasoning lives on a branch whose commits are
      easy to miss. A merge commit is the one place to record what a
      whole branch changed and what was traded away to get there.

      ``git merge --no-edit`` accepts the default message instead. That
      is reasonable for a small merge; it is not reasonable here.

   .. dropdown:: Why ``--no-ff`` here?
      :class-container: sd-border-info

      You already merged ``main`` into the feature branch when you
      resolved the conflict. That means ``main`` has no commits the
      feature branch is missing: ``main`` is an **ancestor** of the
      feature branch.

      When that is true, Git does not need to merge anything. It just
      slides the ``main`` pointer forward to the feature branch's tip.
      That is a **fast-forward**, and it leaves no record that a feature
      branch ever existed.

      ``--no-ff`` tells Git to create a merge commit anyway. The history
      then shows where the feature started and where it landed, which is
      what you want for a reviewable unit of work.

      .. list-table::
         :widths: 30 70
         :header-rows: 1
         :class: compact-table

         * - Result
           - When you get it
         * - Fast-forward
           - The target branch has no commits of its own since the
             branch point. No merge commit is created.
         * - Merge commit
           - Both branches moved on independently, **or** you passed
             ``--no-ff``.

7. Clean up feature branch.

   .. code-block:: bash

      git branch -d feature/gps-navigation


.. figure:: /_static/images/version_control/git-graph-final.png
   :alt: Final git graph after the feature is merged into main
   :align: center
   :width: 100%

   The feature branch label is gone, but its commits ``B``, ``D``,
   and ``E`` are still in history. ``main`` now points at the final
   merge commit ``F``. Nothing is lost.


Reading History
----------------------------------------------------


Four commands answer almost every "what happened here?" question.

.. list-table::
   :widths: 42 58
   :header-rows: 1
   :class: compact-table

   * - Command
     - Question it answers
   * - ``git log --oneline --graph --all``
     - What is the shape of the history?
   * - ``git show <hash>``
     - What exactly did that one commit change?
   * - ``git blame <file>``
     - Who last touched each line, and in which commit?
   * - ``git log -p <file>``
     - How did this one file change over time?

**Who changed this line, and why?**

``git blame`` puts a commit hash, an author, and a date in front of every
line of a file:

.. code-block:: bash

   git blame robot_config.yaml

.. code-block:: text

   4f7a2e9c (You  2026-09-14 12:47:11 -0400  8)   update_rate: 8
   9f8e7d6c (You  2026-09-14 09:12:03 -0400  9)   coordinate_system: "WGS84"

That gives you a hash. Feed the hash to ``git show`` to see the whole
change and, more importantly, the message explaining it:

.. code-block:: bash

   git show 4f7a2e9c

.. tip::

   Six weeks from now, ``git blame`` points somebody at your commit and
   they read your message to find out why the value is 8 and not 10.
   "fixed
   stuff" will not help them.

**Searching history for a string:**

.. code-block:: bash

   git log -S "update_rate" --oneline   # commits that added or removed it
   git log --grep "hotfix" --oneline    # commits whose message mentions it


5:00 End of Day Review
----------------------------------------------------


.. admonition:: **5:00 PM** · End of Day Review
   :class: vc-stage

   You review your day's work.

1. View complete project history.

   .. code-block:: bash

      git log --oneline --graph --all

2. Check final file status.

   .. code-block:: bash

      git status

3. View the complete configuration file: ``cat robot_config.yaml``
4. Create a summary of what was accomplished.

   .. code-block:: bash

      git log --oneline --since="1 day ago"

5. View detailed changes for the day. Copy the short hash of your first
   commit of the day out of ``git log --oneline``, then:

   .. code-block:: bash

      git diff <that-hash>..HEAD --stat

.. note::

   Many Git commands are available directly within Visual Studio Code,
   typically located in the **Source Control** view or through the
   **Command Palette**.


Git: Writing Good History
====================================================


.. _vc-commit-well:

How to Commit Well
----------------------------------------------------


Two students did the same day's work. These are the resulting
histories.

.. code-block:: text

   # Student A
   * 8f2a1c9 end of day

   # Student B
   * 4c1d8ab Add bounds check to waypoint indexing
   * 9b3e772 Extract distance maths into navigation::euclidean()
   * 2a7f109 Shorten GPS timeout from 30s to 5s
   * e81c4d5 Add unit tests for waypoint parsing

Same code at the end. Very different repositories.

On Thursday the robot starts driving past its waypoints. Student B runs
``git log``, sees ``2a7f109``, and thinks "the timeout". One
``git revert 2a7f109`` and the robot behaves again, with the other three
changes untouched.

Student A has one commit containing everything. Reverting it throws away
the bounds check, the refactor and the tests as well. So they do not
revert it, they debug by hand instead, and the day is gone.

**Commit as you go, not at the end of the day.** A commit is the unit
Git can undo, review, and search. Oversized commits remove the ability
to perform any of those operations on part of the work.


One Commit, One Change
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The test is the message. **Write the subject line first. If you need the
word "and", you have two commits.**

.. code-block:: text

   Add waypoint bounds check and fix the GPS timeout and tidy up
                             ^^^                  ^^^

Three changes wearing one hat. Split them. If you have already made the
edits, ``git add -p`` walks through your changes one hunk at a time so
you can stage the bounds check by itself, commit it, then stage the
timeout fix.

A good commit is one you could explain in a sentence and undo on its own.


Writing the Message
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


A commit message has a **subject line**, then a blank line, then an
optional **body**.

.. code-block:: text

   Shorten GPS timeout from 30s to 5s

   The 30s default was inherited from the indoor test rig, where the
   robot had no GPS at all and the timeout never fired. Outdoors the
   fix takes about 2s, so a 30s timeout meant the navigation stack
   waited half a minute before falling back to dead reckoning.

   5s leaves headroom over the measured 2s without stalling the
   fallback. Measured on the test robot on the loading dock, 20 runs.

The subject says what changed. The body says **why**, which is the part
the diff cannot tell you. Anyone can see that a 30 became a 5. Nobody
can see that you measured it, or what it was doing there in the first
place.

Two widely used conventions:

**Write the subject in the imperative.** It should complete this
sentence: *"If applied, this commit will ..."*.

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - Write this
     - Not this
   * - ``Add bounds check to waypoint indexing``
     - ``Added bounds check``
   * - ``Fix GPS timeout on cold start``
     - ``Fixes the gps timeout``
   * - ``Remove unused sensor_config.yaml``
     - ``removing old file``

Git writes its own messages in the imperative, so ``Merge branch
'main'`` and ``Revert "Add bounds check"`` appear in the same log as
yours. Matching the convention keeps the log consistent.

**Keep the subject to about 50 characters, with no full stop.** Tools
truncate it: ``git log --oneline``, GitHub's commit list, and the pull
request title all show the subject alone.


Good and Bad Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. list-table::
   :widths: 36 64
   :header-rows: 1
   :class: compact-table

   * - Message
     - Verdict
   * - ``fixed stuff``
     - Fixed what? Every commit fixes stuff.
   * - ``update``
     - Says nothing at all. So does ``changes``, ``wip`` and ``asdf``.
   * - ``final``
     - Carries no information, and is typically followed by
       ``final2``.
   * - ``end of day``
     - Describes when you committed, not what you changed.
   * - ``Fix bug``
     - Which bug? Name the symptom.
   * - ``Fix crash when waypoint list is empty``
     - Good. Names the symptom and the condition.
   * - ``Add battery voltage monitoring for the 6S pack``
     - Good. You could find this again in six weeks.
   * - ``Revert "Shorten GPS timeout" pending outdoor retest``
     - Good. Says what and why in one line.

.. warning::

   Repeated ``git commit -m "wip"`` produces a history that cannot be
   read later, including by its author. For work that is genuinely
   unfinished, use :ref:`git stash <vc-stash>` or a feature branch. An
   unfinished commit on a branch with a descriptive message is fine.


When to Commit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


"As you go" is vague, so here are the actual triggers. Commit when:

- **A test passes.** The obvious one. The code works and you can say
  what it does.
- **One logical piece works**, even if the feature is not done. A parser
  that parses is a commit, whether or not the thing using it exists yet.
- **Before you try something risky.** Commit the working version first,
  then experiment. If it goes badly you have ``git restore`` and an
  actual point to return to.
- **Before you stop for the day.** On a branch, with a real message,
  even if unfinished. Not one commit *for* the day.
- **Before you switch tasks.** Half-done work you will not touch for
  three days should be a commit, not a stash.

A rough calibration: on an assignment, if a work session produced no
commits, something is wrong. If it produced thirty, they are probably
too small to be meaningful.

.. admonition:: What this looks like in a graded repository
   :class: important

   Your commit history is visible to whoever grades your work, and it
   answers questions the final code cannot: did this person build it in
   pieces, or paste it in at once? Did they test as they went?

   A repository whose entire history is one commit called ``final``,
   pushed two hours before the deadline, is a weak submission even when
   the code is correct. It is also a slow one to debug, because you gave
   yourself nothing to bisect.

   This matters most in the group projects. Small commits make pull
   requests readable, and readable pull requests receive real review
   rather than unread approval.


.. _vc-stash:

Parking Work with ``git stash``
----------------------------------------------------


Half-finished work is normal. Git will not always let you walk away from
it: if switching branches would overwrite your edits, Git refuses.

.. code-block:: text

   error: Your local changes to the following files would be overwritten by checkout:
       robot_config.yaml
   Please commit your changes or stash them before you switch branches.
   Aborting

You have three ways out: commit the half-finished work, throw it away, or
**stash** it. Stashing lifts your uncommitted changes off the working
tree, stores them, and leaves you with a clean checkout.

.. code-block:: bash

   git stash push -m "half-done waypoint block"   # park the work
   git switch main                                # now this works
   # ... deal with the interruption ...
   git switch feature/waypoints
   git stash pop                                  # bring the work back

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - Command
     - What it does
   * - ``git stash push -m "msg"``
     - Parks tracked modifications and cleans the working tree.
   * - ``git stash push -u -m "msg"``
     - Also parks **untracked** files. Without ``-u`` they stay behind.
   * - ``git stash list``
     - Shows the parked entries, newest first (``stash@{0}``).
   * - ``git stash show -p stash@{0}``
     - Shows what is inside an entry before you restore it.
   * - ``git stash pop``
     - Restores the newest entry and removes it from the list.
   * - ``git stash apply stash@{1}``
     - Restores an older entry and **keeps** it in the list.
   * - ``git stash drop stash@{0}``
     - Throws an entry away.

.. warning::

   A stash is a scratch pad, not a backup.

   - Stashes are local. They are never pushed, so they are not a way to
     move work between machines or teammates.
   - Stashes have no branch and no message unless you give them one.
     Three unlabeled stashes from last week are indistinguishable.
   - ``git stash pop`` can itself produce a conflict, if the branch moved
     while your work was parked.

   For anything you cannot afford to lose, commit it on a branch
   instead. A commit remains recoverable and carries a message, a branch
   and a position in the history. An unlabeled stash carries none of
   these.


Git: Recovering from Mistakes
====================================================


Everything so far has worked first time. Real Git use is not like that.
This section is the one you will come back to.

There is a single question that picks the right command:
**where is the change you want to undo?** Every answer maps to one of the
three areas, plus a fourth case for changes you have already shared.

.. list-table::
   :widths: 34 30 36
   :header-rows: 1
   :class: compact-table

   * - Where the change is
     - Command
     - What happens
   * - Working directory, not staged
     - ``git restore <file>``
     - The file goes back to the last committed version.
   * - Staged, not committed
     - ``git restore --staged <file>``
     - Unstaged. Your edits stay on disk.
   * - Committed, not pushed
     - ``git commit --amend``
     - The last commit is replaced by a new one.
   * - Committed **and** pushed
     - ``git revert <hash>``
     - A new commit undoes the old one. History is untouched.

.. danger::

   The line between rows three and four is the most important line in
   Git. ``--amend``, ``reset`` and ``rebase`` all **rewrite** history:
   they replace commits with different ones. That is harmless on commits
   only you have, and hostile on commits other people have already
   pulled, because their history and yours no longer agree.

   **The rule:** rewrite freely before you push. After you push, undo
   with ``git revert``.


Undoing Uncommitted Work
----------------------------------------------------


.. code-block:: bash

   git restore robot_config.yaml     # discard edits to one file
   git restore .                     # discard all edits in this directory
   git restore --staged robot.log    # unstage, keep the edits on disk
   git restore --staged --worktree robot_config.yaml   # unstage AND discard

.. warning::

   ``git restore <file>`` deletes work that Git has never seen. There is
   no undo for it and no reflog entry. Check ``git diff`` first.


Fixing the Last Commit
----------------------------------------------------


You committed, then noticed the typo in the message, or that you forgot a
file. As long as you have **not pushed**, fix it in place:

.. code-block:: bash

   git commit --amend                       # reword the message in the editor
   git commit --amend -m "Better message"   # reword in one line

   git add forgotten_file.cpp               # forgot a file?
   git commit --amend --no-edit             # fold it in, keep the message

``--amend`` does not edit the old commit. It builds a replacement and
moves the branch pointer to it. The original is still in the reflog, but
for everyone else it has simply been swapped out, which is why this is
safe only before pushing.


Undoing a Commit You Have Pushed
----------------------------------------------------


Once teammates have pulled a commit, you may not remove it. You add a new
commit that reverses it:

.. code-block:: bash

   git log --oneline                 # find the bad commit's hash
   git show 0f7c291                  # confirm it is the right one
   git revert 0f7c291                # create a commit that undoes it
   git push

``git revert`` opens an editor with a prepared message. The bad commit
stays in the history, and so does the commit that undid it. The record
is complete, and no action is required from anyone else.

.. note::

   Reverting a **merge** commit needs ``-m 1`` to say which parent to
   treat as the mainline, for example ``git revert -m 1 <hash>``. If you
   need this, read ``git revert --help`` first rather than guessing.


``git reset``: the Three Flavors
----------------------------------------------------


``git reset`` moves the current branch pointer to a different commit. The
flag decides what happens to your files.

.. list-table::
   :widths: 26 74
   :header-rows: 1
   :class: compact-table

   * - Flag
     - Effect on the staging area and your files
   * - ``--soft``
     - Both untouched. The changes from the discarded commits are left
       staged, ready to be recommitted differently.
   * - ``--mixed`` (default)
     - Staging area cleared, files untouched. Changes are back in the
       working directory as unstaged edits.
   * - ``--hard``
     - Both thrown away. Your files become exactly the target commit.

.. code-block:: bash

   git reset --soft HEAD~1    # undo the commit, keep everything staged
   git reset HEAD~1           # undo the commit, keep the edits unstaged
   git reset --hard HEAD~1    # undo the commit and destroy the edits

A common, legitimate use: you made three messy commits that should have
been one.

.. code-block:: bash

   git reset --soft HEAD~3            # roll the branch back three commits
   git commit -m "Add GPS waypoint support"   # recommit as one

.. danger::

   Do not run ``git reset --hard`` on commits you have pushed. Your
   teammates' histories still contain the commits you deleted, and their
   next ``git pull`` reintroduces them. Use ``git revert`` on anything
   that has been pushed.


.. _vc-reflog:

``git reflog``: the Undo History
----------------------------------------------------


Deleted the wrong branch? Ran ``git reset --hard`` and regretted it?
Commits are almost never gone immediately. Git records **every** position
``HEAD`` has held, including the ones no branch points at any more.

.. code-block:: bash

   git reflog

.. code-block:: text

   c3c0e33 HEAD@{0}: checkout: moving from feature/battery-monitor to main
   46fa602 HEAD@{1}: commit: Enable the battery monitor in the configuration
   31bfa20 HEAD@{2}: commit: Add battery voltage monitoring
   c3c0e33 HEAD@{3}: checkout: moving from main to feature/battery-monitor

The work you thought you lost is at ``46fa602``. Put a branch back on it:

.. code-block:: bash

   git branch feature/battery-monitor 46fa602
   git switch feature/battery-monitor

The same trick undoes a bad reset: find the hash you were on before, then
``git reset --hard <hash>``.

.. note::

   The reflog is **local to your clone** and it expires (unreachable
   entries default to 30 days). It cannot rescue a colleague's mistake,
   and it is not a backup strategy. It is a safety net for the last few
   weeks of your own work.

.. admonition:: The two-minute version
   :class: tip

   - Wrong edits, not staged: ``git restore <file>``
   - Staged the wrong file: ``git restore --staged <file>``
   - Bad message on the last commit: ``git commit --amend``
   - Bad commit, not pushed: ``git reset --soft HEAD~1``
   - Bad commit, pushed: ``git revert <hash>``
   - Commits appear to be lost entirely: ``git reflog``

.. seealso::

   Reading about recovery is not the same as having done it once. The
   :doc:`vc_exercises` page ends with **Live Workshop: The Broken
   Repository**, a script that drops you into seven repositories that
   are already broken (detached ``HEAD``, a half-finished merge, a
   deleted branch, a pushed mistake) and asks you to get each one out.
   Every one of them is solved with a command from this section.


GitHub: Getting Started
====================================================


GitHub is a cloud-based platform that hosts Git repositories online. It
adds features like:

- Remote storage for your projects.
- Collaboration tools.
- Issue tracking.
- Project management features.
- Portfolio showcase for your work.


Creating an Account and an SSH Key
----------------------------------------------------


1. **Create a GitHub account.**

   - Go to `github.com <https://github.com/>`_.
   - Sign up with your university email.
   - Verify your email address.

2. **Set up SSH authentication.**

   - Generate a new SSH key:

     .. code-block:: bash

        ssh-keygen -t ed25519 -C "your.email@university.edu"

   - Copy the public key to your clipboard:

     .. tab-set::

        .. tab-item:: Linux

           .. code-block:: bash

              sudo apt install xclip
              xclip -sel clip < ~/.ssh/id_ed25519.pub

        .. tab-item:: macOS

           .. code-block:: bash

              pbcopy < ~/.ssh/id_ed25519.pub

        .. tab-item:: Windows (Git Bash)

           .. code-block:: bash

              clip < ~/.ssh/id_ed25519.pub

   - Add the key to GitHub:

     1. Go to **GitHub** -> **Settings** -> **SSH and GPG keys** ->
        **New SSH key**.
     2. Paste the key (``Ctrl + V``) and click **Add SSH key**.

   .. note::

      - The ``-t`` flag selects the cryptographic algorithm.
        ``ed25519`` is a modern, fast, and highly secure
        elliptic-curve algorithm recommended for new SSH keys.
      - The ``-C`` flag adds a label to help you identify the key
        later. GitHub matches the **key itself**, not the comment.


Check That It Works
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Do not wait until your first ``git push`` to find out whether the key
works. Ask GitHub directly:

.. code-block:: bash

   ssh -T git@github.com

A working setup answers like this:

.. code-block:: text

   Hi yourusername! You've successfully authenticated, but GitHub does not
   provide shell access.

This is a success message, not a rejection. GitHub does not provide
shell access to anyone. The phrase "successfully authenticated"
confirms the key works.

.. dropdown:: ``Permission denied (publickey)``
   :class-container: sd-border-warning

   GitHub does not recognize your key. Work through these in order:

   1. **Does the key exist?**

      .. code-block:: bash

         ls -l ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub

      Nothing there means ``ssh-keygen`` never ran, or ran somewhere
      else. Generate it again.

   2. **Did you paste the public key, not the private one?** GitHub
      needs ``id_ed25519.pub``, the one ending in ``.pub``. The file
      without ``.pub`` is private and must never leave your machine.

   3. **Is the key loaded?**

      .. code-block:: bash

         eval "$(ssh-agent -s)"
         ssh-add ~/.ssh/id_ed25519

   4. **Are the permissions too open?** SSH refuses keys that other
      users could read.

      .. code-block:: bash

         chmod 700 ~/.ssh
         chmod 600 ~/.ssh/id_ed25519

   5. **Still stuck?** Ask SSH what it is trying:

      .. code-block:: bash

         ssh -vT git@github.com

.. dropdown:: ``fatal: Authentication failed`` or a password prompt
   :class-container: sd-border-warning

   Your remote is an HTTPS URL, not an SSH one, so Git is asking for a
   password. GitHub stopped accepting account passwords for Git
   operations in 2021: over HTTPS you need a **personal access token**
   instead.

   Check which one you have:

   .. code-block:: bash

      git remote -v

   ``https://github.com/...`` is HTTPS. ``git@github.com:...`` is SSH.
   Since your key is already set up, switch the remote over:

   .. code-block:: bash

      git remote set-url origin git@github.com:yourusername/robot-config.git

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * -
     - SSH
     - HTTPS
   * - Remote URL
     - ``git@github.com:user/repo.git``
     - ``https://github.com/user/repo.git``
   * - Proves who you are with
     - A key pair on your machine
     - A personal access token
   * - Set up
     - Once per machine
     - Token expires, then again
   * - Recommended here
     - **Yes**
     - Only if SSH is blocked by a firewall


Public vs. Private Repositories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. grid:: 2

   .. grid-item-card:: Public Repository

      - Anyone can view
      - Anyone can clone/download
      - Shows up in search engines
      - Others can star/follow
      - Completely open source

   .. grid-item-card:: Private Repository

      - Only you can view
      - Only invited collaborators can access
      - Hidden from search engines
      - Cannot be cloned by public
      - Perfect for private work


Connecting a Local Repository to GitHub
----------------------------------------------------


.. tab-set::

   .. tab-item:: Scenario 1: Local repo first
      :sync: scenario1

      You already have a local repository and want to push it to
      GitHub.

      1. Create an empty repository on GitHub: ``robot-config``

         - **IMPORTANT**: When creating on GitHub, **do not check**:

           - "Add a README file"
           - "Add .gitignore"
           - "Choose a license"

      2. Connect local repository to GitHub:

         - Add GitHub as remote origin:

           .. code-block:: bash

              git remote add origin git@github.com:yourusername/robot-config.git

         - Verify the remote was added: ``git remote -v``

      3. Push your local ``main`` branch to GitHub.

         .. code-block:: bash

            git push -u origin main


         - This command pushes your local ``main`` branch to the
           remote repository named ``origin``, and establishes a
           tracking relationship so that in the future you can simply
           use ``git push``.

      .. figure:: /_static/images/version_control/scenario-1-sequence.png
         :alt: Sequence diagram of Scenario 1 (local repo first)
         :align: center
         :width: 100%

         Scenario 1: create the empty GitHub repo, add it as a remote
         from your local repo, then push your existing history.

   .. tab-item:: Scenario 2: GitHub repo first
      :sync: scenario2

      You start by creating the repository on GitHub and then bring
      it down to your local machine.

      1. Create a repository on GitHub: ``new-project``

         - When creating on GitHub, check the following since you
           are starting fresh:

           - "Add a README file"
           - "Add .gitignore" (optional)
           - "Choose a license" (optional)

      2. Clone to your local machine:

         .. code-block:: bash

            git clone git@github.com:yourusername/new-project.git

            # Move into the directory
            cd new-project

            # Start working
            echo "# My New Project" >> README.md
            git add README.md
            git commit -m "Update README"
            git push origin main

      .. figure:: /_static/images/version_control/scenario-2-sequence.png
         :alt: Sequence diagram of Scenario 2 (GitHub repo first)
         :align: center
         :width: 100%

         Scenario 2: create the GitHub repo, clone it locally, work,
         then push. No ``git remote add`` or ``git push -u`` needed;
         ``git clone`` sets both up automatically.


GitHub: Everyday Workflow
====================================================


Staying in Sync with the Remote
----------------------------------------------------


Pushing your own work is the easy half. The interesting half is what
happens when somebody else pushed while you were working, which on a
group project is most of the time.

Before the commands, three names that look alike and are not:

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - Name
     - What it is
   * - ``main``
     - **Your** branch, in your clone. It moves when you commit.
   * - ``origin``
     - The nickname for the GitHub repository, set when you ran
       ``git remote add origin ...`` or when ``git clone`` did it for
       you. Nothing about the name is special; it is just the
       convention for "the repository I cloned from".
   * - ``origin/main``
     - A **remote-tracking branch**: a local, read-only pointer
       recording where ``main`` on ``origin`` was **the last time you
       fetched**.

``origin/main`` is not the remote itself. It is your clone's record of
the remote, and it updates
only when you run ``git fetch`` (or ``git pull``, which fetches first).
If you have not fetched since yesterday, ``origin/main`` is a day out
of date and nothing will warn you.

``git fetch`` on its own refreshes ``origin/main``, so you can inspect
what arrived without changing your branch or your files.

.. admonition:: Reading ``A..B``
   :class: note

   Two dots between two names mean "commits reachable from ``B`` but
   not from ``A``", which in practice reads as "what ``B`` has that
   ``A`` does not":

   .. code-block:: bash

      git log --oneline main..origin/main   # on the remote, not in my branch
      git log --oneline origin/main..main   # in my branch, not on the remote

   Swapping the two sides answers the opposite question. Run both
   before a merge.

Three commands, and the difference between them matters:

.. list-table::
   :widths: 28 72
   :header-rows: 1
   :class: compact-table

   * - Command
     - What it does
   * - ``git fetch``
     - Downloads new commits and updates ``origin/main``. Your branch
       and your files are **not** touched.
   * - ``git merge origin/main``
     - Merges what you downloaded into your current branch.
   * - ``git pull``
     - ``fetch`` followed by ``merge``, in one step.

``git pull`` is convenient and it is also how people get surprised. The
safer habit is to look before you leap:

.. code-block:: bash

   git fetch origin
   git log --oneline main..origin/main    # what they have that I do not
   git log --oneline origin/main..main    # what I have that they do not
   git diff main origin/main              # what actually differs
   git merge origin/main                  # now merge, knowing what is coming


When the Push Is Rejected
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   ! [rejected]        main -> main (fetch first)
   error: failed to push some refs to 'github.com:team/robot-project.git'
   hint: Updates were rejected because the remote contains work that you do
   hint: not have locally.

This is not an error in your repository. It means a teammate pushed
after you last pulled, so the remote has commits you have never seen.
Git refuses rather than silently discarding their work.

The fix is always the same shape: bring their work in, then push.

.. code-block:: bash

   git pull            # fetch + merge their commits into yours
   # resolve conflicts if there are any
   git push

.. danger::

   ``git push --force`` removes the rejection by **deleting your
   teammate's commits from the remote**. Never use it on a shared
   branch.

   If you genuinely need to force-push your own feature branch after
   rewriting it, use ``git push --force-with-lease``, which refuses if
   anyone else has pushed to that branch since you last fetched. On
   ``main``, the answer is simply no.


When Git Asks How to Reconcile
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The first time you ``git pull`` into a branch that has diverged, Git
stops and refuses to choose for you:

.. code-block:: text

   hint: You have divergent branches and need to specify how to reconcile them.
   hint:   git config pull.rebase false  # merge
   hint:   git config pull.rebase true   # rebase
   hint:   git config pull.ff only       # fast-forward only
   fatal: Need to specify how to reconcile divergent branches

Nothing is broken. Git wants to know what shape you want the history to
take. Set it once and never see this again:

.. code-block:: bash

   git config --global pull.rebase false     # merge: the course default

To see what the three settings actually do, start from the same
situation each time. You committed locally; a teammate pushed while you
were working:

.. code-block:: text

   * 984e031 (HEAD -> main) Widen the obstacle margin      <- yours, local
   | * 9c0ca2f (origin/main) Document the heartbeat timeout <- theirs, pushed
   |/
   * 0c169ac Initial commit                                <- where you split

Each setting resolves that fork differently.

**pull.rebase false: merge (the course default)**

Git makes a new commit joining the two lines:

.. code-block:: text

   *   fc57018 (HEAD -> main) Merge branch 'main' of origin
   |\
   | * 9c0ca2f Document the heartbeat timeout
   * | 984e031 Widen the obstacle margin
   |/
   * 0c169ac Initial commit

Both original commits survive untouched, including their hashes. The
fork stays visible, which is an accurate record of what happened: two
people worked at the same time. The cost is the extra merge commit, and
a busy project collects a lot of them.

**pull.rebase true: rebase**

Git sets your commit aside, fast-forwards to your teammate's, then
re-applies yours on top:

.. code-block:: text

   * 48a34c1 (HEAD -> main) Widen the obstacle margin
   * 9c0ca2f Document the heartbeat timeout
   * 0c169ac Initial commit

One straight line, no merge commit, and it reads as though you started
after your teammate finished. Look closely at the hash: your commit was
``984e031`` and is now ``48a34c1``. **It is not the same commit.** Git
built a new one with the same changes and a different parent, and threw
the original away. Their commit, ``9c0ca2f``, is untouched.

That is the whole risk of rebasing. Rewriting a commit only you have is
harmless. Rewriting one somebody else already pulled gives the two of
you different commits for the same work, and Git cannot tell they are
related.

**pull.ff only: refuse**

Git fetches, then stops rather than deciding for you:

.. code-block:: text

   hint: Diverging branches can't be fast-forwarded, you need to either:
   hint:   git merge --no-ff
   hint: or:
   hint:   git rebase
   fatal: Not possible to fast-forward, aborting.

Nothing is merged and your branch does not move. Note that the *fetch*
part still ran, so ``origin/main`` is now up to date even though your
branch is not: you can inspect what arrived before choosing. Then you
run ``git merge`` or ``git rebase`` yourself.

This is the strictest option and the most work. It suits people who want
to decide case by case, and it never surprises you.

.. list-table::
   :widths: 22 30 48
   :header-rows: 1
   :class: compact-table

   * - Setting
     - Shape
     - Your commits
   * - ``pull.rebase false``
     - Fork preserved, merge commit added
     - Kept exactly, same hashes
   * - ``pull.rebase true``
     - One straight line
     - **Rebuilt with new hashes**
   * - ``pull.ff only``
     - Unchanged; nothing happens
     - Kept, and you choose what happens next

**Use** ``merge`` **for this course.** It never rewrites a commit, so it
cannot put you and a teammate out of step, and the merge commits it
leaves behind are a truthful record rather than clutter.


Rebase and Its One Rule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Merging joins two histories with a merge commit. **Rebasing** takes your
commits, sets them aside, fast-forwards your branch to the other tip, and
replays your commits on top. The result reads as if you had started your
work after their work landed.

.. code-block:: bash

   git switch feature/gps-navigation
   git fetch origin
   git rebase origin/main       # replay my commits on top of theirs

.. grid:: 2

   .. grid-item-card:: Merge
      :class-card: sd-border-info

      - Never changes existing commits.
      - History shows what really happened, including the branching.
      - Always safe.
      - Many merge commits make ``git log`` noisy.

   .. grid-item-card:: Rebase
      :class-card: sd-border-info

      - Creates **new** commits with new hashes.
      - History is a straight line and easy to read.
      - Conflicts can come back once per replayed commit.
      - Dangerous on anything already shared.

.. danger::

   **The golden rule of rebasing: never rebase commits that other
   people already have.**

   Rebasing replaces commits with new ones that have different hashes.
   For you the result looks tidy. For anyone who already pulled the old
   commits, their Git now sees two versions of the same work and the
   next pull tangles them together.

   Rebase your own unpushed work as much as you like. Once it is on a
   shared branch, merge.

For ENPM702, use merges. Rebase is listed here so you recognize it, and
so that when a teammate proposes it you know which question to ask:
"has anyone pulled this branch yet?"


Tagging a Submission
----------------------------------------------------


A branch pointer moves every time you commit. A **tag** does not: it
names one specific commit permanently. That makes tags the right way to
mark "this is the version I am submitting".

.. code-block:: bash

   git tag -a rwa1-final -m "RWA1 submission"   # tag the current commit
   git push origin rwa1-final                   # tags are not pushed by git push

Useful follow-ups:

.. code-block:: bash

   git tag                        # list tags
   git show rwa1-final            # what commit is it, and what is in it
   git tag -a rwa2-final -m "..." 9f8e7d6    # tag an older commit by hash
   git push origin --tags         # push all tags at once

.. note::

   ``-a`` creates an **annotated** tag: a real object with your name, the
   date, and a message. Without ``-a`` you get a lightweight tag, which
   is just a name. Use ``-a`` for anything you submit or release, so the
   record says who tagged it and when.

On GitHub, a tag shows up under **Releases**, where anyone can download
that exact snapshot as a zip. If the grading instructions ask for a
commit hash or a tag, this is the mechanism they mean: it pins the
graded version, so work you push afterwards cannot change what was
submitted.


GitHub: Collaborating
====================================================


When working with teams, you need to choose between **branching** and
**forking** workflows. The choice depends on your team structure and
project permissions.

.. grid:: 2

   .. grid-item-card:: Branch Workflow (Private Repo)

      **Use when:** You have write access to the repository (team
      member, collaborator).

      - Direct access to main repository.
      - Simpler workflow for team members.
      - Better for small to medium teams.
      - Easier to manage releases.

   .. grid-item-card:: Fork Workflow (Public Repo)

      **Use when:** You do not have write access (open source
      contributor, external collaborator).

      - Works without write permissions.
      - Safe for open source projects.
      - Each contributor has complete copy.
      - Maintainers control what gets merged.


Branch Workflow
----------------------------------------------------


.. figure:: /_static/images/version_control/branch-workflow.png
   :align: center
   :width: 100%

   Branch workflow diagram.

1. Clone the main repository.

   .. code-block:: bash

      git clone git@github.com:team/robot-project.git
      cd robot-project

2. Create feature branch.

   .. code-block:: bash

      git switch -c feature/sensor-integration

3. Work on your changes.

4. Commit and push to shared repository.

   .. code-block:: bash

      git add .
      git commit -m "Add ultrasonic sensor integration"
      git push origin feature/sensor-integration

5. Create Pull Request on GitHub: After review and approval, merge to
   main.

**Repository Structure:**

::

   main repository: team/robot-project
       main branch
       feature/sensor-integration (your branch)
       feature/camera-module (teammate's branch)
       hotfix/battery-issue (another branch)


Fork Workflow
----------------------------------------------------


.. figure:: /_static/images/version_control/fork-workflow.png
   :align: center
   :width: 100%

   Fork workflow diagram.

The repository used for this walkthrough is
`rubixcubic/enpm702-fall-2026-fork-demo
<https://github.com/rubixcubic/enpm702-fall-2026-fork-demo>`__.
It is deliberately small, since it exists to demonstrate the workflow
rather than the code:

.. code-block:: text

   enpm702-fall-2026-fork-demo/
   |
   |-- .gitignore
   |-- LICENSE                    Apache-2.0
   |-- README.md                  what the repository is for
   |
   |-- contributors/              one file per person: no two PRs collide
   |   |-- README.md              what to add and how to name it
   |   `-- TEMPLATE.md            copy this, rename it to your username
   |
   `-- demo/
       `-- robot_config.yaml      the shared file used for the live conflict

Two directories, two jobs:

.. list-table::
   :widths: 24 76
   :header-rows: 1
   :class: compact-table

   * - Directory
     - Why it is shaped this way
   * - ``contributors/``
     - Your pull request adds **one new file**, named after your GitHub
       username. Nobody else touches that file, so every pull request
       merges cleanly no matter what order they arrive in.
   * - ``demo/``
     - A single file that everyone shares, used only in the live demo.
       Two people editing the same line is how you make a conflict on
       purpose. Do not put your contribution here.

.. note::

   Most merge conflicts are not caused by difficult problems. They are
   caused by two people editing the same line. A repository laid out so
   that contributions land in separate files produces far fewer. Think
   about this when you set up your GP repository: split the work by
   file, and your team spends its time on code instead of on conflict
   markers.

1. **Fork** the repository on GitHub (this creates your own copy, see
   `fork a repo <https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo>`__).

   - *Original*: ``rubixcubic/enpm702-fall-2026-fork-demo.git``

   - *Your fork*: ``yourusername/enpm702-fall-2026-fork-demo.git``

2. Clone **your** fork.

   .. code-block:: bash

      git clone git@github.com:yourusername/enpm702-fall-2026-fork-demo.git
      cd enpm702-fall-2026-fork-demo

3. Add original repository as upstream.

   .. code-block:: bash

      git remote add upstream https://github.com/rubixcubic/enpm702-fall-2026-fork-demo.git
      git remote -v
      # origin    git@github.com:yourusername/enpm702-fall-2026-fork-demo.git (your fork)
      # upstream  https://github.com/rubixcubic/enpm702-fall-2026-fork-demo.git (original)

.. figure:: /_static/images/version_control/fork-demo-setup.png
   :alt: Fork demo, setup phase (fork, clone, add upstream)
   :align: center
   :width: 100%

   Setup phase: fork the original repository on GitHub, clone your
   fork to your machine, then add the original repository as the
   ``upstream`` remote.

4. Create feature branch.

   .. code-block:: bash

      git switch -c feature/new-algorithm


5. Work on your changes.

6. Commit and push to **your** fork.

   .. code-block:: bash

      git add .
      git commit -m "Implement new pathfinding algorithm"
      git push origin feature/new-algorithm

7. Create Pull Request from your fork to original repository.

.. figure:: /_static/images/version_control/fork-demo-contribute.png
   :alt: Fork demo, branch, commit, push, open PR
   :align: center
   :width: 100%

   Contribution phase: create a feature branch, commit your changes,
   push the branch to your fork, then open a pull request from your
   fork to the original repository.


Live Demo: Two People Required
----------------------------------------------------


Everything above can be read alone. It cannot be **shown** alone. A pull
request has two sides, and one person cannot be on both at once:

.. grid:: 2

   .. grid-item-card:: Maintainer
      :class-card: sd-border-info

      Owns the original repository. Receives the pull request, reads the
      diff, leaves a comment, asks for a change, then merges. Never sees
      the contributor's terminal.

   .. grid-item-card:: Contributor
      :class-card: sd-border-info

      Owns a fork. Branches, commits, pushes, opens the pull request,
      responds to the review, pushes again. Never has write access to
      the original repository.

.. admonition:: Volunteer wanted
   :class: important

   **One student volunteers and plays the contributor.** The instructor
   plays the maintainer. Both screens go up side by side, so the class
   watches a change travel from one machine to the other and back
   again.

   To volunteer you need, **before the session starts**:

   - A GitHub account, signed in on the machine you will use.
   - SSH working: ``ssh -T git@github.com`` answers "Hi *yourusername*!
     You've successfully authenticated".
   - Git configured with your name and email (check ``git config
     --list``).

   Nothing else. No code is written during the demo, and mistakes made
   during it are useful teaching material.

**What the two of you will do:**

.. list-table::
   :widths: 5 19 38 38
   :header-rows: 1
   :class: compact-table

   * - \#
     - Step
     - Contributor (volunteer)
     - Maintainer (instructor)
   * - 1
     - Fork
     - Clicks **Fork**, clones the fork, adds ``upstream``.
     - Shows the fork appearing under the volunteer's account.
   * - 2
     - Branch and commit
     - ``git switch -c feature/add-<username>``, adds
       ``contributors/<username>.md``, commits.
     - Shows that the original repository has not changed at all.
   * - 3
     - Push and open the PR
     - ``git push origin feature/add-<username>``, then opens the pull
       request from the fork.
     - The pull request appears. Reviews the diff with the class.
   * - 4
     - Review
     - Waits, and watches the comment arrive.
     - Leaves a review comment asking for one small change.
   * - 5
     - Respond
     - Edits, commits, pushes to the **same branch**.
     - The pull request updates itself. No second PR needed.
   * - 6
     - Merge
     - Nothing to do.
     - Merges, then deletes the branch on GitHub.
   * - 7
     - Sync
     - ``git fetch upstream``, ``git switch main``,
       ``git merge upstream/main``. Their own commit comes back down.
     - Shows the commit now in the original's history.
   * - 8
     - A conflict, on purpose
     - Edits ``demo/robot_config.yaml`` and opens a second pull
       request.
     - Has already changed the same line on ``main``. GitHub reports
       the conflict, and the volunteer resolves it on their fork.

.. tip::

   Step 5 demonstrates an important detail: a review does not require a
   new pull request. A pull request tracks a **branch**, so every push
   to that branch updates the same pull request, keeping the discussion
   in one place.

.. note::

   Nothing here can break anything. The volunteer has no write access
   to the original repository, which is the entire point of the fork
   workflow. The worst case is a pull request that gets closed.


Keeping Your Fork Updated
----------------------------------------------------


1. Fetch latest changes from the original repository.

   .. code-block:: bash

      git fetch upstream

   This downloads their commits and updates ``upstream/main``. Your
   branch and your files are untouched, so there is nothing to undo.

2. **Look at what arrived, before merging it.**

   .. code-block:: bash

      git log --oneline main..upstream/main

   Everything the original repository has that your ``main`` does not:
   typically the pull requests merged since you last synced, including
   your own. The reverse direction should normally print nothing,
   because your own work belongs on feature branches rather than on
   ``main``:

   .. code-block:: bash

      git log --oneline upstream/main..main

   If that second command *does* list commits, you have work on ``main``
   that the original repository has never seen. Move it to a branch
   before going any further.

3. Switch to your main branch.

   .. code-block:: bash

      git switch main

4. Merge the upstream changes into your local ``main``.

   .. code-block:: bash

      git merge upstream/main

5. Push the updated ``main`` to your fork.

   .. code-block:: bash

      git push origin main

6. Create new feature branches from the updated ``main``.

   .. code-block:: bash

      git switch -c feature/next-feature

.. figure:: /_static/images/version_control/fork-demo-merged.png
   :alt: Fork demo, after the maintainer merges the PR
   :align: center
   :width: 100%

   After the maintainer merges your pull request into the original
   repository, sync your local ``main`` using the steps above, then push
   to your fork to keep everything aligned.

**Repository Structure:**

::

   Original: rubixcubic/enpm702-fall-2026-fork-demo (upstream)
       main branch

   Your Fork: yourusername/enpm702-fall-2026-fork-demo (origin)
       main branch (synced with upstream)
       feature/new-algorithm (your work)


When to Use Each Approach
----------------------------------------------------


.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **Scenario**
     - **Recommended Approach**
   * - Team member with repository access
     - Branch Workflow
   * - Contributing to open source project
     - Fork Workflow
   * - External contractor/collaborator
     - Fork Workflow
   * - Company internal project
     - Branch Workflow
   * - Public project accepting contributions
     - Fork Workflow
   * - Small team (< 10 people)
     - Branch Workflow
   * - Large community project
     - Fork Workflow


Best Practices
----------------------------------------------------


.. admonition:: Best Practices
   :class: tip

   - **Clear branch naming**: ``feature/name``, ``bugfix/name``,
     ``hotfix/name``
   - **Regular commits**: small, focused commits with clear messages,
     made as you go rather than in one lump at the end. See
     :ref:`How to Commit Well <vc-commit-well>`.
   - **Pull requests**: Always use pull requests for code review.
   - **Stay updated**: Regularly sync with main branch/upstream.
   - **Test before merging**: Ensure changes do not break existing
     functionality.

**Action items:**

- Practice both workflows with your team.
- Set up proper branch protection rules.
- Establish team conventions for branch naming.
- Configure automated testing for pull requests.


.. _vc-protect:

Protecting the ``main`` Branch
----------------------------------------------------


"Always use pull requests" is a promise your team will break under
deadline pressure. Make it a setting instead, so the repository enforces
it. Do this once, at the start of each group project, before anyone
writes code.

On GitHub: **Settings** -> **Branches** -> **Add branch ruleset** (older
repositories say **Add rule**), targeting ``main``:

.. list-table::
   :widths: 45 55
   :header-rows: 1
   :class: compact-table

   * - Setting
     - Why
   * - Require a pull request before merging
     - Nothing lands on ``main`` without review.
   * - Required approvals: **1**
     - One teammate must actually read it. On a team of four, more than
       one approval stalls the project.
   * - Dismiss stale approvals on new commits
     - An approval covers the code that was approved, not whatever gets
       pushed afterwards.
   * - Block force pushes
     - Nobody can rewrite shared history, even by accident.
   * - Restrict deletions
     - ``main`` cannot be deleted.

.. note::

   Do not enable "Require status checks" until your project actually has
   a build running on GitHub Actions. A required check that never reports
   blocks every pull request permanently.

.. warning::

   Branch protection applies to everyone, including the person who
   created the repository. If your team decides one member should be
   able to merge without review, agree on that
   explicitly and change the setting, rather than working around it.


Pull Requests
----------------------------------------------------


A Pull Request (PR) is a method of submitting contributions to a
project. It allows you to tell others about changes you have pushed to
a branch in a repository.

**Why Use Pull Requests?**

- **Code Review**: Team members can review changes before merging.
- **Discussion**: Collaborate and discuss proposed changes.
- **Testing**: Automated tests run on proposed changes.
- **Quality Control**: Maintain code standards and catch bugs.
- **Documentation**: Track what changes were made and why.

**Basic Workflow:**

.. code-block:: bash

   git switch -c feature/add-lidar-support
   # Make changes, add, commit
   git push origin feature/add-lidar-support
   # Create PR on GitHub -> Review -> Merge -> Delete branch


Creating a Good Pull Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: text

   Title: Add LiDAR sensor integration for obstacle detection

   ## What this PR does
   - Adds support for Velodyne VLP-16 LiDAR sensor
   - Implements point cloud processing for obstacle detection
   - Updates robot configuration with LiDAR parameters

   ## Testing
   - [x] Unit tests pass
   - [x] Integration tests with physical sensor

   ## Related Issues
   Fixes #123: Robot needs better obstacle detection

.. admonition:: Best Practices for PRs
   :class: tip

   - Use clear, descriptive titles and explain WHAT and WHY.
   - Include testing information and link to related issues.
   - Keep PRs focused and reasonably sized (< 400 lines).
   - Use "Draft PR" for work-in-progress to get early feedback.


PR Merge Strategies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. grid:: 3

   .. grid-item-card:: Merge Commit

      - Preserves branch history
      - Shows when merged
      - Can create "bubbles"

   .. grid-item-card:: Squash and Merge

      - Combines all commits
      - Cleaner history
      - **Recommended**

   .. grid-item-card:: Rebase and Merge

      - Linear history
      - Preserves commits
      - Advanced technique

.. warning::

   **Common Mistakes to Avoid:**

   - Mixing unrelated changes in one PR.
   - Vague descriptions or poor commit messages.
   - Not testing before submitting.
   - Ignoring review feedback or force-pushing after reviews.
   - Committing sensitive data (passwords, keys).

Set up branch protection rules requiring reviews before merging.


Pull Request Reviews
----------------------------------------------------


Pull request (PR) reviews are crucial for maintaining code quality and
knowledge sharing.

**Review Process:**

1. **Pre-Review Checklist** (2 minutes)

   - Check CI/CD status and understand context.
   - Verify no merge conflicts, correct target branch.

2. **High-Level Review** (5-10 minutes)

   - Architecture fit, security implications, overall approach.

3. **Detailed Review** (15-30 minutes)

   - Logic, code quality, performance, testing.


Reference and Course Rules
====================================================


.. _vc-quickref:

Quick Reference
----------------------------------------------------


A compact card with the commands you will use most often. See
:doc:`vc_references` for links to the official Git documentation.

.. grid:: 2

   .. grid-item-card:: Inspecting State

      .. code-block:: bash

         git status              # Working/staging state
         git log --oneline       # Compact history
         git diff                # Unstaged changes
         git diff --staged       # Staged changes

   .. grid-item-card:: Staging & Committing

      .. code-block:: bash

         git add <file>          # Stage specific file
         git add -u              # Stage tracked modifications
         git add -p              # Interactively stage hunks
         git commit              # Commit (opens editor)
         git commit -v           # Commit with diff in editor

   .. grid-item-card:: Branching

      .. code-block:: bash

         git branch              # List branches
         git switch <br>         # Switch branch
         git switch -c <br>      # Create + switch
         git merge <br>          # Merge branch
         git branch -d <br>      # Delete branch

   .. grid-item-card:: Remotes

      .. code-block:: bash

         git clone <url>         # Download repo
         git remote -v           # List remotes
         git fetch origin        # Download, do not merge
         git push origin <br>    # Upload branch
         git pull origin <br>    # Download + merge

   .. grid-item-card:: Undoing

      .. code-block:: bash

         git restore <f>         # Discard edits
         git restore --staged <f># Unstage
         git commit --amend      # Fix last commit
         git revert <hash>       # Undo a pushed commit
         git reflog              # Find lost commits

   .. grid-item-card:: Parking & History

      .. code-block:: bash

         git stash push -m "msg" # Park edits
         git stash pop           # Bring them back
         git show <hash>         # One commit
         git blame <file>        # Who wrote each line
         git tag -a <name> -m ".."  # Mark a version


Older Command Forms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


This module uses ``git switch`` throughout, because it is the modern,
dedicated command. You will nevertheless meet ``git checkout``
constantly (in tutorials, in Stack Overflow answers, and in your
colleagues' muscle memory), so you need to recognize it.

.. list-table::
   :widths: 35 35 30
   :header-rows: 1
   :class: compact-table

   * - Older form
     - Modern / safer form
     - Why
   * - ``git add .``
     - ``git add <files>`` (or ``git add -u``)
     - Avoids staging unwanted files. Worth the habit on a real project.
   * - ``git commit -m "msg"``
     - ``git commit``
     - Opens an editor, which encourages a real message. The examples
       in this module use ``-m`` only to keep them short on the page.
   * - ``git checkout -b <br>``
     - ``git switch -c <br>``
     - ``switch`` is a dedicated command; ``checkout`` also restores
       files, which makes it easy to misuse.
   * - ``git checkout <br>``
     - ``git switch <br>``
     - Clearer intent. Use ``git restore`` for files.


Git Rules for This Course
----------------------------------------------------


.. admonition:: Confirm against the syllabus and Canvas before teaching
   :class: caution

   This section states the workflow rules the course expects. Check the
   specifics (repository names, who to add as a collaborator, submission
   format) against the current assignment instructions on Canvas, which
   take precedence if they differ.


Individual Assignments (RWA1 to RWA3)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. danger::

   **Keep RWA repositories private.** A public repository containing
   your solution is visible to every other student and to next year's
   class. If a classmate copies from it, both of you are in an academic
   integrity case, and "I did not know it was public" is not a defense.

   Check now: on GitHub, a private repository shows a **Private** badge
   next to its name. If yours says **Public**, fix it under
   **Settings** -> **General** -> **Danger Zone** -> **Change
   visibility**.

- One repository per RWA, private, owned by you.
- Add the instructor and the TAs as collaborators so the work can be
  graded (**Settings** -> **Collaborators** -> **Add people**).
- Do not fork a classmate's assignment repository, and do not accept a
  fork of yours.
- Commit as you go. A repository whose entire history is one commit
  called "final" the night before the deadline tells the grader nothing
  about your process, and tells them something about your process. The
  triggers for "as you go" are listed in :ref:`How to Commit Well
  <vc-commit-well>`.


Group Projects (GP1 to GP3)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


- One repository per team, with every member as a collaborator.
- Protect ``main`` on day one, as described above.
- Everybody works on branches. Nobody commits directly to ``main``.
- Every change reaches ``main`` through a pull request that a teammate
  approved.
- Use your real name and university email in ``git config``, so
  contributions are attributable to the right person.

.. note::

   Git history is part of how group work is assessed. ``git log
   --author="Your Name" --oneline`` is a command the teaching staff can
   run. If one member has four hundred commits and another has three,
   the history says so. Commit your own work under your own name, from
   the start, rather than trying to reconstruct a story at the end.


Never Commit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - Do not commit
     - Instead
   * - ``build/``, ``install/``, ``log/``, ``*.o``
     - ``.gitignore``, written before the first commit.
   * - Passwords, tokens, keys, ``.env``
     - Keep them out of the repository. If one slips in, rotate it.
   * - Large binaries, datasets, bag files
     - Link to them, or use Git LFS if the assignment allows it.
   * - AI-generated code
     - Course policy: you write the code you submit. This applies to
       every commit, not just the final one.
   * - Somebody else's solution
     - Cite and link anything you adapt, in the commit message and in
       the README.

.. admonition:: Before every deadline
   :class: tip

   .. code-block:: bash

      git status                    # nothing uncommitted, nothing untracked
      git log --oneline -5          # the work is really committed
      git push                      # the work is really on GitHub

   Then **open the repository in a browser** and look at it. Pushing to
   the wrong remote, pushing a branch that is not ``main``, and
   forgetting to push at all are the three ways students submit an empty
   repository. Thirty seconds in the browser catches all three.
