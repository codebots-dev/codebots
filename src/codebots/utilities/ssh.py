import paramiko
import os
from pathlib import Path


def gen_keypair(ssh_folder=None, password=None):
    """Create a set of public and private keys and save them in the given
    folder.

    Parameters
    ----------
    ssh_folder : str
        folder where the keys are saved.
    password : str
        encrypt the private key with a password.
    """

    if not ssh_folder:
        ssh_folder = os.path.join(Path.home(), '.ssh')
    key = paramiko.RSAKey.generate(4096)
    with open(os.path.join(ssh_folder, "id_rsa.pub"), "w") as key_file:
        key_file.write("ssh-rsa {}".format(key.get_base64()))
    with open(os.path.join(ssh_folder, "id_rsa"), "w") as key_file:
        key.write_private_key(key_file, password)

    return "Key pair successfully generated in {}".format(ssh_folder)


def add_pubkey_to_server(bot, ssh_folder, os_type='linux'):
    """Adds the public key to the server's list.

    Parameters
    ----------
    bot : obj
        `sshBot` object to access the server.
    ssh_folder : str
        folder where the keys are stored.

    Warnings
    --------
    This works only on linux servers.
    """
    with open(os.path.join(ssh_folder, 'id_rsa.pub'), "r") as pubkey_file:
        pubkey = pubkey_file.readline()
    bot.execute_cmds(commands=['(umask 077 && test -d ~/.ssh || mkdir ~/.ssh)',
                               '(umask 077 && touch ~/.ssh/authorized_keys)',
                               'echo {} >>  ~/.ssh/authorized_keys'.format(pubkey)],
                     close_connection=False,
                     verbose=False)
    return ("public key successfully added. Try to run `ssh hostname`")
