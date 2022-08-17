********************************************************************************
Use DriveBot to upload a document to your Google Drive
********************************************************************************

This example shows how to instantiate a `drivebot` authenticating through a web
interface and upload a simple document.


Configuration
-------------
The first time you use a `DriveBot` you probably want to use a web interface to
authenticate. If you save your credentials (this will be saved in the `.tokens`
folder) you don't have to do it again: just set `authentication='local` when you
instantiate your bot.

In action
---------

this is an example implementation:

.. literalinclude:: /../examples/drivebot.py
    :language: python
