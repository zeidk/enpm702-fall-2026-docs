====================================================
Changelog
====================================================

All notable changes to the ENPM702 Fall 2026 course documentation are recorded here.


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
