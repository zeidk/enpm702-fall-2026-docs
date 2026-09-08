====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 6: Functions,
Advanced. Work through them in order, as each exercise builds on the
skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1: Struct Usage
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Demonstrate ``struct`` with aggregate initialization and structured bindings.

   **Specification**

   1. Define a ``struct Sensor`` with fields: ``std::string name``, ``double reading``, and ``bool is_active`` (with a default value of ``true``).
   2. Create three ``Sensor`` instances using aggregate initialization.
   3. Write a function ``print_sensor`` that takes a ``const Sensor&`` and prints all fields.
   4. Use structured bindings (``auto [name, reading, active] = ...``) to decompose one sensor and print its fields individually.
   5. Use a reference structured binding (``auto& [...]``) to modify a sensor's reading and verify the change.

.. dropdown:: Exercise 2: Function Templates
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write a set of function templates that perform common operations.

   **Specification**

   1. Write a function template ``clamp(T value, T low, T high)`` that returns ``value`` constrained to the range ``[low, high]``.
   2. Write a function template ``swap_values(T& a, T& b)`` that swaps two values using a temporary.
   3. Write a function template with two type parameters ``auto convert_and_add(T a, U b)`` that adds two values of possibly different types.
   4. Test all three templates with ``int``, ``double``, and (for ``clamp`` and ``swap_values``) ``char``.

.. dropdown:: Exercise 3: Template Specialization
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Write a function template ``to_string_pretty(T value)`` that converts a value to a formatted string, with specializations for ``bool`` and ``double``.

   **Specification**

   1. Write the **generic** version that uses ``std::to_string``.
   2. Write a **full specialization** for ``bool`` that returns ``"true"`` or ``"false"`` (instead of ``"1"`` or ``"0"``).
   3. Write a **full specialization** for ``double`` that formats the number to exactly 2 decimal places using ``std::ostringstream`` with ``std::fixed`` and ``std::setprecision(2)``.
   4. Test with ``int``, ``bool``, and ``double`` values.

.. dropdown:: Exercise 4: Lambda Expressions
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Use lambda expressions with STL algorithms.

   **Specification**

   1. Create a ``std::vector<int>`` with values ``{5, -3, 8, -1, 7, 2, -4, 6}``.
   2. Use ``std::sort`` with a lambda to sort the vector by **absolute value** (ascending).
   3. Use ``std::count_if`` with a lambda to count negative numbers.
   4. Use ``std::transform`` with a lambda to create a new vector where each element is squared.
   5. Use ``std::for_each`` with a lambda that captures a running total by reference to compute the sum.
   6. Use a lambda with the ``mutable`` keyword that captures a counter by value and increments it on each call. Call it 3 times and verify the original variable is unchanged.

.. dropdown:: Exercise 5 std::function Callbacks
   :icon: gear
   :class-container: sd-border-primary
   :class-title: sd-font-weight-bold

   **Goal**

   Demonstrate ``std::function`` as a flexible callback mechanism.

   **Specification**

   1. Write a function ``apply_operation(const std::vector<int>& data, std::function<int(int)> op)`` that applies an operation to each element and returns a new vector.
   2. Define a free function ``negate_value`` that negates an integer.
   3. Define a functor ``ScaleBy`` that multiplies by a configurable factor.
   4. Call ``apply_operation`` three times using: a lambda (double each value), the free function, and the functor.
   5. Demonstrate checking an empty ``std::function`` before calling it.

.. dropdown:: Challenge: Generic Sorting with Templates and Lambdas
   :icon: gear
   :class-container: sd-border-warning
   :class-title: sd-font-weight-bold

   **Goal**

   Write a generic sorting utility that combines templates and lambdas.

   **Specification**

   1. Write a function template ``sort_by(std::vector<T>& data, Comparator comp)`` where ``Comparator`` is also a template parameter. It should implement selection sort (do not use ``std::sort``).
   2. Define a ``struct Student`` with fields: ``std::string name``, ``double gpa``, ``int credits``.
   3. Create a vector of 5 students.
   4. Sort by GPA (descending) using a lambda comparator.
   5. Sort by name (alphabetical) using a lambda comparator.
   6. Sort by credits (ascending) using a lambda comparator.
   7. Print the sorted results after each sort.
