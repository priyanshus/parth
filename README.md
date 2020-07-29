## parth
Parth is a super-fast JWT (https://jwt.io/) hacking tool.

![Screenshot](https://github.com/priyanshus/parth/blob/master/media/screenshot.png)

**Features**
- Parth can help you to discover the secret for JWT creation.
- Can generate secrets based on wordlist given.
- Generates around 8 million secrets for 4 words given as input.
- Generates tempered `None` algorithms and other combinations to test jwt signatures.
- Parth runs in multiprocessiong mode. For 8 million secrets to be tested against JWT, it hardly takes 60-70s.
- In absence of custom secret, Parth is capable of brute-forcing JWT secret against 1 million top most common passwords.

**How to run**

`git clone https://github.com/priyanshus/parth.git` 

`cd parth`

`pip install -r requirements.txt`

`python parth.py --token='jwtoken_to_be_hacked' --w='my custom word list' --thread=50`

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


**Important Notes** :warning:
- Be wise while using Parth to generate custom secrets. As Parth is capable of generating huge combinations based on input. For four string, it generates 8 million secrets. Having too many custom words can slow down your system.
- Parth only support HMAC based JWT. 



 
