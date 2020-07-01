# An application to assist in the encryption and decryption of simple
# monaalphabetic substitution ciphers.

# M. Sansome June 2020
# Version 0.4

#Version History
#===============
# v0.0 Basic tkinter structure constructed
# v0.1 Inclusion of automated break algorithm plus improved alphabet entry events
# v0.2 Addition of copy to keyboard facility
# v0.3 Addition of "Import Key" functionality plus code tidy-up
# v0.4 Inclusion of pattern matching decryption

# ToDo: Implement Threading for automated break task.
# Implement word pattern matching auto break method
# Implement frequency analysis tools

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from random import shuffle
import os, re, copy, wordPatterns, makeWordPatterns
import simpleSubHackerV2 as ss_hack
from CryptanalysisV02 import Cryptanalyse as Crypto # My crypto tools
from break_simplesub_3 import Mono_break as mb # Hill-climbing algorithm adapted from Practical Cryptography

class App(tk.Tk):
    def __init__(self, title="Sample App", *args, **kwargs):
        super().__init__()
        self.title(title)
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.ciphertext =""

        # Create the top (input) frame:
        self.input_frame = tk.LabelFrame(self, text="Ciphertext")
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.rowconfigure(0, weight=1)

        # Create the middle (alphabet) frame:
        self.alphabet_frame = tk.LabelFrame(self, text="The Alphabet")
        self.alphabet_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.alphabet_frame.columnconfigure(0, weight=1)
        self.alphabet_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the middle (tools) frame:
        self.tools_frame = tk.LabelFrame(self, text="Tools")
        self.tools_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.tools_frame.columnconfigure(0, weight=1)
        self.tools_frame.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create the bottom (output) frame:
        self.output_frame = tk.LabelFrame(self, text="Plaintext")
        self.output_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.NSEW)
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        self.rowconfigure([0, 2], minsize=90)  # Set min size for top and bottom
        self.rowconfigure(1, weight=1)  # Row 1 should adjust to window size
        self.columnconfigure(0, weight=1)  # Column 0 should adjust to window size

        # Content for the input frame
        tk.Label(self.input_frame,
                 text="Please type, or paste, the text to be analysed into this box:").grid(row=0, columnspan=3,
                                                                                            sticky=tk.W)
        self.input_box = scrolledtext.ScrolledText(self.input_frame, height=8, wrap=tk.WORD)
        self.input_box.columnconfigure(0, weight=1)
        self.input_box.grid(row=1, column=0, columnspan=5, sticky=tk.NSEW)
        ttk.Button(self.input_frame,
                   text="Load from File",
                   command=self.fileDialog).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Button(self.input_frame,
                   text="Encrypt/Decrypt",
                   command=self.encDec).grid(row=2, column=2, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self.input_frame,
                   text="Pattern Decrypt",
                   command=self.pattern_decrypt).grid(row=2, column=3, padx=5, pady=5, sticky=tk.E)
        ttk.Button(self.input_frame,
                   text="Auto Decrypt",
                   command=self.auto_break).grid(row=2, column=4, padx=5, pady=5, sticky=tk.E)

        # Content for the tools frame
        ttk.Button(self.tools_frame,
                   text="Random Key",
                   command=self.random_alphabet).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(self.tools_frame,
                   text="Copy Key to Clipboard",
                   command=self.copy_key_to_clipboard).grid(row=1, column=0, sticky=tk.W)
        ttk.Button(self.tools_frame,
                   text="Import Key",
                   command=self.create_key_import_window).grid(row=2, column=0, sticky=tk.W)
        ttk.Button(self.tools_frame,
                   text="Reset Key",
                   command=self.make_blank_alphabet).grid(row=3, column=0, sticky=tk.W)

        # Content for the output frame, (one text box only).
        self.output_box = scrolledtext.ScrolledText(self.output_frame, width=40, height=8, wrap=tk.WORD)
        self.output_box.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        ttk.Button(self.output_frame,
                   text="Copy to Clipboard",
                   command=self.copy_output_to_clipboard).grid(row=1, column=0,padx=5, pady=5, sticky=tk.W)

        self.draw_alphabet()
        self.make_blank_alphabet()

    def make_blank_alphabet(self):
        # Fill the dictionary with *'s
        self.alphabet_dict = {}
        for i in range(26):
            self.alphabet_dict[self.alphabet[i]] = "*"
        self.draw_key()

    def make_dict_from_key(self): # Use the method in the Cryptanalysis class
        key = self.key
        self.alphabet_dict = Crypto(self.ciphertext, self.key).make_dictionary_from_key()

    def make_key_from_dict(self):
        # Creates a 26 character string of the key
        # We cant just invert the dictionary, because missing letters would cause an error
        # so we have to find our which letters are missing and add them as * to the key.
        self.output_key = ""
        missing_letters = []
        missing_letter_count = 0
        key_list = list(self.alphabet_dict.keys()) # Create lists of the keys and values
        val_list = list(self.alphabet_dict.values())
        for letter in self.alphabet:
            if letter not in val_list:
                missing_letters.append(letter)
        for i in range(26):
            if val_list[i] not in self.alphabet:
                cletter = "*"
            else:
                cletter = key_list[i]
            self.output_key += cletter

    def inv_key(self):
        # Not currently used
        invkey = [i2a(key.index(i)) for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

    def draw_alphabet(self):
        # This method will run through and create all the labels and entry boxes
        # for the 26 letters of the alphabet in a loop (and store the entry objects in a list)
        self.entries = [] # Empty list to store entry objects
        for i in range(26): # Display each letter and an entry box to enter letter
            tk.Label(self.alphabet_frame,
                        text=self.alphabet[i]
                        ).grid(row=0, column=i, padx=1, pady=1, sticky=tk.W)
            entry = tk.Entry(self.alphabet_frame, width=1, name=f"letter{self.alphabet[i]}")
            #entry.insert(0,self.alphabet_dict[self.alphabet[i]])
            entry.grid(row=1, column=i, padx=1, pady=1, sticky=tk.W)
            entry.bind("<FocusIn>", self.handleIN)
            entry.bind("<Return>",self.handleOut)
            entry.bind("<FocusOut>", self.handleOut)
            entry.bind("<Escape>", self.handle_esc)
            entry.bind("<Delete>", self.handle_del)
            entry.bind("<BackSpace>", self.handle_del)
            self.entries.append(entry) # write the object into the list for later access

    def draw_key(self):
        # Draw the Alphabet from the dictionary
        #print("In Draw Key. Key is:", self.key)
        for i in range(26):
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, self.alphabet_dict[self.alphabet[i]])

    def encDec(self):
        # This method will apply the key to the ciphertext and write the output into the output box
        self.ciphertext = self.input_box.get(0.0, tk.END)
        self.plaintext = ""
        for j in range(len(self.ciphertext)):
            cLetter = self.ciphertext[j].upper()
            if cLetter in self.alphabet:
                pLetter = self.alphabet_dict[cLetter]
                if self.ciphertext[j].islower():
                    pLetter = pLetter.lower()
                self.plaintext += pLetter
            else:
                self.plaintext += self.ciphertext[j] # Skip stuff like punctuation etc.
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)

    def auto_break(self):
        # This will instantiate a Mono_break object from the Mono_break class imported break_simplesub_3
        # and try to perform a hill-climbing algorithm attack on the cipher.
        print("Going to delete")
        self.output_box.delete(0.0, tk.END)
        print("Should have deleted")
        message = "\nThis could take some time. Please be Patient."
        print(message)
        self.output_box.insert(0.0, message)
        self.ciphertext = self.input_box.get(0.0, tk.END)
        self.key = mb(self.ciphertext).bestkey
        print("Bestkey =",self.key)
        #self.initialise_dictionaries()
        self.make_dict_from_key()
        self.draw_key()
        print("Going to Crypto with key:",self.key)
        self.plaintext = Crypto(self.ciphertext, self.key).decipher()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)

    def pattern_decrypt(self):
        self.ciphertext = self.input_box.get(0.0, tk.END)
        letterMapping = ss_hack.hackSimpleSub(self.ciphertext)
        self.key = ss_hack.decryptWithCipherletterMapping(self.ciphertext, letterMapping)
        self.make_dict_from_key()
        self.draw_key()
        self.plaintext = Crypto(self.ciphertext, self.key).decipher()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext)

    def stop(self):
        # Not currently used
        mb.stopped = True

    def copy_to_clipboard(self, output):
        # Main Copy to clipboard method (takes the desired item as a parameter)
        self.clipboard_clear()
        self.clipboard_append(output)
        self.update()  # now it stays on the clipboard after the window is closed

    def copy_key_to_clipboard(self):
        # Copy the key to the clipboard
        self.make_key_from_dict()
        outkey = self.output_key
        self.copy_to_clipboard(outkey)

    def copy_output_to_clipboard(self):
        # Copy the output to the clipboard
        out_txt = self.output_box.get(0.0, tk.END)
        self.copy_to_clipboard(out_txt)

    def import_key(self):
        # Called from the Import Key button on the spawned Import Key window
        self.key = self.key_import_entry.get()
        self.make_dict_from_key()
        self.draw_key()
        self.encDec()
        self.key_import_window.destroy()

    def print_values(self):
        # Will cycle though the letter entry boxes and return their contents
        # (not currently used)
        for entry in self.entries:
            print(entry, entry.get())

    def handleIN(self,event):
        # Method triggered by event when cursor clicked in entry box
        letter = str(event.widget) # Find which letter we're in by referencing the widget name
        self.letterpos = letter[-1] # Get the actual letter by looking at the last character of the widget name
        self.current_letter = self.alphabet_dict[self.letterpos]
        event.widget.delete(0, tk.END)

    def handleOut(self, event):
        # Method triggered by event when cursor clicked out of entry box
        typed = event.widget.get()
        if typed.isalpha() and len(typed)==1:
            typed = typed.upper()
            inverted_dict = {v: k for k, v in self.alphabet_dict.items()} #create an inverted dictioanry to look up position
            if typed in self.alphabet_dict.values() and inverted_dict[typed] != self.letterpos:
                message = f"Careful! You've used {typed} already at {inverted_dict[typed]}!"
                tk.messagebox.showwarning("Warning",message)
                typed = "*"
        elif typed =="":
            typed = self.current_letter
        else:
            typed = "*"
        event.widget.delete(0, tk.END)
        event.widget.insert(0, typed)
        self.alphabet_dict[self.letterpos] = typed
        self.encDec()
        self.output_box.delete(0.0, tk.END)
        self.output_box.insert(0.0, self.plaintext) # Redraw the modified plaintext

    def handle_esc(self, event):
        # Method triggered by event when escape pressed when in entry box
        event.widget.delete(0, tk.END)
        event.widget.insert(0, self.current_letter)

    def handle_del(self, event):
        # Method triggered by event when delete key pressed when in entry box
        event.widget.delete(0, tk.END)
        event.widget.insert(0, "*")
        self.alphabet_dict[self.letterpos] = "*"
        return "break"

    def random_alphabet(self):
        # Will create a random key and draw it into the display
        new_alphabet = list(self.alphabet)
        shuffle(new_alphabet)
        self.key = "".join(new_alphabet)
        self.make_dict_from_key()
        self.draw_key()

    def create_key_import_window(self):
        # New window spawned when "Import Kwy" button is clicked
        self.key_import_window = tk.Toplevel(self)
        self.key_import_window.title("Key Import")
        self.key_import_frame = tk.LabelFrame(self.key_import_window, text="Key Import")
        self.key_import_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
        self.key_import_frame.columnconfigure(0, weight=1)
        self.key_import_frame.rowconfigure(0, weight=1)
        key_import_label = ttk.Label(self.key_import_frame, text="Please type or paste the key \n(as a 26 character string - all uppercase)")
        self.key_import_entry = tk.Entry(self.key_import_frame, width=36)
        key_import_button = ttk.Button(self.key_import_frame, text="Import Key", command=self.import_key)
        key_import_cancel_button = ttk.Button(self.key_import_frame, text="Cancel", command=lambda :self.key_import_window.destroy())
        key_import_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.key_import_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        key_import_button.grid(row=2, column=0, padx=5, pady=5, sticky = tk.W)
        key_import_cancel_button.grid(row=2, column=1, padx=5, pady=5, sticky = tk.E)

    def fileDialog(self):
        # Method which invokes the inport file dialogue
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select A File", filetypes=[
        ("TXT", "*.txt"),
        ("All files", "*")])
        with open(self.filename) as input_file:
            self.input_box.delete(0.0,tk.END)
            self.input_box.insert(0.0, input_file.read())


if __name__ == "__main__":
    App("Simple Substitution Cipher Tool").mainloop()
