# External imports
import string

# Internal imports
from utils import *


class SorgeCipher:
    '''Class containing the Sorge Cipher implementation'''

    def __init__(self, key, book_key, plain_text='', cipher_text=''):
        # Check the given strings
        key_verifier(key)
        book_key_verifier(book_key)
        text_verifier(plain_text)
        cipher_text_verifier(cipher_text)

        # Save the key & plain_text or key & cipher_text
        self.key = key
        self.plain_text = plain_text
        self.cipher_text = cipher_text

        # Generate the matrix
        self.matrix = self.generate_matrix()

        # Generate the mappings
        self.mappings = self.generate_mapping()

        # Create the plain text pairs if needed
        # self.plain_pairs = self._seperate_letters(self.plain_text)

        # Create the cipher text pairs if needed
        # self.cipher_pairs = self._seperate_letters(self.cipher_text)

        # Set the encryption flag to True
        self.encrypt_flag = True

    def generate_matrix(self):
        # Create an empty matrix
        matrix = []

        # Create helper alphabet
        alphabet = list(string.ascii_uppercase)
        alphabet.append('.')
        alphabet.append('/')

        # Create index variable for the alphabet
        idx_alphabet = 0

        # Fill the matrix
        for i in range(MATRIX_ROW_SIZE):
            row = []
            for j in range(MATRIX_COL_SIZE):
                if i == 0:
                    row.append(self.key[j])
                    alphabet.remove(self.key[j])
                else:
                    if idx_alphabet != len(alphabet):
                        row.append(alphabet[idx_alphabet])
                        idx_alphabet += 1
                    else:
                        row.append(None)
            matrix.append(row)

        # Return the filled matrix
        return matrix

    def generate_mapping(self):
        letter_mapping = {}

        for idx in range(len(COMMON_LETTERS)):
            letter_mapping[COMMON_LETTERS[idx]] = str(idx)

        letter_idx = 80

        for i in range(MATRIX_COL_SIZE):
            for j in range(MATRIX_ROW_SIZE):
                if self.matrix[j][i] not in letter_mapping.keys() and self.matrix[j][i] is not None:
                    letter_mapping[self.matrix[j][i]] = str(letter_idx)
                    letter_idx += 1

        return letter_mapping

    def _seperate_letters(self, text):
        # Split the plain text into list of characters
        text_list = list(text)

        # Add bogus letter where needed
        for idx in range(len(text_list) - 1):
            if text_list[idx] == text_list[idx + 1] and idx % 2 == 0:
                text_list.insert(idx + 1, BOGUS_LETTER)

        # Fill the last element when needed
        if len(text_list) % 2 != 0:
            if text_list[-1] != FILLER_LETTER:
                text_list.append(FILLER_LETTER)
            else:
                text_list.append(BOGUS_LETTER)

        # Create the pairs
        first_elements = text_list[::2]
        second_elements = text_list[1::2]

        pairs = [[first_elements[i], second_elements[i]] for i in range(len(first_elements))]

        # Return the list of pairs
        return pairs

    # def encrypt_decrypt_cases(self, pair):
    #     # Find the indexes in the matrix
    #     e1_x, e1_y = find_index(pair[0], self.matrix)
    #     e2_x, e2_y = find_index(pair[1], self.matrix)

    #     # Checks based on the rules
    #     if e1_x == e2_x:
    #         new_pair = self._encrypt_decrypt_row(e1_x, e1_y, e2_x, e2_y)
    #     elif e1_y == e2_y:
    #         new_pair = self._encrypt_decrypt_col(e1_x, e1_y, e2_x, e2_y)
    #     else:
    #         new_pair = self._encrypt_decrypt_rec(e1_x, e1_y, e2_x, e2_y)

    #     return new_pair

    def encrypt(self):
        self.encrypt_flag = True
        self.cipher_text = ''
        self.cipher_pairs = []

        # Variable to help with the duplication
        inside_numbers = False

        # Go through all of the characters and map
        for character in self.plain_text:
            if inside_numbers and character in string.digits:
                self.cipher_text += character * 2
            else:
                self.cipher_text += self.mappings[character]

            if character == '/' and not inside_numbers:
                inside_numbers = True
            elif character == '/' and inside_numbers:
                inside_numbers = False

        # Check if additional zeros are needed
        fill_zeros = len(self.cipher_text) % 5

        # Fill with zeros if needed
        for i in range(5 - fill_zeros):
            self.cipher_text += '0'

        # Split the list into chunks of size 5
        self.cipher_pairs = [self.cipher_text[i:i + 5] for i in range(0, len(self.cipher_text), 5)]

        # Additional encrypting by the book method
        # TODO:!!!

        return self.cipher_text

    def decrypt(self):
        self.encrypt_flag = False
        self.plain_text = ''
        self.plain_pairs = []

        for pair in self.cipher_pairs:
            # Append the plain pair
            self.plain_pairs.append(self.encrypt_decrypt_cases(pair))

        # Create a string out of the pairs
        self._fill_plain_cipher_text()

        return self.plain_text

    # def _encrypt_decrypt_col(self, e1_x, e1_y, e2_x, e2_y):
    #     # Create an empty list
    #     pair = []

    #     if self.encrypt_flag:
    #         pair.append(self.matrix[(e1_x + 1) % 5][e1_y])
    #         pair.append(self.matrix[(e2_x + 1) % 5][e2_y])
    #     else:
    #         pair.append(self.matrix[(e1_x - 1) % 5][e1_y])
    #         pair.append(self.matrix[(e2_x - 1) % 5][e2_y])

    #     return pair

    # def _encrypt_decrypt_row(self, e1_x, e1_y, e2_x, e2_y):
    #     # Create an empty list
    #     pair = []

    #     if self.encrypt_flag:
    #         pair.append(self.matrix[e1_x][(e1_y + 1) % 5])
    #         pair.append(self.matrix[e2_x][(e2_y + 1) % 5])
    #     else:
    #         pair.append(self.matrix[e1_x][(e1_y - 1) % 5])
    #         pair.append(self.matrix[e2_x][(e2_y - 1) % 5])

    #     # Return the pair
    #     return pair

    # def _encrypt_decrypt_rec(self, e1_x, e1_y, e2_x, e2_y):
    #     return [self.matrix[e1_x][e2_y], self.matrix[e2_x][e1_y]]

    def _fill_plain_cipher_text(self):
        if self.encrypt_flag:
            # Fill the cipher_text variable
            for pair in self.cipher_pairs:
                self.cipher_text += pair[0] + pair[1]
        else:
            for pair in self.plain_pairs:
                self.plain_text += pair[0] + pair[1]

sorge = SorgeCipher(key='SUNDAY', plain_text='PGP.VERSION/2.6.3/IREADMEFIRSTAPRIL/1996.')
print(sorge.matrix)
print(sorge.mappings)
print(sorge.plain_text)
helper=sorge.encrypt()
print(sorge.cipher_pairs)

#81948 18996 05763 49322 89668 93393 65029 09509 16571 28156 92931 19999 66890
#81948 18996 05763 49322 89668 93393 65029 09509 16571 28156 92931 19999 66890000