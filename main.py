import argparse

from parth_core.jwt_decoder import decode_jwt
from parth_core.seclist_downloader import get_1000k_seclist
from parth_core.seclist_generator import SeclistGenerator


def arg_parser() -> argparse:
    parser = argparse.ArgumentParser("JWT Scanner")

    parser.add_argument(
        "--token",
        metavar='token',
        help="token to decode",
        required=True,
    )

    parser.add_argument(
        "--wordlist",
        metavar='wordlist',
        help='custom word list',
        required=False
    )

    parser.add_argument(
        "--thread",
        metavar='threads',
        help='threads',
        default=8
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = arg_parser()

    # Generate custom seclist
    seclist_generator = SeclistGenerator(args.wordlist.split())
    seclist = seclist_generator.generate()

    # Download seclist from Github
    git_sec_list = get_1000k_seclist()

    seclist.extend(git_sec_list)
    print('Testing JWT against {} secrets'.format(len(seclist)))

    # Decode JWT
    decode_jwt(args.token, seclist, int(args.thread))
