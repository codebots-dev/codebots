=====
Usage
=====

A simple example of typical applicaiton can be to have a `bot` to send you a
message (over email, slack, telegram, ...) once your code triggers an action.

For example::

    import codebots
    from codebots.bots import <your-bot>

    bot = <your-bot>(...)

    YOUR SUPER AWESOME CODE

    bot.send_message("your code is working!")


For more datiled examples of applicaitons, check the list below!


********************************************************************************
Examples
********************************************************************************

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :glob:

   examples/slackbot.rst
   examples/emailbot.rst
   examples/telegrambot.rst
   examples/sshbot.rst
