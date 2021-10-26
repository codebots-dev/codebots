import os
import importlib
import subprocess
import tempfile
from pathlib import Path
from sys import platform


from ._bot import BaseBot
from ..utilities.web_tools import download_file
from ..utilities import os_tools

__all__ = [
    'LatexBot',
]


class LatexBot(BaseBot):
    """LatexBot.
    """

    def __init__(self, config_file=None, sender=None) -> None:
        self.__name__ = "latexbot"

    def install_dependencies(self, git, pandoc, miktex):
        """Installs the dependencies needed, namely:
            - git
            - pandoc 2.15
            - latex

        Parameters
        ----------
        None

        Kwargs
        ------
        git : bool, optional
            install git if not already present
        pandoc : bool, optional
            install pandoc if not already present
        miktex : bool, optional
            install latex (miktex distribution) if not already present

        Raises
        ------
        Exception
            in case of an exeption, the temp_dir is automatically removed.
        """
        temp_dir = tempfile.TemporaryDirectory()
        try:

            if platform == "linux" or platform == "linux2":  # linux
                raise NotImplementedError("your os is currently not supported")
            elif platform == "darwin":  # OS X
                raise NotImplementedError("your os is currently not supported")
            elif platform == "win32":  # Windows
                settings = {
                    'pandoc':
                    {'url': 'https://github.com/jgm/pandoc/releases/download/2.15/pandoc-2.15-windows-x86_64.msi',
                     'function': 'install_msi',
                     'file_name': 'pandoc.msi'},
                    'git':
                    {'url': 'https://github.com/git-for-windows/git/releases/download/v2.33.1.windows.1/Git-2.33.1-64-bit.exe',
                     'function': 'install_exe',
                     'file_name': 'git.exe'},
                    'miktex':
                    {'url': 'https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-21.8-x64.exe',
                     'function': 'install_exe',
                     'file_name': 'miktex.exe'}
                }
            for tool, parameter in settings.items():
                file_path = Path().joinpath(temp_dir.name, parameter['file_name'])
                if not os_tools.is_tool(tool) and locals()[tool]:
                    print(f'downloading {tool}')
                    download_file(url=parameter['url'],
                                  file_path=file_path)
                    print(f'installing {tool}')
                    installation_function = getattr(os_tools, parameter['function'])
                    installation_function(file_path=file_path)

                else:
                    print(f'{tool} skipped or already installed')
        except:
            temp_dir.cleanup()
            raise Exception("ERROR, something went wrong")

    def _clone_overleaf_temp(self, document_code):
        """Temporarily clone the overleaf project on the local machine.

        Parameters
        ----------
        document_code : str
            code of the overleaf project. you can find in the address bar in your
            broweser when you open the overleaf project.

        Returns
        -------
        TemporaryDirctory object
            the temporary directory where the project has been cloned. This can
            be used later to be cleaned up using `temp_dir.cleanup()`.

        Raises
        ------
        Exception
            if this exception is raised, the cloning process has been aborted.
            Check if the `document_code` is correct and that you have `git`
            installed on your machine.
        """
        temp_dir = tempfile.TemporaryDirectory()
        try:
            out = subprocess.run(["git", "clone", f"https://git.overleaf.com/{document_code}"], cwd=temp_dir.name)
            if out.returncode == 0:
                print(f"project temporary saved in {temp_dir.name}")
        except:
            temp_dir.cleanup()
            raise RuntimeError
        return temp_dir

    def convert_tex_to_docx(self, input_path, output_path=None, open_docx=False):
        """convert all the .tex files in a folder into .docx files. If no `output_path`
        is provided, the .docx files will be saved in the same directory as the .tex
        files.

        Parameters
        ----------
        input_path : str
            path to the folder containing the .tex file(s)
        output_path : str, optional
            path to the output .docx file(s), by default None
        """
        pathlist = Path(input_path).rglob('*.tex')
        for file in pathlist:
            if not output_path:
                output = str(file).split('.tex')[0]+'.docx'
                open_docx = True
            else:
                output = Path().joinpath(output_path, str(file.name).split('.tex')[0]+'.docx')
            out = subprocess.run(['pandoc', '-o', output, '-t', 'docx', file])
            print(f"docx saved in {output}")
            # print("The exit code was: %d" % out.returncode)
            if open_docx:
                print("opening file... don't forget to save it (save as...)!")
                p = subprocess.Popen(output, shell=True)
                p.wait()

    def convert_overleaf_to_docx(self, document_code, output_path):
        """convert the overleaf project into a .docx file. Any .tex file in the
        overleaf repository will be converted into a .docx file with the same name.

        Parameters
        ----------
        document_code : str
            code of the overleaf project. you can find in the address bar in your
            broweser when you open the overleaf project.
        output_path : str
            path to the output .docx file
        """
        temp_dir = self._clone_overleaf_temp(document_code)
        try:
            self.convert_tex_to_docx(Path().joinpath(temp_dir.name, document_code), output_path)

            temp_dir.cleanup()
            print("temporary clone removed")
        except:
            temp_dir.cleanup()
            raise Exception("ERROR")
