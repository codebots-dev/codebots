********************************************************************************
Get notified via email
********************************************************************************

This example shows how to set-up an emailbot.

First, you need to setup an email account.

.. warning:: Create a brand new account!

    It is STRONGLY advised to create a new email account (must be `GMAIL`)!!
    You will have to save the login credentials on your system, which is a huge
    security issue!

.. note:: Allow 'less secure app access'

    in order for the bot to be able to send messages, you have to turn on the
    **less secure app acces** option in the gmail security settings.

Now you have to register your credentials. You can simply do it from the command
line (obviously change the placeholders with your credentials):

.. code-block:: bash

    $ emailbot set-token "username@gmail.com" "PaSsWoRd!"


Alternatively, manually create a secret json file somewhere hidden on your
system with the username and the password. Then run the following command:

.. code-block:: bash

    $ codebots set-tokens-path "path=to-the-folder-where-the-json-file-is-saved"


The json file should look like this:

.. code-block:: json

    {
        "username": "username@gmail.com"
        "password": "PaSsWoRd!"
    }



Here an example on how to receive an email from the bot:

.. literalinclude:: /../examples/email_message.py
    :language: python
