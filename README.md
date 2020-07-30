## parth
Parth is a super-fast JWT (https://jwt.io/) hacking tool. Mainly developed for brute-forcing the JWT against millions of secret. It also generates a few tempered JWTs to test the JWT None signature.

<img src="https://github.com/priyanshus/parth/blob/master/media/screenshot.png">

**Features**
- Parth can help you to discover the secret used for JWT creation.
- Can generate secrets based on wordlist given.
- Generates around 8 million secrets for 4 words (eg. my james jwt secret) given as input.
- Generates tempered `None` algorithms and other combinations to test jwt signatures.
- Parth runs in multiprocessiong mode. For 8 million secrets to be tested against JWT, it hardly takes 60-70s.
- In absence of custom secret, Parth is capable of brute-forcing JWT secret against 1 million top most common passwords.
- While generating the secrets, Parth is intelligent enough to replace the common characters with the ones which are commonly used in passwords a -> @, i - !, 0 - @, 3 -> E etc.

**How to run**

- `git clone https://github.com/priyanshus/parth.git` 
- `cd parth`
- `pip install -r requirements.txt`
- `python parth.py --token='jwtoken_to_be_hacked' --w='my custom word list' --thread=50`

Example:

`python3 parth.py --token='eyJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiSm9obiBEb2UifQ.q5LSN4zcymGB7Echer9KjO1xZ4b1xLRSLa6V1LxAP8g' --w='my secret jwt' --thread=50`

For more details: `python parth.py -h`

**CLI Args**
| Arg | Required | Default Value | Description |
| :---: | :---: | :---: | :---: |
| --token | Yes | | JWT to be hacked |
| --thread | No | 8 | Number of threads to be used for bruteforcing |
| --wordlist | No | | A custom word list separated by whitespace to be used to form the secrets |
| --file | No | true | To write the secrets in a file |
| --mode | No | both | To run the Parth in crack or generate mode. Choices [crack, generate] |

One can run Parth in crack or generate mode to perform either cracking the secret or only generating the tempered JWTS.

**How it can help you**
- Mainly developed for bugbounty/white hat penetration testing purpose.
- QA can use this tool to check if production JWT is created using weak secret.
- QA can also use this tool to only generate tempered JWTs to test the None algorithms. `python parth.py --token='<jwt>' --mode=generate`
- One can use seclist generation feature of Parth to generate millions of password for bruteforcing. 

**Important Notes** :warning:
- Be wise while using Parth to generate custom secrets. As Parth is capable of generating huge combinations based on input. For four string, it generates 8 million secrets. Having too many custom words can slow down your system.
- Parth only support HMAC based JWT.

