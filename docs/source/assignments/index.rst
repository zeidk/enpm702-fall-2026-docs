====================================================
Assignments
====================================================

.. warning::

   The RWAs and GPs described on this page are **tentative and subject to
   change**. Requirements, point values, and due dates may be revised as
   the semester progresses. The content of this page is provided for
   planning only; always check **ELMS-Canvas** for the authoritative,
   up-to-date version of each assignment.

This course includes three individual **Real-World Applications (RWAs)**
focused on core C++ and two team-based **Group Projects (GPs)** focused
on ROS 2 development. Both RWAs and GPs are **cumulative**: each
deliverable builds on the previous one.


Real-World Applications (RWAs)
------------------------------

The RWAs progressively build a C++ application using robotics-themed
use cases. Each RWA refactors and extends the previous one,
demonstrating why each new C++ feature improves the codebase.

.. note::

   Only **RWA1**, **RWA2** and **RWA3** are published so far. The other rows here,
   and the group projects below, are the plan for the semester. Each one
   becomes a link when that assignment is released.

.. list-table::
   :header-rows: 1
   :widths: 15 40 15 15 15
   :class: compact-table

   * - Assignment
     - Focus
     - Posted
     - Due
     - Duration
   * - :doc:`RWA1 <rwa1>`
     - Pointers, References, and Dynamic Memory
     - Sep 15
     - Oct 1
     - 2 weeks
   * - :doc:`RWA2 <rwa2>`
     - STL Containers and Functions
     - Oct 9
     - Oct 23
     - 2 weeks
   * - :doc:`RWA3 <rwa3>`
     - Smart Pointers and OOP
     - Nov 3
     - Nov 17
     - 2 weeks


Group Projects (GPs)
---------------------

The two GPs build one ROS 2 application for a mobile robot that patrols
a building. GP1 runs in the terminal, with a stand-in robot node. GP2
runs the same nodes on a simulated robot in Gazebo.

.. list-table::
   :header-rows: 1
   :widths: 15 40 15 15 15
   :class: compact-table

   * - Project
     - Focus
     - Posted
     - Due
     - Duration
   * - :doc:`GP1 <gp1>`
     - Patrol and Inspect (terminal only)
     - Nov 17
     - Nov 24
     - 1 week
   * - :doc:`GP2 <gp2>`
     - Patrol and Inspect in Gazebo (parameters, services, actions, frames)
     - Nov 24
     - Dec 11
     - About 2.5 weeks


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   rwa1
   rwa2
   rwa3
   gp1
   gp2
