====================================================
Changelog
====================================================

All notable changes to the ENPM702 Fall 2026 course documentation are recorded here.


.. dropdown:: v1.4.0: Lecture 3 Synced with the L3 Slide Deck (2026-09-15)
   :icon: tag
   :class-container: sd-border-success
   :open:

   Lecture 3 brought into **one-to-one correspondence** with the
   ``ENPM702-L3-v1.0`` slide deck: everything the deck teaches is on the
   page, and anything commented out of the deck has been taken off it.

   **Lecture (**\ ``l3_lecture.rst``\ **)**

   - New **Memory Addresses and Hexadecimal** section, ahead of
     everything else: what an address is, why it is printed in base 16,
     that one hex digit is 4 bits so two are exactly one byte, and the
     arithmetic trap that makes ``0x…a28 + 8`` look like two bytes when
     it is eight. Also explains the ``0x7ffd…a10`` elision used
     throughout the page, and why addresses end in ``0``, ``4``, ``8``
     or ``c``.
   - New **Debug and Release Builds** section covering all five variants
     VS Code's *CMake: Select Variant* offers, with the flags CMake adds
     for each, measured rather than quoted: ``Debug`` ``-g``,
     ``Release`` ``-O3 -DNDEBUG``, ``MinSizeRel`` ``-Os -DNDEBUG``,
     ``RelWithDebInfo`` ``-O2 -g -DNDEBUG``, and ``Unspecified``
     nothing at all. Includes the ``if(NOT CMAKE_BUILD_TYPE)`` guard,
     since the course project sets no build type of its own, and a
     warning that ``Unspecified`` gives neither optimization nor debug
     information.
   - New **Same address, and the same type** subsection: ``&altitude_m``
     does not yield "an address" in some generic sense, it yields an
     ``int*``, which is why the initialization compiles. Demonstrated
     with ``typeid`` and ``c++filt -t``, including the mangled ``Pi``
     that students will actually see first.
   - **Pointer Arithmetic** now opens by naming the operations
     (``ptr + n``, ``ptr - n``, ``++ptr``, ``--ptr``, ``ptr2 - ptr1``)
     and the single rule behind all of them, before working the
     example.
   - **The delete Operator** now opens with the ownership handoff and
     the ``delete p; p = nullptr;`` pair, and states the sentence the
     rest of the section unpacks: ``delete`` acts on the **storage**,
     not on the pointer.
   - The **unit suffix** convention is now explained where the running
     example is introduced, rather than left for students to infer:
     ``altitude_m`` is metres, ``voltage_v`` volts, ``battery_pct``
     percent, with the Mars Climate Orbiter as the reason it matters.
   - ``voltage`` renamed to ``voltage_v`` throughout, so the convention
     is applied consistently. It was previously the one unit-bearing
     variable without a suffix, sitting next to ``altitude_m`` in the
     same examples.
   - The reason ``const Battery&`` costs 8 bytes is now stated: it
     passes an **address**, the same 8 bytes any pointer is, rather than
     copying the object.
   - Addresses in the pointer-arithmetic example changed from
     ``…a24``/``…a28``/``…a30`` to ``…a10``/``…a14``/``…a20``/``…a28``,
     so the hex arithmetic reads correctly whether or not the reader
     notices it is hex.
   - **ES.10: Declare one name (only) per declaration** now linked from
     the "one declaration per line" rule, matching how it is cited in
     Lecture 2 and RWA1.
   - The pointer-formatting note no longer sends students to the VS Code
     ``Vc Format`` settings, which have no effect while clang-format is
     the active engine. It now points at the ``.clang-format`` file
     added to the course code repository.

   **Removed, because the slides no longer cover them**

   - **The Modern Alternative** section, with RAII, the which-tool-for-
     which-job table and **C++20 and pointers**.
   - **Discussion 2** (reading a real signature).
   - The implementation half of *What a reference is in memory*: the
     compiler's-answer discussion, the ``reference_memory`` figure and
     the Debug/Release assembly walkthrough. The language's answer and
     its three-row table stay, which is what the slide shows.
   - The *when byte order becomes visible* material, leaving the
     little-endian and big-endian comparison the slide carries.
   - The ``memory_leak`` and ``null_dereference`` figures, along with
     captions such as "the pointer was the only way to reach the block",
     which never appeared on a slide.
   - The **Where Objects Live** wrapper, so the page opens the two
     sections the way the deck does: *Three Storage Durations* and
     *Stack and Heap*.

   **Figures**

   - ``typed_pointer.png`` redrawn to show each object's bytes as bits,
     split into nibbles the way Lecture 2 draws them, and relabelled for
     ``voltage_v``.
   - Two new figures added to match the deck: ``new.png`` on **The new
     Operator**, showing the stack pointer and the unnamed heap object
     it addresses, and ``new2.png`` on the same page, showing the pointer
     gone and the object stranded.
   - ``new_delete.png`` moved to **The delete Operator**, where the deck
     places it.
   - The page and the deck now use the **same ten figures**, with none
     left over on either side.

   **Glossary**

   - Four Lecture 3 terms added: *Alignment*, *Build Type*,
     *Endianness*, and *Hexadecimal*.

   **Exercises and quiz**

   - ``l3_exercises.rst``: new **Exercise 7, Debug and Release Are Not
     the Same Build**, which has students watch Valgrind lose the line
     number when ``-g`` goes away and get it back under
     ``RelWithDebInfo``. The Valgrind-clean challenge is now Exercise 8.
   - ``l3_quiz.rst``: 27 questions, up from 23. New questions on hex
     address arithmetic, the type of ``&x``, why ``Release`` costs
     Valgrind its line numbers, and why leaving the build type unset is
     not a safe default.

   **Knock-on fixes**

   - ``l3_index.rst``: the overview no longer promises the C++20
     constant-expression material, the RAII and C++20 learning
     objectives are gone, and *Next Steps* no longer refers to a
     Discussion 2 that is not there. Two objectives added for the new
     hexadecimal and build-type sections.
   - ``glossary.rst``: **RAII** now points at :doc:`L7
     </lectures/lecture7/l7_lecture>`, Smart Pointers, rather than at a
     Lecture 3 section that no longer exists.

   **Shell exercises**

   - Unchanged. They teach general shell skills and already finish with
     a Valgrind script.


.. dropdown:: v1.3.0: Lecture 2 and Reading Material Updates (2026-09-07)
   :icon: tag
   :class-container: sd-border-success
   :open:

   **Lecture 2**

   - New section on **characters**: single quotes, escape sequences, and
     why ``char`` counts as an integral type.
   - New section on **validating input**, covering what happens when the
     user types something that is not a number, and two ways to handle
     it.
   - New section on **stream manipulators** such as ``std::boolalpha``
     and ``std::setprecision``.
   - New material on **how long a variable's memory lasts**, and on the
     stack.
   - New short history of why variables have names instead of addresses.
   - Global variables now show how a local can hide a global, and how
     ``::`` reaches the global anyway.
   - The list of promotions is now complete rather than a selection.
   - Corrections: the memory-segment table now matches the diagram, and
     the description of ``std::setprecision`` now says when it counts
     significant digits and when it counts decimal places.

   **Reading material**

   - Every C++ snippet from the reading modules is now collected in one
     file in the course repository, ready to uncomment and run. Each
     lecture page links to it.
   - Exercise pages now state clearly that the exercises are not graded
     and are not submitted on Canvas.
   - Fixed an error in **Flow Control**, where an example printed
     "1 is even".
   - Fixed three examples that could not be compiled as printed because
     they were missing an ``#include``.
   - The **Flow Control** diagrams now display correctly.


.. dropdown:: v1.2.0: Lecture 2 Rebuilt, and C++20 Applied Site-wide (2026-09-04)
   :icon: tag
   :class-container: sd-border-success
   :open:

   Lecture 2 rewritten from the ``ENPM702_L2_CPPIntroduction`` slide
   deck, and the C++20 language standard applied across every page.

   **Lecture (**\ ``l2_lecture.rst``\ **)**

   - The C++ overview, standards timeline, hardware-interfacing
     capabilities, and the full write/build/run walkthrough were
     **removed**: Lecture 1 now covers all of that in more depth. What
     remains is a one-table recap of the preprocessor/compiler/linker
     pipeline that links back to Lecture 1.
   - New **Basic Input and Output** section: ``std::cout`` and
     ``std::cin``, the insertion and extraction operators, the scope
     resolution operator, statements, and comments.
   - **Bits, Bytes, and Words** expanded with a full memory-segment
     table (reserved, text, data, BSS, heap, stack, arguments) and the
     four memory-management failure modes from the slides.
   - **Variables** expanded: the five characteristics worked through one
     example, identifier rules with legal and illegal cases, what
     ``int number{20};`` does in memory step by step, and the ``&``
     operator.
   - **Integral types** now list the wide character types, document the
     omittable modifiers, and note that plain ``char``, ``signed char``
     and ``unsigned char`` are three distinct types.
   - **Floating-point types**: the ``long double`` row corrected to the
     x86-64 80-bit extended format (about 18 significant digits, not
     33), plus the ``1f`` versus ``1.0f`` suffix error and
     ``std::fixed``.
   - **Type conversion** expanded: the five implicit-conversion
     contexts, ``typeid`` with ``c++filt -t``, promotion versus
     conversion, why only braces reject narrowing, both usual
     arithmetic conversion rules with worked examples, and the integer
     division trap.
   - **Constants** expanded: literal suffixes, west/east ``const``, the
     concrete failure modes of macros, compile-time versus runtime
     constants, and why ``constexpr`` is preferred.
   - **Scopes** now covers lifetime at the closing brace and which
     segment globals live in.
   - **Namespaces** now covers the ``using`` declaration separately from
     the ``using namespace`` directive, with the ambiguity and
     readability arguments against the latter.
   - Six figures added (``_static/images/l2/``): bits/bytes/words,
     memory segments and addressable bytes, variable allocation, the
     simplified memory notation, going out of scope, and globals in
     data and BSS. The stale entity-relationship diagrams left in that
     folder by an earlier course were removed.

   **Index, exercises, quiz, references, glossary**

   - ``l2_index.rst``: overview, twelve learning objectives, and next
     steps rewritten to match the new material.
   - ``l2_exercises.rst``: new **Part A**, seven predict-and-fix drills
     taken from the slides (identifiers, declarations and
     initializations, two on arithmetic conversions, ``const`` and
     ``constexpr`` errors, type deduction, scope), each with a worked
     answer. The six programming exercises are now **Part B**, with
     added steps on ``c++filt``, namespace ambiguity, and ``enum class``.
   - ``l2_quiz.rst``: 27 questions, up from 15. New questions on stream
     operators, memory segments, promotion versus conversion, integer
     division, macros, ``auto`` and ``const``, scoped enumerations,
     ``c++filt``, signed/unsigned comparison, overflow, type aliases,
     and literal suffixes.
   - ``l2_references.rst``: added a table of every Core Guideline cited
     in the lecture, cppreference pages for initialization, implicit
     conversions, fundamental types and enumerations, and ``c++filt``.
   - ``glossary.rst``: 39 Lecture 2 terms added (bit, byte, word, data
     and BSS segments, declaration, the three initialization forms,
     literal, identifier, lifetime, macro, mangling and demangling,
     numeric conversion, signedness, scope resolution operator, scoped
     enumeration, type conversion, ``typeid``, the ``using`` forms, and
     more). A new **G** section was added for *Global Scope*, and
     *Wild Pointer* was moved out of **V** into **W**.

   **Language standard**

   - Every page now targets **C++20**. ``-std=c++17`` in the Lecture 2
     to Lecture 9 exercises and the Lecture 2, 3 and 7 shell material,
     ``CMAKE_CXX_STANDARD 17`` in the VSCode/CMake module and the
     Lecture 4 shell exercises, ``"C_Cpp.default.cppStandard": "c++17"``
     in the module and in the downloadable ``settings.json``, the
     "C++17 or later" build requirement in RWA1 to RWA3, and learning
     outcome 1 in ``docs/latex-slides/ENPM702-L1-v1.0.tex`` were all
     updated. Statements about *when* a feature was introduced (for
     example structured bindings in C++17) are historical facts and
     were left alone.
   - The course previously claimed C++20 without using any of it.
     Lecture 2 now teaches four C++20 facilities, each attached to the
     topic it belongs to:

     - ``std::numbers::pi`` (``<numbers>``) in **Constant Variables**,
       replacing hand-typed digits.
     - ``std::cmp_less`` and its siblings (``<utility>``) in
       **Compiler Behavior Differences**, as the fix for the
       ``-1 < 1u`` trap the section already teaches.
     - ``std::format`` (``<format>``) in **std::setprecision**, as the
       non-sticky alternative to the iostream manipulators. Flagged as
       requiring GCC 13 specifically.
     - ``using enum`` in **Scoped Enumerations**.

     Exercise B3 gained a step comparing a typed pi against
     ``std::numbers::pi`` at 20 digits, ``l2_references.rst`` gained a
     **C++20 Facilities** card, and the glossary gained
     ``std::format``, ``std::numbers`` and ``using enum``.

   **Corrections found in a technical review of the page**

   - ``const double pi{3.141598}`` in the slide deck is wrong in the
     sixth decimal place (pi is 3.141592...). The lecture no longer
     carries the value: the west/east ``const`` example uses a radius,
     and the constant itself comes from ``std::numbers::pi``.
   - The ``std::numbers`` example did not compile as first written. A
     ``const double`` is **not** usable in a constant expression (only
     ``const`` objects of *integral* type are), so
     ``constexpr double area{pi * radius * radius};`` over a
     ``const double radius`` is an error. The example now uses
     ``constexpr``, and a new warning under **Compile-time and Runtime
     Constants** documents the asymmetry.
   - The arithmetic-conversion section presented a flat priority list as
     if it were the rule. It is a simplification, and it predicts the
     wrong answer for ``long long + unsigned long`` on 64-bit Linux
     (the result is ``unsigned long long``). The section is now a
     three-step procedure, and a warning states where the shortcut
     breaks and why it does not matter if you avoid mixing signedness.
   - The worked examples annotated ``typeid(...).name()`` with
     ``// double``, ``// long`` and so on, but that function returns the
     **mangled** code (``d``, ``l``, ``m``). Comments corrected, and a
     table of GCC's codes for the fundamental types added.
   - ``int _break1;`` was marked simply "OK". Leading-underscore names
     are reserved for the implementation in cases students cannot be
     expected to distinguish, so the example now carries the rule.
   - "A declaration reserves storage" conflated declaration with
     definition. Reworded, with a note pointing forward to Lecture 5.
   - The ``SQUARE(x)`` macro was captioned "no type checking at all",
     which is not what goes wrong (the expansion *is* type-checked). It
     now shows the real hazard, double evaluation of ``SQUARE(i++)``.
   - ``sizeof(bool)`` was stated as 1 byte; that is true everywhere this
     course runs but is not guaranteed by the standard. Qualified.
   - ``int a{}`` was called zero initialization without noting that the
     standard's term is value-initialization. Both names now given.
   - Several ``// Error:`` comments paraphrased GCC rather than quoting
     it. Aligned with the real diagnostics.
   - Instructions to read ``typeid`` output through ``c++filt -t``
     were removed. Whether it demangles bare single-letter type codes
     could not be verified, so the lecture now gives the code table
     directly and presents ``c++filt`` for the linker-symbol case,
     where its behavior is not in doubt.


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
