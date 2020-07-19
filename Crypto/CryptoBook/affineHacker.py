# Affine Cipher
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 198

import pyperclip, affineCipher, detectEnglish, cryptomath

SILENT_MODE = False

def main():
    # From source code at https://www.nostarch.com/crackingcodes/
    myMessage = """"5QG9ol3La6QI93!xQxaia6faQL9QdaQG1!!axQARLa!!AuaRLQADQALQG93!xQxaGaAfaQ1QX3o1RQARL9Qda!AafARuQLX1LQALQI1iQX3o1RN"Q-5!1RQP36ARu"""

    hackedMessage = hackAffine(myMessage)

    if hackedMessage != None:
        # The plaintext is displayed on the screen. For the convenience of
        # the user, we copy the text of the code to the clipboard:
        print('Copying cracked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to find encryption key.')


def hackAffine(message):
    print('Attempting decryption...')

    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')

    # Brute-force by looping through every possible key:
    for key in range(len(affineCipher.SYMBOLS)**2):
        keyA = affineCipher.getKeyParts(key)[0]
        if cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) != 1:
            continue

        decryptedText = affineCipher.decryptMessage(key, message)
        if not SILENT_MODE:
            print(f'Tried Key {key}... ({decryptedText[:40]})')

        if detectEnglish.isEnglish(decryptedText):
            # Check with the user if the decryption key has been found:
            print()
            print('Possible decryption key:')
            print(f'Key: {key}')
            print('Decrypted message: ' + decryptedText[:200])
            print()
            print('Enter D for done, or any other key to continue trying:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText
    return  None

if __name__ == '__main__':
    main()
