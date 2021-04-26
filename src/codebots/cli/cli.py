"""Console script for codebots."""
import sys
import click
from codebots.bots import SlackBot
from codebots.bots import TeleBot
from codebots.utilities.tokens import add_token, set_token_dir, reset_token_dir


@click.group()
def main():
    pass


@main.command()
def one_o_one():
    """Basic explanation of command line usage."""

    click.echo("\nHey there! this is codebots, a family of bots here to help you!\n\n"
               "To use codebots directly from the command line, type the name of your bot followed by the action.\n"
               "For example, this command sends a message through slack:\n\n"
               "    slackbot --channel=random \"Hello from your slacbot!\"\n")


@main.command()
@click.argument('path')
def set_tokens_path(path):
    """Set the path to the tokens folder.\n

    Parameters\n
    ----------\n
    path : str\n
        path to the folder containing the tokens or passwords for the codebots.\n
    """
    out = set_token_dir(path)
    click.echo(out)


@main.command()
def reset_tokens_path():
    """Reset the tokens path to the default (~/.tokens)."""
    out = reset_token_dir()
    click.echo(out)


@click.group()
def slackbot():
    """bot to interact with slack"""
    pass


@slackbot.command()
@click.argument('token')
def set_token(token):
    """create the token file with the credentials.\n

    Parameters\n
    ----------\n
    token : str\n
        token of the telegram bot.\n
    chatid : str\n
        chatID of the chat with the bot.\n
    """
    out = add_token("slack", bot_token=token)
    click.echo(out)


@slackbot.command()
@click.option('--channel', default='general', help='')
@click.argument('message', default='Ciao Mamma!')
def send(message, channel):
    """Send a message using slack.\n
    message : txt\n
        the message you want to send to yo.ur slack channel, by default `Ciao Mamma!`
    """
    bot = SlackBot()
    bot.send_message(channel, message)


@click.group()
def telebot():
    """bot to interact with telegram"""
    pass


@telebot.command()
@click.argument('message', default='Ciao Mamma!')
def send(message):
    """Send a message using slack.\n
    message : txt\n
        the message you want to send to yo.ur slack channel, by default `Ciao Mamma!`
    """

    bot = TeleBot()
    bot.send_message(message)


@telebot.command()
@click.argument('token')
@click.argument('chatid')
def set_token(token, chatid):
    """create the token file with the credentials.\n

    Parameters\n
    ----------\n
    token : str\n
        token of the telegram bot.\n
    chatid : str\n
        chatID of the chat with the bot.\n
    """
    out = add_token("telegram", bot_token=token, bot_chatID=chatid)
    click.echo(out)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
