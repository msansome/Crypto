#from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk



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
        master.title("Substitution Ciphers")
        self.scrollbar1 = tk.Scrollbar(master)
        self.scrollbar2 = tk.Scrollbar(master)

        for i in range (0,28):
            master.grid_columnconfigure(i, weight=1) # Allow columns to grow

        self.inputValue=""
        
        self.heading = ttk.Label(master, text="Monoalphabetic Substitution Cipher encryption / decryption tool")
        self.enc_instructions = ttk.Label(master, text="PLAINTEXT: Please type, or paste, the text to be encrypted into this box")
        self.dec_instructions = ttk.Label(master, text="CIPHERTEXT: Please type, or paste, the text to be decrypted into this box")

        self.alph_desc_label = ttk.Label(master, text="Cipher\nAlphabet")
        self.A_box_label = ttk.Label(master, text="A")
        self.B_box_label = ttk.Label(master, text="B")
        self.C_box_label = ttk.Label(master, text="C")
        self.D_box_label = ttk.Label(master, text="D")
        self.E_box_label = ttk.Label(master, text="E")
        self.F_box_label = ttk.Label(master, text="F")
        self.G_box_label = ttk.Label(master, text="G")
        self.H_box_label = ttk.Label(master, text="H")
        self.I_box_label = ttk.Label(master, text="I")
        self.J_box_label = ttk.Label(master, text="J")
        self.K_box_label = ttk.Label(master, text="K")
        self.L_box_label = ttk.Label(master, text="L")
        self.M_box_label = ttk.Label(master, text="M")
        self.N_box_label = ttk.Label(master, text="N")
        self.O_box_label = ttk.Label(master, text="O")
        self.P_box_label = ttk.Label(master, text="P")
        self.Q_box_label = ttk.Label(master, text="Q")
        self.R_box_label = ttk.Label(master, text="R")
        self.S_box_label = ttk.Label(master, text="S")
        self.T_box_label = ttk.Label(master, text="T")
        self.U_box_label = ttk.Label(master, text="U")
        self.V_box_label = ttk.Label(master, text="V")
        self.W_box_label = ttk.Label(master, text="W")
        self.X_box_label = ttk.Label(master, text="X")
        self.Y_box_label = ttk.Label(master, text="Y")
        self.Z_box_label = ttk.Label(master, text="Z")

        self.I_box_label.configure(anchor='center')

        letter = ""
        vcmd = master.register(self.validate_L), '%P', '%S', '%W' ,*letter # we have to wrap the command
        self.A_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd), width=1)
        self.B_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.C_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.D_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.E_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.F_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.G_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.H_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.I_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.J_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.K_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.L_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.M_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.N_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.O_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.P_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.Q_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.R_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.S_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.T_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.U_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.V_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.W_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.X_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.Y_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)
        self.Z_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=1)



        self.key_label = ttk.Label(master, text="Enter the Encryption / Decryption key (1-26)")

        vcmd = master.register(self.validate) # we have to wrap the command
        self.key_entry_box = ttk.Entry(master, validate="key", validatecommand=(vcmd, '%P'), width=3)


        self.encrypt_button = ttk.Button(master, text="Encrypt", command=self.encrypt)
        self.decrypt_button = ttk.Button(master, text="Decrypt", command=self.decrypt)
        self.close_button = ttk.Button(master, text="Close", command=master.quit)

        self.text_entry_box = tk.Text(master, wrap='word', yscrollcommand=self.scrollbar1.set, height=5)
        self.text_output_box = tk.Text(master,wrap='word', yscrollcommand=self.scrollbar2.set, height=5)

        #self.text_entry_box.bind('<Key>',self.retrieve_input)


        # LAYOUT
        self.heading.grid(row=0, column=0, columnspan=27, sticky='WE')

        self.alph_desc_label.grid(row=1,column=0, rowspan=2, sticky='WE')
        
        self.A_box_label.grid(row=1,column=2, sticky='we')
        self.B_box_label.grid(row=1,column=3, sticky='we')
        self.C_box_label.grid(row=1,column=4, sticky='we')
        self.D_box_label.grid(row=1,column=5, sticky='we')
        self.E_box_label.grid(row=1,column=6, sticky='we')
        self.F_box_label.grid(row=1,column=7, sticky='we')
        self.G_box_label.grid(row=1,column=8, sticky='we')
        self.H_box_label.grid(row=1,column=9, sticky='we')
        self.I_box_label.grid(row=1,column=10, sticky='we')
        self.J_box_label.grid(row=1,column=11, sticky='we')
        self.K_box_label.grid(row=1,column=12, sticky='we')
        self.L_box_label.grid(row=1,column=13, sticky='we')
        self.M_box_label.grid(row=1,column=14, sticky='we')
        self.N_box_label.grid(row=1,column=15, sticky='we')
        self.O_box_label.grid(row=1,column=16, sticky='we')
        self.P_box_label.grid(row=1,column=17, sticky='we')
        self.Q_box_label.grid(row=1,column=18, sticky='we')
        self.R_box_label.grid(row=1,column=19, sticky='we')
        self.S_box_label.grid(row=1,column=20, sticky='we')
        self.T_box_label.grid(row=1,column=21, sticky='we')
        self.U_box_label.grid(row=1,column=22, sticky='we')
        self.V_box_label.grid(row=1,column=23, sticky='we')
        self.W_box_label.grid(row=1,column=24, sticky='we')
        self.X_box_label.grid(row=1,column=25, sticky='we')
        self.Y_box_label.grid(row=1,column=26, sticky='we')
        self.Z_box_label.grid(row=1,column=27, sticky='we')

        

        self.A_entry_box.grid(row=2,column=2, sticky='we')
        self.B_entry_box.grid(row=2,column=3, sticky='we')
        self.C_entry_box.grid(row=2,column=4, sticky='we')
        self.D_entry_box.grid(row=2,column=5, sticky='we')
        self.E_entry_box.grid(row=2,column=6, sticky='we')
        self.F_entry_box.grid(row=2,column=7, sticky='we')
        self.G_entry_box.grid(row=2,column=8, sticky='we')
        self.H_entry_box.grid(row=2,column=9, sticky='we')
        self.I_entry_box.grid(row=2,column=10, sticky='we')
        self.J_entry_box.grid(row=2,column=11, sticky='we')
        self.K_entry_box.grid(row=2,column=12, sticky='we')
        self.L_entry_box.grid(row=2,column=13, sticky='we')
        self.M_entry_box.grid(row=2,column=14, sticky='we')
        self.N_entry_box.grid(row=2,column=15, sticky='we')
        self.O_entry_box.grid(row=2,column=16, sticky='we')
        self.P_entry_box.grid(row=2,column=17, sticky='we')
        self.Q_entry_box.grid(row=2,column=18, sticky='we')
        self.R_entry_box.grid(row=2,column=19, sticky='we')
        self.S_entry_box.grid(row=2,column=20, sticky='we')
        self.T_entry_box.grid(row=2,column=21, sticky='we')
        self.U_entry_box.grid(row=2,column=22, sticky='we')
        self.V_entry_box.grid(row=2,column=23, sticky='we')
        self.W_entry_box.grid(row=2,column=24, sticky='we')
        self.X_entry_box.grid(row=2,column=25, sticky='we')
        self.Y_entry_box.grid(row=2,column=26, sticky='we')
        self.Z_entry_box.grid(row=2,column=27, sticky='we')
        

        
        self.dec_instructions.grid(row=3, column=0, columnspan=27, sticky='we')
        self.key_label.grid(row=10,column=0, columnspan=14,sticky='we')
        self.key_entry_box.grid(row=10, column=15, columnspan=5, sticky='we')
        self.encrypt_button.grid(row=10, column=22, columnspan=5, sticky='e')
        self.enc_instructions.grid(row=11, column=0, columnspan=27, sticky='we')
        self.decrypt_button.grid(row=16, column=22, columnspan=5, sticky='e')
        self.close_button.grid(row=17, column=0, sticky='we')
        
##
        self.scrollbar1.config(command=self.text_entry_box.yview)
        self.scrollbar2.config(command=self.text_output_box.yview)
        self.scrollbar1.grid(column=27, row=4,  sticky='nsw')
        self.scrollbar2.grid(column=27, row=12,  sticky='nsw')

        self.text_entry_box.grid(row=4, column=0, columnspan=27, sticky='we')
        self.text_entry_box.config(yscrollcommand=self.scrollbar1.set)
##        self.text_output_box.grid(row=7, column=0, columnspan=27, sticky='we')
##        self.text_output_box.config(yscrollcommand=self.scrollbar2.set)
##

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

    def validate_L(self, S, P ,W, *letter):
        self.text.delete("1.0", "end")
        print("Got",S, 'W =',W, "P=",P)
        print(S.isalpha())
        
        if not S.isalpha() or len(S) > 1:
            print('Len S =',len(S))
            return False
        else:
            print('OK - Updating the alphabet with',S)
            if S == "":
                print("S = *")
            return True
                                                                              
##        if not new_letter:  # the field is being cleared
##            self.entered_letter = ""
##            return True
##
##        if not str(new_letter).isalpha() and len(new_letter) == 1:
##            return False
##        else:
##            return True
        
        
    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

root = tk.Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
