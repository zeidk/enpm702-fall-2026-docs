Syllabus
========

.. role:: reading
.. role:: quiz
.. role:: assignment
.. role:: no-class

Grade Breakdown
---------------

.. list-table::
   :header-rows: 1
   :widths: 48 16 16
   :class: compact-table

   * - Component
     - Percentage
     - Points
   * - RWAs (3) + GPs (2)
     - 70%
     - 280
   * - Quizzes (5)
     - 25%
     - 100
   * - Participation/Engagement
     - 5%
     - 20
   * - **Total**
     - **100%**
     - **400**

.. note::

   The course is graded out of **400 points** (each component is scored
   on this scale to simplify grading); final letter grades are computed
   from the percentages above. **Participation** is earned by actively
   engaging in class discussions or by submitting weekly exercise
   solutions on Canvas.


.. _course-schedule:

Course Schedule
---------------

Lectures meet on **Tuesdays**. The first lecture is **September 1, 2026**
and the last day of class is **Friday, December 11, 2026**. There is
**no class on Tuesday, October 13** (Fall Break), so every lecture from
Smart Pointers on meets one week later than first planned, and the
course has 14 lectures instead of 15. The Thanksgiving recess (**Nov 25
to 29**) does not fall on a Tuesday, so the Nov 24 lecture meets as
scheduled.

**Color key:** :reading:`reading material`; :quiz:`quizzes`;
:assignment:`assignments (RWAs and GPs) posted/due`;
:no-class:`no class`.

.. list-table::
   :header-rows: 1
   :widths: 6 8 20 38 28
   :class: compact-table schedule-table

   * - Week
     - Date
     - Before Class
     - During Class
     - After Class
   * - Week 1
     - Sep 1
     - :reading:`Read: Linux Shell, VSCode & CMake, Version Control`
     - Course Introduction and Conventions
     -
   * - Week 2
     - Sep 8
     -
     - Introduction to C++ (Variables, Types, Constants, Namespaces)
     - Submit Lecture 2 exercises
   * - Week 3
     - Sep 15
     - :reading:`Read: Flow Control & Operations`
     - Pointers and Memory Management (Stack, Heap, References)
     - | Submit Lecture 3 exercises
       | :assignment:`RWA1 posted`
   * - Week 4
     - Sep 22
     -
     - | STL Containers (Strings, Arrays, Vectors, Iterators)
       | :quiz:`Quiz 1`
     - Submit Lecture 4 exercises
   * - Week 5
     - Sep 29
     -
     - Functions, Basics (Declarations, Parameters, Overloading, Recursion)
     - | Submit Lecture 5 exercises
       | :assignment:`RWA1 due`
   * - Week 6
     - Oct 6
     -
     - | Functions, Advanced (Structs, ``std::optional``, Templates and Concepts, Lambdas, ``std::function``)
       | :quiz:`Quiz 2`
     - | Submit Lecture 6 exercises
       | :assignment:`RWA2 posted (Fri, Oct 9)`
   * - Week 7
     - Oct 13
     -
     - :no-class:`No class (Fall Break)`
     -
   * - Week 8
     - Oct 20
     - :reading:`Read: Exception Handling`
     - Smart Pointers and Move Semantics (``unique_ptr``, ``shared_ptr``, ``weak_ptr``)
     - | Submit Lecture 7 exercises
       | :assignment:`RWA2 due (Fri, Oct 23)`
   * - Week 9
     - Oct 27
     -
     - | OOP Basics (Classes, Objects, Encapsulation, Constructors)
       | :quiz:`Quiz 3`
     - Submit Lecture 8 exercises
   * - Week 10
     - Nov 3
     -
     - OOP Advanced (Inheritance, Polymorphism, Abstraction)
     - | Submit Lecture 9 exercises
       | :assignment:`RWA3 posted`
   * - Week 11
     - Nov 10
     -
     - | ROS 2, Foundations (Publisher, Subscriber, Custom Interfaces)
       | :quiz:`Quiz 4`
     - Submit Lecture 10 exercises
   * - Week 12
     - Nov 17
     -
     - ROS 2, Configuration and Orchestration (Parameters, Launch Files, Executors)
     - | Submit Lecture 11 exercises
       | :assignment:`RWA3 due, GP1 posted`
   * - Week 13
     - Nov 24
     -
     - | ROS 2, Communication Patterns (Services, Actions)
       | :quiz:`Quiz 5`
     - | Submit Lecture 12 exercises
       | :assignment:`GP1 due, GP2 posted`
   * - Week 14
     - Dec 1
     -
     - ROS 2, Coordinate Frames and Transforms
     - Submit Lecture 13 exercises
   * - Week 15
     - Dec 8
     -
     - ROS 2, Robot Autonomy Architecture (Sense-Plan-Act, where AI/ML fits)
     - | Submit Lecture 14 exercises
       | :assignment:`GP2 due (Dec 11)`

.. note::

   This is a tentative schedule, and subject to change as necessary.
   Monitor ELMS-Canvas for current deadlines.


Real-World Applications (RWAs)
------------------------------

The three RWAs are **cumulative** individual assignments that progressively
build a C++ application using robotics-themed use cases. Each RWA refactors
and extends the previous one, demonstrating why each new C++ feature
improves the codebase:

.. list-table::
   :header-rows: 1
   :widths: 36 12 12 12 10
   :class: compact-table

   * - Assignment
     - Posted
     - Due
     - Duration
     - Points
   * - RWA1: Search-and-Rescue Drone
     - Sep 15
     - Sep 29
     - 2 weeks
     - 44
   * - RWA2: STL Containers and Functions
     - Oct 9
     - Oct 23
     - 2 weeks
     - 48
   * - RWA3: Smart Pointers and OOP
     - Nov 3
     - Nov 17
     - 2 weeks
     - 48


Group Projects (GPs)
--------------------

The two GPs are **cumulative** team-based projects that progressively
build a ROS 2 application with a mobile robot in Gazebo. GP2 extends the
GP1 deliverable:

.. list-table::
   :header-rows: 1
   :widths: 36 12 12 12 10
   :class: compact-table

   * - Project
     - Posted
     - Due
     - Duration
     - Points
   * - GP1: ROS 2 Pub/Sub with Gazebo
     - Nov 17
     - Nov 24
     - 1 week
     - 44
   * - GP2: Services, Actions, Frames, and a Decision Layer
     - Nov 24
     - Dec 11
     - About 2.5 weeks (incl. Thanksgiving recess)
     - 96

.. tip::

   Start assignments early. RWAs and GPs are cumulative, so a strong
   foundation in each deliverable makes the next one easier.


.. _peer-evaluation:

Peer Review
-----------

Your project grade is not purely a team grade.

.. list-table::
   :header-rows: 1
   :widths: 70 30
   :class: compact-table

   * - Component
     - Share
   * - Team project grade
     - 60%
   * - Peer review score
     - 40%

- Peer evaluations are **emailed to the instructor** within **48 hours** of
  every project deadline. The format is below.
- They are **not optional**. Not submitting yours forfeits your own peer
  review score for that project. Your teammates' scores are unaffected.
- Each member is responsible for understanding the **whole** submission, not
  only the part they wrote. You may be asked to walk through any part of it.
- Ratings are confidential. Teammates see only their final peer score, never
  who rated them what, and never the comments.

.. important::

   Forty percent is a lot, and that is deliberate. On a team project, the
   person who knows who did the work is not the instructor. The form rates **contribution**, not whether people liked
   each other.


The form
^^^^^^^^

Rate each teammate, **and yourself**, on five criteria.

Scale: **1** = well below what the team needed, **3** = a fair share,
**5** = carried more than their share, and did it well.

.. list-table::
   :header-rows: 1
   :widths: 5 25 70
   :class: compact-table

   * - #
     - Criterion
     - What it means
   * - 1
     - Technical contribution
     - Wrote, debugged, or tested a meaningful part of the submission.
   * - 2
     - Reliability
     - Did what they said, when they said. Told the team early when they
       could not.
   * - 3
     - Communication
     - Kept the team informed, asked when stuck, answered when asked.
   * - 4
     - Understanding
     - Can explain any part of the submission, including parts they did
       not write.
   * - 5
     - Collaboration
     - Reviewed others' work, helped unblock teammates, handled
       disagreement well.

**One required sentence per teammate** naming the specific thing they
contributed. "Worked hard" and "did their part" do not count. "Wrote the
obstacle-detection subscriber and found the timer bug in the search
node" does.

**Your self-rating** is not used in your score. It is compared with what your
teammates said, and a large gap is one of the things that triggers a
conversation.

**One optional question:** is there anything the instructor should know
about how this team worked?


How to submit
^^^^^^^^^^^^^

One email per student, from your UMD address, to ``zeidk@umd.edu``.

**Subject line, exactly:**

.. code-block:: text

   [ENPM702] GP1 peer evaluation - Team X

**Body**, plain text, no attachments. Copy this template and fill it in.
One block per teammate, then your own block, then the optional question.

.. code-block:: text

   Project: GP1
   Team: X
   From: Alice Nguyen

   --- Bob Ortiz ---
   Technical contribution: 3
   Reliability: 3
   Communication: 3
   Understanding: 3
   Collaboration: 4
   What they contributed: Wrote the launch file and the YAML
   parameters, and the README.

   --- Carol Singh ---
   Technical contribution: 5
   Reliability: 5
   Communication: 4
   Understanding: 5
   Collaboration: 5
   What they contributed: Wrote the custom message and the
   obstacle-detection subscriber, and found the timer bug in the search node.

   --- Alice Nguyen (self) ---
   Technical contribution: 4
   Reliability: 5
   Communication: 4
   Understanding: 4
   Collaboration: 4
   What I contributed: Wrote the search node's publisher and
   recorded the demo video.

   Anything the instructor should know: (optional)


How the score is computed
^^^^^^^^^^^^^^^^^^^^^^^^^

For each student, take the mean of the ratings **received** from teammates
across all five criteria. Call it :math:`R`. Take the team's mean of all
:math:`R` values. Call it :math:`T`. The student's peer factor is

.. math::

   F = \frac{R}{T}, \quad \text{clamped to } [0.6,\ 1.1]

Peer score for the project :math:`= 40 \times F`, capped at 40. The team
project grade supplies the other 60.

What this does in practice:

- A team where everyone rates everyone 5 gets :math:`F = 1.0` for everyone.
  So does a team where everyone rates everyone 3. Generous ratings do not
  inflate anyone. Only **relative differences** move the score.
- A member rated a full point below their teammates on a three-person team
  lands near :math:`F = 0.8`, an 8-point loss on a 100-point project.
- The clamp keeps a single project from being decided entirely by peer
  ratings. The floor is 0.6, so the worst case for a member who did
  contribute something is a 16-point loss. Genuine non-contribution is
  handled by the instructor, not by the formula.

**Worked example: Team X on GP1**

Team X's project scored 82 out of 100. Three members: Alice, Bob and Carol.
Each rated the other two on the five criteria. Received ratings, averaged
over the five criteria:

.. list-table::
   :header-rows: 1
   :widths: 16 21 21 21 21
   :class: compact-table

   * - Rated
     - From Alice
     - From Bob
     - From Carol
     - Received mean :math:`R`
   * - Alice
     - (self)
     - 4.6
     - 4.4
     - 4.5
   * - Bob
     - 3.0
     - (self)
     - 3.2
     - 3.1
   * - Carol
     - 4.8
     - 4.6
     - (self)
     - 4.7

Team mean :math:`T = (4.5 + 3.1 + 4.7) / 3 = 4.1`.

.. list-table::
   :header-rows: 1
   :widths: 12 18 14 22 16 18
   :class: compact-table

   * - Student
     - :math:`R / T`
     - :math:`F` after clamp
     - Peer score (40 × :math:`F`, cap 40)
     - Team part (60% of 82)
     - Individual grade
   * - Alice
     - 4.5 / 4.1 = 1.10
     - 1.10
     - 40.0 (capped from 44)
     - 49.2
     - **89.2**
   * - Bob
     - 3.1 / 4.1 = 0.76
     - 0.76
     - 30.4
     - 49.2
     - **79.6**
   * - Carol
     - 4.7 / 4.1 = 1.15
     - 1.10
     - 40.0 (capped from 44)
     - 49.2
     - **89.2**

Read across a row. The team part is the same 49.2 for everyone, since it is
60% of the shared project grade. The peer part is where the rows differ.
Bob's teammates rated him about a point and a half below the others, and
that costs him roughly 10 points against them on a 100-point project. Alice
and Carol both hit the cap, so the small difference between them disappears.
The peer score rewards pulling your weight, not out-rating a teammate who
also pulled theirs.

**The same team, rating everyone 5.** Every :math:`R` would be 5.0,
:math:`T` would be 5.0, every :math:`F` would be 1.0, and every member would
receive 40 + 49.2 = 89.2. Generosity changes nothing.

**Then scaled.** GP1 is worth 44 points, so each individual grade above is
multiplied by 0.44. Bob's 79.6 becomes 35.0, and Alice's and Carol's 89.2
becomes 39.2.

**With three members, one opinion carries a lot.** Each :math:`R` is the
mean of only two ratings. Bob's 3.1 came from a 3.0 and a 3.2, which agree,
so the score stands. If it had come from a 2.0 and a 4.2, the mean would be
the same 3.1 but the divergence rule below fires and the instructor reads
the comments before applying it.


Rules
^^^^^

- **Not submitting the evaluation forfeits your own peer score** for that
  project. Late evaluations are not accepted outside the documented-absence
  process.
- **No AI.** The sentences are yours.
- **Ratings that diverge sharply are read, not just averaged.** If one
  member rates a teammate two or more points below the others, or a
  self-rating differs from the received ratings by two or more points, the
  instructor reads the comments and may talk to the team before applying
  the score.
- **Reported non-contribution is a separate process.** If a teammate did
  not contribute to a project, say so in the optional question. The
  instructor follows up with the whole team, and the outcome may be a zero
  on the project for that member rather than a clamped factor.
- **Retaliation** for an honest evaluation is an academic integrity matter.


Where the formula comes from
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dividing a student's mean received rating by the team mean is the standard
way of turning peer ratings into an individual weighting, in use since the
early 1990s. Goldfinch and Raeside [1]_ introduced it, and Conway, Kember,
Sivan and Wu [2]_ reduced it to the single multiplicative factor used here.
Kaufman, Felder and Fuller [3]_ applied it in engineering courses with
self-ratings excluded and a maximum factor of 1.10, which is the ceiling
used here. It is also the "adjustment factor" computed by CATME [4]_, the
most widely used peer evaluation instrument in engineering education,
whose five rating dimensions the criteria above condense, and the factor
computed by SPARK [5]_. The five sources apply the factor to the whole
team grade; this course applies it to the 40% peer share only, and adds a
floor of 0.6, so that a single project cannot be decided entirely by peer
ratings.

.. [1] Goldfinch, J. and Raeside, R. (1990). Development of a peer
   assessment technique for obtaining individual marks on a group project.
   *Assessment & Evaluation in Higher Education*, 15(3), 210 to 231.
.. [2] Conway, R., Kember, D., Sivan, A. and Wu, M. (1993). Peer assessment
   of an individual's contribution to a group project. *Assessment &
   Evaluation in Higher Education*, 18(1), 45 to 56.
   https://doi.org/10.1080/0260293930180104
.. [3] Kaufman, D. B., Felder, R. M. and Fuller, H. (2000). Accounting for
   individual effort in cooperative learning teams. *Journal of Engineering
   Education*, 89(2), 133 to 140.
   https://doi.org/10.1002/j.2168-9830.2000.tb00507.x
.. [4] Ohland, M. W., Loughry, M. L., Woehr, D. J., Bullard, L. G., Felder,
   R. M., Finelli, C. J., Layton, R. A., Pomeranz, H. R. and Schmucker,
   D. G. (2012). The Comprehensive Assessment of Team Member Effectiveness:
   development of a behaviorally anchored rating scale for self and peer
   evaluation. *Academy of Management Learning & Education*, 11(4),
   609 to 630. See also https://info.catme.org/instructor-faq/what-is-the-adjustment-factor/
.. [5] Freeman, M. and McKenzie, J. (2002). SPARK, a confidential web-based
   template for self and peer assessment of student teamwork: benefits of
   evaluating across different subjects. *British Journal of Educational
   Technology*, 33(5), 551 to 569. https://doi.org/10.1111/1467-8535.00291


Quizzes
-------

There are five short quizzes, each worth **20 points**. They are
comprehension checks given in class on the dates below:

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 12
   :class: compact-table

   * - Quiz
     - Week
     - Date
     - Points
   * - Quiz 1
     - Week 4
     - Sep 22
     - 20
   * - Quiz 2
     - Week 6
     - Oct 6
     - 20
   * - Quiz 3
     - Week 9
     - Oct 27
     - 20
   * - Quiz 4
     - Week 11
     - Nov 10
     - 20
   * - Quiz 5
     - Week 13
     - Nov 24
     - 20


Reading Material
----------------

The following topics are provided as self-study reading modules.
Students are expected to work through these outside of class by the recommended
deadline:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30
   :class: compact-table

   * - Topic
     - Description
     - When to Complete
   * - Linux Shell
     - The Linux command-line shell: shell types, configuration files, aliases, and functions.
     - **Before the semester starts**
   * - VSCode and CMake
     - VSCode installation and interface, the ``.vscode`` folder, recommended extensions, the Command Palette, and the ``CMakeLists.txt`` build configuration.
     - **Before the semester starts**
   * - Version Control (Git and GitHub)
     - Distributed version control, branching, merging, pull requests, and the fork workflow.
     - **Before the semester starts**
   * - Flow Control and Operations
     - Conditionals, loops, and operators.
     - **Before Sep 15** (before Lecture 3)
   * - Exception Handling
     - Exception handling with ``try``, ``catch``, ``throw``, standard and custom exception classes, and RAII.
     - **Before Oct 20** (before Smart Pointers)
