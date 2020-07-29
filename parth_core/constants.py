
SPECIAL_CHARACTERS_REPLACEMENTS = {
    "a": "@",
    "o": "0",
    "s": "$",
    "e": "3",
    "i": "!"
}

SPECIAL_CHARACTERS_REPLACEMENTS_FOR_DIGITS = {
    "0": ["@", "$"],
    "1": ["I", "!"],
    "3": "E"
}

SPECIAL_END_CHARACTERS = ['#', '$', '@', '!', '_', ' ']
SPECIAL_NUMBERS = ['1', '123', '1234', '007']

TOP_1000K_URL = ("https://github.com/danielmiessler/SecLists/raw/master/Passwords/Common-Credentials/10-million"
                 "-password "
                 "-list-top-1000000.txt")

JWT_HMAC_NONE_ALGOS = ['None', 'NULL', ' ', None]
JWT_HMAC_ALGOS = ['HS256', 'HS384', 'HS512']