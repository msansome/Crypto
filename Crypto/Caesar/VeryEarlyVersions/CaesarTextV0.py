# A Simple implementation of the Caesar Cipher
# M Sansome March 2018



def caesar(text,key):
    SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.upper()
    newText=""
    
    for i in range(0, len(text)):
        pos = SYMBOLS.find(text[i])
        if pos == -1: # The character is not in the alphabet, leave it as it is
            newChar = text[i]
        else:
            newChar = SYMBOLS[(pos + key) % len(SYMBOLS)]
        newText += newChar  
        #print(text[i], ord(text[i]), cipherChar)
    return newText

txt = input("Please enter some text: ")
ky = int(input("Please enter a key: "))

newtxt = caesar(txt,ky)

print(newtxt)
