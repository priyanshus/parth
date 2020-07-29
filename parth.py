import argparse

from parth_core.jwt_decoder import decode_jwt
from parth_core.jwt_generator import JWTGenerator
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

    parser.add_argument(
        "--file",
        metavar='file',
        help='write secrets to a file',
        choices=['true', 'false'],
        default='true'
    )

    parser.add_argument(
        "--mode",
        metavar='mode',
        help='run the parth in crack or generate mode',
        choices=['crack', 'generate'],
        default='both'
    )

    return parser.parse_args()

def crack():
    seclist = []
    if args.wordlist:
        word_list = args.wordlist.split()
        seclist_generator = SeclistGenerator(word_list, args.file)
        seclist = seclist_generator.generate()

    # Download seclist from Github
    git_sec_list = get_1000k_seclist()

    seclist.extend(git_sec_list)
    print('Testing JWT against {} secrets'.format(len(seclist)))

    # Decode JWT
    decode_jwt(args.token, seclist, int(args.thread))


def generate():
    generator = JWTGenerator(args.token)
    generator.generate_jwt()


if __name__ == '__main__':
    args = arg_parser()

    if args.mode == 'crack':
        crack()
    elif args.mode == 'generate':
        generate()
    else:
        crack()
        generate()
