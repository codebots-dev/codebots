********************************************************************************
Get notified on telegram
********************************************************************************

This example shows how to set-up a telegram bot. First, you need to setup things in telegram.

Create your own bot
-------------------

1. On Telegram, search :code:`@ BotFather` and send him a :code:`/start` message;
2. Type :code:`/newbot` and BotFather will guide you through the creation of a new bot;
3. Your bot is now ready: **annotate your API token**!
4. On Telegram, search your bot (by the username you just created), and send a :code:`/start` message

Set-up a :code:`TeleBot`
------------------------

Now that your bot is ready, you need to store your token on your machine and link
it to :code:`codebots`. Piece of cake... ;)

1. Open your Terminal and type (make sure to remove the `<` `>` when pasting your token:

.. code-block:: bash

    telebot set-token <paste-your-token-here>

2. DONE! if everything went smooth, you should be able to send messages over slack. Try it:

.. code-block:: bash

    telebot send "ciao mamma!"


In action
---------

This type of bot is most useful inside scripts (for example to send a message at
some function completion). This is an example implementation (but check the
:code:`decorator` section):

.. literalinclude:: /../examples/telegram_message.py
    :language: python
