import argparse
import sys
import jwt
from typing import Tuple, List
import functools
import os
import requests
from time import time
from multiprocessing import Pool as ThreadPool
from pathlib import Path

from password_generator import PasswordGenerator

TOP_1000K_URL = ("https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10-million"
                 "-password "
                 "-list-top-1000000.txt")


def generate_custom_seclist(keys) -> List:
    generator = PasswordGenerator(keys)
    return generator.generate()


def get_seclist_path() -> Tuple[str, str]:
    parth_dir = os.path.join(str(Path.home()), '.parth')
    if not os.path.exists(parth_dir):
        os.mkdir(parth_dir)

    return TOP_1000K_URL, os.path.join(parth_dir, '10-million-password-list-top-1000000.txt')


def download_secret_list():
    url, file_path = get_seclist_path()

    if not os.path.exists(file_path):
        print('Downloading secret list file...')
        res = requests.get(url, verify=False)
        with open(file_path, 'wb') as f:
            f.write(res.content)


def get_candidates(args):
    custom_secrets = []
    _, file_path = get_seclist_path()
    with open(file_path, 'r') as f:
        lines = [line.replace('\n', '') for line in f]

    if args.w:
        print('Generating secrets based on wordlist...')
        custom_secrets = generate_custom_seclist(args.w.split())

    lines.extend(custom_secrets)
    print('Testing JWT against {} secrets'.format(len(lines)))
    return lines


def arg_parser() -> argparse:
    parser = argparse.ArgumentParser("JWT Scanner")

    parser.add_argument(
        "--token",
        metavar='token',
        help="token to decode",
        required=True,
    )

    parser.add_argument(
        "--w",
        metavar='wordlist',
        help='custom word list',
        required=False
    )

    return parser.parse_args()


def decode(token, secret):
    """This function checks if a secret can decrypt a JWT token.
    Arguments:
        secret {string} -- A candidate word for decoding
    Returns:
        [boolean] -- Result of the decoding attempt
    """
    try:
        payload = jwt.decode(token, secret)
        print(f"Found secret: {secret}")
        print(f"Decoded token payload: {payload}")
    except jwt.exceptions.DecodeError:
        pass
    except jwt.exceptions.InvalidTokenError:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        sys.exit(1)


def main():
    args = arg_parser()
    download_secret_list()
    candidates = get_candidates(args)
    pool = ThreadPool(50)
    start = time()
    pool.map(functools.partial(decode, args.token), candidates)
    pool.close()
    pool.join()
    print('Took %s seconds' % (time() - start))


if __name__ == '__main__':
    main()
