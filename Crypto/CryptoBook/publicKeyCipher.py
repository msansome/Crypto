# Public Key Cipher
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import sys
import math

# The public and private keys for this program are created by
# the makePublicPrivateKeys.py program.
# This program must remain in the same folder as the key files.

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'


def main():
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    filename = 'encrypted_file.txt'  # The file to write to/read from.
    mode = 'decrypt'  # Set to either 'encrypt' or 'decrypt'.

    if mode == 'encrypt':
        message = 'Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets. Gerald Priestland. The Founding fathers gave the free press the protection it must have to bare the secrets of government and inform the people. Hugo Black.'
        pubkeyFilename = 'm_sansome_pubkey.txt'
        print(f'Encrypting and writing to {filename}')
        encrypedText = encryptAndWriteToFile(filename, pubkeyFilename,
                                             message)

        print('Encrypted text:')
        print(encrypedText)

    elif mode == 'decrypt':
        privKeyFilename = 'm_sansome_privkey.txt'
        print(f'Reading from {filename} and decrypting...')
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

        print('Decrypted text:')
        print(decryptedText)


def getBlocksFromText(message, blockSize):
    # Converts a string message to a list of block integers.
    for character in message:
        if character not in SYMBOLS:
            print(f'ERROR: The symbol set does not have the character '
                  '{character}.')
            sys.exit
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        # Calculate the block integer for this block of text.
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize,
                                       len(message))):
            blockInt += (SYMBOLS.index(message[i])) * \
                (len(SYMBOLS) ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last block
    # integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Decode the message string for the first 128 (or whatever
                # blockSize is set to) characters from this block integer:
                charIndex = blockInt // (len(SYMBOLS) ** i)
                blockInt = blockInt % (len(SYMBOLS) ** i)
                blockMessage.insert(0, SYMBOLS[charIndex])
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encrypedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        encrypedBlocks.append(pow(block, e, n))
    return encrypedBlocks


def decryptMessage(encrypedBlocks, messageLength, key, blockSize):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encrypedBlocks:
        # plaintext = cipherText ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n, e) or (n, d) tuple value.
    with open(keyFilename, 'r') as handle:
        content = handle.read()
    keySize, n, eORd = content.split(',')
    return (int(keySize), int(n), int(eORd))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=None):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keySize, n, e = readKeyFile(keyFilename)
    if blockSize is None:
        # If blockSize isn't given, set it to the largest size allowed by the
        # key size and and symbol set size.
        blockSize = int(math.log(2 ** keySize, len(SYMBOLS)))
    # Check that key size is large enough for the block size:
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit(f'ERROR: Block size is too large for the key and symbol '
                 'set size. Did you specify the correct key file and encrypted '
                 ' file?')
    # Encrypt the message:
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # Convert the large int vlaues to one string value:
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # Write ou the encrypted string to the output file:
    encryptedContent = f'{len(message)}_{blockSize}_{encryptedContent}'
    with open(messageFilename, 'w') as handle:
        handle.write(encryptedContent)
    # Also return the encrypted string:
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keySize, n, d = readKeyFile(keyFilename)

    # Read in the message length and the encrypted message from the file:
    with open(messageFilename, 'r') as handle:
        content = handle.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # Check that key size is large enough for the block size:
    if not (math.log(2 ** keySize, len(SYMBOLS)) >= blockSize):
        sys.exit(f'ERROR: Block size is too large for the key and symbol set '
                 'size. Did you specify the correct key file and encrypted file?')

    # Convert the encrypted message into large int values:
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    # Decrypt the large int values:
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


if __name__ == '__main__':
    main()
