********************************************************************************
Use :code:`codebots` from the command line
********************************************************************************

:code:`codebots` ships with a command line interface. This can (and should)be
used for setting up things or to directly use the bots from the shell.

For detailed information about the different comands, type the name of the bot
followed by :code:`--help`, like:

.. code-block:: bash
    :emphasize-lines: 1

    >>> codebots --help

    Usage: codebots [OPTIONS] COMMAND [ARGS]...

    base bot to setup the common settings for all the other bots.

    Run `codebots ono-o-one` for more info.

    Options:
    --help  Show this message and exit.

    Commands:
    get-tokens-path    Get the path to the tokens folder.
    one-o-one          Basic explanation of command line usage.
    reset-tokens-path  Reset the tokens path to the default (~/.tokens).
    set-tokens-path    Set the path to the tokens folder.


Setting things up
=================

The first thing to do is to set-up the `tokens` folder: :code:`codebots` uses
json files to store the credentials information for the different platforms. It
is important that you store this data in a safe place (!) and tell :code:`codebots`
where. By default, :code:`codebots` will create a `.token` folder in the user's
directory, but you can override this with:

.. code-block:: bash

    >>> codebots set-token-path "path-to-new-tokens-folder"

