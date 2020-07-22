# Public Key Generator
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import random
import sys
import os
import primeNum
import cryptomath


def main():
    # Create a public/private keypair with 1024-bit keys:
    print('Making key files...')
    makeKeyFiles('m_sansome', 1024)
    print('Key files made.')


def generateKey(keySize):
    # Creates public/private keys keySize bits in size.
    p = 0
    q = 0
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q:
    print('Generating p & q prime...')
    while p == q:
        p = primeNum.generateLargePrime(keySize)
        q = primeNum.generateLargePrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1):
    print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Keep trying random numbers for e until one is valid:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e:
    print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    print('Public Key:', publicKey)
    print('Private Key:', privateKey)

    return (publicKey, privateKey)


def makeKeyFiles(name, keySize):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x
    # is the value in name) with the n,e and d,e integers written in
    # them, delimited by a comma.

    # Our safety check will prevent us from overwriting our old key files:
    if os.path.exists(f'{name}_pubkey.txt') or os.path.exists(f'{name}_privkey.txt'):
        sys.exit(
            f'WARNING: the file {name}_pubkey.txt or {name}_privkey.txt already exists! '
            'Use a different name or delete these files and return to this program.')

    publicKey, privateKey = generateKey(keySize)

    print()
    print(
        f'The public key is a {len(str(publicKey[0]))} and '
        'a {len(str(publicKey[1]))} digit number.')
    print(f'Writing public key to file as {name}_pubkey.txt...')
    with open(f'{name}_pubkey.txt', 'w') as handle:
        handle.write(f'{keySize},{publicKey[0]},{publicKey[1]}')

    print()
    print(
        f'The private key is a {len(str(privateKey[0]))} and '
        'a {len(str(privateKey[1]))} digit number.')
    print(f'Writing private key to file as {name}_privkey.txt...')
    with open(f'{name}_privkey.txt', 'w') as handle:
        handle.write(f'{keySize},{privateKey[0]},{privateKey[1]}')


if __name__ == '__main__':
    main()
