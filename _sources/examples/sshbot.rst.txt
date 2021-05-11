********************************************************************************
Create a bot to deploy your application to a server using git
********************************************************************************

This example shows how to set-up a bot to ease deploy your application on the
server. It can also be configured to automatically create git hooks for
continuous development


Configuration
-------------
First, you need to configure your local and server sides. These are  one-time-only
operations to do every time you start a new project. Once things are configured,
then you will be able to deploy with just one line of code ;)



You are also goind to need to access the server through SSH: fortunately we have
a bot for it (!) but you can also set things manually if you know what to do.


In action
---------

this is an example implementation:

.. literalinclude:: /../examples/sshbot.py
    :language: python
