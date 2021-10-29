import subprocess
import os


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

### ------------------------------ LINUX ------------------------------------###


def install_deb(file_path):
    out = subprocess.run(["sudo", "dpkg", "-i", file_path])
    if out.returncode == 0:
        print("installation complete")


def register_GPG_key(keyserver="hkp://keyserver.ubuntu.com:80", recv_key="D6BC243565B2087BC3F897C9277A7293F59E4889"):
    out = subprocess.run(["sudo", "apt-key", "adv", "--keyserver", keyserver, "--recv-keys", recv_key])
    return out


def install_miktex_ubuntu(url="http://miktex.org/download/ubuntu bionic universe"):
    os.system(f"echo deb {url} | sudo tee /etc/apt/sources.list.d/miktex.list")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install miktex")


### ------------------------------ DEBUG ------------------------------------###
if __name__ == "__main__":
    register_GPG_key()
    install_miktex_ubuntu()
