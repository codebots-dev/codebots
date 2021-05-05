from ..bots import sshBot
from pathlib import Path


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


def configure_server(server_repo_path, branch='main', sshbot=None, os_type='linux'):
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

    # git_folder = Path(server_repo_path).joinpath('.git')
    git_folder = server_repo_path + '/.git'
    if not sshbot:
        sshbot = sshBot()

    # check if server folder exists and if it is a git repository
    tests = ["if test -d {}; then echo {}; fi".format(x, "yes") for x in [server_repo_path, git_folder]]
    std_dict = sshbot.execute_cmds(tests, False, False)

    cmds = ['{} {}'.format('mkdir' if os_type == 'windows' else 'mkdir -p', server_repo_path),
            'git --git-dir={} init -b {}'.format(git_folder, branch),
            'git --git-dir={} config receive.denyCurrentBranch updateInstead'.format(git_folder)]

    if std_dict["stdout"][0] != 'yes':
        cmd = cmds
    else:
        cmd = cmds[1:] if std_dict["stdout"][1] != 'yes' else [cmds[-1]]
    out = sshbot.execute_cmds(cmd, verbose=False)

    for x in out["stdout"]:
        if x != '':
            print(x)

    for x in out["stderr"]:
        if x != '':
            return x
    return 'server repository configured!'
