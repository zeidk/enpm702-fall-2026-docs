====================================================
Documentation with Sphinx and Breathe
====================================================

Overview
--------

This reading material shows a second way to build reference pages from
Doxygen comments. Doxygen reads the comments, **Sphinx** builds the pages, and
**Breathe** is the Sphinx extension that connects the two. It is a self-study
reading module. Work through it after
:doc:`Lecture 5 </lectures/lecture5/l5_lecture>`, which writes the comments and
builds the pages with Doxygen alone. It uses the same program,
``project/week5/arm_demo``.

.. admonition:: Learning Objectives
   :class: learning-objectives

   By the end of this material, you will be able to:

   - Make Doxygen write XML as well as HTML.
   - Create a Sphinx project and configure Breathe to read Doxygen's XML.
   - Choose the Breathe directive that shows a file, a function or a whole
     project.
   - Rebuild the pages after a comment changes, running both tools in the
     right order.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   sb_lecture
   sb_references
