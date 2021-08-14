# This code is written by Nicky Ru
from re import match

from des import *
from generator import *
import os

video = Video(VIDEO_FILE)
trng = Generator(video, RESULT_OUTPUT)

if __name__ == '__main__':
    print("Welcome to the best DES encrypter/decrypter ever")

    while True:
        action = input("\nWhat you want to do\n1. Encrypt \n2. Decrypt \n")
        if not ((action.isdigit()) and (action in ["1", "2"])):
            print("\nYou selected an option out of range")
        else:
            break

    while True:
        message = input("\nEnter your message (Only ASCII): ")
        if not (isASCII(message)):
            print("\nThere are non-ASCII characters in your message")
        else:
            break

    while True:
        type_key = input("\nChoose: \n1. Enter your key \n2. Generate a key\n")
        key = ""
        if not ((type_key.isdigit()) and (type_key in ["1", "2"])):
            print("\nYou selected an option out of range")
        else:
            while True:
                if type_key == "1":
                    while True:
                        key = input("\nEnter your key (Only 8-chars ASCII)")
                        if not (isASCII(key) and len(key) == 8):
                            print("\nYou have entered an invalid key")
                            print(len(key))
                            print(isASCII(key))
                        else:
                            print(len(key))
                            print(isASCII(key))
                            break
                    break
                elif type_key == "2":
                    for i in range(8):
                        tmp_value = (trng.next() / (256 / 126) / (126 / 94)) + 32  # cast to ASCII range
                        key += chr(round(tmp_value))
                    print("\nThe generated key is: " + key)
                    break
        break

    result = ''
    if action == '1':
        result = encrypt(message, key)
        print("\nEncrypted message: " + result)
    elif action == '2':
        result = decrypt(message, key)
        print("Decrypted message: " + result)
