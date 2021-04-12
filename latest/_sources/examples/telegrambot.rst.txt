********************************************************************************
Get notified on telegram
********************************************************************************

This example shows how to set-up a telegram bot. First, you need to setup things in telegram.

Create your own bot
-------------------

1. On Telegram, search `@ BotFather`, send him a “/start” message;
2. Using the “/newbot” message, BotFather will guide you through the creation of a new bot;
3. Your bot is now ready: annotate your API token!


Getting your ChatID
--------------------

1. On Telegram, search your bot (by the username you just created), and send a “/start” message
2. Open a new tab with your browser, enter `https://api.telegram.org/bot<yourtoken>/getUpdates` , replace `<yourtoken>` with your API token, press enter and you should see something like this:

.. code-block:: JSON

    {
    "ok": true,
    "result": [
        {
        "update_id": 4871110,
        "message": {
            "message_id": 2,
            "from": {
                "id": 171111114,
                "is_bot": false,
                "first_name": "frankie",
                "language_code": "en"
            },
            "chat": {
                "id": 171111114,
                "first_name": "frankie",
                "type": "private"
            },
            "date": 1618152626,
            "text": "36380"
        }
        }
    ]
    }

3. Look for `id` under `chat` and annotate it.


Store your credentials
----------------------

Almost there! :) Now that you have what you need, create a json file in a secret location and paste the `bot_token` and the `chatID` in it
using the template below:

.. literalinclude:: ./templates/telegram.json
  :language: JSON


In action
---------

this is an example implementation:

.. literalinclude:: /../examples/telegram_message.py
    :language: python
