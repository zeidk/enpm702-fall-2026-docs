# CLAUDE.md — ENPM702 Course Documentation Preferences

## C++ Code Style
- Always use `'\n'` instead of `std::endl`. Only use `std::endl` if explicitly flushing the buffer is required.
- Use **uniform initialization** (`int a{1};`) as the default initialization style.
- Use **snake_case** naming convention for variables and functions.

## RST / Sphinx Conventions
- Use `toctree` with `:hidden:` in index pages.
- All top-level pages must be visible in the navbar — nothing in "More" dropdown. Set `header_links_before_dropdown` in conf.py to match the number of toctree entries. Current order: Syllabus, Setup, Lectures, Glossary, Reading Material, Changelog.
- Lecture pages follow this structure: Lecture, Shell Exercises, C++ Exercises, Quiz, References.
- Shell exercises (`lN_shell.rst`) increase in complexity across lectures.
- C++ exercises (`lN_exercises.rst`) are titled "C++ Exercises" (not just "Exercises").
- Lecture 1 has no C++ exercises.
- Use `.. code-block:: cpp` for C++ code, `.. code-block:: bash` for shell commands.
- Use cards, dropdowns, grids, admonitions, and list-tables from sphinx-design.
- Quiz format: `.. admonition:: Question N` with `:class: hint`, followed by `.. dropdown:: Answer` with `:class-container: sd-border-success`.
- Figure placeholders use: `.. figure:: /_static/images/lN/filename.ext` — keep original filenames and formats from LaTeX.
- C++ exercises and shell exercises use dropdown format: `.. dropdown:: Exercise N -- Title` with `:icon: gear`, `:class-container: sd-border-primary`, `:class-title: sd-font-weight-bold`. Challenge exercises use `:class-container: sd-border-warning`. Solutions are nested `.. dropdown:: Solution` with `:class-container: sd-border-success`.

## Course Structure
- Course: ENPM702 — Introduction to Robot Programming (Fall 2026).
- 14 weeks (including Thanksgiving), not 15. Week 15 is submission-only.
- 9 C++ lectures + 4 ROS 2 lectures = 13 lectures.
- Reading materials are **pre-recorded videos on Canvas** (not self-study text). Currently: Version Control, Flow Control & Operations.
- Assignments: 3 RWAs (Real-World Applications, individual, pure C++) + 3 GPs (Group Projects, team, ROS 2).
- RWAs and GPs are **cumulative** — each builds on the previous deliverable.
- 5 quizzes, grading: RWAs+GPs 70%, Quizzes 25%, Participation 5%.
- ROS lectures must come after OOP (ROS uses inheritance from `rclcpp::Node`).
- ROS lecture order: L10 (Pub/Sub, Custom Interfaces), L11 (Parameters, Launch Files, Executors), L12 (Services, Actions), L13 (Frames, Lifecycle Nodes).
- GPs use Gazebo with a mobile robot. GP2 introduces robot type inheritance/polymorphism.

## File Organization
- Docs root: `/home/zeidk/github/docs/enpm702-fall-2026-docs/docs/source/`
- LaTeX source: `/home/zeidk/github/docs/ENPM_2025_LECTURE/ENPM702/Lectures/`
- Setup split into: `ubuntu_setup.rst`, `cpp_setup.rst`, `ros_setup.rst`
- Glossary updated after each lecture with new terms, using `.. glossary::` directive with `:doc:` links back to the lecture.
- Changelog should contain only one entry (original version) unless told otherwise.

## Lecture LaTeX File Mapping
- L1: `ENPM702_L1_CourseIntroduction.tex` (v2.0)
- L2: `ENPM702_L2_CPPIntroduction_2.0.tex`
- L3: `ENPM702_L3_NORMAL_POINTERS_2.0.tex`
- L4: `ENPM702_L4_STL_containers_2.1.tex` (use v2.1)
- L5: `ENPM702_L5_functions_basic_v1.0.tex`
- L6: `ENPM702_L6_functions_advanced_v2.0.tex`
- L7: `ENPM702_L7_smart_pointers_v1.0.tex`
- L8: `ENPM702_L8_OOP_Basics_v1.0.tex`
- L9: `ENPM702_L9_OOP_Basics_v1.0.tex` (OOP Advanced)
- RM (reading material): `ENPM702_RM.tex` (Flow Control), `ENPM702_VersionControl.tex`
