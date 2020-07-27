# Public Key Cipher
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

# A modified version which uses the ASCII character set (and allows
# file entry for plaintext)

import sys
import math

# The public and private keys for this program are created by
# the makePublicPrivateKeys.py program.
# This program must remain in the same folder as the key files.

symbol_set_size = 256


def main():
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    import_filename = 'test.txt'
    filename = 'encrypted_file.txt'  # The file to write to/read from.
    mode = 'encrypt'  # Set to either 'encrypt' or 'decrypt'.

    with open(import_filename, 'r') as handle:
        message = handle.read()
        print(message)

    if mode == 'encrypt':
        # message = 'Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets. Gerald Priestland. The Founding fathers gave the free press the protection it must have to bare the secrets of government and inform the people. Hugo Black.'
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
    # if not message.isascii():
    #     sys.exit('ERROR: The text contains non alphanumeric data!')
    try:
        message.encode('ascii')
    except UnicodeEncodeError:
        sys.exit('ERROR: The text contains non alphanumeric data!')
    blockInts = []
    for blockStart in range(0, len(message), blockSize):
        # Calculate the block integer for this block of text.
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize,
                                       len(message))):
            blockInt += (ord(message[i])) * \
                (symbol_set_size ** (i % blockSize))
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
                charIndex = blockInt // (symbol_set_size ** i)
                blockInt = blockInt % (symbol_set_size ** i)
                blockMessage.insert(0, chr(charIndex))
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
        blockSize = int(math.log(2 ** keySize, symbol_set_size))
    # Check that key size is large enough for the block size:
    if not (math.log(2 ** keySize, symbol_set_size) >= blockSize):
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
    if not (math.log(2 ** keySize, symbol_set_size) >= blockSize):
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
