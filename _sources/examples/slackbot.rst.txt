********************************************************************************
Get notified on slack
********************************************************************************

This example shows how to set-up a slackbot.

First, you need to setup things in slack. Follow this guide to create a custom
Slack bot to deploy to your workspace:

.. note:: Create a new workspace!

    It is advised to create a new workspace (for free) in Slack before starting
    spamming people...! ;)


You can go here to create the app: https://api.slack.com/apps?new_granular_bot_app=1

Give it a name ('codebot' for example) and select the workspace where it will be deployied.

Once you have created the app, you need to grant it acces to writing and reading
in your workspace. Go to `OAuth $ Permissions` and in `Scopes` and add:

- `channels:read`
- `chat:write`

Install the app in your workspace and copy the `OAuth Token`

Finally, create a secret file (no extension needed) somewhere hidden on your
system and paste the token in it. You will reference this file when you create
your `SlackBot`. In the example below it is saved in in the folder `.tokens` with
the name `slack`


.. literalinclude:: /../examples/slack_message.py
    :language: python
