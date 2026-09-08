====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 4: STL
Containers. Work through them in order, as each exercise builds on
the skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1: String Operations
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate key ``std::string`` operations and observe Small String
    Optimization (SSO).

    **Specification**

    1. Create a short string (fewer than 15 characters) and a long string
       (more than 30 characters).
    2. Print the ``size()`` and ``capacity()`` of each string. Observe the
       difference caused by SSO.
    3. Use ``.insert()`` to insert ``"C++ "`` at the beginning of a string.
    4. Use ``.erase()`` to remove the first 4 characters from a string.
    5. Use ``.append()`` to add ``" is great!"`` to the end.
    6. Use ``.at()`` to access a character. Then try accessing an out-of-bounds
       index and observe the exception.

.. dropdown:: Exercise 2: Array Manipulation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate both C-style arrays and ``std::array``.

    **Specification**

    1. Declare a C-style array of 5 integers and initialize it with values.
    2. Declare a ``std::array<int, 5>`` and initialize it with different values.
    3. Use ``.fill()`` to set all elements of the ``std::array`` to a single value.
    4. Access elements using ``[]`` and ``.at()``.
    5. Use a range-based for loop to print all elements.
    6. Print ``.size()`` and ``.empty()`` for the ``std::array``.

.. dropdown:: Exercise 3: 2D Array
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Create a 3x3 matrix using ``std::array``, fill it with values, and
    print it row by row.

    **Specification**

    1. Declare a 2D ``std::array`` of size 3x3.
    2. Fill the matrix with values 1 through 9
       (``row * 3 + col + 1``).
    3. Print the matrix in a grid format.
    4. Calculate and print the sum of each row.

.. dropdown:: Exercise 4: Vector Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate basic ``std::vector`` operations.

    **Specification**

    1. Create a vector of integers with initial values ``{10, 20, 30}``.
    2. Use ``push_back()`` to add 40 and 50. Print size and capacity
       after each ``push_back()``.
    3. Use ``pop_back()`` to remove the last element.
    4. Use ``front()``, ``back()``, ``[]``, and ``.at()`` to access elements.
    5. Use a range-based for loop to print all elements.

.. dropdown:: Exercise 5: Vector Memory
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate how vector capacity grows dynamically and how to manage
    memory with ``reserve()``, ``resize()``, and ``shrink_to_fit()``.

    **Specification**

    1. Start with an empty vector.
    2. In a loop, ``push_back()`` integers from 0 to 31. Print size and
       capacity each time the capacity changes.
    3. After the loop, use ``reserve(100)`` and print size and capacity.
    4. Use ``shrink_to_fit()`` and print size and capacity.
    5. Use ``resize(10)`` then ``shrink_to_fit()`` again.
    6. Observe the pattern of capacity growth (typically doubles).

.. dropdown:: Exercise 6: Simple Gradebook (Challenge)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Implement a simple gradebook using vectors and strings with iterator
    traversal.

    **Specification**

    1. Store student names in a ``std::vector<std::string>``.
    2. Store each student's grades in a ``std::vector<std::vector<int>>``.
    3. Add at least 3 students with 4 grades each.
    4. Calculate and display the average grade for each student.
    5. Use iterators (not index-based loops) to traverse the containers.
    6. Find and display the student with the highest average.
