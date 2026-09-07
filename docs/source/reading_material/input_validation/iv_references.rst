References
==========


.. dropdown:: Validating Terminal Input
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Validating Terminal Input**

        Covers the three outcomes of a ``std::cin`` extraction, stream
        state and recovery with ``clear()`` and ``ignore()``, and
        whole-line parsing with ``std::getline`` and
        ``std::from_chars``.


.. dropdown:: Standard Library Documentation
    :class-container: sd-border-secondary

    .. card::
        :class-card: sd-border-secondary

        **cppreference**

        - `std::from_chars <https://en.cppreference.com/w/cpp/utility/from_chars>`_
          -- the C++17 parser used in Approach 2. No exceptions, no
          locale, and it reports where it stopped.
        - `std::basic_istream::ignore <https://en.cppreference.com/w/cpp/io/basic_istream/ignore>`_
          -- discarding the rest of a bad line.
        - `std::basic_ios::clear <https://en.cppreference.com/w/cpp/io/basic_ios/clear>`_
          -- resetting the stream's error state.
        - `std::getline <https://en.cppreference.com/w/cpp/string/basic_string/getline>`_
          -- reading a whole line, including the whitespace.
        - `std::basic_ios::operator bool <https://en.cppreference.com/w/cpp/io/basic_ios/operator_bool>`_
          -- why ``if (std::cin >> x)`` works.
