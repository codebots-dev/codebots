import json


class BaseBot():
    """BaseBot class for the other bots.
    """

    def __init__(self, config_file) -> None:
        self._credentials = self._get_token(config_file)
        for k, v in self._credentials.items():
            self.__setattr__(k, v)

    def _get_token(self, config_file):
        """read the access token form a json file.

        Parameters
        ----------
        config_file : json
            json file containing the bot_token and the bot_chatID

        Returns
        -------
        dict
            credential info
        """
        try:
            with open(config_file, "r") as f:
                token = json.load(f)
            return token
        except FileNotFoundError:
            raise FileNotFoundError("there is no token for this bot in the tokens folder.\n\n\
please provide one by running in the command line the following command:\n\
`{} set-token` and provide the required information\n\n\
or set a new tokens folder using:\n\
`codebots set-tokens-path \"path-to-tokens-folder\"`\n".format(self.__name__))
