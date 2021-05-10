import json
import os
import requests
from .. import SETTINGS, TOKENS


def set_token_dir(path):
    """Set the location where codebots looks for the bots credentials.

    Parameters
    ----------
    path : str
        path to the folder where the json files with credentials are stored.

    Returns
    -------
    str
        message
    """
    path_dic = {}
    try:
        with open(SETTINGS, 'w') as f:
            path_dic["tokens_path"] = path
            json.dump(path_dic, f)
        return "tokens path updated!"
    except Exception:
        return "something went wrong!"


def reset_token_dir():
    """Reset the credentials folder to default.

    Returns
    -------
    str
        message
    """
    set_token_dir("None")
    return "tokens path resetted!"


def add_token(alias, **kwargs):
    """Create a json file with the credential settings needed for the bot to
    operate.

    Parameters
    ----------
    alias : str
        name of the bot/project/server to configure.

    Examples
    --------
    >>> add_token(telegram, bot_token="some_token", bot_chatID=12345)
    """

    config_dict = {k: v for k, v in kwargs.items()}
    config_file = os.path.join(TOKENS, "{}.json".format(alias))
    msg = "tokens file for {} {}!".format(alias, 'created' if not os.path.isfile(config_file) else 'updated')

    try:
        with open(config_file, "w") as f:
            json.dump(config_dict, f)
            return msg
    except Exception:
        return "something went wrong saving the file!"


def get_telegram_chatid(token):
    response = requests.get("https://api.telegram.org/bot{}/getUpdates".format(token))
    return response.json()['result'][0]['message']['chat']['id']
