"""Console script for codebots.

You can get detaled information about each of the bots with the :code:`--help` option.

.. code-block:: bash

    codebots    --help
    emailbot    --help
    telebot     --help
    slackbot    --help
    sshbot      --help
    deploybot   --help


"""
import sys
import os
from pathlib import Path
import click
import codebots
from codebots.bots import SlackBot
from codebots.bots import TeleBot
from codebots.bots import EmailBot
from codebots.bots import sshBot
from codebots.bots.deploybot import DeployBot
from codebots.utilities.ssh import gen_keypair, add_pubkey_to_server
from codebots.utilities.tokens import add_token, set_token_dir, reset_token_dir
from codebots.utilities.deploy import configure_local, configure_server


### -------------------------------- MAIN ----------------------------------###
@click.group()
def main():
    """base bot to setup the common settings for all the other bots.

    Run `codebots ono-o-one` for more info.
    """
    pass


@main.command()
def one_o_one():
    """Basic explanation of command line usage."""

    click.echo("\nHey there! this is codebots, a family of bots here to help you!\n\n"
               "To use codebots directly from the command line, type the name of your bot followed by the action.\n"
               "For example, this command sends a message through slack:\n\n"
               "    slackbot --channel=random \"Hello from your slacbot!\"\n")


@main.command()
def get_tokens_path():
    """Get the path to the tokens folder.\n

    Return\n
    ------\n
    str\n
        path to the folder containing the tokens or passwords for the codebots.\n
    """
    out = codebots.TOKENS
    click.echo(out)


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

### -------------------------------- SLACK ----------------------------------###


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
@click.option('--channel', default='general', help='the channel you want to send the message to')
@click.argument('message', default='Ciao Mamma!')
def send(message, channel):
    """Send a message using slack.\n
    message : txt\n
        the message you want to send to yo.ur slack channel, by default `Ciao Mamma!`
    """
    bot = SlackBot()
    bot.send_message(channel, message)

### ----------------------------- TELEGRAM ----------------------------------###


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

### -------------------------------- EMAIL ----------------------------------###


@click.group()
def emailbot():
    """bot to send emails from the command line"""
    pass


@emailbot.command()
@click.argument('receiver', default='mamma@email.com')
@click.argument('subject', default='Ciao')
@click.argument('body', default='Ciao Mamma!')
# @click.option('--attach',  type='path', help='path to any file you want to attach')
def send(receiver, subject, body):
    """Send an email to an email address.\n

        Parameters\n
        ----------\n
        receiver : str\n
            email address of the receiver\n
        subject : str\n
            subject of the email\n
        body : str\n
            body text of the email\n
        attachment : str, optional\n
            path to the file to attach, by default None\
    """

    # sender = Sender.form_file(".tokens/email")
    receiver = "francesco.ranaudo@gmail.com"
    subject = "message from bot"
    body = "This message was sent by a bot"
    attach = "document.pdf"

    bot = EmailBot()
    bot.send_email(receiver, subject, body)


@emailbot.command()
@click.argument('username')
@click.argument('password')
def set_token(username, password):
    """create the token file with the credentials.\n

    Parameters\n
    ----------\n
    token : str\n
        token of the telegram bot.\n
    chatid : str\n
        chatID of the chat with the bot.\n
    """
    out = add_token("email", username=username, password=password)
    click.echo(out)


### --------------------------------- SSH -----------------------------------###
@click.group()
def sshbot():
    """bot to interact with telegram"""
    pass


@sshbot.command()
@click.argument('hostname')
@click.argument('username')
@click.option('--password', default='', help='password to access the host or to decrypt the private key')
@click.option('--pvtkey', default='', help='path to the private key')
def set_token(hostname, username, password, pvtkey):
    """create the token file with the credentials.\n

    Parameters\n
    ----------\n
    hostname : str\n
        ip address of the server.\n
    username : str\n
        username on the server.\n
    password : str\n
        password on the server, by default empty.\n
    pvtkey : str\n
        path to the private RSA key file, by default empty.\n
    """
    out = add_token("ssh", hostname=hostname, username=username, password=password, pvtkey=pvtkey)
    click.echo(out)


@sshbot.command()
@click.option('--ssh_folder', default=None, help='path where the key pair will be saved, by default None (the `USER/.ssh` folder will be used)')
@click.option('--password', default=None, help='encrypt the private key with a password')
def genkeys(ssh_folder):
    """Create a set of public and private keys and save them in the given folder.
    """
    out = gen_keypair(ssh_folder)
    click.echo(out)


@sshbot.command()
@click.argument('hostname')
@click.argument('username')
@click.argument('password')
@click.option('--ssh_folder', help='path where the key pair will be saved')
def link_keys(hostname, username, password, ssh_folder):
    """Adds the public key to the server's list.\n

    Parameters\n
    ----------\n
    hostname : str\n
        ip address of the server.\n
    username : str\n
        username on the server.\n
    password : str\n
        password on the server, by default empty.\n
    """
    bot = sshBot(config_file=None, hostname=hostname, username=username, password=password, pvtkey="")
    out = add_pubkey_to_server(bot, ssh_folder)
    click.echo(out)
    out = add_token("ssh", hostname=hostname, username=username, password="", pvtkey=os.path.join(ssh_folder, 'id_rsa'))
    click.echo(out)


### ------------------------------- DEPLOY ----------------------------------###
@click.group()
def deploybot():
    """bot to deploy projects to a server"""
    pass


@deploybot.command()
@click.argument('project')
@click.argument('address')
@click.argument('local')
@click.argument('server')
@click.option('--sshbot', default=None, help='instance of an `sshBot` with access to the server.')
def configure(project, address, local, server, sshbot):
    """Configure a local repository to sync with a server.\n

    Parameters\n
    ----------\n
    local : str\n
        path to the local clone of the repository\n
    server : str\n
        path to the server bare repository. If no repository is present\n
        at the given location a bare new one is created.\n
    """
    out = add_token(bot=project, server_address=address, local_repo_path=local, server_repo_path=server)
    click.echo(out)
    bot = DeployBot(project)
    out = configure_local(bot.local_repo, bot.server_complete_path)
    click.echo(out)
    out = configure_server(bot.server_repo_path, sshbot)
    click.echo(out)


### -------------------------------- DEBUG ----------------------------------###
if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
