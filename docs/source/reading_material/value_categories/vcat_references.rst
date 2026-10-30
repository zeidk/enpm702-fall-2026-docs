====================================================
References
====================================================

.. dropdown:: Value Categories
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **Value Categories**

        The three categories (lvalue, xvalue, prvalue) and the two groups
        (glvalue, rvalue). Four steps to find the category of any
        expression, the ``CATEGORY`` helper, worked examples, five traps,
        and why the category decides reference binding and the choice
        between a copy and a move. It extends the Value Categories part
        of :doc:`Lecture 7 </lectures/lecture7/l7_lecture>`.


.. dropdown:: The C++20 Standard
    :class-container: sd-border-secondary

    The page quotes the C++20 draft N4861. Each card opens one section of
    it.

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: [basic.lval]
            :link: https://timsong-cpp.github.io/cppwp/n4861/basic.lval
            :class-card: sd-border-secondary

            **7.2.1 Value category**: the tree and the five definitions

        .. grid-item-card:: [expr.call]
            :link: https://timsong-cpp.github.io/cppwp/n4861/expr.call
            :class-card: sd-border-secondary

            **7.6.1.2 Function call**: paragraph 14, the category of a call

        .. grid-item-card:: [class.temporary]
            :link: https://timsong-cpp.github.io/cppwp/n4861/class.temporary
            :class-card: sd-border-secondary

            **6.7.7 Temporary objects**: when a temporary is destroyed, and
            when a reference extends its life


.. dropdown:: cppreference Links
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Value categories
            :link: https://en.cppreference.com/w/cpp/language/value_category
            :class-card: sd-border-secondary

            **cppreference: Value categories**, with a list of the
            expressions in each category

        .. grid-item-card:: decltype
            :link: https://en.cppreference.com/w/cpp/language/decltype
            :class-card: sd-border-secondary

            **cppreference: decltype specifier**

        .. grid-item-card:: References
            :link: https://en.cppreference.com/w/cpp/language/reference
            :class-card: sd-border-secondary

            **cppreference: Reference declaration**, lvalue and rvalue
            references

        .. grid-item-card:: std::move
            :link: https://en.cppreference.com/w/cpp/utility/move
            :class-card: sd-border-secondary

            **cppreference: std::move**

        .. grid-item-card:: Lifetime
            :link: https://en.cppreference.com/w/cpp/language/lifetime
            :class-card: sd-border-secondary

            **cppreference: Lifetime**, with the lifetime of temporaries
