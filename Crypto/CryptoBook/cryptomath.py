# Cryptomath Module
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 182

def gcd(a,b):
    # Return the GCD of a and b using Euclid's Algorithm:
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a,m):
    # Using Euclid's Extended Algorithm
    # Return the modular inverse of a % m, which is
    # the number x such that a*x % m =1.

    if gcd(a, m) != 1:
        return None # No mod inverse if a & m aren't relatively prime.

    # Calculate using the extended Euclidean algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # Integer division
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m
