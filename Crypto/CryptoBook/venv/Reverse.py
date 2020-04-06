# Reverse Cipher (simple reversal of string)
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# Cracking Codes Book p. 40


message = 'Three can keep a secret, if two of them are dead.'
message = '.daed era meht fo owt fi ,terces a peek nac eerhT'
translated = ''

i = len(message) -1
while i >= 0:
    translated += message[i]
    i -= 1
print(translated)