====================================================
C++ Exercises
====================================================

Six exercises reinforcing :doc:`Lecture 3 <l3_lecture>`, in the order
the lecture covers the material. Exercises 1 to 4 are **code**, Exercise
5 is a **written** trace done on paper, and Exercise 6 is a **challenge**
that puts the whole lecture together. None of them needs an array;
arrays and the containers that replace them are
:doc:`Lecture 4 </lectures/lecture4/l4_index>`.

.. note::

   **What to submit.** All six, in a **single file** named
   ``firstname_lastname.cpp`` (for example, ``bjarne_stroustrup.cpp``),
   uploaded to **Canvas**. Written answers go in comments. Each code
   exercise gets its own **block** inside ``main()``, headed by a
   comment, so that names do not collide between exercises:

   .. code-block:: cpp

      int main() {
          {   // ===== Exercise 1: Pointer Basics =====

          }

          {   // ===== Exercise 2: Const-Correctness =====

          }
      }

   Keep the ``=====`` markers and the numbering. They are how your work
   gets found.

.. note::

   **Building.** Use the course project in VS Code, exactly as in
   Lecture 1. ``-std=c++20 -Wall -Wextra`` are already set in
   ``CMakeLists.txt``. To build one of these by hand instead:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -Wpedantic -g main.cpp -o main

   The ``-g`` is not optional this week: without it, Valgrind reports
   leaks without telling you which line allocated them.

.. warning::

   Several exercises ask you to write a line that **must not compile**,
   or that is undefined behavior. Comment those lines out before you
   submit, and leave the explanation next to them. A file that does not
   build cannot be graded.

.. note::

   **Memory checking.** Exercises 3 and 6 are checked with Valgrind:

   .. code-block:: bash

      valgrind --leak-check=full ./main

   A clean run ends with ``All heap blocks were freed -- no leaks are
   possible``. Anything else is a bug to fix, not a warning to note.


----


.. dropdown:: Exercise 1: Pointer Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice declaring pointers, using the address-of operator (``&``),
    and dereferencing pointers (``*``).

    **Specification**

    1. Declare an ``int`` variable ``altitude_m`` and initialize it to
       ``42``.
    2. Declare a pointer ``altitude_ptr`` and initialize it to the
       address of ``altitude_m``.
    3. Print the following:

       - The value of ``altitude_m``
       - The address of ``altitude_m`` (using ``&altitude_m``)
       - The value stored in ``altitude_ptr`` (the address it holds)
       - The object ``altitude_ptr`` points at (using ``*altitude_ptr``)

    4. Change ``altitude_m`` through the pointer, with
       ``*altitude_ptr = 100;``.
    5. Print ``altitude_m`` again to confirm the change.
    6. Declare a second ``int`` variable ``target_alt_m{200}`` and point
       ``altitude_ptr`` at it instead.
    7. Print ``*altitude_ptr`` to confirm it now reads
       ``target_alt_m``.

.. dropdown:: Exercise 2: Const-Correctness
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate all three modes of const-correctness with pointers.

    **Specification**

    1. Declare two ``int`` variables: ``altitude_m{120}`` and
       ``target_alt_m{80}``.
    2. Create a **pointer to const data**:
       ``const int* alt_ptr1{&altitude_m};``

       - Try to change the object through it (``*alt_ptr1 = 90;``).
         Comment the line out and note the error.
       - Point ``alt_ptr1`` at ``target_alt_m``. This should work.

    3. Create a **const pointer**: ``int* const alt_ptr2{&altitude_m};``

       - Change the object through it (``*alt_ptr2 = 90;``). This should
         work.
       - Try to point it at ``target_alt_m``. Comment the line out and
         note the error.

    4. Create a **const pointer to const data**:
       ``const int* const alt_ptr3{&altitude_m};``

       - Try to change the object through it. Comment out and note the
         error.
       - Try to point it somewhere else. Comment out and note the error.

    5. For each commented-out line, add a comment explaining **why** it
       fails.

.. dropdown:: Exercise 3: Dynamic Memory with Valgrind
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use ``new`` and ``delete`` for dynamic memory allocation, then
    verify with Valgrind that there are no leaks.

    **Specification**

    1. Dynamically allocate a single ``int`` holding a battery
       percentage:

       .. code-block:: cpp

          int* battery_pct{new int{99}};

    2. Print the value and the address.
    3. Release the memory with ``delete`` and set ``battery_pct`` to
       ``nullptr``.
    4. Dynamically allocate a ``double`` holding a battery voltage:

       .. code-block:: cpp

          double* voltage{new double{11.1}};

    5. Print the value and the address, then write a new value through
       the pointer and print it again.
    6. Deallocate it with ``delete`` and set ``voltage`` to ``nullptr``.
    7. Prove to yourself that a second ``delete`` is now harmless: call
       ``delete voltage;`` once more and explain in a comment why this is
       safe, where it would have been undefined behavior without step 6.
    8. Build the project and run it under Valgrind. Verify the output
       says ``All heap blocks were freed -- no leaks are possible``.
    9. **Intentional leak test:** comment out the two ``delete``
       statements and run Valgrind again. Note how many bytes are
       "definitely lost" and which line numbers it names.

.. dropdown:: Exercise 4: Reference vs. Pointer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Perform the same operations using both a pointer and a reference,
    then compare the behavior.

    **Specification**

    1. Declare an ``int`` variable ``altitude_m{50}``.
    2. Create a pointer ``alt_ptr`` to it and a reference ``alt`` to it.
    3. Print the object each one reaches (``*alt_ptr`` and ``alt``) and
       the address each one reaches (``alt_ptr`` and ``&alt``).
    4. Change ``altitude_m`` through the pointer (``*alt_ptr = 75;``) and
       print all three (``altitude_m``, ``*alt_ptr``, ``alt``).
    5. Change it through the reference (``alt = 100;``) and print all
       three again.
    6. Declare a second variable ``target_alt_m{120}``.

       - Point ``alt_ptr`` at ``target_alt_m``.
       - Try to "repoint" ``alt`` at it as well (``alt = target_alt_m;``)
         and watch what actually happens.

    7. Print ``altitude_m``, ``*alt_ptr``, ``alt`` and ``target_alt_m``
       to show the difference.

    **Key observation:** ``alt = target_alt_m;`` does **not** rebind the
    reference. It copies the value of ``target_alt_m`` into
    ``altitude_m``, the object ``alt`` names.

.. dropdown:: Exercise 5: Memory Tracing
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Analyze code on paper to trace memory allocation/deallocation and
    identify issues (dangling pointers, memory leaks).

    **Trace the following code:**

    .. code-block:: cpp
       :linenos:

       #include <iostream>

       int main() {
           int* imu_reading{new int{10}};
           int* gps_reading{new int{20}};
           int* imu_copy{imu_reading};

           std::cout << *imu_reading << '\n';
           std::cout << *gps_reading << '\n';
           std::cout << *imu_copy << '\n';

           delete imu_reading;
           imu_reading = nullptr;

           *gps_reading = 30;

           std::cout << *gps_reading << '\n';

           gps_reading = new int{40};

           std::cout << *gps_reading << '\n';

           delete gps_reading;
           gps_reading = nullptr;

           return 0;
       }

    **Tasks**

    1. For each line, state what happens in memory.
    2. After line 6, draw a diagram showing which pointers point where.
    3. After line 12, identify any dangling pointers. Is ``imu_copy``
       dangling?
    4. After line 19, identify any memory leaks. Has the first
       ``gps_reading`` block (value 20) been freed?
    5. Identify **all** issues in this code (dangling pointers, memory
       leaks, undefined behavior).
    6. Rewrite the code to fix all issues.

.. dropdown:: Exercise 6: Make It Valgrind-Clean (Challenge)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Take a program that compiles without a single warning, find every
    memory defect in it, and fix them all. This is the exercise that most
    resembles what you will actually do with this material.

    **The program**

    .. code-block:: cpp
       :linenos:

       #include <iostream>

       int main() {
           int* imu_reading{new int{121}};
           int* gps_reading{new int{118}};

           int* best{nullptr};
           if (*imu_reading > *gps_reading) { best = imu_reading; }
           std::cout << "best: " << *best << '\n';

           int* backup{gps_reading};
           delete gps_reading;
           delete backup;

           gps_reading = new int{119};
           imu_reading = gps_reading;
           std::cout << "imu: " << *imu_reading << '\n';

           delete imu_reading;
       }

    **Tasks**

    1. Without running it, find the defects. There are **four**, one of
       each failure mode from the lecture: a null dereference waiting to
       happen, a memory leak, a double delete, and a pointer left
       dangling.
    2. Say which line each one is on, and what the smallest fix is.
    3. One of the four does not go wrong with *these* numbers, but would
       with different readings. Which one, and what readings would set it
       off?
    4. Fix the program. It must print the larger reading, then ``119``,
       and finish with Valgrind reporting ``All heap blocks were freed --
       no leaks are possible`` and ``ERROR SUMMARY: 0 errors``.
    5. In two or three sentences, explain which of the four defects would
       disappear on their own if both readings were owned by
       ``std::unique_ptr`` instead of raw pointers.

    .. dropdown:: Hint: what to look for
        :class-container: sd-border-info

        Ask of every heap block: **who owns it**, and is that still true
        on the next line? Three of the four defects are that question
        going wrong: one block with two owners, one block with none, one
        block freed twice. The fourth is a pointer the program follows
        without ever checking whether it points at anything.
