import requests
import subprocess
import tempfile
from pathlib import Path

from tqdm import tqdm


from codebots.cli.cli import main


def download(url='https://github.com/jgm/pandoc/releases/download/2.15/pandoc-2.15-windows-x86_64.msi'):

    print('downloading pandoc 2.15')
    temp_dir = tempfile.TemporaryDirectory()
    setup_file_path = Path().joinpath(temp_dir.name, 'pandoc.msi')

    r = requests.get(url, stream=True)  # Streaming to allow the progressbar.
    total_size_in_bytes = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(setup_file_path, 'wb') as f:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

    try:

        out = subprocess.run(["msiexec.exe", "/i", setup_file_path, "/QN", "/L*V",
                             f"{temp_dir.name}\msilog.log", "STARTAPP=1", "SHOWHELP=Yes"])
        if out.returncode == 0:
            print(f"pandoc successfully installed")
    except:
        temp_dir.cleanup()
        raise Exception("ERROR, something went wrong")


if __name__ == "__main__":
    download()
