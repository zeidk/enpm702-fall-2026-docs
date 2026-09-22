.. _l4-references:

====================================================
References
====================================================


.. dropdown:: Lecture 4
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM702 L4: The Standard Library and Its Containers**

        Covers ``std::size_t`` and the traps of unsigned arithmetic;
        time complexity and how to work out a loop's Big-O; the STL and
        where it sits inside the standard library; the four categories
        of container and the interface they share; C-style arrays,
        contiguity, array decay, pointer arithmetic on an array and
        ``sizeof`` after decay; ``std::array`` and why it never decays;
        multidimensional arrays and row-major order; iterators, the
        half-open range and the three ways to write a loop;
        ``std::vector`` as three pointers and a heap block, its growth,
        reallocation, ``reserve``, ``shrink_to_fit``, insertion, deletion
        and iterator invalidation; C-strings against ``std::string``,
        where a literal lives, the small string optimization, ``find``,
        ``npos``, ``getline`` and ``std::string_view``; ``std::map`` and
        ``std::unordered_map`` and the subscript trap; how to choose a
        container; and the algorithms that take iterators. Lambdas,
        class templates and structured bindings are named where they
        appear and taught in
        :doc:`Lecture 6 </lectures/lecture6/l6_index>`.

.. dropdown:: The standard and the guidelines
    :class-container: sd-border-secondary

    - `N4861, the C++20 working draft <https://timsong-cpp.github.io/cppwp/n4861/>`_.
      Cited on the slides: [support.types.layout] for ``size_t``,
      [stmt.jump] for destruction on scope exit, and [basic.string] for
      ``std::string`` being a contiguous container.
    - `C++ Core Guidelines <https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines>`_.
      Rules cited on the slides: ES.71 (prefer range-based for), I.13 (do not pass an array as a single
      pointer), R.1 (RAII), SL.con.1 (prefer ``std::array`` to a C
      array), SL.con.2 (prefer ``std::vector``), SL.con.3 (avoid bounds
      errors), SL.str.1 (use ``std::string``), SL.str.2 (use
      ``std::string_view`` to refer to character sequences).

.. dropdown:: cppreference
    :class-container: sd-border-secondary

    - `Containers library <https://en.cppreference.com/w/cpp/container>`_,
      including the table of
      `iterator invalidation <https://en.cppreference.com/w/cpp/container#Iterator_invalidation>`_.
    - `std::array <https://en.cppreference.com/w/cpp/container/array>`_
      and `std::size <https://en.cppreference.com/w/cpp/iterator/size>`_.
    - `Iterator library <https://en.cppreference.com/w/cpp/iterator>`_
      and `range-based for <https://en.cppreference.com/w/cpp/language/range-for>`_.
    - `std::vector <https://en.cppreference.com/w/cpp/container/vector>`_:
      `reserve <https://en.cppreference.com/w/cpp/container/vector/reserve>`_,
      `shrink_to_fit <https://en.cppreference.com/w/cpp/container/vector/shrink_to_fit>`_,
      `data <https://en.cppreference.com/w/cpp/container/vector/data>`_,
      `std::erase and std::erase_if <https://en.cppreference.com/w/cpp/container/vector/erase2>`_.
    - `Null-terminated byte strings <https://en.cppreference.com/w/cpp/string/byte>`_,
      `string literals <https://en.cppreference.com/w/cpp/language/string_literal>`_,
      `std::string <https://en.cppreference.com/w/cpp/string/basic_string>`_,
      `string::find <https://en.cppreference.com/w/cpp/string/basic_string/find>`_,
      `std::getline <https://en.cppreference.com/w/cpp/string/basic_string/getline>`_,
      `std::string_view <https://en.cppreference.com/w/cpp/string/basic_string_view>`_.
    - `std::map <https://en.cppreference.com/w/cpp/container/map>`_,
      `map::insert_or_assign <https://en.cppreference.com/w/cpp/container/map/insert_or_assign>`_,
      `map::contains <https://en.cppreference.com/w/cpp/container/map/contains>`_,
      `std::unordered_map <https://en.cppreference.com/w/cpp/container/unordered_map>`_,
      `structured bindings <https://en.cppreference.com/w/cpp/language/structured_binding>`_.
    - `Algorithms library <https://en.cppreference.com/w/cpp/algorithm>`_
      and the `constrained algorithms <https://en.cppreference.com/w/cpp/algorithm/ranges>`_
      of C++20.

.. dropdown:: Where the STL and Big-O came from
    :class-container: sd-border-secondary

    - Alexander Stepanov and Meng Lee, *The Standard Template Library*,
      HP Laboratories Technical Report 95-11(R.1), 1995.
    - Paul Bachmann, *Die analytische Zahlentheorie*, 1894, and Edmund
      Landau, *Handbuch der Lehre von der Verteilung der Primzahlen*,
      1909: the origin of the *O* notation.
    - Donald Knuth, "Big Omicron and big Omega and big Theta", *SIGACT
      News* 8(2), 1976: how the notation entered the analysis of
      algorithms.

.. dropdown:: Recommended reading
    :class-container: sd-border-secondary

    - *A Tour of C++*, Bjarne Stroustrup, third edition: chapter 12
      (Containers) and chapter 13 (Algorithms).
    - *C++ Primer*, Lippman, Lajoie and Moo, fifth edition: chapter 3
      (Strings, Vectors, and Arrays) and chapter 9 (Sequential
      Containers).
    - `LearnCpp.com: introduction to std::vector <https://www.learncpp.com/cpp-tutorial/introduction-to-stdvector-and-list-constructors/>`_,
      `std::vector capacity and stack behavior <https://www.learncpp.com/cpp-tutorial/stdvector-capacity-and-stack-behavior/>`_,
      and `introduction to std::string <https://www.learncpp.com/cpp-tutorial/introduction-to-stdstring/>`_.
