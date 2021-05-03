import os
from git import Repo
from ._bot import BaseBot

COMMITS_TO_PRINT = 5


class DeployBot(BaseBot):
    """Bot to help with the deployment of code on a server. It uses a `sshBot` in
    the background.

    Parameters
    ----------
    project : str
        project name. It is used to find the configuration file associated to it.
    config_file : json
        path to a json file containing the required info. You can use the command
        line to create one or manually configure a json file following this
        template:

            .. code-block:: json

                {
                    "local_repo_path" :  "_______",
                    "server_repo_path" : "_______",
                    "server_addres" :    "_______",
                }

    Attributes
    ----------
    local_repo_path : str
        path to the local clone of the repository
    server_repo_path : str
        path to the server bare repository.
    server_addres : str
        complete server address (*username@host*).
    server_complete_path : str
        complete path to the server repository (*username@host:pat/to/server/repository*)
    local_repo : obj
        gitpython Repo object pointing to the local repository.

    Examples
    --------
    .. code-block:: python

        bot = DeployBot('my_project')
        bot.deploy_to_server()

    Warnings
    --------
    I still need to figure out how to avoid the use of sshkeys for the pushing part
    """

    def __init__(self, project=None, config_file=None) -> None:
        self.__name__ = "deploybot"
        if not config_file:
            if not project:
                raise ValueError("Either a project name or a config_file must be passed")
            from .. import TOKENS
            config_file = os.path .join(TOKENS, "{}.json".format(project))
        super().__init__(config_file)
        self.server_complete_path = self.server_address+":"+self.server_repo_path
        self.local_repo = Repo(self.local_repo_path)

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
        self.local_repo.git.commit(m=commit_message)
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
    bot = DeployBot('my_project')
    bot.deploy_to_server(local_name="master")
