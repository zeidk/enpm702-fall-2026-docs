References
==========

.. dropdown:: Version Control
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Version Control**

        Covers version control fundamentals, centralized vs. distributed
        systems, Git commands, branching, merging, merge conflicts,
        GitHub, collaboration workflows (branch and fork), and pull
        requests.


.. dropdown:: Git Cheat Sheets (Downloads)
    :class-container: sd-border-secondary
    :open:

    Printable one-page command references. Download one, print it, and
    keep it next to you while you work through the exercises. All four
    cover the same core commands, so pick whichever layout you find
    easiest to scan.

    - :download:`git-cheat-sheet-github.pdf </_static/files/git-cheat-sheet-github.pdf>`,
      GitHub Education. Two pages, the clearest layout of the four, and
      the one to print if you only print one.
    - :download:`git-cheat-sheet-atlassian.pdf </_static/files/git-cheat-sheet-atlassian.pdf>`,
      Atlassian. Grouped by task rather than alphabetically.
    - :download:`git-cheat-sheet-gitlab.pdf </_static/files/git-cheat-sheet-gitlab.pdf>`,
      GitLab. Compact, one page.
    - :download:`git-cheat-sheet-tower.pdf </_static/files/git-cheat-sheet-tower.pdf>`,
      Tower. Includes a short section on undoing things.

    .. note::

       The GitHub sheet is reproduced here from
       `github/training-kit <https://github.com/github/training-kit>`__,
       which is licensed CC BY 4.0. The others are hosted locally so
       they still work if the vendor moves the file, or if the network
       does not.


.. dropdown:: Interactive Cheat Sheets and Visualizers
    :class-container: sd-border-secondary
    :open:

    A printed list of commands tells you what to type. These show you
    what the commands **do**, which is a different and usually more
    useful thing.

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Dangit, Git!?!
            :link: https://dangitgit.com/
            :class-card: sd-border-secondary

            **dangitgit.com**

            Organized by the problem, not by the command: "I committed
            to the wrong branch", "I need to undo a commit". Go here
            first when something has gone wrong. Pairs with the
            :doc:`recovery section <vc_lecture>` of the lecture.

        .. grid-item-card:: Visualizing Git
            :link: https://git-school.github.io/visualizing-git/
            :class-card: sd-border-secondary

            **git-school.github.io/visualizing-git**

            A sandbox: type real commands and watch ``HEAD``, the branch
            pointers and the commits move. The fastest way to make the
            pointer model concrete. Try ``git commit`` three times, then
            ``git switch --detach HEAD~1``, and watch what happens to
            ``HEAD``. (The sandbox also accepts the older
            ``git checkout HEAD~1``.)

        .. grid-item-card:: Learn Git Branching
            :link: https://learngitbranching.js.org/
            :class-card: sd-border-secondary

            **learngitbranching.js.org**

            Guided exercises on the same visual model, from your first
            commit through rebasing. Good practice before the workshop
            drills.

        .. grid-item-card:: NDP Git Cheatsheet
            :link: https://ndpsoftware.com/git-cheatsheet.html
            :class-card: sd-border-secondary

            **ndpsoftware.com/git-cheatsheet.html**

            An interactive diagram placing each command across stash,
            workspace, index, local repository and upstream. The same
            mental model as the lecture's three areas, with the remote
            added.


.. dropdown:: Video Tutorials (YouTube)
    :class-container: sd-border-secondary
    :open:

    There is no pre-recorded course video for this topic. The following
    beginner-friendly video tutorials are recommended for self-study:

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Git and GitHub Crash Course (freeCodeCamp)
            :link: https://www.youtube.com/watch?v=mAFoROnOfHs
            :class-card: sd-border-secondary

            **freeCodeCamp: Git and GitHub Crash Course for Beginners**

            A one-hour crash course covering version control, commits,
            branching, merging, and pull requests with hands-on examples.

        .. grid-item-card:: Git and GitHub Tutorial for Beginners
            :link: https://www.youtube.com/watch?v=tRZGeaHPoaw
            :class-card: sd-border-secondary

            **Git and GitHub Tutorial for Beginners**

            A beginner-friendly walkthrough of the core Git and GitHub
            workflow used in this course.


.. dropdown:: Git Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Official Git Documentation
            :link: https://git-scm.com/doc
            :class-card: sd-border-secondary

            **git-scm.com: Documentation**

        .. grid-item-card:: Pro Git Book
            :link: https://git-scm.com/book/en/v2
            :class-card: sd-border-secondary

            **Pro Git by Scott Chacon and Ben Straub**, Free online
            book covering Git fundamentals through advanced topics.

        .. grid-item-card:: Git Reference
            :link: https://git-scm.com/docs
            :class-card: sd-border-secondary

            **git-scm.com: Reference Manual**


.. dropdown:: GitHub Guides
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: GitHub Quickstart
            :link: https://docs.github.com/en/get-started/quickstart
            :class-card: sd-border-secondary

            **GitHub Docs: Quickstart**

        .. grid-item-card:: Understanding the GitHub Flow
            :link: https://docs.github.com/en/get-started/using-github/github-flow
            :class-card: sd-border-secondary

            **GitHub Docs: GitHub Flow**

        .. grid-item-card:: Forking a Repository
            :link: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo
            :class-card: sd-border-secondary

            **GitHub Docs: Fork a Repo**

        .. grid-item-card:: About Pull Requests
            :link: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
            :class-card: sd-border-secondary

            **GitHub Docs: About Pull Requests**
