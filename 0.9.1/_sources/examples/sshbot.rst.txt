********************************************************************************
Create a bot to operate on a server using SSH
********************************************************************************

This example shows how to set-up a SSH bot to ease operations with a server.


Store your credentials
----------------------

:code:`codebots` uses `.json` files to manage credentials. You can create one
using the CLI (check the related example) or create a json file yourself in a
secret location using the template below:

.. literalinclude:: ./templates/ssh.json
  :language: JSON

.. note:: **about keypairing**

    You can choose to connect either using *username* and *password* (less secure)
    or using a SSH key. If you opt for the first approach, than leave blank the
    *pvtkey* field (`""`).


.. note:: **ssh keys generation**

    If you don't have a set of SSH key pairs or you don't know how to create one,
    ask the bot! ;)

    .. code-block:: bash

       >>> sshbot genkeys --ssh_folder "my_folder"

    After running the code there will be a set of private and public keys in the
    give folder that you can use to set-up your connection.


.. note:: **password key**

    the password key in the json file is either the password used to login to the
    server, or the password to decrypt the private SSH key (leave blank if not encrypted).


In action
---------

this is an example implementation:

.. literalinclude:: /../examples/sshbot.py
    :language: python
