import json
import os
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


def add_token(bot, **kwargs):
    """Create a json file with the credential settings needed for the bot to
    operate.

    Parameters
    ----------
    bot : str
        name of the bot to configure.

    Examples
    --------
    >>> add_token(telegram, bot_token="some_token", bot_chatID=12345)
    """

    config_dict = {k: v for k, v in kwargs.items()}
    config_file = os.path.join(TOKENS, "{}.json".format(bot))

    try:
        with open(config_file, "w") as f:
            json.dump(config_dict, f)
            return "tokens file for {} updated!".format(bot)
    except Exception:
        return "something went wrong!"
