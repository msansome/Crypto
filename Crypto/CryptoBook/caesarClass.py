class Caesar():

    def __init__(self, message='', key=0, extended_symbol_set=False):
        self.message = message
        self.key = key
        self.extended_symbol_set = extended_symbol_set
        self.EXT_SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'
        self.BASIC_SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if extended_symbol_set:
            self.SYMBOLS = self.EXT_SYMBOLS
        else:
            self.SYMBOLS = self.BASIC_SYMBOLS
        self.symb_size = len(self.SYMBOLS)
        self.opCode = '+'

    def translate(self):
        self.translated_message = ''
        for symbol in self.message:
            # Note: Only symbols in the SYMBOLS string can be encrypted/decrypted.
            if not self.extended_symbol_set:
                symbol = symbol.upper()
                # If we're using the basic alphabet we need to convert to uppercase only
            if symbol in self.SYMBOLS:
                symbolIndex = self.SYMBOLS.find(symbol)

                # Perform encryption/decryption:
                translatedIndex = (
                    eval((str('symbolIndex' + self.opCode + 'self.key'))) % self.symb_size)
                # We construct a string using the variables and the opCode (either a '+' or a '-' and then evaluate it
                # Then perform modular arithmetic to wrap round
                self.translated_message += self.SYMBOLS[translatedIndex]

            else:
                # Append the symbol without encrypting/decrypting:
                self.translated_message += symbol
        return self.translated_message

    def encrypt(self, key=0):
        self.key = key
        self.opCode = '+'
        return self.translate()

    def decrypt(self, key=0):
        self.key = key
        self.opCode = '-'
        return self.translate()

    def brute_force(self):
        for i in range(len(self.SYMBOLS)):
            newtext = self.decrypt(i)
            print(i, '\t', newtext[:80])


text = 'This is my secret message.'
message = Caesar(text, 13, True)
ciphertext = message.encrypt(13)
print(ciphertext)
message2 = Caesar(ciphertext, 13, True)
print(message2.decrypt(13))
message2.brute_force()

# Brute Force
