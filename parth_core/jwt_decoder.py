import sys
import jwt
import json
import functools
import base64
from tqdm import tqdm
from time import time
from multiprocessing import Pool as ThreadPool
from parth_core.constants import JWT_HMAC_ALGOS


def __is_hmac_algo(token):
    encoded_header = token.split('.')[0]
    decoded_header = base64.urlsafe_b64decode(encoded_header).decode()
    alg = json.loads(decoded_header)['alg']
    return alg, alg in JWT_HMAC_ALGOS

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
    alg, is_hmac = __is_hmac_algo(token)
    if not is_hmac:
        print('Algorithm {} used by JWT is not supported by Parth'.format(alg))
        sys.exit(1)
    print('Decoding JWT on {} threads'.format(threads))
    pool = ThreadPool(threads)
    start = time()
    pool.map(functools.partial(__decoder, token), tqdm(secrets))
    pool.close()
    pool.join()
    print('Took %s seconds' % (time() - start))
