.. The definitions of make_obstacle, lookup and first_pose, included by
.. vcat_lecture.rst and vcat_quiz.rst. _static/vcat-hover.js reads this block
.. (class vcat-defs) to show each definition when the mouse is over the name.

.. code-block:: cpp
   :linenos:
   :class: vcat-defs

   Obstacle make_obstacle(int id) {
     return Obstacle{id};  // the other members take their defaults
   }

   // The Obstacle with this id, or the first one when no id matches.
   Obstacle& lookup(std::vector<Obstacle>& seen, int id) {
     for (Obstacle& obstacle : seen) {
       if (obstacle.id == id) {
         return obstacle;
       }
     }
     return seen[0];
   }

   // The first pose of a path.
   const Pose& first_pose(const std::vector<Pose>& path) {
     return path[0];
   }
