# des.py

from constans import *


def permutation(str_, filter_):
    """ make permutations"""
    return "".join([str_[i - 1] for i in filter_])


def left_circular_shift(str_):
    """ left shift 1 bit """
    return str_[1:] + str_[0]


def divide(str_):
    """ divide into 2 array """
    return str_[:len(str_) // 2], str_[len(str_) // 2:]


def binary_to_hex(*args):
    """ bin to hex """
    return "".join([f"{int(arg, 2):x}" for arg in args])


def string_to_binary(args):
    """ string to bin """
    return "".join(format(ord(arg), '08b') for arg in args)


def hex_to_binary(args):
    """ hex to bin """
    return "".join(format(int(arg, 16), '04b') for arg in args)


def bin_to_string(*args):
    """ bin to string """
    array8bits = [("".join(args))[index: index + 8] for index in range(0, len(("".join(args))), 8)]
    while '00000000' in array8bits: array8bits.remove('00000000')
    return "".join([chr(int(binary, 2)) for binary in array8bits])


def isASCII(text):
    """ checks if all characters are from an ASCII table """
    return all(31 < ord(c) < 128 for c in text)


def add_pads(s):
    """ adding bits to make an string of 64-bit blocks """
    number_of_vacancy = len(s) % 64
    need_pads = number_of_vacancy > 0
    if need_pads:
        for i in range(64 - number_of_vacancy):
            s += "0"
    return s


def xor(str_1, str_2):
    """ xor """
    str_1 = [int(item) for item in str_1]
    str_2 = [int(item) for item in str_2]

    # implementing xor formula
    result = [(bit_1 and not bit_2) or (not bit_1 and bit_2) for bit_1, bit_2 in zip(str_1, str_2)]

    result = "".join([str(int(item)) for item in result])
    return result


def transform(str_, row_len):
    """ splits one-line string into a list of strings """
    matrix = []
    tmp = ""
    for index, item in enumerate(str_):
        tmp += item
        if index != 0 and (index + 1) % row_len == 0:
            matrix.append(tmp)
            tmp = ""
    return matrix


def s_boxing(*args):
    """ transforms 6bit rows into 4bit rows """
    values = []
    for s_box_num, arg in enumerate(args):
        row = arg[0] + arg[-1]
        row = int(row, 2)

        column = arg[1:-1]
        column = int(column, 2)

        values.append(S_BOXES[s_box_num][row][column])

    return "".join([f"{value:04b}" for value in values])


def one_round(l_in_, r_in_, k_):
    # e-bit selection for r_in
    r_out = permutation(r_in_, BIT_SELECTION)

    # xor R with sub key
    r_out = xor(r_out, k_)

    # 6bit rows to 4bit
    r_out = s_boxing(*(transform(r_out, 6)))

    # permutation
    r_out = permutation(r_out, PERMUTATNION)

    # xor left and right
    r_out = xor(l_in_, r_out)
    return r_in_, r_out


def generate_keys(c, d):
    """ generate keys"""
    sub_keys = []
    for round_number in range(16):
        c, d = left_circular_shift(c), left_circular_shift(d)
        if round_number not in [0, 1, 8, 15]:
            c, d = left_circular_shift(c), left_circular_shift(d)
        sub_keys.append(permutation(c + d, PC2))
    return sub_keys


def encrypt(message, key):
    """ encryptor """
    # ONE - convert message and key to binary string
    message = string_to_binary(message)
    message = add_pads(message)
    key = string_to_binary(key)

    # TWO - apply initial permutation to the message
    message = permutation(message, IP)

    # THREE - apply permuted choice 1 (PC-1) to the key
    key = permutation(key, PC1)
    c, d = divide(key)

    # FOUR - generate 16 sub keys
    sub_keys = generate_keys(c, d)

    # FIVE - encode each block of the data
    l_in, r_in = divide(message)
    for round_num in range(16):
        l_in, r_in = one_round(l_in, r_in, sub_keys[round_num])

    # SIX - apply final permutation
    result = permutation(r_in + l_in, IP_REVERSED)
    result = transform(result, 4)
    result = binary_to_hex(*result)
    return result


def decrypt(message, key):
    """ decryptor """
    # ONE - convert message and key to binary string
    message = hex_to_binary(message)
    message = add_pads(message)
    key = string_to_binary(key)

    # TWO - apply initial permutation to the message
    message = permutation(message, IP)

    # THREE - apply permuted choice 1 (PC-1) to the key
    key = permutation(key, PC1)
    c, d = divide(key)

    # FOUR - generate 16 sub keys
    sub_keys = generate_keys(c, d)

    sub_keys.reverse()

    # FIVE - encode each block of the data
    l_in, r_in = divide(message)
    for round_num in range(16):
        l_in, r_in = one_round(l_in, r_in, sub_keys[round_num])

    # SIX - apply final permutation
    result = permutation(r_in + l_in, IP_REVERSED)
    result = transform(result, 4)
    result = bin_to_string(*result)
    return result
