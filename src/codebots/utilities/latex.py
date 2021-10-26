import requests
import subprocess
import tempfile
from pathlib import Path

from tqdm import tqdm


from codebots.cli.cli import main


def download(url='https://github.com/jgm/pandoc/releases/download/2.15/pandoc-2.15-windows-x86_64.msi'):

    # r = requests.get(url, allow_redirects=True)

    # Streaming, so we can iterate over the response.
    r = requests.get(url, stream=True)
    total_size_in_bytes = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open('C:/temp/pandoc.msi', 'wb') as f:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")

    # with open('C:/temp/pandoc.msi', 'wb') as f:
    #     f.write(r.content)
    # print(r)

    # temp_dir = tempfile.TemporaryDirectory()
    # try:
    #     process = subprocess.Popen(Path().joinpath(temp_dir.name, 'pandoc.msi'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
    # except:
    #     temp_dir.cleanup()


if __name__ == "__main__":
    download()
