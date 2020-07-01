# Transposition File Cipher - Encrypt / Decrypt Files
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 129

import time, os, sys, transpositionEncrypt, transpositionDecrypt

def main():
    inputFilename = 'frankenstein.txt'
    # BE CAREFUL! If a file with the outputFilename name already exists,
    # this program will overwrite that file:
    outputFilename = 'frankenstein.encrypted.txt'
    myKey = 10
    myMode = 'encrypt' # Set to 'encrypt' or 'decrypt'.

    # If the input filename does not exist, the program terminates early:
    if not os.path.exists(inputFilename):
        print(f'The file {inputFilename} does not exist. Quitting...')
        sys.exit()

    # If the output file already exists, give the user a chance to quit:
    if os.path.exists(outputFilename):
        print(f'This will overwrite the file {outputFilename}. (C)ontinue or (Q)uit?')
        response = input('> ')
        if not response.lower().startswith('c'):
            sys.exit()

    # Read in the message from the input file
    fileObj = open(inputFilename)
    content = fileObj.read()
    fileObj.close()

    print(f'{myMode.title()}ing {inputFilename}...')

    # Measure how long the encryption / decryption takes:
    startTime = time.time()
    if myMode == 'encrypt':
        translated = transpositionEncrypt.encryptMessage(myKey, content)
    elif myMode == 'decrypt':
        translated = transpositionDecrypt.decryptMessage(myKey, content)
    totalTime = round(time.time() - startTime, 2)
    print(f'{myMode.title()}ion time: {totalTime} seconds')

    # Write out the translated message to the output file:
    outputFileObj = open(outputFilename,'w')
    outputFileObj.write(translated)
    outputFileObj.close()

    print(f'Done {myMode}ing {inputFilename} ({len(content)} characters)')
    print(f'{myMode.title()}ed file is "{outputFilename}".')


# if TranspositionFileCipher.py is run (instead of imported as a module) call
# the main() function:
if __name__ == '__main__':
    main()
