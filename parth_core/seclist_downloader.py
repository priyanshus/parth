import os
from pathlib import Path
from typing import List

import requests

from parth_core.constants import TOP_1000K_URL

_FILE_NAME_1000K = '10-million-password-list-top-1000000.txt'


def __download_secret_list() -> str:
    parth_dir = os.path.join(str(Path.home()), '.parth')
    if not os.path.exists(parth_dir):
        os.mkdir(parth_dir)

    file_path = os.path.join(parth_dir, _FILE_NAME_1000K)

    if not os.path.exists(file_path):
        print('Downloading secret list file...')
        res = requests.get(TOP_1000K_URL, verify=False)
        with open(file_path, 'wb') as f:
            f.write(res.content)

    return file_path


def get_1000k_seclist() -> List:
    file_path = __download_secret_list()
    with open(file_path, 'r') as file:
        secrets = file.readlines()

    sec_list = [x.strip() for x in secrets]
    return sec_list
