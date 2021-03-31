********************************************************************************
Get notified via email
********************************************************************************

This example shows how to set-up an emailbot.

First, you need to setup an email account.

.. warning:: Create a brand new account!

    It is STRONGLY advised to create a new email account (must be `GMAIL`)!!
    You will have to save the login credentials on your system, which is a huge
    security issue!


Create a secret file (no extension needed) somewhere hidden on your system with
the username in the first line and the password in the line below. it should look
like this:

.. code-block::

    username@gmail.com
    PaSsWoRd!

Here an example on how to receive an email from the bot:

.. literalinclude:: /../examples/email_message.py
    :language: python
