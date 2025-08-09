from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os


from ._bot import BaseBot

__all__ = [
    'SlackBot'
]


class SlackBot(BaseBot):
    """Bot that automatically sends messages over slack

    Parameters
    ----------
    config_file : file
        file with the access token for the slack workspace.
    """

    def __init__(self, config_file=None) -> None:
        # Use BaseBot for modern token handling
        if not config_file:
            from .. import TOKENS
            config_file = os.path.join(TOKENS, "slack.json")
        super().__init__(config_file)
        self._client = self.connect()

    @property
    def client(self):
        """class : slack `WebClient` class"""
        return self._client

    def connect(self):
        """connect to the slack webclient."""
        token = getattr(self, 'bot_token', None)
        if not token:
            raise ValueError("Slack bot token not found. Set SLACKBOT_BOT_TOKEN env var or provide a token file.")
        return WebClient(token=token)

    def _fetch_channel_id(self, channel, output=False, verbose=False):
        """Retrive the channel ID from its name"""
        result = self.client.conversations_list()
        channels = result.get("channels", [])
        conversation_id = None
        for chn in channels:
            if chn["name"] == channel:
                conversation_id = chn["id"]
                if verbose:
                    print(f"Found conversation ID: {conversation_id}")
                if output:
                    return conversation_id
                break
        if conversation_id is None:
            raise ValueError(f"Channel '{channel}' not found.")
        return conversation_id

    def send_message(self, verbose=False, **kwargs):
        """Send a message to a channel.

        Parameters
        ----------
        message : str, optional
            message to send over slack. If not provided a default message is sent.
        channel : str, optional.
            slack channel where the message is sent to. If not provided, the message
            is sent to `general`.
        verbose : bool, optional
            print WebClient respons, by default False

        Notes
        -----
        Make sure that the bot has been previously added the bot to the channel.
        """
        message = kwargs.get('message', "Ciao! Your results are ready! :)")
        channel = kwargs.get('channel', "general")
        channel_id = self._fetch_channel_id(channel)
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

    bot = SlackBot()
    bot.send_message(channel='general', message='test')
