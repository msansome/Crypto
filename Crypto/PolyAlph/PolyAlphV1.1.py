# A Simple implementation of a Polyalphabetic ciper
# using pseudo random number generation
# M Sansome December 2018

from random import randint, seed

def polyalph(text,key,decrypt=False):
    '''Encryption / decryption function:
    Takes parameters "text" (the string to be worked on; "key" (the seed value for
    the random number generator; and "decrypt" (a flag to denote whether we are
    encrypting or decrypting which is set to False (i.e. encrypting) by
    default).'''

    numbersize = 100
    # this is used to pick a random number between 1 and numbersize
    symbs = [ chr(x) for x in range(32,592) if x < 127 or x > 160]
    # Use a list comprehension to create a list of printable symbols from
    # the ASCII table
    SYMBOLS = ''.join(symbs)
    # Convert this list to a (constant) string (for easier processing)
    seed(key)
    # Seed the random number generator with the key to be used using the seed
    # function for the random library
    newText=""
    # Blank output string

    if not decrypt:
        for i in range(0, len(text)):
            pos = SYMBOLS.find(text[i])
            if pos != -1: # The character is not in the alphabet
                # just ignore it (it's probably a control character - e.g. LF)
                newChar = SYMBOLS[(pos + randint(1,numbersize)) % len(SYMBOLS)]
                # Calculate the encrypted character by adding a random mumber
                # and wrap round if necessary
                newText += newChar
                # Add this encrypted characer to the output string
    else:
        # We're decrypting so subtract the key rather than add it.
        for i in range(0, len(text)):
            pos = SYMBOLS.find(text[i])
            newChar = SYMBOLS[(pos - randint(1,numbersize)) % len(SYMBOLS)]
            newText += newChar

    return newText


text = '''Labour's shadow attorney general Nick Thomas-Symonds accused Mr Cox of "hiding" his full legal advice on Theresa May's Brexit deal "for fear of the political consequences".

Mr Cox mounted an impassioned defence of his decision not to publish the full advice, insisting it would not be "in the national interest" to break a longstanding convention that law officers' advice to ministers is confidential. He said he would answer all MPs' questions and there was no cover-up, adding: "There is nothing to see here."

He angrily told MPs calling for it to be published to "grow up and get real", prompting Green MP Caroline Lucas to accuse him of indulging in "amateur dramatics" and turning the debate into a "farce".

Nigel Dodds, leader of the Democratic Unionist Party at Westminster, told Mr Cox MPs needed to see the full legal advice he had given to the government - and denounced the Irish "backstop" plan as "deeply unattractive".'''

mykey = 42

newtxt = polyalph(text,mykey)
print("CiperText")
print(newtxt)
newnewtxt = polyalph(newtxt, mykey, True)
print("Plaintext")
print(newnewtxt)
#print(newnewtxt.count("backstop"))

words = ["the","be","to","of","and","that","have"]
newnewtxt = newnewtxt.lower()

'''This is a way of breaking this cipher using brute force.
We cycle through (in this case 100 - but could be more) keys sequentially and
look at the output to see how often common words such as "the" and "and" appear
in the output. This will always happen by chance but, as you can see, the actual
key used in the encryption (42) scores far higher than any other.
This makes such a cipher trivially easy to crack.'''

for index in range(1,100):
    newnewtxt = polyalph(newtxt, index, True)
    score = 0
    for i in words:
        score += newnewtxt.count(i)
    print(f"Key is {index} Score is: {score}")
    
