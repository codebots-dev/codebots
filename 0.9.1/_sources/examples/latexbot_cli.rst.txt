********************************************************************************
use :code:`latexbot` from the command-line
********************************************************************************

:code:`latexbot` helps you to set-up your machine to work with latex. The first
step is to install everything you need. Instead of you spending time doing that
let it do it. Later we will see how to convert documents and connect your
overleaf project to your google drive.

Basics
======

For detailed information about the different comands, type :code:`latexbot --help`:

.. code-block:: bash
    :emphasize-lines: 1

    >>> latexbot --help

    Usage: latexbot [OPTIONS] COMMAND [ARGS]...

    bot to help with latex documents

    Options:
    --help  Show this message and exit.

    Commands:
    configure                 Download dependencies and set everything up.
    convert-overleaf-to-docx  Convert an overleaf project to a .docx file.
    convert-tex-to-docx       Convert the .tex files in a folder to .docx.


Install dependencies
====================

:code:`latexbot` needs to know what you need. If your are new to this, probably
you will need everything.

Run the following command:

.. code-block:: bash
    :emphasize-lines: 1

    >>> latexbot configure --git=True --pandoc=True --miktex=True


Convert a latex document to docx
================================

This command uses `pandoc` in the background. This software is prettty awesome,
but don't expect the conversion to be 100% perfect...

.. code-block:: bash
    :emphasize-lines: 1

    >>> latexbot convert-tex-to-docx --input "C:\temp\...\my_tex_file.tex" --output= "C:\temp\...\my_folder"

Convert an overleaf project to google doc
=========================================

Here we do even more: we get a project from overleaf and convert it directly to
google doc, were you can use all the fancy collaboration/commenting features.

.. note::

    remember to change the XXXXXXXXXX placeholder with a code of your oveleaf
    project.

.. code-block:: bash
    :emphasize-lines: 1

    >>> latexbot convert-overleaf-to-docx XXXXXXXXXX --upload=True
