# External imports
import string

# Internal imports

# Constants
KEY_LEN = 6
BOOK_KEY_LEN = 5
MATRIX_ROW_SIZE = 5
MATRIX_COL_SIZE = 6
# BOGUS_LETTER = 'X'
# FILLER_LETTER = 'Z'
COMMON_LETTERS = 'ETAONRIS'


def check_alphabet(text, is_key=False):
    for character in text:
        if character not in list(string.ascii_uppercase):
            if not is_key and (character not in list(string.digits) and character != "/" and character != "."):
                return False
            # return False
    return True


def key_verifier(key):
    if not check_alphabet(key, is_key=True):
        raise Exception('The allowed alphabet consists only of the capital English letters.')

    if len(key) != KEY_LEN:
        raise Exception('The key lehgth is has to be 6.')

    if len(key) == 0:
        raise Exception('The secret key field cannot be empty.')

    alphabet_set = set()

    for letter in key:
        if letter in alphabet_set:
            raise Exception('The secret key field cannot have repeating letters.')

    return True


def book_key_verifier(key):
    if len(key) != BOOK_KEY_LEN:
        raise Exception('The key lehgth is has to be 5.')

    if len(key) == 0:
        raise Exception('The secret book key field cannot be empty.')

    if not all_digits_verifier(key):
        raise Exception('The secret book key field should only contain digits.')


def text_verifier(text):
    if not check_alphabet(text, is_key=False):
        raise Exception('The allowed alphabet consists only of the capital English letters, digits and "/", ".".')

    return True


def cipher_text_verifier(text):
    if not all_digits_verifier:
        raise Exception('The cipher text field should only contain digits.')

    if len(text) % 5 != 0:
        raise Exception('The cipher text field should have length that is a multiple of 5.')


def all_digits_verifier(text):
    for character in text:
        if character not in list(string.digits):
            return False
    return True


def find_index(element, matrix):
    for i in range(MATRIX_ROW_SIZE):
        for j in range(MATRIX_COL_SIZE):
            if matrix[i][j] == element:
                return i, j
