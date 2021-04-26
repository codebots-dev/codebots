import json
import os
from codebots import SETTINGS, TOKENS


def set_token_dir(path):
    path_dic = {}
    try:
        with open(SETTINGS, 'w') as f:
            path_dic["tokens_path"] = path
            json.dump(path_dic, f)
        return "tokens path updated!"
    except:
        return "something went wrong!"


def reset_token_dir():
    set_token_dir("None")
    return "tokens path resetted!"


def add_token(bot, **kwargs):
    """create a json file with the credential settings needed for the bot to
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
    except:
        return "something went wrong!"
