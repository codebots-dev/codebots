===============
Getting Started
===============

:code:`codebots` is a family of very different :code:`bots` that can make very
different things.

A simple example of a typical applicaiton can be to have a :code:`bot` to send
you a message (over email, slack, telegram, ...) once your code triggers an action.

For example::

    import codebots
    from codebots.bots import <your-bot>

    bot = <your-bot>(...)

    YOUR SUPER AWESOME CODE

    bot.send_message("your code is working!")

or simply using a decorator::

    import codebots

    @codebots.monitor("<your-bot>")
    def your_awesome_function(args, kwargs)
        YOUR SUPER AWESOME CODE

But with :code:`codebots` you can also set-up ssh connections, run commands on a
host directly from your code, deploy your application on a server using git hooks,
and much more...!

For more datiled examples of applications, check the links below!


********************************************************************************
Examples
********************************************************************************

basics
======

The source of everything is.......the **commmand line** (yup!). Hence, the fist
step is to get familiar with :code:`codebots`'s CLI.

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :glob:

   examples/cli-codebots.rst
   examples/cli-sshbot.rst

However, shells and terminals are for nerds (yup!). Why don't you try to use
:code:`codebots` functionalities iniside a script?! check these out:

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :glob:

   examples/decorators.rst

notifications
=============

:code:`codebots` was born to get notifications once my simulations where complete.
Let's see how do it! Currently, you can get notified by email, slack or telegram
(I suggest telegram because it is super easy to setup).

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :glob:

   examples/slackbot.rst
   examples/telegrambot.rst
   examples/emailbot.rst

ssh and deploy
==============

Have you have ever tried to set-up an ssh connection wiht a linux server?! If yes.
you know the pain of generating keys, aliases, etc. Well, it is actually not that
hard, but at the beginning can be intimitading, so why not let :code:`codebots` do
it for us?

Even better, why not be one of those cool kids who do *DevOps* and set-up an automtic
deployment of our app?! You can do all this with :code:`codebots`...magic! :)

.. toctree::
   :maxdepth: 2
   :titlesonly:
   :glob:

   examples/sshbot.rst
   examples/deploybot.rst
