import sys
import jwt
import functools
from time import time
from multiprocessing import Pool as ThreadPool


def __decoder(token, secret):
    """This function checks if a secret can decrypt a JWT token.
    Arguments:
        token {String} -- Token
        secret {List} -- A seclist for decoding the token
    Returns:
        [boolean] -- Result of the decoding attempt
    """
    try:
        payload = jwt.decode(token, secret)
        print(f"Found secret: {secret}")
        print(f"Decoded token payload: {payload}")
        return True
    except jwt.exceptions.DecodeError:
        return False
    except jwt.exceptions.InvalidTokenError:
        return False
    except Exception as ex:
        sys.exit(1)


def decode_jwt(token, secrets, threads=8):
    print('Decoding JWT on {} threads'.format(threads))
    pool = ThreadPool(threads)
    start = time()
    pool.map(functools.partial(__decoder, token), secrets)
    pool.close()
    pool.join()
    print('Took %s seconds' % (time() - start))
