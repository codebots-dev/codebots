import os
import subprocess
import tempfile
from pathlib import Path


from ._bot import BaseBot

__all__ = [
    'LatexBot',
]


class LatexBot(BaseBot):
    """LatexBot.
    """

    def __init__(self, config_file=None, sender=None) -> None:
        self.__name__ = "emailbot"

    def _clone_overleaf(self, document_code):
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

    def convert_tex_to_docx(self, input_path, output_path=None):
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
            output = str(file).split('.tex')[
                0]+'.docx' if not output_path else Path().joinpath(output_path, str(file.name).split('.tex')[0]+'.docx')
            out = subprocess.run(["pandoc", "-o", output, "-t", "docx", file])
            print("The exit code was: %d" % out.returncode)

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
        temp_dir = self._clone_overleaf(document_code)
        self.convert_tex_to_docx(Path().joinpath(temp_dir.name, document_code), output_path)
        print(f"project saved in {output_path}")
        temp_dir.cleanup()
        print("temporary clone removed")
