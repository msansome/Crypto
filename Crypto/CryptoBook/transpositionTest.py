# Transposition Cipher - Automated Testing
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 114

import random, sys, transpositionEncrypt, transpositionDecrypt

def main():
    random.seed(42) # Set the random "seed" to a static value

    for i in range(20): # Run 20 tests
        # Generate random messages to test:

        # The message will have random length:
        message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * random.randint(4,40)

        # Convert the message string to a list to shuffle it:
        message = list(message)
        random.shuffle(message)
        message = ''.join(message) # Convert the list back to a string.

        print(f'Test No. {i+1}: {message[:50]}...')

        # Check all possible keys for each message:
        for key in range(1, int(len(message)/2)):
            encrypted = transpositionEncrypt.encryptMessage(key, message)
            decrypted = transpositionDecrypt.decryptMessage(key, encrypted)

            # If the decryption doesn't match the original message, display
            # an error message and quit:
            if message != decrypted:
                print(f'Mismatch with key {key} and message {message}.')
                print('Decrypted as:' + decrypted)
                sys.exit()

    print('Transposition cipher test passed.')

# if TranspositionTest.py is run (instead of imported as a module) call
# the main() function:
if __name__ == '__main__':
    main()
