import argparse
import os
from pathlib import Path
from typing import List

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


class PasswordGenerator:
    """Generate a list of password based on wordlist provided by user"""

    def __init__(self, word_list):
        self.__word_list: List[str] = word_list
        self.__password = []
        self.__word = ''
        self.__db = dict()

    def generate(self) -> List:
        for word in self.__word_list:
            self.__generate_one_word_passwords(word)
        self.__generate_two_words_passwords()
        self.__generate_three_words_passwords()

        print('Generated {} passwords'.format(len(self.__password)))
        return self.__password

    def __generate_one_word_passwords(self, word):
        self.__word = word
        self.__password = []
        self.__generate_word_forms(word)
        self.__replace_with_special_chars()
        self.__append_connectors()
        self.__append_numbers()

    def __generate_word_forms(self, word):
        word_forms = []
        if not word.isdigit():
            word_forms.extend([word.upper(), word.title(), word.lower()])
        else:
            word_forms.append(word)

        self.__password.extend(word_forms)
        self.__db[word] = {}

    def __replace_with_special_chars(self):
        words_with_special_chars = []

        for key in self.__password:
            if key.isdigit():
                for char in SPECIAL_CHARACTERS_REPLACEMENTS_FOR_DIGITS:
                    if key.__contains__(char):
                        for item in SPECIAL_CHARACTERS_REPLACEMENTS_FOR_DIGITS[char]:
                            output = key.replace(char, item)
                            words_with_special_chars.append(output)

            for char in SPECIAL_CHARACTERS_REPLACEMENTS:
                if key.__contains__(char):
                    output = key.replace(char, SPECIAL_CHARACTERS_REPLACEMENTS[char])
                    if not words_with_special_chars.__contains__(output):
                        words_with_special_chars.append(output)

        # self.__db[self.__word]['special_chars'] = words_with_special_chars
        self.__password.extend(words_with_special_chars)

    def __append_connectors(self):
        words_with_connectors = []
        for key in self.__password:
            for char in SPECIAL_END_CHARACTERS:
                output = key + char
                words_with_connectors.append(output)

        # self.__db[self.__word]['connectors'] = words_with_connectors
        self.__db[self.__word]['connectors'] = words_with_connectors
        self.__password.extend(words_with_connectors)

    def __append_numbers(self):
        words_ending_with_numbers = []
        for key in self.__db[self.__word]['connectors']:
            for number in SPECIAL_NUMBERS:
                output = key + number
                words_ending_with_numbers.append(output)
        # self.__db[self.__word]['numbers'] = words_ending_with_numbers
        self.__password.extend(words_ending_with_numbers)
        self.__db[self.__word]['passwords'] = self.__password

    def __generate_two_words_passwords(self):
        all_two_words_password = []
        if len(self.__word_list) > 1:
            for i in range(0, len(self.__word_list)):
                for j in range(0, len(self.__word_list)):
                    if i != j:
                        index = self.__word_list[i]
                        next = self.__word_list[j]
                        index_connectors = self.__db[index]['connectors']
                        next_passwords = self.__db[next]['passwords']
                        temp_passwords = [(first + second).rstrip() for first in index_connectors
                                          for second in next_passwords]
                        all_two_words_password.extend(temp_passwords)

        self.__db['two_words'] = all_two_words_password
        self.__password.extend(all_two_words_password)

    def __generate_three_words_passwords(self):
        all_three_words_password = []
        if len(self.__word_list) > 2:
            temp_passwords = [password + connector for password in self.__db['two_words']
                              for connector in SPECIAL_END_CHARACTERS]
            for temp_password in temp_passwords:
                for input_key in self.__word_list:
                    for entry in self.__db[input_key]['connectors']:
                        three_word_password = (temp_password + entry).rstrip()
                        all_three_words_password.append(three_word_password)

            all_three_words_password.extend(temp_passwords)
        self.__db['three_words'] = all_three_words_password
        self.__password.extend(all_three_words_password)


def main():
    parser = argparse.ArgumentParser(description='generate a password list from permutation of probable words')
    parser.add_argument("--w", metavar='words', type=str, help='words', required=True)
    args = parser.parse_args()
    keys = args.w.split()

    generator = PasswordGenerator(keys)
    passwords = generator.generate()

    # Check if scanners directory exists and create a password list file
    parth_directory = os.path.join(str(Path.home()), '.parth')
    if not os.path.exists(parth_directory):
        os.mkdir(parth_directory)
    file_path = os.path.join(parth_directory, 'password-list.txt')
    if os.path.exists(file_path):
        print('Found an existing password list file. Removing it.')
        os.remove(file_path)
    with open(file_path, 'a') as file:
        for password in passwords:
            file.write(password + '\n')

    print('Password file path: {}'.format(file_path))
    return passwords


if __name__ == '__main__':
    main()
