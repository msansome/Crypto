# Affine Cipher
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 186

import sys, pyperclip, cryptomath, random
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

def main():
    myMessage = '''"A computer would deserve to be called intelligent if it could deceive a human into believing that it was human." - Alan Turing'''
    #myMessage = '''"5QG9ol3La6QI93!xQxaia6faQL9QdaQG1!!axQARLa!!AuaRLQADQALQG93!xQxaGaAfaQ1QX3o1RQARL9Qda!AafARuQLX1LQALQI1iQX3o1RN"Q-Q5!1RQP36ARu'''
    myKey = 2894
    myMode = 'encrypt' # Set to either 'encrypt' or 'decrypt'.

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)
    print(f'Key: {myKey}')
    print(f'{myMode.title()}ed text:')
    print(translated)
    pyperclip.copy(translated)
    print(f'Full {myMode}ed text copied to clipboard.')


def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)


def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        sys.exit('Cipher is weak if Key A is 1. Please choose a different key.')
    if keyB == 0 and mode == 'encrypt':
        sys.exit('Cipher is weak if Key B is 0. Please choose a different key.')
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS)-1:
        sys.exit(f'Key A must be greater than 0 and Key B must be between 0 and {len(SYMBOLS)-1}')
    if cryptomath.gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit(f'Key A ({keyA}) and the symbols set size ({len(SYMBOLS)}) are not relatively prime. Please choose a different key.')


def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    ciphertext = ''
    for symbol in message:
        if symbol in SYMBOLS:
            # Encrypt the symbol:
            symbolIndex = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symbolIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += symbol # Append the symbol without encrypting:
    return ciphertext


def decryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plaintext = ''
    modInverseOfKeyA = cryptomath.findModInverse(keyA, len(SYMBOLS))

    for symbol in message:
        if symbol in SYMBOLS:
            # Decrypt the symbol:
            symbolIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symbolIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol # Append the symbol without decrypting:
    return plaintext


def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if cryptomath.gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB


if __name__ == '__main__':
    main()