import paramiko
import os
import socket


from ._bot import BaseBot

__all__ = [
    'sshBot'
]


class sshBot(BaseBot):
    """sshBot to help with ssh connections to a server.

    Parameters
    ----------
    hostname : str
        ip address of the server, by default None.
    username : str
        username on the server, by default None.
    password : str
        password on the server, by default None.
    pvtkey : str
        path to the private RSA key file, by default None.

    Attributes
    ----------
    hostname : str
        ip address of the server, by default None.
    username : str
        username on the server, by default None.
    password : str
        password on the server, by default None.
    pvtkey : str
        path to the private RSA key file, by default None.
    ssh_client : obj
        paramiko `SSHClient` object, if a connection is active, otherwise None.
    sftp_client : obj
        paramiko `SFTPClient` object, if a connection is active, otherwise None.
    """

    def __init__(self, config_file='default', **kwargs) -> None:

        self.__name__ = "sshbot"
        if not config_file:
            self._credentials = kwargs
            for k, v in self._credentials.items():
                self.__setattr__(k, v)
        elif config_file == 'default':
            from .. import TOKENS
            config_file = os.path .join(TOKENS, "ssh.json")
            super().__init__(config_file)
        else:
            super().__init__(config_file)

        self.host_address = self.hostname if '.' in self.hostname else socket.gethostbyname(self.hostname)
        self._ssh_client = None
        self._sftp_client = None

    # @classmethod
    # def from_credentials_file(cls, json_file):
    #     """Get credentials from json file

    #     Parameters
    #     ----------
    #     json_file : str
    #         path to the json file with the credentials for the server.
    #         it should have the following structure:

    #         .. code-block:: json

    #             {
    #                 "hostname" : "_______",
    #                 "username" : "_______",
    #                 "password" : "_______",
    #                 "pvtkey"   : "_______"
    #             }

    #     Returns
    #     -------
    #     cls
    #         sshBot
    #     """
    #     with open(json_file, 'r') as f:
    #         credentials = json.load(f)
    #     return cls(**credentials)

    @property
    def ssh_client(self):
        return self._ssh_client

    @property
    def sfpt_client(self):
        return self._sfpt_client

    def connect_ssh_client(self):
        """Establish the ssh connection

        Returns
        -------
        obj
            ssh_client obj
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file(self.pvtkey, password=self.password) if self.pvtkey else None
        ssh_client.connect(hostname=self.host_address, username=self.username, password=self.password, pkey=k)
        print("\nconnected\n")
        return ssh_client

    def execute_cmds(self, commands, close_connection=True, verbose=True):
        """Execute general command on the server side

        Parameters
        ----------
        commands : list of str
            list of commands (str) to execute on the server.
        close_connection : bool (optional)
            if true close the ssh connection, by default True. Leave the connection
            open if you plan to run several commands.

        Returns
        -------
        None
        """
        if not self._ssh_client:
            self._ssh_client = self.connect_ssh_client()

        out_dict = {"stdout": [], "stderr": []}

        for command in commands:
            if verbose:
                print("Executing {}:\n".format(command))
            stdin, stdout, stderr = self._ssh_client.exec_command(command)
            out_dict["stdout"].append(stdout.read().rstrip().decode("utf-8"))
            out_dict["stderr"].append(stderr.read().rstrip().decode("utf-8"))

            if verbose:
                print(out_dict["stdout"][-1])
                print("\nErrors (if any):")
                print(out_dict["stderr"][-1])

        # close the connection
        if close_connection:
            self._ssh_client.close()
            self._ssh_client = None

        return out_dict

    def connect_sftp_client(self):
        """Connect to the server through SFPT on port 22.

        Returns
        -------
        obj
            paramiko sfpt client object
        """
        transport = paramiko.Transport((self.host_address, 22))
        k = paramiko.RSAKey.from_private_key_file(self.pvtkey, password=self.password) if self.pvtkey else None
        transport.connect(username=self.username, password=self.password, pkey=k)
        return paramiko.SFTPClient.from_transport(transport)

    def get_folder_from_server(self, path, dest, recursive=True, close_connection=True):
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
            if true get subfolders content, by default
        close_connection : bool (optional)
            if true close the ssh connection, by default True. Leave the connection open if you plan to run several commands.

        Warnings
        --------
        If in any folder there are files without extensions, the code will fail!
        """

        # connect to the server through SFPT
        if not self._sftp_client:
            self._sftp_client = self.connect_sftp_client()
            print("connection enstablished")

        for item in self._sftp_client.listdir(path):
            remotefile = os.path.join(path, str(item))
            if not os.path.isdir(dest):
                os.mkdir(dest)
            localfilepath = os.path.join(dest, str(item))
            # check if it is a folder (note file w/o ext will thorw an exception!)
            if '.' in item:
                self._sftp_client.get(remotefile, localfilepath)
            else:
                if recursive:
                    self.get_folder_from_server(self._sftp_client, remotefile, localfilepath)
        print("files tranferred!")
        # close the connection
        if close_connection:
            self._sftp_client.close()
            self._sftp_client = None
            print("connection closed")


if __name__ == '__main__':
    pass

    # bot = sshBot(config_file=None, hostname="192.168.0.199", username="franaudo", password="Sxcdews23", pvtkey="")
    bot = sshBot()

    bot.execute_cmds(commands=['ls'], close_connection=True)
    # print(bot.ssh_client)
    # bot.execute_cmds(commands=['ls -l'], close_connection=True)
    # print(bot.ssh_client)
