====================================================
Lecture
====================================================


Linux Shell
====================================================


.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Definition**

    A :term:`shell <Shell>` is a program that provides a command-line
    interface (CLI) for users to interact with the operating system,
    allowing them to execute commands, run scripts, manage files, and
    control processes.


Common Shell Types
------------------

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Bash
        :class-card: sd-border-secondary

        `Bourne Again Shell <https://www.gnu.org/software/bash/>`_

        The default shell for most Linux distributions, known for its
        scripting capabilities.

    .. grid-item-card:: Zsh
        :class-card: sd-border-secondary

        `Z Shell <https://www.zsh.org/>`_

        Similar to Bash, with additional features like better
        autocompletion and customization options.

    .. grid-item-card:: Fish
        :class-card: sd-border-secondary

        `Friendly Interactive Shell <https://fishshell.com/>`_

        User-friendly and highly customizable, with a focus on simplicity.

    .. grid-item-card:: Csh / Tcsh
        :class-card: sd-border-secondary

        `C Shell / Tenex C Shell <https://www.tcsh.org/>`_

        Shells with syntax similar to the C programming language, often
        used in certain Unix environments.

    .. grid-item-card:: Ksh
        :class-card: sd-border-secondary

        `Korn Shell <http://www.kornshell.com/>`_

        A shell with advanced scripting features, sometimes used in
        enterprise environments.

.. tip::

   Check your current shell with:

   .. code-block:: bash

      ps -p $$


Configuration Files
-------------------

A :term:`shell configuration file <Configuration File (Shell)>` is a
script that runs each time a new shell session starts. It allows users to
customize their shell environment by defining settings, aliases,
functions, and environment variables.

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - Shell
     - Config File
     - Location
   * - Bash
     - ``.bashrc``
     - Home directory (``~/``)
   * - Zsh
     - ``.zshrc``
     - Home directory (``~/``)
   * - Fish
     - ``config.fish``
     - ``~/.config/fish/``
   * - Csh / Tcsh
     - ``.cshrc``
     - Home directory (``~/``)
   * - Ksh
     - ``.kshrc``
     - Home directory (``~/``)

.. note::

   In most Unix-like operating systems (including Ubuntu), the tilde
   ``~`` symbol refers to the current user's home directory.
   ``cd ~`` takes you to your home directory.


Aliases
^^^^^^^

:term:`Aliases <Alias>` are shortcuts that save you from having to
remember or type long commands.

.. code-block:: bash

   alias identifier='value'

- An alias declaration starts with the ``alias`` keyword, followed by the
  alias name, an equal sign, and the command to be run.
- The command should be enclosed in quotes, with **no spaces around the
  equal sign**.
- Each alias should be declared on a separate line.

.. dropdown:: Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: bash

       alias cdd='cd ~/Documents'
       alias meminfo='free -m -l -t'     # display memory usage
       alias weather='curl wttr.in'      # display weather information


Functions
^^^^^^^^^

:term:`Functions <Function (Shell)>` are reusable blocks of code that
allow you to group commands and execute them by calling the function's
name.

.. code-block:: bash

   # Method 1: Using the function keyword
   function function_name {
       commands
   }

   # Method 2: Without the function keyword
   function_name() {
       commands
   }

.. dropdown:: Examples
    :class-container: sd-border-secondary
    :open:

    .. code-block:: bash

       function greeting {
           echo "Hello $1 $2"
       }

    Call the function: ``greeting John Doe``

    .. code-block:: bash

       print_arguments() {
           echo "Function or script name: $0"
           echo "Number of arguments: $#"
           echo "All arguments (\$*): $*"
           echo "Each argument separately:"
           for arg in "$@"; do
               echo "$arg"
           done
       }

    Call the function: ``print_arguments 1 2 hello world``


Applying Changes: the ``source`` Command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A configuration file such as ``.bashrc`` is only read **when a new shell
session starts**. This means that when you edit ``.bashrc`` (for example,
to add an alias or a function), your **current** terminal does not see the
change yet, because that terminal started before the edit was made.

The ``source`` command reads and executes a file in your **current**
shell session, applying its contents immediately:

.. code-block:: bash

   source ~/.bashrc

This is an alternative to **closing and reopening the terminal**: instead
of starting a fresh session to pick up the change, you re-read the
configuration file into the session you already have open.

.. dropdown:: Demonstration: an alias does not work until you source ``.bashrc``
    :class-container: sd-border-secondary
    :open:

    Add a new alias to the **end** of your ``.bashrc`` file. Here we
    append it directly from the terminal with ``>>``:

    .. code-block:: bash

       echo "alias hello='echo Hello, ENPM702!'" >> ~/.bashrc

    Now try to use the alias **in the same terminal**. It is not
    available yet, because your current session has not re-read
    ``.bashrc``:

    .. code-block:: console

       $ hello
       hello: command not found

    Source the configuration file to apply the change to your current
    session:

    .. code-block:: bash

       source ~/.bashrc

    Try the alias again. It now works:

    .. code-block:: console

       $ hello
       Hello, ENPM702!

.. important::

   Whenever you make a change to ``.bashrc`` (or ``.zshrc``), it does not
   take effect automatically in terminals that are already open. To apply
   the change, do **one** of the following:

   - Close and reopen your terminal, **or**
   - Open a new terminal, **or**
   - Run ``source ~/.bashrc`` (or ``source ~/.zshrc``) in the current
     terminal.
