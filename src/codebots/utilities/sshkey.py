import paramiko
import os
from io import StringIO
import sys

def connect_with_pvtkey():
    k = paramiko.RSAKey.from_private_key_file("/home/fr/.ssh/id_rsa", password="Sxcdews23")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("connecting")
    c.connect( hostname = "192.168.0.199", username = "franaudo", pkey = k )
    print ("connected")
    # commands = [ "/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh" ]
    # for command in commands:
    # 	print "Executing {}".format( command )
    # 	stdin , stdout, stderr = c.exec_command(command)
    # 	print stdout.read()
    # 	print( "Errors")
    # 	print stderr.read()
    # c.close()

def ssh_key_gen(length=2048, type='rsa', password=None, username='jumpserver', hostname=None):
    """Generate user ssh private and public key

    Use paramiko RSAKey generate it.
    :return private key str and public key str
    """

    if hostname is None:
        hostname = os.uname()[1]

    f = StringIO()
    try:
        if type == 'rsa':
            private_key_obj = paramiko.RSAKey.generate(length)
        elif type == 'dsa':
            private_key_obj = paramiko.DSSKey.generate(length)
        else:
            raise IOError('SSH private key must be `rsa` or `dsa`')
        private_key_obj.write_private_key(f, password=password)
        private_key = f.getvalue()
        public_key = ssh_pubkey_gen(private_key_obj, username=username, hostname=hostname)
        return private_key, public_key
    except IOError:
        raise IOError('These is error when generate ssh key.')



def create_keypair():

    key = paramiko.RSAKey.generate(4096)
    print(key.get_base64())  # print public key
    key.write_private_key(sys.stdout)  # print private key

    with open("/home/fr/.ssh/pubkey", "w") as key_file:
        key_file.write(key.get_base64())

    key.write_private_key("/home/fr/.ssh/pvtkey")


if __name__ == "__main__":
    connect_with_pvtkey()
