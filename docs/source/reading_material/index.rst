====================================================
Reading Material
====================================================

Supplemental topics provided as self-study reading modules. Students
are expected to work through these outside of class.

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Topic**
     - **Covers**
   * - :doc:`compiler_warnings/cw_index`
     - Compiler warning flags: ``-Wall``, ``-Wextra``, ``-pedantic-errors``,
       the warnings each one enables, and the additional flags
       ``-Wshadow``, ``-Wconversion``, and ``-Werror``
   * - :doc:`sphinx_breathe/sb_index`
     - Reference pages built from Doxygen comments with Sphinx and the
       Breathe extension: Doxygen XML output, ``conf.py``, Breathe
       directives, rebuilding after a change
   * - :doc:`exception_handling/eh_index`
     - Exception handling with ``try``, ``catch``, ``throw``, standard
       and custom exception classes, ``noexcept``, RAII
   * - :doc:`flow_control/fc_index`
     - Selection statements (``if``, ``switch``), iteration statements
       (``while``, ``do-while``, ``for``), operators (arithmetic,
       relational, logical)
   * - :doc:`linux_shell/ls_index`
     - The Linux command-line shell: common shell types, configuration
       files (``.bashrc``, ``.zshrc``), aliases, and functions
   * - :doc:`input_validation/iv_index`
     - Validating terminal input: what ``std::cin >> value`` does when the
       input is not a number, stream state and recovery, and whole-line
       parsing with ``std::getline`` and ``std::from_chars``
   * - :doc:`version_control/vc_index`
     - Git fundamentals, branching, merging, GitHub, pull requests,
       fork workflow
   * - :doc:`vscode_cmake/vcm_index`
     - VSCode installation and interface, workspace layout, the
       ``.vscode`` folder, recommended extensions, Command Palette,
       ``CMakeLists.txt``, hybrid per-lecture build setup


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   compiler_warnings/cw_index
   sphinx_breathe/sb_index
   exception_handling/eh_index
   flow_control/fc_index
   linux_shell/ls_index
   input_validation/iv_index
   version_control/vc_index
   vscode_cmake/vcm_index
