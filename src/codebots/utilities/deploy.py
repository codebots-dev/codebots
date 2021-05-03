import os
from ..bots import sshBot


def configure_local(local_repo, server_complete_path):
    """Configure the local repository to sync with the server.

    Parameters
    ----------
    local_repo_path : str
        path to the local clone of the repository
    server_complete_path : str
        complete path to the server repository (*username@host:pat/to/server/repository*)
    """
    if 'deploy' in local_repo.remotes:
        local_repo.delete_remote("deploy")
    local_repo.create_remote("deploy", server_complete_path)

    return """`deploy` added to remotes.
        local repository configured!"""


def configure_server(server_repo_path, sshbot=None, os_type='linux'):
    """Configure the server side:
        - check if server has git repository folder;
        - if not create a bare repository;
        - configure the server repository to sync with the local.

    Parameters
    ----------
    server_repo_path : str
        path to the server bare repository.
    sshbot : obj, optional
        instance of an `sshBot` with access to the server, by default None.
    """
    git_folder = os.path.join(server_repo_path, '.git')

    if not sshbot:
        sshbot = sshBot()
    std_dict = sshbot.execute_cmds(["if test -d {}; then echo {}; fi".format(server_repo_path, "yes"),
                                    "if test -d {}; then echo {}; fi".format(git_folder, "yes")], False, False)
    # check if folder exists:
    if std_dict["stdout"][0] != 'yes':
        try:
            cmd = 'mkdir' if os == 'windows' else 'mkdir -p'
            sshbot.execute_cmds(['{} {}'.format(cmd, server_repo_path),
                                'git --git-dir={} {}'.format(git_folder, 'init'),
                                 'git --git-dir={} {}'.format(git_folder, 'config receive.denyCurrentBranch updateInstead')], verbose=False)
        except:
            raise Exception("Something went wrong!! Please make sure that the server path is valid and you have git\
                on the server side.")
    else:
        if std_dict["stdout"][1] != 'yes':
            sshbot.execute_cmds(['git --git-dir={} {}'.format(git_folder, 'init'),
                                 'git --git-dir={} {}'.format(git_folder, 'config receive.denyCurrentBranch updateInstead')], verbose=False)
        else:
            sshbot.execute_cmds(['git --git-dir={} {}'.format(git_folder,
                                                              'config receive.denyCurrentBranch updateInstead')], verbose=False)
    return 'server repository configured!'
