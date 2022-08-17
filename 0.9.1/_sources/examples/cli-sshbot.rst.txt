********************************************************************************
set-up :code:`sshbot`
********************************************************************************

:code:`sshbot` helps you to set-up a connection with a (linux) server and run
commands on it directly from your app. However, we need to first store the
credentials that :code:`sshbot` will use for the connection. This section explains
how.

Basics
======

For detailed information about the different comands, type :code:`sshbot --help`:

.. code-block:: bash
    :emphasize-lines: 1

    >>> sshbot --help

    Usage: sshbot [OPTIONS] COMMAND [ARGS]...

    bot to remotely operate on a (linux) server

    Options:
    --help  Show this message and exit.

    Commands:
    genkeys    Create a set of public and private keys and save them in the...
    link-keys  Adds the public key to the server's list.
    set-token  create the token file with the credentials.


Setting the credentials
=======================

:code:`codebots` reads the credential information from a `.json` file stored on
your local machine. It can either connect to the server using a password (not
super safe) or using a ssh-key pair (better!).

Here it is explained how to do both.

Using a password
~~~~~~~~~~~~~~~~

Run the following command:

.. code-block:: bash
    :emphasize-lines: 1

    >>> sshbot set-token myhost myusername --password mySECRETEpassword

Using ssh keys
~~~~~~~~~~~~~~

If you already have a pair of private and public ssh keys, you can skip the first
part.

Running the following command:

.. code-block:: bash
    :emphasize-lines: 1

    >>> sshbot genkeys

    Key pair successfully generated in ~\username\.ssh

will generate in the user `.ssh` folder a pair of ssh keys.

.. note::

    if you want to use already existings keys, make sure that they have the
    standard names **id_rsa** and **id_rsa.pub**. They can be saved in any location
    on your machine, but if it is not the standard `ssh` folder, you need to pass
    the optional argument :code:`--ssh_folder` to the command below.

You now need to link the two keys (basically, add the public key to the list of
keys acceppted by the server). This can be automatically done with:

.. code-block:: bash
    :emphasize-lines: 1

    >>> sshbot link-keys myhost myusername mySECRETEpassword

    connected

    public key successfully added. Try to run `ssh myusername@nefcmyhostloud`

    tokens file for myusername@nefcmyhostloud created!

To check that everything is working, try to connect to the server:

.. code-block:: bash

    >>> ssh myusername@myhost


Using the credentials
=====================

Both procedures will generate a `myusername@myhost.json` file in the default
location with the given information. You can use the `alias` :code:`myusername@myhost`
when you create an :code:`sshBot` (check the other examples).

.. code-block:: python

    bot = sshBot('myusername@myhost')
