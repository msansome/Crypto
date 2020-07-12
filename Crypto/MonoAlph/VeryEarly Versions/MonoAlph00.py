# M Sansome
# May 2019

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from CryptanalysisV01 import Cryptanalise
# Use my Cryptanalyse class which provides some basic funtionality

def instructions():
    insts = '''
This program will help to decrypt a simple monoalphabetic substitution cipher.
Start by typing (or pasting) the ciphertext to be decrypted at the prompt (if you
enter nothing the ciphertext from Simon Singh's Code Book challenge 1 will be used
for practice).
It will then display the first few lines of the ciphertext (usually enough to get
started).
At the prompt, type in two letters - the fist being the ciphertext character you wish to identify, the second being the plaintext letter you think it represents.
When you have all the letters of the alphabet the program will end and display the
full ciphertext.
If you have finished without finding all the letters of the alphabet press enter
without a typing to end.
To display these instructions again, type &&.
To show the frequencies again type !!
To show the alphabet type @@
'''
    print(insts)


def init_alphabet(alph = "abcdefghijklmnopqrstuvwxyz"):
    alphabet = {}
    ''' This function will intitialse the alphabet dictionary with a "*"
        for every letter. Later the "*" will be replaced with a plaintext
        alphabet letter.'''
    for i in alph:
        alphabet[i] = "*"
    return alphabet
  
def print_text(ciphertext, alphabet):
    ''' This will print the ciphertext and then the plaintext (as it is currently
        understood to be according to the alphabet key.'''
    maxshow = 250 # The first part of the ciphertext (enough to examine)
    plaintext =""
    
    # Print the ciphertext
    print()
    if len(ciphertext)<maxshow:
        maxshow = len(ciphertext)
    short_ciphertext = ciphertext[0:maxshow]
    # Print the first part of the ciphertext (enough to examine)
    print(short_ciphertext)
        
    # Print the plaintext (as far as we have decryped it)
    print()
    for i in range(0,maxshow):
        if ciphertext[i].lower() in alphabet:
            # (spaces and punctuation aren't stored in the dictionary)
            plaintext += alphabet[ciphertext[i].lower()]
        else:
            plaintext += ciphertext[i]
    print(plaintext)
    print()

def modify_alphabet(c,p):
    if p == '*':
        alphabet[c] = p
    elif p not in alphabet.values():
        alphabet[c] = p
    else:
        print(f"Wait! you've already got {p} in the alphabet")
    if '*' not in alphabet.values():
        print("\nYou have completed the cipher alphabet\n")
        show_full_text()
        
    
def get_substitution():
    try:
        c,p = input('Please enter in the form "cp" where "c" is the ciphertext letter and "p" is the plaintext letter: ')
        if c=="!" and p=="!":
            print()
            mytry.print_freqs()
        if c=="&" and p=="&":
            print()
            instructions()
        if c=="@" and p=="@":
            print()
            print(alphabet)
        else:
            modify_alphabet(c,p)
    except ValueError:
        
        show_full_text()
        

def show_full_text():
    full = input("Do you want to see the full plaintext? (Y/N): ")
    if full.lower() == "y":
        print()
        print(ciphertext)
        print()
        plaintext =""
        for i in range(0,len(ciphertext)):
            if ciphertext[i].lower() in alphabet:
                # (spaces and punctuation aren't stored in the dictionary)
                plaintext += alphabet[ciphertext[i].lower()]
            else:
                plaintext += ciphertext[i]
        print(plaintext)
    end = input("Do you want to end? (Y/N): ")
    if end.lower() == "y":
        print("\nThe alphabet used was:\n",alphabet)
        raise SystemExit


# Main Program Starts Here
# ========================

instructions()

default_ciphertext = '''BT JPX RMLX PCUV AMLX ICVJP IBTWXVR CI M LMT’R PMTN, MTN YVCJX CDXV MWMBTRJ JPX AMTNGXRJBAH UQCT JPX QGMRJXV CI JPX YMGG CI JPX HBTW’R QMGMAX; MTN JPX HBTW RMY JPX QMVJ CI JPX PMTN JPMJ YVCJX. JPXT JPX HBTW’R ACUTJXTMTAX YMR APMTWXN, MTN PBR JPCUWPJR JVCUFGXN PBL, RC JPMJ JPX SCBTJR CI PBR GCBTR YXVX GCCRXN, MTN PBR HTXXR RLCJX CTX MWMBTRJ MTCJPXV. JPX HBTW AVBXN MGCUN JC FVBTW BT JPX MRJVCGCWXVR, JPX APMGNXMTR, MTN JPX RCCJPRMEXVR. MTN JPX HBTW RQMHX, MTN RMBN JC JPX YBRX LXT CI FMFEGCT, YPCRCXDXV RPMGG VXMN JPBR YVBJBTW, MTN RPCY LX JPX BTJXVQVXJMJBCT JPXVXCI, RPMGG FX AGCJPXN YBJP RAM'''

ciphertext = input("Please type or paste the ciphertext to be decrypted (blank = practise text): ")
if ciphertext == "":
    ciphertext = default_ciphertext

mytry = Cryptanalise(ciphertext)# Instantiate a cryptanalise object
mytry.print_freqs() # Use the object to find the letter frequencies
mytry.print_doubles() # Use the object to find the double letters 
alphabet = init_alphabet() # Initialise the alphabet dictionary

# Run the program...
while True:
	print_text(ciphertext,alphabet)
	get_substitution()
