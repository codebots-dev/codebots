.. highlight:: shell

============
Installation
============


Stable release (WIP)
--------------------


To install codebots, run this command in your terminal:

.. code-block:: console

    $ pip install codebots

This is the preferred method to install codebots, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


.. warning::

    sometimes (not sure why yet) the requirements are not installed with the package.
    this is simply fixe by running 'pip install slack_sdk click yagmail' in the same
    environment you have installed `codebots`



From sources
------------

The sources for codebots can be downloaded from the `Github repo`_.

The easiest way is to install the package directly from GitHub. Execute the following
in your terminal:

.. code-block:: console

    pip install git+git://github.com/franaudo/codebots

Alternatively, you can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/franaudo/codebots

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/franaudo/codebots/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/franaudo/codebots
.. _tarball: https://github.com/franaudo/codebots/tarball/master
