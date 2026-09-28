====================================================
Lecture
====================================================

Lecture 5 builds the reference pages with Doxygen alone. This page shows a
second way, used by many projects: Doxygen reads the comments, **Sphinx** builds
the pages, and **Breathe** is the Sphinx extension that connects the two. It
reads the XML that Doxygen writes and turns it into Sphinx pages, like the ones
you are reading now.

.. code-block:: text

   comments in include/  ->  doxygen  ->  docs/xml/  ->  sphinx + breathe  ->  docs/sphinx/build/html/

Every path below is relative to ``project/week5/arm_demo/``, the program from
the Documenting Functions section of
:doc:`Lecture 5 </lectures/lecture5/l5_lecture>`.

.. note::

   Tested on Ubuntu 24.04 with Doxygen 1.9.8, Sphinx 9.1.0, Breathe 5.0.0 and
   Furo 2025.12.19.


1. Install
==========

Doxygen comes from apt, as in Lecture 5. Sphinx, Breathe and the Furo theme
go in a Python virtual environment:

.. code-block:: bash

   sudo apt install doxygen python3-venv
   cd project/week5/arm_demo
   python3 -m venv .venv
   source .venv/bin/activate
   pip install sphinx breathe furo

The course repository already ignores ``.venv/``, so it is never committed.

The apt packages ``python3-sphinx`` and ``python3-breathe`` also work, but they
are older (Sphinx 7.2.6 and Breathe 4.35.0 on Ubuntu 24.04).


2. Make Doxygen Write XML
=========================

Breathe reads Doxygen's XML, not its HTML, and XML is off by default. Change one
key in ``docs/Doxyfile`` and keep the other settings as they are:

.. code-block:: text

   GENERATE_XML   = YES

Then run Doxygen from ``docs``, as always:

.. code-block:: bash

   cd docs
   doxygen Doxyfile
   ls              # Doxyfile  html  xml

``docs/xml/index.xml`` must exist before you go on.


3. Create the Sphinx Project
============================

Still in ``docs``:

.. code-block:: bash

   sphinx-quickstart -q -p "Lecture 5" -a "ENPM702" --sep sphinx

This creates ``docs/sphinx/`` with ``source/`` (your pages and ``conf.py``) and
``build/`` (the output). ``--sep`` keeps the two apart.


4. Configure Breathe
====================

``sphinx-quickstart`` already wrote ``extensions = []`` and
``html_theme = 'alabaster'`` into ``docs/sphinx/source/conf.py``. **Edit those two
lines in place.**

.. warning::

   Do not add a second copy of those lines. ``conf.py`` runs from top to bottom,
   so the last assignment wins, and a Breathe block placed above the defaults is
   silently undone.

The finished file:

.. code-block:: python

   project = 'Lecture 5'
   copyright = '2026, ENPM702'
   author = 'ENPM702'

   extensions = ['breathe']

   templates_path = ['_templates']
   exclude_patterns = []

   # -- Breathe -----------------------------------------------------------------
   # Relative to this file (docs/sphinx/source), so this is docs/xml.

   breathe_projects = {'lecture5': '../../xml'}
   breathe_default_project = 'lecture5'

   html_theme = 'furo'
   html_static_path = ['_static']

``../../xml`` is relative to ``conf.py``, which sits in ``docs/sphinx/source/``,
so it points at ``docs/xml/``.


5. Write the Pages
==================

``docs/sphinx/source/index.rst``:

.. code-block:: rst

   Lecture 5
   =========

   .. toctree::
      :maxdepth: 2

      api

``docs/sphinx/source/api.rst``:

.. code-block:: rst

   API Reference
   =============

   .. doxygenfile:: kinematics.hpp
   .. doxygenfile:: joint_limits.hpp

Useful directives:

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Directive
     - Shows
   * - ``.. doxygenfile:: kinematics.hpp``
     - everything declared in one file
   * - ``.. doxygenfunction:: convert_deg_to_rad``
     - one function
   * - ``.. doxygenclass:: JointLimits``
     - one class (later lectures)
   * - ``.. doxygenindex::``
     - everything Doxygen found

Use ``doxygenfile`` **or** ``doxygenfunction`` for a given function, not both.
With both, Sphinx warns ``Duplicate C++ declaration``.

``doxygenindex`` gives the same warning here. ``INPUT`` covers ``src`` as well as
``include``, so each function is found twice: once in its header and once in its
``.cpp``. List the headers with ``doxygenfile`` instead.


6. Build and Open
=================

.. code-block:: bash

   cd docs/sphinx
   make html
   xdg-open build/html/index.html

``make html`` runs ``sphinx-build -M html source build``.


Rebuilding After a Change
=========================

Sphinx does not run Doxygen. After you edit a comment, run both, in this order:

.. code-block:: bash

   cd docs && doxygen Doxyfile && cd sphinx && make html

If you skip the first step, Sphinx rebuilds from the old XML and the page does
not change.


Notes
=====

- **Keep** ``@file`` **on every header**, as Lecture 5 says. Without it,
  Doxygen gives the header no page of its own.
- **What to commit:** only the ``Doxyfile``. The course repository ignores
  ``docs/html/``, ``docs/xml/`` and the whole of ``docs/sphinx/``, so the Sphinx
  project stays on your machine. Rebuild it from steps 3 to 5 on a new clone.
