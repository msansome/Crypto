from tkinter import *
from tkinter import messagebox



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


class MyFirstGUI:
    
    def __init__(self, master):
        self.master = master
        master.title("A simple Caesar Cipher encryption / decryption tool")
        self.scrollbar1 = Scrollbar(master)
        self.scrollbar2 = Scrollbar(master)

        master.grid_columnconfigure(2, weight=1) # Allow columns to grow
        self.inputValue=""
        
        self.heading = Label(master, text="This is my first GUI for decypting Caesar Ciphers")
        self.instructions = Label(master, text="Please type, or paste, the text to be decrypted into the first box")

        self.key_label = Label(master, text="Enter the Encryption / Decryption key (1-26)")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.key_entry_box = Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=3)

        self.encrypt_button = Button(master, text="Encrypt", command=self.convert)
        self.decrypt_button = Button(master, text="Decrypt", command=self.convert)
        self.close_button = Button(master, text="Close", command=master.quit)

        self.text_entry_box = Text(master, wrap=WORD, yscrollcommand=self.scrollbar1.set, height=5)
        self.text_output_box = Text(master,wrap=WORD, yscrollcommand=self.scrollbar2.set, height=5)

        #self.text_entry_box.bind('<Key>',self.retrieve_input)


        # LAYOUT
        self.heading.grid(row=0, column=0, sticky=W+E)
        self.instructions.grid(row=2, column=0, sticky=W)
        self.key_label.grid(row=4,column=0, sticky=W)
        self.key_entry_box.grid(row=4, column=1, sticky=W)
        self.encrypt_button.grid(row=4, column=2, sticky=E)
        self.decrypt_button.grid(row=7, column=2, sticky=E)
        self.close_button.grid(row=8, column=0, sticky=W)
        

        self.scrollbar1.config(command=self.text_entry_box.yview)
        self.scrollbar2.config(command=self.text_output_box.yview)
        self.scrollbar1.grid(column=3, row=3,  sticky=N+S+W)
        self.scrollbar2.grid(column=3, row=6,  sticky=N+S+W)

        self.text_entry_box.grid(row=3, column=0, columnspan=3, sticky=W+E)
        self.text_entry_box.config(yscrollcommand=self.scrollbar1.set)
        self.text_output_box.grid(row=6, column=0, columnspan=3, sticky=W+E)
        self.text_output_box.config(yscrollcommand=self.scrollbar2.set)

    def convert(self):
        # This will encrypt /decrypt the text (note a negative key will decrypt)
        #mode1 = mode
        self.inputValue=self.text_entry_box.get("1.0","end-1c")
        try:
            key = int(self.key_entry_box.get())
            if mode=="decrypt":
                key = -key
    
        except ValueError:
            messagebox.showwarning("Key Length!","Warning! \nYou must enter a decryption key!")
            return False
        
        if key < 0 or key > 26:
            messagebox.showwarning("Key Length!","Warning! \nThe key can only be a number between 1 and 26!")
            key = 0

        self.convertedText = caesar(self.inputValue, key)
        self.text_output_box.delete("1.0", END)
        self.text_output_box.insert(END,self.convertedText)


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
