import requests
from tqdm import tqdm


def download_file(url, file_path):
    """[summary]

    Parameters
    ----------
    url : str
        url to the file to be downloaded
    temp_dir : obj
        TemporaryDirectory object containing the msi package
    file_path : str
        complete path (directory/name.msi) to the msi package
    """

    r = requests.get(url, stream=True)  # Streaming to allow the progressbar.
    total_size_in_bytes = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(file_path, 'wb') as f:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    # if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    #     print("ERROR, something went wrong")
    #     return 1
    # else:
    #     return 0


# if __name__ == "__main__":
#     download_file(url='https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-21.8-x64.exe')
