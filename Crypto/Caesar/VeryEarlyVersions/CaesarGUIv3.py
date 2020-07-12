from tkinter import *
from tkinter import messagebox



def caesar(text,key, mode):
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
    if mode == "decrypt":
        newText = newText.lower()
    return newText


class MyFirstGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("A simple Caesar Cipher encryption / decryption tool")
        self.scrollbar1 = Scrollbar(master)
        self.scrollbar2 = Scrollbar(master)

        master.grid_columnconfigure(2, weight=1) # Allow columns to grow
        self.inputValue=""
        
        self.heading = Label(master, text="This is my first GUI for decypting Caesar Ciphers")
        self.enc_instructions = Label(master, text="PLAINTEXT: Please type, or paste, the text to be encrypted into this box")
        self.dec_instructions = Label(master, text="CIPHERTEXT: Please type, or paste, the text to be decrypted into this box")


        self.key_label = Label(master, text="Enter the Encryption / Decryption key (1-26)")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.key_entry_box = Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=3)


        self.encrypt_button = Button(master, text="Encrypt", command=self.encrypt)
        self.decrypt_button = Button(master, text="Decrypt", command=self.decrypt)
        self.close_button = Button(master, text="Close", command=master.quit)

        self.text_entry_box = Text(master, wrap=WORD, yscrollcommand=self.scrollbar1.set, height=5)
        self.text_output_box = Text(master,wrap=WORD, yscrollcommand=self.scrollbar2.set, height=5)

        #self.text_entry_box.bind('<Key>',self.retrieve_input)


        # LAYOUT
        self.heading.grid(row=0, column=0, sticky=W+E)
        self.enc_instructions.grid(row=1, column=0, sticky=W)
        self.key_label.grid(row=4,column=0, sticky=W)
        self.key_entry_box.grid(row=4, column=1, sticky=W)
        self.encrypt_button.grid(row=4, column=2, sticky=E)
        self.dec_instructions.grid(row=5, column=0, sticky=W)
        self.decrypt_button.grid(row=8, column=2, sticky=E)
        self.close_button.grid(row=9, column=0, sticky=W)
        

        self.scrollbar1.config(command=self.text_entry_box.yview)
        self.scrollbar2.config(command=self.text_output_box.yview)
        self.scrollbar1.grid(column=3, row=3,  sticky=N+S+W)
        self.scrollbar2.grid(column=3, row=7,  sticky=N+S+W)

        self.text_entry_box.grid(row=3, column=0, columnspan=3, sticky=W+E)
        self.text_entry_box.config(yscrollcommand=self.scrollbar1.set)
        self.text_output_box.grid(row=7, column=0, columnspan=3, sticky=W+E)
        self.text_output_box.config(yscrollcommand=self.scrollbar2.set)


    def encrypt(self):
        self.mode = "encrypt"
        self.text = self.text_entry_box.get("1.0","end-1c")
        self.key = self.get_key()
        self.convertedText = caesar(self.text, self.key, self.mode)
        self.text_output_box.delete("1.0", END)
        self.text_output_box.insert(END,self.convertedText)

    def decrypt(self):
        self.mode = "decrypt"
        self.text = self.text_output_box.get("1.0","end-1c")
        self.key = self.get_key()
        self.key = -self.key # Decrypting
        self.convertedText = caesar(self.text, self.key, self.mode)
        self.text_entry_box.delete("1.0", END)
        self.text_entry_box.insert(END,self.convertedText)

    def get_key(self):
        try:
            key = int(self.key_entry_box.get())
    
        except ValueError:
            messagebox.showwarning("Key Length!","Warning! \nYou must enter a decryption key!")
            return False
        
        if key < 0 or key > 26:
            messagebox.showwarning("Key Length!","Warning! \nThe key can only be a number between 1 and 26!")
            key = 0

        return key

        
    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
