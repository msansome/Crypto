# Transposition Cipher - Brute Force cracking tool
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 162

import pyperclip, detectEnglish, transpositionDecrypt

def main():
    # Text copied from the source code at https://www.nostarch.com/crackingcodes/:
    myMessage = myMessage = """AaKoosoeDe5 b5sn ma reno ora'lhlrrceey e  enlh na  indeit n uhoretrm au ieu v er Ne2 gmanw,forwnlbsya apor tE.no euarisfatt  e mealefedhsppmgAnlnoe(c -or)alat r lw o eb  nglom,Ain one dtes ilhetcdba. t tg eturmudg,tfl1e1 v  nitiaicynhrCsaemie-sp ncgHt nie cetrgmnoa yc r,ieaa  toesa- e a0m82e1w shcnth  ekh gaecnpeutaaieetgn iodhso d ro hAe snrsfcegrt NCsLc b17m8aEheideikfr aBercaeu thllnrshicwsg etriebruaisss  d iorr."""

    hackedMessage = hackTransposition(myMessage)

    if hackedMessage == None:
        print('Failed to crack the encryption')
    else:
        print('Copying cracked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)


def hackTransposition(message):
    print('Cracking....')
    print('(Press Ctrl-C (on Windows) or Ctrl-D (on MacOS and Linux) to quit at any time.)')

    # Brute-force by looping through every possible key:
    for key in range(1, len(message)):
        print(f'Trying key #{key}...')

        decryptedText = transpositionDecrypt.decryptMessage(key, message)

        if detectEnglish.isEnglish(decryptedText):
            # Ask user if this is the correct decryption:
            print()
            print('Possible decryption:')
            print(f'Key {key}: {decryptedText[:100]}')
            print()
            print('Enter D if done, anything else to continue trying:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    return  None

if __name__ == '__main__':
    main()