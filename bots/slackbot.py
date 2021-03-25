from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

__all__ = [
    'SlackBot'
]


class SlackBot():
    """Bot that automatically sends messages over slack

    Parameters
    ----------
    config_file : file
        file with the access token for the slack workspace.
    """

    def __init__(self, config_file, **kwargs) -> None:
        self._token = self._get_token(config_file)
        self._client = self.connect()

    @property
    def client(self):
        """class : slack `WebClient` class"""
        return self._client

    def _get_token(self, config_file):
        """read the access token form a file.

        Returns
        -------
        str
            access token
        """
        with open(config_file, "r") as f:
            token = f.readline()
        return token

    def connect(self):
        """connect to the slack webclient.

        Returns
        -------
        class
            slack WebClient class
        """
        return WebClient(token=self._token)

    def fetch_channel_id(self, channel, output=False, verbose=False):
        """Retrive the channel ID from its name

        Parameters
        ----------
        channel : str
            slack channel where the message is sent to.
        output : bool, optional
            return the channel id, by default False
        verbose : bool, optional
            print output, by default False

        Returns
        -------
        str
            id of the channel
        """
        result = self.client.conversations_list()
        for chn in result["channels"]:
            if chn["name"] == channel:
                conversation_id = chn["id"]
                # Print result
                if verbose:
                    print(f"Found conversation ID: {conversation_id}")
                if output:
                    return conversation_id
                break

        return conversation_id

    def send_message(self, verbose=False, **kwargs):
        """Send a message to the channel

        Parameters
        ----------
        verbose : bool, optional
            print WebClient respons, by default False
        message : str, optional
            message to send over slack. If not provided a default message is sent.
        channel : str, optional.
            slack channel where the message is sent to. If not provided, the message
            is sent to `general`.
        Note
        ----
        The bot has to have been previously added to the channel
        """
        message = kwargs.get('message', "Ciao! Your results are ready! :)")
        channel = kwargs.get('channel', "general")
        channel_id = self.fetch_channel_id(channel)
        try:
            # Call the conversations.list method using the WebClient
            result = self._client.chat_postMessage(
                channel=channel_id,
                text=message
                # You could also use a blocks[] array to send richer content
            )
            # Print result, which includes information about the message (like TS)
            if verbose:
                print(result)

        except SlackApiError as e:
            print(f"Error: {e}")


# Debug
if __name__ == "__main__":

    bot = SlackBot(".tokens/token")
    bot.send_message(channel='topopt', message='test')
