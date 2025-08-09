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

    def __init__(self, alias=None, config_file=None, **kwargs) -> None:
        env_host = os.getenv("SSHBOT_HOSTNAME")
        env_user = os.getenv("SSHBOT_USERNAME")
        env_pass = os.getenv("SSHBOT_PASSWORD")
        env_pvtkey = os.getenv("SSHBOT_PVTKEY")
        if env_host and env_user:
            self.hostname = env_host
            self.username = env_user
            self.password = env_pass
            self.pvtkey = env_pvtkey
        else:
            if not config_file:
                if not alias:
                    if not kwargs:
                        raise ValueError("Either an existing config_file or the credentials must be passed")
                    self._credentials = kwargs
                    for k, v in self._credentials.items():
                        setattr(self, k, v)
                else:
                    from .. import TOKENS
                    config_file = os.path.join(TOKENS, f"{alias}.json")
                    super().__init__(config_file)
            else:
                super().__init__(config_file)
            # Ensure all required attributes are set
            for attr in ["hostname", "username", "password", "pvtkey"]:
                if not hasattr(self, attr):
                    setattr(self, attr, self._credentials.get(attr, None))
        self.host_address = getattr(self, 'hostname', None)
        if self.host_address and '.' not in self.host_address:
            self.host_address = socket.gethostbyname(self.host_address)
        self._ssh_client = None
        self._sftp_client = None

    @property
    def ssh_client(self):
        return self._ssh_client

    @property
    def sftp_client(self):
        return self._sftp_client

    def connect_ssh_client(self):
        """Establish the ssh connection"""
        import paramiko
        hostname = getattr(self, 'hostname', None)
        username = getattr(self, 'username', None)
        password = getattr(self, 'password', None)
        pvtkey = getattr(self, 'pvtkey', None)
        if not hostname or not username:
            raise ValueError("Missing required SSH credentials: hostname and username.")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file(pvtkey, password=password) if pvtkey else None
        ssh_client.connect(hostname=hostname, username=username, password=password, pkey=k)
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
