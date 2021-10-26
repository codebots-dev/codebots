import subprocess


### ------------------------ CROSS PLATFORM ---------------------------------###
def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


### ---------------------------- WINDOWS ------------------------------------###
def install_msi(file_path):
    """Perform a silent install of a msi package (Windows only)

    Parameters
    ----------
    file_path : str
        complete path (directory/name.msi) to the msi package.

    Raises
    ------
    Exception
        in case of an exeption, the temp_dir is automatically removed.
    """
    out = subprocess.run(["msiexec.exe", "/i", file_path, "/QN", "STARTAPP=1", "SHOWHELP=Yes"])
    if out.returncode == 0:
        print("installation complete")


def install_exe(file_path):
    """Call the installation executable

    Parameters
    ----------
    file_path : obj
        pathlib Path object with the location of the exe file

    Returns
    -------
    int
        0 - Succes!
        1 - Fail
    """
    print("follow installation dialogue...")
    out = subprocess.run(file_path)
    if out.returncode == 0:
        print("installation complete")
    return out


### ------------------------------ DEBUG ------------------------------------###
if __name__ == "__main__":
    import os
    # print(is_tool("latexmk"))
    # install_exe('c:/temp/miktex.exe')
    p = subprocess.Popen('C:/temp/main.docx', shell=True)
    p.wait()
    # os.startfile('C:/temp/main.docx')

    print('ciao')
