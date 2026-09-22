.. _l4-exercises:

====================================================
C++ Exercises
====================================================

Eight exercises reinforcing :doc:`Lecture 4 <l4_lecture>`, in the order
the lecture covers the material. Exercises 1 to 7 are **code**, and
Exercise 8 is a **challenge** that puts the containers and the
algorithms together.
None of them needs a function of your own, a class or a lambda; those
are Lectures 5 and 6.

.. note::

   **What to submit.** All eight, in a **single file** named
   ``firstname_lastname.cpp`` (for example, ``bjarne_stroustrup.cpp``),
   uploaded to **Canvas**. Each exercise gets its own **block** inside
   ``main()``, headed by a comment, so that names do not collide between
   exercises:

   .. code-block:: cpp

      int main() {
          {   // ===== Exercise 1: Two Kinds of Array =====

          }

          {   // ===== Exercise 2: Row-major Order =====

          }
      }

   Keep the ``=====`` markers and the numbering. They are how your work
   gets found.

.. note::

   **Building.** Work in the course project in VS Code, exactly as in
   Lecture 1. Write your code in ``project/week4/src/main.cpp``, make
   sure ``add_subdirectory(project/week4)`` is uncommented in the
   top-level ``CMakeLists.txt``, then open the Command Palette
   (``Ctrl + Shift + P``), run *CMake: Set Build Target* and pick
   ``week4``, and run *CMake: Build*. ``-std=c++20 -Wall -Wextra
   -pedantic-errors`` are already set for you.

   Submit a **copy** of that file renamed ``firstname_lastname.cpp``.
   The name is for grading; the file you actually build is
   ``project/week4/src/main.cpp``.

   Exercise 5 asks for AddressSanitizer. The two lines that turn it on
   are in ``project/week4/CMakeLists.txt``, commented out; uncomment
   them for that exercise and comment them back before you submit.

.. warning::

   Several exercises ask you to write a line that **must not compile**,
   or that is undefined behaviour. Comment those lines out before you
   submit, and leave the explanation next to them. A file that does not
   build cannot be graded.

.. note::

   **Headers you will need**, all at the top of the file:
   ``<algorithm>``, ``<array>``, ``<cstddef>``, ``<cstring>``,
   ``<iostream>``, ``<map>``, ``<numeric>``, ``<string>``,
   ``<unordered_map>``, ``<utility>``, ``<vector>``.


----




.. dropdown:: Exercise 1 (code): Two Kinds of Array
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    See decay happen, see ``std::array`` refuse to decay, and see the
    difference between the two subscripts.

    **Specification**

    .. code-block:: cpp

       {   // ===== Exercise 1: Two Kinds of Array =====

           // TODO 1: declare int c_deg[6] holding 10, 20, 30, 40, 50, 60,
           //         and std::array<int, 6> s_deg holding the same values.

           // TODO 2: print sizeof(c_deg), sizeof(s_deg), and
           //         std::size(c_deg) and s_deg.size(). In a comment, say
           //         why the two sizeof values are equal.

           // TODO 3: print the addresses &c_deg[0], &c_deg[1] and
           //         &c_deg[2]. In a comment, say how many bytes apart
           //         they are and what that number is.

           // TODO 4: int* p{c_deg};  then print *(p + 2) and c_deg[2].
           //         In a comment, write the definition of c_deg[2] in
           //         terms of p, from the lecture.

           // TODO 5: write  int* q{s_deg};  Comment it out with the
           //         compiler's error next to it, then write the line
           //         that DOES give you a pointer into s_deg.

           // TODO 6: print s_deg.at(2), then write s_deg.at(9) inside a
           //         try block and print what the exception's what()
           //         says. (Exceptions are a reading module; catch
           //         const std::out_of_range& e and print e.what().)

           // TODO 7: write  s_deg[9] = 1;  and comment it out with a note
           //         saying what kind of error this is and why the
           //         compiler said nothing.
       }


----


.. dropdown:: Exercise 2 (code): Row-major Order
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Store an occupancy grid in one flat block and index it by hand, the
    way a real costmap does.

    **Specification**

    The grid from the lecture, three rows of four cells:

    .. code-block:: text

       0  0  1 -1
       0  0  1 -1
       1  0  0  0

    .. code-block:: cpp

       {   // ===== Exercise 2: Row-major Order =====

           // TODO 1: std::size_t rows{3}; std::size_t cols{4};
           //         Declare std::vector<int> grid(rows * cols, 0) and
           //         fill it with the twelve values above, in row-major
           //         order, using ONE range of push_back-free writes:
           //         grid[i * cols + j] = ...

           // TODO 2: print the grid as three lines of four numbers using
           //         two nested loops, rows outside, columns inside.

           // TODO 3: print the flat index and the value of the cell at
           //         row 1, column 2, and of the cell at row 2, column 0.

           // TODO 4: count the blocked cells (value 1) with std::count,
           //         passing grid.begin() and grid.end(), and print the
           //         count.

           // TODO 5: in a comment, give the flat index of row r, column
           //         c for a grid with 5 columns instead of 4, and say
           //         which of the two numbers, rows or columns, the
           //         formula needs.
       }


----


.. dropdown:: Exercise 3 (code): Three Loops and One Erase
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write the three traversals from the lecture, use a const iterator,
    and erase while looping without skipping an element.

    **Specification**

    .. code-block:: cpp

       {   // ===== Exercise 3: Three Loops and One Erase =====

           // TODO 1: std::vector<double> ranges_m{3.55, 0.20, 1.28, 0.10, 4.12};

           // TODO 2: print every element three times over: once by
           //         index, once by iterator, once with a range-based
           //         for that takes const auto&. One line per loop.

           // TODO 3: print ranges_m.end() - ranges_m.begin(). In a
           //         comment, say what number that is and why it needs
           //         no plus or minus one.

           // TODO 4: auto ct{ranges_m.cbegin()};  then write *ct = 0.0;
           //         and comment it out with the compiler's error.

           // TODO 5: remove every reading below 0.5 by looping with an
           //         iterator and  it = ranges_m.erase(it);  when the
           //         element goes, ++it when it stays. Print what is
           //         left. In a comment, say why ++it after erase would
           //         skip an element.

           // TODO 6: restore the five values and do the same removal in
           //         ONE line with std::erase_if and a named predicate.
           //         (A predicate is a function; write  bool is_close(double r)
           //         above main(). It is the one function this file
           //         needs, and Lecture 5 explains the rest.)
       }


----


.. dropdown:: Exercise 4 (code): Growth, Reserve and Shrink
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Watch capacity grow, count the reallocations yourself, remove them
    with ``reserve``, and see what ``shrink_to_fit`` costs.

    **Specification**

    .. code-block:: cpp

       {   // ===== Exercise 4: Growth, Reserve and Shrink =====

           // TODO 1: before running anything, write in a comment the
           //         size/capacity you expect after each of ten
           //         push_back calls on an empty std::vector<int>, and
           //         how many reallocations that is.

           // TODO 2: now do it. Keep  const int* block{v.data()};
           //         before the loop; inside it, after each push_back,
           //         compare v.data() with block. When they differ, print
           //         "moved at push i" and update block. Print
           //         size/capacity on every pass. Count the moves.

           // TODO 3: compare with your prediction in a comment. Then say
           //         which of these facts the standard promises and
           //         which belong to libstdc++: the exact capacities,
           //         geometric growth, every element moved on each
           //         reallocation.

           // TODO 4: repeat TODO 2 on a fresh vector after v.reserve(10).
           //         How many moves now? In a comment, say what else
           //         reserve prevents, using the lecture's word for it.

           // TODO 5: on the reserved vector, print capacity, call
           //         v.clear(), print capacity again, then
           //         v.shrink_to_fit() and print once more. In a
           //         comment, say why shrink_to_fit is allowed to do
           //         nothing, and why, when it does something, it moves
           //         every element.
       }


----


.. dropdown:: Exercise 5 (code): Iterator Invalidation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Produce Lecture 3's use-after-free without writing ``new`` or
    ``delete``, see AddressSanitizer name it, and fix it two ways.

    **Specification**

    .. code-block:: cpp

       {   // ===== Exercise 5: Iterator Invalidation =====

           // TODO 1: std::vector<int> ranges_m{10, 20, 30};
           //         int* first{&ranges_m[0]};
           //         ranges_m.push_back(40);
           //         std::cout << *first << '\n';
           //         Run it once WITHOUT the sanitizer and record in a
           //         comment what it printed.

           // TODO 2: uncomment the two -fsanitize lines in
           //         project/week4/CMakeLists.txt, rebuild, run again, and
           //         copy the first line of the report into a comment.
           //         Name the Lecture 3 bug it is.

           // TODO 3: fix A: reserve. Add ONE line before taking the
           //         pointer so that the push cannot move the block.
           //         Confirm the sanitizer is now quiet.

           // TODO 4: fix B: take the pointer AFTER the push instead.
           //         Explain in a comment which fix you would use in a
           //         loop that keeps pushing, and why.

           // TODO 5: using the invalidation table from the lecture, say
           //         in a comment whether an iterator to element 0
           //         survives each of: pop_back(); erase(begin() + 2);
           //         clear(); at(1). Then comment the two sanitizer lines
           //         back out.
       }


----


.. dropdown:: Exercise 6 (code): Two Kinds of String
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Tell a C-string from a ``std::string`` by what each one stores, and
    fix the ``getline`` trap.

    **Specification**

    .. code-block:: cpp

       {   // ===== Exercise 6: Two Kinds of String =====

           // TODO 1: auto name{"lidar_front"};  Print sizeof(name) and
           //         std::strlen(name). In a comment, say what each
           //         number measures and where the eleven characters
           //         live.

           // TODO 2: write  name[0] = 'L';  and comment it out with the
           //         compiler's error. Then write  name = "imu";  and
           //         print name. In a comment, say what changed and what
           //         did not.

           // TODO 3: char copy[]{"lidar_front"};  Print sizeof(copy) and
           //         std::strlen(copy), change copy[0] to 'L', and print
           //         copy. In a comment, say why this write is allowed
           //         when the one in TODO 2 was not.

           // TODO 4: using namespace std::literals;
           //         auto topic{"/robot/scan"s};
           //         Print topic.size(), topic.capacity() and
           //         sizeof(topic). In a comment, explain the third
           //         number and where the characters live for a string
           //         this short.

           // TODO 5: print topic.find("scan") and topic.find("imu").
           //         Print the second one with std::string::npos next to
           //         it, then write the if statement that correctly tests
           //         whether "imu" is present.

           // TODO 6: read an int id and then a whole line into a
           //         std::string with std::getline. Type 7, Enter,
           //         /robot/scan, Enter. Record what topic holds. Then
           //         apply the lecture's fix and record it again.
       }


----


.. dropdown:: Exercise 7 (code): A Sensor Registry
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use ``[]``, ``at``, ``find`` and ``contains`` each for what it is
    for, and see the difference between the two maps.

    **Specification**

    .. code-block:: cpp

       {   // ===== Exercise 7: A Sensor Registry =====

           // TODO 1: std::unordered_map<std::string, std::vector<double>> readings;
           //         Push 2.31 and 2.28 onto "lidar" and 0.04 onto "imu"
           //         using readings[name].push_back(...). In a comment,
           //         say why [] is the right call HERE.

           // TODO 2: print readings.size(). Then write
           //         double last{readings["gps"].back()};  comment it out,
           //         and say in a comment what it would do to the map
           //         and why back() on the result is undefined behaviour.

           // TODO 3: look up "gps" with find and print either its last
           //         reading or "no gps readings yet". Then do the same
           //         test with contains.

           // TODO 4: write readings.at("gps") inside a try block, catch
           //         const std::out_of_range& e, and print e.what().

           // TODO 5: loop over the map with a structured binding and
           //         print each name with its sample count. Run it twice
           //         and note in a comment whether the order is
           //         promised.

           // TODO 6: build a std::map<std::string, double> periods from
           //         {"lidar", 0.25}, {"imu", 0.01}, {"camera", 0.05},
           //         inserted in that order, and print the names in a
           //         loop. In a comment, say why the order differs from
           //         the insertion order and which container you would
           //         pick for a report sorted by name.

           // TODO 7: periods.insert({"imu", 99.0}); then print
           //         periods.at("imu"). Then periods.insert_or_assign("imu", 99.0);
           //         and print again. In a comment, explain both results.
       }


----


.. dropdown:: Exercise 8 (challenge): A Scan Pipeline
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Put the lecture together on one lidar scan: pick the container,
    reserve it, fill it, and process it with algorithms instead of hand
    loops.

    **Specification**

    A lidar scan is 1080 range values in metres. Readings below 0.1 are
    sensor noise, and readings above 25.0 mean nothing was hit. Write a
    single block that:

    1. Declares the scan as the container the lecture says to use for
       "count known before the first sample, at run time", sized for
       1080 with no reallocation during the fill. Say in a comment why it
       is not ``std::array``.
    2. Fills it with 1080 synthetic readings: reading *i* is
       ``0.05 + (i % 300) * 0.1``. In a comment, work out from the formula
       how many readings are below 0.1 and how many are above 25.0,
       before you run anything.
    3. Prints how many readings were moved by the fill, using the
       ``data()`` comparison from Exercise 4. It must be 0.
    4. Removes the noise and the misses with two ``std::erase_if`` calls
       and two named predicates, and prints ``size()`` and ``capacity()``
       afterwards. In a comment, say why the capacity did not change and
       what would change it.
    5. Prints the nearest and the farthest remaining reading with
       ``std::min_element`` and ``std::max_element``, the number of
       readings closer than 1.0 with ``std::count_if`` and a third
       predicate, and the mean with ``std::accumulate``. Say in a
       comment what the mean would print if the seed were ``0`` instead
       of ``0.0``.
    6. Sorts the scan with ``std::ranges::sort`` and prints the first
       three and the last three readings using ``front()``, ``back()``
       and the subscript.
    7. Stores the sorted readings by a tenth-of-a-metre bucket in a
       ``std::map<int, int>`` that counts how many readings fall in each
       bucket, using ``operator[]`` on purpose, and prints the five
       fullest buckets. In a comment, say why ``[]`` is the honest choice
       here and why the buckets come out in order.

    .. note::

       Every predicate is a one-line function above ``main()`` of the
       form ``bool is_noise(double r) { return r < 0.1; }``. That is the
       only kind of function this exercise needs.
