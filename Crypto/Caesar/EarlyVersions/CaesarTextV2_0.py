# A Simple implementation of the Caesar Cipher
# M Sansome March 2018



def caesar(text,key,decrypt = False):
    # The main Caesar Cipher encryption / decryption function
    SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.upper()
    newText=""

    if decrypt:
        key = -key
    for i in range(0, len(text)):
        pos = SYMBOLS.find(text[i])
        if pos == -1: # The character is not in the alphabet, leave it as it is
            newChar = text[i]
        else:
            newChar = SYMBOLS[(pos + key) % len(SYMBOLS)]
            if decrypt:
                newChar = newChar.lower()
        newText += newChar  
        #print(text[i], ord(text[i]), cipherChar)
    return newText

def bruteForce(text):
    # This function will print a short extract of all possible 25 keys used
    # and leave the user to select the appropriate key
    screenWidth = 78
    if len(text) > screenWidth:
        shortText = text[:screenWidth]
    else:
        shortText = text[:]
            
    for i in range(1,26):
        print(i,":",caesar(shortText,i,True))

def automated_bruteForce(txt):
    # This function will attempt to find the key using analysis of the decrypted
    # text 
    words = ["the","be","to","of","and","that","have","you"]
    topscore = 0

    for index in range(1,26):
        newtxt = caesar(txt, index, True)
        score = 0
        for i in words:
            score += newtxt.count(i)
        #print(f"Key is {index} Score is: {score}")
        if score > topscore:
            topscore = score
            ky = index
    return ky
    
    

def load_file():
    # Fuction to load the cyphertext from a text file
    while True:
        fname = input("Pleae enter filename of file to be decrypted: ")
        try:
            with open(fname, 'r') as file: # Use file to refer to the file object
                txt = file.read()
                return txt
        except FileNotFoundError:
            print("Sorry",fname,"does not exist. Please try again")
        

################################################################
########                                                ########
########          Main Program Starts Here              ########
########                                                ########        
################################################################

def main():
    typed_text = False
    load_from_file = False
    
    entry = input("Do you want to Type Some text to decrypt(T) or Load from File(F)?: ")
    while entry.upper() != "T" and entry.upper() != "F":
        entry = input("Please enter(T) to type text or (F) to Load from File: ")
    if entry.upper() == "T":
        typed_text = True
    if entry.upper() == "F":
        load_from_file = True   

    if typed_text:
        txt = input("Please enter some text: ")
    if load_from_file:
        txt = load_file()

    mode = input("Do you want to use Manual(M) or Automatic(A) decryption?: ")
    # We will assume that unless the user wants (A)utomatic decryption the default
    # will be (M)anual
    if mode.upper() == "A":
        key = automated_bruteForce(txt) # Call the automated cracking function
        print("\nThe Key used was", key)
    else:
        bruteForce(txt) # Call the manual brute force function
        key = int(input("\nWhich key do you want to use? "))

    print()
    print(caesar(txt,key,True))
    print()
         

        
if __name__ == "__main__":
    main()
    
