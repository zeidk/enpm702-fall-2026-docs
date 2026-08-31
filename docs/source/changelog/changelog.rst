====================================================
Changelog
====================================================

All notable changes to the ENPM702 Fall 2026 course documentation are recorded here.


.. dropdown:: v1.1.0: Lecture 1 Rebuilt from the L1 Slides (2026-08-30)
   :icon: tag
   :class-container: sd-border-success
   :open:

   Lecture 1 rewritten to match the ``ENPM702-L1-v1.0`` slide deck.

   **Lecture (**\ ``l1_lecture.rst``\ **)**

   - New **Syllabus** section: course overview, learning outcomes,
     logistics, weekly cycle, self-study deadlines, required resources,
     assessments, assignment milestones, quiz dates, participation,
     grading and late-work policies, academic integrity and the AI
     policy, weekly schedule, and support resources.
   - New **C++ Overview** section: authoritative and secondary sources
     (including `N4868 <https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4868.pdf>`_,
     the free C++20 working draft this course refers to), the standards
     timeline, what each standard added, why the course targets C++20,
     why C++ for robotics, and a note for students arriving from
     Python.
   - New **From Source to Executable** section: cloning the course
     code repository, writing ``main.cpp``, comments, and the
     preprocessor, compiler, and linker stages, then loading and
     execution.
   - New **Building with CMake** section: a minimal project, the
     configure/build/run cycle, and the VSCode equivalents.
   - New **Environment Verification** section: the toolchain version
     check, building the Week 1 code two ways, and a table of common
     failures.
   - Four figures added (``_static/images/l1/``): the C++ standards
     timeline, the write/build/run development process, the build
     pipeline, and the whole path from source to a running process.

   **Language standard**

   - Lecture 1 now targets **C++20** with GCC 13 and CMake 3.22,
     replacing the previous C++17 material. Other pages still reference
     C++17.

   **Index, references, and quiz**

   - ``l1_index.rst``: overview, learning objectives, and next steps
     rewritten to cover the new material.
   - ``l1_references.rst``: added the course code repository, C++
     language references, and build/toolchain references; the C++17
     working draft is now labeled as reference only.
   - ``l1_quiz.rst``: eight new multiple-choice questions and four new
     true/false questions on the standards, the build pipeline, CMake,
     and the AI policy (24 questions total).


.. dropdown:: v1.0.1: VSCode/CMake Reading Material Fixes (2026-08-30)
   :icon: tag
   :class-container: sd-border-success
   :open:

   Corrections to the *VSCode and CMake* reading material and its
   downloadable configuration files.

   **Downloads (**\ ``_static/files/``\ **)**

   - ``extensions.json``: now matches the six extensions documented in
     the lecture, exercises, and references. Added ``twxs.cmake``,
     ``usernamehw.errorlens``, and ``eamodio.gitlens``; removed the
     undocumented Python and ROS 2 entries.
   - ``settings.json``: replaced the stale personal configuration with
     the documented workspace settings (format on save, 80-column
     ruler, C++17).
   - ``cout.code-snippets``: prefix corrected from ``zz`` to ``cout``
     so the documented "type ``cout``, press ``Tab``" workflow works.

   **Lecture (**\ ``vcm_lecture.rst``\ **)**

   - New **Regular Approach** section for CMake, with a directory tree
     showing one self-contained project per lecture folder.
   - Added a directory tree to the **Hybrid Approach** section to
     contrast it with the regular layout.
   - Added ``Error Lens`` to the extension list in the introduction.
   - Added ``"scope": "cpp"`` to the ``cout`` snippet so the lecture
     matches Exercise 7.
   - Fixed three reStructuredText warnings (duplicate link targets and
     an unterminated inline literal).

   **Quiz (**\ ``vcm_quiz.rst``\ **)**

   - Q9: corrected the explanation --- ``build/`` sits at the workspace
     root in the hybrid layout, not inside ``weekX/``.
   - Q10: corrected the explanation, which said VSCode fails
     "silently" and then told students where to find the error message.

   **Index (**\ ``vcm_index.rst``\ **)**

   - Learning objectives now cover distinguishing the regular from the
     hybrid CMake approach.
   - "Students should *watch* this" corrected to "*read*"; this is a
     reading module with no course video.


.. dropdown:: v1.0.0: Original Version (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   Initial release of the ENPM702 Fall 2026 course documentation.

   - Course structure: 13 lectures (9 C++ + 4 ROS 2), 3 RWAs, 3 GPs, 5 quizzes.
   - Syllabus with 14-week schedule.
   - Lecture 1: Course Introduction (Linux Shell, VSCode, CMake).
   - Glossary with L1 terms.
   - Reading material placeholders (Version Control, Flow Control).
