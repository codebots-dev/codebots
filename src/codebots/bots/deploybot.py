from git import Repo
from codebots.bots import sshBot

COMMITS_TO_PRINT = 5


class DeployBot():
    """Bot to help with the deployment of code on a server. It uses a `sshBot` in
    the background.

    Parameters
    ----------
    local_repo_path : str
        path to the local clone of the repository
    server_repo_path : str
        path to the server bare repository. If no repository is present
        at the given location a bare new one is created.
    server_addres : str
        complete server address (username@host).

    Attributes
    ----------
    local_repo_path : str
        path to the local clone of the repository
    server_repo_path : str
        path to the server bare repository.
    server_addres : str
        complete server address (*username@host*).
    server_complete_address : str
        complete path to the server repository (*username@host:pat/to/server/repository*)
    local_repo : obj
        gitpython Repo object pointing to the local repository.

    Examples
    --------
    .. code-block:: python

        bot = DeployBot('/path/to/local/repo', '/path/to/server/repo', 'username@host')
        sshbot = sshBot.from_credentials_file(".tokens/ssh.json")
        # initial configuration (first time only)
        bot.configure_local()
        bot.configure_server(sshbot)
        # deployment
        bot.deploy_to_server()

    Warnings
    --------
    I still need to figure out how to avoid the use of sshkeys for the pushing part
    """

    def __init__(self, local_repo_path, server_repo_path, server_address) -> None:
        self.local_repo_path = local_repo_path
        self.server_repo_path = server_repo_path
        self.server_address = server_address
        self.server_complete_path = server_address+":"+server_repo_path
        self.local_repo = Repo(local_repo_path)

    def configure_local(self):
        """Configure the local repository to sync with the server.
        """
        if 'deploy' in self.local_repo.remotes:
            self.local_repo.delete_remote("deploy")
        self.local_repo.create_remote("deploy", self.server_complete_path)
        print('deploy added to remotes')
        print('local repository configured!')

    def configure_server(self, sshbot, os='linux'):
        """Configure the server side:
            - check if server has git repository folder;
            - if not create a bare repository;
            - configure the server repository to sync with the local.

        Parameters
        ----------
        sshbot : obj
            instance of an `sshBot` with access to the server.
        """
        git_folder = os.path.join(self.server_repo_path, '.git')

        std_dict = sshbot.execute_cmds(["if test -d {}; then echo {}; fi".format(self.server_repo_path, "yes"),
                                        "if test -d {}; then echo {}; fi".format(git_folder, "yes")], False, False)
        # check if folder exists:
        if std_dict["stdout"][0] != 'yes':
            try:
                cmd = 'mkdir' if os == 'windows' else 'mkdir -p'
                sshbot.execute_cmds(['{} {}'.format(cmd, self.server_repo_path),
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
        print('server repository configured!')

    def deploy_to_server(self, remote_name="deploy", local_name="master", commit_message="deployed"):
        """Deploy the changes to the server.

        Parameters
        ----------
        remote_name : str, optional
            name of the git remote, by default "deploy"
        local_name : str, optional
            name of the local branch to push, by default "master"
        commit_message : str, optional
            message for the commit, by default "deployed"
        """
        if remote_name not in self.local_repo.remotes:
            self.configure_local()
        self._git_push(commit_message, remote_name, local_name)

    def _git_hooks(self):
        raise NotImplementedError()

    def _git_push(self, commit_message, remote_name, local_name):
        """Push the local repo to the server

        Parameters
        ----------
        commit_message : str
            message for the commit.
        remote_name : str
            name of the git remote.
        local_name : str, optional
            name of the local branch to push.
        """

        # if self.local_repo.index.diff(None) or self.local_repo.untracked_files:

        self.local_repo.git.add(A=True)
        self.local_repo.git.commit(m='msg')
        self.local_repo.git.push('--set-upstream', remote_name, local_name)
        print('local deployed to server')
        # else:
        #     print('no changes')

    # def print_commit(commit):
    #     print('----')
    #     print(str(commit.hexsha))
    #     print("\"{}\" by {} ({})".format(commit.summary,
    #                                      commit.author.name,
    #                                      commit.author.email))
    #     print(str(commit.authored_datetime))
    #     print(str("count: {} and size: {}".format(commit.count(),
    #                                               commit.size)))

    # def print_repository(repo):
    #     print('Repo description: {}'.format(repo.description))
    #     print('Repo active branch is {}'.format(repo.active_branch))
    #     for remote in repo.remotes:
    #         print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
    #     print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))


if __name__ == "__main__":
    bot = DeployBot('/home/fr/Code/myRepos/rpc', '/home/franaudo/code/rpc', 'franaudo@nefcloud')
    sshbot = sshBot.from_credentials_file(".tokens/home.json")
    bot.configure_local()
    bot.configure_server(sshbot)
    bot.deploy_to_server(local_name="master")
