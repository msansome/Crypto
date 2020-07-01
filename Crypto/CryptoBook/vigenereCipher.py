# Vigenere Cipher (Polyalphabetic Substitution Cipher)
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 251

import pyperclip

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    myMessage = '''Alan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist.'''
    myKey = 'ASIMOV'
    myMode = 'encrypt' # Set to either 'encrypt' or 'decrypt'.

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print(f'{myMode.title()}ed message:')
    print(translated)
    pyperclip.copy(translated)
    print()
    print('The message has been copied to the clipboard.')


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = [] # Stores the encrypted/decrypted message string.

    keyIndex = 0
    key = key.upper()

    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1: # -1 means symbol.upper() was not found in LETTERS.
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex]) # Add if encrypting
            elif mode == 'decrypt': # Subtract if decrypting
                num -= LETTERS.find(key[keyIndex])  # Subtract if decrypting


            num %= len(LETTERS) # Handle any wraparound

            # Add the encrypted/decrypted symbol to the end of translated:
            if symbol.isupper():
                translated.append(LETTERS[num].upper())
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            keyIndex += 1 # Move to the next letter in the key.
            if keyIndex == len(key):
                keyIndex = 0

        else:
            # Append the symbol without encrypting/decrypting
            translated.append(symbol)
    return ''.join(translated)

if __name__ == '__main__':
    main()

