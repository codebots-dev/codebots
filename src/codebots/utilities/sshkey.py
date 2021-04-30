import paramiko
import os
import sys
from pathlib import Path
# from io import StringIO
import subprocess


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
    if not ssh_folder:
        ssh_folder = os.path.join(str(Path.home()), '.ssh')
    with open(os.path.join(ssh_folder, 'id_rsa.pub'), "r") as pubkey_file:
        pubkey = pubkey_file.readline()
    bot.execute_cmds(commands=['(umask 077 && test -d ~/.ssh || mkdir ~/.ssh)',
                               '(umask 077 && touch ~/.ssh/authorized_keys)',
                               'echo {} >>  ~/.ssh/authorized_keys'.format(pubkey)],
                     close_connection=False,
                     verbose=False)
    return ("public key successfully added. Try to run `ssh hostname`")

    # def connect_with_pvtkey():
    #     k = paramiko.RSAKey.from_private_key_file("/home/fr/.ssh/id_rsa", password="Sxcdews23")
    #     c = paramiko.SSHClient()
    #     c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     print("connecting")
    #     c.connect(hostname="192.168.0.199", username="franaudo", pkey=k)
    #     print("connected")
    #     # commands = [ "/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh" ]
    #     # for command in commands:
    #     # 	print "Executing {}".format( command )
    #     # 	stdin , stdout, stderr = c.exec_command(command)
    #     # 	print stdout.read()
    #     # 	print( "Errors")
    #     # 	print stderr.read()
    #     # c.close()

    # # def ssh_key_gen(length=2048, type='rsa', password=None, username='jumpserver', hostname=None):
    # #     """Generate user ssh private and public key

    # #     Use paramiko RSAKey generate it.
    # #     :return private key str and public key str
    # #     """

    # #     if hostname is None:
    # #         hostname = os.uname()[1]

    # #     f = StringIO()
    # #     try:
    # #         if type == 'rsa':
    # #             private_key_obj = paramiko.RSAKey.generate(length)
    # #         elif type == 'dsa':
    # #             private_key_obj = paramiko.DSSKey.generate(length)
    # #         else:
    # #             raise IOError('SSH private key must be `rsa` or `dsa`')
    # #         private_key_obj.write_private_key(f, password=password)
    # #         private_key = f.getvalue()
    # #         public_key = ssh_pubkey_gen(private_key_obj, username=username, hostname=hostname)
    # #         return private_key, public_key
    # #     except IOError:
    # #         raise IOError('These is error when generate ssh key.')

    # def create_keypair():

    #     key = paramiko.RSAKey.generate(4096)
    #     print(key.get_base64())  # print public key
    #     key.write_private_key(sys.stdout)  # print private key

    #     with open("/home/fr/.ssh/pubkey", "w") as key_file:
    #         key_file.write(key.get_base64())

    #     key.write_private_key("/home/fr/.ssh/pvtkey")


if __name__ == "__main__":
    from codebots.bots import sshBot
    bot = sshBot(config_file=None, hostname="192.168.0.199", username="franaudo", password="Sxcdews23", pvtkey="")
    add_pubkey_to_server(bot, path_local="C:/Users/franaudo/.ssh/pubkey")
