====================================================
C++ Exercises
====================================================

These exercises reinforce the concepts covered in Lecture 7: Smart
Pointers and Move Semantics. Work through them in order, as each
exercise builds on the skills from the previous one.

.. note::

   Compile all programs with warnings enabled:

   .. code-block:: bash

      g++ -std=c++20 -Wall -Wextra -o program program.cpp


----


.. dropdown:: Exercise 1: Unique Pointer Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate basic ``std::unique_ptr`` usage.

    **Specification**

    1. Create a ``std::unique_ptr<int>`` using ``std::make_unique``
       with value ``42``.
    2. Print the value by dereferencing the pointer.
    3. Print the raw address using ``get()``.
    4. Modify the managed value and print the new value.
    5. Call ``reset()`` without arguments and verify the pointer is
       ``nullptr``.
    6. Call ``reset(new int(100))`` to manage a new resource and print
       the new value.

.. dropdown:: Exercise 2 Ownership Transfer with std::move
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate ownership transfer between ``std::unique_ptr`` instances
    and into sink functions.

    **Specification**

    1. Create a ``std::unique_ptr<std::string>`` managing ``"Hello, ENPM702!"``.
    2. Print the value and address.
    3. Transfer ownership to a second ``std::unique_ptr`` using ``std::move``.
    4. Verify the original pointer is ``nullptr`` and the new one holds
       the resource.
    5. Create a sink function ``void consume(std::unique_ptr<std::string> ptr)``
       that prints the string. Call it with ``std::move``.
    6. Verify the source pointer is ``nullptr`` after the call.

.. dropdown:: Exercise 3: Shared Pointer and Reference Counting
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate ``std::shared_ptr`` and its reference counting mechanism.

    **Specification**

    1. Create a ``std::shared_ptr<int>`` using ``std::make_shared``
       with value ``10``. Print ``use_count()``.
    2. Create two more shared pointers by copying. Print ``use_count()``
       after each copy.
    3. Reset the first pointer and print ``use_count()`` on the others.
    4. Let one pointer go out of scope (nested block) and print the
       final ``use_count()``.
    5. Confirm the resource is still alive.

.. dropdown:: Exercise 4: Weak Pointer Lifetime Observation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Demonstrate how ``std::weak_ptr`` observes a resource without
    extending its lifetime.

    **Specification**

    1. Declare a ``std::weak_ptr<int>`` outside a block scope.
    2. Inside a block, create a ``std::shared_ptr<int>`` with value
       ``100`` and assign it to the weak pointer.
    3. Inside the block, use ``lock()`` to access the resource and
       check ``expired()``.
    4. After the block, check ``expired()`` again.
    5. Attempt to ``lock()`` and handle the case where the resource
       no longer exists.

.. dropdown:: Exercise 5: Factory Function Returning unique_ptr
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use the factory function pattern to create objects with
    ``std::unique_ptr``.

    **Specification**

    1. Define a struct ``Sensor`` with ``std::string name`` and
       ``double reading``.
    2. Write a factory function ``create_sensor`` that returns a
       ``std::unique_ptr<Sensor>``.
    3. Call the factory and print the sensor's fields.
    4. Transfer ownership to a second pointer and verify the original
       is ``nullptr``.
    5. Write a reseat function ``void recalibrate(std::unique_ptr<Sensor>& ptr)``
       that resets the sensor to a new one.

.. dropdown:: Exercise 6: Resource Manager with Smart Pointers (Challenge)
    :icon: gear
    :class-container: sd-border-warning
    :class-title: sd-font-weight-bold

    **Goal**

    Design a resource manager demonstrating all three smart pointer
    types working together.

    **Specification**

    1. Define a ``Resource`` class with a ``std::string id`` member.
       Print messages in constructor and destructor.
    2. Write a ``ResourceManager`` class with:

       - ``std::vector<std::shared_ptr<Resource>>`` registry
       - ``add_resource(const std::string& id)``
       - ``get_resource(int index)`` returning ``std::shared_ptr``
       - ``get_observer(int index)`` returning ``std::weak_ptr``
       - ``remove_resource(int index)``

    3. In ``main()``:

       a. Create a manager and add three resources.
       b. Get a ``shared_ptr`` to the second resource, print ``use_count()``.
       c. Get a ``weak_ptr`` observer to the same resource.
       d. Remove it from the manager.
       e. Check if the resource is still alive via the shared pointer.
       f. Reset the shared pointer and check ``expired()`` on the weak pointer.
