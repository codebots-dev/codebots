import paramiko
import os
import json

import sys
import subprocess
import argparse

__all__ = ["sshBot"]


class sshBot():
    """sshBot to help with ssh connections to a server.

    Parameters
    ----------
    hostname : str
        ip address of the server
    username : str
        username on the server
    password : str
        password on the server
    pvtkey : str
        path to the private RSA key file
    """

    def __init__(self, hostname=None, username=None, password=None, pvtkey=None) -> None:

        self.hostname = hostname
        self.username = username
        self.password = password
        self.pvtkey = pvtkey
        self.ssh_client = None
        self.sftp_client = None

    @classmethod
    def from_credentials_file(cls, json_file):
        """get credentials from json file

        Parameters
        ----------
        json_file : str
            path to the json file with the credentials for the server.
            it should have the following structure:

            .. code-block:: json
                {
                    "hostname" : "_______",
                    "username" : "_______",
                    "password" : "_______",
                    "pvtkey"   : "_______"
                }

        Returns
        -------
        cls
            sshBot
        """
        with open(json_file, 'r') as f:
            credentials = json.load(f)
        return cls(**credentials)

    def gen_keypair(self, ssh_folder="/home/fr/.ssh"):
        """create a set of public and private keys and save them in the given
        folder.

        Parameters
        ----------
        ssh_folder : str, optional
            folder where the keys are saved
        """
        key = paramiko.RSAKey.generate(4096)
        with open(os.path.join(ssh_folder, "pubkey"), "w") as key_file:
            key_file.write(key.get_base64())
        with open(os.path.join(ssh_folder, "pvtkey"), "w") as key_file:
            key_file.write(key.write_private_key(sys.stdout))

    def connect_ssh_client(self):
        """establish the ssh connection

        Returns
        -------
        obj
            ssh_client obj
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.pvtkey:
            k = paramiko.RSAKey.from_private_key_file(self.pvtkey, password=self.password)
        ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password, pkey=k)
        print("connected")
        return ssh_client

    def exectute_cmds(self, commands):
        """execute general command on the server side

        Parameters
        ----------
        commands : list of str
            list of commands (str) to execute on the server.

        Returns
        -------
        None
        """
        if not self.ssh_client:
            self.ssh_client = self.connect_ssh_client()

        # commands = [ "/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh" ]
        for command in commands:
            print("Executing {}".format(command))
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            print(stdout.read())
            print("Errors")
            print(stderr.read())
        self.ssh_client.close()

    def connect_sftp_client(self):
        """connect to the server through SFPT on port 22.

        Return
        ------
        obj
            paramiko sfpt client object
        """
        transport = paramiko.Transport((self.hostname, 22))
        if self.pvtkey:
            k = paramiko.RSAKey.from_private_key_file(self.pvtkey, password=self.password)
        transport.connect(username=self.username, password=self.password, pkey=k)
        return paramiko.SFTPClient.from_transport(transport)

    def get_folder_from_server(self, path, dest, recursive=True):
        """Retrieve the content of a folder from the server.

        Parameters
        ----------
        sftp_client : obj
            paramiko sftp client object
        path : str
            path to the folder on the server
        dest : str
            path to the folder on the client (local)
        recursive : bool (optional)
            if true get subfolders content, by default True

        Return
        ------
        None

        Warning
        -------
        If in any folder there are files without extensions, the code will fail!
        """

        # connect to the server through SFPT
        sftp_client = self.connect_sftp_client()

        for item in sftp_client.listdir(path):
            remotefile = os.path.join(path, str(item))
            if not os.path.isdir(dest):
                os.mkdir(dest)
            localfilepath = os.path.join(dest, str(item))
            # check if it is a folder (note file w/o ext will thorw an exception!)
            if '.' in item:
                sftp_client.get(remotefile, localfilepath)
            else:
                if recursive:
                    self.get_folder_from_server(sftp_client, remotefile, localfilepath)

        # close the connection
        sftp_client.close()


if __name__ == '__main__':

    bot = sshBot.from_credentials_file(".tokens/home.json")

    # bot.connect_ssh_client()

    # # get folder content
    # remotefolder =  '/home/franaudo/Documents/code/'
    # localfolderpath = '/home/fr/Desktop/'
    # bot.get_folder_from_server(remotefolder, localfolderpath)

    bot.exectute_cmds(commands=['ls'])
