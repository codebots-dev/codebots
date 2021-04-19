import os
import re
from git import Repo
import subprocess
from codebots.bots import sshBot

COMMITS_TO_PRINT = 5


class DeployBot():
    def __init__(self, local_repo_path, server_repo_path, server_address) -> None:
        self.local_repo_path = local_repo_path
        self.server_repo_path = server_repo_path
        self.server_address = server_address
        self.local_repo = Repo(local_repo_path)
        self.server_complete_path = server_address+":"+server_repo_path

    def configure_local(self):
        if 'deploy' in self.local_repo.remotes:
            self.local_repo.delete_remote("deploy")
        self.local_repo.create_remote("deploy", self.server_repo_path)
        print('deploy added to remotes')
        print('local repository configured!')

    def configure_server(self):
        """
        - check if server has git repo folder
        - if not clone repo or create a bare repo
        - configure server to UpdateInstead
        """
        git_folder = os.path.join(self.server_repo_path, '.git')
        sshbot = sshBot.from_credentials_file(".tokens/home.json")

        std_dict = sshbot.execute_cmds(["if test -d {}; then echo {}; fi".format(self.server_repo_path, "yes"),
                                        "if test -d {}; then echo {}; fi".format(git_folder, "yes")], False, False)
        # check if folder exists:
        if std_dict["stdout"][0] != 'yes':
            sshbot.execute_cmds(['mkdir {}'.format(self.server_repo_path),
                                'git --git-dir={} {}'.format(git_folder, 'init'),
                                 'git --git-dir={} {}'.format(git_folder, 'config receive.denyCurrentBranch updateInstead')], verbose=False)
        else:
            if std_dict["stdout"][1] != 'yes':
                sshbot.execute_cmds(['git --git-dir={} {}'.format(git_folder, 'init'),
                                     'git --git-dir={} {}'.format(git_folder, 'config receive.denyCurrentBranch updateInstead')], verbose=False)
            else:
                sshbot.execute_cmds(['git --git-dir={} {}'.format(git_folder,
                                                                  'config receive.denyCurrentBranch updateInstead')], verbose=False)
        print('server repository configured!')

    def git_push(self, commit_message, remote_name):
        try:
            self.local_repo.git.add(A=True)
            self.local_repo.index.commit(commit_message)
            remote = self.local_repo.remote(name=remote_name)
            remote.push()
        except:
            print('Some error occured while pushing the code')

    def deploy_to_server(self, remote_name="deploy", commit_message="deployed"):
        if remote_name not in self.local_repo.remotes:
            self.configure_local()
        self.git_push(commit_message, remote_name)

    def print_commit(commit):
        print('----')
        print(str(commit.hexsha))
        print("\"{}\" by {} ({})".format(commit.summary,
                                         commit.author.name,
                                         commit.author.email))
        print(str(commit.authored_datetime))
        print(str("count: {} and size: {}".format(commit.count(),
                                                  commit.size)))

    def print_repository(repo):
        print('Repo description: {}'.format(repo.description))
        print('Repo active branch is {}'.format(repo.active_branch))
        for remote in repo.remotes:
            print('Remote named "{}" with URL "{}"'.format(remote, remote.url))
        print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))


if __name__ == "__main__":
    bot = DeployBot('/home/fr/Code/repo_test', '/home/franaudo/code/repo_test2', 'franaudo@nefcloud')
    bot.configure_server()

    # bot.configure_local()
    # bot.deploy_to_server()
